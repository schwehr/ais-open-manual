# Chapter 58 — Threat model and security implications of AIS

> **Part IX — Security.** A rigorous analysis of the maritime Automatic Identification System attack surface, threat actors, structural protocol vulnerabilities, and engineering mitigations across the radio, network, and application domains.

**In this chapter.** You will learn how to systematically evaluate the security architecture and threat landscape of the Automatic Identification System (**AIS**). We establish an operational threat model across five classes of threat actors—ranging from opportunistic script users and commercial sanctions evaders to sophisticated state-sponsored electronic warfare units—and analyze their capabilities across the physical radio frequency layer, terrestrial and satellite network aggregators, and downstream bridge command systems. You will examine the core structural vulnerabilities arising from the absence of cryptographic authentication and integrity controls in Recommendation ITU-R M.1371, evaluate the landmark taxonomy established by Balduzzi, Pasta, and Wilhoit (2014), and differentiate between physical radio-frequency attacks and software-side crowd-sourced ingestion compromises. Finally, you will explore defensive architectures, including kinematic validation, physical-layer radio frequency fingerprinting, multi-receiver time difference of arrival verification, and emerging public-key cryptographic proposals.

## 58.1 The unauthenticated broadcast premise

The Automatic Identification System was engineered in the late 1990s as a cooperative, autonomous collision-avoidance broadcast system for mariners and coastal Vessel Traffic Services (**VTS**). Codified under Regulation 19 of Chapter V of the International Convention for the Safety of Life at Sea (**SOLAS**) by the International Maritime Organization (**IMO**) in Resolution MSC.99(73) (2000), its fundamental mandate was rapid, unencumbered situational awareness at sea. To ensure universal interoperability across commercial fleets, international flag registries, fishing vessels, and shore stations, the physical and link layer specifications established in Recommendation ITU-R M.1371 (2014, 2026) were designed entirely without cryptographic authentication, message integrity validation, or transport encryption.

When the system was standardized, the operational maritime environment was presumed to consist of honest, professional mariners operating type-approved transponders conforming to IEC 61993-2 (2018). The high monetary cost and engineering complexity of specialized maritime VHF radio hardware served as an effective economic barrier to signal manipulation. A maritime VHF transponder was a dedicated piece of marine avionics costing thousands of dollars, interfaced directly with shipborne Electronic Position Fixing Devices (**EPFD**) and gyrocompasses via NMEA 0183 / IEC 61162 serial lines ([Chapter 26](ch26-interfaces-and-logging.md)).

Over the subsequent two decades, two technological revolutions shattered this trust premise:
1. **The advent of low-cost Software-Defined Radios (SDRs):** Commodity, commercial off-the-shelf SDR transceivers—such as the HackRF, bladeRF, and Ettus USRP platforms—democratized the radio frequency spectrum ([Chapter 33](ch33-hardware-and-sdr.md)). Any actor with a modest budget and open-source signal processing libraries like GNU Radio could synthesize and broadcast arbitrary Gaussian Minimum Shift Keying (**GMSK**) waveforms directly into the maritime VHF data link (**VDL**).
2. **The rise of global AIS aggregation networks:** The expansion of commercial crowd-sourced terrestrial sensor networks and low Earth orbit (**LEO**) satellite constellations ([Chapter 39](ch39-satellite-ais.md); [Chapter 41](ch41-networks-and-providers.md)) transformed AIS from a localized, line-of-sight tactical tool (15–30 nmi; 28–56 km) into a globally aggregated data feed. Downstream consumers—including customs authorities, intelligence agencies, commodity traders, naval operations centers, and autonomous routing engines—began ingesting unauthenticated telemetry to make high-consequence decisions.

Because AIS operates as an unauthenticated open broadcast, any transmission over maritime VHF channels AIS 1 (161.975 MHz) and AIS 2 (162.025 MHz) is accepted as genuine by standard receivers as long as it adheres to the basic High-Level Data Link Control (**HDLC**) packet framing and CRC-16 checksum formatting. The checksum provides robust detection of random bit errors introduced by thermal noise or atmospheric multipath fading, but provides zero defense against intentional forgery.

> **Threat model.**
> - **Primary Assets:** Navigational safety of life at sea; integrity of Electronic Chart Display and Information Systems (**ECDIS**) and collision warnings (CPA/TCPA); availability of the maritime VHF Data Link (**VDL**); operational reliability of coastal VTS airspace; authenticity of global maritime supply chain telemetry.
> - **Threat Actors:** Opportunistic hobbyists and pranksters; merchant crew and fishing vessel masters attempting regulatory evasion; transnational organized crime, smuggling networks, and sanctions-evasion cartels; state-sponsored electronic warfare units and naval combatants; compromised software developers and network data aggregators.
> - **Attacker Capabilities:**
>   - *Receive-only:* Passive interception and logging of tactical movements, cargo declarations, and offshore infrastructure operations.
>   - *Software-side feed injection:* Direct injection of fabricated NMEA sentences into crowd-sourced aggregator APIs and unauthenticated TCP/UDP streaming endpoints.
>   - *RF transmission (SDR):* Over-the-air injection of spoofed vessel identities, false aids to navigation, phantom search-and-rescue beacons, and slot-starvation denial-of-service bursts using software-defined radios and power amplifiers.
>   - *GNSS manipulation:* Over-the-air spoofing or jamming of satellite navigation signals feeding legitimate onboard transponders.
>   - *Firmware/hardware tampering:* Physical or network modification of Class A or Class B shipborne transponders, bridge serial interfaces, or pilot plug connections.
> - **Impact:** Tactical bridge confusion and induced collision risk; false collision alarms triggering hazardous maneuvers; slot starvation blinding VTS and nearby vessels; cloaking of illegal transshipments and sanctions evasion; corruption of global maritime logistics and commodity pricing nowcasts.
> - **Engineering Mitigations:** Multi-sensor kinematic and spatial plausibility filtering; physical-layer RF fingerprinting; multi-station Time Difference of Arrival (**TDOA**) cross-bearing verification; correlation with primary radar and spaceborne Synthetic Aperture Radar (**SAR**); adoption of backward-compatible cryptographic authentication frameworks.

## 58.2 Taxonomy of threat actors and capabilities

Security analysis requires evaluating maritime adversaries across their technical capabilities, resources, risk tolerance, and strategic objectives (Kessler, Craiger & Haass 2018). In maritime cybersecurity, attackers range from low-skill script operators injecting data into web portals to national military units deploying multi-kilowatt electronic warfare suites.

