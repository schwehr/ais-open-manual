# Chapter 35 — Direction finding and independent geolocation

> **Part V — Radio.** Terrestrial direction finding, multi-station time difference of arrival, and spaceborne RF radiolocation determine the physical origin of AIS transmissions without relying on self-reported GNSS coordinates.

**In this chapter.** You will learn how to verify, locate, and track maritime Automatic Identification System (**AIS**) transmitters independently of the positions they broadcast. You will analyze the physical principles of Direction Finding (**DF**) algorithms—including Watson-Watt amplitude-comparison, Doppler/pseudo-Doppler phase-rate, and correlative interferometer methods—operating on single 26.67 ms Gaussian Minimum Shift Keying (**GMSK**) bursts. You will evaluate multi-receiver Time Difference of Arrival (**TDOA**) architectures across coastal base station networks, calculating Geometric Dilution of Precision (**GDOP**) and evaluating Extended Kalman Filter (**EKF**) radiolocation models. You will explore spaceborne RF geolocation, comparing single-satellite Doppler curve inversion with formation-flying multi-satellite TDOA and Frequency Difference of Arrival (**FDOA**) constellations. You will examine computationally lightweight plausibility screening techniques, including receiver radio-horizon range-ring tests, multi-station presence patterns, and radar-to-AIS kinematic track correlation. Finally, you will apply passive radiolocation to catch deliberate spoofers, relocate drifting Aids to Navigation (**AtoN**), and execute Search and Rescue (**SAR**) homing operations.

## 35.1 The necessity of independent geolocation

AIS is a cooperative, unauthenticated broadcast system ([Chapter 1](ch01-what-ais-is.md)). Transponders encode GNSS coordinates into digital payloads ([Chapter 22](ch22-message-catalog.md), [Chapter 25](ch25-gnss-and-ais.md)) without cryptographic authentication or origin proof.

Receiving stations traditionally accept reports on trust. This exposes maritime domain awareness to three vulnerabilities:
1. **Malicious spoofing and phantom vessels.** Low-cost software-defined radios (**SDRs**) allow adversaries to synthesize bit-perfect AIS bursts broadcasting arbitrary Maritime Mobile Service Identities (**MMSIs**) and false coordinates ([Chapter 33](ch33-hardware-and-sdr.md), [Chapter 58](ch58-threat-model.md), [Chapter 59](ch59-spoofing.md)). Vessels evading sanctions or fisheries enforcement broadcast ghost tracks hundreds of miles from their true positions while conducting illicit transfers or entering restricted zones.
2. **GNSS spoofing and interference.** External RF interference corrupts shipboard positioning. Civil GNSS spoofing incidents (in the Black Sea, eastern Mediterranean, and Baltic Sea) force ship receivers to compute false fixes, which transponders faithfully retransmit across the VHF Data Link (**VDL**) ([Chapter 62](ch62-gnss-jamming-spoofing.md)).
3. **Physical displacement and sensor faults.** Aids to Navigation break loose during storms, yet their transponders continue broadcasting charted coordinates if geofencing alarms fail ([Chapter 20](ch20-architecture-and-station-classes.md)). Installation errors also misconfigure antenna offsets or hardcode incorrect coordinates into fixed stations ([Chapter 36](ch36-failure-modes.md)).

Kinematic filters catch gross anomalies like speed jumps ([Chapter 47](ch47-data-quality-track-reconstruction.md)), but fail against sophisticated spoofers simulating realistic tracks along established shipping lanes.

The definitive countermeasure is **independent geolocation**: measuring the electromagnetic properties of the received VHF radio wave—its Angle of Arrival (**AoA**), Time of Arrival (**ToA**), and Frequency of Arrival (**FoA**)—to locate the emitter. While an attacker can forge any payload bit inside an AIS frame, they cannot manipulate propagation delay, wave-front tilt, or orbital Doppler shift.

## 35.2 Terrestrial direction finding on the VHF data link

Radio Direction Finding determines the Angle of Arrival or line of bearing (**LOB**) from an antenna array to an active transmitter, providing the foundation for maritime SAR homing and coastal surveillance.

### 35.2.1 Burst structure and the single-slot challenge

In conventional maritime voice communications, an emitter transmits continuously for several seconds, allowing analog receivers ample integration time. In contrast, AIS transmissions are transient time-division multiple-access (**TDMA**) bursts ([Chapter 21](ch21-link-layer-tdma.md)). Under Recommendation ITU-R M.1371-5 Annex 2, each nominal AIS slot lasts 26.667 ms (256 bits at 9,600 bit/s, bit duration $T_b \approx 104.2\ \mu\text{s}$). Within this slot, transmitter ramp-up consumes 8 bits ($83.3\ \mu\text{s}$), followed by a 24-bit preamble (`010101...`), 16-bit start flag, data payload with HDLC bit stuffing, 16-bit CRC checksum, 16-bit end flag, and an 8-bit buffer. A DF system must extract a valid bearing from a signal existing for less than 27 ms, modulated via Gaussian Minimum Shift Keying with $BT = 0.4$ on transmit and modulation index $h = 0.5$ ([Chapter 28](ch28-rf-encoding-physical-layer.md)).

### 35.2.2 DF operating principles

Modern VHF direction finders (156.000 to 162.050 MHz) rely on three primary architectures:
1. **Watson-Watt amplitude comparison.** Uses an Adcock array of orthogonal dipole pairs surrounding a central sense antenna. Voltages follow cosine and sine patterns with azimuth $\theta$: $V_{\text{NS}}(t) = V_0 \cos(\theta) s(t)$ and $V_{\text{EW}}(t) = V_0 \sin(\theta) s(t)$. The central antenna resolves $180^\circ$ ambiguity, yielding $\theta = \arctan(V_{\text{EW}} / V_{\text{NS}})$. Calculating bearings within 1 to 5 ms, the method is vulnerable to site reflections, producing errors of $\pm 5^\circ$ to $\pm 10^\circ$ in harbors.
2. **Doppler and pseudo-Doppler phase-rate detection.** An antenna moving in a circle of radius $R$ perceives Doppler modulation: $\Delta f(t) = (v_{\text{rot}} / \lambda) \cos(\omega_{\text{rot}} t - \theta)$. Modern VHF systems implement **pseudo-Doppler**, electronically commutating between 4 to 8 vertical antennas arranged in a circle. High-speed commutators execute multiple rotations during a 26.67 ms burst. Dual-direction rotation cancels carrier frequency offsets, achieving $\pm 3^\circ$ to $\pm 5^\circ$ RMS accuracy on single AIS slots.
3. **Correlative interferometer (vector matching).** The correlative interferometer (**CI**) is the benchmark for high-precision digital direction finding (such as Rohde & Schwarz DDF systems). A circular array of 5 to 9 wideband VHF elements samples the wavefield into coherent downconverters. The complex voltage vector $\mathbf{x}(t)$ is correlated against a calibrated reference database $\mathbf{a}(\theta, f)$ representing the pre-measured array manifold:

$$\rho(\theta) = \frac{|\mathbf{a}^H(\theta, f) \mathbf{x}|^2}{\|\mathbf{a}(\theta, f)\|^2 \|\mathbf{x}\|^2}$$

The estimated angle of arrival maximizes $\rho(\theta)$. Correlative interferometry delivers bearing accuracies of $1^\circ$ to $2^\circ$ RMS even under signal-to-noise ratios below 10 dB, rejecting coherent multipath reflections caused by sea clutter or ship superstructures.

| DF Principle | Typical Array | Integration Time | Maritime RMS Accuracy | Multi-slot Required? | Primary Strength / Weakness |
|---|---|---|---|---|---|
| **Watson-Watt** | 4-element Adcock + sense | 1–5 ms | $\pm 5^\circ$ to $\pm 10^\circ$ | No (single slot) | Simple hardware; vulnerable to multipath |
| **Pseudo-Doppler** | 4 to 8 switched monopoles | 5–15 ms | $\pm 3^\circ$ to $\pm 5^\circ$ | No (single slot) | Robust design; phase jumps require filtering |
| **Correlative Interferometer** | 5 to 9 coherent elements | 2–10 ms | $\pm 1^\circ$ to $\pm 2^\circ$ | No (single slot) | Highest precision, suppresses multipath; higher cost |

### 35.2.3 The association problem: pairing bearings with MMSIs

Direction finders operate at the physical layer: they measure Angle of Arrival relative to north with a timestamp and signal level, but do not decode digital payloads. In congested waterways, matching a bearing to a specific MMSI requires:
1. **Time-tagged metadata fusion.** The DF receiver and an adjacent AIS receiver share a common time reference (GNSS 1PPS). The DF logs detected RF bursts with microsecond timestamps ($t_{\text{DF}}$) and bearings $\theta$. Simultaneously, the AIS receiver decodes packets with arrival timestamps ($t_{\text{AIS}}$) and MMSIs ([Chapter 26](ch26-interfaces-and-logging.md)). A fusion processor pairs bearings to messages where $|t_{\text{DF}} - t_{\text{AIS}}| < 1\text{ ms}$.
2. **Integrated DF-demodulator architectures.** High-end coastal surveillance systems feed digitized baseband I/Q streams from the DF array directly into an internal AIS demodulation pipeline, attaching computed bearing angles directly into NMEA or JSON records.

> **Case file.** *The RHOTHETA RT-500-M and Rohde & Schwarz coastal surveillance arrays.*
> The RHOTHETA RT-500-M is an industry-standard dual-band maritime SAR direction finder installed on Coast Guard cutters and lifeboats worldwide. Operating from 118 to 470 MHz, it covers all 88 maritime VHF channels, aeronautical distress frequencies (121.5 and 243.0 MHz), and Cospas-Sarsat beacons (406.025 to 406.040 MHz). Utilizing a four-element pseudo-Doppler antenna array with automated dual-direction rotation, it achieves a nominal bearing accuracy of $\pm 5^\circ$ RMS. While decoding digital Cospas-Sarsat 406 MHz alert frames directly, on maritime VHF channels it outputs raw bearing lines over NMEA 0183 (`$RATGM` or `$HEROT`) without decoding packet data. Bridge integration requires external software to correlate bearings with ECDIS AIS targets.
> 
> At commercial VTS centers, fixed direction finding is performed by systems such as the Rohde & Schwarz DDF series (including DDF205, DDF255, and DDF550). Utilizing wide-aperture 9-element circular arrays and multi-channel correlative interferometry, these systems achieve $1^\circ$ to $2^\circ$ RMS accuracy atop harbor surveillance towers, cross-referencing radio bearings against primary radar plots to identify unregistered vessels or unmask AIS spoofers attempting to project phantom positions inside busy traffic separation schemes.

## 35.3 Coastal TDOA radiolocation using base station networks

While single-station direction finding yields a line of bearing, fixing coordinates in two dimensions requires intersecting bearing lines (triangulation) or Time Difference of Arrival radiolocation (multilateration).

### 35.3.1 Principles of multi-receiver TDOA

Time Difference of Arrival radiolocation determines position by measuring relative arrival times of a single burst across $M \ge 3$ geographically separated base stations. An AIS transmitter at unknown coordinates $\mathbf{x}_{\text{tx}} = [x, y]^T$ transmits at unknown time $t_0$. Arrival time $t_i$ recorded at receiver $\mathbf{s}_i = [x_i, y_i]^T$ is:

$$t_i = t_0 + \frac{\|\mathbf{x}_{\text{tx}} - \mathbf{s}_i\|}{c} + \epsilon_i$$

where $c = 299{,}792{,}458\text{ m/s}$ is the speed of light and $\epsilon_i$ represents measurement noise and clock errors. Selecting receiver 1 as reference, range difference is:

$$\Delta d_{i,1} = c(t_i - t_1) = \|\mathbf{x}_{\text{tx}} - \mathbf{s}_i\| - \|\mathbf{x}_{\text{tx}} - \mathbf{s}_1\|$$

A constant range difference defines a hyperbola with foci at the two antennas. A network of $M \ge 3$ non-collinear stations yields $M - 1$ independent hyperbolic lines of position, fixing the vessel coordinates. Since radio waves travel $\approx 300\text{ m/\mu s}$ ($1\ \mu\text{s} \approx 299.79\text{ m}$), a $1\ \mu\text{s}$ clock bias shifts the line of position by 300 m. Resolving coordinates to 100 m requires 100–300 ns inter-station timing synchronization.

### 35.3.2 The Papi et al. framework: mining existing AIS networks

