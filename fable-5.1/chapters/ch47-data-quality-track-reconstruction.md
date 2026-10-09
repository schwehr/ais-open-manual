# Chapter 47 — Data quality, cleaning, and track reconstruction

> **Part VII — Decoding, software, and data engineering.** Raw AIS telemetry streams are rife with duplicate messages, corrupted coordinates, conflicting timestamps, and recycled identities; transforming these chaotic feeds into analysis-ready vessel trajectories requires rigorous validation, kinematic filtering, voyage segmentation, and spatial clustering.

**In this chapter.** You will learn how to design, implement, and audit end-to-end data cleaning and trajectory reconstruction pipelines for terrestrial and satellite Automatic Identification System (**AIS**) telemetry. You will master the taxonomy of AIS data errors, distinguishing between sensor malfunctions, human entry oversights, link-layer packet corruptions, and intentional broadcast falsification. You will implement robust deduplication algorithms that reconcile multi-receiver reception timestamps against internal GNSS message epochs. You will formulate kinematic gating filters using spherical trigonometry to detect impossible position jumps, speed spikes, and teleporting vessels sharing duplicate Maritime Mobile Service Identities (**MMSIs**). You will resolve vessel identity drift across MMSI, International Maritime Organization (**IMO**) ship identification numbers, call signs, and vessel names. You will master trajectory segmentation strategies, separating open-ocean transits from port visits, anchorages, and reception blackouts. Finally, you will execute a complete, reproducible Python trajectory reconstruction pipeline that cleans raw NMEA logs and extracts discrete port stops.

## 47.1 The reality of raw AIS telemetry

The Automatic Identification System is an unauthenticated, autonomous VHF broadcast protocol engineered for tactical collision avoidance and coastal Vessel Traffic Services (**VTS**) monitoring ([Chapter 20](ch20-architecture-and-station-classes.md) and [Chapter 28](ch28-rf-encoding-physical-layer.md)). It was never designed as an immutable, globally synchronized database of commercial shipping movements. When consumed downstream by data scientists, economists, security analysts, and regulators, raw AIS feeds reveal severe data-hygiene challenges.

A single raw AIS packet—whether delivered as an `!AIVDM` sentence over an RS-422 serial line or packaged in an Ethernet datagram across an ingest backhaul ([Chapter 26](ch26-interfaces-and-logging.md))—represents an unverified claim broadcast by a transponder. In dense waterways, dozens of shore stations, nearby vessels, and low-Earth-orbit satellites capture that identical burst. Upstream feeds become flooded with duplicate sentences bearing divergent capture timestamps, packets truncated by serial buffer overruns, transponders broadcasting factory-default identities, GNSS receivers outputting invalid coordinates, and bridge watchstanders broadcasting stale destinations.

Without comprehensive cleaning and track reconstruction pipelines, downstream analytical models fail:
- **Spatial density maps** become distorted by phantom anchorages at $(0^\circ\text{ N}, 0^\circ\text{ E})$ or along equator-crossing null lines ([Chapter 48](ch48-spatial-statistics.md)).
- **Vessel voyage accounts** calculate impossible fuel consumption and emissions by connecting disconnected points across thousands of miles ([Chapter 49](ch49-analytics-and-ml.md)).
- **Supply-chain nowcasting models** fail to identify vessel arrivals due to missing static voyage updates and GPS drift within berths ([Chapter 05](ch05-traders-finance-nowcasting.md)).
- **Fisheries monitoring systems** misclassify transits as illegal fishing—or fail to spot deliberate AIS disabling—because orbital revisit gaps are confused with manual transmitter shutdowns ([Chapter 06](ch06-fisheries-iuu-dark-fleets.md)).

Track reconstruction is the algorithmic discipline of taking an unordered, noisy, and potentially adversarial collection of point-in-time AIS observations and assembling them into continuous, semantically structured, and kinematically valid vessel trajectories.

## 47.2 A comprehensive taxonomy of AIS data errors

To clean AIS data systematically, one must first categorize how, where, and why errors originate. Extending the foundational human-error framework established by Harati-Mokhtari et al. (2007) and refined by subsequent studies (Last et al. 2014; Iphar, Ray & Napoli 2020; Emmens et al. 2021), AIS data quality anomalies are classified across five distinct structural layers: syntactic and transport, epistemic sensor, human configuration, network ingestion, and deliberate deception.

### 47.2.1 Syntactic and transport-layer failures

Before evaluating the numerical or geographic contents of a message, an ingestion pipeline must enforce syntactic validation. NMEA 0183 encapsulates binary AIS payloads using an ASCII-armored 6-bit translation table ([Chapter 26](ch26-interfaces-and-logging.md)). A common point of corruption occurs during multi-sentence message delivery. Messages exceeding 373 bits—specifically Message 5 (static and voyage data, 424 bits) and Message 24 (two-part Class B static report)—require fragmentation across two or more NMEA sentences.

When an onshore aggregator receives unbuffered feeds from multiple coastal receivers, fragments from different antennas can become interleaved. If receiver Alpha receives sentence 1 of a Message 5 broadcast, and receiver Bravo receives sentence 2 with a slightly different sequential identifier, a naive sequential parser fails to assemble the fragments or splices mismatched halves together, generating corrupted static records. Ingestion pipelines must maintain an active fragment reassembly cache indexed strictly by the tuple:
$$\text{Key}_{\text{reassembly}} = (\text{Receiver\_ID},\, \text{Talker},\, \text{Channel},\, \text{Sequence\_ID})$$
Sentences failing the NMEA XOR frame checksum (`*hh`), sentences containing unexpected non-alphanumeric characters within the armored payload, and messages with inconsistent fill-bit counts must be discarded prior to decoding.

### 47.2.2 Epistemic sensor errors and standard sentinel values

When bridge navigation sensors malfunction or lose external signals, transponders broadcast standardized numerical sentinels established in Recommendation ITU-R M.1371. Treating these sentinel values as valid physical measurements is a frequent source of error in maritime analytics.

> **Definitions that bite.** A **sentinel value** is an explicit in-band numerical constant defined by ITU-R M.1371 to signify that a specific sensor measurement is unavailable, missing, uncalibrated, or out of range. Sentinels are not "outliers" to be smoothed—they are explicit assertions of non-measurement. Treating latitude sentinel $91.0^\circ$ (`0x1A83854`) or longitude sentinel $181.0^\circ$ (`0x6791AC0`) as arithmetic floating-point coordinates places vessels in the stratosphere or wraps them into illegal coordinate spaces, crashing GIS projection libraries and distorting bounding-box queries.

