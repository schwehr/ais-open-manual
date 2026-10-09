# Chapter 53 — How mariners are trained to use AIS (and how it varies)

> **Part VIII — Charts, bridge systems, and mariners.** How professional deck officers, pilots, vessel traffic operators, and recreational mariners are instructed in the operational use and inherent limitations of AIS, and why disparities in qualification standards create systemic risks at sea.

**In this chapter.** You will learn how maritime training regimes prepare mariners to operate the Automatic Identification System (**AIS**), how statutory competencies vary across jurisdictions, and why operational practice frequently diverges from international guidance. You will examine the mandatory competencies established by the International Convention on Standards of Training, Certification and Watchkeeping for Seafarers (**STCW**) under Table A-II/1 and Table A-II/2, guided by International Maritime Organization (**IMO**) Model Course 1.34 and Resolution A.1106(29). You will analyze national implementations across the United States Coast Guard (**USCG**), the United Kingdom Maritime and Coastguard Agency (**MCA**), and European administrations. You will investigate specialized training pipelines for maritime pilots and Vessel Traffic Services (**VTS**) operators under the International Association of Marine Aids to Navigation and Lighthouse Authorities (**IALA**) V-103 framework. Furthermore, you will assess the recreational boating sector, where Class B carriage occurs largely without statutory training. Finally, you will explore human-factors research into automation bias, the phenomenon of "VHF/AIS-assisted collisions," simulator design criteria, and instructional methodologies that build resilient bridge watchkeeping.

## 53.1 The statutory architecture: STCW, IMO Model Course 1.34, and Resolution A.1106(29)

Maritime navigation training operates internationally under the International Convention on Standards of Training, Certification and Watchkeeping for Seafarers (**STCW**), 1978, as amended. When Class A shipborne AIS carriage was phased into Chapter V of the International Convention for the Safety of Life at Sea (**SOLAS**) between 2002 and 2008 ([Chapter 10](ch10-standardization-1996-2004.md)), bridge officers received automated broadcast transponders before statutory curricula existed to teach data interpretation, sensor verification, or interface management.

The 2010 Manila Amendments to the STCW Convention and Code integrated digital bridge technologies into mandatory officer proficiencies. Under **Table A-II/1** (Officers in Charge of a Navigational Watch [**OICNW**] on ships $\ge 500\text{ GT}$), *Maintain a safe navigational watch* requires operational knowledge of bridge navigation systems, explicitly including the capabilities, limitations, and operational use of AIS. For senior officers, **Table A-II/2** (Masters and Chief Mates $\ge 500\text{ GT}$) mandates proficiency in evaluating integrated Radar, Automatic Radar Plotting Aids (**ARPA**), Electronic Chart Display and Information Systems (**ECDIS**), and AIS to execute command decisions under the International Regulations for Preventing Collisions at Sea (**COLREGs**).

To guide maritime academies, the IMO developed **IMO Model Course 1.34** (*Automatic Identification Systems*). Issued in 2006 and revised in 2019, Model Course 1.34 provides a 24- to 30-hour modular syllabus structured around five core instructional domains:

1. **Link architecture and protocols:** TDMA channel access ([Chapter 21](ch21-link-layer-tdma.md)), VHF propagation, simplex channels (87B/88B; 161.975/162.025 MHz), dynamic reporting intervals, and Class A versus Class B station tiers ([Chapter 20](ch20-architecture-and-station-classes.md)).
2. **Message taxonomy and parameter integrity:** Differentiating **static data** (MMSI, IMO number, call sign, name, dimensions; Message 5 every 6 min), **dynamic data** (position, UTC, COG, SOG, heading, rate of turn, navigational status; Messages 1–3 every 2 s to 3 min), and **voyage data** (draught, hazardous cargo, destination, ETA; manually entered).
3. **Operational handling and interfaces:** Operating the Minimum Keyboard and Display (**MKD**), selecting primary/secondary sensor feeds (EPFS, gyro, speed log), configuring target presentation on radar and ECDIS ([Chapter 51](ch51-charts-enc-ecdis.md)), and sending safety text (Messages 12/14).
4. **Sensor error propagation and failure modes:** Diagnosing datum offsets, inverted antenna dimension offsets, gyro slippage, GNSS spoofing ([Chapter 62](ch62-gnss-jamming-spoofing.md)), VDL slot contention ([Chapter 30](ch30-network-loading-packet-loss.md)), and receiver desensitization.
5. **Collision avoidance and legal boundaries:** Cross-referencing AIS vectors with ARPA radar, applying COLREG Rules 5 and 7, maintaining visual lookout primacy, preventing VHF-assisted errors, and applying master switch-off discretion under SOLAS V/19.2.4.7.

Operational doctrine in Model Course 1.34 stems from **IMO Resolution A.1106(29)** (*Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems (AIS)*, adopted 2 December 2015, superseding A.917(22) and A.956(23)). Resolution A.1106(29) provides the standard baseline for flag-state examinations, explicitly cautioning:

> "The potential of AIS as an anti-collision aid is recognized and AIS may be recommended as such a device in due time in respect of suitable radar targets, but the user must be aware that AIS is an aid to navigation and does not replace radar/ARPA, visual lookout, or standard collision avoidance procedures." (Resolution A.1106(29), Section 40)

Paragraphs 24–27 mandate updating voyage parameters prior to departure and upon each operational change: static draught, UN/LOCODE destination, ETA, and navigational status (e.g., *Under way using engine* [0], *At anchor* [1], or *Constrained by her draught* [4]).

> **Definitions that bite.**
>
> In bridge operations and maritime law, **Heading** and **Course Over Ground (COG)** represent fundamentally different physical quantities, yet navigators frequently confuse their vectors on electronic displays.
>
> - **Heading:** The instantaneous direction in which the ship's bow is pointed relative to true north, supplied directly to the AIS transponder by the vessel's transmitting heading device (**THD**), typically a marine gyrocompass or GNSS heading sensor (codified in ITU-R M.1371 Message 1/2/3 as bits 63–71, in units of 1° with a valid range of 0° to 359°, or 511 indicating *not available*).
> - **Course Over Ground (COG):** The actual direction of motion of the vessel's center of mass relative to the earth's surface, calculated by the internal or external GNSS receiver from successive position solutions (codified in bits 42–53, in units of 0.1°, range 0.0° to 359.9°, or 3600 indicating *not available*).
>
> In the presence of strong cross-currents, leeway caused by gale-force beam winds, or when an unpowered vessel is drifting sideways, Heading and COG diverge by substantial angles (the **drift angle** or **leeway**). An officer examining an electronic chart who interprets an AIS target's COG vector as its heading will misjudge the vessel's physical aspect, miscalculate its relative movement under COLREG Rules 14 and 15, and risk initiating an incorrect collision-avoidance maneuver.