A major breakthrough in maritime radiolocation was demonstrated by Francesco Papi, Dario Tarchi, Michele Vespe, Franco Oliveri, Francesco Borghese, Giuseppe Aulicino, and Antonio Vollero (2015) with the European Commission'''s Joint Research Centre (**JRC**).

Papi et al. demonstrated that existing coastal AIS base-station networks conforming to IEC 62320-1 ([Chapter 20](ch20-architecture-and-station-classes.md)) can perform precision radiolocation opportunistically—requiring zero hardware modifications to vessels:
1. **GNSS-disciplined base-station clocks.** Fixed base stations discipline TDMA slot clocks using GNSS receivers with 1-Pulse-Per-Second (**1PPS**) outputs, aligning internal sampling registers across the network to within $\pm 20$ to $\pm 50\text{ ns}$ of UTC.
2. **Preamble cross-correlation.** When an AIS burst arrives, the station cross-correlates digitized I/Q samples against the known 24-bit training sequence (`010101...`). The cross-correlation peak establishes Time of Arrival with sub-symbol precision.
3. **Extended Kalman Filter in geodetic coordinates.** Papi et al. formulated an Extended Kalman Filter tracking vessel kinematics on the WGS-84 ellipsoid, filtering out Gaussian timing noise, multipath jitter, and transient geometric dilution of precision.

In trials on vessel traffic, Papi et al. demonstrated that this opportunistic network detects discrepancies between broadcast AIS positions and true physical origins "on the order of hundreds of meters." When an adversary broadcasts false coordinates, TDOA residual vectors explode, immediately flagging the target as spoofed.

### 35.3.3 Geometric Dilution of Precision (GDOP)

Station geometry relative to the target dictates radiolocation accuracy, quantified by Geometric Dilution of Precision (**GDOP**). Let range-difference measurement vector be $\mathbf{z} = \mathbf{h}(\mathbf{x}) + \mathbf{v}$, where $\mathbf{v} \sim \mathcal{N}(\mathbf{0}, \mathbf{R})$. The measurement Jacobian matrix $\mathbf{H}$ evaluated at true position $\mathbf{x} = [x, y]^T$ contains rows corresponding to unit direction vectors:

$$\mathbf{H}_i = \frac{\mathbf{x} - \mathbf{s}_i}{\|\mathbf{x} - \mathbf{s}_i\|} - \frac{\mathbf{x} - \mathbf{s}_1}{\|\mathbf{x} - \mathbf{s}_1\|} = \mathbf{u}_i - \mathbf{u}_1$$

Position estimation error covariance is $\operatorname{Cov}(\Delta \mathbf{x}) = (\mathbf{H}^T \mathbf{R}^{-1} \mathbf{H})^{-1}$. Assuming independent timing errors with variance $\sigma_d^2 = c^2 \sigma_t^2$, horizontal dilution of precision (**HDOP**) is:

$$\text{HDOP} = \frac{\sqrt{\operatorname{Tr}[(\mathbf{H}^T \mathbf{H})^{-1}]}}{\sigma_d}$$

GDOP degrades when stations are collinear (hyperbolae run parallel offshore, blowing up cross-range error) or when baselines are small relative to target distance (unit vectors $\mathbf{u}_i$ become nearly identical, ill-conditioning $\mathbf{H}$).

> **Worked example.** *Two-dimensional TDOA fix with three coastal base stations.*
> Three coastal AIS monitoring stations are positioned in a Cartesian coordinate system: Station 1 at $[0,\ 0]^T\text{ m}$ (Shore A), Station 2 at $[40{,}000,\ 10{,}000]^T\text{ m}$ (Shore B), and Station 3 at $[15{,}000,\ 35{,}000]^T\text{ m}$ (Shore C).
> 
> A vessel transmits an AIS Message 1 burst from true position $\mathbf{x}_{\text{true}} = [25{,}000,\ 18{,}000]^T\text{ m}$, while broadcasting spoofed coordinates $\mathbf{x}_{\text{spoofed}} = [45{,}000,\ 35{,}000]^T\text{ m}$ (displaced by 26.2 km).
> 
> Physical ranges to each station are $d_1 = 30{,}806\text{ m}$, $d_2 = 17{,}000\text{ m}$, and $d_3 = 19{,}723\text{ m}$. Measured range differences relative to Station 1 are $\Delta d_{2,1} = -13{,}806\text{ m}$ ($\Delta t_{2,1} = -46.051\ \mu\text{s}$) and $\Delta d_{3,1} = -11{,}083\text{ m}$ ($\Delta t_{3,1} = -36.968\ \mu\text{s}$).
> 
> If the vessel were at claimed position $\mathbf{x}_{\text{spoofed}}$, ranges would be $d_{1,\text{sp}} = 57{,}009\text{ m}$, $d_{2,\text{sp}} = 25{,}495\text{ m}$, and $d_{3,\text{sp}} = 30{,}000\text{ m}$, yielding expected range difference $\Delta d_{2,1,\text{sp}} = -31{,}514\text{ m}$ ($\Delta t_{2,1,\text{sp}} = -105.118\ \mu\text{s}$). The timing residual $|\Delta t_{2,1} - \Delta t_{2,1,\text{sp}}| = 59.067\ \mu\text{s}$ represents $17{,}708\text{ m}$ of range error. A chi-squared test rejects the broadcast report ($p < 10^{-15}$). Gauss-Newton iteration recovers true position $[25{,}000,\ 18{,}000]^T\text{ m}$ within 4 iterations.

## 35.4 Spaceborne RF geolocation

In the open ocean beyond coastal base station reception, independent geolocation relies on Low Earth Orbit (**LEO**) satellite constellations ([Chapter 39](ch39-satellite-ais.md)). Satellites orbit at altitudes between 450 km and 650 km with velocities around $v_{\text{sat}} \approx 7.6\text{ km/s}$. From orbit, spaceborne systems exploit single-satellite Doppler curve matching and multi-satellite formation-flying TDOA/FDOA.

### 35.4.1 Single-satellite Doppler curve inversion

A single satellite traversing the sky above a vessel observes a continuous Doppler frequency shift on the received carrier. For an AIS transmission at nominal carrier $f_0 \approx 162.0\text{ MHz}$, received frequency $f_{\text{rx}}(t)$ is:

$$f_{\text{rx}}(t) = f_{\text{tx}} \left(1 - \frac{\mathbf{v}_{\text{rel}}(t) \cdot \mathbf{u}_{\text{los}}(t)}{c}\right)$$

For an orbital altitude of 550 km, line-of-sight velocity as the satellite rises or sets across the horizon approaches $7.0\text{ km/s}$, producing Doppler shifts of $\Delta f_{D,\text{max}} \approx \pm 3{,}775\text{ Hz}$.

As documented by Guo (2014) and generalized by Ellis, Van Rheeden, and Dowla (2020), Doppler shift and Doppler rate ($\dot{f}_D = df/dt$) contain spatial information:
- **Zero-Doppler crossing:** The moment when $f_{\text{rx}}(t) = f_{\text{tx}}$ defines closest point of approach (**CPA**). The emitter lies along a surface curve perpendicular to the satellite velocity vector at that instant.
- **Slope at CPA:** The steepness of the Doppler S-curve ($\dot{f}_D$ at $t_{\text{CPA}}$) is inversely proportional to slant range at CPA. Overhead passes produce steep transitions; distant off-track passes produce shallow slopes.

Single-satellite Doppler geolocation faces three key constraints:
1. **Oscillator bias.** ITU-R M.1371 permits $\pm 500	ext{ Hz}$ ($\pm 3.1	ext{ ppm}$) frequency offsets ([Chapter 28](ch28-rf-encoding-physical-layer.md)). An uncalibrated offset shifts zero-Doppler timing, causing along-track errors unless frequency and position are jointly estimated.
2. **Cross-track ambiguity.** A straight satellite pass cannot differentiate emitters equidistant to the left or right of the ground track without multi-pass tracking or landmask constraints.
3. **Burst sparsity.** Orbital packet collisions ([Chapter 30](ch30-network-loading-packet-loss.md)) often limit captures to 1–2 packets per pass, precluding full Doppler S-curve fitting.

### 35.4.2 Multi-satellite formation flying: TDOA and FDOA

To achieve instantaneous, single-burst radiolocation anywhere on the globe, commercial operators deploy satellites in tight orbital formations (clusters). A satellite cluster typically comprises three or four spacecraft flying in controlled geometry separated by baselines of 50 km to 200 km. When an emitter transmits, all spacecraft in the cluster capture the waveform simultaneously, solving two simultaneous measurement domains:
1. **TDOA (Differential Propagation Time):** Differential arrival times $\Delta t_{ij} = t_i - t_j$ generate hyperbolic surfaces intersecting the Earth'''s geoid.
2. **FDOA (Differential Doppler Shift):** Because each spacecraft maintains a slightly different velocity vector relative to the emitter, received carrier frequencies differ by $\Delta f_{ij} = f_i - f_j$. FDOA defines isochrone curves of constant differential relative velocity.

