# Chapter 24 — Timing in AIS

> **Part IV — The system: architecture and protocol.** How universal time coordinates the maritime radio link, driving slot synchronization from internal satellite receivers to distributed semaphore hierarchies, and how systems degrade when clocks drift or fail.

**In this chapter.** You will learn how precision timing underpins the entire Automatic Identification System (**AIS**) VHF Data Link (**VDL**). You will trace how Coordinated Universal Time (**UTC**) from internal Global Navigation Satellite System (**GNSS**) receivers carves radio spectrum into 2,250 synchronized 26.67-millisecond time slots per frame, examine the microsecond transmitter jitter budget, and master the five-tier synchronization hierarchy governing stations when direct satellite access is lost. You will explore the operational logic of base station timing, semaphore elections, and Class B carrier-sense fallback modes. You will dissect how time is transmitted over the air—contrasting the 6-bit position report time stamp from the SOTDMA communication state and full date-time broadcasts in Messages 4 and 11. Finally, you will investigate how equipment copes with GNSS denial, clock holdover, leap seconds, and week-number rollovers, evaluate network disruption threats, and audit time-stamp reconciliation in downstream telemetry pipelines.

## 24.1 Universal time and the TDMA frame architecture

The Automatic Identification System is a time-synchronized distributed radio network. Unlike terrestrial cellular systems that rely on authoritative central basestations or asynchronous packet networks like Ethernet that resolve contention after collisions occur, AIS operates autonomously across the open ocean without central arbiters. As introduced in [Chapter 20](ch20-architecture-and-station-classes.md) and [Chapter 21](ch21-link-layer-tdma.md), AIS shares two international maritime VHF channels—AIS 1 (161.975 MHz) and AIS 2 (162.025 MHz)—by dividing time into deterministic discrete intervals.

Under Recommendation ITU-R M.1371-6 Annex 2 (§A2-3.1.2), radio transmissions are organized into repeating **frames**, with one frame occurring every minute:
- Each frame lasts exactly 60 seconds (1 min).
- Each frame is partitioned into 2,250 **time slots**.
- Each slot spans $60 / 2250 = 0.026666...$ seconds, or exactly 26.67 milliseconds ($26rac{2}{3}	ext{ ms}$).
- Across the two parallel channels, a maritime cell offers 4,500 available slots per minute.

```
+-------------------------------------------------------------------------+
|                        ONE AIS FRAME (1 MINUTE)                         |
|                             60.0 SECONDS                                |
+-------------------------------------------------------------------------+
| Slot 0  | Slot 1  | Slot 2  | ...... | Slot 2248 | Slot 2249 |
| 26.67ms | 26.67ms | 26.67ms | ...... |  26.67ms  |  26.67ms  |
+---------+---------+---------+--------+-----------+-----------+
^                                                              ^
|                                                              |
UTC minute start                                   Next UTC minute
(Second 00.000)                                    (Second 00.000)
```

By default, access to the data link begins at the start of a slot. Under §A2-3.1.2, "The frame start and stop coincide with the UTC minute, when UTC is available." Slot 0 begins precisely at second 00.000 of every UTC minute, slot 1 begins at second 00.02667, slot 2 at second 00.05333, progressing continuously until slot 2249 begins at second 59.97333. When the next UTC minute rolls over, slot counting resets to 0.

At the standard physical-layer modulation rate of 9,600 bits per second (bit/s) with Gaussian Minimum Shift Keying (**GMSK**), one bit occupies:

$$T_{	ext{bit}} = rac{1}{9600	ext{ s}^{-1}} pprox 104.167\ \mu	ext{s}$$

Consequently, each 26.67 ms slot holds exactly 256 bit intervals ($26.6667	ext{ ms} / 0.104167	ext{ ms} = 256	ext{ bits}$). Every transmission burst must fit neatly within this 256-bit envelope without spilling over into neighboring slots.

## 24.2 The slot budget and transmission jitter

To prevent transmissions from colliding as RF energy propagates over water, the link layer allocates the 256 bits of a standard single-slot burst into distinct functional segments. Recommendation ITU-R M.1371-6 Figure 8 establishes the transmission timing timeline, breaking a slot down into specific events:
- **$T_0$ (0.000 ms, bit 0):** Transmitter power ramp-up initiates.
- **$T_{	ext{TS}}$ (0.833 ms, bit 8):** Synchronization training sequence begins (24 bits of alternating preamble `0101...`).
- **$T_1$ (1.000 ms, bit 9.6):** Transmitter RF power is stable at full nominal output (within +1.5 dB / −1 dB).
- **$T_2$ (3.333 ms, bit 32):** Start flag begins (`01111110`, 8 bits). Under ITU-R M.1371-6 §A2-3.2.2.10, "This event can be used as a secondary synchronization source should the primary source (UTC) be lost."
- **$T_S$ (4.167 ms, bit 40):** End of start flag. This event serves as the nominal **slot-phase synchronization marker**.
- **$T_3$ (24.167 ms, bit 232):** End of transmission burst, following data payload, 16-bit CRC Frame Check Sequence (**FCS**), end flag (`01111110`), and nominal bit stuffing.
- **$T_4$ ($T_3 + 1.0	ext{ ms}$):** Transmitter RF power ramp-down completes, dropping below −50 dBc.
- **$T_5$ (26.667 ms, bit 256):** End of time slot.

```
Slot Start                                                     Slot End
  T0     T1          T2    Ts                               T3    T4    T5
  |--RF--|--Train----|FLAG-|------- DATA PAYLOAD + CRC ------|--RF--|---GUARD---|
  0     9.6         32    40                               232   241.6 256 bits
  0.0   1.0        3.33  4.17                             24.17 25.17 26.67 ms
                           ^
                           |
                     Slot-phase sync
```

The difference between $T_3$ (bit 232) and $T_5$ (bit 256) defines a 24-bit **buffer** (spanning 2.50 ms) governed by §A2-3.2.2.8. This buffer absorbs three physical uncertainties:
1. **Bit stuffing allowance (4 bits):** The High-Level Data Link Control (**HDLC**) framing inserts a zero after any sequence of five consecutive ones. A standard position report can expand by several stuffed bits; 4 bits are budgeted.
2. **Distance propagation delay (14 bits):** Radio signals travel through the troposphere at approximately the speed of light ($c pprox 299,792	ext{ km/s}$, or $3.336\ \mu	ext{s/km} pprox 6.178\ \mu	ext{s/nmi}$). In 14 bit periods ($14 	imes 104.167\ \mu	ext{s} = 1.4583	ext{ ms}$), RF waves propagate:

$$d = 1.45833	imes 10^{-3}	ext{ s} 	imes 299,792	ext{ km/s} pprox 437.2	ext{ km} pprox 236.1	ext{ nautical miles}$$

