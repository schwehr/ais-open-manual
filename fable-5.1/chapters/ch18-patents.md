# Chapter 18 — Patents

> **Part III — Identity, institutions, law.** How competing intellectual property claims over time-slotted spectrum almost derailed maritime standardization, why Class B transponders were re-engineered around proprietary algorithms, and where patent rights govern the commercial data layer today.

**In this chapter.** You will master the intellectual property landscape that shaped the technical foundation, standardization, and commercial evolution of the Automatic Identification System (**AIS**). You will dissect the seminal patent family of Swedish inventor Håkan Lans and GP&C Systems International covering Self-Organized Time-Division Multiple Access (**SOTDMA**), tracing its 1991 priority filings, international prosecution, and eventual expiry and cancellation. You will examine the institutional mechanics of the Common Patent Policy governing the International Telecommunication Union (**ITU**), International Electrotechnical Commission (**IEC**), and International Organization for Standardization (**ISO**), understanding how declarations and royalty-free waivers enabled compulsory carriage under the International Convention for the Safety of Life at Sea (**SOLAS**). You will investigate the origin of Carrier-Sense TDMA (**CSTDMA**), designed specifically to circumvent Lans's patents, and the commercial fallout when Software Radio Technology (**SRT**) acquired and asserted rights to US Patent 7,512,095. You will analyze modern patent portfolios spanning satellite decollision, Doppler separation, receiver hardware, and trajectory analytics. Finally, you will establish operational verification protocols to audit patent registers and evaluate freedom-to-operate risks across software and hardware deployments.

## 18.1 The foundational STDMA dispute: Håkan Lans and GP&C

Modern maritime tracking rests upon an elegant architecture: mobile stations, synchronized to an absolute geodetic time standard, autonomously reserve transmission windows over a shared radio channel without centralized infrastructure. This protocol—Self-Organized Time-Division Multiple Access (**SOTDMA**)—originated as a privately patented invention created by the Swedish computer graphics and navigation pioneer Anders Håkan Lans and his operating entity, GP&C Systems International AB.

The interaction between Lans's patent rights and the safety obligations of the International Maritime Organization (**IMO**) represents a critical episode in maritime electronics. Had this patent standoff not been resolved through diplomatic compromise and licensing waivers, universal tracking might have splintered into incompatible regional proprietary architectures.

### 18.1.1 The Lans patent family and Claim 1 of US 5,506,587

Håkan Lans conceptualized a synchronized radio reporting scheme during the late 1980s and early 1990s. The core patent family traces its legal priority to two initial Swedish national patent filings:
1. **SE 9102034**, filed in Sweden on **1 July 1991**.
2. **SE 9103542**, filed in Sweden on **28 November 1991**.

An intermediate Swedish application, **SE 9102362**, filed on 15 August 1991, matured into Swedish national patent **SE 468 452 B** ("Position indicating system and position station for a position indicating system"), published on 18 January 1993. On **29 June 1992**, GP&C Systems International AB filed an international application under the Patent Cooperation Treaty (**PCT**), designated **PCT/SE92/00485**, claiming priority from the 1991 Swedish applications. Published on **21 January 1993** as **WO 93/01576 A1**, the application entered national and regional phases in North America, Europe, and Asia.

In the United States, national stage entry under 35 U.S.C. § 371 was assigned application number **08/170,167** on **23 December 1993**. The patent was granted by the United States Patent and Trademark Office (**USPTO**) on **9 April 1996** as **US Patent 5,506,587 A**, titled *"Position indicating system"*, naming Håkan Lans as sole inventor and GP&C Systems International AB as original assignee, comprising 13 claims.

The broadest independent apparatus claim, Claim 1 of US 5,506,587, captures the exact conceptual framework of what ITU-R M.1371 later standardized as SOTDMA:

> "1. A position indicating system comprising:  
> a plurality of movable stations each having:  
> (a) means for receiving position signals from a plurality of geometrically distributed transmitters;  
> (b) means for determining the station's geographical coordinates based upon said position signals;  
> (c) a time base common to all of said movable stations, said common time base defining time blocks which are standardized, enumerable and form a common, accurate, repeating maximal frame of known length, said maximal frame being of fixed duration and being divided into a predetermined number of said standardized time blocks;  
> (d) a transmitter for transmitting position signals in a common radio channel; and  
> (e) means for occupying a free time block in each maximal frame and for autonomously transmitting therein of a position signal in the common radio channel, said means occupying a free time block without receiving an assignment from any central coordinating unit, said position signal including information indicating the station's identity and geographical coordinates."

A comparison between Claim 1 of US 5,506,587 and Annex 2 of Recommendation ITU-R M.1371 ([Chapter 21](ch21-link-layer-tdma.md)) reveals identical technical structures:
- "Position signals from a plurality of geometrically distributed transmitters" corresponds to GNSS, specifically GPS.
- "Common time base" defining "time blocks which are standardized, enumerable and form a common, accurate, repeating maximal frame of known length" corresponds directly to the UTC frame of 60 seconds, subdivided into 2,250 discrete time slots of 26.67 milliseconds each.
- "Means for occupying a free time block ... autonomously ... without receiving an assignment from any central coordinating unit" is the operational definition of SOTDMA slot selection.

The patent specification focused on civil aviation (air traffic control, Area Control Centers, and collision avoidance), later pursued as **VDL Mode 4**. It migrated to maritime operations when the Swedish Maritime Administration (*Sjöfartsverket*, **SMA**) recognized that Lans's autonomous TDMA scheme could solve ship-to-ship tracking without saturated voice channels.

In Europe, regional application **EP 0 592 560 A1** was granted on **27 August 1997** as **EP 0 592 560 B1**, validated in Germany, the United Kingdom, France, Denmark, Finland, Greece, and Norway, with counterparts granted in Canada, Japan, South Korea, Australia, and Russia.

