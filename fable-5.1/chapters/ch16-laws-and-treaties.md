# Chapter 16 — Laws and treaties

> **Part III — Identity, institutions, law.** How international conventions, regional directives, and national statutes transform an open radio protocol into a compulsory surveillance regime, where the legal mandate to transmit collides with electronic warfare and sovereignty, and why switching off remains the captain's contentious prerogative.

**In this chapter.** You will master the statutory, treaty, and regulatory structures that mandate and govern the Automatic Identification System (**AIS**) across international waters and domestic jurisdictions. You will trace the carriage requirements established in Chapter V of the International Convention for the Safety of Life at Sea (**SOLAS**) and analyze the December 2002 diplomatic acceleration that bound maritime identity to post-9/11 security regimes alongside the International Ship and Port Facility Security (**ISPS**) Code. You will dissect how the International Regulations for Preventing Collisions at Sea (**COLREGs**) treat broadcast telemetry as "available means" rather than an authoritative substitute for radar, and evaluate coastal and flag state jurisdiction under the United Nations Convention on the Law of the Sea (**UNCLOS**). You will examine the United States dual-agency regulatory model spanning the Maritime Transportation Security Act of 2002 (**MTSA**), 33 CFR § 164.46, and Federal Communications Commission (**FCC**) rules under 47 CFR Part 80. You will explore European Union directives mandating Class A on fishing vessels over 15 meters, the Port State Measures Agreement (**PSMA**), and global maritime sanctions enforcement against dark fleets. Finally, you will establish rigorous compliance verification procedures and quantify regulatory telemetry uncertainty in operational data streams.

## 16.1 The international treaty architecture: SOLAS Chapter V

The global legal mandate to install and operate an Automatic Identification System originates in public international maritime law under the International Maritime Organization (**IMO**). While national coast guards enforce equipment installation within domestic harbors, their statutory authority over foreign merchant shipping derives from the International Convention for the Safety of Life at Sea (**SOLAS**), 1974.

The technical foundation for navigational telemetry was established by the Maritime Safety Committee (**MSC**) in Resolution MSC.74(69) Annex 3 on 12 May 1998, defining universal performance standards for shipborne AIS. On 5 December 2000, the IMO adopted Resolution MSC.99(73), revising SOLAS Chapter V (*Safety of Navigation*). Entering into force on 1 July 2002, revised Regulation 19.2.4 established the first binding international carriage mandate for digital tracking transponders on commercial merchant fleets.

### 16.1.1 Mandatory carriage thresholds: SOLAS Regulation V/19.2.4

Under SOLAS Chapter V, Regulation 19.2.4, compulsory carriage is defined strictly by vessel category, voyage profile, and gross tonnage (**GT**):
1. **International voyages:** All ships of 300 gross tonnage and upwards.
2. **Domestic cargo vessels:** Cargo ships of 500 gross tonnage and upwards.
3. **Passenger vessels:** All passenger ships irrespective of size, on international or domestic voyages.

SOLAS relies on volumetric tonnage under the 1969 Tonnage Convention rather than length. Regulation 19.2.4 compels installation of **Class A** transponders meeting Recommendation ITU-R M.1371 and IEC 61993-2. Voluntary carriage of low-power **Class B** units does not satisfy compulsory SOLAS mandates.

Under Regulation 19.2.4.5, fitted systems must automatically broadcast ship identity, type, position, course over ground (**COG**), speed over ground (**SOG**), navigational status, and safety-related information; receive telemetry from similarly fitted ships; monitor and track vessels across the VHF cell; and exchange data with shore traffic facilities. Transponders must operate autonomously and continuously, deriving fixes from an Electronic Position Fixing System (**EPFS**) using WGS-84 datum and interfacing with a certified gyrocompass or Transmitting Heading Device (**THD**).

### 16.1.2 Post-9/11 acceleration and the December 2002 Conference

The original rollout in Resolution MSC.99(73) (2000) extended through 1 July 2008. The 11 September 2001 attacks upended this schedule. At the IMO Diplomatic Conference on Maritime Security (London, 9–13 December 2002), governments adopted SOLAS Chapter XI-2, the mandatory **International Ship and Port Facility Security** (**ISPS**) Code, and Conference Resolution 1 (12 December 2002), accelerating carriage:

$$\text{Deadline} = \min\left(\text{First safety equipment survey after 1 July 2004},\; \text{31 December 2004}\right)$$

Establishing a hard backstop of 31 December 2004 compressed a seven-year transition into twenty-four months, driving a global manufacturing push. New ships constructed on or after 1 July 2002 fitted AIS upon delivery, passenger ships complied by 1 July 2003, and international tankers complied at their first survey on or after 1 July 2003. Domestic non-international cargo vessels retained their 1 July 2008 completion window.

### 16.1.3 The continuous operation mandate and the "switch-off" exception

The operational mandate is codified in SOLAS Chapter V, Regulation 19.2.4.7:

> "AIS shall be operated taking into account the guidelines adopted by the Organization. Ships fitted with AIS shall maintain AIS in operation at all times except where international agreements, rules or standards provide for the protection of navigational information."

The operational scope of the "protection of navigational information" exception is defined in IMO Resolution **A.1106(29)** (*Revised Guidelines for the Onboard Operational Use of Shipborne AIS*), adopted on 2 December 2015, which revoked earlier interim guidance in Resolutions A.917(22) and A.956(23). Paragraph 22 of the Annex to Resolution A.1106(29) establishes the master's legal prerogative:

> "AIS should always be in operation when ships are underway or at anchor. If the master believes that the continual operation of AIS might compromise the safety or security of his/her ship or where security incidents are imminent, the AIS may be switched off. ... Actions of this nature should always be recorded in the ship's logbook together with the reason for doing so. The master should however restart the AIS as soon as the source of danger has disappeared."

In high-risk piracy corridors—such as the Gulf of Aden, Western Indian Ocean, or Gulf of Guinea—broadcasting high-rate dynamic vectors, speed, cargo type, and free-text destination metadata presents a direct tactical vulnerability to armed skiffs monitoring VHF.