Intersecting TDOA hyperbolae with FDOA Doppler curves generates a closed **geolocation error ellipse** from a single burst.

### 35.4.3 Commercial RF geolocation constellations

Commercial spaceborne RF geolocation provides global emitter tracking:
- **HawkEye 360** (Herndon, VA). Operating clusters of three formation-flying satellites (first launched Dec 2018), HawkEye 360 processes joint TDOA/FDOA across VHF, UHF, and radar bands. Unmatched emissions are categorized as **DarkRF**, achieving sub-kilometer precision across multiple bursts.
- **Unseenlabs** (Rennes, France). Uses proprietary **monosatellite radiolocation** (first launched Aug 2019, 25 satellites as of Oct 2026). Each satellite operates autonomously, geolocating emitters to ~1 km across 300,000 km$^2$ swaths per pass.
- **Kleos Space** (Luxembourg). Deployed 4-satellite clusters (2020–2022). Entered insolvency proceedings in July 2023; commercial data collection ceased, illustrating the high capital costs of space surveillance.

| Provider | Constellation Architecture | First Launch | Operational Satellites (as of Oct 2026) | Primary Geolocation Method | Quoted Maritime Precision | Commercial Status |
|---|---|---|---|---|---|---|
| **HawkEye 360** | Formation-flying clusters (triads) | Dec 2018 (Pathfinder) | >30 satellites in multiple clusters | TDOA + FDOA cross-satellite fusion | Several km (single-burst) to <500 m (multi-burst) | Fully operational |
| **Unseenlabs** | Independent monosatellites (BRO series) | Aug 2019 (BRO-1) | 25 satellites | Single-satellite passive RF analysis | ~1 km | Fully operational |
| **Kleos Space** | Formation clusters (4-satellite blocks) | Nov 2020 (KSM1) | Constellation non-operational | Cluster TDOA / FDOA | ~1 to 5 km | Operations halted; insolvent 2023 |

## 35.5 Computationally lightweight plausibility screening

While high-precision TDOA arrays and satellite clusters provide rigorous fixes, analysts processing historical archives or operating low-cost shore stations can perform effective independent verification using three lightweight plausibility checks.

### 35.5.1 Radio horizon and range-ring consistency

VHF radio waves propagate via line-of-sight space waves bent by atmospheric refraction ([Chapter 27](ch27-rf-basics.md), [Chapter 29](ch29-propagation-modeling.md)). In a standard atmosphere (4/3-Earth model, $R_e pprox 8{,}495	ext{ km}$), maximum line-of-sight distance between receiver height $h_{	ext{rx}}$ and transmitter height $h_{	ext{tx}}$ (meters) is:

$$d_{	ext{max}} pprox 4.12 \left(\sqrt{h_{	ext{rx}}} + \sqrt{h_{	ext{tx}}}
ight)	ext{ km} pprox 2.22 \left(\sqrt{h_{	ext{rx}}} + \sqrt{h_{	ext{tx}}}
ight)	ext{ nmi}$$

A shore station with $h_{	ext{rx}} = 50	ext{ m}$ receiving a vessel at $h_{	ext{tx}} = 25	ext{ m}$ has $d_{	ext{max}} pprox 49.7	ext{ km}$ ($26.8	ext{ nmi}$). If the decoded position claims 150 nmi range, the report is physically anomalous under standard conditions.

*Caveat: Tropospheric ducting.* Strong temperature inversions over water create elevated ducts trapping 162 MHz waves out to 300–500 nmi ([Chapter 29](ch29-propagation-modeling.md)). Ducting must be evaluated via regional refractivity ($M$-curves) before asserting spoofing.

### 35.5.2 Multi-receiver reception patterns (spatial absence)

In coastal networks, screening exploits **spatial presence versus absence**. If a vessel claims a position 3 km from Station A, both Station A and adjacent Station B should receive its bursts. If Stations A and B log zero packets while distant Station C (150 km away) captures every burst, the vessel is physically near Station C. Androjna, Perkovič, Pavic, and Mišković (2021) demonstrated this spatial inconsistency analysis in the 2019 Elba Island spoofing incident, proving that coastal multi-station reception logs can isolate terrestrial spoofers.

### 35.5.3 Primary radar and AIS track correlation

In VTS operations, the primary defense against AIS spoofing is **radar-to-AIS correlation** (governed by IEC 62388). Cooperative AIS tracks are continuously associated with non-cooperative primary radar returns (X-band 9 GHz, S-band 3 GHz) via range and bearing gates: $\Delta r = \|\mathbf{x}_{\text{radar}} - \mathbf{x}_{\text{AIS}}\| < R_{\text{gate}}$ and $\Delta \theta = |\theta_{\text{radar}} - \theta_{\text{AIS}}| < \Theta_{\text{gate}}$.
- **Radar target without AIS ("Dark target"):** Vessel has disabled AIS, lost power, or is beneath carriage mandates.
- **AIS target without radar ("Ghost target"):** AIS report without matching primary radar return in line-of-sight conditions, exposing synthetic spoofing or displaced virtual AtoNs.

## 35.6 Operational applications

Independent geolocation transforms AIS from a brittle display layer into a robust, verifiable surveillance sensor.

### 35.6.1 Countering sanctions evasion and dark fleets

Vessels engaged in illicit trade—such as crude oil smuggling violating international sanctions or illegal, unreported, and unregulated (**IUU**) fishing—routinely switch off AIS transponders or broadcast fraudulent positions ([Chapter 6](ch06-fisheries-iuu-dark-fleets.md), [Chapter 8](ch08-security-and-national-security-uses.md)).