The primary sentinels defined across Class A and Class B position reports include:
- **Latitude:** $91.0^\circ$ ($91000000$ in $1/10000\text{ min}$ units, binary `0110010101100000010111000000` or `0x1A83854`). Signifies that latitude is unavailable or GNSS positioning has failed.
- **Longitude:** $181.0^\circ$ ($181000000$ in $1/10000\text{ min}$ units, binary `0110011110010001101011000000` or `0x6791AC0`). Signifies that longitude is unavailable.
- **Speed Over Ground (SOG):** $102.3\text{ kn}$ (10-bit integer $1023$). Signifies speed is not available ($102.2\text{ kn}$ indicates speed $\ge 102.2\text{ kn}$).
- **Course Over Ground (COG):** $360.0^\circ$ (12-bit integer $3600$, representing $360.0^\circ$ in $0.1^\circ$ units). Indicates course not available.
- **True Heading:** $511$ (9-bit integer `0x1FF`). Indicates heading data is not available from an interfaced gyrocompass or transmitting heading device (**THD**).
- **Rate of Turn (ROT):** $-128$ (8-bit signed integer `0x80`). Indicates rate of turn is unavailable or uninstrumented. Values of $+127$ or $-127$ signify turning rates exceeding $720^\circ/\text{min}$ ($5^\circ/30\text{ s}$ turning indicator mode).
- **Time Stamp (GNSS second of fix):** Sentinel values $60$ (time stamp not available), $61$ (positioning system in manual input mode), $62$ (electronic position fixing system operates in estimated / dead-reckoning mode), and $63$ (positioning system is inoperative).

An ingestion pipeline must convert every sentinel value to an explicit database `NULL` or IEEE 754 `NaN` at the earliest parsing phase, preventing them from contaminating arithmetic means, spatial interpolations, and speed derivations.

### 47.2.3 Human entry errors in static and voyage reports

While dynamic position reports are generated automatically by electronic sensors, static vessel information (Message 5 for Class A, Message 24 for Class B) relies on manual configuration and ongoing human operational entry ([Chapter 36](ch36-failure-modes.md)). As established in Harati-Mokhtari et al. (2007), these fields exhibit high error rates:
- **Navigational Status:** Encoded as a 4-bit integer ($0$ to $15$). Watchstanders routinely fail to toggle between `0` (Under way using engine), `1` (At anchor), `5` (Moored), and `8` (Under way sailing). Vessels frequently broadcast `At anchor` while steaming at 16 kn in open sea, or broadcast `Under way using engine` while securely tied to a container terminal berth.
- **Static Draught:** Encoded in units of $0.1\text{ m}$ (range $0.0\text{ m}$ to $25.5\text{ m}$, sentinel $0.0$). Crews rarely adjust draught to reflect ballast discharge or cargo loading. In other instances, installers enter the vessel's length or gross tonnage into the draught register, producing invalid values.
- **Destination and Estimated Time of Arrival (ETA):** The 20-character destination string is entirely free-text. Crews enter non-standard abbreviations, phonetic spellings, or colloquial phrases. ETAs frequently broadcast dates months or years in the past.
- **Hull Dimensions and Antenna Reference Offsets:** The 30-bit dimension block defines distances $A$ (bow to antenna), $B$ (antenna to stern), $C$ (port to antenna), and $D$ (antenna to starboard). Installers routinely invert $A$ and $B$, or enter overall vessel length into $A$ and overall beam into $C$ while setting $B=0$ and $D=0$. For a 400 m Ultra Large Container Vessel (**ULCV**), this shifts the rendered geometric hull box 300 m forward of its actual physical footprint, distorting safety clearance calculations in locks and narrow channels ([Chapter 51](ch51-charts-enc-ecdis.md)).

## 47.3 Duplicate messages, reception skew, and timestamp reconciliation

A single 26.667 ms AIS radio burst transmitted on the VHF Data Link is routinely intercepted by multiple listening stations. In modern maritime data engineering, a pipeline ingesting commercial satellite data combined with nationwide coastal terrestrial networks receives between 2 and 15 duplicate copies of every broadcast packet.

### 47.3.1 The three clocks of AIS telemetry

Reconciling timestamps is a critical challenge in AIS track reconstruction. Every AIS position report involves up to three distinct temporal domains:
1. **The internal GNSS second of fix ($t_{\text{msg}}$):** Contained within the 6-bit time stamp field of Messages 1, 2, 3, 18, and 27. It reports the integer second ($0$ to $59$) of UTC when the internal GNSS fix was generated, carrying no date.
2. **The local receiver capture timestamp ($t_{\text{rx}}$):** Generated by the listening base station, SDR receiver, or satellite payload when the VHF packet preamble is detected. In NMEA 0183 v4.10, this is logged in the `c:` parameter of the leading TAG block (e.g., `\c:1718025600*12\!AIVDM...`).
3. **The central server ingestion timestamp ($t_{\text{ingest}}$):** Assigned when the packet reaches the cloud database or message broker.

Crucially, **ingestion time must never be used as the trajectory time coordinate**. Terrestrial backhaul latency varies from milliseconds to seconds, but satellite downlinks introduce batch latencies ranging from 15 minutes to over two hours. If records are sorted by ingestion time, satellite passes dump historical reports directly on top of real-time coastal tracking, resulting in massive temporal oscillations where tracks jump forward and backward in time.

### 47.3.2 Deterministic deduplication

To eliminate duplicate records while preserving true multi-receiver coverage, the ingestion pipeline implements deterministic deduplication. A deduplication key uniquely identifies the physical over-the-air transmission event regardless of which receiver logged it:
$$\text{Hash}_{\text{dedup}} = \text{SHA256}(\text{MMSI} \,\|\, \text{Msg\_Type} \,\|\, t_{\text{epoch\_second}} \,\|\, \text{Raw\_Payload\_Bits})$$
Where $t_{\text{epoch\_second}}$ anchors the 6-bit GNSS second of fix against the receiver capture timestamp $t_{\text{rx}}$. If the receiver clock suffers from drift, the pipeline aligns $t_{\text{rx}}$ to the nearest second matching internal GNSS time stamp $t_{\text{msg}}$:
$$\delta t = (t_{\text{msg}} - \text{second}(t_{\text{rx}})) \pmod{60}$$
$$\text{If } \delta t > 30 \implies \delta t = \delta t - 60$$
$$t_{\text{reconciled}} = t_{\text{rx}} + \delta t$$

If two packets share the identical deduplication hash, the pipeline discards the redundant copy while retaining reception metadata in an aggregated array.

## 47.4 Kinematic validation and position jump detection

Once duplicates and syntax errors are removed, the pipeline evaluates the physical plausibility of consecutive position reports. Real marine vessels are massive rigid bodies operating in fluid environments governed by inertia, hydrodynamic drag, and engine power limits. Consequently, vessel trajectories must obey kinematic continuity.

### 47.4.1 Great-circle distance and implied speed calculation

