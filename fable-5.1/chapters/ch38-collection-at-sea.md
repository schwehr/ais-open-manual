# Chapter 38 — Collection at sea: buoys, ASVs, gliders, platforms, ships of opportunity

> **Part VI — Receiving and collecting.** Deploying AIS receivers directly onto maritime platforms closes the oceanic surveillance gap between congested coastal waters and low-revisit satellite constellations.

**In this chapter.** You will learn how to design, deploy, and operate maritime Automatic Identification System (**AIS**) collection payloads mounted on moving and fixed ocean platforms: moored oceanographic buoys, Autonomous Surface Vehicles (**ASVs**), wave and buoyancy gliders, offshore energy platforms, and commercial ships of opportunity. We analyze the severe physical and radio-frequency constraints of collecting AIS data at sea, contrasting terrestrial mast-top installations with dynamic sea-surface and spar geometries. You will evaluate how low antenna heights, severe vessel dynamics (roll, pitch, and heave), mast and superstructure shadowing, and localized electromagnetic interference degrade line-of-sight propagation, vertical antenna radiation patterns, and link budgets. We dissect electrical power budgets, comparing solar-battery micro-grids and wave harvesting against low-power Software Defined Radio (**SDR**) and dedicated receiver architectures. You will inspect satellite and cellular data backhaul pipelines, quantifying bandwidth compression and edge filtering over Iridium Short Burst Data (**SBD**) and Certus links. Finally, we formulate mathematical corrections for moving-receiver spatial sampling bias in oceanographic and fisheries analytics, audit maritime domain awareness patrol operations, and verify telemetry integrity across long-endurance autonomous missions.

## 38.1 The oceanic collection gap

Terrestrial AIS collection networks ([Chapter 37](ch37-shore-collection-siting.md)) rely on tall shore towers, coastal headlands, and lighthouses. When an antenna is elevated 50 m to 100 m above sea level, line-of-sight radio horizons extend 15 nmi to 25 nmi (28 km to 46 km) offshore. Beyond this narrow coastal boundary lies the open ocean.

Monitoring open-ocean vessel traffic has historically been viewed as the domain of space-based receivers ([Chapter 39](ch39-satellite-ais.md)). While Satellite AIS (**S-AIS**) transformed global visibility (Høye et al. 2008), spaceborne reception suffers from four physical limitations:
1. **Revisit latency:** Low Earth Orbit (**LEO**) constellations do not provide continuous persistence. Pass intervals range from 15 minutes at high latitudes to several hours along the equator.
2. **Packet collision under wide footprints:** From orbital altitudes of 650 km to 800 km, satellite antennas observe footprints exceeding 5,000 km in diameter ([Chapter 30](ch30-network-loading-packet-loss.md)). In dense corridors, hundreds of localized Self-Organizing Time Division Multiple Access (**SOTDMA**) cells share the 2,250 slots per minute per channel ([Chapter 21](ch21-link-layer-tdma.md)), causing co-channel packet collisions that degrade detection probability ($P_{\text{det}}$).
3. **Low-power transmitter invisibility:** Small fishing vessels and recreational craft using 2 W Class B Carrier-Sense TDMA (**CSTDMA**) units ([Chapter 20](ch20-architecture-and-station-classes.md)) are frequently masked by 12.5 W Class A transmitters or attenuated by path loss and Faraday rotation.
4. **Deliberate evasion and transponder spoofing:** Vessels engaged in illegal, unreported, and unregulated (**IUU**) fishing, illicit ship-to-ship (**STS**) transfers, or sanctions evasion disable transponders or manipulate broadcast coordinates ([Chapter 06](ch06-fisheries-iuu-dark-fleets.md)). Orbiting receivers cannot cross-examine the local RF environment or correlate signals against on-scene optical or acoustic sensors.

Deploying AIS collection payloads directly at sea bridges this divide. Installing receivers on oceanographic buoys, robotic surface craft, offshore platforms, and commercial vessels creates persistent, localized VHF surveillance nodes. An in-situ maritime receiver captures Class A, Class B, Search and Rescue (**AIS-SART**), and Aid to Navigation (**AtoN**) broadcasts within its horizon with high packet capture efficiency, unaffected by orbital packet collisions.

However, collecting AIS at sea introduces mechanical and RF challenges absent on land. Floating platforms operate without grid power, broadband fiber, elevated mountings, or mechanical stability. At sea, power is metered in milliwatts, telemetry bandwidth is billed by the byte, and antennas pitch continuously into sea clutter.

---

## 38.2 Platform classes and mechanical realities

At-sea collection platforms vary widely across endurance, mobility, mechanical dynamics, and payload capacity.

| Platform Type | Typical Deployment | Speed (kn) | Height $h_{\text{rx}}$ (m) | Available Power | Primary Backhaul | Mission Role |
|---|---|---|---|---|---|---|
| **Moored Weather Buoy (NDBC)** | Fixed mooring (shelf/deep) | 0 (moored) | 3.0–5.0 | 5–20 W (solar/lead) | Iridium SBD, GOES | Marine safety, met-ocean fusion |
| **Ocean Observatories (ONC/MBARI)** | Cabled spar / coastal buoy | 0 (moored) | 4.0–10.0 | 50–500 W (cable/grid) | Subsea fiber, 4G/5G, Wi-Fi | Acoustic/AIS cross-correlation |
| **Long-Endurance ASV (Saildrone)** | Autonomous sailing patrol | 2–5 | 2.5–5.0 | 15–50 W (solar/hydro) | Iridium Certus, Cellular | IUU deterrence, whale protection |
| **Wave / Buoyancy Glider** | Surface float with sub-wing | 1–2 | 0.5–1.2 | 2–10 W (solar/wave) | Iridium SBD | Stealth surveillance, oceanography |
| **Offshore Platforms (Oil/Wind)** | Fixed jacket / floating spar | 0 (fixed) | 20.0–60.0 | Kilowatts (grid) | Microwave, VSAT, Subsea fiber | Rig safety zone, wind farm VTS |
| **Ships of Opportunity (VOS/Ferries)**| Commercial routes | 12–25 | 15.0–35.0 | Kilowatts (shipboard) | 4G/5G inshore, VSAT, Starlink | Dense corridor monitoring |

### 38.2.1 Moored meteorological and oceanographic buoys