Under §A2-3.2.2.8.2, this provides absolute protection for propagation ranges exceeding 120 nautical miles (nmi), preventing distant transmitters from intruding into the next slot of a local receiver.
3. **Synchronization jitter (6 bits):** Timing uncertainties at the transmitter, equal to $6 	imes 104.167\ \mu	ext{s} = 625\ \mu	ext{s}$.

Transmitter timing precision is tightly circumscribed by ITU-R M.1371-6 §A2-3.2.2.8.3. A mobile station must lock its transmission timing to its synchronization source within $\pm 104\ \mu	ext{s}$ ($\pm 1$ bit period). Because timing errors can accumulate when one station synchronizes to another, the standard establishes an upper bound on accumulated jitter:

$$\Delta t_{	ext{accum, mobile}} \le 312\ \mu	ext{s} \quad (\pm 3	ext{ bit periods})$$

For base stations, whose antenna elevations cover wide radio horizons and whose transmissions discipline other nodes, the requirements are twice as stringent: timing error must remain within $\pm 52\ \mu	ext{s}$ ($\pm 0.5$ bits), with maximum accumulated jitter capped at $\pm 104\ \mu	ext{s}$ ($\pm 1$ bit). Emergency locating devices, including AIS-SARTs, MOB beacons, and EPIRB-AIS operating under Annex 8, are granted a timing error budget of $\pm 312\ \mu	ext{s}$ ($\pm 3$ bits) during direct UTC synchronization.

> **Worked example.** Calculating propagation delay and jitter margin.
> Consider a Class A transponder aboard a ship located 45 nmi (83.34 km) from a coastal receiver. The propagation delay of the VHF signal is:
> $$t_{	ext{prop}} = rac{83,340	ext{ m}}{2.99792 	imes 10^8	ext{ m/s}} = 277.99\ \mu	ext{s} pprox 2.67	ext{ bit periods}$$
> If the transmitting ship has direct UTC lock with a transmission jitter of $+80\ \mu	ext{s}$ (+0.77 bits), the signal arrives at the receiver's antenna with a total phase delay of $277.99 + 80 = 357.99\ \mu	ext{s}$ relative to slot start. The receiver's slot-phase detector locks onto the end of the start flag ($T_S$) at bit 40. Because the nominal 24-bit buffer reserves 14 bits (1,458.3 $\mu	ext{s}$) for propagation delay and 6 bits (625 $\mu	ext{s}$) for jitter, the arrival delay of $357.99\ \mu	ext{s}$ consumes only 3.44 bits of the 20-bit combined margin. Even with an extreme 4-bit bit-stuffing penalty, the RF energy terminates safely 16.56 bit periods before the start of the subsequent slot.

## 24.3 The synchronization hierarchy

How does a mobile or shore transponder know when slot 0 begins? When satellite signals are available, every station locks to celestial atomic clocks. But when GNSS signals are obstructed or jammed, an alternative synchronization mechanism is required. 

To maintain network coherence without central supervision, ITU-R M.1371-6 defines an autonomous **synchronization hierarchy**. The Link Management Entity (**LME**) tracks its available time sources and continuously assigns itself one of five standardized operational sync states, summarized in Table 24-1.

| Priority | Synchronization State | Over-the-air Code | Usable as Sync Source? | Description |
|:---:|---|:---:|:---:|---|
| 1 | **UTC direct** | `0` | Yes | Direct access to UTC via operational internal GNSS clock |
| 2 | **UTC indirect** | `1` | No | Synchronized to a station that is operating UTC direct |
| 3 | **Base direct** | `2` | Yes | Synchronized to a qualified base station |
| 4 | **Base indirect** | `3` | No | Synchronized to a station that is operating Base direct |
| 5 | **Mobile semaphore** | `3` | No | Synchronized to a mobile station acting as a semaphore |

*Table 24-1: The five-level AIS synchronization hierarchy under ITU-R M.1371-6 Table 9.*

```
                 [ UTC GNSS Satellites ]
                            |
                            v
               +--------------------------+
               | 1. UTC Direct (Code 0)   | <----+ (Free-running base
               +-------------+------------+      |  with atomic/PTP clock)
                             |
         +-------------------+-------------------+
         |                                       |
         v                                       v
+--------------------------+           +--------------------------+
| 2. UTC Indirect (Code 1) |           | 3. Base Direct (Code 2)  |
|  (Cannot be sync source) |           +-------------+------------+
+--------------------------+                         |
                                                     v
                                       +--------------------------+
                                       | 4. Base Indirect (Code 3)|
                                       |  (Cannot be sync source) |
                                       +--------------------------+
                                                     |
                                                     v
                                       +--------------------------+
                                       | 5. Mobile Semaphore      |
                                       |    (Code 3, terminal)    |
                                       +--------------------------+
```

### 24.3.1 UTC direct (Code 0)
A station with direct access to UTC timing that meets the $\pm 104\ \mu	ext{s}$ accuracy requirement must set its synchronization state to **UTC direct** (`00` binary). Under normal operational conditions, virtually all commercial Class A and Class B transponders occupy this state, slaved to internal GNSS receivers. A station in UTC direct acts as an authoritative timing beacon for the entire cell.

### 24.3.2 UTC indirect (Code 1)
When a station loses its direct UTC source (e.g., antenna failure or GNSS outage), it searches for surrounding stations transmitting with sync state `0` (UTC direct). Under §A2-3.1.1.2, it locks its slot phase to those transmissions and announces its sync state as **UTC indirect** (`01` binary). 

Crucially, the standard enforces a strict **one-level-of-indirection rule**: "Only one level of UTC indirect synchronization is allowed." A station operating in UTC indirect cannot serve as a timing reference for other stations. This rule prevents open-loop timing drift from cascading across the ocean: error cannot accumulate beyond the single hop's 312 $\mu	ext{s}$ jitter envelope.

### 24.3.3 Base direct (Code 2)
If no UTC direct or UTC indirect stations can be heard, but a shore base station is received, the mobile station transitions to **Base direct** (`10` binary). Under §A2-3.1.1.3, the mobile locks to the base station that indicates the highest number of received stations, provided that at least two reports have been received from that base within the preceding 40 seconds. If two or more base stations report identical station counts, the station with the numerically lowest Maritime Mobile Service Identity (**MMSI**) breaks the tie.

Base direct stations *are* permitted to serve as a synchronization source for neighboring units that cannot receive the shore station directly.

### 24.3.4 Base indirect (Code 3)
A station unable to hear a base station directly, but receiving a station operating in Base direct, transitions to **Base indirect**. Under §A2-3.1.1.3, only one level of indirect access to the base station is permitted. Because the SOTDMA communication state dedicates only 2 bits to sync state, Base indirect shares the binary code `11` (decimal 3) over the air.

### 24.3.5 Mobile as semaphore (Code 3)
If a group of vessels finds itself completely cut off from GNSS signals and shore infrastructure (for example, in a remote polar archipelago or an electronic-warfare jamming corridor), the vessels must coordinate their TDMA frame to avoid destructive mutual interference. In this isolated state, a designated mobile station steps forward as a **semaphore station**.

