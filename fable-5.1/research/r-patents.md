# Dossier: Patents and intellectual property in AIS

**Purpose.** This dossier collects what can be confirmed, as of October 2026,
about the patents that shaped AIS: the Håkan Lans / GP&C "Position indicating
system" family that covers STDMA/SOTDMA (priority 1991, US grant 1996, EP grant
1997, US claims cancelled on reexamination 2010, all members expired), the
Johnson/Lesch "Multiple access communication system for moveable objects"
patent that covers the carrier-sense scheme used by Class B "CS" transponders
(US 7,512,095; SRT acquired a share in 2015), the satellite-AIS decollision and
anomaly-detection families held by COM DEV/exactEarth (now Spire → Kpler),
ORBCOMM, CNES and Harris, the Saab "validity check" patent, and the Spire
"AIS spoofing and dark-target detection" patent. It also records how the
ITU-R/IEC/ISO common patent policy handles declarations and why the Class B CS
scheme was deliberately designed around the Lans IPR. It feeds **Chapter 18**
(Patents) primarily, and supplies material to **Chapter 9** (Lans and STDMA),
**Chapter 10** (the IMO/ITU royalty question in 1996–1998), **Chapter 11**
(Class B 2006 and the CSTDMA choice), **Chapter 17** (Lans litigation; SRT
licensing demands), **Chapter 20/21** (why Class B CS exists), **Chapter 30/39**
(satellite decollision techniques as claimed), **Chapter 59** (spoof-detection
claims), **Chapter 33** (OEM landscape; SRT), and **Appendix A** (timeline).

> Research-session note. Patent bibliographic facts marked *high* were read
> directly from Google Patents record pages (which mirror USPTO/EPO/DOCDB
> data) or from the Google Patents search endpoint during this session on
> 2026-10-05. Legal-status fields on Google Patents ("Expired - Lifetime",
> "Anticipated expiration", "Adjusted expiration") are Google's computed
> estimates, not legal conclusions; they are reported as such. The USPTO
> reexamination certificate and the IEC/ITU declaration databases could not be
> opened directly (JS forms / 404) and are marked *medium* or *(verify)*.

## Key questions

1. What exactly did the Lans/GP&C patent family claim, when was it filed,
   granted, and when did it expire in each jurisdiction?
2. Was the US patent ever invalidated? (Yes — ex parte reexamination
   certificate, 2010, all claims cancelled; confirm the certificate number.)
3. How did IMO/ITU/IEC handle the Lans IPR when AIS was standardized
   (1996–1998) and when Class B was standardized (2003–2006)? What
   declarations exist in the ITU-R and IEC patent databases?
4. Why was Class B built on carrier-sense TDMA rather than SOTDMA, and who
   held (and holds) the CSTDMA patent? What happened when SRT acquired it in
   2015 and asked for royalties?
5. Which patents cover satellite-AIS reception (decollision, field-of-view
   segmentation, Doppler separation, on-board processing), who owns them now
   after the COM DEV → exactEarth → Spire → Kpler chain, and which are live?
6. Which patents cover AIS data analytics (position validity checks, anomaly
   detection, spoof/dark-target detection) that chapters 47/59 may describe?
7. What is the "chilling lesson" of Lans's US litigation (the unrelated colour
   graphics patent) and how should the book tell it accurately?
8. What is a realistic "what is expired / what is live" table for 2026?

## Primary sources located

