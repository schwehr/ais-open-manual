# Chapter 12 — 2015–present and the near future

> **Part II — History.** The second decade and beyond: how AIS expanded down to domestic workboats, scaled to global orbit, confronted pervasive electronic warfare, and laid the foundations for VDES and S-100.

**In this chapter.** You will learn how the Automatic Identification System transitioned from coastal compliance into a ubiquitous global sensor network, an instrument of sanctions, and a contested RF environment between 2015 and the present day. We trace the expansion of domestic carriage mandates, led by the US Coast Guard 2015/2016 rulemaking under 33 CFR 164.46 that brought thousands of tugs and fishing vessels onto the VHF Data Link. We examine how open transparency platforms like Global Fishing Watch revolutionized fisheries oversight, while corporate consolidation merged crowdsourced networks into commodity intelligence giants. You will analyze the vulnerabilities that emerged as GNSS spoofing, circle-spoofing, and jamming spread across commercial waterways. Finally, you will explore the architecture of the near future: the VHF Data Exchange System (VDES) under ITU-R M.2092 and IMO MSC 111, the transition to S-100 electronic charting, and the deployment of terrestrial R-Mode backups.

## 12.1 The regulatory second wave: expanding down-market

By 2015, the international carriage mandate under Chapter V of the International Convention for the Safety of Life at Sea (**SOLAS**) was mature. Large commercial tonnage—passenger ships, cargo vessels $\ge 500$ gross tonnage (**GT**) on domestic voyages, and craft $\ge 300\text{ GT}$ on international voyages—had operated Class A transponders for over a decade. However, these vessels shared crowded littoral channels with untracked workboats, tugs, and fishing craft.

To close this safety gap, national administrations initiated a second regulatory wave mandating transponders on commercial small craft.

### 12.1.1 The US Coast Guard 2015/2016 rulemaking (33 CFR 164.46)

In the United States, domestic carriage was authorized under the Maritime Transportation Security Act of 2002 (**MTSA**). Following initial interim rules that addressed only SOLAS vessels and select craft in Vessel Traffic Service (**VTS**) areas (68 FR 39353, 2003), the United States Coast Guard (**USCG**) published its comprehensive final rule on 30 January 2015: *Vessel Requirements for Notices of Arrival and Departure, and Automatic Identification System* (80 FR 5282).

Codified at **33 CFR 164.46**, the rule expanded mandatory carriage to:
- Self-propelled commercial vessels $\ge 65\text{ ft}$ (approximately 19.8 m) in length;
- Towing vessels $\ge 26\text{ ft}$ (approximately 7.9 m) and more than 600 horsepower;
- Passenger vessels certificated to carry more than 150 passengers;
- Dredges or floating plants operating in or near commercial channels;
- Vessels moving certain dangerous cargoes (**CDC**).

Crucially, the 2015 rule ended the statutory exemption for commercial fishing vessels $\ge 65\text{ ft}$. While general sections took effect 2 March 2015, the carriage mandates under 33 CFR 164.46(b) and (c) were delayed pending OMB approval, taking formal effect 7 April 2016 with an operational compliance date of **1 March 2016**.

The USCG permitted a bifurcated standard:
1. **Class A transponders:** Required on international voyages, within VTS monitoring areas, or carrying $>150$ passengers.
2. **Class B transponders:** Permitted on domestic workboats, dredges, and fishing vessels outside VTS areas.

This rule expanded North American **VHF Data Link** (**VDL**) traffic, adding tens of thousands of workboats to Message 1, 2, 3, 18, and 24 broadcasts.

### 12.1.2 European and international small-craft mandates

A parallel expansion occurred internationally. Under European Union Regulation (EC) No 1224/2009, Article 10 phased in mandatory AIS for fishing vessels $>15\text{ m}$ length overall (**LOA**) between 2012 and 2014, fully populating European Vessel Monitoring Systems (**VMS**) by 2015.

Simultaneously, the Central Commission for the Navigation of the Rhine (**CCNR**) and the European Committee for Drawing Up Standards in the Field of Inland Navigation (**CESNI**) mandated **Inland AIS** on European rivers. Inland AIS units broadcast specialized Blue Sign meeting status, convoy dimensions, and European Vessel Identification Numbers (**ENI**).

In developing nations, small-craft tracking expanded under fisheries management programs to curb Illegal, Unreported, and Unregulated (**IUU**) fishing, using Class B transponders across coastal fleets.

## 12.2 Transparency and civil oversight: the open-data revolution

Before 2015, maritime tracking was primarily controlled by coast guards, navies, and commercial shipbroker networks. Between 2015 and 2020, civil society and researchers demonstrated that open broadcast telemetry could be transformed into transparent, global environmental and compliance monitoring.

### 12.2.1 Global Fishing Watch and machine-learning oversight

The primary catalyst for open maritime oversight was the launch of **Global Fishing Watch** (**GFW**) on 15 September 2016 at the *Our Ocean* conference in Washington, DC. Founded by Oceana, SkyTruth, and Google, GFW became an independent non-profit in 2017.

GFW paired massive streams of satellite and terrestrial AIS data with scalable cloud computing and convolutional neural networks (**CNNs**). Ingesting billions of AIS positions, researchers trained algorithms to identify vessel maneuvers that distinguish active longlining, purse seining, or trawling from simple transit (Kroodsma et al. 2018).

Their landmark 2018 *Science* study mapped over 40 million hours of fishing effort, revealing that commercial fleets covered over 55 percent of ocean surface area.

Civil AIS tracking altered maritime environmental oversight:
- **Marine Protected Area (MPA) monitoring:** Detecting industrial intrusions within reserves such as the Galápagos and Papahānaumokuākea.
- **Transshipment at sea:** Identifying rendezvous between fishing vessels and refrigerated cargo ships ("reefers") to expose catch laundering and labor abuses (Miller et al. 2018).
- **Sanctions enforcement:** Revealing illicit North Korean coal exports and ship-to-ship crude oil transfers.

