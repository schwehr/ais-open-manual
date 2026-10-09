# Chapter 19 — Privacy and ethics

> **Part III — Identity, institutions, law.** How mandated open navigational telemetry creates a ubiquitous surveillance regime, pitting maritime safety against fundamental privacy rights, operational security, and national data sovereignty.

**In this chapter.** You will analyze the privacy and ethical dilemmas created by the Automatic Identification System (**AIS**). You will examine how an unauthenticated, unencrypted VHF broadcast system designed for collision avoidance evolved into a planetary tracking apparatus monitored by commercial data brokers, intelligence services, researchers, and open-source intelligence (**OSINT**) investigators. You will evaluate the legal status of vessel telemetry under data protection regimes including the European Union General Data Protection Regulation (**GDPR**), inspect national open-data filtering policies in Norway and Finland, and dissect United States Fourth Amendment doctrines emerging from the Nationwide AIS (**NAIS**) program. You will mathematically demonstrate why classical de-identification and pseudonymization fail when applied to spatiotemporal trajectories and vessel kinematics. Finally, you will establish rigorous ethical protocols for fisheries monitoring, dark-vessel exposure, and the coordinated vulnerability disclosure of maritime radio flaws.

## 19.1 AIS as mandated public self-surveillance

The Automatic Identification System creates an unprecedented civic paradox: it is an unauthenticated, unencrypted radio broadcast mandated by international treaty that operates as a global self-surveillance mechanism. When the International Maritime Organization (**IMO**) revised Chapter V of SOLAS in December 2000, safety authorities sought to eliminate the ambiguities of radar plotting and voice radio in dense traffic ([Chapter 10](ch10-standardization-1996-2004.md)). By requiring merchant ships to continuously broadcast kinematics, dimensions, and voyage itineraries, the international community established an open commons on the VHF maritime mobile band.

Crucially, the physical layer of AIS cannot enforce privacy. Transponders transmit in the clear across VHF channels AIS 1 (161.975 MHz) and AIS 2 (162.025 MHz) at 1 W to 12.5 W ([Chapter 28](ch28-rf-encoding-physical-layer.md)). Any dipole antenna connected to a low-cost SDR captures every burst within line of sight ([Chapter 27](ch27-rf-basics.md)). Space-based AIS payloads in Low Earth Orbit (**LEO**) deployed since 2008 eliminated mid-ocean isolation ([Chapter 39](ch39-satellite-ais.md)). Because confidentiality cannot be engineered into the protocol without breaking backward compatibility with bridge navigation systems ([Chapter 20](ch20-architecture-and-station-classes.md)), privacy protections can only be implemented downstream at the aggregation, filtering, and redistribution layers.

The populations subjected to this mandated self-surveillance fall into four distinct categories:
- **Commercial Merchant Crews:** Seafarers navigating cargo ships and tankers. Broadcasting port destinations, draught variations, and real-time speeds exposes crews to physical security threats, notably piracy in high-risk areas like the Gulf of Aden and Gulf of Guinea.
- **Commercial Fishers:** Operators whose livelihood depends on keeping proprietary fishing grounds confidential. Pervasive tracking exposes commercial secrets to competitors and subjects crews to algorithmic surveillance by regulatory agencies and non-governmental organizations.
- **Recreational Boaters and Yacht Owners:** Private citizens operating sailing vessels and motor yachts equipped with Class B transponders. On small craft, the vessel serves as a private vehicle and domestic residence. Real-time telemetry exposes personal vacation schedules, family movements, home ports, and physical absence from primary residences ashore.
- **Vulnerable Transiting Vessels:** Non-governmental search-and-rescue ships in the Mediterranean, maritime transport transiting conflict zones, and commercial vessels navigating near belligerent coastlines where open positional data can be weaponized for kinetic targeting or boarding operations.

```
       Is the vessel owned by a natural person?
                    /                             YES            NO (Corporate/State Asset)
                  /                        Does the Maritime           General navigational telemetry
      Mobile Service Identity       is non-personal corporate data.
      (MMSI) resolve to an          (Security/piracy considerations
     identifiable individual?       apply; data protection does not.)
            /                   YES          NO (Unregistered/Obscured)
          /                  Telemetry is      Kinematics, berth visits,
   PERSONAL DATA      and vessel dimensions may
   under GDPR Art 4   re-identify the owner via
     and UK GDPR.     auxiliary public databases.
```

### 19.1.1 The IMO's 2004 web publication condemnation

At its seventy-ninth session in December 2004, the IMO Maritime Safety Committee (**MSC**) confronted internet ship-tracking sites. The Committee issued a formal declaration in document MSC 79/23 (IMO 2004msc79), establishing that "the publication on the world-wide web or elsewhere of AIS data transmitted by ships could be detrimental to the safety and security of ships and port facilities and was undermining the efforts of the Organization and its Member States to enhance the safety of navigation and security in the international maritime transport sector."

The Committee condemned the "regrettable publication" of navigational telemetry and urged member governments to discourage internet republishing "subject to national laws." The IMO recognized that masters, alarmed by the public availability of their coordinates, might turn transponders off. The MSC strongly urged masters not to switch AIS off on account of internet republication, emphasizing that collision avoidance took precedence over commercial or personal privacy concerns.

However, the IMO's declaration was hortatory. The organization lacked authority to prohibit entities from receiving and republishing radio signals broadcast over public airwaves. Within three years, commercial aggregators such as MarineTraffic (launched in 2007) and VesselFinder expanded globally. Today, the IMO's 2004 position stands as a historic artifact: coastal states that supported the condemnation now operate public web portals distributing open AIS feeds.