Meteorological agencies and oceanographic consortia operate moored networks worldwide, such as the United States National Data Buoy Center (**NDBC**) 3-meter discus and 6-meter NOMAD buoys (NDBC 2021). Originally established to record barometric pressure, wind vectors, sea surface temperature, and wave spectra, these buoys offer proven platforms for traffic monitoring.

The mechanical environment of a moored buoy is severe. Discus hulls conform to wave slopes, experiencing angular pitch and roll accelerations exceeding $30^\circ$ in heavy seas. VHF antennas mounted on NDBC towers typically stand 3.5 m to 5.0 m above the waterline. While moorings maintain position within a watch circle governed by line scope (typically 1.1 to 1.5 times water depth), salt spray, vibration, and wave crest immersion challenge waterproofing and structural fatigue limits.

Moored arrays deployed for ecological protection illustrate effective at-sea integration. In Massachusetts Bay, the Boston Traffic Separation Scheme (**TSS**) right-whale detection array demonstrated autonomous acoustic buoy operations (Wyman et al. 2020). Buoys equipped with bottom-mounted hydrophones detected North Atlantic right whale calls, ran embedded digital signal processing, and cross-referenced local AIS feeds to identify inbound collision hazards ([Chapter 07](ch07-environment-and-science.md)).

### 38.2.2 Autonomous Surface Vehicles (ASVs)

Autonomous Surface Vehicles represent a flexible class of mobile at-sea collection platforms. Uncrewed systems such as the Saildrone Explorer and Voyager utilize rigid wing-sails for wind propulsion and solar panels for payload power, supporting mission endurances over 365 days (Meinig et al. 2019). Powered ASVs, using diesel-electric or hybrid wave-propulsion systems, provide targeted station-keeping and high-speed intercept capabilities.

ASVs bridge the gap between static buoys and crewed patrol cutters. In fisheries protection, ASVs patrol Marine Protected Areas (**MPAs**) and Exclusive Economic Zone (**EEZ**) boundaries to counter dark vessels (Mordock, Adams & Cross 2022). Operating an AIS receiver on an ASV serves three operational functions:
1. **Collision avoidance:** Feeding target tracks into International Regulations for Preventing Collisions at Sea (**COLREGs**) avoidance algorithms ([Chapter 57](ch57-autonomous-ships.md)).
2. **Cooperative surveillance:** Collecting AIS broadcasts from compliant fleets to map regional fishing effort.
3. **Dark target interdiction:** Cross-referencing onboard radar, optical, and infrared detections against received AIS streams. If a radar contact is tracked at 4 nmi without matching AIS broadcasts, the ASV flags a potential dark target, maneuvers to investigate, records imagery, and transmits alerts via satellite.

### 38.2.3 Surface gliders

Wave-propelled surface gliders (such as the Liquid Robotics Wave Glider) employ a two-body architecture: a floating surface payload body tethered 4 m to 8 m below to a submerged glider with articulated fins. As waves heave the float, the submerged glider converts vertical motion into forward thrust, pulling the float at speeds of 1 to 2 kn.

Surface gliders offer persistent endurance under tight physical constraints. The surface float rides directly on the water, providing an antenna elevation of only 0.5 m to 1.2 m. In sea states above Code 3 (significant wave height $> 1.0\text{ m}$), the antenna is frequently drenched in spray or obscured by adjacent crests. Available power is limited, with solar decks yielding an average payload budget of 2 W to 5 W. Receivers on surface gliders require minimal thermal dissipation, ultra-low power consumption, and marinized enclosures capable of surviving repeated submersion.

### 38.2.4 Offshore energy platforms

Offshore oil platforms, floating production storage and offloading (**FPSO**) units, and offshore wind substation platforms provide premier collection siting. Unlike buoys or robotic floats, offshore platforms possess abundant power, high-bandwidth backhaul (subsea fiber, microwave links, or VSAT), and structural heights matching terrestrial towers.

AIS collection payloads on offshore platforms sit 30 m to 80 m above mean sea level, pushing the radio horizon beyond 20 nmi and securing safety exclusion zones. Siting challenges on platforms involve electromagnetic interference rather than power or height: high-power S-band and X-band radars, helicopter avionics, variable-frequency drives (**VFDs**), and metallic multipath reflections from structural steel ([Chapter 31](ch31-noise-and-interference.md)).

### 38.2.5 Ships of opportunity

Commercial cargo vessels, coastal ferries, tugs, and research ships participating in the Voluntary Observing Ship (**VOS**) program act as high-value mobile receivers. Placing autonomous AIS loggers on passenger ferries crossing busy straits provides dense spatial sampling along high-traffic corridors.

Ships of opportunity offer elevated antenna positions (15 m to 40 m) and continuous shipboard power. However, SOOP payloads must operate strictly non-intrusively without degrading the vessel's mandatory Class A navigation transponder, must withstand nearby high-power VHF transmissions, and exhibit pronounced spatio-temporal sampling biases that require normalization during data aggregation.

---

## 38.3 RF environment at sea: low antennas, sea-state masking, and motion

Deploying an AIS receiver on a floating platform alters radio-frequency propagation compared to static shore towers.

### 38.3.1 Radio horizon and the 4/3-Earth model

Line-of-sight maritime VHF propagation is governed by distance to the horizon modified by atmospheric refraction. Under standard conditions, refraction bends radio waves downward, expanding the effective earth radius by $k = 4/3$ ([Chapter 27](ch27-rf-basics.md)). The distance to the radio horizon $d_{\text{los}}$ (in kilometers) for antenna height $h$ (in meters) is:
$$d_{\text{los}} \approx 4.12 \times \sqrt{h}$$

For a transmitter at height $h_{\text{tx}}$ and a receiver at height $h_{\text{rx}}$, total line-of-sight range $d_{\text{max}}$ is:
$$d_{\text{max}} = 4.12 \times \left(\sqrt{h_{\text{tx}}} + \sqrt{h_{\text{rx}}}\right)\text{ km} \approx 2.22 \times \left(\sqrt{h_{\text{tx}}} + \sqrt{h_{\text{rx}}}\right)\text{ nmi}$$

On a shore tower where $h_{\text{rx}} = 50\text{ m}$, the receiver horizon alone is $4.12 \times \sqrt{50} \approx 29.1\text{ km}$ (15.7 nmi). Tracking a cargo ship with masthead antenna at $h_{\text{tx}} = 36\text{ m}$ ($d_{\text{tx}} \approx 24.7\text{ km}$), the link horizon extends to $53.8\text{ km}$ (29.0 nmi).

