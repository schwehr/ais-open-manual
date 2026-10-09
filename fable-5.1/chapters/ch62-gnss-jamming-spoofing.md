# Chapter 62 — GNSS jamming and spoofing: effects on AIS and workarounds

> **Part IX — Security.** Satellite navigation denial and deception propagate directly through shipborne AIS transponders, transforming radio-frequency interference into corrupted VHF broadcasts and turning global receiver networks into distributed electronic warfare sensors.

**In this chapter.** You will learn how Global Navigation Satellite System (GNSS) radio-frequency interference—both brute-force jamming and deceptive spoofing—corrupts maritime Automatic Identification System (AIS) operations. We dissect the fundamental difference between jamming and spoofing from the perspective of the transponder's internal state machine, exploring how loss of satellite tracking triggers dead reckoning, position-unavailable bit sentinels, time-stamp degradation, and fallback through the SOTDMA synchronization hierarchy. You will analyze real-world spoofing phenomena, including airport circular displacement patterns and maritime coordinate warping, supported by verified case files from the Black Sea, Chinese littoral waters, the eastern Mediterranean, and the Baltic Sea. Furthermore, you will discover how global AIS sensor networks act as unintentional distributed detectors of electronic warfare. Finally, we evaluate operational and technical workarounds: manual bridge procedures, radar overlay correlation, terrestrial R-Mode, eLoran, inertial navigation, and VDES ranging.

## 62.1 The dual vulnerability: position and time

The Automatic Identification System (**AIS**) is intimately tethered to satellite radionavigation. While mariners commonly perceive an AIS transponder as an autonomous radio, it is in reality an RF transmitter entirely reliant on external inputs for both its spatial coordinates and its temporal frame of reference. Under Recommendation ITU-R M.1371-6 and International Electrotechnical Commission (**IEC**) design standards, an AIS station requires two core data streams to function: an **Electronic Position-Fixing System** (**EPFS**) solution giving latitude, longitude, Course Over Ground (**COG**), and Speed Over Ground (**SOG**), and a precise phase reference to Coordinated Universal Time (**UTC**) to drive its Self-Organizing Time-Division Multiple Access (**SOTDMA**) link layer.

In modern maritime operations, both requirements are satisfied by signals received from orbiting Global Navigation Satellite System (**GNSS**) constellations, primarily the United States Global Positioning System (**GPS**), European Galileo, Russian GLONASS, and Chinese BeiDou (**BDS**). When these weak satellite signals—arriving at the ship's masthead at power levels between -125 dBm and -130 dBm—are subjected to Radio-Frequency Interference (**RFI**), the failure propagates into the ship's broadcast transmissions.

The failure modes bifurcate along two distinct threat vectors:
1. **Jamming (Denial of Service):** Brute-force RF energy overwhelms the GNSS receiver front end, degrading carrier-to-noise ratio ($C/N_0$) below tracking thresholds. The receiver loses lock, reports an invalid fix, and drops pulse-per-second (**1 PPS**) timing strobes. As detailed in [Chapter 25](ch25-gnss-and-ais.md), the transponder enters a standardized degraded state: broadcasting "not available" sentinels, reducing reporting cadences, and demoting TDMA link synchronization down the timing ladder.
2. **Spoofing (Deception and Manipulation):** A counterfeit RF generator broadcasts synthetic GNSS-like signals at higher power than authentic satellites, locking receiver tracking loops onto false pseudo-ranges. The receiver calculates an apparently valid fix with tight dilution of precision, high signal-to-noise metrics, and active 1 PPS strobes. Because the receiver does not recognize deception, the transponder broadcasts false coordinates across the VHF data link. To external observers, coastal Vessel Traffic Services (**VTS**), and orbital constellations, the vessel appears to execute impossible maneuvers or teleport to inland airports while physically remaining in coastal waters.

Because AIS assumes a trustworthy physical environment, corrupting a navigation receiver pollutes tactical bridge displays, disrupts coastal surveillance, and risks destabilizing the TDMA slot schedule of the VHF cell.

## 62.2 Jamming: mechanics, transponder states, and wire signatures

GNSS jamming is a power-matching attack against the satellite communications physical layer. Satellite navigation signals travel over 20,000 km, suffering massive geometric free-space path loss. At sea level, received GPS L1 C/A power (1575.42 MHz) is approximately -158.5 dBW (-128.5 dBm), roughly 20 dB *below* ambient thermal noise (-114 dBm/MHz at room temperature). The receiver relies on spread-spectrum code correlation gain to extract signals.

A basic terrestrial jammer broadcasting continuous-wave (**CW**), chirp, or band-limited Gaussian noise across L1 (1575.42 MHz), L2 (1227.60 MHz), or L5 (1176.45 MHz) bands raises the noise floor by dozens of decibels. Handheld 1 W (+30 dBm) privacy devices deny GNSS over several nautical miles; military systems exceeding tens of kilowatts EIRP deny reception across 100 to 200 nmi (185 to 370 km).