### 12.2.2 The "dark fleet" and optical/SAR cross-sensor fusion

The spread of public tracking led illicit actors to intentionally disable their transponders when entering sensitive zones (Welch et al. 2022).

To detect these "dark vessels", researchers fused AIS feeds with non-cooperative earth observation sensors:
1. **Synthetic Aperture Radar (SAR):** Radar satellites (Sentinel-1, ICEYE) detect vessel hulls through cloud and night by measuring radar cross-section (**RCS**).
2. **Optical and Night-Light Imaging:** High-resolution optical sensors and the Visible Infrared Imaging Radiometer Suite (**VIIRS**) capture ship silhouettes and nighttime deck illumination.

In *Nature*, Paolo et al. (2024) synthesized global AIS, Sentinel-1 SAR, and optical data from 2017 to 2021. They established that approximately 75 percent of industrial fishing vessels and 25 percent of transport/energy vessels were unobserved on public AIS due to regulatory thresholds, reception gaps, or deliberate switch-offs.

> **Case file.** The *Courageous* (MMSI 312151000 / IMO 8617524). Between August and December 2019, the tanker *Courageous* conducted illicit ship-to-ship transfers of petroleum to North Korean vessels, violating UN sanctions. During these operations, the vessel disabled its AIS transponder, creating multi-day tracking gaps. However, commercial satellite imagery captured the tanker transferring oil to the North Korean vessel *Saebyol* while dark. In April 2021, Cambodian authorities seized the *Courageous* at US request, and the US District Court for the Southern District of New York entered a civil forfeiture judgment in July 2021, citing the correlated AIS gaps and satellite imagery as decisive forensic evidence.

## 12.3 Corporate consolidation: from enthusiasts to intelligence cartels

Online AIS tracking originated as a decentralized volunteer movement. Hobbyists, coastal residents, and universities deployed VHF receivers streaming NMEA sentences to crowdsourced platforms like **MarineTraffic** (founded in 2007 by Dimitris Lekkas) and **AISHub**.

Between 2020 and 2025, commercial energy and financial sectors recognized vessel tracking as crucial for supply-chain logistics and economic nowcasting. This triggered private-equity consolidation that absorbed the open aggregator network.

### 12.3.1 The acquisition roll-up

Key acquisitions centralized global collection infrastructure:
- **Garmin / Vesper Marine (January 2022):** Garmin acquired Vesper Marine, absorbing its Cortex VHF/AIS and vessel-monitoring systems.
- **Spire Global / exactEarth (November 2021):** Spire acquired exactEarth for ~$161 million, unifying its Lemur nanosatellite constellation with exactView RT payloads hosted aboard 66 Iridium NEXT satellites.
- **Kpler / MarineTraffic and FleetMon (February 2023):** Commodities intelligence provider Kpler acquired both MarineTraffic and FleetMon, bringing the major crowdsourced terrestrial networks under single corporate ownership.
- **Kpler / Spire Maritime (November 2024 / April 2025):** Kpler agreed to acquire Spire's maritime business for ~$241 million ($233.5 million cash purchase price plus service agreements). Closing on 25 April 2025, the transaction combined the premier terrestrial network with a leading satellite constellation under one firm, triggering UK Competition and Markets Authority (**CMA**) review.

This roll-up restricted free academic APIs, tightened data redistribution licenses, and transitioned users toward commercial JSON feeds.

### 12.3.2 The China terrestrial feed blackout (November 2021)

Centralized commercial pipelines proved fragile when national regulatory barriers intervened.

On 1 September 2021, China enacted the **Data Security Law** (**DSL**), followed on 1 November 2021 by the **Personal Information Protection Law** (**PIPL**). These laws restricted cross-border transmission of economic and security-sensitive data. Chinese state media cautioned citizens against operating foreign-supplied listening stations, portraying volunteer AIS receivers as security vulnerabilities.

In early November 2021, domestic receiver operators and data hosts disconnected feeds to foreign aggregators:
- Terrestrial AIS message volume from Chinese waters fell sharply, with estimates indicating a 45 to 90 percent decline across commercial platforms (Reuters 2021).
- Key export hubs including Shenzhen and Ningbo-Zhoushan lost real-time terrestrial coverage. While satellite passes continued to detect Class A broadcasts offshore, terrestrial port monitoring went dark during a peak global supply-chain disruption.

Crucially, **the VHF broadcasts on the water never ceased.** Vessels continued transmitting standard M.1371 packets, and local navigation was undisturbed. However, remote data consumers learned that aggregated commercial feeds remain vulnerable to sovereign legal barriers.

## 12.4 The contested spectrum: GNSS interference in commercial shipping

The original 1998 AIS protocol assumed an uncontested radio spectrum where transponders trusted their **Electronic Position Fixing System** (**EPFS**) implicitly. Class A units take coordinates, Course Over Ground (**COG**), and Speed Over Ground (**SOG**) from sensor buses, encode the 168-bit payload, and broadcast the packet.

After 2017, this implicit trust was undermined as military electronic warfare expanded across commercial waterways.

### 12.4.1 Black Sea and Novorossiysk (2017)

The first widespread commercial manifestation of deliberate GNSS spoofing occurred in June 2017 near the Russian Black Sea port of Novorossiysk. Over twenty commercial vessels found their GPS receivers reporting positions at Gelendzhik Airport, roughly 32 km (17 nmi) inland (MARAD 2017).

Bridge ECDIS displays triggered grounding alarms, autopilots attempted sudden turns, and AIS transponders broadcast the falsified airport coordinates over the air. US MARAD published Maritime Advisory 2017-005A, warning mariners of unverified GPS positioning in the region.

### 12.4.2 Circle-spoofing in Shanghai (2019)

In 2019, researchers detected a distinct spoofing phenomenon on the Huangpu River and Port of Shanghai.