| Jurisdiction | Patent / Publication | Application / Priority | Grant Date | Statutory Expiry |
|:---|:---|:---|:---|:---|
| **Sweden (SE)** | SE 468 452 B | SE 9102362 (15 Aug 1991) | 18 Jan 1993 | 29 Jun 2012 |
| **PCT (WIPO)** | WO 1993/001576 A1 | PCT/SE92/00485 (29 Jun 1992) | N/A (Pub. 21 Jan 1993) | N/A |
| **United States (US)** | US 5,506,587 A | US 08/170,167 (29 Jun 1992) | 9 Apr 1996 | 9 Apr 2013 (Cancelled 2010) |
| **European Patent Office (EP)** | EP 0 592 560 B1 | EP 92913936.8 (29 Jun 1992) | 27 Aug 1997 | 29 Jun 2012 |
| **Canada (CA)** | CA 2,111,980 C | CA 2111980 (29 Jun 1992) | 18 Mar 2003 | 29 Jun 2012 |
| **Japan (JP)** | JP 3,262,332 B2 | JP 51199392 (29 Jun 1992) | 4 Mar 2002 | 29 Jun 2012 |
| **Republic of Korea (KR)** | KR 100238959 B1 | KR 19940700085 (29 Jun 1992) | 15 Jan 2000 | 29 Jun 2012 |
| **Australia (AU)** | AU 661,706 B2 | AU 199222387 (29 Jun 1992) | 3 Aug 1995 | 29 Jun 2012 |

### 18.1.2 Patent term arithmetic: 17 years from grant versus 20 years from filing

Calculating the expiration dates of the Lans portfolio illustrates the transitional rules enacted under the Uruguay Round Agreements Act (**URAA**) of 1994, harmonizing United States patent terms under **GATT**.

Under international practice (EPC Article 63), a patent term runs strictly **20 years from the filing date**. For EP 0 592 560 B1 (filed **29 June 1992**), the term ended on **29 June 2012** across all validated European states.

In the United States, patent terms historically ran for **17 years from the date of patent grant**. To implement GATT harmonization, 35 U.S.C. § 154 was amended effective **8 June 1995**. For United States applications filed prior to 8 June 1995:

$$\text{Term} = \max\left(17\text{ years from grant date},\; 20\text{ years from earliest effective filing date}\right)$$

For US 5,506,587, the effective United States filing date (the PCT filing date under 35 U.S.C. § 365(c)) was 29 June 1992. The grant date was 9 April 1996:
1. 20 years from effective filing date: $1992\text{-}06\text{-}29 + 20\text{ years} = \mathbf{2012\text{-}06\text{-}29}$.
2. 17 years from patent grant date: $1996\text{-}04\text{-}09 + 17\text{ years} = \mathbf{2013\text{-}04\text{-}09}$.

Because 17 years from grant was later, the statutory term of US 5,506,587 extended to **9 April 2013**—ten months after its European counterpart expired.

> **Worked example.**
>
> **Pre-GATT Patent Term Calculation.**
>
> Determine the statutory term of an early 1990s US patent under 35 U.S.C. § 154(c)(1):
>
> - **PCT Filing Date ($T_{\text{filing}}$):** 29 June 1992
> - **US Issue Date ($T_{\text{grant}}$):** 9 April 1996
> - **GATT Transition Cutoff:** 8 June 1995
>
> 1. Because $T_{\text{filing}} < \text{June 8, 1995}$, the patent qualifies under 35 U.S.C. § 154(c)(1).
> 2. Compute 20-year term from filing: $\text{Date}_{20} = 1992\text{-}06\text{-}29 + 20\text{ years} = 2012\text{-}06\text{-}29$.
> 3. Compute 17-year term from issue: $\text{Date}_{17} = 1996\text{-}04\text{-}09 + 17\text{ years} = 2013\text{-}04\text{-}09$.
> 4. Statutory expiration: $\text{Expiration} = \max(\text{Date}_{20}, \text{Date}_{17}) = 2013\text{-}04\text{-}09$.
>
> The patent remains in force until 9 April 2013, whereas foreign counterparts expired on 29 June 2012.

### 18.1.3 The 2010 USPTO reexamination and claim cancellation

Although the statutory lifetime of US 5,506,587 extended to 9 April 2013, the patent did not survive intact. During the mid-2000s, third parties challenged the patent's validity, initiating an *ex parte* reexamination proceeding before the USPTO under 35 U.S.C. §§ 302–307. The reexamination cited extensive prior art in packet radio communications, time-division multiplexing, and satellite timing synchronization.

On **30 March 2010**, the USPTO issued *Ex Parte* Reexamination Certificate **7428** for US Patent 5,506,587, formally cancelling **all 13 claims**. The cancellation extinguished the patent as a matter of law, eliminating prospective infringement liability within the United States three years prior to its nominal expiration.

### 18.1.4 The unrelated colour graphics litigation: A cautionary tale in standing

Håkan Lans is often described in industry lore as having lost his navigation patent in court. This is incorrect. The litigation that consumed Lans in United States courts involved an unrelated invention: **US Patent 4,303,986**, granted 1 December 1981, covering a colour graphics display architecture.

In 1997, Lans sued personal computer manufacturers in his individual capacity in the District Court for the District of Columbia (*Lans v. Digital Equipment Corp.*). Defendants revealed during discovery that Lans had previously assigned all title in the patent to his corporate holding company, **Uniboard Aktiebolag**. 

Because an individual lacking title has no standing to sue under 35 U.S.C. § 281, the court dismissed the case and awarded defense attorney fees under 35 U.S.C. § 285. On appeal, the Federal Circuit affirmed in ***Lans v. Digital Equipment Corp.*, 252 F.3d 1320 (Fed. Cir. 2001)**, holding that an assignor lacks standing and that pre-suit notice in the inventor's personal name did not satisfy 35 U.S.C. § 287.

> **Case file.**
>
> ***Lans v. Digital Equipment Corp.*, 252 F.3d 1320 (Fed. Cir. 2001).**
>
> - **Patent at issue:** US 4,303,986 (Colour graphics display architecture, granted 1 Dec 1981).
> - **Procedural defect:** Lans sued in his personal name in 1997 after having assigned the patent to Uniboard AB in 1989.
> - **Holding:** An inventor assigning title to his own entity lacks standing under 35 U.S.C. § 281; substitution was denied under FRCP 17(a) and attorney fees were awarded against the plaintiff.
> - **Impact on maritime tracking:** The multi-million-dollar defeat in *Lans v. DEC* occurred between 1997 and 2001—the exact window when the IMO and ITU were drafting AIS standards. This heightened institutional caution regarding patented algorithms, reinforcing demands for royalty waivers.

## 18.2 Standardization, IPR declarations, and the SOLAS compromise

