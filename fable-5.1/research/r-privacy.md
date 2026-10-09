# Dossier: Privacy, data protection, and research ethics around AIS

**Purpose.** This dossier collects what can be confirmed, as of October 2026,
about the privacy and ethics questions that AIS raises: AIS as mandated,
unencrypted self-reporting that anyone can receive; the IMO's 2004 condemnation
of web republication and its practical irrelevance; how national
administrations filter small-craft and fishing-vessel data from open feeds
(Norway's 15 m / 45 m rule; Finland's type-30 filter; Marine Cadastre's
2010–2014 MMSI encryption); the US NAIS information-sharing policy and the
EPIC v. USCG FOIA case; the GDPR "is it personal data?" question for owners of
small craft; China's 2021 data-law shock as a sovereignty argument; the ethics
of researchers, NGOs and journalists who publish tracks (GFW's data-ethics
programme; the fisheries-governance literature); and the norms for disclosing
AIS security findings (Trend Micro 2013; ISO/IEC 29147). It feeds
**Chapter 19** (Privacy and ethics) primarily, and supplies material to
**Chapter 2** (uses and their consequences), **Chapter 6** (fisheries, AIS
disabling), **Chapter 8** (security uses; China 2021), **Chapter 13** (MMSI
registries), **Chapter 16/17** (law; FOIA; GDPR), **Chapter 34** (RF
fingerprinting implications), **Chapter 41** (provider licences and
filtering), **Chapter 46** (NAIS data recipients), **Chapter 58–60** (threat
model and disclosure), **Chapter 65** (hacks and unintended uses), and
**Chapter 67** (mobile-phone privacy at sea, by analogy).

> Research-session note. Facts marked *high* were read directly from the cited
> primary page during this session (2026-10-05): Kystverket, EPIC, Google
> Patents, ITU. Facts marked *medium* come from search summaries that cite a
> primary page which could not be opened (federalregister.gov, imo.org,
> marinecadastre.gov and digitraffic.fi are JavaScript-rendered or
> access-restricted). Items marked *(verify)* could not be confirmed. No
> national data-protection-authority decision specifically about AIS was
> found; the dossier says so rather than inventing one.

## Key questions

1. Is AIS data "personal data"? For whom (owner-operators, yacht owners,
   small fishers, crew), under which law (GDPR, UK GDPR, PIPL, US sectoral
   law), and with what consequences for collectors and republishers?
2. What did the IMO actually say about publishing AIS on the web (MSC 79,
   Dec 2004), and what effect did it have?
3. How do government open-data feeds handle small craft and fishing vessels
   (Norway, Finland, Denmark, USA)? What do the filters look like in practice?
4. What is the US position: NAIS information-sharing policy (75 FR 2557,
   2010), DHS "no expectation of privacy" stance, the BoatU.S. comments,
   the EPIC FOIA case and what it revealed about recipients and retention?
5. What is the legal basis under which crowdsourced networks (MarineTraffic,
   AISHub, VesselFinder) and satellite operators collect and sell AIS? What do
   their terms say about re-use and scraping?
6. Does de-identification work for ships? (No — the kinematics, dimensions
   and port calls re-identify; Marine Cadastre's 2010–2014 MMSI encryption is
   the natural experiment.)
7. What did China's Data Security Law / PIPL (2021) do to AIS, and how should
   the book frame "data sovereignty" versus "privacy"?
8. What obligations do researchers, NGOs and journalists take on when they
   publish vessel tracks, fishing-effort maps, "AIS-off" lists, or spoofing
   evidence? What do GFW's data-ethics principles and the fisheries-governance
   literature say?
9. What are the norms for disclosing AIS protocol/implementation
   vulnerabilities (coordinated disclosure, ISO/IEC 29147/30111, CISA CVD) and
   how did the 2013 Trend Micro team handle it?
10. Where does the master's right to switch off AIS "for security" (SOLAS
    V/19.2.4.7; A.1106(29)) meet privacy claims by owners and crews?

## Primary sources located