> **Definitions that bite.**
>
> **"Maintain in operation at all times" versus "Switch-off prerogative".**
> Under SOLAS Regulation V/19.2.4.7, continuous operation is mandatory. However, under IMO Resolution A.1106(29) paragraph 22, the master holds the explicit unilateral legal authority to switch off the transponder if continual operation compromises safety or security.
>
> The legal line between lawful discretion and a treaty violation turns entirely on procedural reporting:
> 1. **The Logbook Entry:** The exact time, position, and specific operational justification must be entered into the official deck logbook at deactivation.
> 2. **VTS Notification:** If operating within a mandatory ship reporting system or Vessel Traffic Service (**VTS**) area, the master must inform the competent shore authority unless doing so would further compromise ship security.
> 3. **Prompt Restoration:** The transponder must be reactivated immediately once the danger recedes.
>
> In sanctions evasion and illegal fishing litigation, enforcement agencies prosecute the absence of a plausible contemporary security justification documented in the vessel log.

### 16.1.4 Annual survey and testing: SOLAS Regulation V/18.9

Under Resolution MSC.308(88) (in force 1 July 2012), SOLAS Regulation V/18.9 mandates that shipborne AIS undergo an annual performance test conducted by an approved surveyor under **MSC.1/Circ.1252**. The survey verifies physical cabling, antenna separation, uninterruptible power supply (**UPS**) failover (per IMO SN/Circ.227 and SN.1/Circ.245), radio frequency measurements (frequency error within $\pm 500\text{ Hz}$, minimum 12.5 W Class A output, and antenna VSWR), static programming audits (MMSI, IMO number, call sign, dimensions, antenna geodetic offsets), sensor integration (gyro/THD heading, SOG, COG, rate of turn), and an on-air test with a shore station or calibrated test set. The resulting AIS Test Report must be retained on board.

## 16.2 COLREGs and navigational status: "Available means" vs. radar

AIS is a supplementary communication system, not a primary anti-collision sensor under the **International Regulations for Preventing Collisions at Sea 1972** (**COLREGs**). The COLREGs do not mention AIS by name. Its application is governed by Rules 5, 7, and 8.

### 16.2.1 Rule 5: Look-out by "all available means"

Rule 5 establishes the universal duty of look-out:

> "Every vessel shall at all times maintain a proper look-out by sight and hearing as well as by all available means appropriate in the prevailing circumstances and conditions so as to make a full appraisal of the situation and of the risk of collision."

Admiralty courts across the United Kingdom, United States, and Singapore have unanimously interpreted "all available means" to encompass operational AIS displays and Electronic Chart Display and Information Systems (**ECDIS**) overlays. Failing to observe an AIS target bearing down on a vessel—especially in restricted visibility—breaches Rule 5. However, AIS supplements, and never replaces, visual lookouts and radar plotting.

### 16.2.2 Rule 7: Risk of collision and "scanty information"

Rule 7(a) requires using all available means to determine if risk of collision exists. Crucially, Rule 7(c) dictates:

> "Assumptions shall not be made on the basis of scanty information, especially scanty radar information."

In Resolution A.1106(29) paragraphs 40–44, the IMO issued direct warnings regarding Rule 7 and AIS data. Closest Point of Approach (**CPA**) and Time to Closest Point of Approach (**TCPA**) derived from AIS rely on reported SOG and COG, which are subject to GNSS receiver smoothing, latency, and interpolation delays. Furthermore, non-mandated vessels (wooden fishing boats, composite yachts, naval craft) may not broadcast AIS. Altering course or speed under Rule 8 based purely on an AIS vector without systematic Automatic Radar Plotting Aid (**ARPA**) tracking constitutes an assumption made on "scanty information" under Rule 7(c).

### 16.2.3 VHF bridge-to-bridge calling and collision liabilities

AIS broadcasts display vessel names, encouraging bridge watchstanders to call targets on VHF Channel 16 or 13. Accident investigation bodies (such as the UK [**MAIB**] and US [**NTSB**]) have documented numerous disasters caused by "VHF-assisted collisions." Navigators negotiate non-standard passing agreements that contradict steering rules (Rules 14, 15, 16), waste crucial minutes in verbal debate, and fail to take positive helm action. IMO Resolution A.1106(29) paragraph 44 explicitly warns mariners against negotiating collision avoidance maneuvers via VHF based on AIS identity.

## 16.3 UNCLOS, flag states, and coastal state jurisdiction

The global reach of AIS exists within the jurisdictional framework established by the 1982 United Nations Convention on the Law of the Sea (**UNCLOS**).

### 16.3.1 Flag state responsibilities: Article 94

Under UNCLOS Article 94, flag states must effectively exercise jurisdiction and control in administrative, technical, and social matters over ships flying their flag. Specifically, Article 94(3)(a) and 94(4)(c) mandate that flag administrations ensure vessels conform to generally accepted international regulations regarding navigation safety and radio communications. Because SOLAS Chapter V constitutes such a regulation, flag states are legally bound to enforce AIS carriage, survey compliance, and accurate MMSI programming across their registered fleets worldwide.

### 16.3.2 Coastal states and innocent passage: Articles 17, 19, and 21

A coastal state's authority over foreign ships transiting its territorial sea (up to 12 nautical miles) is constrained by **innocent passage** (Articles 17–19). While Article 21(1)(a) permits coastal legislation regarding navigation safety, Article 21(2) dictates that such laws *“shall not apply to the design, construction, manning or equipment of foreign ships unless they are giving effect to generally accepted international rules or standards.”* Coastal states cannot unilaterally require foreign vessels in innocent passage to carry non-standard radio equipment; they can only enforce international standards established under SOLAS Regulation V/19.2.4.

### 16.3.3 Exclusive Economic Zones and high seas freedom

