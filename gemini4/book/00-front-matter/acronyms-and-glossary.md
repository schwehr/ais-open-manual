# Acronyms and Comprehensive Technical Glossary

> **Scope:** Over 150 essential acronyms and technical definitions spanning AIS protocol internals, VHF RF engineering, GNSS timing, hydrographic charting (ECDIS/S-100), Vessel Traffic Services (VTS), 3D visualization, and maritime cybersecurity/intelligence.

---

## A
* **ADC (Analog-to-Digital Converter):** Electronic component in an SDR or receiver that samples continuous analog IF/baseband voltage into discrete digital numbers (e.g., 8-bit in RTL-SDR/HackRF, 12-bit in Airspy, 14-bit in SDRplay).
* **AIS (Automatic Identification System):** Autonomous, self-organizing VHF maritime broadcast transponder system operating around $162\text{ MHz}$ standardized under ITU-R M.1371 and mandated by IMO SOLAS Chapter V, Regulation 19.
* **AIS 1 / AIS 2:** Primary international AIS simplex VHF channels: **AIS 1** is Channel 87B ($161.975\text{ MHz}$) and **AIS 2** is Channel 88B ($162.025\text{ MHz}$).
* **AIS-MOB (Man Overboard):** Personal lifejacket-mounted AIS survival beacon standardized under IEC 63269 and RTCM 11901.1 using MMSI prefix `972`.
* **AIS-SART (Search and Rescue Transmitter):** Survival craft homing beacon standardized under IEC 61097-14 operating on AIS 1/2 using MMSI prefix `970`.
* **`!AIVDM` (AIS VHF Data-Link Message):** NMEA 0183 / IEC 61162-1 sentence formatter encapsulating an AIS message received from *another* vessel or station over the VHF Data Link.
* **`!AIVDO` (AIS VHF Data-Link Own-Vessel Report):** NMEA 0183 / IEC 61162-1 sentence formatter encapsulating the *own ship's* locally generated AIS payload.
* **AMRD (Autonomous Maritime Radio Device):** Uncrewed floating radio device defined in ITU-R M.2135, divided into **Group A** (safety-related, permitted on AIS 1/2) and **Group B** (non-navigation, e.g., fishing net buoys, restricted to Ch 2006 at $160.900\text{ MHz}$ with MMSI prefix `979`).
* **AMVER (Automated Mutual-Assistance Vessel Rescue):** USCG-managed voluntary global ship reporting system for search and rescue.
* **AoA (Angle of Arrival):** Physical direction from which an RF wavefront arrives at a Direction Finding (DF) or phased-array antenna.
* **APM / AREPS (Advanced Propagation Model / Advanced Refractive Effects Prediction System):** US Navy split-step Parabolic Equation (PE) electromagnetic propagation modeling suite used to predict VHF tropospheric ducting.
* **ARPA (Automatic Radar Plotting Aid):** Shipboard radar processing system that tracks radar echoes to compute target course, speed, CPA, and TCPA.
* **ASM (Application Specific Message):** Binary payload messages (AIS Messages 6, 8, 25, 26) identified by a 10-bit Designated Area Code (DAC) and 6-bit Functional Identifier (FI), or dedicated VDES channels ASM 1 ($161.950\text{ MHz}$) and ASM 2 ($162.000\text{ MHz}$).
* **ASV / USV (Autonomous / Uncrewed Surface Vessel):** Uncrewed ocean platform (e.g., Liquid Robotics Wave Glider, Saildrone) used for persistent offshore AIS and hydrographic collection.
* **ATI (`AnyTimeInterrogation`):** SS7 Mobile Application Part (MAP) signaling query exploited to retrieve the real-time cell ID or maritime picocell location of a 2G/3G mobile phone.
* **AtoN (Aid to Navigation):** Buoy, beacon, lighthouse, or mark assisting mariners (Message 21, MMSI prefix `99MIDxxxx`). Classified into **Real** (physical unit on the buoy), **Synthetic Monitored**, **Synthetic Predicted**, and **Virtual** (broadcast by a shore Base Station for a coordinate where no physical buoy exists).
* **AVIS (Authoritative Vessel Identification Service):** USCG intelligence and vessel identity correlation database.