## 53.2 Flag-state differences: USCG, MCA, and European regimes

Although STCW establishes an international foundation, national administrations implement and assess AIS competencies through divergent regulatory frameworks, producing noticeable disparities in operational knowledge among watchkeepers.

### 53.2.1 United States Coast Guard (USCG)

In the United States, the USCG National Maritime Center (**NMC**) credentials mariners under Title 46 of the Code of Federal Regulations (**46 CFR**). Rather than requiring a standalone AIS certificate, the USCG embeds competencies into radar, ARPA, and ECDIS courses governed by Navigation and Vessel Inspection Circulars (**NVICs**).

Under **NVIC 12-14** (OICNW $\ge 500\text{ GT}$) and **NVIC 10-14** (Master/Chief Mate $\ge 3,000\text{ GT}$), candidates complete practical assessment sign-offs covering MKD operation, sensor verification, manual voyage entry, target correlation on ECDIS/ARPA, and compliance with 33 CFR § 164.46 (the US AIS carriage mandate). Written Regional Examination Center (**REC**) tests evaluate AIS within *Navigation General* and *Watchkeeping* modules. However, multiple-choice items traditionally test regulatory thresholds under the Maritime Transportation Security Act of 2002 (**MTSA 2002**) rather than serial interface diagnostics or tactical filtering. Domestic towing masters operating under 46 CFR Subchapter M must carry and monitor AIS under 33 CFR § 164.46, yet their licensing pathway rarely mandates the full simulator regimens required for unlimited ocean officers.

### 53.2.2 United Kingdom Maritime and Coastguard Agency (MCA)

The UK Maritime and Coastguard Agency (**MCA**) enforces STCW compliance via accredited nautical degree programs and comprehensive oral examinations conducted by MCA surveyors. Operational doctrine is codified in Marine Guidance Notes:
- **MGN 324 (M+F):** *Watchkeeping Safety – Use of VHF Radio and AIS*. Explicitly warns against treating AIS as an anti-collision aid, emphasizes that AIS does not possess radar tracking precision, and prohibits using VHF radio to negotiate collision avoidance.
- **MGN 379 (M+F):** *Use of Electronic Navigation Aids*. Analyzes automation complacency and single-sensor fixation.

During MCA oral board examinations, candidates face dynamic multi-vessel encounters. Relying on AIS target identities to broker VHF passing agreements or failing to verify target tracks with optical bearings and relative-motion radar plotting results in immediate failure. This oral examination enforces COLREG primacy over digital convenience.

### 53.2.3 European Maritime Safety Agency (EMSA) and continental frameworks

Across continental Europe, maritime education falls under EU Directive 2008/106/EC audited by the European Maritime Safety Agency (**EMSA**). National administrations—such as Germany's *Bundesamt für Seeschifffahrt und Hydrographie* (**BSH**), France's *Direction des Affaires Maritimes*, and the Netherlands' *Inspectie Leefomgeving en Transport* (**ILT**)—embed AIS into multi-year maritime academy curricula.

European training also features **Inland AIS** governed by the Central Commission for the Navigation of the Rhine (**CCNR**) and EU Directive 2005/44/EC (River Information Services [**RIS**]). Inland navigators train on tactical inland ECDIS operating in *information* and *navigation* modes. Inland AIS incorporates decimeter vessel dimensions, blue-sign passing status, and air-draught clearances, requiring inland-specific operational instruction absent from deep-sea programs.

| Jurisdiction | Primary Regulatory Instruments | AIS Curriculum Format | Assessment Methodology | Key Training Emphases |
| :--- | :--- | :--- | :--- | :--- |
| **International (IMO)** | STCW Code Tables A-II/1, A-II/2; Res. A.1106(29) | IMO Model Course 1.34 (24–30 h modular syllabus) | Academy course completion; continuous practical assessment | Technical TDMA architecture, MKD programming, COLREG non-conflict |
| **United States (USCG)** | 46 CFR Subchapter B; NVIC 12-14, 10-14; 33 CFR § 164.46 | Embedded within ECDIS, ARPA, and Radar Observer courses | Multiple-choice REC exams; NVIC practical task sign-offs | US domestic carriage rules, MTSA requirements, bridge team procedures |
| **United Kingdom (MCA)** | MGN 324 (M+F), MGN 379 (M+F); MSN 1856 | Integrated into Nautical Science diplomas and MNTB modules | College coursework plus rigorous MCA surveyor oral examination | Human-factors over-reliance, strict COLREG Rule 7 compliance, VHF prohibition |
| **European Union (BSH / ILT / CCNR)** | Directive 2008/106/EC; CCNR Inland AIS; RIS Directive | Degree curricula; dedicated Inland Navigation certification | Simulator assessments; state maritime administration practical tests | Inland ECDIS modes, River Information Services, blue-sign passing protocols |

## 53.3 The unconstrained domain: recreational boaters and Class B transponders

While commercial mariners operate within statutory certification structures, the fastest-growing segment of the AIS ecosystem—recreational yachting, sport fishing, and small coastal craft—operates almost entirely outside statutory training mandates.

Under IMO and SOLAS mandates, recreational craft are not required to carry AIS. However, the international standardization of Class B transponders in 2006 (IEC 62287-1 for Carrier Sense TDMA [**CSTDMA**], followed by IEC 62287-2 for Self-Organized TDMA [**SOTDMA**]; [Chapter 20](ch20-architecture-and-station-classes.md)) unleashed widespread voluntary adoption across leisure fleets. Boaters install Class B devices to enhance visibility to commercial traffic and display nearby ships on multifunction chartplotters or consumer tablets running navigation applications.

This voluntary expansion has created critical operational disconnects:

1. **The illusion of universal radar equivalence:** Boaters frequently assume that transmitting Class B guarantees visibility. In practice, commercial bridge teams configure aggressive target filtering or sleep modes to suppress clutter ([Chapter 51](ch51-charts-enc-ecdis.md)). On many ARPA radars, sleeping Class B targets trigger no audible collision alarms unless manually unmasked. Relying on AIS rather than a radar reflector and visual watch exposes leisure craft to extreme danger.
2. **Static data misconfiguration:** Class B units require one-time programming (MMSI, call sign, dimensions, antenna position). Lacking training, boaters frequently deploy dummy MMSIs (`111111111`, `123456789`), default vessel type codes (e.g., classifying a sailing sloop as a towing vessel), or inverted antenna offsets.
3. **Misinterpreting reporting intervals:** Class B CSTDMA units transmit Message 18 every 3 min at $\le 2\text{ kn}$ ($3.7\text{ km/h}$) and every 30 s at $> 2\text{ kn}$, subject to slot availability. Under link contention, units defer transmissions. Untrained users assume vectors reflect instantaneous reality, unaware that a fast craft covers hundreds of metres between updates.