```
       Attacker Sophistication & Resource Scale
   Low -----------------------------------------> High
   [Tier 1]         [Tier 2]         [Tier 3]          [Tier 4]
 Opportunistic    Commercial /     Transnational     State-Sponsored
  Web & SDR      Crew Sanctions    Crime & Cartels   Electronic Warfare
  Hobbyists         Evaders
      |                |                |                 |
  Unchecked API     Selective        Fabricated        High-power GNSS
  injection; basic  transponder      convoys; VDL      spoofing; cell
  phantom tracks    disabling        flooding          starvation
```

### 58.2.1 Tier 1: Opportunistic actors and radio hobbyists
Tier 1 actors possess modest technical skill and operate commodity hardware. Their motivations are typically curiosity, intellectual challenge, or petty disruption.
- **Tools:** Budget SDR dongles (e.g., RTL-SDR for reception, HackRF or LimeSDR for transmission) paired with open-source tools such as `gr-ais` or custom Python scripts; unauthenticated web accounts on commercial tracking platforms.
- **Capabilities:** Spoofing single phantom vessel tracks within a local harbor; injecting fabricated NMEA `!AIVDM` sentences into crowdsourced network feeds (e.g., AISHub, VesselFinder); transmitting false AIS text messages (Message 14).
- **Constraints:** Limited transmit power (<100 mW without external amplification); lack of maritime domain expertise; inability to coordinate synchronized slot reservations or maintain long-term kinematic consistency.

### 58.2.2 Tier 2: Commercial operators and non-compliant crew
Tier 2 actors operate within the legitimate maritime transport sector but intentionally manipulate AIS telemetry for commercial advantage, regulatory evasion, or avoidance of environmental monitoring.
- **Tools:** Shipboard transponder controls; Minimum Keyboard and Display (**MKD**) configuration menus; hardware power switches; GPS antenna attenuators or shielding caps.
- **Capabilities:** Intentional transponder deactivation ("going dark") during illicit ship-to-ship (**STS**) transfers; tampering with static voyage data (falsifying destination, draught, or cargo type in Message 5); broadcasting invalid or reassigned Maritime Mobile Service Identities (**MMSI**); deliberately generating GPS antenna faults to force fallback dead-reckoning reporting.
- **Constraints:** Bound by physical vessel kinematics; subject to port state control inspections, flag state audits, and primary radar detection by coastal patrol aircraft.

### 58.2.3 Tier 3: Transnational criminal networks and sanctions-evasion cartels
Tier 3 entities are well-funded illicit organizations engaged in narcotics trafficking, illegal, unreported, and unregulated (**IUU**) fishing, human smuggling, and sovereign sanctions evasion (e.g., illicit crude oil transport).
- **Tools:** Commercial marine transponders cloned with legitimate vessels' MMSIs; offshore shore-based or vessel-mounted high-gain VHF transmitters; coordinated digital proxy networks injecting false vessel tracks into commercial data aggregators.
- **Capabilities:** Fabricating elaborate "digital ghost voyages"—broadcasting realistic AIS tracks across legitimate maritime trade lanes while the physical tanker diverts hundreds of miles away to load embargoed cargo; synchronized transponder identity swapping where two vessels rendezvous, swap broadcast profiles, and diverge; coordinated spoofing of Class B fishing fleets.
- **Constraints:** Susceptible to satellite imagery correlation (optical and SAR), radio frequency direction finding, and maritime insurance forensics.

### 58.2.4 Tier 4: State-sponsored electronic warfare and naval units
Tier 4 represents nation-state actors possessing military-grade electronic warfare suites, high-powered terrestrial transmitters, and cyber capabilities.
- **Tools:** High-power multi-band GNSS spoofing and jamming transmitters; high-power VHF maritime transmission arrays; covert cyber access to maritime telecommunications backbones, satellite ground stations, and port VTS databases.
- **Capabilities:** Wide-area GNSS spoofing that forces dozens of commercial ships simultaneously to report circular, inland, or airport-centered AIS tracks (as documented extensively in the Black Sea and eastern Mediterranean; C4ADS 2019); coordinated tactical spoofing of naval combatants entering foreign territorial seas (e.g., the June 2021 HMS *Defender* incident off Sevastopol); intentional protocol-level denial of service across entire maritime chokepoints via VHF slot starvation and frequency reallocation commands.
- **Constraints:** Geopolitical escalation risks; diplomatic exposure; intelligence attribution.

## 58.3 Security analysis: The CIA triad applied to AIS

The classical security framework—evaluating Confidentiality, Integrity, and Availability (**CIA**)—provides a clear foundation for analyzing the fundamental vulnerabilities of AIS.

| Security Pillar | AIS Protocol Status | Technical Vulnerability | Operational Consequence |
|---|---|---|---|
| **Confidentiality** | Non-existent by design | All transmissions are open, unencrypted, broadcast RF bursts across international VHF channels. | Hostile tracking of military, commercial, and private vessels; intelligence gathering by pirates and competitive corporate espionage. |
| **Integrity** | Absent | Transmissions lack digital signatures, cryptographic message authentication codes (MACs), or transmitter verification. | Identity impersonation, vessel location spoofing, fabrication of phantom navigation hazards, and collision warning tampering. |
| **Availability** | Structurally fragile | Decentralized SOTDMA relies on self-policing slot allocation, unprotected base-station management messages, and shared RF medium. | Intentional slot reservation flooding, frequency hopping dislocation via Message 22, and assignment quiet-time denial of service. |

*Table 58.1: Security posture of the maritime VHF Data Link under the CIA triad.*

### 58.3.1 Confidentiality: The dilemma of open surveillance
The complete lack of confidentiality was an intentional engineering choice in SOLAS Chapter V. AIS was conceived as an open beacon, ensuring that every vessel within VHF horizon could instantly perceive the identity, aspect, and motion of nearby traffic without cryptographic key management hurdles. 

However, in modern operations, this total transparency poses grave security liabilities. Commercial shipowners transiting pirate-infested waters (such as the Gulf of Aden or Gulf of Guinea) face tactical reconnaissance from hostile skiffs equipped with consumer AIS receivers. Sovereign naval combatants, coast guard interdiction cutters, and specialized research vessels must continuously balance situational safety against tactical exposure. While IMO Resolution A.1106(29) (2015) explicitly authorizes shipmasters to switch off AIS transponders when they believe operational security is compromised, doing so blinds nearby commercial traffic, disables collision alerting algorithms, and increases navigation hazards.

