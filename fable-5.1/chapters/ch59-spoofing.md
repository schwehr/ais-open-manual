# Chapter 59 — AIS spoofing techniques and detection

> **Part IX — Security.** An analysis of maritime Automatic Identification System spoofing mechanisms, illicit track fabrication, physical-layer and kinematic detection methodologies, and spaceborne verification frameworks.

**In this chapter.** You will learn how to identify, categorize, and detect deliberate spoofing across the maritime Automatic Identification System (**AIS**). We dissect the mechanics of identity spoofing, synthetic track injection, and collateral GNSS-induced position corruption, contrasting radio frequency (**RF**) synthesis with aggregator-level software manipulation. You will evaluate high-profile geopolitical and commercial cases—including the Black Sea naval displacements, Shanghai container port "crop circles", Point Reyes ghost tracks, and sanctions-evasion operations. We develop multi-layered defensive frameworks spanning kinematic consistency, radio horizon and propagation plausibility, multi-receiver Time Difference of Arrival (**TDOA**), RF fingerprinting, and spaceborne Synthetic Aperture Radar (**SAR**) cross-correlation. Finally, you will execute automated track-triage algorithms and establish responsible disclosure procedures for verified maritime electronic attacks.

## 59.1 Taxonomy of AIS spoofing

The operational architecture of the Automatic Identification System relies on unauthenticated, cleartext broadcasts over maritime VHF frequencies (161.975 MHz and 162.025 MHz), as standardized in Recommendation ITU-R M.1371 (2014). Because the link layer incorporates no cryptographic signatures or sender verification ([Chapter 58](ch58-threat-model.md)), any transmitter capable of formatting High-Level Data Link Control (**HDLC**) frames and calculating a standard 16-bit Cyclic Redundancy Check (**CRC**) can inject arbitrary data into the maritime domain. To dissect these attacks rigorously, we classify maritime deception across three technical vectors: identity spoofing, RF/software position spoofing, and collateral GNSS-induced spoofing.

```
                        AIS Manipulation Landscape
                                    |
     +------------------------------+------------------------------+
     |                                                             |
[RF Domain Attacks]                                     [Network & Sensor Attacks]
     |                                                             |
     +--> Identity Spoofing (MMSI cloaking/cloning)                +--> Software Ingestion Injection
     +--> Phantom/Ghost Track RF Synthesis                         +--> Transponder Interface Tampering
     +--> Fake AtoN & SART Injection                               +--> Collateral GNSS Spoofing
     +--> Coordinated "Dark Fleet" Masking
```

### 59.1.1 Identity spoofing vs. position spoofing
Maritime deception bifurcates into the manipulation of *who* is broadcasting versus *where* the broadcaster claims to be located:

1. **Identity Spoofing (MMSI and Static Tampering):** The transmitting vessel alters its identity parameters while broadcasting from its genuine physical position, or assumes the identity of another legitimate hull.
   - *MMSI Cloning:* An illicit vessel programs its transponder with the Maritime Mobile Service Identity (**MMSI**) of an active, compliant merchant ship operating elsewhere ([Chapter 13](ch13-mmsi-deep-dive.md)). Downstream aggregation engines receive interleaved position reports, generating erratic "teleportation" jumps across ocean basins.
   - *Zombie Vessel Hijacking:* Illicit operators adopt the identity credentials (MMSI, IMO ship identification number, callsign, and name) of a retired, scrapped, or dormant hull (Windward 2021). The ghost entity appears legally registered in global databases while the underlying physical ship conducts clandestine operations.
   - *Static Flag Hopping:* Rapid alteration of flag state, callsign, or vessel classification in Message 5 / Message 24 static reports to frustrate Port State Control (**PSC**) screening.

2. **Position Spoofing (Kinematic and Spatial Fabrication):** The transmitter preserves or falsifies its identity but broadcasts coordinates that do not correspond to the physical antenna position.
   - *Offshore Projection (False Alibi):* A vessel engaged in illicit ship-to-ship (**STS**) petroleum transfers or illegal, unreported, and unregulated (**IUU**) fishing broadcasts realistic cruising or drifting tracks in international waters, while its physical hull is tied to an embargoed crude terminal or operating inside an exclusive economic zone (**EEZ**).
   - *Phantom Vessel Synthesis:* A terrestrial Software-Defined Radio (**SDR**) or shore station synthesizes complete "ghost ships" that have no physical hull counterpart at sea, fabricating standard periodic Message 1, 2, or 3 position reports and Message 5 static voyage data.

> **Definitions that bite.**
> - **AIS "Dark Activity" vs. AIS Spoofing:** A vessel going "dark" disables its transponder (cutting power or disconnecting the antenna), ceasing transmission. In contrast, **AIS spoofing** is active transmission: the vessel emits RF energy or software telemetry, but the broadcast data is deliberately falsified, displaced, or synthesized.
> - **Direct RF Spoofing vs. Aggregator Injection:** Direct RF spoofing radiates electromagnetic energy on VHF channels AIS 1 and AIS 2, deceiving local shipboard radars, ECDIS units, and coastal VTS antennas within radio line-of-sight. Aggregator injection transmits forged NMEA sentences directly into unauthenticated network ingestion feeds, polluting global map displays without emitting an RF signal.
> - **AIS Spoofing vs. GNSS Spoofing:** In AIS spoofing, the transponder or SDR generates an AIS protocol frame with forged lat/lon fields. In GNSS spoofing, an external RF jammer/simulator attacks the ship's GNSS antenna with false satellite signals; the ship's onboard transponder is authentic, but faithfully broadcasts the forged GNSS fix it received ([Chapter 25](ch25-gnss-and-ais.md); [Chapter 62](ch62-gnss-jamming-spoofing.md)).

### 59.1.2 Collateral GNSS spoofing-induced AIS anomalies
A significant portion of historical maritime "AIS spoofing" incidents are fundamentally GNSS electronic warfare attacks observed through the lens of AIS telemetry. Under IEC 61993-2 (2018), Class A transponders are hardwired to internal or external Electronic Position Fixing System (**EPFS**) receivers via NMEA 0183 `GNS`, `GGA`, or `RMC` sentences ([Chapter 26](ch26-interfaces-and-logging.md)). When a regional electronic warfare system broadcasts false GNSS satellite ranging signals, the ship's GNSS receiver computes a false position solution.

The AIS transponder cannot validate the GNSS solution independently; it packages the erroneous coordinates directly into Message 1, 2, or 3 payloads and transmits them over the VHF data link (**VDL**). Consequently, coastal and spaceborne receivers record spatial anomalies—such as dozens of merchant ships suddenly clustering on an inland airport runway or drawing geometric spirals—even though ship masters committed no intentional deception.

## 59.2 Ghost ships, fake fleets, and synthetic infrastructure

The unauthenticated nature of Recommendation ITU-R M.1371 enables the synthetic fabrication of entire naval formations, phantom maritime hazards, and fake emergency distress beacons (Balduzzi, Pasta & Wilhoit 2014).

```
                      Synthetic AIS Entity Types
                                  |
     +----------------------------+----------------------------+
     |                            |                            |
[Vessel Targets]          [Fixed & Floating AtoN]      [Search & Rescue SART]
Message 1, 2, 3, 5, 18    Message 21                   Message 1, 9, 14
- Naval warship incursions - Phantom shoal/wreck buoys  - False MOB beacons
- Sanctions shadow fleets  - Misplaced safe-water marks - False 970xxxxxx SART
- False alibi tracks       - Spoofed virtual AtoN locks - Emergency search diversion
```