## B
* **BAMS (Bridge Alert Management System):** Standardized shipboard alarm prioritization framework (IMO MSC.302(87) / IEC 62923).
* **BeiDou (BDS):** Chinese Global Navigation Satellite System supported by modern multi-constellation AIS receivers and used exclusively by some domestic Chinese fishing terminals.
* **Blender (`bpy`):** Open-source 3D creation and rendering suite (released 1994; open-sourced under GPL in 2002) scriptable via its embedded Python API (`bpy`) and `BlenderGIS` for 3D/4D vessel casualty reconstruction, viewshed raycasting, and bathymetric/acoustic animation.
* **`BMAP <GO>`:** Bloomberg Terminal interactive geospatial map function used by commodity traders to track live AIS ship positions, draughts, port queues, and floating storage.
* **$BT$ Product (Bandwidth-Time Product):** Dimensionless parameter of the Gaussian pre-modulation filter in GMSK ($BT \times T_{\text{bit}}$); in AIS, $BT = 0.4$ for transmit and $BT = 0.5$ for receive.

## C
* **CAN Bus (Controller Area Network):** Differential two-wire serial bus (ISO 11898) underlying **NMEA 2000 (IEC 61162-3)** at $250\text{ kbps}$.
* **CCNR (Central Commission for the Navigation of the Rhine):** European regulatory body governing **Inland AIS** specifications.
* **CFO (Carrier Frequency Offset):** Frequency deviation between a transmitter's RF carrier and the nominal channel frequency ($161.975 / 162.025\text{ MHz}$), used in Specific Emitter Identification (RF fingerprinting) and satellite Doppler processing.
* **CGI / ECGI (Cell Global Identity / E-UTRAN Cell Global Identifier):** Unique global identifier of a 2G/3G/4G cellular base station sector, returned by SS7/Diameter queries when tracking mobile phones near coasts or on shipboard picocells.
* **Class A AIS:** Mandatory SOLAS commercial transceiver ($12.5\text{ W}$ TX power, SOTDMA MAC, dual receivers + DSC receiver, mandatory MKD and Pilot Plug, certified to IEC 61993-2).
* **Class B "CS" (Carrier-Sense) AIS:** Non-SOLAS light commercial/recreational transceiver ($2\text{ W}$ TX power, CSTDMA listen-before-talk MAC, certified to IEC 62287-1).
* **Class B "SO" (SOTDMA / Class B+) AIS:** Higher-performance Class B transceiver ($5\text{ W}$ TX power, full SOTDMA slot reservation, speed-dependent reporting up to every 5 seconds, certified to IEC 62287-2).
* **COG (Course Over Ground):** Direction of a vessel's actual motion path over the Earth's surface relative to True North ($0.1^\circ$ resolution in AIS), which differs from **True Heading (HDG)** in the presence of wind leeway or cross-currents.
* **COLREGs (International Regulations for Preventing Collisions at Sea, 1972):** IMO treaty governing navigation rules, lookout duties (Rule 5), collision risk assessment (Rule 7), avoidance maneuvers (Rule 8), and navigation light sectors.
* **CPA / TCPA (Closest Point of Approach / Time to Closest Point of Approach):** Fundamental geometric collision-avoidance metrics computed from relative position and velocity vectors.
* **CRC-CCITT (Cyclic Redundancy Check):** 16-bit Frame Check Sequence (FCS) appended to every AIS HDLC burst using generator polynomial $G(x) = x^{16} + x^{12} + x^5 + 1$.
* **CRPA (Controlled Reception Pattern Antenna):** Multi-element phased-array GNSS antenna that steers spatial nulls toward RF jammers.
* **CSTDMA (Carrier-Sense Time Division Multiple Access):** Listen-before-talk access scheme used by Class B "CS" units, which measures background RSSI in a slot before transmitting to avoid stepping on Class A reservations.

