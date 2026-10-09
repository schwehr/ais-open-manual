# Chapter 63 — Blue-force, encrypted, and military AIS

> **Part IX — Security.** An examination of military, naval, and governmental Automatic Identification Systems, focusing on cryptographic tactical modes, international warship standards, electromagnetic signature control, and physical-layer interoperability with civilian traffic.

**In this chapter.** You will learn how naval combatants, coast guards, and maritime security agencies resolve the tension between navigational safety and tactical secrecy on the maritime VHF data link (**VDL**). You will examine the legal basis of military AIS, including sovereign immunity exemptions under SOLAS Chapter V and 33 CFR § 164.01(c). We analyze NATO Warship AIS (**W-AIS**) under STANAG 4668 and 4669, and contrast vendor cryptographic architectures—including Saab Secure Link, Kongsberg Blue Force, and L3Harris Protec-M—with standard Class A transponders. You will inspect the packet framing and slot reservation mechanisms of encrypted Application-Specific Messages (**ASMs**), specifically Message 25 and Message 26 under DAC 366. Finally, you will evaluate the safety hazards of running dark, the post-2017 surface force policy reversals, and the key management practices needed to coordinate coalition forces without disrupting the civilian Time Division Multiple Access (**TDMA**) network.

## 63.1 The warship dilemma: safety versus tactical signature

The Automatic Identification System was conceived and codified as an open, unauthenticated, autonomous broadcast network designed to eliminate bridge-to-bridge ambiguity and prevent maritime collisions ([Chapter 1](ch01-what-ais-is.md); [Chapter 21](ch21-link-layer-tdma.md)). By transmitting periodic, unencrypted reports containing a vessel's identity, Maritime Mobile Service Identity (**MMSI**), dimensions, kinematic state, navigation status, and voyage intent over maritime VHF frequencies (161.975 MHz and 162.025 MHz), AIS ensures that every neighboring vessel within VHF line-of-sight maintains an accurate tactical plot of surrounding traffic.

For sovereign naval combatants and maritime security agencies, this universal transparency represents a severe operational vulnerability. Modern warships are engineered at tremendous expense to minimize their radar cross-section, acoustic emissions, and infrared signatures. Broadcasting a continuous, unencrypted 12.5 W VHF signal that advertises exact coordinates, speed, course, call sign, and destination directly undermines operational security (**OPSEC**).

```
+-----------------------------------------------------------------------------------+
|                           THE WARSHIP AIS DILEMMA                                 |
+-----------------------------------------------------------------------------------+
|  NAVIGATIONAL SAFETY (SOLAS Mandate)     |   OPERATIONAL SECURITY (OPSEC Mandate) |
|  - Continuous VHF beaconing (12.5 W)     |   - Emissions Control (EMCON / Silent) |
|  - Open broadcast of identity & MMSI     |   - Concealment of combatant identity  |
|  - Unencrypted real-time GNSS kinematics |   - Concealment of position & maneuvers|
|  - Universal collision avoidance (ECDIS) |   - Avoidance of adversary OSINT & ESM |
|                                          |                                        |
|  Outcome: Low risk of collision;         |   Outcome: Low probability of detection|
|  Total tactical exposure.                |   High risk of peacetime collision.    |
+-----------------------------------------------------------------------------------+
```

During wartime or high-readiness deployments, the choice is straightforward: warships enforce complete Emissions Control (**EMCON**), silencing all non-essential radio frequency emitters, including navigation transponders. In peacetime and transition-to-crisis phases, however, naval vessels spend significant operational time navigating through densely populated commercial waterways, such as the Strait of Malacca, the Strait of Hormuz, the English Channel, and coastal Traffic Separation Schemes (**TSSs**).

In these congested choke points, operating completely "dark" creates severe navigational hazards. Commercial merchant vessels navigate with lean bridge teams who rely heavily on Electronic Chart Display and Information Systems (**ECDIS**) and Automatic Radar Plotting Aids (**ARPA**) integrated with AIS ([Chapter 51](ch51-charts-enc-ecdis.md); [Chapter 53](ch53-mariner-training.md)). While primary navigation radar detects the physical presence of a warship, radar targets lack immediate vessel names, navigational intent, and verified rates of turn. In close-quarters crossing or overtaking situations, commercial watchstanders cannot call the warship by name via VHF Channel 16 or Channel 13 ([Chapter 3](ch03-at-sea-operations.md)), leading to dangerous misunderstandings.

To resolve this conflict between tactical concealment and navigational safety, naval forces and maritime electronics manufacturers developed specialized military architectures:
1. **Warship AIS (W-AIS):** Standardized military transponder modes that provide multi-level signature control, ranging from normal civilian Class A broadcasts to receive-only passive listening, parameter spoofing, and low-power tactical operation.
2. **Encrypted AIS / Blue Force Tracking (BFT):** Cryptographic extensions overlaid on the standard VHF Data Link (**VDL**) that allow friendly naval and coast guard units to exchange tactical position and status reports securely without disclosing their telemetry to civilian receivers or adversary Electronic Support Measures (**ESM**) suites.
3. **Dedicated Military VHF Links:** Migration of tactical position exchanges away from international maritime channels AIS 1 and AIS 2 to dedicated national, NATO, or regional VHF frequencies.

## 63.2 Legal frameworks and sovereign immunity

The legal mandate for AIS carriage is established in Regulation 19.2.4 of Chapter V of the SOLAS Convention, adopted by the International Maritime Organization (**IMO**). Regulation 19 requires all commercial ships of 300 gross tonnage (**GT**) and upward engaged on international voyages, cargo ships of 500 GT and upward not engaged on international voyages, and all passenger ships irrespective of size to be fitted with an AIS Class A transponder.

However, sovereign warships and state-operated vessels enjoy broad legal exemptions under international and national law:

### 63.2.1 SOLAS Sovereign Immunity Exemption
Under SOLAS Chapter I, Regulation 3(a), the convention explicitly states that its regulations—unless expressly provided otherwise—do not apply to "ships of war and troopships." Consequently, naval warships are not legally bound by the mandatory carriage or operation rules of SOLAS Chapter V, Regulation 19.

Furthermore, IMO Resolution A.1106(29), which superseded Resolution A.917(22) as the governing *Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems (AIS)*, reinforces the master's operational authority. Paragraph 22 stipulates:
> "The AIS should always be in operation when ships are underway or at anchor. If the master believes that the continual operation of AIS might compromise the safety or security of his ship or where security incidents are imminent, the AIS may be switched off."

Paragraph 3 affirms that the guidelines apply to ships subject to SOLAS Chapter V, recognizing that sovereign vessels operate outside commercial mandates.

### 63.2.2 United States Statutory and Regulatory Exemptions
In the United States, maritime navigation safety regulations mirror this international doctrine. Title 33 of the Code of Federal Regulations (**CFR**), Section 164.46, mandates AIS Class A carriage for commercial vessels on U.S. navigable waters. However, 33 CFR § 164.01(c) explicitly exempts sovereign vessels:
> "This part does not apply to: ... Warships, naval auxiliaries, or other vessels owned or operated by a State or by the United States and used, for the time being, only on government non-commercial service, provided that each such vessel is equipped with electronic navigation systems that meet the requirements of the agency concerned."

Naval vessels are similarly exempt from statutory licensing and type-approval mandates governed by the Federal Communications Commission (**FCC**) under 47 CFR Part 80. Instead, military maritime radio transmitters operate under frequency authorizations issued by the National Telecommunications and Information Administration (**NTIA**) within the executive branch.