### 58.3.2 Integrity: The unauthenticated data link
The absence of integrity controls represents the most exploited architectural defect in AIS. Recommendation ITU-R M.1371 defines packet structures where identity is asserted purely by a 30-bit integer: the Maritime Mobile Service Identity (**MMSI**). 

A receiving station has no cryptographic mechanism to verify that:
1. The transmitter legitimately owns or is authorized to use the broadcast MMSI.
2. The kinematic data (latitude, longitude, SOG, COG, heading) matches the actual physical position and motion of the radiating antenna.
3. The message contents were not altered, replayed, or synthesized in transit.

Standard transponders, ECDIS displays, and radar tracking systems simply parse the incoming bitstream, recalculate the 16-bit CRC to verify that no bits were flipped by RF channel noise, and immediately plot the target on the navigational chart.

### 58.3.3 Availability: Vulnerability to medium exhaustion
The Self-Organizing Time Division Multiple Access (**SOTDMA**) scheme dividing the VHF radio spectrum into 2,250 slots per minute across two channels (4,500 total slots/min) depends on cooperative politeness ([Chapter 21](ch21-link-layer-tdma.md)). A transponder listens to the channel, builds an internal slot map, and selects empty slots to broadcast while announcing its future slot reservations in the 19-bit communication state field.

Because there is no mutual authentication or resource authorization, the link layer is inherently vulnerable to intentional exhaustion:
- A rogue transmitter can announce reservations for all 2,250 slots in a frame, causing compliant transponders to back off, enter contention states, or drop transmissions.
- High-power transmitters can overwhelm local receivers through the physical "near-far" effect, desensitizing receiver front ends and raising the RF noise floor across both channels ([Chapter 31](ch31-noise-and-interference.md)).

## 58.4 The Balduzzi, Pasta & Wilhoit (2014) taxonomy

In 2013 and 2014, security researchers Marco Balduzzi, Kyle Wilhoit, and Alessandro Pasta published a landmark vulnerability assessment of AIS, presented at Hack in the Box Kuala Lumpur (2013) and the Annual Computer Security Applications Conference (Balduzzi, Pasta & Wilhoit 2014). Their research provided the first comprehensive, peer-reviewed taxonomy categorizing attacks against the AIS ecosystem into three functional domains: **spoofing attacks**, **hijacking attacks**, and **availability disruption**.

```
                   Balduzzi et al. (2014) Attack Taxonomy
                                      |
         +----------------------------+----------------------------+
         |                                                         |
         v                                                         v
   Radio Frequency (RF) Domain                         Software & Provider Domain
   - Ghost Ship Spoofing                               - Crowdsourced Feed Poisoning
   - Aid to Navigation (AtoN) Fabrication              - Aggregator API Injection
   - SAR Aircraft & SART Injection                     - Web Visualization Tampering
   - Closest Point of Approach (CPA) Triggering        - Buffer Overflow in Decoders
   - Slot Starvation (Msg 4 + 20)
   - Frequency Hopping Dislocation (Msg 22)
   - Assignment Delay / Silencing (Msg 16 / 23)
   - Vessel Hijacking via RF Power Override
```

### 58.4.1 Spoofing attacks
Balduzzi et al. demonstrated that an attacker using a software-defined radio (specifically an Ettus USRP B100 paired with GNU Radio and custom modulators) could synthesize valid over-the-air packets to fabricate entirely fictional maritime entities:
- **Fictional vessel creation ("Ghost ships"):** Injecting valid Class A position reports (Messages 1, 2, and 3) paired with static data (Message 5) to project nonexistent vessels onto nearby radar and ECDIS screens.
- **Aid to Navigation (AtoN) spoofing:** Generating Message 21 reports to create synthetic maritime hazards—such as projecting a false reef, an unlit buoy, or a virtual hazard directly into a navigable deep-water channel, potentially forcing mariners to alter course into real shallows.
- **Search and Rescue (SAR) craft and SART fabrication:** Synthesizing Message 9 (SAR aircraft position reports) or Message 1 (with an MMSI prefix of `970`, representing an AIS-SART emergency beacon). In testing, this instantly altered the search-and-rescue status on nearby monitoring consoles, triggering urgent rescue alerts.
- **Marine safety information and weather spoofing:** Broadcasting false meteorological and hydrographic binary messages (Message 8 Application-Specific Messages) to report nonexistent storms, gale warnings, or extreme wave heights.
- **False Closest Point of Approach (CPA) alarms:** Calculating the trajectory of a target ship and broadcasting a ghost vessel trajectory precisely calculated to intersect the victim's projected path within seconds. In their laboratory tests connected to an operational ECDIS, this induced urgent audible and visual collision alarms ("collision expected in 2 seconds"), demonstrating how an attacker could force evasive maneuvers in tight waterways.

### 58.4.2 Vessel hijacking via RF power override
The researchers evaluated scenarios where an attacker overwrites the legitimate telemetry of an active vessel. If an attacker knows a target ship's MMSI, they can transmit fabricated position reports using that same MMSI at higher RF power or timing precedence. Under standard SOTDMA logic, if a receiver detects a packet with a valid CRC from an MMSI, it updates the kinematic state of that track. 

In lab experiments using calibrated RF attenuators, Balduzzi et al. demonstrated that by overcoming the legitimate signal by 30 dB (e.g., transmitting at a level received at 120 dB vs. 90 dB for the victim), the attacker's false coordinates completely superseded the legitimate vessel's track on listening displays, effectively "hijacking" the vessel's digital footprint.

### 58.4.3 Availability disruption: Starvation, hopping, and timing manipulation
The most alarming technical findings in Balduzzi et al. (2014) concerned link-layer management and denial-of-service vulnerabilities embedded within ITU-R M.1371:

1. **Slot starvation via base station spoofing (Messages 4 and 20):**
   An attacker transmits a forged Message 4 (Base Station Report), asserting an MMSI with a coastal base station prefix (format `00MIDXXXX`). The attacker simultaneously transmits Message 20 (Data Link Management Message), reserving specific future slots. By cycling through reservation blocks, the attacker can systematically reserve all 2,250 slots in a 60-second frame. Compliant mobile stations within range observe these slots as occupied by a shore authority, defer transmission, and become completely silenced.
