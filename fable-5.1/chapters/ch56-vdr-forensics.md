# Chapter 56 — Voyage Data Recorders and forensic reconstruction

> **Part VIII — Charts, bridge systems, and mariners.** How shipboard Voyage Data Recorders capture raw navigational telemetry, and how forensic investigators extract, synchronize, and fuse on-board sensor logs with shore-based and satellite AIS to reconstruct maritime casualties for marine accident investigation boards and admiralty courts.

**In this chapter.** You will learn the statutory frameworks, digital interfaces, and forensic methodologies required to extract and reconstruct maritime casualties from Voyage Data Recorders (**VDRs**), Simplified VDRs (**S-VDRs**), and multi-source Automatic Identification System (**AIS**) telemetry. You will examine the International Maritime Organization (**IMO**) carriage mandates and International Electrotechnical Commission (**IEC**) technical standards—specifically Resolution MSC.333(90), IEC 61996-1, and IEC 61996-2—governing protective capsule survivability and mandatory sensor channels. You will trace how raw AIS data is ingested via IEC 61162-1, IEC 61162-2, and IEC 61162-450 Ethernet networks, identifying systemic failure modes including missing target streams, silent buffer truncation, and baud rate mismatch. You will learn rigorous forensic protocols for data preservation, physical and logical extraction, timestamp reconciliation across unsynchronized clocks, and track interpolation. You will analyze landmark marine casualty investigations—including the *El Faro* sinking, the *Sanchi* collision, and the *Dali* bridge allision—evaluating how multi-sensor fusion establishes ground truth. Finally, you will execute programmatic forensic pipelines using Python and render time-accurate 3D incident animations in Blender, while navigating strict evidentiary standards for admiralty litigation.

## 56.1 The Voyage Data Recorder in the maritime safety architecture

The modern **Voyage Data Recorder** (**VDR**) serves as the maritime counterpart to aviation flight data and cockpit voice recorders. Codified under Regulation 20 of Chapter V of the International Convention for the Safety of Life at Sea (**SOLAS**), a VDR maintains an objective record of shipboard parameters, mechanical commands, bridge audio, navigational telemetry, and environmental interactions during marine accidents.

Unlike commercial aircraft flight recorders, which log compressed bus frames across dedicated avionics channels, maritime VDRs operate within a federated bridge architecture. A ship's navigational bridge brings together disparate subsystems: Global Navigation Satellite System (**GNSS**) receivers, gyrocompasses, speed logs, radars, Electronic Chart Display and Information Systems (**ECDIS**), engine automation interfaces, rudder angle indicators, bridge microphones, and VHF radiotelephones. Each subsystem operates as an autonomous node communicating over standardized serial links or local area networks.

The VDR functions as a central data sink, listening to these distributed broadcasts, packetizing them with precise temporal indexing, and streaming the synchronized archive to survivable memory capsules. Following a casualty—whether a collision, allision, grounding, or structural loss—retrieved VDR data provides safety investigation boards, classification societies, and admiralty litigators with the empirical foundation required to determine root causes.

AIS plays a dual role in this architecture. On board the vessel, the Class A AIS transponder broadcasts dynamic position reports (Messages 1, 2, 3), static voyage parameters (Message 5), and safety messages (Messages 12, 14) over the VHF Data Link (**VDL**) to nearby craft and shore stations, as detailed in [Chapter 20](ch20-architecture-and-station-classes.md) and [Chapter 22](ch22-message-catalog.md). Concurrently, the transponder decodes the VDL radio environment, generating a serial stream of `!AIVDM` sentences representing all traffic within radio line-of-sight (typically 15–25 nautical miles). When recorded by the VDR, this stream preserves an external radar-independent record of the surrounding marine domain.

```
       +-------------------------------------------------------------+
       |                  BRIDGE SENSOR SUBSYSTEMS                   |
       |  Gyrocompass    GNSS Receiver    Speed Log     Class A AIS  |
       |  (HEHDT)        (GPRMC/GPGGA)    (VMVHW)       (!AIVDM/O)   |
       +-------+---------------+--------------+--------------+-------+
               |               |              |              |
               | IEC 61162-1   | IEC 61162-1  | IEC 61162-1  | IEC 61162-2
               | (4,800 bps)   | (4,800 bps)  | (4,800 bps)  | (38,400 bps)
               ▼               ▼              ▼              ▼
       +-------------------------------------------------------------+
       |                 DATA ACQUISITION UNIT (DAU)                 |
       | - High-density RS-422 isolated serial concentrator          |
       | - Audio mixer (microphones + VHF radiotelephone)            |
       | - Video frame grabbers (ECDIS / Radar video capture)        |
       | - IEC 61162-450 Lightweight Ethernet (LWE) interface        |
       | - Internal system clock synchronized to GNSS UTC            |
       +------------------------------+------------------------------+
                                      │ Encrypted / Authenticated
                                      ▼
       +-------------------------------------------------------------+
       |                 SURVIVABLE MEMORY CAPSULES                  |
       |  Fixed Hardened Capsule     Float-Free Capsule              |
       |  (3,000 g shock; 6,000 m    (Hydrostatic release; 406 MHz   |
       |   depth; min 48 h log)       beacon; min 48 h log)          |
       |                                                             |
       |  Long-Term Internal Storage (DAU non-volatile: min 30 days) |
       +-------------------------------------------------------------+
```

## 56.2 Regulatory mandates and technical standards

The technical requirements governing Voyage Data Recorders have evolved over three decades in response to investigation findings following major maritime disasters.

### 56.2.1 Statutory carriage requirements: SOLAS Chapter V Regulation 20

Under SOLAS Chapter V, Regulation 20, carriage requirements depend on vessel type, gross tonnage (**GT**), and construction date:
1. **Passenger ships:** All passenger vessels regardless of size constructed on or after 1 July 2002 must carry a compliant VDR. Existing passenger ships constructed before 1 July 2002 were required to retrofit prior to their first scheduled safety survey.
2. **Cargo ships $\ge 3,000$ GT:** Cargo vessels of 3,000 gross tonnage and upwards constructed on or after 1 July 2002 must carry a fully compliant VDR.
3. **Existing cargo ships (The S-VDR Compromise):** Cargo ships built before 1 July 2002 were permitted to fit a Simplified Voyage Data Recorder (**S-VDR**) under IMO Resolution MSC.163(78). The S-VDR reduced retrofit costs by omitting requirements for watertight hull door indicators, thrusters, rudder orders, and main engine telemetry, focusing strictly on bridge audio, VHF radio, GNSS position, speed, heading, and radar video.

### 56.2.2 IMO Performance Standards: A.861(20) to MSC.333(90)