| Source | Identifier / edition / year | URL | What it covers | Access |
|---|---|---|---|---|
| US patent (Lans) | US 5,506,587 A, "Position indicating system", granted 1996-04-09 | https://patents.google.com/patent/US5506587A/en | The STDMA/SOTDMA claims; priority SE 9102034 (1991-07-01) and SE 9103542 (1991-11-28); PCT/SE92/00485 filed 1992-06-29; WO 93/01576 | Free |
| European patent (Lans) | EP 0 592 560 B1, granted 1997-08-27 | https://patents.google.com/patent/EP0592560B1/en | Same family; EP filed 1992-06-29; A1 published 1994-04-20 | Free |
| Swedish patent (Lans) | SE 468 452 B, published 1993-01-18 (application SE 9102362 filed 1991-08-15) | https://patents.google.com/patent/SE468452B/en | National Swedish grant in the family ("Position indicating system and position station …") | Free |
| PCT publication | WO 1993/001576 A1, published 1993-01-21 | https://patents.google.com/patent/WO1993001576A1/en | International publication of the family | Free |
| Wikipedia, "Håkan Lans" | accessed 2026-10-05 | https://en.wikipedia.org/wiki/H%C3%A5kan_Lans | Pointer to USPTO ex parte reexamination certificate (cited there as "certificate 7428, issued 30 March 2010"); colour-graphics litigation summary | Free (secondary) |
| Fed. Cir. decision | *Lans v. Digital Equipment Corp.*, 252 F.3d 1320 (Fed. Cir. 2001) | (search-confirmed citation; read the opinion on CourtListener/FindLaw before quoting) | Standing: inventor who assigned patent to his own company (Uniboard AB) could not sue; notice under 35 U.S.C. § 287 | Free |
| US patent (Johnson & Lesch) | US 7,512,095 B2, "Multiple access communication system for moveable objects", granted 2009-03-31 | https://patents.google.com/patent/US7512095B2/en | Carrier-sense ("listen before transmit") access for Class B; priority 2003-06-09 (provisional 60/477,125); filed 2004-06-07; assigned in part to Software Radio Technology plc 2015-02-26 | Free |
| Panbo (Ben Ellison) | "SRT acquires Class B AIS patent, consequences uncertain", 1 Jul 2015 | https://www.panbo.com/srt-acquires-class-b-ais-patent-consequences-uncertain/ | Documented account of the SRT acquisition, IEC TC80/WG15 history, Joe Hersey (ret. USCG) on the record, SRT CEO statement, royalty email (5 % of net retail, ~US$35/unit) | Free (secondary, but quotes primary emails/statements) |
| US patent (COM DEV) | US 7,876,865 B2, "System and method for decoding automatic identification system signals", granted 2011-01-25 (priority 2007-06-08; inventor Robert Peach) | https://patents.google.com/patent/US7876865B2/en | Satellite AIS decollision / decoding | Free |
| US patent (COM DEV) | US 8,780,788 B2, "Systems and methods for decoding automatic identification system signals", granted 2014-07-15 (priority 2009-09-25; Peach) | https://patents.google.com/patent/US8780788B2/en | Second-generation decollision | Free |
| US patent (COM DEV) | US 9,015,567 B2, "Methods and systems for consistency checking and anomaly detection in automatic identification system …", granted 2015-04-21 (priority 2012-04-12; Peach) | https://patents.google.com/patent/US9015567B2/en | Data-quality / anomaly detection on satellite AIS | Free |
| EP patent (COM DEV) | EP 2 211 486 B1, "Satellite detection of automatic identification system signals", granted 2013-01-09 (priority 2009-01-27; inventor Phillip R. Cowles) | https://patents.google.com/patent/EP2211486B1/en | Satellite detection method; US counterpart published as US 2009/0161797 A1 (Cowles, priority 2007-06-08) | Free |
| CA patent (COM DEV) | CA 2,720,190 C, "Systems and methods for segmenting a satellite field of view for detecting …", granted 2016-05-10 (priority 2010-06-09; inventor Weiguo Chen) | https://patents.google.com/patent/CA2720190C/en | Field-of-view segmentation (multi-beam) for decollision; US app. US 2011/0304502 A1 | Free |
| US patent (exactEarth) | US 9,094,048 B2, "Methods and systems for enhanced detection of e-Navigation messages", granted 2015-07-28 (priority 2013-03-05; Baljinder S. Randhawa) | https://patents.google.com/patent/US9094048B2/en | Enhanced detection (exactEarth era) | Free |
| US patent (exactEarth) | US 9,842,504 B2, "Systems and methods for vessel position reporting and monitoring", granted 2017-12-12 (priority 2015-06-30; Christopher M. Short) | https://patents.google.com/patent/US9842504B2/en | Position reporting/monitoring (likely ABSEA/Class B satellite-enhanced reporting — (verify) scope) | Free |
| US patent (ORBCOMM) | US 7,809,370 B2, "Space based monitoring of global maritime shipping using automatic identification system", granted 2010-10-05 (priority 2006-05-30; John Stolte) | https://patents.google.com/patent/US7809370B2/en | ORBCOMM's early S-AIS claim | Free |
| US patent (CNES) | US 9,246,575 B2, "Method for detecting AIS messages", granted 2016-01-26 (priority FR 11 57849, 2011-09-05; de Latour & Faup); status Active, adjusted expiration 2033-10-23 | https://patents.google.com/patent/US9246575B2/en | Satellite AIS detection; **assigned to CNES, not COM DEV** (web summaries misattribute it) | Free |
| US patent (Harris) | US 9,729,374 B2, "Co-channel spatial separation using matched Doppler filtering", granted 2017-08-08 (priority 2015-08-07; Timothy F. Dyson) | https://patents.google.com/patent/US9729374B2/en | Doppler-based separation of co-channel bursts (Harris built the exactView RT payloads on Iridium NEXT) — (verify) that the specification names AIS | Free |
| US patent (Spire) | US 11,156,723 B2, "AIS spoofing and dark-target detection methodology", granted 2021-10-26 (priority 2016-04-04; Peter Platzer) | https://patents.google.com/patent/US11156723B2/en | Spoof/dark-target detection from satellite data | Free |
| US patent (Saab) | US 8,610,619 B2, "Validity check of vehicle position information", granted 2013-12-17 (priority 2008-06-18; Svante Andersson); EP 2 136 221 B1 granted 2013-10-09 | https://patents.google.com/patent/US8610619B2/en | Checking a reported AIS position against TDMA timing (relevant to ch. 59 detection) — (verify) claim details | Free |
| US patent (True Heading) | US 9,804,254 B2, "Method for determining the timing of the receipt of a radio message", granted 2017-10-31 (priority 2013-10-04; Nils Willart); US 9,807,554 B2 (priority 2012-11-09) | https://patents.google.com/patent/US9804254B2/en | Swedish Class B/AtoN maker's timing-based patents | Free |
| US patent (SRT) | US 9,473,197 B2, "Reversible TDD transceiver", granted 2016-10-18 (priority 2013-01-29; Phil Longhurst), assignee SRT Marine Technology Ltd | https://patents.google.com/patent/US9473197B2/en | SRT hardware patent | Free |
| US application (eOdyn) | US 2016/0290812 A1, "Method for calculating the surface speed of at least one vessel …", Yann Guichoux (priority 2013-11-12) | https://patents.google.com/patent/US20160290812A1/en | Surface-current retrieval from AIS (ch. 7/65) — (verify) whether granted | Free |
| ITU IPR portal | Common Patent Policy for ITU-T/ITU-R/ISO/IEC; Guidelines (applicable from 16 Dec 2022); declaration forms (2018) | https://www.itu.int/en/ITU-T/ipr/Pages/default.aspx | The three-option declaration regime (free of charge/RAND; RAND; neither) | Free |
| ITU-R patent database | "ITU-R Patent Statement and Licensing Declaration Information" | https://www.itu.int/ITU-R/go/patents/en and https://www.itu.int/net4/ipr/search.aspx?sector=ITU-R | Search form; M.1371 is a selectable Recommendation (results require interactive query) | Free |
| IEC patent declarations database | IEC "Patent declarations" (TC 80, IEC 62287) | https://patents.iec.ch/iec/pa.nsf/pa_h?OpenForm (verify URL) | Panbo reports a single 2007 declaration by Anders Håkan Lans for IEC 62287 (option 2, RAND) | Free |
| Swedish Maritime Administration brochure | "AIS — the Swedish story" (see `r-history.md`) | https://www.sjofartsverket.se/globalassets/framtidens-sjofart/foi/ais_eng.pdf | Lans accepted the ITU Code of Practice; dropped compensation claims for SOLAS-mandated ships | Free |
| Moberg Publications | "The Judgment against Håkan Lans — a planned judicial crime?" (partisan, Lans side) | https://mobergpublications.se/patents/ | Lans-side narrative of the US litigation; use only as a pointer | Free (advocacy) |

