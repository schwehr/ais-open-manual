# Chapter 17 — Legal issues and court cases around AIS

> **Part III — Identity, institutions, law.** How open navigational telemetry transforms into decisive judicial evidence, where unencrypted radio broadcasts collide with intellectual property battles, collision liabilities, criminal sanctions, data scraping doctrines, and administrative transparency.

**In this chapter.** You will master the legal precedents, evidentiary standards, and judicial doctrines governing the Automatic Identification System (**AIS**) across admiralty, intellectual property, criminal, and regulatory proceedings. You will analyze patent conflicts surrounding Self-Organizing Time Division Multiple Access (**STDMA**) and Carrier-Sense TDMA (**CSTDMA**), examining Håkan Lans's litigation pitfalls and subsequent licensing disputes. You will dissect landmark collision litigation—including *Ever Smart v. Alexandra 1*, the *Cosco Busan* allision, the *Sanchi* disaster, and the *Dali* bridge strike—evaluating how AIS and Voyage Data Recorder (**VDR**) records settle liability under the International Regulations for Preventing Collisions at Sea 1972 (**COLREGs**). You will inspect the forensic integrity of tracking records in the *Sewol* disaster and examine how prosecutors leverage dark-voyage telemetry to seize vessels in sanctions and illegal fishing cases. Finally, you will establish chain-of-custody protocols for digital maritime evidence and navigate terms of service, Freedom of Information Act (**FOIA**) disclosure, and data privacy frameworks.

## 17.1 Intellectual property litigation: STDMA and the Class B conflicts

The technological architecture of AIS was shaped directly by patent law and intellectual property declarations before international standards bodies. Because the protocol relies on autonomous slot reservation across a coordinated radio frame, its adoption required navigating aggressive patent assertions, reexamination proceedings, and corporate licensing strategies.

### 17.1.1 The Lans STDMA patent family and standard-setting declarations

The foundational technique underlying Class A transponders—Self-Organizing Time Division Multiple Access (**SOTDMA**)—was invented by Swedish inventor Håkan Lans and assigned to GP&C Systems International AB. Lans filed Swedish priority applications SE 9102034 on 1 July 1991 and SE 9103542 on 28 November 1991, followed by international application PCT/SE92/00485 on 29 June 1992 (WO 93/01576). The United States counterpart was granted on 9 April 1996 as US Patent 5,506,587 (Lans 1996stdma), titled "Position indicating system," and the European counterpart issued as EP 0 592 560 B1 on 27 August 1997.

Claim 1 of US 5,506,587 claimed a system of movable stations establishing a position via GNSS with:

> "...a time base common to all of said movable stations... defining time blocks which are standardized, enumerable and form a common, accurate, repeating maximal frame of known length, and means for occupying a free time block in each maximal frame and for autonomously transmitting therein of a position signal in the common radio channel."

This defined the slot map formalized in Recommendation ITU-R M.1371, dividing a 60-second frame into 2,250 standardized slots of 26.67 ms. Lans originally drafted the specification around civil aviation for VHF Data Link Mode 4 (**VDL Mode 4**) under ICAO. Its maritime application emerged through trials with the Swedish Maritime Administration (**SMA**) in the Baltic during the early 1990s ([Chapter 9](ch09-prehistory-and-stdma.md)).

When the IMO drafted performance standards in Resolution MSC.74(69) Annex 3 (1998) and ITU standardized Recommendation ITU-R M.1371-0, member states objected to compelling patented technology on merchant fleets. Under the Common Patent Policy for ITU-T/ITU-R/ISO/IEC, patent holders declare whether they will license royalty-free or on Reasonable and Non-Discriminatory (**RAND** / **FRAND**) terms. Lans agreed to waive royalties specifically for commercial ships mandated to carry AIS under SOLAS ([Chapter 16](ch16-laws-and-treaties.md)). Crucially, this royalty-free waiver excluded non-compulsory applications—including recreational boats, fishing vessels, Aids to Navigation (**AtoN**), and base stations. In 2007, Lans filed an IEC declaration against Class B standard IEC 62287 under "Option 2" (RAND licensing).

### 17.1.2 The procedural disaster of *Lans v. Digital Equipment Corp.*

Lans's enforcement posture in the United States collapsed through a catastrophic procedural defect involving his separate color graphics patent, US Patent 4,303,986 (*Lans v. Digital Equipment Corp.*, 252 F.3d 1320 (Fed. Cir. 2001)). In 1996–1997, Lans sued major computer manufacturers in federal district court in his individual capacity. In discovery, defendants revealed Lans had assigned the patent in 1989 to his holding company, Uniboard Aktiebolag. Under 35 U.S.C. § 281, only the legal titleholder possesses standing to sue.

District Judge Royce C. Lamberth denied Lans's motion to substitute Uniboard AB under Rule 17(a), dismissed the suits with prejudice, and assessed substantial Rule 11 attorney fees against Lans personally. The Federal Circuit affirmed in 2001. By the time Uniboard refiled, the patent had expired, severely limiting damages under 35 U.S.C. § 286. 