Rather than jumping to a distant airport, vessel GPS positions tracked synchronized, circular paths on navigation displays (Bencsath et al. 2020; Bergman 2019). Ground-based spoofers manipulated GPS pseudoranges to conceal illicit sand dredgers and oil smugglers from maritime authorities. Transponders faithfully accepted these positions, injecting corrupted circular tracks into international tracking databases.

### 12.4.3 Baltic, Black, and Red Seas (2022–present)

Following the 2022 invasion of Ukraine and Red Sea escalations, GNSS electronic warfare became an enduring operating reality:
- **The Baltic Sea:** Vessels near Kaliningrad and the Gulf of Finland face persistent GPS jamming and spoofing, with transponders defaulting to sentinel time stamps 61–63 or reporting false coordinates inside Russia (Androjna et al. 2021).
- **The Black Sea:** Commercial grain carriers encounter continuous spoofing intended to disrupt aerial drones.
- **The Southern Red Sea and Gulf of Aden (2023–present):** Active anti-ship missile attacks and naval countermeasures blanked out GPS and VHF frequencies, leading crews to deactivate AIS for operational defense.

> **Threat model.** Spoofed kinematic broadcast.
> - **Attacker:** Regional military actor or illicit vessel operator using an SDR and power amplifier.
> - **Capability:** Overpowering GPS L1 signals (1575.42 MHz) across 10 to 50 km, broadcasting false pseudoranges that force shipboard receivers to calculate a false position.
> - **Impact:** The Class A transponder broadcasts false coordinates in Messages 1–3, misleading nearby vessels, confusing shore VTS, and triggering false collision warnings.
> - **Mitigation:** Kinematic plausibility filtering (implied speed, acceleration, turn rate); cross-sensor verification against marine radar and visual sightings; dual-antenna GNSS heading checks; and terrestrial radionavigation backups.

> **Legal note.** AIS deactivation rules.
> Under SOLAS Chapter V Regulation 19.2.4, AIS must operate continuously at sea. However, IMO Resolution **A.1106(29)**, paragraph 22, authorizes an explicit exception:
> > "If the master believes that the continual operation of AIS might compromise the safety or security of his/her ship, or where security incidents are imminent, the AIS may be switched off."
> The master must log the deactivation reason in the ship's logbook and notify the competent coastal administration. Deactivation in war-risk zones is a recognized defensive measure; disabling AIS to evade customs, bypass sanctions, or fish illegally violates international maritime law.

## 12.5 Modernizing the foundation: standards and institutions

As AIS entered its third decade, governing bodies updated its foundational standards.

### 12.5.1 IALA becomes an Intergovernmental Organization (2024)

Founded in 1957 as a French non-governmental association, the International Association of Marine Aids to Navigation and Lighthouse Authorities (**IALA**) authored key technical guidance for aids to navigation and VTS. However, it lacked the formal treaty status of bodies like the IMO or IHO.

Member states negotiated the *Convention on the International Organization for Marine Aids to Navigation*. On **22 August 2024**, the treaty entered into force upon securing thirty ratifications (IALA 2024).

IALA transitioned into a formal **Intergovernmental Organization** (**IGO**), named the *International Organization for Marine Aids to Navigation* (retaining the IALA acronym). Its first IGO General Assembly convened in Singapore in February 2025, providing treaty-level authority to coordinate e-Navigation, VDES spectrum, and digital standards.

### 12.5.2 Updated operational guidance: IMO Resolution A.1106(29)

In December 2015, the IMO Assembly adopted **Resolution A.1106(29)**, *Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems (AIS)*, revoking Resolution A.917(22):
- Reaffirmed that AIS is an aid to navigation that complements, but never replaces, radar plotting (ARPA) and visual lookouts under COLREGs Rules 5 and 7.
- Defined procedures for master-authorized deactivation in security zones (§22).
- Established guidance for Application-Specific Messages (**ASMs**) and virtual Aids to Navigation (**AtoN**).

### 12.5.3 ITU-R M.1371 maintenance

Recommendation **ITU-R M.1371** was updated by ITU-R Working Party 5B:
- **M.1371-5 (2014):** Refined Class B CSTDMA and SOTDMA specifications and slot-management rules for Message 27.
- **M.1371-6 (February 2026):** Harmonized channel definitions with VDES, aligned regional frequency tables, and formalized multi-system PNT receiver identifiers.

## 12.6 The digital bridge: S-100, MSC.530(106), and the chart sunset

Alongside radio links, electronic chart systems on ship bridges underwent a fundamental transformation.

```
       1998               2010             2015              2022             2026            2028-2029
      MSC.74             S-100            M.2092           MSC.530          MSC.592/593        Mandatory
     (Class A)         Ed. 1.0.0          (VDES)          (S-100 ECDIS)     (VDES SOLAS)      S-100 ECDIS
        |                  |                 |                 |                 |                 |
========+==================+=================+=================+=================+=================+========>
        |                  |                 |                 |                 |                 |
      SOLAS             AISSat-1          US 65-ft           S-100            S-100 Dual         VDES in
     Carriage           libais              Rule            Ed. 5.0.0         Fuel ECDIS          force
     Complete             ASM               (OMB)            5.2.0            Voluntary         (1 Jan 2028)
```
*Figure 12.1: Key regulatory, technical, and charting milestones from early standardization to the modern S-100 and VDES implementation decade (see also [Appendix A](../appendices/appendix-a-timeline.md)).*

### 12.6.1 The IHO S-100 framework and MSC.530(106)

For thirty years, Electronic Navigational Charts (**ENCs**) were structured under IHO **S-57** and portrayed via **S-52** libraries. While reliable, S-57 was an unextendable vector format incapable of carrying real-time, dynamic hydrographic data.

The IHO established the **S-100 Universal Hydrographic Data Model**, an ISO 19100-compliant framework structured into domain specifications:
- **S-101:** Next-generation Electronic Navigational Charts;
- **S-102:** High-resolution Bathymetric Surface data;
- **S-104:** Water Level Information for Surface Navigation (dynamic tides);
- **S-111:** Surface Currents;
- **S-124:** Navigational Warnings;
- **S-125:** Marine Aids to Navigation (digital AtoN status);
- **S-421:** Route Plan Exchange (IEC 63173-1).

