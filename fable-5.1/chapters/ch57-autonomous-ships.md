# Chapter 57 — AIS and autonomous/remotely operated ships (MASS)

> **Part VIII — Charts, bridge systems, and mariners.** How Maritime Autonomous Surface Ships (MASS) ingest, process, and broadcast AIS data, balancing cooperative situational awareness against unauthenticated cyber-physical liabilities.

**In this chapter.** You will learn how Maritime Autonomous Surface Ships (**MASS**) and Remote Operations Centres (**ROCs**) utilize the Automatic Identification System (**AIS**) within automated perception, navigation, and collision-avoidance pipelines. We analyze the four regulatory degrees of autonomy codified by the International Maritime Organization (**IMO**) and evaluate how AIS functions as an indispensable yet hazardous input for automated decision systems. You will examine the statutory obligations of MASS under SOLAS Chapter V, the emerging mandatory **MASS Code**, and the operational friction between **COLREGs** Rule 5 lookout requirements and digital sensor architectures. We dissect multi-sensor data fusion combining AIS, marine radar, LiDAR, and computer vision, demonstrating how unauthenticated broadcasts expose autonomy engines to ghost tracks, kinematic spoofing, and Denial of Service. You will review operational deployments including *Yara Birkeland* and the *Mayflower Autonomous Ship*, and inspect concrete verification and validation frameworks required to harden autonomous vessels against VHF Data Link (**VDL**) corruption.

## 57.1 Autonomy at sea: the IMO MASS framework and degrees of autonomy

Commercial shipping is transitioning from human bridge crews to algorithmically assisted, remotely supervised, and fully autonomous systems. Central to this is the regulatory concept of **Maritime Autonomous Surface Ships** (**MASS**), defined by the International Maritime Organization (**IMO**) as any ship which, to a varying degree, can operate independent of human interaction.

Following its Regulatory Scoping Exercise (**RSE**) approved at the 103rd session of the Maritime Safety Committee (**MSC.1/Circ.1638** in June 2021) and trial guidelines (**MSC.1/Circ.1604** in June 2019), the IMO established four non-hierarchical **degrees of autonomy**:

1. **Degree One — Automated processes and decision support:** Seafarers operate shipboard systems. Certain operations are automated, but crew remain ready to take control. Integrated bridge systems (**IBS**), adaptive autopilots, and ECDIS route-monitoring fall here.
2. **Degree Two — Remotely controlled ship with seafarers on board:** The vessel is operated from a shore-based **Remote Operations Centre** (**ROC**). Seafarers remain on board to take control during complex fairway transits.
3. **Degree Three — Remotely controlled ship without seafarers on board:** The vessel is operated entirely from an ROC without crew aboard. Navigation and machinery control are mediated over wireless data links.
4. **Degree Four — Fully autonomous ship:** The operating system makes decisions and executes actions autonomously without real-time human intervention.

```text
+-----------------------------------------------------------------------------------+
|                           IMO MASS Autonomy Framework                             |
+-------------------+--------------------+--------------------+---------------------+
|    Degree 1       |     Degree 2       |     Degree 3       |      Degree 4       |
| Decision Support  | Remote Control     | Remote Control     | Fully Autonomous    |
| (Crew Onboard)    | (Crew Onboard)     | (Uncrewed)         | (Uncrewed)          |
+-------------------+--------------------+--------------------+---------------------+
| Master on bridge; | ROC controls or    | ROC holds watch;   | Onboard AI system   |
| algorithms advise | monitors; crew     | no humans aboard;  | executes COLREGs;   |
| collision evasions| ready to take helm | sat/cellular link  | ROC fail-safe only  |
+-------------------+--------------------+--------------------+---------------------+
```

In every autonomy degree, situational awareness remains the decisive prerequisite for safe navigation. The shipboard system—or the shore-based remote operator—must construct a continuous spatial-temporal model of surrounding water space, identifying all physical obstacles, calculating closest points of approach (**CPA**) and time to closest point of approach (**TCPA**), and anticipating vessel trajectories.

Because AIS is mandated internationally under SOLAS Chapter V, Regulation 19 ([Chapter 1](ch01-what-ais-is.md)), it presents autonomy engineers with an attractive data source. Over the open VHF Data Link (**VDL**), commercial vessels exceeding 300 gross tonnage (**GT**) on international voyages broadcast their Global Navigation Satellite System (**GNSS**) coordinates, speed over ground (**SOG**), course over ground (**COG**), true heading (**HDG**), rate of turn (**ROT**), ship dimensions, identity, and destination ([Chapter 20](ch20-architecture-and-station-classes.md)). 

For an autonomous perception engine, decoding incoming AIS sentences provides immediate target identity, velocity vectors, and navigational status without requiring computationally intensive visual segmentation or radar track extraction. However, this convenience introduces a profound safety paradox: **AIS was designed as a cooperative, unauthenticated, broadcast protocol for human bridge officers who verify data by looking out the window.** When ingested raw by autonomous path planners, the unauthenticated nature of AIS transforms it from an operational aid into an existential vulnerability.

## 57.2 The dual role of AIS: perception asset versus algorithmic liability

