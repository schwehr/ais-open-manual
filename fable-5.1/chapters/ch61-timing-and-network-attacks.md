# Chapter 61 — Timing and network-disruption attacks

> **Part IX — Security.** An examination of physical-layer and link-layer denial-of-service vulnerabilities in the Automatic Identification System, analyzing whether an adversary can collapse a self-organizing cell through timing de-synchronization, slot starvation, or protocol abuse.

**In this chapter.** You will learn how the maritime Automatic Identification System (**AIS**) behaves under adversarial link-layer manipulation, protocol abuse, and timing corruption. We analyze the theoretical and practical feasibility of collapsing an operational Self-Organizing Time Division Multiple Access (**SOTDMA**) cell. You will examine the five-tier synchronization hierarchy codified in Recommendation ITU-R M.1371, assessing whether a malicious station transmitting fabricated base station reports (Message 4) or false Universal Coordinated Time (**UTC**) sub-messages can drag a cell off its slot boundaries. You will evaluate denial-of-service mechanisms documented by Balduzzi, Pasta, and Wilhoit (2014), including slot starvation via Message 20, forced regional frequency-hopping via Message 22, and transmission suppression via Message 23 quiet-time commands. By modeling these disruptions using a link-layer simulator and analyzing type-approval standards, you will distinguish real physical constraints from theoretical protocol vulnerabilities and explore robust countermeasures in the VHF Data Exchange System (**VDES**).

## 61.1 The fragile equilibrium of self-organizing TDMA

The link layer of the Automatic Identification System operates as an autonomous, distributed coordination system without centralized scheduling. Unlike cellular networks, where base stations orchestrate every uplink slot, an AIS cell relies on mobile Class A transponders dynamically negotiating channel access over 2,250 slots per minute across two designated VHF frequencies: channel AIS 1 (161.975 MHz) and channel AIS 2 (162.025 MHz) ([Chapter 21](ch21-link-layer-tdma.md); [Chapter 28](ch28-rf-encoding-physical-layer.md)).

This distributed architecture accommodates hundreds of transponders within a shared line-of-sight cell (typically 20–30 nautical miles; 37–56 km). However, its operational stability rests upon three structural premises:
1. **Universal temporal synchronization:** All transmitting stations must share a common time base so that transmission bursts occur precisely within rigid 26.67 ms slot boundaries.
2. **Cooperative slot awareness:** Stations must continuously decode High-Level Data Link Control (**HDLC**) bursts, parse communication-state fields, and respect future reservations announced by neighboring hulls.
3. **Implicit trust in supervisory commands:** The protocol allows shore-based Vessel Traffic Services (**VTS**) to manage spectrum congestion, command channel shifts, assign reporting intervals, and reserve slot blocks using privileged broadcast messages without cryptographic authentication.

Because the underlying radio standard, Recommendation ITU-R M.1371-6 (2026), provides zero cryptographic authentication, transport layer encryption, or digital signatures ([Chapter 58](ch58-threat-model.md)), an attacker equipped with a Software-Defined Radio (**SDR**) can inject arbitrary packets into the VHF data link (**VDL**). This structural absence of verification raises a fundamental electronic warfare question: *Can an adversary collapse a local AIS network cell?*

Network disruption against AIS diverges from conventional wideband RF noise jamming. Brute-force RF jamming requires an adversary to emit continuous high-power noise across both channels, demanding substantial electrical power, specialized amplification hardware, and large antennas that are readily geolocated by coastal direction-finding infrastructure ([Chapter 31](ch31-noise-and-interference.md); [Chapter 35](ch35-direction-finding-geolocation.md)). In contrast, protocol-aware timing and network-disruption attacks exploit deterministic state machines within type-approved transponders. By transmitting crafted protocol frames at modest power levels (1 W to 12.5 W), an adversary seeks to manipulate link-layer timing, starve legitimate transponders of available transmission slots, redirect vessels to dead channels, or command transponders into extended silence.

> **Threat model.**
> - **Attacker & Capability:** A malicious actor possessing a commercial off-the-shelf software-defined radio transceiver (e.g., HackRF, bladeRF, or USRP) paired with a 12.5 W marine VHF power amplifier, located ashore or aboard a vessel within line-of-sight. The attacker can synthesize bit-exact GMSK waveforms conforming to ITU-R M.1371, inject arbitrary AIS message types (Messages 4, 16, 20, 22, 23), and schedule bursts at arbitrary sub-millisecond offsets.
> - **Attack Vectors:** Broadcast of false UTC timing references (Message 4 and SOTDMA sub-messages); synthetic exhaustion of TDMA slot maps (Message 20 FATDMA reservation storms); remote retuning of marine transceivers (Message 22 regional area assignments); forced rate throttling and quiet-time transmission suppression (Message 16 and Message 23 assignment commands).
> - **Potential Impact:** Regional denial of maritime situational awareness; suppression of emergency position reports in congested waterways; starvation of Class B recreational targets from collision-avoidance displays; de-synchronization of transponders into mutual interference; blindness of shore-side Vessel Traffic Services.
> - **Mitigations:** Receiver sanity checking of administrative messages against physical plausibility; isolation of critical position reporting from unauthenticated management commands; independent GNSS/atomic clock anchoring; hardware-enforced rate bounds in type-approval standards; migration to authenticated VDES control channels.

## 61.2 Anatomy of synchronization attacks

To evaluate whether an attacker can de-synchronize a dynamic AIS cell, one must analyze how transponders establish and maintain temporal alignment on the wire.

### 61.2.1 The ITU-R M.1371 synchronization hierarchy
Recommendation ITU-R M.1371 Annex 2 §3.1 establishes a strict five-tier synchronization hierarchy. When transponders transmit position reports via SOTDMA (Message 1, 2, or 3), they encode their current synchronization status into a 2-bit `sync_state` field embedded within the 19-bit SOTDMA communication state ([Chapter 24](ch24-timing.md)):