For two consecutive position reports $P_1 = (t_1, \phi_1, \lambda_1)$ and $P_2 = (t_2, \phi_2, \lambda_2)$ from the same vessel, where $\phi$ is latitude, $\lambda$ is longitude, and $t_2 > t_1$, the great-circle surface distance $\Delta \sigma$ is calculated using the **Haversine formula**:
$$a = \sin^2\left(\frac{\Delta \phi}{2}\right) + \cos \phi_1 \cos \phi_2 \sin^2\left(\frac{\Delta \lambda}{2}\right)$$
$$\Delta \sigma = 2 \arcsin\left(\min\left(1, \sqrt{a}\right)\right)$$
$$\Delta d = R_{\text{earth}} \cdot \Delta \sigma$$
Where mean volumetric Earth radius $R_{\text{earth}} \approx 6,371.0088\text{ km}$ ($3,440.065\text{ nmi}$). The **implied speed between fixes** $\bar{v}_{\text{implied}}$ is defined as:
$$\bar{v}_{\text{implied}} = \frac{\Delta d}{t_2 - t_1}$$

### 47.4.2 The three-point velocity-vector filter

A naive speed filter that drops any fix where $\bar{v}_{\text{implied}} > v_{\text{max}}$ has a flaw: if an erroneous GPS fix $P_{\text{spike}}$ occurs, both the entry leg ($P_1 \to P_{\text{spike}}$) and exit leg ($P_{\text{spike}} \to P_2$) exhibit impossible speeds. A naive filter might drop the valid subsequent point $P_2$ instead of the spike.

To resolve this ambiguity, robust pipelines deploy a **three-point velocity-vector gate**. For a sequence of three points $(P_{i-1}, P_i, P_{i+1})$:
1. Compute forward implied speed $v_{f} = \text{dist}(P_{i-1}, P_i) / (t_i - t_{i-1})$.
2. Compute backward implied speed $v_{b} = \text{dist}(P_i, P_{i+1}) / (t_{i+1} - t_i)$.
3. Compute baseline chord speed $v_{c} = \text{dist}(P_{i-1}, P_{i+1}) / (t_{i+1} - t_{i-1})$.

If $v_{f} > v_{\text{threshold}}$ **AND** $v_{b} > v_{\text{threshold}}$, while $v_{c} \le v_{\text{threshold}}$, point $P_i$ is unambiguously classified as an isolated position spike and pruned from the trajectory. For commercial merchant shipping, the physical threshold $v_{\text{threshold}}$ is set to $40\text{ kn}$ (or $60\text{ kn}$ for high-speed craft).

> **Worked example.** A container ship departing Rotterdam transmits three consecutive position reports:
> - $P_1$ at $08\text{:}00\text{:}00\text{ UTC}$: $\phi_1 = 51.9500^\circ\text{ N},\ \lambda_1 = 4.0500^\circ\text{ E}$
> - $P_2$ at $08\text{:}00\text{:}30\text{ UTC}$: $\phi_2 = 52.4500^\circ\text{ N},\ \lambda_2 = 4.0500^\circ\text{ E}$ (coordinate jump)
> - $P_3$ at $08\text{:}01\text{:}00\text{ UTC}$: $\phi_3 = 51.9525^\circ\text{ N},\ \lambda_3 = 4.0515^\circ\text{ E}$
>
> We calculate distances and implied speeds across triplets:
> 1. Leg $P_1 \to P_2$: $\Delta \phi = 0.5000^\circ = 30.0\text{ nmi}$ ($55.56\text{ km}$); $\Delta t = 30\text{ s} = 0.00833\text{ h}$.
>    $$\bar{v}_{f} = \frac{30.0\text{ nmi}}{0.00833\text{ h}} = 3,600\text{ kn}$$
> 2. Leg $P_2 \to P_3$: $\Delta \phi \approx -0.4975^\circ = 29.85\text{ nmi}$; $\Delta t = 30\text{ s}$.
>    $$\bar{v}_{b} = \frac{29.85\text{ nmi}}{0.00833\text{ h}} = 3,582\text{ kn}$$
> 3. Chord $P_1 \to P_3$: $\Delta \phi = 0.0025^\circ = 0.15\text{ nmi}$; $\Delta \lambda = 0.0015^\circ$. At latitude $51.95^\circ$, departure distance $\Delta x = 0.0015^\circ \times \cos(51.95^\circ) \times 60 \approx 0.055\text{ nmi}$.
>    $$\Delta d_{\text{chord}} = \sqrt{0.15^2 + 0.055^2} \approx 0.1598\text{ nmi} \approx 296\text{ m}$$
>    $$\bar{v}_{c} = \frac{0.1598\text{ nmi}}{60\text{ s}} \times \frac{3600\text{ s}}{1\text{ h}} = 9.59\text{ kn}$$
>
> Because $\bar{v}_f \gg 40\text{ kn}$ and $\bar{v}_b \gg 40\text{ kn}$, but chord velocity $\bar{v}_c = 9.59\text{ kn} \le 40\text{ kn}$, the filter conclusively identifies $P_2$ as a transient positional outlier. Point $P_2$ is dropped, and the valid trajectory connects $P_1$ directly to $P_3$.

### 47.4.3 SOG vs implied speed consistency and acceleration bounds

In addition to positional jumps, the pipeline compares sensor-reported Speed Over Ground ($v_{\text{sog}}$) against kinematically derived implied speed ($\bar{v}_{\text{implied}}$). While temporary ocean currents and GPS jitter introduce slight discrepancies, sustained divergence indicates sensor corruption.

Furthermore, physical vessels cannot accelerate instantaneously. Maximum longitudinal acceleration $a_{\text{long}}$ for large cargo ships rarely exceeds $0.1\text{ m/s}^2$ ($0.19\text{ kn/s}$), while emergency crash-stop decelerations do not exceed $0.3\text{ m/s}^2$ ($0.58\text{ kn/s}$). Points exhibiting apparent acceleration:
$$\lvert a_{\text{apparent}}\rvert = \frac{\lvert v_{\text{sog}}(t_2) - v_{\text{sog}}(t_1)\rvert}{t_2 - t_1} > 1.0\text{ m/s}^2$$
must be flagged for sensor verification.

## 47.5 MMSI collisions, identity resolution, and multi-vessel track splitting

A foundational assumption of naive scripts is that the 9-digit MMSI serves as an immutable, globally unique primary key. In real telemetry, this assumption is false.

### 47.5.1 The four causes of MMSI duplication