| Source | Identifier / edition / year | URL | What it covers | Access |
|---|---|---|---|---|
| Norwegian Coastal Administration (Kystverket) | "Access to AIS data" (web page, read 2026-10-05) | https://www.kystverket.no/en/sea-transport-and-ports/ais/access-to-ais-data/ | Open vs closed AIS components; exclusion of fishing vessels < 15 m and recreational craft < 45 m from open data; NLOD licence; application and use restrictions for the closed component; raw feed 153.44.253.27:5631 | Free |
| EPIC | "EPIC v. USCG – Nationwide Automatic Identification System" case page and FOIA productions | https://epic.org/documents/epic-v-uscg-nationwide-automatic-identification-system/ | FOIA request 29 May 2015; complaint 18 Sep 2015 (No. 15-1527, D.D.C.); settlement 28 Mar 2016; released NAIS Information Sharing Policy, NAIS Information Recipients, PIAs, Northrop Grumman progress reports 2011–2015, technical specs | Free |
| US Coast Guard, Federal Register | "Interim Policy for the Sharing of Information Collected by the Coast Guard Nationwide Automatic Identification System", 75 FR 2557 (15 Jan 2010), Docket USCG-2009-0701, FR Doc. 2010-632 | https://www.federalregister.gov/citation/75-FR-2557 (verify link) | The policy on which BoatU.S. and EPIC commented | Free |
| DHS Privacy Office | DHS/USCG/PIA-006 "Vessel Requirements for Notices of Arrival and Departure (NOAD) and Automatic Identification System (AIS)" | https://www.dhs.gov/privacy-impact-assessments (search USCG) | The PIA attached to the NOAD/AIS rulemaking (see `r-law-us.md`) | Free |
| IMO | MSC 79 (1–10 Dec 2004) report, agenda item on AIS data on the web (MSC 79/23 (verify paragraph)) | IMO Docs (members) ; quoted on IMO AIS page https://www.imo.org/en/OurWork/Safety/Pages/AIS.aspx | The Committee's statement that web publication "could be detrimental to the safety and security of ships and port facilities" | Free (IMO page); paid/members (IMODOCS) |
| IMO | Resolution A.1106(29) (2015) "Revised Guidelines for the Onboard Operational Use of Shipborne AIS" (supersedes A.917(22)/A.956(23)) | https://www.imo.org (resolution text via IMODOCS or national mirrors) | The master's discretion to switch AIS off where continual operation might compromise safety or security | Free (mirrors) |
| EU | Regulation (EU) 2016/679 (GDPR), Art. 4(1) (definition of personal data), Recital 26 (identifiability), Art. 6(1)(f) (legitimate interests), Art. 85 (journalism) | https://eur-lex.europa.eu/eli/reg/2016/679/oj | The test that decides whether a small-craft track is personal data | Free |
| EU | Directive 2002/59/EC (VTMIS), consolidated; Art. 24 "Confidentiality of information" | https://eur-lex.europa.eu/eli/dir/2002/59/oj | Member States' duty to keep information received under the Directive confidential (verify current wording) | Free |
| Marine Cadastre (NOAA/BOEM) | AIS Vessel Traffic Data documentation/FAQ | https://marinecadastre.gov/ais/ (JS site; see also InPort metadata) | 2010–2014 products had MMSI encrypted and names/call signs removed at USCG request; practice discontinued from 2015 (AVIS used for identity) | Free |
| Fintraffic / Väylä | Digitraffic marine AIS API documentation | https://www.digitraffic.fi/en/marine-traffic/ais/ (JS site) | Vessel-type filtering/modification rules in the open Finnish feed (fishing vessels, type 30, removed) — (verify) | Free |
| Danish Maritime Authority | "AIS data" page and historical AIS files | https://www.dma.dk/safety-at-sea/navigational-information/ais-data | Danish open historic AIS (CSV); check filtering/terms — (verify) | Free |
| Global Fishing Watch / Open Data Institute | GFW data-ethics programme (ODI partnership 2024; principles rolled out 2025; internal data-ethics committee; "consequence scanning") | https://globalfishingwatch.org (data-ethics pages; exact URL (verify)) and https://theodi.org (case study) | Six principles: transparency, impact assessment, sustainability, responsible management, accessibility, inclusivity | Free |
| Toonen, H. M. & Bush, S. R. | "The digital frontiers of fisheries governance: fish attraction devices, drones and satellites", *J. Environ. Policy & Planning* 22(1):125–137 (2020), doi:10.1080/1523908X.2018.1461084 | https://doi.org/10.1080/1523908X.2018.1461084 | Legitimacy and surveillance critique of digital MCS including AIS-based transparency | Paid (OA (verify)) |
| Balduzzi, M., Pasta, A. & Wilhoit, K. | "A Security Evaluation of AIS Automated Identification System", ACSAC 2014 (and Trend Micro research paper 2013/2014) | https://dl.acm.org/doi/10.1145/2664243.2664257 (verify DOI) | Lab-only testing; notification of ITU-R, IALA, IMO, USCG and online providers before disclosure | Paid (ACM) / free (Trend Micro PDF) |
| ISO/IEC | ISO/IEC 29147:2018 "Vulnerability disclosure"; ISO/IEC 30111:2019 "Vulnerability handling processes" | https://www.iso.org/standard/72311.html ; https://www.iso.org/standard/69725.html | The international norm for coordinated disclosure | Paid (29147:2018 made freely available by ISO (verify)) |
| CISA | Coordinated Vulnerability Disclosure Process | https://www.cisa.gov/coordinated-vulnerability-disclosure-process | US CVD norm for ICS/maritime vendors | Free |
| Reuters / Maritime Executive | Nov 2021 reports on the collapse of terrestrial AIS feeds from China after PIPL (1 Nov 2021) and DSL (1 Sep 2021) | (see `r-history.md`; exact Reuters headline (verify)) | The sovereignty/"privacy" framing of restricting AIS exports | Free |
| Welch, H. et al. | "Hot spots of unseen fishing vessels", *Science Advances* 8(44): eabq2109 (2022) (verify) | https://www.science.org/doi/10.1126/sciadv.abq2109 (verify) | Legitimate reasons for AIS disabling (piracy, competitors) vs illicit ones — relevant to the ethics of "AIS-off" lists | Free (OA) |
| Press coverage of 2022 superyacht tracking | *The Guardian*, *Washington Post*, Bloomberg, Mar 2022 | (verify specific articles) | Oligarch yachts switching off AIS; OSINT "yacht-watchers" | Free |
| US FCC | Universal Licensing System (ULS) public search; 47 CFR Part 80 ship station licences | https://wireless2.fcc.gov/UlsApp/UlsSearch/searchLicense.jsp | Licensee names/addresses for FCC-issued MMSIs are public records | Free |
| ITU | MARS (Maritime mobile Access and Retrieval System) ship-station database | https://www.itu.int/mmsapp/ShipStations/list | Public lookup of ship-station particulars by MMSI/name/call sign | Free |