> **Legal note.**
> - **Jurisdiction & Immunity:** Warships and state-operated non-commercial vessels possess sovereign immunity under customary international law and the United Nations Convention on the Law of the Sea (**UNCLOS**, Articles 32, 95, and 96). They are exempt from coastal and port state jurisdiction, enforcement boarding, and mandatory commercial radio carriage rules.
> - **SOLAS Status:** Under SOLAS Chapter I, Regulation 3, and IMO Resolution A.1106(29), warships are not legally bound to broadcast AIS. Commanding officers possess sovereign authority to silence, alter, or encrypt their broadcasts at their discretion.
> - **National Compliance:** In U.S. navigable waters, warships are explicitly excluded from commercial AIS rules pursuant to 33 CFR § 164.01(c). Similar sovereign immunity exemptions exist across European Union maritime safety directives (e.g., Directive 2002/59/EC, Article 2(2)).
> - **Civil Liability Consequences:** Sovereign immunity from regulatory enforcement does not shield a government from civil liability in admiralty collisions. In international maritime collision litigation (governed by the International Regulations for Preventing Collisions at Sea, **COLREGs**), admiralty courts consistently evaluate whether running "AIS dark" or emitting misleading data in congested fairways violates the "ordinary practice of seamen" under Rule 2 (Responsibility) or contributes to a failure to maintain a proper lookout under Rule 5. Sovereign exemption from carriage does not constitute a legal defense against maritime negligence.

## 63.3 NATO standards: STANAG 4668 and STANAG 4669

To achieve seamless interoperability across allied naval forces while mitigating operational vulnerabilities, the North Atlantic Treaty Organization (**NATO**) standardized military AIS requirements through two primary Standardization Agreements (**STANAGs**):

```
+-----------------------------------------------------------------------------------+
|                            NATO W-AIS ARCHITECTURE                                |
+-----------------------------------------------------------------------------------+
|  STANAG 4668: TECHNICAL SPECIFICATION                                             |
|  - Physical & Link Layer: ITU-R M.1371 compliance                                 |
|  - RF Bands: Standard maritime VHF (AIS 1/2) + Military VHF-P                     |
|  - Protocol Containers: Encrypted ASM payloads (Msg 25 / Msg 26)                  |
|  - Cryptographic Algorithms: Symmetric block ciphers (AES-128/256, Blowfish)      |
+-----------------------------------------------------------------------------------+
                                      |
                                      v
+-----------------------------------------------------------------------------------+
|  STANAG 4669: OPERATIONAL EMPLOYMENT GUIDELINES                                   |
|  - Operational Modes: Active, Passive (Silent), Protected, Deceptive (Simulated)  |
|  - Identity Management: Dynamic masking, alternative call signs/MMSIs             |
|  - Integration: Electronic Chart Precise Integrated Navigation Systems (ECPINS)   |
|  - Tactical Picture: Blue Force Tracking (BFT) fused into Combat Management System|
+-----------------------------------------------------------------------------------+
```

### 63.3.1 STANAG 4668 (Technical Specification for W-AIS)
NATO STANAG 4668, titled *Warship - Automatic Identification System (W-AIS)* (Edition 2 promulgated in March 2010), defines the technical architecture, data structures, and cryptographic interfaces required for military shipborne AIS equipment.

The standard establishes that a compliant W-AIS transponder must retain physical-layer compatibility with civil Class A transponders governed by Recommendation ITU-R M.1371 and IEC 61993-2. This ensures that a warship can operate in an unclassified civil mode without requiring auxiliary civilian transponders.

STANAG 4668 specifies two core operational frequencies and protocol layers:
- **Civilian VDL Mode:** Transmits and receives standard ITU-R M.1371 messages over international maritime VHF channels AIS 1 (161.975 MHz) and AIS 2 (162.025 MHz) using Gaussian Minimum Shift Keying (**GMSK**) at 9,600 bit/s.
- **Protected Tactical Mode:** Injects encrypted payloads into standard single-slot (Message 25) and multi-slot (Message 26) binary containers, or transitions transmission entirely to dedicated military VHF frequencies (often designated within the NATO VHF-P maritime band).
- **Cryptographic Engine:** Outlines standardized interfaces to symmetric encryption algorithms. The standard mandates or supports Advanced Encryption Standard (**AES**) with 128-bit or 256-bit keys, as well as legacy support for Blowfish with variable key lengths (up to 448 bits), ensuring robust data confidentiality against civilian intercept receivers.

### 63.3.2 STANAG 4669 (Operational Employment of AIS on Warships)
While STANAG 4668 defines the radio and message formats, STANAG 4669, titled *Automatic Identification System (AIS) on Warships* (Edition 2 promulgated in March 2010), establishes doctrinal operating procedures for allied naval vessels.

STANAG 4669 defines five standard operational states:
1. **Active (Standard Civil) Mode:** The W-AIS transponder broadcasts authentic vessel telemetry (valid MMSI, true name, true dimensions, and live GNSS position) exactly like a commercial Class A transponder. This mode is employed during routine peacetime open-ocean transits, port arrivals, and when operating under civil Vessel Traffic Services (**VTS**) control.
2. **Passive (Silent / Receive-Only) Mode:** The transponder's RF power amplifiers are inhibited, completely disabling all autonomous transmissions on both AIS channels. However, the dual-channel receiver remains fully active, feeding incoming commercial AIS tracks into the ship's navigation consoles and Combat Management System (**CMS**). This mode allows the warship to maintain complete maritime situational awareness while preserving total electromagnetic silence.
3. **Protected (Encrypted / Blue Force) Mode:** The transponder ceases broadcasting open position reports (Messages 1, 2, and 3). Instead, it broadcasts encrypted tactical data bursts (using Message 25 or 26) either on AIS 1/2 or on an assigned tactical channel. Only authorized coalition vessels possessing the appropriate cryptographic key variables can decrypt and plot these blue-force tracks.
4. **Restricted / Masked Mode:** The vessel broadcasts on public channels but dynamically modifies static and voyage data. For example, a warship may broadcast a generic merchant ship type, mask its naval identity, or adjust its reported dimensions while broadcasting accurate kinematics to facilitate collision avoidance without disclosing combatant status.
5. **Simulated / Deceptive Mode:** Authorized only under specific tactical operational orders, the system generates artificial AIS tracks, position offsets, or simulated phantom vessel contacts to mislead adversary Electronic Support Measures and commercial tracking systems.

## 63.4 Vendor implementations and commercial-military architectures

Naval forces typically acquire W-AIS capabilities through specialized defense electronics contractors who develop military-grade variants of commercial maritime transponders.

### 63.4.1 Saab TransponderTech: Secure Link and the R4/R5/R6 Architecture
Saab TransponderTech (a pioneer of civilian Self-Organized TDMA technology) produces the primary W-AIS hardware utilized by numerous NATO and international navies. The architecture evolved across three major generations:
- **Saab R4S / R4A / R40 Secure:** Introduced the foundational concept of the "Secure Link." The R4S transponder utilized an internal cryptographic board to encapsulate encrypted telemetry into addressed Message 6 or broadcast binary messages. It pioneered the use of a dedicated "third channel" (a tunable VHF synthesizer operating outside AIS 1 and AIS 2), allowing naval task groups to conduct encrypted communications without consuming civilian VDL slot capacity.
- **Saab R5 Supreme Secure / W-AIS:** Built upon a flexible Software-Defined Radio (**SDR**) processing core. The R5 Secure system interfaces directly with naval Electronic Chart Precise Integrated Navigation Systems (**ECPINS**), such as those developed by OSI Maritime Systems. It provides multi-level security separation, automated key loading via standard fill devices, and support for NATO STANAG 4668 modes.
- **Saab R6 Supreme Secure (VDES Generation):** The modern generation of secure transponders incorporates full VHF Data Exchange System (**VDES**) capabilities compliant with Recommendation ITU-R M.2092-1 ([Chapter 69](ch69-vdes-ais-2.md)), featuring an SDR architecture with up to 64 parallel processing channels. It supports:
  - Simultaneous monitoring of civilian AIS 1, AIS 2, and Application-Specific Message channels (ASM 1 at 161.950 MHz and ASM 2 at 162.000 MHz).
  - Dedicated third-channel tactical operation on frequencies between 156.000 MHz and 162.500 MHz.
  - Organizational sub-grouping: The Saab Secure Link protocol allows up to eight distinct sub-groups (e.g., naval strike group, auxiliary supply vessels, coast guard cutters, special operations craft) to share a single RF channel while segregating their tactical tracking feeds using distinct organizational cryptographic key identifiers.