The baseline operational specifications are established by two benchmark IMO resolutions:
- **Resolution A.861(20)** (Adopted November 1997): Governed VDR systems installed prior to 1 July 2014. It required recording date, time, GNSS position, speed over ground, gyro heading, bridge audio, VHF communications, radar data, echo sounder depth, main alarms, rudder angle, engine order and response, hull opening status, and watertight/fire doors. Crucially, **Resolution A.861(20) did not mandate recording of AIS telemetry**, nor did it mandate ECDIS recording. Systems installed under A.861(20) were only required to maintain a **12-hour continuous recording duration** in a single fixed hardened capsule.
- **Resolution MSC.333(90)** (Adopted 22 May 2012): Revised the VDR performance standard for installations on or after **1 July 2014**:
  1. **Mandatory AIS recording:** Clause 5.5.11 mandates that "all AIS data should be recorded." This requires logging both own-ship transmissions (`!AIVDO`) and all received target reports (`!AIVDM`), as well as interrogation and control messages.
  2. **Mandatory ECDIS recording:** The VDR must record the electronic chart display in use, logging screen capture snapshots (minimum 1 frame every 15 seconds) or vector chart configuration databases, including ENC chart edition, safety contours, and displayed target overlays.
  3. **Dual capsule architecture:** The system must stream data to two survivable capsules: a **fixed hardened capsule** and a **float-free capsule** deployed with an integrated hydrostatic release and satellite localization beacon.
  4. **Expanded retention window:** Capsule retention was increased to a minimum of **48 hours**. Furthermore, the Data Acquisition Unit must incorporate internal non-volatile storage retaining at least **30 days** of voyage telemetry.
  5. **Electronic inclinometers:** Mandatory logging of ship heel, roll period, and pitch angles.

### 56.2.3 Testing specifications: IEC 61996-1 and IEC 61996-2

The international test methods and electrical standards that turn IMO resolutions into certified marine hardware are produced by IEC Technical Committee 80:
- **IEC 61996-1:2013** (*VDR performance requirements, methods of testing and required test results*, incorporating Amendment 1:2021): Translates MSC.333(90) into formal type-approval tests. It specifies electrical isolation, continuous cyclic buffer integrity, audio frequency response (150 Hz to 3.5 kHz across bridge microphones), radar image compression codecs, and mechanical survival tests for the hardened capsule.
- **IEC 61996-2:2007** (*Simplified voyage data recorder (S-VDR)*): Governs equipment built under MSC.163(78).

To survive catastrophic casualties, the fixed protective capsule is subjected to environmental testing defined in IEC 61996-1:
- **Impact shock:** A mechanical shock impulse of $3,000\ g$ ($30,000\ \text{m/s}^2$) for 5 milliseconds.
- **Penetration resistance:** A hardened steel pin weighing 250 kg dropped from a height of 3 meters.
- **High-temperature fire:** Exposure to continuous flames at $260^\circ\text{C}$ for 10 hours, and a high-temperature flash fire of $1,100^\circ\text{C}$ for 1 hour.
- **Deep-sea hydrostatic immersion:** Continuous submersion at a hydrostatic pressure of 60 MPa (simulating water depth of 6,000 meters) for 30 days.
- **Underwater locating beacon:** An acoustic pinger operating at $37.5\ \text{kHz} \pm 1\ \text{kHz}$, triggered automatically upon water immersion, capable of transmitting for at least 90 days (increased from 30 days under older A.861(20) specifications).

## 56.3 AIS as a recorded channel

Recording AIS telemetry aboard commercial vessels provides a continuous external check against internal bridge logs.

### 56.3.1 Own-ship vs target traffic logging

A compliant installation records two distinct categories of AIS traffic:
1. **Own-ship telemetry (`!AIVDO`):** Sentences output by the transponder on its presentation interface representing its own static metadata, GNSS antenna offsets, Voyage Static Data (**VSD**), and dynamic position broadcasts. This logs what the host vessel projected over the radio network.
2. **External target telemetry (`!AIVDM`):** Sentences decoded from the VDL representing external vessels, base stations, search and rescue aircraft, virtual Aids to Navigation (**AtoN**), and Search and Rescue Transponders (**AIS-SART**).

Under MSC.333(90) §5.5.11, the VDR must record *all* received AIS messages without filtering. In congested waterways such as the Dover Strait or Singapore Strait, the Class A presentation interface can sustain burst traffic exceeding 25 to 40 sentences per second.

```
       +--------------------------------------------------------------+
       |                  CLASS A AIS TRANSPONDER                     |
       |  [Antenna Rx] ──► RF Demodulator (161.975 / 162.025 MHz)     |
       |                         │                                    |
       |                         ▼                                    |
       |                Presentation Interface                        |
       |         IEC 61162-2 RS-422 Serial (38,400 baud)              |
       |              or IEC 61162-450 Ethernet                       |
       +-------------------------+------------------------------------+
                                 │
                                 │ Output sentences:
                                 │ !AIVDM (all targets on VDL)
                                 │ !AIVDO (own-ship transmissions)
                                 │
                                 ▼
       +--------------------------------------------------------------+
       |                 VDR DATA ACQUISITION UNIT                    |
       |  Serial RX Buffer (Hardware FIFO -> OS ring buffer)          |
       |  ├─► Checksum validation (XOR parity)                        |
       |  ├─► Timestamp assignment (DAU UTC microsecond counter)      |
       |  └─► Encapsulation into log blocks                           |
       +--------------------------------------------------------------+
```

### 56.3.2 Physical and logical interface topologies

AIS transponders interface with the VDR Data Acquisition Unit across three primary electrical topologies:
- **IEC 61162-2 High-Speed Serial:** Operates over shielded twisted pair using balanced differential RS-422 signaling at **38,400 bit/s** (8 data bits, 1 stop bit, no parity). This dedicated presentation interface is standard on vessels built between 2002 and 2018. Because standard bridge serial links operate under IEC 61162-1 at 4,800 bit/s, connecting an AIS interface to an unconfigured 4,800 baud DAU port results in framing errors and total data loss.
- **IEC 61162-450 Ethernet ("Lightweight Ethernet"):** On integrated bridges conforming to IEC 61162-460, bridge devices broadcast NMEA sentences encapsulated in UDP multicast datagrams. The AIS transponder multicasts `!AIVDM` and `!AIVDO` datagrams onto designated multicast groups (such as `239.192.0.2` for target data or `239.192.0.4` for VDR logging, typically on UDP port 60002 or 60004). Each packet begins with the 6-byte token `UdPbC\0`, followed by a TAG block containing monotonic sequence counters and talker IDs.
- **Dual-channel multiplexer configurations:** On refitted tonnage, bridge engineers frequently routed the AIS presentation interface into an NMEA 0183 multiplexer combining GPS, gyro, and AIS into a single serial feed to the VDR. Multiplexer buffer starvation under heavy radio loads represents a prevalent cause of missing telemetry in marine casualty records.