In November 2022, IMO MSC adopted **Resolution MSC.530(106)**, updated and revoked by **MSC.530(106)/Rev.1** on 24 May 2024:
1. **1 January 2026 (Voluntary phase):** ECDIS installations may conform to S-100 (MSC.530(106)/Rev.1) or legacy S-57 (MSC.232(82)). Manufacturers released "dual-fuel" ECDIS units displaying S-57 and S-101 charts simultaneously.
2. **1 January 2029 (Mandatory phase):** All new ECDIS installations on SOLAS vessels must conform to MSC.530(106)/Rev.1, requiring native support for S-100 dynamic datasets and Part 15 digital signatures.

### 12.6.2 The paper and raster chart sunset

As digital navigation achieved dominance, hydrographic offices began phasing out legacy paper and raster charts.

In the United States, NOAA initiated a five-year sunset program in 2019, formally discontinuing all traditional paper nautical charts and raster products (NOAA RNCs) in **December 2024**. Navigation in US waters shifted entirely to ENC databases and digital NOAA Custom Charts.

## 12.7 The near future: VDES, R-Mode, and autonomous shipping

As AIS approached its third decade, the VHF Data Link reached saturation in congested shipping lanes. What was designed as a 9,600 bit/s tracking channel was burdened with weather reports, lock reservations, and virtual buoys. To protect collision-avoidance capacity, the international community designed the **VHF Data Exchange System** (**VDES**).

### 12.7.1 The architecture of VDES (ITU-R M.2092)

Codified in **Recommendation ITU-R M.2092-0** (2015), **M.2092-1** (2022), and **M.2092-2** (February 2026), VDES separates data exchange from core safety tracking across four components in Radio Regulations Appendix 18:
1. **AIS (Channels 2087 and 2088):** Preserves AIS 1 (161.975 MHz) and AIS 2 (162.025 MHz) for position reporting and collision avoidance.
2. **Application-Specific Messages (ASM 1 and ASM 2):** Allocates Channels 2027 (161.950 MHz) and 2028 (162.000 MHz) exclusively for digital ASMs (Messages 6 and 8), removing non-safety traffic from AIS 1 and 2.
3. **VDE-Terrestrial (VDE-TER):** Higher-speed digital channels in the VHF band (157.1875–157.3375 MHz and 161.7875–161.9375 MHz) aggregating 25 kHz blocks into 50 kHz, 100 kHz, or 150 kHz channels. Employing π/4-QPSK, 8PSK, and 16-QAM modulations, VDE-TER reaches data rates up to **307.2 kbit/s** on a 100 kHz channel—a **32-fold throughput increase** over legacy AIS that enables transmission of S-100 chart updates and dynamic routing files.
4. **VDE-Satellite (VDE-SAT):** Allocates dedicated channels (1026, 1086, 2026, 2086) approved at WRC-19 for bi-directional ship-satellite data links.

### 12.7.2 Satellite demonstrations and the MSC 111 milestone

Between 2017 and 2025, orbital demonstrators validated spaceborne VDES:
- **NorSat-2 (2017):** Built by UTIAS-SFL for Norway with a Kongsberg Seatex payload, receiving the first orbital VDE transmissions.
- **Sternula-1 (2023):** Danish 6U satellite launched on Transporter-6 demonstrating commercial maritime VDES links under the MARIOT project.
- **YMIR-1 (2023):** Built by AAC Clyde Space with a Saab VDES transceiver, testing two-way orbital communication.

The major regulatory breakthrough occurred at IMO MSC 111 (13–22 May 2026):
- Adopted **Resolution MSC.592(111)**, introducing VDES into the IMO framework.
- Adopted **Resolution MSC.593(111)**, establishing *Performance Standards for Shipborne VHF Data Exchange System (VDES)*.
- Approved **MSC.1/Circ.1699**, providing operational guidelines for shipborne VDES.
- Amended SOLAS Chapter V and HSC Codes permitting **voluntary carriage of VDES as an alternative to AIS**, effective **1 January 2028**. Under this provision, a type-approved VDES unit satisfies the statutory AIS carriage requirement via its internal AIS module.

### 12.7.3 Terrestrial radionavigation: R-Mode

To counter GNSS jamming and spoofing, maritime nations developed **Ranging Mode** (**R-Mode**).

Led by the German Aerospace Center (**DLR**), Swedish Maritime Administration, and regional partners, R-Mode modulates ranging signals onto existing coastal maritime transmitters:
1. **MF R-Mode:** Adds continuous-wave ranging signals to 283.5–325 kHz marine DGPS beacons, providing 15 to 30 m accuracy across coastal waters (Rizzi et al. 2023; Koch & Gewies 2020).
2. **VDES/AIS R-Mode:** Uses synchronized VHF base station pulses for terrestrial multilateration.

IALA published operational guidance under **Guideline G1158**, defining multi-source PNT engines to cross-check satellite signals against terrestrial VHF/MF ranging.

### 12.7.4 Maritime Autonomous Surface Ships (MASS)

The IMO is finalizing a mandatory **MASS Code** governing Maritime Autonomous Surface Ships, targeted for mandatory entry into force by 2028/2030.

Autonomous navigation algorithms utilize AIS telemetry to evaluate collision risk under COLREGs. However, because AIS is unauthenticated and susceptible to GNSS spoofing, autonomous bridge systems treat AIS strictly as advisory data, verifying every target against radar, optical cameras, and LiDAR before taking maneuvering action.

## Then & now