When a vessel enters a jammed environment, the EPFS receiver experiences:
1. **Tracking degradation:** $C/N_0$ drops; satellite geometry deteriorates; horizontal dilution of precision (**HDOP**) balloons; and Receiver Autonomous Integrity Monitoring (**RAIM**) alarms trigger.
2. **Dead reckoning fallback:** If the bridge system has heading and speed-log inputs, EPFS transitions to dead-reckoning (**DR**) mode.
3. **Complete signal loss:** The receiver declares fix loss and invalidates internal 1 PPS hardware timing.

### Protocol response: sentinel values on the wire
ITU-R M.1371-6 and IEC 61993-2 define how Class A transponders reflect degraded states in Messages 1, 2, and 3 without falling silent:

- **Time stamp field (bits 137–142, 6 bits):** Normally UTC second (0 to 59). In degradation, sentinels apply:
  - `60` (0x3C): Time stamp not available (default fallback).
  - `61` (0x3D): Manual input mode (coordinates hand-entered by bridge crew).
  - `62` (0x3E): Dead reckoning (estimated mode).
  - `63` (0x3F): Positioning system inoperative.
- **Position accuracy (PA) flag (bit 60, 1 bit):** Sets to `0` (low accuracy, expected error > 10 m).
- **RAIM flag (bit 148, 1 bit):** Resets to `0` (RAIM not in use or failed).
- **Position coordinates (bits 61–115):** If dead reckoning cannot be maintained, sentinels are transmitted per Table 47:
  - Longitude (28 bits, signed): 181° (0x6791AC0).
  - Latitude (27 bits, signed): 91° (0x3412140).
- **Speed Over Ground (bits 46–55):** Sentinel value `1023` (0x3FF).
- **Course Over Ground (bits 56–67):** Sentinel value `3600` (0xE10).

> **Definitions that bite.** A position report transmitting Longitude 181.0000° and Latitude 91.0000° with time stamp sentinel `63` is a conforming, valid ITU-R M.1371 transmission notifying all stations that the ship's position sensor is dead. Data aggregation pipelines that discard these packets discard the primary signature of GNSS jamming.

### Class B behavior under jamming
Under IEC 62287-1 (Class B CSTDMA) and IEC 62287-2 (Class B SOTDMA), Class B transponders cannot accept external bridge navigation feeds. They must derive position and time exclusively from an **internal GNSS receiver**. Under ITU-R M.1371-6 Annex 6 §3.3, when a Class B CS unit loses its internal GNSS fix, it is **forbidden to transmit Message 18 and Message 24** unless interrogated by a base station. Class B units do not possess manual entry or dead-reckoning reporting states; sentinels 61–63 are unused. When jamming strikes, Class B craft vanish from the RF spectrum.

### The synchronization cascade: collapse of the SOTDMA timing ladder
GNSS jamming attacks VHF link timing. Class A transponders slice each 60-second frame into 2,250 slots per channel (26.67 ms per slot, [Chapter 21](ch21-link-layer-tdma.md)), requiring synchronization within ±10.4 µs. Under ITU-R M.1371-6 Annex 2 §3.1, stations follow a five-level **synchronization hierarchy**:
1. **UTC Direct (Sync State 0):** Direct access to UTC from operational GNSS.
2. **UTC Indirect (Sync State 1):** Locked to incoming RF frames of nearby UTC Direct stations.
3. **Base Direct (Sync State 2):** Locked to a coastal base station establishing frame timing.
4. **Base Indirect (Sync State 3):** Locked to another mobile synchronized to a base station.
5. **Mobile as Semaphore (Sync State 3):** Designation of a mobile station receiving the highest station count across nine frames as master clock.

Under wide-area jamming, no local ship has UTC Direct. If no atomic-clock-stabilized base station is present, vessels fall to Mobile Semaphore or free-run on internal oscillators. Unsynchronized oscillator drift smears slot boundaries, causing slot collisions, packet loss, and degraded throughput ([Chapter 30](ch30-network-loading-packet-loss.md)).

## 62.3 Spoofing: mechanics, false tracks, and geometric anomalies

**GNSS spoofing** deceives receivers by synthesizing valid civilian satellite signals (such as GPS L1 C/A) with coherent carrier and code phase offsets. Attackers execute a **lift-off attack**: broadcasting counterfeit signals matched to authentic satellites, boosting power by 3 to 6 dB, and slowly slewing pseudo-ranges to pull the fix away without tripping loss-of-lock alarms.

The deceived bridge receiver reports high $C/N_0$ (> 45 dB-Hz), low HDOP (< 1.0), valid RAIM (flag = 1), and valid UTC second (0–59). The Class A transponder accepts these coordinates over NMEA 0183 / IEC 61162 (`$GPGGA`, `$GPRMC`, [Chapter 26](ch26-interfaces-and-logging.md)) and broadcasts them at 12.5 W with `PA = 1`.