> **Definitions that bite.**
> - **AIVDM:** An NMEA 0183 / IEC 61162-1 transport sentence carrying an AIS message received over the radio link from an external transmitting station.
> - **AIVDO:** An NMEA 0183 / IEC 61162-1 transport sentence carrying the transponder's *own* broadcast information—what the host vessel sent out across the VHF Data Link.
> - **Fixed Hardened Capsule:** A high-survivability container permanently secured to the vessel's exterior bridge superstructure, engineered to withstand deep-sea hydrostatic pressure, structural crush, and severe fire.
> - **Float-Free Capsule:** An exterior enclosure designed to hydrostatically disengage from a sinking vessel before reaching a depth of 4 meters, floating to the surface while activating an internal 406 MHz COSPAS-SARSAT emergency locator beacon and AIS locator transmitter.
> - **Presentation Interface (PI):** The primary bi-directional communications port on a Class A transponder (IEC 61162-2, 38,400 baud) used to exchange NMEA sentences with ECDIS, radar, and VDR systems.

## 56.4 Extraction, chain of custody, and evidentiary standards

The integrity of a maritime safety or judicial investigation hinges on the rigor of the physical and digital recovery operation.

### 56.4.1 Capsule recovery and physical preservation

In minor incidents where the ship remains afloat, data preservation is initiated via the VDR's manual "Save" button or maintenance terminal. This instruction freezes the current 48-hour buffer and writes the contents to non-volatile flash partitions, preventing the cyclic buffer from overwriting critical pre-incident telemetry.

In catastrophic sinkings, salvage teams recover the capsules:
1. **Float-free capsule retrieval:** The hydrostatic release mechanism cuts its physical tether at a depth of 1.5 to 4 meters. The buoyant unit floats to the surface and begins broadcasting a 406 MHz alert. Responders home in on the capsule using aircraft, AIS receivers, or direction-finding equipment ([Chapter 35](ch35-direction-finding-geolocation.md)).
2. **Fixed capsule sub-sea recovery:** If the float-free unit fails to deploy, salvage teams deploy Remotely Operated Vehicles (**ROVs**) equipped with acoustic receivers tuned to the $37.5\ \text{kHz}$ pinger. Once located, the ROV unbolts or cuts the capsule from its mounting bracket on the compass deck.
3. **Desalination and physical stabilization:** If the capsule's watertight seal has been breached, immediate washing with deionized water is mandatory. Allowing seawater to dry within recovered circuit boards causes rapid salt crystallization, tearing surface-mount traces and corroding solid-state memory dies. Salvage protocols dictate immersing the recovered memory module in fresh demineralized water baths until laboratory disassembly.

```
       +--------------------------------------------------------------+
       |                     CASUALTY OCCURRENCE                      |
       +------------------------------+-------------------------------+
                                      │
                   Is vessel floating and powered?
                    ├──► YES: Actuate Bridge "Backup / Save" Button
                    │         Export via maintenance Ethernet/USB
                    │
                    └──► NO: Vessel Sunk / Superstructure Damaged
                              │
                              ├─► Float-free deployed: Search & recover
                              │   via 406 MHz / AIS beacon
                              │
                              └─► Fixed capsule submerged: ROV homing on
                                  37.5 kHz pinger -> Cut & hoist
                                      │
                                      ▼
       +--------------------------------------------------------------+
       |                PHYSICAL EVIDENCE PRESERVATION                |
       |  - Document serial numbers, tamper seals, physical trauma    |
       |  - If breached: Rinse in demineralized water, keep submerged |
       |  - Formal Chain of Custody manifest executed with flag state |
       +------------------------------+-------------------------------+
                                      │
                                      ▼
       +--------------------------------------------------------------+
       |                 CONTROLLED LABORATORY EXTRACTION             |
       |  - Cleanroom inspection and module bake-out                  |
       |  - Write-blocked hardware imaging (NAND flash bit-stream)    |
       |  - Generate cryptographically secure hashes (SHA-256)        |
       |  - Master bit-stream locked; all analysis on working copies  |
       +--------------------------------------------------------------+
```

### 56.4.2 Bit-level logical acquisition and hashing

Once inside an accredited casualty forensics facility (such as those maintained by the US NTSB, UK MAIB, or German BSU), extraction proceeds under strict protocols:
- **Write-blocked imaging:** Forensic engineers connect directly to the memory controller or desolder NAND flash chips (chip-off forensics). The memory is imaged using certified hardware write-blockers to generate bit-for-bit physical disk clones (`.raw` or `.dd` images).
- **Cryptographic hashing:** Prior to analysis, the investigator calculates cryptographic digests—specifically **SHA-256** hashes—of the primary bit-stream. Any subsequent copy generated for court proceedings or expert witnesses must verify identically against this baseline hash.
- **Manufacturer playback toolchains:** Marine VDRs employ proprietary file formats (e.g., Danelec, Furuno, JRC, Consilium, Sperry Marine). Extraction tools decrypt and unpack the archive into discrete streams: audio files (`.wav`), radar/ECDIS frame sequences, and tabular sensor records containing timestamped NMEA 0183 sentences.

### 56.4.3 Chain of custody and admiralty evidentiary rules

In maritime liability litigation, digital logs are scrutinized under strict rules of evidence. Under Rule 901 of the Federal Rules of Evidence (**FRE**) in the United States, and equivalent common-law doctrines in English Admiralty proceedings, the proponent of digital telemetry must prove that the evidence is authentic, free from tampering, selective erasure, or extraction artifacts.

> **Legal note.**
> Under international maritime law codified in the IMO Code of the International Standards and Recommended Practices for a Safety Investigation into a Marine Casualty or Marine Incident (**Casualty Investigation Code**, Resolution MSC.255(84)), marine safety accident investigations conducted by statutory bodies (NTSB, MAIB, TSB, BSU) are non-judicial. Their purpose is the prevention of future casualties, not the apportionment of civil liability or criminal blame.
> 
> In many jurisdictions, bridge voice recordings (**VDR audio**) are protected by statutory confidentiality privileges and cannot be entered directly into civil liability lawsuits without court order. However, **navigational sensor records—specifically NMEA logs, gyro headings, radar captures, and AIS telemetry—are non-privileged factual data**. They are routinely subpoenaed, admitted into evidence, and relied upon by admiralty judges to apportion fault under the International Regulations for Preventing Collisions at Sea 1972 (**COLREGs**), as demonstrated in landmark cases such as *Ever Smart v. Alexandra 1* [2021] UKSC 6 ([Chapter 17](ch17-legal-issues-and-court-cases.md)).

## 56.5 Multi-source forensic fusion: VDR, shore, and satellite AIS