2. **Frequency hopping dislocation (Message 22):**
   Recommendation ITU-R M.1371 defines Message 22 (Channel Management) to allow shore authorities and VTS centers to instruct transponders to shift from standard international frequencies (161.975 MHz and 162.025 MHz) to designated regional or simplex channels. Balduzzi et al. demonstrated that an attacker could broadcast a forged Message 22 specifying geographic coordinates that instructed all transponders entering a specified bounding box to shift operating frequencies by 4.950 MHz. In laboratory tests with commercial Class B transponders, the receivers immediately switched frequencies and ceased communicating on international channels. Crucially, the researchers noted that commercial Class B units provided no manual override or user alerting, requiring specialized technician software to restore standard frequencies.
3. **Assignment quiet-time manipulation ("Timing attack"):**
   The authors identified that Message 23 (Group Assignment Command) and Message 16 (Assigned Mode Command) allow a base station to control reporting intervals and transmission behavior. An attacker can broadcast a forged Message 23 commanding all mobile transponders of a certain class within a specified geographic area to enter "quiet mode," suppressing transmissions for up to 15 minutes, or alternatively, commanding them to transmit at the maximum burst rate, flooding the maritime band.

> **On the wire: Protocol bounds and link-layer guard rails.**
> While Balduzzi et al. (2014) proved the theoretical viability of these attacks, Recommendation ITU-R M.1371 and IEC equipment test standards incorporate specific link-layer constraints that limit their geographic and temporal persistence:
> 1. **Base-station priority and internal UTC:** Under ITU-R M.1371-6 (Annex 2 §3.1.3.4), an AIS station with direct access to internal UTC timing (Sync State 0) never synchronizes its slot clock to an external base station. A spoofed Message 4 cannot corrupt a mobile station's slot phase if the mobile has a healthy internal GNSS fix.
> 2. **Message 23 quiet-time ceilings:** Under Annex 2 §3.3.7, the quiet-time field in Message 23 is bounded between 0 and 15 minutes. A station cannot be silenced permanently with a single transmission; the attacker must continuously broadcast over-the-air commands.
> 3. **Autonomous timeout reversion:** Under Annex 2 §3.3.6 and IEC 62320-2, assigned modes and slot reservations commanded by base stations automatically expire after a timeout interval (typically 3 to 10 minutes) if not refreshed by the controlling base station, reverting the mobile station to autonomous SOTDMA mode.
> 4. **AtoN immunity:** Under IEC 62320-2 (Table 1), physical and virtual Aids to Navigation transponders are explicitly prohibited from responding to assignment Messages 16 and 23.

## 58.5 Software-side injection vs. RF transmission

A critical distinction in modern maritime security is the operational difference between **over-the-air RF manipulation** and **software-side data injection** into terrestrial aggregation networks.

```
+--------------------------------------------------------------------------+
|                        ATTACK VECTOR COMPARISON                          |
+------------------------------------+-------------------------------------+
| Over-the-Air RF Transmission       | Software-Side Aggregator Injection  |
+------------------------------------+-------------------------------------+
| Physical VHF radiation via SDR     | TCP/IP socket / REST API injection  |
| Affects local vessels & VTS        | Bypasses local RF receivers entirely|
| Range: Line-of-sight (15–30 nmi)   | Range: Global web platform visibility|
| Bound by physics & propagation     | Immune to RF path loss / line-of-sight|
| Detected by RF direction finding   | Detected by ingest IP / API audits  |
| High hardware & transmission cost  | Negligible financial/operational cost|
+------------------------------------+-------------------------------------+
```

### 58.5.1 Over-the-air RF transmission mechanics
In an over-the-air attack, the adversary must deploy a physical radio transmitter and antenna operating within the VHF maritime mobile band.
- **Physical constraints:** The attacker's signal is bound by line-of-sight propagation, atmospheric refraction, antenna gain, and terrain masking ([Chapter 29](ch29-propagation-modeling.md)). To spoof a vessel 20 miles offshore, the attacker must be positioned within radio horizon or utilize airborne or seaborne platforms.
- **Tactical impact:** RF attacks directly deceive the bridge crew of nearby vessels, port radar/AIS combiners, and coastal VTS operations. An ECDIS receiving a locally radiated RF packet will plot the target, calculate collision geometry, and sound alarms.
- **Detection vector:** RF transmissions can be localized using Direction Finding (**DF**), Angle of Arrival (**AoA**), and Time Difference of Arrival (**TDOA**) networks ([Chapter 35](ch35-direction-finding-geolocation.md)).

### 58.5.2 Software-side aggregator injection mechanics
In a software-side injection attack, the adversary exploits the architectures of commercial crowd-sourced aggregators (such as MarineTraffic, VesselFinder, and AISHub). These aggregators rely on thousands of volunteer stations worldwide streaming raw NMEA 0183 sentences via unauthenticated TCP/IP sockets or UDP datagrams.
- **Zero RF emission:** The attacker transmits nothing over the radio spectrum. Instead, they open a network connection to an aggregator's ingest endpoint and stream synthetic `!AIVDM` sentences formatted with valid checksums.
- **Global reach:** An attacker in an inland apartment can stream synthetic telemetry depicting an entire fleet of warships maneuvering inside foreign territorial waters. The aggregator's servers parse the incoming NMEA stream and project the fictional tracks onto their public web maps and enterprise APIs.
- **Operational consequence:** Software injection does **not** affect tactical bridge navigation or local ECDIS displays, as ships at sea do not listen to commercial web feeds for collision avoidance. However, it severely impacts macro-scale consumers: maritime intelligence analysts, supply chain algorithms, automated customs platforms, and news organizations.
- **Detection vector:** Detected via network telemetry, ingest IP anomaly detection, API authentication tokens, and cross-referencing with terrestrial coastal base stations that ought to have heard the vessel via RF line-of-sight but logged zero packets.

> **Case file: The June 2021 Black Sea warship spoofing incident.**
> On 18 June 2021, commercial AIS aggregation portals displayed tracking tracks showing the British Royal Navy destroyer HMS *Defender* (Type 45) and the Royal Netherlands Navy frigate HNLMS *Evertsen* departing the port of Odesa, Ukraine, and steaming directly toward the naval base of Sevastopol in Russian-occupied Crimea, approaching within 2 nautical miles of the naval harbor.
> 
> However, live webcam streams from Odesa harbor and physical eyewitness confirmation proved that both warships were moored alongside the quay in Odesa at the exact moment their AIS tracks claimed they were operating off Crimea. Analysis of the received data revealed that the synthetic telemetry was fed directly into commercial data feeds. The fabricated tracks exhibited perfect linear courses and unnatural speed profiles, demonstrating how unauthenticated ingestion feeds can be manipulated to generate geopolitical provocation and disinformation.

## 58.6 Threat evolution: From academic POC to industrial evasion