```
+------+----------------------+------------+------------------+--------------+
| Rank | Synchronization Mode | Sync Code  | Timing Reference | Relayed As   |
+------+----------------------+------------+------------------+--------------+
|  1   | UTC Direct           |     0      | Internal GNSS    | Usable sync  |
|  2   | UTC Indirect         |     1      | UTC Direct peer  | Invalid sync |
|  3   | Base Direct          |     2      | VTS Base Station | Usable sync  |
|  4   | Base Indirect        |     3      | Base Direct peer | Invalid sync |
|  5   | Mobile Semaphore     |     3      | Master Mobile    | Invalid sync |
+------+----------------------+------------+------------------+--------------+
```

Under normal maritime operating conditions, virtually every operational Class A shipborne mobile station operates in **UTC Direct** (`sync_state = 0`). Under international carriage requirements (IMO Resolution A.1106(29); IEC 61993-2:2018), Class A transponders are equipped with an internal GNSS receiver dedicated to deriving precise UTC 1PPS timing and slot phase. The transmission of slot 0 coincides exactly with the start of each UTC minute.

A transponder moves down the synchronization hierarchy only when it suffers an internal loss of its primary GNSS time reference. If internal GNSS tracking is lost, the transponder transitions to **UTC Indirect** (`sync_state = 1`), locking its slot phase to received packets from nearby vessels that broadcast `sync_state = 0`. If no UTC Direct stations are audible, the station searches for a legitimate shore base station broadcasting Message 4, locking to **Base Direct** (`sync_state = 2`). If only indirect base references are heard, it falls to **Base Indirect** (`sync_state = 3`). Finally, in a completely isolated GNSS-denied environment without shore infrastructure, the cluster of drifting vessels executes a distributed semaphore election: the mobile station that reports hearing the highest number of other stations across the preceding nine frames is elected as the **Mobile Semaphore** (`sync_state = 3`), serving as the pseudo-master clock for the local cell.

Crucially, ITU-R M.1371-6 Annex 2 §3.1.3.4.3 defines strict rules governing sync source priority: internal UTC Direct holds absolute priority over all received radio broadcasts. This priority rule provides immediate defense against naive synchronization attacks. If an adversary injects a rogue base station broadcasting Message 4 with corrupted time, or emits fabricated position reports claiming to be a high-capacity mobile semaphore, compliant transponders with healthy internal GNSS receivers completely ignore the adversary's timing. Because internal UTC Direct holds top priority, a vessel will never slave its clock to an external VHF burst while its internal GNSS maintains lock.

### 61.2.2 De-synchronizing GNSS-denied cells
The vulnerability window opens when a local cell is subjected to compound electronic warfare—specifically, simultaneous GNSS jamming or spoofing coupled with VHF packet manipulation ([Chapter 62](ch62-gnss-jamming-spoofing.md)).

When an electronic warfare unit disables regional GPS/Galileo reception across a chokepoint, transponders lose UTC lock. Internal holdover clocks begin drifting. At this juncture, the transponders must drop to lower tiers in the hierarchy.

Here, an adversary can mount a false semaphore attack or rogue base station timing drag:
1. **Rogue Base Station Injection (Message 4):** An attacker transmits Message 4 claiming to be an authoritative coastal base station. Under M.1371-6 Annex 2 §3.1.1.3, a GNSS-denied mobile station synchronizes its slot timing to the base station indicating the highest number of received stations, provided at least two reports have been received from that base in the last 40 seconds.
2. **Sub-Message Timing Corruption:** In SOTDMA position reports where the 3-bit slot time-out decrements to 1, the 14-bit sub-message field carries the current UTC hour and minute. An adversary broadcasting high-volume packets can inject false slot offsets and corrupted UTC hour/minute values.
3. **Slot Phase Creep:** The physical slot duration is $60\text{ s} / 2250 = 26.666\overline{6}\text{ ms}$. At a baud rate of 9,600 bit/s, one bit occupies $104.167\ \mu\text{s}$. A complete slot comprises 256 bits. The standard incorporates a 24-bit buffer (2.5 ms) at the trailing end of each packet (M.1371-6 Annex 2 §3.2.2.8), accommodating up to 4 bits of bit stuffing, 14 bits of distance delay (protecting ranges over 120 nmi; 222 km), and 6 bits of synchronization jitter (625.0 µs).

If an attacker controls the synchronization source of a GNSS-denied cell, they can introduce incremental clock skew ($\Delta t$). If the attacker shifts their transmitted slot markers beyond the 6-bit jitter budget, slave transponders track the drifting slot boundary. If different clusters of ships slave to competing timing references, their transmission packets overlap in time, creating severe packet collisions across the slot map.

> **Case file.**
> **The 2005 Saab R3/R4 Leap-Second Timing Flaw.**
> A vivid real-world demonstration of what happens when AIS slot timing drifts occurred on a massive scale without malice in late 2005. At midnight on December 31, 2005, the International Earth Rotation and Reference Systems Service (**IERS**) introduced a positive leap second into UTC. GPS satellites began broadcasting the upcoming leap-second announcement in navigation subframes in July 2005.
> Due to a firmware defect in the internal GPS engine deployed within Saab TransponderTech R3 and R4 Class A transponders, the receiver applied the leap second *immediately upon receiving the broadcast announcement* in September 2005, rather than waiting for December 31 (Saab TransponderTech Bulletin PT-05-0078; Norwegian Maritime Directorate Safety Message SM 10/2005; USCG Marine Safety Alert 5-05).
> The consequence was an exact one-second timing error ($1.0\text{ s} = 1,000\text{ ms}$). In the AIS slot structure, $1.0\text{ s} / 0.026666\overline{6}\text{ s} = 37.5\text{ slots}$. Because the offset ended in half a slot (13.33 ms), every transmission from an affected Saab transponder began precisely in the middle of a legitimate TDMA slot. Each transmission effectively spanned two adjacent slots, colliding with properly synchronized bursts and rendering the messages undecodable by standard receivers. The incident proved that while a half-slot error degrades communication gracefully in a low-density cell, it causes severe packet loss in congested waters.

## 61.3 Supervisory command exploitation (Messages 16, 20, 22, 23)

Beyond physical synchronization, the AIS protocol incorporates link-management and channel-assignment messages engineered for shore-based VTS authorities ([Chapter 22](ch22-message-catalog.md)). These supervisory commands provide tools to mitigate spectrum congestion and manage regional radio configurations. In their landmark ACSAC research, Balduzzi, Pasta, and Wilhoit (2014) demonstrated that the total absence of authentication allows an adversary to weaponize these administrative functions.