- ⟨H⟩ **1990:** Swedish Maritime Administration Director General Kaj Janérus approves SEK 2 million in development funding for the Automatic Vessel Monitoring System (AVMS), the predecessor to STDMA maritime tracking.
- ⟨H⟩ **1993:** Swedish 4S transponder trials begin on Lake Vänern, the Trollhätte Canal, and Styrsöbolaget passenger ferries in Gothenburg, demonstrating autonomous VHF time-slot sharing without master stations.
- ⟨H⟩ **1998:** ITU approves Recommendation ITU-R M.1371-0; IMO MSC.74(69) Annex 3 adopts universal shipborne AIS performance standards.
- ⟨H⟩ **2000:** IMO adopts Resolution MSC.99(73), revising SOLAS Chapter V Regulation 19 to establish the phased international carriage mandate.
- ⟨H⟩ **2002:** Accelerated AIS carriage adopted post-9/11 at London SOLAS Conference, moving commercial vessel compliance forward to 31 December 2004.
- ⟨H⟩ **2006:** IEC publishes 62287-1 Ed. 1, introducing low-cost Class B CSTDMA transponders for recreational and non-SOLAS commercial craft.
- ⟨H⟩ **2008:** CanX-6 (NTS) demonstrates the first spaceborne reception of maritime AIS signals from low Earth orbit.
- ⟨H⟩ **2010:** AISSat-1 launches; libais open-source decoder released during Deepwater Horizon response.
- ⟨H⟩ **2012:** Whale Alert mobile app and AIS binary message system deployed to protect endangered right whales in the Boston TSS.
- ⟨+⟩ **2015:** US Coast Guard issues final rule (80 FR 5282) expanding 33 CFR 164.46 carriage to commercial vessels $\ge 65\text{ ft}$, commercial towing craft $\ge 26\text{ ft}$, and fishing vessels; ITU approves Recommendation ITU-R M.2092-0 establishing the VDES framework; IMO adopts Resolution A.1106(29) updating AIS operational guidelines.
- ⟨+⟩ **2016:** US Coast Guard domestic carriage expansion compliance date takes effect on 1 March 2016; Global Fishing Watch launches publicly at the Our Ocean conference in Washington, DC.
- ⟨+⟩ **2017:** Large-scale commercial GNSS spoofing documented in the Black Sea near Novorossiysk, triggering US MARAD Maritime Advisory 2017-005A; launch of NorSat-2 carrying the first orbital VDES test payload.
- ⟨+⟩ **2019:** Systematic GNSS circle-spoofing documented across Shanghai port waters and the Huangpu River; WRC-19 allocates radio spectrum for satellite VDES (VDE-SAT).
- ⟨+⟩ **2021:** Spire Global acquires exactEarth; China enacts the Data Security Law and Personal Information Protection Law, precipitating a collapse of terrestrial AIS exports to foreign data aggregators.
- ⟨+⟩ **2022:** Garmin acquires Vesper Marine; Russian invasion of Ukraine escalates persistent GNSS jamming and spoofing across the Baltic and Black Seas; IMO MSC 106 adopts Resolution MSC.530(106) establishing S-100 ECDIS performance standards.
- ⟨+⟩ **2023:** Kpler acquires crowdsourced aggregators MarineTraffic and FleetMon; launch of Sternula-1 and YMIR-1 VDES test satellites.
- ⟨+⟩ **2024:** IALA Convention enters into force on 22 August 2024, formally transforming IALA into an Intergovernmental Organization; NOAA completes the final sunset of traditional paper nautical charts; Kpler announces agreement to acquire Spire Maritime.
- ⟨+⟩ **2025:** Kpler completes the acquisition of Spire Maritime for ~$241 million, centralizing major satellite and terrestrial feeds; first IALA General Assembly as an IGO convenes in Singapore.
- ⟨+⟩ **2026:** ITU approves Recommendations ITU-R M.1371-6 and M.2092-2; IMO MSC 111 adopts Resolutions MSC.592(111) and MSC.593(111), permitting voluntary VDES carriage under SOLAS Chapter V effective 1 January 2028; voluntary deployment of S-100 "dual-fuel" ECDIS begins on 1 January 2026.

## Validation, uncertainty & data quality

In the post-2015 era, data validation shifted from diagnosing static configuration errors to detecting deliberate kinematic manipulation and filtering multi-sensor satellite anomalies:

```
  +--------------------------------------------------------------------------+
  |                        Raw AIS Sentence / Bitstream                      |
  +--------------------------------------------------------------------------+
                                       |
                                       v
  +--------------------------------------------------------------------------+
  | 1. Syntactic & Integrity Filter                                          |
  |    - Verify NMEA 0183 checksum (*hh)                                     |
  |    - Check 16-bit CRC on bit payload                                     |
  |    - Validate MMSI structure (200000000 <= MMSI < 800000000)             |
  +--------------------------------------------------------------------------+
                                       |
                                       v
  +--------------------------------------------------------------------------+
  | 2. Sensor Integrity Sentinel Filter                                      |
  |    - Dynamic time stamp == 61 (positioning system in manual/DR mode)     |
  |    - Dynamic time stamp == 62 (electronic position-fixing system failed) |
  |    - Dynamic time stamp == 63 (positioning system inoperative)          |
  |    - Position coordinates == 181° lon / 91° lat (position unavailable)  |
  +--------------------------------------------------------------------------+
                                       |
                                       v
  +--------------------------------------------------------------------------+
  | 3. Kinematic Plausibility & Spoofing Triage                              |
  |    - Implied speed = Haversine(p1, p2) / delta_t                         |
  |    - Flag if implied_speed > class_cap (e.g. 45 kn Class A, 60 kn Class B)|
  |    - Flag if |implied_speed - reported_SOG| > 5.0 kn                     |
  |    - Rate of turn > 10.0 deg/s                                           |
  |    - Receiver distance > horizon (terrestrial VHF rarely > 60 nmi)        |
  +--------------------------------------------------------------------------+
                                       |
                                       v
  +--------------------------------------------------------------------------+
  |                    Cleaned & Validated Trajectory                        |
  +--------------------------------------------------------------------------+
```

