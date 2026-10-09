# Chapter 68 — Special-purpose AIS: fishing gear, AtoN, SART/MOB/EPIRB, and ADS-B kinship

> **Part X — Adjacent and complementary systems; the future.** Beyond standard shipboard navigation, the VHF data link hosts a diverse ecosystem of specialized markers, survival beacons, aids to navigation, and autonomous radio devices that stretch the boundaries of the original protocol.

**In this chapter.** You will learn the technical design, protocol structures, and operational roles of specialized AIS equipment operating outside conventional shipboard Class A and Class B transponders. We examine Aids to Navigation (**AtoN**), analyzing the mechanical and logical distinctions among physical, synthetic, and virtual AtoNs codified in ITU-R Message 21 and the modern single-slot Message 28 under IALA guidelines and IEC 62320-2. You will master the radio architecture of search and rescue burst transmitters—including survival craft AIS-SARTs (IEC 61097-14), man-overboard (**MOB**) personal beacons (ETSI EN 303 098), and emergency position-indicating radio beacons (**EPIRB-AIS**)—dissecting their 8-message burst schedule, 1-Watt e.i.r.p. link budgets, and 12-character identity encoding under Recommendation ITU-R M.585-10. We confront the widespread deployment of illicit AIS fishing net buoys, assessing the RF slot-map congestion, safety collisions, and regulatory enforcement actions across the FCC and international administrations. Finally, we establish a rigorous technical comparison between maritime AIS and aeronautical **ADS-B**, exploring their common ancestry in VDL Mode 4, differing modulation and MAC choices, physical-layer fingerprinting, and shared architectural vulnerabilities.

## 68.1 Beyond the ship: the special-purpose AIS ecosystem

The Automatic Identification System was conceived under IMO Resolution MSC.74(69) primarily as a shipborne transponder network to facilitate vessel-to-vessel collision avoidance, coastal surveillance, and Vessel Traffic Services (**VTS**). However, the underlying physical and data-link layers defined in Recommendation ITU-R M.1371—operating at 9.6 kbit/s Gaussian Minimum Shift Keying (**GMSK**) across two 25 kHz channels in the maritime VHF mobile band—offer a versatile broadcast pipeline. Over two decades, the maritime community expanded AIS far beyond ship bridges.

Special-purpose AIS encompasses five major equipment categories:
1. **Aids to Navigation (AtoN):** Fixed or floating navigational marks—such as lighthouses, lateral channel buoys, safe water markers, and isolated danger beacons—broadcasting their position, status, and identification directly to electronic chart displays ([Chapter 51](ch51-charts-enc-ecdis.md)).
2. **Search and rescue locating devices (AIS-SART, MOB, EPIRB-AIS):** Low-power battery-operated emergency beacons designed to rapidly guide nearby surface craft and rescue aircraft to life rafts, persons in the water, or sunken vessels.
3. **Autonomous Maritime Radio Devices (AMRD):** Radio devices operating independently at sea, partitioned by Recommendation ITU-R M.2135 into Group A (safety of navigation devices such as approved MOB beacons) and Group B (non-safety maritime devices, such as commercial fishing gear locators).
4. **Fishing gear markers:** Radio transmitters attached to driftnets, longlines, fish aggregating devices (**FADs**), and pot strings. While legal regimes strictly regulate these devices, an illicit market of transmitters broadcasts on maritime AIS channels, creating acute link-layer challenges.
5. **Aeronautical AIS stations:** Search and Rescue (**SAR**) aircraft broadcasting specialized Message 9 position reports to coordinate joint aeronautical-maritime rescue operations ([Chapter 40](ch40-aircraft-and-drones.md)).

Each specialized application places distinct demands on the VHF Data Link (**VDL**). Shipboard Class A units operate with mains power, dedicated 12.5 W amplifiers, dual VHF receivers, and continuous GNSS synchronization. In contrast, an AIS-SART or MOB beacon must survive in freezing sea spray on a compact lithium cell, wake up instantly upon water immersion, and transmit high-priority emergency bursts with a tiny whip antenna operating inches above the waterline without overloading local TDMA slot maps. Similarly, coastal AtoN stations mounted on offshore channel buoys must run continuously for years on modest solar panels and battery banks, necessitating ultra-low-power transmission schemes.

To accommodate these disparate requirements without disrupting primary collision-avoidance operations, international bodies—chiefly the International Telecommunication Union (**ITU**), the International Electrotechnical Commission (**IEC**), the International Association of Marine Aids to Navigation and Lighthouse Authorities (**IALA**), and the European Telecommunications Standards Institute (**ETSI**)—developed dedicated protocol rules, message formats, and channel-access mechanisms.

---

## 68.2 Aids to navigation: physical, synthetic, and virtual

Marine aids to navigation warn mariners of submerged hazards, delineate navigable channels, mark traffic separation schemes, and indicate anchorages. Traditional aids rely on visual daytime markers and night signals, supplemented by passive radar reflectors or radar beacons (**racons**). The integration of AIS into aids to navigation transforms these passive structures into digital broadcast nodes visible on Electronic Chart Display and Information Systems (**ECDIS**) and radar displays in zero visibility.

Operational policy governing AIS AtoN is codified in IMO Circular MSC.1/Circ.1473 (*Policy on Use of AIS Aids to Navigation*), with technical characteristics and management practices detailed in IALA Recommendation R0126 and Guideline G1050. Type approval and performance testing are governed globally by IEC 62320-2 (*AIS AtoN stations*).

### 68.2.1 Operational categories of AtoN

Under IALA and IMO definitions, an AIS AtoN is classified into one of three operational delivery categories:

1. **Physical AIS AtoN:** A physical aid to navigation (such as a steel buoy, light beacon, or offshore tower) carrying an actual AIS transmitter mounted directly on the structure. The transmitted position is derived from an internal GNSS receiver mounted on the buoy or programmed from a geodetic survey. If the aid is a floating buoy subject to anchor swinging circles, the internal GNSS continuously monitors whether the buoy has moved "off position."
2. **Synthetic AIS AtoN:** A physical aid to navigation existing in real water space (e.g., an unlit spar buoy), but lacking an onboard AIS radio. Instead, a shore-based AIS station broadcasts the AIS message representing that physical aid. Synthetic AtoNs divide into:
   - *Monitored synthetic AtoN:* The physical aid is fitted with an independent telemetry link or shore optical monitor confirming that the mark is in position and operating.
   - *Predicted (unmonitored) synthetic AtoN:* The shore station broadcasts the charted position of the physical aid with no real-time telemetry confirming its physical presence.
3. **Virtual AIS AtoN:** A digital mark broadcast over AIS for which *no physical structure exists in the water*. A shore base station broadcasts a digital symbol onto mariners' electronic charts at a specified geographic coordinate. Virtual AtoNs mark temporary hazards after a maritime casualty (e.g., a newly sunken wreck or container spill before salvage buoys arrive), mark dynamic sandbars, or establish dynamic routing limits.

```
+-------------------+-----------------------------+-----------------------------+
| AtoN Category     | Physical Mark in Water?     | Radio Transmitter Location  |
+-------------------+-----------------------------+-----------------------------+
| Physical AtoN     | Yes (buoy, tower, beacon)   | Directly on the mark        |
| Synthetic AtoN    | Yes (unpowered buoy/beacon) | Remotely at coastal base    |
| Virtual AtoN      | No (pure digital datum)     | Remotely at coastal base    |
+-------------------+-----------------------------+-----------------------------+
```

> **Definitions that bite.** Virtual AtoN vs Synthetic AtoN. A synthetic AtoN marks an *actual physical buoy* or lighthouse that lacks its own transmitter, broadcasting its identity from an onshore base station. A virtual AtoN marks a coordinate where *nothing physical exists in the water*. Confusing the two can lead a mariner navigating visually in fog to expect a physical buoy hull that is not there.