### 61.3.1 Slot starvation via Message 20 (FATDMA reservations)
Fixed Access Time Division Multiple Access (**FATDMA**) allows a coastal base station to pre-emptively reserve recurring slots for its own broadcasts, for physical or virtual Aids to Navigation (**AtoN**), or for offshore infrastructure ([Chapter 20](ch20-architecture-and-station-classes.md)).

Under Recommendation ITU-R M.1371-6 Annex 7 §3.18, a base station broadcasts **Message 20 (Data Link Management Message)**. A single Message 20 specifies up to four reservation blocks, defining slot offsets, consecutive slot counts, allocation time-outs (0–7 minutes), and recurring increments (0–1,125 slots).

When a mobile Class A or Class B station receives a valid Message 20, its link-management entity (**LME**) updates its internal slot map, marking the designated slots as `UNAVAILABLE`. Under intentional slot reuse rules (M.1371-6 Annex 2 §4.4.1), a station may reuse occupied slots from the most distant mobile stations when link saturation exceeds 100%, but **slots reserved by a base station within 120 nmi are strictly protected and may never be intentionally reused by a mobile station.**

Balduzzi, Pasta, and Wilhoit (2014) demonstrated that an attacker can synthesize a rogue base station broadcasting Message 4 paired with a sequence of Message 20 frames that declare all 2,250 slots on both AIS 1 and AIS 2 as reserved. By broadcasting reservations across the entire frame, the attacker purports to allocate 100% of link capacity to shore infrastructure.

However, real-world transponders exhibit built-in protocol defenses:
1. **The Message 4 pairing rule:** ITU-R M.1371-6 Annex 2 §3.3.4.3 explicitly mandates that a Message 20 without a base station report (Message 4) should be ignored. The mobile station uses Message 4 to calculate its distance from the transmitting base station; if range exceeds 120 nmi (222 km), the transponder disregards the reservation.
2. **Class B CS vulnerability:** While Class A transponders enforce the 120 nmi distance check, Class B Carrier-Sense (**CS**) units conforming to IEC 62287-1 (2017) are far more fragile. Under Annex 6 §4.3.1.5, Class B CS transponders treat slots reserved by Message 20 as `UNAVAILABLE` *regardless of range*. A Message 20 flood can instantly silence local Class B small craft across an entire bay, extinguishing them from radar and ECDIS screens.

### 61.3.2 Frequency hopping and regional displacement via Message 22
Under international maritime agreements, the default global channels for AIS are channels 87B (AIS 1, 161.975 MHz) and 88B (AIS 2, 162.025 MHz). To automate channel switching in territorial waters without mariner intervention, the protocol provides **Message 22 (Channel Management)**.

Message 22 can be transmitted as an addressed command to an individual vessel or as a broadcast defining a Regional Operating Area using North-East and South-West WGS-84 coordinates. Inside this boundary, Message 22 specifies Channel A and B numbers, transmit/receive modes, and RF power levels. When a vessel crosses the boundary, its transponder automatically retunes its internal VHF synthesizers.

An adversary broadcasting forged Message 22 frames defining a geographic polygon encompassing a busy harbor can assign non-standard VHF channels outside marine VHF monitoring bands (Balduzzi, Pasta & Wilhoit 2014). Class B transponders possess no manual channel override buttons, retuning automatically without audible warning to the bridge watch. Under ITU-R M.1371-6 Annex 2 §4.1.6, a transponder stores up to eight regional operating areas in memory. A regional setting is purged only if the vessel is more than 500 nmi (926 km) from the nearest boundary, after 24 hours have elapsed, or when overwritten. Consequently, an adversary radiating Message 22 bursts can isolate local vessels on dead channels for up to 24 hours.

### 61.3.3 Quiet-time and rate throttling via Message 23
Under ITU-R M.1371-6 Annex 7 §3.21, a base station can issue **Message 23 (Group Assignment Command)** to dynamically control reporting behavior within a geographic area.

Message 23 carries two disruptive parameters:
1. **Reporting Interval (4 bits):** Can force stations into pre-defined cadences ranging from autonomous mode (code 0) to 10 minutes (code 1) or 2 seconds (code 11).
2. **Quiet Time (4 bits):** Specifies a silence period from 1 to 15 minutes (values 1–15; 0 = no quiet time).

The vulnerability to Message 23 depends heavily on transponder class:
- **Class A resilience:** Under M.1371-6 Annex 2 §3.3.6, a Class A transponder in assigned mode evaluates its autonomous interval against the commanded interval: if autonomous mode requires a shorter reporting interval, the station must use the autonomous interval. Because an underway vessel navigating at >14 kn transmits autonomously every 2 to 6 seconds ([Chapter 20](ch20-architecture-and-station-classes.md)), a spoofed Message 23 commanding a 10-minute interval is overridden by the Class A state machine.
- **Class B CS suppression:** In contrast, Class B CS transponders strictly obey quiet time. Under M.1371-6 Annex 6 §4.3.3.3.2, during quiet time the station continues scheduling transmissions but does not transmit Messages 18 and 24. An attacker re-transmitting Message 23 every 15 minutes can effectively suppress Class B broadcasts indefinitely.

## 61.4 Modeling cell collapse with SOTDMA simulation

To quantify the operational impact of slot starvation and network disruption, we utilize a link-layer simulator based on the formal rules of ITU-R M.1371-6. The simulator models a single 2,250-slot frame operating on a single channel.

### 61.4.1 Simulation methodology
The simulation model (`code/tdma/sotdma_sim.py`) instantiates two vessel populations operating within a shared radio line-of-sight cell:
- **Class A population ($N_A$):** Autonomous SOTDMA stations. Each station selects a nominal start slot ($NSS$) and an autonomous reporting interval ($RI$). In accordance with M.1371-6 Annex 2 §3.3.4.4.2, the selection interval ($SI$) spans:
  $$SI = [NS - 0.1 \cdot NI, NS + 0.1 \cdot NI]$$
  where $NI = 2250 / R_r$ is the nominal increment. If candidate slots are free, the station selects randomly among them. If all candidate slots are occupied, the station is forced into intentional slot reuse, colliding with the prior occupant.