> **Definitions that bite.**
>
> **Personal data vs. navigational telemetry.**
> Under European data protection law, data is not inherently personal or non-personal by its semantic label. A string of six-bit ASCII characters representing coordinates is purely navigational telemetry when emitted by a state-owned icebreaker or a commercial container line. However, the exact same sentence becomes **personal data** under Article 4(1) of Regulation (EU) 2016/679 (**GDPR**) the moment it relates to an "identifiable natural person"—such as the owner-operator of an 11-meter coastal trawler or the skipper of a 14-meter recreational sailboat. If any third party can combine the Maritime Mobile Service Identity (**MMSI**) with a public licensing directory, a marina berth ledger, or social media to identify the individual, the entire spatiotemporal track constitutes personal data subject to legal restrictions on storage, processing, and transfer.

## 19.2 Legal frameworks: GDPR, national open feeds, and the US doctrine

Open maritime radio broadcasts create sharp jurisdictional divergences between European individual-rights paradigms, United States constitutional doctrines, and authoritarian data sovereignty frameworks.

### 19.2.1 The European Union General Data Protection Regulation (GDPR)

Under Regulation (EU) 2016/679 (**GDPR**; EU 2016gdpr) and the UK GDPR, personal data encompasses any information relating to an identified or identifiable natural person. Recital 26 clarifies that identifiability turns on all means reasonably likely to be used by any party to identify the individual directly or indirectly.

When applied to AIS:
1. **Identifiability of Small Craft:** Recreational craft and artisanal fishing vessels are overwhelmingly owned by individuals or families. Broadcast MMSIs in Type 18, 19, or 24 messages resolve directly to natural persons via public telecommunications databases, amateur radio registries, and ship station directories.
2. **Controller Status:** Entities that capture, index, and redistribute raw or decoded small-craft trajectories qualify as **data controllers** under GDPR Article 4(7). Controllers require an Article 6(1) legal basis (legal obligation or legitimate interests) and must support data subject rights of access, rectification, and erasure.
3. **The Bridge Carve-Out:** Mariners receiving telemetry on bridge displays do not maintain a structured filing system under Article 2(1). Real-time collision avoidance processing falls outside GDPR liability, or is justified under vital interests (Art. 6(1)(d)) and legal obligations under COLREGs Rule 5 and Rule 7 ([Chapter 16](ch16-laws-and-treaties.md)).
4. **Journalistic and Research Exemptions:** Media organizations and researchers tracking high-profile vessels (e.g., sanctioned oligarch yachts) rely on Article 85 derogations. However, amateur OSINT hobbyists scraping and publishing unredacted tracks on social media lack institutional protections and risk regulatory penalties.

### 19.2.2 National open-data filtering: Norway and Finland

Recognizing that raw VHF feeds contain personal data, national administrations use algorithmic filtering to reconcile transparency mandates with privacy rights.

The Norwegian Coastal Administration (**Kystverket**) streams live AIS telemetry at `153.44.253.27:5631` (Kystverket 2026access). To protect commercial fishing secrets and individual privacy, Kystverket divides dissemination into two operational tiers:
- **The Open Component:** Free under the Norwegian Licence for Open Government Data (**NLOD**) without registration. Kystverket strips all fishing vessels under 15 m and recreational craft under 45 m, distributing only commercial shipping where privacy expectations do not attach.
- **The Closed Component:** Access to small-craft telemetry requires registration demonstrating a justified need (safety research or SAR development) and legal commitments prohibiting onward distribution.

Finland's transport infrastructure agency (**Fintraffic** / Väylä) distributes live telemetry via the Digitraffic API under CC BY 4.0. To protect artisanal fishers from commercial surveillance, the pipeline strips all broadcasts designated as Ship Type 30 (Fishing).

| Administration | Scope | Exclusion Threshold | Basis / Licence | Access Model |
| :--- | :--- | :--- | :--- | :--- |
| **Norway (Kystverket)** | Norwegian EEZ, Svalbard | Fishing < 15 m; Recreational < 45 m | NLOD (Open); Restricted (Closed) | Raw TCP feed (`153.44.253.27:5631`); web portal |
| **Finland (Digitraffic)** | Finnish waters, Baltic | Ship Type 30 (Fishing) removed | CC BY 4.0 | REST and WebSocket APIs |
| **United States (Marine Cadastre)** | US Navigable Waters, EEZ | None (2010–2014 encrypted MMSI; 2015+ open) | Public domain | Historical CSV / GeoParquet |
| **Denmark (DMA)** | Danish waters, Kattegat | None (full historic logs published) | Open Government Data | Bulk historical CSV archive files |

### 19.2.3 The United States doctrine: *Jones*, NAIS, and *EPIC v. USCG*

In the United States, privacy claims against government tracking derive from the Fourth Amendment and administrative law rather than comprehensive data protection statutes.

The Department of Homeland Security (**DHS**) and the United States Coast Guard (**USCG**) maintain that mariners hold no reasonable expectation of privacy in unencrypted radio broadcasts transmitted across public waterways. However, the legal landscape surrounding prolonged location tracking shifted with *United States v. Jones*, 565 U.S. 400 (2012). Justice Sonia Sotomayor's concurrence emphasized that pervasive GPS monitoring intrudes upon reasonable expectations of privacy by generating a comprehensive record of public movements.

This tension surfaced during the rollout of the Nationwide AIS (**NAIS**). On 15 January 2010, the Coast Guard published an interim policy for sharing NAIS information across federal, state, and foreign agencies (75 FR 2557; USCG 2010nais). Boating associations reacted vigorously. BoatU.S. urged the Coast Guard to confine data sharing strictly to safety and SAR missions. Ralph Naranjo highlighted the core concern: voluntary carriage of a safety transponder effectively enrolled recreational boaters in a permanent federal tracking database.