## Verified facts

| Fact | Source | Confidence |
|---|---|---|
| Kystverket's open AIS feed covers vessels in the Norwegian EEZ and the Svalbard/Jan Mayen zones but "does not include data on fishing vessels under 15 metres and recreational craft under 45 metres"; the open data are licensed under NLOD and need no registration; a raw TCP feed is published at 153.44.253.27 port 5631. | Kystverket "Access to AIS data" (read 2026-10-05) | high |
| For the closed component "the user must complete a registration form specifying, among other things, the reason for access"; data on < 15 m fishing vessels and < 45 m recreational craft "must not be used for anything other than the stated purpose and will not be distributed to third parties"; Kystverket can filter individual access by area, vessel, update rate. | same | high |
| EPIC filed a FOIA request to USCG on 29 May 2015, sued on 18 Sep 2015 (complaint No. 15-1527, D.D.C.), obtained "nearly 2,500 pages" and settled on 28 Mar 2016. Released documents include a NAIS "Information Sharing Policy", "NAIS Information Recipients", "Privacy Impact Assessments" (received 25 Jan 2016), Northrop Grumman progress reports 2011–2015 and technical specifications. | EPIC case page (read 2026-10-05) | high |
| EPIC's page (quoting USCG) says NAIS transceivers are near 58 US ports and 11 coastal areas, that NAIS "currently receives about 92 million AIS messages a day from 12,700 unique vessels", that NAIS "relied mostly on existing infrastructure when it was first rolled out in 2006", that permanent transceivers reach ~50 nmi and satellite data were intended to extend coverage to 2,000 nmi. | same | high (that EPIC says so; figures are 2015-era) |
| EPIC's legal framing: the Privacy Act of 1974 requires a System of Records Notice; the E-Government Act of 2002 requires a PIA; EPIC argued NAIS lacked NAIS-specific versions. EPIC invokes Justice Sotomayor's concurrence in *United States v. Jones* (2012), which agreed with Justice Alito that "longer term GPS monitoring in investigations of most offenses impinges on expectations of privacy". | same | high |
| Ralph Naranjo (mariner, author, former Vanderstar Chair, US Naval Academy), quoted by EPIC: "a sailor's Good Samaritan effort to share location data will automatically enroll them in a data bank that tracks all of their movements." BoatU.S. ("the nation's largest organization of recreational boaters") filed comments to USCG on NAIS data dissemination. | same | high |
| The USCG published an "Interim Policy for the Sharing of Information Collected by the Coast Guard Nationwide Automatic Identification System" in the Federal Register on 15 Jan 2010, 75 FR 2557, Docket USCG-2009-0701, FR Doc. 2010-632, and requested comments; BoatU.S. commented in Feb 2010 urging USCG to "narrowly confine the use of [the] data for safety and homeland security purposes". | Search summaries citing federalregister.gov and epic.org (page not openable) | medium — (verify) citation and quote against the FR page |
| Marine Cadastre's AIS products for 2010–2014 had the MMSI field encrypted and vessel name/call sign removed at USCG's request; from 2015 the MMSI is published and identities are cleaned via the Authoritative Vessel Identification Service (AVIS). | Search summary citing marinecadastre.gov (JS page not readable) | medium — (verify) on the Marine Cadastre FAQ/InPort metadata |
| At MSC 79 (Dec 2004) the IMO Maritime Safety Committee agreed that "the publication on the world-wide web or elsewhere of AIS data transmitted by ships could be detrimental to the safety and security of ships and port facilities and was undermining the efforts of the Organization and its Member States to enhance the safety of navigation and security in the international maritime transport sector", condemned the "regrettable publication", urged Member Governments to discourage it "subject to national laws", and urged masters not to switch AIS off on that account. | Search summaries citing imo.org, uscg.mil, gcaptain (IMO page body not rendered) | medium–high — wording widely reproduced; (verify) against MSC 79/23 |
| MarineTraffic (founded 2007) and other web services nonetheless grew; no jurisdiction surveyed prohibits reception and republication of AIS broadcasts by private parties (the IMO statement is hortatory). | Absence of any located prohibition; Kystverket/Digitraffic/Marine Cadastre themselves publish | medium (negative finding) |
| GDPR Art. 4(1) defines personal data as "any information relating to an identified or identifiable natural person"; Recital 26 applies the test of "all the means reasonably likely to be used" to identify. Applied to AIS: a Class B position report from a privately owned yacht whose MMSI resolves (via FCC ULS, ITU MARS or a national registry) to a named individual is personal data; a position report from a 100,000 GT tanker owned by a company is not, though crew-related ASMs could be. | Regulation (EU) 2016/679 text (well-known; not re-read this session) | high (law); medium (application — no DPA decision found) |
| No decision of a national data-protection authority (Datatilsynet NO/DK, IMY SE, ICO UK, CNIL FR, etc.) specifically about AIS tracking of pleasure craft was found in this session. | Searches 2026-10-05 | medium (negative finding; (verify) with DPA case databases) |
| Finland's Digitraffic open AIS API applies vessel-type filtering/modification rules; fishing vessels (ship type 30) are reported as removed from the feed. | Search summary citing digitraffic.fi docs (JS page not readable) | medium — (verify) in the API docs |
| Global Fishing Watch engaged the Open Data Institute in 2024 for a data-ethics maturity assessment; developed six data-ethics principles (transparency, impact assessment, sustainability, responsible management, accessibility, inclusivity); rolled them out internally in 2025 with a cross-team data-ethics committee, a formal review process for technology/innovation projects, and "consequence scanning". GFW states it cannot release raw AIS because it is licensed commercial data, and applies delays to some public data "to protect individuals". | Search summaries citing globalfishingwatch.org and theodi.org (exact pages (verify)) | medium |
| Toonen & Bush (2020) argue that digital monitoring, control and surveillance (AIS, drones, satellites) creates a legitimacy problem for fishers who experience it as an expansion of surveillance and discretionary authority. | *J. Environ. Policy & Planning* 22(1):125–137, doi:10.1080/1523908X.2018.1461084 (citation confirmed by search; full text paywalled) | medium–high |
| The Trend Micro team (Balduzzi, Wilhoit, Pasta) tested in a lab (wired, not over the air) and state they "reached out to the appropriate providers and authorities" — ITU-R, IALA, IMO, USCG and online providers (MarineTraffic, AISHub, VesselFinder, ShipFinder) — before public disclosure at HITB KL (Oct 2013) and ACSAC 2014. | Search summary citing the Black Hat/HITB abstracts and the team's slides | medium — (verify) in the ACSAC paper's disclosure section |
| China's Data Security Law took effect 1 Sep 2021 and the Personal Information Protection Law on 1 Nov 2021; in early Nov 2021 foreign aggregators reported a sharp fall (figures from ~45 % to ~90 % depending on source) in terrestrial AIS from Chinese waters as domestic providers stopped exporting data; the radio broadcasts themselves continued. | Reuters/Maritime Executive/Lloyd's List (see `r-history.md`) | medium–high |
| In March 2022 multiple superyachts linked to sanctioned Russian owners stopped transmitting AIS; the episode produced a public "yacht-watching" OSINT culture built on MarineTraffic-type services. | Guardian/Washington Post/Bloomberg coverage (specific articles (verify)) | medium |
| Patents now exist on AIS-derived surveillance analytics — e.g., Spire's US 11,156,723 B2 "AIS spoofing and dark-target detection methodology" (granted 26 Oct 2021) and COM DEV's US 9,015,567 B2 "consistency checking and anomaly detection" (2015) — i.e., "AIS-off" inference is a commercial product, not only an academic exercise. | Google Patents (see `r-patents.md`) | high |
| ISO/IEC 29147:2018 (vulnerability disclosure) and ISO/IEC 30111:2019 (vulnerability handling processes) are the current international standards for coordinated disclosure; CISA operates a published CVD process. | ISO catalogue; CISA page (ids well established; not re-read this session) | high |
| SOLAS V/19.2.4.7 requires AIS to be "in operation at all times except where international agreements, rules or standards provide for the protection of navigational information"; IMO A.1106(29) allows the master to switch AIS off "if the master believes that the continual operation of AIS might compromise the safety or security of his/her ship or where security incidents are imminent" (paragraph number (verify)), with a log-book entry and restart as soon as the danger has passed. | SOLAS consolidated; A.1106(29) (see `r-standards-imo.md`) | high (substance); (verify) exact paragraph |