- **Class B CS population ($N_B$):** Carrier-sense stations operating under Annex 6. When an unscheduled transmission is pending, the station probes 10 candidate periods within a 10-second window ($TI$). If all 10 candidate periods are detected as busy (or reserved by an adversarial jammer), the transmission is deferred, registering as packet starvation.
- **Adversarial Jammer / Reservation Flood:** An attacker occupies a designated fraction ($f_{\text{jam}} \in [0.0, 0.9]$) of the TDMA slot map, simulating physical GMSK slot corruption or synthetic Message 20 FATDMA reservations.

> **Try it.**
> Run the link-layer simulator across varying jamming fractions using the book's repository environment:
> ```bash
> cd /usr/local/google/home/schwehr/sdd-books/ais/fable
> . .venv/bin/activate
> python code/tdma/sotdma_sim.py --n-a 200 --ri-a 75 --n-b 50 --jam 0.5
> ```
> Expected output:
> ```text
> {'a_tx': 14985, 'a_collided': 12436, 'b_tx': 24, 'b_deferred': 346, 'slots_used': 8010, 'slots_jammed': 5625, 'occupancy': 0.712, 'a_loss_rate': 0.83, 'b_defer_rate': 0.935}
> ```

### 61.4.2 Empirical simulation results
Executing parameter sweeps across vessel densities and jamming fractions reveals the non-linear failure modes of the SOTDMA protocol:

```
+-------+-------+---------+----------+-----------+------------+-----------------+
|  N_A  |  N_B  |  f_jam  | Total Tx | Occupancy | A Loss Rate| B Deferral Rate |
+-------+-------+---------+----------+-----------+------------+-----------------+
|   60  |   40  |   0.0   |   1,265  |   0.112   |    0.000   |      0.000      |
|   60  |   40  |   0.3   |   1,265  |   0.112   |    0.000   |      0.000      |
|   60  |   40  |   0.6   |   1,255  |   0.112   |    0.000   |      0.036      |
|  200  |   50  |   0.0   |  15,000  |   0.533   |    0.012   |      0.048      |
|  200  |   50  |   0.3   |  15,000  |   0.622   |    0.341   |      0.482      |
|  200  |   50  |   0.5   |  15,009  |   0.712   |    0.830   |      0.935      |
+-------+-------+---------+----------+-----------+------------+-----------------+
```

These simulation metrics highlight critical architectural dynamics:
1. **Graceful degradation at low traffic density:** In a lightly loaded waterway ($N_A = 60, N_B = 40$; 11.2% link occupancy), an adversary reserving or jamming 30% of the slot map ($f_{\text{jam}} = 0.3$) produces zero measurable packet loss for Class A hulls. Because 70% of slots remain available, SOTDMA candidate selection identifies uncorrupted candidate slots within its $\pm10\%$ selection interval.
2. **The Class B starvation cliff:** As the adversarial jamming fraction reaches 50% under moderate traffic ($N_A = 200, N_B = 50$), Class B CS stations experience a catastrophic 93.5% deferral rate. Because Class B CS transponders check only 10 consecutive candidate periods and defer whenever carrier energy is detected, saturating half the slots extinguishes Class B visibility.
3. **Class A cascade failure:** Under the same 50% denial conditions, Class A packet collision rates surge to 83.0%. When available free slots fall below 4 per selection interval, SOTDMA is forced into aggressive intentional reuse. In a localized cell without geographic distance separation, vessels repeatedly overwrite each other's slot reservations, triggering cascading packet loss.

> **Worked example.**
> **Nominal Increment and Selection Interval Arithmetic under Attack.**
> Consider a fast container vessel equipped with Class A AIS transiting an estuary at 18 kn. Under ITU-R M.1371-6 Annex 1 Table 1, its reporting interval is $RI = 6\text{ s}$.
> The reporting rate per minute is $R_r = 60 / 6 = 10\text{ reports/min}$. The nominal increment ($NI$) between successive transmissions on one channel is:
> $$NI = \frac{2250\text{ slots}}{10} = 225\text{ slots}$$
> The selection interval ($SI$) spans $\pm10\%$ of $NI$:
> $$SI = [NS - 0.1 \times 225, NS + 0.1 \times 225] = [NS - 22, NS + 22]$$
> The total width of the selection window is $2 \times 22 + 1 = 45\text{ slots}$. Under standard conditions, the transponder requires a minimum of 4 candidate slots in this 45-slot window (M.1371-6 Annex 2 §3.3.1.2).
> If an adversary broadcasts Message 20 reserving 42 of these 45 slots, the transponder finds only 3 free slots. Unable to satisfy the minimum 4-candidate threshold, the transponder's LME is forced to initiate intentional slot reuse. Under M.1371-6 Annex 2 §4.4.1, it must select the candidate allocated to the vessel with the greatest geographic range. But if all other slots are falsely marked as base station reservations within 120 nmi, the LME cannot reuse them (Rule 5 violation), forcing the transponder to transmit into a degraded candidate slot or drop the transmission entirely.

## 61.5 Detectability and physical-layer signatures

While protocol-level attacks exploit legitimate state transitions, they generate conspicuous physical, temporal, and spatial anomalies that allow terrestrial sensor networks and coastal authorities to identify and isolate the rogue transmitter.

### 61.5.1 Multi-receiver Time Difference of Arrival (TDOA)
An attacker synthesizing phantom vessels or broadcasting supervisory commands must emit RF energy through a physical antenna ([Chapter 35](ch35-direction-finding-geolocation.md)). When an adversary broadcasts Message 20, 22, or 23 frames claiming to be a base station or multiple distinct ships, the emitted RF bursts propagate at the speed of light ($c \approx 3 \times 10^8\text{ m/s}$).