In the Exclusive Economic Zone (**EEZ**, up to 200 nautical miles) and on the high seas, foreign vessels enjoy navigation freedoms preserved under UNCLOS Articles 58 and 87. Coastal state jurisdiction in the EEZ is functional, limited to resource exploration, fisheries, and environmental protection. Coastal states cannot unilaterally demand that passing foreign merchant ships broadcast proprietary data or submit to tracking in the EEZ, outside multilateral frameworks such as Long-Range Identification and Tracking (**LRIT**) under SOLAS Regulation V/19-1 or IMO-adopted mandatory reporting systems under SOLAS Regulation V/11.

## 16.4 United States law and regulation

The United States governs AIS through a synchronized dual-agency model. The **United States Coast Guard** (**USCG**) dictates carriage mandates, operational rules, navigation safety deviations, and harbor traffic monitoring under Title 33 of the Code of Federal Regulations (**33 CFR**). Concurrently, the **Federal Communications Commission** (**FCC**) regulates spectrum, equipment certification, emission masks, and operator licensing under Title 47 of the Code of Federal Regulations (**47 CFR**).

### 16.4.1 Statutory mandate: 46 U.S.C. § 70114 and MTSA 2002

The domestic statutory mandate was enacted as Section 102 of the **Maritime Transportation Security Act of 2002** (**MTSA**, Public Law 107-295), codified at **46 U.S.C. § 70114**. Enacted following 9/11, § 70114 mandates carriage on US navigable waters for self-propelled commercial vessels $\ge 65\text{ ft}$ overall length, passenger vessels carrying more than a Secretary-determined number of passengers for hire, and towing vessels $> 26\text{ ft}$ and $> 600\text{ hp}$. Section 70114(a)(2) authorizes exemptions where AIS is not necessary for safe navigation, and § 70114(b) directs implementing regulations for equipment maintenance and operation.

### 16.4.2 33 CFR § 164.46: Carriage, operation, and pilot plug rules

The Coast Guard implemented 46 U.S.C. § 70114 through **33 CFR § 164.46**, mandating carriage by **1 March 2016** (80 FR 5282). Under § 164.46(b)(1), **Class A** transponders are mandatory for commercial vessels $\ge 65\text{ ft}$, towing vessels $\ge 26\text{ ft}$ and $> 600\text{ hp}$, passenger vessels certificated for $> 150$ passengers, dredges in commercial channels, and vessels carrying Certain Dangerous Cargo (**CDC**) or bulk flammable liquids. Under § 164.46(b)(2), **Class B** transponders are permitted for fishing vessels, dredges outside channels, and commercial vessels $\ge 65\text{ ft}$ carrying $< 150$ passengers operating outside VTS areas at speeds $\le 14\text{ knots}$.

Operational rules under § 164.46(d) mandate continuous operation underway, at anchor, and 15 minutes before getting underway. Silent periods require logging and COTP/VTC notification. Broadcasters must transmit an accurate MMSI (§ 164.46(d)(2)(iii)). Safety text messaging is restricted to English navigation warnings (`SECURITE`). Application-Specific Messages are limited to IMO-adopted applications at most once per minute (§ 164.46(d)(4)). Pilotage vessels must provide a pilot plug adjacent to a dedicated 120 V AC receptacle within 3 feet (§ 164.46(g)). Class A or B broadcasts from aircraft, barges, or land are prohibited (§ 164.46(i)).

> **Legal note.**
>
> **Land-based transmissions and portable AIS equipment in US jurisdiction.**
> Under 33 CFR § 164.46(i) and 47 CFR § 80.231, transmitting with a marine Class A or Class B transponder from shore, a vehicle, or a residence is a federal violation punishable by civil forfeitures and equipment seizure.
>
> 1. **Receive-only stations:** Operating an SDR or AIS receiver on land to capture VDL packets and feed public aggregators (such as MarineTraffic, AISHub, or NOAA) is completely unrestricted.
> 2. **Prohibited land transmissions:** Operating a Class B transponder in an office or on a boat sitting on a highway trailer is prohibited under § 164.46(i).
> 3. **Portable AIS (§ 164.46(f)):** Battery-powered portable AIS units used aboard towing vessels must not generate electromagnetic interference with bridge sensors, and only one transponder may transmit on board simultaneously.

### 16.4.3 FCC Part 80 rules: Type approval and dealer programming

Under 47 CFR Part 80, the FCC controls equipment authorization and licensing. Transponders undergo two-step certification (§§ 80.231, 80.275): Coast Guard review (**CG-ENG-4**) verifies IEC compliance, after which the FCC issues a Grant of Equipment Authorization with an **FCC ID**. Certified units display an FCC ID and a USCG Type Approval number.

Under 47 CFR § 80.231(b), entry of static data into Class B devices by end users is strictly prohibited; programming must be performed by an authorized marine electronics dealer or technician, and devices carry a mandatory warning label. Reprogramming requires dealer service under RTCM Standard 10160.0. Domestic recreational vessels are licensed by rule under § 80.13 with agent-issued MMSIs; compulsory vessels or vessels on international voyages must hold an individual FCC Ship Station License via the Universal Licensing System (**ULS**), synchronized with ITU MARS.

### 16.4.4 Enforcement against non-certified AIS fishing net buoys

In the late 2010s, coastal VHF channels were flooded by unauthorized drifting "AIS fishing net buoys" transmitting continuous Class A Message 1 or pseudo-Message 21 bursts on 161.975 MHz and 162.025 MHz with bogus MMSIs (`888888888`, `123456789`). Lacking SOTDMA reservations or polite CSTDMA sensing, they caused packet collisions and cluttered radar displays with phantom targets.