As the Swedish Maritime Administration demonstrated the GP&C transponder during 1993–1994 trials on Lake Vänern and Gothenburg archipelago ferries, Sweden introduced the "4S" system to the IMO Navigation Sub-Committee (**NAV**). Maritime nations objected: SOLAS conventions cannot mandate that shipowners worldwide license a proprietary patent from a single vendor.

### 18.2.1 The Common Patent Policy of ITU-T/ITU-R/ISO/IEC

Standards bodies operate under the **Common Patent Policy for ITU-T/ITU-R/ISO/IEC**. Participants holding potential **Standard-Essential Patents** (**SEPs**) must file a *Patent Statement and Licensing Declaration* selecting one of three options:
- **Option 1 (Royalty-free):** Licenses negotiated royalty-free and non-discriminatorily for standard implementation.
- **Option 2 (FRAND / RAND):** Licenses negotiated on Fair, Reasonable, and Non-Discriminatory terms with reasonable royalties.
- **Option 3 (Refusal):** Unwilling to license under Options 1 or 2, compelling standards committees to engineer around the technology.

### 18.2.2 The 1998 SOLAS Class A royalty-free waiver

When the IMO Maritime Safety Committee evaluated AIS standards in 1998, delegates insisted that the Swedish proposal would be rejected unless Lans waived royalties. Lans accepted the ITU Code of Practice, formally waiving claims for compensation on **vessels subject to mandatory IMO carriage requirements**.

This concession unblocked adoption. On **12 May 1998**, the IMO adopted **Resolution MSC.74(69) Annex 3**. In **November 1998**, the ITU released **Recommendation ITU-R M.1371-0**, followed by revised SOLAS Chapter V (Resolution MSC.99(73)) in December 2000 mandating carriage under Regulation 19.2.4.

However, Lans's waiver was strictly limited to mandatory SOLAS commercial vessels (300 GT international, 500 GT domestic, and passenger ships). It did not cover non-SOLAS small commercial craft, recreational vessels, or fixed Aids to Navigation (**AtoN**), prompting standards committees to develop an alternative protocol for small craft.

## 18.3 The Class B dilemma: CSTDMA and the SRT controversy

By 2002, with Class A equipment costing upwards of US$5,000 to US$10,000, IEC Technical Committee 80 Working Group 15 (**IEC TC80/WG15**) began drafting **IEC 62287** for small craft. Because Lans's waiver excluded leisure vessels, standardizing SOTDMA would require recreational manufacturers to negotiate commercial licenses with GP&C.

### 18.3.1 Engineering around Lans: The Carrier-Sense (CSTDMA) protocol

To bypass Lans's patent, WG15 developed **Carrier-Sense Time-Division Multiple Access** (**CSTDMA**). Unlike SOTDMA, a CSTDMA transponder does not advertise future slot reservations. Instead, it synchronizes to the TDMA slot grid via GPS UTC, listens during a brief carrier-sense window prior to transmission, and broadcasts a 1-slot report (Message 18) only if the channel is idle. If occupied by a Class A transmission, it defers to an alternate slot, operating as a "polite guest" that never overwrites scheduled slots. CSTDMA was published in **IEC 62287-1** in 2006.

### 18.3.2 The Johnson & Lesch patent: US 7,512,095

The protocol engineered to escape Lans's patent was itself promptly patented. On **7 June 2003**, engineer Mark M. Johnson wrote to IEC TC80/WG15:

> "I will be proposing a non-SOTDMA lower cost Class B variant that is low in cost, very 'polite', and compatible with existing Class A AIS. I am quite confident that it avoids the IPR issues."

Two days later, on **9 June 2003**, Johnson and Andreas Lesch filed US Provisional Application **60/477,125**. Their non-provisional application (US 10/709,928) was granted on **31 March 2009** as **US Patent 7,512,095 B2**, titled *"Multiple access communication system for moveable objects"*. Claim 1 covered a listen-before-talk protocol on a time-slotted channel. Crucially, no patent declaration was ever filed for US 7,512,095 in the IEC database for IEC 62287-1.

### 18.3.3 The 2015 SRT acquisition and royalty assertions

In early 2015, **Software Radio Technology plc** (**SRT**), the dominant OEM supplier of AIS transponder modules, acquired rights to US 7,512,095 from co-inventor Lesch. In March 2015, SRT announced a licensing program on FRAND terms. As documented on *Panbo* by Ben Ellison, SRT proposed:
- A continuing royalty of **5% of net retail sales price** (~US$35 per unit on a US$700 Class B device).
- Retroactive royalties for the prior six years.
- Quarterly schedules through March 2019.

The industry reacted with hostility, arguing that asserting an undeclared patent against an open safety standard violated the spirit of standards development. Behind the scenes, manufacturers examined the prosecution file, and US 7,512,095 subsequently lapsed for failure to pay maintenance fees (*Expired - Fee Related* under 35 U.S.C. § 41(b)).

### 18.3.4 The emergence of Class B "SO" (SOTDMA Class B)

Following the 2010 cancellation of Lans's US claims and the 2012 expiry of EP 0 592 560, the patent barrier against using SOTDMA on small vessels dissolved. The IEC completed **IEC 62287-2**, enabling **Class B "SO"** (or **Class B+**) transponders. Operating at 5 watts, reserving slots via SOTDMA, and reporting every 5 seconds at high speed, Class B SO brought Class A performance to small craft free of patent encumbrances.

## 18.4 Modern patent landscape: Space, sensors, and analytics

With foundational link-layer patents expired or lapsed, modern patenting focuses on three domains:
1. **Space-Based AIS (Satellite Decollision and Signal Separation)**
2. **Specialized Emitter Hardware and Transceivers**
3. **Trajectory Analytics, Spoof Detection, and Dark-Vessel Surveillance**

### 18.4.1 Satellite-AIS decollision and processing patents

In Low Earth Orbit (**LEO**), a satellite footprint spans over 5,000 km, causing mutual packet collisions among thousands of overlapping VHF cells. Overcoming this collision challenge generated significant aerospace patents:
1. **COM DEV / exactEarth:** Established foundational patents covering successive interference cancellation (**SIC**), multi-channel decollision, and multi-beam field-of-view segmentation: **US 7,876,865 B2** (granted 2011; Peach), **US 8,780,788 B2** (2014; Peach), **EP 2 211 486 B1** (2013; Cowles), **CA 2,720,190 C** (2016; Chen), **US 9,094,048 B2** (2015; Randhawa), and **US 9,842,504 B2** (2017; Short).
2. **ORBCOMM:** Secured early system claims under **US Patent 7,809,370 B2** (granted 2010; Stolte) for space-based AIS maritime monitoring.
3. **CNES (French Space Agency):** Holds **US Patent 9,246,575 B2** (granted 2016; de Latour & Faup), titled *"Method for detecting AIS messages"*, which remains **Active** until **23 October 2033**.
4. **Harris Corporation (now L3Harris):** Developed hosted exactView RT payloads on Iridium NEXT, securing **US Patent 9,729,374 B2** (granted 2017; Dyson) for matched Doppler spatial separation.

