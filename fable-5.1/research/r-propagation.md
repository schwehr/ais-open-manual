# Dossier: VHF propagation for AIS — radio horizon, two-ray over sea, ducting, ITU-R P-series models, terrain tools, and AIS as a propagation probe

**Purpose.** This dossier collects what could be confirmed, as of 5 October
2026, about how 162 MHz AIS signals propagate over sea and coast; which ITU-R
P-series recommendations and open terrain models apply; what the published
literature says about observed AIS ranges and anomalous (ducted) reception; and
how received AIS — a dense field of transmitters with known positions, known
nominal power, and known reporting intervals — has been used to observe
tropospheric ducting. It is the primary dossier for **Chapter 29** (propagation
modeling and AIS as a propagation probe) and feeds **Chapter 27** (RF basics:
radio horizon, free-space and two-ray loss, link budgets), **Chapter 37** (shore
siting and coverage prediction), **Chapter 42** (expected ranges for a home
receiver), **Chapter 48** (coverage/detection-probability estimation for honest
maps), **Chapter 59** (receiver-coverage plausibility checks for spoofing
detection), and **Appendix I** (radio-horizon and link-budget calculators).

> Research-session note. ITU-R edition numbers were read from the itu.int
> recommendation pages listed below. Paper metadata (authors, venue, volume,
> pages, DOI, date) were verified against the Crossref API; abstracts quoted
> are Crossref-deposited abstracts or the publisher's page. Where only a search
> summary was seen, the row says so and confidence is lowered. No full-text
> figures from paywalled papers were read in this session.

## Key questions

1. What is the radio horizon for AIS as a function of antenna heights, and how
   does the 4/3-Earth convention enter (d ≈ 4.12(√h₁ + √h₂) km)?
2. What path-loss models apply at 162 MHz over sea: free space (P.525), two-ray
   with sea reflection, spherical-earth diffraction (P.526), point-to-area
   empirical curves (P.1546), the general wide-range model (P.2001), and
   path-specific P.1812; what does each need as input and where does each
   break down?
3. What are evaporation ducts, surface ducts and elevated ducts; how often do
   they occur over the sea areas the book cares about; and what is the evidence
   that they explain 500–1,000 km AIS receptions?
4. Which terrain-aware tools (ITM/Longley–Rice, SPLAT!, Signal Server, Radio
   Mobile, the NTIA ITM C++ code) are open and usable for AIS shore-station
   coverage prediction, and what are their limits over water?
5. Which peer-reviewed studies have measured AIS range statistics or used AIS
   receptions to detect/characterise anomalous propagation?
6. How can a receiver operator turn message counts versus distance into a
   coverage estimate, and what does that imply for Chapter 48?
7. Where does the R-Mode (ranging-mode) work on AIS/VDES touch propagation
   (group delay, multipath, sky-wave for MF; VHF two-ray for VDES)?
8. What is still unproven or contested (e.g., sporadic-E at 162 MHz, troposcatter
   versus ducting as the dominant over-the-horizon mechanism)?

## Primary sources located