### 12.8.1 Sensor sentinel filtering
When a shipboard GNSS receiver loses lock or encounters RF jamming, compliant transponders populate standard ITU-R M.1371 sentinel values in Messages 1, 2, 3, and 18:
- **Time stamp 61:** Indicates that the positioning system operates in manual input or dead-reckoning (**DR**) mode.
- **Time stamp 62:** Indicates that the positioning system operates in estimated mode or that internal integrity failed.
- **Time stamp 63:** Sent when the positioning system is completely inoperative.
- **Coordinate sentinels:** Longitude defaults to `181000000` ($181^\circ$), and latitude defaults to `91000000` ($91^\circ$), signaling that coordinates are unavailable.

Decoders must explicitly filter fixes where time stamp $\ge 61$ or latitude $> 90^\circ$ to prevent phantom targets at polar coordinates.

### 12.8.2 Kinematic anomaly scoring

To detect GNSS spoofing, circle-spoofing, and teleports, automated processing pipelines evaluate sequential position reports against physical vessel maneuvering limits.

Given two consecutive fixes $p_1 = (\phi_1, \lambda_1, t_1)$ and $p_2 = (\phi_2, \lambda_2, t_2)$, the implied speed over ground $V_{\text{implied}}$ is computed using the great-circle Haversine distance $D(p_1, p_2)$:

$$D(p_1, p_2) = 2 R \arcsin \left( \sqrt{ \sin^2\left(\frac{\Delta \phi}{2}\right) + \cos(\phi_1)\cos(\phi_2)\sin^2\left(\frac{\Delta \lambda}{2}\right) } \right)$$

$$V_{\text{implied}} = \frac{D(p_1, p_2)}{t_2 - t_1}$$

where $R \approx 3440.065\text{ nmi}$ (mean Earth radius).

A kinematic triage engine scores anomalies across six criteria:
1. **Implied speed violation:** $V_{\text{implied}} > V_{\text{cap}}$ ($45\text{ kn}$ Class A, $60\text{ kn}$ Class B).
2. **Speed discrepancy:** $|V_{\text{implied}} - \text{SOG}_{\text{reported}}| > 5.0\text{ kn}$.
3. **Turn-rate violation:** $\Delta \text{COG} / \Delta t > 10.0^\circ/\text{s}$.
4. **Spatial teleport:** $D(p_1, p_2) > 1.0\text{ nmi}$ when $\Delta t < 60\text{ s}$.
5. **Receiver horizon violation:** Distance to receiving station $R_{\text{rx}} > 60\text{ nmi}$ under standard line of sight.
6. **MMSI syntax corruption:** MMSI outside valid MID range ($200000000 \le \text{MMSI} < 800000000$) or matching test sequences (`0`, `1193046`, `123456789`).

> **Try it.** Run the kinematic plausibility triage script on sample harbor data to score anomalous tracks:
> ```bash
> . /usr/local/google/home/schwehr/sdd-books/ais/fable/.venv/bin/activate
> python code/security/kinematic_checks.py data/samples/synthetic_harbor.nmea --rx 42.36 -70.95
> ```
> Output:
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

The software ecosystem supporting AIS expanded substantially:

**Open source:**
- **libais** (Kurt Schwehr): Fast C++ library with Python bindings for decoding binary broadcast messages, Message 27, and Application-Specific Messages. Caveat: parses packet bitstreams; does not handle NMEA sentence reassembly or stateful tracking pipelines.
- **pyais** (Tomasz Bzh): Pure-Python AIS decoding library supporting NMEA 0183 AIVDM/AIVDO sentences, multiline payloads, and tag blocks. Caveat: Python interpretation overhead limits line-rate processing on high-volume satellite streams compared to compiled parsers.
- **ais-catcher** (Jasper den Ouden): High-speed C/C++ SDR receiver decoding raw IQ samples from RTL-SDR, Airspy, and HackRF dongles into NMEA and JSON. Caveat: focused on reception; lacks persistent database storage and geospatial analytics.
- **MovingPandas** (Anita Graser): Open-source Python library built on GeoPandas for trajectory data exploration and spatio-temporal movement analysis. Caveat: memory-bound; massive satellite archives require chunking or distributed engines like DuckDB.

**Free but closed:**
- **OpenCPN:** Navigation software and chart plotter supporting real-time AIS target display, collision warnings, and S-57/S-63 charts. Caveat: S-100 support is developmental and lacks type approval.
- **BarentsWatch:** Arctic portal providing visualization of Norwegian coastal AIS data. Caveat: limited to Scandinavian waters and subject to state security filtering.

**Commercial:**
- **Kpler (incorporating MarineTraffic and FleetMon):** Enterprise commodity tracking platform providing consolidated terrestrial and satellite vessel tracking. Caveat: proprietary subscription; raw NMEA streams are not publicly available.
- **Spire Maritime (Kpler):** Global satellite constellation API delivering satellite AIS positions and weather data. Caveat: message dropouts persist in high-density choke points such as the South China Sea.
- **Windward:** Predictive maritime analytics platform using machine learning to detect dark transshipments, sanctions evasion, and flag manipulation. Caveat: proprietary risk-scoring models cannot be externally audited.

## Standards & guides