### 68.2.2 Station hardware architectures: Types 1, 2, and 3

To meet power constraints on offshore buoys, IEC 62320-2 Table 1 defines three distinct hardware station architectures for AIS AtoN equipment:

```
+---------------------+-------------------+---------------------+---------------------+
| Feature / Parameter | Type 1 AtoN       | Type 2 AtoN         | Type 3 AtoN         |
+---------------------+-------------------+---------------------+---------------------+
| Receiver capability | No receiver       | Receiver for query, | Two receiving       |
|                     | (transmit-only)   | configuration/ctrl  | processes (RATDMA)  |
| VDL Access scheme   | FATDMA only       | FATDMA only         | FATDMA and RATDMA   |
| UTC Synchronization | UTC Direct (GNSS) | UTC Direct (GNSS)   | UTC Direct, UTC     |
|                     |                   |                     | indirect, semaphore |
| VDL Configuration   | No                | Yes (addressed Msg) | Yes (addressed Msg) |
| Power consumption   | Extremely low     | Low                 | Moderate            |
| Primary deployment  | Remote solar buoy | Accessible buoys    | Autonomous offshore |
+---------------------+-------------------+---------------------+---------------------+
```

- **Type 1 (Transmit-only):** Designed for minimal electrical power consumption. The device contains a VHF transmitter and an internal GNSS receiver for position and UTC timing, but *completely lacks a VHF receiver*. Because it cannot listen to the channel, a Type 1 AtoN cannot perform Carrier Sense or Self-Organized slot allocation. It operates exclusively using Fixed Access Time Division Multiple Access (**FATDMA**). Its transmission slots must be pre-reserved on the VDL by an authorized regional AIS base station using Message 20 (Data Link Management Message). If no base station reserves the slots, the Type 1 AtoN risks transmitting in slots occupied by local ship traffic.
- **Type 2 (Transmit and Control Receiver):** Adds a basic VHF receiver dedicated solely to receiving remote configuration, diagnostic, and control commands from coastal authorities (via addressed binary messages or polling). Like Type 1, its regular broadcasts are restricted to FATDMA pre-reserved slots.
- **Type 3 (Autonomous Transceiver):** Equipped with full dual-channel VHF receivers capable of monitoring the VDL slot map. A Type 3 AtoN can operate in areas without coastal base station FATDMA reservations by utilizing Random Access TDMA (**RATDMA**), autonomously selecting unoccupied slots from the local radio environment. It can also respond to polling requests, repeat AIS messages, and support complex health-monitoring telemetry.

Under IEC 62320-2, all AIS AtoN stations are specifically prohibited from responding to channel management assignment messages (Message 16 and Message 23) to prevent unauthorized remote frequency redirection or silencing of critical safety marks.

---

## 68.3 Message 21 and the modern single-slot Message 28

The primary mechanism for broadcasting aids to navigation over the VDL is **Message 21** (Aid-to-Navigation Report). In Recommendation ITU-R M.1371-6 (February 2026), the ITU standardized **Message 28** (Single-slot Aid-to-Navigation Report), addressing slot-capacity bottlenecks in congested ports.

### 68.3.1 Message 21 structure and field layout

Message 21 is a 272-bit message that normally spans **two consecutive TDMA slots** (occupying 360 bits with framing, sync, and buffer). It carries detailed descriptive information about the aid, including its IALA buoyage category, exact physical dimensions, and position integrity status:

```
+-------------------------------------------------------------------------------+
|                    ITU-R M.1371 MESSAGE 21 BIT LAYOUT                         |
+-------------------------------------------------------------------------------+
| Field Name                  | Bits | Type   | Description / Valid Range       |
| --------------------------- | ---- | ------ | ------------------------------- |
| Message ID                  |   6  | uint   | Constant 21                     |
| Repeat Indicator            |   2  | uint   | 0 = default; 3 = do not repeat  |
| MMSI (Source ID)            |  30  | uint   | Format: 99MIDXXXX               |
| Type of Aids to Navigation  |   5  | uint   | 0–31 (IALA navigation aid code) |
| Name of AtoN                | 120  | string | 20 6-bit ASCII characters       |
| Position Accuracy           |   1  | bool   | 1 = DGNSS (<10 m); 0 = standard |
| Longitude                   |  28  | int    | Minutes / 10,000 (East +, W -)  |
| Latitude                    |  27  | int    | Minutes / 10,000 (North +, S -) |
| Dimension: to Bow (A)       |   9  | uint   | Distance antenna to bow/edge (m)|
| Dimension: to Stern (B)     |   9  | uint   | Distance antenna to stern (m)   |
| Dimension: to Port (C)      |   6  | uint   | Distance antenna to port (m)    |
| Dimension: to Starboard (D) |   6  | uint   | Distance antenna to stbd (m)    |
| Type of EPFD                |   4  | uint   | 1=GPS, 2=GLONASS, 7=internal    |
| UTC Second of report        |   6  | uint   | 0–59; 60 = not available        |
| Off-position Indicator      |   1  | bool   | 0 = on position; 1 = off pos.   |
| Regional reserved           |   8  | bits   | Reserved for regional use       |
| RAIM Flag                   |   1  | bool   | 0 = RAIM not active; 1 = active |
| Virtual AtoN Flag           |   1  | bool   | 0 = physical/synthetic; 1 = virt|
| Assigned-mode Flag          |   1  | bool   | 0 = autonomous; 1 = assigned    |
| Spare                       |   1  | bit    | Set to 0                        |
| Name Extension              | 0–88 | string | Optional 0–14 6-bit characters  |
+-------------------------------------------------------------------------------+
```

The 5-bit "Type of Aids to Navigation" field maps directly to the IALA Maritime Buoyage System, defining Cardinal marks (North, South, East, West), Lateral marks (port and starboard hand according to IALA Region A or Region B), Isolated Danger marks, Safe Water marks, and Special marks.

The **Off-position Indicator** is a critical safety bit. When a floating buoy breaks its mooring chain or drags anchor outside its defined swing circle, the onboard processor toggles this bit to 1. Receiving ECDIS equipment renders the buoy icon with an alarming color change and generates an audible navigational alert on the bridge.

The **Virtual AtoN Flag** (bit 269) dictates display symbology under IEC 62288 and IHO S-52. When set to 1, the ECDIS displays a distinctive dashed virtual symbol with the letter "V", informing the navigator that no physical structure will be encountered on radar or visual lookout.

### 68.3.2 Message 28: single-slot optimization

Because Message 21 requires two slots, widespread deployment of multiple virtual AtoNs rapidly depletes available VDL slot capacity. In congested maritime choke points, slot occupancy from dual-slot AtoN broadcasts contributed to channel saturation.

To resolve this, ITU-R M.1371-6 standardized **Message 28**, an Aid-to-Navigation Report compressed into exactly **168 bits**, fitting cleanly inside a **single TDMA slot**. Message 28 reallocates bit budgets:
- It eliminates the 120-bit embedded name string, decoupling identification by optionally pairing with a compact Message 24A static report or relying on an external Maritime Resource Name (**MRN**) per IALA Guideline G1143.
- It expands the "Types of AtoN" field from 5 bits (32 types) to 7 bits (128 types), introducing explicit codes for mobile aids, environmental data buoys (Ocean Data Acquisition Systems, **ODAS**), hazard markers, oil spill perimeters, and search-and-rescue datum marks.
- It adds an explicit 1-bit **Authentication Flag**, signaling whether the broadcast payload is cryptographically authenticated per IALA Guideline G1192 ([Chapter 64](ch64-authentication-future-security.md)).

---

## 68.4 Search and rescue locating devices: AIS-SART, MOB, and EPIRB-AIS