### 59.2.1 Fake Aids to Navigation (AtoN)
AIS Message 21 defines Aids to Navigation (**AtoN**) reporting, including physical AtoN and **virtual AtoN** (where a shore station broadcasts a Message 21 designating a navigational hazard at coordinates where no physical structure exists, displayed directly on ECDIS screens; see [Chapter 22](ch22-message-catalog.md)).

An attacker with an SDR can broadcast fraudulent Message 21 frames:
- **Phantom Hazard Injection:** Injecting virtual isolated danger marks, sunken wreck buoys, or restricted area polygons across a busy shipping channel or Traffic Separation Scheme (**TSS**). Navigating officers and autonomous surface vessels (**ASVs**) observing these official symbols on ECDIS may execute abrupt collision-avoidance maneuvers.
- **Off-Position Falsification:** Spoofing a physical buoy's Message 21 while clearing the "off-position" indicator bit, or altering the reported position coordinates by several cables (hundreds of meters), creating grounding hazards in restricted visibility.
- **AtoN Identity Spoofing:** Transmitting under the 99-MID-XXXX structure reserved for aids to navigation, evading basic vessel filtering.

### 59.2.2 Search and Rescue Transmitter (SART) spoofing
AIS Search and Rescue Transmitters (**AIS-SART**, Message 1 and 14), Man Overboard devices (**AIS-MOB**), and EPIRB-AIS units use specific MMSI prefix ranges (e.g., `970XXXXXX` for SART, `972XXXXXX` for MOB; see [Chapter 13](ch13-mmsi-deep-dive.md) and [Chapter 68](ch68-special-purpose-ais.md)).

When an AIS-SART message is received, shipboard ECDIS and radar units generate high-priority visual and audible emergency alarms, displaying a circle with an "X" symbol and broadcasting text messages: `SART ACTIVE`. 
- **Resource Exhaustion:** Fabricating multiple SART beacons in offshore waters diverts Coast Guard cutters and commercial vessels under SOLAS Chapter V rescue obligations away from primary operational sectors.
- **Alarm Storms:** Broadcasting a continuous barrage of rotating SART MMSIs saturates bridge displays, inducing cognitive fatigue or compelling watchstanders to silence alarms entirely.

### 59.2.3 Commercial "Spoofing-as-a-Service" and sanctions evasion
The enforcement of international maritime sanctions has transformed AIS spoofing into a specialized underground industry catering to the crude oil "shadow fleet" (Windward 2021).

Specialized service providers execute sophisticated evasion tactics:
- **Pre-programmed Track Injection:** Vendors generate kinematically plausible synthetic voyage files mimicking round-trip voyages in international waters.
- **Physical RF Simulators Onboard:** Vessels install hardware emulators connected directly to the transponder's external GNSS antenna input or pilot port. While the tanker physically docks at an embargoed terminal to load crude, the simulator broadcasts the synthetic track over the local VHF link or routes it to satellite constellations.
- **AIS Rendezvous and Swapping:** Two identical-class tankers meet in open water. Vessel A (illicit) assumes the identity and AIS transmissions of Vessel B (clean), while Vessel B disables its transponder or spoofs an anchored position. Vessel A sails into port under the clean identity, discharges cargo, and returns, swapping digital identities back upon rendezvous.

> **Threat model.**
> - **Primary Assets:** ECDIS and radar situational awareness; VTS maritime safety surveillance; global sanctions compliance monitoring; Search and Rescue (**SAR**) emergency response resources.
> - **Threat Actors:** Hostile state electronic warfare battalions; transnational sanctions-evasion syndicates; rogue fishing fleets (IUU); maritime smugglers; cyber-security researchers and script hobbyists.
> - **Attacker Capabilities:**
>   - *Terrestrial SDR Transmit:* 1–25 W VHF transmission of crafted GMSK bursts from shore, small watercraft, or covert shore sites, injecting false vessels, AtoNs, and SARTs within a 20–30 nmi radius.
>   - *GNSS Meaconing/Simulation:* Over-the-air broadcasting of false GPS/GLONASS signals targeting commercial transponders in straits or anchorages.
>   - *Network Ingestion Injection:* Automated TCP/IP socket connections injecting thousands of forged `!AIVDM` sentences directly into open crowd-sourced aggregators without RF hardware.
> - **Impact:** Severe navigational collision hazards in confined waterways; bridge alarm saturation; diversion of search-and-rescue assets; systematic blinding of sanctions enforcement bodies.
> - **Engineering Mitigations:** Kinematic speed/acceleration filters; multi-receiver coverage and line-of-sight plausibility checking; dual-station TDOA geolocation; RF physical-layer fingerprinting; multi-modal spaceborne SAR/optical validation.

## 59.3 Documented spoofing cases

Real-world AIS and GNSS spoofing has transitioned from academic demonstrations to geopolitical electronic warfare, port-level economic manipulation, and industrialized sanctions cloaking.

```
                             Chronology of Key Incidents
  2017                   2019                   2020                   2021             2023–2026
   |                      |                      |                      |                   |
Black Sea              Shanghai               Point Reyes            Black Sea            Baltic Sea
Gelendzhik Airport     "Crop Circles"         "Crop Circles"         HMS Defender         Mass Jamming &
Inland Relocation      Huangpu River          Global Relocations     Phantom Track        Runway Offsets
(C4ADS 2019)           (Harris 2019)          (SkyTruth / Bergman)   Sevastopol Probe     (Gattis et al. 2026)
```

### 59.3.1 Black Sea and Gelendzhik Airport (June 2017)
On June 22, 2017, the master of the commercial tanker *Atria*, anchored off the Russian Black Sea port of Novorossiysk, observed that the vessel's primary GPS display and Class A AIS transponder reported its position as Gelendzhik Airport—approximately 32 km (17 nmi) inland (C4ADS 2019). Over 20 commercial ships in the anchorage experienced the identical coordinate shift. When vessels navigated away from the anchorage, their reported GPS positions remained locked to the airport runway or hopped erratically across inland locations.

The Center for Advanced Defense Studies (C4ADS) investigated this and subsequent regional anomalies in their report *Above Us Only Stars* (2019). C4ADS documented 9,883 individual instances of GNSS spoofing affecting 1,311 commercial vessels across the Black Sea, Crimea, the Sea of Azov, and Syrian waters between 2016 and 2018. The primary vector was ground-based GNSS spoofing: military electronic warfare transmitters forced commercial GNSS receivers to lock onto coordinates deliberately mapped to civilian airports. This tactic exploited the built-in "no-fly zone" geofencing firmware of commercial drones, forcing approaching quadcopters to land immediately. The disruption to maritime AIS was collateral damage.

### 59.3.2 Shanghai and the Huangpu River "Crop Circles" (2019)
Throughout 2019, maritime analysts, container ship captains, and academic researchers noticed extreme spatial distortions in AIS data originating from the Port of Shanghai and the mouth of the Yangtze River (Harris 2019). Commercial vessels navigating the congested waterways—including the US-flagged container ship *MV Manukai* in July 2019—observed phantom targets appearing on radar and ECDIS, followed by sudden failure of their own primary GPS receivers.