The LME continuously evaluates candidates using the semaphore qualification rules in ITU-R M.1371-6 Tables 10 and 11:
- A mobile station may qualify as a semaphore only if its own current sync state is UTC direct or Base direct, and the highest sync state received from any neighbor (excluding its own synchronization parent) is state 3 (indirect).
- When multiple mobile stations qualify, the election is governed by a deterministic rule: the candidate reporting the highest number of other stations received during the last nine frames wins. If station counts are equal, the candidate with the numerically lowest MMSI becomes the semaphore.
- A mobile semaphore adopts sync code 3 over the air, identical to Base indirect.

Under §A2-3.1.3.3.2, a mobile station serving as a semaphore increases its transmission rate, broadcasting its position report using the `MAC.SyncMobileRate` parameter (once every 2 seconds) to keep surrounding vessels locked. Mobile stations synchronizing to the semaphore cannot be used as sources by anyone else.

> **Definitions that bite.** Sync state 3 ambiguity on the wire.
> The SOTDMA and ITDMA communication states allocate exactly 2 bits to the `Sync state` field: `0` = UTC direct, `1` = UTC indirect, `2` = Base direct, and `3` = Base indirect *or* Mobile semaphore. In decoded NMEA sentences, code 3 is ambiguous. Without tracking preceding frames and correlating transmitter IDs against station directories, a data parser cannot distinguish whether a vessel reporting sync state 3 is an offshore ship relaying base station timing or an isolated vessel locked to a mobile semaphore.

## 24.4 Base stations and master timing sources

Shore base stations play an architectural role in regional AIS cells. Under IEC 62320-1 and ITU-R M.1371-6, base stations anchor slot timing for vessel traffic services (**VTS**), execute channel management, and broadcast authoritative system information.

A standard base station is equipped with an internal multi-GNSS receiver providing sub-microsecond pulse-per-second (**1PPS**) discipline. Base stations are subject to a jitter budget of $\pm 52\ \mu	ext{s}$ ($\pm 0.5$ bits), half that of mobile stations. Furthermore, modern coastal base stations (such as the Saab R60 VDES basestation) feature external frequency and time inputs:
- **1PPS and IRIG-B:** Coaxial inputs accepting 1 pulse-per-second and Inter-Range Instrumentation Group time code format B signals from station master atomic standards (rubidium or caesium clocks).
- **Network Time Protocol (NTP) and PTP (IEEE 1588):** High-precision network timing interfaces that discipline transponder slots across land-based wide-area networks even if local GNSS antennas fail.

```
+------------------------------------------------------------------------+
|                          AIS BASE STATION                              |
|                                                                        |
|  +--------------------+  1PPS  +------------------+                    |
|  | Internal Multi-GNSS|------->|                  |                    |
|  +--------------------+        |  Base TDMA Slot  |    VHF Burst       |
|  +--------------------+ 1PPS/  |    Controller    |------------------> |
|  | Atomic / PTP Clock |------> | (±52 µs jitter)  | (Message 4 / 11)   |
|  +--------------------+ IRIG-B +------------------+                    |
+------------------------------------------------------------------------+
```

Under ITU-R M.1371-6 §A2-3.1.3.3.1, a base station that loses its primary UTC reference may qualify to operate as a base semaphore. While acting as a semaphore, the base accelerates its Message 4 broadcasts to the `MAC.SyncBaseRate`—transmitting once every $3rac{1}{3}$ seconds (three times per 10-second interval)—to stabilize the regional link until the outage clears or fallback time-outs elapse (typically 3 minutes).

## 24.5 How time is represented in AIS messages

Time data travels across the VHF link through three completely distinct mechanisms, serving different protocols, precisions, and update rates.

```
+-------------------------------------------------------------------------+
|                  THREE TIME SCALES IN AIS TRANSMISSIONS                 |
+-------------------------------------------------------------------------+
| Scale 1: Position Report Time Stamp (Messages 1, 2, 3, 18)              |
| 6 bits | Range 0–59 (seconds), 60 (n/a), 61 (manual), 62 (DR), 63 (bad) |
| Carries: Second of fix generation. NO minute, NO hour, NO date.         |
+-------------------------------------------------------------------------+
| Scale 2: SOTDMA Communication State (Sub-message when Time-out = 1)     |
| 14 bits | Bits 13-9: UTC Hour (0–23) | Bits 8-2: UTC Minute (0–59)      |
| Carries: Hour and minute of current slot. NO second, NO date.           |
+-------------------------------------------------------------------------+
| Scale 3: Base Station / UTC Inquiry (Messages 4 and 11)                 |
| 168 bits total | Year (14b), Month (4b), Day (5b), Hour (5b), Min (6b), |
|                 Sec (6b), Position, Comm State                          |
| Carries: Full calendar date and UTC timestamp down to the second.       |
+-------------------------------------------------------------------------+
```

### 24.5.1 The 6-bit position report time stamp
Every standard Class A position report (Messages 1, 2, 3) and Class B position report (Message 18) contains a 6-bit `Time stamp` field. It represents the **UTC second** when the navigation sensor generated the position fix:
- Values **0–59:** Valid UTC second of fix acquisition.
- Value **60:** Time stamp not available (the default power-up condition).
- Value **61:** Positioning system operating in manual input mode.
- Value **62:** Positioning system operating in estimated (dead reckoning) mode.
- Value **63:** Electronic position-fixing system (**EPFS**) is inoperative.

This field does not convey the minute, hour, or date. It does not even convey the time the radio burst was scheduled; rather, it records the sensor sampling epoch. If an external GNSS receiver computes a fix at second 14.2 and latency delays transmission until slot 600 (second 16.0), the time stamp field reads `14`.

### 24.5.2 The SOTDMA communication-state UTC sub-message
The 19-bit SOTDMA communication state embedded in position reports carries dynamic link-scheduling parameters. As detailed in [Chapter 21](ch21-link-layer-tdma.md), the 3-bit `Slot time-out` field decrements from frame to frame ($7 	o 6 	o ... 	o 0$). The meaning of the 14-bit `Sub-message` field rotates based on the time-out value:
- When time-out is 3, 5, or 7: sub-message contains `Received stations`.
- When time-out is 2, 4, or 6: sub-message contains `Slot number` (0–2249).
- **When time-out is 1:** sub-message carries **UTC hour and minute**:
  - Bits 13–9 (5 bits): UTC hour (0–23; values 24–31 indicate not available).
  - Bits 8–2 (7 bits): UTC minute (0–59; values 60–127 indicate not available).
  - Bits 1–0: Reserved spare bits.
- When time-out is 0: sub-message carries `Slot offset`.

Every several frames, when time-out hits 1, a mobile station broadcasts its current UTC hour and minute across the data link.