In an automated navigation pipeline, AIS fulfills two distinct, mirror-image functions: **inbound perception** (listening to surrounding vessels to avoid collisions) and **outbound broadcast** (announcing the autonomous vessel's presence and intentions to the maritime community). Each role presents stark technical tradeoffs.

### 57.2.1 Inbound AIS as a perception input

Autonomous perception at sea requires range, all-weather resilience, and semantic identification. Marine radars detect reflective surfaces through precipitation, but echoes suffer sea clutter and multipath reflections ([Chapter 51](ch51-charts-enc-ecdis.md)). Optical and long-wave infrared (**LWIR**) cameras provide high-resolution classification but degrade in fog, rain, and darkness.

Inbound AIS bridges these physical sensor gaps:
- **Non-line-of-sight awareness:** At 161.975 MHz and 162.025 MHz, VHF signals diffract around islands and headlands. An autonomous vessel approaching a blind bend can track incoming traffic minutes before radar or cameras achieve line-of-sight.
- **Direct kinematic vectors:** Unlike radar Automatic Radar Plotting Aids (**ARPA**), which require 1 to 3 minutes of filtering to converge on a stable vector, AIS position reports (Messages 1, 2, and 3) broadcast instantaneous GNSS-derived SOG, COG, and heading at cadences down to 2 seconds ([Chapter 21](ch21-link-layer-tdma.md)).
- **Identity and dimensions:** AIS transmits Maritime Mobile Service Identity (**MMSI**), callsign, vessel name, and antenna offsets (Message 5), allowing path planners to model targets as oriented polygons with realistic turning radii.

### 57.2.2 Inbound AIS as an algorithmic liability

Despite these advantages, treating AIS as a trusted primary sensor in an autonomous control loop introduces acute operational failure modes:
1. **The Dark Vessel problem:** Non-mandatory vessels—including small fishing vessels under 15 m, recreational sailing craft, human-powered kayaks, military warships, and non-compliant commercial ships—do not broadcast AIS ([Chapter 6](ch06-fisheries-iuu-dark-fleets.md)). An autonomous system that conditions collision avoidance primarily on AIS will steam into a wooden fishing dory or fiberglass sailboat at cruising speed.
2. **Total lack of cryptographic authentication:** As codified in ITU-R M.1371-5, AIS broadcasts contain zero cryptographic signatures, message authentication codes, or session tokens. Any actor equipped with an inexpensive software-defined radio (**SDR**) can inject synthetic position reports claiming a non-existent 300 m container ship is bearing down on the autonomous vessel ([Chapter 59](ch59-spoofing.md)).
3. **Kinematic and configuration latency:** Static and voyage-related data (Message 5) is transmitted only once every 6 minutes, or upon request. Navigational status, draft, and vessel type are frequently misconfigured by human crews on manned ships ([Chapter 53](ch53-mariner-training.md)). Furthermore, Class B transponders update at significantly slower cadences (30 seconds to 3 minutes) using Carrier-Sense TDMA (**CSTDMA**), making fast-turning targets appear to lag their physical positions.
4. **GNSS corruption propagation:** If an external vessel experiences GNSS spoofing, ionospheric scintillation, or receiver failure, it faithfully broadcasts those erroneous coordinates across the VDL. An autonomous ship ingesting those broadcasts will compute phantom collision vectors against targets whose real physical positions are miles away.

> **Definitions that bite.** Sensor vs. Transmission. A marine radar or camera is an *independent physical sensor*: it collects objective physical measurements (electromagnetic reflections, photon flux) directly from the environment. An AIS transponder is a *cooperative communications terminal*: it receives unverified digital assertions broadcast by external parties about where they claim to be. Treating an AIS data stream as a physical sensor measurement in an autonomous world-model conflates telemetry with observation.

## 57.3 The MASS Code and SOLAS carriage obligations

The regulatory framework governing international commercial shipping is grounded in the International Convention for the Safety of Life at Sea (**SOLAS**), 1974. Under SOLAS Chapter V, Regulation 19.2.4:
> *All ships of 300 gross tonnage and upwards engaged on international voyages and cargo ships of 500 gross tonnage and upwards not engaged on international voyages and passenger ships irrespective of size shall be fitted with an automatic identification system (AIS).*

Furthermore, SOLAS Regulation V/19.2.4.7 stipulates that ships fitted with AIS shall maintain AIS in operation at all times, except where international agreements, rules, or standards provide for the protection of navigational information.

### 57.3.1 Class A transponder mandates for MASS

Flag administrations and classification societies (DNV, ABS, Lloyd's Register) affirm that autonomous cargo vessels within SOLAS thresholds must carry a type-approved **Class A transponder** meeting **IEC 61993-2** and **ITU-R M.1371** ([Chapter 20](ch20-architecture-and-station-classes.md)). Class B transponders are prohibited for commercial MASS under SOLAS. Class A guarantees 12.5 W transmission power (15–25 nmi coverage), SOTDMA link-layer access preventing preemption ([Chapter 21](ch21-link-layer-tdma.md)), mandatory sensor interfacing via IEC 61162 ([Chapter 26](ch26-interfaces-and-logging.md)), and reporting cadences down to 2 seconds.

```text
+-----------------------------------------------------------------------------------+
|               Class A Transceiver Integration on an Uncrewed MASS                 |
+-----------------------------------------------------------------------------------+
|   +-----------------------+     +-----------------------+                         |
|   | Dual Antenna GNSS /   |     | Primary Gyrocompass / |                         |
|   | Inertial Navigation   |     | Fiber-Optic Gyro (FOG)|                         |
|   +-----------+-----------+     +-----------+-----------+                         |
|               |                             |                                     |
|               | RMC / GNS / GBS (10 Hz)     | HDT / THS (50 Hz)                   |
|               v                             v                                     |
|       +---------------------------------------------+                             |
|       |         IEC 61993-2 Type-Approved           |                             |
|       |           Class A AIS Transceiver           |                             |
|       +----------------------+----------------------+                             |
|                              |                                                    |
|                              | IEC 61162-450 (Lightweight Ethernet)               |
|                              | Sentences: !AIVDM, !AIVDO, $AIVSI                  |
|                              v                                                    |
|       +---------------------------------------------+                             |
|       |        Autonomous Navigation Computer       |                             |
|       |  - World Model & Multi-Sensor Fusion Engine |                             |
|       |  - Kinematic Track Validation               |                             |
|       |  - Fail-Safe Watchdog & Telemetry Gateway   |                             |
|       +----------------------+----------------------+                             |
|                              |                                                    |
|                              | High-Throughput Satcom (LEO/GEO) + 4G/5G           |
|                              v                                                    |
|       +---------------------------------------------+                             |
|       |        Shore Remote Operations Centre       |                             |
|       |  - Synthetic Bridge & Video Display         |                             |
|       |  - Certified Remote Master Watchstation     |                             |
|       +---------------------------------------------+                             |
+-----------------------------------------------------------------------------------+
```

### 57.3.2 The draft IMO MASS Code

To harmonize national trials, the IMO Maritime Safety Committee developed the **International Code of Safety for Maritime Autonomous Surface Ships (MASS Code)**. Finalized as a non-mandatory code at MSC 108 in May 2024 (effective July 2026, targeting mandatory SOLAS status by 2028–2030), the code mandates:
- **Continuous digital situational awareness:** Systems must detect and track all entities and hazards, with AIS formally recognized as a contributing stream.
- **Fail-safe operational states:** Upon sensor degradation or link loss, vessels must enter a **Minimum Risk Condition** (**MRC**), updating broadcasted AIS navigational status to signal degradation.
- **Interface integrity:** Systems must secure bidirectional data integrity between transponders and the ROC against unauthorized manipulation.

### 57.3.3 The Navigational Status dilemma

A persistent operational hurdle under the current ITU-R M.1371 standard is the 4-bit **Navigational Status** field broadcast in Message 1, 2, and 3 ([Chapter 22](ch22-message-catalog.md)). The field accommodates values 0 through 15:
`0` (Under way using engine), `1` (At anchor), `2` (Not under command, **NUC**), `3` (Restricted manoeuvrability, **RAM**), `4` (Constrained by draught), `5` (Moored), `6` (Aground), `7` (Engaged in fishing), `8` (Under way sailing), `9–13` (Reserved for future amendment / regional use), `14` (AIS-SART / MOB / EPIRB active), `15` (Undefined / default).

Crucially, **there is currently no internationally standardized AIS navigational status code for "Autonomous Vessel" or "Uncrewed Vessel under Remote Operation."**

During initial commercial trials, operators of vessels like *Yara Birkeland* faced a dilemma:
- If they broadcast status `0` (*Under way using engine*), conventional vessels assume a human bridge team is maintaining visual watchkeeping and listening on VHF Channel 16.
- If they broadcast status `2` (*Not under command*), they invoke Rule 27 of the International Regulations for Preventing Collisions at Sea (**COLREGs**), which grants absolute right-of-way over ordinary power-driven vessels. Maritime administrations have firmly rejected the notion that routine autonomous operation constitutes an exceptional disabling condition warranting NUC privilege.

Pending future ITU Radiocommunication Sector (**ITU-R**) revisions to Recommendation M.1371, national administrations require autonomous vessels to broadcast status `0` (*Under way using engine*) while broadcasting explicit autonomous trial identifiers via AIS Application-Specific Messages (**ASMs**) or free-text Message 14 safety-related broadcasts ([Chapter 22](ch22-message-catalog.md)).

## 57.4 COLREGs compliance and the Rule 5 challenge

The core regulatory friction surrounding autonomous ships centers on the **International Regulations for Preventing Collisions at Sea, 1972** (**COLREGs**). Specifically, **Rule 5 (Look-out)** dictates:
> *"Every vessel shall at all times maintain a proper look-out by sight and hearing as well as by all available means appropriate in the prevailing circumstances and conditions so as to make a full appraisal of the situation and of the risk of collision."*

For over five decades, maritime admiralty courts have interpreted Rule 5 as an uncompromising requirement for competent human sensory perception—human eyes peering through bridge windows and human ears listening for fog signals, sound blasts, and VHF transmissions.

```text
+-----------------------------------------------------------------------------------+
|                        COLREG Rule 5: Human vs. MASS                              |
+------------------------------------+----------------------------------------------+
|     Traditional Bridge Watch       |         Autonomous Sensor Array              |
+------------------------------------+----------------------------------------------+
| Sight: Human eyes on bridge wings  | Multi-spectral: 360° 4K EO/LWIR Cameras      |
| Hearing: Human ears on open bridge | Acoustic array: Calibrated microphones       |
| Radar: Watch officer plots ARPA    | Digital radar: Native raw target extraction  |
| AIS: MKD / ECDIS target display    | AIS: Direct VDL packet parsing into fusion   |
| Seamanship: Intuitive appraisal    | Algorithms: Deterministic COLREG rule engine |
+------------------------------------+----------------------------------------------+
```

In an uncrewed Degree 3 or Degree 4 MASS, compliance with Rule 5 must be achieved through an algorithmic equivalent:
1. **"By sight":** Replaced by high-resolution electro-optical (**EO**) cameras, thermal long-wave infrared (**LWIR**) cameras, and LiDAR point clouds.
2. **"By hearing":** Replaced by calibrated, omnidirectional digital microphone arrays mounted on the masthead, running acoustic signal processing to detect and triangulate sound signals (such as one prolonged blast every 2 minutes in fog under Rule 35).
3. **"By all available means appropriate":** This clause explicitly legitimizes the incorporation of marine radar and **AIS**.

In automated collision-avoidance engines, incoming AIS tracks feed directly into deterministic or probabilistic trajectory planners. The algorithm categorizes every encounter under COLREGs Part B:
- **Rule 13 (Overtaking):** Any vessel approaching from more than 22.5° abaft the beam. AIS provides relative bearing, SOG, and COG vectors to determine overtaking geometry unambiguously.
- **Rule 14 (Head-on situation):** Two power-driven vessels meeting on reciprocal courses involving risk of collision. The algorithm evaluates reciprocal heading lines and near-zero relative bearing.
- **Rule 15 (Crossing situation):** When two power-driven vessels are crossing so as to involve risk of collision, the vessel which has the other on her own starboard side shall keep out of the way.

Under Rules 16 (Action by give-way vessel) and 17 (Action by stand-on vessel), the autonomous ship must execute maneuvers that are large enough to be readily apparent to another vessel observing visually or by radar (Rule 8(b)).

Here, AIS plays a crucial dual role. First, the autonomous ship monitors the target's broadcasted Rate of Turn (**ROT**) in Message 1, 2, or 3. If a target begins an evasive maneuver, its ROT field changes instantaneously—seconds before radar ARPA can detect an angular course alteration. Second, the autonomous vessel's own course alteration is broadcast immediately across the VDL via its Class A transponder, signaling its compliance to the target vessel's bridge watch.

> **Rule of thumb.** Rate of Turn (ROT) latency in automation. An autonomous path planner should never rely solely on ARPA filtering to detect when a stand-on vessel takes emergency action. AIS ROT reports provide angular turning acceleration within 2.0 seconds of rudder movement, compared to 30–60 seconds for radar tracker convergence. However, if the target's AIS heading is derived from an uncalibrated fluxgate compass rather than a certified gyro, the ROT field will broadcast noisy oscillation; always cross-verify ROT against multi-frame optical or radar bearing drift.

## 57.5 Multi-sensor data fusion: AIS, radar, LiDAR, and computer vision

Because no single sensor provides total reliability across all maritime environments, autonomous surface vessels deploy **multi-sensor data fusion** (**MSDF**) architectures. The system ingests disparate sensor streams, each characterized by distinct spatial accuracy, refresh rates, noise distributions, and failure modes, synthesizing them into a unified, coherent **world-model**.

```text
+-----------------------+     +-----------------------+     +-----------------------+     +-----------------------+
|   Class A Transceiver |     | Marine Radar (X/S)    |     | 3D LiDAR Array        |     | Optical / LWIR Cameras|
|   (ITU-R M.1371 VDL)  |     | (ARPA / Raw Video)    |     | (Solid-state / Mech)  |     | (360° Panoramic EO/IR)|
+-----------+-----------+     +-----------+-----------+     +-----------+-----------+     +-----------+-----------+
            |                             |                             |                             |
            | NMEA 0183 / IEC 61162       | ASTERIX Cat 240 / NMEA      | Point Cloud (Ethernet)      | RTSP / GigE Vision    |
            v                             v                             v                             v
+-----------------------------------------------------------------------------------------------------------------+
|                                     Sensor Preprocessing & Track Extraction                                     |
|  - AIS Parser & Validator           - CFAR Detection & Tracking   - Point Cloud Clustering      - CNN Object Detector   |
|  - Kinematic plausibility check     - Target extraction (ARPA)    - Bounding-box extraction     - Bounding-box & class  |
+-------------------------------------+-----------------------------+-----------------------------+-----------------------+
                                          |                             |                             |
                                          +---------------------+       |       +---------------------+
                                                                |       |       |
                                                                v       v       v
+-----------------------------------------------------------------------------------------------------------------+
|                                          Spatial-Temporal Coordinate Alignment                                  |
|  - Lever-arm compensation (antenna vs. sensor physical baseline offsets via SE(3) transforms)                   |
|  - Time-stamping & latency synchronization (PTP IEEE 1588 / GNSS PPS clock)                                    |
+-----------------------------------------------------------------+-----------------------------------------------+
                                                                  |
                                                                  v
+-----------------------------------------------------------------------------------------------------------------+
|                                     Track Association & Gating Engine                                           |
|  - Global Nearest Neighbor (GNN) / Joint Probabilistic Data Association (JPDA)                                 |
|  - Mahalanobis distance validation gates across state vectors [x, y, vx, vy]^T                                  |
+-----------------------------------------------------------------+-----------------------------------------------+
                                                                  |
                                                                  v
+-----------------------------------------------------------------------------------------------------------------+
|                                   Multi-Hypothesis Extended Kalman Filter (EKF)                                 |
|  - State estimation: Position, SOG, COG, Heading, ROT, Extent Dimensions                                       |
|  - Track confidence scoring & sensor cross-validation                                                           |
+-----------------------------------------------------------------+-----------------------------------------------+
                                                                  |
                                                                  v
+-----------------------------------------------------------------------------------------------------------------+
|                                 Unified World Model & COLREGs Decision Engine                                   |
|  - Target classification (Verified Manned, Unverified AIS, Non-AIS Radar Obstacle, Debris)                      |
|  - CPA / TCPA calculations & COLREG encounter classification (Head-on, Crossing, Overtaking)                   |
|  - Path generation & autonomous collision-avoidance maneuver execution                                          |
+-----------------------------------------------------------------+-----------------------------------------------+
```

### 57.5.1 Spatial-temporal coordinate alignment and gating

Every sensor on an autonomous vessel operates in its own local coordinate reference frame:
- The AIS Class A transponder references the vessel's primary GNSS antenna position.
- Radars measure target range and azimuth relative to the radar scanner center.
- Cameras and LiDARs measure angular line-of-sight and point clouds in camera coordinate frames.

To fuse these inputs, the system applies rigid-body spatial transformations ($\mathbf{p}_{\text{ship}} = \mathbf{R}_{\text{sensor}} \mathbf{p}_{\text{local}} + \mathbf{t}_{\text{sensor}}$), where $\mathbf{R}_{\text{sensor}}$ is the 3D rotation matrix accounting for sensor boresight misalignment, and $\mathbf{t}_{\text{sensor}}$ is the lever-arm translation vector relative to the common reference point (**CRP**).

Concurrently, Precision Time Protocol (**PTP**, IEEE 1588) synchronized to GNSS pulse-per-second (**PPS**) timing aligns asynchronous sensor streams. When an AIS position report arrives, the perception engine determines whether it associates with an active radar or optical track using **validation gating**. A spatial gate based on the **Mahalanobis distance** ($d_M$) is evaluated:
$$d_M^2 = \mathbf{y}^T (\mathbf{H}\mathbf{P}\mathbf{H}^T + \mathbf{R})^{-1} \mathbf{y}$$
where $\mathbf{y} = \mathbf{z} - \mathbf{H}\mathbf{x}$ is the innovation vector, $\mathbf{P}$ is state covariance, and $\mathbf{R}$ is measurement covariance. If $d_M^2$ falls below a chi-square threshold ($\chi^2_{\alpha, m}$), the measurement updates the track state in an **Extended Kalman Filter** (**EKF**). Radar provides range accuracy, while AIS contributes identity, heading, and ROT.

## 57.6 Threat model: AIS exploitation against autonomous perception

Because an uncrewed ship lacks human bridge watchstanders to look through binoculars, the automation engine is singularly vulnerable to digital spoofing and radio frequency interference.

> **Threat model.**
> - **Attacker:** Malicious actors ranging from commercial competitors, smugglers, and pirates to electronic warfare units and rogue hobbyists equipped with $50 software-defined radios (HackRF, RTL-SDR transmit-capable mods, bladeRF).
> - **Capability:** Transmission of arbitrary RF waveforms on AIS 1 (161.975 MHz) and AIS 2 (162.025 MHz); generation of synthetically valid ITU-R M.1371 bit payloads; GPS/GNSS jamming and spoofing in L1/E1 bands; local VHF Data Link slot starvation.
> - **Impact:** Induction of phantom collision evasions causing grounding or fairway blockage; blinding of autonomous collision avoidance; forced fallback into emergency minimum risk states; hijacking of path-planning logic to steer vessels off-course.
> - **Mitigation:** Mandatory multi-sensor gating; rejection of AIS targets lacking corroborating physical radar echoes or optical detections within line-of-sight; kinematic plausibility filtering; Doppler and physical-layer RF fingerprinting; GNSS RAIM and multi-constellation validation.

```text
+-----------------------------------------------------------------------------------+
|                        Spoofing Attack Vector on MASS                             |
+-----------------------------------------------------------------------------------+
|    +------------------------+                                                     |
|    | Attacker SDR Transmit  | --> Synthesizes Msg 1/2/3 "Ghost Vessel" (CPA = 0)  |
|    +-----------+------------+                                                     |
|                |                                                                  |
|                v Ingests raw !AIVDM string                                        |
|    +------------------------+                                                     |
|    | MASS Class A Receiver  |                                                     |
|    +-----------+------------+                                                     |
|                |                                                                  |
|         +------+--------------------------------------------------+               |
|         |                                                         |               |
|         v                                                         v               |
|   +------------------------------------+    +---------------------------------+   |
|   | PATH A: Unhardened Autonomy Engine |    | PATH B: Hardened Fusion Engine  |   |
|   | - Accepts AIS position as truth    |    | - Checks Radar: No echo at range|   |
|   | - Detects imminent head-on collision|   | - Checks Vision: Zero visual mass|  |
|   | - Executes violent starboard turn  |    | - Rejects target from planner   |   |
|   |   --> RESULT: Vessel runs aground  |    |   --> RESULT: Maintains fairway |   |
|   +------------------------------------+    +---------------------------------+   |
+-----------------------------------------------------------------------------------+
```

### 57.6.1 Specific AIS attack vectors against MASS

1. **Ghost Target Injection:** An attacker transmits synthetic Messages 1, 2, or 3 representing a phantom ship on reciprocal course (CPA = 0, TCPA < 3 min). An unhardened planner executes emergency evasion, potentially running aground on fairway shoals.
2. **Kinematic Teleportation and Velocity Manipulation:** An attacker broadcasts a valid MMSI with an impossible 102 kn speed or abrupt coordinate jumps. Without Kalman innovation gating, the tracker diverges, destabilizing the perception pipeline.
3. **Navigational Status Manipulation:** An attacker transmits status `1` (*At anchor*) or `5` (*Moored*) for an approaching ship, tricking naive rule engines into demoting collision urgency.
4. **VHF Data Link Slot Starvation (DoS):** High-power burst transmissions over 161.975/162.025 MHz saturate the 2,250-slot SOTDMA frame ([Chapter 21](ch21-link-layer-tdma.md)), blinding transponders and forcing vessels into fail-safe stops.
5. **Base Station Message 22/23 Spoofing:** Spoofed base stations issue channel switches (Message 22) or quiet-time commands (Message 23) ([Chapter 22](ch22-message-catalog.md)), silencing fairway broadcasts.

## 57.7 Remote Operations Centres (ROCs) and bandwidth constraints

For Degree 2 and Degree 3 MASS, operational responsibility is centered in the **Remote Operations Centre** (**ROC**). The ROC houses human master mariners and remote watchstanders who supervise autonomous voyages, intervene during complex berthing maneuvers, or assume direct teleoperation when onboard algorithms request assistance.

```text
+-----------------------------------------------------------------------------------+
|                        ROC Data Pipeline & Telemetry Tiering                      |
+-----------------------------------------------------------------------------------+
|   MASS Shipboard Network                                                          |
|   - Raw Sensors: Radar (100 Mbps) | 4K Cameras (40 Mbps) | AIS (38.4 kbps)        |
|                                         |                                         |
|                                         v                                         |
|   Onboard Compression & Edge Perception Engine                                    |
|   - Executes local sensor fusion and COLREGs obstacle avoidance                   |
|   - Extracts compact target metadata: [ID, Type, Lat, Lon, SOG, COG, Conf]        |
|                                         |                                         |
|                        Satcom / Coastal 4G/5G Wireless Link                       |
|                   (Bandwidth: 128 kbps – 20 Mbps; Latency: 250–1200 ms)           |
|                                         |                                         |
|                                         v                                         |
|   Shore Remote Operations Centre (ROC)                                            |
|   - High Priority: Compressed AIS Target Stream & Radar Vectors (~64 kbps)        |
|   - Medium Priority: Compressed Keyframe Video Bounding Boxes (~256 kbps)         |
|   - On-Demand: Full-Resolution Video Stream (Restricted to Teleoperation)         |
|                                         |                                         |
|                                         v                                         |
|   Synthetic Bridge Display (ECDIS + 360° Augmented Reality Projection)            |
|   - Renders validated AIS targets with radar-verified confidence rings            |
+-----------------------------------------------------------------------------------+
```

While raw AIS traffic over the VDL is remarkably lightweight—transmitting at 9,600 bps over the radio link, generating roughly 38.4 kbps on the shipboard NMEA serial bus—transmitting raw radar video and multi-camera 4K optical streams over satellite communication (**satcom**) links requires 50 to 150 Mbps of bandwidth.

Over maritime satellite constellations (such as Inmarsat Fleet Xpress, Iridium Certus, or Starlink Maritime), satellite uplink bandwidth is subject to rain fade, mast blockage during vessel roll, and severe latency variations (from 40 ms in Low Earth Orbit to 600–1,200 ms in Geostationary Orbit).

Consequently, the ROC situational awareness pipeline relies on **edge-computed target metadata**:
1. The autonomous ship's onboard perception engine fuses raw radar, optical, and AIS streams locally on shipboard server racks.
2. Instead of streaming raw video, the vessel transmits compressed target state vectors ($\mathbf{T}_k = [\text{Target ID}, \text{MMSI}, \text{Lat}, \text{Lon}, \text{SOG}, \text{COG}, \text{HDG}, \text{Confidence}]$).
3. In the ROC, the synthetic bridge workstation recreates the external world on an electronic chart display, projecting target icons and vector predictors directly onto the operator's screens.
4. Raw video is down-sampled to low-frame-rate keyframes, streaming full-bandwidth video only when the remote master initiates direct manual maneuvering.

Because AIS data is already structured, highly compressed, and universally standardized via IEC 61162 sentences, it serves as the ultimate low-bandwidth fallback: even if severe satellite degradation cuts uplink bandwidth to 64 kbps, the complete AIS traffic picture surrounding the autonomous ship continues to stream reliably to the shore operator.

## 57.8 Operational deployments and research platforms

The theoretical principles of MASS operation have been validated across several pioneering commercial and research platforms.

### 57.8.1 Yara Birkeland

Commissioned in Norway in 2021 for service between Horten, Larvik, and Brevik, **Yara Birkeland** (IMO 9865049) is the world's first fully electric commercial autonomous container ship (LOA 80 m, beam 15 m, 3,200 DWT, 120 TEU).
- **Sensors:** Kongsberg Maritime suite with dual X/S-band radars, 360° optical/infrared cameras, LiDARs, and dual Class A AIS transponders.
- **Operations:** Progressed from manned trials (Degree 1) to uncrewed shore monitoring (Degree 3) via the Massterly ROC in Horten.
- **AIS integration:** Inbound AIS targets are cross-checked against optical and radar tracking gates. Outbound AIS transmits route progress to VTS Brevik and coastal shipping.

### 57.8.2 Mayflower Autonomous Ship (MAS400)

Developed by ProMare with IBM and MarineAI, the **Mayflower Autonomous Ship** (**MAS400**) is a 15 m autonomous research trimaran powered by solar-hybrid propulsion.
- **Architecture:** Edge-computed "AI Captain" running IBM ODM rule engines for deterministic COLREGs compliance.
- **Transatlantic achievement:** In June 2022, MAS400 crossed the Atlantic autonomously from Plymouth, UK, to Halifax and Plymouth, Massachusetts.
- **AIS role:** A Class A transponder served as a primary non-line-of-sight sensor alongside solid-state radar and cameras. In mid-ocean transits with constrained satellite uplinks, onboard AIS parsing drove autonomous COLREGs collision avoidance.

> **Case file.** In 2022, during the transatlantic deployment of the *Mayflower Autonomous Ship*, the AI Captain encountered multiple vessels in the open North Atlantic whose AIS broadcasts exhibited substantial positional latency and unflagged course changes. In several instances, Class B-equipped sailing yachts broadcast position updates at erratic intervals due to wave shadowing on their low-mounted VHF antennas. The AI Captain's multi-sensor fusion engine maintained track continuity by using marine radar returns to propagate target positions across AIS reception dropouts, preventing false-alarm evasive course alterations.

## 57.9 Digital route exchange and cooperative intent (S-421 and VDES)

As autonomous navigation advances toward higher degrees of autonomy, the maritime community is moving beyond passive target tracking toward **cooperative intent exchange**. 

Under conventional VHF radio procedures, watch officers resolve ambiguous collision risks by calling surrounding ships by name over VHF Channel 16 or 13, verbally negotiating a passing arrangement ("passing port-to-port"). For an uncrewed ship, voice radiotelephony is deeply problematic: natural language processing of heavily accented, static-filled VHF audio is prone to catastrophic misinterpretation.

```text
+-----------------------------------------------------------------------------------+
|               Evolution of Intent Exchange: From Voice to S-421                   |
+-----------------------------------------------------------------------------------+
|  Legacy AIS Broadcast (Current)                                                   |
|  - Transmits instantaneous kinematics: Lat, Lon, SOG, COG, Heading                |
|  - Encodes ZERO intent: Where is the ship turning 2 minutes from now?             |
|  - Surrounding ships must infer intentions from past track history                |
|                                         |                                         |
|                                         v                                         |
|  S-421 Digital Route Exchange via VDES (Future Standard)                          |
|  - Ship broadcasts planned trajectory: Next 4 to 8 waypoints with arrival times   |
|  - Formatted under IEC 63173-1 / S-100 data framework                             |
|  - Autonomous collision engines negotiate non-conflicting trajectories digitally  |
+-----------------------------------------------------------------------------------+
```

To solve this, international standards organizations have developed digital route-exchange frameworks:
- **IEC 63173-1 (S-421):** *Maritime Navigation and Radiocommunication Equipment and Systems – Data Interfaces – Part 1: S-421 Route Plan Based on S-100*. Standardizes XML and binary representation of complete voyage route plans, including scheduled waypoints, leg speeds, turn radii, and cross-track limits (**XTL**).
- **VHF Data Exchange System (VDES):** Codified in Recommendation ITU-R M.2092 ([Chapter 69](ch69-vdes-ais-2.md)), VDES incorporates legacy AIS while adding wideband **VDE-Terrestrial** and **VDE-Satellite** channels operating at bandwidths up to 100 kHz.

Using VDES and S-421, an autonomous ship does not merely broadcast where it is now; it broadcasts its planned trajectory for the next 15 minutes. Nearby autonomous and manned vessels ingest this route plan directly into their ECDIS and navigation computers. When two ships detect a future trajectory conflict, their algorithms execute an automated digital handshake, computing mutually optimal, COLREGs-compliant passing maneuvers without uttering a single word over VHF radio.

> **Legal note.**
> Under international maritime law, broadcasted route plans (S-421) and digital passing negotiations do **not** supersede the statutory obligations of the COLREGs. An autonomous ship broadcasting an intended turning maneuver remains strictly bound by COLREG Rules 16 and 17 as the give-way or stand-on vessel. If an external vessel fails to acknowledge or comply with a negotiated digital passing agreement, the autonomous ship must revert instantly to standard COLREGs rules of good seamanship.

## Then & now

How situational awareness, collision avoidance, and tracking technologies for uncrewed craft evolved over the last century:

- ⟨H⟩ 1898 — Nikola Tesla demonstrates the world's first radio-controlled unmanned boat (*teleautomaton*) in Madison Square Garden, using coherent radio pulses to control rudder and propeller.
- ⟨H⟩ 1904 — Christian Hülsmeyer patents the *Telemobiloskop*, the spark-gap forerunner of marine radar, detecting remote metallic ships to prevent collisions in fog.
- ⟨H⟩ 1944 — First operational deployment of radio-guided uncrewed explosive boats (German *Linse* and Allied drone craft) during World War II.
- ⟨H⟩ 1970 — First commercial automated radar plotting aids (**ARPA**) deployed on commercial ships, providing automated vector calculations for tracked radar targets.
- ⟨+⟩ 1998 — IMO adopts Resolution MSC.74(69), establishing international performance standards for universal AIS, specifying autonomous and continuous operation across the maritime VHF band.
- ⟨+⟩ 2012 — European Union MUNIN (Maritime Unmanned Navigation through Intelligence in Networks) research project commences, establishing the earliest comprehensive technical architecture for uncrewed autonomous merchant ships.
- ⟨+⟩ 2014 — Marco Balduzzi, Alessandro Pasta, and Kyle Wilhoit publish the first systematic security evaluation of AIS at ACSAC, demonstrating trivial spoofing of ghost ships, AtoNs, and synthetic CPA alerts using software-defined radios (Balduzzi, Pasta and Wilhoit 2014).
- ⟨+⟩ 2017 — Rolls-Royce and Svitzer demonstrate the world's first remotely operated commercial tug (*Svitzer Hermod*) in Copenhagen harbour, utilizing sensor fusion and shore-based teleoperation.
- ⟨+⟩ 2018 — IMO Maritime Safety Committee initiates the formal Regulatory Scoping Exercise (**RSE**) for Maritime Autonomous Surface Ships (MASS) at MSC 99.
- ⟨+⟩ 2019 — IMO approves MSC.1/Circ.1604, establishing *Interim Guidelines for MASS Trials*, governing flag-state authorization and safety assessments for autonomous operations.
- ⟨+⟩ 2021 — IMO completes its Regulatory Scoping Exercise with the publication of MSC.1/Circ.1638, categorizing SOLAS, STCW, and COLREGs provisions across four degrees of autonomy.
- ⟨+⟩ 2021 — *Yara Birkeland*, the world's first fully electric commercial container ship designed for autonomous operations, enters service in Norwegian coastal waters.
- ⟨+⟩ 2022 — The *Mayflower Autonomous Ship* (MAS400) completes an autonomous transatlantic crossing using IBM's AI Captain, navigating with multi-sensor fusion combining AIS, radar, and optical vision.
- ⟨+⟩ 2024 — IMO Maritime Safety Committee (MSC 108) finalizes the draft text of the non-mandatory MASS Code, setting goal-based functional requirements for remote operations centres, digital situational awareness, and automated fail-safe states.
- ⟨+⟩ 2026 — Entry into force of the non-mandatory IMO MASS Code, establishing the baseline international regulatory framework for commercial autonomous ship trials and type-approval certification.

## Validation, uncertainty & data quality

In an autonomous navigation system, the validation and verification of inbound AIS data streams is a safety-critical function. Ingesting unvalidated AIS reports into path-planning algorithms can cause phantom collision maneuvers or blind the vessel to legitimate traffic.

### Concrete validation pipeline

An autonomous vessel's perception pipeline must subject every decoded IEC 61162 `!AIVDM` sentence to five sequential validation gates before admitting the track into the multi-sensor fusion matrix:

1. **Syntactic and checksum verification:** The sentence must possess valid NMEA 0183 / IEC 61162 encapsulation, correct field delimiters, and a passing XOR payload checksum. Corrupted characters or framing errors immediately discard the packet.
2. **Identity plausibility:** The 30-bit MMSI is checked against ITU Radio Regulations Article 19:
   - Valid standard mobile MMSI format: $200000000 \le \text{MMSI} \le 799999999$.
   - Flag and isolate test/bogus identities: `000000000`, `111111111`, `123456789`, `999999999`.
   - Identify station class from MMSI prefix: coastal stations ($00MIDxxxx$), SAR aircraft ($111MIDxxx$), AIS Aids to Navigation ($99MIDxxxx$), and Autonomous Maritime Radio Devices ($972xxxxxx$ per ITU-R M.2135).
3. **Spatial-temporal bounding:** Coordinates must fall within legitimate geographic limits ($-90.0^\circ \le \text{lat} \le +90.0^\circ$ and $-180.0^\circ \le \text{lon} \le +180.0^\circ$). Sentinel default values indicating unavailable coordinates (`lat = 91.0`, `lon = 181.0`) must be segregated. The timestamp field must fall within $\pm 60\text{ s}$ of local UTC to detect stale replayed messages.
4. **Kinematic plausibility filtering:** The state delta between consecutive fixes $(\mathbf{p}_{k-1}, t_{k-1})$ and $(\mathbf{p}_k, t_k)$ is evaluated against physical hydrodynamic caps:
   - **Implied velocity check:** The implied velocity over ground $v_{\text{implied}} = \Delta d / \Delta t$ must not exceed physical vessel limits ($45\text{ kn}$ for commercial cargo/tanker vessels, $60\text{ kn}$ for fast ferries/craft).
   - **Velocity consistency:** The absolute difference between reported SOG and implied speed $|v_{\text{implied}} - \text{SOG}_{\text{reported}}|$ must not exceed $5.0\text{ kn}$.
   - **Rate of Turn plausibility:** Turn rate must not exceed $\Delta \text{COG} / \Delta t \le 10.0^\circ/\text{s}$.
   - **Teleportation detection:** Any positional jump $\Delta d > 1.0\text{ nmi}$ over an elapsed interval $\Delta t < 60\text{ s}$ flags the track as an anomalous teleportation event.
5. **Multi-sensor physical corroboration:** An AIS target whose calculated range falls within the instrumented horizon of onboard physical sensors (marine radar and optical vision) must be corroborated by physical measurements. If an AIS target claims to be within 2.0 nmi, yet dual marine radars (CFAR threshold tuned for low radar cross-section) and thermal cameras detect zero physical mass, the track is assigned an unverified confidence score ($C_{\text{track}} < 0.2$) and suppressed from triggering emergency evasive course changes.

```text
+-----------------------------------------------------------------------------------+
|                        Kinematic Plausibility Logic                               |
+-----------------------------------------------------------------------------------+
|   New Position Fix (t_k, Lat_k, Lon_k, SOG_k, COG_k)                              |
|                          |                                                        |
|                          v                                                        |
|   Compute Haversine distance: Delta_d = dist(p_{k-1}, p_k)                        |
|   Compute Elapsed time:       Delta_t = t_k - t_{k-1}                             |
|   Compute Implied Speed:      v_implied = Delta_d / Delta_t                       |
|                          |                                                        |
|         +----------------+----------------+                                       |
|         |                                 |                                       |
|         v                                 v                                       |
|   [v_implied > 45 kn]           [Delta_d > 1.0 nmi AND Delta_t < 60 s]            |
|         |                                 |                                       |
|         v                                 v                                       |
|   FLAG: Speed Violation         FLAG: Teleportation Jump                          |
|         |                                 |                                       |
|         +----------------+----------------+                                       |
|                          |                                                        |
|                          v                                                        |
|   Calculate Anomaly Score: S = sum(Flags)                                         |
|   IF S >= 2: Quarantine track, alert ROC, require radar corroboration             |
+-----------------------------------------------------------------------------------+
```

### Worked numerical validation example

Consider an uncrewed MASS vessel navigating coastal waters. At time $t_0 = 12:00:00\text{ UTC}$, an incoming Class A AIS message reports a target vessel at:
$$\mathbf{p}_0 = (42.3500^\circ\text{ N}, 070.9000^\circ\text{ W}), \quad \text{SOG}_0 = 12.0\text{ kn}, \quad \text{COG}_0 = 090.0^\circ$$

At time $t_1 = 12:00:15\text{ UTC}$ ($\Delta t = 15\text{ s} = 0.004167\text{ h}$), a subsequent message arrives with the same MMSI reporting:
$$\mathbf{p}_1 = (42.3580^\circ\text{ N}, 070.8800^\circ\text{ W}), \quad \text{SOG}_1 = 12.5\text{ kn}, \quad \text{COG}_1 = 090.0^\circ$$

The latitudinal and longitudinal displacements are:
$$\Delta \phi = 42.3580^\circ - 42.3500^\circ = +0.0080^\circ = 0.48\text{ nmi} \quad (889\text{ m})$$
$$\Delta \lambda = 070.8800^\circ - 070.9000^\circ = +0.0200^\circ$$
Accounting for mean latitude $\phi_m = 42.354^\circ$:
$$\Delta d_{\text{lon}} = \Delta \lambda \cdot \cos(\phi_m) \cdot 60 = 0.0200 \cdot 0.73898 \cdot 60 = 0.8868\text{ nmi} \quad (1,642\text{ m})$$
Total geographic distance:
$$\Delta d = \sqrt{(0.48)^2 + (0.8868)^2} = \sqrt{0.2304 + 0.7864} = \sqrt{1.0168} = 1.0084\text{ nmi} \quad (1,867.5\text{ m})$$

Now, compute the implied speed over ground:
$$v_{\text{implied}} = \frac{\Delta d}{\Delta t} = \frac{1.0084\text{ nmi}}{0.004167\text{ h}} = 242.0\text{ kn} \quad (448.2\text{ km/h})$$

Evaluating against validation criteria:
1. **Speed cap violation:** $v_{\text{implied}} = 242.0\text{ kn} > 45.0\text{ kn}$ (Violation flag triggered).
2. **SOG mismatch:** $|v_{\text{implied}} - \text{SOG}_{\text{reported}}| = |242.0 - 12.5| = 229.5\text{ kn} > 5.0\text{ kn}$ (Violation flag triggered).
3. **Teleportation check:** $\Delta d = 1.0084\text{ nmi} > 1.0\text{ nmi}$ in $\Delta t = 15\text{ s} < 60\text{ s}$ (Violation flag triggered).

The target accumulates an anomaly score of $S = 3$. The validation filter quarantines the track instantly, isolates it from the COLREGs collision avoidance engine, and logs a high-priority telemetry alarm to the shore ROC.

> **Try it.** The script `code/security/kinematic_checks.py` implements these kinematic gating algorithms, parsing raw NMEA AIS feeds and evaluating speed caps, turn rates, teleportation jumps, and receiver footprint plausibility. You can execute this triage utility against synthetic harbor traffic:
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

## Software

Autonomous maritime software stacks bridge low-level NMEA sensor decoding with high-level trajectory planning and shore telemetry:

**Open source:**
- `ROS 2 (Robot Operating System 2)` (Open Robotics, Apache 2.0): Middleware framework for autonomous robotics research and MASS prototypes. Provides deterministic publish-subscribe nodes, DDS messaging transport, and hardware abstraction layers for marine radar, LiDAR, and AIS drivers. Caveat: Standard ROS 2 lacks native marine NMEA / IEC 61162 drivers out of the box; engineers must wrap serial/UDP sockets in custom bridge nodes.
- `libais` (Google / Kurt Schwehr, Apache 2.0): Robust C++ library with Python bindings for decoding ITU-R M.1371 binary payloads. Ideal for real-time AIS decoding pipelines on autonomous edge compute nodes. Caveat: Strictly a decoder; does not provide track association, Kalman filtering, or multi-sensor fusion.
- `OpenCPN` (Open Source Community, GPL v2+): Open-source chartplotter and navigation software supporting marine charts, radar overlays, and AIS target rendering. Frequently used as a baseline situational awareness display in academic autonomous vessel testbeds. Caveat: Not type-approved under IEC 61174 for SOLAS vessels; UI is optimized for human desktop interaction rather than headless autonomous execution.

**Free but closed:**
- `Marine Traffic API (Community Tier)` (Commercial API, Free evaluation tier): Provides cloud-aggregated global AIS feeds and vessel metadata lookups. Useful for ROC macro-monitoring and voyage planning. Caveat: Community tiers enforce strict rate limits and introduce 5-to-15-minute data latency, making them entirely unsuitable for tactical real-time collision avoidance.

**Commercial:**
- `Kongsberg Maritime K-Mate` (Kongsberg Maritime, Proprietary): Commercial autonomy controller and vessel automation engine deployed on *Yara Birkeland* and commercial autonomous workboats. Executes real-time multi-sensor fusion, COLREGs-compliant path planning, and remote control handover. Caveat: Closed proprietary hardware-software ecosystem with substantial commercial licensing costs.
- `Wärtsilä SmartPredict / Voyage AI` (Wärtsilä, Proprietary): Commercial navigation and automated situational awareness engine providing predictive trajectory modeling and anti-collision guidance for commercial ships. Caveat: Requires deep integration with proprietary bridge automation networks and vendor-approved hardware.
- `Orca AI` (Orca AI, Proprietary): Commercial vision-based situational awareness platform combining thermal cameras, computer vision, and AIS cross-referencing to provide automated collision alerts to bridge crews and shore fleet operation centers. Caveat: Requires proprietary masthead sensor pods and cloud connectivity for model retraining.

## Standards & guides

- **IMO MSC.1/Circ.1604 (2019):** *Interim Guidelines for MASS Trials*. Approved at MSC 101; establishes baseline risk management, safety assessment, and qualification criteria for testing autonomous ships at sea.
- **IMO MSC.1/Circ.1638 (2021):** *Outcome of the Regulatory Scoping Exercise for the Use of Maritime Autonomous Surface Ships (MASS)*. Comprehensive regulatory analysis mapping SOLAS, COLREGs, STCW, and MARPOL provisions across four degrees of autonomy.
- **IMO MASS Code (MSC 108/WP.6, 2024):** *International Code of Safety for Maritime Autonomous Surface Ships*. The goal-based international safety code governing the design, construction, remote control, and operation of MASS.
- **ITU-R M.1371-5 (2014):** *Technical Characteristics for an Automatic Identification System Using Time Division Multiple Access in the VHF Maritime Mobile Frequency Band*. Defines physical layer, link layer, and bit-level message formats for all AIS transponders.
- **ITU-R M.2135-1 (2023):** *Technical Characteristics of Autonomous Maritime Radio Devices Operating in the Frequency Band 156–162.05 MHz*. Governs Autonomous Maritime Radio Devices (AMRD) Group A (safety) and Group B (non-safety beacons).
- **IEC 61993-2 Edition 3.0 (2018):** *Class A Shipborne Equipment of the Automatic Identification System (AIS) – Operational and Performance Requirements, Methods of Test and Required Test Results*. Governs type-approval testing for mandatory shipboard Class A transponders.
- **IEC 61162-1 Edition 5.0 (2016):** *Digital Interfaces – Part 1: Single Talker and Multiple Listeners*. Governs the NMEA 0183 serial protocol carrying `!AIVDM` / `!AIVDO` sentences between transponders and navigation processors.
- **IEC 62288 Edition 3.0 (2021):** *Presentation of Navigation-Related Information on Shipborne Navigational Displays*. Defines standardized presentation symbols and operational icons for target display.
- **IEC 63173-1 Edition 1.0 (2021):** *Maritime Navigation and Radiocommunication Equipment and Systems – Data Interface – Part 1: S-421 Route Plan Based on S-100*. Defines digital route exchange formats between ships, shore authorities, and autonomous platforms.
- **IACS Unified Requirement E26 (2023):** *Cyber Resilience of Ships*. Mandates cyber risk management and network zoning on commercial vessels to protect navigational bridge systems against unauthorized network penetration.
- **IALA Guideline 1139 (2019):** *The Use of the Technical Standards for VHF Data Exchange System (VDES)*. Technical roadmap for wideband digital communications and route exchange supporting e-Navigation and MASS.

## Pitfalls

1. **Treating AIS as a primary obstacle detector in autonomy** → Small craft, fishing vessels, kayaks, and debris do not broadcast AIS → Require primary obstacle detection to rely on physical radar, LiDAR, and optical sensors; treat AIS strictly as a cooperative secondary metadata stream.
2. **Accepting AIS target positions without multi-sensor corroboration** → SDR spoofers can inject synthetic "ghost vessels" on direct collision courses → Cross-reference all AIS targets within radar range against physical radar echoes and optical bounding boxes before executing evasive maneuvers.
3. **Allowing unvalidated AIS kinematic spikes to crash tracking filters** → A single corrupted or spoofed coordinate jump destabilizes single-hypothesis Kalman filters → Implement strict Mahalanobis distance gating and kinematic velocity caps ($v \le 45\text{ kn}$) to quarantine unphysical fixes.
4. **Broadcasting Navigational Status 2 (Not Under Command) during routine autonomous transits** → Autonomous operations are not legally recognized as an exceptional disabling casualty under COLREG Rule 27 → Broadcast Navigational Status 0 (*Under way using engine*) unless an actual propulsion, steering, or system failure occurs.
5. **Relying on verbal VHF communications for collision avoidance** → Uncrewed vessels cannot interpret nuanced radiotelephone banter across static-heavy VHF Channel 16 → Implement deterministic COLREGs maneuvering based strictly on physical behavior, and utilize standardized digital route exchange (S-421 via VDES).
6. **Failing to model Class B reception latency in collision planners** → Class B transponders broadcast at slow, erratic intervals (30 s to 3 min) and suffer packet loss in congested TDMA cells → Project target covariance ellipses forward in time; never assume a target's position is static between delayed updates.
7. **Neglecting antenna lever-arm offsets in multi-sensor fusion** → On a 200 m container ship, the GNSS antenna may be 150 m aft of the bow, while the forward radar is on the forecastle → Rigorously apply rigid-body $\text{SE}(3)$ lever-arm transformations to map all target reports to a common vessel reference point.
8. **Underestimating satcom latency during shore ROC teleoperation** → Geostationary satellite hops introduce round-trip latency exceeding 1,000 ms, causing operator over-control oscillations → Ensure autonomous vessels retain local real-time reactive collision avoidance at the edge; never attempt closed-loop manual steering over high-latency links.
9. **Failing to switch to an emergency fail-safe status upon link loss** → If an uncrewed ship loses communications with the ROC and experiences navigation system degradation, surrounding ships remain unaware → Program the Class A transponder to alter broadcasted navigational status and trigger Message 14 safety broadcasts automatically upon entering a Minimum Risk Condition.
10. **Conflating receiver autonomous integrity with external data integrity** → A transponder reporting RAIM active only validates its internal GNSS fix, not the legitimacy of received VDL packets → Maintain an independent on-ship telemetry validation layer independent of the transponder firmware.

## Key takeaways

- **AIS is an essential metadata layer, not an obstacle sensor:** While AIS delivers invaluable non-line-of-sight awareness, target identification, and instantaneous velocity vectors, its cooperative nature means it cannot detect non-broadcasting hazards (the dark vessel problem).
- **Commercial MASS must carry type-approved Class A transponders:** Under SOLAS Chapter V Regulation 19 and the emerging IMO MASS Code, commercial autonomous ships must install certified Class A transponders operating with SOTDMA link-layer access.
- **The unauthenticated nature of AIS creates critical security vulnerabilities:** Without cryptographic authentication, autonomous collision-avoidance engines are vulnerable to phantom vessel spoofing, kinematic manipulation, and slot-starvation Denial of Service.
- **Multi-sensor data fusion is mandatory for algorithmic safety:** Robust autonomous architectures fuse AIS, marine radar, LiDAR, and optical/infrared vision using Extended Kalman Filtering and Mahalanobis distance gating to prevent uncorroborated ghost targets from causing grounding.
- **The Navigational Status dilemma persists:** Current ITU-R M.1371 standards lack an explicit code for "autonomous vessel"; MASS must broadcast status `0` (*Under way using engine*) while trial status is communicated via auxiliary digital messages or national registry databases.
- **Edge computing protects the ROC situational awareness pipeline:** Because satellite backhaul bandwidth is constrained, autonomous ships fuse high-bandwidth radar and video streams locally on board, transmitting lightweight target state vectors and AIS feeds to shore Remote Operations Centres.
- **Digital route exchange (S-421 via VDES) is the future of automated intent:** Standardized trajectory exchange over wideband VHF Data Exchange System channels replaces ambiguous radiotelephone voice calls, enabling automated algorithmic passing negotiations.

## References

- Balduzzi, M., Pasta, A., Wilhoit, K. (2014). A Security Evaluation of AIS Automated Identification System. In *Proceedings of the 30th Annual Computer Security Applications Conference (ACSAC '14)*, pages 436–445. New Orleans, LA: ACM. doi:10.1145/2664243.2664257
- IACS (2023). *Cyber Resilience of Ships* (Unified Requirement UR E26 Rev.1). London: International Association of Classification Societies.
- IALA (2019). *The Use of the Technical Standards for VHF Data Exchange System (VDES)* (IALA Guideline 1139). Saint-Germain-en-Laye: International Association of Marine Aids to Navigation and Lighthouse Authorities.
- IEC (2016). *Maritime Navigation and Radiocommunication Equipment and Systems – Digital Interfaces – Part 1: Single Talker and Multiple Listeners* (IEC 61162-1:2016 Edition 5.0). Geneva: International Electrotechnical Commission.
- IEC (2018). *Maritime Navigation and Radiocommunication Equipment and Systems – Automatic Identification Systems (AIS) – Part 2: Class A Shipborne Equipment of the Automatic Identification System (AIS) – Operational and Performance Requirements, Methods of Test and Required Test Results* (IEC 61993-2:2018 Edition 3.0). Geneva: International Electrotechnical Commission.
- IEC (2021). *Maritime Navigation and Radiocommunication Equipment and Systems – Presentation of Navigation-Related Information on Shipborne Navigational Displays – General Requirements, Methods of Testing and Required Test Results* (IEC 62288:2021 Edition 3.0). Geneva: International Electrotechnical Commission.
- IEC (2021). *Maritime Navigation and Radiocommunication Equipment and Systems – Data Interface – Part 1: S-421 Route Plan Based on S-100* (IEC 63173-1:2021 Edition 1.0). Geneva: International Electrotechnical Commission.
- IMO (2019). *Interim Guidelines for MASS Trials* (Circular MSC.1/Circ.1604). London: International Maritime Organization.
- IMO (2021). *Outcome of the Regulatory Scoping Exercise for the Use of Maritime Autonomous Surface Ships (MASS)* (Circular MSC.1/Circ.1638). London: International Maritime Organization.
- IMO (2024). *International Code of Safety for Maritime Autonomous Surface Ships (MASS Code)* (Document MSC 108/WP.6). London: International Maritime Organization.
- ITU-R (2014). *Technical Characteristics for an Automatic Identification System Using Time Division Multiple Access in the VHF Maritime Mobile Frequency Band* (Recommendation ITU-R M.1371-5). Geneva: International Telecommunication Union.
- ITU-R (2023). *Technical Characteristics of Autonomous Maritime Radio Devices Operating in the Frequency Band 156–162.05 MHz* (Recommendation ITU-R M.2135-1). Geneva: International Telecommunication Union.
- Porathe, T., Prison, J., Man, Y. (2014). Situation Awareness in Remote Control Centres for Unmanned Ships. In *Human Factors in Ship Design & Operation*, pages 1–9. London: Royal Institution of Naval Architects.
- Rødseth, Ø. J., Burmeister, H.-C. (2012). Developments toward the Unmanned Ship. In *Proceedings of the International Symposium Information on Ships (ISIS 2012)*, pages 1–11. Hamburg: DGON.
- Thombre, S., Zhao, Z., Ramm-Schmidt, H., García Valdés, J. M., Malkamäki, T., Nikolskiy, S., Hammarberg, T., Bhuiyan, M. Z. H., Särkkä, S., Lehtola, V., Kuusniemi, H. (2022). Sensors and AI Techniques for Situational Awareness in Autonomous Ships: A Review. *IEEE Transactions on Intelligent Transportation Systems*, 23(1):64–83. doi:10.1109/TITS.2020.3023921