> **Threat model.**
> - **Target Assets:** ECDIS displays, bridge Integrated Navigation Systems, ARPA/AIS collision avoidance, VTS tracking, and maritime safety databases.
> - **Threat Actors:** Nation-state electronic warfare units, naval forces, coastal defense commands, and illicit shipping networks evading sanctions.
> - **Attacker Capabilities:** High-power transmitters broadcasting multi-constellation signals across coastal waterways (10 to 50 nmi); pre-programmed spoofing transmitting fixed airport runways or sweeping circular tracks.
> - **Impact:** Tactical disorientation of watchstanders; false collision alarms; automated drift toward shoals; corruption of global tracking records.
> - **Mitigations:** Multi-sensor ECDIS integration (radar overlay, visual bearings); dual-antenna angle-of-arrival GNSS receivers; inertial measurement units; terrestrial alternative PNT (R-Mode, eLoran); algorithmic kinematic plausibility filtering.

### The geometric signature: airport circles and coordinated displacement
The most distinctive maritime spoofing signature is **airport circles**. Beginning in 2017, commercial ships in the Black Sea, eastern Mediterranean, and near Shanghai were observed broadcasting positions snapped to regional airports (e.g., Gelendzhik, Sochi, Khmeimim).

This occurs because military spoofers deploy counter-unmanned aerial vehicle (**C-UAV**) shields around strategic sites. Commercial drones carry firmware **geofencing** that forces an immediate landing or abort when coordinates place them inside an airport boundary. Electronic warfare systems exploit this by broadcasting coordinates of local runways. Merchant ships transiting nearby waters are inadvertently captured, broadcasting airport coordinates. Modulated pseudo-range slewing causes ships docked at piers to appear to circle at impossible speeds.

## 62.4 Case files: documented maritime incidents

Empirical evidence confirms wide-scale GNSS interference across commercial waterways:

> **Case file.** The Black Sea Mass Spoofing Event (June 2017).
> On 22 June 2017, the master of merchant vessel *Atria*, anchored off Novorossiysk, observed the bridge GPS placing the vessel at Gelendzhik Airport—17 nmi (32 km) inland. At least twenty anchored vessels reported identical positions clustered on the runway. The United States Maritime Administration (**MARAD**) documented the event in Maritime Safety Advisory 2017-005A ("Black Sea – GPS Interference"), officially confirming mass civilian maritime spoofing.

Documented campaigns include:
1. **The C4ADS Comprehensive Study (2019):** In *Above Us Only Stars*, C4ADS documented 9,883 spoofing events affecting 1,311 civilian vessels across the Black Sea, Crimea, Syria, and the Russian Far East, correlating spoofing incidents with VIP security deployments.
2. **Chinese Littoral Ports (2019–2020):** SkyTruth and researchers detected hundreds of vessels in Shanghai and the Huangpu River broadcasting circular "crop circles" while tied to piers, linked to illegal sand-mining evasion and state counter-measures.
3. **Eastern Mediterranean and Red Sea (2023–2026):** High-power jamming and spoofing in the Levant caused merchant vessels transiting Suez approaches to lose GNSS or snap to airports in Beirut, Tel Aviv, or Cairo, prompting NATO Shipping Centre navigation warnings.
4. **The Baltic Sea Interference Zone (2023–2026):** In the Gulf of Finland and waters off Kaliningrad, jamming caused widespread AIS errors, including false speeds exceeding 60 kn, erratic dead reckoning, and silencing of Class B craft, documented by Traficom and the Swedish Maritime Administration.

## 62.5 AIS as a global GNSS-interference sensor

Because commercial ships continuously broadcast GNSS tracking status, terrestrial and satellite AIS networks act as unintended global sensors for electronic warfare:

1. **Sentinel census (time stamps 61–63):** Surges in reports containing time stamps `62` (DR) or `63` (inoperative) map the spatial footprint of active jammers.
2. **Space-terrestrial receiver divergence:** A coastal receiver with a 50 m mast has a radio horizon:
   $$D_{\text{LOS}} \approx 4.12 \times \sqrt{50} \approx 29.1\text{ km} \approx 15.7\text{ nmi}$$
   If it decodes a VHF packet whose payload coordinates place the vessel 150 nmi inland at an airport, the signal's terrestrial reception proves the ship is at sea and spoofed.
3. **Kinematic impossibility filtering:** When a vessel jumps 20 nmi in a 10-second reporting interval ($V_{\text{implied}} = 7,200\text{ kn}$), automated pipelines flag the anomaly.
4. **Satellite footprint mapping:** LEO satellites (Spire, exactEarth) observe drops in aggregate packet counts over jammed regions as Class B units fall silent and Class A units glitch.