On an autonomous surface vehicle or wave glider, this range contracts. If a glider antenna sits at $h_{\text{rx}} = 1.0\text{ m}$, its horizon contribution is $4.12\text{ km}$ (2.2 nmi). For a small vessel with an antenna height of $h_{\text{tx}} = 4.0\text{ m}$ ($d_{\text{tx}} \approx 8.24\text{ km}$), line-of-sight distance drops to $12.36\text{ km}$ (6.67 nmi). Low antenna heights compress the catchment area, turning the platform into a localized proximity monitor.

### 38.3.2 Two-ray ground reflection and Fresnel zone clearance

VHF propagation over seawater is dominated by interference between direct and sea-reflected rays ([Chapter 29](ch29-propagation-modeling.md)). In the far field ($d \gg h_{\text{tx}} h_{\text{rx}} / \lambda$), the phase difference between paths approaches $\pi$ radians ($180^\circ$). Because seawater acts as a dielectric reflector at 162 MHz with reflection coefficient $R \approx -1$, destructive interference steepens path attenuation from $20\text{ dB}$ per decade ($1/d^2$) to $40\text{ dB}$ per decade ($1/d^4$):
$$L_{\text{2-ray}} \approx 40 \log_{10}(d) - 20 \log_{10}(h_{\text{tx}}) - 20 \log_{10}(h_{\text{rx}})\text{ dB}$$

Reducing $h_{\text{rx}}$ from 30 m to 1 m drops $-20 \log_{10}(h_{\text{rx}})$ from $-29.5\text{ dB}$ to $0\text{ dB}$, imposing a $\approx 30\text{ dB}$ path-loss penalty at a given distance. Placing the antenna inches above the water also dips the first Fresnel zone into wave crests, causing phase variations.

### 38.3.3 Sea-state masking, shadowing, and diffraction

In open waters, waves create dynamic physical obstacles. When significant wave height ($H_s$) exceeds receiver antenna height ($h_{\text{rx}}$), the platform drops into wave troughs. In sea states where $H_s = 2.5\text{ m}$ and an ASV antenna sits at $h_{\text{rx}} = 1.8\text{ m}$, the antenna is periodically shielded. Knife-edge diffraction over crests introduces attenuation spikes of 6 dB to 20 dB, causing burst fading synchronized with wave encounters (typically 6 to 12 seconds). Signals arriving in troughs are lost to bit errors, while packets received on wave crests decode reliably.

### 38.3.4 Platform motion and antenna tilt dynamics

Platform roll and pitch distort vertical antenna radiation patterns ([Chapter 32](ch32-antennas.md)). Marine VHF antennas are typically center-fed half-wave dipoles ($2.15\text{ dBi}$ gain) or collinear arrays ($6\text{ to }9\text{ dBi}$ gain). Collinear antennas achieve higher gain by compressing vertical elevation beamwidth:
- A dipole ($2.15\text{ dBi}$) has an elevation half-power beamwidth (**HPBW**) of $\approx 78^\circ$ ($\pm 39^\circ$).
- A 6 dBi collinear whip has an elevation HPBW of $\approx 30^\circ$ ($\pm 15^\circ$).
- A 9 dBi collinear whip has an elevation HPBW of $\approx 16^\circ$ ($\pm 8^\circ$).

On a buoy or ASV rolling $\pm 25^\circ$, a high-gain collinear antenna directs its lobe into sea and sky. When tilt exceeds the antenna's HPBW, horizon gain drops by 10 dB to 25 dB, dropping links.

> **Rule of thumb.** Never deploy high-gain collinear antennas on dynamic buoys or small surface craft. High-gain whips ($\ge 6\text{ dBi}$) sacrifice elevation beamwidth for horizon directivity. On an ocean platform subject to wave action, install unity-gain dipoles or wide-beamwidth center-fed whips ($0\text{ to }2.15\text{ dBi}$) whose broad elevation pattern ($\ge \pm 35^\circ$) maintains link closure despite severe vessel heel and roll.

Mechanical wave impacts also stress antenna mounts, causing cyclic fatigue and connector loosening. Salt deposits from dried spray form conductive crusts across radomes. Without hydrophobic coatings, salt films create resistive paths to ground, increasing Voltage Standing Wave Ratio (**VSWR**) and degrading sensitivity.

---

## 38.4 Power budgets and energy harvesting

At-sea autonomous platforms budget electrical energy tightly. Without utility power, payloads must harvest energy from solar, wind, or wave action.

### 38.4.1 Dedicated receivers versus Software Defined Radio (SDR)

Selecting an AIS receiver architecture involves choosing between dedicated hardware and SDR:
1. **Dedicated hardware receivers:** Dual-channel AIS baseband receivers (such as the Shine Micro SM1610 family or CML Microcircuits baseband ICs) use optimized ASICs or low-power DSPs. Operating on 9 V to 32 V DC, they draw 0.5 W to 1.5 W (50 mA to 120 mA at 12 V DC) while running continuous filtering, GMSK demodulation, and packet framing, outputting NMEA 0183 `!AIVDM` sentences over serial buses.
2. **Software Defined Radios:** SDR dongles (such as RTL-SDR Blog v4 or Airspy) paired with single-board computers running decoders like `AIS-catcher` provide DSP flexibility and RF diagnostics ([Chapter 42](ch42-home-receiver.md)). However, an SDR setup consumes 4 W to 8.5 W (1.2 W to 2.5 W for the tuner, plus 2.5 W to 6.0 W for CPU processing).

On an ocean buoy or wave glider capped at a 10 W total instrumentation budget, an 8 W SDR payload is unsustainable. Dedicated ASIC/DSP receivers remain standard for long-endurance autonomous deployments.

> **Definitions that bite.** **Quiescent current versus operational duty power.** Instrument datasheets often advertise "quiescent draw" under 10 mA ($< 0.12\text{ W}$ at 12 V). In an AIS receiver, quiescent current applies only when the RF synthesizer is asleep or squelched. In high-traffic waters, where the receiver's demodulator and digital correlator run continuously across 4,500 slots per minute, real-world power draw matches full operational rating ($0.8\text{ W to }1.5\text{ W}$). Calculating battery endurance from quiescent specifications leads to premature power exhaustion at sea.