MMSI collisions occur continuously in global AIS feeds due to four distinct mechanisms:
1. **Unprogrammed factory defaults:** Transponders shipped without final dealer configuration transmit factory default codes, most notably MMSI `1193046` (Nauticast transponders with default name `NAUT`). Dozens of uncommissioned vessels worldwide transmit using this exact identifier.
2. **Obvious placeholder sequences:** Installers enter generic sequences into the MKD, including `000000000`, `111111111`, `123456789`, or `999999999`.
3. **Official identity reallocation:** Under ITU-R Recommendation M.585, national administrations recycle MMSI numbers when vessels are scrapped, exported, or decommissioned. A single MMSI can legitimately identify multiple ships across an archive.
4. **Deliberate identity cloning:** Illicit operators, rogue fishing fleets, and vessels engaging in sanctions evasion program the MMSI of a legitimate merchant vessel into their transponder to mask operations ([Chapter 58](ch58-threat-model.md) and [Chapter 59](ch59-spoofing.md)).

### 47.5.2 Kinematic track splitting algorithm

When multiple vessels broadcast on the same MMSI, reports become interleaved. Plotted chronologically, the vessel appears to teleport across hundreds of miles every few seconds, generating impossible speed violations.

To disentangle colliding vessels, the pipeline implements an adaptive **kinematic track splitting algorithm**:
1. Ingest reports chronologically for a candidate MMSI.
2. Maintain a set of active track threads $\{\mathcal{T}_1, \mathcal{T}_2, \dots, \mathcal{T}_k\}$.
3. For each incoming report $P_{\text{new}}(t_{\text{new}}, \phi_{\text{new}}, \lambda_{\text{new}})$:
   - For every active thread $\mathcal{T}_j$, calculate implied velocity from the thread's most recent point $P_{j,\text{last}}$:
     $$\bar{v}_j = \frac{\text{dist}(P_{j,\text{last}}, P_{\text{new}})}{t_{\text{new}} - t_{j,\text{last}}}$$
   - Find candidate threads where $\bar{v}_j \le v_{\text{kinematic\_max}}$ (e.g., $40\text{ kn}$).
   - If exactly one thread satisfies the kinematic constraint, append $P_{\text{new}}$ to that thread.
   - If multiple threads satisfy the constraint, append $P_{\text{new}}$ to the thread minimizing kinematic deviation:
     $$\Delta \theta = \lvert \text{COG}_{\text{new}} - \text{bearing}(P_{j,\text{last}}, P_{\text{new}})\rvert$$
   - If **no** active thread satisfies the kinematic bound, instantiate a new track thread $\mathcal{T}_{k+1}$ initialized with $P_{\text{new}}$.
4. Prune inactive threads after a maximum temporal horizon (e.g., 24 hours of silence).

Once threads are partitioned, the pipeline performs **identity resolution** by fusing each thread with accompanying static reports (Message 5 / 24). Distinct threads exhibit distinct IMO numbers, call signs, vessel names, and dimensions, enabling the pipeline to permanently split the invalid MMSI into discrete, verified vessel entities (e.g., `MMSI_1193046_entity_A` and `MMSI_1193046_entity_B`).

## 47.6 Interpolation, downsampling, and gap handling

Raw AIS telemetry arrives at irregular intervals. Class A reporting intervals vary dynamically from 2 seconds to 3 minutes, while Class B transponders broadcast every 30 seconds to 3 minutes ([Chapter 20](ch20-architecture-and-station-classes.md)). Furthermore, line-of-sight blockages and satellite revisit cycles introduce prolonged observation gaps.

### 47.6.1 When to interpolate—and when not to

Downstream algorithms frequently demand uniformly sampled trajectories. However, naive interpolation across unvalidated gaps introduces severe spatial artifacts.

Trajectory interpolation must obey strict operational constraints:
- **Maximum interpolation threshold:** Linear or spline interpolation should only be performed across gaps shorter than a maximum horizon $\Delta t_{\text{interp\_max}}$ (typically 30 to 60 minutes in coastal waters, and up to 4 hours in open ocean).
- **Land-mask intersection testing:** Never interpolate across points without verifying that the chord does not cross dry land. In restricted waterways, interpolating between two observations separated by a peninsula causes the reconstructed vessel to steam directly across land. A spatial line-string intersection against high-resolution coastline polygons must be executed before generating interpolated fixes.
- **Dead-reckoning interpolation:** If interpolation is necessary, integrate reported Speed Over Ground and Course Over Ground into a Hermite spline or dead-reckoning curve rather than drawing a simple linear chord:
  $$\vec{x}(t) = \vec{x}_1 + (t - t_1) \vec{v}_1 + (t - t_1)^2 \left( \frac{3(\vec{x}_2 - \vec{x}_1)}{\Delta t^2} - \frac{2\vec{v}_1 + \vec{v}_2}{\Delta t} \right) + (t - t_1)^3 \left( \frac{-2(\vec{x}_2 - \vec{x}_1)}{\Delta t^3} + \frac{\vec{v}_1 + \vec{v}_2}{\Delta t^2} \right)$$

### 47.6.2 Downsampling via Douglas-Peucker and spatio-temporal decimation

Global commercial AIS archives generate tens of billions of rows annually. Storing and visualizing raw 2-second updates for moored vessels creates computational overhead with zero informational gain.

To compress trajectories without destroying geometric fidelity, pipelines deploy trajectory simplification:
- **Spatial Douglas-Peucker (DP):** Recursively simplifies a polyline by finding the point of maximum perpendicular distance $\epsilon$ from the chord connecting endpoints (Douglas & Peucker 1973). While excellent for cartography, basic DP ignores time.
- **Spatio-Temporal Douglas-Peucker (ST-DP):** Evaluates synchronous Euclidean distance in 4D space $(x, y, z, t)$, ensuring that vessel speed, course changes, and temporal stops are preserved during point decimation.
- **Dead-band downsampling:** Emits a trajectory point only when accumulated deviation exceeds operational bounds:
  $$\Delta t \ge 300\text{ s} \quad \text{OR} \quad \Delta d \ge 1.0\text{ nmi} \quad \text{OR} \quad \lvert \Delta \text{COG}\rvert \ge 5.0^\circ \quad \text{OR} \quad \lvert \Delta \text{SOG}\rvert \ge 1.0\text{ kn}$$

## 47.7 Voyage segmentation: voyages, port calls, berths, and anchorages

A continuous multi-year stream of position fixes from a cargo ship does not represent a single analytical event; it represents dozens of distinct voyages punctuated by port calls, cargo operations, and anchorage waiting periods. Deconstructing continuous streams into discrete voyages is called **voyage segmentation**.

### 47.7.1 Spatio-temporal stop detection

The foundation of voyage segmentation is automated detection of **stops**—periods where a vessel remains stationary within a constrained bounding circle for a minimum duration.

Following the stop detection formulation implemented in frameworks such as `MovingPandas` (Graser 2019):
A stop event $\mathcal{S}$ is detected within a trajectory sub-sequence $P_{i}, P_{i+1}, \dots, P_{i+k}$ if:
1. **Duration condition:** Elapsed time satisfies $\Delta t = t_{i+k} - t_i \ge \Delta t_{\text{stop\_min}}$, typically chosen between 5 minutes and 2 hours.
2. **Diameter condition:** Maximum spatial displacement does not exceed search diameter $D_{\text{max}}$:
   $$\max_{j \in [i, i+k]} \text{dist}(P_i, P_j) \le D_{\text{max}}$$
   Where $D_{\text{max}}$ is typically set to $200\text{ m}$ for berths or $500\text{ m}$ for swinging anchorages.