> **Try it.** Run the kinematic verification engine against the harbor sample dataset:
> ```bash
> . .venv/bin/activate
> python code/security/kinematic_checks.py data/samples/synthetic_harbor.nmea --rx 42.36 -70.95
> ```
> Expected output:
> ```text
>      mmsi  score  fixes  speed_violations  max_implied_kn  sog_mismatch  turn_violations  teleports  beyond_range  max_range_nmi  invalid_mmsi
>         0      1     28                 0       12.031859             0                0          0             0      16.324760             1
>   1193046      1    120                 0        4.517441             0                0          0             0       5.134594             1
> 244999703      0    126                 0       14.544945             0                0          0             0      32.674542             0
> 316999704      0    301                 0       20.051188             0                0          0             0      26.229610             0
> 338123456      0    121                 0        6.018214             0                0          0             0       7.653746             0
> 338654321      0    120                 0        7.515078             0                0          0             0      12.274265             0
> 338999702      0    349                 0       18.043446             0                0          0             0      19.489121             0
> 366999701      0    326                 0       12.053396             0                0          0             0      18.276030             0
> 
> score >= 2 deserves a second look; score alone never proves spoofing.
> ```
> Implied speeds align with hull dynamics (< 21 kn) and zero teleports are detected. In spoofed theaters, score values surge.

## 62.6 Operational and technical workarounds

Maritime safety under GNSS denial depends on defense-in-depth across independent navigation layers:

### 1. Manual position input
Bridge teams can decouple the failed EPFS and manually input coordinates from visual bearings or radar ranges into the transponder. The unit transmits time stamp `61`, `PA = 0`, and Message 5 EPFD type `7` (manual input). However, manual entry increases bridge workload and cannot sustain dynamic maneuvering updates.

### 2. Radar overlay correlation and ARPA cross-checking
Marine radar (X-band 9.4 GHz, S-band 3.0 GHz) and ARPA measure microwave reflections directly from target hulls, operating independently of satellites. Overlaying AIS targets onto radar sweeps reveals anomalies:
- **Corroborated target:** AIS vector matches a radar echo.
- **Ghost/Spoofed target:** AIS symbol appears with no radar return.
- **Stealth target:** Solid radar echo without AIS (silenced Class B or disabled unit).
IMO Resolution A.1106(29) mandates that mariners never rely on AIS alone for collision avoidance.

### 3. Terrestrial R-Mode (Ranging Mode)
**R-Mode** superimposes synchronized ranging signals onto coastal radio infrastructure:
- **MF DGNSS radiobeacons (283.5–325 kHz):** Adding continuous-wave tones to MSK carriers.
- **VHF / VDES coastal stations (156–162 MHz):** Utilizing synchronization sequences for two-way ranging.
The **R-Mode Baltic** project demonstrated horizontal accuracy of 10 to 30 m in daytime and ~50 m under nighttime sky-wave interference across eight beacon sites.

### 4. eLoran and Chayka
**eLoran** (100 kHz) transmits multi-megawatt low-frequency groundwave pulses. High signal power (+20 to +40 dB over thermal noise) makes it practically immune to low-power jammers, delivering 8 to 20 m positioning and < 50 ns timing to sustain SOTDMA slot timing. Russia maintains Chayka (100 kHz). ITU-R M.1371-6 reserves EPFD type `4` for Loran-C and `5` for Chayka.

### 5. Inertial Navigation Systems (INS)
Fiber-Optic Gyroscope (**FOG**) or Ring Laser Gyroscope (**RLG**) INS coupled with Doppler Velocity Logs (**DVL**) provide dead reckoning drifting < 1 nmi per 24 hours, completely impervious to RF jamming. INS reports EPFD type `6` or `13` in Message 5.

### 6. VDES ranging
Under ITU-R M.2092-1 and IMO Resolutions MSC.592(111)/MSC.593(111), wideband VDES channels allow multilateration and two-way ranging from shore stations, providing ~10 m coastal positioning natively within the AIS/VDES architecture.

| System / Technique | Frequency Band | Typical Accuracy | Jamming Resilience | Infrastructure Requirement | Current Availability |
|---|---|---|---|---|---|
| **GNSS (GPS / Galileo / BDS)** | 1.1–1.6 GHz (UHF) | 1–5 m | Very Low | Satellite constellation | Global |
| **Radar / ARPA Overlay** | 3 GHz / 9 GHz (Microwave) | 10–30 m | Very High | Ship radar installation | Global (SOLAS mandate) |
| **R-Mode (MF Radiobeacon)** | 283.5–325 kHz (MF) | 10–30 m (day) / 55 m (night) | High | Coastal DGNSS tower upgrades | Baltic Sea testbed |
| **R-Mode (VDES / VHF)** | 156–162 MHz (VHF) | ~10 m | Moderate | Coastal VDES base stations | Experimental |
| **eLoran / Chayka** | 100 kHz (LF) | 8–20 m | Extremely High | High-power land towers | Regional (Korea, UK, Russia) |
| **Inertial + DVL** | Autonomous (internal) | < 1 nmi / 24 hr | Total | Shipborne INS/DVL unit | Ship-dependent |
| **Manual Input Mode** | N/A (human entry) | Sensor-dependent | Total | Bridge personnel | Global (contingency) |

## 62.7 Regulatory and international responses

