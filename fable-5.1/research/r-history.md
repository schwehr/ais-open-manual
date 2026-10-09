# Dossier: History of AIS (prehistory → standardization → growth → present)

**Purpose.** This dossier collects verified dates, identifiers, people and primary
sources for the historical narrative of *The AIS Handbook*. It feeds Part II
directly — **Chapter 9** (prehistory to Lans and STDMA), **Chapter 10**
(standardization 1996–2004), **Chapter 11** (growth 2004–2015), **Chapter 12**
(2015–present) — plus **Appendix A** (master timeline) and the *Then & now*
sections of every chapter. It also completes the Phase 0 task "Import
gis-history entries" by listing every AIS-relevant or adjacent entry from
[schwehr/gis-history](https://github.com/schwehr/gis-history) with `⟨H⟩` tags
(§9 below). Everything stated here was checked against the URL given in the
table; anything not confirmed is marked `(verify)`.

*Research date: 2026-10-04.*

---

## Key questions

1. Who invented the TDMA scheme behind AIS, when, and what exactly do the patents
   claim and when did they expire?
2. What role did the Swedish Maritime Administration (SMA), the Swedish Space
   Corporation, GP&C and Saab play, and what were the "4S" / AVMS trials?
3. What were the parallel US (post-*Exxon Valdez*/OPA-90), UK (Dover Strait) and
   Panama Canal efforts, and how did they converge at IMO/ITU?
4. Exact dates and ids: IMO MSC.74(69) Annex 3; ITU-R M.1371-0; SOLAS Ch. V
   revision (MSC.99(73)); the December 2002 SOLAS Conference acceleration; IEC
   61993-2 Ed. 1; the US 2003 and 2015 rules.
5. Milestones of growth: Class B (IEC 62287-1), AIS-SART (MSC.246(83)),
   satellite AIS (NTS 2008, AISSat-1 and NORAIS 2010, OG2 2014, Spire 2015,
   exactView RT on Iridium NEXT 2017–19), crowdsourcing (MarineTraffic 2007),
   open-source decoders (libais 2010).
6. Recent structural shifts: VDES (M.2092, 2015→), M.1371-6 (2026), the Chinese
   terrestrial-feed collapse (Nov 2021), market consolidation (Garmin–Vesper
   2022; Kpler–MarineTraffic/FleetMon 2023; Kpler–Spire Maritime 2024/25), IALA
   becoming an IGO (Aug 2024).
7. What does the GFW history article (Cutlip 2017) actually say, and which of
   its claims need correction against primary sources?
8. Which gis-history entries belong in the AIS timeline and *Then & now* boxes?

---

## Primary sources located

| Source | Identifier / edition / year | URL | What it covers | Access |
|---|---|---|---|---|
| Swedish Maritime Administration, *AIS — How a Swedish innovation became a global standard* (brochure; texts by T. Gardebring, R. Zetterberg, U. Svedberg) | 16-page PDF; file metadata created 2018-11-05 | https://www.sjofartsverket.se/globalassets/framtidens-sjofart/foi/ais_eng.pdf | Benny Pettersson's 1965 Kobe typhoon origin story; SMA 1990 funding decision (SEK 2 M); AVMS trials; GP&C; 1993 Trollhätte/Vänern and Styrsöbolaget trials; "4S"; IMO 1994/1997; ITU 1997/1998; Lans dropping royalty claim; IEC test standard 2002 | Free |
| Google Patents: US 5,506,587 A "Position indicating system" (H. Lans; GP&C Systems International AB) | Filed 1992-06-29 (PCT/SE92/00485); granted 1996-04-09; priority SE 9102034 (1991-07-01) | https://patents.google.com/patent/US5506587A/en | The STDMA patent family; priority chain; anticipated expiry 2013-04-09 | Free |
| ITU-R Recommendation M.1371 edition list | M.1371-0 (11/1998) … M.1371-5 (02/2014), **M.1371-6 (02/2026)** | https://www.itu.int/rec/R-REC-M.1371/en | Edition dates of the technical standard | Free (ITU-R recs are free PDFs) |
| ITU-R M.1371-0 landing page | 11/1998 | https://www.itu.int/rec/R-REC-M.1371-0-199811-S/en | First edition (also the gis-history link) | Free |
| IMO Res. MSC.74(69) Annex 3, *Recommendation on performance standards for a universal shipborne AIS* | Adopted 12 May 1998 | (IMO docs via imorules.com mirror; official text in IMO Docs) https://www.imorules.com/ (verify exact page) | Original performance standard | Free (mirror) / IMO Docs login |
| IMO Res. MSC.99(73), revised SOLAS Chapter V | Adopted 5 Dec 2000; in force 1 Jul 2002 | https://www.imo.org/en/OurWork/Safety/Pages/AIS.aspx | Carriage requirement V/19.2.4 and phase-in | Free |
| IMO Conference of Contracting Governments to SOLAS 1974, London 9–13 Dec 2002 (Resolution 1; new Ch. XI-2 / ISPS; amended V/19 AIS phase-in) | Dec 2002; in force 1 Jul 2004 | https://www.imo.org/en/OurWork/Security/Pages/SOLAS-XI-2%20ISPS%20Code.aspx (verify exact page) | Acceleration of AIS carriage to not later than 31 Dec 2004 | Free |
| IMO Res. MSC.246(83), AIS-SART performance standards | Adopted 8 Oct 2007; applies to AIS-SART installed on/after 1 Jan 2010 | https://www.imo.org (resolution text via IMO Docs / imorules mirror) (verify URL) | AIS-SART | Free |
| US Coast Guard interim rule, *Automatic Identification System; Vessel Carriage Requirement* | 68 FR 39353, 1 Jul 2003 | https://www.federalregister.gov/ (search 68 FR 39353) (verify direct URL) | First US AIS carriage rule under MTSA 2002 | Free |
| US Coast Guard final rule, *Vessel Requirements for Notices of Arrival and Departure, and Automatic Identification System* | 80 FR 5282, 30 Jan 2015; AIS provisions (33 CFR 164.46(b),(c)) effective 7 Apr 2016; fit-by date 1 Mar 2016 | https://www.federalregister.gov/documents/2015/01/30/2015-01331/vessel-requirements-for-notices-of-arrival-and-departure-and-automatic-identification-system (verify slug) | US AIS expansion | Free |
| Cutlip, K. (2017) "AIS for Safety and Tracking: A Brief History", Global Fishing Watch | Published 2017-03-31 (page modified 2025-10-02) | https://globalfishingwatch.org/article/ais-brief-history/ (canonical; also reachable at /data/ais-for-safety-and-tracking-a-brief-history/) | Arroyo interview; US origin story; purposes; 1998 New Orleans; 9/11; carriage thresholds; US 65-ft rule | Free |
| Kpler press release, acquisition of MarineTraffic and FleetMon | 15 Feb 2023 | https://www.kpler.com/ (press/newsroom) (verify direct URL) | Consolidation | Free |
| Kpler / Spire press releases, acquisition of Spire Maritime | Announced 13 Nov 2024; closed 25 Apr 2025; ~US$241 M total incl. service agreement | https://www.kpler.com/ and https://ir.spire.com/ (verify direct URLs) | Consolidation | Free |
| Garmin press release, acquisition of Vesper Marine | 3 Jan 2022 | https://www.garmin.com/en-US/newsroom/ (verify direct URL) | Consolidation | Free |
| IALA, entry into force of the Convention on the International Organization for Marine Aids to Navigation | 22 Aug 2024 | https://www.iala.int/ (news) (verify direct URL) | IALA becomes an IGO | Free |
| ITU-R M.2092 edition list | M.2092-0 (10/2015), M.2092-1 (2022), M.2092-2 (verify year) | https://www.itu.int/rec/R-REC-M.2092/en | VDES technical characteristics | Free |
| schwehr/gis-history README | commit as of 2026-10-04 (local clone) | https://github.com/schwehr/gis-history | ⟨H⟩ timeline entries | Free (CC0-1.0) |
| schwehr/libais repository | first public release 2010 | https://github.com/schwehr/libais | Open-source decoder written for the Deepwater Horizon response | Free (Apache-2.0) |
| Johnny Harris, *What's really happening in the ocean's "dark zones"* (YouTube `2tuS1LLOcsI`) | Published 10 Nov 2025 | https://www.youtube.com/watch?v=2tuS1LLOcsI | The "2025 video" named in PLAN ch. 6 — **not a GFW talk**; see `r-sources-gfw-bloomberg.md` | Free |

Secondary pointers used only for leads (must be backed by a primary source
before citation in a chapter): Wikipedia AIS/AISSat-1/NTS pages; eoPortal
mission pages; SFL (Space Flight Laboratory) mission pages; Maritime Executive
and Lloyd's List coverage of the Nov 2021 China feed drop; Black Hat / HITB
abstracts for the 2013 Trend Micro work.

---

## Verified facts

| Fact | Source (with clause/page where possible) | Confidence |
|---|---|---|
| The STDMA patent US 5,506,587 "Position indicating system", inventor Håkan Lans, assignee GP&C Systems International AB, was filed 1992-06-29 (PCT/SE92/00485, PCT pub. WO93/01576 of 1993-01-21), granted 1996-04-09, with earliest priority SE 9102034 of **1991-07-01** (also SE 9103542, 1991-11-28). Google Patents lists anticipated expiration 2013-04-09; status "Expired – Lifetime". | https://patents.google.com/patent/US5506587A/en (bibliographic header and "Applications Claiming Priority") | High |
| The first ITU technical standard, Rec. ITU-R M.1371-0, is dated 11/1998. Subsequent editions: -1 (08/2001), -2 (03/2006), -3 (06/2007), -4 (04/2010), -5 (02/2014), **-6 (02/2026)**. | https://www.itu.int/rec/R-REC-M.1371/en | High |
| IMO Res. MSC.74(69) Annex 3 (performance standards for a universal shipborne AIS) was adopted 12 May 1998. | IMO resolution header (imorules mirror; IMO Docs) | High |
| Revised SOLAS Chapter V (Res. MSC.99(73)) was adopted 5 Dec 2000 and entered into force 1 Jul 2002; Reg. V/19.2.4 requires AIS on all ships ≥ 300 GT on international voyages, cargo ships ≥ 500 GT not on international voyages, and all passenger ships irrespective of size; phase-in originally ran to 1 Jul 2008 for non-international-voyage ships. | https://www.imo.org/en/OurWork/Safety/Pages/AIS.aspx ; USCG NAVCEN AIS requirements page | High |
| The SOLAS Conference of Contracting Governments (London, 9–13 Dec 2002) adopted amendments (Resolution 1) that created Ch. XI-2 / ISPS and accelerated AIS carriage for ships 300–50,000 GT (other than passenger ships and tankers) to the first safety-equipment survey after 1 Jul 2004 or **31 Dec 2004, whichever earlier**; in force 1 Jul 2004. | IMO ISPS/SOLAS XI-2 page; ClassNK technical information; SMA brochure p. 12 ("The new completion date for implementation was 2004") | High |
| SMA brochure chronology: Benny Pettersson (SMA pilot) conceived the need in 1965 (typhoon off Kobe); mid-1980s tests with manufacturers; **1990** SMA Director General Kaj Janérus approved development with **SEK 2 million**; AVMS (Automatic Vessel Monitoring System) tested on Sweden–Finland ferries; Sweden/Finland first to implement maritime DGPS per IALA standard; 1992 AVMS maker failed, concept sold to Saab for military use; Lans's GP&C transponder evaluated by Swedish Space Corporation and Civil Aviation Administration; **1993** trials began with Trollhätte canal / Lake Vänern administrations and Styrsöbolaget ferries (Gothenburg), ~10 ferries + pilot boats, NorControl VTS display modified; **1994** raised at IMO, system then called **"4S"** (ship-to-ship, ship-to-shore); **1997** IMO requirement specification named "AIS" and request to ITU for two VHF channels; **1997** ITU decision; **1998** first ITU standard; Lans dropped royalty claims for ships under IMO carriage after some countries opposed mandatory patented equipment (Lans had accepted the ITU Code of Practice); 2000 SOLAS decision; IEC test standard approved **2002**; Saab TransponderTech took over product from Swedish Space Corporation. | https://www.sjofartsverket.se/globalassets/framtidens-sjofart/foi/ais_eng.pdf pp. 6–12 | High (for what the brochure says); Medium (as independent history — single national source) |
| SMA brochure technical summary: 2,250 slots/min, 26.6 ms slots, 256 bits per slot at 9,600 bit/s with 88 bits overhead and 168 bits payload; dynamic reports every 2–12 s under way, every 3 min at anchor; static/voyage data every 6 min. | Same PDF, pp. 8–9 (R. Zetterberg) | High (matches M.1371) |
| GFW history article: by Kimbra Cutlip, published 31 Mar 2017; quotes USCG Program Analyst **Jorge Arroyo**; traces US origin to *Exxon Valdez* (24 Mar 1989) → OPA-90 → USCG tanker tracking in Alaska; names UK Dover Strait VHF trials, Panama Canal Commission UHF trials, and a Swedish protocol; three purposes (collision avoidance, VTS, coastal surveillance); 1998 USCG VTS modernization with New Orleans as first primarily AIS-based port; 9/11 accelerated; US 65-ft commercial rule, fishing-vessel exemption ended March 2016; EU 15 m fishing-vessel rule 2009. | https://globalfishingwatch.org/article/ais-brief-history/ (text extracted 2026-10-04) | High (for what it says) |
| **Error in the GFW article:** it states SOLAS required AIS on "all tankers and passenger vessels equal to or greater than 150 gross tons"; SOLAS V/19.2.4 actually applies to all passenger ships irrespective of size and to ships ≥ 300 GT on international voyages (tankers are not given a separate 150 GT threshold). The article also spells VHF as "VHS" throughout and duplicates one paragraph. | Compare article text with IMO AIS page | High |
| The GFW article's "more detailed presentation on the history of AIS" link is broken: it points to `https://192.168.1.66/sites/default/files/pdf/AIS/Arroyo@NMFS-PAC.pdf` (a private IP). The USCG overview link is `https://www.navcen.uscg.gov/?pageName=AISmain`. | Extracted from article HTML 2026-10-04 | High |
| US interim rule *Automatic Identification System; Vessel Carriage Requirement*, 68 FR 39353, published 1 Jul 2003, one of six MTSA-2002 interim rules; aligned with the Dec 2002 SOLAS amendments. | federalregister.gov (68 FR 39353) | High |
| US final rule 80 FR 5282 (30 Jan 2015) expanded AIS carriage (33 CFR 164.46); most provisions effective 2 Mar 2015; the AIS carriage paragraphs (b) and (c) were delayed pending OMB approval and became effective 7 Apr 2016; newly covered vessels had to fit AIS by 1 Mar 2016. | federalregister.gov 80 FR 5282 and the 2016 effective-date notice; eCFR 33 CFR 164.46 | High |
| IEC 61993-2 Ed. 1.0 (Class A AIS test standard) published 2001; current edition is Ed. 3 (2018). IEC 62287-1 Ed. 1 (Class B "CS" CSTDMA) published 2006; current edition 2017 (+ amendments). | IEC webstore listings (iec.ch) | Medium (edition years from catalogue summaries; confirm month on webstore) |
| IMO Res. MSC.246(83) (AIS-SART performance standards) adopted 8 Oct 2007; applies to AIS-SARTs installed on or after 1 Jan 2010; AIS-SART accepted as a SOLAS search-and-rescue locating device from 1 Jan 2010; test standard IEC 61097-14. | IMO resolution; imorules mirror | High |
| Satellite AIS firsts: **NTS (CanX-6)**, COM DEV / UTIAS-SFL, launched 28 Apr 2008 on PSLV; **AISSat-1** (Norway; SFL-built GNB nanosat ~6–7 kg) launched 12 Jul 2010 on PSLV-C15 from Sriharikota; **NORAIS** (FFI / Kongsberg Seatex) on ESA Columbus module of the ISS began operating June 2010; **ORBCOMM OG2** first six satellites launched 14 Jul 2014 on Falcon 9 (AIS payloads); **Spire Lemur-2** first four satellites launched 28 Sep 2015 on PSLV (AstroSat mission); **exactView RT** = 58 L3Harris-built hosted payloads on Iridium NEXT, launches Jan 2017–Jan 2019, constellation declared complete 5 Feb 2019; exactEarth acquired by Spire 2021. | SFL mission pages; eoPortal; ESA NORAIS page; Iridium; Spire | Medium–High (dates consistent across sources; cite mission pages in chapters) |
| MarineTraffic began in 2007 as an academic project of Prof. Dimitris Lekkas, University of the Aegean (Ermoupoli, Syros); trial version late 2007; acquired by Kpler (announced 15 Feb 2023, together with FleetMon). | Kpler press release 2023-02-15; MarineTraffic "about" history | Medium (founding detail from secondary summaries) |
| Kpler acquired Spire's maritime business: announced 13 Nov 2024; closed 25 Apr 2025; ~US$233.5 M purchase price + US$7.5 M service agreement (~US$241 M); UK CMA merger inquiry opened mid-2025. | Spire investor release; Kpler release; gov.uk CMA case page | Medium–High |
| Garmin announced acquisition of Vesper Marine (Auckland, NZ; Cortex VHF/AIS) on 3 Jan 2022; terms undisclosed. | Garmin newsroom | High |
| In the first half of Nov 2021, after China's Personal Information Protection Law took effect (1 Nov 2021) alongside the Data Security Law, terrestrial AIS data from Chinese waters available to foreign aggregators fell sharply (figures cited range from ~45 % to ~90 %, the latter from VesselsValue via Reuters). | Reuters (Nov 2021); Maritime Executive; Lloyd's List | Medium (percentages differ by source; cite Reuters directly) |
| IALA's Convention entered into force 22 Aug 2024; IALA became an intergovernmental organization renamed "International Organization for Marine Aids to Navigation" (acronym retained); first General Assembly as IGO in Singapore, Feb 2025. | iala.int news | High |
| VDES: Rec. ITU-R M.2092-0 approved 10/2015; M.2092-1 2022; WRC-19 made the satellite (VDE-SAT) allocations. | ITU rec page; WRC-19 final acts | Medium–High |
| Global Fishing Watch was launched 15 Sep 2016 at the Our Ocean conference (Washington, DC) by Oceana, SkyTruth and Google; became an independent non-profit in 2017. | GFW site footer ("Founded by Oceana, SkyTruth and Google"); Oceana | High |
| libais was written by Kurt Schwehr in 2010 for the Deepwater Horizon response (replacing the slower Python `noaadata`); C++ core with Python bindings; used by NOAA ERMA and Whale Alert. | https://github.com/schwehr/libais ; UNH CCOM page; gis-history ⟨H⟩ | High |
| USCG NAIS program chartered Dec 2004 under MTSA; Increment 1 (receive at 58 ports / 11 waterways) full operational capability 30 Sep 2010; Increment 2 transceivers to ~24 nmi transmit / 50 nmi receive; Increment 3 adds satellite coverage to ~2,000 nmi; transitioned to sustainment Aug 2018. | DHS/USCG acquisition summaries (verify specific document) | Medium |
| New Orleans VTS: USCG awarded Lockheed Martin a PAWSS integration contract in 1998 (MTM200 system; Lower Mississippi from Baton Rouge to the Gulf); GFW article says New Orleans was designated the first primarily AIS-based US VTS in 1998. | GFW article; Lockheed/USCG PAWSS references (verify) | Medium |
| Trend Micro researchers Balduzzi, Wilhoit and Pasta presented "AIS Exposed" at Hack in the Box Kuala Lumpur, Oct 2013 (later ACSAC 2014 paper). | Black Hat/HITB abstracts | High |
| Costa Concordia grounding: 13 Jan 2012; Sewol capsizing: 16 Apr 2014. | Official reports (MIT Italy; KMST) — cite in `r-incidents.md` | High |
| Lans's unrelated US litigation (colour-graphics patent US 4,303,986; suits against Gateway, Dell et al., 1997) ended in dismissal for lack of standing (patent had been assigned to his company Uniboard AB) and an award of defendants' attorney fees; this is the "chilling lesson" mentioned in PLAN ch. 17/18. | Reported case summaries (*Lans v. Digital Equipment Corp.*, D.D.C.; Fed. Cir. 2001) (verify neutral citations) | Medium |

---

## Notes and quotes

**From the SMA brochure (primary, free PDF; page numbers are the booklet's).**

- Captain Bengt Viknander (Stena Danica): "AIS has meant a great deal for maritime
  safety." (p. 3)
- Benny Pettersson on the 1965 typhoon: "It was impossible to see – by sight or by
  radar – if there were other ships nearby." (p. 6) and "Owners of big luxury
  yachts showed greater interest in technology than shipping companies. The only
  explanation I can find is that shipping is – or at least has been – a
  conservative business." (p. 7)
- On 9/11: "The major breakthrough for the Swedish concept came in connection
  with the 9/11 terrorist attacks in 2001. 'Then resistance broke, and we won the
  support worldwide for the Swedish proposal … I even presented a lecture at the
  Pentagon.'" (p. 7)
- On patents: "despite Håkan Lans accepting the ITU's Code of Practice for
  standardized patented systems, some countries strongly opposed the idea of
  making patented equipment mandatory onboard. Finally, Håkan Lans dropped the
  claim for compensation for the use of the patent on ships covered by the IMO's
  carriage requirements, thereby permitting a consensus to base the transponder
  system on the Swedish proposal. The ITU published the first version of the
  standard in 1998." (p. 12)
- On naming: "The system was now called the '4S' system, a reference to
  ship-to-ship, ship-to-shore applications." (p. 12)
- People named: Benny Pettersson, Bertil Arvidsson, Kaj Janérus, Bo Tryggö,
  Håkan Lindley, Rolf Zetterberg (SMA); Rolf Bäckström (Finnish Maritime
  Administration); Håkan Lans (inventor); Saab TransponderTech; NorControl.

**From the GFW article (Cutlip 2017), Arroyo quotes with attribution.**

- "The British were testing a VHS [sic] -based tracking system for ships going in
  and out of the Dover Strait," Arroyo says. "The Panama Canal Commission was
  testing a UHF system, and Swedes were developing another protocol."
- The intent, per Arroyo, was to improve "situational awareness" for navigators
  and provide tracking for shore-based VTS "akin to Air Traffic Control".
- "Its three primary purposes were: 1] Collision avoidance 2] Vessel Traffic
  Service 3] Coastal Surveillance."
- "By 1998, the U.S. Coast Guard had embarked on a plan to modernize their entire
  vessel tracking service network … New Orleans was designated as the first port
  to adopt a primarily AIS-based system."
- "When the regulations were first drawn up in 2003, vocal pushback from industry
  led the Coast Guard to exempt fishing vessels and passenger vessels with fewer
  than 150 passengers from the 65-foot threshold … Last March (2016), the full AIS
  regulations went into effect."

**Narrative notes.**

- Two origin stories coexist and are both true: the *American* one (OPA-90 →
  USCG tanker tracking → VTS modernization → 9/11) told by Arroyo/GFW, and the
  *Swedish* one (Pettersson → SMA → Lans/GP&C → IALA/IMO/ITU) told by SMA. The
  chapters should present them as converging streams, with the UK Dover and
  Panama UHF trials as the third and fourth streams that lost out.
- The patent royalty story is central to ch. 17/18: Lans accepted ITU's
  (RAND-style) Code of Practice but IMO member states still balked at a mandated,
  patented system; the compromise was a royalty waiver *for SOLAS-mandated ships*.
  The US patent's anticipated expiry (2013-04-09) and 1991 Swedish priority should
  be stated precisely; the PLAN's "Swedish patent 1989" is not supported by the
  Google Patents record and must be corrected or verified against the Swedish
  PRV register.
- The 2002 acceleration is often misdescribed as "9/11 made AIS mandatory". AIS
  was already mandatory from the Dec 2000 SOLAS V revision (in force 1 Jul 2002);
  what 9/11 and the Dec 2002 conference did was compress the phase-in for the
  large middle band of cargo ships from 2007/2008 to 31 Dec 2004.
- Satellite AIS has two independent roots: Canadian (COM DEV/SFL, NTS 2008 →
  exactEarth) and Norwegian (FFI/Kongsberg Seatex/SFL, AISSat-1 and NORAIS 2010),
  followed by US commercial (ORBCOMM OG2 2014, Spire 2015) and the hosted-payload
  model (exactView RT on Iridium NEXT). Chapter 39 should keep the receive-only
  framing: no M.1371 downlink has ever been operational from orbit (VDE-SAT
  experiments are a different thing; see `r-vdes.md`).
- The 2021 China event is the clearest modern example that "AIS data" is not a
  single global commons: the *radio* broadcasts continued; what collapsed was
  the *terrestrial aggregation feed* to foreign providers.

---

## Open questions / (verify)

- (verify) The Swedish national patent(s) behind US 5,506,587 — SE 9102034
  (1991-07-01) and SE 9103542 (1991-11-28) — their grant numbers, and whether any
  **1989** Swedish filing exists as PLAN ch. 9 asserts. Check PRV/Espacenet
  family for SE 468 989? (number not confirmed — do not cite).
- (verify) EP and other family members (EP 0 592 560? — unconfirmed) and their
  expiry dates for ch. 18.
- (verify) The "ITU decision in 1997" referenced by SMA — likely WRC-97
  identification of AIS 1/AIS 2 channels in RR Appendix 18; confirm the WRC-97
  resolution/footnote number.
- (verify) IMO 1994 agenda item: which NAV sub-committee session first took up
  transponders (NAV 40?) and which MSC resolution first requested ITU action.
- (verify) Dover Strait VHF trials (UK MCA/Trinity House, early 1990s) and Panama
  Canal Commission UHF transponder trials — find primary reports; Arroyo's
  interview is the only source so far.
- (verify) USCG post-*Exxon Valdez* Prince William Sound tracking system
  specifics (OPA-90 §4107? and the Valdez VTS upgrade) — cite the statute section
  and the USCG report.
- (verify) PAWSS/New Orleans dates: 1998 Lockheed award vs. first AIS-based VTS
  operations; find the USCG or GAO document.
- (verify) NAIS increment dates and the 2018 sustainment transition — cite the
  DHS acquisition decision memo or GAO report (GAO-11-… ?).
- (verify) IEC 61993-2 Ed. 1 publication month (2001) and whether an interim
  "IEC 61993-2 (2001-12)" date is correct; IEC 62287-1 Ed. 1 month (2006).
- (verify) AISHub founding year and founder; FleetMon founding (Rostock, 2007?).
- (verify) Exact Reuters headline/date for the Nov 2021 China AIS story and the
  VesselsValue 90 % figure.
- (verify) ITU-R M.2092-2 approval date and whether M.2092-1 is 2022-02.
- (verify) MSC.570(109) — reportedly new AIS performance standards applying to
  ships with building contracts/delivery on or after 1 Jan 2029; confirm number,
  adoption date and scope (would be a major addition to ch. 10/15 and App. B).
- (verify) Content of M.1371-6 (02/2026): what changed from -5 (this affects every
  protocol chapter; PLAN currently treats -5 as current).
- (verify) The broken "detailed presentation" link in the GFW article —
  `Arroyo@NMFS-PAC.pdf` — probably a USCG NAVCEN slide deck given to NMFS Pacific;
  try archive.org or NAVCEN.
- (verify) Neutral citations for *Lans v. Digital Equipment Corp.* (D.D.C. 1999;
  Fed. Cir. 2001) and *Uniboard AB v. Acer* for ch. 17.

---

## Candidate figures and worked examples

1. **Master timeline (App. A, ch. 9–12):** a single horizontal timeline from 1912
   (Titanic) to 2026 (M.1371-6), colour-coded by stream: *regulatory*
   (SOLAS 1914, MSC.74(69) 1998, MSC.99(73) 2000, Dec 2002 conference, 68 FR
   39353 2003, 80 FR 5282 2015, IALA IGO 2024), *technical* (STDMA priority 1991,
   M.1371-0 1998, -1 2001, -2 2006, -3 2007, -4 2010, -5 2014, -6 2026; M.2092
   2015), *systems* (AVMS, GP&C trials 1993, New Orleans VTS 1998, NAIS 2004–18),
   *space* (NTS 2008, AISSat-1/NORAIS 2010, OG2 2014, Lemur-2 2015, Iridium NEXT
   2017–19), *data ecosystem* (MarineTraffic 2007, libais 2010, Whale Alert 2012,
   GFW 2016, China feed drop 2021, Kpler 2023/2025).
2. **"Four streams converge" diagram (ch. 9):** Sweden/Finland (SMA, GP&C, 4S) ·
   USA (OPA-90, USCG) · UK (Dover VHF) · Panama (UHF) → IMO 1994–98 → ITU 1998.
3. **Phase-in table (ch. 10):** SOLAS V/19 original phase-in (2002–2008) side by
   side with the Dec 2002 accelerated dates; highlight the 300–50,000 GT band.
4. **Worked example (ch. 10/18):** patent term arithmetic — PCT filing 1992-06-29,
   US grant 1996-04-09, 17-years-from-grant vs. 20-years-from-filing transition
   rule → anticipated expiry 2013-04-09 (explain why Google Patents shows that
   date).
5. **Worked example (ch. 9):** the SMA brochure's slot budget — 60 s / 2,250 =
   26.67 ms; 26.67 ms × 9,600 bit/s = 256 bits; 256 − 88 overhead = 168 payload
   bits — as an on-ramp to ch. 21/28.
6. **Satellite-AIS lineage chart (ch. 39):** two root nodes (Canada: NTS →
   exactEarth → exactView RT → Spire → Kpler; Norway: AISSat-1 → AISSat-2/-3 →
   NorSat; plus ORBCOMM OG2 and Spire Lemur-2).
7. **Consolidation map (ch. 12/41):** who owns what in 2026 (Kpler ⊃ MarineTraffic,
   FleetMon, Spire Maritime ⊃ exactEarth; Garmin ⊃ Vesper; ORBCOMM independent).

---

## gis-history import (`⟨H⟩` entries)

All entries below are copied from the local clone of
`schwehr/gis-history/README.md` (CC0-1.0) with the gis-history date kept, per
STYLE_GUIDE §6. Grouped by the chapter(s) they feed. Items in the TASKS Phase 0
list are marked ★. Adjacent items (useful for *Then & now* boxes) are included
without ★.

**Navigation, radio and radar prehistory (ch. 9, 25, 27)**
- ⟨H⟩ 206 BC — Compass invented; not used for navigation until the 11th century.
- ⟨H⟩ 1569 — Mercator projection.
- ⟨H⟩ 1656 — Pendulum clock.
- ⟨H⟩ 1731 — Sextant first implemented.
- ⟨H⟩ 1761 — H4 marine chronometer (Harrison).
- ⟨H⟩ 1807 — US funds the Coast Survey that later became NOAA.
- ⟨H⟩ 1884 — International Meridian Conference.
- ⟨H⟩ 1902 — Atlas Elektronik founded.
- ⟨H⟩ 1903 — GEBCO started.
- ⟨H⟩ 1904 — Radar: beginnings of detecting remote metal objects.
- ⟨H⟩ 1912 — Sinking of the RMS Titanic.
- ⟨H⟩ 1913 — Sonar: first echo-sounder patent.
- ⟨H⟩ 1914 — ★ International Convention for the Safety of Life at Sea (SOLAS).
- ⟨H⟩ 1917 — Nautical time standard developed.
- ⟨H⟩ 1928 — Universal Time (UT).
- ⟨H⟩ 1931 — ★ Simrad founded; became the start of Kongsberg Maritime.
- ⟨H⟩ 1940 — Gee radio navigation; Project 3 (LORAN predecessor).
- ⟨H⟩ 1942 — Decca Navigator; first INS; LORAN.
- ⟨H⟩ 1948 — *A Mathematical Theory of Communication* (Shannon).
- ⟨H⟩ 1949 — Atomic clock (ammonia); ⟨H⟩ 1955 — Cesium atomic clock (Atomichron).
- ⟨H⟩ 1957 — Sputnik 1.
- ⟨H⟩ 1958 — Kalman filter.
- ⟨H⟩ 1960 — Coordinated Universal Time (UTC) starts.
- ⟨H⟩ 1969 — CHAYKA (Russian LORAN-like system).
- ⟨H⟩ 1970 — Unix time 0; NOAA formed.
- ⟨H⟩ 1973 — ★ Air traffic control radar beacon system (ATCRBS) — gis-history
  itself flags "??? or was this 1961?" → (verify) before use.
- ⟨H⟩ 1974 — LORAN-C opened to civilian use.
- ⟨H⟩ 1979 — Network Time Protocol (NTP).
- ⟨H⟩ 1984 — ★ NMEA 0183 first released; WGS84/EGM84.
- ⟨H⟩ 1985 — Cellular telephone first introduced.
- ⟨H⟩ 1989 — Garmin founded (as ProNav); RINEX.
- ⟨H⟩ 1996 — Differential GPS: first production-quality transmissions (gis-history
  asks about Maritime DGPS in the 1980s → reconcile with SMA brochure, which says
  Sweden/Finland were first to implement maritime DGPS per the IALA standard,
  early 1990s).
- ⟨H⟩ 1997 — Wi-Fi introduced.

**GNSS (ch. 24, 25, 62)**
- ⟨H⟩ 1978 — ★ GPS first satellite launched.
- ⟨H⟩ 1982 — ★ GLONASS first launch.
- ⟨H⟩ 2000 — ★ BeiDou first satellite launched.
- ⟨H⟩ 2000 — ★ Selective Availability disabled.
- ⟨H⟩ 2003 — ★ WAAS first launched (gis-history wording; WAAS was commissioned
  for IFR use in July 2003 — (verify) phrasing before citing).
- ⟨H⟩ 2011 — ★ Galileo first launch (2005 test satellite; operational 2016).

**Law (ch. 16)**
- ⟨H⟩ 1982 — ★ UNCLOS signed; ⟨H⟩ 1994 — ★ UNCLOS effective.

**AIS core (ch. 10–12, 44)**
- ⟨H⟩ 1998 — ★ M.1371-0, first specification of AIS (links to
  https://www.itu.int/rec/R-REC-M.1371-0-199811-S/en).
- ⟨H⟩ 2002 — ★ AIS mandated for large ships (Wikipedia pointer; use SOLAS
  MSC.99(73) as the primary source).
- ⟨H⟩ 2010 — ★ Deepwater Horizon oil spill.
- ⟨H⟩ 2010 — ★ Kurt Schwehr released the first version of libais (for the DWH
  spill).
- ⟨H⟩ 2012 — ★ Whale Alert released / presented to US Congress (Google Slides
  link in gis-history).
- ⟨H⟩ 2013 — ★ "All the Ships" — Google I/O talk about geospatial in Google Cloud
  (http://youtu.be/MT7cd4M9vzs).
- ⟨H⟩ 2016-09 — ★ Global Fishing Watch launched.
- ⟨H⟩ 2001 — SkyTruth founded (GFW co-founder).
- ⟨H⟩ 2006 — NOAA ERMA started (libais consumer).

**Software and data stack used in Parts VII–VIII (ch. 44, 45, 47–50)**
- ⟨H⟩ 1890 — ★ Peano curve; ⟨H⟩ 1891 — ★ Hilbert curve (space-filling indexes
  for ch. 50).
- ⟨H⟩ 1974 — Quadtree invented.
- ⟨H⟩ 1992 — ★ Terralens (Kongsberg Geospatial, formerly InterMAPhics) — VTS/C2
  mapping SDK lineage for ch. 45/46.
- ⟨H⟩ 1992 — Python first appeared; ⟨H⟩ 1994 — Blender initial release;
  ⟨H⟩ 2002 — Blender released as open source (ch. 45).
- ⟨H⟩ 2000 — GDAL first release; SQLite initial release.
- ⟨H⟩ 2001 — PostGIS initial release; ⟨H⟩ 2002 — QGIS initial release; GEOS first
  commit.
- ⟨H⟩ 2004 — OpenStreetMap; Google MapReduce paper; AWS start.
- ⟨H⟩ 2005 — git initial release; Google Maps launched.
- ⟨H⟩ 2008 — GeoJSON specification; KML becomes an OGC standard.
- ⟨H⟩ 2009 — Google Ocean in Google Earth; Earth Engine started.
- ⟨H⟩ 2010 — Leaflet first commit; Planet Labs founded; Mapbox founded.
- ⟨H⟩ 2011 — CesiumJS started; IPython Notebook.
- ⟨H⟩ 2013-06 — geopandas first commit.
- ⟨H⟩ 2014 — Sentinel-1 first launch (SAR for dark-vessel detection, ch. 6/66).
- ⟨H⟩ 2015-04 — Apache Sedona first commit; ⟨H⟩ 2015-01 — Dask.
- ⟨H⟩ 2016-01 — deck.gl started; ⟨H⟩ 2018-03 — kepler.gl first commit.
- ⟨H⟩ 2018-07 — DuckDB first commit.
- ⟨H⟩ 2018-12 — MovingPandas first commit.
- ⟨H⟩ 2021 — GeoParquet spec first commit.
- ⟨H⟩ 2024-11 — "Mapping the ionosphere with millions of phones" (Nature) —
  analogue for crowd-sourced sensing (ch. 29/65).

**Not in gis-history but needed as `⟨+⟩` in App. A (all verified above):** Lans
priority 1991; IMO 1994 "4S"; MSC.74(69) 1998; MSC.99(73) 2000; Dec 2002 SOLAS
conference; 68 FR 39353 2003; IEC 61993-2 2001; IEC 62287-1 2006; MarineTraffic
2007; MSC.246(83) 2007; NTS 2008; AISSat-1/NORAIS 2010; OG2 2014; M.2092 2015;
Lemur-2 2015; 80 FR 5282 2015; Iridium NEXT complete 2019; China feed drop 2021;
Garmin–Vesper 2022; Kpler–MarineTraffic 2023; IALA IGO 2024; Kpler–Spire
Maritime 2025; M.1371-6 2026.

---

## Recommended use by chapter

- **Ch. 1 (What AIS is):** the "three purposes" list, quoted from Arroyo/GFW, and
  the SMA slot-budget paragraph as the first *On the wire* taste.
- **Ch. 4 (VTS):** New Orleans 1998 as first AIS-centric US VTS (GFW/Arroyo), with
  PAWSS/Lockheed detail only once (verify)-cleared; SMA's NorControl display
  modification 1993 as the first VTS–transponder integration.
- **Ch. 6 (Fisheries):** the "2025 GFW video" is actually Johnny Harris's
  10 Nov 2025 piece built on GFW data (see companion dossier); cite GFW's 15 Sep
  2016 launch ⟨H⟩ and the EU 15 m rule (2009) from the GFW article.
- **Ch. 9 (Prehistory):** the SMA brochure as the spine (Pettersson 1965 → 1990
  funding → AVMS → GP&C 1993 → 4S 1994); Arroyo's Dover/Panama/Sweden triad; patent
  facts (priority 1991-07-01, grant 1996-04-09, expiry 2013-04-09); ⟨H⟩ Titanic
  1912 → SOLAS 1914; ⟨H⟩ radar 1904; ⟨H⟩ ATCRBS (verify year).
- **Ch. 10 (Standardization):** MSC.74(69) 12 May 1998; M.1371-0 11/1998;
  MSC.99(73) 5 Dec 2000 / 1 Jul 2002; Dec 2002 conference → 31 Dec 2004; 68 FR
  39353; IEC 61993-2 Ed. 1 (2001); SMA "test standard approved 2002"; correct the
  GFW article's "150 gross tons" error in a *Definitions that bite* box.
- **Ch. 11 (Growth):** IEC 62287-1 2006; MarineTraffic 2007; MSC.246(83) 2007 /
  2010; NTS 2008; AISSat-1 + NORAIS 2010; libais 2010 ⟨H⟩; Whale Alert 2012 ⟨H⟩;
  Trend Micro Oct 2013; OG2 2014; NAIS Increment 1 FOC 2010.
- **Ch. 12 (2015–present):** 80 FR 5282 (effective dates 2016); M.2092 2015; Lemur-2
  2015; GFW 2016 ⟨H⟩; Iridium NEXT/exactView RT 2019; China Nov 2021; Garmin–Vesper
  Jan 2022; Kpler Feb 2023 and Apr 2025; IALA IGO 22 Aug 2024; **M.1371-6
  Feb 2026** (flag in *Then & now*).
- **Ch. 17/18 (Law, patents):** Lans royalty waiver (SMA p. 12); patent family and
  expiry; the unrelated colour-graphics litigation as the standing/fees cautionary
  tale (verify citations).
- **Ch. 39 (Satellite AIS):** mission dates table from the Verified facts.
- **Ch. 41 (Providers):** consolidation facts and the 2021 China feed episode.
- **Ch. 44 (Open-source decoders):** libais 2010 ⟨H⟩ origin; hand off repository
  archaeology to `r-history-oss.md`.
- **App. A:** merge the ⟨H⟩ list in §9 with the ⟨+⟩ list at its end.