## Notes and quotes

- **The structural fact.** AIS is a legally mandated, unauthenticated,
  unencrypted broadcast of identity, position, course, speed, destination and
  dimensions. Privacy therefore cannot be engineered at the radio; it can only
  be managed at the *aggregation and republication* layer — which is exactly
  where governments (Kystverket's 15 m/45 m filters; Marine Cadastre's
  2010–2014 MMSI encryption; Digitraffic's type-30 filter) and NGOs (GFW's
  delays and non-release of raw data) act. Chapter 19 should open with this.
- **IMO 2004 vs reality.** MSC 79's language is strong — "regrettable
  publication", "undermining the efforts of the Organization" — but it was a
  committee statement, not a regulation, and asked Member Governments to act
  only "subject to national laws". Two decades later the same administrations
  publish open feeds. The honest framing: the IMO lost the argument on
  republication and shifted to urging masters *not* to switch off.
- **Kystverket as the model filter.** The thresholds (15 m fishing, 45 m
  recreational) are a legible policy: below them, data are personal enough to
  need purpose limitation and a no-onward-distribution condition; above them,
  they are open under NLOD. Note the asymmetry: the *radio* signal from a
  12 m fishing boat is still receivable by anyone with a US$30 dongle — the
  filter governs only the state's own redistribution.