On 28 November 2018, the FCC Enforcement Bureau issued an Enforcement Advisory confirming that marketing, sale, or use of non-certified net buoys violates 47 U.S.C. § 301 and 47 CFR Part 80. AIS frequencies are restricted to certified transponders, AIS-SARTs, and Maritime Survivor Locating Devices. Gear marking buoys must operate on allocated frequencies (e.g., 1900–2000 kHz). Under 47 U.S.C. § 503, statutory civil forfeitures exceed $19,000 per violation day, up to $147,000 for continuing violations. Section 8416 of the FY2021 NDAA (Public Law 116-283) directed the FCC to initiate rulemaking on authorized gear-marking devices, leading to **WT Docket No. 21-230** in June 2021 to consider alternative frequencies such as 160.900 MHz.

## 16.5 European Union and regional legal frameworks

The European Union extends tracking requirements significantly beyond SOLAS baselines.

### 16.5.1 Directive 2002/59/EC and the VTMIS architecture

Enacted 27 June 2002 following the *Erika* (1999) and *Prestige* (2002) spills, **Directive 2002/59/EC** established the Community **Vessel Traffic Monitoring and Information System** (**VTMIS**) and created **SafeSeaNet**, managed by the European Maritime Safety Agency (**EMSA**). Article 9 mandated coastal shore-based AIS monitoring infrastructure across all Member States.

### 16.5.2 Directives 2009/17/EC and 2011/15/EU: Lowering thresholds and Annex II

Under Directive 2009/17/EC and Commission Directive **2011/15/EU** (Annex II), the EU lowered the domestic non-international cargo carriage threshold from SOLAS's 500 GT down to **300 gross tonnage**. Passenger ships are mandated irrespective of size. Member States may exempt passenger ships $< 15	ext{ m}$ or $< 300	ext{ GT}$ on domestic routes, and cargo ships 300–500 GT operating exclusively in sheltered internal waters.

### 16.5.3 Fishing vessel AIS mandates: Article 6a and Regulation 1224/2009

Fishing vessels are exempt under SOLAS Chapter V. However, under **Article 6a** of Directive 2002/59/EC (inserted by Directive 2009/17/EC):

> "Any fishing vessel with an overall length of more than 15 metres and flying the flag of a Member State and registered in the Community, or operating in the internal waters or territorial sea of a Member State, or landing its catch in the port of a Member State shall, in accordance with the timetable set out in Annex II, part I(3), be fitted with an AIS (Class A) which meets the performance standards drawn up by the IMO."

Phased compliance dates in Annex II Part I(3):
- $\ge 24\text{ m}$ to $< 45\text{ m}$ LOA: **31 May 2012**.
- $\ge 18\text{ m}$ to $< 24\text{ m}$ LOA: **31 May 2013**.
- $> 15\text{ m}$ to $< 18\text{ m}$ LOA: **31 May 2014**.
- New-built vessels $> 15\text{ m}$: **30 November 2010**.

Article 6a mandates continuous broadcast: *"Fishing vessels equipped with AIS shall maintain it in operation at all times,"* permitting deactivation only in exceptional safety/security circumstances. Under **Council Regulation (EC) No 1224/2009** (the *Control Regulation*), Article 10(3) authorizes fisheries control authorities to cross-check AIS against satellite **Vessel Monitoring System** (**VMS**) feeds and electronic logbooks. The revised Control Regulation (**Regulation (EU) 2023/2842**, applicable from 10 January 2026) maintained continuous AIS broadcast while extending tracking across small-scale vessels under 12 meters.

### 16.5.4 Inland AIS: River Information Services and Regulation 2019/838

Under River Information Services (**RIS**) Directive 2005/44/EC, the Central Commission for the Navigation of the Rhine (**CCNR**) and the European Commission standardized **Inland AIS** under Commission Implementing Regulation **(EU) 2019/838** (repealing Regulation (EC) No 415/2007) and CESNI **ES-TRIN**. Inland AIS broadcasts European Vessel Identification Numbers (**ENIs**), convoy dimensions, draft adjustments, and hazardous cargo blue-cone indicators. Carriage is mandatory on the Rhine and Danube under regional police rules (*Rheinpolizeiverordnung*).

## 16.6 Specialized treaties and international security regimes

Beyond SOLAS and regional traffic directives, AIS intersects with port access, marine environmental protection, and United Nations sanctions.

### 16.6.1 FAO Port State Measures Agreement (PSMA)

Concluded under the UN FAO, the 2009 Agreement on Port State Measures to Prevent, Deter and Eliminate Illegal, Unreported and Unregulated Fishing (**PSMA**, in force 5 June 2016) combatting IUU fishing verifies vessel identity prior to port entry. Under Annex A, foreign fishing vessels must submit advance port entry requests with vessel name, flag, external markings, call sign, IMO number, and VMS verification. Authorities cross-reference transmitted AIS tracks and transshipment encounters against Annex A declarations; unexplained gaps provide statutory grounds under Article 9 to deny port entry or seize illegal catch.

### 16.6.2 MARPOL and emissions monitoring

Under MARPOL Annex VI, sulfur ($\text{SO}_x$), nitrogen ($\text{NO}_x$), and carbon intensity rules (**CII**) rely on reported fuel consumption (**IMO DCS**). However, AIS has become the primary independent regulatory science tool for tracking emissions. The **Fourth IMO GHG Study 2020** (MEPC 75/7/15) used a bottom-up, voyage-based activity model ingesting global terrestrial and satellite AIS archives to calculate engine loads, speeds, and greenhouse gas emissions across trade routes from 2012 to 2018.

### 16.6.3 Sanctions enforcement: OFAC and UN Security Council regimes

Under **UNSCR 2397** (adopted 22 December 2017) and related North Korea resolutions, the UN Security Council capped refined petroleum imports to the DPRK, banned mineral exports, and prohibited ship-to-ship (**STS**) transfers of illicit cargo. The UN Panel of Experts established pursuant to Resolution 1874 (2009) documented sophisticated AIS evasion tactics in its reports (such as S/2019/171), including dark voyages, identity laundering, and GNSS spoofing during covert STS transfers.