For decades, maritime Search and Rescue (**SAR**) relied on the 9 GHz radar transponder (**radar-SART**) defined under the Global Maritime Distress and Safety System (**GMDSS**). When interrogated by an X-band (3 cm) marine radar, a radar-SART paints a distinctive trail of twelve blips extending outward from the target along its line of bearing. However, radar-SARTs suffer severe operational limitations: detection ranges are degraded by rain clutter and sea spray; surface ships must tune radar gain manually to see them; and consumer leisure craft and small lifeboats frequently lack 9 GHz radar altogether.

In 2007, IMO Resolution MSC.246(83) adopted performance standards for the **AIS-SART** (AIS Search and Rescue Transmitter). Governed by IEC 61097-14, the AIS-SART operates on standard maritime AIS VHF channels. Subsequent standards expanded the family to include **MOB-AIS** personal locating devices for crew overboard recovery (governed in Europe by ETSI EN 303 098 and in the United States by RTCM 11901.2) and hybrid **EPIRB-AIS** beacons integrating 406 MHz satellite alerts with local AIS homing.

### 68.4.1 Transmission protocol: the eight-message burst

Unlike ship transponders that continuously negotiate slots across an indefinite voyage, an emergency locating device is a burst transmitter. When switched on (manually by a survivor or automatically by an inflation sensor or hydrostatic release), the device must guarantee reception by nearby vessels without causing persistent interference.

Recommendation ITU-R M.1371 (Annex 8) and ETSI EN 303 098 (Annex B) specify the mandatory survival transmitter burst schedule:
- **Burst sequence:** Within each 1-minute frame, the transmitter wakes up and broadcasts a sequence of **eight messages in rapid succession**, alternating between AIS 1 (161.975 MHz) and AIS 2 (162.025 MHz)—four messages on each channel.
- **Message mix:** The burst consists of standard Position Reports (**Message 1**) and Safety Related Broadcast Messages (**Message 14**). Under the standard schedule, Message 14 is broadcast during bursts 1 and 5, while Position Reports dominate the remaining bursts.
- **Slot allocation:** Because locating devices lack full dual receivers to track the complete regional slot map, they synchronize internal timing directly to GNSS (UTC direct). To reserve slots across the 1-minute window, Message 1 utilizes SOTDMA communication state with increment values pre-announcing upcoming slots. Within the 8-message burst, messages are transmitted across randomized slot offsets (typically spaced 25 to 50 slots apart), ensuring that at least one message penetrates local slot contention or destructive multi-path wave fading.
- **Repetition interval:** The 8-message burst repeats once every minute for the full operational life of the device (at least 96 hours for an AIS-SART per IEC 61097-14, and at least 24 hours for an MOB-AIS device per ETSI EN 303 098).

```
+-------------------------------------------------------------------------------+
|             SEARCH & RESCUE LOCATING BURST TIMELINE (1 MINUTE)                |
+-------------------------------------------------------------------------------+
| Slot:   s_0        s_1        s_2        s_3        s_4        s_5 ... s_2249 |
| Chan:  AIS 1      AIS 2      AIS 1      AIS 2      AIS 1      AIS 2           |
| Msg:   Msg 1      Msg 1      Msg 1      Msg 1      Msg 14     Msg 14          |
|        [-- Burst 1: 8 messages within ~10 seconds --]                         |
|                                                                               |
| Sleep: Low-power state, GNSS receiver maintaining fix                         |
| Next:  Advance frame; schedule next 8-message burst with random slot offset   |
+-------------------------------------------------------------------------------+
```

### 68.4.2 RF link budgets and sea-surface propagation

A critical engineering challenge for AIS survival devices is the physical antenna environment. An AIS-SART mounted on a life raft canopy achieves an antenna height ($h_{\text{tx}}$) of approximately 1.0 m above sea level. An MOB device attached to an inflatable lifejacket floats at sea level with an antenna height of merely 0.2 m to 0.3 m.

Under ETSI EN 303 098 and IEC 61097-14, these devices operate with a nominal effective isotropic radiated power (**e.i.r.p.**) of **1 Watt** (+30 dBm). 

Calculating the geometric radio horizon using the $4/3$ effective Earth radius approximation:
$$d \approx 4.12 \times \left(\sqrt{h_{\text{tx}}} + \sqrt{h_{\text{rx}}}\right) \quad [\text{km}]$$
For an MOB beacon ($h_{\text{tx}} = 0.3\text{ m}$) communicating with a commercial ship bridge antenna ($h_{\text{rx}} = 20\text{ m}$):
$$d \approx 4.12 \times \left(\sqrt{0.3} + \sqrt{20}\right) \approx 4.12 \times (0.548 + 4.472) \approx 20.7\text{ km } (11.2\text{ nmi})$$

However, at sea level, line of sight is heavily obstructed by oceanic swell. In sea state 4 or 5 (wave heights of 1.5 m to 3.0 m), the transmitting antenna spends substantial fractions of each wave cycle deep within troughs, completely shadowed from surface antennas. This explains the rationale behind the **8-message burst**: by transmitting eight bursts distributed over several seconds across two frequencies, the probability that at least one burst occurs while the beacon is perched on a wave crest is maximized.

While surface ship detection ranges in rough seas typically range between 2 nmi and 5 nmi (3.7 km to 9.3 km), detection from an elevated Search and Rescue aircraft ($h_{\text{rx}} = 3,000\text{ m} \approx 10,000\text{ ft}$) extends past 130 nmi (240 km).

### 68.4.3 Bridge presentation and alarming

When a ship's AIS receiver intercepts an AIS-SART or MOB transmission, onboard navigation systems trigger statutory alerts defined under IEC 62288:
- **Navigational status:** The beacon transmits **Navigational Status 14** ("AIS-SART is active"). Status 15 is transmitted when operating in self-test mode.
- **Symbology:** Under IEC 62288, an active SART/MOB target is rendered as a bold circle enclosing an inscribed cross (the GMDSS survival symbol).
- **Safety broadcast (Message 14):** In addition to the kinematic icon, the unit broadcasts text strings:
  - AIS-SART: `"SART ACTIVE"`
  - MOB beacon: `"MOB ACTIVE"`
  - EPIRB-AIS: `"EPIRB ACTIVE"`
- **Bridge alert:** The ECDIS and radar units generate an immediate high-priority emergency alarm, activating audible buzzers, flashing visual banners, and computing immediate range, bearing, CPA, and TCPA to the distress coordinate.

```
          / \                 ( + )
         /   \             AIS-SART / MOB
        /  A  \                Target
       /_______\           (Inscribed Cross)
    Standard Vessel
```

---

## 68.5 Numbering schemes and identity resolution: M.585

The 9-digit Maritime Mobile Service Identity (**MMSI**) defined in Recommendation ITU-R M.585 governs all maritime transmissions. To distinguish survival craft, aids to navigation, and autonomous radio devices from commercial vessels, M.585 reserves specific prefix spaces.

Recommendation ITU-R M.585-10 partitions these identities into structured formats:

```
+-------------------------------------------------------------------------------+
|               ITU-R M.585-10 SPECIAL-PURPOSE IDENTITY FORMATS                 |
+-------------------------------------------------------------------------------+
| Identity Format   | Category / Device Class        | Numbering Structure      |
| ----------------- | ------------------------------ | ------------------------ |
| 99MIDXXXX         | Aids to Navigation (AtoN)      | 99 + MID + 4 digits      |
|                   |  - 6th digit 1 = Physical      | 99MID1XXX                |
|                   |  - 6th digit 6 = Virtual       | 99MID6XXX                |
|                   |  - 6th digit 8 = Mobile AtoN   | 99MID8XXX                |
| 111MIDXXX         | SAR Aircraft                   | 111 + MID + 3 digits     |
| 970XXYYYY         | AIS-SART                       | 970 + Manufacturer + Ser.|
| 972XXYYYY         | Man Overboard (MOB)            | 972 + Manufacturer + Ser.|
| 974XXYYYY         | EPIRB-AIS                      | 974 + Manufacturer + Ser.|
| 979YYYYYY         | AMRD Group B (Non-safety)      | 979 + 6-digit pseudorand.|
+-------------------------------------------------------------------------------+
```