- **US framing is Fourth-Amendment, not data-protection.** EPIC's argument
  runs through *Jones* and the Privacy Act/E-Government Act procedural duties,
  not through a "personal data" definition. DHS's stance (as characterised by
  EPIC/BoatU.S.) is that boaters have no reasonable expectation of privacy in
  a broadcast. Chapter 19 should present the two legal cultures side by side.
- **Naranjo's point is about recruitment, not surveillance per se.** His
  objection is that a *safety* device becomes an *enrolment* device: fit AIS
  to be seen by the ferry and you are thereby entered into a federal data bank
  shared with the recipients on the NAIS list EPIC obtained. That list (NAIS
  Information Recipients, Oct 2015 production) is primary material for
  Chapter 46 and should be summarised there.
- **De-identification does not work for ships.** Marine Cadastre's encrypted
  MMSIs (2010–2014) still carried length, beam, draught, ship type, speed
  profiles and berth visits; linking an encrypted track to a named ship via a
  single port call or a public photo is trivial. The practice was dropped from
  2015. This is the cleanest worked example for the "k-anonymity fails"
  argument (ch. 19 candidate figure 3).
- **GDPR application, stated carefully.** The book should not claim a DPA has
  ruled. It can say: (a) Art. 4(1)/Recital 26 make identifiability
  context-dependent; (b) MMSI → owner resolution is "reasonably likely" via
  public registries (FCC ULS for US ship-station licences; ITU MARS; many
  national registers), so small-craft tracks are personal data for
  controllers in scope; (c) Art. 6(1)(f) legitimate interests (safety,
  transparency) and Art. 85 (journalism) are the likely bases; (d) safety-
  of-life use on the bridge is outside the controller problem because no
  filing system is kept. Mark the whole analysis as the authors' reading, not
  authority.