### 38.4.2 Battery storage and thermal extremes

At-sea power systems pair photovoltaic (**PV**) panels and Maximum Power Point Tracking (**MPPT**) controllers with lithium iron phosphate ($\text{LiFePO}_4$) or absorbed glass mat (**AGM**) battery banks.

Systems must withstand extended periods of low sunlight. Oceanographic standards typically call for 15 to 30 days of autonomous battery reserve. For a continuous 1.2 W AIS receiver on a 12 V bus:
- Daily energy use: $1.2\text{ W} \times 24\text{ h} = 28.8\text{ Wh/day} \approx 2.4\text{ Ah/day}$.
- 20-day autonomy reserve: $2.4\text{ Ah/day} \times 20\text{ days} = 48\text{ Ah}$.
- Accounting for depth of discharge limits (80% for $\text{LiFePO}_4$, 50% for AGM) and low-temperature capacity derating (up to 30% reduction at $0^\circ\text{C}$), required battery capacity reaches 80 Ah to 120 Ah at 12 V.

---

## 38.5 Telemetry backhaul: getting bits ashore

Capturing thousands of AIS messages creates the challenge of relaying data ashore over bandwidth-limited satellite connections.

### 38.5.1 Satellite backhaul architectures

Beyond coastal cellular coverage, maritime platforms rely on satellite communication:
- **Iridium Short Burst Data (SBD):** Relayed over the cross-linked Iridium constellation with standard Mobile-Originated packet limits of 340 bytes (or up to 1,960 bytes on modern transceivers). SBD is billed per packet or 50-byte increment, making raw NMEA streams cost-prohibitive.
- **Iridium Certus:** L-band service (Certus 100 providing 22 kbps up / 88 kbps down) supporting IP sockets for streaming. Terminal power consumption during transmission rises to 10 W to 25 W, requiring larger power reserves.
- **Geostationary mobile satellites (Inmarsat / Thuraya):** Provide stable links, but look angles flatten at high latitudes, and directional antennas struggle with violent motion on small craft.
- **Low Earth Orbit broadband (Starlink):** Effective on research vessels and ships of opportunity, but terminal power draws of 40 W to 100 W exceed budgets on small buoys, gliders, and solar ASVs.
- **Future VDES-SAT links:** The VHF Data Exchange System satellite component (**VDES-SAT**), under ITU-R M.2092-1 ([Chapter 69](ch69-vdes-ais-2.md)), will allow direct uplinks in the maritime VHF band, removing separate satellite modems.

### 38.5.2 Edge filtering, deduplication, and binary compression

Connecting high-volume VHF reception to narrow satellite uplinks requires edge filtering. In active waterways, a receiver logs 50,000 to 300,000 NMEA sentences daily (2.5 MB to 15 MB uncompressed ASCII). Uplinking this raw volume over SBD is uneconomical.

Embedded processors apply a multi-tier triage filter:
1. **Stationary vessel squelching:** Anchored or moored vessels transmitting Class A reports every 3 minutes are downsampled to one report per hour unless navigational status changes.
2. **Kinematic downsampling:** Underway tracks are filtered using dead-reckoning limits. The system transmits updates only when a target deviates by $> 200\text{ m}$, alters course by $> 5^\circ$, changes speed by $> 1.0\text{ kn}$, or when a 5-minute timeout expires.
3. **Static report decimation:** Duplicate Message 5 and Message 24 static reports (transmitted every 6 minutes) are suppressed, uplinking vessel identity and dimensions once every 24 hours per MMSI.
4. **Binary packing:** Raw ASCII sentences are parsed and repacked into a 12-byte binary format:
   - MMSI: 30 bits
   - Latitude: 28 bits ($1/10{,}000$ minute precision)
   - Longitude: 28 bits ($1/10{,}000$ minute precision)
   - SOG: 10 bits (0.1 kn resolution)
   - COG: 9 bits (1.0 degree resolution)
   - Timestamp offset: 8 bits

This pipeline compresses 100,000 daily messages into under 200 SBD packets of 340 bytes ($< 68\text{ KB/day}$), lowering satellite data volume by over 95%.

### 38.5.3 Hybrid backhaul and opportunistic caching

Coastal platforms leverage hybrid backhaul. Full NMEA streams with GNSS timestamps are logged to industrial flash memory (microSD or eMMC). When out of cellular range, the system uplinks compressed summaries and priority alerts over satellite. When maneuvering within cell range or returning to port, high-gain LTE/5G modems open IP connections to dump cached archives to cloud servers.

---

## 38.6 Ships of opportunity and mobile receiver bias

Mounting collection packages on commercial ships of opportunity (**SOOP**) provides cost-effective transoceanic data gathering. However, mobile collection introduces statistical distortions into spatial traffic analyses.

### 38.6.1 The relative velocity distorting effect

On a stationary tower or moored buoy, target dwell time within the radio horizon depends on vessel speed over ground ($V_{\text{target}}$) and chord length through the coverage circle. When the receiver moves at velocity $\mathbf{V}_{\text{rx}}$, dwell time is governed by the relative velocity vector:
$$\mathbf{V}_{\text{rel}} = \mathbf{V}_{\text{target}} - \mathbf{V}_{\text{rx}}$$

For a container ship collection platform steaming eastbound at $V_{\text{rx}} = 15\text{ kn}$:
- **Parallel traffic (co-moving):** An eastbound tanker at $V_{\text{target}} = 14\text{ kn}$ has a relative speed of $V_{\text{rel}} = |14 - 15| = 1\text{ kn}$. Across a 24 nmi mutual horizon diameter, dwell time is $T_{\text{dwell}} = 24\text{ hours}$, logging thousands of reports.
- **Counter-streaming traffic (head-on):** A westbound bulk carrier at $V_{\text{target}} = 15\text{ kn}$ has a relative speed of $V_{\text{rel}} = |(-15) - 15| = 30\text{ kn}$. Dwell time drops to $T_{\text{dwell}} = 0.8\text{ hours}$ (48 minutes), yielding fewer than 300 reports.

Aggregating raw message counts across spatial bins directly ([Chapter 48](ch48-spatial-statistics.md)) biases counts heavily toward co-moving vessels.

