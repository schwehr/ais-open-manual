# Dossier: IHO standards relevant to AIS (S-57, S-52, S-100 and the S-1xx/S-2xx/S-4xx product specifications)

**Purpose.** This dossier collects what can be confirmed, as of 5 October 2026,
about the International Hydrographic Organization (IHO) documents that govern
how AIS information is drawn on official chart displays and how AIS-adjacent
data (water levels, currents, navigational warnings, aids to navigation, route
plans, application-specific messages) is being re-expressed in the S-100
framework: S-57 (ENC transfer format), S-52 (ECDIS presentation), S-63 and
S-100 Part 15 (data protection), S-100 itself (Editions 1.0.0 to 5.2.1), the
Phase 1 product specifications S-101/S-102/S-104/S-111/S-124/S-128/S-129, the
AtoN pair S-125 (IHO/IALA) and S-201 (IALA), IEC's S-421 route plan, IALA's
planned S-230 ASM specification, and the IMO instrument that makes S-100 ECDIS
real, resolution MSC.530(106) and its Rev.1. It feeds **Chapter 51** (charts,
ENC vs ECDIS vs ECS, AIS on the display), **Chapter 52** (AIS and the S-100
family), **Chapter 54** (tide, water level and met-ocean transmissions),
**Chapter 14** (key organizations), **Chapter 15** (standards narrative),
**Chapter 12** (2015–present history), **Chapter 68** (AtoN) , **Chapter 69**
(VDES), **Appendix B** (standards register) and **Appendix J** (organizations
directory).