A coastal monitoring network comprising three or more synchronized SDR listening posts records the exact time of arrival ($t_i$) of the HDLC training preamble at each receiver:
$$\Delta t_{ij} = t_i - t_j = \frac{d_i - d_j}{c}$$
Each receiver pair defines a hyperbolic line of bearing. The intersection of these hyperbolas localizes the physical transmitter coordinates to within tens of meters, regardless of the synthetic MMSIs or forged coordinates encoded in the packet payloads. An attacker broadcasting thousands of packets from a single shoreside rooftop or vessel is unmasked instantly because every packet emanates from the identical TDOA centroid.

### 61.5.2 Radio Frequency (RF) and protocol fingerprinting
In addition to TDOA multilateration, individual VHF transmitters impart unique physical-layer impairments during GMSK modulation ([Chapter 34](ch34-rf-forensics-fingerprinting.md)):
- **Transmitter Ramp-Up Envelope:** ITU-R M.1371-6 Annex 2 §3.2.2.10 specifies an 8-bit power ramp-up duration (833 µs, event $T_0$ to $T_1$). Rise-time slope, overshoot ringing, and power stabilization curves are governed by the analog power amplifier circuitry of the specific transmitter.
- **Modulation Index and Phase Drift:** Variations in voltage-controlled oscillators produce subtle frequency offsets ($\Delta f$) and Gaussian filter deviations ($BT = 0.4 \pm 0.05$).
- **Protocol Quirks:** Adversarial scripts built on open-source libraries frequently omit mandatory HDLC bit-stuffing on edge cases, transmit static communication-state sub-messages, or fail to rotate the slot time-out counters in accordance with SOTDMA countdown rules (Balduzzi, Pasta & Wilhoit 2014).

### 61.5.3 RSSI and spatial coverage dissonance
In a genuine maritime network, received signal strength indicators (**RSSI**) correlate naturally with ship kinematics and radar tracks ([Chapter 31](ch31-noise-and-interference.md)). When a genuine coastal base station transmits Message 20 or Message 22, its signal is received across a broad coastal sector with an RSSI profile consistent with an elevated, high-gain mast.

If an SDR attacker located aboard a small boat in a harbor attempts to broadcast Message 20 across a 120 nmi radius, receivers 30 nmi away record immediate signal attenuation below the receiver sensitivity floor (typically $-107\text{ dBm}$ for 20% packet error rate per IEC 61993-2). The rogue supervisory messages fail to reach outer vessels, fragmenting the network rather than collapsing the entire cell.

## 61.6 Architectural mitigations and the VDES horizon

The vulnerability of AIS to timing and network-disruption attacks is an inevitable artifact of its 1990s engineering heritage: an unauthenticated, cooperative radio protocol deployed prior to ubiquitous software-defined radios. Modern maritime engineering has developed both immediate software mitigations and long-term architectural replacements.

### 61.6.1 Firmware sanity checking and command isolation
The most cost-effective near-term defense involves hardening the Presentation Interface (**PI**) and link-management state machines within transponder firmware:
1. **Physical plausibility validation for Message 20:** Transponder firmware must verify that the transmitting base station of a Message 20 is already established in the transponder's internal track database with a consistent history of legitimate Message 4 transmissions and valid kinematic tracks over several minutes.
2. **Rate bounds on administrative commands:** Type-approval testing under IEC 61993-2 should require firmware to enforce a hard ceiling on the rate of accepted Message 22 and Message 23 commands. A transponder should reject any regional channel switch that re-routes primary AIS channels unless confirmed via a verified bridge NMEA sentence.
3. **Class A autonomous rate inviolability:** Firmware must strictly enforce the precedence rule of M.1371-6 Annex 2 §3.3.6: under no circumstances may an external Message 16 or Message 23 command increase the reporting interval of an underway Class A vessel beyond its autonomous kinetic schedule.

### 61.6.2 The VHF Data Exchange System (VDES)
The definitive technical resolution to legacy AIS link-layer disruption is the migration to the **VHF Data Exchange System (VDES)**, standardized under Recommendation ITU-R M.2092-1 (2022) ([Chapter 69](ch69-vdes-ais-2.md)).

VDES fundamentally restructures maritime VHF digital communications into four distinct subsystems:
- **Legacy AIS:** Retained on 161.975 MHz and 162.025 MHz exclusively for basic tactical collision avoidance (Messages 1, 2, 3, 5).
- **Application-Specific Messages (ASM):** Offloaded from AIS to dedicated ASM 1 (161.950 MHz) and ASM 2 (162.000 MHz) channels.
- **VDE Terrestrial (VDE-TER):** Wideband multichannel digital communications delivering data rates up to 307.2 kbit/s across 100 kHz contiguous channel bands.
- **VDE Satellite (VDE-SAT):** Direct-to-orbit uplink and downlink communication links.

Crucially, VDES incorporates modern cryptographic frameworks (IALA Guideline G1139; Kessler 2020; Wimpenny et al. 2022). Administrative link management, regional channel switching, and slot reservation functions are migrated to authenticated VDE channels governed by public-key infrastructure (**PKI**). Under VDES, base station supervisory frames carry digital signatures, mobile stations reject unauthenticated supervisory commands, and high-rate data traffic is isolated from legacy collision-avoidance channels.