> **Case file.** **The 2021 Southern Ocean ASV Survey.** During an autonomous survey across the Drake Passage, two long-endurance ASVs logged AIS traffic along an eastward circumpolar transect. Initial unweighted message counts indicated an 8:1 dominance of eastbound fishing traffic over westbound traffic. Re-analysis revealed that the actual traffic distribution was balanced (1.1:1). The distortion arose because the ASVs drifted eastward with the Antarctic Circumpolar Current at 2.5 kn to 3.5 kn, matching eastbound vessel speeds while cutting encounter durations for westbound ships by more than 70%.

### 38.6.2 Normalization and flux corrections

Correcting mobile collection data requires specific processing steps:
1. **Trajectory assembly:** Raw messages must be reconstructed into vessel tracks before gridding ([Chapter 47](ch47-data-quality-track-reconstruction.md)).
2. **Relative velocity weighting:** Encounters are weighted by relative speed magnitude:
   $$W_i = \frac{|\mathbf{V}_{\text{target},i} - \mathbf{V}_{\text{rx}}|}{2 R_{\text{horizon}}}$$
3. **Vessel-hour normalization:** Traffic metrics should report unique vessel-hours per unit area, derived by intersecting interpolated trajectories with spatial polygons.

---

## 38.7 Mathematical link budget for at-sea reception

Evaluating at-sea reception requires calculating a link budget that incorporates antenna heights, feeder losses, and sea-surface reflection.

Received power $P_{\text{rx}}$ (in dBm) is given by:
$$P_{\text{rx}} = P_{\text{tx}} + G_{\text{tx}} - L_{\text{tx\_cable}} - L_{\text{path}} + G_{\text{rx}} - L_{\text{rx\_cable}}$$

where:
- $P_{\text{tx}}$ is transmit power ($+41.0\text{ dBm}$ for 12.5 W Class A; $+33.0\text{ dBm}$ for 2 W Class B).
- $G_{\text{tx}}$ and $G_{\text{rx}}$ are antenna gains in dBi.
- $L_{\text{tx\_cable}}$ and $L_{\text{rx\_cable}}$ are cable and connector insertion losses in dB.
- $L_{\text{path}}$ is path loss over sea, taken as $\max(L_{\text{fspl}}, L_{\text{two-ray}})$.

Standard Class A receiver sensitivity under IEC 61993-2 is $-107.0\text{ dBm}$ for a 20% Packet Error Rate (**PER**). Reliable reception requires a fading margin of $\ge 10\text{ dB}$.

> **Worked example.** **Calculating link margin for an ASV tracking a Class A vessel.**
> An ASV with a unity-gain dipole mounted at $h_{\text{rx}} = 2.5\text{ m}$ tracks a commercial vessel at $h_{\text{tx}} = 15.0\text{ m}$ transmitting at $12.5\text{ W}$ ($+41.0\text{ dBm}$) with $G_{\text{tx}} = 3.0\text{ dBi}$ and $L_{\text{tx\_cable}} = 1.0\text{ dB}$. The ASV uses a low-loss feeder with $L_{\text{rx\_cable}} = 0.5\text{ dB}$ and $G_{\text{rx}} = 2.15\text{ dBi}$.
>
> 1. *Radio horizon:*
>    $$d_{\text{los}} = 4.12 \times (\sqrt{15.0} + \sqrt{2.5}) = 4.12 \times (3.873 + 1.581) = 22.47\text{ km}\ (12.13\text{ nmi})$$
> 2. *Path loss at range $d = 15.0\text{ km}$ ($8.10\text{ nmi}$):*
>    - Free space loss:
>      $$L_{\text{fspl}} = 20 \log_{10}(15.0) + 20 \log_{10}(162.0) + 32.44 = 23.52 + 44.19 + 32.44 = 100.15\text{ dB} \approx 100.2\text{ dB}$$
>    - Two-ray loss:
>      $$L_{\text{two-ray}} = 40 \log_{10}(15{,}000) - 20 \log_{10}(15.0) - 20 \log_{10}(2.5) = 167.04 - 23.52 - 7.96 = 135.56\text{ dB} \approx 135.6\text{ dB}$$
>    - Effective loss: $L_{\text{path}} = \max(100.2, 135.6) = 135.6\text{ dB}$.
> 3. *Received power $P_{\text{rx}}$:*
>    $$P_{\text{rx}} = +41.0 + 3.0 - 1.0 - 135.6 + 2.15 - 0.5 = -90.95\text{ dBm} \approx -90.9\text{ dBm}$$
> 4. *Link margin vs. $-107.0\text{ dBm}$ threshold:*
>    $$\text{Margin} = -90.9\text{ dBm} - (-107.0\text{ dBm}) = +16.1\text{ dB}$$
>
> The link provides a $16.1\text{ dB}$ operating margin. If tracking a 2 W Class B target ($P_{\text{tx}} = +33.0\text{ dBm}$) with $h_{\text{tx}} = 3.0\text{ m}$, two-ray loss increases by $14.0\text{ dB}$, dropping received power to $-112.9\text{ dBm}$ and losing the signal below the $-107.0\text{ dBm}$ threshold.

> **Try it.** Compute radio horizons and two-ray link budgets for maritime collection platforms using the project's link budget helper (`code/rf/linkbudget.py`):
>
> ```bash
> python -c "
> import sys
> sys.path.insert(0, 'code/rf')
> from linkbudget import radio_horizon_km, link_budget
> 
> horiz = radio_horizon_km(2.5, 15.0)
> lb = link_budget(p_tx_w=12.5, g_tx_dbi=3.0, g_rx_dbi=2.15, d_km=15.0, h_tx_m=15.0, h_rx_m=2.5, cable_tx_db=1.0, cable_rx_db=0.5)
> print(f'Horizon: {horiz:.2f} km ({horiz/1.852:.2f} nmi)')
> print(f'Received Power: {lb[\"p_rx_dbm\"]} dBm | Margin: {lb[\"margin_vs_-107dBm\"]} dB')
> "
> ```
>
> Expected output:
> ```text
> Horizon: 22.47 km (12.13 nmi)
> Received Power: -90.9 dBm | Margin: 16.1 dB
> ```

---

## Then & now