On 14 May 2020, OFAC, the US Department of State, and the USCG issued the *“Sanctions Advisory for the Maritime Industry, Energy and Metals Sectors, and Related Communities.”* The advisory identified **AIS manipulation and disabling** as a leading deceptive shipping practice, establishing compliance expectations for ship owners, charterers, insurers (P&I clubs), and traders:
- Continuous monitoring of AIS tracks for unexplained transmission gaps.
- Inclusion of charter-party clauses authorizing contract termination if a vessel tampers with AIS without documented safety justification.
- Verification of historical AIS tracks prior to financing or bunkering operations.

Following the expiration of the UN Panel mandate in April 2024, eleven partner nations established the **Multilateral Sanctions Monitoring Team** (**MSMT**) in October 2024 to track sanctions evasion using fused AIS analytics.

## Then & now

How the statutory, operational, and telecommunications rules governing AIS transformed from an open safety broadcast into an instrument of international regulatory surveillance:

- **1990** ⟨+⟩: The United States enacts OPA-90 (Public Law 101-380), mandating in § 5004 vessel tracking and route deviation alarms in Prince William Sound following the *Exxon Valdez* spill.
- **1998** ⟨H⟩: The IMO adopts Resolution MSC.74(69) Annex 3 on 12 May 1998, establishing universal performance standards for AIS as an open, unauthenticated radio protocol.
- **2000** ⟨H⟩: IMO Resolution MSC.99(73) concludes the revision of SOLAS Chapter V on 5 December 2000, creating the first carriage mandate under Regulation 19.2.4.
- **2002** ⟨+⟩: The EU enacts Directive 2002/59/EC on 27 June 2002, establishing SafeSeaNet and mandating coastal shore-based AIS networks.
- **2002** ⟨H⟩: Following 9/11, the IMO Diplomatic Conference adopts the ISPS Code and Conference Resolution 1 on 12 December 2002, accelerating the SOLAS carriage deadline for international cargo ships to 31 December 2004.
- **2002** ⟨+⟩: The US enacts the Maritime Transportation Security Act of 2002 (MTSA, Public Law 107-295), creating 46 U.S.C. § 70114 and mandating domestic carriage for commercial vessels $\ge 65\text{ ft}$.
- **2003** ⟨+⟩: The USCG publishes an interim carriage rule (68 FR 39353) restricting initial domestic compliance to SOLAS vessels and VTS areas.
- **2006** ⟨+⟩: The IMO adopts Resolution MSC.202(81), adding SOLAS Regulation V/19-1 (LRIT) to establish confidential long-range tracking.
- **2009** ⟨+⟩: The EU enacts Directive 2009/17/EC and Council Regulation (EC) No 1224/2009, mandating Class A AIS on commercial fishing vessels exceeding 15 meters overall length.
- **2010** ⟨+⟩: IMO Resolution MSC.308(88) amends SOLAS to introduce Regulation V/18.9, mandating annual performance testing of shipborne AIS under MSC.1/Circ.1252.
- **2015** ⟨+⟩: The USCG issues its final AIS expansion rule (80 FR 5282, 33 CFR § 164.46), requiring transponders on commercial vessels $\ge 65\text{ ft}$ across all US navigable waters by 1 March 2016.
- **2015** ⟨H⟩: The IMO adopts Resolution A.1106(29), updating operational guidelines and clarifying the master's authority to switch off AIS for vessel security.
- **2018** ⟨+⟩: The FCC Enforcement Bureau issues an advisory prohibiting uncertified "AIS fishing net buoys" on maritime frequencies under 47 CFR Part 80.
- **2020** ⟨+⟩: OFAC, the US Department of State, and USCG issue the Global Maritime Sanctions Advisory, classifying AIS manipulation as a deceptive shipping practice.
- **2021** ⟨+⟩: China enacts data security and personal information laws, causing domestic providers to halt terrestrial feeds to commercial aggregators and reducing visible coastal telemetry by 90%.
- **2024** ⟨+⟩: Following the expiration of the UN DPRK Panel mandate, eleven nations establish the Multilateral Sanctions Monitoring Team (MSMT) to track maritime sanctions evasion.
- **2026** ⟨+⟩: Main operational provisions of EU Regulation 2023/2842 take effect, extending tracking across small-scale fishing vessels while enforcing continuous AIS broadcast rules.

## Validation, uncertainty & data quality

In regulatory compliance, enforcement litigation, and maritime casualty reconstruction, raw AIS telemetry cannot be accepted at face value. Data analysts and investigators must isolate collection artifacts from statutory violations.

### 16.5.1 The three primary error mechanisms

1. **Sensor Misalignment and Configuration Failures:** Transponders broadcast static data programmed into non-volatile memory during installation. If an installer transposes digits in the MMSI or IMO number, enters the GPS antenna offset incorrectly, or fails to interface the ship's gyrocompass, the transponder continuously broadcasts invalid compliance data across its operational life.
2. **Channel Congestion and Terrestrial Packet Loss:** The VHF data link operates at 9,600 bit/s, partitioned into 2,250 time slots per minute per channel ($4,500\text{ slots/min}$ total). In congested waterways (Dover Strait, Singapore Strait, lower Mississippi River), SOTDMA slot contention and Class B CSTDMA starvation frequently cause packet loss rates exceeding 30% to 50%. Coastal receivers may experience reception dropouts of 10 to 30 minutes without the vessel deactivating its transmitter.
3. **Satellite Latency and Co-Channel Collisions:** Low Earth Orbit (**LEO**) satellites capture messages from thousands of vessels simultaneously within footprints exceeding 5,000 km in diameter. Mutual packet collisions destroy bursts, creating artificial gaps in historical satellite archives that can be misconstrued as intentional "AIS dark" events.

### 16.5.2 Quantitative triage: Separating true switch-offs from receiver dropouts

When auditing an alleged statutory switch-off violation under 33 CFR § 164.46(d) or EU Directive 2002/59/EC Article 6a, analysts calculate the **Reception Probability** $P(\text{gap})$ across observed time window $\Delta t$:

$$P(\text{gap}) = (1 - p_{\text{rx}})^{\frac{\Delta t}{T_{\text{rep}}}}$$

