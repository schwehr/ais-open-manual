# Chapter 40 — AIS in aircraft and drones

> **Part VI — Receiving and collecting.** Deploying AIS receivers and transmitters on airborne platforms extends maritime domain awareness across vast ocean expanses while bridging aeronautical and maritime search and rescue operations.

**In this chapter.** You will learn how the Automatic Identification System (**AIS**) functions when elevated above the earth on crewed aircraft, uncrewed aerial vehicles (**UAVs**), and high-altitude platforms. We dissect the specific protocol extensions governing airborne operations, centered on ITU-R Message 9 for Search and Rescue (**SAR**) aircraft position reports and Recommendation ITU-R M.585 numbering formats (`111MIDXXX`). You will analyze the severe radio-frequency challenges of airborne collection: radio horizons expanding past 200 nautical miles, slot map saturation from multiple coastal cells, Doppler shifts up to 125 Hz, and vertical antenna nulling during aircraft bank angles. We contrast AIS with aviation's Automatic Dependent Surveillance–Broadcast (**ADS-B**) and examine their common technological ancestry in VHF Digital Link (**VDL**) Mode 4. Finally, you will explore surveillance architectures deployed on maritime patrol aircraft and drones, evaluate strict legal prohibitions on unauthorized airborne AIS transmissions, and implement automated validation pipelines to filter airborne telemetry anomalies.

## 40.1 The airborne perspective

Terrestrial AIS collection networks ([Chapter 37](ch37-shore-collection-siting.md)) rely on fixed coastal towers and lighthouses. Even on headlands 100 m above sea level, a shore receiver's radio horizon rarely extends beyond 25 nmi to 30 nmi (46 km to 56 km). While surface platforms such as moored buoys and autonomous surface vehicles ([Chapter 38](ch38-collection-at-sea.md)) provide persistent in-situ monitoring, their low antenna elevations (typically 2 m to 5 m) constrain coverage to roughly 5 nmi to 8 nmi. At the opposite extreme, low Earth orbit (**LEO**) satellites ([Chapter 39](ch39-satellite-ais.md)) orbit between 500 km and 800 km, capturing footprints exceeding 5,000 km in diameter; however, spaceborne reception suffers from revisit latencies and acute packet collisions within congested corridors.

Airborne platforms—crewed maritime patrol aircraft (**MPA**), search and rescue helicopters, tactical uncrewed aerial vehicles, and high-altitude pseudo-satellites (**HAPS**)—occupy the operational sweet spot between surface nodes and orbital sensors. Cruising between 1,000 ft and 45,000 ft (300 m to 13,700 m), an airborne receiver achieves continuous line-of-sight coverage over circular ocean patches spanning 50 nmi to more than 200 nmi in radius. A patrol aircraft cruising at 250 kn to 350 kn sweeps tens of thousands of square nautical miles per hour, gathering real-time RF intelligence, cross-indexing radar and electro-optical/infrared (**EO/IR**) tracks against transponder broadcasts, and coordinating tactical rescue assets on scene.

```
+-------------------------------------------------------------------------------+
|                      AIRBORNE AIS ALTITUDE & HORIZON                          |
+-------------------------------------------------------------------------------+
|  Altitude (ft)    Altitude (m)    Horizon (km)    Horizon (nmi)   Area (sq nmi)|
|  ----------------------------------------------------------------------------|
|    1,000 ft          304.8 m         87.9 km        47.5 nmi        7,088     |
|    5,000 ft        1,524.0 m        176.8 km        95.5 nmi       28,650     |
|   10,000 ft        3,048.0 m        243.4 km       131.4 nmi       54,240     |
|   25,000 ft        7,620.0 m        375.6 km       202.8 nmi      129,200     |
|   45,000 ft       13,716.0 m        498.5 km       269.2 nmi      227,650     |
+-------------------------------------------------------------------------------+
   *Radio horizon calculated to a surface vessel mast height of 15 m (h_tx = 15 m)
    using 4/3 Earth radius refraction model: d = 4.12 * (sqrt(h_tx) + sqrt(h_rx))
```

Airborne AIS operations divide into two functional domains:
1. **Passive airborne collection:** The aircraft carries an AIS receiver coupled to an external belly-mounted VHF antenna. It intercepts maritime VHF transmissions (Class A Messages 1–3, 5; Class B Messages 18, 19, 24; AtoN Message 21; search and rescue transmitters Messages 1 and 14). It feeds decoded NMEA sentences into the mission management system (**MMS**) to correlate electronic tracks with surveillance radar and infrared payloads.
2. **Active airborne transmission:** Dedicated aeronautical search and rescue platforms (such as US Coast Guard HC-130J aircraft, HC-144 patrol planes, and MH-60T helicopters) broadcast specialized AIS messages. Under international regulations, these aircraft broadcast **Message 9** (SAR aircraft position report) to announce their presence, altitude, speed, and track to surface vessels and coast stations.

Because uncontrolled transmissions from high altitudes would devastate coastal link budgets and slot allocations, active airborne AIS transmission is tightly restricted by international treaty and domestic radio regulations.

---

## 40.2 Message 9 and SAR aircraft protocols

When an aircraft participates actively in maritime operations, it does not broadcast standard Class A position reports (Messages 1, 2, or 3). The kinetics of fixed-wing aircraft and helicopters—altitudes up to several thousand metres and speeds exceeding several hundred knots—exceed the dynamic range and semantic definitions of surface reports. Instead, Recommendation ITU-R M.1371 specifies **Message 9: Standard SAR Aircraft Position Report**.

Message 9 is a single-slot transmission occupying exactly 168 bits. It uses Self-Organizing Time Division Multiple Access (**SOTDMA**) on the international AIS VHF data link (**VDL**) channels AIS 1 (161.975 MHz) and AIS 2 (162.025 MHz).