A single shipboard VDR log provides an inward-looking snapshot of an incident. In modern marine casualty forensics, investigators correlate on-board VDR records with independent external observation layers:
- **Shipboard VDR:** Continuous 1-second dynamic updates; captures internal helm orders, gyro, and bridge audio; subject to shipboard power loss.
- **Shore-based AIS:** High cadence (2–10 seconds); coastal coverage (20–40 nmi from shore); independent of vessel power; referenced to atomic UTC standards.
- **Satellite AIS:** Irregular cadence (15 minutes to hours); global ocean coverage; subject to orbital revisits and message packet collisions.
- **Harbor Surveillance Radar:** Continuous sweeps (2.5–3.0 seconds); tracks uncooperative targets, wooden craft, and vessels running without AIS.

### 56.5.1 Ingestion and alignment across disparate streams

Forensic fusion requires resolving four primary dimensions of divergence:
1. **Clock drift and epoch synchronization:** VDR internal clocks drift if the Data Acquisition Unit failed to synchronize against the GNSS receiver's 1PPS signal or `GPRMC` sentence. Shore-based AIS networks lock ingest servers directly to atomic UTC standards. Satellite downlinks stamp records upon orbital reception, adding propagation delays and ground-station ingest latencies.
2. **Coordinate frame and geodetic reference:** Modern GNSS systems report coordinates referenced to WGS-84. However, position reports originating from differential beacons or regional satellite augmentations (BeiDou, GLONASS) may carry subtle offsets if local datum conversions were improperly configured.
3. **Sensor location vs vessel reference points:** A ship is an extended physical polygon, not a dimensionless point. An AIS transponder broadcasts coordinates derived from its assigned GNSS antenna. If the VDR logs gyro heading and speed from a doppler log in the bow, while the AIS GNSS antenna is mounted on the radar mast aft of the bridge, the two telemetry streams will diverge during sharp maneuvers. Reconstructing physical hull clearances requires applying static dimension offsets from AIS Message 5 (`to_bow`, `to_stern`, `to_port`, `to_starboard`), as detailed in [Chapter 22](ch22-message-catalog.md).
4. **Target association and track correlation:** External shore logs record the host vessel's MMSI from the outside. The VDR logs own-ship data via `!AIVDO` and surrounding ships via `!AIVDM`. Matching VDR-recorded target sentences against external shore logs allows investigators to verify whether the target vessel experienced radio desynchronization, packet dropouts, or power interruptions prior to collision.

## 56.6 Case files: Dissecting landmark casualty reconstructions

Marine accident investigation boards have established gold-standard precedents in applying VDR and AIS data fusion to resolve contested casualties.

> **Case file: The loss of S.S. El Faro (NTSB/MAR-17/01).**
> On 1 October 2015, the 790-foot US cargo ship S.S. *El Faro* sank during Hurricane Joaquin northeast of Acklins and Crooked Island, Bahamas, resulting in the loss of all 33 crew members. The vessel came to rest on the ocean floor at a depth of 15,400 feet ($4,690\ \text{m}$).
> 
> In August 2016, following a ten-month undersea search utilizing US Navy CURV-21 ROVs, salvage teams recovered the fixed hardened VDR capsule (a Sperry Marine VoyageMaster VDR). Despite ten months immersed at hydrostatic pressures exceeding $47\ \text{MPa}$, forensic specialists at the NTSB laboratory successfully extracted the internal flash memory without data loss.
> 
> The capsule yielded 26 hours of continuous bridge voice audio, gyro heading, engine orders, and anemometer wind data. By correlating recovered VDR gyro headings and wind observations with external satellite AIS reports, satellite weather imagery, and high-resolution weather models, investigators established the ship's deteriorating speed profile, wind-induced heel angles, and the sequence of hold flooding that culminated in main boiler shutdown and loss of stability.

> **Case file: The Sanchi / CF Crystal collision.**
> On 6 January 2018, the Suezmax tanker M/T *Sanchi*, laden with 111,300 metric tons of natural gas condensate, collided with the bulk carrier M/V *CF Crystal* in the East China Sea, 160 nautical miles off Shanghai. The collision ruptured *Sanchi*'s forward starboard tanks, igniting an inferno that consumed the tanker and killed all 32 mariners on board. *CF Crystal* suffered bow damage but remained afloat, and its crew survived.
> 
> Because *Sanchi* drifted for eight days enveloped in flames before sinking in 115 meters of water, salvage teams could only retrieve the float-free VDR capsule. However, *CF Crystal*'s VDR was secured immediately upon reaching port.
> 
> The joint investigation hinged on synchronizing *CF Crystal*'s VDR telemetry with regional shore-based and satellite AIS archives. The VDR recorded *CF Crystal*'s gyro heading, radar targets, and bridge conversations, confirming an open-sea crossing situation under COLREGs Rule 15. The AIS tracking records proved *Sanchi* was on a course of $358^\circ$ at 10.4 knots, while *CF Crystal* was steering $217^\circ$ at 13.2 knots. Crucially, forensic track fusion demonstrated that *CF Crystal* altered course $5^\circ$ to starboard 15 minutes before the collision to resume its planned route, altering relative geometry and eliminating CPA expansion, while neither vessel established radar target tracking or sounded sound signals, exposing mutual look-out failure under Rule 5 and improper collision assessment under Rule 7.

> **Case file: The M/V Dali / Francis Scott Key Bridge allision (NTSB DCA24MM031).**
> On 26 March 2024, the 9,962 TEU container ship M/V *Dali* suffered electrical blackouts while outbound from the Port of Baltimore, losing steering control and striking Pier 17 of the Francis Scott Key Bridge. The collision collapsed the steel truss spans within seconds, severing Interstate 695 and causing the deaths of six highway construction workers.
> 
> NTSB forensic investigators boarded the vessel within hours, securing the Data Acquisition Unit of the ship's Consilium VDR. The VDR recorded own-ship AIS broadcasts, bridge audio, rudder angles, engine speed, and electrical alarms.
> 
> Aligning the VDR's internal audio channel with external USCG NAIS base station logs revealed the timeline down to sub-second precision:
> 1. At 01:24:59 EDT, the VDR ceased recording shipboard sensor telemetry (gyro, rudder, engine RPM) when main electrical breakers tripped, plunging the vessel into a blackout.
> 2. The VDR's internal uninterruptible power supply (**UPS**) maintained bridge audio recording, capturing pilot commands and emergency VHF calls.
> 3. External USCG shore-based AIS stations maintained continuous reception of the ship's auxiliary-powered transponder broadcasts, providing investigators with ground-truth trajectory ($107^\circ$ at ~8 knots) during the blackout intervals where internal sensor logging was paralyzed.
> 4. At 01:26:02, auxiliary generators re-energized bridge emergency switchboards, and the VDR resumed sensor logging, capturing the emergency anchor drop order and rudder commands moments before the bow struck the bridge pier at 01:28:45.

## 56.7 Technical pitfalls in forensic data acquisition

Forensic engineers routinely encounter recurring points of failure when analyzing recorded telemetry from marine casualties:

1. **Multiplexer buffer overflow and dropped multi-sentence packets:** Class A static messages (Message 5) and binary payloads require two-sentence NMEA encapsulation (`!AIVDM,2,1,...` and `!AIVDM,2,2,...`), as detailed in [Chapter 26](ch26-interfaces-and-logging.md). In high-density waterways, bridge multiplexers drop individual sentences during burst traffic. When sentence 1 is dropped, downstream forensic parsers reject orphan sentence 2 due to incomplete sequence numbering, creating artificial gaps in vessel identification records.
2. **Serial baud rate mismatch (4,800 vs 38,400 baud):** IEC 61162-1 specifies 4,800 bit/s, whereas IEC 61162-2 requires 38,400 bit/s for AIS. Connecting an AIS transponder to an unconfigured 4,800 baud DAU serial port causes framing errors and total data corruption.
3. **Uninterruptible Power Supply (UPS) battery failure:** Under MSC.333(90), the VDR must be backed by an internal battery supply powering the DAU and bridge microphones for at least **2 hours** following total electrical failure. Degraded batteries fail prematurely; when the ship loses auxiliary power, the VDR instantly shuts down, leaving investigators blind during an evolving crisis.
4. **Uncalibrated system clock drift:** If the VDR internal real-time clock (**RTC**) does not continuously synchronize against GNSS `ZDA` or `RMC` sentences, it drifts by seconds per month. When reconstructing collisions involving high-speed craft ($>30\ \text{knots}$), a 5-second clock error displaces the reconstructed impact point by over 75 meters.
5. **Transponder antenna offset omission:** Failing to account for GNSS antenna reference offsets (`to_bow`, `to_stern`, `to_port`, `to_starboard`) recorded in Message 5 results in positioning errors exceeding the width or length of the vessel. For a 400-meter container ship, assuming the antenna sits at the vessel's geometric center introduces an instantaneous longitudinal displacement of up to 150 meters.
6. **False-positive target disappearance from RF slot starvation:** In congested anchorages, receiving transponders fail to decode distant targets due to TDMA slot collisions or local RF interference, as explored in [Chapter 30](ch30-network-loading-packet-loss.md) and [Chapter 31](ch31-noise-and-interference.md). Novice investigators frequently misinterpret these missing `!AIVDM` records as deliberate AIS switch-offs by the target vessel.
7. **Loss of heading data yielding inverted drift models:** When a target ship transmits heading as 511 (not available), naïve visualization software defaults to Course Over Ground (**COG**) as a proxy for ship orientation. In strong cross-currents or drift conditions, this creates a false perception of the vessel steaming under engine power, obscuring actual crab angles and leeway drift.
8. **Inappropriate spline over-smoothing:** Reconstructing trajectories by applying cubic spline interpolation across sparse Class B AIS reports introduces severe physical overshoot, producing mathematically smooth paths that violate hydrodynamic constraints.

## 56.8 3D reconstruction and animation pipelines

Visualizing complex casualties for courts, arbitrators, and technical investigators demands transforming tabular telemetry into physically and cartographically accurate animations. As introduced in [Chapter 45](ch45-processing-software.md), the open-source 3D Digital Content Creation suite **Blender** provides an ideal scientific toolchain through its headless Python API (`bpy`).

### 56.8.1 Local coordinate projection in 3D float32 space

Standard 3D graphics engines, including Blender, utilize single-precision 32-bit floating point arithmetic (`float32`) for vertex coordinates. Feeding raw geographic degrees (e.g., latitude $42.33958^\circ$, longitude $-70.91902^\circ$) directly into a 3D scene introduces catastrophic floating-point rounding jitter and vertex tearing.

To maintain sub-centimeter geometric precision across a 20-nautical-mile casualty domain, the pipeline projects all geographic coordinates onto a **local tangent plane** centered on the incident origin $(\phi_0, \lambda_0)$ using an equirectangular approximation:

$$x = R_{\text{earth}} \cdot (\lambda - \lambda_0) \cdot \cos(\phi_0) \cdot \frac{\pi}{180^\circ}$$

$$y = R_{\text{earth}} \cdot (\phi - \phi_0) \cdot \frac{\pi}{180^\circ}$$

where $R_{\text{earth}} = 6{,}371{,}000\ \text{m}$. Within 20 nautical miles of the origin, geometric distortion remains below $0.01\%$, providing rigorous spatial fidelity without GIS overhead.

### 56.8.2 Hull scaling, orientation, and sightline analysis

Reconstructing a collision requires representing vessels as scaled polygonal bounding boxes matching their physical hull geometries, rather than dimensionless point markers:
1. **Dimension extraction:** The pipeline parses AIS Message 5 parameters (`dimension_to_bow`, `dimension_to_stern`, `dimension_to_port`, `dimension_to_starboard`) to establish overall length $L$, beam $B$, and the exact offset of the GNSS antenna relative to the physical hull envelope.
2. **Heading vs Course Over Ground:** Hull orientation (yaw) must be driven strictly by the vessel's **True Heading** (from gyrocompass or AIS dynamic reports). If heading is unavailable (value 511), the script falls back to COG, flagging the orientation vector in the visualization metadata.
3. **Linear interpolation:** Keyframes must be interpolated using **linear motion models** (`kp.interpolation = "LINEAR"`). Standard cubic or Bézier interpolation generates fictitious acceleration loops and rotational wobble between sparse telemetry fixes.
4. **Bridge visibility cones:** Parenting a virtual camera to the height and coordinates of the bridge conning position allows investigators to render the watchstander's exact sightline, visually establishing whether an oncoming vessel was obscured by deck cranes, container stacks, or structural blind spots under SOLAS Chapter V Regulation 22.

> **Try it.**
> Execute the headless Blender animation script located at `code/viz/blender_ais_animation.py` using synthetic multi-vessel casualty data. This generates a keyframed 3D reconstruction scene in Blender, mapping real-world AIS trajectories into local Euclidean coordinates:
>
> ```bash
> # Ensure the environment is activated and execute the headless renderer
> python3 code/viz/blender_ais_animation.py \
>     --csv data/samples/synthetic_harbor_truth.csv \
>     --out /tmp/casualty_reconstruction.blend \
>     --seconds-per-frame 5.0 \
>     --origin 42.25 -70.70
> ```
>
> Inspecting the generated `.blend` file verifies that each vessel is instantiated with true physical dimensions, linear keyframe interpolation, and heading-driven yaw rotation.

## Then & now