## Verified facts

| Fact | Source | Confidence |
|---|---|---|
| US 5,506,587 "Position indicating system": inventor Håkan Lans; original assignee GP & C Systems International AB; application US 08/170,167; PCT/SE92/00485 filed 29 Jun 1992; §371 date 23 Dec 1993; WO 93/01576 published 21 Jan 1993; granted 9 Apr 1996; 13 claims. | Google Patents US5506587A (abstract header and bibliographic block), read 2026-10-05 | high |
| Priority claims of the family: SE 9102034 (1 Jul 1991) and SE 9103542 (28 Nov 1991); an additional Swedish application SE 9102362 (filed 15 Aug 1991) is listed among "applications claiming priority". | Google Patents US5506587A "Applications Claiming Priority (7)" | high |
| Google Patents lists US 5,506,587 as "Expired - Lifetime" with "Anticipated expiration 2013-04-09" (17 years from grant — the pre-GATT transition rule gives the later of 17 years from grant or 20 years from filing; 20 years from 29 Jun 1992 = 29 Jun 2012). | Google Patents US5506587A legal events | high (that Google shows this); medium (as legal conclusion) |
| Claim 1 (abridged): a population of movable stations each knowing its position from a plurality of geometrically distributed transmitters, with "a time base common to all of said movable stations … defining time blocks which are standardized, enumerable and form a common, accurate, repeating maximal frame of known length", and "means for occupying a free time block in each maximal frame and for autonomously transmitting therein of a position signal in the common radio channel". | Google Patents US5506587A, Claims | high |
| The specification is written around civil aviation (ACC/FIC/FIR terminology; "Appendix X … potential applications for civil aviation"), not shipping. | Google Patents US5506587A, Description | high |
| EP 0 592 560 B1 (same title; applicant GP&C Systems International AB): filed 29 Jun 1992; A1 published 20 Apr 1994; granted 27 Aug 1997; Google lists "Anticipated expiration 2012-06-29" and "Expired - Lifetime". | Google Patents EP0592560B1 | high |
| Family members by country (DOCDB, as listed on the EP record): AT E157474 T1; AU 661706 B2; BR 9206225 A; CA 2111980 C; DE 69221871 T2; DK 0592560 T3; ES 2109366 T3; FI 109492 B; GR 3025456 T3; JP 3262332 B2; KR 100238959 B1; NO 309670 B1; RU 2108627 C1; US 5506587 A; WO 93/01576 A1. | Google Patents EP0592560B1, "Also published as" | high |
| Swedish national patent SE 468 452 B ("Position indicating system and position station for a position indicating system"), applicant Håkan Lans, application SE 9102362 filed 15 Aug 1991, published 18 Jan 1993. | Google Patents SE468452B | high |
| Wikipedia states "a US patent ex-parte reexamination certificate was issued in 2010 canceling all claims", citing "USPTO ex-parte reexamination certificate 7428, issued on 30 March 2010". The Google Patents record for US 5,506,587 does **not** display a C1 publication and `US5506587C1` returns 404 on Google Patents. | Wikipedia "Håkan Lans" (read 2026-10-05); Google Patents | medium — the cancellation is corroborated by Panbo (Hersey/Ellison: "the Håkan Lans patent claim was cancelled after reexamination") but the certificate itself was not opened; (verify) via USPTO Patent Center for 08/170,167 or reexam control no. |
| Panbo (2015) reports that the IEC patent-declarations database contains exactly one declaration against IEC 62287 (Class B): filed by Anders Håkan Lans in 2007, offering licences for SOTDMA Class B on RAND terms (IEC "option 2"), and that no declaration was ever filed for the CSTDMA standard by Johnson or Lesch. | Panbo, 1 Jul 2015 (Ellison; Hersey quote) | medium (secondary; (verify) in IEC DB) |
| US 7,512,095 B2 "Multiple access communication system for moveable objects": inventors Mark M. Johnson and Andreas Lesch; original assignee "Individual"; application US 10/709,928 filed 7 Jun 2004; priority 9 Jun 2003 (provisional 60/477,125 per Panbo); PCT/US2004/017966; pre-grant publication US 2005/0129050 A1 (16 Jun 2005); granted 31 Mar 2009; assignment to SOFTWARE RADIO TECHNOLOGY PLC recorded 26 Feb 2015; Google status "Expired - Fee Related"; Google "Adjusted expiration 2027-02-26"; Darts-ip flags "first worldwide family litigation filed" (no date shown). | Google Patents US7512095B2 | high (bibliographic); the "adjusted expiration" date is inconsistent with a 2004 filing + normal PTA and with SRT's own 2015 statement that the patent expires March 2019 — (verify) |
| Abstract of US 7,512,095: "A non-complex low cost communication, navigation and identification system … The present invention listens before each transmission and transmits only when there are no other protocols transmitting, thus avoiding communication collisions and supporting high channel load scenarios." AIS, SOTDMA and CSTDMA are not named in the title/abstract. | Google Patents US7512095B2; Panbo | high |
| Mark Johnson wrote to IEC TC80/WG15 on 7 Jun 2003: "I will be proposing a non-SOTDMA lower cost Class B variant that is low in cost, very 'polite', and compatible with existing Class A AIS. I am quite confident that it avoids the IPR issues." The provisional application was filed two days later (9 Jun 2003). | Panbo quoting WG15 email chain | medium (Panbo saw the emails; not independently verifiable) |
| SRT announced in March 2015 (stock-market announcement) that it had acquired "joint and several rights" to US 7,512,095 (Lesch's share) and would license it on FRAND terms; a manufacturer showed Panbo an SRT email proposing 5 % of net-of-tax retail price (≈US$35/unit on a US$700 Class B), arrears for the prior six years, and quarterly payments "until March 2019 when the patent expires". | Panbo, 1 Jul 2015 | medium–high (quotes documents Panbo saw) |
| Joe Hersey Jr. (ret. USCG, secretary of the US TAG to IEC TC80) on the record: WG15 "were very well aware early in the CSTDMA development process that Mark had filed a provisional patent application … its use was being offered free of charge on a non-discriminatory basis"; "Hakan Lans filed noting the second option under the Class B SOTDMA standard IEC 62287-2. No filing was ever made regarding the Class B CSTDMA standard". | Panbo, 1 Jul 2015 | high (as an attributed on-record statement) |
| COM DEV / exactEarth satellite-AIS patents (US): US 7,876,865 B2 (granted 25 Jan 2011; priority 8 Jun 2007; Peach), US 8,780,788 B2 (15 Jul 2014; priority 25 Sep 2009; Peach), US 9,015,567 B2 (21 Apr 2015; priority 12 Apr 2012; Peach), US 9,094,048 B2 (28 Jul 2015; priority 5 Mar 2013; Randhawa; assignee exactEarth), US 9,842,504 B2 (12 Dec 2017; priority 30 Jun 2015; Short; exactEarth); EP 2 211 486 B1 (9 Jan 2013; Cowles); CA 2,720,190 C (10 May 2016; Chen). | Google Patents search endpoint, assignee "Com Dev" / "exactEarth", 2026-10-05 | high (bibliographic) |
| ORBCOMM holds US 7,809,370 B2 "Space based monitoring of global maritime shipping using automatic identification system" (priority 30 May 2006; granted 5 Oct 2010; inventor John Stolte). | Google Patents search endpoint | high |
| US 9,246,575 B2 "Method for detecting AIS messages" is assigned to **Centre National d'Études Spatiales (CNES)**, inventors Antoine de Latour and Michel Faup; FR priority 11 57849 (5 Sep 2011); filed 29 Aug 2012; granted 26 Jan 2016; status Active; adjusted expiration 23 Oct 2033. Web-search summaries that attribute it to COM DEV are wrong. | Google Patents US9246575B2 | high |
| Spire holds US 11,156,723 B2 "AIS spoofing and dark-target detection methodology" (priority 4 Apr 2016; granted 26 Oct 2021; inventor Peter Platzer; assignee Spire Global Subsidiary, Inc.). | Google Patents search endpoint | high |
| Saab AB holds US 8,610,619 B2 / EP 2 136 221 B1 "Validity check of vehicle position information (transmitted over a time-…)" (priority 18 Jun 2008; US granted 17 Dec 2013; inventors Svante Andersson, Andreas Persson). | Google Patents search endpoint | high (bibliographic); claim scope (verify) |
| True Heading AB (Sweden) holds US 9,804,254 B2 and US 9,807,554 B2 (both granted 31 Oct 2017; inventor Nils Willart). | Google Patents search endpoint | high |
| SRT Marine Technology Ltd holds US 9,473,197 B2 "Reversible TDD transceiver" (priority 29 Jan 2013; granted 18 Oct 2016). | Google Patents search endpoint | high |
| No Google Patents hit exists for assignee "Shine Micro" or "Software Radio Technology" with "automatic identification system" in the text; SRT's patents are filed under "SRT Marine Technology Ltd". | Google Patents search endpoint | high (for that query) |
| ITU-T/ITU-R/ISO/IEC operate a Common Patent Policy with a Patent Statement and Licensing Declaration form (current form dated 2 Nov 2018; Guidelines applicable from 16 Dec 2022). | https://www.itu.int/en/ITU-T/ipr/Pages/default.aspx | high |
| The Swedish Maritime Administration's own history says Lans accepted the ITU Code of Practice but "some countries strongly opposed the idea of making patented equipment mandatory onboard. Finally, Håkan Lans dropped the claim for compensation for the use of the patent on ships covered by the IMO's" carriage requirement. | SMA brochure p. 12 (see `r-history.md`) | high (as SMA's account) |
| *Lans v. Digital Equipment Corp.*, 252 F.3d 1320 (Fed. Cir. 2001): Lans sued (1997) as an individual on US 4,303,986 (colour graphics, granted 1 Dec 1981); defendants showed the patent had been assigned to Uniboard AB (wholly owned by Lans); dismissed for lack of standing; the court refused substitution; attorney fees awarded; Uniboard's own suit failed because the patent had expired. | Search-confirmed citation; Wikipedia; (verify) by reading the opinion | medium–high |

## Notes and quotes

- **What the Lans patent actually claims.** Claim 1 is a *system* claim: GNSS-
  derived common time base → enumerable time blocks in a repeating "maximal
  frame" → each station autonomously occupies a free block to transmit its
  position on a common channel. That is SOTDMA in one sentence. The
  specification is aviation-centric; maritime use came via the Swedish trials
  (see `r-history.md`). Chapter 18 should quote claim 1 and then show the
  M.1371 slot map next to it (2,250 slots/min = the "maximal frame").
- **Term arithmetic worth showing (ch. 18 worked example).** For a US patent
  filed before 8 Jun 1995 and in force on that date, term = later of 17 years
  from grant (9 Apr 1996 + 17 = 9 Apr 2013) or 20 years from the earliest US
  filing/PCT date (29 Jun 1992 + 20 = 29 Jun 2012). Hence Google's 2013-04-09.
  The EP term is 20 years from filing → 29 Jun 2012. So by mid-2013 the entire
  family was dead everywhere — and in the US the claims had already been
  cancelled in 2010.
- **Royalty-free for SOLAS ships, not for everyone.** The SMA text says Lans
  waived compensation for ships under IMO carriage. That leaves open Class B,
  AtoN, base stations, and aviation (VDL Mode 4) — which is precisely why the
  IEC Class B working group in 2003 wanted a non-SOTDMA access scheme. Panbo's
  anonymous correspondent: "The whole point of using CSTDMA instead of SoTDMA
  in the original design of Class B was to avoid any problems with patents".
- **Irony of the CSTDMA patent.** The scheme adopted to escape one patent was
  itself the subject of a provisional application filed two days after its
  proposer promised WG15 it "avoids the IPR issues". Hersey's account is that
  the application was known and offered free of charge; SRT's 2015 position
  (CEO Simon Tucker): "no formal license statement and or license procedure
  for this patent had been established by the owners … SRT took the
  opportunity to acquire rights to the Patent to secure its use for the AIS
  standard going forward" and would license on a FRAND basis. Tucker on
  pricing: "I see no valid reason why the licensing of a long known and
  established patent … should affect end user pricing; proof of this is that
  licenses are already agreed and there has been no price increase."
- **Class B "SO" (SOTDMA Class B).** Hersey: IEC "did not complete the B/SO
  standard until after the Håkan Lans patent claim was cancelled after
  reexamination" — i.e., the 2010 cancellation cleared the path for IEC
  62287-2 and for the Class B SO products that appeared in the mid-2010s
  (Chapter 11/20 should connect these dots, with (verify) on the 62287-2
  edition date).
- **Satellite-AIS patents are a Canadian story first.** The earliest priority
  in the COM DEV set is 8 Jun 2007 (Peach; Cowles), one year before the NTS
  demonstration satellite (2008). ORBCOMM's priority (30 May 2006) is earlier
  still and claims the *system concept* ("space based monitoring of global
  maritime shipping using AIS"). CNES (2011) and Harris (2015) add
  signal-processing methods. Chapter 39 can present these as the IP layer
  under the decollision techniques it describes, without asserting that any
  specific operator practises any specific claim.
- **Analytics patents to be aware of (ch. 47/59).** Saab's "validity check"
  (2008) tests a reported position against TDMA/propagation timing; COM DEV's
  "consistency checking and anomaly detection" (2012); Spire's "AIS spoofing
  and dark-target detection" (2016, granted 2021). The book describes the
  *methods* from the open literature; it should note that patents exist and
  are live (Spire to ~2036, CNES to 2033) without offering legal advice.
- **How to tell the Lans litigation story honestly.** The famous US defeat
  (1997–2001) concerned the *colour graphics* patent US 4,303,986, not STDMA.
  It was lost on standing (assignment to Uniboard) and fees, not on the
  merits. Lans then sued his own lawyers (settled April 2012 per Wikipedia).
  The STDMA patent's US claims were cancelled on reexamination in 2010, in a
  separate proceeding. Keep the two threads distinct; PLAN ch. 17 currently
  conflates them as "Lans's US litigation history".
- **PLAN corrections.** PLAN ch. 9 says "Swedish patent 1989"; the earliest
  priority found anywhere in the family is 1 Jul 1991 (SE 9102034), with SE
  468 452 B published 18 Jan 1993. Unless a 1989 Swedish filing is found in
  the PRV register, the book should say "Swedish priority 1991".

## Open questions / (verify)

- (verify) Obtain the USPTO ex parte reexamination certificate for US
  5,506,587 (Wikipedia: "certificate 7428, 30 March 2010"); confirm the reexam
  control number (90/0xx,xxx), the requester, the prior art relied on, and
  that *all* 13 claims were cancelled. Google Patents does not show a C1
  document — check Patent Center for application 08/170,167.
- (verify) Who requested the reexamination and when (2007–2008?) — relevant
  to whether it was driven by Class B SO or VDL-4 interests.
- (verify) The IEC patent-declaration record for IEC 62287 by Anders Håkan
  Lans (2007): exact date, option selected, and whether it names 62287-2
  specifically. Also whether SRT filed a declaration for US 7,512,095 after
  March 2015 (Tucker said SRT "would be following this process").
- (verify) Whether the ITU-R patent database holds any declaration against
  M.1371 (by GP&C, Lans, Johnson/Lesch, SRT, or others). The search form
  lists M.1371 as a selectable Recommendation; an interactive query is needed.
- (verify) Expiry/lapse date of US 7,512,095: Google shows "Expired - Fee
  Related" (maintenance fee not paid) with an implausible "adjusted
  expiration 2027-02-26"; SRT's 2015 email said "March 2019". Compute from
  USPTO maintenance-fee records (grant 31 Mar 2009 → fee windows at 3.5, 7.5,
  11.5 years).
- (verify) The Darts-ip "family litigation" flag on US 7,512,095 — identify
  the case (SRT v. ? or a declaratory action) and outcome.
- (verify) Whether US 9,729,374 (Harris, Doppler separation) names AIS/VDES
  in its specification, and whether exactView RT practised it.
- (verify) Scope of US 9,842,504 (exactEarth "vessel position reporting and
  monitoring") — is this the ABSEA satellite-enhanced Class B scheme?
- (verify) Any Kongsberg Seatex / FFI patents on AISSat/NORAIS receivers
  (search returned Kongsberg Seatex's maritime broadband radio CN 103503232 B,
  not AIS-specific).
- (verify) Whether any patent covers the AIS-SART burst scheme (8 messages per
  minute, 14 messages) — none found; IEC 61097-14 appears to be unencumbered.
- (verify) VDES patents: search returned a Korean slot-management application
  (US 2019/0208533 A1, Ju Hwan Lee) and a GMT Co. beamforming patent; a proper
  landscape for ch. 69 is still needed.
- (verify) Current assignee of the COM DEV/exactEarth families after Spire's
  2021 acquisition of exactEarth and Kpler's 2025 acquisition of Spire
  Maritime — check USPTO assignment records.
- (verify) Read *Lans v. Digital Equipment Corp.*, 252 F.3d 1320 (Fed. Cir.
  2001) and the D.D.C. decision below it; confirm the fee award amount and the
  Uniboard follow-on case citation.

## Candidate figures and worked examples

1. **Lans family map (ch. 18):** SE 9102034 (1 Jul 1991) and SE 9103542 (28
   Nov 1991) → SE 468 452 B (18 Jan 1993) → PCT/SE92/00485 (29 Jun 1992) →
   WO 93/01576 (21 Jan 1993) → US 5,506,587 (9 Apr 1996) / EP 0 592 560 B1
   (27 Aug 1997) + 13 national members → US claims cancelled (30 Mar 2010,
   verify) → EP expiry 29 Jun 2012 → US expiry 9 Apr 2013.
2. **Worked example — patent term arithmetic (ch. 18):** the 17-from-grant vs
   20-from-filing rule for a 1992 PCT / 1996 grant; EP 20-years-from-filing;
   show why the two dates differ by ten months.
3. **Claim 1 vs the slot map (ch. 18/21):** side-by-side of claim 1 language
   ("standardized, enumerable … repeating maximal frame") and the 2,250-slot
   minute of M.1371 Annex 2.
4. **Timeline of AIS IPR events (ch. 18, App. A):** 1991 priority · 1996 US
   grant · 1997 EP grant · 1996–98 IMO/ITU royalty debate and SOLAS waiver ·
   7–9 Jun 2003 Johnson email and provisional · 2006 Class B CS standard
   (IEC 62287-1) · 2007 Lans IEC declaration for 62287 · 2007 COM DEV first
   S-AIS priority · 2010 US claims cancelled · 2012/2013 family expiry ·
   Mar 2015 SRT acquires CSTDMA patent share · 2021 Spire spoof-detection
   grant.
5. **Table — "what is expired, what is live" (ch. 18):** columns: patent,
   owner (2026), subject, priority, grant, status (expired/lapsed/active),
   affects (Class A / Class B CS / Class B SO / S-AIS / analytics).
6. **Satellite-AIS IP lineage (ch. 39):** ORBCOMM 2006 → COM DEV 2007/2009/
   2010/2012 → exactEarth 2013/2015 → CNES 2011 → Harris 2015 → Spire 2016,
   mapped to techniques (on-board decoding, FOV segmentation, Doppler
   separation, anomaly detection).

## Recommended use by chapter

- **Chapter 9 (Prehistory/Lans):** state the Swedish priority as 1 Jul 1991
  (not 1989); the patent is aviation-framed; SE 468 452 B as the national
  grant.
- **Chapter 10 (Standardization 1996–2004):** the royalty question — Lans's
  acceptance of the ITU Code of Practice, member-state objections, the waiver
  for SOLAS-mandated ships (SMA account); the ITU/IEC common patent policy
  options.
- **Chapter 11 (Growth 2004–2015):** Class B CS (2006) as a patent-avoidance
  design; Class B SO only after the 2010 cancellation (Hersey).
- **Chapter 17 (Legal issues):** two distinct Lans threads — the 1997–2001
  colour-graphics standing defeat (*Lans v. DEC*) and the 2010 STDMA
  reexamination; the 2015 SRT royalty demand (5 %, arrears) as a case file.
- **Chapter 18 (Patents):** everything above; the family table; the term
  arithmetic; the "expired vs live" table; the IPR-declaration mechanics;
  the satellite and analytics patent sets; a Legal note that the book does not
  offer freedom-to-operate advice.
- **Chapter 20/21 (Architecture; link layer):** why Class B CS "listens before
  transmitting" (the abstract of US 7,512,095 as the design statement) and why
  Class B SO exists at all.
- **Chapter 30/39 (Loading; satellite AIS):** cite the COM DEV/ORBCOMM/CNES/
  Harris patents as the documented record of decollision techniques (FOV
  segmentation, Doppler separation, multi-pass decoding), with a caution that
  claims ≠ deployed practice.
- **Chapter 33 (Hardware):** SRT's role as OEM and as CSTDMA patent co-owner
  since 2015; SRT Marine Technology's own hardware patent.
- **Chapter 47/59 (Data quality; spoof detection):** Saab 2008, COM DEV 2012
  and Spire 2016/2021 patents exist on plausibility/anomaly checks; describe
  methods from open literature and flag the IP.
- **Chapter 65/7 (Hacks; science uses):** eOdyn's surface-current application
  (Guichoux, 2013 priority) as the IP trace of AIS-derived currents.
- **Appendix A (Timeline):** the IPR events above as ⟨+⟩ entries.