> **Rule of thumb.**
>
> **The Class B Vector Lag Rule:** Never calculate collision margins or execute close-quarters passing maneuvers around a Class B AIS contact using only its electronic chart vector. A Class B CSTDMA target moving at $24\text{ kn}$ ($44.4\text{ km/h}$) updates its position only once every 30 s (assuming zero packet loss); in that reporting window, the vessel advances $370\text{ m}$ along an unprojected track. If the vessel initiates a sharp course alteration immediately following a broadcast, the electronic display portrays an obsolete dead-reckoned vector for over half a minute. Verify all dynamic maneuvers of small craft visually or via continuous ARPA radar tracking.

## 53.4 Specialized training pipelines: maritime pilots and VTS operators

Beyond ship's bridge officers, two groups of specialized marine professionals undergo rigorous, advanced AIS training: **maritime pilots** and **Vessel Traffic Services (VTS) operators**.

### 53.4.1 Maritime pilots and Portable Pilot Units (PPUs)

Maritime pilots board commercial vessels in coastal approaches, estuaries, and confined harbor channels to navigate them through high-risk pilotage waters. Pilots operate in a demanding cognitive environment: they must instantly assess the handling characteristics of an unfamiliar ship while interacting with a bridge team whose language and procedures may differ from local practice.

To maintain independent situational awareness, modern pilots rely on **Portable Pilot Units** (**PPUs**)—ruggedized laptops or tablets running specialized high-precision piloting software (e.g., Navicom Dynamics, Transas/Wärtsilä Pilot PRO, QPS Qastor). The pilot interfaces the PPU with the ship's navigation stack via the standardized Class A **AIS Pilot Plug** (codified under IEC 61993-2 and IMO SN/Circ.227; [Chapter 26](ch26-interfaces-and-logging.md)).

Pilot training pipelines endorsed by the International Maritime Pilots' Association (**IMPA**) emphasize:
- **Pilot plug diagnostics:** Verifying RS-422 differential signaling, 38,400 baud rates, and common defects (reversed polarity, ungrounded wiring).
- **Sensor latency and gyro errors:** Recognizing that the pilot plug echoes host vessel sensors. Gyro hunting or lag destabilizes PPU track prediction, prompting pilots to deploy independent dual-antenna GNSS heading/ROT units and use the ship's plug solely for target traffic.
- **Berthing kinematics:** Leveraging rate-of-turn (ROT) data and centimeter-level GNSS to calculate bow and stern lateral velocities, accounting for Message 5 antenna offset distortions ([Chapter 51](ch51-charts-enc-ecdis.md)).

```
+--------------------------------------------------------------------------+
|                      SHIPBOARD CLASS A AIS TRANSPONDER                   |
|  - Internal/External GNSS (Position, SOG, COG)                           |
|  - Transmitting Heading Device (Gyro / THD)                              |
|  - Static & Voyage Data Database                                         |
+------------------------------------+-------------------------------------+
                                     |
                          NMEA 0183 / IEC 61162-2
                          (38,400 baud, RS-422)
                                     |
                                     v
                       +---------------------------+
                       |   STANDARD PILOT PLUG     |
                       |   (ISO 8468 / SN/Circ.227)|
                       +-------------+-------------+
                                     |
                        Differential Serial Cable
                        or Secure Wi-Fi/Bluetooth
                                     |
                                     v
            +-------------------------------------------------+
            |           PORTABLE PILOT UNIT (PPU)             |
            | - Independent Centimeter-Accurate RTK GNSS      |
            | - High-Rate Gyro / ROT Sensor Module            |
            | - Precision Chart Engine (ENC / S-100 Bathy)    |
            | - Predictive Docking & Hydrodynamic Vectors     |
            +-------------------------------------------------+
```

### 53.4.2 Vessel Traffic Services (VTS) operators and IALA V-103

Shore-based Vessel Traffic Services manage vessel movements in complex waterways to enhance navigational safety and protect maritime infrastructure. VTS operators undergo a specialized training regime distinct from shipboard watchkeeping, governed globally by the International Association of Marine Aids to Navigation and Lighthouse Authorities (**IALA**).

IALA establishes training standards under **Recommendation R0103** (formerly **V-103**), supported by dedicated **Model Courses**:
- **C0103-1 (Model Course V-103/1):** *VTS Operator Training*. Basic qualifying standard covering radar tracking, VHF radio communications, traffic organization, and shore-based AIS integration.
- **C0103-2 (Model Course V-103/2):** *VTS Supervisor Training*. Advanced training focusing on crisis management, incident investigation, and multi-sensor surveillance fusion.
- **C0103-3 (Model Course V-103/3):** *VTS On-the-Job Training*. Port-specific practical qualification.
- **C0103-4 (Model Course V-103/4):** *VTS On-the-Job Training Instructor*.

In addition, IALA published **Guideline G1149** (*VTS Training for Deck Officers*), which bridges the perceptual gap between shipboard navigators and shore operators. Under the V-103 framework, VTS operators are taught that shore-based AIS surveillance is fundamentally asymmetric compared to shipboard reception. Shore systems utilize high-elevation base station networks, redundant receiver arrays, and multi-sensor tracking processors that fuse AIS data with primary shore radar and electro-optical cameras ([Chapter 4](ch04-vts-and-ports.md)).

V-103 training emphasizes:
- **Broadcast scheduling and assignment:** Managing base station commands, polling targets (Message 15), and assigning dynamic reporting rates (Messages 16 and 23) in critical channels.
- **Synthetic and virtual AtoNs:** Broadcasting Message 21 to project physical, synthetic, or virtual aids marking wrecks, drifting buoys, or exclusion zones.
- **Link load monitoring:** Tracking slot allocation, frame utilization, and resolving local VDL congestion.

## 53.5 Human factors, automation bias, and the "VHF/AIS-assisted" collision

The operational deployment of AIS has transformed maritime situational awareness, yet accident investigations demonstrate that the system has introduced serious human-factors failure modes. Rather than merely eliminating uncertainty, AIS can alter cognitive behavior in ways that actively undermine safety.

### 53.5.1 Cognitive mechanisms: automation bias and premature closure