```
+-------------------------------------------------------------------------------+
|                       MESSAGE 9 BIT SPECIFICATION (168 BITS)                  |
+-------------------------------------------------------------------------------+
| Field Name               Bits   Units / Format         Description            |
| ----------------------------------------------------------------------------- |
| Message ID                  6   Unsigned integer       Constant 9             |
| Repeat Indicator            2   Unsigned integer       0-3 (0 = default)      |
| User ID (MMSI)             30   Unsigned integer       MMSI (111MIDXXX)       |
| Altitude                   12   Metres (0-4094 m)      4095 = n/a; 4094 = >=  |
| SOG                        10   Knots (0-1022 kn)      1023 = n/a; 1 knot step|
| Position Accuracy (PA)      1   Boolean flag           1 = high (<= 10 m)     |
| Longitude                  28   1/10000 min (twos)     +/- 180 deg            |
| Latitude                   27   1/10000 min (twos)     +/- 90 deg             |
| Course Over Ground (COG)   12   0.1 deg (0-3599)       3600 = n/a             |
| Time Stamp                  6   Seconds (0-59)         60-63 special / n/a    |
| Altitude Sensor             1   Flag                   0 = GNSS, 1 = baro     |
| Spare                       7   Reserved               Set to zero            |
| DTE                         1   Data terminal ready    0 = available, 1 = not |
| Spare                       3   Reserved               Set to zero            |
| Assigned Mode               1   Flag                   0 = autonomous, 1 = ass|
| RAIM Flag                   1   Boolean flag           RAIM in use (0/1)      |
| Communication State Selector 1  Flag                   0 = SOTDMA, 1 = ITDMA  |
| Communication State        19   Bitfield               Sync & slot reservation|
+-------------------------------------------------------------------------------+
| Total bits: 168 bits (exactly one TDMA slot, matching 256 bits with training) |
+-------------------------------------------------------------------------------+
```

Key architectural differences distinguish Message 9 from surface position reports:
- **Altitude representation:** Message 9 allocates 12 bits to altitude in 1-metre increments from 0 m to 4,094 m (~13,432 ft). An altitude of 4,094 indicates 4,094 m or higher, while 4,095 encodes "not available". A dedicated 1-bit **altitude sensor** flag indicates whether altitude derives from GNSS ellipsoidal height (0) or a barometric altimeter (1).
- **Speed Over Ground dynamic range:** In Messages 1–3, SOG is encoded in tenths of a knot up to 102.2 kn. In Message 9, SOG is encoded across 10 bits in whole knots from 0 kn to 1,022 kn (with 1,023 indicating not available), accommodating high-speed aircraft while discarding sub-knot precision.
- **Absence of Rate of Turn (ROT) and Heading:** Ships require ROT and heading for anti-collision dead reckoning. Aircraft maneuver along three rotational axes; bank-to-turn flight renders instantaneous heading ambiguous. Message 9 omits ROT and True Heading, relying on Course Over Ground (**COG**) and GNSS position.
- **Reporting intervals:** Per Recommendation ITU-R M.1371, an autonomous SAR aircraft transponder transmits Message 9 every **10 seconds** in cruising flight. When executing tactical search maneuvers or changing course, speed, or altitude, the nominal reporting interval accelerates to **2 seconds**.

```
+-------------------------------------------------------------------------------+
|                  MESSAGE 9 DUAL ALTERNATING CHANNEL TIMING                    |
+-------------------------------------------------------------------------------+
|  t = 0 s        t = 10 s       t = 20 s       t = 30 s       t = 40 s         |
|  [Msg 9: Ch A]  [Msg 9: Ch B]  [Msg 9: Ch A]  [Msg 9: Ch B]  [Msg 9: Ch A]    |
|  Slot #1420     Slot #0812     Slot #1940     Slot #0225     Slot #1104       |
|                                                                               |
|  *Maneuvering state (turning / descending):                                   |
|  t = 0s     t = 2s     t = 4s     t = 6s     t = 8s     t = 10s               |
|  [Ch A]     [Ch B]     [Ch A]     [Ch B]     [Ch A]     [Ch B]                |
+-------------------------------------------------------------------------------+
```

For static identity reporting, SAR aircraft do not transmit the 424-bit Class A Message 5. Instead, modern SAR aircraft transmit **Message 24 Part A** every 6 minutes, alternating between VHF channels. Message 24A broadcasts the aircraft's radio name encoded in 120 bits (20 6-bit ASCII characters). The name field begins with the standardized prefix `SAR AIRCRAFT ` followed by the tail number or flight call sign (for example, `SAR AIRCRAFT 2001`).

---

## 40.3 MMSI allocation and station classes

Every station on the maritime VHF data link requires a unique nine-digit Maritime Mobile Service Identity (**MMSI**). Under Recommendation ITU-R M.585 Annex 1 §3, all search and rescue aircraft are assigned MMSI numbers using the fixed prefix **`111`**, followed by the three-digit Maritime Identification Digit (**MID**), followed by three station digits:

$$\text{MMSI}_{\text{SAR}} = \mathbf{111} \parallel \mathbf{MID} \parallel \mathbf{X}_1\mathbf{X}_2\mathbf{X}_3$$

```
+-------------------------------------------------------------------------------+
|                       SAR AIRCRAFT MMSI ARCHITECTURE                          |
+-------------------------------------------------------------------------------+
| Digit:   1   2   3   |   4   5   6   |   7   8   9                            |
| Value:   1   1   1   |   M   I   D   |   X   X   X                            |
| Meaning: Aircraft    | Country code  | Platform specific identifier           |
|          Identifier  | (e.g. 366=USA,| (Optional 7th digit:                   |
|                      |  232=UK,      |  1 = Fixed-wing aircraft               |
|                      |  215=Italy)   |  5 = Rotary-wing helicopter)           |
+-------------------------------------------------------------------------------+
| Group Broadcast Address: 111MID000 (Addresses all SAR aircraft of that nation)|
+-------------------------------------------------------------------------------+
```

Under ITU-R M.585 guidelines, administrations may structure the trailing three digits:
- A 7th digit of **`1`** designates **fixed-wing aircraft** (e.g., `111366101` for a US Coast Guard HC-130J).
- A 7th digit of **`5`** designates **rotary-wing aircraft / helicopters** (e.g., `111366502` for an MH-65D).
- The group address format **`111MID000`** addresses all SAR aircraft of a specific flag state simultaneously via Addressed Binary Messages (Message 6) or Safety Related Messages (Message 12).

### Protocol restrictions: the semaphore prohibition

The SOTDMA protocol ([Chapter 21](ch21-link-layer-tdma.md)) relies on distributed synchronization. Fixed base stations synchronized to UTC via GNSS act as timing masters. In coastal areas lacking base station coverage, mobile stations establish network synchronization through **semaphore synchronization** ([Chapter 24](ch24-timing.md)).