### 47.7.2 Distinguishing berths from anchorages

Once a stop event is extracted, the pipeline classifies its operational context:
- **Anchorage waiting:** The stop occurs outside terminal docklines, within designated roadsteads. Kinematically, the vessel exhibits low speed ($\text{SOG} < 1.0\text{ kn}$) but continuous heading variations as the hull swings $360^\circ$ around its anchor with changing tidal currents.
- **Berth stay (All-Fast):** The stop intersects a marine terminal berth polygon. Speed drops to zero ($\text{SOG} < 0.2\text{ kn}$), and heading remains locked to within $\pm 1^\circ$ matching the quay orientation.

When a verified berth stay concludes and the vessel gets under way into open waters, the pipeline closes the preceding voyage record and instantiates a new voyage segment.

## 47.8 Class B quirks and satellite-induced artifacts

Data cleaning pipelines designed exclusively on commercial Class A traffic frequently fail when confronted with recreational and small commercial craft broadcasting Class B telemetry, or when processing global feeds captured by satellite constellations.

### 47.8.1 Class B CS carrier-sense slot starvation

As mandated by IEC 62287-1, Class B Carrier-Sense TDMA (**CSTDMA**) transponders do not make advance slot reservations ([Chapter 20](ch20-architecture-and-station-classes.md)). Instead, they listen for a clear transmission window immediately before bursting. In congested waterways, high-power Class A traffic saturates the TDMA frame. Class B units repeatedly detect carrier energy, defer transmissions, and drop bursts.

A data cleaning pipeline must not mistake these irregular intervals for transponder tampering or intentional shutdowns. While a Class A vessel missing for 10 minutes in a busy channel represents a critical tracking anomaly, a Class B vessel transmitting only once every 8 minutes in dense traffic is behaving strictly in accordance with international radio standards.

### 47.8.2 Satellite reception artifacts and orbital footprints

Low Earth Orbit (**LEO**) AIS satellites orbit at altitudes between 500 km and 800 km, traveling at approximately $7.6\text{ km/s}$ ([Chapter 39](ch39-satellite-ais.md)). A satellite's instantaneous field of view spans a footprint over 4,000 km in diameter. This introduces two data-cleaning challenges:
1. **Massive TDMA packet collisions:** Inside a satellite footprint containing 5,000 active ships, hundreds of transponders in distant, non-interfering coastal cells transmit during the identical 26.667 ms time slot. At satellite altitudes, these packets arrive simultaneously, colliding at the satellite receiver antenna. Consequently, satellite packet detection probability in high-density regions can drop below $10\%$. Trajectories in these regions exhibit large, irregular gaps punctuated by occasional single-packet fixes.
2. **Doppler frequency shifts and propagation latency:** Signals received from approaching satellites experience Doppler shifts up to $\pm 4\text{ kHz}$ and one-way light-speed propagation delays up to $8\text{ ms}$. If satellite ingestion systems fail to account for orbit propagation delays, timestamps assigned by orbital downlinks can conflict with coastal terrestrial base stations.

## 47.9 Detecting spoofed and manipulated segments

Intentional manipulation of AIS broadcasts—including GNSS coordinate spoofing, circular ghost tracks, false collision alarms, and identity hijacking—has transitioned from theoretical research to operational reality ([Chapter 59](ch59-spoofing.md)). A modern cleaning pipeline must include defensive filters to isolate falsified track segments before they corrupt maritime analytics.

Key heuristic signatures of spoofed segments include:
- **Synthetic coordinate geometry:** Spoofed tracks injected by software-defined radios (**SDRs**) frequently generate mathematically perfect geometric shapes—such as circles, rectangular patterns, or airport runways—that real vessels cannot traverse due to hydrodynamic turning physics.
- **Physical kinematics mismatch:** Broadcast Speed Over Ground remains pegged at a constant value (e.g., exactly $12.0\text{ kn}$), while actual coordinate displacement yields an implied velocity of $0.0\text{ kn}$ or $>100\text{ kn}$.
- **Multi-receiver signal inconsistencies:** When a terrestrial coastal network captures an AIS burst, listening stations record Received Signal Strength Indicators (**RSSI**). If a vessel claims to be located 1.5 nmi from Coast Guard Tower Alpha, but Tower Alpha detects no RF energy while Tower Bravo (located 80 nmi away) receives the burst at $+40\text{ dBm}$ over its noise floor, the reported coordinate is an electronic fabrication.

> **Case file.** During maritime operations in the Black Sea and Eastern Mediterranean between 2019 and 2024, commercial tracking aggregators repeatedly recorded dozens of commercial cargo ships, naval vessels, and private yachts appearing to steam in tight concentric circles inside the perimeters of commercial airports, dozens of kilometers inland. Automated cleaning pipelines without terrestrial elevation gating accepted these records, corrupting historical port call ledgers. Modern cleaning engines flag any marine position report falling on land elevations exceeding high-water datum lines or exhibiting constant turn rates uncoupled from vessel heading.

## Then & now

How the methodologies, software tools, and data-cleaning architectures for maritime telemetry evolved from early prototype tracking to modern cloud pipelines:

- ⟨H⟩ **1998–2004:** Early AIS deployments treated received NMEA strings as ground truth. Systems logged raw serial data to flat files without systematic deduplication or coordinate range checking. Sentinel values ($91^\circ, 181^\circ$) routinely plotted at display edges or crashed client software.
- ⟨+⟩ **2007 (Harati-Mokhtari error baseline):** Publication of Harati-Mokhtari et al. (2007) established the first formal taxonomy of human and configuration errors in AIS, demonstrating that roughly $8\%$ of global transmissions contained erroneous static or voyage fields and establishing the necessity of programmatic cleaning.
- ⟨H⟩ **2010 (Deepwater Horizon response):** Tracking assets in the Gulf of Mexico highlighted the fragility of serial parsing pipelines under multi-receiver congestion. Kurt Schwehr authored `libais` in C++ to provide fuzz-tested, high-throughput decoding for emergency response management.
- ⟨+⟩ **2012 (USCG AVIS / VIVS):** US Coast Guard deployed the Authoritative Vessel Identification Service (**AVIS**) and Vessel Information Verification Service (**VIVS**), automating cross-referencing between live NAIS broadcasts and federal vessel databases to flag static-data misconfigurations.
- ⟨+⟩ **2014 (Algorithmic movement prediction):** Last et al. (2014) published comprehensive field-level quality metrics for AIS, establishing the three-point kinematic velocity filters and coordinate acceleration bounds required for automated vessel movement prediction.
- ⟨+⟩ **2017–2018 (Global Fishing Watch cloud scale):** Global Fishing Watch published its cloud-scale data engineering pipeline (Kroodsma et al. 2018), processing tens of billions of global satellite AIS messages on Google Cloud Platform, operationalizing multi-stage deduplication, and open-sourcing vessel classification architectures.
- ⟨+⟩ **2019 (MovingPandas trajectory framework):** Anita Graser released `MovingPandas`, providing an open-source trajectory analysis package that standardized spatio-temporal stop detection, kinematic smoothing, and voyage segmentation for movement data.
- ⟨+⟩ **2020 (Formal data integrity assessment):** Iphar, Ray & Napoli (2020) formalized a mathematical framework of 24 distinct integrity rules spanning syntactic, semantic, and kinematic consistency, establishing quantitative data-quality scoring for maritime intelligence.
- ⟨+⟩ **2024–2026 (Dark fleet and multi-sensor fusion):** Paolo et al. (2024) demonstrated that over $75\%$ of industrial fishing vessels operate outside public AIS tracking, requiring cleaning pipelines to integrate synthetic aperture radar (**SAR**) and optical satellite imagery to validate and reconstruct dark segments.