where $p_{\text{rx}}$ is the empirical single-packet detection probability of the receiving sensor network in that geodetic cell, and $T_{\text{rep}}$ is the statutory Class A reporting interval (e.g., $10\text{ seconds}$ at $12\text{ knots}$). If $p_{\text{rx}} \approx 0.60$ and a gap of $\Delta t = 600\text{ seconds}$ occurs (60 expected reporting intervals):

$$P(\text{gap}) = (1 - 0.60)^{60} = (0.40)^{60} \approx 1.33 \times 10^{-24}$$

This small probability mathematically refutes random packet loss, proving that the transmitter was deactivated, shadowed by severe topography, or jammed.

> **Try it.**
>
> You can audit maritime telemetry for statutory compliance and kinematic anomalies using the codebase's built-in triage suite:
>
> ```bash
> . /usr/local/google/home/schwehr/sdd-books/ais/fable/.venv/bin/activate
> python code/security/kinematic_checks.py data/samples/synthetic_harbor.nmea --rx 42.36 -70.95
> ```
>
> Expected command output:
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
>
> Notice how the verification pipeline isolates non-compliant transmissions: MMSI `0` and MMSI `1193046` (a factory test pattern) are flagged with `invalid_mmsi = 1`, failing 33 CFR § 164.46(d)(2)(iii).

> **Worked example.**
>
> **Verifying an IMO Ship Identification Number Check Digit.**
> Under SOLAS Chapter XI-1 Regulation 3 and 33 CFR § 164.46(a), commercial vessels must broadcast an authentic seven-digit IMO number in Message 5. The seventh digit ($D_7$) is an integrity check digit derived from digits $D_1$ through $D_6$ using descending scalar multiplier weights:
>
> $$\text{Check Digit } D_7 = \left(\sum_{i=1}^{6} D_i \times (8 - i)\right) \pmod{10}$$
>
> Consider a vessel broadcasting reported IMO number `9241061`:
>
> | Position $i$ | Digit $D_i$ | Weight $(8 - i)$ | Product $D_i \times (8 - i)$ |
> |:---:|:---:|:---:|:---:|
> | 1 | 9 | 7 | $9 \times 7 = 63$ |
> | 2 | 2 | 6 | $2 \times 6 = 12$ |
> | 3 | 4 | 5 | $4 \times 5 = 20$ |
> | 4 | 1 | 4 | $1 \times 4 = 4$ |
> | 5 | 0 | 3 | $0 \times 3 = 0$ |
> | 6 | 6 | 2 | $6 \times 2 = 12$ |
>
> Summing the products:
>
> $$\text{Sum} = 63 + 12 + 20 + 4 + 0 + 12 = 111$$
>
> Calculating the modulo-10 remainder:
>
> $$111 \pmod{10} = 1$$
>
> The calculated check digit ($1$) matches reported seventh digit ($D_7 = 1$). If the broadcaster transmitted `9241065`, the checksum failure would immediately establish a data integrity violation.

## Software

The software tools utilized to verify statutory compliance, process official regulatory feeds, and audit historical tracks:

- **Open source:**
  - `libais` (C++ with Python bindings): Reference parsing library for decoding raw AIVDM/AIVDO NMEA sentences into structured JSON, supporting standard Messages 1–27 and international ASMs. Caveat: strict conformance parsing causes it to drop truncated sentences emitted by certain legacy transponders.
  - `pyais` (Python): Pure-Python decoder supporting extensive sentence reassembly, TAG block parsing, and bitfield extraction. Caveat: higher decoding latency compared to compiled C++ libraries when processing multi-gigabyte streams.
  - `OpenCPN` (C++): Open-source chartplotter supporting AIS target visualization, CPA/TCPA collision alarms, and pilot plug input. Caveat: does not validate cryptographic authenticity of received targets, rendering it susceptible to displayed ghost targets.
- **Free but closed:**
  - NOAA / BOEM `Marine Cadastre AccessAIS`: Web platform providing public access to filtered historical United States NAIS data. Caveat: records are downsampled to one-minute intervals and scrubbed of specific sensitive vessel categories.
  - USCG NAVCEN Historical Data Request (**HDR**) portal: Direct online mechanism allowing researchers to request targeted raw NAIS archives. Caveat: substantial administrative review required before data release.
- **Commercial:**
  - S&P Global Maritime `Sea-web`: Definitive shipping registry linking broadcast MMSIs, call signs, and names to permanent IMO numbers and registered owners. Caveat: high recurring subscription cost and strict contractual redistribution limits.
  - GateHouse Maritime `AIS Hub`: Enterprise maritime surveillance engine used by coastal states to manage shore networks and detect regulatory deviations. Caveat: proprietary closed-source architecture licensed exclusively to sovereign agencies and port authorities.

## Standards & guides

The official conventions, statutory rules, and administrative standards governing AIS carriage, operation, and type approval:

- **International Maritime Organization**, *International Convention for the Safety of Life at Sea (SOLAS)*, 1974, Chapter V, Regulation 19 (amended by Res. MSC.99(73) and 2002 Conference Res. 1). Governs international carriage thresholds and continuous operation.
- **International Maritime Organization**, Resolution MSC.74(69), Annex 3 (1998). Universal performance standards for shipborne AIS.
- **International Maritime Organization**, Resolution A.1106(29) (2015). Operational use guidelines, switch-off authority, and collision avoidance limitations; revokes A.917(22) and A.956(23).
- **International Maritime Organization**, Resolution MSC.308(88) (2010). Mandates annual testing of shipborne AIS under SOLAS Regulation V/18.9.
- **International Maritime Organization**, Circular MSC.1/Circ.1252 (2007). Annual AIS testing guidelines and model test report.
- **United Nations**, *Convention on the Law of the Sea (UNCLOS)*, 1982 (Articles 17, 19, 21, 58, 87, 94). Governs flag state duties and innocent passage limits.
- **International Maritime Organization**, *International Regulations for Preventing Collisions at Sea (COLREGs)*, 1972 (Rules 5, 7, 8). Look-out and risk of collision standards.
- **United States Congress**, *Maritime Transportation Security Act of 2002 (MTSA)* (46 U.S.C. § 70114). Domestic carriage mandate.
- **United States Coast Guard**, 33 CFR § 164.46. Domestic carriage rules, operating standards, and pilot plug requirements.
- **United States Federal Communications Commission**, 47 CFR Part 80 (§§ 80.13, 80.231, 80.275). Station licensing, equipment certification, and Class B static data programming.
- **European Parliament and Council**, Directive 2002/59/EC (amended by 2009/17/EC and 2011/15/EU). Establishes SafeSeaNet, 300 GT domestic threshold, and >15 m fishing vessel AIS mandate.
- **European Council**, Regulation (EC) No 1224/2009 (amended by Reg. (EU) 2023/2842). Fisheries Control Regulation and AIS cross-checking.