In the decade following Balduzzi et al.'s 2014 disclosures, maritime AIS manipulation shifted rapidly from academic proof-of-concept demonstrations to industrialized, state-backed, and commercial evasion operations.

### 58.6.1 Industrial sanctions evasion and the "Dark Fleet"
International trade sanctions imposed on oil exports from sanctioned states catalyzed an unprecedented expansion in AIS manipulation techniques ([Chapter 6](ch06-fisheries-iuu-dark-fleets.md)):
- **Digital identity cloning:** Tankers regularly purchase decommissioned or scrapped vessels' identities, programming obsolete MMSIs and IMO numbers into transponders to mask their true flag and ownership.
- **Coordinated STS cloaking:** Tankers rendezvous offshore to conduct ship-to-ship oil transfers. One or both vessels switch off transponders, alter broadcast positions by 50–100 nautical miles, or deploy tethered Class B AIS beacons on service barges to project a false location while the parent vessel loads crude oil undetected.
- **Spoofing-as-a-Service:** Commercial investigative reports have uncovered organized maritime service providers offering pre-packaged digital track generation, delivering synthetic voyage data directly to ship management consoles and shore-side reporting networks to satisfy maritime insurers and financial institutions.

### 58.6.2 State-sponsored GNSS-induced AIS distortion
A critical evolution in the threat landscape is the convergence of electronic warfare and AIS manipulation. Rather than attacking the AIS VHF link directly, state actors frequently deploy high-power GNSS spoofers.

Because a Class A AIS transponder derives its position, speed, and time from an Electronic Position Fixing System (**EPFS**)—typically an internal or connected GPS receiver ([Chapter 25](ch25-gnss-and-ais.md))—corrupting the GPS signal directly corrupts the transmitted AIS telemetry:
- **Black Sea and Eastern Mediterranean anomalies:** Beginning in 2017, hundreds of merchant vessels operating near the Black Sea and Russian territorial waters reported extreme GNSS displacement. Onboard GPS receivers locked onto spoofed signals, causing ship transponders to broadcast positions locating the vessels dozens of miles inland at civilian airports (e.g., Sochi and Gelendzhik airports; C4ADS 2019).
- **Crop circle and phantom fleet patterns:** In 2019 and 2020, commercial shipping off Shanghai and the port of Qingdao exhibited bizarre circular tracks ("crop circles"), where dozens of vessels appeared to rotate in tight formations. Subsequent analysis determined that terrestrial GNSS spoofers were manipulating satellite navigation timing, forcing transponders to compute cyclical false positions.

## 58.7 Defense in depth: Verification and countermeasures

Because altering the global ITU-R M.1371 standard to require cryptographic signatures across hundreds of thousands of installed marine transponders presents massive diplomatic and economic barriers, maritime security relies on a **defense-in-depth architecture**. Defenses operate across three distinct tiers: kinematic analysis, physical-layer validation, and cryptographic protocol extensions.

```
+--------------------------------------------------------------------------+
|                     DEFENSE-IN-DEPTH ARCHITECTURE                        |
+--------------------------------------------------------------------------+
|  Tier 3: Cryptographic Protocols & Standards Evolution                    |
|  - Digital signatures (ECDSA / Ed25519) within ASM payloads              |
|  - Maritime Certificate-less Identity-Based Cryptography (mIBC)          |
|  - VDES Phase 2 authenticated channels                                   |
+--------------------------------------------------------------------------+
|  Tier 2: Physical Layer & Sensor Fusion                                   |
|  - RF Fingerprinting (carrier frequency offset, modulation transient)    |
|  - Terrestrial & Satellite Multi-Station TDOA / FDOA Geolocation         |
|  - Spaceborne Synthetic Aperture Radar (SAR) & Optical Cross-Correlation |
|  - Shipboard Radar (ARPA) vs. AIS Target Fusion                          |
+--------------------------------------------------------------------------+
|  Tier 1: Kinematic & Geospatial Plausibility Filtering                   |
|  - Speed Over Ground (SOG) vs. implied Haversine distance gating        |
|  - Rate of Turn (ROT) and angular acceleration caps                      |
|  - Line-of-sight receiver footprint / propagation bounds                 |
|  - MMSI mid-digit and ITU-R M.585 registry compliance screening          |
+--------------------------------------------------------------------------+
```

### 58.7.1 Tier 1: Kinematic and geospatial plausibility filtering
Data consumers and bridge systems can detect the majority of basic spoofing attempts by applying strict physical kinematics and RF propagation constraints to incoming tracks ([Chapter 47](ch47-data-quality-track-reconstruction.md)):
1. **Speed and acceleration bounds:** Comparing the reported Speed Over Ground ($SOG$) against the velocity implied by consecutive coordinates:
   $$v_{\text{implied}} = \frac{d_{\text{geodesic}}(\mathbf{p}_k, \mathbf{p}_{k-1})}{\Delta t}$$
   If $v_{\text{implied}}$ exceeds physical hull caps (e.g., 40 knots for commercial cargo, 60 knots for high-speed craft) or if the instantaneous acceleration exceeds $a_{\text{max}} = 2.0\text{ m/s}^2$, the report is flagged as physically anomalous.
2. **Receiver footprint gating:** Verifying that the reported coordinates fall within the realistic physical reception horizon of the receiving base station:
   $$D_{\text{max}} = 2.22 \left( \sqrt{h_{\text{rx}}} + \sqrt{h_{\text{tx}}} \right)\text{ nmi}$$
   A terrestrial shore station with an antenna height of 50 m receiving an AIS burst reporting a position 200 nmi offshore (in the absence of severe tropospheric ducting) indicates a forged injection or anomalous propagation.
3. **Identity and registry validation:** Cross-referencing broadcast MMSIs against the ITU Maritime mobile Access and Retrieval System (**MARS**) database to verify valid Maritime Identification Digits (**MID**; ITU-R M.585) and identify known test strings (e.g., `123456789`, `111111111`, or `1193046`).