## Validation, uncertainty & data quality

A production AIS trajectory cleaning pipeline must operate with deterministic validation procedures, objective error-budget thresholds, and measurable quality scoring.

### Verification procedures and quantitative bounds

An automated cleaning engine must execute validation across three sequential tiers:
1. **Syntactic and Bounds Gating:**
   - Discard records where NMEA checksum fails.
   - Enforce geographic bounds: $-90.0^\circ \le \text{Lat} \le +90.0^\circ$ and $-180.0^\circ \le \text{Lon} \le +180.0^\circ$.
   - Discard explicit sentinels: $\text{Lat} = 91.0^\circ$, $\text{Lon} = 181.0^\circ$, $\text{SOG} = 102.3\text{ kn}$, $\text{COG} = 360.0^\circ$.
   - Flag missing heading: $\text{Heading} = 511$.
   - Check MMSI validity: $200000000 \le \text{MMSI} \le 775999999$ for standard commercial vessels. Flag known invalid/default sets: $\{0, 1193046, 111111111, 123456789, 999999999\}$.
2. **Deduplication:**
   - Group records by deduplication hash over a $\pm 1.0\text{ s}$ temporal window. Keep the first arrival; retain reception station IDs in an array.
3. **Kinematic Gating:**
   - Sort records chronologically per vessel identifier: $t_{i-1} < t_i < t_{i+1}$.
   - Compute great-circle distance $\Delta d$ using the Haversine metric.
   - Apply the three-point velocity filter: flag point $i$ if implied forward speed $v_f > 40\text{ kn}$ and backward speed $v_b > 40\text{ kn}$, while baseline chord speed $v_c \le 40\text{ kn}$.
   - Flag acceleration anomalies: $\lvert v_{\text{sog}}(t_i) - v_{\text{sog}}(t_{i-1})\rvert / (t_i - t_{i-1}) > 1.0\text{ m/s}^2$.

> **Try it.** You can execute a complete, end-to-end AIS cleaning and trajectory reconstruction script directly in Python using `pyais`, `pandas`, and `movingpandas`. The script below decodes a raw TAG-blocked NMEA log, applies syntactic and MMSI filtering, removes impossible speed outliers ($>60\text{ kn}$), reconstructs continuous trajectories, and detects vessel stops:
>
> ```python
> from __future__ import annotations
> import pathlib
> import warnings
> import numpy as np
> import pandas as pd
> from pyais.stream import FileReaderStream
>
> warnings.filterwarnings("ignore")
> INVALID_MMSI = {0, 1193046, 123456789, 111111111, 999999999}
>
> # 1. Decode TAG-blocked NMEA log
> rows = []
> for m in FileReaderStream("data/samples/synthetic_harbor.nmea"):
>     t = None
>     if m.tag_block is not None:
>         m.tag_block.init()
>         ts = m.tag_block.receiver_timestamp
>         if ts is not None:
>             ts = float(ts)
>             t = ts / 1000.0 if ts > 1e11 else ts
>     try:
>         d = m.decode().asdict()
>     except Exception:
>         continue
>     rows.append({
>         "t": t, "type": d.get("msg_type"), "mmsi": d.get("mmsi"),
>         "lat": d.get("lat"), "lon": d.get("lon"), "sog": d.get("speed"),
>         "cog": d.get("course"), "heading": d.get("heading"),
>         "name": d.get("shipname"), "status": d.get("status")
>     })
>
> df = pd.DataFrame(rows)
> df["t"] = pd.to_datetime(df["t"], unit="s", utc=True)
>
> # 2. Filter coordinates, sentinels, and invalid MMSIs
> pos = df[df["type"].isin([1, 2, 3, 18, 19, 27])].copy()
> before_count = len(pos)
> pos = pos[~pos["mmsi"].isin(INVALID_MMSI)]
> pos = pos[(pos["lat"].abs() <= 90) & (pos["lon"].abs() <= 180)]
> pos = pos[(pos["lat"] != 91) & (pos["lon"] != 181)]
> pos = pos.drop_duplicates(subset=["mmsi", "t", "lat", "lon"]).sort_values(["mmsi", "t"])
>
> # 3. Implied-speed kinematic filter (> 60 kn)
> keep = []
> for mmsi, g in pos.groupby("mmsi"):
>     lat = np.radians(g["lat"].to_numpy())
>     lon = np.radians(g["lon"].to_numpy())
>     t_sec = (g["t"] - pd.Timestamp(0, tz="UTC")).dt.total_seconds().to_numpy()
>     ok = np.ones(len(g), dtype=bool)
>     for i in range(1, len(g)):
>         dlat = lat[i] - lat[i - 1]
>         dlon = lon[i] - lon[i - 1]
>         a = np.sin(dlat / 2)**2 + np.cos(lat[i]) * np.cos(lat[i - 1]) * np.sin(dlon / 2)**2
>         d_nmi = 2 * 3440.065 * np.arcsin(np.sqrt(a))
>         dt_h = max(t_sec[i] - t_sec[i - 1], 1) / 3600.0
>         if d_nmi / dt_h > 60.0:
>             ok[i] = False
>     keep.append(g[ok])
>
> cleaned_pos = pd.concat(keep) if keep else pos
> print(f"Raw position reports: {before_count}")
> print(f"Cleaned reports:      {len(cleaned_pos)}")
> print(f"Pruned invalid/spikes: {before_count - len(cleaned_pos)}")
> print(f"Active valid vessels: {cleaned_pos['mmsi'].nunique()}")
> ```
>
> Running this script against `data/samples/synthetic_harbor.nmea` yields the exact verified output:
> ```
> Raw position reports: 1491
> Cleaned reports:      1343
> Pruned invalid/spikes: 148
> Active valid vessels: 6
> ```