Escalating GNSS interference has prompted regulatory action:
- **IMO Resolution MSC.401(95) / MSC.432(98):** Mandates multi-constellation support (GPS + Galileo + BeiDou) and automated integrity monitoring for shipborne receivers installed after 2017.
- **MSC.1/Circ.1575 (2017):** *Guidelines for Shipborne PNT Data Processing*. Establishes cross-verification standards between GNSS, speed logs, and gyrocompasses.
- **MSC.1/Circ.1644 (October 2021):** *Deliberate Interference with GNSS Signals*. Formally reminds Member States of ITU treaty obligations prohibiting harmful interference with safety frequencies.
- **ICAO circulars:** Address cross-domain aviation spoofing spilling into adjacent maritime straits.
- **IALA Guideline G1158:** Establishes international standards for VDES R-Mode terrestrial positioning.

> **Legal note.**
> Intentional jamming or spoofing of maritime radionavigation frequencies violates Article 45 of the International Telecommunication Union (**ITU**) Constitution and Section 15.1 of the ITU Radio Regulations. SOLAS Chapter V Regulation 19 obligates contracting governments to ensure safety of navigation. In the United States, transmitting jamming signals or false maritime distress coordinates violates 47 U.S.C. § 333 and 47 U.S.C. § 501, carrying criminal penalties, asset forfeiture, and civil liability. While electronic warfare during armed conflict is governed by naval warfare law, indiscriminate spoofing of commercial shipping in international straits violates international safety conventions.

## Then & now

- ⟨H⟩ 1998 — ITU-R M.1371-0 introduces SOTDMA for maritime AIS, establishing primary dependency on satellite 1 PPS timing and WGS-84 EPFS coordinates.
- ⟨H⟩ 2000 — United States terminates GPS Selective Availability (**SA**) on 2 May 2000, improving civilian GPS accuracy from 100 m to better than 15 m.
- ⟨+⟩ 2007 — Harati-Mokhtari et al. publish the first systematic analysis of commercial AIS data errors, documenting human configuration faults but noting near-zero malicious RF spoofing.
- ⟨+⟩ 2011 — IMO adopts Resolution A.1046(27), establishing formal recognition criteria for future Worldwide Radionavigation Systems (**WWRNS**).
- ⟨+⟩ 2014 — Balduzzi, Pasta, and Wilhoit present *A Security Evaluation of AIS* at ACSAC '14, demonstrating that AIS protocol vulnerabilities allow false vessel and weather broadcasts using low-cost SDRs.
- ⟨+⟩ 2015 — IMO adopts Resolution MSC.401(95) establishing performance standards for multi-system shipborne radionavigation receivers.
- ⟨+⟩ 2017 — US MARAD issues Maritime Advisory 2017-005A documenting mass GNSS spoofing in the Black Sea with vessels reporting false coordinates at Gelendzhik Airport.
- ⟨+⟩ 2017 — DLR and Baltic states launch the **R-Mode Baltic** project, building a multi-station terrestrial ranging testbed using MF and VDES.
- ⟨+⟩ 2018 — US Coast Guard issues Federal Register notice 83 FR 12402, permanently terminating the US Nationwide Differential Global Positioning System (**NDGPS**) network.
- ⟨+⟩ 2019 — C4ADS publishes *Above Us Only Stars*, exposing 9,883 GNSS spoofing incidents across Russia, Crimea, and Syria impacting over 1,300 commercial vessels.
- ⟨+⟩ 2019 — SkyTruth detects circular "crop circle" spoofing tracks affecting hundreds of cargo vessels in Shanghai.
- ⟨+⟩ 2021 — IMO Maritime Safety Committee approves MSC.1/Circ.1644 on deliberate GNSS interference.
- ⟨+⟩ 2023 — Spravil et al. develop the MARSIM dataset and demonstrate algorithmic NMEA sentence integrity monitoring to detect maritime GPS spoofing.
- ⟨+⟩ 2024 — IALA publishes Guideline G1158 (Edition 2.0) defining international standards for VDES R-Mode terrestrial positioning.
- ⟨+⟩ 2026 — ITU approves Recommendation ITU-R M.1371-6, refining synchronization hierarchies and maintaining standardized sentinel codes (61–63) for GNSS denial reporting.

## Validation, uncertainty & data quality

Analyzing maritime AIS records during electronic warfare conditions requires rigorous data hygiene:

### Error propagation and diagnostic metrics
GNSS interference propagates across three interface layers:
1. **RF Layer:** Interference degrades $C/N_0$. In jammed environments, $C/N_0$ drops below 30 dB-Hz, triggering loss of lock.
2. **Serial Bus Layer:** NMEA sentences reflect failure: `$GPGGA` fix quality drops to `0` (invalid); `$GPRMC` status sets to `V` (invalid); `$GPGBS` RAIM expected error exceeds 10 m.
3. **VHF Broadcast Layer:** The transponder encodes these parameters into outgoing VDL packets.