Commercial RF geolocation defeats both tactics. Even when dark vessels disable AIS, bridge crews continue to use standard VHF marine voice radios (Channel 16 at 156.800 MHz), navigation radars, and satellite terminals. Spaceborne RF sensors geolocate these incidental emissions, cueing high-resolution Synthetic Aperture Radar (**SAR**) or optical satellites to image the dark vessel. When a vessel transmits spoofed AIS, spaceborne TDOA/FDOA fixes the true transmitter coordinates, exposing the fraud.

In March 2020, the Iranian-flagged crude tanker *Romina* (IMO 9549554) disabled its AIS transponder near the Suez Canal, disappearing from commercial tracking systems. HawkEye 360 tasked its Pathfinder cluster over the eastern Mediterranean, intercepting and geolocating active VHF Channel 16 bridge-to-bridge communications off Syria near Baniyas. The geolocated RF error ellipse cued high-resolution optical imagery from Planet Labs, visually confirming the *Romina* anchored off Baniyas offloading crude oil. This established an operational precedent for commercial "DarkRF" maritime interdiction: even when AIS is silenced, vessels routinely emit detectable radio energy.

### 35.6.2 Relocating drifting Aids to Navigation

AIS AtoN transponders (Message 21) transmit positions and an off-position status flag ([Chapter 20](ch20-architecture-and-station-classes.md)). When moorings break, buoys can drift while broadcasting nominal positions if internal alarms fail. Buoy tenders use shipboard VHF direction finders (e.g., RHOTHETA RT-500-M) to track physical bearings to Message 21 bursts, recovering displaced buoys even when GNSS fixes are corrupt.

### 35.6.3 Search and Rescue (SAR) homing

Survival craft deploy AIS-SART (`970...`) and AIS-MOB (`972...`) beacons ([Chapter 13](ch13-mmsi-deep-dive.md), [Chapter 68](ch68-special-purpose-ais.md)). If water immersion degrades internal GNSS reception (broadcasting sentinel `63`), rescue cutters and aircraft home in using direction finders locked onto 161.975/162.025 MHz bursts. Combined beacons emit auxiliary 121.5 MHz analog tones, cross-verifying digital fixes with analog bearings.