### 24.5.3 Message 4 and Message 11
Fixed base stations broadcast **Message 4** periodically (nominally every 10 seconds), providing an authoritative reference for the entire cell. In addition, mobile stations transmit **Message 11** when interrogated by a base station via **Message 10** (UTC/Date Inquiry).

Under ITU-R M.1371-6 Table 49, Messages 4 and 11 transmit a 168-bit packet containing a complete, uncompressed calendar timestamp:
- **UTC Year:** 14 bits (1–9999; 0 = not available).
- **UTC Month:** 4 bits (1–12; 0 = not available).
- **UTC Day:** 5 bits (1–31; 0 = not available).
- **UTC Hour:** 5 bits (0–23; 24 = not available).
- **UTC Minute:** 6 bits (0–59; 60 = not available).
- **UTC Second:** 6 bits (0–59; 60 = not available).

Surrounding vessels use Message 4 to confirm the date and calibrate their internal clocks. Furthermore, under §A7-3.2, receiving Message 4 allows a mobile station to compute its geometric range to the shore station, verifying whether it lies within the 120 nmi radius required to obey assignment commands from Messages 20 and 23.

## 24.6 Equipment requirements: the internal GNSS mandate

A widespread misconception across maritime software engineering is that Class A transponders take their time from the vessel's primary navigation suite over NMEA 0183 (`$GPGGA` or `$GPRMC` sentences). In reality, the regulatory framework strictly mandates an **internal GNSS receiver** dedicated to slot timing.

The origin of this requirement reflects the layered nature of international maritime regulation:
1. **IMO Resolution MSC.74(69) Annex 3:** The fundamental IMO performance standard for shipborne AIS defines required components (communications processor, sensor inputs, BITE, display) and lists dynamic data as "Time in UTC" with footnote: "*Date to be established by receiving equipment.*" MSC.74(69) does not mention slots, TDMA, or internal satellite engines; it explicitly delegates radio technical specifications to the ITU.
2. **IMO Resolution A.1106(29):** The IMO operational guidelines note in Annex paragraph 1 that an onboard Class A installation comprises antennas, transmitters, receivers, and "an electronic position-fixing system, Global Navigation Satellite System (GNSS) receiver for timing purposes and position redundancy."
3. **ITU-R M.1371-6:** Specifies the radio timing characteristics, demanding direct access to UTC within $\pm 104\ \mu	ext{s}$. While Annex 2 is technically source-neutral for Class A, Annex 6 (§A6-3.1) explicitly mandates an internal GNSS engine for Class B "CS" transponders.
4. **IEC 61993-2 (Class A) & IEC 62287-1/2 (Class B):** The type-approval standards cement the requirement. Under IEC 61993-2, an AIS transponder must contain an internal GNSS receiver. Even when a vessel connects an external bridge DGNSS sensor supplying sub-meter navigation fixes over IEC 61162-1, the transponder must derive its slot timing exclusively from its internal GNSS core. If the external bridge navigator fails, the transponder falls back to its internal engine for position reporting, flagging the change in the position report.

```
+---------------------------------------------------------------------+
|                      SHIPBORNE AIS ARCHITECTURE                     |
|                                                                     |
|  External Ship's Bridge EPFS                                        |
|  (DGNSS / INS / ECDIS)                                              |
|            |                                                        |
|            | IEC 61162-1 (NMEA 0183)                                |
|            v                                                        |
|  +---------------------------------------------------------------+  |
|  | CLASS A TRANSPONDER                                           |  |
|  |                                                               |  |
|  |  +--------------------+   Nav Data                            |  |
|  |  | External EPFS Port |------------+                          |  |
|  |  +--------------------+            |                          |  |
|  |                                    v                          |  |
|  |  +--------------------+  1PPS  +--------------+   VHF Burst   |  |
|  |  | Internal GNSS Core |------->| TDMA Frame   |-------------> |  |
|  |  | (Mandatory Timing) |        | Controller   | (GMSK 9600)   |  |
|  |  +--------------------+        +--------------+               |  |
|  |                                                               |  |
|  +---------------------------------------------------------------+  |
+---------------------------------------------------------------------+
```

## 24.7 Stations without GNSS or without VHF receivers

While standard shipborne transponders combine VHF transceivers with internal GNSS receivers, several specialized classes intentionally omit one or both components:

1. **Aids to Navigation (AtoN) Type 1:** Standardized under IEC 62320-2, an **AtoN Type 1** is a transmit-only navigational marker installed on inexpensive buoys. To minimize power consumption and hardware cost, Type 1 AtoN units omit the VHF receiver entirely. Because they cannot monitor the channel, they cannot run SOTDMA or detect neighbor sync states. Instead, they transmit via Fixed Access Time Division Multiple Access (**FATDMA**) in slots pre-reserved by coastal authorities. Although they have no VHF receiver, they retain an internal GNSS engine to maintain direct UTC synchronization (IEC 62320-2 Table 1).
2. **Receive-only AIS units:** Deployed at shore monitor sites, coastal research stations, and small recreational craft, receive-only stations contain VHF receivers but no transmitter. Under ITU-R M.1371-6 §A2-3.1.1, the AIS reception process is not slot synchronized: an AIS receiver continuously samples the discriminator output and bitstream, locking onto the 24-bit training preamble and start flag whenever a packet arrives. Receive-only stations require no GNSS clock discipline to decode the VDL.
3. **Shore base stations with atomic holdover:** Specialized base stations in secure coastal networks can operate without active GNSS satellite reception by slaving their TDMA controllers to external caesium/rubidium atomic frequency standards or PTP time servers over terrestrial fibre networks.

## 24.8 Clock degradation, drift, and transmission cessation

What happens when an operational transponder loses its GNSS satellite lock? Clock degradation proceeds through three deterministic phases:

1. **Phase 1: Internal holdover (0 to ~30 seconds).** The transponder's internal crystal oscillator (typically a Temperature-Compensated Crystal Oscillator, **TCXO**, or Oven-Controlled Crystal Oscillator, **OCXO**) free-runs, maintaining slot phase. Because oscillator drift accumulates error ($\Delta t = \int rac{\Delta f}{f} dt$), standard uncalibrated crystals drift out of the $\pm 104\ \mu	ext{s}$ window within seconds.
2. **Phase 2: Indirect synchronization fallback.** If GNSS lock cannot be re-established, the LME steps down the synchronization hierarchy. If a UTC direct station is received, the unit adopts sync state 1 (UTC indirect), resetting its slot phase on incoming start flags. If a base station is present, it transitions to Base direct (state 2).
3. **Phase 3: Class-specific degradation and cessation.**
   - **Class A:** If isolated from all sync sources, Class A transponders may elect a mobile semaphore. If timing drift exceeds operational thresholds and no valid sync source can be acquired, the station transitions its EPFS sensor status to code 63 (inoperative). Under IEC 61993-2 testing, transponders must cease transmitting autonomous position reports if timing certainty cannot guarantee slot alignment.
   - **Class B "CS" (CSTDMA):** Governed by IEC 62287-1 and ITU-R M.1371-6 Annex 6, Class B units do not maintain a predictive slot map. They require slot phase only to align their 8-bit carrier-sense detection window. If a Class B CS transponder loses direct UTC, it falls back to listening for incoming bursts (Sync Mode 2). If no sync frames are heard for 30 seconds, it free-runs on its internal clock. If satellite lock is not recovered within 360 minutes (6 hours), the transponder ceases transmission of Messages 18 and 24 entirely.