```
+-----------------------------------------------------------------------------------+
|                        SAAB R6 SUPREME SECURE ARCHITECTURE                        |
+-----------------------------------------------------------------------------------+
|               DUAL BROADBAND VHF ANTENNA / PRE-SELECTOR (156-163 MHz)             |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                 MULTI-CHANNEL SOFTWARE-DEFINED RADIO (SDR) ENGINE                 |
|  +---------------------+  +---------------------+  +----------------------------+ |
|  |  Receiver A (AIS 1) |  |  Receiver B (AIS 2) |  |  Dedicated Tactical Ch.    | |
|  |  161.975 MHz GMSK   |  |  162.025 MHz GMSK   |  |  User-tuned (VHF-P)        | |
|  +---------------------+  +---------------------+  +----------------------------+ |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
+-----------------------------------------------------------------------------------+
|                           CRYPTOGRAPHIC PROCESSING ENGINE                         |
|  - Cryptographic Subsystem (AES-128 / AES-256 / Blowfish)                         |
|  - Key Management Store (Up to 8 organizational sub-group crypto keys)             |
|  - Plaintext / Ciphertext Red-Black Isolation Boundary                            |
+-----------------------------------------------------------------------------------+
       |                                                              |
       v (Decrypted Tactical Tracks)                                  v (Civilian Tracks)
+-----------------------------------------------------------------------------------+
|               PRESENTATION INTERFACE (IEC 61162-450 DUAL LAN / RS-422)            |
|  - Naval CMS / C2 Systems (Link 16 / Link 22 / JREAP Fusion)                      |
|  - Warship Electronic Chart Display (OSI ECPINS / Tactical Radar)                 |
+-----------------------------------------------------------------------------------+
```

### 63.4.2 Kongsberg Discovery / Seatex: AIS Blue Force Series
Kongsberg manufactures the AIS 300BF and subsequent military variants, engineered for coast guard cutters, naval auxiliaries, and maritime surveillance aircraft.
- The Kongsberg Blue Force architecture focuses on stealth and autonomous tactical plotting. In "Protective Mode," the transponder completely inhibits open transmission on civil frequencies while continuously generating encrypted Blue Force telemetry.
- Kongsberg transponders are frequently integrated with the Norwegian Armed Forces and international coast guards, using proprietary cryptographic overlays that allow aircraft (such as maritime patrol aircraft like the P-8A Poseidon) to act as airborne Blue Force relays, extending tactical VDL coverage over the horizon.

### 63.4.3 L3Harris: ProTec and ProTec-M
L-3 Communications (now L3Harris Technologies) developed the ProTec-M Class A military AIS transponder. Engineered to military shock and vibration specifications (MIL-STD-810 and MIL-STD-461 for electromagnetic compatibility), the ProTec-M supports STANAG 4668 Edition 2. It features hardware-enforced crypto-ignition keys (**CIKs**) and zeroize switches to rapidly erase cryptographic key variables in the event of imminent vessel boarding or compromise.

> **Threat model.**
> - **Primary Assets:** Tactical unit disposition; combatant identity; warship patrol tracks; coalition force composition; integrity of warship navigation and Electronic Chart Systems.
> - **Threat Actors:** Adversary naval intelligence services; foreign Electronic Support Measures (**ESM**) and signals intelligence (**SIGINT**) collection stations; low-Earth-orbit commercial and military RF reconnaissance satellites; non-state hostile actors, pirates, and asymmetric surface threats.
> - **Attacker Capabilities:**
>   - *Passive SIGINT/ESM:* Broadband intercept receivers capable of detecting, logging, and direction-finding unencrypted 12.5 W VHF transmissions across hundreds of miles via elevated antennas or satellite constellations.
>   - *Physical-layer RF Fingerprinting:* Measuring subtle transient turn-on characteristics, phase jitter, and frequency offsets of GMSK transmissions to uniquely identify specific transponder hardware, even when vessels randomize their MMSIs ([Chapter 60](ch60-malicious-payloads-robustness.md)).
>   - *Spoofing and Network Flooding:* Injecting false phantom targets or jamming civilian VDL channels to degrade warship situational awareness during tactical evolutions ([Chapter 59](ch59-spoofing.md); [Chapter 61](ch61-timing-and-network-attacks.md)).
> - **Impact:** Loss of operational surprise; exposure of covert operations and special warfare insertions; target cueing for over-the-horizon anti-ship missiles; increased collision risk during EMCON operations.
> - **Engineering Mitigations:** Strict operational adherence to STANAG 4669 tactical modes; utilization of military-grade symmetric encryption (AES-256) embedded in standardized Message 26 containers; off-band transmission on dedicated VHF-P frequencies; hardware zeroize mechanisms for key management; RF power attenuation (1 W low-power mode) in close-quarters littoral navigation.

## 63.5 United States Navy and Coast Guard practices: EAIS and the post-2017 doctrine

The operational employment of AIS by United States maritime armed forces reflects a distinct divergence between military combatant forces and law enforcement/homeland security missions.

### 63.5.1 The United States Coast Guard: EAIS and STEDS
The United States Coast Guard (**USCG**), operating under both the Department of Homeland Security and Title 14 of the U.S. Code, maintains an extensive fleet of national security cutters, patrol boats, and response boats. Because USCG units execute law enforcement, counter-narcotics interdiction, and fisheries protection missions alongside Search and Rescue (**SAR**), broadcasting open AIS would alert smugglers and non-compliant vessels to cutter movements.

To support these missions, the USCG established the **Encrypted Automatic Identification System (EAIS)** program, governed by the *EAIS Interface Design Description (IDD)*:
- **STEDS Integration:** EAIS interfaces directly with the USCG's Sensitive But Unclassified Tactical Information Exchange and Display System (**STEDS**). This allows USCG command centers, sector command posts, and cutter command bridges to share real-time tactical tracks and Common Operational Pictures (**COPs**) across the Nationwide Automatic Identification System (**NAIS**) infrastructure ([Chapter 46](ch46-government-software.md)).
- **AIS Ad-Hoc Networks (AISANETs):** EAIS enables tactical units on scene to form encrypted ad-hoc tactical clusters. Cutters, small boats, and MH-60T / MH-65E helicopters exchange high-rate encrypted kinematic tracks without alerting target vessels.

### 63.5.2 United States Navy Post-2017 AIS Doctrine
Prior to late 2017, the United States Navy maintained an institutional culture prioritizing emissions security over civilian transparency. Surface combatants routinely operated with their AIS transponders turned off (passive receive-only mode or complete power-down), even while transiting congested international commercial waterways.