## D
* **DAC (Designated Area Code):** 10-bit code in Binary Messages 6 and 8 identifying the jurisdiction defining the message structure (`DAC = 1` for international IMO messages; `DAC = 200` for European Inland AIS; `DAC = 316` for Canada; `DAC = 366` for the United States).
* **dAISy:** Low-power dedicated AIS hardware receiver family developed by Adrian Studer (Wegmatt LLC).
* **$\text{dBd}$ / $\text{dBi}$:** Decibels relative to a half-wave dipole ($\text{dBd}$) vs. an isotropic radiator ($\text{dBi}$), where $\text{dBi} = \text{dBd} + 2.15\text{ dB}$.
* **DGNSS / DGPS (Differential GNSS / GPS):** Augmentation system broadcasting pseudorange corrections via coastal MF radiobeacons ($283.5\text{–}325\text{ kHz}$) or AIS **Message 17**.
* **Diameter:** Authentication, Authorization, and Accounting (AAA) signaling protocol (RFC 6733) used in **4G LTE and 5G** core networks (`S6a`/`S6d` interfaces), superseding 2G/3G SS7 MAP.
* **DMA / SMA (Dynamic Management Area / Seasonal Management Area):** NOAA speed-restriction zones ($10\text{ kts}$ limit for vessels $\ge 65\text{ ft}$) protecting North Atlantic Right Whales, broadcast via AIS Area Notices and **Whale Alert**.
* **DMON (Digital Acoustic Monitoring Instrument):** WHOI-developed autonomous hydrophone package mounted on buoys and gliders to detect whale vocalizations in real time.
* **DSC (Digital Selective Calling):** $1,200\text{ bps}$ FSK paging system on VHF **Channel 70 ($156.525\text{ MHz}$)** used for GMDSS distress alerts and regional AIS channel management fallback.

## E
* **EAIS (Encrypted AIS):** Military and Coast Guard extension encapsulating AES-256 or NSA Type 1 encrypted Blue Force position reports inside standard AIS Binary Messages 6 and 8.
* **ECDIS (Electronic Chart Display and Information System):** IMO SOLAS-certified bridge navigation computer (IEC 61174) that legally replaces paper charts when running official ENCs.
* **ECS (Electronic Chart System):** Non-SOLAS chartplotter software or hardware.
* **eLORAN (Enhanced LORAN):** Modernized high-power $100\text{ kHz}$ terrestrial positioning and UTC timing system providing an independent backup to jammed GNSS.
* **EMSA (European Maritime Safety Agency):** EU agency operating **SafeSeaNet (SSN)**, **CleanSeaNet**, and **Integrated Maritime Services (IMS)**.
* **ENC (Electronic Navigational Chart):** Official vector chart database issued by a national Hydrographic Office under **IHO S-57** or **IHO S-101**.
* **ENU (East-North-Up):** Local Cartesian tangent-plane coordinate frame centered at $(\lambda_0, \phi_0, h_0)$, used for vessel kinematics and to eliminate `float32` precision jitter in **Blender**.
* **EPIRB-AIS:** 406 MHz Cospas-Sarsat Emergency Position Indicating Radio Beacon with an integrated AIS transmitter (MMSI prefix `974`).
* **ERMA® (Environmental Response Management Application):** NOAA web-based common operational picture used during the 2010 *Deepwater Horizon* spill, powered by `libais`.

## F–G
* **FATDMA (Fixed Access TDMA):** Deterministic slot allocation scheme reserved exclusively for shore Base Stations (Message 4) and Data Link Management (Message 20).
* **FI (Functional Identifier):** 6-bit sub-type identifier (paired with a 10-bit DAC) specifying the binary schema of an Application-Specific Message (e.g., `DAC=1, FI=22` is Area Notice; `DAC=1, FI=31` is Met/Hydro).
* **Galileo / GLONASS / GPS:** European, Russian, and US Global Navigation Satellite Systems.
* **GFW (Global Fishing Watch):** Non-profit organization founded by Oceana, SkyTruth, and Google that uses AIS, VMS, SAR, and optical satellite data to map global human activity at sea.
* **GMSK (Gaussian Minimum Shift Keying):** Continuous-phase frequency-shift keying modulation ($h = 0.5$) where the rectangular NRZI bit pulse train is filtered by a Gaussian low-pass filter before frequency modulation.