Crucially, **Recommendation ITU-R M.1371 explicitly prohibits SAR aircraft stations from acting as a semaphore master**:

> *"The Class B 'SO' and AIS SAR aircraft station should not act as the semaphore."* (ITU-R M.1371-6, Annex 2 §3.1.3.3.2)

If a patrol aircraft cruising at 250 kn were to become the semaphore timing master for a coastal cell, its rapid transit would continuously pull local ship clocks across varying propagation delays. Furthermore, when the aircraft flies over the horizon, the cell would instantly lose its timing master, causing synchronization collapse and slot collisions. Airborne transponders must synchronize to external GNSS UTC or existing surface semaphores, but may never advertise themselves as the timing reference.

Additionally, in TDMA interrogation protocols (ITU-R M.1371 Annex 7 Table 63), when interrogated by a coast station using Message 15, a SAR aircraft is required to respond only with Message 9 and Message 24A, exempt from commercial voyage and cargo reporting structures.

---

## 40.4 Airborne reception: footprints, geometry, and link budgets

When an aircraft mounts an AIS receiver for surveillance or search and rescue coordination, elevation transforms the radio link geometry.

### Radio horizon and footprint expansion

In terrestrial VHF communications, the line-of-sight distance $d$ over the curvature of the earth is modeled using the effective Earth radius factor of $4/3$ for atmospheric refraction:

$$d \approx 4.12 \cdot \left(\sqrt{h_{\text{tx}}} + \sqrt{h_{\text{rx}}}\right) \quad [\text{km}]$$

Converting to nautical miles ($1\text{ nmi} = 1.852\text{ km}$):

$$d \approx 2.22 \cdot \left(\sqrt{h_{\text{tx}}} + \sqrt{h_{\text{rx}}}\right) \quad [\text{nmi}]$$

where $h_{\text{tx}}$ is the ship antenna height above sea level in metres, and $h_{\text{rx}}$ is the aircraft altitude in metres.

For a commercial ship with a mast height of 15 m ($h_{\text{tx}} = 15\text{ m}$), line-of-sight horizons are:
- At **1,000 ft** (304.8 m): Horizon is **87.9 km** (47.5 nmi).
- At **5,000 ft** (1,524 m): Horizon is **176.8 km** (95.5 nmi).
- At **10,000 ft** (3,048 m): Horizon is **243.4 km** (131.4 nmi).
- At **25,000 ft** (7,620 m): Horizon is **375.6 km** (202.8 nmi).
- At **45,000 ft** (13,716 m): Horizon is **498.5 km** (269.2 nmi).

At 25,000 ft, the aircraft observes an ocean surface area exceeding 129,000 square nautical miles ($442,000\text{ km}^2$), intercepting transmissions from thousands of surface craft simultaneously.

```
+-------------------------------------------------------------------------------+
|                       AIRBORNE RF LINK GEOMETRY                               |
+-------------------------------------------------------------------------------+
|                                                                               |
|                             \ / (Airborne Rx Antenna)                         |
|                           +-----+                                             |
|                           | UAV |  Altitude h_rx                              |
|                           +-----+                                             |
|                             / \                                               |
|                            /   \                                              |
|                           /     \                                             |
|                          /       \                                            |
|                         /         \                                           |
|       Free-Space Path  /           \                                          |
|       Loss (FSPL)     /             \  Line-of-Sight                          |
|                      /               \ Radio Horizon: d_max                   |
|                     /                 \                                       |
|                    v                   v                                      |
|                 +----+              +----+                                    |
|                 |Ship|              |Ship|                                    |
|       ~~~~~~~~~~+----+~~~~~~~~~~~~~~+----+~~~~~~~~~~~~~~~~~~~ Earth Curvature|
|                 h_tx=15m            h_tx=5m                                   |
|                                                                               |
+-------------------------------------------------------------------------------+
```

### Path loss: transition to free-space propagation

For surface-to-surface links ([Chapter 29](ch29-propagation-modeling.md)), propagation over seawater is dominated by the **two-ray ground reflection model**, where destructive interference causes power to attenuate as $1/d^4$ ($40\log_{10} d$).

In airborne collection, the grazing angle between the aircraft and sea surface is steeper. For elevation angles above a few degrees, sea surface roughness scatters the reflected wavefront diffusely, eliminating destructive specular interference. Propagation between surface vessels and elevated aircraft closely matches **Free-Space Path Loss (FSPL)**:

$$\text{FSPL}_{\text{dB}} = 20\log_{10}(d) + 20\log_{10}(f) + 32.44$$

where $d$ is distance in kilometres and $f$ is frequency in megahertz ($162\text{ MHz}$).

Applying link budget equations from `code/rf/linkbudget.py`:
- At $162\text{ MHz}$, a 12.5 W (+41 dBm) Class A transmitter received at 10,000 ft over **100 nmi** (185.2 km) experiences an FSPL of **122.0 dB**.
- Assuming a ship antenna gain of 2.0 dBi, aircraft blade antenna gain of 2.0 dBi, and 2.5 dB total cable losses:

$$P_{\text{rx}} = +41\text{ dBm} + 2.0\text{ dBi} + 2.0\text{ dBi} - 2.5\text{ dB} - 122.0\text{ dB} = -79.5\text{ dBm}$$

Against a receiver sensitivity threshold of $-107\text{ dBm}$ (for 20% packet error rate per IEC 61993-2), the airborne receiver enjoys a **+27.5 dB link margin**.

For a 2 W (+33 dBm) Class B transponder at **50 nmi** (92.6 km, FSPL = 116.0 dB), received power is:

$$P_{\text{rx}} = +33\text{ dBm} + 2.0\text{ dBi} + 2.0\text{ dBi} - 2.5\text{ dB} - 116.0\text{ dB} = -81.5\text{ dBm}$$

yielding a **+25.5 dB link margin**.

### The airborne slot collision crisis

While link margins are high, altitude introduces a severe operational penalty: **VDL packet collisions** ([Chapter 30](ch30-network-loading-packet-loss.md)).