> **Case file.**
>
> **EPIC v. United States Coast Guard (2015–2016).**
> In May 2015, the Electronic Privacy Information Center (**EPIC**) filed a FOIA request demanding Coast Guard Privacy Impact Assessments (**PIAs**), data-sharing agreements, and system specifications for NAIS. When the agency failed to meet deadlines, EPIC sued in federal district court (*EPIC v. USCG*, Civil Action No. 15-1527; EPIC 2016nais).
> 
> The litigation compelled the USCG to release nearly 2,500 pages of internal records. Documents revealed that NAIS transceivers across 58 ports and 11 coastal sectors captured 92 million AIS messages daily from 12,700 vessels, routinely sharing unredacted feeds with intelligence agencies and foreign partners. EPIC demonstrated that NAIS operated without a system-specific System of Records Notice (**SORN**) under the Privacy Act of 1974 or an updated PIA under the E-Government Act of 2002. Although settled in March 2016 without reaching Fourth Amendment merits, the case exposed the vast scope of domestic maritime tracking.

## 19.3 The failure of de-identification and trajectory privacy

When sharing public mobility datasets, administrators frequently attempt to anonymize records by stripping or hashing vessel names, call signs, and MMSIs. In mobility analytics, trajectory de-identification fails due to the high dimensional uniqueness of movement profiles: as few as three or four spatiotemporal observations uniquely single out an individual vessel among millions ($k=1$).

In maritime telemetry, re-identification is accelerated by static invariants and physical chokepoints:
1. **Static Invariants:** Message 5 (Class A) and Message 24 Part B (Class B) broadcast overall length and beam. The tuple of length, beam, and vessel type narrows candidates to a fraction of a percent of the fleet.
2. **Terminal Port Visits:** Vessels moor at specific berths. Departures and arrivals cross-referenced against marina logs, bridge logs, or satellite imagery resolve pseudonyms immediately.
3. **Kinematic Profiles:** Acceleration, cruising speed, and maneuvering habits form behavioral signatures that survive identifier hashing.

### 19.3.1 The Marine Cadastre natural experiment

The definitive demonstration of de-identification failure occurred within the US Marine Cadastre program (BOEM/NOAA). In historical NAIS archives for 2010 through 2014, the Coast Guard mandated replacing MMSIs with cryptographic hashes and removing vessel names.

Researchers and analysts demonstrated that re-identifying vessels was trivial. Extracting length, beam, and draught from Message 5 and matching arrival timestamps against harbor pilot logs or Lloyd's Register resolved the cryptographic pseudonym back to a specific registered vessel. Recognizing that hashing provided zero privacy while impairing academic safety research and collision investigations ([Chapter 47](ch47-data-quality-track-reconstruction.md)), Marine Cadastre abandoned MMSI hashing in 2015, standardizing identities using the Authoritative Vessel Identification Service (**AVIS**).

> **Worked example.**
>
> **Kinematic re-identification of an encrypted vessel track.**
> Consider a dataset where identifying static fields and MMSIs have been replaced by a SHA-256 hash. An analyst seeks the identity of hashed track `e3b0c442...`.
> 
> 1. **Extract Static Dimensions:** Message 5 yields length 183 m, beam 32 m, draught 10.4 m, and tanker designation (Ship Type 80).
> 2. **Extract Spatial-Temporal Chokepoints:** The track shows the tanker entering a fairway, passing a pilot boarding station at (42 deg 20.4 min N, 070 deg 53.1 min W) at 14:22 UTC on 14 October, and mooring at an oil terminal berth at 16:05 UTC.
> 3. **Query Public Auxiliary Databases:** The port authority log lists two tanker arrivals on 14 October: *MT Atlantic Pride* (IMO 9234567, length 183 m, beam 32 m, pilot aboard 14:20) and *MT Baltic Energy* (IMO 9345678, length 228 m, beam 40 m, arriving 21:30).
> 4. **Conclusion:** Dimensions exclude the second tanker. *MT Atlantic Pride* matches with certainty ($P=1.0$). Pseudonymizing the MMSI failed completely.

## 19.4 Data sovereignty, geopolitics, and national restrictions

The global reception of maritime telemetry has collided with national security and data sovereignty doctrines. Ubiquitous LEO satellite reception and crowdsourced terrestrial networks inverted traditional coastal surveillance, enabling foreign entities to monitor domestic harbors and naval facilities in real time. Several nations have re-conceptualized navigational telemetry as sensitive intelligence subject to state export control.

### 19.4.1 China's 2021 data security regulations

The primary precedent occurred in late 2021 in the People's Republic of China. On 1 September 2021, the Data Security Law (**DSL**) took effect, followed on 1 November 2021 by the Personal Information Protection Law (**PIPL**).

Under the DSL, data impacting national security or economic operations is classified as Core or Important Data, imposing strict export barriers. State security authorities seized unauthorized coastal receivers operated by domestic hobbyists and logistics entities feeding foreign aggregators, characterizing coastal telemetry feeds as espionage.

The impact was immediate. In November 2021, commercial aggregators reported a 45% to 90% collapse in terrestrial AIS feeds from Chinese coastal waters. Tracking displays appeared blank across major hubs including Shanghai, Shenzhen, and Ningbo-Zhoushan. While ships continued broadcasting AIS over the air for local collision avoidance, data was barred from crossing the digital border.