When analysts plotted the historical AIS tracks of hundreds of affected vessels, the trajectories formed unmistakable geometric patterns: concentric loops, expanding ovals, and repeating circles over land and water, dubbed "GPS crop circles" (Harris 2019). Rather than shifting ships to a fixed airport, the spoofing system systematically shifted the computed position along a rotating circular vector, with track speeds exceeding 60–100 kn. Investigations linked the spoofing to a combination of military electronic protection testing and clandestine commercial operations—specifically illegal sand-dredging barges operating in the Yangtze River, utilizing commercial GPS jammers and spoofers to cloak illegal extraction sites from surveillance authorities.

### 59.3.3 The Point Reyes global anomaly (2020)
In mid-2020, data analyst Bjorn Bergman, conducting research for SkyTruth and Global Fishing Watch, uncovered an extraordinary anomaly: multiple commercial vessels operating in disparate regions of the globe suddenly began transmitting AIS positions that placed them in tight circular patterns off Point Reyes, California, just north of San Francisco (Bergman 2020).

The affected vessels included an offshore supply vessel in the Gulf of Guinea, a livestock carrier in the Mediterranean Sea near Libya, a crude tanker in the Persian Gulf, and a bulk carrier in the Suez Canal. Across several weeks, their transponders broadcasted trajectories tracing repeating ovals and circles directly across the Point Reyes peninsula and surrounding coastal waters. Unlike the Shanghai or Black Sea cases—where vessels were physically present in the general region of the jamming transmitter—the Point Reyes vessels were physically located 5,000 to 12,000 km away. Analysis indicated that the anomaly was caused by false GNSS coordinate injection into transponders, where coordinates 38°N, 123°W represented a default test coordinate in marine navigation firmware or deliberate electronic manipulation testing. The signals were recorded simultaneously by terrestrial coastal stations in California and commercial satellite AIS constellations, proving that the anomaly was broadcasted over the RF link rather than injected into an aggregator's database.

### 59.3.4 Black Sea naval phantom incursions: HMS Defender and HNLMS Evertsen (June 2021)
On June 18, 2021, public AIS tracking services displayed live tracks showing two major NATO warships—the UK Royal Navy Type 45 destroyer *HMS Defender* (D36) and the Royal Netherlands Navy frigate *HNLMS Evertsen* (F805)—departing the Ukrainian port of Odesa and sailing directly toward Sevastopol in occupied Crimea. The AIS tracks showed the warships closing to within 2 nmi (3.7 km) of Sevastopol harbor entrance.

In reality, neither warship had left the pier. Live harbor webcams, commercial satellite imagery, and on-scene civilian observers confirmed that both *HMS Defender* and *HNLMS Evertsen* remained moored alongside in Odesa throughout the entire incident. The false tracks were generated via synthetic AIS injection, designed to create a provocative digital narrative of Western naval aggression in the regional information space. Five days later, on June 23, 2021, *HMS Defender* undertook a physical transit from Odesa to Batumi, Georgia, exercising innocent passage through the territorial waters of Ukraine off Cape Fiolent, Crimea—leading to a widely publicized confrontation with Russian naval and air forces.

### 59.3.5 Baltic Sea GNSS and AIS disruptions (2023–2026)
Following the Russian invasion of Ukraine in 2022, the Baltic Sea basin emerged as an active zone of sustained GNSS interference and maritime tracking corruption (Gattis, Cydejko & Akos 2026). Across the Gulf of Finland, the waters off Kaliningrad, and the central Baltic shipping lanes, commercial vessels, oil tankers, and passenger ferries have experienced daily GNSS outages, position jumps, and false runway-offset spoofing.

Civil aviation and maritime safety agencies in Finland (Traficom), Sweden, Estonia, and Poland logged thousands of hours of severe satellite navigation degradation. Ground-based multi-receiver radiolocation studies confirmed that primary interference sources were high-powered military electronic warfare stations operating from the Kaliningrad exclave and coastal sites near Saint Petersburg, complemented by mobile shipborne jammers deployed on Russian auxiliary naval vessels (Gattis, Cydejko & Akos 2026). The disruption forced commercial mariners to revert to visual terrestrial navigation, primary X-band/S-band radar fixing, and terrestrial radio navigation testbeds such as R-Mode Baltic ([Chapter 43](ch43-demonstration-programs.md)).

## 59.4 Detection methodologies: physics, kinematics, and propagation

Because AIS carries no cryptographic integrity guarantees, verification must rely on physical properties that an adversary cannot forge: the laws of kinematics, the geometric limits of radio propagation, and the physical characteristics of the transmitted RF signal.

```
                      Layered Spoofing Detection Stack
                                    |
   +--------------------------------+--------------------------------+
   |                                |                                |
[Level 1: Kinematic Triage]   [Level 2: Spatial & RF Coverage]  [Level 3: Physical Geometry]
- Implied SOG vs. Class Cap   - Radio Horizon / Footprint       - Dual/Triple Base TDOA Fix
- Rate of Turn (ROT) Limits   - Terrestrial vs. Satellite Sync  - LEO Doppler Curve Match
- Acceleration / Teleports    - Multi-Station Overlap Grid      - RF Fingerprinting (SEI)
```

### 59.4.1 Kinematic and trajectory consistency
The first line of automated defense is track kinematic plausibility. A genuine ship is a massive physical body subject to hydrodynamic resistance, inertia, and propulsion constraints. Any reported trajectory violating these physical bounds indicates data corruption or deliberate spoofing.

Let consecutive position reports $P_i = (\phi_i, \lambda_i, t_i)$ and $P_{i+1} = (\phi_{i+1}, \lambda_{i+1}, t_{i+1})$ define the trajectory of a vessel with broadcast MMSI $M$.
1. **Implied Speed Over Ground ($V_{\text{implied}}$):**
   Using great-circle haversine distance $D(P_i, P_{i+1})$:
   $$\Delta t = t_{i+1} - t_i, \quad V_{\text{implied}} = \frac{D(P_i, P_{i+1})}{\Delta t}$$
   If $V_{\text{implied}} > V_{\text{cap}}(C)$, where $V_{\text{cap}}$ is the physical maximum speed for vessel class $C$ (e.g., 45 kn for Class A cargo, 60 kn for high-speed craft), the segment is flagged.
2. **Kinematic SOG Mismatch:**
   Comparing implied speed to the transponder's self-reported Speed Over Ground ($SOG_i, SOG_{i+1}$):
   $$\epsilon_v = \left| V_{\text{implied}} - \frac{SOG_i + SOG_{i+1}}{2} \right|$$
   A persistent divergence $\epsilon_v > 5.0\text{ kn}$ over multiple reporting intervals indicates inconsistent positioning.
3. **Turn Rate Violations:**
   The implied angular velocity $\omega_{\text{implied}}$ derived from consecutive Course Over Ground ($COG$) reports:
   $$\Delta COG = |(COG_{i+1} - COG_i + 180^\circ) \pmod{360^\circ} - 180^\circ|, \quad \omega_{\text{implied}} = \frac{\Delta COG}{\Delta t}$$
   Commercial cargo vessels rarely exceed turning rates of $2^\circ/\text{s}$ to $4^\circ/\text{s}$; an $\omega_{\text{implied}} > 10.0^\circ/\text{s}$ indicates synthetic positioning.
4. **Teleportation Discontinuities:**
   Any spatial displacement $D(P_i, P_{i+1}) > 1.0\text{ nmi}$ occurring over an interval $\Delta t < 60\text{ s}$ constitutes an unphysical spatial discontinuity.