AIS relies on local self-organization within cells spanning 20 nmi to 30 nmi. An aircraft flying at 20,000 ft over congested waters sees ten to twenty independent coastal cells simultaneously. Ships in separate cells reuse the same TDMA slots. Arriving simultaneously at the elevated antenna, these uncoordinated RF bursts collide, corrupting the 16-bit CRC and destroying packet decodes. In dense waters, packet loss rates in airborne receivers can exceed **70% to 90%**. Mitigating this requires specialized DSP: fast-settling digital AGC, Successive Interference Cancellation (**SIC**), and multi-element directional antenna arrays.

### Doppler shifts at aviation velocities

Surface vessels move at speeds below 30 kn, generating Doppler shifts under $8.3\text{ Hz}$ at 162 MHz. Aircraft cruise at higher velocities, where Doppler shift $\Delta f$ is:

$$\Delta f = f_0 \frac{v_{\text{rel}}}{c}$$

```
+-------------------------------------------------------------------------------+
|                       AIRBORNE DOPPLER SHIFT VALUES                           |
+-------------------------------------------------------------------------------+
| Platform Type           Speed (kn)    Speed (m/s)     Max Doppler Shift (Hz)  |
| ----------------------------------------------------------------------------- |
| Maritime Helicopter        120 kn       61.7 m/s             +/- 33.4 Hz      |
| Turboprop Patrol (C-130)   250 kn      128.6 m/s             +/- 69.5 Hz      |
| Jet MPA (Boeing P-8)       450 kn      231.5 m/s            +/- 125.1 Hz      |
| High-Altitude Jet          550 kn      282.9 m/s            +/- 152.9 Hz      |
+-------------------------------------------------------------------------------+
```

Because maritime receivers (IEC 61993-2) maintain lock over $\pm 500\text{ Hz}$, maximum aviation Doppler shifts ($\pm 125\text{ Hz}$) remain within demodulation tolerance. However, when combined with transmitter oscillator offsets ($\pm 400\text{ Hz}$), high closing speeds can push total offsets past filter skirts.

---

## 40.5 Drones, UAVs, and high-altitude platforms

Uncrewed aerial systems (**UAS**) serve as force multipliers for coast guards, navies, and environmental agencies across three distinct tiers:

```
+-------------------------------------------------------------------------------+
|                   UNCREWED MARITIME SURVEILLANCE PLATFORMS                    |
+-------------------------------------------------------------------------------+
| Category | Platforms            | Altitude | Endurance | Payload Architecture |
| ---------+----------------------+----------+-----------+--------------------- |
| Tactical | ScanEagle, Aerosonde,| 1,000 -  | 12-24 hrs | Miniaturized SDR Rx, |
| Ship-UAV | Schiebel CAMCOPTER   | 8,000 ft |           | Line-of-sight C2     |
| ---------+----------------------+----------+-----------+--------------------- |
| MALE UAS | MQ-9B SeaGuardian,   | 10,000 - | 25-40 hrs | Dual-channel AIS Rx, |
|          | Hermes 900 Maritime  | 35,000 ft|           | 360-deg radar, SATCOM|
| ---------+----------------------+----------+-----------+--------------------- |
| HAPS     | Airbus Zephyr,       | 60,000 - | Weeks to  | Ultra-light SDR Rx,  |
|          | Stratospheric Balloons| 70,000 ft| months    | Edge filtering, SBD  |
+-------------------------------------------------------------------------------+
```

### Tactical and shipboard drones

Small ship-launched drones (ScanEagle, Aerosonde, CAMCOPTER S-100) operate from patrol cutters at 2,000 ft to 5,000 ft, expanding the mother ship's horizon from 12 nmi to over 80 nmi. Miniaturized AIS receiver payloads weigh under 150 grams and draw less than 2 watts. Because line-of-sight datalinks have limited bandwidth, edge processors decode packets locally and inject compressed NMEA streams into the telemetry downlink.

### Medium-Altitude Long-Endurance (MALE) UAS

Large drones like the MQ-9B SeaGuardian and Hermes 900 operate at 10,000 ft to 35,000 ft with 30-hour endurance, fusing AIS with 360° maritime search radar and EO/IR turrets:

```
+-------------------------------------------------------------------------------+
|                   MULTISENSOR TRACK CORRELATION ON UAS                        |
+-------------------------------------------------------------------------------+
|   +-------------------+      +-------------------+      +-----------------+   |
|   | 360-deg Sea Radar |      | Passive AIS Rx    |      | EO/IR Gimbal    |   |
|   +---------+---------+      +---------+---------+      +--------+--------+   |
|             | Target Track             | Identity Track          | Visual Conf|
|             v                          v                         v            |
|       +-------------------------------------------------------------+         |
|       |             FUSION & CORRELATION ENGINE (MMS)               |         |
|       +-------------------------------------------------------------+         |
|                  +------------------+------------------+                      |
|                  v                                     v                      |
|       [Correlated Contact]                   [Anomaly / Dark Target]          |
|       Radar matches AIS.                     Radar contact with NO AIS.       |
|       Vessel compliant.                      -> Slew EO/IR turret to target   |
+-------------------------------------------------------------------------------+
```

The mission computer correlates radar and AIS tracks using haversine distance:

$$\Delta d = \text{haversine}\left(\text{lat}_{\text{radar}}, \text{lon}_{\text{radar}}, \text{lat}_{\text{ais}}, \text{lon}_{\text{ais}}\right)$$

When radar detects a large surface contact lacking AIS emissions, the system flags an **AIS Dark Vessel**, commanding the camera gimbal to capture optical confirmation.

### High-Altitude Pseudo-Satellites (HAPS)

Operating at 60,000 ft to 70,000 ft, solar-powered HAPS (Airbus Zephyr) and stratospheric balloons observe surveillance footprints of roughly 330,000 square nautical miles ($d_{\text{horizon}} \approx 325\text{ nmi}$). They provide persistent multi-week loitering over remote economic zones with path losses 25 dB lower than LEO satellites, though severe slot collisions require FPGA-accelerated channelized filterbanks and decollision processing.

---

## 40.6 ADS-B comparison and VDL Mode 4 ancestry

Engineers studying AIS and aeronautical surveillance encounter direct parallels between maritime AIS and civil aviation's **Automatic Dependent Surveillance–Broadcast (ADS-B)**.