## H–I
* **H3:** Uber's open-source hierarchical hexagonal discrete global grid system (DGGS) used for spatial aggregation of AIS trajectories.
* **HDG (True Heading):** Direction in which a vessel's bow is physically pointing relative to True North (measured by gyrocompass or THD), distinct from **COG**.
* **HDLC (High-Level Data Link Control):** ISO/IEC 13239 synchronous bit-oriented framing protocol (`0x7E` flags + zero-bit stuffing + CRC-16) used by AIS.
* **IALA:** International Organization for Marine Aids to Navigation (elevated from an NGO to an Intergovernmental Organization in August 2024).
* **IEC (International Electrotechnical Commission):** Standards organization whose Technical Committee 80 (TC 80) writes hardware certification tests for AIS, ECDIS, Radar, VDR, and NMEA interfaces.
* **IHO (International Hydrographic Organization):** Intergovernmental body governing nautical charting standards (**S-52, S-57, S-63, S-100, S-101, S-102, S-104, S-111, S-124, S-421**).
* **IMO (International Maritime Organization):** United Nations specialized agency responsible for the safety and security of shipping (**SOLAS, COLREGs, STCW, MARPOL**).
* **IMO Number:** Permanent 7-digit vessel hull identifier (`IMO` + 6 digits + 1 check digit) assigned at keel laying that never changes across flag or owner transfers.
* **INS / IBS (Integrated Navigation System / Integrated Bridge System):** Multi-sensor shipboard bridge architecture (IEC 61924-2).
* **ITDMA (Incremental TDMA):** Access scheme used by mobile stations to pre-announce temporary changes in reporting rate, autonomous slot bootstrapping, or Message 9/18 transmissions.
* **ITU-R (International Telecommunication Union – Radiocommunication Sector):** UN agency governing global radio spectrum (RR Appendix 18) and the core AIS standard **ITU-R M.1371**.
* **IWRAP Mk II (IALA Waterway Risk Assessment Program):** Quantitative maritime collision and grounding probability modeling tool developed with **GateHouse Maritime**.

## L–N
* **`libais`:** High-performance open-source C++/Python AIS decoding library created by Kurt Schwehr in April 2010 during the *Deepwater Horizon* oil spill response.
* **LNA (Low-Noise Amplifier):** Front-end RF amplifier mounted near the antenna to establish a low system noise figure and overcome coaxial cable loss.
* **LOA (Length Overall):** Total length of a vessel hull ($L_{\text{OA}} = d_{\text{bow}} + d_{\text{stern}}$ in AIS Message 5 / 24).
* **LRIT (Long-Range Identification and Tracking):** Closed, point-to-point satellite tracking system mandated under SOLAS Chapter V, Regulation 19-1 (reporting every 6 hours to flag/port/coastal state data centers).
* **LWE (Lightweight Ethernet / IEC 61162-450):** Shipboard UDP/IP multicast transport wrapping NMEA 0183 sentences inside NMEA TAG blocks.
* **MID (Maritime Identification Digits):** 3-digit country/administration code (`201`–`775`) embedded in an MMSI.
* **MISLE (Marine Information for Safety and Law Enforcement):** USCG national inspection, casualty, and law-enforcement database.
* **MKD (Minimum Keyboard and Display):** Mandatory physical alphanumeric display and keypad unit on a Class A AIS transponder.
* **MMSI (Maritime Mobile Service Identity):** 9-digit decimal radio identity (`000000000`–`999999999`, packed in 30 bits in AIS) defined by **ITU-R M.585-9**.
* **`MovingPandas`:** Open-source Python library created by Anita Graser for spatiotemporal trajectory analysis built on `geopandas`.
* **MSSIS (Maritime Safety and Security Information System):** US DoT Volpe-operated multilateral government-to-government AIS network sharing raw real-time NMEA feeds among $>70$ nations.
* **MTSA 2002 (Maritime Transportation Security Act of 2002):** Post-9/11 US federal law mandating port security plans, domestic AIS carriage, and the USCG **NAIS** network.
* **NAIS (Nationwide Automatic Identification System):** USCG national network of coastal towers, buoys, and satellites collecting and transmitting AIS across US waters.
* **NMEA 0183 / NMEA 2000:** National Marine Electronics Association serial ASCII (`4,800`/`38,400` baud RS-422) and CAN-bus (`250 kbps`) marine instrumentation standards.
* **NRZI (Non-Return-to-Zero Inverted):** Line code in which a binary `0` causes a signal transition and a binary `1` causes no transition.
* **NWR (NOAA Weather Radio):** Continuous $100\text{–}1,000\text{ W}$ FM voice broadcasts on **$162.400\text{–}162.550\text{ MHz}$**—located immediately adjacent to AIS 2 ($162.025\text{ MHz}$) and a primary source of receiver front-end overload if unfiltered.