In cognitive ergonomics, **automation bias** is the tendency for decision-makers to favor automated digital sensor readouts over contradictory sensory cues or manual cross-verification. In the maritime context, an AIS display provides a tidy, highly resolved digital target: an alphanumeric ship name, exact call sign, numerical speed to the tenth of a knot, and a sharply rendered track vector.

This apparent precision creates a cognitive trap known as **premature closure**:
- **The veneer of certainty:** ARPA requires minutes of steady tracking before velocity vectors stabilize; AIS vectors appear immediately alongside vessel names, prompting watchkeepers to mistake numerical precision for physical truth.
- **Tunnel vision and lookout degradation:** Eye-tracking research reveals that watchkeepers in multi-target encounters spend disproportionate visual time on electronic consoles, neglecting optical horizon scans (**COLREG Rule 5**).
- **Target blindness:** Clearly rendered AIS targets cause subconscious blindness to non-broadcasting hazards: wooden or fiberglass hulls, unpowered barges, floating containers, and non-compliant fishing craft.

### 53.5.2 The "VHF/AIS-assisted collision" phenomenon

One of the most persistent behavioral distortions caused by AIS is the **"VHF/AIS-assisted collision."**

Prior to AIS, attempting to contact an unknown ship in open water via VHF radio was fraught with uncertainty. An officer broadcasting on Channel 16 would call: *"Vessel on my port bow, distance four miles, this is the container ship heading northeast..."* In congested waters, multiple ships might match that general description, or the target vessel might fail to recognize itself.

AIS dismantled this identification barrier. By rendering the target's exact name, MMSI, and call sign on the radar or ECDIS, AIS allows a watchkeeper to call the target ship directly: *"Container ship Pacific Mariner, this is bulk carrier Nordic Star on your port bow."* While intended to improve communication, accident investigation boards—notably the UK Marine Accident Investigation Branch (**MAIB**) and the US National Transportation Safety Board (**NTSB**)—have repeatedly found that direct VHF calling frequently causes collisions:

1. **Substituting verbal agreements for COLREGs:** Officers negotiate informal passing agreements (e.g., *"passing green-to-green"*) contrary to COLREG Rules 14–17.
2. **Ambiguous language:** Colloquial phrases (*"I'll go around you"*) and language barriers produce conflicting interpretations of agreed maneuvers.
3. **The "mental snapshot" trap:** After a radio exchange, watchkeepers experience cognitive relaxation, assuming risk is eliminated and terminating active radar plotting. If one vessel maneuvers late or incorrectly, the vessels close without either watchkeeper intervening in time.

> **Case file.**
>
> **MAIB Investigation: Huayang Endeavour and Seafrontier (Report No. 11/2018).**
>
> On 1 July 2017 at 0204 UTC, the bulk carrier *Huayang Endeavour* and the chemical tanker *Seafrontier* collided in the Dover Strait Traffic Separation Scheme (**TSS**) in clear visibility. Both vessels were equipped with operational Class A AIS, ARPA radar, and ECDIS.
>
> The MAIB investigation revealed that despite having ample sea room to execute a standard collision-avoidance maneuver under COLREG Rule 15 (as the give-way vessel), the watch officer on *Huayang Endeavour* identified *Seafrontier* by its AIS target name on the electronic display and initiated VHF radio communication. Over several minutes of broken VHF dialogue, the two officers attempted to negotiate a non-standard passing arrangement contrary to the collision regulations.
>
> The verbal communication generated deep confusion: each officer formed a contradictory mental model of what the other ship had agreed to do. Furthermore, engaging in the radio dialogue distracted both officers from monitoring their ARPA radar plotting and maintaining a proper visual lookout. *Seafrontier* maintained its heading, while *Huayang Endeavour* altered course directly into the tanker's path. The bow of *Huayang Endeavour* penetrated *Seafrontier*'s port side hull.
>
> In its final report, the MAIB concluded that AIS had facilitated the premature, hazardous use of VHF radio to negotiate collision avoidance, highlighting that AIS target names lead navigators to abandon the COLREGs in favor of dangerous verbal agreements.

## 53.6 Simulator training: pedagogical design, failure injection, and assessment

Given the severe human-factors pitfalls associated with digital bridge systems, advanced maritime training centers rely heavily on **Full Mission Bridge Simulators** (**FMBS**) conforming to STCW Section A-I/12 and certified under standards such as DNV-ST-0033 (*Maritime Simulator Systems*).

However, historical simulator training frequently treated AIS as an infallible background layer: simulated target ships faithfully broadcast perfect kinematic tracks, perfect GPS positions, and clean gyro headings. Such idealized simulation reinforces automation bias, conditioning student officers to place unquestioning trust in electronic screens. Modern, effective AIS training curricula employ **adversarial failure injection** to teach resilient watchkeeping.

### 53.6.1 Core simulator failure injection scenarios

To develop critical evaluation skills in bridge watchkeepers, accredited simulation programs deliberately expose candidates to authentic sensor anomalies and protocol constraints:

- **Heading vs. COG divergence in strong cross-currents:** Setting a simulated river estuary or tidal channel with a 5-knot cross-current. Trainees must maneuver past a crossing target whose AIS heading points $25^\circ$ away from its COG vector. Trainees who execute maneuvers based on the AIS COG line rather than the target's physical aspect (heading) fail the scenario.
- **Transmitting heading device (gyro) failure:** Injecting a $15^\circ$ heading slewing error into an AIS-equipped target vessel while its GNSS position track remains accurate. Trainees must identify the mismatch between the target's radar echo orientation, visual aspect, and distorted AIS heading line.
- **Antenna offset inversion:** Simulating a 400 m container vessel where the transmitting AIS unit has its Message 5 dimension parameters inverted (e.g., swapping internal GPS antenna offsets $A$ and $B$, shifting the rendered electronic hull icon 300 m aft of its actual position). In close-quarters maneuvering or docking simulations, trainees who rely on the ECDIS hull outline rather than visual lookouts and raw radar echoes initiate premature turns and strike obstructions.
- **Static and voyage data corruption:** Introducing targets displaying erroneous navigational statuses—such as a vessel actively steaming at 16 knots while broadcasting status *At anchor* (status 1) or *Not under command* (status 2)—or transmitting dummy MMSIs. Trainees are assessed on their ability to cross-examine target behavior using radar and visual observation rather than blindly accepting broadcast data.
- **GNSS jamming and position jumps:** Simulating localized RF jamming or spoofing zones where the own-ship AIS GNSS receiver loses fix or teleports miles off-track ([Chapter 62](ch62-gnss-jamming-spoofing.md)), triggering cascade alarms across ECDIS and ARPA displays. Trainees must promptly identify the sensor failure, silence nuisance alarms, shift conning to raw radar and optical bearings, and manually update the AIS transponder.