- **Sovereignty is not privacy.** China's 2021 restriction was justified
  under data-security law, and the PIPL framing was secondary; the effect was
  to deny *foreign* aggregators, not to protect *individuals* (the data still
  flowed domestically). The book should resist the "privacy" label here and
  call it export control of a public broadcast.
- **The ethics of "AIS-off" lists.** Welch et al. (2022) themselves note that
  disabling AIS can be legitimate (piracy risk, hiding productive grounds from
  competitors). Publishing per-vessel "gap" tables therefore implies
  wrongdoing without proof. GFW's "impact assessment" principle and its
  public-data delays are the operational response; Toonen & Bush give the
  theoretical critique (legitimacy, discretionary authority). Chapter 6 and 19
  should agree on one treatment.
- **Journalists and OSINT.** The 2022 yacht-watching episode shows the
  symmetric problem: AIS lets the public hold sanctioned owners to account,
  and lets anyone track a family's holiday. Art. 85 GDPR and national press
  law are the relevant carve-outs; the book should note that OSINT hobbyists
  do not enjoy them automatically.
- **Disclosure norms for AIS security research.** The Trend Micro precedent —
  lab-only RF, prior notice to ITU-R/IALA/IMO/USCG and to the web providers,
  then conference disclosure — is a reasonable template. Add ISO/IEC 29147
  and CISA CVD as the formal frameworks and note that protocol-level flaws
  (no authentication) have no "vendor" to patch, so disclosure is about
  operator awareness, not fixes (→ ch. 58/64).
- **Fingerprinting (ch. 34).** RF fingerprinting that ties a *unit* to a
  *transmission* independent of the claimed MMSI is a privacy technology in
  reverse: it defeats identity changes. The chapter should carry a Legal note
  that persistent device identification of private craft is personal-data
  processing in GDPR jurisdictions.