| Source | Identifier / edition / year | URL | What it covers | Access |
|---|---|---|---|---|
| Rec. ITU-R P.525 | P.525-5 (11/2024) | https://www.itu.int/rec/R-REC-P.525/en | Free-space attenuation formulae | Free |
| Rec. ITU-R P.526 | P.526-16 (11/2025) | https://www.itu.int/rec/R-REC-P.526/en | Propagation by diffraction (spherical earth, knife-edge, terrain) | Free |
| Rec. ITU-R P.1546 | P.1546-6 (08/2019); earlier -5 (09/2013), -4 (10/2009) | https://www.itu.int/rec/R-REC-P.1546/en | Point-to-area field-strength curves 30 MHz–4 GHz, land/sea/mixed paths, time percentages; the standard tool for coastal coverage planning | Free |
| Rec. ITU-R P.2001 | P.2001-6 (09/2025) | https://www.itu.int/rec/R-REC-P.2001/en | General-purpose wide-range terrestrial model 30 MHz–50 GHz including ducting/layer reflection and troposcatter sub-models | Free |
| Rec. ITU-R P.1812 | P.1812-8 (09/2025) | https://www.itu.int/rec/R-REC-P.1812/en | Path-specific point-to-area prediction VHF/UHF | Free |
| Rec. ITU-R P.453 | P.453-14 (08/2019) | https://www.itu.int/rec/R-REC-P.453/en | Radio refractive index, refractivity N and modified refractivity M; duct statistics | Free |
| Rec. ITU-R P.372 | P.372-18 (09/2026) | https://www.itu.int/rec/R-REC-P.372/en | Radio noise (galactic, atmospheric, man-made) — needed for the VHF noise floor in Chapters 27/31 | Free |
| Rec. ITU-R P.1409 | P.1409-4 (09/2025) | https://www.itu.int/rec/R-REC-P.1409/en | Propagation data for high-altitude platform systems (relevant to Chapter 40 balloons/HAPS) | Free |
| Hufford, Longley & Kissick, *A Guide to the Use of the ITS Irregular Terrain Model in the Area Prediction Mode* | NTIA Report 82-100, 1982; DOI 10.70220/zjkb4hxb | https://doi.org/10.70220/zjkb4hxb | ITM (Longley–Rice) area mode | Free |
| Hufford, *The ITS Irregular Terrain Model, version 1.2.2: The Algorithm* | NTIA memorandum (Crossref year 1999 (verify: often cited as 1995)); DOI 10.70220/9qncd6hb | https://doi.org/10.70220/9qncd6hb | ITM point-to-point algorithm | Free |
| NTIA/ITS ITM source | GitHub `NTIA/itm` (current C++); `NTIA/itm-longley-rice` (archived FORTRAN/C++ v1.2.2) | https://github.com/NTIA/itm ; https://github.com/NTIA/itm-longley-rice | Reference implementation | Free (open source) |
| SPLAT! | John A. Magliacane, KD2BD; Longley–Rice/ITM based; 20 MHz–20 GHz | https://www.qsl.net/kd2bd/splat.html | Terrain coverage, LOS and path-loss maps; SRTM input | Free (GPL) |
| Signal Server | Alex Farrant / Cloud-RF; SPLAT!-derived multi-threaded engine | https://github.com/Cloud-RF/Signal-Server | Coverage and profile generation; multiple models incl. ITM | Free (GPL) |
| Radio Mobile / Radio Mobile Online | Roger Coudé, VE2DBE; ITM-based | https://www.ve2dbe.com/english1.html | Coverage prediction (desktop freeware for amateur use; online service) | Free for amateur use (proprietary) |
| Rautiainen, Johansson, Lensu, Tyynelä, Jalkanen, Hasu, Stenbäck, Lonka, Laakso (family names per Crossref; initials (verify)), "Studying anomalous propagation over marine areas using an experimental AIS receiver set-up" | *Atmos. Meas. Tech.* 19, 2763–2785, 23 April 2026; DOI 10.5194/amt-19-2763-2026 | https://doi.org/10.5194/amt-19-2763-2026 | One year of AIS from two antennas (7 m and 30 m) at Utö, Baltic; over-the-horizon statistics vs. measured refractivity profiles | Free (open access) |
| Valčić, S. & Brčić, D., "On Detection of Anomalous VHF Propagation over the Adriatic Sea Utilising a Software-Defined Automatic Identification System Receiver" | *J. Mar. Sci. Eng.* 11(6), 1170, 2 June 2023; DOI 10.3390/jmse11061170 | https://doi.org/10.3390/jmse11061170 | 24-h SDR AIS campaign, N. Adriatic; 159,965 packets, 54.3 % PER; receptions at hundreds of NM attributed to refraction | Free (open access) |
| Sirkova, I., "Revisiting Enhanced AIS Detection Range under Anomalous Propagation Conditions" | *J. Mar. Sci. Eng.* 11(9), 1838, 2023; DOI 10.3390/jmse11091838 (preprint 10.20944/preprints202308.1720.v1) | https://doi.org/10.3390/jmse11091838 | Parabolic-equation comparison of ducting vs troposcatter path loss at AIS frequencies | Free (open access) |
| Tang, Cha, Wei, Tian, "A Study on the Propagation Characteristics of AIS Signals in the Evaporation Duct Environment" | 2018 International Applied Computational Electromagnetics Society Symposium (ACES); DOI 10.23919/acess.2018.8669309 | https://doi.org/10.23919/acess.2018.8669309 | PE modelling of 162 MHz in evaporation ducts | Paid (IEEE) |
| Høye, G. K., Eriksen, T., Meland, B. J., Narheim, B. T., "Space-based AIS for global maritime traffic monitoring" | *Acta Astronautica* 62(2–3), 240–245, 2008; DOI 10.1016/j.actaastro.2007.07.001 | https://doi.org/10.1016/j.actaastro.2007.07.001 | Satellite AIS geometry, path loss and collision model (see `r-loading.md`) | Paid |
| Grundhöfer, L., Rizzi, F. G., Gewies, S., Hoppe, M., Bäckstedt, J., et al., "Positioning with medium frequency R-Mode" | *NAVIGATION* 68(4), 829–841, 2021; DOI 10.1002/navi.450 | https://doi.org/10.1002/navi.450 | R-Mode Baltic MF results (propagation delay/sky-wave treatment) | Free (open access) |
| Wirsing, Dammann, Raulefs, "Direct Position Estimation for VDES R-Mode" | IEEE/ION PLANS 2023, pp. 724–728; DOI 10.1109/plans53410.2023.10140053 | https://doi.org/10.1109/plans53410.2023.10140053 | VHF ranging on VDES signals | Paid |
| Johnson, Swaszek, Hoppe, Grant, Safar, "Initial Results of MF-DGNSS R-Mode as an Alternative Position Navigation and Timing Service" | ION ITM 2017, pp. 1206–1226; DOI 10.33012/2017.14886 | https://doi.org/10.33012/2017.14886 | R-Mode MF beacons; the ACCSEAS feasibility lineage | Paid (ION) |