> **Threat model.** *Adversarial evasion of independent geolocation.*
> - **Attacker & Motivation:** A state actor, sanctions-evading tanker operator, or IUU fishing fleet seeking to broadcast falsified AIS positions while preventing authorities from discovering the vessel'''s true location via RF geolocation.
> - **Attack Mechanics:**
>   - *Terrestrial TDOA evasion:* Operating outside coastal base station line-of-sight (>50 nmi offshore) or navigating where station geometries are nearly collinear (maximizing GDOP).
>   - *Direction finder evasion:* Minimizing transmit duty cycle, dropping RF power to 1 W (Class A low-power mode), or alternating short bursts across channels.
>   - *Satellite RF evasion:* Practicing electromagnetic silence—deactivating AIS, silencing VHF radios, securing marine radar, and powering down satellite terminals during scheduled LEO overpasses (calculated from orbital ephemerides).
> - **Impact:** Degraded geolocation accuracy; commercial RF surveillance systems may require multiple passes or fail to achieve sub-kilometer fixes.
> - **Defensive Mitigations:**
>   - Spaceborne constellations with unpredictable or randomized orbital planes (such as mid-inclination orbits) that defeat ephemeris evasion schedules.
>   - Multi-static radar and passive SAR imaging that detect metallic hull signatures without requiring active radio emissions.
>   - Sensor fusion linking satellite RF geolocation with optical, infrared, and spaceborne SAR data.

> **Legal note.** *Regulatory status of passive radio direction finding and spaceborne RF surveillance.*
> Passive reception and direction finding of radio signals broadcast on public maritime VHF channels is lawful under international law and domestic telecommunications statutes. Under Article 19 of the ITU Radio Regulations and Chapter V, Regulation 19 of the International Convention for the Safety of Life at Sea (**SOLAS**), AIS transmissions are mandatory public safety broadcasts intended for open reception by all mariners and shore authorities.
> 
> Operating passive VHF direction finders or recording base-station arrival times violates no wiretapping or communications privacy laws (such as 18 U.S.C. § 2511 in the United States), because maritime safety frequencies are expressly exempted public radio transmissions.
> 
> However, commercial spaceborne RF surveillance occupies a complex regulatory tier. While capturing open VHF AIS emissions from space is unrestricted, commercial constellations (such as HawkEye 360 and Unseenlabs) intercept emissions across multiple radio bands, including tactical military radars, public safety links, and encrypted uplinks. In the United States, space-based RF sensing is licensed and regulated by the Federal Communications Commission (**FCC**) and the National Oceanic and Atmospheric Administration (**NOAA**) Commercial Remote Sensing Regulatory Affairs (**CRSRA**) office. License conditions impose strict national security restrictions, data tiering, and shutter control mandates during geopolitical crises. For detailed analysis of the privacy implications of emitter surveillance, see [Chapter 19](ch19-privacy-and-ethics.md).

## Then & now

| Period | ⟨H⟩ / ⟨+⟩ | Technology & Operational Doctrine | Accuracy & Performance |
|---|---|---|---|
| **1940s–1970s** | ⟨H⟩ | **Analog VHF Direction Finding.** Mechanically rotated loop antennas and analog Watson-Watt displays used for coastal SAR voice homing on VHF Channel 16 (156.800 MHz). | Bearing accuracy $\pm 5^\circ$ to $\pm 15^\circ$; required continuous 5–10 second voice carrier; blind to digital bursts. |
| **1980s–1990s** | ⟨H⟩ | **Electronic Doppler DF and VTS Radars.** Multi-element circular antenna arrays with diode commutation (pseudo-Doppler). Coastal VTS centers deploy primary radar, plotting voice radio bearings against radar targets. | Bearing accuracy $\pm 3^\circ$ to $\pm 5^\circ$ on analog transmissions; unable to process transient digital TDMA signals. |
| **2000–2004** | ⟨H⟩ | **AIS Rollout and Cooperative Display.** SOLAS Chapter V mandate accelerates AIS carriage. Bridge and VTS operations switch from primary radar tracking to trusting broadcast AIS GPS coordinates. DF relegated to 121.5 MHz SAR homing. | Zero independent geolocation of AIS; positional integrity relied entirely on unauthenticated GPS fixes broadcast in packets. |
| **2014–2015** | ⟨+⟩ | **Opportunistic TDOA & Early Satellite Doppler.** Papi et al. (2014, 2015) demonstrate TDOA radiolocation using existing coastal base-station networks. Guo (2014) publishes spaceborne Doppler spoof-detection models. | Coastal TDOA resolves emitter discrepancies to "hundreds of meters" without hardware modifications; satellite Doppler resolves single-burst consistency. |
| **2018–2020** | ⟨+⟩ | **Commercial Spaceborne RF Geolocation.** HawkEye 360 launches Pathfinder cluster (Dec 2018); Unseenlabs launches BRO-1 (Aug 2019). Commercial mapping of "DarkRF" begins (e.g., tracking the *Romina* in 2020). | Formation-flying satellite clusters achieve sub-kilometer to 5 km geolocation from space on arbitrary VHF emissions. |
| **2021–2026** | ⟨+⟩ | **Multi-Constellation Emitter Surveillance.** Constellations expand (Unseenlabs reaches 25 operational satellites; HawkEye 360 expands global revisit to <1 hour). Automated multi-sensor fusion combines TDOA, SAR, optical, and primary radar. | Real-time global independent verification; automated alerts flag spoofed tracks, sanctions evasion, and GNSS-interference sources. |

## Validation, uncertainty & data quality

Independent geolocation derives vessel coordinates through non-linear estimation subject to physical measurement noise and environmental distortions. Ensuring data quality requires rigorous uncertainty propagation and validation procedures.

### Sources of error and physical propagation

The error budget in radiolocation systems comprises four fundamental terms:

$$\sigma_{\text{total}}^2 = \sigma_{\text{timing}}^2 + \sigma_{\text{geometry}}^2 + \sigma_{\text{channel}}^2 + \sigma_{\text{motion}}^2$$

1. **Clock synchronization uncertainty ($\sigma_{\text{timing}}$).** Timing offsets between digitizers map to range errors via $c \approx 300\text{ m/\mu s}$. While GNSS 1PPS references achieve $\sigma_{\text{clk}} \approx 20\text{--}50\text{ ns}$, cable delays ($4\text{--}5\text{ ns/m}$) and receiver filter group delays ($50\text{--}200\text{ ns}$) introduce inter-station biases if uncalibrated.
2. **Geometric Dilution of Precision ($\sigma_{\text{geometry}}$).** GDOP scales timing errors: $\sigma_{\text{pos}} = \text{GDOP} \cdot c \cdot \sigma_{\Delta t}$. Inside the base station network hull, GDOP is 1.5–3.0, but expands beyond 10–20 for vessels far offshore, magnifying small timing errors into substantial position offsets.
3. **Multipath propagation ($\sigma_{\text{channel}}$).** Sea reflections and port structures distort the 24-bit preamble correlation peak, jittering arrival times by tens of nanoseconds and inducing bearing errors of $1^\circ\text{--}3^\circ$.
4. **Platform kinematics ($\sigma_{\text{motion}}$).** While ship motion during a 26.67 ms slot is negligible (<0.5 m at 30 kn), spaceborne receivers travel ~200 m per slot at 7.6 km/s, requiring integration of satellite orbital state vectors during signal capture.

### Calibration and validation procedure

To maintain forensic-grade data quality, operators implement a continuous three-step validation pipeline:
1. **Daily zero-baseline calibration using surveyed AtoNs.** Coastal networks must use fixed, surveyed AIS Aids to Navigation as ground-truth references. Because physical positions of these stations are known to centimeter accuracy via differential GNSS surveys, expected arrival times at all base stations can be computed exactly. Persistent non-zero means in observed TDOA residuals reflect receiver hardware drift or cable temperature changes, subtracted as calibration offset vector $\mathbf{b}_{\text{cal}}$.
2. **Measurement gating and residual thresholding.** Raw burst captures must pass signal-to-noise ratio gates ($\text{SNR} \ge 10\text{ dB}$) and preamble correlation sharpness metrics before ingestion into the radiolocation solver. Bursts exhibiting multiple correlation peaks (indicative of severe multipath reflections or packet collisions) are pruned. The least-squares or EKF solution evaluates the normalized chi-squared residual:

   $$\chi^2 = (\mathbf{z} - \mathbf{h}(\hat{\mathbf{x}}))^T \mathbf{R}^{-1} (\mathbf{z} - \mathbf{h}(\hat{\mathbf{x}}))$$

   If $\chi^2$ exceeds the critical value for $M - 2$ degrees of freedom at $\alpha = 0.01$, the fix is rejected.
3. **Uncertainty reporting standard.** Independent geolocation data points must never be exported as bare point coordinates. Every computed fix must be accompanied by an uncertainty tuple: semi-major axis length ($a_{95}$ in meters), semi-minor axis length ($b_{95}$ in meters), error ellipse orientation angle ($\phi$ in degrees true), solution method (DF, TDOA, TDOA/FDOA, Doppler), and discrepancy metric ($\Delta_{\text{claim}} = \|\hat{\mathbf{x}} - \mathbf{x}_{\text{claimed}}\|$ in meters).

## Software

**Open source:**
- **AIS-catcher** (v0.61+, GPL-3.0). C++ software-defined radio receiver and demodulator for AIS. Supports RTL-SDR, Airspy, SDRplay, and HackRF. Extracts physical-layer metadata for decoded bursts—including received power (in dBFS), carrier frequency offset (in ppm), and nanosecond-resolution hardware arrival timestamps. Caveat: does not include an onboard multi-station hyperbolic TDOA solver; arrival logs must be exported to an external pipeline.
- **GNU Radio (`gr-radar` and `gr-ais`)** (GPL-3.0). Modular signal-processing framework containing blocks for direction-finding beamforming, phase-correlation, and GMSK demodulation. Enables custom flowgraphs for Watson-Watt and pseudo-Doppler phase calculations on multi-channel USRP platforms. Caveat: steep learning curve; requires advanced FPGA programming and coherent RF front-ends to synchronize multi-channel phase measurements.
- **Scipy / NumPy TDOA Solvers** (BSD-3-Clause). Standard scientific computing libraries in Python providing non-linear optimization (`scipy.optimize.least_squares`) and Kalman filtering routines suitable for implementing hyperbolic multilateration equations. Caveat: user must hand-craft coordinate transformation matrices, WGS-84 ellipsoid projections, and GDOP jacobians.

**Free but closed:**
- **RTLSDR-Airband** (open/mixed license, binary distributions). Multichannel AM/NFM demodulator that records time-stamped audio and signal-strength levels across marine VHF frequencies; useful for logging received power levels across multiple listening posts. Caveat: limited to analog demodulation; lacks automated digital AIS frame parsing.

**Commercial:**
- **Rohde & Schwarz R&S MobileLocator / RAMON** (Commercial, proprietary). Radiolocation software integrated with R&S DDF digital direction finders. Automates bearing calculation, triangulation, transmitter tracking, and map overlay in real time across maritime and coastal bands. Caveat: high capital acquisition cost; proprietary interface tightly coupled to Rohde & Schwarz hardware.
- **HawkEye 360 Mission Space / DarkRF Feed** (Commercial subscription API). Cloud-based analytical platform delivering spaceborne RF geolocation fixes, error ellipses, and automated dark-vessel alerts globally. Caveat: high subscription cost; data access restricted to authorized government, defense, and maritime compliance entities.
- **Unseenlabs Maritime Domain Awareness API** (Commercial subscription API). Planetary maritime RF surveillance feed providing independent monosatellite vessel geolocations, track histories, and correlation with AIS records. Caveat: proprietary closed-source signal processing; access subject to commercial licensing.

> **Try it.** *Solving a 3-station coastal TDOA fix with Python and NumPy.*
> The following script takes arrival times of an AIS burst across three coastal stations and solves emitter coordinates via non-linear least squares. Run it inside the book'''s Python environment:
> 
> ```python
> import numpy as np
> from scipy.optimize import least_squares
> 
> C = 299792458.0  # Speed of light in m/s
> stations = np.array([[0.0, 0.0], [40000.0, 10000.0], [15000.0, 35000.0]])
> dt_measured = np.array([-46.051e-6, -36.968e-6])
> claimed_pos = np.array([45000.0, 35000.0])
> 
> def tdoa_residuals(xy, stations, dt_obs):
>     r1 = np.linalg.norm(xy - stations[0])
>     r2 = np.linalg.norm(xy - stations[1])
>     r3 = np.linalg.norm(xy - stations[2])
>     return np.array([(r2 - r1)/C - dt_obs[0], (r3 - r1)/C - dt_obs[1]])
> 
> result = least_squares(tdoa_residuals, [20000.0, 20000.0], args=(stations, dt_measured))
> delta = np.linalg.norm(result.x - claimed_pos)
> print(f"Estimated: {result.x[0]:.1f}m, {result.x[1]:.1f}m | Delta: {delta:.1f}m")
> ```
> 
> **Expected output:**
> ```
> Estimated: 25000.0m, 18000.0m | Delta: 26248.8m
> ```