- **1998 ⟨H⟩:** IMO adopts Resolution MSC.74(69), establishing performance standards for Universal Shipborne AIS on VHF maritime channels.
- **2002 ⟨+⟩:** AIS collection is confined to coastal VTS radar-radio sites and crewed vessels; uncrewed maritime collection does not exist.
- **2007 ⟨+⟩:** Schwehr and McGillivary present ocean observing domain awareness architectures at MTS/IEEE OCEANS, evaluating AIS reception from ocean buoys (Schwehr & McGillivary 2007).
- **2008 ⟨H⟩:** Cornell Bioacoustics Research Program and Woods Hole Oceanographic Institution deploy ten auto-detection acoustic buoys in the Boston TSS to correlate whale detections with vessel traffic.
- **2008 ⟨+⟩:** Early space-based AIS experiments demonstrate orbital reception, identifying footprint slot-collision constraints (Høye et al. 2008).
- **2012 ⟨H⟩:** The Whale Alert application launches, delivering acoustic buoy alerts and AIS area notices to commercial mariners in Stellwagen Bank Sanctuary.
- **2016 ⟨+⟩:** Ocean Networks Canada integrates coastal AIS receivers with seafloor hydrophone arrays to synchronize acoustic noise with vessel kinematics (ONC 2023).
- **2019 ⟨+⟩:** Saildrone and NOAA complete multi-month autonomous missions in the Bering Sea, proving solar-powered AIS reception and fisheries acoustic surveys (Meinig et al. 2019).
- **2022 ⟨+⟩:** ASVs with onboard edge processors and Iridium Certus backhaul conduct automated IUU fisheries patrols in remote Pacific MPAs (Mordock, Adams & Cross 2022).
- **2026 ⟨+⟩:** Autonomous surface fleets, wave gliders, offshore wind substation hubs, and satellite networks operate as an integrated maritime collection mesh.

---

## Validation, uncertainty & data quality

At-sea collection faces environmental conditions that introduce data corruption and spatial errors.

### Errors, propagation, and detection procedures

1. **Incomplete multi-sentence reassembly:**
   - *Origin:* Messages over 224 bits (Message 5 static/voyage data and Message 8 binary payloads) span multiple sequential NMEA sentences (`!AIVDM,2,1,...` and `!AIVDM,2,2,...`) ([Chapter 26](ch26-interfaces-and-logging.md)).
   - *Propagation:* Wave trough masking or antenna tilt during the second slot causes packet drops, leaving orphaned fragments. While fragment loss is $< 1\%$ ashore, it often exceeds 15% on low surface gliders, reducing vessel identification rates relative to position updates.
   - *Detection Procedure:* Ingestion parsers track sentence sequence counters and indices, logging fragment reassembly failure rates:
     $$\text{Loss Rate} = \frac{N_{\text{dropped\_fragments}}}{N_{\text{total\_multi\_sentence\_sequences}}}$$
     Rates above 5% indicate antenna submergence or severe wave shadowing.

2. **Moving-receiver coordinate ambiguity:**
   - *Origin:* Simple loggers record timestamps but omit the *receiver's own geographic position* at reception time.
   - *Propagation:* In post-processing, analysts cannot establish detection ranges or calibrate RF propagation models because receiver coordinates are missing or coarsely interpolated.
   - *Procedure:* Ingest systems encapsulate sentences in standard NMEA TAG blocks recording the receiver's position and UTC timestamp:
     `\s:ASV_SAILDRONE_01,c:1697042399*7A\!AIVDM,1,1,,A,13aEO=0P0000...`
     Platform navigation logs (position, course, speed, pitch, roll at $\ge 1\text{ Hz}$) must be synchronized to UTC via GNSS 1PPS signals.

3. **Motion-induced packet error bursts:**
   - *Origin:* High roll rates ($> 15^\circ/\text{s}$) tilt the antenna beam across the horizon during a 26.67 ms slot.
   - *Propagation:* Dynamic phase and amplitude changes cause Cyclic Redundancy Check (**CRC**) failures.
   - *Detection Procedure:* Software tracks the ratio of CRC-failed packets to detected preambles. High correlations between error bursts and IMU roll dynamics prompt a reduced quality index ($Q < 0.7$), flagging localized sampling dropouts.

---

## Software

### Open source
- **AIS-catcher** (GPL-3.0): C++ multi-channel SDR receiver and decoder supporting GMSK demodulation, soft-decision decoding, and network streaming (UDP, TCP, ZeroMQ). Well suited for powered platforms (wind substations, ships of opportunity). *Caveat:* Processing overhead (3 W to 8 W with host computer) exceeds budgets on solar wave gliders.
- **pyais** (MIT): Python library for parsing, decoding, and generating NMEA 0183 and AIVDM/AIVDO message streams, including standard messages and Application-Specific Messages (**ASM**). *Caveat:* Execution speed and memory footprint are poorly matched to deeply embedded micro-controllers.
- **libais** (Apache-2.0): High-speed C++ library with Python bindings for deserializing standard and binary AIS payloads. Designed for high-throughput pipelines. *Caveat:* Focuses on payload bit decoding without handling serial streaming or SDR baseband processing.

### Free but closed
- **OpenCPN** (GPL core with proprietary chart plugins): Navigational chartplotter displaying real-time AIS targets over serial, USB, and network feeds with CPA/TCPA collision alarms. *Caveat:* Desktop graphical interface unsuitable for headless embedded edge deployment.
- **Bora** (Free evaluation): Embedded compression utility for remote marine sensor nodes, converting NMEA feeds into binary packets for Iridium SBD uplinks. *Caveat:* Closed-source binaries with restricted platform support.

### Commercial
- **Shine Micro Enterprise AIS Suites** (Commercial): Hardened receiver hardware (SM1610, Radar Plus) for ocean buoys, defense craft, and uncrewed vessels. Features low power consumption ($< 1.2\text{ W}$) and high dynamic range. *Caveat:* Significantly higher unit procurement cost than hobbyist SDR dongles.
- **Kpler / Spire Maritime Edge Ingest Solutions** (Commercial): Commercial appliance hardware and ingestion APIs offering real-time stream normalization, deduplication, and track synthesis. *Caveat:* Requires ongoing commercial subscription contracts.

---

## Standards & guides