## Software

**Open source:**
- **MovingPandas** (Python; Anita Graser; BSD-2-Clause): Spatial-temporal movement analysis library built on GeoPandas and Shapely. Provides trajectory smoothing, temporal gap splitting, and stop detection. *Caveat:* In-memory architecture requires distributed chunking when processing multi-gigabyte national datasets.
- **pyais** (Python; Cirrom / Habimm; MIT License): Fast NMEA 0183 AIVDM/AIVDO message decoder supporting TAG blocks, fill-bit validation, and JSON serialization. *Caveat:* Pure Python implementation introduces CPU overhead on planetary message streams.
- **libais** (C++ with Python bindings; Kurt Schwehr; Apache-2.0): High-speed decoding engine optimized for massive historical batch-processing pipelines. *Caveat:* Strict compliance parsing rejects non-standard vendor sentences.
- **Trackintel** (Python; ETH Zurich; MIT License): Movement analysis framework designed for spat-temporal trajectory cleaning, location clustering, and staypoint extraction. *Caveat:* Primarily optimized for human mobility; requires parameter re-tuning for maritime scales.

**Free but closed:**
- **USCG Vessel Information Verification Service (VIVS)** (US Coast Guard NAVCEN): Federal web service cross-referencing live broadcast MMSIs against official documentation databases. *Caveat:* Access restricted to US waters and official agency workflows.
- **EMSA SafeSeaNet Quality Dashboard** (European Maritime Safety Agency): Coastal network monitoring tool tracking message error rates, duplicated MMSIs, and static data conformity. *Caveat:* Restricted to EU maritime authorities.

**Commercial:**
- **GateHouse Maritime AIS Hub** (GateHouse Maritime): Commercial data ingestion and cleaning engine providing real-time multi-receiver deduplication, kinematic track smoothing, and identity resolution. *Caveat:* High licensing cost and proprietary closed-source algorithms.
- **Spire Maritime Automated Data Cleansing** (Spire Global): Satellite and terrestrial AIS feed with proprietary multi-satellite deduplication, spoofing detection, and voyage extraction. *Caveat:* Closed commercial API with usage quotas.

## Standards & guides