### 68.5.1 The 12-character extended identity for burst transmitters

The 9-digit freeform identity format for survival devices (`97 T XX YYYY`) presents a severe namespace constraint. With only four digits dedicated to the unit serial number (`YYYY`), an individual manufacturer (`XX`, assigned 01 through 99 by CIRM, the Comité International Radio-Maritime) can produce only 10,000 unique units before exhausting its number block.

To resolve this limitation without breaking backwards compatibility with legacy decoders that expect a 30-bit integer in Message 1, ITU-R M.1371 (Annex 8 §6) and ITU-R M.585-10 established a **12-character extended identity scheme**:
$$\text{Format: } 97\text{ }T\text{ }XX\text{ }M\text{ }PP\text{ }YYYY$$
- $T$: Device type code ($0 = \text{SART}$, $2 = \text{MOB}$, $4 = \text{EPIRB-AIS}$).
- $XX$: CIRM-assigned manufacturer identifier (01–99; 00 reserved for test units).
- $M$: Manufacturer-assigned model/range suffix (single uppercase ASCII character, A–Z).
- $PP$: Manufacturer prefix sequence number (two alphanumeric digits, 01–99).
- $YYYY$: Unit serial sequence number (0000–9999).

Under this protocol, the unit broadcasts the standard 9-digit prefix `97TXXYYYY` in its primary Message 1 position reports, while transmitting the full extended 12-character identity in its accompanying Message 14 safety broadcasts (`"SART ACTIVE MPP"`). Decoders concatenate both to reconstruct the unique factory identity.

---

## 68.6 Illicit AIS fishing gear: proliferation, collisions, and the regulatory clash

A highly disruptive development in maritime VHF data link operations is the massive, unregulated proliferation of **AIS fishing net buoys**.

### 68.6.1 The operational problem

Industrial commercial fishing fleets (longliners, purse seiners, gillnetters, and trawlers) routinely set fishing gear that drifts over dozens of square miles of open ocean. Traditionally, fishermen tracked drifting nets, longline strings, and Fish Aggregating Devices (**FADs**) using radio direction-finding (**RDF**) buoys transmitting on medium frequencies (MF, 1.6 MHz to 3 MHz) or proprietary satellite beacons (such as Argos or Iridium).

Around 2012, equipment manufacturers in East Asia began producing cheap (sub-$50), solar-powered VHF beacons designed to be lashed directly to net flags and longline buoys. Instead of transmitting on designated telemetry frequencies, these devices transmit directly on standard maritime AIS frequencies (161.975 MHz and 162.025 MHz).

These net markers broadcast standard AIS position reports (typically Message 1 or Message 21), claiming arbitrary or spoofed MMSIs. A single industrial vessel may deploy 50 to 100 net buoys. In areas of intense fishing activity—such as the South China Sea, the East China Sea, and waters off West Africa—tens of thousands of unregulated net buoys broadcast simultaneously.

### 68.6.2 Impact on the VHF data link and navigational safety

The uncontrolled deployment of AIS fishing net markers introduces three severe hazards to the maritime environment:

1. **RF slot exhaustion and packet collisions:** As demonstrated in [Chapter 30](ch30-network-loading-packet-loss.md), the AIS VDL operates with a hard physical capacity of 4,500 slots per minute across both channels. Unregulated net beacons utilize rudimentary carrier-sensing or unsynchronized pseudo-random slot selection, ignoring standard SOTDMA reservations. In congested choke points, thousands of net buoys saturate the link, driving channel load above 50% to 70%. Transmissions collide with high-priority Class A position reports from commercial ships, causing critical vessel targets to drop off shipboard radar and ECDIS screens.
2. **Bridge display clutter and alert desensitization:** Under IMO carriage mandates, commercial ships must display AIS targets on radar and ECDIS. When a vessel enters a fishing ground contaminated with hundreds of net buoys, the bridge display becomes blanketed by false vessel icons (green sleeping triangles). Crucial navigation targets are visually drowned out. Watchkeepers, overwhelmed by incessant proximity alarms against stationary nets, frequently mute alarms or disable AIS overlays entirely, directly undermining collision avoidance ([Chapter 53](ch53-mariner-training.md)).
3. **MMSI piracy and registry corruption:** Illicit net markers lack authorized MMSI allocations. Manufacturers hardcode fabricated numbers into beacon firmware, frequently utilizing fabricated ship MMSIs (`412XXXXXX`, `413XXXXXX`), spoofed country codes, or even mimicking foreign naval prefixes. When these buoys transmit, coastal surveillance engines falsely register ghost fishing vessels or assign commercial ship identities to drifting plastic poles ([Chapter 47](ch47-data-quality-track-reconstruction.md)).

### 68.6.3 International standards and the AMRD Group B compromise

To resolve this crisis, the ITU Radiocommunication Sector established a dedicated study group that formulated **Recommendation ITU-R M.2135** (*Autonomous Maritime Radio Devices*):

- **Group A AMRD (Safety of Navigation):** Devices that support navigational safety, search and rescue, or distress operations (e.g., approved AIS-SARTs, MOB beacons, and official aids to navigation). Group A devices are authorized to operate on core AIS channels (AIS 1 and AIS 2) and DSC Channel 70.
- **Group B AMRD (Non-safety Devices):** Devices that do *not* support navigational safety, explicitly encompassing fishing gear locators, oceanographic research sensors, and sports buoys. Under ITU-R M.2135-1 and the ITU Radio Regulations (Appendix 18), Group B AMRDs are **strictly banned from AIS 1 and AIS 2**. Instead, they are relegated to a separate frequency: **Channel 2006 (160.900 MHz)**.

Furthermore, Recommendation ITU-R M.585-10 established a designated numbering block for Group B devices:
$$\text{Identity Format: } 979YYYYYY$$
where the six digits $YYYYYY$ are derived from a pseudorandom algorithm over 000000 to 999999. Because Channel 2006 is separate from primary collision-avoidance channels, Group B broadcasts cannot corrupt shipboard ECDIS displays or deplete SOLAS slot budgets.

```
+-------------------------------------------------------------------------------+
|                       AMRD GROUP CLASSIFICATION MATRIX                        |
+-------------------------------------------------------------------------------+
| Parameter           | Group A AMRD (Safety)       | Group B AMRD (Non-Safety) |
| ------------------- | --------------------------- | ------------------------- |
| Operational purpose | MOB, SAR, official AtoN     | Fishing net buoy, FAD     |
| Permitted channels  | AIS 1, AIS 2, DSC Ch 70     | Channel 2006 (160.900 MHz)|
| Identity prefix     | 970 (SART), 972 (MOB), 99   | 979 (Pseudorandom 6-digit)|
| Bridge display      | Mandatory ECDIS alert/icon  | Filtered; no ECDIS clutter|
| Governing standard  | IEC 61097-14, EN 303 098    | ITU-R M.2135-1            |
+-------------------------------------------------------------------------------+
```

Despite the international adoption of M.2135, non-compliant manufacturers continue to mass-produce cheap net markers operating on AIS 1 and AIS 2, creating an enduring operational challenge that requires active regulatory and technological countermeasures.

> **Threat model.** Attacker / Actor: Commercial fishing operators deploying uncertified AIS net buoys. Capability: Low-cost (sub-$50) autonomous VHF transmitters broadcasting Class A/B position reports or AtoN Message 21 on 161.975/162.025 MHz. Impact: Localized VDL slot starvation, ECDIS display clutter, target masking of real vessels, and false collision alarms. Mitigation: Coastal receiver RF direction-finding, satellite cluster tracking of buoy signatures, automated ECDIS filtering of static drift trajectories, and port-state enforcement seizures.