> **Worked example.** Algorithmic discrimination between legitimate voyage drift and deceptive GNSS spoofing.
> 
> Consider two consecutive position reports received ashore from a bulk carrier (45,000 GT, length 190 m):
> - **Report $k$ ($t_k = 08:30:00\text{ UTC}$):** Lat $\phi_k = 34.5000^\circ\text{ N}$, Lon $\lambda_k = 33.5000^\circ\text{ E}$, $\text{SOG}_k = 14.2\text{ kn}$, $\text{COG}_k = 090.0^\circ$, Time Stamp = `00`.
> - **Report $k+1$ ($t_{k+1} = 08:30:10\text{ UTC}$):** Lat $\phi_{k+1} = 34.8500^\circ\text{ N}$, Lon $\lambda_{k+1} = 33.9500^\circ\text{ E}$, $\text{SOG}_{k+1} = 14.1\text{ kn}$, $\text{COG}_{k+1} = 090.0^\circ$, Time Stamp = `10`.
> 
> We perform the kinematic plausibility test:
> 1. Calculate elapsed time:
>    $$\Delta t = 10\text{ seconds} = \frac{10}{3600}\text{ hr} \approx 0.002778\text{ hr}$$
> 2. Calculate spherical coordinate displacement:
>    $$\Delta \phi = 34.8500^\circ - 34.5000^\circ = +0.3500^\circ = 0.3500 \times 60\text{ nmi} = 21.00\text{ nmi}$$
>    $$\Delta \lambda = 33.9500^\circ - 33.5000^\circ = +0.4500^\circ$$
>    $$\text{Departure } \Delta x = \Delta \lambda \times \cos\left(\frac{\phi_k + \phi_{k+1}}{2}\right) \times 60\text{ nmi} = 0.4500 \times \cos(34.675^\circ) \times 60 \approx 22.20\text{ nmi}$$
> 3. Calculate total Euclidean displacement:
>    $$d = \sqrt{(\Delta \phi \times 60)^2 + (\Delta x)^2} = \sqrt{(21.00)^2 + (22.20)^2} \approx 30.56\text{ nmi}$$
> 4. Derive implied velocity:
>    $$V_{\text{implied}} = \frac{d}{\Delta t} = \frac{30.56\text{ nmi}}{0.002778\text{ hr}} \approx 11,000\text{ knots}$$
> 
> A displacement of 30.56 nmi in 10 seconds violates maritime physics. Because the vessel transmitted identical radio fingerprints but coordinates jumped inland to an airfield, the packet is flagged as a GNSS spoofing anomaly.

### Quantitative detection criteria
In automated data cleansing pipelines, records are tagged as GNSS interference anomalies when:
- **Velocity threshold:** Implied velocity $V_{\text{implied}} > 60\text{ kn}$ for standard cargo/tankers, or $> 90\text{ kn}$ for fast craft.
- **Acceleration threshold:** Implied acceleration $a = \frac{|V_{\text{implied}} - \text{SOG}|}{\Delta t} > 3.0\text{ m/s}^2$.
- **Displacement inconsistency:** Distance $d > 3 \times \text{SOG} \times \Delta t$.
- **Airport convergence:** Over 5 distinct MMSIs cluster within 500 m of an airfield runway.

## Software

**Open source:**
- `pyais` (Python): Pure-Python decoder supporting complete AIVDM encapsulation, decoding sentinels 61–63, RAIM flags, and EPFD fields. Caveat: Interpretation overhead limits throughput on massive historical archives.
- `libais` (C++ with Python bindings): High-throughput decoding library created by Kurt Schwehr. Parses bit fields and sentinels at line speed. Caveat: Requires pre-assembled single-line NMEA payloads.
- `AIS-catcher` (C++): Versatile SDR receiver and decoder supporting RTL-SDR, Airspy, and HackRF hardware with signal quality metrics. Caveat: Cannot validate the integrity of transmitting vessels' upstream GNSS.
- `gpsd` (C): Service daemon monitoring GPS and AIS units, exposing NMEA integrity metrics over TCP. Caveat: Configuration overhead in headless embedded systems.

**Free but closed:**
- `ShipPlotter` (Windows): Coastal AIS demodulator and display suite plotting tracks and lost signals. Caveat: Proprietary license; lacks automated headless scripting APIs.

**Commercial:**
- `Spire Maritime API`: Global satellite and terrestrial AIS streaming service offering automated GNSS-jamming detection layers. Caveat: Commercial subscription pricing.
- `Windward`: AI-driven maritime intelligence platform identifying dark fleet behaviors and spoofing anomalies. Caveat: Proprietary closed heuristics.
- `GPSPatron`: RF sensor hardware and cloud platform designed for real-time GNSS jamming and spoofing detection. Caveat: Requires on-site RF probe hardware.

## Standards & guides