## Pitfalls

The operational mistakes, legal misunderstandings, and data interpretation traps encountered in maritime law and AIS regulation:

- **Assuming SOLAS governs all domestic commercial craft** $	o$ Assuming small harbor tugs or passenger boats must meet SOLAS Chapter V $	o$ SOLAS applies strictly to international voyages and domestic vessels $\ge 500	ext{ GT}$; domestic commercial carriage is governed exclusively by national legislation such as 33 CFR § 164.46.
- **Treating an AIS gap as a per se criminal violation** $	o$ Initiating enforcement solely because a vessel ceased broadcasting for twelve hours $	o$ Under SOLAS Regulation V/19.2.4.7 and IMO Resolution A.1106(29) §22, the master possesses unilateral authority to deactivate AIS for vessel safety or security, provided it is contemporaneously recorded in the official deck logbook.
- **Relying on AIS CPA for COLREGs collision avoidance** $	o$ Altering course based strictly on an AIS vector without radar plotting $	o$ Violates COLREGs Rule 7(c); AIS target data is subject to sensor smoothing delays and gyro offsets, constituting "scanty information" in collision liability litigation.
- **Permitting vessel crews to reprogram Class B static data** $	o$ Giving configuration software to vessel owners to edit names or MMSIs $	o$ Violates 47 CFR § 80.231(b), which strictly restricts Class B static data programming to authorized marine electronics dealers and qualified technicians.
- **Operating marine transponders on land** $	o$ Powering a Class A or B transponder in an office or on a trailer $	o$ Violates 33 CFR § 164.46(i) and 47 CFR Part 80; transmitting maritime bursts from land without an FCC coast station authorization is illegal and risks severe forfeitures.
- **Confusing IMO ship identification numbers with MMSIs** $	o$ Tracking a hull across years using its MMSI as an immutable primary key $	o$ Ships frequently change flags and surrender their MMSI, whereas the seven-digit IMO number remains permanently welded to the hull under SOLAS Regulation XI-1/3.
- **Deploying uncertified AIS fishing net buoys** $	o$ Using low-cost VHF net markers transmitting pseudo-Message 1 or 21 bursts $	o$ Violates FCC Part 80 rules and ITU Radio Regulations; non-certified beacons pollute the VHF data link and expose operators to statutory forfeitures exceeding $19,000 per day.
- **Omitting the pilot plug electrical receptacle** $	o$ Installing an AIS pilot plug without an adjacent 120 V AC outlet $	o$ Violates 33 CFR § 164.46(g), which mandates a permanently affixed NEMA 5-15 power receptacle within 3 feet of the plug.
- **Assuming EU fishing vessel rules apply worldwide** $	o$ Expecting commercial fishing boats in US waters to carry Class A transponders $	o$ Fishing vessels are exempt under SOLAS; mandatory Class A carriage on fishing vessels $> 15	ext{ m}$ is unique to the European Union under Directive 2002/59/EC Article 6a.
- **Misinterpreting coastal jurisdiction over innocent passage** $	o$ Expecting a coastal state to detain a foreign ship in innocent passage for lacking domestic telemetry $	o$ Under UNCLOS Article 21(2), coastal states cannot impose domestic equipment rules on foreign ships in innocent passage beyond generally accepted international standards.

## Key takeaways

- **SOLAS Chapter V anchors global carriage:** Regulation 19.2.4 mandates Class A AIS on all ships $\ge 300\text{ GT}$ on international voyages, domestic cargo ships $\ge 500\text{ GT}$, and all passenger ships irrespective of size.
- **The post-9/11 acceleration transformed deployment:** Conference Resolution 1 of December 2002 pulled the international carriage deadline for cargo ships forward to 31 December 2004, compressing an eight-year phase-in into twenty-four months alongside the ISPS Code.
- **The master retains switch-off authority:** Under IMO Resolution A.1106(29) §22, the master may deactivate AIS if continuous broadcast compromises ship safety or security; lawful exercise requires a contemporaneous logbook entry and notification to coastal authorities.
- **AIS is an aid, not an anti-collision radar:** COLREGs Rules 5 and 7 designate AIS as "available means"; maneuvering solely on AIS-derived CPA vectors without radar verification violates Rule 7(c) prohibiting assumptions based on scanty information.
- **UNCLOS balances flag and coastal authority:** Coastal states cannot impose unilateral equipment rules on foreign vessels exercising innocent passage in the territorial sea beyond generally accepted international rules (UNCLOS Article 21(2)).
- **United States law expands carriage via MTSA:** Codified at 46 U.S.C. § 70114 and 33 CFR § 164.46, US law enforces carriage on commercial vessels $\ge 65\text{ ft}$ and towing vessels $> 26\text{ ft}$ and $> 600\text{ hp}$, permitting Class B only under specific speed and waterway restrictions.
- **US Class B equipment is locked to installers:** Under 47 CFR § 80.231(b), static data entry into Class B devices by end users is illegal; programming must be performed by authorized dealers.
- **The EU extends mandates to fisheries:** Directive 2002/59/EC (Article 6a) and Regulation (EC) No 1224/2009 mandate Class A AIS on all commercial fishing vessels exceeding 15 meters overall length.
- **Deceptive AIS manipulation triggers sanctions liability:** Disabling or spoofing AIS to obscure illicit oil transfers or trade violates UNSCR 2397 and represents a major red flag under the OFAC May 2020 Maritime Advisory.