> **Legal note.** Under US Federal Communications Commission regulations (47 CFR Part 80) and federal enforcement precedent (FCC Enforcement Advisory DA 18-1210), the marketing, sale, and operational use of non-certified AIS fishing net buoys on maritime frequencies is illegal. Violators face statutory civil forfeitures up to $19,639 per day under 47 CFR § 1.80, reaching statutory maximums exceeding $147,290 for continuing violations, alongside criminal seizure of radio equipment. Similar statutory prohibitions exist under EU Directive 2014/53/EU (Radio Equipment Directive).

---

## 68.7 Kinship with aviation: AIS vs. ADS-B

In the history of autonomous transport surveillance, maritime AIS does not exist in isolation. Its closest technological cousin is aviation's **Automatic Dependent Surveillance–Broadcast** (**ADS-B**), codified by the International Civil Aviation Organization (**ICAO**) under Annex 10 to the Chicago Convention and technical specifications RTCA DO-260B / DO-260C.

Both systems emerged from the late-20th-century push to replace passive radar tracking with autonomous, satellite-derived digital broadcasts. Examining the kinships and technical divergences between AIS and ADS-B illuminates fundamental tradeoffs of cooperative radio surveillance.

### 68.7.1 Shared technological lineage: the VDL Mode 4 connection

The technical kinship between AIS and ADS-B is historical and architectural. During the late 1980s and early 1990s, Swedish inventor Håkan Lans pioneered Time Division Multiple Access communications synchronized by Global Positioning System (**GPS**) timing ([Chapter 9](ch09-prehistory-and-stdma.md)). Lans envisioned a universal transponder standard that would serve both aircraft and ocean-going ships.

In civil aviation, this architecture was standardized by ICAO as **VHF Digital Link Mode 4** (**VDL Mode 4**). VDL Mode 4 utilized GMSK modulation in the aeronautical VHF band (118–137 MHz) with Self-Organizing TDMA to allow aircraft to exchange surveillance vectors autonomously. 

When the maritime community through the IMO, ITU, and IALA sought a digital surveillance transponder in the mid-1990s, they directly adopted the physical and link-layer foundations of VDL Mode 4, transposing them into the maritime VHF mobile band (156–162 MHz) to create **Recommendation ITU-R M.1371**.

However, while maritime transport embraced SOTDMA as its universal global standard, civil aviation took a sharply divergent path.

### 68.7.2 Technical architecture comparison: AIS vs. ADS-B

Aviation authorities evaluated VDL Mode 4 for air traffic surveillance but ultimately selected **1090 MHz Extended Squitter** (**1090ES**) as the primary global standard for commercial transport aircraft, supplemented in the United States by **Universal Access Transceiver** (**UAT**) on 978 MHz for general aviation.

The technical parameters of the two systems reflect starkly different operating regimes:

```
+-----------------------------------+-----------------------------------+-----------------------------------+
| Parameter / Dimension             | Maritime AIS (ITU-R M.1371)       | Aeronautical ADS-B (1090ES)       |
+-----------------------------------+-----------------------------------+-----------------------------------+
| Governing body                    | IMO / ITU-R / IEC / IALA          | ICAO / RTCA / Eurocae / FAA       |
| Primary frequency                 | 161.975 MHz & 162.025 MHz         | 1090 MHz (secondary: 978 MHz UAT) |
| Spectrum band                     | Maritime Mobile VHF               | Aeronautical Radionavigation UHF  |
| Modulation scheme                 | GMSK (BT = 0.4 / 0.3)             | Pulse Position Modulation (PPM)   |
| Raw bit rate                      | 9,600 bit/s                       | 1,000,000 bit/s (1 Mbit/s)        |
| Channel access scheme             | SOTDMA / CSTDMA / FATDMA / RATDMA | Stochastic pure ALOHA (squitter)  |
| Frame / Timing structure          | Synchronized 1-minute frames      | Asynchronous random pulses;       |
|                                   | (2,250 slots @ 26.67 ms each)     | no slotting; pulse width 0.5 µs   |
| Primary position payload          | Messages 1, 2, 3 (168 bits)       | Type 9–18 airborne pos. (112 bits)|
| Reporting interval                | 2 seconds to 3 minutes (speed dep)| 0.4 to 0.6 seconds (nominal 2 Hz) |
| Standard transmit power           | 1 W (Class B) / 12.5 W (Class A)  | 125 W to 500 W peak pulse power   |
| Nominal radio horizon             | 20–30 nmi (surface ship)          | 150–250 nmi (cruising aircraft)   |
| Target velocity range             | 0 to 50 knots (rarely >100 kn)    | 0 to 600+ knots                   |
| Doppler shift tolerance           | Narrow (±125 Hz nominal)          | Broad (operating at 1 GHz)        |
| Identity scheme                   | 9-digit MMSI (ITU-R M.585)        | 24-bit ICAO aircraft address      |
| Cryptographic authentication      | None (raw broadcast)              | None (raw broadcast)              |
+-----------------------------------+-----------------------------------+-----------------------------------+
```

### 68.7.3 Protocol mechanics: SOTDMA vs. Stochastic ALOHA

The most profound divergence between AIS and ADS-B lies at the Medium Access Control (**MAC**) layer:
- **AIS relies on slot synchronization:** AIS mandates strict time-slot discipline. Every station divides time into 2,250 slots per minute, synchronized to UTC via GNSS. Stations listen to the channel, construct a dynamic map of occupied slots, and announce future slot reservations within their transmission headers. This SOTDMA mechanism provides deterministic channel utilization, reaching link efficiencies of 80% to 90% before experiencing localized packet degradation.
- **ADS-B 1090ES relies on pure ALOHA:** In contrast, 1090ES transponders do not synchronize time slots or listen before transmitting. An aircraft transponder wakes up approximately twice per second and "squitters" a 112-microsecond pulse burst into the air on 1090 MHz at a random time interval (stochastic ALOHA). Because the transmission burst is extraordinarily short (112 bits at 1 Mbit/s occupies only 120 microseconds including preamble), multiple aircraft can share the frequency. However, as airspace density increases, overlapping bursts inevitably collide, requiring ground multi-lateration and advanced receiver processing to disentangle overlapping pulses.

### 68.7.4 Physical-layer fingerprinting and security kinship

Despite frequency and MAC differences, AIS and ADS-B share a critical vulnerability: **both protocols are unauthenticated and unencrypted**.

In both domains, transmitters broadcast plain-text digital packets that can be intercepted with a low-cost Software Defined Radio (**SDR**). An attacker with an SDR transmitter can inject phantom aircraft or ghost vessels into air traffic control or VTS systems.

Because retrofitting cryptographic signatures into low-bandwidth legacy broadcast protocols is technically complex, security researchers turned to **Radio Frequency Fingerprinting** (**RFF**) and physical-layer Specific Emitter Identification (**SEI**).

The research lineage between the two domains is directly coupled:
- **Aeronautical foundations:** In aviation, Strohmeier and Martinovic (2015) demonstrated that passive data-link layer timing and protocol-quirk analysis could accurately distinguish distinct Mode S and ADS-B transponder hardware. Subsequently, Leonardi, Di Gregorio, and Di Fausto (2017) demonstrated that subtle phase-pattern variations within the 1090 MHz pulse preamble provide stable radiometric signatures capable of classifying aircraft transponder models and manufacturers.
- **Maritime adoption:** Maritime researchers adapted these identical methodologies to AIS. Because AIS transponders utilize continuous-phase GMSK, researchers focus on transmitter-specific hardware imperfections—such as carrier frequency offsets (**CFO**), Gaussian filter bandwidth-time ($BT$) product deviations, modulation index errors, and transient power amplifier ramp-up slopes ([Chapter 34](ch34-rf-forensics-fingerprinting.md)). While RF fingerprinting can reliably distinguish transponder manufacturers or detect naive spoofers replaying recorded payloads, open-set unit-level identification of thousands of ships across varying weather and propagation channels remains an ongoing research challenge.