This defeat paralyzed Lans's US licensing campaign. In separate administrative proceedings, US Patent 5,506,587 was challenged in ex parte reexamination. On 30 March 2010, the USPTO issued Reexamination Certificate No. 7428, cancelling all 13 claims over prior art. European patent EP 0 592 560 B1 expired on 29 June 2012, and the US patent reached lifetime expiration on 9 April 2013, placing foundational STDMA completely in the public domain.

### 17.1.3 The Class B CSTDMA avoidance architecture and SRT's acquisition

In 2003, when IEC Working Group TC80/WG15 convened to standardize low-cost Class B equipment, delegates sought to avoid SOTDMA to escape Lans's licensing demands. Engineers Mark M. Johnson and Andreas Lesch designed Carrier-Sense TDMA (**CSTDMA**): rather than reserving future slots in advance, the transponder listens immediately prior to a candidate slot for 1,111 bits (115.7 ms) and transmits only if unoccupied by Class A traffic ([Chapter 20](ch20-architecture-and-station-classes.md); [Chapter 21](ch21-link-layer-tdma.md)). Johnson assured WG15 this avoided IPR issues.

Two days later, on 9 June 2003, Johnson and Lesch filed US Provisional 60/477,125, issuing on 31 March 2009 as US Patent 7,512,095 (Johnson 2009cstdma). Although designed to circumvent one patent, the avoidance scheme was itself patented.

> **Case file.**
>
> **The SRT CSTDMA patent acquisition (2015).**
> In March 2015, Software Radio Technology plc (SRT Marine Systems), holding an estimated 80% market share in Class B transceiver OEM modules, acquired rights to US Patent 7,512,095 from co-inventor Lesch. In June 2015, SRT sent licensing demands to competitors requesting 5% of net retail sales (~$35 per unit), six years of retroactive arrears, and quarterly royalties. Competitors resisted, citing standard-setting equitable estoppel and prior art. The patent lapsed for failure to pay maintenance fees, demonstrating the risks of standard-setting patent holdup.

## 17.2 Collision litigation: AIS and VDR telemetry in admiralty courts

In collision litigation, admiralty courts evaluate negligence under COLREGs using logbooks, audio transcripts, and electronic tracking data. With compulsory carriage under SOLAS Chapter V and certified Voyage Data Recorders (**VDR**; IEC 61996), AIS telemetry provides objective tracking evidence to reconstruct encounters and apportion fault.

### 17.2.1 *Ever Smart v. Alexandra 1* [2021] UKSC 6: Channel approaches

The interaction between narrow channels and crossing rules was resolved by the UK Supreme Court in *Evergreen Marine (UK) Ltd v. Nautical Challenge Ltd (The "Ever Smart" and "Alexandra 1")* [2021] UKSC 6 (UKSC_2021_6). 

On 11 February 2015, container ship *Ever Smart* (83,651 GT), exiting Jebel Ali fairway at 12 knots, collided with inbound VLCC *Alexandra 1* (164,286 GT), awaiting a pilot while drifting under 2 knots. The ships approached on a steady relative bearing for 23 minutes before colliding, sustaining over $12 million in damage.

The legal issue was whether COLREGs Rule 9 (Narrow Channels) or Rule 15 (Crossing Rules) governed:
- Under Rule 15, *Alexandra 1* had *Ever Smart* on her starboard bow as the give-way vessel, obligated to keep clear under Rule 16, while *Ever Smart* was stand-on under Rule 17.
- Lower courts held Rule 9 displaced Rule 15 because *Ever Smart* had not fully exited the channel and *Alexandra 1* was not on a steady course, apportioning liability 80% to *Ever Smart* and 20% to *Alexandra 1*.

The Supreme Court unanimously reversed, using second-by-second AIS telemetry to establish two legal rules:
1. **Crossing Rules Apply at Fairway Exits:** Crossing rules govern whenever vessels navigate on crossing paths involving collision risk, even if one is exiting a channel. Rule 9 overrides crossing rules only once an inbound vessel actually shapes its course to enter and align with the channel.
2. **Heading Constancy Is Not Required:** The give-way vessel need not maintain a constant course along the water; steady bearing across AIS data engaged Rule 15.

On remittal, liability was adjusted to 70% against *Ever Smart* and 30% against *Alexandra 1*.

### 17.2.2 The *Cosco Busan* allision (2007): Criminal record tampering

On 7 November 2007, containership *M/V Cosco Busan* (68,000 GT) allided with the San Francisco–Oakland Bay Bridge in dense fog, spilling 53,569 gallons of fuel oil (NTSB_MAR_09_01).

ECDIS/AIS logs correlated with USCG VTS shore radar proved the pilot, impaired by prescription drugs, misidentified bridge tower icons for navigable spans. The master failed to conduct a proper Master-Pilot Exchange (**MPX**) or cross-check radar. AIS proved the ship tracked directly into the tower fender at 10.5 knots without slowing down until seconds before impact.