### 59.4.2 Receiver coverage and radio horizon plausibility
Radio propagation in the maritime VHF band (156–162 MHz) is governed by line-of-sight propagation modified by atmospheric refraction ([Chapter 27](ch27-rf-basics.md); [Chapter 29](ch29-propagation-modeling.md)). Under standard atmospheric conditions ($k = 4/3$), the maximum radio horizon distance $d_{\text{los}}$ between a transmitter with antenna height $h_{\text{tx}}$ and a receiver with antenna height $h_{\text{rx}}$ (in meters) is:

$$d_{\text{los}} \approx 4.12 \left( \sqrt{h_{\text{tx}}} + \sqrt{h_{\text{rx}}} \right) \quad [\text{km}] \approx 2.22 \left( \sqrt{h_{\text{tx}}} + \sqrt{h_{\text{rx}}} \right) \quad [\text{nmi}]$$

For a typical shore base station on a headland ($h_{\text{rx}} = 100\text{ m}$) receiving a Class A shipboard antenna ($h_{\text{tx}} = 25\text{ m}$):
$$d_{\text{los}} \approx 4.12 (\sqrt{100} + \sqrt{25}) = 4.12 (10 + 5) = 61.8\text{ km} \approx 33.4\text{ nmi}$$

**The Coverage Plausibility Rule:**
If a terrestrial shore receiver $R_k$ receives an unamplified terrestrial AIS message directly over the air, the true transmitter *must* lie within the receiver's physical line-of-sight horizon (accounting for extreme tropospheric ducting, which can occasionally extend ranges to 150–300 nmi; see [Chapter 29](ch29-propagation-modeling.md)). If the coordinates broadcasted inside the payload place the ship 1,000 nmi away across an ocean basin, the report is unequivocally spoofed or the victim of severe GNSS dislocation.

Furthermore, in multi-receiver shore networks, **spatial non-detection** provides powerful negative evidence:
If a vessel claims to be navigating 2 nmi off Station A's mast, but Station A receives no signal, while Station B (located 80 nmi away) receives strong $-85\text{ dBm}$ bursts from the vessel, the vessel is not at its reported position.

### 59.4.3 Satellite vs. terrestrial reception disagreement
Low Earth Orbit (**LEO**) satellite constellations operate at altitudes between 500 km and 850 km, sweeping an instantaneous field of view (**FOV**) with a footprint diameter of 4,000 to 5,000 km ([Chapter 39](ch39-satellite-ais.md)).

Comparing terrestrial and spaceborne reception logs exposes specific attack modalities:
1. **Ghost Fleets Heard Only Terrestrially:** When an attacker injects thousands of synthetic ships into an aggregator via unauthenticated Internet feeds, terrestrial aggregators display the vessels globally. However, spaceborne AIS satellites flying over the claimed open-ocean coordinates record zero VDL bursts in those TDMA slots.
2. **Terrestrial Masking:** An attacker broadcasting local RF spoofing with a low-power, horizontally directed antenna may deceive nearby surface vessels within 5 nmi while failing to generate sufficient vertical power to reach overhead LEO receivers, or conversely, saturating satellite receivers while being blocked by coastal terrain from reaching shore base stations.

## 59.5 Independent physical-layer verification

When kinematic triage indicates suspicion, definitive verification requires physical-layer measurement of the emitted waveform. An attacker can forge every byte of an AIS packet, but cannot forge the physical propagation delay of the radio wave or alter the orbital velocity of an observing satellite.

```
       Physical-Layer Verification Modalities
                         |
     +-------------------+-------------------+
     |                                       |
[Time Difference of Arrival]           [Satellite Doppler Radiolocation]
- Shore Station Hyperbolic Fixing      - Single-LEO Frequency Shift Curves
- Requires nanosecond time-stamping    - Matches expected pass profile
- Discrepancies > 500 m exposed        - FOV velocity differential: ±3.8 kHz
```

### 59.5.1 Multi-receiver Time Difference of Arrival (TDOA)
Time Difference of Arrival radiolocation determines the true physical position of an emitter by measuring the difference in arrival times of the exact same transmitted burst at three or more geographically separated, time-synchronized receiving stations (Papi et al. 2015).

An AIS burst occupies a single 26.67 ms TDMA time slot (256 bits at 9,600 bit/s; [Chapter 21](ch21-link-layer-tdma.md)). The preamble consists of a 24-bit alternating training sequence (`0101...`), followed by an 8-bit start flag (`01111110`). By cross-correlating sampled raw I/Q baseband waveforms or timestamping detected synchronization flags using GNSS-disciplined oscillators (timing jitter $\sigma_t < 50\text{ ns}$), each receiver logs an exact time of arrival $t_k$.

For receivers $R_1, R_2, R_3$ located at Cartesian positions $\mathbf{r}_1, \mathbf{r}_2, \mathbf{r}_3$:
$$\Delta t_{jk} = t_j - t_k = \frac{\|\mathbf{r}_j - \mathbf{x}\| - \|\mathbf{r}_k - \mathbf{x}\|}{c}$$

where $\mathbf{x}$ is the true emitter position and $c$ is the speed of light ($2.99792 \times 10^8\text{ m/s}$).

Each pair of stations defines a hyperbola of possible positions:
$$d_{jk} = c \cdot \Delta t_{jk} = \|\mathbf{r}_j - \mathbf{x}\| - \|\mathbf{r}_k - \mathbf{x}\|$$

The intersection of two or more independent hyperbolae yields an unambiguous physical fix $\mathbf{x}_{\text{true}}$ on the surface of the earth.

If the distance between the reported position inside the decoded payload $\mathbf{x}_{\text{AIS}}$ and the physical TDOA solution $\mathbf{x}_{\text{true}}$ exceeds the system's geometric dilution of precision (**GDOP**) error boundary:
$$\|\mathbf{x}_{\text{AIS}} - \mathbf{x}_{\text{true}}\| > 3\sigma_{\text{TDOA}}$$
the transmission is definitively classified as spoofed. As demonstrated by Papi et al. (2015) using coastal base stations, TDOA networks detect position falsifications on the order of hundreds of meters without requiring modifications to shipboard hardware.

### 59.5.2 Satellite Doppler radiolocation
A single LEO satellite orbiting at altitude $H \approx 650\text{ km}$ moves with an orbital velocity $v_{\text{sat}} \approx 7.5\text{ km/s}$. Due to this high relative velocity, any VHF signal transmitted at nominal carrier frequency $f_0 = 161.975\text{ MHz}$ undergoes a significant Doppler frequency shift $f_D(t)$ at the satellite receiver ([Chapter 39](ch39-satellite-ais.md)):

$$f_D(t) = - f_0 \frac{\mathbf{v}_{\text{rel}}(t) \cdot \mathbf{u}(t)}{c}$$

where $\mathbf{v}_{\text{rel}}$ is the relative velocity vector and $\mathbf{u}$ is the unit line-of-sight vector from the satellite to the vessel (Guo 2014; Ellis, Van Rheeden & Dowla 2020).