## 24.9 Network disruption and timing attacks

The open, unauthenticated nature of the AIS radio link makes timing mechanisms a target for electronic interference and denial-of-service (**DoS**) attacks.

In 2014, Marco Balduzzi, Alessandro Pasta, and Kyle Wilhoit evaluated VHF link vulnerabilities. They demonstrated that while commercial transponders enforce rigid state machines, those state machines can be exploited if an attacker broadcasts fabricated link-management commands using Software-Defined Radios (**SDRs**):

```
+------------------------------------------------------------------------+
|                 DISRUPTION MECHANISMS ON THE WIRE                      |
+------------------------------------------------------------------------+
| 1. Slot Starvation (Messages 4 + 20)                                   |
| Attacker masquerades as coastal base station via Msg 4, then issues    |
| Msg 20 (Data Link Management) reserving all 2,250 slots. Nearby mobile |
| stations vacate slots, resulting in complete regional denial.          |
+------------------------------------------------------------------------+
| 2. Transmission Delay / Quiet Time (Message 23)                        |
| Attacker sends Message 23 (Group Assignment Command) specifying a      |
| "Quiet Time" of up to 15 minutes. Receiving stations are forced into   |
| radio silence, concealing vessels from local VTS tracking.             |
+------------------------------------------------------------------------+
| 3. Dynamic Rate Flooding (Message 16)                                  |
| Attacker issues Message 16 (Assigned Mode) commanding high-frequency   |
| reporting (e.g. every 2 s) for distant vessels, exhausting cell slots. |
+------------------------------------------------------------------------+
```

Although frequently cited as "timing attacks," these exploits manipulate link-layer scheduling commands rather than distorting the transponder's internal physical clock. 

Under the ITU-R M.1371-6 standard, several structural barriers limit the impact of these attacks:
- **Priority of UTC direct:** A mobile station with an operational internal GNSS receiver (sync state 0) *never* re-synchronizes its physical slot clock to an external base station. Priority 1 is strictly reserved for the internal engine (§A2-3.1.3.4.3). A spoofed Message 4 cannot shift the physical slot boundary of a vessel with healthy satellite lock.
- **Quiet time bounds:** Under §A7-3.15, Message 23 quiet time is restricted to a maximum of 15 minutes.
- **AtoN immunity:** Under IEC 62320-2 Table 1, AIS Aids to Navigation ignore assignment Messages 16 and 23 completely.
- **Reversion time-outs:** Base station slot reservations and regional channel assignments automatically time out after 3 minutes if not continuously refreshed.

> **Threat model.** Spoofed base station timing and slot starvation.
> - **Attacker:** Malicious shore or shipborne actor equipped with an inexpensive SDR (e.g. HackRF, USRP) and a 10 W VHF power amplifier.
> - **Capability:** Transmission of arbitrary AIS frames, forged Message 4 base station broadcasts, and forged Message 20/23 reservation sentences.
> - **Impact:** Denial of service across a coastal cell by commanding mobile stations to silence transmissions or abandon standard channels.
> - **Mitigation:** Marine receivers and VTS monitors must enforce cryptographic message authentication (e.g. Protected AIS or PKI digital signatures), flag base stations appearing at invalid geographic coordinates, and reject Message 20 reservation bursts from unverified base station MMSIs.

> **Legal note.** Radio transmission and interference.
> Operating a radio transmitter on maritime VHF frequencies without a valid station license issued by a competent national authority (such as the FCC in the United States or Ofcom in the United Kingdom) is unlawful under national telecommunications legislation and the ITU Radio Regulations. Deliberately broadcasting spoofed AIS base station messages, jamming GNSS frequencies, or manipulating maritime safety signals constitutes a serious maritime offense under international law, violating the Safety of Life at Sea (SOLAS) Convention and domestic criminal statutes.

## 24.10 Leap seconds and GPS week-number rollovers

Precision timing depends on the mathematical relationship between the celestial timescale (UTC) and the continuous atomic timescale maintained by satellite constellations. Divergences between these timescales have triggered severe real-world AIS failures.

```
GPS Time: Continuous atomic timescale (starts 1980-01-06, zero leap seconds)
UTC Time: Stepped astronomical timescale (intercalary leap seconds inserted)
Offset:   GPS Time - UTC Time = +18 seconds (as of 2026)
```

The GPS navigation message broadcasts the current leap-second offset in its subframe almanac data. If a transponder's firmware or GNSS receiver mishandles this offset, the device calculates an erroneous UTC minute boundary.

> **Case file.** The 2005 Saab R3/R4 leap-second fault.
> On 31 December 2005, the International Earth Rotation and Reference Systems Service (**IERS**) inserted a positive leap second into UTC at 23:59:60. In early 2005, the GPS constellation transmitted an advance notification flag warning receivers of the upcoming event. 
> 
> Due to a software flaw in the internal GPS engine deployed across thousands of Saab TransponderTech R3 and R4 Class A transponders, the receiver applied the announced 1-second correction immediately upon receiving the advisory flag—months before the actual leap second occurred. The internal receiver shifted its internal UTC calculation by exactly 1.0 second.
> 
> In the AIS slot structure, 1.0 second corresponds to:
> $$1.0	ext{ s} 	imes rac{2250	ext{ slots}}{60	ext{ s}} = 37.5	ext{ slots}$$
> Rather than shifting slot timing by an integer slot count, the 37.5-slot offset placed the transponder's transmission burst directly across the boundary between two adjacent slots (a half-slot phase offset of 13.33 ms). Each burst occupied the tail end of one slot and the front end of the next. 
> 
> The consequences were documented in Saab Technical Bulletin PT-05-0078, Norwegian Maritime Authority Safety Message SM 10/2005, and USCG Marine Safety Alert 5-05:
> - Receiving stations detected corrupted CRC frame check sequences due to colliding transmissions.
> - While transponders with wide reception buffers decoded some bursts, older coastal base stations discarded the misaligned packets entirely.
> - Because traffic density in 2005 was moderate, the transponders degraded gracefully without collapsing regional cells, prompting Saab to note that users had not reported catastrophic failures even in busy waters. Saab rapidly distributed firmware patches to correct the GPS leap-second parsing logic.