This operational posture contributed directly to two catastrophic surface collisions in the Western Pacific in the summer of 2017:
- **USS *Fitzgerald* (DDG 62) Collision:** On 17 June 2017, the guided-missile destroyer USS *Fitzgerald* collided with the Philippine-flagged container ship *ACX Crystal* in the high-density approaches to Tokyo Bay, Japan, resulting in the deaths of seven U.S. Navy sailors. The *Fitzgerald*'s AIS transponder was secured (off), leaving the container ship's watchstanders unaware of the warship's identity and dynamic maneuvers until seconds before impact.
- **USS *John S. McCain* (DDG 56) Collision:** On 21 August 2017, the guided-missile destroyer USS *John S. McCain* collided with the chemical tanker *Alnic MC* near the eastern entrance to the Singapore Strait TSS, resulting in the deaths of ten U.S. Navy sailors. Like the *Fitzgerald*, the *John S. McCain* was navigating one of the most heavily congested maritime choke points in the world with its AIS transmitter turned off.

```
+-----------------------------------------------------------------------------------+
|                     POST-2017 U.S. NAVY AIS DOCTRINAL REVERSAL                    |
+-----------------------------------------------------------------------------------+
|  PRE-2017 POLICY: "DEFAULT DARK"                                                  |
|  - Presumption of OPSEC priority across all underway operations                   |
|  - AIS transmitters powered off or placed in passive mode                         |
|  - Commercial traffic forced to rely entirely on primary radar / visual contact   |
|  - Result: 2017 Western Pacific collisions (17 fatalities, catastrophic damage)   |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
|  THE REVERSAL: ADMIRAL JOHN RICHARDSON (CNO) DIRECTIVE (SEPTEMBER 2017)           |
|  - Stated Navy held a "distorted perception of operational security"              |
|  - Mandated active AIS transmission in congested waterways and TSSs               |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
|  CURRENT OPERATIONAL DOCTRINE (COMNAVSURFPAC / COMNAVSURFLANT GUIDANCE)           |
|  - MANDATORY AIS ON: Coastal navigation, port approaches, archipelagic waters,    |
|    Traffic Separation Schemes (TSSs), and designated high-density waterways.      |
|  - CO DISCRETION TO SILENCE: Restricted strictly to tactical combat evolutions,   |
|    contested waters, amphibious warfare exercises, or specific strike missions.   |
|  - Standardized integration into Surface Force Navigation Instructions.           |
+-----------------------------------------------------------------------------------+
```

Following investigations by the Navy and the National Transportation Safety Board (**NTSB**), Chief of Naval Operations (**CNO**) Admiral John Richardson testified before Congress in September 2017, stating that the fleet held a "distorted perception of operational security" regarding AIS, and issued a direct fleet directive reversing historical practice.

Commander, Naval Surface Forces (**COMNAVSURFOR**), alongside Pacific and Atlantic Fleet type commanders (COMNAVSURFPAC / COMNAVSURFLANT), codified the updated doctrine:
1. **Mandatory Broadcast in Congested Waters:** U.S. Navy surface combatants are required to actively transmit AIS Class A data when operating in coastal waters, harbor approaches, designated Traffic Separation Schemes, and waterways with heavy commercial traffic densities.
2. **Commanding Officer Authority:** The authority to secure (turn off) AIS transmission is restricted to specific, justified tactical scenarios—such as combat operations, classified task group maneuvering, or operations where the tactical commander formally declares that electronic emissions present an unacceptable threat.

## 63.6 TDMA slot occupancy, spectrum physics, and civilian coexistence

A critical engineering question regarding encrypted and military AIS is its coexistence with civilian traffic on the VHF data link.

The SOTDMA protocol divides each 60-second frame on AIS 1 and AIS 2 into 2,250 time slots, providing a combined total of 4,500 slots per minute across both channels ([Chapter 21](ch21-link-layer-tdma.md)). The network relies on strict distributed slot scheduling: transponders broadcast their current position alongside the exact slot number they intend to occupy in subsequent frames.

```
+-----------------------------------------------------------------------------------+
|               TDMA COEXISTENCE: ENCRYPTED MESSAGE 26 ON THE VDL                   |
+-----------------------------------------------------------------------------------+
| Slot N     | Preamble (24) | Start Flag (8) | Encrypted Payload | CRC (16) | End  |
|            | 0101010101... |    01111110    | (Msg 26, DAC 366) | Checksum | Flag |
+-----------------------------------------------------------------------------------+
|            |                                                    |                 |
|            v                                                    v                 |
|  Physical Layer (All Receivers):               Link Layer (Civilian Receivers):   |
|  - Energy detected above carrier sense         - Packet decoded; CRC-16 passes    |
|  - SOTDMA slot marked "OCCUPIED"               - Recognized as Message 26         |
|  - SOTDMA comm state preserved                 - Payload unparseable (discarded)  |
|  - No RF collision or packet corruption        - Slot reservation respected       |
+-----------------------------------------------------------------------------------+
```

When military vessels operate on public maritime channels AIS 1 and AIS 2, they must maintain protocol coexistence to avoid collapsing the local SOTDMA cell:

### 63.6.1 Standard Encrypted ASM Encapsulation
When transmitting encrypted data over public channels, compliant military transponders encapsulate ciphertext into ITU-R M.1371 **Message 26** (*Multi-slot Binary Message with Communications State*).

Message 26 is uniquely suited for secure operations because it retains an unencrypted 20-bit communications state tail (SOTDMA or Incremental TDMA, **ITDMA**). Its burst structure preserves standard framing:
- **Preamble and Start Flag:** Transmitted in the clear (24-bit preamble and 8-bit HDLC start flag `01111110`) to enable carrier recovery, bit synchronization, and frame locking ([Chapter 28](ch28-rf-encoding-physical-layer.md)).
- **Container Header:** Unencrypted 6-bit message ID (26), 2-bit repeat indicator, 30-bit source MMSI, and 16-bit Application Identifier (DAC/FI).
- **Ciphertext Payload:** The application data field contains the ciphertext produced by the cryptographic processor.
- **Communications State:** The unencrypted 20-bit comm-state announces future slot reservations under standard SOTDMA rules.
- **FCS and End Flag:** The 16-bit CRC-16 checksum and 8-bit end flag are computed across the entire burst and transmitted in the clear.

### 63.6.2 Link Layer Behavior of Civilian Receivers
When a standard civilian Class A or Class B transponder receives this transmission, the following sequence occurs:
1. The civilian receiver's physical layer demodulates the GMSK signal and validates the 16-bit CRC checksum. Because the CRC is calculated over the ciphertext, the burst is verified as error-free.
2. The link layer extracts the SOTDMA comm-state bits. The civilian transponder enters the reserved slot number into its internal slot map as **OCCUPIED**. Consequently, no civilian transponder within the RF line-of-sight cell will select or transmit in that reserved slot, preventing packet collision.
3. The presentation layer examines the Application Identifier (e.g., DAC 366). Because the civilian software lacks the cryptographic key to parse the proprietary ciphertext payload, the message is discarded without error, or passed to the presentation interface as an unparsed `!AIVDM` sentence.

Thus, **encrypted AIS transmissions on public channels fully consume TDMA slot capacity.** A naval squadron exchanging encrypted telemetry on AIS 1 and AIS 2 imposes the exact same channel loading burden on the local cell as commercial ships broadcasting standard position reports.

### 63.6.3 Dedicated Tactical Channels (Third-Channel Operation)
To eliminate spectrum contention in crowded ports and preserve civilian safety margins, modern W-AIS architectures (such as the Saab R6 Supreme Secure) utilize dedicated VHF tactical channels.