## Verified facts

| Fact | Source | Confidence |
|---|---|---|
| Current ITU-R editions: P.525-5 (11/2024); P.526-16 (11/2025); P.1546-6 (08/2019); P.2001-6 (09/2025); P.1812-8 (09/2025); P.453-14 (08/2019); P.372-18 (09/2026); P.1409-4 (09/2025). | itu.int recommendation index pages read 2026-10-05 (URLs above) | high |
| P.1546's scope is "point-to-area predictions for terrestrial services in the frequency range 30 MHz to 4 000 MHz" (title). | https://www.itu.int/rec/R-REC-P.1546/en | high |
| Radio-horizon arithmetic: with effective Earth radius k·a = (4/3)(6,371 km) ≈ 8,495 km, d_km = √(2·8,495·h/1000) = √(16.99 h_m) ≈ 4.12 √h_m; for two terminals d ≈ 4.12 (√h₁ + √h₂) km. Example: h₁ = 30 m, h₂ = 15 m → 4.12(5.48 + 3.87) = 38.5 km ≈ 20.8 nmi. | Derived in this session from the 4/3-Earth convention (the convention itself is standard in ITU-R P.526/P.1546; cite clause (verify)) | high (arithmetic); medium (which ITU clause to cite) |
| Rautiainen et al. 2026: 1-year AIS data from antennas at 7 m and 30 m a.m.s.l. on Utö (59°46′50″ N, 21°22′23″ E), co-located with mast T/RH sensors at 4, 7, 12, 22, 32, 59 m; over-the-horizon observations 34 % of the time (7 m) and 59 % (30 m), mainly spring/summer; receptions up to 600 km; slower RSS decay with distance under ducting; with duct height 59 m, OTH occurrence 90 % (7 m) and 95 % (30 m); strong diurnal cycle in the Archipelago Sea north of Utö, none in open sea to the south. | Abstract and §2 of the paper at https://doi.org/10.5194/amt-19-2763-2026 (read 2026-10-05) | high |
| Rautiainen et al. state that under normal conditions AIS range is "limited to < 100 km". | Introduction, same URL | high (as their statement) |
| Valčić & Brčić 2023: fixed SDR AIS receiver, Northern Adriatic; 24 h from 25 Feb 2023 15:32 LT; 115 targets, 159,965 packets, 54.3 % PER; great-circle distances to decoded positions of "hundreds of Nautical Miles"; by exclusion they attribute the OTH reception to refraction (ducting), not troposcatter, diffraction or sporadic-E. | Crossref-deposited abstract, DOI 10.3390/jmse11061170 | high |
| Sirkova 2023: parabolic-equation comparison; "in most studied cases, the ducting ensures a significantly greater reduction in path loss than troposcatter even when the AIS frequencies are not well trapped in the duct"; emphasis on elevated trapping layers. | Crossref-deposited abstract, DOI 10.3390/jmse11091838 | high |
| Tang et al. 2018 (ACES Symposium) modelled 162 MHz AIS propagation in evaporation ducts. | Crossref record 10.23919/acess.2018.8669309 (title/venue only) | medium (content not read) |
| ITM (Longley–Rice) is documented by NTIA Report 82-100 (Hufford, Longley, Kissick 1982) and the v1.2.2 algorithm memo (Hufford); NTIA publishes C++ source on GitHub (`NTIA/itm`) and archives the v1.2.2 FORTRAN/C++ in `NTIA/itm-longley-rice`. | Crossref DOIs 10.70220/zjkb4hxb, 10.70220/9qncd6hb; search summary citing github.com/NTIA | high (documents); medium (repo details not opened) |
| SPLAT! is by John A. Magliacane (KD2BD), uses ITM, covers 20 MHz–20 GHz; Signal Server (Cloud-RF, Alex Farrant) is a SPLAT!-derived multi-threaded engine; Radio Mobile is by Roger Coudé (VE2DBE), ITM-based, free for amateur use with an online version. | Search summary citing qsl.net, github.com/Cloud-RF, ve2dbe.com (read 2026-10-05) | medium |
| M.1371-6 reserves 14 buffer bits (235.9 NM one-way) and states this "provides protection for a propagation range of over 120 NM" — i.e., the protocol designers budgeted for receptions well beyond the optical horizon. | M.1371-6 §A2-3.2.2.8.2 (see `r-rf-phy.md`) | high |
| Satellite AIS literature treats path loss and footprint geometry explicitly (Høye et al. 2008; Cervera, Ginesi & Eckstein 2011, *Int. J. Satell. Commun. Netw.* 29, 117–142): a "relatively small constellation of LEO satellites can guarantee good ship position detection probability" per Cervera et al.'s abstract. | Crossref records and abstract (10.1002/sat.957) | high (metadata); medium (details) |
| R-Mode Baltic: MF R-Mode positioning results published as Grundhöfer et al. 2021 *NAVIGATION* 68:829–841; sea trials near Rostock published as Rizzi et al. 2023 *Appl. Sci.* 13:1872; VDES R-Mode direct position estimation Wirsing et al. PLANS 2023 and flight experiments PLANS 2025. | Crossref records | high (metadata) |
| Johnson, Swaszek et al. presented "Initial Results of MF-DGNSS R-Mode" at ION ITM 2017 (pp. 1206–1226). The earlier ACCSEAS R-Mode feasibility study (2014) named in the PLAN was not located via Crossref in this session. | Crossref record 10.33012/2017.14886 | high (2017 paper); ACCSEAS 2014 report (verify) |