> Research-session note. Facts marked *high* were read directly from an IHO
> PDF (text extracted with `pdftotext`) or from an IHO web page read live on
> 2026-10-05 (iho.int pages sit behind a cookie check; they were fetched with
> `curl` after setting the `iho_v` cookie the site's JavaScript sets). The IHO
> Geospatial Information Registry (registry.iho.int, hosted by KHOA) was
> queried via its `productspec/list.json` endpoint and per-version `view.do`
> pages; the S-104, S-125 and S-201 PDFs were downloaded from it. Facts marked
> *medium* come from web-search summaries that cite iho.int, imo.org, iec.ch or
> class-society circulars, or from pages whose text could only be partly read.
> Items marked *(verify)* could not be confirmed.

## Key questions

1. What is the IHO, who are its members, and which committees and working
   groups (HSSC, S-100WG, NIPWG, TWCWG, WWNWS-SC) own the documents AIS people
   meet?
2. What do S-57 and S-52 actually say about AIS, and which editions are
   current? (Chapters 51, 15, App. B)
3. What is S-100, what are its Parts, and what is its edition history? Which
   edition is the baseline for S-100 ECDIS and for the "operational" product
   specifications? (Chapters 52, 12)
4. What are the current editions, dates and status of the S-100 product
   specifications that touch AIS or AIS-carried data: S-101, S-104, S-111,
   S-124, S-125, S-201, S-421, S-230, S-240? Which are "operational" versus
   "implementation and testing only"? (Chapters 52, 54, 68)
5. What exactly does IMO MSC.530(106) require, on what dates, and how does it
   reference AIS, S-57, S-100, S-101, S-98 and S-63/Part 15? (Chapters 51, 52,
   16)
6. What is the "dual fuel" transition plan (S-57 and S-101 in parallel), what
   is the IHO Roadmap for the S-100 Implementation Decade, and what did it
   actually say happened in 2025–2026? (Chapters 12, 52)
7. Do S-104/S-111 (water levels, currents) define any VHF Data Link bearer, or
   is the "ASM today, VDES tomorrow" story an IALA/VDES matter rather than an
   IHO one? (Chapters 54, 69)
8. How do S-125 and S-201 model AIS AtoN (physical/virtual/synthetic) and how
   do they relate to Message 21 and IALA R0126? (Chapter 68)
9. What is free, and where? (Chapter 15, App. B)
10. When did NOAA stop producing traditional paper and raster charts?
    (Chapter 51 — PLAN says "2025 (verify)")

## Primary sources located

| Source | Identifier / edition / year | URL | What it covers | Access |
|---|---|---|---|---|
| IHO *Standards and Specifications* index page | Read live 2026-10-05; page "Last modified 28/09/2026" | https://iho.int/en/standards-and-specifications | Authoritative list of current editions/dates for S-4…S-164, with download links | Free |
| IHO S-57 *Transfer Standard for Digital Hydrographic Data*, main document | Edition 3.1, November 2000 (page lists "Edition 3.1.0") | https://iho.int/uploads/user/pubs/standards/s-57/31Main.pdf | ISO/IEC 8211-encapsulated vector transfer standard; Parts 1–3; App. A Object/Attribute Catalogues; App. B.1 ENC Product Specification | Free |
| IHO S-57 Supplement No. 3 to Edition 3.1 | June 2014 (incorporates Supplement No. 2) | https://iho.int/uploads/user/pubs/standards/s-57/S-57_e3.1_Supp3_Jun14_EN.pdf | Additions for ENC; "Edition 3.1.3" in common usage | Free |
| IHO S-57 App. B.1 Annex A, *Use of the Object Catalogue for ENC* | Edition 4.4.0 (link name) | https://iho.int/uploads/user/pubs/standards/s-57/S-57%20Appendix%20B.1%20Annex%20A_Ed%204.4.0_FINAL.pdf | ENC encoding guidance | Free |
| IHO S-52 *Specifications for Chart Content and Display Aspects of ECDIS* | Edition 6.1(.1), October 2014, with clarifications to June 2015 | https://iho.int/uploads/user/pubs/standards/s-52/S-52%20Edition%206.1.1%20-%20June%202015.pdf | ECDIS display rules; colour tokens incl. RESBL reserved for AIS/VTS; historical background since 1986 | Free |
| IHO S-52 Annex A, *IHO ECDIS Presentation Library* | Edition 4.0(.4), October 2014, with clarifications up to March 2025 | Linked from the standards page (`S-52 PresLib Ed 4.0.3 Part I Addendum_Clean.pdf` for the addendum) | Symbol library, incl. IEC "navigational elements and parameters" and AIS vessel-report symbols on ECDIS Chart 1 | Free |
| IHO S-52 Annex A:100, *S-100 ECDIS Presentation Library for S-57 ENC* | Edition 5.0(.0), October 2025 | Distributed via the S-100 Security Scheme package (standards page note) | PresLib for S-57 ENCs displayed in MSC.530(106) ECDIS | Registration |
| IHO S-63 *Data Protection Scheme* | Edition 1.2(.2), September 2026 | https://iho.int/uploads/user/pubs/standards/s-63/S-63_Ed1.2.2_FINAL.pdf | Encryption/authentication of S-57 ENCs | Free (scheme documents by sign-up) |
| IHO S-64 / S-64:100 Test Data Sets | S-64 Ed. 3.0(.3), Dec 2020; S-64:100 Ed. 4.0(.0), Oct 2025 | Standards page | ECDIS type-approval test data (S-57 in classic and S-100 ECDIS) | Free |
| IHO S-65 Annex B / Annex C | S-57→S-101 Conversion Guidance Ed. 2.0.0, Oct 2025; S-101→S-57 Ed. 1.0.0, May 2025 | Standards page | Dual-fuel production options | Free |
| IHO S-66 *Facts about Electronic Charts and Carriage Requirements* | Edition 2.0.0, October 2024 | https://iho.int/uploads/user/pubs/standards/s-66/S-66%20Ed%202.0.0_Final.pdf | Plain-language ECDIS/ENC/RNC/ECS definitions; SOLAS V/18, 19, 27 text; carriage schedule 2012–2018 | Free |
| IHO S-98 *S-100 ECDIS and Interoperability Specification* | Edition 2.0.0, October 2025 (zip) | Standards page (`S-98 Ed 2.0.0.zip`) | How S-100 layers combine in ECDIS; Annex C dynamic water level | Free |
| IHO S-100 *Universal Hydrographic Data Model* | Edition 5.2.1, December 2025 (plus 1.0.0, 2.0.0, 3.0.0, 4.0.0, 5.0.0, 5.1.0, 5.2.0 archived) | https://iho.int/uploads/user/pubs/standards/s-100/S-100%20Ed%205.2.1_FINAL.pdf | Framework: Parts 0–18 (registers, GFM, metadata, feature catalogue, CRS, portrayal incl. Lua, encodings 8211/GML/HDF5, Part 15 encryption, Part 17 discovery metadata) | Free |
| IHO *S-100 based Product Specifications* page | "Last modified 29/07/2026" | https://iho.int/en/s-100-based-product-specifications | Domain allocation: IHO S-101–S-199; IALA S-201–S-299; IOC S-301–S-399; IEHG S-401–S-410; WMO S-411–S-420; IEC TC80 S-421–S-430; NATO AML S-501–S-525 | Free |
| IHO *IHO S-101 to S-199* page | "Last modified 17/07/2023" | https://iho.int/en/iho-s-101-to-s-199 | Scope statements and responsible bodies for S-101…S-164 | Free |
| IHO *IALA S-201 to S-299* page | "Last modified 18/10/2021" | https://iho.int/en/iala-s-201-to-s-299 | S-201 scope; S-210/211/212/230/240/245/246/247 listed | Free |
| IHO Geospatial Information Registry, Product Specification Register | Queried 2026-10-05 (`POST /productspec/list.json`; `view.do?idx=…`) | https://registry.iho.int/productspec/list.do | Per-edition status, version date, S-100 baseline, files | Free (downloads anonymous) |
| IHO S-101 ENC Product Specification | Ed. 2.0.0, version date 2024-12-27 (S-100 5.2.0); Ed. 2.1.0 in "Approval process" dated 2026-09-14 | Registry entry idx=214 | ENC under S-100; "first operational Edition" | Free |
| IHO S-104 *Water Level Information for Surface Navigation* | Ed. 2.0.0, 2024-12-27 (S-100 5.2.0); 116 pp. | Registry download (`cmm/downLoad.do`, idx=957) | Gridded water-level time series in HDF5 (dataCodingFormat 2); delivery "by any appropriate means" | Free |
| IHO S-111 *Surface Currents* | Ed. 2.0.0, 2024-12-27 | Registry | Surface-current grids (HDF5) | Free |
| IHO S-124 *Navigational Warnings* | Ed. 1.0.0 2023-05-13 (testing); Ed. 2.0.0 2025-03-28, "first operational Edition" | Registry | MSI/navigational warnings for ECDIS; owned by WWNWS-SC | Free |
| IHO/IALA S-125 *Marine Aids to Navigation (AtoN)* | Ed. 1.0.0; cover "December 2025", registry version date 2026-06-01, IHO page "June 2026"; "implementation and testing purposes only" | Registry download idx=1075 | AtoN information for ECDIS/ECS; physical/virtual/synthetic AIS AtoN; GML | Free |
| IALA S-201 *Aids to Navigation Information* | Ed. 1.0.0 2019-10-31; 1.1.0 2022-10-27; 2.0.0 19 May 2025, "first operational Edition" | Registry download idx=1018 | AtoN asset exchange for authorities (not ECDIS); AIS AtoN features; GML | Free |
| IALA S-240 *DGNSS Station Almanac* | Ed. 1.0.0 2020-10-30, "development and trial" | Registry | DGNSS beacon almanac | Free |
| IEC S-421 *Route Plan* = IEC 63173-1:2021 | Ed. 1.0.0 (registry 2021-06-01; IEC publication 16 June 2021 per iec.ch search) | Registry; https://webstore.iec.ch | S-100 route exchange successor to RTZ | Registry metadata free; IEC text paid |
| IHO Council, *Roadmap for the S-100 Implementation Decade (2020–2030)* | Version 5.0, October 2025 | https://iho.int/uploads/user/About%20IHO/Council/S-100_ImplementationStrategy/S100_Roadmap_Decade_v5.0_clean_October2025.pdf | Dual-fuel plan, IMO synchronization, references to Council decisions C2–C9 and Assembly A2/A3 | Free |
| IHO Roadmap Annex 2, *S-100 Timelines* | Version 5.0, 9 July 2025 (HSSC-17 report Annex A) | https://iho.int/uploads/user/About%20IHO/Council/S-100_ImplementationStrategy/S-100%20Roadmap_Annex_2_v5.0_July2025.pdf | Phase 1/2/3 lists; ENDS tree; S-164 approval planned Feb 2026 | Free |
| IMO Resolution MSC.530(106), *Performance standards for ECDIS* | Adopted 7 November 2022 (MSC 106/19/Add.1, Annex 22) | https://wwwcdn.imo.org/localresources/en/KnowledgeCentre/IndexofIMOResolutions/MSCResolutions/MSC.530(106).pdf | 2026/2029 dates; ENDS definition; AIS clauses 1.6, 7.1–7.3; Appendix 1 reference list (S-52, S-57, S-100, S-101, S-98, S-61, S-63, S-32, M-3) | Free |
| IMO Resolution MSC.530(106)/Rev.1 | Adopted 24 May 2024 at MSC 108 (medium; search summary citing class/ADMIRALTY notices and MSC 108/20/Add.1) | GISIS / IMO docs | Adds digital route-plan exchange (S-421) ; replaces original | Paid/registered |
| IHO HSSC page | Read live 2026-10-05 | https://iho.int/en/hssc | HSSC remit; HSSC-18 Gdynia 18–22 May 2026; documents moved to IHO Portal (CL 44/2024) | Free |
| NOAA Office of Coast Survey, *Farewell to traditional nautical charts* | Read live 2026-10-05 | https://nauticalcharts.noaa.gov/charts/farewell-to-traditional-nautical-charts.html | Raster/paper sunset announced 2019, completed December 2024 (1,007 charts) | Free |

## Verified facts

| Fact | Source (clause/page) | Confidence |
|---|---|---|
| The IHO was founded as the International Hydrographic Bureau on 21 June 1921 in Monaco; it became the IHO under a convention in force 22 September 1970; the 2005 Protocol of Amendments (Assembly, Council, "IHO Secretariat") entered into force 8 November 2016; 104 Member States as of 2025/26 | Web-search summary citing iho.int and Wikipedia; the iho.int "About" page returned only navigation when fetched | medium |
| HSSC "is in charge of promoting and coordinating the development of standards, specifications and guidelines for official products and services"; its work elements include "S-100 Framework" and "S-57 Framework"; HSSC-18 is in Gdynia, 18–22 May 2026; HSSC/NIPWG resources moved to the IHO Portal per CL 44/2024 | https://iho.int/en/hssc (read 2026-10-05) | high |
| Development of S-100 was included in the IHO Work Programme in 2001; developed by the TSMAD WG; since 2015 by the S-100 Working Group (S100WG); aligned with the ISO 19100 series | S-100 Ed. 5.2.1, Part 0 Foreword, p. i | high |
| S-100 document control: 1.0.0 January 2010 (CL 83/2009, 4 Dec 2009); 2.0.0 June 2015 (CL 39/2015); 3.0.0 June 2017 (CL 32/2017, 2 May 2017); 4.0.0 December 2018 (CL 60/2018, 17 Dec 2018); 5.0.0 December 2022 (CL 45/2022, 12 Dec 2022); 5.1.0 October 2023 (CL 36/2023, 31 Oct 2023); 5.2.0 June 2024 (CL 27/2024, 7 Jun 2024); 5.2.1 December 2025 (S-100WG) | S-100 Ed. 5.2.1, Part 0, Document Control table | high |
| The IHO standards web page lists S-100 Ed. 3.0.0 as "April 2017" whereas the Ed. 5.2.1 document-control table says "June 2017" | Compare https://iho.int/en/standards-and-specifications with S-100 Ed. 5.2.1 Part 0 | high (discrepancy noted) |
| S-100 Parts: 0 Overview; 1 Conceptual Schema Language; 2/2a/2b Registers; 3 General Feature Model; 4 Metadata; 5 Feature Catalogue; 6 CRS; 7 Spatial Schema; 8 Imagery and Gridded Data; 9/9a Portrayal (Lua); 10/10a/10b/10c Encoding Formats (ISO/IEC 8211, GML, HDF5); 11 Product Specifications; 12 Maintenance; 13 Scripting; 14 Online Communication Exchange; 15 Encryption and Data Protection; 16/16a Interoperability Catalogue / Harmonised Portrayal; 17 Discovery Metadata; 18 Language Packs | S-100 Ed. 5.2.1, Part 0, §0-4 contents list | high |
| S-100 objectives include complying with ISO TC 211 standards and separating "the data content from the encoding format, enabling format neutral product specifications" | S-100 Ed. 5.2.1, Part 0, §0-3 | high |
| S-100 Foreword states S-57 "has been used almost exclusively for encoding ENCs", "is not a contemporary standard that is widely accepted in the GIS domain", and that "S-57 will continue to exist as the designated format for ENC data for the foreseeable future" | S-100 Ed. 5.2.1, Part 0 Foreword | high |
| S-57 Edition 3.1 was "officially made available in November 2000", superseding Edition 3.0 of November 1996; a familiarization version was distributed November 1999; Ed. 3.0 was frozen for four years from November 1996; Ed. 3.1 frozen "until at least November 2002"; origin traced to the 6th CoE meeting, November 1994, and a February 1995 workshop | S-57 Ed. 3.1 Main document, Preface pp. i–ii (signed RAdm Neil Guy, Nov 2000) | high |
| S-57 changes from 2.0 to 3.0: binary implementation added to ASCII; new cell structure; updating by unique object identifiers; main section + two appendices (Object Catalogue; Product Specifications incl. ENC) | S-57 Ed. 3.1 Preface | high |
| S-57 Supplement No. 3 to Edition 3.1 is dated June 2014 and incorporates former Supplement No. 2; S-57 Appendix A Annex A (producer codes) replaced by S-62; App. B.1 Annex C (validation checks) replaced by S-58 (now Ed. 8.0.0, October 2024) | IHO standards page | high |
| S-52 current edition: 6.1(.1), October 2014, with clarifications up to June 2015; Annex A Presentation Library Ed. 4.0(.4), October 2014, with clarifications up to March 2025; Edition 6.0 was March 2010 | S-52 PDF cover and "Change control history since 2010"; IHO standards page | high |
| S-52 historical background: a 1986 North Sea Hydrographic Commission study led to the IHO Committee on ECDIS (COE), later CHRIS, now HSSC | S-52 Ed. 6.1.1 §1.1.3 | high |
| S-52 names AIS explicitly: integration of ARPA and AIS targets into the ECDIS display is "another option" (§1.2 (b)); AIS is listed among non-chart information on the display; "By agreement with the IEC, symbols for the 'Navigational Elements and Parameters' of the IMO PS Appendix 3, and also symbols being developed by IMO for AIS vessel reports, are included in the Presentation Library" (§3.2 item 23); colour token **RESBL** = "blue … symbol, line or text colour reserved for AIS and VTS" | S-52 Ed. 6.1.1 full text (grep hits at lines 417–418, 816, 2178, 2902, 3153 of extracted text) | high |
| S-52 Annex A:100 "IHO S-100 ECDIS Presentation Library for S-57 ENC", Edition 5.0(.0), October 2025, "has been prepared for IMO S-100 ECDIS Performance Standard MSC.530(106); it is not to be used in conjunction with any other Performance Standard" and is distributed through the S-100 Security Scheme | IHO standards page | high |
| MSC.530(106) was adopted 7 November 2022 (MSC 106/19/Add.1, Annex 22). It recommends ECDIS installed on/after 1 January 2029 conform to the new annex; installed 1 January 2026 – 31 December 2028 may conform to either the new annex or MSC.232(82); installed 1 January 2009 – 31 December 2025 to MSC.232(82); installed 1996–2008 to A.817(19) as amended by MSC.64(67) and MSC.86(70) | MSC.530(106) PDF, operative paras 2(a)–(d) | high |
| "Installed on or after 1 January 2029" means: building contract on/after that date (or constructed if no contract), or equipment delivered to the ship on/after that date | MSC.530(106), para 3 | high |
| MSC.530(106) §1.6: "The ECDIS display may also be used for the display of radar, radar tracked target information, AIS and other appropriate data layers to assist in route monitoring." §7.1: radar/AIS information "may be transferred from systems compliant with the relevant standards"; §7.2: removable "by single operator action"; §7.3: common reference system or an indication | MSC.530(106) Annex §§1.6, 7.1–7.3 | high |
| MSC.530(106) introduces the term **ENDS** (electronic navigational data service): "a special-purpose database compiled from nautical chart and nautical publication data … conforming to IHO standards … The navigational base layer of ENDS is the electronic navigational chart (ENC)." Data protection: "IHO Publication S-63 – Data Protection Scheme (for S-57 ENCs) and S-100, Part 15 – Data Protection Scheme (for S-100 products)" | MSC.530(106) §3.3 and footnote to §4.8; quoted again in Roadmap Annex 2 | high |
| MSC.530(106) Appendix 1 lists IHO references S-52 (+ App. 1, App. 2), S-32, S-57, S-100, S-101, S-98, S-61, S-63, M-3; IMO references include MSC.191(79) as amended by MSC.466(101), A.694(17), MSC.302(87), SN.1/Circ.207, SN.1/Circ.243/Rev.2, MSC/Circ.982 | MSC.530(106) Appendix 1 | high |
| MSC.530(106)/Rev.1 was adopted 24 May 2024 at MSC 108 to add standardized digital exchange of route plans (S-421 / IEC 63173-1) and replaces the original | Web-search summary (class-society and ADMIRALTY notices); Roadmap v5.0 §3 says S-421 "Endorsed by IMO NCSR10 2023, but depending IMO MSC approval May 2024" | medium |
| IHO Roadmap v5.0 §4: "Amendments were made in IMO's ECDIS Performance Standards to incorporate S-100, approved by MSC in November 2022. S-100 ECDIS can be used voluntary from 1 January 2026 and will be mandated in new installations from 1 January 2029." IHO will provide an annual status report to IMO NCSR on S-101 coverage | Roadmap v5.0, p. 5 | high |
| Roadmap v5.0 §3: new ECDIS from 2025 "will have to be capable to process both formats: S-57 ENCs and S-101 ENCs in parallel"; this "dual fuel" model is detailed in Annex 4 (v1.2, July 2024, Council decision C8/34); the Assembly adopted the Dual Fuel Concept as Decision A3/13 and an S-100 Infrastructure Center as A3/14 | Roadmap v5.0 references K, L; §1, §3 | high |
| Roadmap v5.0 §3: IHO sought commitment from Member States "to start regular native production of S-101 ENCs in 2025 and regular availability gradually growing in the course of 2026 in parallel to regular S-57 ENC production"; converted S-57→S-101 cells will have "limitations … in some cartographic details" | Roadmap v5.0, pp. 2–3 | high |
| Roadmap v5.0 §3: additional S-1xx services "It is not anticipated that these services will be mandated by IMO, but will be available at the option of users" | Roadmap v5.0, p. 3 | high |
| Roadmap Annex 2 (9 July 2025): "Most S-100 Phase 1 product specifications … have been approved in their operational editions late 2024 or 2025"; HSSC-17 (2025) endorsed S-98 Ed. 2.0.0 but "the need for a new edition 3.0.0 has already been identified"; IHO MS approval of S-164 test datasets "planned for February 2026"; S-158:xxx validation checks "not yet fully finalized" | Roadmap Annex 2 v5.0, p. 1 | high |
| Phase 1 / Route monitoring: S-101, S-102, S-104, S-111, S-124, S-129; Critical Framework: GI Registry, S-98, S-100, S-128, S-158:xxx, S-164. Phase 2 / Route planning: S-122, S-123, S-125, S-127, S-131, S-411, S-412. Phase 3: S-126, S-413, S-414 | Roadmap Annex 2 v5.0, Table A | high |
| Roadmap Annex 2 figure caption: SOLAS requirements on navigational and meteorological warnings "are still based on Radiocommunication Services (GMDSS), SOLAS chapter IV. S-100 MSI related products … are supplementary products (S-124 and S-41x) until further decisions are taken by IMO" | Roadmap Annex 2 v5.0, Figure 1 caption | high |
| Phase 1 product specifications "entered into force" 1 January 2026 (S-101, S-102, S-104, S-111, S-124, S-128, S-129) | Web-search summary citing iho.int news and Hydro International | medium |
| Current editions on the IHO page (read 2026-10-05): S-101 Ed. 2.0.0 Dec 2024; S-102 Ed. 3.0.0 Dec 2024; S-104 Ed. 2.0.0 Dec 2024; S-111 Ed. 2.0.0 Dec 2024; S-121 Ed. 1.0.0 Oct 2019; S-122 Ed. 1.0.0 Jan 2019; S-123 Ed. 1.0.0 Jan 2019; S-124 Ed. 2.0.0 Mar 2025; S-125 Ed. 1.0.0 Jun 2026; S-127 Ed. 1.0.0 Dec 2018; S-128 Ed. 2.0.0 Mar 2025; S-129 Ed. 2.0.0 Dec 2024; S-130 Ed. 2.0.0 Oct 2025; S-131 Ed. 1.0.0 Apr 2023; S-97 Ed. 1.1.0 Jun 2020; S-98 Ed. 2.0.0 Oct 2025; S-99 Ed. 2.0.0 Oct 2022; S-158 Ed. 1.0.0 Feb 2025 | IHO standards page | high |
| IHO page note: "S-121, S-122, S-123, S-125, S-127 and S-131 Edition 1.0.0 Product Specifications are released for implementation and testing purposes only" | IHO standards page | high |
| Registry edition history — S-101: 1.0.0 2018-12-21 (S-100 4.0.0, now *Retired*, "implementation and testing"); 1.1.0 2023-04-28 (S-100 5.0.0); 1.2.0 2024-03-22 (S-100 5.1.0); 2.0.0 2024-12-27 (S-100 5.2.0, "first operational Edition"); 2.1.0 dated 2026-09-14 in "Approval process" ("currently subject to adoption by the IHO Member States") | registry.iho.int product spec entries | high |
| Registry — S-104: 1.0.0 2021-08-31 (S-100 4.0.0); 1.1.0 2023-04-10 (5.0.0); 2.0.0 2024-12-27 (5.2.0, "first operational Edition"). S-111: 1.0.0 2018-12-21; 1.2.0 2023-03-31; 2.0.0 2024-12-27 (first operational). S-124: 1.0.0 2023-05-13 (5.0.0, testing); 1.5.0 StakeholderReview; 2.0.0 2025-03-28 (5.2.0, first operational) | registry.iho.int | high |
| Registry — S-201 (IALA, domain "IALA AtoNs"): 1.0.0 2019-10-31 (S-100 4.0.0, "development and trial"); 1.1.0 2022-10-27 (5.0.0); 2.0.0 2025-05-19 (5.2.0, "first operational Edition of S-201"). S-240: 1.0.0 2020-10-30 (development and trial). S-421 (IEC): 1.0.0 2021-06-01 (S-100 4.0.0) "published as an IEC standard IEC 63173-1 Edition 1.0:2021" | registry.iho.int | high |
| Registry — S-125: single edition 1.0.0, version date 2026-06-01, S-100 5.2.0; remark "S-125 is a joint IHO/IALA Publication. S-125 Edition 1.0.0 is released for implementation and testing purposes only." The PDF cover reads "Edition 1.0.0 – December 2025" while its copyright line reads "June 2026" | registry.iho.int; S-125 PDF p. 1 and p. 2 | high (date discrepancy noted) |
| S-125 scope (IHO page): "navigational features including lights and other navigation aids, both physical and virtual; temporary and seasonal marks; and local AIS application-specific messages"; responsible body NIPWG | https://iho.int/en/iho-s-101-to-s-199 | high |
| S-125 data model: "supports three types of AIS features, physical (real), virtual and synthetic. The broadcasting station for virtual AIS is encoded as RadioStation, and may be associated with the virtual AIS it broadcasts by an association labelled VirtualAIS … Only RadioStation that are AIS base stations can be included." Encoding is GML | S-125 Ed. 1.0.0 PDF (36 pp.), application-schema overview; §on GML | high |
| S-125 document history shows drafts 0.0.1 (2022-03-07) through 1.0.0 by the "IALA ARM S-201 TG", then alignment with S-201 and S-125 TG comments | S-125 Ed. 1.0.0 revision table | high |
| S-201 Ed. 2.0.0 (May 2025, date 19 May 2025): covers "buoys, beacons, racons, lights, sound signals and AIS"; "S-201 is not intended to be for navigation systems like ECDIS, and therefore is not constrained by ECDIS requirements" and can include "AtoN fixing method, moorings and power source"; model has PhysicalAISAidToNavigation, VirtualAISAidToNavigation, SyntheticAISAidToNavigation associated with a RadioStation of type AIS Base Station; GML encoding per S-100 Ed. 5.2.0 Part 10b; revision log: 15/08/2017 "Edition 3.0.0, included AIS AtoNs" (internal draft numbering) | S-201 Ed. 2.0.0 PDF (39 pp.) §1.1, §1.2.1, application schema, §encoding | high |
| S-104 Ed. 2.0.0 uses a single encoding, HDF5 (S-100 Part 10c), with `dataCodingFormat = 2` (regular grids); purpose is dynamic depth display in ECDIS with S-102/S-101 and UKC management (S-98 Annex C); datasets "may be distributed by any appropriate means, such as transfer to an accessible Internet service or via a licensed distribution channel"; the document does not mention AIS, ASM or VDES | S-104 Ed. 2.0.0 §1.1, §1.1.3, §7.4, §10.2, Table 10-1; grep of full text | high |
| S-230 "Application Specific Messages" is listed on the IHO IALA S-2xx page with empty scope and responsible body IALA; it does **not** appear in the registry's product-spec list (28 entries) as of 2026-10-05 | https://iho.int/en/iala-s-201-to-s-299; registry JSON | high |
| Domain allocations for S-100 product specifications: IHO S-101–S-199; IALA S-201–S-299; IOC S-301–S-399 (none proposed yet); IEHG S-401–S-410 (S-401 Inland ENC, S-402); WMO SERCOM S-411–S-420 (S-411…S-415); IEC TC80 S-421–S-430 (S-421 Route Plan); NATO GMWG AML S-501–S-525 (none proposed yet) | https://iho.int/en/s-100-based-product-specifications | high |
| Registry domain tags include "IALA AIS", "IALA AtoNs", "IALA VTS", "WMO Ice", "Inland ENC", "Port ENC", "AML", "IEC" | registry.iho.int view page filter list | high |
| S-66 Ed. 2.0.0 (October 2024): "The current version of S-57 is Edition 3.1. A new ENC Product Specification S-101 is currently (2024) under development"; ECS defined as "Electronic Chart System (does not meet SOLAS requirements)"; mandatory ECDIS carriage under SOLAS V/19.2.10 "was subject to a staged entry into force between 1 July 2012 and 1 July 2018"; SOLAS V/18.4 ties ECDIS acceptance to performance standards in effect on installation date (A.817(19) of 23 November 1995 for pre-1999 systems) | S-66 Ed. 2.0.0 §§ glossary, 3.5, 6.2; quoted SOLAS text | high |
| S-52 (ECDIS vs ECS): "electronic chart systems not meeting these ECDIS specifications of IHO and IMO, or ECDIS using non-official data, are known as ECS" | S-52 Ed. 6.1.1 §1.2 (a) | high |
| IEC 63173-1 Edition 1.0 (S-421 Route Plan) published 16 June 2021; Edition 2.0 in CDV stage in 2026 | iec.ch via web search; registry remark | medium |
| IEC 61174 Edition 5 (S-100 ECDIS test standard) was still under development, not published, as of October 2026; Edition 4.0 (2015) remains the type-approval basis | Web-search summary (no primary page read) | low–medium (verify) |
| NOAA announced sunsetting of raster/paper charts in a 2019 Federal Register notice; "The raster sunset program was completed in December of 2024 with the cancellation of the last of NOAA's 1,007 paper charts"; replaced by NOAA ENC and the NOAA Custom Chart (NCC) application | https://nauticalcharts.noaa.gov/charts/farewell-to-traditional-nautical-charts.html | high |
| IMO's e-navigation Strategy Implementation Plan (MSC.1/Circ.1595, "Update 1") adopts S-100 as the basis of the Common Maritime Data Structure (CMDS) | Web-search summary citing imo.org; Roadmap v5.0 §4 states "S-100 is the adopted data model for e-navigation" | medium (Roadmap wording high) |
| An IMO/IHO Harmonization Group on Data Modelling (HGDM) exists to align S-100 with IMO Maritime Services | Web-search summary only | low (verify establishment date and terms of reference) |
| IHO GI Registry is hosted/operated with KHOA (Korea Hydrographic and Oceanographic Agency) | registry page footer "KHOA Acknowledgements" | medium |

## Notes and quotes

**What the IHO is to AIS.** The IHO writes none of the AIS radio or message
standards; those are ITU-R, IMO, IEC, IALA and NMEA. The IHO matters to this
handbook in three ways: (1) it defines the official chart data (S-57 ENC today,
S-101 tomorrow) and the display rules (S-52 PresLib) on which AIS targets are
drawn in a type-approved ECDIS; (2) it owns the S-100 framework that IMO has
adopted as the data model for e-navigation and that IALA, IEC and WMO use to
express AtoN, route-plan and met-ocean products that overlap with what AIS
application-specific messages carry today; (3) through MSC.530(106) it has, in
effect, set the 2026–2029 calendar on which bridge software will change.

**S-52 on AIS (verbatim).** "Integration of tracked radar targets provided for
collision avoidance radar (ARPA) and targets tracked by AIS (Automatic
Identification System) into the ECDIS display is another option." (S-52 Ed.
6.1.1 §1.2(b).) And: "By agreement with the IEC, symbols for the 'Navigational
Elements and Parameters' of the IMO PS Appendix 3, and also symbols being
developed by IMO for AIS vessel reports, are included in the Presentation
Library. These are on the last diagram of the ECDIS Chart 1." (§3.2 item 23.)
The colour table reserves token `RESBL` (blue) "for AIS and VTS". The actual
AIS target symbol shapes and behaviours (sleeping/activated, lost target,
vectors) are specified by IEC 62288 and IMO MSC.191(79)/SN.1/Circ.243 — IHO
hosts them in the PresLib by agreement rather than authoring them. Chapter 51
should say this plainly: "AIS symbols on an ECDIS come from IMO/IEC; the chart
under them comes from IHO."