In *United States v. Fleet Management Ltd.*, No. CR-08-0160 SI (N.D. Cal. 2009; US_v_Fleet_2009), the manager pleaded guilty to OPA-90 violations and felony obstruction under 18 U.S.C. § 1519. Shore executives had fabricated training logs post-casualty to counter the telemetry. File creation timestamps exposed the forgery. Fleet Management paid a $10 million fine, the pilot served prison time, and civil claims settled for $44.4 million.

### 17.2.3 The *Sanchi* / *CF Crystal* disaster (2018): Electronic target complacency

On 6 January 2018, Suezmax tanker *Sanchi* (carrying 136,000 metric tons of condensate) collided with bulk carrier *CF Crystal* in the East China Sea, killing all 32 crew on *Sanchi* in an inferno (MSA_Sanchi_2018).

AIS and VDR data recovered from *CF Crystal* proved the vessels tracked on steady relative bearings for 26 minutes prior to collision (*CF Crystal* heading southwest at 13.2 knots; *Sanchi* heading north at 10.4 knots). As the give-way vessel under Rule 15, *Sanchi* failed to act. As the stand-on vessel, *CF Crystal* made minor starboard alterations that breached Rule 17.

Crucially, both conning officers tracked each other as passive AIS icons on ECDIS without computing manual or ARPA radar vectors to determine CPA/TCPA. Investigators censured both crews under Rule 5 and Rule 7(c), emphasizing that broadcast AIS telemetry cannot substitute for systematic radar plotting.

### 17.2.4 The *Dali* Key Bridge disaster (2024): Limitation of liability

On 26 March 2024, containership *M/V Dali* suffered switchboard blackout and steering loss outbound from Baltimore, striking Pier 17 of the Francis Scott Key Bridge (NTSB_Dali_2024). The bridge collapsed, killing six workers and closing the port.

NTSB and FBI investigators secured VDR and NAIS records, reconstructing the second-by-second timeline: blackout at 01:24:59; auxiliary emergency power restoration at 01:26:02 reconnecting AIS; uncontrolled drift at 8.7 knots with starboard yaw; and Mayday broadcast at 01:27:50 enabling police to close bridge traffic before impact at 01:28:45.

Shipowner Grace Ocean and manager Synergy Marine petitioned to limit liability under 46 U.S.C. §§ 30501 *et seq.* to $43.7 million against $4+ billion in claims. Claimants used historical AIS and power telemetry from prior voyages to argue the ship had unresolved electrical faults within management's **privity or knowledge**. The owners settled federal channel clearance claims for $102 million in October 2024 while limitation trials proceeded.

| Casualty Event | Primary Legal Issue | AIS / Telemetry Role | Final Legal Disposition |
|---|---|---|---|
| *Ever Smart / Alexandra 1* (2021) | COLREGs Rule 9 vs. Rule 15 | Second-by-second bearing proved crossing rules applied | UK Supreme Court reversed lower courts; 70/30 fault apportionment (UKSC_2021_6) |
| *Cosco Busan* (2007) | Pilot impairment, poor BRM, corporate record falsification | Proved zero deceleration; telemetry exposed post-crash forgery | $10M fine; 18 U.S.C. § 1519 obstruction guilty plea (US_v_Fleet_2009) |
| *Sanchi / CF Crystal* (2018) | Rule 15 crossing; look-out failure under Rule 5 | Constant relative bearing for 26 minutes with zero action | Mutual liability; casualty report censured AIS target complacency |
| *Dali / Key Bridge* (2024) | 46 U.S.C. §§ 30501 *et seq.* (Limitation of Liability) | Synchronized power loss, yaw, and VHF Mayday | $102M federal cleanup settlement; ongoing trial on privity |

## 17.3 Forensic disputes: The *Sewol* ferry disaster (2014)

The sinking of ferry *MV Sewol* on 16 April 2014, killing 304 passengers, produced intense forensic disputes over tracking data (KMST_Sewol_2014). Independent analysts identified a 36-second AIS transmission gap (08:48:37 to 08:49:13 KST) during the vessel's fatal starboard turn, while coastal radar tracks showed abrupt angular shifts, sparking allegations of government tampering.

Inquiries by the Special Commission on Social Disaster Investigation and a Special Prosecutor audited all raw NMEA logs and VTS buffers. They determined the 36-second gap resulted from physical failure, not sabotage: excessive cargo overloading caused extreme listing beyond 30 degrees during the turn, cutting fuel suction, tripping generators, and causing a bridge blackout. The transponder lost power and rebooted, taking several slot frames to regain GNSS lock. In August 2021, the Special Prosecutor closed the probe, finding no evidence of falsification. The case highlights that tracking gaps can stem from casualty power losses.

## 17.4 Criminal and sanctions enforcement: Dark fleets and illicit transfers

In international sanctions enforcement, maritime tracking telemetry has become a decisive prosecutorial weapon to prove evasion and seize vessels under civil forfeiture.

### 17.4.1 The *M/T Courageous* civil forfeiture (2021)