For an emitter within the satellite's footprint, the observed Doppler shift swings dynamically from approximately $+3.8\text{ kHz}$ as the satellite approaches the horizon, passes through $0\text{ Hz}$ at the point of closest approach (**PCA**), and decreases to $-3.8\text{ kHz}$ as the satellite recedes.
- **Doppler Consistency Verification:** When a satellite receives an AIS burst, the demodulator measures the received center frequency $f_{\text{rx}}$. The satellite computing system calculates theoretical Doppler shift $f_{D,\text{calc}}$ that a transmitter located at broadcast coordinates $(\phi, \lambda)$ should produce.
- **Discrepancy Detection:** If the observed frequency offset differs from calculated Doppler by more than the maximum permissible transmitter oscillator drift ($\pm 500\text{ Hz}$ under IEC 61993-2; see [Chapter 28](ch28-rf-encoding-physical-layer.md)):
  $$|f_{\text{rx}} - (f_0 + f_{D,\text{calc}})| > \Delta f_{\text{threshold}}$$
  the burst could not have originated from the claimed coordinates (Guo 2014).

```
   Frequency Offset (kHz)
       +4 |           \
          |            \  <-- Expected Doppler curve for claimed position
       +2 |             \
          |              \
        0 |---------------\----------------------- (Time of Closest Approach)
          |                \
       -2 |                 \     * <-- Received burst frequency:
          |                  \          Claims position at PCA, but
       -4 |                   \         measured offset is -2.4 kHz (SPOOFED)
          +---------------------------------------> Time (seconds)
```

Commercial RF monitoring constellations—such as HawkEye 360 (operating formation-flying clusters solving combined TDOA and Frequency Difference of Arrival / **FDOA**) and Unseenlabs (deploying single-satellite RF characterization)—routinely utilize physical-layer radiolocation to detect "dark ships" and expose vessels broadcasting false AIS identities (HawkEye 360 2020).

### 59.5.3 Spaceborne SAR and optical cross-correlation
The ultimate spatial ground truth is spaceborne remote sensing. Synthetic Aperture Radar (**SAR**) satellites—including Copernicus Sentinel-1, RADARSAT-2, ICEYE, and Capella Space—transmit active microwave pulses (C-band and X-band) that penetrate cloud cover and darkness to image the ocean surface.

Because steel hulls exhibit high radar backscatter against sea clutter, automated vessel detection algorithms (**CFAR**—Constant False Alarm Rate) identify ship targets and compute precise physical coordinates, length, and heading.

```
       AIS Feed                           Sentinel-1 SAR Radar
  (Broadcast Coordinates)                  (Physical Ground Truth)
          |                                          |
          v                                          v
   [Reported Tanker]                          [Empty Ocean]  ==> GHOST TARGET
   Lat: 34.12, Lon: 128.45                     No return          (Spoofed AIS)
          
   [No AIS Broadcast]                         [Bright Radar Return] ==> DARK TARGET
   Transponder Off                             Length: 280m, Beam: 45m   (Unreported Ship)
```

Cross-matching SAR detections against decoded AIS tracks produces two unambiguous anomaly classes:
1. **Ghost Target (AIS without SAR):** An AIS track claims a 300-meter VLCC crude tanker is at a specific coordinate during a satellite overpass, but the SAR image reveals an empty ocean surface with no radar return. The target is an electronic ghost.
2. **Dark Target (SAR without AIS):** The SAR image reveals a 250-meter vessel underway, but the AIS registry contains zero broadcasts within a 30 nmi radius. The vessel has disabled its transponder or is spoofing an alibi position elsewhere.

High-resolution optical satellites (Planet Labs, Maxar WorldView, Sentinel-2) provide secondary daytime confirmation, directly imaging ship deck markings, superstructure configurations, and wake vectors to verify whether a broadcasted vessel name matches the physical hull.

> **Case file.**
> In mid-2020, commercial maritime intelligence analysts investigated the Iranian-flagged Aframax crude tanker *Romina* (IMO 9324564; HawkEye 360 2020). After transiting through the Suez Canal, the tanker disabled its AIS transponder, disappearing from international tracking screens. While public databases showed no AIS broadcasts, HawkEye 360's formation-flying satellite cluster geolocated active VHF Channel 16 marine radio communications originating from waters just off the Baniyas crude refinery in Syria. Subsequent high-resolution electro-optical satellite imagery captured the *Romina* moored at the Baniyas offshore terminal, discharging approximately one million barrels of Iranian crude in direct violation of international sanctions.

## 59.6 Automated spoofing detection in data pipelines

To protect maritime analytics systems, automated ingestion pipelines must process streaming AIS messages through structural and kinematic filters before persisting data into production repositories ([Chapter 47](ch47-data-quality-track-reconstruction.md); [Chapter 50](ch50-big-data-architecture.md)).

```
Raw AIS Stream ---> [Structural Sanity] ---> [Kinematic Filter] ---> [Coverage Checker] ---> Persisted Track
(!AIVDM / JSON)     - Valid MMSI             - Speed < 45 kn         - Distance < Radio Horizon
                    - CRC Check              - Turn < 10 deg/s       - Multi-Station Overlap
                    - Coords != 0, 91, 181   - No teleports          - Flag suspicious scores
```

The scoring algorithm evaluates each incoming vessel position against its track history, computing a composite anomaly score. 

> **Try it.**
> You can execute the repository's native kinematic validation script to evaluate real-time track plausibility across synthetic harbor data. Run the following command from the workspace environment:
> ```bash
> . .venv/bin/activate
> python code/security/kinematic_checks.py data/samples/synthetic_harbor.nmea --rx 42.36 -70.95
> ```
> Expected output:
> ```
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

### 59.6.1 Scoring heuristic for anomaly triage
The Python pipeline implements a weighted multi-factor heuristic:
$$\text{Score} = \mathbb{I}(V_{\text{viol}} > 0) + \mathbb{I}(\omega_{\text{viol}} > 2) + \mathbb{I}(N_{\text{teleport}} > 0) + \mathbb{I}(N_{\text{beyond\_range}} > 0) + \mathbb{I}(\text{Invalid\_MMSI}) + \mathbb{I}(N_{\text{sog\_mismatch}} > 0.2 N)$$

where:
- $V_{\text{viol}}$ flags speeds exceeding vessel type cap ($V_{\text{cap}} = 45.0\text{ kn}$ for Class A, $60.0\text{ kn}$ for Class B);
- $\omega_{\text{viol}}$ flags angular turn rates exceeding $10.0^\circ/\text{s}$;
- $N_{\text{teleport}}$ identifies displacements exceeding 1.0 nmi within 60 seconds;
- $N_{\text{beyond\_range}}$ identifies reports received by a terrestrial station whose antenna horizon is smaller than reported vessel distance;
- $\text{Invalid\_MMSI}$ catches test codes (`123456789`), reserved ranges used improperly, or numbers failing MID format validation ([Chapter 13](ch13-mmsi-deep-dive.md)).

A composite score $\ge 2$ triggers automatic quarantine of the track segment, routing data to secondary verification pipelines before permitting records to update public maritime maps.

## 59.7 Reporting, coordinated disclosure, and evidence preservation

Detecting maritime electronic deception carries significant legal, commercial, and operational consequences. Falsely accusing a commercial vessel of sanctions evasion or piracy can trigger catastrophic economic losses, wrongful vessel arrests, and international diplomatic friction.

```
       Evidence Collection and Triage Lifecycle
                         |
  +----------------------+----------------------+
  |                                             |
[Raw Ingestion Capture]                 [Sensor Corroboration]
- Unmodified raw NMEA 0183              - Independent Station Logging
- Nanosecond GPS hardware timestamps   - Satellite S-AIS Cross-check
- SDR I/Q baseband recordings (pcap)    - Spaceborne SAR/EO Imagery Match
                         |
                         v
              [Chain of Custody Dossier]
              - SHA-256 Hashes of Raw Captures
              - Receiver Site Survey & Calibration
              - TDOA Hyperbolic Solution Bounds
                         |
                         v