## References

- European Commission (2002). Directive 2002/59/EC of 27 June 2002 establishing a Community vessel traffic monitoring and information system. *Official Journal of the European Communities*, L 208:10–27.
- European Commission (2009). Directive 2009/17/EC of 23 April 2009 amending Directive 2002/59/EC establishing a Community vessel traffic monitoring and information system. *Official Journal of the European Union*, L 131:101–113.
- European Commission (2009). Council Regulation (EC) No 1224/2009 of 20 November 2009 establishing a Community control system for the common fisheries policy. *Official Journal of the European Union*, L 343:1–50.
- European Commission (2011). Commission Directive 2011/15/EU of 23 February 2011 amending Directive 2002/59/EC on vessel traffic monitoring. *Official Journal of the European Union*, L 49:33–36.
- European Commission (2019). Commission Implementing Regulation (EU) 2019/838 of 20 February 2019 on vessel tracking and tracing systems (Inland AIS). *Official Journal of the European Union*, L 138:31–69.
- European Commission (2023). Regulation (EU) 2023/2842 of 20 December 2023 amending Council Regulation (EC) No 1224/2009. *Official Journal of the European Union*, L 2023/2842:1–123.
- Food and Agriculture Organization (2009). *Agreement on Port State Measures to Prevent, Deter and Eliminate Illegal, Unreported and Unregulated Fishing*. Rome: FAO.
- International Maritime Organization (1972). *Convention on the International Regulations for Preventing Collisions at Sea, 1972 (COLREGs)*. London: IMO.
- International Maritime Organization (1974). *International Convention for the Safety of Life at Sea, 1974 (SOLAS)*. London: IMO.
- International Maritime Organization (1998). *Recommendation on Performance Standards for an Universal Shipborne Automatic Identification System (AIS)*. Resolution MSC.74(69), Annex 3. London: IMO.
- International Maritime Organization (2000). *Amendments to SOLAS 1974 (Revised Chapter V)*. Resolution MSC.99(73). London: IMO.
- International Maritime Organization (2002). *Adoption of Amendments to SOLAS 1974 (Accelerated AIS Carriage)*. Conference Resolution 1. London: IMO.
- International Maritime Organization (2003). *Guidelines for the Installation of a Shipborne Automatic Identification System (AIS)*. Circular SN/Circ.227. London: IMO.
- International Maritime Organization (2004). *Amendments to Guidelines for Installation of Shipborne AIS*. Circular SN.1/Circ.245. London: IMO.
- International Maritime Organization (2006). *Adoption of Amendments to SOLAS 1974 (LRIT Regulation V/19-1)*. Resolution MSC.202(81). London: IMO.
- International Maritime Organization (2007). *Guidelines on Annual Testing of the Automatic Identification System (AIS)*. Circular MSC.1/Circ.1252. London: IMO.
- International Maritime Organization (2010). *Guidance on the Use of AIS Application-Specific Messages*. Circular SN.1/Circ.289. London: IMO.
- International Maritime Organization (2010). *Amendments to SOLAS 1974 (Regulation V/18.9 Annual Testing)*. Resolution MSC.308(88). London: IMO.
- International Maritime Organization (2014). *Policy on Use of AIS Aids to Navigation*. Circular MSC.1/Circ.1473. London: IMO.
- International Maritime Organization (2015). *Revised Guidelines for the Onboard Operational Use of Shipborne AIS*. Resolution A.1106(29). London: IMO.
- International Maritime Organization (2020). *Fourth IMO Greenhouse Gas Study 2020*. Document MEPC 75/7/15. London: IMO.
- International Telecommunication Union (2014). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band*. Recommendation ITU-R M.1371-5. Geneva: ITU.
- United Nations (1982). *United Nations Convention on the Law of the Sea (UNCLOS)*. Treaty Series, 1833:3. New York: United Nations.
- United Nations Security Council (2017). *Resolution 2397 (2017)*. Document S/RES/2397(2017). New York: United Nations.
- United Nations Security Council (2019). *Report of the Panel of Experts Established Pursuant to Resolution 1874 (2009)*. Document S/2019/171. New York: United Nations.
- United States Congress (1990). *Oil Pollution Act of 1990*. Public Law 101-380, 104 Stat. 484. Washington, DC: Government Publishing Office.
- United States Congress (2002). *Maritime Transportation Security Act of 2002*. Public Law 107-295, 116 Stat. 2064. Washington, DC: Government Publishing Office.
- United States Congress (2021). *National Defense Authorization Act for Fiscal Year 2021*. Public Law 116-283, 134 Stat. 3388. Washington, DC: Government Publishing Office.
- United States Coast Guard (2015). Vessel Requirements for Notices of Arrival and Departure, and Automatic Identification System. *Federal Register*, 80(20):5282–5335.
- United States Coast Guard (2024). *Title 33, Section 164.46 — Automatic Identification System*. Code of Federal Regulations. Washington, DC: Government Publishing Office.
- United States Department of the Treasury, Department of State, and Coast Guard (2020). *Sanctions Advisory for the Maritime Industry, Energy and Metals Sectors, and Related Communities*. Washington, DC: US Government.
- United States Federal Communications Commission (2018). *FCC Enforcement Advisory: Marketing, Sale, and Use of Noncompliant Fishing Net Buoys is Illegal*. Enforcement Advisory No. DA 18-1210. Washington, DC: FCC.
- United States Federal Communications Commission (2024). *Title 47, Part 80 — Stations in the Maritime Services*. Code of Federal Regulations. Washington, DC: Government Publishing Office.