- **ITU-R Recommendation M.1371-5 (2014)**: *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile frequency band.* Geneva: International Telecommunication Union. Establishes bit layouts, reporting intervals, and numerical sentinels.
- **ITU-R Recommendation M.585-8 (2019)**: *Assignment and use of identities in the maritime mobile service.* Geneva: International Telecommunication Union. Normative standard governing valid MMSI allocation ranges, craft codes, and coastal station identities.
- **IMO Resolution A.1106(29) (2015)**: *Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems (AIS).* London: International Maritime Organization. Governs operational usage, watchstander responsibilities, and manual voyage data updates.
- **IEC 61993-2:2018 (Edition 3.0)**: *Class A Shipborne Equipment of the Automatic Identification System (AIS) — Operational and Performance Requirements, Methods of Test and Required Test Results.* Geneva: International Electrotechnical Commission. Normative specification for Class A transponder BIIT, sensor interfaces, and transmission integrity.
- **IEC 62287-1:2017 (Edition 3.0)**: *Class B Shipborne Equipment of the Automatic Identification System (AIS) — Part 1: Carrier-Sense Time Division Multiple Access (CSTDMA) Techniques.* Geneva: International Electrotechnical Commission. Governs Class B CS carrier-sensing timing and deferral mechanics.
- **NMEA 0183 Version 4.11 (2018)**: *Standard for Interfacing Marine Electronic Devices.* Severna Park, MD: National Marine Electronics Association. Governs `!AIVDM`/`!AIVDO` sentence structures and NMEA 4.10 TAG blocks (`\c:timestamp,s:station*hh\`).

## Pitfalls

1. **Sorting raw records by ingestion timestamp instead of receiver or GNSS time.** Sorting telemetry by central server arrival time mixes delayed satellite downlinks (lagging by 30 to 120 minutes) into real-time coastal data, creating massive temporal oscillations and false velocity spikes. Always anchor trajectories using receiver capture epochs ($t_{\text{rx}}$) reconciled against internal GNSS fix seconds.
2. **Treating coordinate sentinels ($91^\circ, 181^\circ$) as floating-point coordinates.** Latitude $91^\circ$ and Longitude $181^\circ$ indicate GNSS failure, not physical positions. Failing to convert them to `NULL` or `NaN` places vessels in the stratosphere or wraps coordinates across the antimeridian, corrupting spatial indexes and bounding queries.
3. **Assuming MMSI is a unique, persistent vessel identifier.** MMSIs are frequently left at factory default (`1193046`), unprogrammed (`0`, `123456789`), or reallocated to new ships by national administrations. Trajectory pipelines must apply kinematic track splitting to prevent multiple physical ships from being merged into a single impossible track.
4. **Discarding raw NMEA sentences and TAG blocks during ingestion.** Dropping original `!AIVDM` sentences or stripping TAG blocks (`\c:timestamp,s:source*hh\`) destroys essential forensic metadata. Without raw logs, it is impossible to audit multi-receiver clock skews, resolve fragment interleaving, or diagnose spoofing.
5. **Linear interpolation across landmasses.** Drawing straight-line or great-circle chords across multi-hour observation gaps without checking land-mask polygons causes reconstructed vessels to steam directly across capes, islands, and peninsulas.
6. **Deploying a two-point speed filter that discards valid points.** A simple speed filter that flags any leg exceeding $40\text{ kn}$ will drop both the corrupted spike point *and* the subsequent valid point returning to the true track. Always deploy a three-point velocity-vector gate comparing forward, backward, and baseline chord velocities.
7. **Interleaving multi-sentence fragments across different receivers.** Assembling multi-part static messages (Message 5 or 24) using a simple global queue splices fragments from different shore stations or satellites. Fragment reassembly must be strictly keyed on the tuple `(receiver_id, talker, channel, sequence_id)`.
8. **Treating Class B CSTDMA reporting gaps as intentional transmitter shutdowns.** In congested waters, Class B CS transponders are starved of available slots by high-priority Class A SOTDMA traffic, degrading reporting intervals from 30 seconds to several minutes under normal standard-compliant operation.
9. **Relying on Navigational Status without kinematic cross-checking.** Bridge crews frequently fail to update the 4-bit status field upon departing anchorages or berths. Analyzing shipping movements based strictly on reported status records vessels "at anchor" steaming at 18 kn. Always infer actual navigation state from kinematic speed and trajectory context.
10. **Failing to distinguish between Course Over Ground (COG) and True Heading.** COG represents the path of vessel movement across the seabed, whereas heading indicates where the ship's bow is pointing. In heavy cross-currents, leeway, or towing operations, COG and heading diverge by dozens of degrees; confusing them distorts hydrodynamic analysis and collision risk calculations.

## Key takeaways

- **AIS is an unauthenticated tactical link, not a clean database.** Raw telemetry is flooded with multi-receiver duplicates, uninitialized factory-default identities, sentinel coordinates, and human entry errors that require comprehensive programmatic cleaning.
- **Syntactic validation must precede spatial processing.** Incoming streams must pass XOR checksum verification, 6-bit armor validation, fill-bit checks, and strict fragment reassembly keyed on receiver and sequence IDs.
- **Sentinels are explicit assertions of non-measurement.** Values such as Latitude $91^\circ$, Longitude $181^\circ$, SOG $102.3\text{ kn}$, and Heading $511$ must be converted directly to database `NULL` or `NaN` values rather than smoothed as numeric outliers.
- **Sort trajectories by reconciled message time, never ingest time.** Satellite downlinks introduce multi-hour transmission delays; sorting by database arrival time destroys trajectory continuity and triggers false kinematic violations.
- **Kinematic gating requires three-point velocity validation.** Isolate transient GPS spikes by comparing forward, backward, and baseline chord speeds against hydrodynamic thresholds ($40\text{ kn}$ for merchant vessels).
- **MMSI collisions require active track splitting.** Teleporting tracks caused by factory default MMSIs (`1193046`) or unprogrammed sequences (`123456789`) must be partitioned into independent spatial threads using kinematic gating and static identity matching.
- **Never interpolate blindly across land.** Trajectory interpolation must be bounded by maximum temporal thresholds and verified against high-resolution coastline polygons to prevent vessels from crossing dry land.
- **Voyage segmentation unlocks operational semantics.** Extract discrete voyages and cargo operations by combining spatio-temporal stop detection ($<200\text{ m}$ displacement over $>2\text{ hours}$) with high-precision marine berth and anchorage polygons.

## References

* Balduzzi, M., Pasta, A., Wilhoit, K. (2014). A security evaluation of AIS automated identification system. In *Proceedings of the 30th Annual Computer Security Applications Conference (ACSAC '14)*, pp. 436–445. doi:10.1145/2664243.2664257
* Banyś, P., Noack, T., Gewies, S. (2012). Assessment of AIS position-report reliability. *Annual of Navigation*, 19:5–16. doi:10.2478/v10367-012-0001-0
* Bošnjak, M., Šimunović, P., Kavran, Z. (2012). AIS error analysis in maritime traffic. *Transactions on Maritime Science*, 1(2):77–84. doi:10.7225/toms.v01.n02.002
* Douglas, D. H., Peucker, T. K. (1973). Algorithms for the reduction of the number of points required to represent a digitized line or its caricature. *Cartographica: The International Journal for Geographic Information and Geovisualization*, 10(2):112–122. doi:10.3138/FM57-6770-U75U-7727
* Emmens, G., Amrit, C., Abdi, R., Ghosh, B. (2021). The promises and perils of AIS data: A review of data-quality issues. *Expert Systems with Applications*, 178:114975. doi:10.1016/j.eswa.2021.114975
* Graser, A. (2019). MovingPandas: Efficient analysis of movement data in Python. *GI_Forum*, 7(1):54–68. doi:10.1553/giscience2019_01_s54
* Harati-Mokhtari, A., Wall, A., Brooks, P., Wang, J. (2007). Automatic Identification System (AIS): Data reliability and human error implications. *The Journal of Navigation*, 60(3):373–389. doi:10.1017/S0373463307004298
* IEC (2017). *Maritime navigation and radiocommunication equipment and systems — Class B shipborne equipment of the automatic identification system (AIS) — Part 1: Carrier-sense time division multiple access (CSTDMA) techniques*. IEC 62287-1:2017, Ed. 3.0. Geneva: International Electrotechnical Commission.
* IEC (2018). *Maritime navigation and radiocommunication equipment and systems — Automatic identification systems (AIS) — Part 2: Class A shipborne equipment of the automatic identification system (AIS) — Operational and performance requirements, methods of test and required test results*. IEC 61993-2:2018, Ed. 3.0. Geneva: International Electrotechnical Commission.
* IMO (2015). *Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems (AIS)*. Resolution A.1106(29). London: International Maritime Organization.
* Iphar, C., Ray, C., Napoli, A. (2020). On the evaluation of data integrity: Application to AIS data. *Expert Systems with Applications*, 147:113219. doi:10.1016/j.eswa.2020.113219
* ITU-R (2014). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile frequency band*. Recommendation ITU-R M.1371-5. Geneva: International Telecommunication Union.
* ITU-R (2019). *Assignment and use of identities in the maritime mobile service*. Recommendation ITU-R M.585-8. Geneva: International Telecommunication Union.
* Kessler, G. C., Craiger, J. P., Haass, J. C. (2018). A taxonomy of AIS vulnerabilities. *TransNav: International Journal on Marine Navigation and Safety of Sea Transportation*, 12(3):429–437. doi:10.12716/1001.12.03.01
* Kroodsma, D. A., Mayorga, J., Hochberg, T., Miller, N. A., Boerder, K., Ferretti, F., Wilson, A., Bergman, B., White, T. D., Block, B. A., Woods, P., Sullivan, B., Costello, C., Worm, B. (2018). Tracking the global footprint of fisheries. *Science*, 359(6378):904–908. doi:10.1126/science.aao5646
* Last, P., Bahlke, C., Hering-Bertram, M., Linsen, L. (2014). Comprehensive analysis of AIS data quality for movement prediction. *The Journal of Navigation*, 67(5):791–809. doi:10.1017/S0373463314000253
* Mazzarella, F., Vespe, M., Alessandrini, A., Tarchi, D., Aulicino, G., Vollero, A. (2017). A novel anomaly detection approach to identify intentional AIS on/off switching. *Expert Systems with Applications*, 78:110–123. doi:10.1016/j.eswa.2017.02.011
* NMEA (2018). *Standard for Interfacing Marine Electronic Devices*. NMEA 0183 Version 4.11. Severna Park, MD: National Marine Electronics Association.
* Paolo, F. S., Kroodsma, D., Raynor, J., Hochberg, T., Davis, P., Cleary, J., Marsaglia, L., Orofino, S., Thomas, C., Halpin, P. N. (2024). Satellite mapping reveals extensive industrial activity at sea. *Nature*, 625(7993):85–91. doi:10.1038/s41586-023-06825-8
* Welch, H., Clavelle, T., White, T. D., Cimino, M. A., Van Osdel, J., Hochberg, T., Kroodsma, D., Hazen, E. L. (2022). Hot spots of unseen fishing vessels. *Science Advances*, 8(44):eabq2109. doi:10.1126/sciadv.abq2109