In *United States v. The Motor Tanker Courageous (IMO 8617524)*, No. 21-cv-03618 (S.D.N.Y. 2021; US_v_Courageous_2021), federal prosecutors used AIS telemetry to seize a 2,734-ton tanker operated by Singaporean national Kwek Kee Seng. Between August and December 2019, *Courageous* delivered refined petroleum to DPRK tankers (including *Saebyol*) violating UNSCR 2397 and IEEPA (50 U.S.C. §§ 1701 *et seq.*).

The ship routinely disabled its AIS transponder to operate "dark" during high-seas rendezvous, transmitted spoofed positions to simulate innocent anchorage, and cleared oil purchases in US dollars through correspondent banks. Satellite imagery verified *Courageous* alongside *Saebyol* on 4 November 2019 conducting an illegal transfer. In April 2021, DOJ filed an in rem forfeiture complaint, and District Judge Valerie E. Caproni entered a default judgment forfeiting the ship to the US government.

### 17.4.2 OFAC red flags and the Multilateral Sanctions Monitoring Team

On 14 May 2020, OFAC, the State Department, and the USCG published a joint sanctions advisory designating AIS disabling and manipulation as a primary deceptive shipping practice. The advisory recommended that charterparties include "AIS exclusion clauses" permitting contract termination if a ship disables AIS without valid safety justification under IMO Resolution A.1106(29). Following Russia's veto of the UNSC 1718 Panel of Experts in March 2024 (UN_PoE_2019_171), eleven states formed the Multilateral Sanctions Monitoring Team (**MSMT**) in October 2024, tracking dark STS operations via satellite AIS, radar, and optical imagery.

### 17.4.3 "AIS off" as evidence in illegal fishing (IUU)

While SOLAS exempts fishing vessels, EU Directive 2002/59/EC (Article 6a) and Regulation (EC) 1224/2009 (Article 10) mandate Class A AIS on fishing vessels exceeding 15 meters LOA. In fisheries enforcement, prosecutors treat AIS gaps along Marine Protected Area boundaries as circumstantial evidence of illegal activity. Under EU Regulation 2023/2842, failing to maintain a contemporaneous logbook entry of a deactivation removes statutory defenses, establishing an administrative violation. Scholars (Toonen and Bush 2020; Toonen2020fisheries) emphasize that treating digital surveillance as absolute proof can marginalize small fishers.

## 17.5 Evidentiary admissibility and chain of custody for AIS data

Introducing digital tracking data into judicial proceedings requires satisfying evidentiary standards governing hearsay, authentication, and chain of custody.

### 17.5.1 The hearsay hurdle and business records exceptions

Under Federal Rule of Evidence (**FRE**) 801, admissibility divides into two categories:
1. **Machine-Generated Telemetry:** Autonomous GNSS coordinates, SOG, COG, and slot timestamps in Messages 1–4 are physical machine measurements, not statements by a person, and do not constitute hearsay under FRE 801(a). They require foundational authentication under FRE 901.
2. **Human-Entered Static Data:** Manually typed fields in Message 5 (vessel name, destination, draft, cargo type) are assertive statements and constitute hearsay. They require admission under the business records exception (FRE 803(6)) via custodian testimony or as public records (FRE 803(8)).

### 17.5.2 Establishing the digital chain of custody