**MSC.530(106) on AIS (verbatim).** §1.6: "The ECDIS display may also be used
for the display of radar, radar tracked target information, AIS and other
appropriate data layers to assist in route monitoring." §7.1–7.3 require that
AIS information come "from systems compliant with the relevant standards of
the Organization", "not degrade the displayed system database information",
be "clearly distinguishable", removable "by single operator action", and share
"a common reference system" with the chart (or an indication be given). These
clauses are the regulatory hook for every "AIS overlay on ECDIS" discussion in
Chapters 51 and 55.

**The 2026/2029 calendar (verbatim).** MSC.530(106) para 2: ECDIS "(a) if
installed on or after 1 January 2029, conforms to performance standards not
inferior to those specified in the annex to the present resolution; (b) if
installed on or after 1 January 2026 but before 1 January 2029, conforms either
to performance standards … in the annex to the present resolution or to …
resolution MSC.232(82)". Note the resolution is a recommendation to
Governments; it binds through SOLAS V/18.4 ("shall conform to the relevant
performance standards not inferior to those adopted by the Organization in
effect on the date of installation"). Existing ECDIS are not forced to upgrade.

**Dual fuel.** IHO Roadmap v5.0: "This 'dual fuel' model is instrumental for
the transition period. From the user's perspective, presentation of
cartographic features to meet the IMO mandated content (ENC = official nautical
chart) should be seamless and presented under the identical presentation
regime." The Roadmap also commits the IHO to assure IMO that "the concurrent
provision of S-57 ENCs and S-101 ENCs will remain through the transition
period" and that both "fulfil the requirements for ENC as defined in IMO ECDIS
instruments". No end date for S-57 ENC production is stated in v5.0; the text
says only that "limited provisions will be made to extend the period" if
residual dependence on S-57 is widespread.

**"Operational" vs "testing".** The registry remarks are consistent: S-101
2.0.0, S-104 2.0.0, S-111 2.0.0, S-124 2.0.0 and S-201 2.0.0 are each "the first
operational Edition"; S-125 1.0.0 and all 1.x editions of the Phase 1 specs are
"released for implementation and testing purposes only". Phase 1 operational
editions are all baselined on S-100 Edition 5.2.0 (June 2024), not 5.0.0 — the
PLAN's "S-100 Ed. 5" shorthand is right but the chapters should cite 5.2.0 for
the product specifications and 5.2.1 (December 2025) as the current framework
edition.

**S-104/S-111 and the VHF data link.** S-104 Ed. 2.0.0 does not mention AIS,
ASM or VDES anywhere. It is an HDF5 gridded time-series product intended for
delivery to ECDIS "by any appropriate means, such as transfer to an accessible
Internet service or via a licensed distribution channel" (§7.4). The idea that
S-104/S-111 would be carried over VDES is an IALA/VDES-side proposition
(see `r-standards-iala.md` G1117 and `r-vdes.md`), not an IHO one. Chapter 54's
line "today over ASM, tomorrow over VDES" should therefore be phrased as: today
IMO SN.1/Circ.289 FI 31 (and USCG DAC 367) carry *point* observations and
forecasts over AIS; S-104/S-111 define *gridded* products for ECDIS delivered
over IP; VDES is a candidate bearer that the IHO specs are agnostic about.

**S-124 and GMDSS.** The Roadmap Annex 2 caption is careful: SOLAS warnings
"are still based on Radiocommunication Services (GMDSS), SOLAS chapter IV.
S-100 MSI related products … are supplementary products (S-124 and S-41x)
until further decisions are taken by IMO." So S-124 over any bearer is
additive to NAVTEX/SafetyNET, not a replacement, as of 2025–26.

**S-125 vs S-201.** Both are S-100 AtoN products, both model
physical/virtual/synthetic AIS AtoN and tie virtual AtoN to an AIS base-station
`RadioStation`. The difference is audience: S-201 (IALA, Ed. 2.0.0 May 2025) is
an authority-to-authority asset exchange that "is not intended to be for
navigation systems like ECDIS"; S-125 (joint IHO/IALA, Ed. 1.0.0 2025/26,
testing only, NIPWG) is the mariner-facing "digital list of lights" meant for
ECDIS/ECS and explicitly includes "local AIS application-specific messages" in
its scope. Chapter 68 can use this pair to explain why an AIS Message 21 you
decode may disagree with a chart: the chart feature (S-57/S-101), the authority
record (S-201) and the broadcast (Message 21, per IALA R0126) are three
different databases.