---

## Then & now

- **1990s** ⟨H⟩ — Håkan Lans and the Swedish Civil Aviation Administration develop GP&C (Global Positioning and Communications), demonstrating SOTDMA technology for simultaneous maritime and aviation surveillance.
- **1998** ⟨H⟩ — ITU-R adopts Recommendation M.1371-0, formalizing the maritime application of SOTDMA on VHF channels 87B and 88B, while civil aviation turns toward 1090 MHz Extended Squitter.
- **2007** ⟨+⟩ — IMO adopts Resolution MSC.246(83), codifying performance standards for AIS Search and Rescue Transmitters (AIS-SART) as an operational alternative to 9 GHz radar-SARTs.
- **2008** ⟨+⟩ — IEC publishes IEC 62320-2 Edition 1.0, defining international test standards for physical, synthetic, and virtual AIS Aids to Navigation (AtoN).
- **2010** ⟨+⟩ — IEC publishes IEC 61097-14, establishing operational and performance test requirements for GMDSS AIS-SART survival devices.
- **2012** ⟨+⟩ — Proliferation of cheap, uncertified AIS fishing net buoys begins across East Asian fishing grounds, creating severe localized VDL slot congestion.
- **2014** ⟨+⟩ — IMO approves MSC.1/Circ.1473, establishing unified international policy for the deployment and charted display of physical, synthetic, and virtual AIS AtoN.
- **2016** ⟨+⟩ — IEC publishes IEC 62320-2 Edition 2.0, refining AtoN station Types 1, 2, and 3 and adding mandatory cyber-security protections for remote VDL configuration.
- **2018** ⟨+⟩ — The US FCC Enforcement Bureau issues Enforcement Advisory DA 18-1210, warning fishermen and marine vendors that marketing, selling, or using non-compliant AIS net buoys violates federal communications law.
- **2019** ⟨+⟩ — ETSI publishes EN 303 098 V2.2.1, harmonizing European standards for maritime low-power personal locating devices (MOB-AIS); ITU adopts M.2135-0 defining Autonomous Maritime Radio Devices (AMRD).
- **2023** ⟨+⟩ — ITU adopts Recommendation ITU-R M.2135-1, firmly relegating Group B non-safety AMRDs (fishing net buoys) to Channel 2006 (160.900 MHz) and banning them from AIS 1/2.
- **2026** ⟨+⟩ — ITU adopts Recommendation ITU-R M.1371-6, formally standardizing Message 28 (Single-slot Aid-to-Navigation Report) with integrated cryptographic authentication flags.

---

## On the wire

Inspecting real-world special-purpose AIS packets reveals the precise field encodings and bit alignments used on the RF link and over standard NMEA 0183 presentation interfaces.

### Example 1: Physical Aid to Navigation (Message 21)

The following NMEA sentence represents a real physical buoy broadcast captured in Boston Harbor:

```
!AIVDM,1,1,,B,E>k`s@IQ7ab7W@0`897PQT@61@1MMwCh<7rjP20@@@P00000000000000000,4*56
```

Decoding this payload byte stream reveals the complete Message 21 structure:

```
+-------------------------------------------------------------------------------+
| Field Name                  | Decoded Value      | Technical Interpretation   |
+-------------------------------------------------------------------------------+
| Message Type                | 21                 | Aid-to-Navigation Report   |
| Repeat Indicator            | 0                  | Original broadcast         |
| MMSI                        | 993672001          | 99=AtoN, 367=USA, ID=2001  |
| AtoN Type                   | 19                 | Special Purpose Mark       |
| Name                        | BOSTON APPROACH LB | 20 6-bit ASCII characters  |
| Position Accuracy           | 1 (True)           | Differential fix (<10 m)   |
| Longitude                   | -70.7836°          | 70° 47.016' W              |
| Latitude                    | 42.3755°           | 42° 22.530' N              |
| Dimension to Bow (A)        | 2 m                | Buoy dimension offset      |
| Dimension to Stern (B)      | 2 m                | Buoy dimension offset      |
| Dimension to Port (C)       | 2 m                | Buoy dimension offset      |
| Dimension to Starboard (D)  | 2 m                | Buoy dimension offset      |
| EPFD Type                   | 1                  | GPS                        |
| UTC Second                  | 0                  | Transmitted at :00 sec     |
| Off-position Indicator      | 0 (False)          | On station within swing rad|
| Virtual AtoN Flag           | 0 (False)          | Physical buoy in water     |
| RAIM Flag                   | 0 (False)          | RAIM not active            |
| Assigned Mode               | 0 (False)          | Autonomous FATDMA schedule |
+-------------------------------------------------------------------------------+
```

The MMSI `993672001` immediately alerts any decoding pipeline that this is an Aid to Navigation belonging to the United States (MID 367). The `Virtual AtoN Flag` is 0, confirming to the bridge display that this is an actual physical floating buoy.

### Example 2: Active AIS-SART distress broadcast (Message 1)

When an AIS-SART or MOB device activates, it broadcasts standard Position Reports (**Message 1**) configured with Navigational Status 14:

```
!AIVDO,1,1,,A,1>M;`h>P00wrFE8LcTf00?vOP000,0*7E
```

Decoding this burst reveals the emergency survival profile:

```
+-------------------------------------------------------------------------------+
| Field Name                  | Decoded Value      | Technical Interpretation   |
+-------------------------------------------------------------------------------+
| Message Type                | 1                  | Position Report (Class A)  |
| Repeat Indicator            | 0                  | Original transmission      |
| MMSI                        | 970123456          | 970=AIS-SART, Mfg 12, S/N  |
| Navigational Status         | 14                 | AIS-SART is active         |
| Rate of Turn (ROT)          | -128               | Not available              |
| Speed Over Ground (SOG)     | 0.0 knots          | Stationary in survival raft|
| Position Accuracy           | 1 (True)           | High accuracy GNSS fix     |
| Longitude                   | -1.2345°           | 001° 14.070' W             |
| Latitude                    | 50.1234°           | 50° 07.404' N (Solent area)|
| Course Over Ground (COG)    | 0.0°               | Not applicable             |
| True Heading                | 511                | Not available              |
| Time Stamp                  | 15                 | Second 15 of current minute|
| Maneuver Indicator          | 0                  | Not available              |
| RAIM Flag                   | 0                  | RAIM not active            |
| SOTDMA Comm State           | 0                  | Pre-announces next burst   |
+-------------------------------------------------------------------------------+
```

### Example 3: SART text alert broadcast (Message 14)

Concurrently with Message 1, the device broadcasts a safety-related text burst on Message 14:

```
!AIVDO,1,1,,A,>>M;`h1<59B04=@UHD,2*3B
```

Decoding the payload yields:
- **Message Type:** 14 (Safety Related Broadcast)
- **Source MMSI:** 970123456
- **Safety Message Text:** `"SART ACTIVE"`

Receiving bridge systems correlate the Message 14 text alert with the Message 1 position report, triggering high-priority audible and visual MOB/SART alarms.

> **Try it.** You can decode and verify special-purpose AIS payloads in Python using `pyais`. The following snippet decodes a physical AtoN report and extracts its key navigational attributes:
>
> ```python
> import pyais
> 
> raw_nmea = "!AIVDM,1,1,,B,E>k`s@IQ7ab7W@0`897PQT@61@1MMwCh<7rjP20@@@P00000000000000000,4*56"
> msg = pyais.decode(raw_nmea)
> 
> print(f"Message Type: {msg.msg_type}")
> print(f"AtoN MMSI:    {msg.mmsi}")
> print(f"AtoN Name:    {msg.name.strip('@ ')}")
> print(f"Position:     {msg.lat:.4f}° N, {msg.lon:.4f}° E")
> print(f"Off-Position: {msg.off_position}")
> print(f"Virtual Mark: {msg.virtual_aid}")
> ```
> Expected output:
> ```
> Message Type: 21
> AtoN MMSI:    993672001
> AtoN Name:    BOSTON APPROACH LB B
> Position:     42.3755° N, -70.7836° E
> Off-Position: False
> Virtual Mark: False
> ```