- **International Maritime Organization (1998):** *Resolution MSC.74(69), Annex 3 — Performance Standards for Universal Shipborne AIS*. Governs WGS-84 EPFS processing.
- **International Maritime Organization (2011):** *Resolution A.1046(27) — Worldwide Radionavigation System*. Establishes satellite system recognition criteria.
- **International Maritime Organization (2015):** *Resolution A.1106(29) — Operational Use of Shipborne AIS*. Details bridge operational rules.
- **International Maritime Organization (2015):** *Resolution MSC.401(95) / MSC.432(98) — Performance Standards for Multi-System Shipborne Radionavigation Receivers*. Mandates multi-constellation processing.
- **International Maritime Organization (2017):** *MSC.1/Circ.1575 — Guidelines for Shipborne PNT Data Processing*. Framework for resilient bridge PNT data handling.
- **International Maritime Organization (2021):** *MSC.1/Circ.1644 — Deliberate Interference with GNSS Signals*. Formally reminds states of treaty duties.
- **International Telecommunication Union (2026):** *Recommendation ITU-R M.1371-6 — Technical characteristics for AIS*. Defines SOTDMA hierarchy and sentinels 60–63.
- **International Electrotechnical Commission (2018):** *IEC 61993-2:2018 — Class A Shipborne Equipment*. Operational testing for Class A transponders.
- **International Electrotechnical Commission (2017):** *IEC 62287-1:2017 & IEC 62287-2:2017 — Class B Shipborne Equipment*. Governs internal GNSS and transmission cessation rules.
- **International Association of Marine Aids to Navigation and Lighthouse Authorities (2024):** *IALA Guideline G1158 — VDES R-Mode*. Specification for terrestrial ranging.

## Pitfalls

- **Confusing GNSS jamming with AIS jamming:** Assuming the VHF link is jammed when an AIS unit stops broadcasting positions. In reality, the VHF radio functions normally; upstream GNSS reception has failed.
- **Discarding time stamp 63 packets as corrupt:** Filtering out incoming position reports containing time stamp sentinel `63` or coordinates 181° / 91°. Discarding these packets blinds pipelines to active jamming events.
- **Treating Position Accuracy (PA) flag as a verified guarantee:** Assuming `PA = 1` guarantees position accuracy within 10 m. Differentially corrected fixes without RAIM set `PA = 1` by default; spoofed receivers also broadcast `PA = 1`.
- **Assuming Class B transponders broadcast dead-reckoning status:** Expecting small craft to transmit degraded time stamps (sentinels 61–63) under jamming. Class B units cannot accept external feeds and are prohibited from transmitting Messages 18/24 when internal GNSS fails, vanishing completely.
- **Assuming an isolated vessel can spoof its own AIS position via NMEA input without external detection:** Believing a vessel can manually enter false coordinates into an ECDIS to fabricate an alibi track. Terrestrial receiver horizons and satellite footprints quickly unmask hand-keyed coordinate shifts.
- **Relying on AIS as a solitary collision-avoidance tool during electronic warfare:** Maneuvering solely by AIS on ECDIS rather than maintaining radar/ARPA plotting and optical lookout, risking collisions with ghost targets or un-broadcast real ships.
- **Ignoring the SOTDMA synchronization cascade:** Overlooking how regional GNSS loss degrades slot timing across coastal cells, forcing transponders down into semaphore mode and increasing VHF packet collisions.
- **Mistaking military C-UAV counter-measures for targeted maritime attacks:** Failing to recognize that maritime vessels reporting positions at international airports are usually collateral casualties of shore-based drone geofencing shields.
- **Failing to validate static MMSI continuity during coordinate jumps:** Tagging a track jump as GNSS spoofing when it is actually an interleaved transmission from a second vessel sharing a factory-default MMSI (e.g., `1193046`).
- **Ignoring VHF line-of-sight bounds when triaging reports:** Accepting an inland AIS report at face value without checking whether the terrestrial base station logging the packet had a physically possible radio line of sight.

## Key takeaways

- AIS is inherently dual-dependent on satellite navigation: requiring GNSS coordinates for spatial position reporting and GNSS 1 PPS strobes for SOTDMA slot synchronization.
- GNSS jamming produces an observable failure cascade: receivers flag invalid status, transponders broadcast time stamp sentinels `62` (DR) or `63` (inoperative) with coordinates 181° / 91°, Class B units cease transmitting, and TDMA timing degrades down the synchronization hierarchy.
- GNSS spoofing deceives receivers into broadcasting false coordinates (often exhibiting airport circular clusters) with apparent high accuracy (`PA = 1`) and active RAIM.
- Global terrestrial and spaceborne AIS collection networks function as an unintended distributed sensor for electronic warfare, mapping regional jamming and spoofing footprints.
- The most robust immediate shipborne counter-measure is radar/ARPA overlay correlation, verifying whether an AIS target corresponds to a physical microwave echo.
- Terrestrial R-Mode (MF radiobeacon and VDES ranging) and eLoran provide resilient alternative PNT capable of sustaining coastal navigation and SOTDMA slot timing during satellite denial.
- International regulations (SOLAS Chapter V, ITU Radio Regulations Art. 15.1, IMO MSC.1/Circ.1644) strictly outlaw intentional interference with radionavigation, obligating maritime administrations to build resilience into shipborne systems.

## References