```
+-------------------------------------------------------------------------------+
|                       AIS VS. ADS-B COMPARISON TABLE                          |
+-------------------------------------------------------------------------------+
| Characteristic        Maritime AIS                  Aviation ADS-B (1090ES)   |
| --------------------+-----------------------------+-------------------------- |
| RF Frequencies      | 161.975 MHz & 162.025 MHz   | 1090 MHz (also 978 UAT)   |
| Frequency Band      | Marine VHF                  | Aeronautical SSR / L-band |
| Channel Bandwidth   | 25 kHz                      | 50 kHz (receiver: 2-3 MHz)|
| Modulation          | GMSK (BT = 0.4)             | Pulse Position Mod. (PPM) |
| Modulation Bitrate  | 9,600 bit/s                 | 1,000,000 bit/s (1 Mbit/s)|
| MAC Protocol        | SOTDMA / CSTDMA / FATDMA    | Pure Aloha (Stochastic)   |
| Slot Coordination   | Synchronized (UTC / GNSS)   | Unslotted, random squitter|
| Slot Duration       | 26.67 ms (2,250 slots/min)  | No slots; burst is 120 us |
| Message Frame Size  | 168 to 1,064 bits (1-5 slots)| 112 bits (Mode S squitter)|
| Standard Transmit Pwr| 2 W (Class B) / 12.5 W (Cl A)| 125 W to 500 W (pulsed)   |
| Dominant Standards  | ITU-R M.1371, IEC 61993-2   | ICAO Annex 10, RTCA DO-260|
| Primary Identifier  | 9-digit MMSI                | 24-bit ICAO Aircraft Addr |
+-------------------------------------------------------------------------------+
```

### The technological fork: VDL Mode 4

Both systems share technological roots in Swedish inventor **Håkan Lans's** patents for self-organizing time division multiple access (US Patent 5,506,587, filed 1992). In the mid-1990s, this architecture was submitted to both the IMO/ITU for maritime tracking and ICAO as **VHF Digital Link Mode 4 (VDL Mode 4)** (ICAO Annex 10; ICAO Doc 9816).

While Lans's STDMA became the global maritime standard under ITU-R M.1371 and SOLAS Chapter V, civil aviation largely bypassed VDL Mode 4. Aviation authorities, led by the FAA and RTCA (DO-242/DO-260), selected **1090 MHz Extended Squitter (1090ES)** for civil ADS-B. Commercial airliners already carried Mode S transponders and TCAS avionics operating on 1090 MHz; squittering 112-bit pulses on existing hardware proved far more economical than outfitting global fleets with new VHF VDL Mode 4 equipment. VDL Mode 4 survived in niche aeronautical roles, but its core STDMA principles flourish in maritime AIS and Message 9.

---

## Then & now

- **1991–1996** ⟨H⟩: Håkan Lans patents the Self-Organizing Time Division Multiple Access (STDMA) protocol (US Patent 5,506,587), coordinating mobile VHF broadcasts using GPS timing pulses.
- **1998** ⟨H⟩: IMO adopts Resolution MSC.74(69) Annex 3, recommending performance standards for universal shipborne AIS and mandating search and rescue aircraft interoperability.
- **1998** ⟨+⟩: ITU formalizes the 168-bit Message 9 specification in Recommendation ITU-R M.1371-0, establishing SOTDMA framing rules for SAR aircraft.
- **2001** ⟨+⟩: ICAO standardizes VDL Mode 4 in Annex 10, creating an aeronautical sibling to maritime AIS based on Lans's STDMA protocols.
- **2002** ⟨H⟩: IMO SOLAS Chapter V carriage mandate takes effect, establishing a dense surface transponder population for airborne surveillance testbeds.
- **2004** ⟨+⟩: RTCA publishes DO-260A, establishing 1090 MHz Extended Squitter as the civil ADS-B standard and curtailing commercial airline adoption of VDL Mode 4.
- **2004** ⟨+⟩: ITU-R M.585-3 codifies the `111MIDXXX` MMSI prefix architecture for fixed-wing and rotary-wing SAR aircraft.
- **2008** ⟨+⟩: US Coast Guard equips HC-130H, HC-130J, and HC-144A maritime patrol aircraft with integrated AIS receivers linked to the Minotaur mission management system.
- **2014** ⟨+⟩: Balduzzi, Pasta, and Wilhoit demonstrate AIS vulnerabilities at ACSAC 2014, including fake SAR aircraft Message 9 injections.
- **2015** ⟨+⟩: US military and maritime agencies begin formal flight trials of tactical UAS (Aerosonde, MQ-9) equipped with lightweight VHF AIS receivers.
- **2019** ⟨+⟩: ITU-R M.1371-6 formalizes Message 24A naming conventions (`SAR AIRCRAFT NNNNNNN`) and confirms airborne slot selection parameters.
- **2021** ⟨+⟩: MQ-9B SeaGuardian conducts persistent maritime domain awareness demonstrations, fusing 360° radar tracking with automated AIS decoding.
- **2023** ⟨+⟩: High-altitude pseudo-satellites (HAPS) and stratospheric balloons demonstrate multi-week continuous AIS surveillance from 65,000 ft.

---

## On the wire

The following sentence represents an authentic Message 9 broadcast from an airborne search and rescue platform in coastal airspace:

```
Raw sentence:
!AIVDO,1,1,,A,91b=CEmo2lo?Vt@EWFs:S;@04TK@,0*75
```

### Full bit layout and field walk-through

The 28 six-bit ASCII characters encode exactly 168 payload bits:

```
Binary payload (168 bits):
001001 00 000110101111110011001111111111 010111011100 0010110100 1 
1101111001111111011010000000 0010011101110100011001110011 
101000111010 101101 0 0000000 0 000 0 1 0 0000010011010000000
```