This event highlighted that **data sovereignty is not personal privacy**. The restrictions secured state control over economic intelligence rather than individual seafarers. Moreover, space-based reception by commercial LEO constellations operating under high-seas and space law continued collecting signals, although orbital detection suffered heavy packet collisions in dense anchorages ([Chapter 30](ch30-network-loading-packet-loss.md); [Chapter 39](ch39-satellite-ais.md)).

## 19.5 Ethics of monitoring, transparency, and research

AIS telemetry powers non-governmental organizations (**NGOs**), researchers, and investigative journalists exposing Illegal, Unreported, and Unregulated (**IUU**) fishing, forced labor at sea, and illicit ship-to-ship (**STS**) transfers ([Chapter 6](ch06-fisheries-iuu-dark-fleets.md); [Chapter 8](ch08-security-and-national-security-uses.md)). However, publishing vessel tracks imposes serious ethical responsibilities.

### 19.5.1 The surveillance critique in fisheries governance

Scholars Hilde Toonen and Simon Bush demonstrated that centralized tracking creates legitimacy crises in fisheries governance (Toonen & Bush 2020digital). Developing-world coastal fishers frequently experience automated tracking as top-down disciplinary surveillance. Because algorithms classify behaviors based on statistical heuristics, false positives can lead to unjust vessel detentions, license cancellations, and economic harm without procedural due process.

### 19.5.2 The ethics of "AIS-off" lists and gap analysis

Publishing lists of "dark vessels" whose transponders ceased transmitting frequently implies illicit activity. In an empirical study analyzing 3.7 billion AIS positions, Heather Welch and co-authors established that vessels routinely disable AIS for legitimate, lawful reasons (Welch et al. 2022hotspots).

Under SOLAS Chapter V Regulation 19.2.4.7 and IMO Resolution A.1106(29) (IMO 2015a1106), the master retains explicit professional discretion to switch AIS off when continual operation compromises vessel safety or security. Documented legitimate rationales include:
- **Piracy Avoidance:** Masters transiting high-risk corridors (Gulf of Aden, Gulf of Guinea) deactivate AIS to avoid broadcasting positions to pirates.
- **Commercial Secrecy:** Fishing vessels disable AIS in international waters to protect proprietary fishing grounds from competitors.
- **RF and Sensor Gaps:** Database gaps frequently stem from satellite pass intervals, packet collisions on the VHF data link ([Chapter 30](ch30-network-loading-packet-loss.md)), or hardware faults rather than intentional deactivations.

Publishing accusatory reports based on tracking gaps alone without corroborating logbooks or radar violates basic research ethics.

> **Threat model.**
>
> **The perils of public dark-fleet attribution.**
> - **Attacker / Adversary:** Malicious maritime actors (sanctions evaders, IUU syndicates) or negligent data analysts.
> - **Attack Vector / Failure Mode:** Misattribution through identity spoofing or unverified gap analysis. An adversary configures their transponder with the MMSI of an innocent vessel, or an automated pipeline flags an innocent vessel whose signal was lost due to RF slot saturation.
> - **Impact:** An innocent ship owner, captain, or crew is publicly branded as a sanctions breaker or illegal fisher, resulting in port entry bans, vessel seizure, bank account freezes, and termination of P&I marine insurance coverage.
> - **Mitigation Protocol:** Analysts must never rely on AIS gap telemetry alone. Ethical attribution requires multi-sensor corroboration:
>   1. Cross-reference Synthetic Aperture Radar (**SAR**) imagery (e.g., Sentinel-1) or high-resolution optical imagery ([Chapter 6](ch06-fisheries-iuu-dark-fleets.md); Paolo et al. 2024satellite).
>   2. Corroborate physical radio frequency characteristics via satellite RF geolocation (TDOA/FDOA) to confirm whether transmissions actually originated from the claimed hull ([Chapter 35](ch35-direction-finding-geolocation.md)).
>   3. Verify whether the flag state or coastal authority authorized a security-related silent period under IMO Resolution A.1106(29).

### 19.5.3 The Global Fishing Watch data-ethics framework

In 2024, Global Fishing Watch (**GFW**) partnered with the Open Data Institute (**ODI**) to establish an institutional data-ethics framework (GFW 2025principles). GFW codified six core principles: transparency, impact assessment, sustainability, responsible management, accessibility, and inclusivity.

Operationally, GFW implemented two key safeguards:
- **Enforced Latency:** Public tracking data is subjected to a mandatory delay (typically 72 hours) to prevent predatory commercial exploitation.
- **Consequence Scanning:** New automated detection models undergo formal impact assessments to prevent erroneous accusations against vulnerable coastal fishers.

## 19.6 Coordinated disclosure of maritime radio vulnerabilities

Because AIS lacks authentication or cryptographic integrity, transponders accept any properly formatted 9,600-baud GMSK signal. Security researchers have repeatedly demonstrated that low-cost SDRs can forge ghost vessels, manipulate navigational status, and trigger false distress alerts on bridge ECDIS consoles ([Chapter 58](ch58-threat-model.md); [Chapter 59](ch59-spoofing.md)). Disclosing vulnerabilities in safety-critical maritime infrastructure requires strict protocols.

### 19.6.1 The Trend Micro disclosure precedent

The ethical baseline for maritime vulnerability disclosure was established by Marco Balduzzi, Alessandro Pasta, and Kyle Wilhoit of Trend Micro Research in 2013–2014 (Balduzzi, Pasta & Wilhoit 2014ais). The team identified fundamental protocol flaws as well as software injection vulnerabilities in major online aggregators.