Spire Global acquired exactEarth in 2021, and Kpler acquired Spire Maritime in April 2025 for ~US$241 million, consolidating COM DEV and exactEarth assets.

### 18.4.2 Transceiver and antenna hardware patents

- **SRT Marine Technology Ltd:** Holds **US Patent 9,473,197 B2** (granted 2016; Longhurst), titled *"Reversible TDD transceiver"*, claiming an RF architecture that rapidly alternates between transmit and receive states across dual VHF channels.
- **True Heading AB:** Holds **US 9,804,254 B2** and **US 9,807,554 B2** (granted 2017; Willart) for arrival-timing estimation in low-cost receivers.
- **Antenna Splitters:** Specialized patents cover zero-loss preamplifiers and fail-safe relays maintaining unpowered voice VHF connection during electrical blackouts.

### 18.4.3 Data analytics, plausibility verification, and spoof detection

- **Saab AB:** Holds **US 8,610,619 B2** and **EP 2 136 221 B1** (granted 2013; Andersson & Persson), verifying positions against time-of-arrival and TDMA propagation delays.
- **COM DEV / exactEarth:** Holds **US 9,015,567 B2** (granted 2015; Peach) for anomaly detection in AIS data streams.
- **Spire Global Subsidiary, Inc.:** Holds **US Patent 11,156,723 B2** (granted 2021; Platzer), claiming algorithms fusing satellite AIS feeds with RF characteristics and optical/SAR imagery to detect coordinate spoofing and intentional disabling.
- **eOdyn:** Filed **US 2016/0290812 A1** (Guichoux, 2013 priority) for calculating ocean surface currents from vessel drift vectors.

| Patent Number | Current Assignee / Owner | Subject Matter | Priority Date | Status (as of Oct 2026) |
|:---|:---|:---|:---|:---|
| **US 5,506,587 A** | GP&C Systems International | SOTDMA position reporting | 1 Jul 1991 | **Expired / Cancelled** (2010) |
| **EP 0 592 560 B1** | GP&C Systems International | SOTDMA position reporting | 1 Jul 1991 | **Expired** (29 Jun 2012) |
| **US 7,512,095 B2** | Software Radio Technology / Lesch | CSTDMA "listen-before-talk" | 9 Jun 2003 | **Lapsed** (Fee non-payment) |
| **US 7,809,370 B2** | ORBCOMM Inc. | Satellite-based AIS monitoring | 30 May 2006 | **Expired / Lifetime** |
| **US 7,876,865 B2** | Kpler (via exactEarth / Spire) | Satellite decollision / SIC | 8 Jun 2007 | **Active** (Exp. ~2027) |
| **US 8,610,619 B2** | Saab AB | Timing-based validity checks | 18 Jun 2008 | **Active** (Exp. ~2028) |
| **US 8,780,788 B2** | Kpler (via exactEarth / Spire) | Multi-channel decollision | 25 Sep 2009 | **Active** (Exp. ~2029) |
| **CA 2,720,190 C** | Kpler (via exactEarth / Spire) | FoV segmentation / multi-beam | 9 Jun 2010 | **Active** (Exp. ~2030) |
| **US 9,246,575 B2** | CNES (French Space Agency) | Satellite AIS message detection | 5 Sep 2011 | **Active** (Exp. 23 Oct 2033) |
| **US 9,015,567 B2** | Kpler (via exactEarth / Spire) | Anomaly detection / consistency | 12 Apr 2012 | **Active** (Exp. ~2032) |
| **US 9,473,197 B2** | SRT Marine Technology Ltd | Reversible TDD transceiver | 29 Jan 2013 | **Active** (Exp. ~2033) |
| **US 9,729,374 B2** | L3Harris Technologies | Matched Doppler separation | 7 Aug 2015 | **Active** (Exp. ~2035) |
| **US 11,156,723 B2**| Spire Global Subsidiary, Inc. | Spoof and dark-target detection | 4 Apr 2016 | **Active** (Exp. ~2036) |

> **Legal note.**
>
> **Freedom to Operate (FTO) and Algorithmic Implementation.**
>
> 1. **Public Standards vs. Proprietary Analytics:** Recommendation ITU-R M.1371 and the IEC 61993/62287 standards are open technical specifications. The core physical and link-layer protocols (SOTDMA, CSTDMA, GMSK modulation, HDLC framing) are unencumbered by active foundational patents.
> 2. **Satellite Decollision and Signal Processing:** Software engineers implementing signal-processing pipelines for LEO satellite receivers (such as successive interference cancellation, matched Doppler filtering, and multi-beam segmentation) must conduct Freedom to Operate (**FTO**) reviews against active portfolios held by Kpler, L3Harris, and CNES.
> 3. **Machine Learning and Anomaly Detection:** Physics-based track verification relies on public-domain mathematics. However, vendors deploying automated dark-vessel inference platforms or orbital RF-fused spoof-detection systems should evaluate the claims of Spire's US 11,156,723 and COM DEV's US 9,015,567.
> 4. **Disclaimer:** Nothing in this handbook constitutes formal legal counsel or an official patent non-infringement opinion. Organizations developing maritime software and hardware must consult registered patent attorneys in their operational jurisdictions.

## Then & now

How intellectual property, standards policies, and licensing battles shaped the evolution of maritime tracking:

- **1991** ⟨H⟩: Anders Håkan Lans files Swedish patent applications SE 9102034 (1 July) and SE 9103542 (28 November), establishing international priority for autonomous, geodetically synchronized time-divided position reporting.
- **1992** ⟨+⟩: GP&C Systems International files PCT application PCT/SE92/00485 on 29 June, initiating worldwide prosecution for the STDMA patent family.
- **1993** ⟨H⟩: Swedish national patent SE 468 452 B is published on 18 January; the Swedish Maritime Administration conducts operational STDMA transponder trials on Lake Vänern and Gothenburg archipelago ferries.
- **1996** ⟨+⟩: The USPTO grants US Patent 5,506,587 A ("Position indicating system") to Håkan Lans on 9 April.
- **1997** ⟨+⟩: The European Patent Office grants EP 0 592 560 B1 on 27 August, establishing patent rights across European maritime nations.
- **1998** ⟨H⟩: The IMO adopts Resolution MSC.74(69) Annex 3 on 12 May after Lans agrees to waive patent royalties for vessels subject to mandatory SOLAS carriage; the ITU publishes Recommendation ITU-R M.1371-0 in November.
- **2001** ⟨+⟩: The US Federal Circuit decides *Lans v. Digital Equipment Corp.*, 252 F.3d 1320, dismissing Lans's colour graphics patent suit for lack of standing and awarding attorney fees, creating intense institutional caution regarding patented standards.
- **2003** ⟨+⟩: IEC TC80/WG15 debates low-cost Class B access; Mark Johnson files US Provisional Application 60/477,125 on 9 June for "listen-before-talk" carrier-sense TDMA after proposing it to the working group as an IPR-free alternative.
- **2006** ⟨+⟩: The IEC publishes IEC 62287-1, standardizing Class B CSTDMA; ORBCOMM files US application 11/443,473 establishing priority for space-based AIS monitoring.
- **2007** ⟨+⟩: COM DEV files priority application US 60/942,889 on 8 June for satellite AIS decollision and successive interference cancellation.
- **2009** ⟨+⟩: The USPTO grants US Patent 7,512,095 B2 (Johnson & Lesch) covering carrier-sense mobile access.
- **2010** ⟨+⟩: On 30 March, the USPTO issues Reexamination Certificate 7428 for US Patent 5,506,587, cancelling all 13 claims; satellite-AIS testing begins with AISSat-1 and NORAIS on the ISS.
- **2012** ⟨+⟩: European patent EP 0 592 560 B1 reaches its statutory 20-year term limit and expires on 29 June across all European contracting states.
- **2013** ⟨+⟩: US Patent 5,506,587 reaches its statutory 17-year term limit from grant on 9 April; Saab AB is granted US Patent 8,610,619 for TDMA timing-based position validity verification.
- **2015** ⟨+⟩: Software Radio Technology (SRT) acquires an interest in US 7,512,095 and issues demands for 5% retail royalties on Class B transponders, triggering industry pushback; the patent subsequently lapses for failure to pay maintenance fees.
- **2016** ⟨+⟩: The Canadian Intellectual Property Office grants CA 2,720,190 C to COM DEV for field-of-view satellite antenna segmentation; CNES is granted US Patent 9,246,575 for satellite detection.
- **2021** ⟨+⟩: Spire Global is granted US Patent 11,156,723 B2 for satellite-derived spoofing and dark-target detection algorithms.
- **2025** ⟨+⟩: Kpler acquires Spire Maritime for approximately US$241 million, consolidating historical COM DEV, exactEarth, and Spire satellite-AIS intellectual property assets.
- **2026** ⟨+⟩: The ITU releases Recommendation ITU-R M.1371-6, maintaining the open, royalty-free VHF Data Link standard as maritime telemetry transitions toward the VHF Data Exchange System (**VDES**).

## Validation, uncertainty & data quality

In the analysis of patents, standards compliance, and intellectual property claims, analytical errors stem from inaccurate legal status records, failure to parse patent reexamination dockets, confusion over statutory expiration formulas, and misattribution of standard-essential claims.

### 18.5.1 The four primary sources of patent data error

1. **Reliance on Automated Expiration Estimates:** Public search engines compute "anticipated expiration" dates using automated heuristic algorithms. These scrapers frequently misapply pre-GATT 17-versus-20-year transition formulas, miscalculate Patent Term Adjustments (**PTA**) under 35 U.S.C. § 154(b), or overlook maintenance fee lapses under 35 U.S.C. § 41(b).
2. **Overlooking Post-Grant Proceedings:** A patent that appears "Active" on bibliographic search pages may have had its claims narrowed or extinguished in post-grant administrative proceedings, including *ex parte* reexaminations or PTAB reviews. Bibliographic summaries often fail to flag that all claims of Lans's US 5,506,587 were formally cancelled in Reexamination Certificate 7428.
3. **Conflating Patent Specifications with Standard Requirements:** Marketing literature frequently claims that a product is "patented" or that a standard "requires" a patented method. A patent's legal monopoly is defined strictly by the numbered **claims**. Analysts must perform claim element mapping to determine whether an asserted patent is truly a Standard-Essential Patent (**SEP**) or merely an implementation option.
4. **Corporate Assignment and Entity Tracking Failures:** Maritime tech firms frequently merge or assign patents to shell entities. Tracking legal ownership of legacy portfolios (e.g., GP&C, Saab TransponderTech, SRT Marine Technology, COM DEV, exactEarth, Spire Global, Kpler) requires querying authoritative title assignment registers.

### 18.5.2 Systematic patent verification procedure

To audit a patent asserted against maritime hardware or software, engineers and compliance teams must follow a rigorous four-stage verification protocol:

1. **Step 1: Authoritative Register Lookup:** Query primary government databases—**USPTO Patent Center** for US patents, **EPO Espacenet** for European filings, and **WIPO Patentscope** for PCT applications. Confirm precise priority filings, PCT filing dates, and national stage entry dates.
2. **Step 2: Maintenance Fee and Legal Status Audit:** Query the **USPTO Patent Maintenance Fees Storefront**. Verify whether maintenance fee payments were timely made at the three statutory windows: 3.5 years, 7.5 years, and 11.5 years post-grant. If unpaid, determine whether the patent lapsed.
3. **Step 3: Post-Grant Docket Inspection:** Review prosecution history and file wrappers for terminal disclaimers, *ex parte* reexaminations, reissues, or PTAB trials, checking for issued certificates of cancellation.
4. **Step 4: Standards Declaration Cross-Referencing:** Query patent declaration databases maintained by ITU-R and IEC:
   - For ITU-R recommendations (e.g., M.1371), search the *ITU-R Patent Statement and Licensing Declaration Information* database.
   - For IEC standards (e.g., IEC 61993, IEC 62287), query the *IEC Patent Declarations* portal under TC 80.
   - Verify whether the patent holder submitted an Option 1 (Royalty-free) or Option 2 (FRAND) statement, or if the patent was unannounced.