By shifting encrypted transmissions to designated military VHF frequencies (e.g., frequencies in the 156.000–162.000 MHz maritime band licensed to military authorities), naval units achieve:
- **Zero Civilian Contention:** The tactical transmissions do not consume any of the 4,500 slots per minute on AIS 1 and AIS 2.
- **Enhanced LPI/LPD:** By transmitting on tactical channels at reduced RF power (e.g., 1 W or 2 W), naval forces drastically reduce their Probability of Intercept (**LPI**) and Probability of Detection (**LPD**) by civilian shore aggregators.
- **Independent SOTDMA Cell:** The naval units establish an independent, synchronized TDMA cell on the tactical channel, utilizing GNSS 1 Pulse Per Second (**1PPS**) timing references to schedule slots without interference from merchant traffic.

## 63.7 Cryptographic key management and coalition interoperability

The technical feasibility of encrypted maritime AIS hinges on robust, standardized cryptographic key management. Because warships frequently deploy in multinational task forces (such as NATO Standing Maritime Groups or combined coalition task forces), cryptographic architectures must support secure key distribution across disparate national systems.

### 63.7.1 Symmetric Cryptography and the Broadcast Constraint
AIS is structurally a broadcast system. A transmitting vessel cannot establish an interactive, negotiated session key (such as an ephemeral Diffie-Hellman handshake) with every unknown observer within VHF line-of-sight. Therefore, tactical encrypted AIS relies on **pre-shared symmetric key variables**.

Every authorized participant in a tactical network must be loaded with identical cryptographic keys:
- **AES-128 / AES-256:** The primary symmetric cipher mandated under NATO STANAG 4668. Payloads are encrypted using block ciphers operating in Cipher Block Chaining (**CBC**) mode or Galois/Counter Mode (**GCM**).
- **Blowfish:** Utilized in legacy military systems and early Saab Secure Link implementations. Blowfish provides high encryption throughput with variable key lengths, but is being systematically phased out in favor of FIPS-compliant AES variants.

### 63.7.2 Key Loading and Fill Devices
Cryptographic keys are distributed and loaded into transponders through standardized military communication security (**COMSEC**) protocols:
- **Electronic Key Loading:** Keys generated by national security authorities are transferred to transponders via Electronic Key Management Systems (**EKMS**) or Key Management Infrastructure (**KMI**).
- **DS-101 / DS-102 Interfaces:** Transponders incorporate front-panel connectors interfacing directly with military fill devices, such as the AN/PYQ-10 Simple Key Loader (**SKL**).
- **Crypto-Ignition Keys (CIKs) and Zeroization:** Physical CIK tokens activate internal key registers. In the event of imminent capture or boarding, activating the zeroize switch dumps key registers to ground in milliseconds.

```
+-----------------------------------------------------------------------------------+
|                        TACTICAL KEY MANAGEMENT HIERARCHY                          |
+-----------------------------------------------------------------------------------+
|  NATIONAL / ALLIED CRYPTOGRAPHIC AUTHORITY (e.g., NSA / NATO Cryptographic Agency)|
|  - Generation of Daily / Weekly / Monthly Symmetric Key Variables                |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
|  ELECTRONIC KEY MANAGEMENT SYSTEM (EKMS / KMI)                                    |
|  - Distribution via secure networks to naval bases and deployed flagships         |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
|  PORTABLE FILL DEVICES (AN/PYQ-10 Simple Key Loader [SKL])                        |
|  - Point-to-point electronic injection into shipboard W-AIS transponders          |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
|  SHIPBOARD W-AIS TRANSPONDER CRYPTOGRAPHIC ENGINE                                 |
|  - Multi-tiered key registers:                                                    |
|    * K_strat : Strategic Fleet Key (Broad blue-force identification)              |
|    * K_tac   : Tactical Task Group Key (Local coalition strike group)             |
|    * K_org   : Organizational Sub-Group Key (e.g., Special Warfare / Boarding team|
|  - Hardware Zeroize: Instantaneous erasure on emergency activation                |
+-----------------------------------------------------------------------------------+
```

### 63.7.3 Key Expiration and Rekeying Vulnerabilities
The operational Achilles' heel of encrypted AIS is key expiration and distribution latency. In distributed maritime operations, if a single allied warship fails to receive an updated cryptographic key roll (e.g., a monthly variable rollover), that vessel immediately drops out of the automated Blue Force Tracking picture.

On the bridge consoles of neighboring allied vessels, the non-updated warship's transmissions will decode as corrupted or unparseable binary ASM packets, causing the vessel to vanish from the tactical screen. Conversely, if a single key is compromised or captured, the confidentiality of the entire tactical AIS network is compromised until emergency out-of-band rekeying can be executed across all deployed assets.

## Then & now

- **1990** ⟨H⟩ Benny Pettersson and the Swedish Maritime Administration initiate the development of digital maritime transponders, originally targeting civilian ferry safety and VTS.
- **1992** ⟨H⟩ Early civil transponder developer fails; patent holder Håkan Lans and Swedish defense authorities adapt the underlying GP&C technology for military coordination and aircraft tracking.
- **1998** ⟨+⟩ ITU adopts Recommendation ITU-R M.1371-1, establishing open, unencrypted Self-Organized TDMA as the international baseline for civilian maritime tracking, deliberately omitting cryptographic protections to ensure rapid global merchant adoption (ITU-R M.1371-1, 1998).
- **2002** ⟨+⟩ IMO SOLAS Chapter V carriage mandates enter into force; NATO navies recognize that unencrypted Class A transmissions create critical operational security (OPSEC) vulnerabilities for warships, initiating W-AIS studies.
- **2004** ⟨+⟩ Saab TransponderTech introduces the R4S secure transponder family, pioneering the "Secure Link" concept using encrypted Type 6/8 messages and dedicated third-channel VHF operation for naval and governmental vessels.
- **2005** ⟨+⟩ Saab and Kongsberg supply specialized Blue Force transponders to Nordic and NATO coast guards; early encrypted implementations rely on Blowfish and proprietary vendor ciphers.
- **2010** ⟨+⟩ NATO promulgates STANAG 4668 Edition 2 (*Warship - Automatic Identification System*) and STANAG 4669 Edition 2 (*Automatic Identification System on Warships*), standardizing W-AIS technical requirements, symmetric encryption interfaces (AES-128/256), and tactical employment modes across alliance navies.
- **2011–2014** ⟨+⟩ NOAA and BOEM publish U.S. Marine Cadastre AIS data products; at the request of the USCG, MMSI identifiers are cryptographically hashed and vessel names removed to protect commercial and military operational patterns, a practice discontinued in 2015 when raw MMSIs are restored.
- **2016–2017** ⟨+⟩ USCG formalizes the Encrypted AIS (EAIS) family of Application-Specific Messages under DAC 366 (e.g., Message 26 FI 13 SAR pattern, FI 15 trackline, FI 39 static data), integrating encrypted tactical tracking into STEDS and NAIS (IALA ASM Register, 2017).
- **2017** ⟨+⟩ Peacetime surface collisions involving the USS *Fitzgerald* (June) and USS *John S. McCain* (August)—operating with their AIS secured ("dark") in high-density Asian traffic—claim 17 lives. In September 2017, Chief of Naval Operations Admiral John Richardson directs U.S. Navy warships to transmit AIS in congested waters, reversing decades of "default dark" fleet culture.
- **2023** ⟨+⟩ Saab launches the R6 Supreme Secure transponder series, integrating multi-channel Software-Defined Radio architectures, VDES spectrum support (ITU-R M.2092-1), and 64-channel parallel signal processing for allied naval operations.

## On the wire

Encrypted military and governmental AIS payloads rely almost exclusively on **Message 25** (*Single Slot Binary Message*) and **Message 26** (*Multi-slot Binary Message with Communications State*). Message 26 provides the optimal container on public VDL channels because its trailing communications state allows transponders to reserve future slots, maintaining harmony with civilian SOTDMA cells.