> **Legal note.**
> **Unlawful Transmission and Malicious Interference on Maritime Frequencies.**
> The radio frequencies allocated to the Automatic Identification System (161.975 MHz, 162.025 MHz) and international maritime VHF communications are protected under strict international treaties and domestic statutes:
> - **International Telecommunication Union (ITU):** Article 15 §15.1 of the ITU Radio Regulations strictly prohibits all stations from transmitting unauthorized signals, superfluous transmissions, or false or misleading distress communications.
> - **United States Federal Law:** Under 47 U.S.C. § 333 (Communications Act of 1934, as amended), willful or malicious interference to any radio communications licensed or authorized under federal law is a felony offense. Penalties include substantial civil forfeitures exceeding $100,000 per violation day, criminal fines, and seizure of radio transmission equipment under 47 U.S.C. § 510. The Federal Communications Commission (**FCC**) and United States Coast Guard (**USCG**) actively investigate and prosecute unauthorized transmissions on maritime safety bands.
> - **European Union & Flag States:** Operating an unauthorized radio transmitter on international maritime safety channels violates national telecommunications acts (e.g., the UK Wireless Telegraphy Act 2006; Germany's Telekommunikationsgesetz) and constitutes criminal endangerment of maritime transport.
> Security research involving AIS protocols must *always* be conducted via direct coaxial cabled attenuation into shielded dummy loads or within certified anechoic radio frequency test chambers. Emitting unauthenticated AIS protocol bursts into open air is universally illegal.

## Then & now

How our understanding of AIS timing, link-layer mechanics, and network disruption has evolved over three decades:

- **1989–1996:** ⟨H⟩ Håkan Lans conceives and patents the Self-Organizing Time Division Multiple Access (**STDMA**) technique (Swedish patent 8902590-0; US Patent 5,506,587), demonstrating autonomous temporal slot negotiation for aviation transponders and maritime vessel tracking.
- **1998:** ⟨H⟩ Recommendation ITU-R M.1371-0 standardizes the 2,250-slot TDMA frame mapped to the UTC minute, incorporating five-tier synchronization and supervisory management messages.
- **2002:** ⟨H⟩ SOLAS Chapter V Regulation 19 enters into force, establishing mandatory AIS carriage for international merchant shipping without cryptographic authentication controls.
- **2005:** ⟨+⟩ A widespread firmware bug in Saab TransponderTech R3/R4 Class A transponders misinterprets the IERS leap-second announcement, causing transponders to transmit 1.0 second (37.5 slots) out of phase, validating that mid-slot transmissions degrade heavily loaded cells (Saab Bulletin PT-05-0078; USCG Alert 5-05).
- **2006:** ⟨+⟩ IEC 62287-1 standardizes Class B Carrier-Sense TDMA (**CSTDMA**), creating a secondary vessel tier that does not maintain a slot map and relies on 10 candidate periods.
- **2013–2014:** ⟨+⟩ Balduzzi, Pasta, and Wilhoit present groundbreaking security evaluations at Hack in the Box and ACSAC 2014, demonstrating that commodity SDRs emitting unauthenticated Messages 20, 22, and 23 can perform slot starvation, forced frequency hopping, and transmission delay attacks in laboratory environments.
- **2018:** ⟨+⟩ IEC 61993-2 Edition 3.0 formalizes rigorous testing protocols for Class A transponders, verifying behavior under conflicting assignment messages and GNSS sync loss.
- **2020–2022:** ⟨+⟩ Academic proposals for Protected AIS (Kessler 2020) and public-key cryptography over AIS (Wimpenny et al. 2022) prove that backwards-compatible authentication is mathematically viable, but carriage momentum shifts toward the native cryptographic architecture of VDES (ITU-R M.2092-1).
- **2026:** ⟨+⟩ Recommendation ITU-R M.1371-6 solidifies legacy link-layer characteristics while global maritime authorities accelerate the deployment of VDES shore and satellite constellations to isolate supervisory commands from unauthenticated VHF broadcast channels.

## On the wire

To detect and diagnose link-layer attacks, engineers must inspect raw NMEA 0183 sentences (`!AIVDM` / `!AIVDO`) and the 19-bit SOTDMA communication state decoded from the wire ([Chapter 26](ch26-interfaces-and-logging.md); [Appendix C](../appendices/appendix-c-message-bit-layouts.md)).

### Dissecting an adversarial Message 20 (FATDMA reservation storm)
The following raw NMEA sentence represents a malicious Message 20 broadcast by a synthetic base station (MMSI 003669999) attempting to starve a local cell:
```text
!AIVDM,1,1,,A,D030p>1;W000,0*11
```

Decoding the 72-bit payload bit-by-bit:
```text
Bit 0-5    : Message ID = 20 (Data Link Management Message)
Bit 6-7    : Repeat Indicator = 0
Bit 8-37   : Source MMSI = 003669999 (Coastal Base Station format)
Bit 38-39  : Spare = 0
Bit 40-51  : Offset 1 = 1209 (Start slot reservation at slot 1209)
Bit 52-55  : Number of Slots 1 = 12 (Reserves a block of 12 consecutive slots)
Bit 56-58  : Time-out 1 = 0 minutes (Allocation valid for current frame only)
Bit 59-69  : Increment 1 = 0 (Repeats every frame)
Bit 70-71  : Spare = 0
```

The message commands all receiving mobile stations within 120 nmi to treat a 12-slot block beginning at slot offset 1,209 as `UNAVAILABLE`. An adversary emitting a stream of such sentences with rotating offsets progressively consumes the entire 2,250-slot map.

### Extracting synchronization state from a Position Report (Message 1)
The health of a cell's temporal alignment is exposed directly within the trailing 19 bits of a standard Class A position report. Consider this raw `!AIVDM` burst:
```text
!AIVDM,1,1,,A,13aEO:0P00000000000000000000,0*3B
```

The final 19 bits encode the SOTDMA communication state:
```text
+-----------------------+-------------------+----------------------------+
| Sync State (Bits 0-1) | Time-out (Bits 2-4)| Sub-Message (Bits 5-18)    |
+-----------------------+-------------------+----------------------------+
|      2 bits           |      3 bits       |          14 bits           |
+-----------------------+-------------------+----------------------------+
```
- **Sync State (Bits 0–1):**
  - `00` (0): **UTC Direct** — Station is locked to internal GNSS timing (healthy baseline).
  - `01` (1): **UTC Indirect** — Station has lost internal GNSS and is locked to a nearby UTC Direct mobile.
  - `10` (2): **Base Direct** — Station is locked to a coastal VTS base station.
  - `11` (3): **Base Indirect / Mobile Semaphore** — Station is locked to a secondary base relay or an elected mobile semaphore.
- **Slot Time-out (Bits 2–4):** Counts down frames remaining before the station abandons this slot (values 0–7).
- **Sub-Message (Bits 5–18):** Interpretation depends on the slot time-out value:
  - If Time-out $\in \{3, 5, 7\}$: Contains the count of received stations ($0–16,383$).
  - If Time-out $\in \{2, 4, 6\}$: Contains the current slot number ($0–2,249$).
  - If Time-out $= 1$: Contains current UTC time (Bits 13–9: UTC Hour $0–23$; Bits 8–2: UTC Minute $0–59$).
  - If Time-out $= 0$: Contains the slot offset to the next allocated transmission ($0–8,191$).

A rapid influx of position reports exhibiting `sync_state = 1` or `sync_state = 3` across multiple distinct vessels provides an immediate signature that local GNSS reception is failing or that an adversary is attempting a timing drag.

## Validation, uncertainty & data quality

Analyzing and mitigating network-disruption attacks requires rigorous validation procedures across both hardware transponders and aggregated telemetry pipelines.

### Data collection and pipeline metrics
In coastal VTS control rooms and commercial data aggregation platforms ([Chapter 41](ch41-networks-and-providers.md)), link-layer health should be monitored continuously using three statistical indicators:
1. **Administrative Message Velocity:** Calculate the hourly frequency of Message 20, Message 22, and Message 23 arrivals per coastal sector. Genuine Message 20 frequency rarely exceeds 20–40 messages per hour per base station. Genuine Message 22 frequency is generally static. Any surge exceeding 5 Message 20 frames per minute or any Message 22 specifying non-standard marine frequencies triggers an immediate security alert.
2. **Synchronization State Distribution:** Compute a rolling census of `sync_state` codes extracted from decoded Message 1, 2, 3, and 4 packets:
   $$\text{Sync Health Ratio } R_{\text{sync}} = \frac{N_{\text{UTC Direct}}}{N_{\text{Total Mobiles}}}$$
   In nominal conditions, $R_{\text{sync}} > 0.99$. If $R_{\text{sync}}$ drops below 0.90 within a 20 nmi radius, the pipeline flags localized GNSS jamming or an active synchronization attack.
3. **Slot Occupancy Rate:** Monitor link density using fixed shore receivers. If total slot occupancy approaches or exceeds 80% (1,800 slots per channel per minute) while physical radar track counts remain static, synthetic slot starvation is underway.

### Forensic validation checklist
When investigating suspected network disruption:
- [ ] Inspect raw NMEA logs for repeated Message 20 sequences containing overlapping slot offsets.
- [ ] Cross-reference the transmitting MMSI of supervisory messages against the official ITU MARS registry.
- [ ] Compare receiver-level RSSI across distributed terrestrial sensor sites to determine whether supervisory frames originate from a single localized emitter.
- [ ] Validate timestamp consistency between packet-level EPFS time stamps (bits 137–142 of Message 1; values 0–59) and the external NMEA sentence arrival time (`c:` TAG block timestamp).

## Software

Software tools for analyzing, simulating, and diagnosing AIS timing and network disruption:

**Open source:**
- **`code/tdma/sotdma_sim.py`:** Built-in Python SOTDMA/CSTDMA slot map simulator. Evaluates collision rates and starvation under jamming. *Caveat:* Single-channel model.
- **pyais:** Type-annotated Python decoding library. Decodes Messages 16, 20, 22, and 23. *Caveat:* Needs batching for real-time streams.
- **AIS-catcher:** C++ SDR receiver. Reports arrival timing, RSSI, and frequency offsets. *Caveat:* Receive-only.
- **GNU Radio (`gr-ais`):** Signal processing framework for GMSK demodulation and packet slicing. *Caveat:* Requires DSP calibration.

**Free but closed:**
- **OpenCPN:** Navigation display and chartplotter. Renders targets and alarms. *Caveat:* Historically vulnerable to DoS from malformed NMEA floods.

**Commercial:**
- **Rohde & Schwarz R&S SMBV100B / CMA180:** Radio communication test sets for IEC 61993-2 testing. *Caveat:* High capital cost.

## Standards & guides

The official specifications and regulatory standards governing AIS timing, link management, and security:

- **ITU-R M.1371-6 (2026):** Technical characteristics for AIS using TDMA in VHF maritime mobile band. Governs sync hierarchy and link layer.
- **ITU-R M.2092-1 (2022):** Technical characteristics for VDES in VHF band. Introduces authenticated digital channels.
- **IMO MSC.74(69) Annex 3 (1998):** Performance standards for shipborne AIS.
- **IMO A.1106(29) (2015):** Guidelines for operational use of shipborne AIS.
- **IEC 61993-2:2018:** Class A shipborne equipment operational and performance tests.
- **IEC 62287-1:2017:** Class B CSTDMA equipment operational requirements.
- **IEC 62287-2:2017:** Class B SOTDMA equipment requirements.
- **IEC 62320-1:2015:** AIS Base Stations requirements and test results.
- **IEC 62320-2:2016:** AIS Aids to Navigation (AtoN) requirements and test methods.
- **IALA Guideline G1139:** Technical Specification of VDES.

## Pitfalls

Eight common analytical, operational, and engineering traps:

1. **Confusing AIS "timing attacks" with clock manipulation.** The term used by Balduzzi, Pasta, and Wilhoit (2014) refers to Message 16/23 assignment delays, not quartz or GNSS clock shifts.
2. **Assuming a rogue base station can drag a healthy Class A cell off time.** Overlooking that UTC Direct holds priority 1 in M.1371-6; transponders with GNSS lock ignore external base timing.
3. **Believing an adversary can slow a moving Class A vessel via Message 23.** Class A transponders maintain their autonomous schedule whenever it requires a faster rate than the assigned command.
4. **Overlooking Class B CS vulnerability.** Class B CS units do not maintain a slot map, treat all Message 20 reservations as unavailable regardless of range, and strictly enforce quiet time.
5. **Treating Message 20 as globally binding without Message 4.** Transponders discard any Message 20 not accompanied by a valid Message 4 from the same MMSI within 120 nmi.
6. **Assuming Message 22 regional channel shifts persist permanently.** Firmware automatically purges stored operating settings after 24 hours or when 500 nmi away.
7. **Relying exclusively on packet content to detect disruption.** Packet decoders silently drop corrupted frames; detecting link starvation requires measuring physical RSSI and raw channel occupancy.
8. **Conducting live RF security experiments over open air.** Transmitting unauthorized signals on marine VHF violates international treaties and domestic laws. Always use shielded cabled loads.

## Key takeaways

1. **No cryptographic controls:** Legacy AIS as specified in ITU-R M.1371-6 possesses zero cryptographic authentication, integrity checks, or transport encryption.
2. **UTC Direct immunity:** Transponders with functioning internal GNSS receivers operate in UTC Direct mode and will not slave slot timing to spoofed base stations.
3. **Compound EW vulnerability:** Synchronization attacks become dangerous primarily when paired with regional GNSS jamming or spoofing.
4. **Asymmetric Class B fragility:** While Class A transponders maintain autonomous reporting rates, Class B CS units are silenced by Message 20 reservations and Message 23 quiet-time commands.
5. **Bounded supervisory persistence:** Malicious Message 22 channel reassignments are automatically purged by transponder firmware after 24 hours or once the vessel travels 500 nmi away.
6. **Physical unmasking via TDOA:** An attacker radiating spoofed supervisory commands from a single physical antenna is rapidly geolocated by coastal multi-receiver TDOA networks.
7. **Simulation confirms non-linear collapse:** SOTDMA link-layer simulation demonstrates that low-density cells absorb slot interference gracefully, but occupancy exceeding 70% triggers rapid cascade failure.
8. **Long-term cure in VDES:** The migration to VDES (ITU-R M.2092-1) introduces public-key cryptography and isolates supervisory functions onto authenticated digital channels.

## References

- Balduzzi, M., Pasta, A. & Wilhoit, K. (2014). A Security Evaluation of AIS Automated Identification System. In *Proceedings of the 30th Annual Computer Security Applications Conference (ACSAC '14)*, pp. 436–445. New Orleans, LA, USA: ACM. doi:10.1145/2664243.2664257
- Balduzzi, M., Wilhoit, K. & Pasta, A. (2014). *A Security Evaluation of AIS: How Hackers Can Hijack the Tracking System of Commercial Ships and Alter Maritime Traffic*. Research White Paper. Tokyo, Japan: Trend Micro Research.
- Center for Advanced Defense Studies (2019). *Above Us Only Stars: Exposing GPS Spoofing in Russia and Syria*. Washington, DC, USA: C4ADS.
- Goudossis, A. & Katsikas, S. K. (2019). Towards a secure automatic identification system (AIS). *Journal of Marine Science and Technology*, 24(2):410–423. doi:10.1007/s00773-018-0561-3
- International Electrotechnical Commission (2015). *Maritime navigation and radiocommunication equipment and systems — Automatic identification system (AIS) — Part 1: AIS Base Stations — Minimum operational and performance requirements, methods of testing and required test results* (IEC 62320-1:2015, Edition 2.0). Geneva, Switzerland: IEC.
- International Electrotechnical Commission (2016). *Maritime navigation and radiocommunication equipment and systems — Automatic identification system (AIS) — Part 2: AIS Aids to Navigation (AtoN) — Minimum operational and performance requirements, methods of testing and required test results* (IEC 62320-2:2016, Edition 2.0). Geneva, Switzerland: IEC.
- International Electrotechnical Commission (2017). *Maritime navigation and radiocommunication equipment and systems — Class B shipborne equipment of the automatic identification system (AIS) — Part 1: Carrier-sense time division multiple access techniques (CSTDMA)* (IEC 62287-1:2017, Edition 3.0). Geneva, Switzerland: IEC.
- International Electrotechnical Commission (2017). *Maritime navigation and radiocommunication equipment and systems — Class B shipborne equipment of the automatic identification system (AIS) — Part 2: Self-organising time division multiple access (SOTDMA) techniques* (IEC 62287-2:2017, Edition 2.0). Geneva, Switzerland: IEC.
- International Electrotechnical Commission (2018). *Maritime navigation and radiocommunication equipment and systems — Automatic Identification Systems (AIS) — Part 2: Class A shipborne equipment of the automatic identification system (AIS) — Operational and performance requirements, methods of test and required test results* (IEC 61993-2:2018, Edition 3.0). Geneva, Switzerland: IEC.
- International Maritime Organization (1998). *Adoption of New and Amended Performance Standards for Navigation Technology: Recommendation on Performance Standards for a Universal Shipborne Automatic Identification System (AIS)* (Resolution MSC.74(69), Annex 3). London, UK: IMO.
- International Maritime Organization (2015). *Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems (AIS)* (Resolution A.1106(29)). London, UK: IMO.
- International Telecommunication Union (2014). *Technical Characteristics for an Automatic Identification System Using Time Division Multiple Access in the VHF Maritime Mobile Band* (Recommendation ITU-R M.1371-5). Geneva, Switzerland: ITU Radiocommunication Sector.
- International Telecommunication Union (2022). *Technical Characteristics for a VHF Data Exchange System in the VHF Maritime Mobile Band* (Recommendation ITU-R M.2092-1). Geneva, Switzerland: ITU Radiocommunication Sector.
- International Telecommunication Union (2026). *Technical Characteristics for an Automatic Identification System Using Time Division Multiple Access in the VHF Maritime Mobile Band* (Recommendation ITU-R M.1371-6). Geneva, Switzerland: ITU Radiocommunication Sector.
- Kessler, G. C. (2020). Protected AIS (pAIS): A Demonstration of Authenticated, Encrypted Automatic Identification System Message Exchange. *TransNav: The International Journal on Marine Navigation and Safety of Sea Transportation*, 14(2):279–286. doi:10.12716/1001.14.02.02
- Norwegian Maritime Authority (2005). *Safety Message 10/2005: Incorrect UTC Implementation in AIS Equipment Caused by Leap Second* (Circular SM 10/2005). Haugesund, Norway: Sjøfartsdirektoratet.
- Saab TransponderTech AB (2005). *Product Information: Leap Second Implementation in R4 AIS* (Technical Bulletin PT-05-0078). Linköping, Sweden: Saab TransponderTech AB.
- United States Coast Guard (2005). *Potential AIS Malfunction Associated with GPS Leap Second* (Marine Safety Alert 5-05). Washington, DC, USA: USCG Office of Investigations and Casualty Analysis.
- Wimpenny, J., Šafář, M., Grant, A. & Bransby, M. (2022). Securing the Automatic Identification System (AIS) Using Public Key Cryptography to Prevent Spoofing Whilst Retaining Backwards Compatibility. *The Journal of Navigation*, 75(2):333–345. doi:10.1017/S0373463321000624