**S-230 ASM.** Listed by name on the IHO site under IALA's S-2xx range with an
empty scope, and absent from the registry. Treat it as planned, not published.
Do not cite an edition.

**S-421 route plans.** The only S-4xx entry from IEC TC 80; Ed. 1.0.0 is IEC
63173-1:2021. MSC.530(106)/Rev.1 (May 2024) folded route-plan exchange into the
ECDIS performance standard. This is the S-100 product with the clearest
future AIS/VDES tie-in (ship-to-shore route exchange), but no IHO document
specifies a VDL bearer for it either.

**NOAA paper charts.** PLAN ch. 51 says "NOAA's end of traditional paper
charts (2025 (verify))". NOAA's own page: the sunset was announced in 2019 and
"completed in December of 2024 with the cancellation of the last of NOAA's
1,007 paper charts". Correct the chapter to December 2024.

**S-57 is older than AIS.** S-57 Ed. 3.0 (November 1996) predates ITU-R
M.1371-0 (1998) and SOLAS AIS carriage (2002); Ed. 3.1 (November 2000) is still
the ENC format in 2026. A useful line for Chapter 51's *Then & now*: the chart
format under every AIS target on a SOLAS bridge was frozen the year AIS was
first standardized.

## Open questions / (verify)

- IHO membership count and founding dates (21 June 1921; convention in force
  22 September 1970; Protocol in force 8 November 2016; 104 Member States) come
  from a search summary; confirm on https://iho.int/en/member-states or the
  IHO Basic Documents (verify).