```
+-------------------------------------------------------------------------------+
|                       DETAILED BIT-BY-BIT BREAKDOWN                           |
+-------------------------------------------------------------------------------+
| Field                  Bits Value (Bin)                   Value (Dec / Meaning)|
| ---------------------+-----+-----------------------------+--------------------|
| Message ID           |   6 | 001001                      | 9 (SAR Pos Report) |
| Repeat Indicator     |   2 | 00                          | 0 (Original Tx)    |
| User ID (MMSI)       |  30 | 000110101111110011001111111111| 111366999 (US SAR) |
| Altitude             |  12 | 010111011100                | 1,500 m (~4,921 ft)|
| Speed Over Ground    |  10 | 0010110100                  | 180 knots          |
| Position Accuracy    |   1 | 1                           | High (GNSS <= 10m) |
| Longitude            |  28 | 1101111001111111011010000000| -122.419400 deg    |
| Latitude             |  27 | 0010011101110100011001110011| +37.774911 deg     |
| Course Over Ground   |  12 | 101000111010                | 270.0 deg          |
| Time Stamp           |   6 | 101101                      | 45 s past minute   |
| Altitude Sensor      |   1 | 0                           | GNSS derived       |
| Spare                |   7 | 0000000                     | Reserved (0)       |
| DTE                  |   1 | 0                           | Available          |
| Spare                |   3 | 000                         | Reserved (0)       |
| Assigned Mode        |   1 | 0                           | Autonomous SOTDMA  |
| RAIM Flag            |   1 | 1                           | RAIM active        |
| Comm State Selector  |   1 | 0                           | SOTDMA             |
| SOTDMA Comm State    |  19 | 0000010011010000000         | Sync: 0, Sub: 19   |
+-------------------------------------------------------------------------------+
```

### Static identity link: Message 24A

On alternating channels every 6 minutes, the platform broadcasts its static identity:
```
!AIVDO,1,1,,A,H1b=CEi<5:04U8=84IB18E<=DG40,0*47
```
This payload decodes as Message 24 Part A (`partno=0`) for MMSI `111366999` with name `SAR AIRCRAFT RESCUE1`, allowing ECDIS and shore displays to associate telemetry with an aeronautical rescue asset.

---

## Validation, uncertainty & data quality

Airborne AIS pipelines exhibit unique error patterns requiring specialized handling.

### Sources of error and physical anomalies

1. **Antenna pattern nulling during bank maneuvers:** Fuselage blade antennas provide omnidirectional azimuth coverage in level flight. In banked turns ($30^\circ\text{ to }45^\circ$), vertical polarization tilts sharply toward horizontal, introducing 15 dB to 20 dB cross-polarization attenuation and pointing fuselage nulls at the sea surface, causing regular signal dropouts during orbiting patterns.
2. **Speed quantization jitter:** Message 9 encodes speed in integer 1-knot steps. Aircraft speed oscillations between successive whole values induce acceleration spikes in Kalman filters unless process noise covariance $\mathbf{Q}$ is dynamically increased for `111MIDXXX` targets.
3. **Barometric vs. GNSS altitude divergence:** Pressure altitude referenced to $1,013.25\text{ hPa}$ deviates from geometric altitude by hundreds of feet under non-standard atmospheres. If the Altitude Sensor flag (bit 85) indicates barometric pressure (1), geodetic fusion engines must apply local altimeter setting corrections ($QNH$).
4. **ECDIS track corruption:** Legacy ECDIS units lacking Message 9 symbology may render aircraft as surface ships moving at 300 kn, triggering critical CPA/TCPA false collision alarms.

### Automated validation routine

```python
def validate_airborne_message_9(msg: dict) -> list[str]:
    """Validates structural and physical constraints of an airborne Message 9."""
    anomalies = []
    mmsi_str = str(msg.get("mmsi", ""))
    
    if not mmsi_str.startswith("111"):
        anomalies.append(f"Invalid SAR MMSI: {mmsi_str} (must start with 111)")
        
    alt_m = msg.get("alt", 4095)
    sog_kn = msg.get("speed", 1023)
    
    if alt_m == 4095:
        anomalies.append("Altitude telemetry reported unavailable")
    elif alt_m > 4094:
        anomalies.append(f"Altitude exceeds ceiling: {alt_m} m")
        
    if sog_kn == 1023:
        anomalies.append("Speed reported unavailable")
    elif sog_kn > 650:
        anomalies.append(f"Suspicious SAR speed: {sog_kn} kn")
        
    lat, lon = msg.get("lat", 91.0), msg.get("lon", 181.0)
    if not (-90.0 <= lat <= 90.0) or not (-180.0 <= lon <= 180.0):
        anomalies.append(f"Coordinates out of bounds: lat={lat}, lon={lon}")
        
    return anomalies
```

### Moving-receiver spatial bias

Harvesting AIS data from aircraft introduces moving-receiver spatial sampling bias ([Chapter 48](ch48-spatial-statistics.md)). An aircraft cruising at velocity $v_{\text{ac}}$ observes an ocean grid cell at cross-track distance $y_{\perp}$ for duration:

$$t_{\text{obs}}(x, y) = \frac{2 \sqrt{d_{\text{horizon}}^2 - y_{\perp}^2}}{v_{\text{ac}}}$$

Cells along the nadir track line ($y_{\perp} = 0$) experience maximum dwell times, whereas swath edges experience brief contact. Analysts compiling traffic maps must normalize message counts by the cumulative time-integrated footprint $\iint t_{\text{obs}}(x, y)\,dx\,dy$ to eliminate corridor bias.

---

## Software

### Open source
- **pyais** (Python): High-performance decoding library with full support for Message 9 and Message 24A. *Caveat:* Does not perform automated kinematic smoothing across high-speed airborne tracks.
- **libais** (C++ / Python bindings): Industry-standard decoder for binary AIS parsing. *Caveat:* Exports altitude as raw integers without pressure datum conversions.
- **AIS-catcher** (C++): Fast software defined radio receiver for RTL-SDR and Airspy. *Caveat:* Multi-cell packet queues require buffer tuning when operated at high altitude to prevent dropped buffers under heavy slot collisions.

### Free but closed
- **dump1090 / Readsb** (C): Reference decoders for 1090 MHz aviation ADS-B squitter packets. *Caveat:* Do not support maritime VHF GMSK or ITU-R M.1371 protocols.

### Commercial
- **Airborne Mission Management Systems** (Collins, Leonardo, Hensoldt): Avionics suites integrating maritime AIS receivers with search radar and FLIR tracking. *Caveat:* Proprietary interfaces, high cost, and export-controlled under ITAR.

---

## Standards & guides