## O–R
* **OPA-90 (Oil Pollution Act of 1990):** US statute enacted after the 1989 *Exxon Valdez* grounding that catalyzed automated tanker tracking in Prince William Sound.
* **PAWSS (Ports and Waterways Safety System):** 1998 USCG program that deployed the first operational AIS-based VTS in New Orleans / Lower Mississippi.
* **PGN (Parameter Group Number):** 18-bit message identifier in NMEA 2000 CAN frames (e.g., PGN `129038` = AIS Class A Position Report).
* **PORTS® (Physical Oceanographic Real-Time System):** NOAA/USCG system measuring and broadcasting real-time tides, currents, winds, and bridge air gap over AIS Message 8.
* **1PPS (One Pulse Per Second):** Hardware logic pulse from a GNSS receiver whose rising edge aligns with the start of each UTC second to within $<100\text{ ns}$, required by Class A/Base Station AIS units to maintain $\pm 2.6\text{ }\mu\text{s}$ TDMA slot timing.
* **PPU (Portable Pilot Unit):** Harbor pilot's ruggedized laptop/tablet connected to a ship's AIS Pilot Plug for high-precision channel navigation and docking.
* **RAIM (Receiver Autonomous Integrity Monitoring):** Algorithm inside a GNSS receiver that uses redundant satellite pseudoranges ($\ge 5$ satellites) to detect a faulty satellite range and set the AIS RAIM flag.
* **RATDMA (Random Access TDMA):** Access scheme used by an AIS unit when transmitting its very first burst upon power-up or unscheduled safety messages.
* **R-Mode (Ranging Mode):** Terrestrial backup positioning system that extracts timing/ranging pseudoranges from synchronized coastal VHF/VDES AIS base stations and MF DGNSS beacons during GNSS jamming.
* **ROT (Rate of Turn):** Angular yaw velocity of a vessel in degrees per minute ($\circ/\text{min}$), non-linearly compressed into an 8-bit signed integer in AIS Messages 1, 2, and 3 via $\text{ROT}_{\text{AIS}} = 4.733\sqrt{\text{ROT}_{\circ/\text{min}}}$.
* **RTCM (Radio Technical Commission for Maritime Services):** Standards body governing DGNSS (SC-104), AIS Binary Messages (SC-121 / RTCM 12301.1), and AIS-MOB (SC-119).