### 58.7.2 Tier 2: Physical-layer forensics and sensor fusion
Sophisticated adversaries capable of generating kinematically realistic tracks cannot easily forge physical radio frequency properties and spatial geometry:
- **Radio Frequency Fingerprinting (RFF):** Every physical radio transmitter possesses micro-imperfections in its analog circuitry, power amplifiers, and local oscillators. By capturing raw in-phase and quadrature (**I/Q**) samples at the receiver, machine learning classifiers can identify distinctive transmitter fingerprints—such as Carrier Frequency Offset (**CFO**), transient turn-on profiles, and modulation phase errors—distinguishing a software-defined radio from genuine marine transponders ([Chapter 34](ch34-rf-forensics-fingerprinting.md)).
- **Multi-station Time Difference of Arrival (TDOA):** When an over-the-air burst is captured by three or more synchronized coastal receivers or formation-flying LEO satellites (such as HawkEye 360 clusters; [Chapter 35](ch35-direction-finding-geolocation.md)), the differential time of arrival produces intersecting hyperbolas:
   $$\Delta t_{ij} = \frac{\|\mathbf{p}_{\text{emitter}} - \mathbf{p}_i\| - \|\mathbf{p}_{\text{emitter}} - \mathbf{p}_j\|}{c}$$
   Comparing the computed hyperbolic intersection against the latitude/longitude asserted in the packet payload instantly exposes spoofed positions.
- **Spaceborne SAR and optical cross-correlation:** Satellite constellations combine high-resolution Synthetic Aperture Radar (**SAR**) imagery with spaceborne AIS telemetry. A vessel broadcasting AIS whose position displays no corresponding radar backscatter signature ("ghost ship"), or a radar target with no associated AIS broadcast ("dark vessel"), is immediately identified for interdiction.

### 58.7.3 Tier 3: Cryptographic authentication frameworks
To permanently solve the integrity deficit, researchers have proposed multiple backward-compatible cryptographic authentication mechanisms:
- **Application-Specific Message authentication:** Utilizing ITU-R M.1371 binary messages (such as Message 8 or Message 26) to broadcast digital signatures generated via Elliptic Curve Digital Signature Algorithms (**ECDSA**) or Ed25519 (Kessler 2020; Wimpenny et al. 2022).
- **Certificate-less Identity-Based Cryptography (mIBC):** Goudossis and Katsikas (2019, 2020) proposed a lightweight public-key framework specifically designed for maritime constraints, eliminating the overhead of full Public Key Infrastructure (**PKI**) certificate chains by deriving public keys directly from vessel identities (MMSI and IMO numbers).
- **VHF Data Exchange System (VDES):** The next-generation evolution of AIS, standardized in ITU-R M.2092, incorporates designated digital channels and cryptographic integrity fields, providing a native migration path toward secure maritime messaging ([Chapter 69](ch69-vdes-ais-2.md)).

> **Try it.**
> You can evaluate the kinematic plausibility of a vessel feed using the repository's security triage pipeline. Run the script against the synthetic harbor dataset:
> 
> ```bash
> . .venv/bin/activate
> python code/security/kinematic_checks.py data/samples/synthetic_harbor.nmea --rx 42.36 -70.95
> ```
> 
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
> Notice how the heuristic immediately flags invalid MMSI values (`0` and `1193046`) while confirming that kinematic speeds and antenna distances remain within plausible operational limits.

> **Legal note.**
> The legal framework governing AIS security research and radio transmission is strictly enforced under national and international law:
> - **Prohibition of unauthorized transmission:** Radiating over-the-air signals on maritime VHF frequencies AIS 1 (161.975 MHz) and AIS 2 (162.025 MHz) without an experimental or station license from national spectrum regulators (e.g., the Federal Communications Commission under 47 CFR Part 80 in the United States, or Ofcom in the United Kingdom) is illegal. Penalties include substantial civil fines, equipment forfeiture, and criminal prosecution.
> - **SOLAS compliance and navigational interference:** Under Regulation 19 of SOLAS Chapter V and domestic statutes (e.g., 33 CFR § 164.46), commercial vessels are legally required to maintain their AIS transponders in effective operating condition. Broadcasters transmitting false navigational safety signals face severe criminal charges for endangering safety of life at sea.
> - **Responsible laboratory research:** Security researchers must conduct all transmit evaluations exclusively within RF-isolated environments (e.g., Faraday cages or cabled RF test benches using calibrated inline attenuators directly terminated into 50-ohm dummy loads), ensuring zero unintentional radiation reaches commercial shipping or coastal monitoring networks.

## Then & now

- **1998** ⟨+⟩: IMO adopts Resolution MSC.74(69), establishing performance standards for shipborne AIS without cryptographic authentication or security provisions.
- **2000** ⟨+⟩: IMO adopts Resolution MSC.99(73), mandating AIS carriage on international commercial vessels under SOLAS Chapter V.
- **2002** ⟨H⟩: SOLAS AIS carriage requirements begin phased implementation for commercial shipping.
- **2004** ⟨H⟩: Universal carriage deadline reached for international passenger ships and tankers.
- **2008** ⟨+⟩: Launch of pioneering space-based AIS receiver payloads demonstrates orbital detection, expanding AIS from line-of-sight VHF to global surveillance.
- **2013** ⟨+⟩: Trend Micro researchers (Balduzzi, Wilhoit, and Pasta) present "AIS Exposed" at Hack in the Box Kuala Lumpur, conducting the first systematic security evaluation of the protocol.
- **2014** ⟨+⟩: Balduzzi, Pasta, and Wilhoit publish their seminal security evaluation at ACSAC '14, proving RF spoofing, CPA hijacking, and slot starvation vulnerabilities.
- **2017** ⟨+⟩: Mass GNSS spoofing incidents in the Black Sea displace dozens of commercial ships' AIS positions to inland airports.
- **2018** ⟨+⟩: Kessler, Craiger, and Haass publish a comprehensive maritime cybersecurity vulnerability taxonomy in *TransNav*.
- **2019** ⟨+⟩: C4ADS releases the landmark report *Above Us Only Stars*, documenting thousands of maritime GNSS and AIS spoofing events across the Russian Federation and Syria.
- **2019** ⟨+⟩: Goudossis and Katsikas introduce the Maritime Certificate-less Identity-Based Cryptography (mIBC) framework for backward-compatible AIS authentication.
- **2021** ⟨+⟩: Fabricated AIS tracks for HMS *Defender* and HNLMS *Evertsen* in the Black Sea illustrate software-side injection into commercial aggregators.
- **2022** ⟨+⟩: Wimpenny et al. publish practical evaluations of public-key cryptography for AIS and VDES in *The Journal of Navigation*.
- **2026** ⟨+⟩: ITU-R M.1371-6 formalizes updated operational requirements, while VDES standards (ITU-R M.2092) advance toward certified secure maritime messaging.

## Validation, uncertainty & data quality

Ingesting and analyzing AIS data requires rigorous validation pipelines to separate benign sensor noise, legitimate operational edge cases, and transmission errors from deliberate malicious manipulation (Iphar, Ray & Napoli 2020).