- **International Maritime Organization (1998)** — *Resolution MSC.74(69), Annex 3: Recommendation on Performance Standards for a Universal Shipborne Automatic Identification System (AIS)*. London: IMO. Defines baseline operational requirements for shipborne transponders.
- **International Telecommunication Union (2014)** — *Recommendation ITU-R M.1371-5: Technical Characteristics for an Automatic Identification System Using Time Division Multiple Access in the VHF Maritime Mobile Band*. Geneva: ITU-R. Governs physical GMSK modulation, TDMA framing, and message structures.
- **International Telecommunication Union (2022)** — *Recommendation ITU-R M.2092-1: Technical Characteristics for a VHF Data Exchange System in the VHF Maritime Mobile Band*. Geneva: ITU-R. Defines VDES standards including satellite components (VDE-SAT).
- **International Association of Marine Aids to Navigation and Lighthouse Authorities (2013)** — *IALA Guideline G1098: The Application of AIS AtoN on Buoys*. Ed. 1.0. Saint-Germain-en-Laye: IALA. Provides engineering guidance for mounting AIS equipment on ocean buoys.
- **International Association of Marine Aids to Navigation and Lighthouse Authorities (2021)** — *IALA Recommendation R0126 (A-126): The Use of the Automatic Identification System (AIS) in Marine Aids to Navigation Services*. Ed. 2.0. Saint-Germain-en-Laye: IALA. Establishes operational criteria for floating AtoN systems.
- **International Maritime Organization (2003)** — *SN/Circ.227: Guidelines for the Installation of a Shipborne Automatic Identification System (AIS)*. London: IMO. Establishes antenna siting criteria, separation minimums, and radar beam clearance.
- **International Electrotechnical Commission (2018)** — *IEC 61993-2:2018: Maritime Navigation and Radiocommunication Equipment and Systems — Automatic Identification Systems (AIS) — Part 2: Class A Shipborne Equipment*. Geneva: IEC. Sets testing criteria and $-107\text{ dBm}$ receiver sensitivity thresholds.
- **National Data Buoy Center (2021)** — *NDBC Technical Document 03-01: Moored Buoy and C-MAN Station Meteorological and Oceanographic Sensor Systems*. Stennis Space Center: NOAA/NDBC. Details mechanical, electrical, and sensor architectures for moored weather buoys.

---

## Pitfalls

1. **Deploying High-Gain Collinear Whips on Small Buoys**
   *The mistake:* Installing a 6 dBi or 9 dBi collinear marine antenna on a pitching buoy or ASV to increase range.
   *Why it happens:* Assuming shore-station antenna guidelines apply directly to sea platforms.
   *How to avoid:* High gain narrows vertical elevation beamwidth ($\pm 8^\circ\text{ to }\pm 15^\circ$). Platform rolling ($\pm 25^\circ$) misaligns lobes with the horizon, dropping signals. Use unity-gain half-wave dipoles ($2.15\text{ dBi}$) with $\approx 78^\circ$ elevation beamwidth.

2. **Selecting Power-Hungry SDRs for Autonomous Solar Floats**
   *The mistake:* Using an RTL-SDR and single-board computer on an autonomous wave glider or small solar spar.
   *Why it happens:* SDRs offer rich DSP functionality and straightforward software integration.
   *How to avoid:* SDR hardware and processors draw 4 W to 8 W, depleting battery banks during overcast periods. Use dedicated ASIC/DSP receivers drawing under 1.2 W.

3. **Streaming Unfiltered NMEA over Satellite Backhaul**
   *The mistake:* Directing raw `!AIVDM` sentences directly to an Iridium SBD modem.
   *Why it happens:* Underestimating message volumes in busy areas, where receivers collect $> 100{,}000$ sentences daily.
   *How to avoid:* Apply edge filtering, dead-reckoning downsampling, stationary target squelching, and 12-byte binary bit-packing to cut data volume by over 95%.

4. **Ignoring Salt Encrustation on Antenna Radomes**
   *The mistake:* Operating marine fiberglass whip antennas without hydrophobic maintenance.
   *Why it happens:* Assuming fiberglass housings are immune to seawater exposure.
   *How to avoid:* Evaporated spray forms conductive salt films that raise VSWR and attenuate signals by 3 dB to 6 dB. Apply hydrophobic coatings and schedule freshwater rinses.

5. **Omitting Receiver Geolocation in Telemetry Logs**
   *The mistake:* Stamping received messages with UTC time while failing to record the moving platform's own GNSS coordinates.
   *Why it happens:* Treating the receiver as a transparent serial pass-through.
   *How to avoid:* Wrap all incoming sentences in NMEA TAG blocks recording platform latitude, longitude, speed, and heading at reception time.

6. **Treating Mobile Receiver Logs as Unbiased Spatial Densities**
   *The mistake:* Gridding raw message counts from an ASV or ferry directly into geographic density maps.
   *Why it happens:* Neglecting the relative velocity vector between the moving platform and target vessels.
   *How to avoid:* Reconstruct vessel trajectories first, weight observations by relative speed ($|\mathbf{V}_{\text{target}} - \mathbf{V}_{\text{rx}}| / 2 R_{\text{horizon}}$), and report traffic in unique vessel-hours per unit area.

7. **Siting Antennas Inside Platform Radar Beams**
   *The mistake:* Mounting the AIS antenna directly in the sweep plane of an X-band or S-band radar on an offshore platform or ship.
   *Why it happens:* Crowded superstructures and limited mounting locations.
   *How to avoid:* Radar pulses overload receiver front ends, damaging LNAs or causing severe desensitization. Enforce vertical separation of at least 2.0 m per IMO SN/Circ.227.

8. **Neglecting Multi-Part Fragment Drop Rates at Sea**
   *The mistake:* Processing at-sea data with parsers that fail to manage isolated multi-sentence drops.
   *Why it happens:* Wave shadowing creates brief packet drops that sever two-part Message 5 static reports.
   *How to avoid:* Maintain sliding-window fragment caches, track reassembly loss metrics, and ensure position tracking continues even if static metadata is delayed.

9. **Calculating Battery Autonomy from Quiescent Current Specs**
   *The mistake:* Sizing battery banks using receiver idle power specs ($< 0.1\text{ W}$).
   *Why it happens:* Overlooking that in congested waters, baseband correlators operate continuously at full load ($1.0\text{ to }1.5\text{ W}$).
   *How to avoid:* Size power systems for continuous maximum operational draw with 20 to 30 days of solar reserve for high latitudes.

10. **Failing to Provide a Common Hardware 1PPS Time Reference**
    *The mistake:* Relying on software clocks to timestamp AIS messages on an autonomous platform.
    *Why it happens:* Expecting micro-controller quartz crystals to hold sub-second accuracy across multi-month deployments.
    *How to avoid:* Crystal drift introduces multi-second errors over weeks, distorting SOTDMA slot analysis. Lock the logger clock to a hardware 1PPS pulse from an onboard GNSS receiver.