### Structure of an Encrypted Message 26 Burst

Under United States Coast Guard EAIS specifications and NATO STANAG 4668 implementations, encrypted tactical data is structured within a Message 26 container using Designated Area Code (**DAC**) 366 (United States) or an international tactical DAC.

| Field Name | Bit Width | Data Type | Description |
|---|---|---|---|
| Message ID | 6 | `uint` | Constant = 26 (Message 26) |
| Repeat Indicator | 2 | `uint` | Broadcast repeat count (typically 0) |
| Source MMSI | 30 | `uint` | True or masked military MMSI |
| Destination Indicator | 1 | `bool` | 0 = Broadcast; 1 = Addressed |
| Binary Data Flag | 1 | `bool` | 1 = Application Identifier (AI) structured |
| Designated Area Code (DAC) | 10 | `uint` | DAC 366 (United States EAIS / Military) |
| Function Identifier (FI) | 6 | `uint` | e.g., FI 15 (Trackline) or FI 39 (Static Data) |
| Encryption Sub-Header | 16 | `bit` | Security Association ID / Key Identifier |
| Initialization Vector (IV) | 64 | `bit` | Ciphertext initialization vector / Nonce |
| Encrypted Payload | 128–896 | `bit` | Ciphertext (AES-128 or AES-256 block-aligned) |
| Comm-State Selector | 1 | `bool` | 0 = SOTDMA; 1 = ITDMA |
| SOTDMA / ITDMA State | 19 | `bit` | Slot reservation tail for network coexistence |

```
+----------------------------------------------------------------------------------------------------+
|                                ANATOMY OF AN ENCRYPTED MESSAGE 26 BURST                            |
+----------------------------------------------------------------------------------------------------+
| Msg ID | Rep | Source MMSI | D | B |  DAC  |  FI  |  Crypto Key ID  |      Ciphertext Payload      |
| 6 bits |  2  |   30 bits   | 1 | 1 |10 bits|6 bits|     16 bits     |       (AES-128 Blocks)       |
+----------------------------------------------------------------------------------------------------+
|  011010| 00  |  369999000  | 0 | 1 |  366  |  39  | 0x04A2 (Key #4) | Encrypted Static/Voyage Data |
+----------------------------------------------------------------------------------------------------+
                                                                      |
                                                                      v
                                                    +-----------------------------------+
                                                    | Comm-State Selector | SOTDMA Tail |
                                                    |        1 bit        |   19 bits   |
                                                    +-----------------------------------+
                                                    |          0          |  Slot Res.  |
                                                    +-----------------------------------+
```

### NMEA Presentation Interface: `!AIVDM` Sentence Decoding

Standard civilian receivers that intercept an encrypted Message 26 burst cannot parse the ciphertext, but they correctly decode and emit a standard NMEA 0183 / IEC 61162-1 `!AIVDM` sentence over their bridge serial interfaces ([Chapter 26](ch26-interfaces-and-logging.md)).

Consider the following two-part encapsulated `!AIVDM` sentence captured from an encrypted naval transponder operating on Channel B (162.025 MHz):

```text
!AIVDM,2,1,7,B,J03000?0000000000000000000000000000000000000,0*1E
!AIVDM,2,2,7,B,000000000008,0*1C
```

> **Try it.**
> Run the following Python snippet to verify the bit layout, DAC/FI extraction, and communications state of an unencrypted container carrying a proprietary binary payload:
>
> ```python
> import bitstring
> 
> # Simulating decoded 240-bit Message 26 binary payload
> # MsgID (6b=26) + Repeat (2b=0) + MMSI (30b=369999000) + Dest (1b=0) + BinFlag (1b=1)
> # DAC (10b=366) + FI (6b=39) + KeyID (16b=0x04A2) + Ciphertext + CommState (20b)
> payload_bits = bitstring.BitArray(
>     uint=26, length=6
> ) + bitstring.BitArray(
>     uint=0, length=2
> ) + bitstring.BitArray(
>     uint=369999000, length=30
> ) + bitstring.BitArray(
>     uint=0, length=1
> ) + bitstring.BitArray(
>     uint=1, length=1
> ) + bitstring.BitArray(
>     uint=366, length=10
> ) + bitstring.BitArray(
>     uint=39, length=6
> ) + bitstring.BitArray(
>     uint=0x04A2, length=16
> )
> 
> print(f"Message ID:  {payload_bits[0:6].uint}")
> print(f"Source MMSI: {payload_bits[8:38].uint}")
> print(f"DAC:         {payload_bits[40:50].uint}")
> print(f"FI:          {payload_bits[50:56].uint}")
> print(f"Key ID:      0x{payload_bits[56:72].uint:04X}")
> ```
> Expected output:
> ```text
> Message ID:  26
> Source MMSI: 369999000
> DAC:         366
> FI:          39
> Key ID:      0x04A2
> ```

## Validation, uncertainty & data quality

Analyzing and integrating military and encrypted AIS data presents severe validation challenges for both defense analysts and civilian vessel traffic managers.

### Error Propagation in Encrypted Maritime Feeds
Errors in military AIS environments propagate primarily through three mechanisms:
1. **Cryptographic Key Misalignment:** If an authorized unit possesses an expired key variable or an unsynchronized Key Identifier (**Key ID**), 100% of received tactical bursts fail decryption. Unlike civil AIS, where partial packet corruptions can occasionally be reconciled, symmetric block ciphers exhibit an extreme avalanche effect: a single incorrect key bit causes the decrypted plaintext to become random noise.
2. **GNSS SOTDMA Clock Desynchronization:** Military transponders frequently operate in environments subject to intentional electronic warfare, including GNSS jamming and spoofing ([Chapter 62](ch62-gnss-jamming-spoofing.md)). If a warship's internal GNSS timing receiver loses synchronization with UTC 1PPS:
   - The transponder cannot accurately align its transmission bursts with the 26.67 ms TDMA time slots.
   - Slot timing drifts across adjacent slot boundaries, causing packet collisions with civilian merchant vessels and degrading the local SOTDMA cell.
   - Transponders must immediately drop back to indirect synchronization via terrestrial base stations or revert to Incremental TDMA (**ITDMA**).
3. **Deceptive and Masked Metadata Ingestion:** When warships operate in STANAG 4669 "Masked Mode"—broadcasting generic cargo vessel types or modified call signs—downstream civilian databases ingest erroneous static profiles. Automated vessel intelligence platforms (e.g., MarineTraffic, Spire, Pole Star) permanently bind these false static declarations to the warship's MMSI, polluting historical registries and disrupting automated port-call analytics.

### Concrete Verification Procedure
Naval operations centers and intelligence fusion nodes apply a rigorous multi-stage validation pipeline to cross-verify military AIS telemetry against non-cooperative sensors:

```
+-----------------------------------------------------------------------------------+
|                     WARSHIP TRACK VERIFICATION PIPELINE                           |
+-----------------------------------------------------------------------------------+
|  1. RF PHYSICAL LAYER CAPTURE                                                     |
|     - Measure burst center frequency (161.975 / 162.025 MHz +/- 500 Hz tolerance) |
|     - Verify GMSK modulation index (h = 0.5 +/- 0.05) & BT = 0.4                  |
|     - Measure Time Difference of Arrival (TDOA) across multi-station receiver net |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
|  2. LINK LAYER & CIPHER INTEGRITY                                                 |
|     - Check CRC-16 checksum integrity over unencrypted frame                      |
|     - Verify SOTDMA slot reservation against local dynamic slot map               |
|     - Validate Key ID against active Task Group Key Register                      |
|     - Execute AES-GCM / CBC decryption; verify message authentication code (MAC)  |
+-----------------------------------------------------------------------------------+
                                         |
                                         v
|  3. KINEMATIC & MULTI-INT FUSION                                                  |
|     - Kinematic plausibility check: Acceleration < 2.5 m/s^2; Rate of turn match  |
|     - Primary Radar Cross-Bearing (S-band / X-band track correlation)             |
|     - Commercial Spaceborne Synthetic Aperture Radar (SAR) match (e.g. Sentinel-1)|
|     - Optical / ESM signature correlation (IFF Mode 5 / Link 16 J-Series match)   |
+-----------------------------------------------------------------------------------+
```