```
Raw AIS Stream
      |
      v
[1. Structural Frame Validation] ----Fail----> [Drop: Corrupt CRC / Framing]
      | Pass
      v
[2. Registry & Identity Gating]  ----Fail----> [Flag: Reserved/Invalid MMSI]
      | Pass
      v
[3. Kinematic Plausibility Test] ----Fail----> [Flag: Impossible Speed/Turn]
      | Pass
      v
[4. RF & Receiver Footprint]    ----Fail----> [Flag: Range/TDOA Inconsistency]
      | Pass
      v
Validated Trajectory Store
```

### 58.7.1 Error propagation and false positive risks
When deploying anti-spoofing heuristics, analysts must understand the primary sources of benign anomalies that mimic hostile attacks:
1. **Multipath and tropospheric ducting:** Severe atmospheric temperature inversions create tropospheric RF ducts, allowing maritime VHF signals to propagate hundreds of nautical miles beyond the normal horizon. A terrestrial receiver logging a distant ship is not necessarily observing an injection attack.
2. **GPS antenna shadowing and multipath:** Vessels maneuvering near high-rise port container cranes or sheer fjord walls experience satellite multipath and temporary Dilution of Precision (**DOP**) spikes, generating brief kinematic jumps.
3. **MKD human input errors:** Transponder static data (Message 5) is entered manually via shipboard keypads. Typographical errors in vessel dimensions, draft, and destination are ubiquitous across commercial fleets and must not be conflated with coordinated deception.

### 58.7.2 Quantified validation procedure
A production-grade ingestion filter should execute the following quantitative checks on every received position report:
- **Checksum verification:** Reject all sentences failing standard 16-bit CRC checks ($P_{\text{error}} \approx 2^{-16} \approx 1.5 \times 10^{-5}$).
- **Kinematic delta-t threshold:** Compute elapsed time $\Delta t = t_k - t_{k-1}$. If $\Delta t < 1.0\text{ s}$ and spatial displacement $\Delta d > 100\text{ m}$, flag for velocity spike.
- **Speed Over Ground consistency:** Validate reported $SOG$ against calculated geodesic velocity:
  $$\epsilon_v = |SOG - v_{\text{implied}}|$$
  Flag if $\epsilon_v > 5.0\text{ kn}$ over three consecutive reporting intervals.
- **Heading vs. Course Over Ground alignment:** For vessels with $SOG > 5\text{ kn}$, the angular difference between True Heading ($HDG$) and Course Over Ground ($COG$) should rarely exceed $45^\circ$ under normal leeway:
  $$\Delta \theta = |(HDG - COG + 180^\circ) \bmod 360^\circ - 180^\circ|$$
  If $\Delta \theta > 45^\circ$, flag for gyrocompass failure or synthetic track injection.

## Software

**Open source:**
- **`pyais`:** High-performance Python library for decoding raw NMEA 0183 and AIVDM/AIVDO message streams into structured dictionaries and objects. *Caveat:* Focuses purely on parsing; does not provide native kinematic trajectory validation.
- **`libais`:** High-throughput C++ decoder with Python bindings developed for large-scale archive processing. *Caveat:* Requires strict upstream sanitization of malformed NMEA sentences to avoid buffer parsing panics.
- **`gr-ais`:** GNU Radio block implementing physical-layer GMSK demodulation and HDLC framing for software-defined radios. *Caveat:* Research-oriented software; requires calibrated RF front ends and manual frequency correction.

**Free but closed:**
- **OpenCPN:** Widely used cross-platform chartplotter and navigation software supporting AIS overlays, collision alerting (CPA/TCPA), and virtual AtoN rendering. *Caveat:* Lacks native cryptographic verification; accepts all valid NMEA inputs without anomaly scoring.
- **BarentsWatch:** Norwegian public information portal providing coastal vessel tracking and maritime safety maps. *Caveat:* Regional coverage restricted to Northern European waters.

**Commercial:**
- **Spire Maritime:** Global constellation provider offering satellite and terrestrial AIS feeds with integrated machine learning spoofing and dark-vessel detection models. *Caveat:* High commercial licensing costs; proprietary heuristic algorithms not open to audit.
- **Kpler (MarineTraffic / FleetMon):** Comprehensive terrestrial and satellite vessel tracking network offering historical voyage archives and API integration. *Caveat:* Ingests crowdsourced feeds that require secondary filtering against software injection.
- **Windward:** Maritime predictive intelligence platform specializing in sanctions compliance, dark fleet tracking, and deceptive shipping behavior profiling. *Caveat:* Closed-source commercial platform targeted primarily at financial and security institutions.

## Standards & guides

- **ITU-R Recommendation M.1371-5 / M.1371-6:** *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band* (2014, 2026). Governs physical radio modulation, slot scheduling, link management, and message formats.
- **ITU-R Recommendation M.585-10:** *Assignment and use of identities in the maritime mobile service* (2026). Specifies allocation and formatting rules for Maritime Mobile Service Identities (MMSI).
- **IMO Resolution MSC.74(69), Annex 3:** *Recommendation on Performance Standards for a Universal Shipborne Automatic Identification System (AIS)* (1998). Establishes operational baseline for shipborne transponders.
- **IMO Resolution A.1106(29):** *Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems (AIS)* (2015). Operational guidance for bridge watchstanders; defines conditions for transponder deactivation.
- **IEC Standard 61993-2:2018:** *Class A shipborne equipment of the automatic identification system (AIS)* (Edition 3.0). Specifies type-approval test standards and environmental performance for commercial shipborne units.
- **IEC Standard 62320-2:2016:** *AIS Aids to Navigation (AtoN) stations* (Edition 2.0). Governs performance and link management rules for physical and virtual AtoN transponders.

## Pitfalls