---

## Validation, uncertainty & data quality

Special-purpose AIS transmissions exhibit distinct data quality and failure profiles compared to conventional shipboard transponders. Ingestion and analytical pipelines must implement explicit validation logic to avoid data corruption.

### 68.8.1 Common failure modes and error propagation

1. **AtoN swinging circle false alarms:** Floating buoys are anchored to the seabed with heavy chain. Under strong tidal currents or wind shifts, a buoy naturally swings in a circular radius:
   $$R_{\text{swing}} \approx \sqrt{L_{\text{chain}}^2 - D_{\text{water}}^2}$$
   If an AtoN firmware profile configures an excessively tight off-position threshold (e.g., setting a 15 m tolerance on a buoy with a 25 m swing radius), the device will toggle its `Off-position Indicator` on every tidal ebb and flood. Automated monitoring pipelines ashore observe flickering off-position alarms, potentially triggering false hazard notices to mariners.
2. **Missing Message 14 in survival beacons:** While Recommendation ITU-R M.1371 requires both Message 1 and Message 14 for locating devices, low-cost or compromised MOB beacons occasionally fail to transmit Message 14, or their Message 14 bursts suffer packet collisions. A compliant ECDIS or shore decoder must trigger an emergency alert based *solely* on Navigational Status 14 in Message 1 and the `970`/`972`/`974` MMSI prefix, without waiting for the text confirmation in Message 14.
3. **MMSI collisions from counterfeit net buoys:** Illicit net buoys typically ship from factories with hardcoded duplicate MMSIs (e.g., hundreds of buoys sharing `888888888` or `123456789`). When multiple buoys drift within range of the same coastal receiver or LEO satellite pass, naive track-assembly algorithms connect disparate coordinates into impossible hyper-speed trajectories spanning hundreds of miles in minutes.

### 68.8.2 Concrete validation procedure

Data pipelines ingesting multi-source AIS streams must apply the following structural validation filters:

```
+-------------------------------------------------------------------------------+
|               SPECIAL-PURPOSE AIS VALIDATION LOGIC                            |
+-------------------------------------------------------------------------------+
| Condition / Test                  | Detection Rule         | Pipeline Action  |
| --------------------------------- | ---------------------- | ---------------- |
| SART / MOB Distress Check         | MMSI starts with 970,  | Elevate to SAR   |
|                                   | 972, 974 OR NavStat=14 | priority alert   |
|                                   |                        |                  |
| Illicit Net Marker Detection      | MMSI starts with 979   | Tag as Net Buoy; |
|                                   | on AIS 1/2 OR drifting | isolate from     |
|                                   | speed <3 kn with       | commercial fleet |
|                                   | erratic Class A packet | tracking tables  |
|                                   |                        |                  |
| Virtual AtoN Integrity Check      | Msg 21 VirtualFlag=1;  | Alert VTS; verify|
|                                   | check shore station    | against national |
|                                   | authorization registry | Notice to Mariners|
|                                   |                        |                  |
| Impossible Kinematic Filter       | Δdistance / Δt > 60 kn | Split track into |
|                                   | on identical MMSI      | separate emitter |
|                                   |                        | clusters         |
+-------------------------------------------------------------------------------+
```

---

## Software

The following tools and libraries support decoding, generating, and inspecting special-purpose AIS packets:

**Open source:**
- `pyais` (Python): Pure-Python AIS message decoder and encoder. Fully decodes Message 21 AtoN, Message 14 text, and Message 1/2/3 survival craft reports with full enum mapping. Caveat: Lacks built-in SOTDMA comm-state slot reservation validation.
- `libais` (C++ / Python): Fast C++ decoding library developed by Kurt Schwehr. Decodes Message 21 and legacy messages with strict standards adherence. Caveat: Does not support the newly standardized single-slot Message 28.
- `gpsd` (C): System daemon that intercepts GPS and AIS feeds. Features extensive support for AtoN and SART presentation sentences. Caveat: Internal heuristics smooth out irregular burst transmission timestamps, potentially obscuring SART burst-timing analysis.

**Free but closed:**
- `OpenCPN` (Cross-platform): Open-source chart plotter with extensive marine electronics community use. Implements full IEC 62288 visual symbols for AIS-SART, MOB cross-in-circle alerts, and physical/virtual AtoN rendering. Caveat: Desktop visualization only; lacks headless bulk pipeline processing interfaces.

**Commercial:**
- `SRT Marine Systems Marine Core`: Commercial AtoN and coastal surveillance software suite providing full FATDMA slot management, Type 1/2/3 configuration, and virtual AtoN generation. Caveat: Proprietary, high license cost, tied to proprietary shore base-station infrastructure.

---

## Standards & guides

- **ITU-R Recommendation M.1371-6** (2026): *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band*. Defines physical and link layers, Message 21, Message 28, and Annex 8 burst transmission requirements.
- **ITU-R Recommendation M.585-10** (2026): *Assignment and use of identities in the maritime mobile service*. Governs formatting for 9-digit MMSIs, AtoN identities (`99MIDXXXX`), SART/MOB/EPIRB freeform identities (`970`, `972`, `974`), and extended 12-character identities.
- **ITU-R Recommendation M.2135-1** (2023): *Technical characteristics of autonomous maritime radio devices operating in the frequency band 156–162.05 MHz*. Segregates AMRD Group A (safety) from Group B (non-safety net markers) and assigns Channel 2006.
- **IEC 61097-14:2010**: *Global maritime distress and safety system (GMDSS) – Part 14: AIS search and rescue transmitter (AIS-SART) – Operational and performance requirements, methods of testing and required test results*. Governs type approval of survival craft AIS-SARTs.
- **IEC 62320-2:2016 (Edition 2.0)**: *AIS AtoN stations – Minimum operational and performance requirements, methods of testing and required test results*. Defines hardware requirements for AtoN station Types 1, 2, and 3.
- **ETSI EN 303 098 V2.2.1** (2019): *Maritime low power personal locating devices employing AIS; Harmonised Standard for access to radio spectrum*. Specifies European requirements and tests for MOB-AIS beacons.
- **RTCM Standard 11901.2** (2024): *Standard for Maritime Survivor Locating Devices (MSLD)*. United States standard governing personal locating and MOB devices.
- **IMO Resolution MSC.246(83)** (2007): *Adoption of Performance Standards for Survival Craft AIS Search and Rescue Transmitters (AIS-SART) for Use in Search and Rescue Operations*. Authorizes AIS-SART under GMDSS.
- **IMO Circular MSC.1/Circ.1473** (2014): *Policy on Use of AIS Aids to Navigation*. Establishes international operational rules for deploying physical, synthetic, and virtual AtoNs.
- **IALA Recommendation R0126 (A-126)**: *The Use of the Automatic Identification System (AIS) in Marine Aids to Navigation Services*. Technical implementation guidelines for maritime authorities.
- **IALA Guideline G1050**: *Management and Monitoring of AIS Information*. Covers shore-based monitoring and maintenance of digital aids.

---

## Pitfalls