Admissibility requires an unbroken chain of custody:
1. **Raw Preservation:** Store raw NMEA 0183 (`!AIVDM`) strings rather than web app screenshots.
2. **TAG Block Provenance:** Preserve NMEA 4.10 TAG blocks (`\s:,c:,n:\`) recording base station IDs and UTC arrival timestamps.
3. **Cryptographic Hashing:** Generate SHA-256 digests immediately upon extraction from VDR or receiver storage.
4. **Tool Validation:** Ensure decoders (`libais`, `pyais`) meet *Daubert* reliability standards without introducing spatial distortion.

> **Try it.**
>
> **Cryptographic hashing of raw AIS NMEA evidence.**
> Parse an authenticated NMEA TAG-block line, verify its checksum, and compute an immutable SHA-256 fingerprint:
>
> ```python
> import hashlib
> from code.decode.tagblock import parse_line
> 
> # Raw log line from a certified USCG shore receiver
> raw_log = r"\s:USCG_BOS,c:1700000000*12\!AIVDM,1,1,,A,13u?etPv2;0n:nvK>QAU=4wf0000,0*21"
> 
> # 1. Parse TAG block and sentence
> tag, sentence = parse_line(raw_log)
> print(f"Source: {tag.source}, UTC: {tag.unix_time}, Checksum OK: {tag.checksum_ok}")
> 
> # 2. Generate SHA-256 evidence fingerprint
> line_hash = hashlib.sha256(raw_log.encode("utf-8")).hexdigest()
> print(f"SHA-256: {line_hash}")
> ```
>
> Expected output:
> ```
> Source: USCG_BOS, UTC: 1700000000.0, Checksum OK: True
> SHA-256: 48edc299e8499994b737f64592673300c17494bf056c5fd97385e7a74caada0b
> ```

## 17.6 Data ownership, copyright, and scraping disputes

Under 17 U.S.C. § 102(b) and *Feist Publications v. Rural Telephone Service*, 499 U.S. 340 (1991), copyright does not protect raw facts. Broadcaster radio telemetry emitted over international marine VHF lacks human authorship and resides in the public domain. Anyone with an SDR receiver may lawfully record and process unencrypted broadcasts.

However, database rights differ by jurisdiction:
- **EU Sui Generis Database Rights:** Under EU Directive 96/9/EC (*Ryanair v. PR Aviation*), aggregators demonstrating "substantial investment" in collecting and verifying vessel data can legally prevent unauthorized extraction or scraping.
- **US Contractual Protection:** The US recognizes no *sui generis* database right. Providers protect web feeds through click-wrap Terms of Service. Under *hiQ Labs v. LinkedIn* (9th Cir. 2022) and *X Corp. v. Bright Data* (N.D. Cal. 2024), scraping public web data outside password walls does not violate the Computer Fraud and Abuse Act (18 U.S.C. § 1030), though scraping authenticated API accounts breaches contract terms.

## 17.7 Data privacy and administrative law: GDPR and FOIA

Expanding AIS to small craft creates tension with privacy and public disclosure laws.

### 17.7.1 GDPR and small craft

Under GDPR Article 4(1), personal data includes information relating to an identifiable natural person. While position reports from large commercial ships are non-personal corporate data, Class B reports from private yachts whose MMSI resolves to an individual owner via public registers (FCC ULS, ITU MARS) constitute personal location data. Aggregators publishing unredacted yacht tracks operate as data controllers under Article 4(7) requiring an Article 6 legal basis. To mitigate risk, Norway's Kystverket filters fishing vessels <15 m and leisure craft <45 m from open feeds ([Chapter 19](ch19-privacy-and-ethics.md)).

### 17.7.2 FOIA litigation: *EPIC v. USCG*

In *Electronic Privacy Information Center v. United States Coast Guard*, Civil Action No. 15-1527 (D.D.C. 2016; EPIC_v_USCG_2016), EPIC sued under FOIA (5 U.S.C. § 552) for NAIS records. The settlement released 2,500 pages showing NAIS ingested 92 million messages daily from 12,700 vessels across 58 ports and shared real-time feeds with numerous intelligence agencies under 75 FR 2557 (USCG_75FR2557). EPIC cited *United States v. Jones*, 565 U.S. 400 (2012), arguing that tracking recreational boaters infringed privacy expectations. In response, NOAA/BOEM Marine Cadastre temporarily encrypted MMSI fields in public datasets from 2010 to 2014 before abandoning hashing as ineffective.

## 17.8 Civil liabilities: Misleading data and the "ghost ship" problem

In maritime torts, civil liability arises when inaccurate or missing data causes damages:
- **Installer Liability:** Under 47 CFR § 80.231(b), only certified installers may program Class B static data. Incorrectly programmed dimensions swap antenna offsets, causing neighboring ECDIS to render distorted hull boundaries. Installers and owners face liability for resulting allisions under 33 CFR § 164.46(d)(2)(iii).
- **Master's Liability for Stale Data:** Failing to update navigation status from "Under way" (Status 0) to "At anchor" (Status 1) creates comparative fault under *The Pennsylvania* doctrine (86 U.S. 125 (1873)), shifting the burden to the offending ship to prove its breach could not have caused the casualty.
- **Spoofing and Reasonable Reliance:** In electronic warfare corridors with GPS spoofing ([Chapter 59](ch59-spoofing.md); [Chapter 62](ch62-gnss-jamming-spoofing.md)), watchstanders who collide while trusting phantom AIS targets cannot escape liability: COLREGs Rules 5 and 7(c) require visual and radar cross-checks. Blind reliance on broadcast telemetry constitutes negligence.

## Then & now

| System / Dimension | Historic Practice (1990s–early 2000s) | Contemporary State (2020s) |
|---|---|---|
| **Collision Reconstruction** | ⟨H⟩ Relied upon handwritten ship logbooks, paper chart pricks, engine tachographs, and conflicting visual testimonies. | ⟨+⟩ Decided by synchronized second-by-second VDR extractions, NAIS shore receiver logs, and radar target track overlays (*Ever Smart*, *Cosco Busan*). |
| **Intellectual Property** | ⟨H⟩ STDMA dominated by Håkan Lans's patents (SE 1991, US 1996); international adoption delayed by member-state royalty disputes. | ⟨+⟩ Lans STDMA patents cancelled/expired; CSTDMA patent disputes lapsed; core protocol architecture resides completely in the public domain. |
| **Sanctions & Smuggling** | ⟨H⟩ Enforcement required physical aerial maritime patrol, naval interdiction on the high seas, and paper cargo manifests. | ⟨+⟩ Federal prosecutors secure judicial civil forfeiture of tankers (*Courageous*) based on dark-voyage AIS anomalies and satellite track fusion. |
| **Admissibility Standards** | ⟨H⟩ Electronic track printouts faced persistent hearsay challenges, requiring live programmer testimony on system architecture. | ⟨+⟩ Machine-generated NMEA telemetry recognized as non-hearsay under FRE 801; authenticated via cryptographic hashes and NMEA 4.10 TAG blocks. |
| **Small-Craft Privacy** | ⟨H⟩ Regarded as a purely theoretical concern; early mandates applied almost exclusively to commercial merchant tonnage above 300 GT. | ⟨+⟩ Intense GDPR and FOIA litigation (*EPIC v. USCG*); open-data feeds filter small craft to prevent unlawful personal location profiling. |
| **Data Scraping Rights** | ⟨H⟩ Data restricted to dedicated physical VTS terminals and direct serial marine electronics interfaces. | ⟨+⟩ Commercial aggregation platforms protect web feeds via click-wrap contracts and EU *sui generis* database rights against automated scraping. |

## Validation, uncertainty & data quality

In forensic and judicial proceedings, raw AIS data cannot be accepted into the record without a documented error budget and uncertainty qualification. When reconstructing a collision or investigating a sanctions breach, expert witnesses must account for four distinct sources of telemetry uncertainty:

```
  Total Positioning Error Budget:
  ────────────────────────────────────────────────────────────────────────
  Component                        Nominal               Degraded
  ────────────────────────────────────────────────────────────────────────
  GNSS Ephemeris & Atmospheric     ±2.5 m (95%)          ±15.0 m (Spoofed/Multichannel)
  Sensor Reference Offset          ±0.5 m (Certified)    ±50.0 m (Stale/Default A,B,C,D)
  Dynamic Latency & Smoothing      ±0.8 m (12 kn, 2s)    ±30.8 m (12 kn, Class B 10s gap)
  Interpolation Jitter             ±0.2 m (Spline)       ±15.0 m (Linear across gap)
  ────────────────────────────────────────────────────────────────────────
  Aggregate RMS Positional Error   ±2.7 m (Certified)    ±63.1 m (Forensic Warning)
```

1. **GNSS Pseudorange and Offset Uncertainties:** Standard shipboard GNSS receivers without differential corrections provide horizontal accuracy of approximately $\pm 2.5\text{ m}$ (95% confidence). However, reported coordinates mark the **antenna location**, not the hull contact point. If internal offsets ($A, B, C, D$ in Message 5; [Chapter 22](ch22-message-catalog.md)) are wrong or unverified, reconstructed hull perimeters can drift by $50\text{ m}$ relative to impact points.
2. **Dynamic Latency and Reporting Intervals:** Class A transmission intervals vary from 2 seconds (maneuvering) to 3 minutes (moored). Class B reports every 30 seconds (or 14 seconds when speed exceeds 14 knots for SOTDMA). A vessel at 24 knots covers 370 meters in 30 seconds; non-linear hydrodynamic spline interpolation is mandatory to avoid track distortion.
3. **Packet Loss and Slot Contention:** In dense ports, slot collisions cause packet loss exceeding 15% ([Chapter 30](ch30-network-loading-packet-loss.md)). A 30–60 second tracking gap is often a normal statistical radio artifact, not proof of deliberate deactivation.
4. **Validation Checklist for Court Exhibits:**
   - Verify CRC checksums on all raw `!AIVDM` lines;
   - Cross-check NMEA 4.10 TAG block timestamps against GPS base station reports (Message 4);
   - Calculate acceleration ($\Delta v / \Delta t$) across sequential fixes: values exceeding $2.5\text{ m/s}^2$ on cargo ships indicate GNSS jumps or spoofing;
   - Corroborate AIS tracks against independent shore radar (VTS ARPA) and physical contact damage.

## Software

**Open source:**
- **libais** (C++ with Python bindings): Industry reference library for decoding raw NMEA 0183 AIVDM/AIVDO strings into structured JSON/C-struct records. Used in forensic discovery without GUI interpolation errors. *Caveat:* Requires custom wrappers to handle non-standard sentence fragments gracefully.
- **pyais** (Python 3): Pure-Python decoder supporting Messages 1–27, NMEA 4.10 TAG blocks, and binary payloads. Excellent for script-driven chain-of-custody verification. *Caveat:* Processing throughput is lower than compiled C++ engines on multi-gigabyte feeds.

**Free but closed:**
- **QGIS with Trajectory Tools**: Open-source GIS platform supporting spatial-temporal track reconstruction and collision bounding-box rendering. *Caveat:* Users must manually configure geodetic projections; default linear interpolation scripts distort turn rates.

**Commercial:**
- **Kongsberg Norcontrol / Wärtsilä Transas Navi-Harbour**: Enterprise VTS recording suites used by coast guards. Generates synchronized playback combining coastal radar, VHF audio, and raw AIS feeds certified for judicial proceedings. *Caveat:* Proprietary binary formats require licensed dongles for court playback.
- **Spire Maritime / Kpler Vessel Tracking APIs**: Global commercial intelligence feeds providing filtered, cleaned, and satellite-interpolated vessel trajectories. *Caveat:* Proprietary cleaning pipelines downsample raw timestamps, creating evidentiary chain-of-custody vulnerabilities if introduced directly without raw NMEA source logs.

## Standards & guides

- **IMO Resolution MSC.74(69), Annex 3** (1998): *Recommendation on Performance Standards for Universal Automatic Identification System (AIS)*. Governs international functional requirements and the baseline non-proprietary status of shipborne transponders.
- **IMO Resolution A.1106(29)** (2015): *Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems (AIS)* (IMO_A1106_29). Codifies operational procedures, bridge look-out rules, and the legal criteria for switching off AIS.
- **International Regulations for Preventing Collisions at Sea 1972 (COLREGs)**: Rules 5, 7, 8, 9, and 15–17. Governs legal liability, lookout duties, crossing geometries, and the prohibition against relying on "scanty information" in collision avoidance.
- **United States Code: 46 U.S.C. § 70114 & 33 CFR § 164.46**: Governs statutory carriage thresholds, continuous operation rules, pilot-plug specifications, and exemptions in United States navigable waters.
- **United States Code: 47 CFR Part 80 (§§ 80.231, 80.275)**: Governs Federal Communications Commission equipment authorization, type-certification, and installer programming restrictions for AIS hardware.
- **ISO/IEC 29147:2018**: *Information technology — Security techniques — Vulnerability disclosure*. The international technical standard establishing coordinated disclosure norms for reporting security and radio vulnerabilities to standard bodies and equipment vendors.
- **Directive 2002/59/EC (as amended by 2009/17/EC)**: *Community vessel traffic monitoring and information system*. Governs mandatory AIS installation and continuous operation for European Union commercial fishing fleets exceeding 15 meters.

## Pitfalls

- **Confusing raw facts with copyrighted databases:** Assuming commercial aggregators own underlying AIS tracking points. → Facts cannot be copyrighted, but structured databases enjoy protection under EU *sui generis* rights and contractual terms. → Scrape raw RF broadcasts directly or license data through formal contracts.
- **Treating temporary data gaps as criminal deactivation:** Inferring intentional sanctions evasion or IUU fishing from a 15-minute tracking gap. → VHF radio contention, terrain shadow, or satellite footprint latency frequently drop packets. → Corroborate tracking gaps with satellite SAR, optical imagery, and logbook entries before asserting dark-voyage intent.
- **Relying on web screenshots in admiralty proceedings:** Submitting consumer tracking app map captures as evidence in court. → Third-party aggregators apply aggressive smoothing, latency buffers, and proprietary interpolation that distort velocity vectors. → Subpoena raw NMEA 0183 strings, VDR memory logs, and certified VTS radar archives with verified TAG blocks.
- **Ignoring the human-input hearsay line:** Attempting to introduce static Message 5 cargo and destination fields without a business records foundation. → Static metadata is entered by crew members and constitutes out-of-court assertive conduct. → Authenticate static data through deck officers or under FRE 803(6)/803(8) exceptions.
- **Neglecting antenna geodetic reference offsets:** Plotting a collision contact point using raw GNSS antenna coordinates. → Antennas may be offset 100 meters from the bow on container vessels. → Apply Message 5 internal dimensions $A, B, C, D$ to reconstruct accurate physical hull perimeters.
- **Assuming SOLAS carriage rules apply to fishing vessels:** Citing SOLAS Chapter V Regulation 19.2.4 to argue that an 18-meter fishing boat was required to transmit AIS. → SOLAS explicitly exempts fishing vessels. → Enforce tracking obligations under regional statutory regimes such as EU Directive 2002/59/EC or national coastal statutes.
- **Permitting vessel owners to self-program Class B transponders in the US:** Allowing an owner to manually enter their own MMSI on a newly purchased Class B unit. → Direct violation of 47 CFR § 80.231(b). → Ensure all static programming is performed by an authorized manufacturer or certified marine technician.
- **Failing to maintain a contemporaneous log of silent periods:** Deactivating transponders for piracy security without entering an explanation in the ship logbook. → Strips the master of the statutory defense under IMO Resolution A.1106(29). → Immediately record the precise time, position, and security justification in the deck logbook upon deactivation.
- **Using AIS as an excuse to ignore ARPA radar plotting:** Maneuvering to avoid an approaching target based solely on an AIS vector. → Violates COLREGs Rule 7(c) ("scanty information"). → Always verify target course, speed, and CPA using systematic radar plotting and visual compass bearings.
- **Ignoring GDPR implications for recreational craft:** Publishing unredacted historical tracks of small sailing yachts and leisure vessels. → Breaches EU data protection law when the MMSI can be resolved to a natural person. → Implement data filtering policies consistent with national open-data frameworks.

## Key takeaways

- **The STDMA patent barrier was real but is now entirely dissolved:** Håkan Lans's foundational US STDMA patent had its claims cancelled in reexamination in 2010 and reached lifetime expiration in 2013, leaving the core Class A SOTDMA protocol fully unencumbered in the public domain.
- **Class B CSTDMA was engineered for patent avoidance:** The carrier-sense architecture of Class B (IEC 62287-1) was created specifically to bypass Lans's STDMA patent, but the avoidance method was itself patented under US Patent 7,512,095, sparking commercial licensing disputes that subsequently lapsed.
- **Admiralty courts treat AIS as supplementary under COLREGs:** Electronic tracking data definitively settled the crossing geometry in landmark appeals such as *Ever Smart v. Alexandra 1* [2021] UKSC 6, but courts censure watchstanders who substitute broadcast vectors for systematic radar plotting under Rule 7(c).
- **Electronic data preserves corporate criminal liability:** As demonstrated in the *Cosco Busan* allision, federal prosecutors use digital timestamps and synchronized AIS/VDR telemetry to convict maritime companies of felony obstruction when shore management attempts to fabricate training and safety records.
- **The *Sewol* disaster proves tracking gaps are not always sabotage:** The 36-second AIS gap during the ferry's fatal turn was the physical result of extreme structural heel inducing auxiliary power blackouts, not digital tampering by state authorities.
- **Dark-voyage telemetry secures criminal and civil forfeitures:** In *United States v. M/T Courageous* (2021), the intentional deactivation and falsification of AIS broadcasts provided primary evidence of criminal intent to evade international sanctions, resulting in the judicial forfeiture of the vessel.
- **Machine telemetry is non-hearsay; static metadata requires an exception:** Raw GNSS coordinates in Messages 1–3 are machine-generated physical evidence admitted under simple authentication, whereas crew-entered static data in Message 5 constitutes hearsay requiring a business or public records exception.
- **Raw radio broadcasts cannot be copyrighted:** Individual AIS position reports are public-domain facts devoid of human authorship; legal protections against scraping are strictly limited to contractual click-wrap terms and the European *sui generis* database right.
- **Recreational tracking is personal location data under GDPR:** When a small craft's MMSI resolves to an individual owner via public licensing registers, broadcasting or republishing the vessel's unredacted movements triggers data privacy regulations, compelling national agencies to filter open feeds.

## References

- Electronic Privacy Information Center (2016). *Electronic Privacy Information Center v. United States Coast Guard*. Civil Action No. 15-1527 (RDM). US District Court for the District of Columbia.
- International Maritime Organization (2015). *Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems (AIS)*. IMO Resolution A.1106(29). London: International Maritime Organization.
- Johnson, M. M., Lesch, A. (2009). *Multiple Access Communication System for Moveable Objects*. US Patent 7,512,095 B2. Washington, D.C.: US Patent and Trademark Office.
- Korean Maritime Safety Tribunal (2014). *Investigation Report on the Sinking of Passenger Ferry Sewol*. Sejong: Ministry of Oceans and Fisheries, Republic of Korea.
- Lans, H. (1996). *Position Indicating System*. US Patent 5,506,587 A. Washington, D.C.: US Patent and Trademark Office.
- Maritime Safety Administration of the People's Republic of China (2018). *Investigation Report on the Collision between the "SANCHI" and "CF CRYSTAL"*. Shanghai: Joint Investigation Team.
- National Transportation Safety Board (2009). *Allision of Hong Kong-Registered Containership M/V Cosco Busan with the San Francisco-Oakland Bay Bridge, San Francisco, California, November 7, 2007*. Marine Accident Report NTSB/MAR-09/01. Washington, D.C.: National Transportation Safety Board.
- National Transportation Safety Board (2024). *Preliminary Report: Contact of Cargo Vessel Dali with Francis Scott Key Bridge and Subsequent Bridge Collapse, Baltimore, Maryland, March 26, 2024*. Accident Report DCA24MM031. Washington, D.C.: National Transportation Safety Board.
- Peach, R. (2011). *System and Method for Decoding Automatic Identification System Signals*. US Patent 7,876,865 B2. Washington, D.C.: US Patent and Trademark Office.
- Platzer, P. (2021). *AIS Spoofing and Dark-Target Detection Methodology*. US Patent 11,156,723 B2. Washington, D.C.: US Patent and Trademark Office.
- Toonen, H. M., Bush, S. R. (2020). The digital frontiers of fisheries governance: fish attraction devices, drones and satellites. *Journal of Environmental Policy & Planning*, 22(1):125–137. doi:10.1080/1523908X.2018.1461084
- UK Supreme Court (2021). *Evergreen Marine (UK) Limited v. Nautical Challenge Limited (The "Ever Smart" and "Alexandra 1")*. [2021] UKSC 6. London: The Supreme Court of the United Kingdom.
- United Nations Security Council (2019). *Report of the Panel of Experts Established Pursuant to Resolution 1874 (2009)*. Document S/2019/171. New York: United Nations.
- United States Coast Guard (2010). *Interim Policy for the Sharing of Information Collected by the Coast Guard Nationwide Automatic Identification System*. Federal Register, 75(10):2557–2559. Docket USCG-2009-0701.
- United States District Court for the Northern District of California (2009). *United States v. Fleet Management Ltd. (M/V Cosco Busan)*. Criminal No. CR-08-0160 SI. San Francisco: US District Court.
- United States District Court for the Southern District of New York (2021). *United States of America v. The Motor Tanker Courageous (IMO 8617524)*. Civil Action No. 21-cv-03618 (VEC). New York: US District Court.