> **Try it.**
>
> **Auditing Patent Expiration and Maintenance Status in Python.**
>
> Using Python's standard library, calculate exact post-GATT statutory patent terms, maintenance fee payment windows, and evaluate fee status:
>
> ```python
> import datetime
> 
> def calculate_us_patent_term(filing_date_str, grant_date_str, pta_days=0):
>     filing_date = datetime.date.fromisoformat(filing_date_str)
>     grant_date = datetime.date.fromisoformat(grant_date_str)
>     gatt_cutoff = datetime.date(1995, 6, 8)
>     
>     if filing_date < gatt_cutoff:
>         term_grant = grant_date.replace(year=grant_date.year + 17)
>         term_filing = filing_date.replace(year=filing_date.year + 20)
>         nominal_expiry = max(term_grant, term_filing)
>         regime = "Pre-GATT (35 U.S.C. 154(c)(1))"
>     else:
>         base_expiry = filing_date.replace(year=filing_date.year + 20)
>         nominal_expiry = base_expiry + datetime.timedelta(days=pta_days)
>         regime = "Post-GATT (35 U.S.C. 154(a)(2))"
>         
>     fee_windows = {
>         "Window 1 (3.5 yr)": grant_date + datetime.timedelta(days=int(3.5 * 365.25)),
>         "Window 2 (7.5 yr)": grant_date + datetime.timedelta(days=int(7.5 * 365.25)),
>         "Window 3 (11.5 yr)": grant_date + datetime.timedelta(days=int(11.5 * 365.25)),
>     }
>     return {"Regime": regime, "Nominal Expiry": nominal_expiry.isoformat(), "Fee Windows": {k: v.isoformat() for k, v in fee_windows.items()}}
> 
> # Audit Håkan Lans foundational US patent 5,506,587
> lans_audit = calculate_us_patent_term("1992-06-29", "1996-04-09", pta_days=0)
> print("US 5,506,587 (Lans STDMA):")
> print(f"  Regime: {lans_audit['Regime']}")
> print(f"  Statutory Expiry: {lans_audit['Nominal Expiry']}")
> 
> # Audit Johnson & Lesch CSTDMA US patent 7,512,095
> cstdma_audit = calculate_us_patent_term("2004-06-07", "2009-03-31", pta_days=0)
> print("\nUS 7,512,095 (Johnson CSTDMA):")
> print(f"  Regime: {cstdma_audit['Regime']}")
> print(f"  Statutory Expiry: {cstdma_audit['Nominal Expiry']}")
> print(f"  Maintenance Fee Due 1: {cstdma_audit['Fee Windows']['Window 1 (3.5 yr)']}")
> ```
>
> Expected output:
> ```text
> US 5,506,587 (Lans STDMA):
>   Regime: Pre-GATT (35 U.S.C. 154(c)(1))
>   Statutory Expiry: 2013-04-09
> 
> US 7,512,095 (Johnson CSTDMA):
>   Regime: Post-GATT (35 U.S.C. 154(a)(2))
>   Statutory Expiry: 2024-06-07
>   Maintenance Fee Due 1: 2012-09-29
> ```

## Software

The software tools, databases, and search interfaces utilized to analyze patent filings, track standards declarations, and assess freedom-to-operate in maritime tracking:

- **Open source:**
  - `python-docx` / `pdfplumber` (Python): Scriptable document parsing libraries used to extract and search claim language, specification disclosures, and prosecution histories from downloaded patent PDFs and PTO office actions. Caveat: does not parse complex embedded chemical or circuit diagrams.
  - `libais` (C++ with Python bindings): Open-source AIS decoding library implementing standard ITU-R M.1371 message parsers. Caveat: contains no analytical patent-checking or IP filtering modules; users must independently verify licensing for downstream proprietary derivatives.
  - `pyais` (Python): Pure-Python AIS message decoder and generator. Caveat: implements open ITU standards without checking whether specific binary application payloads (ASMs) infringe regional utility patents.
- **Free but closed:**
  - **USPTO Patent Center** (United States Patent and Trademark Office): Definitive United States public registry providing complete file wrappers, prosecution histories, maintenance fee payment ledgers, and reexamination certificates. Caveat: bulk downloading requires navigating API rate limits.
  - **EPO Espacenet** (European Patent Office): Global patent database containing over 140 million patent documents with comprehensive DOCDB family tracking and legal event timelines. Caveat: legal status updates from non-EPO partner nations can lag by several months.
  - **WIPO Patentscope** (World Intellectual Property Organization): Primary portal for searching international PCT applications, national phase entry records, and global IPR declaration histories. Caveat: user interface requires complex boolean queries for multi-jurisdiction cross-referencing.
  - **Google Patents**: High-speed text-search interface covering USPTO, EPO, WIPO, and national patent offices, with automated prior art citations and machine translation. Caveat: legal status indicators and expiration projections are computed heuristics that frequently omit reexamination outcomes or maintenance fee lapses.
- **Commercial:**
  - **Clarivate Derwent Innovation**: Commercial patent intelligence platform providing editorially normalized patent titles, indexed abstracts, and verified litigation/reexamination histories. Caveat: expensive annual subscription required; optimized for corporate IP departments.
  - **LexisNexis PatentSight**: Business analytics suite mapping patent portfolios against technological benchmarks and corporate ownership structures. Caveat: high enterprise cost; requires proprietary training for custom query construction.

## Standards & guides

The official institutional policies, standards guidelines, and formal specifications governing intellectual property in maritime tracking:

- **International Telecommunication Union / International Organization for Standardization / International Electrotechnical Commission**, *Common Patent Policy for ITU-T/ITU-R/ISO/IEC* (current edition applicable 2022). Governs patent disclosure obligations and the three-option declaration regime (Royalty-free, FRAND, Refusal).
- **International Telecommunication Union**, *Guidelines for the Implementation of the Common Patent Policy for ITU-T/ITU-R/ISO/IEC* (2022). Detailed administrative procedures for filing, recording, and resolving patent declarations.
- **International Telecommunication Union**, *Patent Statement and Licensing Declaration Form for ITU-T or ITU-R Recommendation | ISO or IEC Deliverable* (2018). Official standardized declaration submission instrument.
- **International Telecommunication Union**, *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band*, Recommendation ITU-R M.1371 (editions M.1371-0 through M.1371-6, 1998–2026). Specifies universal SOTDMA and CSTDMA protocols.
- **International Maritime Organization**, Resolution MSC.74(69), Annex 3 (1998). *Recommendation on Performance Standards for a Universal Shipborne Automatic Identification System (AIS)*. Governs SOLAS carriage compatibility.
- **International Electrotechnical Commission**, Standard IEC 61993-2 (Ed. 1, 2001; Ed. 2, 2012; Ed. 3, 2018). *Maritime navigation and radiocommunication equipment and systems — Automatic identification systems (AIS) — Part 2: Class A shipborne equipment of the automatic identification system (AIS)*.
- **International Electrotechnical Commission**, Standard IEC 62287-1 (Ed. 1, 2006; Ed. 2, 2017). *Maritime navigation and radiocommunication equipment and systems — Class B shipborne equipment of the automatic identification system (AIS) — Part 1: Carrier-sense time division multiple access (CSTDMA) techniques*.
- **International Electrotechnical Commission**, Standard IEC 62287-2 (Ed. 1, 2013; Ed. 2, 2017). *Maritime navigation and radiocommunication equipment and systems — Class B shipborne equipment of the automatic identification system (AIS) — Part 2: Self-organising time division multiple access (SOTDMA) techniques*.
- **United States Patent and Trademark Office**, *Manual of Patent Examining Procedure (MPEP)*, Ninth Edition. Governs pre-GATT and post-GATT patent term calculations (35 U.S.C. § 154) and maintenance fee payments (35 U.S.C. § 41).

## Pitfalls

The operational mistakes, legal misunderstandings, and engineering assumptions encountered when evaluating intellectual property in AIS:

- **Assuming an active patent on Google Patents is legally enforceable** $\to$ Accepting a search engine's "Active" flag without checking file wrappers $\to$ Patents often lapse mid-term due to failure to pay required maintenance fees under 35 U.S.C. § 41(b), or have their claims cancelled in reexamination (as occurred with US 5,506,587 in 2010); always verify status in the USPTO Patent Maintenance Fees Storefront.
- **Confusing patent specifications with actual claim scope** $\to$ Reading the background or description of a patent and assuming the patentee owns the entire concept $\to$ A patent's legal monopoly is defined strictly by the numbered claims at the end of the document; broad narrative statements in the specification do not prevent competitors from practicing unclaimed concepts.
- **Believing Håkan Lans lost his STDMA patent in court** $\to$ Repeating the myth that Lans's navigation patent was defeated in a United States infringement trial $\to$ The famous defeat in *Lans v. Digital Equipment Corp.* (2001) concerned his unrelated colour graphics display patent (US 4,303,986) on procedural standing; the STDMA patent claims were cancelled years later in an administrative USPTO reexamination.
- **Assuming the 1998 SOLAS royalty waiver applied to all AIS devices** $\to$ Assuming manufacturers could build Class B transponders or base stations without patent considerations $\to$ Lans's formal waiver applied strictly to vessels subject to the IMO's mandatory carriage requirements (SOLAS commercial ships); non-mandated small craft, recreational boats, and AtoNs were not covered, which directly motivated the creation of CSTDMA ([Chapter 20](ch20-architecture-and-station-classes.md)).
- **Relying on foreign patent expiration dates for United States filings** $\to$ Assuming that because EP 0 592 560 expired in June 2012, US 5,506,587 also expired on that date $\to$ Because US 5,506,587 was filed prior to 8 June 1995, its statutory lifetime ran for 17 years from its 1996 grant date (until 9 April 2013), outliving its European counterpart by nearly ten months.
- **Believing CSTDMA was completely free of patent claims** $\to$ Designing Class B hardware assuming carrier-sense TDMA had no intellectual property encumbrances $\to$ The inventors of CSTDMA filed US Patent 7,512,095 two days after proposing it to IEC WG15; SRT acquired rights in 2015 and demanded 5% retail royalties before the patent subsequently lapsed.
- **Assuming open-source decoders protect against analytics patent infringement** $\to$ Believing that using MIT- or Apache-licensed decoding libraries shields a data analytics platform from infringement $\to$ Open-source software licenses grant rights only to the underlying copyrighted source code; they provide no immunity against utility patents that cover downstream analytical processes, such as satellite decollision (Kpler) or dark-target detection (Spire).
- **Ignoring regional patent jurisdictional boundaries** $\to$ Assuming a United States patent prevents hardware manufacturing in Europe or Asia $\to$ Patent rights are strictly territorial; a US patent can only be infringed by making, using, offering for sale, selling, or importing the claimed invention within the United States.
- **Failing to track patent ownership changes after corporate acquisitions** $\to$ Directing licensing inquiries or infringement analyses to defunct corporate entities $\to$ The satellite-AIS patent landscape underwent successive waves of consolidation (COM DEV $\to$ exactEarth $\to$ Spire $\to$ Kpler); always verify current recorded assignments via official patent office registers.
- **Assuming published international standards guarantee freedom to operate** $\to$ Deploying a system strictly compliant with an ITU-R or IEC standard under the assumption that standards bodies clear all IP $\to$ Standards organizations do not guarantee that recommendations are patent-free; they rely on voluntary disclosure statements, and non-participating third parties may assert undeclared patents against standard-compliant hardware.

## Key takeaways