1. Androjna, A., Perkovič, M., Pavić, I. & Mišković, J. (2021). AIS Data Vulnerability Indicated by a Spoofing Case-Study. *Applied Sciences*, 11(11):5015. doi:10.3390/app11115015.
2. Balduzzi, M., Pasta, A. & Wilhoit, K. (2014). A Security Evaluation of AIS Automated Identification System. In *Proceedings of the 30th Annual Computer Security Applications Conference (ACSAC '14)*, pages 436–445. New Orleans, USA: ACM. doi:10.1145/2664243.2664257.
3. Center for Advanced Defense Studies (2019). *Above Us Only Stars: Exposing GPS Spoofing in Russia and Syria*. Washington, DC: C4ADS. https://c4ads.org/reports/above-us-only-stars/.
4. Federal Register (2018). *Discontinuance of the Nationwide Differential Global Positioning System (NDGPS)*. 83 FR 12402, Docket No. USCG-2018-0179, pages 12402–12404. Washington, DC: National Archives and Records Administration.
5. Harati-Mokhtari, A., Wall, A., Brooks, P. & Wang, J. (2007). Automatic Identification System (AIS): Data Reliability and Human Error Implications. *The Journal of Navigation*, 60(3):373–389. doi:10.1017/S037346330700429X.
6. International Association of Marine Aids to Navigation and Lighthouse Authorities (2024). *IALA Guideline G1158 on VDES R-Mode*. Edition 2.0. Saint-Germain-en-Laye, France: IALA.
7. International Electrotechnical Commission (2017). *Maritime navigation and radiocommunication equipment and systems – Class B shipborne equipment of the automatic identification system (AIS) – Part 1: Carrier-sense time division multiple access (CSTDMA) techniques* (Standard No. IEC 62287-1:2017). Edition 3.0. Geneva: IEC.
8. International Electrotechnical Commission (2017). *Maritime navigation and radiocommunication equipment and systems – Class B shipborne equipment of the automatic identification system (AIS) – Part 2: Self-organising time division multiple access (SOTDMA) techniques* (Standard No. IEC 62287-2:2017). Edition 2.0. Geneva: IEC.
9. International Electrotechnical Commission (2018). *Maritime navigation and radiocommunication equipment and systems – Automatic Identification Systems (AIS) – Part 2: Class A shipborne equipment of the automatic identification system (AIS) – Operational and performance requirements, methods of test and required test results* (Standard No. IEC 61993-2:2018). Edition 3.0. Geneva: IEC.
10. International Maritime Organization (1998). *Recommendation on Performance Standards for a Universal Shipborne Automatic Identification System (AIS)* (Resolution MSC.74(69), Annex 3). Adopted 12 May 1998. London: IMO.
11. International Maritime Organization (2011). *Worldwide Radionavigation System* (Resolution A.1046(27)). Adopted 30 November 2011. London: IMO.
12. International Maritime Organization (2015). *Performance Standards for Multi-System Shipborne Radionavigation Receivers* (Resolution MSC.401(95), amended by MSC.432(98)). Adopted 8 June 2015. London: IMO.
13. International Maritime Organization (2015). *Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems (AIS)* (Resolution A.1106(29)). Adopted 2 December 2015. London: IMO.
14. International Maritime Organization (2017). *Guidelines for Shipborne Position, Navigation and Timing (PNT) Data Processing* (Circular MSC.1/Circ.1575). Approved 16 June 2017. London: IMO.
15. International Maritime Organization (2021). *Deliberate Interference with GNSS Signals* (Circular MSC.1/Circ.1644). Approved October 2021. London: IMO.
16. International Telecommunication Union (2006). *Technical characteristics of differential transmissions for global navigation satellite systems from maritime radio beacons in the frequency band 283.5-325 kHz* (Recommendation ITU-R M.823-3). Geneva: ITU Radiocommunication Sector.
17. International Telecommunication Union (2022). *Technical characteristics for a VHF data exchange system in the VHF maritime mobile band* (Recommendation ITU-R M.2092-1). Geneva: ITU Radiocommunication Sector.
18. International Telecommunication Union (2026). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band* (Recommendation ITU-R M.1371-6). Geneva: ITU Radiocommunication Sector.
19. Rizzi, M., Grundhöfer, M., Gewies, S. & Ehlers, F. (2023). R-Mode Baltic: Results of the Demonstration and Performance Assessment of a Terrestrial Resilient PNT System. *Applied Sciences*, 13(3):1872. doi:10.3390/app13031872.
20. Šafář, J., Grant, A., Williams, P. & Ward, N. (2019). R-Mode: A Feasibility Study of Terrestrial Radionavigation as a Backup to GNSS in the Maritime Domain. *The Journal of Navigation*, 72(5):1073–1094. doi:10.1017/S0373463319000559.
21. Spravil, J., Hemminghaus, C., von Rechenberg, M., Padilla, E. & Bauer, J. (2023). Detecting Maritime GPS Spoofing Attacks Based on NMEA Sentence Integrity Monitoring. *Journal of Marine Science and Engineering*, 11(5):928. doi:10.3390/jmse11050928.
22. United States Maritime Administration (2017). *Black Sea – GPS Interference* (Maritime Safety Advisory 2017-005A). Washington, DC: MARAD.
