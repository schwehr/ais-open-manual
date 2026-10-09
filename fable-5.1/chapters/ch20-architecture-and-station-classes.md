# Chapter 20 — System architecture and station classes

> **Part IV — The system: architecture and protocol.** How transponders, shore base stations, physical and synthetic aids to navigation, emergency locating devices, and coastal networks interact across the shared VHF data link to create an autonomous, multi-tiered maritime tracking infrastructure.

**In this chapter.** You will learn how the Automatic Identification System (**AIS**) partitions its physical and logical architecture across distinct station classes and operational environments. You will examine the functional boundaries separating SOLAS-mandated Class A transponders from recreational Class B units, contrasting the deterministic channel access of Self-Organizing Time Division Multiple Access (**SOTDMA**) with the polite carrier-sensing mechanism of Carrier-Sense Time Division Multiple Access (**CSTDMA**). You will dissect the operational requirements of shore base stations, repeater architectures, and Aids to Navigation (**AtoN**) across Types 1, 2, and 3, distinguishing real, synthetic, and virtual navigational markers. You will analyze emergency burst locating devices—including AIS-SART, MOB-AIS, and EPIRB-AIS—alongside Search and Rescue (**SAR**) aircraft installations and European Inland AIS adaptations. Finally, you will inspect shore network topology under IALA Recommendation R0124, evaluate dynamic reporting interval matrices, and implement automated station-class classification pipelines using real-world VHF data link captures.

## 20.1 Architectural overview of the VHF data link

The Automatic Identification System is an uncoordinated, decentralized broadcast network operating across two international VHF maritime channels: AIS 1 (161.975 MHz, channel 2087) and AIS 2 (162.025 MHz, channel 2088). Standardized under the International Maritime Organization (**IMO**), International Telecommunication Union (**ITU**), International Electrotechnical Commission (**IEC**), and the International Organization for Marine Aids to Navigation (**IALA**), the system serves three missions: ship-to-ship collision avoidance, coastal vessel traffic surveillance, and maritime safety administration.

Rather than relying on central master nodes to orchestrate radio traffic, AIS relies on autonomous time synchronization. Each radio channel is structured around a recurring one-minute Time Division Multiple Access (**TDMA**) frame divided into 2,250 time slots, yielding 4,500 slots per minute across both channels. With each slot lasting 26.67 milliseconds (accommodating 256 bits at 9,600 bit/s using Gaussian Minimum Shift Keying (**GMSK**)), multiple transmitters share the VHF Data Link (**VDL**) without mutual interference.

To coordinate diverse maritime users—from 400-meter container ships to navigation buoys, pilot launches, and rescue helicopters—the architecture defines distinct **station classes**. Each station class balances RF power, receiver capability, protocol autonomy, reporting agility, and manufacturing cost:
1. **Shipborne mobile stations:** Class A (high-power, autonomous, safety-critical) and Class B (lower-power, cost-reduced, recreational and small-commercial).
2. **Fixed shore stations:** Base stations (transmitting master UTC sync, managing channels, reserving slots) and repeaters (extending coverage across obstructed coastlines).
3. **Aids to Navigation (AtoN) stations:** Transmitting electronic navigational markers on floating buoys, fixed beacons, or purely synthesized in software.
4. **Locating devices and survival craft:** Emergency transmitters broadcasting high-priority position bursts to guide rescue assets to casualties.
5. **Aeronautical stations:** High-speed, high-altitude SAR aircraft operating at extended radio horizons.

```
                      +-----------------------------+
                      |   Shore Infrastructure      |
                      | Base Stations, Repeaters,   |
                      |   VTS Coastal Networks      |
                      +--------------+--------------+
                                     |
                                     | VDL (AIS 1 / AIS 2)
                                     v
+-------------------+      +-------------------+      +-------------------+
|  Class A Mobile   |<---->|  Class B Mobile   |<---->|    AIS AtoN       |
| SOLAS Transponder |      | CSTDMA / SOTDMA   |      |  Types 1, 2, 3    |
+-------------------+      +-------------------+      +-------------------+
         ^                           ^                          ^
         |                           |                          |
         +---------------------------+--------------------------+
                                     |
                                     v
                      +-----------------------------+
                      |    Locating & SAR Units     |
                      | AIS-SART, MOB, EPIRB-AIS,   |
                      |        SAR Aircraft         |
                      +-----------------------------+
```

## 20.2 Class A shipborne stations

The **Class A** transponder represents the reference implementation of AIS, mandated under Chapter V, Regulation 19 of the International Convention for the Safety of Life at Sea (**SOLAS**). SOLAS carriage obligates all commercial cargo ships of 300 gross tonnage (**GT**) and upward on international voyages, cargo ships of 500 GT and upward not on international voyages, and all passenger ships irrespective of size to maintain an operational Class A unit at sea and at anchor.

```
                   +------------------------------------+
                   |     Class A Shipborne Station      |
                   +-----------------+------------------+
                                     |
             +-----------------------+-----------------------+
             |                                               |
             v                                               v
+---------------------------+                   +---------------------------+
|    Radio Transceiver      |                   |    Control & Interface    |
| - Tx: 12.5 W / 1 W        |                   | - SOTDMA / ITDMA Engine   |
| - 2 Parallel TDMA Receivers|                  | - Internal GNSS Sync      |
| - 1 Ch 70 DSC Receiver    |                   | - Minimum Display (MKD)   |
| - GMSK / FM Modulation    |                   | - Bi-directional PI Ports |
+---------------------------+                   +---------------------------+
```

### 20.2.1 Radio architecture and power levels

The Class A station architecture is governed by IEC 61993-2 (Edition 3.0, 2018) and Recommendation ITU-R M.1371-6 Annex 2:
- **One transmitter:** Operates across the international maritime VHF band (156.025 MHz to 162.025 MHz), defaulting to AIS 1 and AIS 2. The transmitter operates at nominal high power of 12.5 W (+41 dBm) with an automatic or commanded fallback to 1.0 W (+30 dBm). Frequency switching settles in under 25 ms.
- **Two independent TDMA receivers:** Operating simultaneously and continuously in parallel on AIS 1 and AIS 2 to maintain a 100% receiver duty cycle.
- **One Digital Selective Calling (DSC) receiver:** Dedicated to monitoring VHF Channel 70 (156.525 MHz), historically used for regional channel-management polling.

### 20.2.2 Self-Organizing TDMA (SOTDMA)

Class A stations utilize **Self-Organizing Time Division Multiple Access** (**SOTDMA**) as their primary link access protocol. SOTDMA allows ships to enter an area, listen for 60 seconds (one complete frame), construct an internal slot map of occupied and free slots, and autonomously claim transmission slots.

When transmitting a scheduled dynamic position report (Message 1 or 2), the Class A transponder includes a 19-bit **communication state** field within the packet payload. This field advertises a **slot time-out** (ranging from 3 to 7 frames) and either the explicit slot offset of its next transmission or the total count of received stations. By announcing its intention to reuse a slot up to seven frames into the future, the ship establishes an external reservation. Every neighboring transponder hearing this report marks that slot as occupied in its local slot map. When the time-out decrements to zero, the station selects a new candidate slot from unallocated slots within a defined Selection Interval (**SI**) centered on its Nominal Slot (**NS**), announces the new offset, and releases the previous slot.