- **IMO Resolution MSC.592(111)** (2026): *Adoption of Amendments to the International Convention for the Safety of Life at Sea, 1974 (SOLAS)*. Governs voluntary carriage of VDES as an alternative to AIS effective 1 January 2028.
- **IMO Resolution MSC.593(111)** (2026): *Performance Standards for Shipborne VHF Data Exchange System (VDES)*. Establishes operational and technical standards for shipborne VDES units.
- **IMO Resolution MSC.530(106)/Rev.1** (2024): *Performance Standards for Electronic Chart Display and Information Systems (ECDIS)*. Governs deployment of S-100 capable ECDIS, authorizing voluntary installation from 1 January 2026 and mandatory fitting for new tonnage from 1 January 2029.
- **IMO Resolution A.1106(29)** (2015): *Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems (AIS)*. Revokes Resolution A.917(22); provides the operational standard for bridge watchkeepers.
- **ITU-R Recommendation M.2092-2** (2026): *Technical characteristics for a VHF data exchange system in the maritime mobile service*. Defines physical modulation, framing, channel assignments, and TDMA protocols for VDES components.
- **ITU-R Recommendation M.1371-6** (2026): *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile frequency band*. Governs core physical and link layers of Class A and Class B AIS.
- **IHO S-100 Edition 5.2.0 / 5.2.1** (2024/2025): *IHO Universal Hydrographic Data Model*. Establishes the geospatial framework for modern digital charts and dynamic data products.
- **IALA Guideline G1117** (2023): *VHF Data Exchange System (VDES) Overview*. Provides system engineering guidance for VDES deployment.
- **IALA Guideline G1158** (2024): *VDES R-Mode*. Defines implementation standards for terrestrial radionavigation backups over maritime VHF.
- **United States Coast Guard Final Rule 80 FR 5282** (2015): *Vessel Requirements for Notices of Arrival and Departure, and Automatic Identification System*. Codified in 33 CFR 164.46; governs mandatory domestic carriage for commercial vessels $\ge 65\text{ ft}$, commercial towing craft $\ge 26\text{ ft}$, and commercial fishing vessels.

## Pitfalls

1. **Assuming the 2015 US AIS expansion required Class A across all vessels** → Small-vessel operators often assumed the USCG rule required expensive SOLAS Class A hardware → In reality, 33 CFR 164.46 specifically permitted certified Class B transponders for most domestic workboats and commercial fishing vessels operating outside VTS zones, saving operators thousands of dollars per vessel.
2. **Treating coordinate sentinels (181° lon / 91° lat) as valid ocean coordinates** → Programmers ingest raw sentences into databases without sentinel checking → The default sentinels ($181.0^\circ, 91.0^\circ$) represent "position unavailable"; failing to filter them causes thousands of phantom ships to appear in polar regions.
3. **Interpreting commercial aggregator API gaps as shipboard transmitter failures** → Analysts conclude that a ship turned off its AIS transponder when its track disappears from a web tracking service → Commercial aggregators experience terrestrial receiver outages, local network drops, or regulatory feed blocks (such as the November 2021 China feed collapse); verify gaps against raw satellite feeds before alleging illicit deactivation.
4. **Failing to check dynamic time-stamp sentinels 61, 62, and 63** → Analysts process invalid positions transmitted during GNSS outages as true coordinates → Transponders broadcast sentinel values 61–63 to explicitly announce that the position fix is operating in dead-reckoning mode, is degraded, or has failed entirely.
5. **Treating AIS as an unassailable source of collision avoidance for autonomous vessels** → Engineers designing autonomous surface vessels program avoidance algorithms that assume all transmitted AIS positions are authentic and accurate → AIS is completely unauthenticated and susceptible to GNSS spoofing, MMSI duplication, and deliberate tampering; autonomous systems must cross-verify all targets with primary radar, LiDAR, and optical tracking.
6. **Confusing VDES channel allocations with legacy AIS frequencies** → Technicians assume that installing VDES equipment requires new masthead antennas and entirely different radio bands → VDES operates in the existing maritime mobile VHF band (ITU Radio Regulations Appendix 18); legacy AIS 1 and AIS 2 channels remain untouched, while higher-speed data channels occupy adjacent 25–150 kHz allocations.
7. **Believing S-100 ECDIS mandates require immediate retirement of all S-57 ENCs** → Navigators assume existing chart holdings become obsolete on 1 January 2026 → IMO Resolution MSC.530(106)/Rev.1 initiates a multi-year transition period; S-100 ECDIS systems operate in a "dual-fuel" mode capable of seamlessly rendering legacy S-57 vector charts alongside modern S-101 datasets until mandatory S-100 deadlines in 2029.
8. **Assuming all vessels transmitting Class B are small recreational pleasure craft** → Watchstanders deprioritize Class B targets on bridge displays, assuming they are harmless sailboats → Under 33 CFR 164.46 and international rules, large commercial tugs, industrial dredges, and heavy 65-foot commercial fishing craft routinely transmit Class B.
9. **Relying solely on reported SOG without calculating implied distance-over-time velocity** → Threat-detection pipelines miss circle-spoofing and position manipulations that report normal speed values → Attackers frequently spoof GNSS coordinates while leaving reported SOG and COG fields intact; only by comparing implied Haversine speed $D/\Delta t$ against reported SOG can spoofing be exposed.
10. **Treating IALA as an informal non-governmental club** → Maritime legal teams cite IALA guidance as voluntary industry recommendations without binding treaty authority → With the entry into force of the IALA Convention on 22 August 2024, IALA became a full Intergovernmental Organization with formal diplomatic status.

## Key takeaways

- Between 2015 and 2016, the United States Coast Guard implemented 33 CFR 164.46, expanding mandatory AIS carriage to commercial craft $\ge 65\text{ ft}$, commercial towing vessels $\ge 26\text{ ft}$, and commercial fishing craft, integrating tens of thousands of domestic workboats into the national VDL.
- The public launch of Global Fishing Watch in September 2016 demonstrated the power of civil open-data tracking, using cloud computing and neural networks to map over 40 million hours of commercial fishing effort and expose international sanctions violations.
- Cross-sensor satellite studies (Paolo et al. 2024) revealed that approximately 75 percent of the world's commercial fishing vessels and 25 percent of transport vessels operate "dark" relative to public AIS, requiring Synthetic Aperture Radar (SAR) and optical imaging to detect.
- Private equity and commercial commodities intelligence dramatically consolidated the AIS data ecosystem between 2021 and 2025, culminating in Kpler's acquisitions of MarineTraffic, FleetMon, and Spire Maritime.
- The November 2021 Chinese terrestrial feed drop proved that foreign API streams do not equal physical VHF reception: local ships continued broadcasting on the water, but data-localization laws severed the cross-border digital feeds.
- The 2017 Novorossiysk incident, 2019 Shanghai circle-spoofing, and persistent 2022–present jamming across the Baltic, Black, and Red Seas ended the era of uncontested GNSS trust, forcing mariners and data scientists to build multi-sensor validation engines.
- The VHF Data Exchange System (VDES), governed by ITU-R M.2092-2 and approved for voluntary SOLAS carriage at IMO MSC 111 (Resolutions MSC.592(111) and MSC.593(111)), offloads ASMs to dedicated channels and provides up to 307.2 kbit/s bandwidth for digital e-Navigation.
- Electronic chart navigation is undergoing a foundational transition: NOAA fully retired traditional paper charts in December 2024, while IMO Resolution MSC.530(106)/Rev.1 authorized voluntary installation of S-100 "dual-fuel" ECDIS on 1 January 2026, leading to mandatory new-ship fitting on 1 January 2029.
- On 22 August 2024, the IALA Convention entered into force, transforming IALA into a formal treaty-level Intergovernmental Organization to coordinate global aids to navigation, VDES, and R-Mode terrestrial backups.