- MSC.530(106)/Rev.1: confirm adoption date (24 May 2024), MSC 108 document
  number (MSC 108/20/Add.1 ?), and the exact wording added for route-plan
  exchange; obtain the PDF from IMO Docs/GISIS (verify).
- IEC 61174 Edition 5 status and expected publication date; whether any
  S-100 ECDIS had been type-approved by October 2026 (verify).
- Exact IHO Circular Letter or news item announcing Phase 1 product
  specifications "in force" on 1 January 2026 — locate the CL number (verify).
- S-125 Edition 1.0.0 date: cover says December 2025, copyright June 2026,
  registry 2026-06-01, IHO page "June 2026". Determine the approval CL and
  which date the handbook should cite (verify).
- S-100 Ed. 3.0.0: April 2017 (web page) vs June 2017 (document control
  table, CL 32/2017 dated 2 May 2017). Pick one and footnote the other (verify).
- HGDM (IMO/IHO Harmonization Group on Data Modelling): establishment session
  (NCSR 4, 2017?), current status, any output relevant to AIS ASM/VDES (verify).
- MSC.1/Circ.1595 e-navigation SIP Update 1: confirm date (2018?) and the
  exact CMDS/S-100 wording (verify).
- S-230 ASM: ask IALA whether a draft exists and whether the IALA ASM
  Collection is intended to migrate into it (verify).