- **⟨H⟩ 1912:** Following the loss of the R.M.S. *Titanic*, the initial 1914 SOLAS convention mandates maritime safety radio watches, but accident investigation relies entirely on human memory, handwritten bridge logbooks, and salvage testimony.
- **⟨H⟩ 1974:** SOLAS 1974 establishes modern safety conventions; bridge operations remain paper-centric, with navigational records preserved via mechanical course recorders and paper echo-sounder rolls.
- **⟨+⟩ 1997 (IMO Res. A.861(20)):** The IMO adopts the first international performance standards for shipborne Voyage Data Recorders, mandating a 12-hour recording loop in a single fixed hardened capsule for passenger ships and large cargo vessels (effective July 2002). AIS is not included in the mandatory data suite.
- **⟨+⟩ 2004 (IMO Res. MSC.163(78)):** The IMO introduces the Simplified VDR (S-VDR) performance standard, offering an economical retrofit path for pre-2002 cargo ships by recording essential sensors (GNSS, gyro, radar, audio) while waiving hull stresses, doors, and engine automation channels.
- **⟨H⟩ 2004 (SOLAS Accelerated Carriage):** Post-9/11 maritime security mandates accelerate universal Class A AIS carriage across international commercial shipping, establishing the open VHF broadcast network that forms the basis of modern external traffic tracking.
- **⟨+⟩ 2012 (IMO Res. MSC.333(90)):** The IMO comprehensively overhauls VDR standards, mandatory for new installations from 1 July 2014. The standard requires **mandatory recording of all AIS data**, introduces dual fixed and float-free capsules, expands capsule retention to 48 hours, mandates 30 days of internal storage, and requires ECDIS display screen logging.
- **⟨+⟩ 2021 (IEC 61996-1 AMD1:2021):** IEC updates VDR testing protocols, integrating IEC 61162-450 Ethernet network logging, cyber security gateways under IEC 61162-460, and modernized digital video acquisition protocols.
- **⟨+⟩ 2026 (Present):** Marine casualty investigations routinely synthesize internal 48-hour high-bandwidth VDR records with multi-constellation satellite AIS archives, shore-based coastal radar, and 3D hydrodynamic simulation pipelines to establish definitive judicial ground truth.

## Validation, uncertainty & data quality

Forensic reconstruction demands quantifying the mathematical and spatial uncertainty associated with every recorded data point. A single coordinate fix in an investigation report represents a probability distribution bounded by sensor physics, network latency, and spatial geometry.

### Error propagation and uncertainty models

To determine the spatial uncertainty of a reconstructed vessel track, investigators apply a layered error model:

1. **GNSS positioning uncertainty ($\sigma_{\text{pos}}$):** Unaugmented commercial marine GNSS operating without differential corrections provides a 95% horizontal accuracy circle of approximately 2.5 to 5.0 meters ($2\sigma$). When satellite geometry degrades (High Horizontal Dilution of Precision, $\text{HDOP} > 2.5$), positioning uncertainty expands to 10–25 meters.
2. **Antenna lever-arm transformation ($\vec{r}_{\text{offset}}$):** If the GNSS antenna is located at vector offset $(x_a, y_a)$ relative to the vessel's center of gravity or pivot point, the true position of the center of gravity $\vec{P}_{\text{cg}}$ as a function of vessel heading $\psi$ is:

$$\vec{P}_{\text{cg}} = \vec{P}_{\text{gnss}} - \mathbf{R}(\psi) \begin{bmatrix} x_a \\ y_a \end{bmatrix}, \quad \text{where } \mathbf{R}(\psi) = \begin{bmatrix} \cos\psi & \sin\psi \\ -\sin\psi & \cos\psi \end{bmatrix}$$

For a 400-meter container vessel where the antenna is located 300 meters from the bow, a gyrocompass error of $1.5^\circ$ displaces the calculated bow envelope by $7.8\ \text{meters}$.

3. **Temporal latency and discrete sampling jitter ($\Delta t$):** Dynamic AIS reports arrive intermittently. For a vessel navigating at speed $V$ (knots) with an update interval $\Delta t$ (seconds), the spatial distance traversed between consecutive position reports is:

$$\Delta s = V \cdot \left(\frac{1852\ \text{m}}{3600\ \text{s}}\right) \cdot \Delta t \approx 0.5144 \cdot V \cdot \Delta t\ \text{meters}$$

At 20 knots, a Class A ship reporting every 2 seconds moves 20.6 meters between fixes. If reporting intervals drop to 10 seconds, the unobserved spatial gap expands to 103 meters.

```
+-----------------------------------------------------------------------------------------+
|                    ERROR BUDGET IN FORENSIC RECONSTRUCTION                              |
+------------------------------+---------------------------+------------------------------+
| Error Source                 | Physical Mechanism        | 95% Confidence Bound (2σ)    |
+------------------------------+---------------------------+------------------------------+
| Autonomous GNSS Fix          | Ionospheric/Multipath     | 2.5 – 5.0 m                  |
| Differential GNSS (DGNSS)    | Local reference beacon    | 0.5 – 1.0 m                  |
| Gyrocompass Heading Offset   | Alignment / Speed-error   | 0.5° – 1.5° (2–8 m at bow)   |
| Antenna Reference Offset     | Message 5 parameter error | 5.0 – 30.0 m (systematic)    |
| Temporal Sampling Gap (10s)  | Vessel motion at 20 kn    | ±10.3 m along-track deadband |
| VDR RTC Clock Drift          | Unsynced quartz oscillator| 1.0 – 5.0 s (10–50 m at speed|
+------------------------------+---------------------------+------------------------------+
```

### Worked example: Quantifying collision geometry uncertainty

Consider a crossing situation between a container ship (Vessel A, length $300\ \text{m}$, beam $40\ \text{m}$, $V_A = 18.0\ \text{knots}$, heading $\psi_A = 090^\circ$) and a bulk carrier (Vessel B, length $225\ \text{m}$, beam $32\ \text{m}$, $V_B = 12.0\ \text{knots}$, heading $\psi_B = 000^\circ$).

> **Worked example.**
> An investigator extracts VDR records from Vessel A and shore AIS records for Vessel B.
> 1. **Temporal synchronization:** Vessel A's VDR clock is found to lead true GNSS UTC by $\Delta t_{\text{err}} = 3.2\ \text{seconds}$. At $18.0\ \text{knots}$ ($9.26\ \text{m/s}$), failing to correct this offset places Vessel A $29.6\ \text{meters}$ too far east along its track.
> 2. **Antenna geometry correction:** Vessel A's AIS Message 5 reports `dimension_to_bow = 240 m` and `dimension_to_stern = 60 m`. Vessel A's GNSS antenna is located 240 meters aft of the bow. At $\psi_A = 090^\circ$, the bow's eastern coordinate is:
> 
> $$x_{\text{bow}} = x_{\text{gnss}} + 240.0\ \text{m}$$
> 
> 3. **Spatial closest approach uncertainty:** Combining the independent 95% circular errors of Vessel A ($\sigma_A = 3.5\ \text{m}$) and Vessel B ($\sigma_B = 4.2\ \text{m}$), the composite position error at the calculated point of impact is:
> 
> $$\sigma_{\text{composite}} = \sqrt{\sigma_A^2 + \sigma_B^2} = \sqrt{3.5^2 + 4.2^2} = \sqrt{12.25 + 17.64} = \sqrt{29.89} \approx 5.47\ \text{meters}$$
> 
> Because the physical beam of Vessel A ($40\ \text{m}$) and length of Vessel B ($225\ \text{m}$) vastly exceed the composite sensor error ($5.47\ \text{m}$), the forensic alignment provides unambiguous mathematical proof of physical hull contact, refuting claims of near-miss clearance.