- **ITU-R Recommendation M.1371-6** (2024): Governs Message 9 structure (Annex 7 Table 60), SOTDMA slot timing, and the prohibition against SAR aircraft serving as semaphores (Annex 2 §3.1.3.3.2).
- **ITU-R Recommendation M.585-10** (2026): Defines `111MIDXXX` MMSI structures for aeronautical SAR assets (Annex 1 §3).
- **IMO Resolution MSC.74(69), Annex 3** (1998): Sets performance standards for shipborne AIS, requiring interoperability with airborne SAR transponders.
- **ICAO Annex 10, Volume III** (2020) & **Doc 9816** (2004): Technical specifications for VHF Digital Link (VDL) Mode 4 STDMA protocols.
- **RTCA DO-260B / DO-242B** (2009/2006): Minimum performance standards for 1090 MHz Extended Squitter ADS-B.
- **IMO/ICAO IAMSAR Manual** (2022 Edition): Operational doctrine for aeronautical search and rescue coordination using AIS.
- **IALA Guideline G1082** (Edition 2.0, 2016): System overview covering SAR aircraft reporting rates and integration.
- **United States 33 CFR § 164.46(i)**: Federal regulation prohibiting unauthorized AIS Class A or Class B broadcasts from aircraft.

---

> **Threat model.** Airborne AIS operates in an unauthenticated RF environment subject to deliberate interference.
> - **Threat Actor:** Hostile electronic warfare assets; adversaries using SDRs to inject falsified maritime data.
> - **Attack Vectors:**
>   1. *SAR Aircraft Spoofing:* Injecting fabricated Message 9 packets with `111MIDXXX` MMSIs to trigger false search missions or divert patrol assets away from maritime smuggling lanes (Balduzzi, Pasta & Wilhoit 2014).
>   2. *Receiver Queue Saturation:* High-repetition shore broadcasts designed to overload airborne receiver buffers.
>   3. *GNSS Spoofing:* Falsifying satellite navigation signals to corrupt transponder position, altitude, and SOTDMA slot alignment.
> - **Impact:** Tactical disruption of search and rescue operations, diversion of emergency patrol aircraft, and corrupted domain awareness.
> - **Defensive Mitigations:**
>   1. *Cross-Sensor Fusion:* Correlating received Message 9 tracks against primary radar skin paints and optical FLIR tracks.
>   2. *Multi-Receiver TDoA Geolocation:* Cross-referencing arrival times across coastal ground stations ([Chapter 35](ch35-direction-finding-geolocation.md)) to verify that `111MIDXXX` signals originate from elevated airborne emitters rather than surface spoofers.
>   3. *Physical-Layer Fingerprinting:* Analyzing RF preamble transient dynamics and modulation phase patterns ([Chapter 34](ch34-rf-forensics-fingerprinting.md); Strohmeier & Martinovic 2015).

---

> **Legal note.** International and federal statutes strictly differentiate between *receiving* and *transmitting* AIS on aircraft:
> - **Passive Reception:** Operating an airborne AIS *receiver* aboard civil or commercial aircraft is entirely lawful. Intercepting unencrypted maritime VHF transmissions complies with international telecommunication conventions.
> - **Prohibition on Active Transmission:** Broadcasting AIS signals from aircraft without explicit maritime mobile authorization is illegal. In the United States, Title 33 of the Code of Federal Regulations, Section 164.46(i), dictates:
>   > *"Except for maritime support stations ... licensed by the FCC, broadcasts from AIS Class A or B devices on aircraft, non-self propelled vessels or from land are prohibited."*
> - Installing an off-the-shelf Class A or Class B ship transponder on an aircraft or drone violates federal law, risking severe FCC/FAA civil penalties and seizure. Active airborne transmissions are restricted exclusively to authorized government search and rescue aircraft, military maritime patrol assets, and licensed research flights.

---

> **Try it.** Decode an authentic airborne Message 9 sentence in Python using `pyais`:
> ```python
> import pyais
> 
> raw_sentence = "!AIVDM,1,1,,A,91b44o1v001@qwhG522Q0?v00000,0*0A"
> msg = pyais.decode(raw_sentence)
> 
> print(f"Message Type: {msg.msg_type}")
> print(f"MMSI:         {msg.mmsi}")
> print(f"Altitude:     {msg.alt} metres ({msg.alt * 3.28084:.0f} feet)")
> print(f"Speed:        {msg.speed} knots")
> print(f"Position:     {msg.lat:.4f}° N, {msg.lon:.4f}° E")
> print(f"Course:       {msg.course}°")
> ```
> Expected output:
> ```text
> Message Type: 9
> MMSI:         111215836
> Altitude:     504 metres (1654 feet)
> Speed:        0.0 knots
> Position:     40.3328° N, 17.6742° E
> Course:       25.6°
> ```

---

> **Case file.** During maritime interdiction patrols in the eastern Pacific Ocean, US Coast Guard HC-130J long-range surveillance aircraft operate alongside cutters. Flying at 10,000 ft, the HC-130J monitors AIS broadcasts across a 130-nmi radius while its APN-241 radar scans for surface contacts. The aircraft identified multiple commercial fishing vessels operating within restricted maritime conservation zones whose radar reflections were confirmed by operators, yet whose AIS transponders were deactivated. The aircraft descended, captured high-resolution optical imagery of hull registrations and deployed gear, and vectored cutters for boarding and seizure.

---

## Pitfalls

1. **Treating SAR aircraft as ship targets in ECDIS** → Early ECDIS software interprets Message 9 as an invalid ship position report or crashes → Ensure bridge software includes an aeronautical renderer displaying standardized SAR aircraft symbols and suppressing false CPA collision alarms.
2. **Mounting standard marine transponders on drones** → Drone operators mount off-the-shelf Class B units on UAVs for fleet tracking → Violates 33 CFR § 164.46 and ITU regulations; high-altitude transmission causes coastal slot starvation. Use ADS-B, cellular, or satellite trackers for drone telemetry.
3. **Ignoring the semaphore synchronization prohibition** → Aeronautical transponders misconfigured to act as SOTDMA semaphores pull surface vessel clocks across varying propagation delays → Ensure airborne transponder firmware strictly disables semaphore qualification per ITU-R M.1371 Annex 2 §3.1.3.3.2.
4. **Failing to account for antenna polarization nulls during turns** → Aircraft banking at $30^\circ\text{ to }45^\circ$ during orbiting patterns introduce severe polarization tilt and antenna pattern nulls toward the surface → Mitigate by mounting paired switched belly antennas or accounting for periodic dropouts in tracking filters.
5. **Treating integer SOG in Message 9 as high-precision velocity** → Message 9 quantizes speed in whole 1-knot increments rather than the 0.1-knot resolution of Message 1, inducing artificial speed steps in Kalman filters → Widen kinematic velocity process noise covariance when tracking airborne MMSI prefixes.
6. **Neglecting moving-receiver spatial sampling bias in density maps** → Aggregating raw airborne AIS message counts over oceanic grids without normalizing for the aircraft's speed and altitude-dependent dwell time produces artificial hotspots along patrol tracks → Normalize counts by the time-integrated surveillance footprint $\iint t_{\text{obs}}(x, y)\,dx\,dy$.
7. **Assuming free-space path loss holds over extreme grazing angles** → At very long ranges near the radio horizon ($> 150\text{ nmi}$), atmospheric refraction, tropospheric ducting, and diffraction cause signals to deviate from pure FSPL → Use hybrid irregular terrain and parabolic wave equation propagation models for horizon link budgets.
8. **Failing to check the Message 9 Altitude Sensor flag** → Assuming reported altitude is always true geometric height introduces errors of several hundred feet due to barometric altimeter deviations from standard pressure → Inspect bit 85 to distinguish GNSS ellipsoidal altitude from barometric pressure altitude.