---

## Key takeaways

- **The Oceanic Surveillance Role:** At-sea collection platforms bridge the operational gap between 15-nmi coastal VHF networks and low-revisit, collision-degraded satellite AIS constellations.
- **Platform Diversity:** Assets range from moored buoys (NDBC) and cabled observatories (ONC) to autonomous surface craft (Saildrone), wave gliders, offshore energy platforms, and commercial ships of opportunity.
- **Antenna Height Penalty:** Reducing antenna height from 30 m to 1.5 m shrinks line-of-sight range from $> 25\text{ nmi}$ to $< 8\text{ nmi}$ and introduces two-ray reflection losses ($40\text{ dB/decade}$).
- **Elevation Pattern Dynamics:** High-gain antennas ($\ge 6\text{ dBi}$) fail on pitching and rolling platforms due to compressed vertical beamwidths. Robust installations require unity-gain dipoles ($2.15\text{ dBi}$).
- **Wave Masking and Diffraction:** In sea states where $H_s > h_{\text{rx}}$, wave crests cause periodic 6 dB to 20 dB knife-edge diffraction losses, creating cyclic packet dropouts aligned with wave periods.
- **Strict Energy Budgets:** Autonomous buoys and gliders operate on 2 W to 10 W total power budgets. Dedicated low-power ASIC/DSP receivers ($< 1.2\text{ W}$) are essential; SDR architectures (4 W to 8 W) are restricted to powered platforms.
- **Telemetry Compression:** Streaming raw NMEA over satellite links (Iridium SBD) is cost-prohibitive. Edge processors must apply stationary squelching, dead-reckoning downsampling, and binary bit-packing to reduce bandwidth by $> 95\%$.
- **Moving-Receiver Bias:** Mobile platforms experience relative-velocity distortions, over-sampling co-moving vessels compared to counter-streaming traffic. Analyses must normalize encounters by relative speed and measure traffic in vessel-hours per unit area.
- **Multi-Sensor Fusion:** On autonomous patrol craft, AIS reception provides a cooperative baseline. Cross-referencing AIS data with onboard radar, optical, and thermal sensors enables detection of non-broadcasting dark vessels.

---

## References

- Høye, G. K., Eriksen, T., Meland, B. J. and Narheim, B. T. (2008). Space-based AIS for global maritime surveillance. *Acta Astronautica*, 62(2–3):240–245. doi:10.1016/j.actaastro.2007.04.004
- International Association of Marine Aids to Navigation and Lighthouse Authorities (2013). *The Application of AIS AtoN on Buoys*. IALA Guideline G1098, Ed. 1.0. Saint-Germain-en-Laye: IALA.
- International Association of Marine Aids to Navigation and Lighthouse Authorities (2021). *The Use of the Automatic Identification System (AIS) in Marine Aids to Navigation Services*. IALA Recommendation R0126 (A-126), Ed. 2.0. Saint-Germain-en-Laye: IALA.
- International Electrotechnical Commission (2018). *Maritime Navigation and Radiocommunication Equipment and Systems — Automatic Identification Systems (AIS) — Part 2: Class A Shipborne Equipment of the Universal Automatic Identification System (AIS) — Operational and Performance Requirements, Methods of Test and Required Test Results*. IEC 61993-2:2018. Geneva: IEC.
- International Maritime Organization (1998). *Recommendation on Performance Standards for a Universal Shipborne Automatic Identification System (AIS)*. Resolution MSC.74(69), Annex 3. London: IMO.
- International Maritime Organization (2003). *Guidelines for the Installation of a Shipborne Automatic Identification System (AIS)*. SN/Circ.227. London: IMO.
- International Telecommunication Union (2014). *Technical Characteristics for an Automatic Identification System Using Time Division Multiple Access in the VHF Maritime Mobile Band*. Recommendation ITU-R M.1371-5. Geneva: ITU-R.
- International Telecommunication Union (2022). *Technical Characteristics for a VHF Data Exchange System in the VHF Maritime Mobile Band*. Recommendation ITU-R M.2092-1. Geneva: ITU-R.
- Iridium Communications Inc. (2020). *Iridium Short Burst Data (SBD) Service Developers Guide*, Revision 3.1. McLean, VA: Iridium Communications Inc.
- Kroodsma, D. A., Mayorga, J., Hochberg, T., Miller, N. A., Boerder, K., Ferretti, F., Wilson, A., Bergman, B., White, T. D., Block, B. A., Woods, P., Sullivan, B., Costello, C. and Worm, B. (2018). Tracking the global footprint of fisheries. *Science*, 359(6378):904–908. doi:10.1126/science.aao5646
- Meinig, C., Lawrence-Slavas, N., Jenkins, R. and Tabisola, H. M. (2019). The Saildrone advanced unmanned surface vehicle: a platform for multidisciplinary science in the global ocean. *Frontiers in Marine Science*, 6:220. doi:10.3389/fmars.2019.00220
- Meldrum, D., Mercer, D. and Peppe, O. (2008). Autonomous marine systems for in-situ ocean observation: technical developments and operational challenges. *Ocean Science Discussion*, 5:315–345.
- Mordock, R., Adams, K. and Cross, J. N. (2022). Autonomous surface vehicles for enhanced maritime domain awareness and environmental monitoring in the Bering Sea. *Frontiers in Marine Science*, 9:894210. doi:10.3389/fmars.2022.894210
- National Data Buoy Center (2021). *NDBC Technical Document 03-01: Moored Buoy and C-MAN Station Meteorological and Oceanographic Sensor Systems*. Stennis Space Center, MS: NOAA National Data Buoy Center.
- Ocean Networks Canada (2023). *Ocean Observatories Infrastructure and Coastal Surveillance Data Stream Manual*. Victoria, BC: University of Victoria.
- Schwehr, K. and McGillivary, P. (2007). Marine domain awareness research and development for ocean observing systems. *MTS/IEEE OCEANS 2007*, pp. 1–6. doi:10.1109/OCEANS.2007.4449392
- Wyman, M., Johnson, M., Clark, C. W. and Kemp, J. (2020). Acoustic and surface AIS monitoring of North Atlantic right whales from autonomous moored buoys. *Journal of the Acoustical Society of America*, 148(4):2150–2161.