- **PLAN wording.** PLAN ch. 19 lists "GDPR opinions (verify)"; none specific
  to AIS were found. Recommend changing the seed to "GDPR Art. 4(1)/Recital 26
  analysis; national open-data filters (NO/FI/US) as de-facto positions".

## Open questions / (verify)

- (verify) Read 75 FR 2557 (15 Jan 2010) directly: the interim policy's
  categories of recipients, retention statement, and whether it asserts "no
  expectation of privacy"; locate the BoatU.S. comment in docket
  USCG-2009-0701 on regulations.gov and quote it exactly.
- (verify) MSC 79/23 paragraph number for the AIS-on-the-web statement, and
  whether it was carried into a circular (there is no MSC circular known; the
  statement appears only in the session report and on the IMO AIS web page).
- (verify) Marine Cadastre FAQ/InPort text on MMSI encryption 2010–2014 and
  the 2015 change; whether Class B records were ever excluded.
- (verify) Digitraffic's exact filter table (ship types removed/remapped) and
  licence (CC BY 4.0?).
- (verify) Danish DMA historic AIS: any filtering of pleasure craft or terms
  restricting re-identification; Swedish Sjöfartsverket's AIS data agreement
  and whether leisure craft are excluded; UK MCA position.
- (verify) Any DPA decision, guidance or enforcement on AIS/ship-tracking
  sites (search GDPRhub, Datatilsynet NO/DK, IMY, ICO, CNIL, AEPD, Garante).
  Also any court decision on scraping MarineTraffic/VesselFinder data (none
  found).
- (verify) GFW's data-ethics page URL and the exact wording of the six
  principles; the ODI case-study URL; the stated public-data delay (72 h?)
  and the terms of GFW's data licence (CC BY-SA 4.0 for processed layers?).
- (verify) Balduzzi et al. ACSAC 2014 DOI and the paper's disclosure
  paragraph; the Trend Micro white-paper title and date.
- (verify) Welch et al. 2022 full citation (vol/issue/eLocator) and the
  passage on legitimate disabling.
- (verify) A.1106(29) paragraph number for the master's switch-off
  discretion, and the exact SOLAS V/19.2.4.7 wording in the current
  consolidated edition.
- (verify) FCC ULS: confirm which licensee fields are public for ship station
  licences (name, address) and whether recreational MMSIs issued by BoatU.S./
  Sea Tow/USPS are searchable anywhere publicly (believed not — they go to
  the USCG SAR database only).
- (verify) ITU MARS: which fields (owner, address) are displayed publicly for
  ship stations; administrations may withhold.
- (verify) Specific Guardian/Washington Post articles (March 2022) on
  superyachts going dark, for citation.
- (verify) Whether IALA has issued guidance on AIS data privacy/dissemination
  (none located; check IALA G-series on AIS shore data exchange).
- (verify) Whether any crew-related personal data flows through AIS in
  practice (Circ.289 FI "number of persons on board" is a count only; pilot
  plug and PPU logs may hold pilot identity — ch. 3/51).

## Candidate figures and worked examples

1. **"Where privacy can be enforced" layer diagram (ch. 19):** ship → VHF
   broadcast (no control) → receivers (anyone) → aggregators (terms, filters)
   → republishers (web, APIs, datasets) → analysts (ethics, law). Annotate
   with the controls that exist at each layer (none / licence / filter /
   delay / review).
2. **Table — national open-feed filters (ch. 19/41):** Norway (fishing < 15 m
   and recreational < 45 m excluded; closed component by application; NLOD);
   Finland (type-30 removed, types remapped (verify)); USA (Marine Cadastre
   2010–2014 MMSI encrypted, names removed; 2015+ full identities, AVIS);
   Denmark, Sweden, UK (verify). Columns: what is removed, legal basis
   stated, licence, historical depth.
3. **Worked example — re-identification of an "anonymised" track (ch. 19/47):**
   take a 2013 Marine Cadastre record with encrypted MMSI; show how length ×
   beam × draught × ship type × a single berth visit narrows candidates to one
   ship using a port-call list; discuss why MMSI hashing was abandoned.
   (Use the book's synthetic sample data; do not re-identify a real small
   craft.)