- **US Maritime Administration (MARAD) / NATO Shipping Centre:** For regional electronic warfare, GPS interference advisories, and state-sponsored spoofing vectors affecting international shipping lanes.
- **Flag State Maritime Administrations:** For formal investigation of merchant vessels suspected of identity cloning or deliberate transponder manipulation under SOLAS Chapter V.

> **Legal note.**
> While passive monitoring, logging, and algorithmic detection of unencrypted AIS broadcasts are completely lawful in almost all jurisdictions under international telecommunications law, intentional transmission of unauthorized AIS signals, false identity parameters, or counterfeit distress beacons is a serious criminal offense. In the United States, transmitting false distress signals or unauthorized radio emissions violates the Communications Act of 1934 (47 U.S.C. § 325 and 47 U.S.C. § 501) and Coast Guard statutory authority (14 U.S.C. § 521), carrying severe federal criminal penalties, civil fines exceeding $10,000 per violation, and liability for all costs incurred by search-and-rescue agencies. Under international law, Regulation 19 of SOLAS Chapter V obligates all flag states to enforce compliance with maritime safety equipment standards and penalize intentional navigational fraud.

## Then & now

How the maritime community's understanding of and response to AIS spoofing has evolved over three decades:

- **1990s ⟨H⟩:** The Automatic Identification System is conceptualized and standardized in ITU-R M.1371 as an open, unencrypted broadcast protocol. The threat model assumes physical transponder costs and professional mariner culture provide sufficient barriers against signal forgery.
- **2002–2004 ⟨H⟩:** The IMO SOLAS carriage mandate takes effect for commercial international shipping; terrestrial monitoring networks consist primarily of localized coastal VTS stations.
- **2013–2014 ⟨+⟩:** Security researchers (Balduzzi, Pasta & Wilhoit 2014) demonstrate the first low-cost SDR attacks against AIS, synthesizing ghost vessels, fake search-and-rescue beacons, and artificial CPA collision alerts.
- **2015 ⟨+⟩:** European Commission Joint Research Centre (JRC) researchers (Papi et al. 2015) demonstrate the feasibility of multi-receiver TDOA radiolocation using existing coastal base stations, detecting position discrepancies down to hundreds of meters.
- **2017 ⟨+⟩:** Large-scale state-sponsored GPS spoofing in the Black Sea displaces over 20 commercial merchant ships to Gelendzhik Airport (C4ADS 2019), demonstrating that GNSS attacks manifest as mass AIS dislocations.
- **2018–2019 ⟨+⟩:** Commercial RF reconnaissance constellations (HawkEye 360, Unseenlabs) launch dedicated satellite clusters, establishing spaceborne TDOA and RF emitter detection to uncover dark and spoofing vessels.
- **2019 ⟨+⟩:** Investigative reporting reveals widespread "GPS crop circles" and synthetic circular AIS tracks affecting shipping in Shanghai and the Yangtze River (Harris 2019).
- **2020 ⟨+⟩:** Global Fishing Watch and SkyTruth document the Point Reyes anomaly, where vessels scattered across three continents simultaneously broadcast circular ghost tracks in California (Bergman 2020).
- **2021 ⟨+⟩:** Synthetic AIS injection fabricates false naval incursions by *HMS Defender* and *HNLMS Evertsen* off Sevastopol while both warships remain moored in Odesa.
- **2023–2026 ⟨+⟩:** High-power electronic warfare blanket-jams and spoofs GNSS across the Baltic Sea and Black Sea, accelerating operational adoption of non-GNSS terrestrial radionavigation (R-Mode) and multi-sensor spaceborne verification frameworks (Gattis, Cydejko & Akos 2026).

## On the wire

A deep analysis of spoofed AIS frames requires inspecting raw bit payloads, HDLC framing, and NMEA encapsulation. Consider an attacker broadcasting a forged Class A position report (Message 1) attempting to project a ghost vessel.

```
       Bit Allocation for Message 1 (168 bits total)
 0      5 7                    37 39         41 42          43 44            48
+--------+--+--------------------+--+----------+--+-----------+--+--------------+
| Type   |RI| MMSI               |St| ROT      |SOG| Pos Acc  | Longitude      |
| (6b)   |(2| (30b)              |(4| (8b)     |(10| (1b)     | (28b)          |
+--------+--+--------------------+--+----------+--+-----------+--+--------------+
 49             76 77         88 89      115 116     127 128     133 136    147
+-----------------+-------------+-----------+-----------+-----------+---+-------+
| Latitude        | COG         | True Head | Timestamp | Special   | RA| Comm  |
| (27b)           | (12b)       | (9b)      | (6b)      | Man (2b)  | (3| (19b) |
+-----------------+-------------+-----------+-----------+-----------+---+-------+
```

### Dissecting an authentic vs. forged NMEA sentence
Consider a real-world position report captured off a coastal receiver:
```text
!AIVDM,1,1,,A,13aEO:001;82aqlF1P@5E`100<0p,0*1E
```

Dissecting the payload bit-by-bit identifies forensic anomalies introduced by amateur spoofing software:
1. **Encapsulated 6-bit Armoring:**
   The ASCII string `13aEO:001;82aqlF1P@5E`100<0p` decodes into 168 bits.
   - `1`: Binary `000001` (Message Type 1: Position Report Class A).
   - `3`: Binary `000011` (Repeat Indicator: 0).
   - `aEO:`: Next 30 bits define the MMSI: `001010 010101 010111 011010` $\rightarrow$ Decimal `244670000` (Netherlands MID `244`).
2. **Navigational Status:**
   - 4-bit integer representing engine status. Spoofers frequently leave this as `0` (Under way using engine) even when projecting stationary coordinates, or set it to `15` (Undefined / default).
3. **Position Encoding:**
   - Longitude: 28-bit two's complement integer in units of $1/10000\text{ min}$.
   - Latitude: 27-bit two's complement integer in units of $1/10000\text{ min}$.
   - Common spoofer flaw: rounding coordinates to coarse decimal degrees, resulting in trailing zeroes in low-order bits (`...0000`), which rarely occurs on authentic high-precision GNSS inputs.
4. **Time Stamp Field (Bits 137–142):**
   - 6-bit unsigned integer representing UTC second of the current minute (0–59). Value `60` indicates time stamp unavailable; `61` indicates manual input mode; `62` indicates dead reckoning; `63` indicates positioning system inoperative.
   - Forensic indicator: Scripted injectors broadcasting recorded or synthetic tracks frequently fail to synchronize the 6-bit second field with the transmission epoch of the TDMA slot, creating a detectable timestamp-to-slot mismatch.
5. **Communication State (Bits 149–167):**
   - 19-bit field containing SOTDMA or ITDMA link management data ([Chapter 21](ch21-link-layer-tdma.md)).
   - In SOTDMA: Sync State (2 bits), Slot Timeout (3 bits), and Sub-message (14 bits).
   - **Forensic Indicator:** Simple SDR transmit scripts frequently hardcode the communication state to all zeroes or static values. An authentic Class A transponder constantly decrements its slot timeout on every successive frame ($3 \rightarrow 2 \rightarrow 1 \rightarrow 0$) and announces its next reserved slot. A transmitter that broadcasts static communication state bytes across consecutive bursts is unequivocally an artificial injector.