## Notes and quotes

- **Why the horizon is soft.** The 4.12 √h rule is an *effective-Earth*
  construction for a standard atmosphere (dN/dh ≈ −39 N-units/km). Over sea the
  refractivity gradient is rarely standard: evaporation ducts (tens of metres
  thick, nearly always present over warm water) and elevated/surface ducts
  (from subsidence inversions or advection of warm dry air over cool sea) trap
  VHF energy. Rautiainen et al. found the 30 m Utö antenna over the horizon
  *59 % of the time*; that is the single most useful number for calibrating
  reader expectations that "AIS is line of sight".
- **Quote (Rautiainen et al. 2026, abstract):** "During periods of anomalous
  signal propagation, the AIS messages were received from farther away, from up
  to 600 km from Utö and the observed received signal strength decayed slower
  with distance, indicating reductions in propagation losses due to ducting."
- **Quote (Valčić & Brčić 2023, abstract):** "In certain instances, the SDR AIS
  receiver detected, received and decoded data packets from AIS targets distant
  several orders of magnitude larger than the VHF nominal ranges." (Note for
  the chapter: "orders of magnitude" is the authors' phrasing; their own
  distances are "hundreds of Nautical Miles", i.e., roughly one order of
  magnitude beyond a 20–40 nmi horizon.)
- **Quote (Sirkova 2023, abstract):** "In most studied cases, the ducting
  ensures a significantly greater reduction in path loss than troposcatter even
  when the AIS frequencies are not well trapped in the duct."
- **Trapping at 162 MHz.** A duct traps a frequency only if it is thick enough;
  the usual rule (P.453 / textbook) is that the minimum trapping frequency
  scales with duct thickness^(−3/2). At 162 MHz, thin evaporation ducts
  (10–20 m) are generally *not* strongly trapping; the elevated and surface
  ducts of several tens to hundreds of metres are. This is why Sirkova
  emphasises elevated layers and why Rautiainen's 59 m duct-height statistic
  matters. (Exact P.453 formula (verify) before quoting numbers.)