A second temporal hazard stems from the **GPS Week Number Rollover (WNRO)**. In legacy GPS civil navigation messages (LNAV), the week counter is represented as a 10-bit integer, rolling over from week 1023 to 0 every 1,024 weeks (approximately 19.6 years). Rollovers occurred in August 1999 and April 2019, with the next scheduled for November 2038.

Older AIS models whose firmware hardcoded epoch lookup tables experienced rollover anomalies:
- **Furuno FA-100:** Experienced an internal GPS rollover on 20 December 2020. The transponder maintained slot-phase timing and communication links, but its internal date reverted, corrupting transmitted log timestamps and voyage logs.
- **Furuno FA-150:** Encountered rollover on 2 January 2022, resolved via firmware update v4.07.
- **Japan Radio Company (JRC):** Several legacy transponders rolled their epoch back 19.6 years on 15 May 2022, causing scheduled transmissions and automated reporting to falter.

## Then & now

- **⟨H⟩ 1998:** IMO adopts Resolution MSC.74(69) Annex 3, defining performance standards for universal shipborne AIS; delegates radio timing specifications entirely to ITU-R.
- **⟨H⟩ 2001:** ITU-R M.1371-0 establishes the 2,250-slot TDMA frame, locking slot 0 to the UTC minute boundary with a 24-bit guard buffer.
- **⟨+⟩ 2005:** The Saab R3/R4 leap-second defect demonstrates the hazard of internal GPS firmware bugs, causing transmitters to shift by 37.5 slots (half-slot phase offset).
- **⟨+⟩ 2006:** IEC 62287-1 standardizes Class B CSTDMA, creating polite carrier-sensing that relies on slot-phase listening rather than global slot maps.
- **⟨+⟩ 2014:** Trend Micro security research demonstrates link-layer availability disruption (Messages 16, 20, 22, 23) using software-defined radios.
- **⟨+⟩ 2015:** IMO adopts Resolution A.1106(29), formally incorporating guidelines identifying internal GNSS as necessary for timing and position redundancy.
- **⟨+⟩ 2018:** IEC 61993-2 Edition 3 refines Class A type-approval testing, enforcing strict internal GNSS slot discipline under simulated satellite denial.
- **⟨+⟩ 2019:** The second GPS 10-bit week-number rollover passes without catastrophic network failure, though several legacy transponders suffer date corruption.
- **⟨+⟩ 2026:** Recommendation ITU-R M.1371-6 formalizes synchronization and slot timing rules for modern digital maritime operations.

## On the wire

Let us examine how timing data appears across actual raw NMEA 0183 sentences broadcast over the VHF Data Link.

### Reading the 6-bit time stamp
Consider a standard Class A position report (Message 1) received from vessel `367123450`:

```text
!AIVDM,1,1,,A,15MwpU@01prtlJ0H9J@<Can00000,0*27
```

Decoding the first 6-bit ASCII character sequence reveals:
- Message type: `000001` (1 = Position Report Class A).
- Repeat indicator: `00` (0).
- MMSI: `367123450`.
- Navigation status: `0000` (0 = Under way using engine).
- Bits 137–142 encode the `Time stamp` field: binary `011110` = decimal **30**.

This indicates the onboard navigation sensor generated this positional fix at precisely second **30** of the UTC minute. The sentence carries no day, hour, or minute.

### Reading UTC in the SOTDMA communication state
When an SOTDMA position report is transmitted with `Slot time-out` equal to 1, the 14-bit sub-message reveals the UTC hour and minute. Consider the raw sentence:

```text
!AIVDM,1,1,,A,153BqUP02lrsFtDH>QITa3d60000,0*04
```

Extracting the 19-bit communication state (bits 149–167):
- **Sync state (bits 149–150):** `00` (0 = UTC direct). The vessel possesses valid satellite lock.
- **Slot time-out (bits 151–153):** `001` (1 = Sub-message carries UTC hour/minute).
- **Sub-message (bits 154–167):**
  - Bits 154–158 (5 bits): `01110` = decimal **14** (UTC Hour: 14:00).
  - Bits 159–165 (7 bits): `100101` = decimal **37** (UTC Minute: :37).
  - Bits 166–167 (2 bits): `00` (Spare).

The vessel reports that the transmission occurred during the **14:37 UTC** minute.

### Complete calendar timestamp: Message 4
Fixed base stations transmit complete calendar dates using Message 4:

```text
!AIVDM,1,1,,A,403Ovl1v`Gd00rs=oPH?A@700000,0*32
```

Decoding the 168-bit binary payload:
- **Message Type (bits 0–5):** `000100` (4 = Base Station Report).
- **MMSI (bits 8–37):** `003669999` (US Coast Guard Base Station).
- **UTC Year (bits 38–51):** `00011111101000` = decimal **2024**.
- **UTC Month (bits 52–55):** `1010` = decimal **10** (October).
- **UTC Day (bits 56–60):** `00110` = decimal **6**.
- **UTC Hour (bits 61–65):** `01110` = decimal **14**.
- **UTC Minute (bits 66–71):** `100101` = decimal **37**.
- **UTC Second (bits 72–77):** `000000` = decimal **00**.
- **Position:** Latitude $37^\circ 48.1234'	ext{ N}$, Longitude $122^\circ 24.5678'	ext{ W}$.
- **SOTDMA Comm State:** Sync state `0` (UTC direct), maintaining regional timing discipline.

## Validation, uncertainty & data quality

Because AIS position reports carry only a 6-bit time stamp representing the sensor fix second, reconstructing reliable chronological records presents profound data-quality challenges:

```
Vessel GNSS Fix  ------>  Transponder Queue  ------>  VHF Broadcast  ------>  Shore Receiver  ------>  Database Ingest
(Generates Sec 14)        (SOTDMA Latency)            (Slot Second 16)        (NMEA TAG Block)         (Server Wall Clock)
```

Data pipelines frequently encounter three categories of timing error:
1. **The 1-minute ambiguity:** If an AIS message is logged without an external reception timestamp, the 6-bit time stamp can only resolve time modulo 60 seconds. A report with time stamp `45` could belong to 12:00:45, 12:01:45, or any other minute.
2. **Sentinel value corruption:** Novice parsers frequently treat time stamp values 60, 61, 62, and 63 as numeric seconds, introducing artificial 60-second spikes into track smoothing filters. Values $\ge 60$ must be parsed as status sentinels (60 = unavailable, 61 = manual, 62 = estimated, 63 = failed).
3. **Sensor-to-slot latency:** Transponders buffer position fixes while waiting for their assigned transmission slot. Under high speeds, a 2-second buffer delay between fix generation and slot transmission creates significant positional offsets:

$$\Delta s = v 	imes \Delta t = 24	ext{ kn} 	imes 2	ext{ s} pprox 12.35	ext{ m/s} 	imes 2	ext{ s} = 24.7	ext{ m}$$

When evaluating track accuracy, telemetry pipelines must calibrate kinematic models using the sensor's 6-bit fix second rather than the receiver's ingestion timestamp.

> **Try it.** Parsing NMEA 4.10 TAG blocks and validating AIS time stamps.
> The following script parses a stream of raw AIS messages with NMEA 4.10 TAG blocks (using `code/decode/tagblock.py`), validates the TAG block UNIX timestamp against the 6-bit fix second, and flags sensor status sentinels.
>
> ```python
> import datetime
> from code.decode.tagblock import parse_line
> 
> # Sample synthetic log line from data/samples/synthetic_harbor.nmea
> raw_log = r"\s:SYNTH01,c:1768478410*63\!AIVDM,1,1,,A,15MwpU@01prtl@4H9K;<FapD0000,0*3C"
> 
> tag, sentence = parse_line(raw_log)
> if tag and tag.checksum_ok:
>     rx_time = datetime.datetime.fromtimestamp(tag.unix_time, tz=datetime.timezone.utc)
>     print(f"Receiver Station : {tag.source}")
>     print(f"Logged UTC Time  : {rx_time.strftime('%Y-%m-%d %H:%M:%S')}")
>     print(f"Sentence         : {sentence}")
> ```
>
> **Expected output:**
> ```text
> Receiver Station : SYNTH01
> Logged UTC Time  : 2026-01-15 12:00:10
> Sentence         : !AIVDM,1,1,,A,15MwpU@01prtl@4H9K;<FapD0000,0*3C
> ```

## Software

Precision timing in AIS interfaces spans specialized embedded decoders, network synchronizers, and analytical pipelines:

**Open source:**
- **libais:** High-performance C++ decoder with Python bindings developed by Kurt Schwehr. Decodes binary communication states, extracts SOTDMA/ITDMA sync state bits, and parses full calendar structures in Messages 4 and 11. *Caveat:* Reconstructing full timestamps from Messages 1–3 requires downstream ingestion clocks; libais does not fabricate missing date fields.
- **gpsd:** System daemon that monitors GPS sensors and AIS receivers. Extracts NMEA sentences, decodes AIVDM packets, and aligns sensor fixes with host system time. *Caveat:* Ingestion latency across serial or USB-to-UART bridges can introduce millisecond-level timestamp jitter.
- **gr-ais:** GNU Radio out-of-tree block for software-defined radio reception of AIS. Implements GMSK demodulation and packet synchronization. *Caveat:* Requires calibrated SDR hardware oscillators; standard RTL-SDR dongles suffer substantial frequency ppm offset and timing drift.

**Free but closed:**
- **OpenCPN:** Chartplotting and navigation software displaying real-time AIS targets. Correlates received position reports with local system time to compute Closest Point of Approach (**CPA**). *Caveat:* Target lost-contact time-outs rely on host OS wall clocks, which may drift if not NTP-synchronized.

**Commercial:**
- **Saab R60 VDES Base Station Software:** Commercial shore infrastructure controller managing regional TDMA slot allocations. Supports 1PPS, IRIG-B, and IEEE 1588 PTP network synchronization with atomic clock fallback. *Caveat:* Proprietary hardware and protocol management interfaces require vendor licensing.

## Standards & guides

- **International Telecommunication Union (ITU-R):** *Recommendation ITU-R M.1371-6 (2026)* — Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band. Governs frame structure (§A2-3.1), slot timing and jitter budgets (§A2-3.2.2), synchronization hierarchy (§A2-3.1.3), communication states (§A2-3.3.7), and message layouts (§A7).
- **International Maritime Organization (IMO):** *Resolution MSC.74(69), Annex 3 (1998)* — Recommendation on performance standards for a universal shipborne Automatic Identification System (AIS). Establishes carriage requirements and basic functional architecture.
- **International Maritime Organization (IMO):** *Resolution A.1106(29) (2015)* — Revised guidelines for the onboard operational use of shipborne Automatic Identification Systems (AIS). Specifies internal GNSS receiver requirements for timing purposes and position redundancy.
- **International Electrotechnical Commission (IEC):** *IEC 61993-2:2018 (Edition 3.0)* — Class A shipborne equipment: Operational and performance requirements, methods of test and required test results. Mandates internal GNSS engine and defines slot synchronization testing.
- **International Electrotechnical Commission (IEC):** *IEC 62287-1:2017 (Edition 3.0)* — Class B shipborne equipment: Carrier-sense time division multiple access techniques (CSTDMA). Governs Class B CS carrier-sensing windows and timing cessation rules.
- **International Electrotechnical Commission (IEC):** *IEC 62287-2:2017 (Edition 2.0)* — Class B shipborne equipment: Self-organising time division multiple access techniques (SOTDMA). Governs Class B SO synchronization and slot allocation.
- **International Electrotechnical Commission (IEC):** *IEC 62320-1:2015 (Edition 2.0)* — AIS Base Stations: Minimum operational and performance requirements, methods of testing and required test results. Governs base station timing precision and external synchronization inputs.
- **International Electrotechnical Commission (IEC):** *IEC 62320-2:2016 (Edition 2.0)* — AIS Aids to Navigation (AtoN): Minimum operational and performance requirements, methods of testing and required test results. Establishes Type 1/2/3 AtoN synchronization rules.

## Pitfalls

- **Confusing fix time with transmission time:** The 6-bit `Time stamp` field represents when the navigation sensor sampled position, not when the RF burst departed the antenna.
- **Misinterpreting status sentinels 60–63 as seconds:** Treating sentinel values $\ge 60$ as valid elapsed seconds corrupts database temporal indexes and tracking filters.
- **Assuming Class A derives slot timing from external bridge NMEA:** Transponders derive slot timing strictly from an internal GNSS engine, ignoring external `$GPGGA` sentences for synchronization.
- **Treating sync state 3 as unambiguous:** Sync state `11` binary denotes either Base indirect or Mobile semaphore; disambiguation requires tracking transmitter context across multiple frames.
- **Believing Class B CS transponders maintain slot maps:** Class B CS transponders use carrier-sensing listeners aligned to slot transitions, maintaining no internal slot reservation directory.
- **Relying on Message 23 quiet time as an absolute silence command:** Type 1, 2, and 3 AtoNs ignore assignment commands under IEC 62320-2; safety-critical navigation beacons cannot be silenced via Message 23.
- **Neglecting leap-second offset handling in GNSS receivers:** Mishandling the UTC leap-second offset shifts frame boundaries by 37.5 slots, causing transmissions to straddle adjacent slots.
- **Assuming receive-only stations require GNSS timing:** AIS packet reception requires no slot synchronization; demodulators lock asynchronously to the 24-bit preamble on incoming signals.
- **Overlooking propagation delay across large cells:** At 120 nmi, propagation delay consumes 7.4 bit periods; without the 24-bit guard buffer, distant bursts would collide with local slots.
- **Reconstructing full calendar dates from Messages 1–3 alone:** Position reports carry only the second modulo 60; full dates must be supplied by receiver TAG blocks or Message 4 broadcasts.

## Key takeaways

- **The UTC minute defines the frame:** An AIS frame spans 60.0 seconds, divided into 2,250 slots of 26.67 ms (256 bits at 9,600 bit/s), with slot 0 aligned to the UTC minute boundary.
- **Rigid jitter budgets preserve the link:** Mobile stations must maintain transmission timing within $\pm 104\ \mu	ext{s}$ ($\pm 1$ bit), with accumulated jitter strictly bounded at $\pm 312\ \mu	ext{s}$ ($\pm 3$ bits).
- **The five-tier hierarchy prevents runaway drift:** Synchronization falls back gracefully from UTC direct $	o$ UTC indirect $	o$ Base direct $	o$ Base indirect $	o$ Mobile semaphore.
- **One level of indirection only:** To prevent timing drift cascading across the ocean, indirect nodes may never serve as synchronization references for other stations.
- **Internal GNSS is regulatory law:** IEC type-approval standards legally mandate an internal GNSS engine dedicated to slot timing, regardless of whether external bridge navigators are connected.
- **Three distinct time mechanisms exist:** The 6-bit fix second in position reports, the rotating hour/minute sub-message in SOTDMA communication states, and full calendar timestamps in Messages 4 and 11.
- **Link-management exploits do not alter physical clocks:** Malicious base station commands (Messages 16, 20, 23) can disrupt channel availability, but cannot force a UTC-direct mobile transponder to abandon its internal satellite clock.
- **Time bugs cause spatial collisions:** The 2005 Saab leap-second defect demonstrated that a 1.0-second clock error shifts transmission by 37.5 slots, placing bursts directly over slot boundaries.

## References

- ACCSEAS (2014). *Feasibility Study of R-Mode Using AIS Transmissions: Part 1 -- Concept Evaluation and Performance Bounds* (Report Issue 1.0 Final). Hamburg: ACCSEAS Project.
- Balduzzi, M., Pasta, A. & Wilhoit, K. (2014). A Security Evaluation of AIS Automated Identification System. In *Proceedings of the 30th Annual Computer Security Applications Conference (ACSAC 2014)*, pages 436–445. New Orleans: ACM. doi:10.1145/2664243.2664257
- Balduzzi, M., Wilhoit, K. & Pasta, A. (2014). *A Security Evaluation of AIS: How Hackers Can Hijack the Tracking System of Commercial Ships and Alter Maritime Traffic* (Technical Report). Tokyo: Trend Micro Research.
- Furuno Singapore Pte Ltd (2020). *Special Announcement -- GPS Rollover on 20th December 2020* (Technical Advisory Bulletin). Singapore: Furuno.
- Harati-Mokhtari, A., Wall, A., Brooks, P. & Wang, J. (2007). Automatic Identification System (AIS): Data Reliability and Human Error Implications. *The Journal of Navigation*, 60(3):373–389. doi:10.1017/S0373463307004298
- IEC (2015). *IEC 62320-1:2015 — Maritime navigation and radiocommunication equipment and systems -- Automatic identification system (AIS) -- Part 1: AIS Base Stations -- Minimum operational and performance requirements, methods of testing and required test results*. Edition 2.0. Geneva: International Electrotechnical Commission.
- IEC (2016). *IEC 61162-1:2016 — Maritime navigation and radiocommunication equipment and systems -- Digital interfaces -- Part 1: Single talker and multiple listeners*. Edition 5.0. Geneva: International Electrotechnical Commission.
- IEC (2016). *IEC 62320-2:2016 — Maritime navigation and radiocommunication equipment and systems -- Automatic identification system (AIS) -- Part 2: AIS Aids to Navigation (AtoN) -- Minimum operational and performance requirements, methods of testing and required test results*. Edition 2.0. Geneva: International Electrotechnical Commission.
- IEC (2017). *IEC 62287-1:2017 — Maritime navigation and radiocommunication equipment and systems -- Class B shipborne equipment of the automatic identification system (AIS) -- Part 1: Carrier-sense time division multiple access techniques (CSTDMA)*. Edition 3.0. Geneva: International Electrotechnical Commission.
- IEC (2017). *IEC 62287-2:2017 — Maritime navigation and radiocommunication equipment and systems -- Class B shipborne equipment of the automatic identification system (AIS) -- Part 2: Self-organising time division multiple access (SOTDMA) techniques*. Edition 2.0. Geneva: International Electrotechnical Commission.
- IEC (2018). *IEC 61993-2:2018 — Maritime navigation and radiocommunication equipment and systems -- Automatic Identification Systems (AIS) -- Part 2: Class A shipborne equipment of the automatic identification system (AIS) -- Operational and performance requirements, methods of test and required test results*. Edition 3.0. Geneva: International Electrotechnical Commission.
- IMO (1998). *Adoption of New and Amended Performance Standards for Navigation Technology: Recommendation on Performance Standards for a Universal Shipborne Automatic Identification System (AIS)* (Resolution MSC.74(69), Annex 3). London: International Maritime Organization.
- IMO (2015). *Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems (AIS)* (Resolution A.1106(29)). London: International Maritime Organization.
- ITU-R (2026). *Technical Characteristics for an Automatic Identification System Using Time Division Multiple Access in the VHF Maritime Mobile Band* (Recommendation ITU-R M.1371-6). Geneva: International Telecommunication Union.
- Japan Radio Co., Ltd. (2021). *Notice: GPS Week Number Rollover for Equipment* (Customer Service Notice). Tokyo: JRC.
- Kessler, G. C. (2020). Protected AIS (pAIS): A Demonstration of Authenticated, Encrypted Automatic Identification System Message Exchange. *TransNav: The International Journal on Marine Navigation and Safety of Sea Transportation*, 14(2):279–286. doi:10.12716/1001.14.02.02
- Norwegian Maritime Authority (2005). *Safety Message 10/2005: Incorrect UTC Implementation in AIS Equipment Caused by Leap Second* (Sjøfartsdirektoratet Circular SM 10/2005). Haugesund: Norwegian Maritime Authority.
- Saab TransponderTech AB (2005). *Product Information: Leap Second Implementation in R4 AIS* (Technical Bulletin PT-05-0078). Linköping: Saab TransponderTech AB.
- United States Coast Guard (2005). *Potential AIS Malfunction Associated with GPS Leap Second* (Marine Safety Alert 5-05). Washington, DC: USCG.
- Wimpenny, J., Šafář, M., Grant, A. & Bransby, M. (2022). Securing the Automatic Identification System (AIS) Using Public Key Cryptography to Prevent Spoofing Whilst Retaining Backwards Compatibility. *The Journal of Navigation*, 75(2):333–345. doi:10.1017/S0373463321000624