## Validation, uncertainty & data quality

Errors and anomalies in AIS spoofing analysis arise from three distinct phenomena: intentional deception, legitimate environmental degradation, and hardware configuration defects. Rigorous operational intelligence requires quantifying uncertainty to prevent false-positive classifications.

```
       Error Propagation and Anomaly Attribution
                         |
  +----------------------+----------------------+
  |                                             |
[True Electronic Attack]                [Benign Systematic Faults]
- Coordinated False Trajectories        - Tropospheric Ducting (100–300 nmi)
- Intentional Identity Cloning          - GNSS Multipath & Antenna Shading
- Unsynchronized Communication States   - Transponder Firmware Coordinate Truncation
                         |                      |
                         +----------+-----------+
                                    |
                                    v
                     [Quantified Uncertainty Assessment]
                     - Confidence Index (0.0 to 1.0)
                     - Environmental Ducting Index (k-factor)
                     - Multi-Station Reception Plausibility
```

### Concrete validation procedures
To evaluate an anomalous vessel track rigorously:
1. **Compute Residual Kinematics:** Calculate point-to-point velocity, acceleration, and angular rate of turn across the entire segment. Flag any segment with $V_{\text{implied}} > 45\text{ kn}$ or acceleration $a > 2.5\text{ m/s}^2$.
2. **Atmospheric Ducting Screening:** Cross-reference receiver station reception logs against numerical weather prediction models (ECMWF or NOAA GFS). High surface pressure, thermal inversions, and steep humidity gradients create tropospheric ducting, enabling authentic VHF signals to propagate 200–400 km beyond the standard radio horizon. Never flag a distant reception as spoofed during documented ducting conditions unless corroborated by kinematic or TDOA failure.
3. **MMSI Structural Verification:** Verify that the broadcast MMSI complies with ITU Radio Regulations Appendix 18 and Recommendation ITU-R M.585: valid Maritime Identification Digits (**MID**, digits 2–4 for ships, e.g., 201–775), valid station class prefixes, and rejection of dummy codes (`000000000`, `123456789`).
4. **Worked Uncertainty Calculation:**
   Suppose three coastal base stations record an AIS burst from a vessel claiming coordinates $(43.500^\circ\text{N}, 16.200^\circ\text{E})$.
   - Station 1: Antenna height $45\text{ m}$, distance to claimed position $18.2\text{ km}$, RSSI $-72\text{ dBm}$.
   - Station 2: Antenna height $30\text{ m}$, distance to claimed position $24.6\text{ km}$, RSSI $-78\text{ dBm}$.
   - Station 3: Antenna height $80\text{ m}$, distance to claimed position $31.0\text{ km}$, RSSI $-82\text{ dBm}$.
   The measured Time Differences of Arrival between Station pairs are:
   $$\Delta t_{12} = 15.20\text{ }\mu\text{s} \pm 0.05\text{ }\mu\text{s}, \quad \Delta t_{13} = -28.40\text{ }\mu\text{s} \pm 0.05\text{ }\mu\text{s}$$
   Multiplying by $c = 0.29979\text{ km/}\mu\text{s}$, the range differences are:
   $$d_{12} = 4.557\text{ km} \pm 0.015\text{ km}, \quad d_{13} = -8.514\text{ km} \pm 0.015\text{ km}$$
   Computing the hyperbolic intersection yields a physical emitter position $\mathbf{x}_{\text{true}}$ at $(43.501^\circ\text{N}, 16.198^\circ\text{E})$.
   The offset from the broadcast position is:
   $$\Delta D = 195\text{ meters}$$
   Because the offset lies well within the combined GNSS dilution of precision and transponder antenna offset envelope ($3\sigma = 250\text{ m}$), the report is confirmed authentic. If the TDOA calculation had yielded an emitter location 45 km away, the report would be definitively classified as spoofed.

## Software

**Open source:**
- **AIS-catcher** (Jasper van Baten): High-performance C++ software-defined radio receiver supporting RTL-SDR, Airspy, HackRF, and SDRplay. Includes built-in signal quality metrics and JSON streaming; caveat: does not natively perform multi-station TDOA cross-correlation.
- **libais** (Kurt Schwehr): Fast, robust C++ library with Python bindings for decoding binary AIS NMEA 0183 sentences. Excellent validation and bounds-checking; caveat: focuses purely on single-message decoding without stateful multi-vessel kinematic tracking.
- **MovingPandas** (Anita Graser): Python spatial data analysis library built on GeoPandas for trajectory manipulation, velocity filtering, and stop detection; caveat: memory intensive on multi-gigabyte production AIS feeds without distributed chunking.

**Free but closed:**
- **GPSPatron GP-Cloud:** Cloud-based GNSS cybersecurity platform processing dual-frequency RINEX and NMEA logs to detect GPS jamming and spoofing anomalies; caveat: requires specialized on-premise hardware sensors to unlock full forensic capabilities.

**Commercial:**
- **Windward Maritime AI:** Enterprise intelligence platform specializing in sanctions screening, dark fleet identification, and AIS digital manipulation detection using behavioral machine learning; caveat: proprietary algorithms operate as a black box without public access to underlying heuristic weights.
- **HawkEye 360 Mission Space:** RF geospatial intelligence analytics platform combining satellite constellation TDOA/FDOA radiolocation with commercial AIS feeds; caveat: high commercial subscription cost and data access restricted to enterprise customers.

## Standards & guides

- **ITU-R M.1371-5 (2014):** *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile frequency band.* Defines TDMA slot structure, physical modulation (GMSK), and unauthenticated packet framing.
- **IEC 61993-2 (2018):** *Maritime navigation and radiocommunication equipment and systems — Automatic Identification Systems (AIS) — Part 2: Class A shipborne equipment.* Establishes minimum operational requirements, reporting intervals, and type-approval test standards.
- **IEC 61162-1 (2016):** *Maritime navigation and radiocommunication equipment and systems — Digital interfaces — Part 1: Single talker and multiple listeners.* Standardizes the NMEA 0183 `!AIVDM` and `!AIVDO` sentence formatting ingested by maritime software.
- **IMO Resolution MSC.74(69) Annex 3 (1998):** *Recommendation on Performance Standards for Universal Automatic Identification System (AIS).* Mandates operational availability and navigational safety objectives.
- **IALA Guideline G1082 (2018):** *An Overview of AIS.* Provides authoritative operational guidance for coastal authorities, VTS operators, and aids to navigation encoding.

## Pitfalls