4. **Timeline (ch. 19, App. A):** 2004 MSC 79 statement · 2006 NAIS start ·
   2007 MarineTraffic · 2010 75 FR 2557 and BoatU.S. comments · 2010–2014
   Marine Cadastre MMSI encryption · 2012 *Jones* · 2013 Trend Micro disclosure
   · 2015–16 EPIC v. USCG · 2016 GFW launch · 2018 GDPR applies · 2021 China
   DSL/PIPL · 2022 yacht-watching · 2024–25 GFW/ODI data-ethics programme.
5. **Decision tree — "Is this AIS record personal data?" (ch. 19):** owner a
   natural person? → MMSI resolvable via public registry? → are you keeping a
   filing system? → purpose (safety / research / journalism / commerce) →
   likely GDPR basis and obligations; with a caveat that it is the authors'
   reading.
6. **Box — Legal note template for data chapters (ch. 41/47/48/50):** three
   sentences on licence, personal-data status, and onward-distribution limits,
   instantiated for Kystverket, Marine Cadastre, GFW and a commercial API.
7. **Box — Disclosure checklist for AIS security findings (ch. 58–60):** lab
   only; no over-the-air transmission; notify flag/coastal administration,
   IALA ENAV, vendor(s), and the web providers; ISO/IEC 29147 timelines; what
   to withhold (transmit code) — modelled on the 2013 Trend Micro practice.

## Recommended use by chapter

- **Chapter 2 (Uses taxonomy):** add a "privacy cost" column to the uses
  table; cite Naranjo for the recreational-boater perspective and Toonen &
  Bush for fishers.
- **Chapter 6 (Fisheries/IUU):** treat AIS-disabling inference with Welch et
  al.'s caveat and GFW's impact-assessment principle; avoid naming vessels on
  "gap" evidence alone.
- **Chapter 8 (Security uses):** China 2021 as export control of a public
  broadcast, not privacy; NAIS recipients list (EPIC) as the US sharing
  picture.
- **Chapter 13 (MMSI):** MMSI → person resolution paths (FCC ULS, ITU MARS,
  national registers) are what make small-craft AIS personal data; note
  which registries are public.
- **Chapter 16/17 (Law; legal issues):** 75 FR 2557; EPIC v. USCG (FOIA,
  settled 2016); GDPR Art. 4(1)/Recital 26/6(1)(f)/85; Directive 2002/59/EC
  Art. 24 confidentiality; MSC 79 statement; no DPA or scraping case found
  (say so).
- **Chapter 19 (Privacy and ethics):** the whole dossier; open with the
  structural fact; the layer diagram; the filter table; the re-identification
  worked example; the decision tree; the ethics section (GFW principles,
  Toonen & Bush, Welch et al., journalism/OSINT); the disclosure checklist.
- **Chapter 34 (Fingerprinting):** Legal note on persistent device
  identification of private craft.
- **Chapter 41 (Providers):** per-provider licence and filter notes
  (Kystverket, Digitraffic, Marine Cadastre, DMA, GFW, commercial APIs).
- **Chapter 46 (Government software):** NAIS Information Sharing Policy and
  recipients list from the EPIC productions.
- **Chapter 47/48 (Data quality; spatial stats):** why hashed MMSIs break
  identity resolution and what Marine Cadastre 2010–2014 data can and cannot
  support.
- **Chapter 58–60, 64 (Security):** disclosure norms (Trend Micro precedent;
  ISO/IEC 29147/30111; CISA CVD); the "no vendor to patch" problem for
  protocol flaws.
- **Chapter 65 (Hacks):** yacht-watching and OSINT as an unintended use with a
  privacy edge.
- **Chapter 67 (Mobile phones at sea):** contrast — AIS is *intentionally*
  public; cellular location leakage (SS7/Diameter) is *unintentionally*
  exposed; the ethics differ accordingly.
- **Appendix A (Timeline):** entries from candidate figure 4 as ⟨+⟩.
- **Appendix G (Datasets):** licence and filter columns populated from the
  table above.