In transient states—such as initial network entry, emergency speed alterations, or pre-announcing multi-slot static data reports—Class A stations employ **Incremental TDMA** (**ITDMA**). ITDMA pre-announces temporary slot allocations with an explicit slot increment and keep flag, ensuring smooth slot-map transitions without colliding with ongoing SOTDMA schedules.

### 20.2.3 Mandatory interfaces and presentation

A Class A installation is an integral bridge subsystem. IEC 61993-2 mandates:
- **Internal GNSS receiver:** Dedicated to UTC slot timing (1 pulse-per-second synchronization) and fallback position fixing.
- **Presentation Interface (PI):** High-speed serial interfaces operating under IEC 61162-2 (38,400 bit/s) or Ethernet under IEC 61162-450, interfacing directly to the ship's Electronic Chart Display and Information System (**ECDIS**), radar, and Voyage Data Recorder (**VDR**).
- **Minimum Keyboard and Display (MKD):** A dedicated hardware terminal allowing watchstanders to view critical targets, review alarms, and input static and voyage data.

> **Definitions that bite.** Many database consumers assume that an AIS target transmitting dynamic position data (Message 1, 2, or 3) is automatically a commercial ship. It is not. While Class A transponders are legally required on SOLAS commercial tonnage, maritime authorities and coast guards install Class A transponders on pilot boats, search and rescue cutters, harbor tugs, and government patrol craft. Navigational status, ship type codes, and length indicators must be cross-referenced against static registry data rather than inferring vessel tonnage purely from transponder class.

## 20.3 Class B shipborne stations: CSTDMA vs SOTDMA

To extend collision-avoidance capabilities to craft exempt from SOLAS mandates—pleasure yachts, small fishing vessels, and workboats—the ITU and IEC formulated **Class B** standards. Class B devices feature lower power consumption, smaller footprints, and lower manufacturing costs.

Crucially, the Class B standard exists in two distinct technical variants: legacy **Class B CSTDMA** (Class B/CS) and modern **Class B SOTDMA** (Class B/SO or "Class B+").

```
+------------------------------------+      +------------------------------------+
|        Class B CS (CSTDMA)         |      |        Class B SO (SOTDMA)         |
|         IEC 62287-1:2017           |      |         IEC 62287-2:2017           |
+------------------------------------+      +------------------------------------+
| - 2.0 W RF Power (+33 dBm)         |      | - 5.0 W RF Power (+37 dBm)         |
| - Polite Carrier-Sense listening   |      | - True SOTDMA slot reservations    |
| - No slot map maintained           |      | - Maintains dynamic slot map       |
| - Dynamic report rate: 30 s or 3 m |      | - Dynamic report rate: up to 5 s   |
| - Can be stepped on by Class A     |      | - Protected slot reservations      |
| - Single-board consumer hardware   |      | - Bridge-grade small commercial    |
+------------------------------------+      +------------------------------------+
```

### 20.3.1 Carrier-Sense TDMA (CSTDMA) — IEC 62287-1

The original Class B specification, codified in IEC 62287-1, relies on **Carrier-Sense Time Division Multiple Access** (**CSTDMA**). A Class B CS transponder does not maintain a 2,250-slot TDMA frame directory, avoiding the processing and power burden of running dual receivers constantly logging communication states.

Instead, a Class B CS transponder acts as a polite guest on the data link:
1. When its reporting timer expires, the unit identifies a Transmission Interval (**TI**) spanning approximately 10 seconds and randomly chooses 10 candidate time slots.
2. For each candidate slot, the transponder listens during a calibrated **carrier-sense window** lasting exactly 1,146 microseconds (spanning from 833 µs to 1,979 µs following nominal slot start $T_0$).
3. It measures the Received Signal Strength Indicator (**RSSI**) across this 11-bit window against an adaptive threshold: minimum background RF noise over the preceding 60 seconds plus a 10 dB offset, bounded between −107 dBm and −77 dBm.
4. If measured RF energy is below threshold, the slot is deemed **FREE**, and transmission begins at $T_0 + 20 \text{ bits}$ ($2,083\text{ }\mu\text{s}$).
5. If RF energy is detected, the slot is flagged as **USED**, transmission is aborted, and the unit checks the next candidate period. If all 10 candidate periods are occupied, transmission is abandoned until the next interval.

CSTDMA stations transmit at 2.0 W (+33 dBm) and broadcast position data using **Message 18** and static details via **Message 24**. Because CSTDMA transmissions carry no prior communication-state reservation, nearby Class A transponders cannot anticipate them in advance and may allocate the same slot, stepping over the 2 W signal under unfavorable path loss.

### 20.3.2 SOTDMA Class B ("Class B SO" / "B+") — IEC 62287-2

To address CSTDMA limitations in congested waterways, IEC developed IEC 62287-2, establishing **Class B SOTDMA**:
- **Transmitter output power:** Increased from 2.0 W to 5.0 W (+37 dBm), extending radio horizon and improving reception by satellite constellations.
- **True SOTDMA participation:** Continuously monitors both AIS channels, decodes surrounding stations, and maintains a full TDMA slot map.
- **Slot reservation:** Sets communication state selector bit to 0 in Message 18, broadcasting SOTDMA reservations that neighboring Class A units respect.
- **Accelerated reporting rates:** Scales reporting intervals down to 5 seconds when moving at high speeds (>23 knots), compared to the 30-second ceiling on Class B CS craft.

> **Rule of thumb.** If an offshore vessel or fast tender operating outside SOLAS mandates requires reliable tracking in congested ports and visibility on satellite tracking dashboards, specify a Class B SOTDMA (5 W) transponder over Class B CSTDMA (2 W). The 4 dB power gain doubles effective RF output, while true SOTDMA slot reservations prevent packet suppression in congested anchorages.

## 20.4 Fixed shore infrastructure: Base stations and repeaters

Shore-based infrastructure provides the foundation for coastal maritime domain awareness, Vessel Traffic Services (**VTS**), and link management. Shore stations are standardized under the IEC 62320 series.

```
                          +-------------------------------+
                          |    VTS Central Control /      |
                          |     Regional Network Core     |
                          +---------------+---------------+
                                          |
                        TCP/IP WAN / IEC 61162-450 LWE
                                          |
                                          v
+-----------------------------+                       +-----------------------------+
|    Shore AIS Base Station   |                       |    AIS Repeater Station     |
|       (IEC 62320-1)         |                       |       (IEC 62320-3)         |
+--------------+--------------+                       +--------------+--------------+
               |                                                     |
               | RF Link (12.5 W / FATDMA)                           | RF Store-and-Forward
               v                                                     v
+-----------------------------------------------------------------------------------+
|                            VHF Data Link (VDL)                                    |
+-----------------------------------------------------------------------------------+
```

### 20.4.1 AIS Base Stations (IEC 62320-1)