## Standards & guides

- **ITU-R Recommendation M.1371-5 / M.1371-6 (2014, 2026).** *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile frequency band.* Geneva: International Telecommunication Union. Governs TDMA slot timing (26.67 ms), bit rates (9,600 bit/s), 24-bit training sequence, GMSK modulation index, and transmitter power ramp-up profiles.
- **IEC 62320-1 Ed. 2.0 (2015).** *Maritime navigation and radiocommunication equipment and systems - Automatic identification system (AIS) - Part 1: AIS Base Stations - Minimum operational and performance requirements, methods of testing and required test results.* Geneva: International Electrotechnical Commission. Mandates GNSS-disciplined timing synchronization (1PPS) and standard interface sentences for fixed coastal infrastructure.
- **IEC 62388 Ed. 2.0 (2013).** *Maritime navigation and radiocommunication equipment and systems - European and international standards for shipborne radar - Performance requirements, methods of testing and required test results.* Governs automated correlation of primary radar targets with AIS reports on bridge navigation displays.
- **IALA Guideline G1082 (Ed. 1.0, 2013 / periodic rev.).** *An Overview of AIS.* Saint-Germain-en-Laye: International Association of Marine Aids to Navigation and Lighthouse Authorities. Provides operational guidance on shore-based AIS network design, coverage planning, and coastal surveillance architectures.
- **ITU Radio Regulations (Edition of 2024), Appendix 18 (REV. WRC-19/23).** *Table of transmitting frequencies in the VHF maritime mobile band.* Establishes international frequency allocations for AIS 1 (161.975 MHz), AIS 2 (162.025 MHz), and adjacent VHF marine channels.
- **IMO Resolution MSC.192(79) (Adopted 2004).** *Revised Recommendation on Performance Standards for Radar Equipment.* London: International Maritime Organization. Specifies standards for radar/AIS target integration and false target rejection on SOLAS vessels.

## Pitfalls

- **Confusing direction finding (lines of bearing) with a position fix.** $\to$ Operating a single DF station and assuming target position is known. $\to$ A single DF produces a 1D line of bearing ($\theta$). Determining a 2D fix requires intersecting bearings from multiple stations or combining bearing with primary radar or TDOA.
- **Assuming DF bearings are tagged with vessel MMSIs.** $\to$ Expecting analog or pseudo-Doppler DF receivers to decode AIS packets. $\to$ DF hardware measures RF phase/amplitude without demodulating the 9,600 bit/s GMSK bitstream. Bridge systems must cross-reference DF bearing sentences (`$RATGM`) with AIS target lists using microsecond timestamps.
- **Ignoring Geometric Dilution of Precision in coastal TDOA.** $\to$ Siting all coastal base stations along a straight coastline to locate vessels far offshore. $\to$ Collinear station geometry causes hyperbolic lines of position to run parallel offshore, expanding cross-range uncertainty. Ensure stations surround bays or provide wide baseline diversity.
- **Mistaking tropospheric ducting for deliberate position spoofing.** $\to$ Flagging reports as spoofed because a shore station received them beyond its 30 nmi horizon. $\to$ Marine temperature inversions trap 162 MHz radio waves in surface ducts, carrying signals 300–500 nmi. Correlate atmospheric refractivity profiles ($M$-curves) and multi-station logs before asserting spoofing.
- **Overlooking transmitter oscillator tolerance in single-satellite Doppler fixes.** $\to$ Inverting single-satellite Doppler curves assuming the vessel is tuned to nominal 162.000 MHz. $\to$ ITU-R M.1371 permits transponders a $\pm 500\text{ Hz}$ frequency offset ($\approx \pm 3.1\text{ ppm}$). An uncalibrated 300 Hz oscillator bias translates to tens of kilometers of along-track error unless carrier offset and position are jointly estimated.
- **Neglecting antenna feeder cable delays in TDOA calibration.** $\to$ Swapping an antenna cable at one base station and experiencing persistent 200 m radiolocation errors. $\to$ Coaxial cable propagation delay is $\approx 4.5\text{ ns/m}$ ($c_{\text{coax}} \approx 0.66 c$). A 50 m cable difference introduces 225 ns timing offset ($\approx 67\text{ m}$ range bias). Station hardware delays must be surveyed and zero-calibrated.
- **Attempting single-slot Doppler geolocation on moving vessels without velocity compensation.** $\to$ Applying stationary emitter formulas to fast vessels. $\to$ A ship steaming at 25 kn ($12.9\text{ m/s}$) imposes up to $\pm 7\text{ Hz}$ kinematic Doppler shift at 162 MHz, biasing precise Doppler-rate curve fits.
- **Relying on received signal strength as a direct proxy for distance.** $\to$ Concluding weak signals indicate distant vessels and strong signals indicate nearby vessels. $\to$ Transmitters use different power classes (12.5 W Class A vs 2 W Class B CS vs 5 W Class B SO), antenna heights vary from 3 m to 45 m, and multipath creates deep interference nulls.
- **Failing to synchronize base-station system clocks to a common GNSS 1PPS reference.** $\to$ Using standard Network Time Protocol (NTP) over internet backhaul to time-tag TDOA bursts. $\to$ Internet NTP jitter commonly ranges from 1 to 20 ms, whereas TDOA radiolocation requires sub-microsecond precision. Base stations must utilize hardware GNSS-disciplined oscillators.
- **Assuming satellite RF geolocation provides real-time collision alerts.** $\to$ Expecting spaceborne RF feeds to alert bridge officers of immediate collision risks. $\to$ Satellite constellations operate with revisit intervals from 15 minutes to several hours and processing latencies of 10 to 45 minutes. Spaceborne RF surveillance is a strategic domain-awareness and forensic tool, not a tactical collision sensor.