- **The Foundations Were Patented:** The core SOTDMA protocol that enables autonomous, decentralized vessel tracking was invented and patented by Swedish inventor Håkan Lans and GP&C Systems International (priority July 1991, US Patent 5,506,587).
- **Compromise Saved Universal AIS:** Universal adoption under SOLAS was achieved in 1998 only after Lans agreed to waive patent royalties for merchant vessels subject to mandatory IMO carriage requirements, avoiding a global standards deadlock.
- **Class B Was Built to Evade IP:** Carrier-Sense TDMA (CSTDMA) in IEC 62287-1 was deliberately engineered to avoid Lans's SOTDMA patents for small craft, but was itself patented by its proposers (US Patent 7,512,095) and later asserted by SRT in 2015.
- **Lans's US Patent Was Cancelled:** US Patent 5,506,587 did not survive to its April 2013 statutory expiration; all 13 claims were formally cancelled by the USPTO in Reexamination Certificate 7428 issued on 30 March 2010.
- **The Standing Lesson of *Lans v. DEC*:** Lans's famous legal defeat in 2001 involved his unrelated colour graphics patent (US 4,303,986) and turned entirely on civil procedure: assigning the patent to his corporation stripped him of individual standing to sue.
- **The Core VHF Link Is Now Public Domain:** All foundational patents covering Class A SOTDMA, Class B CSTDMA, GMSK modulation, and HDLC framing have expired, lapsed, or been cancelled, ensuring the physical and link-layer protocol remains open to all developers.
- **Class B SO Emerged Post-Expiry:** Once the Lans patent encumbrance disappeared, the IEC completed IEC 62287-2, allowing recreational and small commercial craft to utilize high-performance SOTDMA transponders without licensing risks.
- **Space-Based AIS Drove New Patenting:** Overcoming the severe message-collision challenge in Low Earth Orbit generated dense patent families covering decollision, successive interference cancellation, and Doppler separation held by Kpler, L3Harris, and CNES.
- **Analytics Represent the Modern IP Frontier:** Commercial patenting today concentrates on automated surveillance, trajectory plausibility checking (Saab), and satellite-fused dark-vessel/spoof detection algorithms (Spire).
- **Rigorous Auditing Requires Authoritative Records:** Web search summaries and commercial databases frequently misstate expiration dates, miss administrative cancellations, and overlook maintenance fee lapses; reliable verification requires querying primary PTO file wrappers.

## References

- European Patent Office (1997). *Position indicating system*. European Patent Specification EP 0 592 560 B1. Munich: EPO.
- European Patent Office (2013). *Satellite detection of automatic identification system signals*. European Patent Specification EP 2 211 486 B1. Munich: EPO.
- European Patent Office (2013). *Validity check of vehicle position information*. European Patent Specification EP 2 136 221 B1. Munich: EPO.
- International Electrotechnical Commission (2001). *Maritime navigation and radiocommunication equipment and systems — Automatic identification systems (AIS) — Part 2: Class A shipborne equipment of the automatic identification system (AIS) — Operational and performance requirements, methods of testing and required test results*. Standard IEC 61993-2, Edition 1.0. Geneva: IEC.
- International Electrotechnical Commission (2006). *Maritime navigation and radiocommunication equipment and systems — Class B shipborne equipment of the automatic identification system (AIS) — Part 1: Carrier-sense time division multiple access (CSTDMA) techniques*. Standard IEC 62287-1, Edition 1.0. Geneva: IEC.
- International Electrotechnical Commission (2013). *Maritime navigation and radiocommunication equipment and systems — Class B shipborne equipment of the automatic identification system (AIS) — Part 2: Self-organising time division multiple access (SOTDMA) techniques*. Standard IEC 62287-2, Edition 1.0. Geneva: IEC.
- International Maritime Organization (1998). *Recommendation on Performance Standards for an Universal Shipborne Automatic Identification System (AIS)*. Resolution MSC.74(69), Annex 3. London: IMO.
- International Maritime Organization (2000). *Amendments to the International Convention for the Safety of Life at Sea, 1974 (Revised SOLAS Chapter V)*. Resolution MSC.99(73). London: IMO.
- International Telecommunication Union (1998). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band*. Recommendation ITU-R M.1371-0. Geneva: ITU.
- International Telecommunication Union (2014). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band*. Recommendation ITU-R M.1371-5. Geneva: ITU.
- International Telecommunication Union (2026). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band*. Recommendation ITU-R M.1371-6. Geneva: ITU.
- International Telecommunication Union, International Organization for Standardization, and International Electrotechnical Commission (2022). *Common Patent Policy for ITU-T/ITU-R/ISO/IEC*. Geneva: ITU.
- Lans v. Digital Equipment Corp. (2001). *Anders Håkan Lans v. Digital Equipment Corporation et al.*, 252 F.3d 1320 (Fed. Cir. 2001).
- Swedish Maritime Administration (2018). *AIS — How a Swedish innovation became a global standard*. Norrköping: Sjöfartsverket.
- United States Patent and Trademark Office (1981). *Data processing system and apparatus for producing images of objects on a color video display*. US Patent 4,303,986. Washington, DC: USPTO.
- United States Patent and Trademark Office (1996). *Position indicating system*. US Patent 5,506,587. Washington, DC: USPTO.
- United States Patent and Trademark Office (2009). *Multiple access communication system for moveable objects*. US Patent 7,512,095 B2. Washington, DC: USPTO.
- United States Patent and Trademark Office (2010). *Ex Parte Reexamination Certificate 7428 for US Patent 5,506,587*. Washington, DC: USPTO.
- United States Patent and Trademark Office (2010). *Space based monitoring of global maritime shipping using automatic identification system*. US Patent 7,809,370 B2. Washington, DC: USPTO.
- United States Patent and Trademark Office (2011). *System and method for decoding automatic identification system signals*. US Patent 7,876,865 B2. Washington, DC: USPTO.
- United States Patent and Trademark Office (2013). *Validity check of vehicle position information*. US Patent 8,610,619 B2. Washington, DC: USPTO.
- United States Patent and Trademark Office (2014). *Systems and methods for decoding automatic identification system signals*. US Patent 8,780,788 B2. Washington, DC: USPTO.
- United States Patent and Trademark Office (2015). *Methods and systems for consistency checking and anomaly detection in automatic identification system signals*. US Patent 9,015,567 B2. Washington, DC: USPTO.
- United States Patent and Trademark Office (2015). *Methods and systems for enhanced detection of e-Navigation messages*. US Patent 9,094,048 B2. Washington, DC: USPTO.
- United States Patent and Trademark Office (2016). *Method for detecting AIS messages*. US Patent 9,246,575 B2. Washington, DC: USPTO.
- United States Patent and Trademark Office (2016). *Reversible TDD transceiver*. US Patent 9,473,197 B2. Washington, DC: USPTO.
- United States Patent and Trademark Office (2017). *Co-channel spatial separation using matched Doppler filtering*. US Patent 9,729,374 B2. Washington, DC: USPTO.
- United States Patent and Trademark Office (2017). *Systems and methods for vessel position reporting and monitoring*. US Patent 9,842,504 B2. Washington, DC: USPTO.
- United States Patent and Trademark Office (2021). *AIS spoofing and dark-target detection methodology*. US Patent 11,156,723 B2. Washington, DC: USPTO.
- World Intellectual Property Organization (1993). *Position indicating system*. International Patent Publication WO 1993/001576 A1. Geneva: WIPO.