1. **Confusing GNSS spoofing with transponder spoofing:** Attributing false positions to rogue shipboard transponders when the ship is a passive victim of regional military GNSS jamming or meaconing $\rightarrow$ verify whether multiple nearby vessels experience identical directional dislocations.
2. **Ignoring tropospheric ducting:** Flagging legitimate distant VHF receptions (>150 nmi) as spoofed ground tracks $\rightarrow$ check real-time barometric pressure and temperature inversion gradients before rejecting distant line-of-sight reports.
3. **Assuming zero speed implies an authentic stationary ship:** Forgers frequently project static coordinates in anchorages while the vessel conducts clandestine operations elsewhere $\rightarrow$ inspect background micro-drift induced by tidal currents and wind; perfectly zero-variance coordinates are an artifact of simulation.
4. **Treating crowdsourced aggregator maps as ground truth:** Basing legal or compliance decisions on web tracker screens without validating raw NMEA sentences $\rightarrow$ aggregators regularly ingest forged unauthenticated TCP data streams directly from internet pranksters.
5. **Over-reliance on kinematic thresholds for fast craft:** Flagging high-speed passenger catamarans, interceptor craft, or pilot boats as spoofers because their speeds exceed 35 kn $\rightarrow$ adjust kinematic speed caps dynamically based on the vessel type code in Message 5.
6. **Failing to check the TDMA communication state:** Relying solely on lat/lon fields while ignoring static or decremented SOTDMA slot timeouts $\rightarrow$ inspect bits 149–167; static repetition of sub-messages exposes synthetic SDR injectors immediately.
7. **Neglecting antenna lever-arm geometry:** Misinterpreting discrepancies between GPS antenna position and hull center during close-quarters maneuvers as position spoofing $\rightarrow$ apply the dimension and reference offsets reported in Message 5/24.
8. **Overlooking MMSI country code validity:** Accepting impossible Maritime Identification Digits (e.g., starting with 0, 1, 8, or 9 for standard commercial hulls) $\rightarrow$ validate MMSI prefixes against ITU-R M.585 tables.
9. **Relying exclusively on single-satellite Doppler:** Assuming a single Doppler curve yields a unique fix $\rightarrow$ Doppler from a single satellite pass generates an ambiguous cone of positions; resolve ambiguity using multiple passes or multi-station TDOA.
10. **Discarding raw RF data before triage:** Discarding baseband I/Q recordings and retaining only parsed ASCII strings $\rightarrow$ without raw I/Q samples, physical-layer RF fingerprinting and precise post-incident TDOA re-evaluation are impossible.

## Key takeaways

- **AIS is inherently unauthenticated:** Recommendation ITU-R M.1371 lacks cryptographic authentication; every field in an AIS transmission can be synthesized by commodity software-defined radios.
- **Distinguish identity from position manipulation:** Deception spans identity tampering (MMSI cloning, ghost vessels), intentional position fabrication (alibis, false AtoNs), and collateral GNSS-induced displacement (airport offsets).
- **Physical laws cannot be forged:** While packet bits can be easily altered, radio frequency propagation delay, reception horizons, and orbital Doppler shifts cannot be faked by the transmitter.
- **Kinematic filtering provides scalable triage:** Automated speed, turn-rate, and acceleration filters catch crude synthetic tracks and script injectors before data enters analytics pipelines.
- **TDOA and Doppler deliver mathematical ground truth:** Multi-receiver time difference of arrival and spaceborne Doppler curve matching resolve true emitter locations to within hundreds of meters.
- **Multi-modal remote sensing pierces deception:** Spaceborne Synthetic Aperture Radar (SAR) and optical imaging provide unequivocal verification of whether a physical hull exists at its broadcast coordinates.
- **Shadow fleets industrialize spoofing:** Commercial sanctions evasion relies on sophisticated "spoofing-as-a-service" hardware emulators to mask illicit petroleum and commodity trades.
- **Preserve raw telemetry for legal enforcement:** Forensic evidence packages must include unmodified NMEA streams, nanosecond timestamps, and cryptographic hash chains to support maritime legal proceedings.

## References

- Androjna, A., Perkovič, M., Pavić, I., Mišković, J. (2021). AIS Data Vulnerability Indicated by a Spoofing Case-Study. *Applied Sciences*, 11(11):5015. doi:10.3390/app11115015
- Balduzzi, M., Pasta, A., Wilhoit, K. (2014). A Security Evaluation of AIS Automated Identification System. In *Proceedings of the 30th Annual Computer Security Applications Conference (ACSAC '14)*, pages 436–445, New York, NY, USA. ACM. doi:10.1145/2664243.2664257
- Bergman, B. (2020). *Bizarre Circles in Satellite AIS Data Reveal Worldwide GPS Spoofing*. Shepherdstown, WV: SkyTruth. URL: https://skytruth.org/ (accessed 2026-10-06)
- Center for Advanced Defense Studies (C4ADS) (2019). *Above Us Only Stars: Exposing GPS Spoofing in Russia and Syria*. Washington, DC: C4ADS.
- d'Afflisio, E., Braca, P., Willett, P. (2021). Malicious Spoofing of AIS Tracks and Stealth Deviations: A Statistical Framework for Anomaly Detection. *IEEE Transactions on Aerospace and Electronic Systems*, 57(4):2093–2108. doi:10.1109/TAES.2021.3083466
- Ellis, M. S., Van Rheeden, D. R., Dowla, F. U. (2020). Use of Doppler and Doppler Rate for RF Geolocation Using a Single LEO Satellite. *IEEE Access*, 8:2965931. doi:10.1109/ACCESS.2020.2965931
- Gattis, J., Cydejko, J., Akos, D. (2026). Real-Time TDOA Localization of Baltic Sea GNSS Interference Emitters. *GPS Solutions*, 30(2):45. doi:10.1007/s10291-026-02061-5
- Goudossis, A., Katsikas, S. K. (2019). Towards a Secure Maritime Architecture: A Survey of Security Vulnerabilities in Maritime Communications. *International Journal of Information Security*, 18(6):767–787. doi:10.1007/s10207-019-00438-6
- Guo, S. (2014). Space-Based Detection of Spoofing AIS Signals Using Doppler Frequency. In *Proceedings of SPIE 9250, International Conference on Radar and Signal Processing*, page 92500W. SPIE. doi:10.1117/12.2050448
- Harris, M. (2019). Ghost Ships, Crop Circles, and Soft Gold: A GPS Mystery in Shanghai. *MIT Technology Review*, 122(6):62–71.
- HawkEye 360 (2020). *Tracking the Romina: Detecting Dark Vessels Through RF Geolocation*. Herndon, VA: HawkEye 360.
- International Electrotechnical Commission (IEC) (2018). *Maritime Navigation and Radiocommunication Equipment and Systems — Automatic Identification Systems (AIS) — Part 2: Class A Shipborne Equipment*. Standard IEC 61993-2:2018. Geneva: IEC.
- International Telecommunication Union (ITU) (2014). *Technical Characteristics for an Automatic Identification System Using Time Division Multiple Access in the VHF Maritime Mobile Frequency Band*. Recommendation ITU-R M.1371-5. Geneva: ITU.
- Kessler, G. C., Craiger, J. P., Haass, J. C. (2018). A Taxonomy Framework for Maritime Cybersecurity: A Demonstration Using the Automatic Identification System. *TransNav, the International Journal on Marine Navigation and Safety of Sea Transportation*, 12(3):429–437. doi:10.12716/1001.12.03.01
- Kruger, M. (2019). Detection of AIS Spoofing in Fishery Scenarios. In *Proceedings of the 22th International Conference on Information Fusion (FUSION 2019)*, pages 1–8. IEEE. doi:10.23919/FUSION43075.2019.9011328
- Papi, F., Tarchi, D., Vespe, M., Oliveri, F., Borghese, A., Aulicino, G., Vollero, A. (2015). Radiolocation and Tracking of AIS Signals for Maritime Surveillance. *IET Radar, Sonar & Navigation*, 9(5):568–580. doi:10.1049/iet-rsn.2014.0292
- Windward (2021). *The Digital Cloak: The New Era of Maritime Sanctions Evasion and AIS Manipulation*. Tel Aviv: Windward Ltd.