### 53.6.2 Objective assessment criteria

Under STCW Table A-II/1, simulator-based assessment of AIS proficiency must measure concrete, observable watchkeeping behaviors:
1. **Verification latency:** Measuring the elapsed time between the appearance of an AIS target and the watch officer's independent verification via ARPA radar acquisition and optical bearing.
2. **COLREG adherence:** Evaluating whether maneuvers executed in crossing and overtaking situations strictly comply with Rules 13–17, regardless of any external radio communications.
3. **Alarm management:** Assessing whether the officer correctly configures CPA/TCPA alarm thresholds to avoid alarm fatigue while maintaining adequate collision margins, and whether the officer correctly diagnoses system alarms (e.g., *AIS: Tx Malfunction*, *AIS: Lost Target*, *AIS: Gyro Error*).
4. **Data housekeeping:** Verifying that the officer updates the own-ship MKD voyage parameters (draught, destination, ETA, navigational status) during pre-departure checks and upon anchoring or getting underway.

## Then & now

How the operational training, regulation, and bridge culture surrounding AIS have transformed over three decades:

- **1990s:** ⟨H⟩ Bridge watchkeeping relies strictly on visual observation, paper nautical charts, manual parallel index plotting, and standalone marine radar with early ARPA tracking. Radio communication to unidentified targets on VHF Channel 16 is discouraged due to target confusion and lack of reliable positive identification.
- **2000–2004:** ⟨+⟩ IMO MSC.74(69) and SOLAS Chapter V mandate Class A AIS transponders. Early shipboard installations feature small, monochrome Minimum Keyboard and Display (**MKD**) units mounted on bridge bulkheads. Initial maritime academy instruction focuses entirely on the mechanical programming of the MKD (entering MMSI, ship dimensions, and voyage data) and basic text-based safety messaging.
- **2006:** ⟨+⟩ IMO issues Model Course 1.34 (*Automatic Identification Systems*), establishing the first formal international curriculum for AIS. IEC completes Class B CSTDMA standardization (IEC 62287-1), opening the floodgates to uncertified recreational and fishing carriage without accompanying training mandates.
- **2010:** ⟨+⟩ The Manila Amendments to the STCW Convention and Code overhaul international watchkeeping standards, formally incorporating AIS and ECDIS competencies into Tables A-II/1 and A-II/2. Simultaneously, MAIB and international casualty boards identify an alarming rise in "VHF-assisted collisions" facilitated by AIS target naming.
- **2015:** ⟨+⟩ IMO Assembly adopts Resolution A.1106(29), superseding A.917(22) and establishing modern operational guidelines for shipborne AIS, highlighting inherent sensor limitations, master's switch-off discretion, and the legal non-replacement of radar.
- **2020s:** ⟨+⟩ Multifunction bridge consoles fully integrate AIS, ARPA, and ECDIS with centralized Bridge Alert Management (**BAM** under IEC 62923). Full Mission Bridge Simulators introduce dynamic failure injection (GNSS spoofing, sensor dropouts, target spoofing) to counter entrenched automation bias among digital-native maritime cadets.

## On the wire

While deck officers interact with AIS through graphical radar or ECDIS interfaces, the underlying bridge integration relies on standardized serial NMEA 0183 / IEC 61162 sentences flowing between the Class A transponder, navigation sensors, and display processors. Understanding these data streams is essential for diagnosing corrupted bridge displays.

```
+-------------------+        NMEA 0183 / IEC 61162-1        +-------------------+
|  GYROCOMPASS /    | ------------------------------------> |  CLASS A AIS      |
|  HEADING DEVICE   |       $--HDT,084.2,T*21               |  TRANSPONDER      |
+-------------------+                                       |                   |
                                                            |  - Generates VDM  |
+-------------------+        NMEA 0183 / IEC 61162-1        |    for targets    |
|  PRIMARY GNSS     | ------------------------------------> |  - Generates VDO  |
|  RECEIVER         |       $--RMC,120000,...               |    for own-ship   |
+-------------------+                                       +---------+---------+
                                                                      |
                                                             IEC 61162-2 High-Speed
                                                             (38,400 baud RS-422)
                                                             !AIVDM / !AIVDO sentences
                                                                      |
                                                                      v
                                                            +-------------------+
                                                            |  ECDIS / RADAR    |
                                                            |  CONNING DISPLAY  |
                                                            +-------------------+
```

When an AIS transponder receives a dynamic position report over the VHF Data Link, it outputs an encapsulated `!AIVDM` sentence to bridge displays. When it broadcasts its own ship's telemetry, it outputs an identical `!AIVDO` sentence. The following trace illustrates an incoming Class A dynamic report (Message 1) received on a bridge conning network:

```text
!AIVDM,1,1,,B,13aEO:0P000004rK5=004?wf0<00,0*13
```