- **Two-ray over sea.** At 162 MHz with antenna heights of 10–50 m the first
  Fresnel-zone clearance is lost within a few km, and the sea-reflected ray
  (reflection coefficient near −1 for vertical polarization at grazing angles
  below the Brewster angle) produces the classical lobing then a 40 dB/decade
  roll-off until diffraction takes over near the horizon. Tide and sea state
  shift the lobes; ship pitch/roll modulate antenna height. The 2026
  conference paper by Yi ("An Improved Two-Ray Path Loss Model for Maritime
  Channels with Earth Curvature and Rough-Sea Effects", 10.1109/aetcse69203.2026.11504422)
  exists per Crossref but was not read (verify content before citing).
- **Open tools over water.** ITM is a terrain-diffraction model with a
  statistical variability layer; it does not model ducting. SPLAT!, Signal
  Server and Radio Mobile inherit that limit; they are excellent for
  shore-station horizon masks and terrain shadowing (Chapter 37) and
  misleading if read as "maximum range". P.1546 provides sea-path curves at 1 %,
  10 % and 50 % time, which is the ITU way of expressing enhanced-propagation
  statistics; P.2001 contains explicit ducting/layer-reflection and troposcatter
  sub-models and is the better choice when one wants a distribution rather than
  a median.
- **AIS as a probe — what makes it attractive.** Each Class A transmits at a
  nominal 12.5 W (±1.5 dB) at a GNSS-timed instant from a GNSS-reported
  position (`r-rf-phy.md`), so a shore receiver sees thousands of calibrated
  (to within a few dB) sources per day at known ranges and bearings. Rautiainen
  et al. exploit exactly this: distance-binned RSS decay slopes and 95th-
  percentile reception distances as duct indicators, validated against mast
  refractivity profiles. The unknowns are antenna height/gain and feeder loss
  per ship (not broadcast), which is why population statistics rather than
  single-ship fits are used.
- **Satellite lineage.** Høye et al. (2008) and Cervera et al. (2011) set the
  satellite path-loss/footprint framework later reused for VDE-SAT; the
  terrestrial loading/collision side of those papers is handled in
  `r-loading.md`.
- **R-Mode.** The MF R-Mode work (Grundhöfer 2021; Rizzi 2023) is mostly about
  MF beacon ranging but documents the DLR/Baltic testbed and the ranging-error
  budget approach that the VDES R-Mode papers (Wirsing et al. 2023, 2025) carry
  to VHF, where two-ray multipath over sea is the dominant ranging error.

## Open questions / (verify)

- Exact ITU-R clause in P.526 or P.1546 that defines the 4/3 effective Earth
  radius and the horizon distance formula, for a clean citation (verify).
- Exact minimum-trapping-frequency relation and the duct-occurrence statistics
  tables in P.453-14 (verify numbers before quoting in Chapter 29).
- Full author list and affiliations for Rautiainen et al. 2026 (Crossref lists
  nine family names: Rautiainen, Johansson, Lensu, Tyynelä, Jalkanen, Hasu,
  Stenbäck, Lonka, Laakso); confirm initials from the paper (verify).
- Whether Hufford's v1.2.2 algorithm memo is dated 1995 (as commonly cited) or
  1999 (Crossref deposit year) (verify).
- SPLAT! current version and licence; Signal Server supported models list;
  Radio Mobile licence terms for non-amateur use (verify from the sites).
- Any peer-reviewed terrestrial study giving AIS *reception probability vs.
  range* curves for a shore station population (as opposed to case studies of
  anomalous events). Candidates to check: GFW's "AIS reception quality" layer
  documentation; EMSA/HELCOM coverage-assessment reports; USCG NAIS coverage
  verification reports; Danish Maritime Authority coverage maps (verify).
- The PLAN names "Sturm? Lessing?" as possible authors of AIS propagation
  papers — neither name was located in this session; treat as unverified and
  drop unless found.
- The ACCSEAS R-Mode feasibility study (Johnson & Swaszek, 2014) — locate the
  project deliverable PDF (verify).
- Sporadic-E at 162 MHz: Valčić & Brčić considered and excluded it for their
  event; whether any documented AIS reception has been attributed to Es (which
  occasionally reaches ~150–200 MHz) is unknown (verify; likely rare).
- Whether the 2026 "Improved Two-Ray Path Loss Model" conference paper (Yi)
  contains anything usable; read before citing (verify).

## Candidate figures and worked examples

1. **Radio-horizon nomogram (Ch. 27):** d = 4.12(√h₁ + √h₂) km for h₁ ∈ {2, 5,
   10, 20, 30, 50, 100, 200 m} vs h₂ ∈ {5, 15, 30 m}; annotate typical cases
   (yacht masthead 15 m ↔ tanker 40 m; lighthouse 60 m ↔ fishing boat 5 m;
   satellite 600 km → footprint radius ≈ 2,800 km, i.e., the ~5,000 km diameter
   quoted in Chapter 39).
2. **Two-ray vs free-space vs horizon curve (Ch. 27/29):** received power vs
   distance at 162 MHz, 12.5 W, 2.15 dBi each end, h₁ = 30 m, h₂ = 15 m; mark
   −107 dBm sensitivity; show lobing, 40 dB/decade region, diffraction knee.
   Code: `code/rf/two_ray.py`.
3. **Duct schematic (Ch. 29):** modified-refractivity M(h) profiles for
   standard, evaporation duct, surface duct, elevated duct; ray traces.
   Redraw; cite P.453 for definitions.
4. **Utö statistics figure (Ch. 29):** bar chart of OTH occurrence (34 % / 59 %)
   and conditional occurrence at 59 m duct height (90 % / 95 %), with the 600 km
   maximum — from Rautiainen et al. 2026 (open access; redraw from numbers).
5. **Worked example — ducting day vs normal day:** take one receiver's hourly
   95th-percentile reception distance; show how to flag anomalous hours
   (threshold = radio horizon × 1.5, say) and how such hours bias density maps
   (hand-off to Ch. 48).
6. **Worked example — coverage estimate from counts:** for a Class A at
   anchor (3-min reports) and under way (2–10 s), compute expected messages per
   hour; ratio observed/expected vs distance bin → empirical detection
   probability curve; discuss Class B cadence. Code: `code/analytics/coverage_curve.py`.
7. **Tool comparison table (Ch. 29/37):** ITM/SPLAT!/Signal Server/Radio
   Mobile/P.1546/P.2001 — inputs, outputs, models ducting?, open source?,
   licence.
8. **Case file box (Ch. 29):** Valčić & Brčić 24-h Adriatic campaign (115
   targets, 159,965 packets, 54.3 % PER, hundreds of NM) as a reproducible
   SDR experiment.

## Recommended use by chapter

- **Ch. 27:** radio-horizon derivation and nomogram (figure 1); free-space
  formula per P.525; two-ray figure 2; cite P.372 for the VHF noise floor
  (man-made noise categories) when discussing receiver sensitivity margins.
- **Ch. 29:** the model ladder (P.525 → two-ray → P.526 → P.1546 → P.2001/
  P.1812 → ITM tools); ducting physics with P.453 definitions; the three 2023–
  2026 AIS papers as the evidence base (Rautiainen for statistics, Valčić &
  Brčić for a case, Sirkova for mechanism); AIS-as-probe method; limits (ship
  antenna height unknown, Class B power differences, receiver gain changes).
- **Ch. 30/39:** hand off Høye 2008 and Cervera 2011 geometry to the loading
  and satellite chapters.
- **Ch. 37:** use ITM-based tools for horizon masks and terrain shadowing;
  warn that none model ducting; recommend P.1546 1 %/10 % time curves to
  anticipate interference from distant base stations and co-channel traffic.
- **Ch. 42:** set expectations: 20–40 nmi typical for a rooftop antenna at
  15–30 m with ship antennas at 10–40 m; occasional 100–300+ nmi under ducting,
  especially spring/summer over cool water (Baltic, Mediterranean, California
  coast); point to the Utö percentages.
- **Ch. 48:** every density/coverage product must either model or exclude
  anomalous-propagation hours; the Utö 59 % figure shows this is not a corner
  case for elevated coastal receivers.
- **Ch. 59:** range-plausibility checks must allow for ducting; a report from
  400 km is not proof of spoofing — corroborate with other receivers and
  timing.
- **Ch. 65:** R-Mode: cite Grundhöfer 2021 (MF) and Wirsing 2023/2025 (VDES) as
  the peer-reviewed anchors; the ACCSEAS 2014 feasibility report remains (verify).
- **App. I:** `radio_horizon.py`, `two_ray.py`, `coverage_curve.py`.