## Key takeaways

- **AIS broadcast coordinates are unauthenticated assertions.** Because Recommendation ITU-R M.1371 incorporates no cryptographic authentication, digital signatures, or geographic proof, broadcast coordinates must be treated as self-reported claims rather than verified facts.
- **Independent geolocation measures immutable radio physics.** While an adversary can forge MMSIs, vessel names, and GPS positions inside digital packets, they cannot fake the wave-front angle of arrival, multi-station propagation delays, or orbital Doppler frequency shifts imposed by nature upon their physical transmissions.
- **Single-slot direction finding requires agile architectures.** AIS bursts exist for only 26.667 ms. Direction finding across the VHF marine band requires high-speed pseudo-Doppler commutation or multi-channel digital correlative interferometers capable of forming valid bearing lines within 2 to 10 ms.
- **Coastal base-station networks perform opportunistic TDOA.** By leveraging the GNSS-disciplined 1PPS clocks mandated in IEC 62320-1 base stations, existing coastal networks can cross-correlate 24-bit burst preambles, achieving hyperbolic radiolocation with accuracies of hundreds of meters without requiring any onboard equipment changes.
- **Spaceborne clusters provide global, single-burst fixes.** By combining differential arrival times (TDOA) and differential Doppler shifts (FDOA) across three or more formation-flying satellites, commercial operators (such as HawkEye 360) geolocate marine VHF and radar emissions down to sub-kilometer precision anywhere on Earth.
- **Monosatellite RF geolocation enables wide-area maritime surveillance.** Independent nanosatellite systems (such as Unseenlabs''' BRO constellation) geolocate maritime emitters down to roughly 1 kilometer across 300,000 km$^2$ swaths without requiring complex orbital formation flying.
- **Lightweight physical screening flags gross anomalies.** Analysts can rapidly screen vast AIS datasets by testing reports against receiver line-of-sight radio horizons ($d \approx 4.12(\sqrt{h_{\text{rx}}} + \sqrt{h_{\text{tx}}})\text{ km}$), multi-station presence/absence patterns, and primary radar correlation gates.
- **Independent geolocation unmasks dark fleets and spoofers.** Whether locating the *Romina* off Syria via VHF voice communications, recovering drifting AtoNs with corrupted GPS, or homing in on liferaft AIS-SART beacons, independent radiolocation provides the ultimate ground truth for maritime safety and security.

## References

- Androjna, A., Perkovič, M., Pavic, I., Mišković, J. (2021). AIS data vulnerability indicated by a spoofing case-study. *Applied Sciences*, 11(11):5015. doi:10.3390/app11115015
- d'''Afflisio, E., Braca, P., Willett, P. (2021). Malicious spoofing of automatic identification system: A framework for statistical detection and stealth deviations. *IEEE Transactions on Aerospace and Electronic Systems*, 57(4):2093–2108. doi:10.1109/TAES.2021.3083466
- Ellis, K., Van Rheeden, D., Dowla, F. (2020). Use of Doppler and Doppler rate for RF geolocation using a single LEO satellite. *IEEE Access*, 8:29659–29671. doi:10.1109/ACCESS.2020.2965931
- Gattis, J., Cydejko, J., Akos, D. (2026). Real-time detection and localization of Baltic Sea GNSS interference emitters using time-difference-of-arrival. *GPS Solutions*, 30(2):45–58. doi:10.1007/s10291-026-02061-5
- Guo, S. (2014). Space-based detection of spoofing AIS signals using Doppler frequency. *Proceedings of SPIE*, 9253:92530O. doi:10.1117/12.2050448
- HawkEye 360 (2020). *Tracking the Romina: Uncovering Dark Vessels with Spaceborne Radio Frequency Geolocation*. Herndon, VA: HawkEye 360 Inc. (accessed 2026-10-06).
- IEC (2013). *IEC 62388 Ed. 2.0: Maritime navigation and radiocommunication equipment and systems - European and international standards for shipborne radar - Performance requirements, methods of testing and required test results*. Geneva: International Electrotechnical Commission.
- IEC (2015). *IEC 62320-1 Ed. 2.0: Maritime navigation and radiocommunication equipment and systems - Automatic identification system (AIS) - Part 1: AIS Base Stations - Minimum operational and performance requirements, methods of testing and required test results*. Geneva: International Electrotechnical Commission.
- IMO (2004). *Resolution MSC.192(79): Adoption of the Revised Recommendation on Performance Standards for Radar Equipment*. London: International Maritime Organization.
- ITU-R (2014). *Recommendation ITU-R M.1371-5: Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile frequency band*. Geneva: International Telecommunication Union.
- Kessler, G. C., Craiger, J. P., Haass, J. C. (2018). A taxonomy of maritime cybersecurity vulnerabilities and mitigations. *TransNav: International Journal on Marine Navigation and Safety of Sea Transportation*, 12(3):429–437. doi:10.12716/1001.12.03.01
- Kruger, M. (2019). Detection of AIS spoofing in fishery scenarios. In *2019 22th International Conference on Information Fusion (FUSION)*, pp. 1–8. Ottawa: IEEE. doi:10.23919/FUSION43075.2019.9011328
- Papi, F., Tarchi, D., Vespe, M., Oliveri, F., Aulicino, G. (2014). Opportunistic radiolocation of automatic identification system signals. In *2014 IEEE Sensor Array and Multichannel Signal Processing Workshop (SAM)*, pp. 504–507. A Coruña: IEEE. doi:10.1109/SSP.2014.6884686
- Papi, F., Tarchi, D., Vespe, M., Oliveri, F., Borghese, F., Aulicino, G., Vollero, A. (2015). Radiolocation and tracking of automatic identification system signals for maritime situational awareness. *IET Radar, Sonar & Navigation*, 9(5):568–580. doi:10.1049/iet-rsn.2014.0292
- RHOTHETA Elektronik (2022). *RT-500-M Wideband Maritime SAR Radio Direction Finder Technical Specification and User Manual*. Murnau: RHOTHETA Elektronik GmbH.
- Rohde & Schwarz (2021). *R&S DDF255 / DDF550 Digital Direction Finder Product Brochure and Technical Specifications*. Munich: Rohde & Schwarz GmbH & Co. KG.