## S–V
* **S-52 / S-57 / S-63 / S-100:** IHO hydrographic standards for ECDIS symbology (**S-52**), legacy ENC vector data (**S-57**), data encryption (**S-63**), and the next-generation Universal Hydrographic Data Model (**S-100**, including **S-101** ENC, **S-102** Bathymetry, **S-104** Water Level, **S-111** Currents, **S-124** Navigational Warnings, **S-212** VTS, and **S-421** Route Exchange).
* **S-AIS (Satellite AIS):** Reception of VHF AIS broadcasts by Low Earth Orbit (LEO) satellites.
* **SAR (Synthetic Aperture Radar):** Active microwave imaging radar (e.g., ESA Sentinel-1, NISAR, ICEYE, Capella) that images metal ship hulls through clouds and darkness to detect "dark ships."
* **SAROPS (Search and Rescue Optimal Planning System):** USCG Monte Carlo drift and search planning software.
* **SAW Filter (Surface Acoustic Wave Filter):** Compact piezoelectric RF bandpass filter ($162\text{ MHz}$) critical for protecting SDR receivers from FM broadcast and NOAA Weather Radio overload.
* **SEI (Specific Emitter Identification):** RF fingerprinting technique that identifies the manufacturer or specific physical transceiver unit from hardware-induced IQ waveform imperfections (PA ramp transients, GMSK phase trajectory, CFO/clock skew, I/Q imbalance).
* **SIC (Successive Interference Cancellation):** DSP algorithm that demodulates the stronger of two colliding AIS bursts, reconstructs its ideal RF waveform, subtracts it from the raw IQ recording, and recovers the weaker underlying packet.
* **SOG (Speed Over Ground):** Magnitude of the vessel's velocity vector over the Earth's surface in knots ($0.1\text{ kt}$ resolution in AIS).
* **SOLAS (International Convention for the Safety of Life at Sea):** Foundational IMO safety treaty; Chapter V, Regulation 19 mandates AIS carriage.
* **SOTDMA (Self-Organized Time Division Multiple Access):** Patented by Håkan Lans (1988); distributed MAC protocol where each ship broadcasts its future slot reservations (`Time-out` and `Slot Offset`) inside its position reports so all neighbors within radio range dynamically build a conflict-free TDMA schedule.
* **SS7 (Signaling System No. 7):** Legacy global telecom signaling protocol suite (ITU-T Q.700 series) whose Mobile Application Part (**MAP**) can be queried to geolocate 2G/3G mobile phones at sea or near coasts.
* **STCW (Standards of Training, Certification and Watchkeeping for Seafarers):** IMO convention governing mariner training (including IMO Model Course 1.34 on AIS).
* **STS (Ship-to-Ship Transfer):** At-sea transfer of crude oil, refined products, LNG, or catch between two vessels moored alongside or steaming at low speed.
* **TAG Block:** IEC 61162-450 metadata header (`\s:station,c:timestamp*HH\`) prepended to an NMEA 0183 sentence to record reception time, station ID, and signal strength.
* **TCXO (Temperature-Compensated Crystal Oscillator):** High-stability reference clock ($0.5\text{–}2.0\text{ ppm}$) in AIS transceivers and SDRs.
* **TPC (Tonnes Per Centimeter Immersion):** Hydrostatic hull parameter specifying how many metric tonnes of cargo change a ship's mean draught by $1\text{ cm}$, used by commodity traders (`BMAP`) to estimate cargo weight from AIS Message 5 draught changes.
* **UKC (Under-Keel Clearance):** Vertical distance between the lowest point of a ship's hull (accounting for static draught, squat, and wave-induced heave/pitch/roll) and the seabed.
* **UNCLOS (United Nations Convention on the Law of the Sea):** 1982 global treaty defining maritime zones and navigational rights.
* **URN (Underwater Radiated Noise):** Acoustic energy radiated into the ocean by ship propellers (cavitation) and machinery, modeled from AIS speed/hull data to assess impact on marine mammals.
* **VDES (VHF Data Exchange System / "AIS 2.0"):** Next-generation maritime digital communication standard (**ITU-R M.2092-1**, entering SOLAS force in 2028) combining legacy AIS, ASM, terrestrial wideband data (**VDE-TER** up to $307.2\text{ kbps}$), and two-way satellite data (**VDE-SAT**).
* **VDL (VHF Data Link):** The shared over-the-air radio medium on AIS 1 and AIS 2 (2,250 time slots per minute per channel = 4,500 slots/min total).
* **VDR / S-VDR (Voyage Data Recorder / Simplified VDR):** Maritime "black box" (IEC 61996-1/2) recording bridge audio, radar/ECDIS images, ship sensors, and raw `!AIVDM`/`!AIVDO` AIS traffic.
* **VMS (Vessel Monitoring System):** Closed, government-mandated satellite tracking system for commercial fishing vessels.
* **VOS (Volunteer Observing Ship):** WMO/NOAA program in which merchant ships voluntarily report marine weather observations.
* **VTS (Vessel Traffic Services):** Shore-side authority (IALA V-128 / IMO A.1158(32)) monitoring and managing vessel traffic in ports, straits, and approaches using fused Radar and AIS.