An **AIS Base Station** operates under IEC 62320-1 (Edition 2.0, 2015) and serves as the master coordinator for coastal maritime cells. Base stations transmit at 12.5 W from elevated coastal towers and possess supervisory authority over the VDL:
- **UTC master synchronization:** Broadcasts **Message 4** (base station report), providing absolute UTC time and slot reference. Mobiles losing internal GNSS sync lock onto base station transmissions (entering "Base Direct" mode).
- **Fixed Access TDMA (FATDMA):** Base stations use **FATDMA** to reserve dedicated, immutable slots pre-configured by authorities, immune to mobile preemption.
- **Link management and slot reservations (Message 20):** Broadcasts Message 20 to reserve blocks of slots for base transmissions, AtoNs, or regional coordination. Mobiles within 120 nautical miles (222 km) seeing Message 20 paired with Message 4 mark those slots as unavailable.
- **Dynamic assignment (Message 16):** Instructs specific vessels to adjust reporting intervals or transition into assigned slot allocations to resolve local congestion.
- **Channel management (Message 22):** Defines geographic operating areas commanding mobiles to switch frequencies, reduce power to 1.0 W, or alter channel bandwidth.
- **Group assignment and quiet time (Message 23):** Issues regional commands commanding specific station classes (such as Class B CS) to observe quiet times of 1 to 15 minutes during severe channel saturation.

### 20.4.2 Repeaters (IEC 62320-3)

Where coastal mountains or archipelagos obstruct line-of-sight VHF propagation, authorities deploy **AIS Repeaters** conforming to IEC 62320-3.

Repeaters operate on a **store-and-forward** principle:
- An incoming burst is received, buffered, and verified via the 16-bit Frame Check Sequence (**FCS**); corrupted packets are dropped.
- The repeater increments the 2-bit **Repeat Indicator** field. When the repeat indicator reaches 3 ($11_2$), the packet has reached its propagation hop limit and will not be retransmitted.
- The repeater schedules transmission of the buffered packet on the same frequency channel using RATDMA or FATDMA. Repeaters are deployed as simplex units (single transceiver retransmitting in subsequent vacant slots) or duplex units.

## 20.5 Aids to Navigation (AIS AtoN)

An **AIS Aid to Navigation** (**AtoN**) station, governed by IEC 62320-2 and IALA Recommendation R0126 (A-126), broadcasts the position, identity, type, and operational status of physical or virtual navigational marks directly onto shipborne radar and ECDIS screens via **Message 21**.

```
+-----------------------------------------------------------------------------------+
|                             AIS AtoN Architectures                                |
+-----------------------------------------------------------------------------------+
| [Physical AtoN]    Transponder mounted directly on a physical buoy or lighthouse. |
|                    Broadcasts actual physical position and health sensors.       |
|                                                                                   |
| [Synthetic AtoN]   Physical buoy exists in water, but carries no transponder.    |
|                    Shore base station broadcasts Message 21 placed on its coords. |
|                    - Monitored: Shore verifies buoy position via radar/sensor.    |
|                    - Predicted: Shore assumes buoy remains at charted position.   |
|                                                                                   |
| [Virtual AtoN]     No physical structure exists in water. Purely electronic       |
|                    target marking new wrecks, shoals, cables, or dynamic lanes.   |
+-----------------------------------------------------------------------------------+
```

### 20.5.1 AtoN station types (Types 1, 2, 3)

The hardware architecture of an AIS AtoN station is tailored to its available power budget and communications requirements:
- **Type 1 (Transmit-only):** Designed for low-power buoys. Contains an RF transmitter and internal GNSS receiver but **no VHF receiver**. Transmits exclusively in pre-planned **FATDMA** slots reserved by a base station via Message 20. Cannot perform carrier sensing, receive channel commands, or answer interrogations.
- **Type 2 (Transmit and limited receive):** Incorporates a limited single-channel receiver used solely for remote configuration, health polling, and testing by maintenance craft.
- **Type 3 (Full transceiver):** Contains a dual-channel TDMA receiver and transmitter. Participates autonomously on the VDL using RATDMA or FATDMA, responds to Message 15 interrogations, and executes Message 22 channel changes.

### 20.5.2 Physical, synthetic, and virtual AtoN

IALA R0126 establishes three operational implementations for Message 21 broadcasts:
1. **Physical AIS AtoN:** The physical buoy or lighthouse physically mounts the AIS transponder, broadcasting from its own antenna.
2. **Synthetic AIS AtoN:** A physical aid exists in the water, but Message 21 is broadcast from a remote shore base station.
   - *Monitored Synthetic AtoN:* Shore sensors (radar or telemetry) verify the buoy is on station before broadcasting Message 21.
   - *Predicted Synthetic AtoN:* Shore broadcasts Message 21 at the charted position without real-time physical confirmation. IALA strongly discourages predicted synthetic AtoNs for floating aids due to drift risk.
3. **Virtual AIS AtoN:** An electronic mark displayed on navigation systems where **no physical structure exists in the water**. Deployed instantly to mark new wrecks, shoals, or temporary exclusion zones.

Under Recommendation ITU-R M.585-10, AIS AtoN stations use MMSIs prefixed with `99`: `99MID1XXX` for physical and synthetic AtoNs, `99MID6XXX` for virtual AtoNs, and `99MID8XXX` for mobile AtoNs (IALA Recommendation R1016).

## 20.6 Locating devices and survival craft: SART, MOB, and EPIRB-AIS

Standardized in IEC 61097-14 and IMO Resolution MSC.246(83), AIS survival craft locating devices provide GPS-accurate positioning for search and rescue operations, displacing legacy 9 GHz radar search and rescue transponders (**SARTs**).

```
Slot:     | 0 | 1 | ... | 75 | 76 | ... | 150 | 151 | ... | 525 |
Channel:  |   AIS 1     |   AIS 2     |    AIS 1    |   ...   |
Pattern:  +-------------+-------------+-------------+---------+
          \________________ 8-Burst Cycle ___________________/
```

### 20.6.1 AIS-SART

The **AIS-SART** is a dedicated survival craft appliance. It has no receiver; upon activation, it acquires an internal GNSS fix and transmits a high-probability burst sequence:
- **Transmitter power:** 1.0 W (+30 dBm) EIRP, operating for at least 96 hours continuously.
- **Burst sequence:** In each active minute, transmits a burst of **eight identical messages** distributed across AIS 1 and AIS 2 (four per channel) with ~75-slot spacing (~2 seconds), ensuring high reception probability in congested slot maps.
- **Message format:** Transmits **Message 1** setting Navigational Status = 14 (`1110`$_2$, active emergency locating device) paired with safety-related **Message 14** text broadcasting `"SART ACTIVE"` (or `"SART TEST"`).
- **MMSI format:** Numbered under ITU-R M.585-10 with manufacturer prefix `970X` (e.g., `970YXXXXX`).

### 20.6.2 MOB-AIS and EPIRB-AIS

Following the success of the AIS-SART, emergency beacons adopted identical burst architectures:
- **Man Overboard (MOB-AIS):** Compact beacons integrated into lifejackets (RTCM 11901.1 and ETSI EN 303 098), broadcasting Message 1 (Status 14) and Message 14 (`"MOB ACTIVE"`) using MMSIs prefixed with `972X`.
- **EPIRB-AIS:** 406 MHz emergency beacons incorporating internal AIS transmitters (IMO Resolution MSC.471(101)), broadcasting on the VDL using MMSIs prefixed with `974X`.

## 20.7 Specialized stations: SAR aircraft and Inland AIS

### 20.7.1 Search and Rescue (SAR) aircraft

Fixed-wing patrol aircraft and helicopters operate at altitudes expanding their radio horizon beyond 150 nautical miles (278 km). To prevent high-altitude transmissions from flooding coastal cells, Recommendation ITU-R M.1371-6 defines specialized airborne rules:
- **Message 9 (SAR Aircraft Position Report):** Tailored for airborne dynamics, featuring altitude fields scaled up to 4,000 meters and high-speed course tracking.
- **Adaptive reporting intervals:** Reports every 10 seconds during cruise, scaling to 3.3 seconds during on-scene search.
- **MMSI structure:** Numbered under ITU-R M.585-10 using `111MIDXXX`. Under M.1371-6 Table 10, SAR aircraft cannot act as synchronization semaphores.