1. **Assuming valid CRC-16 proves message authenticity.** The CRC-16 checksum detects accidental bit flips caused by channel noise; it provides zero protection against malicious packet synthesis or over-the-air injection.
2. **Treating crowdsourced web platforms as real-time tactical ground truth.** Commercial aggregation websites ingest unauthenticated TCP/IP feeds from volunteer receivers, making them vulnerable to software-side injection that does not exist in local airspace.
3. **Assuming a ship that disappears from AIS has intentionally "gone dark."** High-density shipping corridors suffer severe TDMA slot contention and satellite packet collision; a missing track often reflects RF physics rather than illicit evasion.
4. **Failing to distinguish between AIS spoofing and GNSS spoofing.** When an onboard GPS receiver is spoofed, the AIS transponder broadcasts genuine, type-approved RF signals containing erroneous coordinates calculated by its compromised navigation sensor.
5. **Ignoring receiver horizon limits when evaluating spoofing alerts.** Flagging a distant ship as "spoofed" without accounting for abnormal tropospheric ducting creates false positives during atmospheric temperature inversions.
6. **Relying solely on CPA alarms without visual or radar confirmation.** Forged ghost ships specifically designed to trigger CPA/TCPA alarms can cause watchstanders to make dangerous evasive maneuvers in restricted waters.
7. **Using planar Euclidean formulas to detect velocity anomalies.** Calculating distance between consecutive fixes using flat-plane geometry induces massive distortion at high latitudes; pipelines must employ geodesic or great-circle formulas.
8. **Disregarding static data entry errors as malicious tampering.** The vast majority of invalid vessel names, zero draughts, and placeholder dimensions in Message 5 stem from human input error via the transponder MKD.
9. **Assuming Class B transponders have base-station assignment overrides.** Commercial Class B transponders lack manual frequency resets; if shifted to non-standard frequencies via a rogue Message 22, they may remain silenced until technician servicing.
10. **Overlooking the impact of satellite revisit gaps.** Satellite AIS collection exhibits orbital latency gaps of 15 to 90 minutes; evaluating vessel kinematics across orbital gaps without interpolating timestamps yields artificial speed anomalies.

## Key takeaways

- The Automatic Identification System was engineered as an open, unencrypted, and unauthenticated VHF broadcast protocol prioritizing safety of life at sea over cryptographic security.
- The proliferation of low-cost Software-Defined Radios and global crowdsourced data aggregators has exposed AIS to widespread spoofing, hijacking, and denial-of-service manipulation.
- Balduzzi et al. (2014) established the foundational threat taxonomy, demonstrating phantom vessel injection, false AtoN creation, CPA alarm manipulation, and link-layer slot starvation.
- Attacks divide fundamentally into local over-the-air RF transmissions (which affect nearby bridge systems and VTS) and software-side network injections (which deceive global web platforms and analysts).
- State-sponsored and sanctions-evasion actors have industrialized AIS manipulation, deploying wide-area GNSS spoofing and "digital ghost fleets" to cloak embargoed oil shipments.
- Defending against AIS manipulation requires defense in depth: kinematic plausibility gating, physical RF fingerprinting, multi-station TDOA cross-correlation, and satellite radar fusion.
- Long-term cryptographic remediation depends on backward-compatible standards evolution, including Application-Specific Message digital signatures and the VHF Data Exchange System (VDES).

## References

- Balduzzi, M., Pasta, A. & Wilhoit, K. (2014). A Security Evaluation of AIS Automated Identification System. In *Proceedings of the 30th Annual Computer Security Applications Conference (ACSAC '14)*, pages 436–445. New Orleans, USA: ACM. doi:10.1145/2664243.2664257.
- Balduzzi, M., Wilhoit, K. & Pasta, A. (2014). *A Security Evaluation of AIS: Automated Identification System* (Research White Paper). Tokyo, Japan: Trend Micro Research. https://documents.trendmicro.com/assets/white_papers/wp-a-security-evaluation-of-ais.pdf.
- Center for Advanced Defense Studies (2019). *Above Us Only Stars: Exposing GPS Spoofing in Russia and Syria*. Washington, DC: C4ADS.
- Goudossis, A. & Katsikas, S. K. (2019). Towards a secure automatic identification system (AIS). *Journal of Marine Science and Technology*, 24(2):410–423. doi:10.1007/s00773-018-0561-3.
- Goudossis, A. & Katsikas, S. K. (2020). Secure AIS with Identity-Based Authentication and Encryption. *TransNav: International Journal on Marine Navigation and Safety of Sea Transportation*, 14(2):287–296. doi:10.12716/1001.14.02.03.
- International Electrotechnical Commission (2016). *Maritime navigation and radiocommunication equipment and systems – Automatic Identification Systems (AIS) – Part 2: AIS Aids to Navigation (AtoN) stations – Operational and performance requirements, methods of test and required test results* (Standard No. IEC 62320-2:2016). Edition 2.0. Geneva: IEC.
- International Electrotechnical Commission (2018). *Maritime navigation and radiocommunication equipment and systems – Automatic Identification Systems (AIS) – Part 2: Class A shipborne equipment of the automatic identification system (AIS) – Operational and performance requirements, methods of test and required test results* (Standard No. IEC 61993-2:2018). Edition 3.0. Geneva: IEC.
- International Maritime Organization (1998). *Recommendation on Performance Standards for a Universal Shipborne Automatic Identification System (AIS)* (Resolution MSC.74(69), Annex 3). Adopted 12 May 1998. London: IMO.
- International Maritime Organization (2000). *Adoption of Amendments to the International Convention for the Safety of Life at Sea, 1974, as Amended (SOLAS Chapter V)* (Resolution MSC.99(73)). Adopted 5 December 2000. London: IMO.
- International Maritime Organization (2015). *Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems (AIS)* (Resolution A.1106(29)). Adopted 2 December 2015. London: IMO.
- International Telecommunication Union (2014). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band* (Recommendation ITU-R M.1371-5). Geneva: ITU Radiocommunication Sector.
- International Telecommunication Union (2026). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band* (Recommendation ITU-R M.1371-6). Geneva: ITU Radiocommunication Sector.
- Iphar, C., Ray, C. & Napoli, A. (2020). Data-integrity assessment framework for maritime awareness systems. *Expert Systems with Applications*, 147:113219. doi:10.1016/j.eswa.2020.113219.
- Kessler, G. C., Craiger, J. P. & Haass, J. C. (2018). A Taxonomy of Maritime Cybersecurity Vulnerabilities and Mitigations. *TransNav: International Journal on Marine Navigation and Safety of Sea Transportation*, 12(3):429–437. doi:10.12716/1001.12.03.01.
- Kessler, G. C. (2020). Protected AIS (pAIS): A Demonstration of Authenticated, Encrypted Automatic Identification System Message Exchange. *TransNav: International Journal on Marine Navigation and Safety of Sea Transportation*, 14(2):279–286. doi:10.12716/1001.14.02.02.
- Wimpenny, E., Šafář, J., Grant, A. & Bransby, C. (2022). Securing the Automatic Identification System (AIS) Using Public Key Cryptography to Prevent Spoofing Whilst Retaining Backwards Compatibility. *The Journal of Navigation*, 75(2):333–345. doi:10.1017/S0373463321000624.