- Does S-101 Ed. 2.0.0 or S-98 Ed. 2.0.0 say anything specific about AIS AtoN
  (virtual AtoN portrayal when both chart feature and Message 21 are present)?
  S-101 and S-98 PDFs were not read this session (verify).
- S-52 PresLib 4.0 upgrade deadline for existing ECDIS (31 August 2017, later
  treated pragmatically to 1 July 2018) — from search summaries only; confirm
  with IHO CL / IMO MSC.1/Circ.1503/Rev.1 (verify).
- YMIR-1 VDES satellite S-124 demonstration (October 2025) appeared in a
  search summary with no primary URL; do not cite until a Danish Maritime
  Authority / Sternula / IALA source is found (verify; belongs in `r-vdes.md`).
- IHO S-61 (RNC) edition and whether NOAA's RNC sunset has any S-61 analogue
  elsewhere (UKHO ARCS status) (verify).

## Candidate figures and worked examples

1. **Stack diagram (Ch. 51/52):** three columns — *data* (S-57 ENC → S-101
   ENC; S-104/S-111/S-124/S-125 layers), *presentation* (S-52 PresLib 4.0.4 →
   S-52 Annex A:100 Ed. 5.0.0 and S-101 Portrayal Catalogue; S-98
   interoperability), *regulation* (A.817(19) 1995 → MSC.232(82) 2006 →
   MSC.530(106) 2022 / Rev.1 2024), with AIS entering from the side via IMO
   MSC.191(79)/IEC 62288 symbols "by agreement with the IEC".