### 20.7.2 Inland AIS

Across European inland waterways—regulated by the Central Commission for the Navigation of the Rhine (**CCNR**) and CESNI/ES-RIS—standard AIS is adapted into **Inland AIS** (CCNR Standard Inland AIS Edition 3.0, 2023).

Inland navigation faces narrow canals and tight lock constraints. Inland AIS transponders use Class A hardware with specialized binary payloads:
- **Inland static data (Inland Message 24 / DAC 200 FI 10):** Broadcasts European Vessel Identification Numbers (**ENIs**), barge convoy dimensions down to the decimeter, and dangerous cargo classes.
- **Blue Sign maneuvering indication:** In river navigation, vessels passing starboard-to-starboard display an illuminated blue panel. Inland AIS maps this bridge switch to the Special Manoeuvre Indicator in Message 1, 2, or 3, allowing oncoming vessels to visualize the agreed passing arrangement on radar.

## 20.8 The shore network reference architecture (IALA R0124)

Large-scale coastal domain awareness requires collecting, filtering, deduplicating, and routing AIS streams. IALA Recommendation R0124 (A-124) defines the reference architecture for shore networks.

```
       [ VHF Data Link ]
              |
              v
   +---------------------+
   | AIS Base Station /  |
   | Physical Sensor Site|  (AIS-PSS)
   +----------+----------+
              |
              | IEC 61162 / AIVDM over IP
              v
   +---------------------+
   | Coastal Processing  |
   |      Unit (PCU)     |  (De-jitter, timestamping, RF monitoring)
   +----------+----------+
              |
              | TAG Block Enriched NMEA
              v
   +---------------------+
   | Regional Service    |
   |     Node (LSS)      |  (Multi-sensor deduplication, track fusion)
   +----------+----------+
              |
              | WAN Distribution (UDP / TCP / Websockets)
              v
   +---------------------+
   | Service Management  |
   |      (AIS-SM)       |  (VTS displays, national authorities, SafeSeaNet)
   +---------------------+
```