1. **Confusing Virtual AtoN with Synthetic AtoN** → Watchstanders assume an approaching synthetic mark has no physical presence in the water → Synthetic marks have actual physical buoys that can be struck by a vessel's hull → Check the `Virtual AtoN Flag` in Message 21; never assume a digital target implies open water unless confirmed virtual.
2. **Deploying Type 1 AtoN in Unmanaged Airspace** → A harbor authority installs a cheap Type 1 transmit-only buoy in an area lacking coastal base station FATDMA reservations → The buoy transmits blindly in slots occupied by Class A ships, causing packet collision → Type 1 AtoNs must *never* be deployed without active base station slot reservations.
3. **Filtering out Navigational Status 14 in Data Pipelines** → Data cleaning scripts treat status 14 as an invalid or reserved state, discarding the records → Active SART, MOB, or EPIRB distress bursts are wiped from the surveillance stream → Explicitly whitelist status 14 and trigger high-priority alerts.
4. **Treating AIS Fishing Net Buoys as Legitimate Vessels** → Maritime analysts count every active MMSI broadcast as a commercial fishing vessel in economic reports → Fleets deploy 50+ net buoys per ship, inflating vessel counts by orders of magnitude → Filter out stationary or drifting targets with unassigned MMSIs or characteristic Group B trajectory patterns.
5. **Relying on Message 14 for Immediate SART Detection** → Software waits to receive `"SART ACTIVE"` text before sounding a bridge alarm → Message 14 bursts suffer higher collision rates in noisy waters than Message 1 → Trigger immediate emergency indicators upon detecting Nav Status 14 or a `970`/`972`/`974` prefix in Message 1.
6. **Failing to Account for Wave Shadowing in MOB Search Planning** → Search and rescue planners calculate VHF detection ranges based on flat-earth line of sight (10–12 nmi) → In sea state 4, lifejacket antennas spend 80% of their time hidden behind wave crests, reducing surface ship detection to 1–3 nmi → Deploy airborne assets to gain high-altitude line of sight when searching for low-power personal beacons.
7. **Misinterpreting Floating AtoN Off-Position Alarms** → System operators treat any off-position flag as a broken mooring → The buoy's configured swing circle tolerance was smaller than the physical anchor chain scope → Verify tidal state and chart depth before dispatching tender vessels.
8. **Assuming ADS-B and AIS Packets Can Directly Interoperate** → System integrators attempt to route ADS-B receivers into maritime VTS software or vice versa → ADS-B operates at 1090 MHz PPM at 1 Mbit/s, while AIS operates at 162 MHz GMSK at 9.6 kbit/s → Translation requires physical RF demodulation and application-level gateway bridging.

---

## Key takeaways

- Special-purpose AIS encompasses Aids to Navigation (AtoN), survival craft locating devices (AIS-SART, MOB, EPIRB-AIS), autonomous maritime radio devices (AMRD), and fishing net markers.
- AtoNs divide operationally into physical (transmitter on the buoy), synthetic (physical buoy in water; transmitted from shore), and virtual (digital mark only; no physical buoy).
- AtoN station hardware divides into Type 1 (transmit-only, FATDMA-only, ultra-low power), Type 2 (adds configuration receiver), and Type 3 (full autonomous dual-channel transceiver with RATDMA).
- Message 21 is a two-slot report providing detailed name and dimension data; the modern Message 28 compresses AtoN reports into a single slot with integrated authentication flags.
- AIS-SART, MOB, and EPIRB-AIS devices broadcast an eight-message burst alternating between AIS 1 and AIS 2 once every minute, operating with 1 W e.i.r.p. to maximize wave-crest penetration.
- Survival devices broadcast Navigational Status 14 in Message 1 alongside text strings in Message 14, triggering distinctive GMDSS cross-in-circle symbols and bridge alarms under IEC 62288.
- Recommendation ITU-R M.585-10 reserves dedicated identity spaces: `99MIDXXXX` for AtoN, `970` for SART, `972` for MOB, `974` for EPIRB-AIS, and extended 12-character identities (`97TXXMPPYYYY`).
- Proliferation of uncertified AIS fishing net buoys on maritime channels threatens the VDL through slot exhaustion and ECDIS display clutter; ITU-R M.2135 relegates non-safety AMRD Group B devices to Channel 2006 (160.900 MHz) with `979` pseudorandom identities.
- Maritime AIS and aeronautical ADS-B share historical roots in VDL Mode 4 but diverge fundamentally in PHY/MAC: AIS uses synchronized TDMA on VHF, whereas ADS-B 1090ES uses asynchronous stochastic ALOHA on UHF.

---

## References

- European Telecommunications Standards Institute (2019). *Maritime low power personal locating devices employing AIS; Harmonised Standard for access to radio spectrum* (Standard No. ETSI EN 303 098 V2.2.1). Sophia Antipolis, France: ETSI.
- Federal Communications Commission (2018). *FCC Enforcement Advisory: Marketing, Sale, and Use of Noncompliant Fishing Net Buoys is Illegal* (Enforcement Advisory No. DA 18-1210). Washington, DC: FCC Enforcement Bureau.
- International Association of Marine Aids to Navigation and Lighthouse Authorities (2017). *Management and Monitoring of AIS Information* (Guideline No. G1050). Saint-Germain-en-Laye, France: IALA.
- International Association of Marine Aids to Navigation and Lighthouse Authorities (2021). *The Use of the Automatic Identification System (AIS) in Marine Aids to Navigation Services* (Recommendation No. R0126, Edition 2.0). Saint-Germain-en-Laye, France: IALA.
- International Electrotechnical Commission (2010). *Global maritime distress and safety system (GMDSS) – Part 14: AIS search and rescue transmitter (AIS-SART) – Operational and performance requirements, methods of testing and required test results* (Standard No. IEC 61097-14:2010). Geneva, Switzerland: IEC.
- International Electrotechnical Commission (2016). *Maritime navigation and radiocommunication equipment and systems – Automatic identification systems (AIS) – Part 2: AIS AtoN stations – Minimum operational and performance requirements, methods of testing and required test results* (Standard No. IEC 62320-2:2016, Edition 2.0). Geneva, Switzerland: IEC.
- International Maritime Organization (2007). *Adoption of Performance Standards for Survival Craft AIS Search and Rescue Transmitters (AIS-SART) for Use in Search and Rescue Operations* (Resolution MSC.246(83)). Adopted 8 October 2007. London, UK: IMO.
- International Maritime Organization (2014). *Policy on Use of AIS Aids to Navigation* (Circular MSC.1/Circ.1473). Approved 23 May 2014. London, UK: IMO.
- International Telecommunication Union (2014). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band* (Recommendation ITU-R M.1371-5). Geneva, Switzerland: ITU Radiocommunication Sector.
- International Telecommunication Union (2023). *Technical characteristics of autonomous maritime radio devices operating in the frequency band 156–162.05 MHz* (Recommendation ITU-R M.2135-1). Geneva, Switzerland: ITU Radiocommunication Sector.
- International Telecommunication Union (2026). *Assignment and use of identities in the maritime mobile service* (Recommendation ITU-R M.585-10). Geneva, Switzerland: ITU Radiocommunication Sector.
- International Telecommunication Union (2026). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band* (Recommendation ITU-R M.1371-6). Geneva, Switzerland: ITU Radiocommunication Sector.
- Leonardi, M., Di Gregorio, L. & Di Fausto, F. (2017). Air Traffic Security: Aircraft Classification Using ADS-B Message Phase Patterns. *Aerospace*, 4(4):51. doi:10.3390/aerospace4040051.
- Radio Technical Commission for Maritime Services (2024). *Standard for Maritime Survivor Locating Devices (MSLD)* (Standard No. RTCM 11901.2). Arlington, VA: RTCM Special Committee 119.
- Strohmeier, M. & Martinovic, I. (2015). On Passive Data Link Layer Fingerprinting of Aircraft Transponders. In *Proceedings of the First ACM Workshop on Cyber-Physical System Security (CPS-SPC '15)*, pages 1–9. Denver, CO: ACM. doi:10.1145/2808705.2808712.