## Software

Reconstructing maritime incidents requires specialized parsing, spatial analysis, and 3D visualization toolchains:

**Open source:**
- **libais / pyais:** High-performance decoders for raw NMEA 0183 AIVDM/AIVDO payload bit-streams. *Caveat:* Standard libraries parse individual sentences independently; multi-sentence fragment reassembly must be implemented statefully in upstream wrapper pipelines.
- **MovingPandas:** Spatio-temporal trajectory analysis library built on GeoPandas and Shapely, providing trajectory cleaning, Kalman smoothing, and stop/turn detection. *Caveat:* Memory-intensive; unsuited for raw ingestion of unindexed nationwide multi-gigabyte AIS streams.
- **Blender (bpy):** 3D Digital Content Creation suite providing headless Python automation for time-accurate incident animation and bridge line-of-sight rendering. *Caveat:* Operates in single-precision float32 local coordinates; geographic coordinates must be projected to a local origin before import.

**Free but closed:**
- **USCG Navigation Center AIS Tools:** Software utilities provided by the US Coast Guard for filtering, validating, and converting National AIS (NAIS) sensor logs. *Caveat:* Windows-centric and tightly coupled to USCG archive file conventions.

**Commercial:**
- **Danelec VDR Playback Software:** Proprietary forensic playback suite for Danelec DM100/DM200/DM300 VDR series, extracting synchronized audio, radar sweeps, and sensor telemetry. *Caveat:* Proprietary binary formats require vendor hardware dongles or signed investigative licenses.
- **Furuno VDR Playback (VR-7000 / VR-3000):** Manufacturer analysis toolchain providing multi-channel playback of bridge audio, ECDIS screens, and IEC 61162 bus captures. *Caveat:* Highly restrictive licensing; exports to open tabular formats often require specialized extraction modules.
- **Wärtsilä Navi-Sailor / Navi-Harbour VTS Playback:** Commercial Vessel Traffic Services replay engine capable of ingesting raw radar video, coastal AIS feeds, and VHF recordings. *Caveat:* Expensive enterprise architecture designed for port control centers rather than stand-alone forensic analysis.

## Standards & guides

- **International Maritime Organization (1997):** *Resolution A.861(20) — Performance Standards for Shipborne Voyage Data Recorders (VDRs)*. London: IMO. Governed systems installed between 2002 and 2014; mandated 12-hour retention in a single hardened capsule.
- **International Maritime Organization (2004):** *Resolution MSC.163(78) — Performance Standards for Shipborne Simplified Voyage Data Recorders (S-VDRs)*. London: IMO. Established reduced carriage specifications for pre-2002 cargo tonnage.
- **International Maritime Organization (2008):** *Resolution MSC.255(84) — Adoption of the Code of the International Standards and Recommended Practices for a Safety Investigation into a Marine Casualty or Marine Incident (Casualty Investigation Code)*. London: IMO. Establishes the non-judicial, safety-focused framework for international maritime casualty investigations.
- **International Maritime Organization (2012):** *Resolution MSC.333(90) — Adoption of Revised Performance Standards for Shipborne Voyage Data Recorders (VDRs)*. London: IMO. Mandates recording of all AIS data, dual capsules (fixed and float-free), 48-hour capsule retention, and 30-day internal storage for systems installed on or after 1 July 2014.
- **International Electrotechnical Commission (2013):** *IEC 61996-1:2013 + AMD1:2021 — Maritime navigation and radiocommunication equipment and systems — Voyage data recorders (VDR) — Part 1: Performance requirements, methods of testing and required test results*. Geneva: IEC. Type-approval test specification for modern MSC.333(90) compliant VDRs.
- **International Electrotechnical Commission (2007):** *IEC 61996-2:2007 — Maritime navigation and radiocommunication equipment and systems — Voyage data recorders (VDR) — Part 2: Simplified voyage data recorder (S-VDR) — Performance requirements, methods of testing and required test results*. Geneva: IEC. Type-approval specification for S-VDR systems.
- **International Electrotechnical Commission (2024):** *IEC 61162-1:2024 — Maritime navigation and radiocommunication equipment and systems — Digital interfaces — Part 1: Single talker and multiple listeners*. Geneva: IEC. Governs the 4,800 baud serial transmission of NMEA sentences.
- **International Electrotechnical Commission (2024):** *IEC 61162-2:2024 — Maritime navigation and radiocommunication equipment and systems — Digital interfaces — Part 2: Single talker and multiple listeners, high-speed transmission*. Geneva: IEC. Governs the 38,400 baud serial interface used by Class A AIS transponders.
- **International Electrotechnical Commission (2024):** *IEC 61162-450:2024 — Maritime navigation and radiocommunication equipment and systems — Digital interfaces — Part 450: Multiple talkers and multiple listeners — Ethernet interconnection*. Geneva: IEC. Lightweight Ethernet standard for multicasting NMEA sentences.
- **Marine Accident Investigators' International Forum (MAIIF) (2019):** *VDR Good Practice Guide*. Southampton: MAIIF. Operational manual detailing physical recovery, data extraction, and chain-of-custody protocols for marine casualty investigators.

## Pitfalls