Adhering to ISO/IEC 29147 (vulnerability disclosure; ISO 2018vulnerability) and ISO/IEC 30111 (handling processes; ISO 2019handling), the team established a disclosure model:
1. **Laboratory Confinement:** All radio testing occurred in RF-shielded enclosures using direct coaxial connections and 50-ohm dummy loads, never radiating signals over the air.
2. **Prior Multi-Stakeholder Notification:** The researchers notified ITU-R Working Party 5B, IALA, the IMO, the US Coast Guard, and aggregator platforms months before public disclosure.
3. **Aggregator Mitigation:** Online tracking providers received private notification and validation vectors to implement server-side filters.
4. **Responsible Presentation:** Public disclosures at Hack in the Box (2013) and ACSAC (2014) detailed architectural vulnerabilities while withholding transmit code and weaponized payloads.

> **Legal note.**
>
> **The illegality of over-the-air radio transmission.**
> Under international and domestic communications law, transmitting unauthorized signals on designated maritime safety frequencies is a serious criminal offense. In the United States, 47 CFR § 80.89 strictly prohibits transmitting unauthorized or false signals on marine VHF, and 18 U.S.C. § 1037 and the Communications Act of 1934 impose severe felony penalties—including substantial fines and imprisonment—for unauthorized radio transmissions. Under 33 CFR § 164.46(i), transmitting AIS signals from unauthorized land-based transmitters or aircraft is explicitly unlawful. Security researchers must never conduct "live" over-the-air experiments. All transmission experiments must take place exclusively inside certified RF-shielded enclosures or through hard-wired coaxial connections terminating directly into matched dummy loads.

### 19.6.2 Ethical guidelines for publishing spoofing evidence

When documenting and publishing spoofing or electronic warfare anomalies:
- **Protect Personnel Safety:** Redact tracking details of naval, diplomatic, or humanitarian vessels operating in active conflict zones.
- **Distinguish Interference from Intent:** Clarify whether anomalous tracks stem from external GNSS spoofing rather than vessel fraud.
- **Preserve Verifiable Provenance:** Publish raw NMEA sentences with complete NMEA 4.10 TAG blocks ([Chapter 26](ch26-interfaces-and-logging.md)) to support independent validation.

## Then & now

- `⟨H⟩` **1998:** The International Telecommunication Union adopts Recommendation ITU-R M.1371-0, standardizing AIS as an open, unencrypted, broadcast-based system designed strictly for ship-to-ship collision avoidance and vessel traffic management.
- `⟨H⟩` **2000:** The IMO adopts revised SOLAS Chapter V Regulation 19, mandating compulsory AIS carriage for international merchant fleets without any technical provision for encryption, authentication, or access control.
- `⟨+⟩` **2002:** The US Congress enacts the Maritime Transportation Security Act (**MTSA**; 46 U.S.C. § 70114), laying the statutory foundation for domestic carriage and nationwide tracking in US navigable waters.
- `⟨+⟩` **2004:** The IMO Maritime Safety Committee issues its MSC 79/23 declaration condemning the publication of AIS data on the internet as a threat to maritime security, urging member states to discourage web republication.
- `⟨+⟩` **2006:** The US Coast Guard initiates the Nationwide AIS (**NAIS**) procurement program, creating a centralized infrastructure to collect, store, and distribute coastal vessel telemetry.
- `⟨+⟩` **2007:** MarineTraffic is founded, demonstrating the viability of crowdsourced terrestrial receiver networks and establishing the modern commercial maritime data aggregation industry.
- `⟨H⟩` **2008:** The launch of pathfinding spaceborne payloads (such as NTS/EV-0) proves the feasibility of tracking AIS from orbit, permanently eliminating mid-ocean privacy.
- `⟨+⟩` **2010:** The US Coast Guard issues an interim policy on NAIS data sharing (75 FR 2557); NOAA and BOEM initiate the Marine Cadastre project, hashing MMSIs in public datasets to preserve anonymity.
- `⟨+⟩` **2013:** Trend Micro security researchers perform the first comprehensive ethical evaluation of AIS protocol and aggregator vulnerabilities, establishing responsible disclosure norms with the ITU, IALA, and IMO.
- `⟨+⟩` **2015:** Marine Cadastre abandons MMSI encryption after researchers demonstrate that vessel dimensions and port visits make trajectory de-identification mathematically impossible.
- `⟨+⟩` **2015:** The IMO adopts Resolution A.1106(29), superseding earlier operational guidelines and codifying the master's professional discretion to switch AIS off for safety or security.
- `⟨+⟩` **2016:** Settling *EPIC v. USCG*, the Coast Guard releases 2,500 pages of NAIS records, revealing extensive data sharing with defense and intelligence agencies.
- `⟨+⟩` **2018:** The European Union General Data Protection Regulation (**GDPR**) takes effect, establishing that small-craft AIS telemetry constitutes regulated personal data.
- `⟨+⟩` **2021:** China implements its Data Security Law and Personal Information Protection Law, causing an abrupt 45% to 90% decline in terrestrial AIS feeds available to foreign commercial aggregators.
- `⟨+⟩` **2022:** The Russian invasion of Ukraine sparks a widespread OSINT culture tracking the movements and AIS deactivations of sanctioned oligarch superyachts.
- `⟨+⟩` **2025:** Global Fishing Watch rolls out an institutional data-ethics framework co-developed with the Open Data Institute, establishing consequence scanning and enforced public data delays.

## On the wire

Navigational telemetry transmitted over the air exposes personal and operational information through specific bit fields. The standard Class A position report—Message Type 1, 2, or 3—encodes 168 bits packaged into a single TDMA slot, formatted according to Recommendation ITU-R M.1371 ([Chapter 22](ch22-message-catalog.md)).