2. **Timeline (Ch. 12/52, App. A):** S-57 3.0 Nov 1996 · S-57 3.1 Nov 2000 ·
   S-100 in work programme 2001 · S-100 1.0.0 Jan 2010 · S-52 6.0 Mar 2010 ·
   S-100 2.0.0 Jun 2015 · S-52 6.1.1/PresLib 4.0 Oct 2014 · S-100 4.0.0 and
   S-101 1.0.0 Dec 2018 · S-100 5.0.0 Dec 2022 · MSC.530(106) 7 Nov 2022 ·
   A-3 dual-fuel May 2023 · S-100 5.2.0 Jun 2024 · MSC.530 Rev.1 May 2024 ·
   S-101/S-104/S-111 2.0.0 27 Dec 2024 · S-124 2.0.0 Mar 2025 · S-201 2.0.0
   May 2025 · S-98 2.0.0 Oct 2025 · S-100 5.2.1 Dec 2025 · 1 Jan 2026
   voluntary S-100 ECDIS · S-125 1.0.0 2026 · 1 Jan 2029 mandatory for new
   installations.
3. **Table (Ch. 52, App. B):** product spec | owner/WG | current edition and
   date | status (operational / testing) | S-100 baseline | encoding
   (8211/GML/HDF5) | AIS relevance. Rows: S-101, S-102, S-104, S-111, S-124,
   S-125, S-127, S-128, S-129, S-201, S-230, S-240, S-401, S-411/412, S-421.