Decoding this payload demonstrates how sensor values map directly into the watchkeeper's visual display:
- Encapsulated Payload: `13aEO:0P000004rK5=004?wf0<00`
- Message Type (bits 0–5): `1` (Position Report Class A)
- Repeat Indicator (bits 6–7): `0` (Initial transmission)
- MMSI (bits 8–37): `244670000` (Dutch commercial cargo vessel)
- Navigational Status (bits 38–41): `0` (*Under way using engine*)
- Rate of Turn (bits 42–49): `0` ($0^\circ/\text{min}$)
- Speed Over Ground (bits 50–59): `0` ($0.0\text{ kn}$)
- Position Accuracy (bit 60): `1` (High accuracy, $<10\text{ m}$)
- Longitude (bits 61–88): $4.416666^\circ\text{ E}$ ($004^\circ 25.000'\text{ E}$)
- Latitude (bits 89–115): $51.916666^\circ\text{ N}$ ($051^\circ 55.000'\text{ N}$)
- Course Over Ground (bits 116–127): `0` ($0.0^\circ$)
- True Heading (bits 128–136): `84` ($084^\circ$)
- Time Stamp (bits 137–142): `0` ($0\text{ s}$)

Notice the critical discrepancy: SOG is $0.0\text{ kn}$, Navigational Status is $0$ (*Under way using engine*), while the vessel is moored at a quay in Rotterdam. The bridge watchkeeper failed to update the MKD status upon securing mooring lines—a classic failure of voyage data housekeeping that degrades traffic domain models worldwide.

> **Try it.**
>
> You can evaluate AIS parameter errors and voyage housekeeping deficiencies directly from raw NMEA stream logs using Python. Activate the handbook environment and run this verification snippet against bridge data:
>
> ```python
> # Sample NMEA sentence: Class A Message 5 static/voyage data
> sample_record = {
>     "mmsi": 367123450,
>     "vessel_name": "COASTAL RUNNER",
>     "callsign": "WDE1234",
>     "nav_status": 0,  # 0 = Under way using engine
>     "sog_knots": 0.0,
>     "speed_zero_hours": 14.5,
>     "draught_meters": 0.0,
>     "destination": "PORT CHARLOTTE",
>     "eta": "02-30 25:00",  # Corrupted month/hour
> }
> 
> def audit_ais_housekeeping(record):
>     anomalies = []
>     if record["nav_status"] == 0 and record["sog_knots"] < 0.2 and record["speed_zero_hours"] > 2.0:
>         anomalies.append("FAULT: NavStatus indicates 'Under way' but vessel stationary >2h")
>     if record["draught_meters"] <= 0.0:
>         anomalies.append("FAULT: Static draught is 0.0m (uninitialized)")
>     try:
>         month = int(record["eta"][:2])
>         day = int(record["eta"][3:5])
>         hour = int(record["eta"][6:8])
>         if not (1 <= month <= 12 and 1 <= day <= 31 and 0 <= hour <= 23):
>             anomalies.append(f"FAULT: Invalid ETA timestamp: {record['eta']}")
>     except Exception:
>         anomalies.append("FAULT: Malformed ETA field")
>     return anomalies
> 
> for issue in audit_ais_housekeeping(sample_record):
>     print(f" [!] {issue}")
> ```
>
> Expected output:
> ```text
>  [!] FAULT: NavStatus indicates 'Under way' but vessel stationary >2h
>  [!] FAULT: Static draught is 0.0m (uninitialized)
>  [!] FAULT: Invalid ETA timestamp: 02-30 25:00
> ```

## Validation, uncertainty & data quality

In operational watchkeeping, the accuracy of the AIS traffic picture presented on the conning display depends entirely on a sequence of external sensors and manual human inputs. Understanding how uncertainty arises and propagates is essential for maintaining safe separation at sea.

### Error taxonomy and propagation

Errors in the AIS presentation stream fall into three distinct operational categories:

1. **Static and Voyage Data Errors (Human Input Failures):**
   - **Static draught:** Frequently left at zero, set to summer load line marks regardless of ballast condition, or entered in feet instead of decimeters (ITU-R M.1371 specifies draught in tenths of a meter, from 0.1 m to 25.5 m).
   - **Ship dimensions and GPS reference offsets:** The four parameters ($A, B, C, D$) define internal GNSS antenna position relative to bow, stern, port, and starboard ([Chapter 22](ch22-message-catalog.md)). On a 366 m container ship, swapping $A$ and $B$ shifts the rendered vessel center 300 m on large-scale ECDIS displays, corrupting docking operations.
   - **Navigational status:** Studies of coastal AIS feeds indicate that between 30% and 50% of moored or anchored vessels fail to switch their navigational status from *Under way using engine* to *Moored* or *At anchor*, creating severe false-positive clutter in harbor safety algorithms.
2. **Dynamic Data Sensor Errors (Interface Failures):**
   - **Transmitting Heading Device (Gyro) drift:** AIS Message 1 encodes heading with a resolution of $1^\circ$. If the bridge gyrocompass loses synchronization or suffers gimbal drift, the AIS unit transmits erroneous headings without alerting the watch officer. The transponder transmits heading status $511$ (*not available*) only if serial NMEA `$HEHDT` sentences cease entirely.
   - **GNSS antenna multipath and differential dropouts:** An unaugmented GNSS position fix typically carries a 95% horizontal accuracy of 3 to 5 m. However, multipath reflections from container stacks or coastal cranes can cause position shifts exceeding 20 m.
3. **Link-Layer Latencies and Reporting Intervals:**
   - Dynamic data reports are not continuous; they are discrete bursts broadcast across TDMA slots. A Class A vessel steaming at 12 knots updates every 10 s (advancing 62 m between transmissions); during a course alteration, it updates every $3\frac{1}{3}\text{ s}$ (advancing 21 m). A Class B CSTDMA craft moving at 15 knots updates only every 30 s (advancing 231 m). The electronic chart display uses dead reckoning to extrapolate target positions between updates, introducing mathematical lag whenever a vessel maneuvers.

```
+--------------------------------------------------------------------------+
|                     PROPAGATION OF UNCERTAINTY IN AIS                     |
|                                                                          |
|  [Master Gyro / Compass] ---> NMEA $--HDT ---> [ Heading Error: ±1°–5° ] |
|                                                      |                   |
|  [GNSS / DGPS Sensor]   ---> NMEA $--RMC ---> [ Position Error: ±3m–15m] |
|                                                      |                   |
|  [Manual Bridge Entry]  ---> MKD / Keyboard -> [ Voyage Errors: 30%–50%] |
|                                                      |                   |
|                                                      v                   |
|                                         +--------------------------+     |
|                                         | AIS CLASS A TRANSPONDER  |     |
|                                         +-------------+------------+     |
|                                                       |                  |
|                                             VHF Broadcast Lag:           |
|                                             2s to 3 min interval         |
|                                                       |                  |
|                                                       v                  |
|                                         +--------------------------+     |
|                                         | RECEIVING SHIP DISPLAY   |     |
|                                         | - Dead-reckoned latency  |     |
|                                         | - False aspect angles    |     |
|                                         | - Potential collision    |     |
|                                         +--------------------------+     |
+--------------------------------------------------------------------------+
```

### Quantitative verification procedures for watchkeepers

Bridge operating procedures require deck officers to execute systematic cross-checks between independent sensors at the start of each watch:

1. **Heading vs. COG cross-check:** Under steady steaming conditions in waters with negligible tidal stream, verify that the ship's gyro heading matches the GNSS COG within the expected leeway angle (typically $<2^\circ$). A larger discrepancy indicates gyro slippage, severe current set, or an uncalibrated magnetic sensor.
2. **Radar echo to AIS overlay association check:** Select three prominent, steady radar targets across different quadrants. Verify that the AIS target triangle aligns exactly over the center of the radar echo return. A persistent range or bearing offset between the radar blip and the AIS icon indicates incorrect own-ship GPS antenna offsets, geodetic datum mismatch, or target association gating errors under IEC 62388 ([Chapter 51](ch51-charts-enc-ecdis.md)).
3. **MKD voyage parameter audit:** Prior to departure and after every sea buoy or port transit, verify:
   - Present static draught matches actual ship loading calculations to the nearest 0.1 m.
   - Navigational status correctly reflects actual propulsion and mooring status.
   - Destination is entered using standard UN/LOCODE syntax (e.g., `US NYC` or `NLRTM`).
   - Persons on Board (**POB**) count matches the actual muster sheet.

## Software

The following software packages support AIS training, simulator development, data verification, and research:

**Open source:**
- **libais** (Python / C++): Core decoding and encoding library for AIS VHF Data Link payloads. Essential for decoding raw `!AIVDM` sentence logs collected during simulator exercises or vessel audits; does not provide a native real-time graphical bridge interface.
- **OpenCPN** (C++): Full-featured marine chartplotter and navigation software supporting official ENCs, NMEA 0183/2000 data streams, and complete AIS target visualization with CPA/TCPA alarms. Used widely in recreational education and maritime academy training laboratories; lacks formal statutory type approval (IEC 61174) for paperless SOLAS carriage.
- **gpsd** (C / Python): System daemon that monitors GPS, GNSS, and AIS receivers via serial, USB, or network sockets, formatting telemetry into structured JSON. Excellent for multiplexing serial feeds on training testbenches; requires external chart or conning software for graphical target portrayal.

**Free but closed:**
- **VesselFinder / MarineTraffic Mobile Apps** (Android / iOS): Widely used commercial AIS visualization platforms providing crowdsourced global ship tracking. Excellent for general situational awareness and student orientation; subject to significant internet reporting latency (often 5 to 30 minutes behind real-time) and must never be used for tactical bridge navigation.

**Commercial:**
- **Wärtsilä Navi-Trainer professional (NTPro)** (Commercial): High-end Full Mission Bridge Simulator software certified to DNV-ST-0033. Simulates realistic AIS transponder networks, MKD interfaces, radar/ECDIS integration, and dynamic sensor failure injection; high cost and proprietary hardware requirements restrict access to certified maritime academies.
- **Kongsberg K-Sim Navigation** (Commercial): Industry-standard bridge simulator engine providing advanced hydrodynamics, multi-sensor integration, and realistic NMEA/AIS error modeling for pilotage and OICNW certification; requires substantial infrastructure and specialized simulator support staff.
- **Transas / Wärtsilä Pilot PRO** (Commercial / iOS): Professional Portable Pilot Unit application designed for maritime pilots, supporting high-rate AIS pilot plug ingestion, precision docking vectors, and custom ENC overlays; requires commercial licensing and dedicated pilot hardware interfaces.

## Standards & guides

- **IMO Convention:** *International Convention on Standards of Training, Certification and Watchkeeping for Seafarers (STCW), 1978, as amended* (specifically Tables A-II/1 and A-II/2). Governs mandatory minimum competencies for deck officers.
- **IMO Resolution A.1106(29) (2015):** *Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems (AIS)*. The governing international operational guideline for mariners.
- **IMO Model Course 1.34 (Edition 2019 / 2006):** *Automatic Identification Systems (AIS)*. Recommends structured course frameworks and simulator training exercises for maritime academies.
- **IMO Resolution MSC.74(69) Annex 3 (1998):** *Recommendation on Performance Standards for Universal Shipborne Automatic Identification Systems (AIS)*. Baseline equipment performance standard.
- **IMO Circular SN/Circ.227 (2003) & SN.1/Circ.245 (2005):** *Guidelines for the Installation of a Shipborne Automatic Identification System (AIS)*. Governs electrical installation, antenna siting, and pilot plug configuration.
- **IALA Recommendation R0103 (Recommendation V-103) & Model Courses C0103-1 to C0103-5:** *Standards for Training and Certification of VTS Personnel*. Governs VTS operator and supervisor qualification pipelines.
- **IALA Guideline G1149 (Edition 1.1, 2022):** *VTS Training for Deck Officers*. Guides training institutions on educating navigators regarding VTS interactions and shore-based AIS surveillance.
- **IEC 61993-2:2018 (Edition 3.0):** *Maritime navigation and radiocommunication equipment and systems -- Automatic Identification Systems (AIS) -- Part 2: Class A shipborne equipment*. Establishes technical and operational requirements, serial interface sentences, and pilot plug pinouts.
- **IEC 62287-1:2017 & IEC 62287-2:2017:** *Class B shipborne equipment (CSTDMA and SOTDMA)*. Defines performance specifications for recreational and non-mandatory transponders.
- **IEC 62288:2021 (Edition 3.0):** *Presentation of Navigation-Related Information on Shipborne Navigational Displays*. Governs AIS target symbology, heading vectors, and display states.
- **UK MCA Marine Guidance Note MGN 324 (M+F):** *Watchkeeping Safety -- Use of VHF Radio and AIS*. Authoritative flag-state guidance detailing the hazards of VHF-assisted collision avoidance.
- **USCG Navigation and Vessel Inspection Circulars NVIC 12-14 & NVIC 10-14:** *Guidelines on Qualification for STCW Endorsements*. Specifies US practical assessment tasks for operational and management level licenses.

## Pitfalls

- **Treating AIS as an anti-collision device under COLREGs:** Assuming that AIS is recognized as an equivalent replacement for radar/ARPA or visual lookout under Rule 7. AIS data lacks the direct physical sensor verification of radar echoes and cannot legally justify departing from standard collision regulations.
- **Negotiating collision avoidance via VHF radio:** Using AIS vessel names to initiate informal radio passing agreements with crossing or head-on targets. This practice creates ambiguous agreements, introduces language misunderstandings, and causes bridge teams to abandon active radar plotting.
- **Conflating Course Over Ground (COG) with Heading:** Misinterpreting an AIS target's COG vector as its physical heading on an ECDIS display. In heavy cross-currents or windy drift conditions, COG and heading diverge substantially, leading to severe misjudgments of target aspect.
- **Assuming all vessels transmit AIS:** Navigating under the assumption that all traffic appears on the electronic chart display. Small recreational craft, wooden or fiberglass fishing boats, warships, and non-compliant vessels frequently transmit no AIS signal.
- **Overlooking Class B transmission lag:** Calculating close-quarters collision risk against a fast-moving Class B vessel using its electronic chart vector. Class B CSTDMA units may update only once every 30 seconds, leaving target displays obsolete during sharp maneuvers.
- **Blind trust in unvalidated static and voyage data:** Assuming that broadcast navigational status, draught, destination, or vessel type are correct. Surveys show up to half of anchored or moored vessels broadcast incorrect status flags due to poor bridge housekeeping.
- **Failing to configure bridge target filters:** Operating in congested coastal approaches with target display filters disabled, overwhelming the bridge conning display with hundreds of sleeping targets and inducing severe screen clutter and cognitive fatigue.
- **Over-filtering targets in open water:** Setting excessively restrictive target filters (e.g., hiding all targets beyond 3 nautical miles) to declutter displays, inadvertently blinding the bridge team to fast-closing container ships or approaching emergency craft.
- **Ignoring antenna offset errors during docking:** Relying on scaled vessel outlines rendered on ECDIS displays during berthing maneuvers without verifying the vessel's Message 5 antenna dimension offsets ($A, B, C, D$). Inverted offsets can shift a ship icon hundreds of metres from its physical hull.
- **Silencing AIS alarms due to nuisance fatigue:** Disabling or muting bridge CPA/TCPA alarms because of frequent false alarms triggered by anchored vessels in adjacent anchorages, leaving the vessel vulnerable to genuine closing threats.

## Key takeaways

- Maritime training for AIS is grounded internationally in the STCW Convention (Tables A-II/1 and A-II/2), supported by IMO Model Course 1.34 and IMO Resolution A.1106(29).
- Flag-state training regimes diverge substantially: the USCG embeds AIS across modular radar/ECDIS courses and written REC exams; the UK MCA emphasizes oral examination rigor and strict warnings against VHF negotiations (MGN 324); European administrations emphasize Inland AIS and RIS integration.
- Recreational boaters operating Class B transponders receive virtually no mandatory statutory training, leading to pervasive misconceptions regarding system visibility, reporting rates, and static data configuration.
- Maritime pilots utilize Portable Pilot Units (PPUs) interfaced via the standardized Class A AIS pilot plug (IEC 61993-2 / SN/Circ.227), requiring specialized training to diagnose shipboard sensor latency and electrical faults.
- Vessel Traffic Services (VTS) operators qualify through IALA Recommendation R0103 (V-103 model courses), learning shore-side multi-sensor fusion, broadcast scheduling, and virtual AtoN projection.
- Automation bias presents a severe human-factors hazard: the high graphic legibility of AIS targets leads navigators to overestimate data accuracy and neglect visual and radar lookouts (COLREG Rules 5 and 7).
- "VHF/AIS-assisted collisions" occur when navigators use AIS target identification to broker informal passing agreements over the radio, causing confusion and compromising active tracking.
- Advanced simulator training combats automation bias by injecting realistic sensor faults: gyro drift, antenna offset inversion, GNSS spoofing, packet dropout, and conflicting kinematic data.
- Bridge watchkeepers must systematically verify AIS target data against primary radar echoes and optical compass bearings throughout every navigational watch.

## References

- Harati-Mokhtari, A., Wall, A., Brooks, P., Wang, J. (2007). Automatic Identification System (AIS): Data Reliability and the Human Element Implications. *The Journal of Navigation*, 60(1):87–96.
- International Association of Marine Aids to Navigation and Lighthouse Authorities (2019). *VTS Operator Training* (IALA Model Course C0103-1 / V-103/1, Edition 2.0). Saint-Germain-en-Laye: IALA.
- International Association of Marine Aids to Navigation and Lighthouse Authorities (2021). *VTS Manual* (Edition 8.0). Saint-Germain-en-Laye: IALA.
- International Association of Marine Aids to Navigation and Lighthouse Authorities (2022). *VTS Training for Deck Officers* (IALA Guideline G1149, Edition 1.1). Saint-Germain-en-Laye: IALA.
- International Electrotechnical Commission (2013). *IEC 62388:2013: Shipborne Radar -- Performance Requirements, Methods of Testing and Required Test Results* (Edition 2.0). Geneva: IEC.
- International Electrotechnical Commission (2015). *IEC 61174:2015: Electronic Chart Display and Information System (ECDIS) -- Operational and Performance Requirements, Methods of Testing and Required Test Results* (Edition 4.0). Geneva: IEC.
- International Electrotechnical Commission (2018). *IEC 61993-2:2018: Maritime Navigation and Radiocommunication Equipment and Systems -- Automatic Identification Systems (AIS) -- Part 2: Class A Shipborne Equipment* (Edition 3.0). Geneva: IEC.
- International Electrotechnical Commission (2021). *IEC 62288:2021: Presentation of Navigation-Related Information on Shipborne Navigational Displays* (Edition 3.0). Geneva: IEC.
- International Maritime Organization (1978). *International Convention on Standards of Training, Certification and Watchkeeping for Seafarers (STCW), as amended* (STCW Code 2010 Manila Amendments). London: IMO.
- International Maritime Organization (1998). *Recommendation on Performance Standards for Universal Shipborne Automatic Identification Systems (AIS)* (Resolution MSC.74(69) Annex 3). London: IMO.
- International Maritime Organization (2003). *Guidelines for the Installation of a Shipborne Automatic Identification System (AIS)* (Circular SN/Circ.227). London: IMO.
- International Maritime Organization (2015). *Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems (AIS)* (Resolution A.1106(29)). London: IMO.
- International Maritime Organization (2019). *Automatic Identification Systems (AIS)* (IMO Model Course 1.34, 2019 Edition). London: IMO.
- International Telecommunication Union (2014). *Technical Characteristics for an Automatic Identification System Using Time Division Multiple Access in the VHF Maritime Mobile Frequency Band* (Recommendation ITU-R M.1371-5). Geneva: ITU.
- Marine Accident Investigation Branch (2018). *Report on the Investigation of the Collision Between the Bulk Carrier Huayang Endeavour and the Oil Tanker Seafrontier in the Dover Strait on 1 July 2017* (Report No. 11/2018). Southampton: MAIB.
- Maritime and Coastguard Agency (2008). *Navigation: Watchkeeping Safety -- Use of Very High Frequency (VHF) Radio and Automatic Identification System (AIS)* (Marine Guidance Note MGN 324 (M+F)). Southampton: MCA.
- Maritime and Coastguard Agency (2008). *Navigation: Use of Electronic Navigation Aids* (Marine Guidance Note MGN 379 (M+F)). Southampton: MCA.
- National Transportation Safety Board (2019). *Collision Between Bulk Carrier Amber L and Towing Vessel John R. Rice, Lower Mississippi River* (Marine Accident Brief MAB-19/27). Washington, D.C.: NTSB.
- United States Coast Guard (2014). *Guidelines on Qualification for STCW Endorsements as Officer in Charge of a Navigational Watch on Vessels of 500 GT or More* (Navigation and Vessel Inspection Circular NVIC 12-14). Washington, D.C.: USCG.
- United States Coast Guard (2014). *Guidelines on Qualification for STCW Endorsements as Master or Chief Mate on Vessels of 3,000 GT or More* (Navigation and Vessel Inspection Circular NVIC 10-14). Washington, D.C.: USCG.