For privacy and data protection, three specific payload segments create significant operational exposure:
1. **The Identity Token (Bits 8–37):** The 30-bit integer encoding the Maritime Mobile Service Identity (**MMSI**). This unique identifier operates as a persistent global primary key across all messages emitted by the hull, enabling effortless correlation across disparate sensor networks.
2. **The Spatial Coordinate Vector (Bits 61–115):** The 28-bit longitude and 27-bit latitude fields, encoded in two's complement integers representing values in units of 1/10000 of a minute. This yields a nominal spatial resolution of approximately 0.18 meters at the equator, exposing exact docking slips and micro-maneuvers.
3. **Static Voyage Metadata (Message Type 5):** Encoded across 424 bits in a two-slot burst, Message 5 broadcasts the vessel's International Maritime Organization (**IMO**) ship identification number (Bits 40–69), radio call sign (Bits 70–111), vessel name in 6-bit ASCII (Bits 112–311), dimensions from the internal GNSS antenna reference point (Bits 312–341), draught in decimeters (Bits 342–351), and declared voyage destination (Bits 352–371).

The following terminal session demonstrates how unencrypted NMEA 0183 sentences broadcast over the air are ingested and parsed into unmasked personal location profiles using open-source tools:

> **Try it.**
>
> Run this Python snippet to decode a live-format synthetic Class B Position Report (Message Type 18) and extract its identifying coordinates and static properties:
>
> ```python
> import pyais
> 
> # Raw NMEA 0183 AIVDM sentence containing a Class B position report
> sentence = r"\s:SYNTH01,c:1768478400*62\!AIVDM,1,1,,A,B52MJh00?6fo8@63Rg1u3wP5P000,0*41"
> 
> msg = pyais.decode(sentence)
> print(f"Message Type : {msg.msg_type}")
> print(f"Vessel MMSI  : {msg.mmsi}")
> print(f"Coordinates  : Lat {msg.lat:.5f}, Lon {msg.lon:.5f}")
> print(f"Speed & Course: {msg.speed} kn, {msg.course} deg")
> print(f"CS Unit Flag : {msg.cs}")
> ```
>
> Expected output:
> ```text
> Message Type : 18
> Vessel MMSI  : 338123456
> Coordinates  : Lat 42.33000, Lon -70.90000
> Speed & Course: 6.0 kn, 200.0 deg
> CS Unit Flag : True
> ```

## Validation, uncertainty & data quality

In privacy compliance, behavioral analysis, and regulatory enforcement, the fundamental error is treating raw or aggregated AIS feeds as a clean, complete, and ground-truth census of vessel movements.

Data quality errors in privacy-sensitive contexts arise from three primary mechanisms:
1. **Dynamic Spatial Sampling Bias:** Terrestrial and satellite AIS networks do not provide uniform coverage. Coastal receivers experience radio horizon limits, terrain shadowing, and atmospheric attenuation ([Chapter 29](ch29-propagation-modeling.md)). In dense harbors, packet collisions cause detection probabilities to collapse to under 30% for lower-powered Class B transponders ([Chapter 30](ch30-network-loading-packet-loss.md)). Consequently, an absence of recorded positions does not validate that a vessel was absent from a sensitive marine zone or intentionally disabled its transponder.
2. **Identity Corruption and Spoofing:** Because transponders lack cryptographic authentication, illegitimate actors can broadcast false identities. Furthermore, configuration mistakes by installers are widespread: thousands of operating vessels broadcast default MMSIs (e.g., `000000000`, `111111111`, or `123456789`), transposing separate physical hulls into a single synthetic, physically impossible trajectory ([Chapter 13](ch13-mmsi-deep-dive.md); [Chapter 47](ch47-data-quality-track-reconstruction.md)).
3. **Timing Inconsistencies:** The timestamp embedded in AIS position reports contains only a 6-bit integer representing the second of the minute (values 0–59), with sentinels 60 (not available), 61 (manual input), 62 (dead reckoning), and 63 (inoperative). High-level trajectory reconstruction depends entirely on the reception timestamp affixed by the local receiving station's system clock. In crowdsourced networks, unsynchronized station clocks routinely create time-inversion anomalies and out-of-order records.

To quantify tracking integrity before drawing ethical, legal, or investigative conclusions, analysts must execute a formal data quality auditing procedure:
1. **Kinematic Integrity Filter:** Compute implied speed between consecutive observations. If implied velocity exceeds the hydrodynamic limit of the hull (e.g., 35 knots for cargo vessels), flag the transition as a GPS jump, receiver clock failure, or multi-vessel MMSI collision.
2. **Station Diversity Check:** Verify that detections are captured across multiple distinct receiver IDs in NMEA TAG blocks. Single-station detections must be treated with low investigative confidence.
3. **Physical Multi-Sensor Corroboration:** Cross-check dark-vessel candidates against Sentinel-1 SAR imagery or satellite RF emitter geolocation before public attribution.
4. **Regulatory Exception Audit:** Verify whether flag-state notifications or maritime security advisories permitted silent periods under IMO Resolution A.1106(29).

In an auditing pipeline, the analyst calculates the kinematic plausibility metric between sequential track observations using great-circle distance divided by elapsed time. If calculated velocity exceeds physical vessel capabilities, the observation is rejected as an artifact.

## Software

The software tools relevant to maritime privacy, data protection, and ethical analytics fall into open-source frameworks, free public interfaces, and commercial intelligence suites:

**Open source:**
- **pyais:** Python library for decoding raw NMEA 0183 and AIVDM/AIVDO AIS messages into structured data models. Indispensable for building local ingestion filters and privacy redaction pipelines. *Caveat:* Operates strictly as a stateless sentence decoder; does not perform track assembly or multi-vessel disambiguation.
- **MovingPandas:** Python spatial analysis library built on GeoPandas and Shapely designed specifically for movement data and trajectory cleaning. Enables kinematic integrity verification, voyage segmentation, and spatial filtering. *Caveat:* High memory overhead when handling massive collections containing hundreds of millions of GPS points.
- **DuckDB (with Spatial extension):** High-performance analytical columnar database capable of querying massive Parquet archives of vessel positions directly on local hardware. *Caveat:* Out-of-memory errors occur if spatial index building is not carefully partitioned by time and bounding box.

**Free but closed:**
- **Kystverket Open AIS Service:** Public streaming TCP service providing live decoded and raw AIS telemetry for the Norwegian maritime domain. Operates an automated privacy filter removing small fishing and leisure vessels. *Caveat:* Upstream infrastructure occasionally undergoes unannounced maintenance outages, and connection limits apply.
- **Digitraffic Marine API (Fintraffic):** Real-time REST and WebSocket endpoints distributing filtered AIS traffic from Finnish waters under an open license. *Caveat:* Automatically suppresses Ship Type 30 (fishing), requiring researchers studying fisheries to seek alternative authenticated access.

**Commercial:**
- **Spire Maritime (Data Services):** Satellite-derived global AIS data feed providing near-real-time coverage and historical archives with advanced algorithmic decollision. *Caveat:* Highly expensive commercial licensing terms with strict restrictions prohibiting redistribution or open-access publication of raw telemetry.
- **Kpler (incorporating MarineTraffic and FleetMon):** Comprehensive commercial vessel tracking and maritime intelligence platform providing web-based mapping, port call analytics, and API integration. *Caveat:* Aggregator terms of service strictly prohibit automated screen scraping, and small-craft privacy is not systematically protected on consumer-facing web displays.

## Standards & guides

- **IMO Resolution A.1106(29)** (2015). *Revised Guidelines for the Onboard Operational Use of Shipborne AIS*. London: International Maritime Organization. Governs operational use of transponders, establishing the master's authority to switch off AIS during security threats.
- **IMO Document MSC 79/23** (2004). *Report of the Maritime Safety Committee on its Seventy-Ninth Session*. London: International Maritime Organization. Contains the committee declaration condemning the publication of vessel tracking telemetry on the internet.
- **Regulation (EU) 2016/679 (GDPR)** (2016). *General Data Protection Regulation*. Brussels: European Parliament and Council of the European Union. Governs lawful collection, processing, storage, and cross-border transfer of personal location data within the EU.
- **Directive 2002/59/EC** (as amended by 2009/17/EC and 2011/15/EU). *Establishing a Community Vessel Traffic Monitoring and Information System (VTMIS)*. Governs mandatory AIS and vessel traffic management across European waters.
- **46 U.S.C. § 70114 & 33 CFR § 164.46**. *Automatic Identification System Regulations*. Washington, DC: United States Coast Guard. Establishes the statutory and administrative carriage and operational rules across US navigable waters.
- **ISO/IEC 29147:2018**. *Information Technology — Security Techniques — Vulnerability Disclosure*. Geneva: ISO/IEC. Establishes international guidelines for vendors, coordinators, and security researchers conducting coordinated vulnerability disclosures.
- **ISO/IEC 30111:2019**. *Information Technology — Security Techniques — Vulnerability Handling Processes*. Geneva: ISO/IEC. Governs operational protocols for processing, investigating, and remediating technical security flaws.
- **Global Fishing Watch Data Ethics Principles** (2025). Washington, DC: Global Fishing Watch and the Open Data Institute. Defines operational standards for the ethical collection, modeling, and publication of industrial and small-scale maritime tracking data.

## Pitfalls