---

## Key takeaways

- **Operational role:** Airborne AIS operates in two modes: passive reception (widely deployed on patrol aircraft, UAVs, and HAPS for wide-area domain awareness) and active transmission (strictly restricted to authorized search and rescue aircraft).
- **Message 9 structure:** Search and rescue aircraft broadcast Message 9 (168 bits, single SOTDMA slot), providing altitude (up to 4,094 m), SOG (in whole knots up to 1,022 kn), COG, GNSS coordinates, and an altitude sensor flag.
- **Identity conventions:** SAR aircraft use Recommendation ITU-R M.585 MMSI formats beginning with the prefix `111MIDXXX` (with digit 7 designating fixed-wing vs. rotary-wing craft), paired with Message 24A broadcasting the prefix `SAR AIRCRAFT `.
- **Protocol restrictions:** SAR aircraft stations are explicitly prohibited by ITU-R M.1371 from acting as SOTDMA semaphore timing masters, preventing unstable aeronautical motion from disrupting surface ship slot synchronization.
- **RF geometry advantages:** Elevated receivers expand radio horizons past 200 nmi and transition propagation from destructive $1/d^4$ two-ray sea-surface loss to $1/d^2$ free-space path loss, yielding high link margins even on low-power Class B signals.
- **High-altitude slot starvation:** Observing multiple independent coastal SOTDMA cells simultaneously causes severe airborne packet collisions, demanding advanced receiver DSP, successive interference cancellation, or multi-element antenna arrays.
- **Shared VDL Mode 4 heritage:** Maritime AIS and aeronautical ADS-B share common technological ancestry in Håkan Lans's STDMA patents; while aviation chose 1090 MHz Extended Squitter for airline surveillance, VDL Mode 4 survived directly in maritime AIS and Message 9.
- **Legal restrictions:** Under 33 CFR § 164.46 and international radio treaties, transmitting AIS from unauthorized aircraft or commercial drones is illegal; active broadcasts are reserved exclusively for licensed aeronautical search and rescue platforms.

---

## References

- Balduzzi, M., Pasta, A., Wilhoit, K. (2014). A Security Evaluation of AIS Automated Identification System. *Proceedings of the 30th Annual Computer Security Applications Conference (ACSAC '14)*, pages 436–445. New Orleans, LA: ACM. doi:10.1145/2664243.2664257
- Federal Communications Commission and United States Coast Guard (2024). Title 33, Code of Federal Regulations, Section 164.46: Automatic Identification System. Washington, DC: Government Publishing Office.
- International Association of Marine Aids to Navigation and Lighthouse Authorities (2016). *Guideline G1082: An Overview of AIS*. Edition 2.0. Saint-Germain-en-Laye: IALA.
- International Civil Aviation Organization (2004). *Doc 9816: Manual on VDL Mode 4 Technical Specifications*. First Edition. Montreal: ICAO.
- International Civil Aviation Organization (2020). *Annex 10 to the Convention on International Civil Aviation: Aeronautical Telecommunications, Volume III (Communication Systems), Part I (Digital Data Communication Systems)*. Second Edition. Montreal: ICAO.
- International Maritime Organization (1998). *Resolution MSC.74(69), Annex 3: Recommendation on Performance Standards for a Universal Shipborne Automatic Identification System (AIS)*. London: IMO.
- International Maritime Organization and International Civil Aviation Organization (2022). *IAMSAR Manual: International Aeronautical and Maritime Search and Rescue Manual, Volumes I–III*. 2022 Edition. London / Montreal: IMO / ICAO.
- International Telecommunication Union (2024). *Recommendation ITU-R M.1371-6: Technical Characteristics for an Automatic Identification System Using Time Division Multiple Access in the VHF Maritime Mobile Frequency Band*. Geneva: ITU.
- International Telecommunication Union (2026). *Recommendation ITU-R M.585-10: Assignment and Use of Identities in the Maritime Mobile Service*. Geneva: ITU.
- Lans, H. (1996). *Position Indicating System*. US Patent 5,506,587. Granted April 9, 1996.
- Leonardi, M., Di Gregorio, L., Di Fausto, F. (2017). Air Traffic Security: Aircraft Classification Using ADS-B Message Phase Patterns. *Aerospace*, 4(4):51. doi:10.3390/aerospace4040051
- RTCA (2006). *DO-242B: Minimum Aviation System Performance Standards for Automatic Dependent Surveillance Broadcast (ADS-B)*. Washington, DC: RTCA Inc.
- RTCA (2009). *DO-260B: Minimum Operational Performance Standards for 1090 MHz Extended Squitter Automatic Dependent Surveillance - Broadcast (ADS-B) and Traffic Information Services - Broadcast (TIS-B)*. Washington, DC: RTCA Inc.
- Strohmeier, M., Martinovic, I. (2015). On Passive Data Link Layer Fingerprinting of Aircraft Transponders. *Proceedings of the First ACM Workshop on Cyber-Physical System Security (CPS-SPC '15)*, pages 1–9. Denver, CO: ACM. doi:10.1145/2808705.2808712
- United States Coast Guard (2013). *Coast Guard Addendum to the United States National Search and Rescue Supplement (NSS) to the International Aeronautical and Maritime Search and Rescue Manual (IAMSAR)*. COMDTINST M16130.2F. Washington, DC: U.S. Department of Homeland Security.