### Worked Example: TDOA Cross-Bearing Verification
To detect whether an AIS transmission originated from an actual naval combatant or a terrestrial spoofing transmitter, coastal surveillance networks compute the Time Difference of Arrival (**TDOA**) across three synchronized monitoring base stations.

> **Worked example.**
> A suspected warship broadcasts an AIS position report claiming coordinates corresponding to a location $P_{	ext{claim}}$ at sea. Three coastal AIS receivers with precisely synchronized atomic clocks record the exact arrival time of the packet's 24-bit preamble:
> - Receiver $S_1$: Position $(0.0, 0.0)	ext{ km}$; arrival time $t_1 = 0.0000000	ext{ s}$
> - Receiver $S_2$: Position $(0.0, 40.0)	ext{ km}$; arrival time $t_2 = 0.0000452	ext{ s}$
> - Receiver $S_3$: Position $(30.0, 0.0)	ext{ km}$; arrival time $t_3 = 0.0000618	ext{ s}$
>
> 1. Compute measured range differences using the speed of light $c pprox 299,792	ext{ km/s}$:
>    $$\Delta R_{21} = c 	imes (t_2 - t_1) = 299,792 	imes 0.0000452 pprox 13.551	ext{ km}$$
>    $$\Delta R_{31} = c 	imes (t_3 - t_1) = 299,792 	imes 0.0000618 pprox 18.527	ext{ km}$$
>
> 2. The claimed position $P_{	ext{claim}} = (25.0, 20.0)	ext{ km}$ yields true geometric ranges:
>    $$R_1 = \sqrt{25.0^2 + 20.0^2} = \sqrt{625 + 400} = \sqrt{1025} pprox 32.016	ext{ km}$$
>    $$R_2 = \sqrt{25.0^2 + (20.0 - 40.0)^2} = \sqrt{625 + 400} = \sqrt{1025} pprox 32.016	ext{ km}$$
>    $$R_3 = \sqrt{(25.0 - 30.0)^2 + 20.0^2} = \sqrt{25 + 400} = \sqrt{425} pprox 20.616	ext{ km}$$
>
> 3. Expected range differences for the claimed position:
>    $$\Delta R_{21,	ext{claim}} = R_2 - R_1 = 32.016 - 32.016 = 0.000	ext{ km}$$
>    $$\Delta R_{31,	ext{claim}} = R_3 - R_1 = 20.616 - 32.016 = -11.400	ext{ km}$$
>
> 4. Residual comparison:
>    $$|\Delta R_{21,	ext{meas}} - \Delta R_{21,	ext{claim}}| = |13.551 - 0.000| = 13.551	ext{ km}$$
>    Because the range residuals exceed measurement error tolerances ($> 0.05	ext{ km}$), the monitoring station identifies that the signal did **not** originate from the claimed coordinates, flagging the transmission as a spoofed or relocated transmitter.

## Software

The software ecosystem for military and encrypted AIS spans open-source decoding utilities, tactical display packages, and classified naval command engines:

**Open source:**
- **`libais`:** Highly optimized C++ and Python library developed by Kurt Schwehr for decoding ITU-R M.1371 binary sentences. It natively parses Message 25 and Message 26 containers and extracts Designated Area Code (DAC) and Function Identifier (FI) metadata. *Caveat:* Does not include cryptographic decryption modules; ciphertext payloads are presented as raw unparsed bit vectors.
- **`gpsd`:** System daemon for interrogating GNSS and maritime receivers, containing comprehensive `!AIVDM`/`!AIVDO` sentence armoring and unpacking logic. *Caveat:* Lacks specialized military STANAG 4668 payload parsing; drops proprietary encrypted binary extensions.
- **GNU Radio:** Open-source software-defined radio development toolkit with out-of-the-box GMSK demodulation and physical-layer packet extraction blocks. *Caveat:* Requires significant custom DSP programming to execute real-time SOTDMA slot synchronization and multi-channel monitoring.

**Free but closed:**
- **OpenCPN:** Community electronic chart system supporting NMEA 0183/2000 AIS feeds, target tracking, and CPA/TCPA collision calculation. *Caveat:* Contains no native support for military encrypted modes; marks encrypted Message 26 bursts as unhandled binary packets.

**Commercial:**
- **OSI Maritime Systems ECPINS:** Warship Electronic Chart Precise Integrated Navigation System, fully compliant with NATO STANAG 4668 and STANAG 4669. Integrates W-AIS transponders directly with warship radar, sonar, and Combat Management Systems, managing active, silent, and protected modes from the primary conning position. *Caveat:* Highly restricted defense-only product subject to Canadian and international export control regimes.
- **Saab Secure Link Manager:** Specialized proprietary command software integrated with Saab R5/R6 transponders for managing organizational sub-groups, tactical channel frequency assignments, and cryptographic key loading. *Caveat:* Proprietary interface limited strictly to authorized defense and government customers.

## Standards & guides

- **International Maritime Organization (IMO)**: *Resolution A.1106(29)* (2015), "Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems (AIS)." Governs operational rules for AIS, affirming master's authority to switch off transponders when security is threatened.
- **International Maritime Organization (IMO)**: *SOLAS Chapter V, Regulation 19* (2000), "Carriage requirements for shipborne navigational systems and equipment." Establishes the mandatory carriage criteria for commercial vessels and codifies sovereign exemptions under Chapter I, Regulation 3.
- **North Atlantic Treaty Organization (NATO)**: *STANAG 4668* (Edition 2, 2010), "Warship - Automatic Identification System (W-AIS)." Defines the technical architecture, message structures, and cryptographic interfaces for NATO military AIS transponders.
- **North Atlantic Treaty Organization (NATO)**: *STANAG 4669* (Edition 2, 2010), "Automatic Identification System (AIS) on Warships." Defines doctrinal operational procedures, standard tactical modes (Active, Passive, Protected), and situational employment rules for NATO warships.
- **International Telecommunication Union (ITU)**: *Recommendation ITU-R M.1371-5* (2014) / *M.1371-6* (2026), "Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band." Governs physical layer GMSK modulation, SOTDMA timing, and Message 25/26 binary encapsulation.
- **United States Coast Guard (USCG)**: *Encrypted Automatic Identification System (EAIS) Interface Design Description (IDD)* (Version 5.4, 2016). Establishes technical specifications for encrypted maritime law enforcement tracking and STEDS integration under DAC 366.
- **International Electrotechnical Commission (IEC)**: *IEC 61993-2* (Edition 3, 2018), "Maritime navigation and radiocommunication equipment and systems - Automatic Identification Systems (AIS) - Part 2: Class A shipborne equipment of the automatic identification system (AIS) - Operational and performance requirements, methods of test and required test results."
- **United States Government**: *33 CFR § 164.01 & § 164.46*, "Navigation Safety Regulations - Automatic Identification System." Codifies commercial carriage mandates and explicitly affirms the statutory sovereign immunity exemption for warships and state-operated vessels.