1. **Treating VDR time as absolute atomic truth:** The mistake is assuming VDR timestamps match true UTC. Clock drift occurs when the internal RTC loses GNSS synchronization. Detect this by comparing VDR timestamps against the internal timestamps of decoded `!AIVDO` sentences or external VTS shore station logs.
2. **Ignoring the physical antenna offset:** The mistake is plotting the vessel's hull centered on the recorded GNSS coordinate. This causes substantial positional displacement on large vessels. Avoid it by parsing the antenna reference points in AIS Message 5 and transforming coordinates to the ship's center of gravity or bow.
3. **Misinterpreting missing AIS targets as deliberate evasion:** The mistake is alleging that a target vessel deliberately switched off its transponder ("went dark") because it disappeared from the VDR's `!AIVDM` log. This happens due to RF slot collisions, terrestrial shielding, or multipath fading. Verify whether external shore-based or satellite AIS networks recorded the target during the same interval.
4. **Accepting corrupted multi-sentence fragments:** The mistake is decoding orphaned NMEA multi-sentence fragments. When buffer overruns cause a multiplexer to drop sentence 1 of a 2-sentence burst, decoding sentence 2 in isolation generates corrupt or misleading metadata. Enforce strict sequential state checking on sequence identifiers.
5. **Over-smoothing trajectories with high-order splines:** The mistake is applying Bézier or cubic splines to sparse casualty tracks. This introduces fictitious acceleration loops and unrealistic hydrodynamic movements. Always employ linear motion models or physics-constrained Kalman smoothing.
6. **Failing to preserve physical evidence under desalination protocols:** The mistake is allowing a recovered submerged memory module to air dry. Salt crystallization destroys delicate microchip bond wires. Keep submerged electronic components in demineralized water until controlled cleanroom disassembly.
7. **Neglecting VDR battery maintenance intervals:** The mistake is assuming an installed VDR will record during a casualty involving total blackout. Degraded internal backup batteries cause the VDR to shut down instantly upon loss of shipboard power. Check annual testing certificates (MSC.1/Circ.1252) to verify battery replacement dates.
8. **Confusing heading with Course Over Ground:** The mistake is assuming a drifting or maneuvering vessel is pointed in its direction of travel. In high winds or strong currents, a ship's heading diverges dramatically from its COG. Reconstruct orientation strictly using gyrocompass records or valid AIS heading fields.
9. **Importing raw geographic coordinates into 3D rendering engines:** The mistake is feeding raw latitude and longitude values directly into software such as Blender. The resulting single-precision floating point rounding generates severe visual jitter. Project all geographic data onto a local tangent plane before rendering.
10. **Conflating safety investigation data with civil admissibility:** The mistake is attempting to introduce privileged VDR audio recordings directly into civil liability lawsuits in jurisdictions where statutory non-disclosure protections apply. Distinguish between privileged bridge voice recordings and non-privileged factual sensor telemetry.

## Key takeaways

- Modern Voyage Data Recorders are statutory multi-channel data loggers mandated under SOLAS Chapter V Regulation 20 to record internal shipboard states and surrounding navigational telemetry for accident investigation.
- Resolution MSC.333(90) transformed VDR capabilities for installations from 1 July 2014, mandating the logging of all AIS data, ECDIS displays, dual fixed and float-free capsules, 48-hour capsule retention, and 30-day internal storage.
- Recording AIS on the VDR captures both own-ship broadcasts (`!AIVDO`) and the entire local traffic environment (`!AIVDM`), providing an independent external check against on-board radar and gyro logs.
- Physical recovery of submerged capsules demands rapid acoustic homing on $37.5\ \text{kHz}$ pingers and continuous wet-bath preservation in demineralized water to prevent catastrophic salt crystallization.
- Forensic integrity requires bit-level write-blocked imaging, calculation of cryptographic SHA-256 digests, and strict chain-of-custody documentation compliant with international rules of evidence.
- Multi-source forensic fusion synchronizes internal VDR logs with shore-based coastal AIS, satellite telemetry, and harbor surveillance radar to establish verified spatial and temporal ground truth.
- High-fidelity 3D incident reconstructions can be automated via Blender's Python `bpy` API, projecting coordinates to local Euclidean tangent planes and utilizing linear keyframing to eliminate interpolation artifacts.
- Navigational telemetry (AIS, gyro, speed, rudder) is non-privileged factual evidence widely admissible in admiralty courts to establish liability under COLREGs, even where bridge voice recordings remain protected.

## References

- Danelec Marine (2021). *VDR and S-VDR Technical and Operational Manual*. Birkerød: Danelec Marine A/S.
- Federal Bureau of Maritime Casualty Investigation (BSU) (2019). *Investigation Report 356/17: Serious Marine Casualty — Collision between M/V Baltic Ace and M/V Corvus J*. Hamburg: BSU.
- Harati-Mokhtari, A., Wall, A., Brooks, P., and Wang, J. (2007). Automatic Identification System (AIS): Data reliability and human error implications. *The Journal of Navigation*, 60(3):373–389.
- International Electrotechnical Commission (2007). *IEC 61996-2:2007 — Maritime navigation and radiocommunication equipment and systems — Voyage data recorders (VDR) — Part 2: Simplified voyage data recorder (S-VDR)*. Geneva: IEC.
- International Electrotechnical Commission (2013). *IEC 61996-1:2013 + AMD1:2021 — Maritime navigation and radiocommunication equipment and systems — Voyage data recorders (VDR) — Part 1: Performance requirements, methods of testing and required test results*. Geneva: IEC.
- International Electrotechnical Commission (2024). *IEC 61162-1:2024 — Maritime navigation and radiocommunication equipment and systems — Digital interfaces — Part 1: Single talker and multiple listeners*. Geneva: IEC.
- International Electrotechnical Commission (2024). *IEC 61162-2:2024 — Maritime navigation and radiocommunication equipment and systems — Digital interfaces — Part 2: Single talker and multiple listeners, high-speed transmission*. Geneva: IEC.
- International Electrotechnical Commission (2024). *IEC 61162-450:2024 — Maritime navigation and radiocommunication equipment and systems — Digital interfaces — Part 450: Multiple talkers and multiple listeners — Ethernet interconnection*. Geneva: IEC.
- International Maritime Organization (1997). *Resolution A.861(20) — Performance Standards for Shipborne Voyage Data Recorders (VDRs)*. London: IMO.
- International Maritime Organization (2004). *Resolution MSC.163(78) — Performance Standards for Shipborne Simplified Voyage Data Recorders (S-VDRs)*. London: IMO.
- International Maritime Organization (2008). *Resolution MSC.255(84) — Adoption of the Code of the International Standards and Recommended Practices for a Safety Investigation into a Marine Casualty or Marine Incident (Casualty Investigation Code)*. London: IMO.
- International Maritime Organization (2012). *Resolution MSC.333(90) — Adoption of Revised Performance Standards for Shipborne Voyage Data Recorders (VDRs)*. London: IMO.
- Marine Accident Investigation Branch (MAIB) (2019). *Report on the investigation of the collision between the container vessel Ever Smart and the oil tanker Alexandra 1 outside Jebel Ali, UAE on 11 February 2015* (Report No. 18/2016). Southampton: MAIB.
- Marine Accident Investigators' International Forum (MAIIF) (2019). *VDR Good Practice Guide: For the Collection, Recovery and Handling of Voyage Data Recorders*. Southampton: MAIIF.
- National Transportation Safety Board (NTSB) (2017). *Sinking of US Cargo Vessel SS El Faro, Atlantic Ocean, Northeast of Acklins and Crooked Island, Bahamas, October 1, 2015* (Marine Accident Report NTSB/MAR-17/01). Washington, D.C.: NTSB.
- National Transportation Safety Board (NTSB) (2024). *Preliminary Report: Contact of Containership Dali with Francis Scott Key Bridge and Subsequent Bridge Collapse* (Accident No. DCA24MM031). Washington, D.C.: NTSB.