## References

- Androjna, A., Perkovič, M., Pavic, I. & Mišković, D. (2021). AIS Data Vulnerability Indicated by a Spoofing Case-Study. *Applied Sciences*, 11(11):5015. doi:10.3390/app11115015
- Bencsath, B., Buttyan, L., Félegyházi, M. & Szalay, M. (2020). Ghost Ships in the Harbor: Analyzing GNSS Spoofing in Shanghai Waters. *IEEE Transactions on Intelligent Transportation Systems*, 22(8):5112–5123.
- Bergman, M. (2019). *Ghost Ships, Crop Circles, and Soft Gold: A GPS Mystery in Shanghai*. MIT Technology Review. Cambridge: MIT Press.
- Cutlip, K. (2017). *AIS for Safety and Tracking: A Brief History*. Washington, DC: Global Fishing Watch. URL: https://globalfishingwatch.org/article/ais-brief-history/
- Gardebring, T., Zetterberg, R. & Svedberg, U. (2018). *AIS — How a Swedish innovation became a global standard*. Norrköping: Swedish Maritime Administration. URL: https://www.sjofartsverket.se/globalassets/framtidens-sjofart/foi/ais_eng.pdf
- IALA (2023). *VHF Data Exchange System (VDES) Overview* (Guideline G1117, Ed. 2.0). Saint-Germain-en-Laye: International Association of Marine Aids to Navigation and Lighthouse Authorities.
- IALA (2024). *Convention on the International Organization for Marine Aids to Navigation enters into force*. Saint-Germain-en-Laye: IALA.
- IALA (2024). *VDES R-Mode* (Guideline G1158, Ed. 2.0). Saint-Germain-en-Laye: International Association of Marine Aids to Navigation and Lighthouse Authorities.
- IHO (2024). *IHO Universal Hydrographic Data Model* (Publication S-100, Edition 5.2.0). Monaco: International Hydrographic Organization.
- IMO (2015). *Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems (AIS)* (Resolution A.1106(29)). London: International Maritime Organization.
- IMO (2024). *Performance Standards for Electronic Chart Display and Information Systems (ECDIS)* (Resolution MSC.530(106)/Rev.1). London: International Maritime Organization.
- IMO (2026). *Adoption of Amendments to the International Convention for the Safety of Life at Sea, 1974* (Resolution MSC.592(111)). London: International Maritime Organization.
- IMO (2026). *Performance Standards for Shipborne VHF Data Exchange System (VDES)* (Resolution MSC.593(111)). London: International Maritime Organization.
- ITU (2026). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile frequency band* (Recommendation ITU-R M.1371-6). Geneva: International Telecommunication Union.
- ITU (2026). *Technical characteristics for a VHF data exchange system in the maritime mobile service* (Recommendation ITU-R M.2092-2). Geneva: International Telecommunication Union.
- Koch, V. & Gewies, F. (2020). Worldwide Availability of Maritime Medium-Frequency Radio Infrastructure for R-Mode-Supported Navigation. *Journal of Marine Science and Engineering*, 8(3):209. doi:10.3390/jmse8030209
- Kroodsma, D. A., Mayorga, J., Hochberg, T., Miller, N. A., Boerder, K., Ferretti, F., Wilson, A., Bergman, B., White, T. D., Block, B. A., Woods, P., Sullivan, B., Costello, C. & Worm, B. (2018). Tracking the global footprint of fisheries. *Science*, 359(6378):904–908. doi:10.1126/science.aao5646
- Miller, N. A., Roan, A., Hochberg, T., Amos, J. & Kroodsma, D. A. (2018). Identifying global patterns of transshipment behavior. *Frontiers in Marine Science*, 5:240. doi:10.3389/fmars.2018.00240
- Paolo, F. S., Kroodsma, D., Raynor, J., Hochberg, T., Davis, P., Cleary, J., Marsaglia, L., Orofino, S., Thomas, C. & Halpin, P. (2024). Satellites reveal widespread unmonitored activity at sea. *Nature*, 625(7993):85–91. doi:10.1038/s41586-023-06825-8
- Reuters (2021). *China's new data laws make waves in shipping*. Reuters Business News (17 Nov 2021).
- Rizzi, M., Grundhöfer, N., Gewies, F. & Ehlers, F. (2023). Performance Evaluation of Medium-Frequency R-Mode in the Baltic Sea. *Applied Sciences*, 13(3):1872. doi:10.3390/app13031872
- United States Coast Guard (2015). Vessel Requirements for Notices of Arrival and Departure, and Automatic Identification System. *Federal Register*, 80 FR 5282:5282–5340. Codified at 33 CFR 164.46.
- United States Maritime Administration (2017). *GPS Interference — Black Sea* (MARAD Advisory 2017-005A). Washington, DC: US Department of Transportation.
- Welch, H., Clavelle, T., White, T. D., Cimino, M. A., Van Osdel, J., Hochberg, T., Kroodsma, D. & Hazen, E. L. (2022). Hot spots of unseen fishing vessels. *Science Advances*, 8(44):eabq2109. doi:10.1126/sciadv.abq2109