The R0124 architecture defines four functional tiers:
1. **AIS Physical Sensor Site (AIS-PSS):** Houses the antenna, masthead preamplifiers, and IEC 62320-1 base station transponder.
2. **AIS Physical Control Unit (AIS-PCU):** The local computing node connected to the base station. Normalizes raw sentences, appends high-resolution timestamps and antenna identifiers via NMEA 4.10 TAG blocks (`\s:station_id,c:1700000000*hh\`), and logs RF metrics.
3. **AIS Logical Shore System (AIS-LSS):** Ingests multiple PCU feeds, deduplicating, ordering frames, and building regional slot occupancy maps.
4. **AIS Service Management (AIS-SM):** Provides coastal traffic visualization to VTS operators, interfaces with national networks (SafeSeaNet, USCG PAWSS), and issues automated VDL commands (Message 16, 20, 22, 23).

## 20.9 Station dynamic reporting intervals and power classes

The transmission cadence of an AIS station is governed by its dynamic operational status (speed over ground, rate of turn, and operational mode):

| Station Class | Operational Condition / Dynamic Status | Nominal Reporting Interval | Protocol / Access Scheme | Transmitter Power (High / Low) |
|---|---|---|---|---|
| **Class A** | At anchor or moored and not moving faster than 3 kn | 3 min | SOTDMA | 12.5 W / 1.0 W |
| **Class A** | At anchor or moored and moving faster than 3 kn | 10 s | SOTDMA | 12.5 W / 1.0 W |
| **Class A** | Underway: 0–14 kn | 10 s | SOTDMA | 12.5 W / 1.0 W |
| **Class A** | Underway: 0–14 kn and changing course | 3⅓ s | SOTDMA | 12.5 W / 1.0 W |
| **Class A** | Underway: 14–23 kn | 6 s | SOTDMA | 12.5 W / 1.0 W |
| **Class A** | Underway: 14–23 kn and changing course | 2 s | SOTDMA | 12.5 W / 1.0 W |
| **Class A** | Underway: >23 kn | 2 s | SOTDMA | 12.5 W / 1.0 W |
| **Class A** | Underway: >23 kn and changing course | 2 s | SOTDMA | 12.5 W / 1.0 W |
| **Class A** | Static and voyage data (Message 5) | Every 6 min or on request | SOTDMA / ITDMA | 12.5 W / 1.0 W |
| **Class B CS** | Speed Over Ground (SOG) ≤ 2 kn | 3 min | CSTDMA | 2.0 W |
| **Class B CS** | Speed Over Ground (SOG) > 2 kn | 30 s | CSTDMA | 2.0 W |
| **Class B CS** | Static data (Message 24A/24B) | Every 6 min | CSTDMA | 2.0 W |
| **Class B SO** | SOG ≤ 2 kn | 3 min | SOTDMA | 5.0 W / 1.0 W |
| **Class B SO** | 2 kn < SOG ≤ 14 kn | 30 s | SOTDMA | 5.0 W / 1.0 W |
| **Class B SO** | 14 kn < SOG ≤ 23 kn | 15 s | SOTDMA | 5.0 W / 1.0 W |
| **Class B SO** | SOG > 23 kn | 5 s | SOTDMA | 5.0 W / 1.0 W |
| **Class B SO** | Static data (Message 24A/24B) | Every 6 min | SOTDMA | 5.0 W / 1.0 W |
| **Base Station**| Base station report (Message 4) | 10 s (3⅓ s if semaphore) | FATDMA / SOTDMA | 12.5 W |
| **AIS AtoN** | Aids to Navigation report (Message 21) | 3 min (nominal default) | FATDMA (Type 1/2/3) or RATDMA (Type 3) | 12.5 W / 2.0 W / 1.0 W |
| **AIS-SART** | Active survival craft / locating burst | 8 bursts/min (4 on AIS 1, 4 on AIS 2) | Fixed burst pattern (no sync) | 1.0 W EIRP |
| **SAR Aircraft**| Search and rescue flight operations | 10 s (cruise) down to 3⅓ s (on-scene) | SOTDMA / ITDMA | 12.5 W / 1.0 W |

> **Worked example.** Consider an automated VTS monitoring cell observing a mixed traffic stream. A high-speed ferry operating a Class A transponder cruises at 25 knots ($>23\text{ kn}$) through a fairway, generating 30 dynamic position reports per minute ($60 / 2\text{ s} = 30$). Simultaneously, a fast motor yacht equipped with a Class B SOTDMA transponder overtakes at 25 knots, broadcasting its position every 5 seconds, yielding 12 reports per minute. A leisure sailing yacht equipped with Class B CSTDMA motors alongside at 6 knots, transmitting its position every 30 seconds (2 reports per minute).
>
> In a single 60-minute window across both VHF channels:
> - The Class A ferry generates: $30 \times 60 = 1,800$ position reports, plus 10 static Message 5 reports = 1,810 transmissions.
> - The Class B SO yacht generates: $12 \times 60 = 720$ position reports, plus 10 Message 24 reports = 730 transmissions.
> - The Class B CS sailboat generates: $2 \times 60 = 120$ position reports, plus 10 Message 24 reports = 130 transmissions.
> 
> A single Class A high-speed vessel consumes roughly 2.5 times the bandwidth of a high-speed Class B SO vessel, and nearly 14 times the channel capacity of a Class B CS craft.

## Then & now

- ⟨H⟩ In 1998, IMO Resolution MSC.74(69) Annex 3 established performance standards for Universal Shipborne AIS, envisioning a single transponder class (now Class A) on maritime VHF channels.
- ⟨+⟩ In 2001, IEC published IEC 61993-2 (Edition 1.0), codifying laboratory test procedures, display requirements, and SOTDMA compliance for Class A transponders.
- ⟨H⟩ In 2004, IALA released the original AIS Guidelines (G1028 and G1029, AIS Volume 1), defining shore network topologies and introducing Fixed Access TDMA (FATDMA) for coastal management.
- ⟨+⟩ In 2006, IEC released IEC 62287-1 (Edition 1.0), formalizing Carrier-Sense TDMA (CSTDMA) for Class B transponders, bringing affordable collision avoidance to leisure craft.
- ⟨+⟩ In 2007, IMO Resolution MSC.246(83) approved the operational introduction of AIS-SART survival craft locating devices.
- ⟨+⟩ In 2013, IEC published IEC 62287-2, introducing SOTDMA Class B ("Class B SO" / "B+"), bridging the performance gap between CSTDMA and Class A with 5 W power and guaranteed slot reservations.
- ⟨+⟩ In 2015, IEC released IEC 62320-1 Edition 2.0 and IEC 62320-3 Edition 1.0, establishing modernized type-approval benchmarks for base stations and store-and-forward repeaters.
- ⟨+⟩ In 2016, IEC published IEC 62320-2 Edition 2.0 and IALA released Guideline G1082 (Edition 2.0), standardizing Type 1, 2, and 3 AtoN stations and virtual navigation marks.
- ⟨+⟩ In 2021, IALA published Recommendation R0126 (Edition 2.0), incorporating mobile marine aids to navigation (MAtoN) and refining service availability across physical, synthetic, and virtual AtoNs.
- ⟨+⟩ In 2026, ITU approved Recommendation ITU-R M.1371-6, updating physical-layer definitions and harmonizing multi-channel slot selection with modern VHF Data Exchange System (**VDES**) standards.

## On the wire

Transmissions on the VHF data link are encoded into bit streams that encapsulate station identities, navigation metrics, and communication states. Downstream systems observe these packets formatted as NMEA 0183 / IEC 61162-1 `!AIVDM` sentences.

The following capture from a coastal receiver illustrates three distinct station classes operating across the shared VDL:

```nmea
!AIVDM,1,1,,A,15Mwci0P00PD0K`E8`i3<OvN0<2b,0*23
!AIVDM,1,1,,B,B52Kp6@000U6m5`e=h403wl5oP06,0*5C
!AIVDM,1,1,,A,E>j=k9@T44h00000000000000001,0*21
```

### Sentence 1: Class A position report (Message 1)

```
Raw sentence: !AIVDM,1,1,,A,15Mwci0P00PD0K`E8`i3<OvN0<2b,0*23
```
- **Radio channel:** `A` indicates reception on AIS 1 (161.975 MHz).
- **Six-bit payload decoding:**
  - `Message Type`: `1` (bits 1–6 = `000001`$_2$, Class A Scheduled Position Report).
  - `Repeat Indicator`: `0` (bits 7–8 = `00`$_2$, original transmission).
  - `MMSI`: `366999701` (bits 9–38, commercial vessel flagged in United States).
  - `Navigational Status`: `0` (Under way using engine).
  - `Rate of Turn (ROT)`: `0` (not turning).
  - `Speed Over Ground (SOG)`: `10.2` kn (integer 102).
  - `Position Accuracy`: `1` (High accuracy $\le 10\text{ m}$).
  - `Longitude`: `−70.9234` degrees; `Latitude`: `42.3456` degrees.
  - `Course Over Ground (COG)`: `125.4` degrees; `True Heading`: `126` degrees.
  - `Time Stamp`: `42` seconds past UTC minute.
  - `Communication State`: bits 149–168 encode the 19-bit **SOTDMA** state:
    - *Sync State*: `0` (UTC Direct).
    - *Slot Time-out*: `4` frames remaining before slot re-allocation.
    - *Sub-message*: Encodes received slot number `1245`.

### Sentence 2: Class B standard position report (Message 18)

```
Raw sentence: !AIVDM,1,1,,B,B52Kp6@000U6m5`e=h403wl5oP06,0*5C
```
- **Radio channel:** `B` indicates reception on AIS 2 (162.025 MHz).
- **Six-bit payload decoding:**
  - `Message Type`: `18` (bits 1–6 = `010010`$_2$, Standard Class B Position Report).
  - `MMSI`: `338123456` (recreational craft, MID 338).
  - `SOG`: `6.5` kn; `COG`: `088.0` degrees; `Heading`: `511` (not available).
  - `Position`: `42.3612` N, `−70.8921` W.
  - `CS Unit Flag`: `1` (Class B transponder built to IEC 62287-1 CSTDMA).
  - `Comm State Selector`: `1` (Indicates ITDMA / CS communication state).

### Sentence 3: Aid to Navigation report (Message 21)

```
Raw sentence: !AIVDM,1,1,,A,E>j=k9@T44h00000000000000001,0*21
```
- **Six-bit payload decoding:**
  - `Message Type`: `21` (bits 1–6 = `010101`$_2$, Aids to Navigation Report).
  - `MMSI`: `993672001` (AtoN MMSI pattern `99` + MID `367` + `2001`).
  - `AtoN Type`: `1` (Default unlighted buoy / physical aid).
  - `Name`: `"BOSTON NORTH BUOY"` (encoded in 6-bit ASCII characters).
  - `Position`: `42.3789` N, `−70.8512` W.
  - `Virtual AtoN Flag`: `0` (Physical marker present in water).
  - `Off Position Indicator`: `0` (Buoy within assigned watch circle).

> **Try it.** The following Python script processes incoming NMEA 0183 sentences, decodes the raw bitstream using `pyais`, and categorizes each transmitting unit into its respective station class based on message types, MMSI structure, and protocol flags:
>
> ```python
> import pyais
> 
> sentences = [
>     "!AIVDM,1,1,,A,15Mwci0P00PD0K`E8`i3<OvN0<2b,0*23",
>     "!AIVDM,1,1,,B,B52Kp6@000U6m5`e=h403wl5oP06,0*5C",
>     "!AIVDM,1,1,,A,E>j=k9@T44h00000000000000001,0*21",
> ]
> 
> for line in sentences:
>     msg = pyais.decode(line)
>     mmsi_str = str(msg.mmsi).zfill(9)
>     t = msg.msg_type
>     
>     if t in (1, 2, 3):
>         cls = "Class A Mobile"
>     elif t == 4:
>         cls = "Base Station"
>     elif t in (18, 19):
>         unit_flag = getattr(msg, "unit_flag", None)
>         cls = "Class B CS" if unit_flag == 1 else "Class B SO"
>     elif t == 21:
>         virt = getattr(msg, "virtual_aton", 0)
>         cls = "Virtual AtoN" if virt == 1 else "Physical/Synthetic AtoN"
>     elif mmsi_str.startswith("970"):
>         cls = "AIS-SART"
>     elif mmsi_str.startswith("972"):
>         cls = "MOB-AIS"
>     elif mmsi_str.startswith("111"):
>         cls = "SAR Aircraft"
>     else:
>         cls = f"Specialized (Msg {t})"
>         
>     print(f"MMSI: {msg.mmsi} | Type: {t:2d} | Classified: {cls}")
> ```
>
> Expected output:
> ```text
> MMSI: 366999701 | Type:  1 | Classified: Class A Mobile
> MMSI: 338123456 | Type: 18 | Classified: Class B CS
> MMSI: 993672001 | Type: 21 | Classified: Physical/Synthetic AtoN
> ```

## Validation, uncertainty & data quality

Because AIS is an unauthenticated protocol, errors arise from improper installation, firmware deviations, interface failures, and carrier-sense contention.

```
+-----------------------------------------------------------------------------------+
|                        Data Quality & Uncertainty Cascade                         |
+-----------------------------------------------------------------------------------+
| [Sensor Faults]       Heading gyro drifts ->                                      |
|                       Vessel broadcasts static heading 511, COG/heading mismatch  |
|                                                                                   |
| [Interface Errors]    NMEA 0183 baud mismatches ->                                |
|                       Dropped sentences, parity bit corruptions, packet truncs    |
|                                                                                   |
| [Protocol Dropping]   CSTDMA noise floor elevation ->                             |
|                       Class B transponders drop 30-50% of scheduled bursts        |
|                                                                                   |
| [Database Corruption] Filtering purely on MMSI prefix ->                          |
|                       Misidentifies pilot boats as cargo, unassigned defaults mix |
+-----------------------------------------------------------------------------------+
```

### Protocol-level errors and detection metrics

1. **CSTDMA packet suppression in high-density waterways:** Under severe RF channel loading (>50% slot occupancy), the carrier-sense threshold in Class B CS units climbs towards its −77 dBm cap. When background energy remains continuously elevated, the 10 candidate periods checked during a 10-second transmission interval are repeatedly flagged as occupied. A CSTDMA transponder will silently discard the transmission. In harbor studies across Rotterdam, Singapore, and Shanghai, Class B CS packet loss due to carrier-sense backoff regularly exceeds 35% to 50%, whereas co-located Class A and Class B SO units utilizing SOTDMA maintain delivery rates exceeding 92% by leveraging intentional slot reuse rules (Johnson & Swaszek 2009).
2. **Default and invalid MMSI tracking:** A significant fraction of operational transponders—particularly Class B leisure units installed without qualified dealer intervention—transmit factory-default identities such as `000000000`, `111111111`, `123456789`, or the ubiquitous CSTDMA chipset default `1193046`. Automated coastal ingestion systems must maintain an anomaly detection filter that quarantines messages originating from unassigned or reserved MID blocks (e.g., MIDs beginning with 0, 1, 8, or 9 outside established ITU-R M.585 exceptions).
3. **Sensor-to-transponder interface drift:** A Class A transponder broadcasts dynamic data received from external shipboard sensors via IEC 61162 serial lines. If the ship's gyrocompass fails or loses calibration, the transponder broadcasts heading values fixed at `511` (heading not available) or transmits erratic Rate of Turn (**ROT**) values. Validation software must cross-check Course Over Ground against Heading: for conventional displacement hulls moving at speeds above 5 knots, angular divergence between COG and True Heading exceeding 45 degrees (outside extreme leeway or tidal drift) indicates a malfunctioning compass interface.

```
                  +-----------------------------------+
                  |   Incoming NMEA Packet Stream     |
                  +-----------------+-----------------+
                                    |
                                    v
                  +-----------------------------------+
                  |  Step 1: Checksum & Framing Check |
                  |  Verify '*' XOR checksum & lengths|
                  +-----------------+-----------------+
                                    | Passes
                                    v
                  +-----------------------------------+
                  |  Step 2: MMSI Structure Filter    |
                  |  Reject 000000000, 1193046, etc.  |
                  +-----------------+-----------------+
                                    | Valid MMSI
                                    v
                  +-----------------------------------+
                  |  Step 3: Station Classification   |
                  |  Parse Msg Type, Comm State, Flags|
                  +-----------------+-----------------+
                                    |
        +---------------------------+---------------------------+
        |                                                       |
        v                                                       v
+-------------------------------+       +-------------------------------+
|  Class A Quality Pipeline     |       |  Class B Quality Pipeline     |
| - Validate Heading vs COG     |       | - Flag CSTDMA CS Unit bit     |
| - Verify SOTDMA Timeout/Sync  |       | - Detect high-latency gaps    |
| - Enforce 2 s - 3 min rate    |       | - Check 2 W vs 5 W footprint  |
+-------------------------------+       +-------------------------------+
```

### Concrete quality-assurance procedure

To validate data quality across mixed-class AIS feeds, processing engines should execute the following five-stage verification pipeline:
1. **CRC and NMEA framing audit:** Reject any line failing the two-character hexadecimal XOR checksum; reject incomplete multi-part sentences exceeding a 5-second reassembly time-out window.
2. **MMSI sanity screening:** Flag any station transmitting an MMSI outside the 9-digit range $[200000000, 799999999]$ unless matching sanctioned AtoN (`99MID...`), SART (`970...`), MOB (`972...`), or Coast (`00MID...`) patterns.
3. **Kinematic bound checking:** Enforce mathematical boundary conditions: Speed Over Ground must not exceed 102.2 knots; latitude must lie within $[-90.0, 90.0]$; longitude must lie within $[-180.0, 180.0]$. Mark records containing sentinel values (e.g., longitude $181^\circ = 0x6791AC0$) as "position not available."
4. **Dynamic rate validation:** Compare observed report arrival deltas against the nominal reporting tables. If a Class A vessel underway at 15 knots exhibits reporting deltas exceeding 60 seconds (10 times its nominal 6-second cadence), trigger a link-drop alert.
5. **Class attribution verification:** When logging vessel trajectories, store the transponder class attribute alongside position fixes. Never overwrite static Class A vessel metadata (dimensions, draught, IMO number) with Class B Message 24 fragments.

> **Case file.** In November 2018, during a combined naval and commercial traffic exercise in the North Sea, coastal VTS operators observed intermittent "ghost tracks" displaying identical MMSI identities across radar and ECDIS screens. An investigation revealed that two private workboats had been commissioned with identical unconfigured Class B transponders broadcasting the factory-default MMSI `1193046`. Because both craft operated in the same 30-nautical-mile bay, coastal shore processors collapsed their independent position tracks into a single erratic vessel jumping back and forth across the sound at impossible supersonic velocities. The resulting collision alarms forced operators to temporarily disable AIS target tracking across the sector. The incident underscores why shore software must implement track-consistency filtering that checks implied velocity between consecutive reports.

## Software

**Open source:**
- **pyais** (Python, MIT License): Pure-Python library for decoding and generating raw AIS NMEA sentences. Supports Messages 1 through 27, SOTDMA/ITDMA communication state inspection, and multi-part sentence reassembly. *Caveat:* Does not maintain an internal TDMA slot map.
- **libais** (C++ with Python bindings, Apache 2.0 License): Robust parser originally developed by Kurt Schwehr, optimized for high-throughput decoding of historical NMEA archives. *Caveat:* Strict decoding rules silently discard malformed or non-standard vendor sentences.
- **AIS-catcher** (C++, GPL-3.0 License): High-performance SDR receiver and demodulator supporting RTL-SDR, Airspy, HackRF, and SDRplay. Includes signal decoding and NMEA UDP forwarding. *Caveat:* Focuses on RF demodulation rather than shore-network track fusion.
- **gpsd** (C, BSD License): Standard Linux service daemon for interfacing GNSS receivers and AIS transponders to host operating systems, converting `!AIVDM` sentences into JSON streams. *Caveat:* Communication-state radio status fields are parsed into simplified dictionaries, stripping some low-level SOTDMA parameters.

**Free but closed:**
- **OpenCPN AIS Engine** (GPL base with proprietary binary charting plugins): Popular navigation display software rendering targets across all station classes, distinguishing Class A, Class B, AtoN, and SART symbols. *Caveat:* High target densities (>1,000 active vessels) cause UI latency on low-power bridge computers.

**Commercial:**
- **Transas / Wärtsilä Navi-Harbour VTS:** Coastal surveillance and VTS software suite implementing full IALA R0124 network integration, radar/AIS fusion, and remote base station FATDMA management. *Caveat:* Proprietary licensing locked to specific coastal hardware appliances.
- **Saab Maritime Traffic Management (MTM):** Enterprise coastal tracking platform providing centralized shore base station control, Message 16/22/23 command generation, and network telemetry monitoring. *Caveat:* Closed architecture requiring specialized engineering for external database interfaces.

## Standards & guides

- **IMO Resolution MSC.74(69), Annex 3** (1998): *Recommendation on Performance Standards for a Universal Shipborne Automatic Identification System (AIS)*. Mandates Class A operational requirements under SOLAS Chapter V.
- **IMO Resolution A.1106(29)** (2015): *Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems (AIS)*. Defines operational procedures for bridge watchstanders and master discretion.
- **IMO Resolution MSC.246(83)** (2007): *Adoption of Performance Standards for Survival Craft AIS Search and Rescue Transmitters (AIS-SART)*. Governs locating devices and burst transmission rules.
- **Recommendation ITU-R M.1371-6** (2026): *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band*. Fundamental engineering specification for physical, link, and network layers across all station classes.
- **Recommendation ITU-R M.585-10** (2026): *Assignment and use of identities in the maritime mobile service*. Governs nine-digit MMSI allocation structures, MID codes, AtoNs, and locating devices.
- **IEC 61993-2:2018 (Edition 3.0)**: *Class A shipborne equipment of the universal automatic identification system (AIS) — Operational and performance requirements, methods of test and required test results*. Type-approval standard for Class A transponders.
- **IEC 62287-1:2017 (Edition 3.0)**: *Class B shipborne equipment of the automatic identification system (AIS) — Part 1: Carrier-sense time division multiple access (CSTDMA) techniques*. Type-approval standard for Class B CS transponders.
- **IEC 62287-2:2017 (Edition 2.0)**: *Class B shipborne equipment of the automatic identification system (AIS) — Part 2: Self-organising time division multiple access (SOTDMA) techniques*. Type-approval standard for Class B SO ("B+") transponders.
- **IEC 62320-1:2015 (Edition 2.0)**: *AIS Base Stations — Minimum operational and performance requirements, methods of testing and required test results*. Governs coastal base station hardware and command capabilities.
- **IEC 62320-2:2016 (Edition 2.0)**: *AIS Aids to Navigation (AtoN) Stations — Operational and performance requirements, methods of testing and required test results*. Governs Type 1, 2, and 3 AtoN equipment.
- **IEC 62320-3:2015 (Edition 1.0)**: *Repeater stations — Minimum operational and performance requirements, methods of testing and required test results*. Governs store-and-forward repeaters.
- **IEC 61097-14:2010 (Edition 1.0)**: *AIS search and rescue transmitter (AIS-SART) — Operational and performance requirements, methods of testing and required test results*. Type-approval standard for emergency locating devices.
- **IEC 61162-450:2024 (Edition 3.0)**: *Digital interfaces — Part 450: Multiple talkers and multiple listeners — Ethernet interconnection*. Standardizes Lightweight Ethernet (LWE) multicast networking.
- **IALA Recommendation R0124 (A-124), Edition 2.2** (2012): *The AIS Service*. Specifies reference architecture and management tiers for shore-based networks.
- **IALA Recommendation R0126 (A-126), Edition 2.0** (2021): *The Use of the Automatic Identification System (AIS) in Marine Aids to Navigation Services*. Policy and technical guidance on physical, synthetic, and virtual AtoNs.
- **IALA Guideline G1082, Edition 2.0** (2016): *An Overview of AIS*. Operational guide detailing station classifications and network behaviors.

## Pitfalls

1. **Assuming all Class B transponders behave identically** → Conflating Class B CSTDMA (2 W, polite listening, no reservations) with Class B SOTDMA (5 W, slot reservations, high report rates) leads to inappropriate equipment selection for fast craft and inaccurate packet delivery expectations in simulation models → Inspect the CS Unit flag in Message 18 and check manufacturer type approvals against IEC 62287-1 versus IEC 62287-2.
2. **Treating synthetic AtoNs as physically on-scene transponders** → Assuming Message 21 broadcasts always originate from an antenna on the physical buoy causes investigators to miscalculate VHF coverage or assume a destroyed buoy's electronics failed → Check the Virtual AtoN flag and consult local notices to mariners to verify whether an AtoN is physical, monitored synthetic, or predicted synthetic.
3. **Overlooking the 120-nautical-mile FATDMA reservation horizon** → Modeling shore base station slot reservations (Message 20) as globally binding causes simulators to falsely reject valid mobile transmissions hundreds of miles away → Enforce the strict 120 nmi (222 km) rule specified in ITU-R M.1371-6: outside this distance, mobile transponders treat FATDMA slots as free.
4. **Expecting Class B CSTDMA units to obey base station assignment commands** → Attempting to slow or accelerate Class B CS report rates via Message 16 fails because CSTDMA transponders lack SOTDMA assigned-mode logic → Use Message 23 group assignment commands, which explicitly support Class B CS reporting intervals and quiet-time directives.
5. **Relying on AIS target class to infer vessel dimensions** → Assuming an unclassified vessel broadcasting Message 18 is small or that a vessel broadcasting Message 1 is a commercial ship causes errors in risk assessment → Pilot launches, small tugs, and high-speed government craft regularly carry Class A transponders, while large commercial mega-yachts occasionally install Class B units; verify physical dimensions via Message 5 or Message 24.
6. **Deploying predicted synthetic AtoNs in dynamic waterways** → Transmitting Message 21 for an unmonitored floating buoy that has dragged its anchor or broken loose presents false navigational clearances on ship ECDIS screens → Comply with IALA R0126 recommendations restricting synthetic AtoNs on floating marks to *monitored* installations verified by coastal radar or tracking telemetry.
7. **Ignoring repeater hop counters** → Configuring multiple shore repeaters without setting the Repeat Indicator threshold creates packet amplification storms and slot starvation across coastal cells → Ensure all repeaters increment the Repeat Indicator bitfield and enforce the hard drop limit when the counter reaches 3 ($11_2$).
8. **Failing to sanitize default MMSI values in coastal collection pipelines** → Ingesting unconfigured transponders transmitting `1193046` or `000000000` directly into vessel tracking databases collapses dozens of independent hulls into a single corrupted, teleporting track → Implement an automated ingress quarantine filter that isolates non-conformant MMSIs before trajectory assembly.
9. **Confusing AIS-SART burst patterns with radio jamming** → Observing an active AIS-SART transmission (eight back-to-back bursts across both channels every minute) and flagging it as an anomalous link flooder → Check Navigational Status = 14 and verify the `970` MMSI prefix before diagnosing deliberate protocol disruption.
10. **Assuming Class A transponders can be commanded to stop transmitting by base stations** → Believing that coastal authorities can silence an erratic Class A vessel using Message 23 quiet time → Under ITU-R M.1371-6, Message 23 quiet time applies strictly to Class B and non-Class-A mobiles; Class A units ignore quiet-time fields and continue broadcasting autonomous position reports.

## Key takeaways

- AIS is not a homogeneous network; it is a partitioned, multi-class architecture balancing RF power, slot-access protocols, and operational safety requirements across diverse maritime users.
- **Class A** transponders (12.5 W) are SOLAS-mandated safety systems utilizing autonomous SOTDMA to continuously negotiate protected time slots across dual parallel receivers.
- **Class B CSTDMA** transponders (2 W) operate as polite guests on the link, measuring local RF noise over a 1,146 µs window and abandoning transmission if background energy exceeds adaptive thresholds.
- **Class B SOTDMA** transponders (5 W) bridge the gap between leisure and commercial shipping, utilizing true SOTDMA slot reservations and supporting accelerated reporting rates up to every 5 seconds.
- **Base Stations** anchor coastal cells using 12.5 W FATDMA broadcasts (Message 4 and Message 20), providing master UTC synchronization and managing regional frequencies via Message 22.
- **AIS AtoNs** transmit Message 21 across three hardware configurations: Type 1 (transmit-only FATDMA), Type 2 (transmit with control receiver), and Type 3 (full transceiver).
- Navigational markers displayed on bridge screens may be **Physical** (transmitting from the buoy), **Synthetic** (transmitted from shore onto an existing physical mark), or **Virtual** (marking digital coordinates with no physical structure).
- Emergency locating devices (**AIS-SART**, **MOB-AIS**, **EPIRB-AIS**) transmit high-probability 8-packet burst sequences at 1 W EIRP with Navigational Status = 14 to guide rescuers directly to victims in the water.
- Coastal shore networks organized under **IALA R0124** ingest, timestamp, deduplicate, and route AIS telemetry across Physical Sensor Sites, Coastal Processing Units, Regional Service Nodes, and Service Management layers.
- Data validation pipelines must actively filter unassigned default MMSIs, monitor CSTDMA packet suppression rates, and verify heading-versus-COG alignment to ensure database integrity.

## References

- CCNR (2023). *Standard Inland AIS — Edition 3.0: Technical Specification for the Inland Automatic Identification System*. Strasbourg: Central Commission for the Navigation of the Rhine.
- IALA (2012). *The AIS Service*. IALA Recommendation R0124 (A-124), Edition 2.2. Saint-Germain-en-Laye: International Association of Marine Aids to Navigation and Lighthouse Authorities.
- IALA (2016). *An Overview of AIS*. IALA Guideline G1082, Edition 2.0. Saint-Germain-en-Laye: International Association of Marine Aids to Navigation and Lighthouse Authorities.
- IALA (2021). *The Use of the Automatic Identification System (AIS) in Marine Aids to Navigation Services*. IALA Recommendation R0126 (A-126), Edition 2.0. Saint-Germain-en-Laye: International Association of Marine Aids to Navigation and Lighthouse Authorities.
- IEC (1998). *Maritime navigation and radiocommunication equipment and systems — Digital interfaces — Part 2: Single talker and multiple listeners, high-speed transmission*. Standard IEC 61162-2:1998, Edition 1.0. Geneva: International Electrotechnical Commission.
- IEC (2010). *Global maritime distress and safety system (GMDSS) — Part 14: AIS search and rescue transmitter (AIS-SART) — Operational and performance requirements, methods of testing and required test results*. Standard IEC 61097-14:2010, Edition 1.0. Geneva: International Electrotechnical Commission.
- IEC (2015). *Maritime navigation and radiocommunication equipment and systems — Automatic identification systems (AIS) — Part 1: AIS Base Stations — Minimum operational and performance requirements, methods of testing and required test results*. Standard IEC 62320-1:2015, Edition 2.0. Geneva: International Electrotechnical Commission.
- IEC (2015). *Maritime navigation and radiocommunication equipment and systems — Automatic identification systems (AIS) — Part 3: Repeater stations — Minimum operational and performance requirements, methods of testing and required test results*. Standard IEC 62320-3:2015, Edition 1.0. Geneva: International Electrotechnical Commission.
- IEC (2016). *Maritime navigation and radiocommunication equipment and systems — Automatic identification systems (AIS) — Part 2: AIS Aids to Navigation (AtoN) Stations — Operational and performance requirements, methods of testing and required test results*. Standard IEC 62320-2:2016, Edition 2.0. Geneva: International Electrotechnical Commission.
- IEC (2017). *Maritime navigation and radiocommunication equipment and systems — Class B shipborne equipment of the automatic identification system (AIS) — Part 1: Carrier-sense time division multiple access (CSTDMA) techniques*. Standard IEC 62287-1:2017, Edition 3.0. Geneva: International Electrotechnical Commission.
- IEC (2017). *Maritime navigation and radiocommunication equipment and systems — Class B shipborne equipment of the automatic identification system (AIS) — Part 2: Self-organising time division multiple access (SOTDMA) techniques*. Standard IEC 62287-2:2017, Edition 2.0. Geneva: International Electrotechnical Commission.
- IEC (2018). *Maritime navigation and radiocommunication equipment and systems — Automatic identification systems (AIS) — Part 2: Class A shipborne equipment of the universal automatic identification system (AIS) — Operational and performance requirements, methods of test and required test results*. Standard IEC 61993-2:2018, Edition 3.0. Geneva: International Electrotechnical Commission.
- IEC (2024). *Maritime navigation and radiocommunication equipment and systems — Digital interfaces — Part 450: Multiple talkers and multiple listeners — Ethernet interconnection*. Standard IEC 61162-450:2024, Edition 3.0. Geneva: International Electrotechnical Commission.
- IMO (1998). *Recommendation on Performance Standards for a Universal Shipborne Automatic Identification System (AIS)*. Resolution MSC.74(69), Annex 3. London: International Maritime Organization.
- IMO (2007). *Adoption of Performance Standards for Survival Craft AIS Search and Rescue Transmitters (AIS-SART) for Use in Search and Rescue Operations*. Resolution MSC.246(83). London: International Maritime Organization.
- IMO (2015). *Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems (AIS)*. Resolution A.1106(29). London: International Maritime Organization.
- ITU (2014). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band*. Recommendation ITU-R M.1371-5. Geneva: International Telecommunication Union.
- ITU (2026). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band*. Recommendation ITU-R M.1371-6. Geneva: International Telecommunication Union.
- ITU (2026). *Assignment and use of identities in the maritime mobile service*. Recommendation ITU-R M.585-10. Geneva: International Telecommunication Union.
- Johnson, G. W. & Swaszek, P. F. (2009). Characteristics of the Carrier Sense TDMA (CSTDMA) Protocol in AIS Class B. *The Journal of Navigation*, 62(4):621–639. doi:10.1017/S037346330999014X