## Pitfalls

- **Assuming "AIS dark" means invisible at sea:** Commanding officers assume securing AIS conceals the vessel → Coastal radar, satellite SAR, and optical lookouts detect the physical hull regardless of transponder status → Maintain a rigorous radar and visual lookout under Rule 5 of the COLREGs; never equate silent running with physical invisibility.
- **Operating dark in congested commercial TSS lanes:** Warships operate with AIS secured to protect mission secrecy while navigating crowded choke points → Commercial merchant bridge teams fail to acquire the warship electronically, leading to catastrophic crossing collisions (e.g., USS *Fitzgerald* and USS *John S. McCain*) → Adhere strictly to post-2017 naval surface force directives mandating active AIS broadcast in high-density traffic.
- **Failing to account for TDMA slot consumption of encrypted bursts:** System operators assume encrypted Message 26 packets are invisible to the radio network → Ciphertext bursts broadcast on AIS 1 and AIS 2 fully occupy SOTDMA slots, contributing to channel loading and triggering packet collision if slot reservations fail → Migrate high-rate tactical blue-force tracking to dedicated off-band VHF frequencies.
- **Treating commercial web aggregator feeds as tactical truth:** Naval operations watchstanders utilize commercial internet-based AIS tracking displays to monitor nearby traffic → Commercial aggregator feeds suffer from satellite ingestion delays (up to 30–60 minutes), internet latency, and unverified crowd-sourced spoofing → Always fuse local RF line-of-sight AIS receiver feeds directly into primary radar and ECDIS consoles.
- **Ignoring key expiration across coalition assets:** Multinational naval task groups conduct tactical maneuvers with desynchronized cryptographic key rolls → Units whose keys expire drop out of the tactical tracking plot instantly and appear as unparseable interference → Implement automated key management alerts and verify key integrity during pre-sail communications checks.
- **Transmitting standard static profiles with masked dynamic data:** A warship attempts to conceal its identity by broadcasting an altered vessel name while maintaining a valid naval MMSI or unique IMO number → Commercial tracking databases easily correlate the permanent identifier with historical naval Lloyd's Register records → Ensure static masking scripts address MMSI, call sign, dimensions, and vessel type comprehensively.
- **Neglecting physical-layer RF fingerprinting risks:** A warship randomizes its transmitted MMSI believing it prevents electronic tracking → Sophisticated adversary SIGINT stations correlate the transponder's unique turn-on transient, phase error, and oscillator offset across transmissions → Employ specialized low-probability-of-intercept (LPI) transceivers or transition entirely to passive receive mode when evading state adversaries.
- **Overlooking internal GNSS synchronization failure during jamming:** Hostile or testing GNSS jamming degrades the transponder's internal clock → The W-AIS transponder drifts outside the 26.67 ms SOTDMA slot boundary, colliding with civilian traffic → Ensure transponder firmware automatically reverts to indirect terrestrial base station synchronization or ITDMA mode upon loss of GNSS timing.

## Key takeaways

- **Sovereign Immunity:** Warships and state-operated non-commercial vessels are exempt from mandatory SOLAS AIS carriage and national regulations under SOLAS Chapter I, Regulation 3, and 33 CFR § 164.01(c).
- **The Core Conflict:** Unencrypted AIS broadcasts present a severe operational security hazard by disclosing real-time warship positions, yet operating completely silent drastically increases collision risks in congested commercial waterways.
- **NATO Standardization:** NATO STANAG 4668 defines the technical parameters for Warship AIS (W-AIS) transponders, while STANAG 4669 codifies operational employment across Active, Passive, Protected, and Masked modes.
- **Cryptographic Containers:** Encrypted military and law enforcement AIS packets are encapsulated within standard ITU-R M.1371 Message 25 and Message 26 containers using symmetric block ciphers (AES-128, AES-256, or Blowfish) under Designated Area Codes such as DAC 366.
- **Spectrum Physics & Coexistence:** Encrypted Message 26 bursts on public channels (AIS 1 and AIS 2) preserve unencrypted SOTDMA communication state tails, allowing civilian transponders to mark slots as occupied without being able to read the ciphertext.
- **Dedicated Tactical Channels:** Modern transponders, such as the Saab R6 Supreme Secure, utilize dedicated off-band VHF frequencies (third-channel operation) to eliminate RF slot contention with commercial shipping.
- **Doctrinal Transformation:** The fatal 2017 collisions of the USS *Fitzgerald* and USS *John S. McCain* compelled the United States Navy to reverse decades of "default dark" operations, mandating active AIS broadcasts in congested waters.
- **Multi-Sensor Fusion:** Military maritime situational awareness requires fusing line-of-sight AIS telemetry with primary radar, ESM, satellite SAR, and kinematic plausibility filters to defeat intentional spoofing and deception.

## References

- Balduzzi, M., Pasta, A., Wilhoit, K. (2014). A Security Evaluation of AIS Automated Identification System. In *Proceedings of the 30th Annual Computer Security Applications Conference (ACSAC '14)*, pages 436–445. New Orleans, USA: ACM. doi:10.1145/2664243.2664257
- Goudossis, A., Katsikas, S. K. (2019). Towards a secure automatic identification system (AIS). *Journal of Marine Science and Technology*, 24(2):410–423. doi:10.1007/s00773-018-0561-3
- International Electrotechnical Commission (2018). *Maritime navigation and radiocommunication equipment and systems - Automatic Identification Systems (AIS) - Part 2: Class A shipborne equipment of the automatic identification system (AIS) - Operational and performance requirements, methods of test and required test results* (IEC 61993-2:2018). Geneva: IEC.
- International Maritime Organization (2000). *Adoption of Amendments to the International Convention for the Safety of Life at Sea, 1974, as Amended* (Resolution MSC.99(73)). London: IMO.
- International Maritime Organization (2015). *Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems (AIS)* (Resolution A.1106(29)). London: IMO.
- International Telecommunication Union (2014). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band* (Recommendation ITU-R M.1371-5). Geneva: ITU.
- Kessler, G. C., Craiger, J. P., Haass, J. C. (2018). A Taxonomy of Maritime Cybersecurity Vulnerabilities and Mitigations. *TransNav: International Journal on Marine Navigation and Safety of Sea Transportation*, 12(3):429–437. doi:10.12716/1001.12.03.01
- National Transportation Safety Board (2019). *Collision between US Navy Destroyer John S McCain and Tanker Alnic MC, Singapore Strait, August 21, 2017* (Marine Accident Report NTSB/MAR-19/01). Washington, DC: NTSB.
- National Transportation Safety Board (2020). *Collision between US Navy Destroyer Fitzgerald and Philippine-Flagged Container Ship ACX Crystal, Sagami Wan, Japan, June 17, 2017* (Marine Accident Report NTSB/MAR-20/02). Washington, DC: NTSB.
- North Atlantic Treaty Organization (2010). *Warship - Automatic Identification System (W-AIS)* (STANAG 4668, Edition 2). Brussels: NATO Standardization Agency.
- North Atlantic Treaty Organization (2010). *Automatic Identification System (AIS) on Warships* (STANAG 4669, Edition 2). Brussels: NATO Standardization Agency.
- United States Coast Guard (2016). *Encrypted Automatic Identification System (EAIS) Interface Design Description (IDD)* (Version 5.4). Washington, DC: USCG Command, Control, and Communications Engineering Center (C3CEN).
- United States Navy (2017). *Report on the Collision between USS Fitzgerald (DDG 62) and Motor Vessel ACX Crystal and the Collision between USS John S McCain (DDG 56) and Motor Vessel Alnic MC*. Washington, DC: Office of the Chief of Naval Operations.