4. **Worked example (Ch. 54):** the same water-level observation expressed
   (a) as an IMO SN.1/Circ.289 FI 31 point report over AIS Message 8 (bit
   budget, update cadence, no authentication) and (b) as one grid node of an
   S-104 `dataCodingFormat = 2` HDF5 time series delivered over IP with an S-100
   Part 15 signature. Show what each can and cannot express (uncertainty,
   datum, forecast horizon).
5. **Worked example (Ch. 68):** one virtual AtoN seen three ways — S-57/S-101
   chart feature, S-201 authority record (`VirtualAISAidToNavigation` ↔
   `RadioStation` base station), and the live Message 21 — and a checklist for
   reconciling them.
6. **Box "Definitions that bite" (Ch. 51):** ENC vs ECDIS vs ECS vs RNC vs
   ENDS, using the S-66 and MSC.530(106) definitions verbatim.
7. **Box "Rule of thumb" (Ch. 51):** "If it is a SOLAS ECDIS installed in
   2026–2028 it may be S-57-only, S-100 dual-fuel, or both; after 1 January
   2029 new installs must be S-100. Ask which PresLib/S-98 edition is loaded
   before you argue about how an AIS target is drawn."

## Recommended use by chapter

- **Chapter 12 (2015–present):** S-100 5.0.0 (Dec 2022) and MSC.530(106)
  (7 Nov 2022) as the twin 2022 milestones; dual-fuel decision A3/13 (May
  2023); Phase 1 operational editions 27 Dec 2024–Mar 2025; 1 Jan 2026
  voluntary S-100 ECDIS; NOAA paper-chart sunset completed December 2024
  (correct the "2025 (verify)").
- **Chapter 14 (organizations):** IHO basics (Monaco, 1921/1970/2016, ~104
  Member States — verify), HSSC and its working groups S-100WG, NIPWG, TWCWG,
  WWNWS-SC; the GI Registry; domain allocation of S-1xx/S-2xx/S-4xx to IHO,
  IALA, IOC, IEHG, WMO, IEC, NATO.
- **Chapter 15 (standards narrative) and Appendix B:** S-57 3.1 (Nov 2000,
  Supp. 3 Jun 2014), S-52 6.1.1 + PresLib 4.0.4, S-52 Annex A:100 5.0.0, S-63
  1.2.2, S-64/S-64:100, S-66 2.0.0, S-98 2.0.0, S-100 5.2.1, and the product
  spec table; all free from iho.int except that S-100-ECDIS PresLib and
  security-scheme materials need registration; IEC 63173-1 (S-421) is paid.
- **Chapter 16 (law):** SOLAS V/18.4 and V/19.2.1.4 text as quoted in S-66;
  MSC.530(106) is a recommendation that bites via V/18.4.
- **Chapter 51 (charts and AIS on the display):** S-52 §1.2(b), §3.2(23) and
  RESBL; MSC.530(106) §§1.6, 7.1–7.3; ENC/ECDIS/ECS/RNC/ENDS definitions; the
  1986 NSHC study → COE → CHRIS → HSSC lineage; NOAA December 2024 sunset.
- **Chapter 52 (S-100 family):** S-100 Parts list and edition history; Phase
  1/2/3 table; operational-vs-testing status; dual-fuel; 2026/2029 dates;
  S-104/S-111/S-124/S-421 scopes; the explicit finding that IHO specs are
  bearer-agnostic (no VDL defined) — hand off to Ch. 69 and `r-vdes.md` for
  VDES; S-124 remains supplementary to GMDSS.
- **Chapter 54 (tide/water level/met-ocean):** S-104 Ed. 2.0.0 details (HDF5,
  `dataCodingFormat = 2`, delivery by Internet/licensed channel, S-98 Annex C
  dynamic depth); contrast with Circ.289 FI 31 over AIS; S-111 analogous.
- **Chapter 68 (AtoN):** S-125 vs S-201 model (physical/virtual/synthetic AIS
  AtoN, `RadioStation` = AIS base station), S-201 2.0.0 operational, S-125
  1.0.0 testing; cross-reference IALA R0126 in `r-standards-iala.md`.
- **Chapter 69 (VDES / "AIS 2.0"):** state that no IHO product specification
  mandates VDES; S-421 and S-124 are the products most often paired with VDES
  in trials; S-230 ASM is planned, unpublished.
- **Appendix J:** IHO Secretariat, 4b quai Antoine 1er, MC 98011 Monaco;
  info@iho.int; +377 93 10 81 00; registry.iho.int; HSSC meeting cadence
  (HSSC-18 May 2026, Gdynia).