- **Equating the lack of a vessel name with true anonymization:** Stripping the static name or call sign while leaving the MMSI intact provides zero anonymity. The MMSI is a global unique identifier indexed in dozens of public registries.
- **Believing that cryptographic hashing of the MMSI protects identity:** Substituting a SHA-256 hash for the MMSI fails because vessel physical dimensions combined with arrival timestamps at a single port berth trivially re-identify the vessel.
- **Treating tracking gaps as conclusive evidence of illicit activity:** Assuming that a vessel whose AIS transmission disappears is engaged in illegal fishing or sanctions evasion. High packet collisions, RF shadowing, equipment failure, and lawful safety deactivations under IMO A.1106(29) routinely cause extended tracking gaps.
- **Assuming small-craft tracking falls outside data protection laws:** Believing that because AIS is broadcast on open radio airwaves, the GDPR does not apply. In the EU, Class B tracks emitted by privately owned recreational or artisanal vessels constitute personal location data.
- **Conducting live over-the-air vulnerability testing:** Radiating forged, spoofed, or modified AIS signals over open maritime frequencies. This is a severe federal and international criminal offense that imperils lives at sea; security research must be confined to closed RF testing or certified Faraday enclosures.
- **Conflating state data sovereignty with individual data privacy:** Assuming that foreign national statutes restricting AIS exports (such as China's 2021 Data Security Law) are designed to protect seafarer privacy rather than establish state control over economic and naval intelligence.
- **Failing to cross-examine single-receiver crowd feeds:** Publishing investigative accusations based on data received by a single unverified crowdsourced station. Rogue or misconfigured terrestrial feeders frequently inject synthetic or corrupted NMEA sentences into open aggregators.
- **Ignoring the piracy and physical security risks of public tracking:** Publishing real-time positional updates of vulnerable merchant or humanitarian vessels transiting high-risk piracy corridors or contested conflict zones.
- **Assuming commercial aggregators filter personal data:** Relying on commercial tracking sites to protect small-boat privacy. Commercial web platforms monetize complete datasets and rarely redact private small craft unless compelled by specific national legislation.
- **Overlooking the master's legal obligation to log silent periods:** Forgetting that when a master lawfully deactivates AIS under SOLAS Chapter V and IMO Resolution A.1106(29), the action, operational rationale, and duration must be entered into the official ship's logbook.

## Key takeaways

- **AIS is an open self-surveillance system by design:** Built without encryption or authentication for tactical collision avoidance, the broadcast protocol cannot enforce privacy at the physical radio layer.
- **Privacy must be governed downstream:** Because radio broadcasts cannot be restricted over the air, data protection can only be applied at the aggregation, filtering, and redistribution layers.
- **Small-craft telemetry is personal data under the GDPR:** Position reports from private yachts and artisanal fishing vessels resolve directly to identifiable natural persons, imposing data controller obligations on aggregators.
- **National open-data filters establish practical compromises:** Administrations like Norway's Kystverket separate open feeds from restricted archives by enforcing explicit physical thresholds (excluding fishing vessels under 15 m and pleasure craft under 45 m).
- **Trajectory de-identification is mathematically impossible:** Hashing MMSIs or stripping names fails because static dimensions, vessel kinematics, and unique port terminal visits re-identify ships with near certainty.
- **National data sovereignty is not personal privacy:** Restrictions on terrestrial AIS data exports, such as China's 2021 regulatory restrictions, represent the geopolitical weaponization of data sovereignty rather than the protection of individual privacy.
- **Dark-vessel analysis demands multi-sensor corroboration:** Analysts must never infer illicit behavior from tracking gaps alone without verifying physical satellite imagery, RF emitter geolocation, and the legal exceptions codified in IMO Resolution A.1106(29).
- **Vulnerability disclosure requires strict laboratory isolation:** Maritime radio security research must never be radiated over the air; findings must be disclosed responsibly following ISO/IEC 29147 protocols in consultation with international maritime bodies.

## References

- Balduzzi, M., Pasta, A. & Wilhoit, K. (2014). A Security Evaluation of AIS Automated Identification System. *Proceedings of the 30th Annual Computer Security Applications Conference (ACSAC 2014)*, pages 436–445. New Orleans, LA: ACM. doi:10.1145/2664243.2664257
- Electronic Privacy Information Center (2016). *EPIC v. USCG — Nationwide Automatic Identification System (Civil Action No. 15-1527, D.D.C.)*. FOIA litigation settlement and document production.
- European Parliament and Council of the European Union (2002). *Directive 2002/59/EC establishing a Community vessel traffic monitoring and information system and repealing Council Directive 93/75/EEC*. Official Journal of the European Communities, L 208:10–27.
- European Union (2016). *Regulation (EU) 2016/679 on the protection of natural persons with regard to the processing of personal data and on the free movement of such data (General Data Protection Regulation)*. Official Journal of the European Union, L 119:1–88.
- Global Fishing Watch (2025). *Data Ethics Principles and Governance Framework*. Washington, DC: Global Fishing Watch and Open Data Institute.
- International Maritime Organization (2004). *Report of the Maritime Safety Committee on its Seventy-Ninth Session*. Document MSC 79/23. London: IMO.
- International Maritime Organization (2015). *Revised Guidelines for the Onboard Operational Use of Shipborne AIS*. Resolution A.1106(29). London: IMO.
- International Organization for Standardization and International Electrotechnical Commission (2018). *Information technology — Security techniques — Vulnerability disclosure*. Standard ISO/IEC 29147:2018. Geneva: ISO/IEC.
- International Organization for Standardization and International Electrotechnical Commission (2019). *Information technology — Security techniques — Vulnerability handling processes*. Standard ISO/IEC 30111:2019. Geneva: ISO/IEC.
- Kroodsma, D. A., Mayorga, J., Hochberg, T., Miller, N. A., Boerder, K., Ferretti, F., Wilson, A., Bergman, B., White, T. D., Block, B. A., Woods, P., Sullivan, B., Costello, C. & Worm, B. (2018). Tracking the global footprint of fisheries. *Science*, 359(6378):904–908. doi:10.1126/science.aao5646
- Kystverket (2026). *Access to AIS data*. Norwegian Coastal Administration. https://www.kystverket.no/en/sea-transport-and-ports/ais/access-to-ais-data/
- Paolo, F. S., Kroodsma, D., Raynor, J., Stevens, T., Stokes, C., Hughes, C., Jarman, B., Hazen, T., Johnston, A. V. & Costello, C. (2024). Satellite mapping reveals extensive industrial activity at sea. *Nature*, 625(7993):85–91. doi:10.1038/s41586-023-06825-8
- Spire Global, Inc. (2021). *AIS spoofing and dark-target detection methodology*. US Patent 11,156,723 B2. Washington, DC: USPTO.
- Toonen, H. M. & Bush, S. R. (2020). The digital frontiers of fisheries governance: fish attraction devices, drones and satellites. *Journal of Environmental Policy & Planning*, 22(1):125–137. doi:10.1080/1523908X.2018.1461084
- United States Coast Guard (2010). *Interim Policy for the Sharing of Information Collected by the Coast Guard Nationwide Automatic Identification System*. Federal Register, 75(10):2557–2559.
- Welch, H., Hazen, T. D., Hines, E. E., White, T. J., Farrugia, T. D., Dyndo, M. J. & Kroodsma, D. (2022). Hot spots of unseen fishing vessels. *Science Advances*, 8(44):eabq2109. doi:10.1126/sciadv.abq2109