# Dossier: Antennas for AIS — types and patterns, installation guidance (SN/Circ.227, COMSAR), splitters, cable loss at 162 MHz, and choices for ships, small craft, tiny devices, shore stations and satellites

**Purpose.** This dossier records what could be confirmed, as of 5 October
2026, about AIS antenna practice: the installation guidance in IMO SN/Circ.227
(2003, as amended) and the COMSAR.1/Circ.32/Rev.3 separation rule quoted in
ITU-R M.1371-6; the physics that follows from a 1.85 m wavelength (dipole,
quarter-wave ground plane, 5/8-wave and collinear gain whips, J-pole, Yagi for
shore); why gain hurts on a rolling small boat; active VHF/AIS antenna
splitters and their failure modes; coaxial cable loss at 162 MHz; antenna
choices for AIS-SART/MOB/EPIRB and AtoN devices and for satellites; and simple
testing with a VNA. It is the primary dossier for **Chapter 32** and feeds
**Chapter 27** (link budget gains and losses), **Chapter 31** (separation and
coupling), **Chapter 36** (antenna/feeder faults, VSWR alarms), **Chapter 37**
(shore-station antennas), **Chapter 39** (satellite antennas), **Chapter 42**
(home receiver antenna build), and **Chapter 68** (tiny-device antennas).

> Research-session note. SN/Circ.227 was downloaded from wwwcdn.imo.org and
> text-extracted; quotations below are verbatim from that PDF. The COMSAR note
> is as quoted inside M.1371-6 (itu.int PDF). Cable-loss and splitter figures
> come from search summaries of vendor data and are marked medium — confirm
> against the manufacturers' datasheets before print. Antenna-theory numbers
> (dipole gain, wavelength) are standard physics, computed here.

## Key questions

1. What do SN/Circ.227 and the COMSAR circular actually say about AIS VHF
   antenna location, separation, cabling and grounding — and where do they
   disagree (5 m vs 10 m same-level separation)?
2. What antenna types are used for AIS, with what gain/pattern, and how does
   vessel motion interact with elevation pattern (why a 9 dBi whip on a
   sailboat is a bad idea)?
3. Should an AIS antenna be tuned for 162 MHz rather than the 156–157 MHz voice
   band, and how much does it matter (VSWR vs frequency, bandwidth of a whip)?
4. How do VHF/AIS splitters work (active, fail-safe, VHF priority), what do
   they cost in dB, and how do they fail?
5. What is the feeder loss per metre at 162 MHz for common cables (RG-58,
   RG-8X, RG-213/214, LMR-240, LMR-400) and what does SN/Circ.227 recommend?
6. What antennas do AIS-SART/MOB/EPIRB-AIS and AIS AtoN use, and what does
   "1 W e.i.r.p." imply for them?
7. What do shore stations and satellites use, and why (height vs. sector
   coverage; circular polarisation and Faraday rotation at VHF)?
8. How does one test an installation (VSWR with a VNA/SWR meter, received
   message statistics) and what do the IEC test standards require?

## Primary sources located

| Source | Identifier / edition / year | URL | What it covers | Access |
|---|---|---|---|---|
| IMO SN/Circ.227, *Guidelines for the installation of a shipborne Automatic Identification System (AIS)* | 6 January 2003 (NAV 48 July 2002; MSC 76 Dec 2002); amended by SN/Circ.245 (15 Dec 2004, UPS recommendation per secondary sources); Corr.1 (2008), Corr.2 (2017) administrative | https://wwwcdn.imo.org/localresources/en/OurWork/Safety/Documents/AIS/SN.1-Circ.227.pdf (read 2026-10-05) | §2.1 interference to VHF radiotelephone; §2.2 VHF antenna location/cabling/grounding; §2.3 GNSS antenna; later sections on reference points, pilot plug, power | Free |
| IMO COMSAR.1/Circ.32/Rev.3 §5.2.8 (as quoted in M.1371-6) | — | quoted at M.1371-6 Table 7 note (itu.int PDF p. 15) | AIS/VHF antenna separation: 2 m vertical, 5 m same-level | Free |
| Rec. ITU-R M.1371-6 | 02/2026 | https://www.itu.int/dms_pubrec/itu-r/rec/m/R-REC-M.1371-6-202602-I!!PDF-E.pdf | Power classes; receiver sensitivity; §A2-2.14 antenna open/short safety; Annex 8 1 W e.i.r.p. for burst devices | Free |
| 33 CFR 164.46 (USCG AIS carriage) | eCFR | https://www.ecfr.gov/current/title-33/section-164.46 | "properly installed" — compliance via SN/Circ.227 as amended or NMEA 0400 (per NAVCEN restatement) | Free |
| NMEA 0400 Installation Standard | v3.10 (verify) | https://www.nmea.org/ | US alternative installation standard named by NAVCEN | Paid |
| IEC 61993-2 Ed. 3.0 (2018); IEC 62287-1/-2; IEC 61097-14; ETSI EN 303 098 | — | webstore.iec.ch; etsi.org | Equipment tests incl. antenna port requirements; MOB device e.i.r.p. | Paid (IEC) / Free (ETSI) |
| Times Microwave LMR datasheets (LMR-400, LMR-240) | current | https://www.timesmicrowave.com/ (403 to fetcher this session) | Attenuation vs frequency | Free |
| Vesper Marine (Garmin) SP160 splitter; Digital Yacht SPL2000 | product pages | vendor sites (not fetched) | Active splitter specs: fail-safe, VHF priority, receive gain | Free |
| ARRL Antenna Book | current edition (verify) | https://www.arrl.org/ | Dipole/ground-plane/collinear/J-pole/Yagi theory and patterns | Paid |

## Verified facts

| Fact | Source | Confidence |
|---|---|---|
| SN/Circ.227 is dated 6 January 2003; NAV 48 (8–12 July 2002) agreed the guidelines "for use on a voluntary basis"; MSC 76 (2–13 December 2002) approved them; they are "meant to be used by manufacturers, installers and surveyors". | SN/Circ.227 cover, paras 1–2 | high |
| SN/Circ.227 §2.1: AIS "may cause interference to a ship's VHF radiotelephone … as a periodic (e.g. every 20 s) soft clicking sound", more noticeable when antennas are close and the radiotelephone is on "channels near the AIS operating channels (e.g. channels 27, 28 and 86)". | SN/Circ.227 Annex §2.1 | high |
| SN/Circ.227 §2.2.1 location rules: omnidirectional vertical polarisation; "elevated position … minimum of 2 metres in horizontal direction from constructions made of conductive materials"; not close to any large vertical obstruction; "see the horizon freely through 360°"; "preferably at least 3 m away from and out of the transmitting beam" of radar and other transmitting antennas; "directly above or below the ship's primary VHF radiotelephone antenna, with no horizontal separation and with a minimum of 2 m vertical separation. If it is located on the same level as other antennas, the distance apart should be at least 10 m." | SN/Circ.227 Annex §2.2.1 | high |
| SN/Circ.227 §2.2.2 cabling: keep cable short; "Double screened coaxial cables equal or better than RG214 are recommended"; waterproof outdoor connectors; separate cable channels at least 10 cm from power cables; cross at 90°; minimum bend radius 5 × cable outside diameter. §2.2.3: coax screen grounded at one end. | SN/Circ.227 Annex §2.2.2–2.2.3 | high |
| SN/Circ.227 §2.3 GNSS antenna: clear view of sky; at least 3 m from and out of the beam of S-band radar/Inmarsat (and the ship's own AIS VHF antenna if separate); GNSS coax ≥ 1 m from high-power lines; crossing at 90°; pre-amplifier gain matched to cable loss. | SN/Circ.227 Annex §2.3 | high |
| M.1371-6 quotes COMSAR.1/Circ.32/Rev.3 §5.2.8 with the same 2 m vertical rule but "at least 5 metres" for same-level separation — a numerical disagreement with SN/Circ.227's 10 m. | M.1371-6 p. 15; SN/Circ.227 §2.2.1 | high |
| M.1371-6 §A2-2.14: AIS stations "should not be damaged by the effects of open circuited or short-circuited antenna terminals". | M.1371-6 p. 17 | high |
| Burst devices (AIS-SART, MOB-AIS, EPIRB-AIS): "Nominal 1 W e.i.r.p." — a *radiated* figure, so the device's small helical/whip antenna efficiency is already included. | M.1371-6 Annex 8 Tables 86 and 89 | high |
| Class A high power is 12.5 W conducted (±1.5 dB); Class B "SO" 5 W; Class B "CS" 33 dBm (2 W) conducted. | M.1371-6 Table 3, §A2-2.12.2, Table 35 | high |
| Wavelength at 162.0 MHz: λ = 299.79/162.0 = 1.851 m; half-wave 0.925 m; quarter-wave 0.463 m (free-space, before end-effect shortening of ~5 %). | Computed | high |
| Half-wave dipole gain 2.15 dBi (0 dBd); quarter-wave ground plane over a good plane ≈ 2–3 dBi with elevation pattern tilted up by a finite ground; 5/8-wave ≈ 3 dBi over ideal ground; two-element collinear whips sold as "6 dBi"/"9 dBi" achieve their gain by compressing the elevation beamwidth to roughly ±15°/±10° (order of magnitude; exact figures depend on design). | Standard antenna theory (ARRL Antenna Book); beamwidth numbers approximate (verify against a specific datasheet before quoting) | high (dipole/λ) / medium (beamwidths) |
| Typical attenuation at 150 MHz (dB per 100 ft): LMR-400 ≈ 1.5; LMR-240 ≈ 3.0; RG-213 ≈ 2.8; RG-8X ≈ 4.7; RG-58 ≈ 6.2. (Per 30.5 m; multiply by 3.28 for dB/100 m.) | Search summary of standard reference charts (2026-10-05) | medium — confirm from manufacturer datasheets |
| Active splitters: Vesper SP160 claimed VHF-RX insertion loss < 1.5 dB, TX insertion loss < 1 dB, 12 dB AIS receive gain, fail-safe to VHF, VHF transmit priority, AM/FM output; Digital Yacht SPL2000 "ZeroLoss" with a 3 dB pre-amplifier, fail-safe; Shakespeare 5257-S is receiver-only (not for transponders). | Search summary of vendor pages (2026-10-05) | medium — verify on datasheets |
| 33 CFR 164.46 requires AIS to be "properly installed"; NAVCEN restates that compliance may be shown via SN/Circ.227 as amended (SN/Circ.244, 245, SN.1/Circ.289) or NMEA 0400 (version per NAVCEN (verify)). | Search summary citing navcen.uscg.gov | medium |

## Notes and quotes

- **Quote (SN/Circ.227 §2.2.1):** "The objective for the AIS VHF antenna is to
  see the horizon freely through 360°."
- **Quote (SN/Circ.227 §2.2.1):** "Digital communication is more sensitive
  than analogue/voice communication to interference created by reflections in
  obstructions like masts and booms."
- **Definitions that bite — 5 m or 10 m?** Two IMO-lineage texts give
  different same-level separations (COMSAR.1/Circ.32/Rev.3 §5.2.8: 5 m, as
  quoted by ITU; SN/Circ.227: 10 m). Both agree on the preferred solution:
  stack the AIS antenna directly above or below the VHF antenna with ≥ 2 m
  vertical separation (collinear vertical antennas have a null along their
  axis, which is why vertical stacking beats horizontal spacing). Chapter 32
  should present both numbers with sources and recommend the stricter one.
- **Why the 20 s click.** A Class A at 10 s on alternating channels puts a
  26.7 ms burst on each channel every 20 s — hence "periodic (e.g. every 20 s)
  soft clicking" in a nearby voice receiver on channels 27/28/86 (adjacent to
  161.950–162.025 MHz). It is a handy diagnostic for a too-close installation.
- **Gain vs roll.** A gain whip narrows the vertical beam. A sailing yacht
  heeled 20° points a ±10° beam at the sea on one side and the sky on the
  other; the far ship falls out of the main lobe exactly when it matters.
  Practical guidance (consistent with vendor literature): ≤ 3 dBi on
  sailboats/small powerboats, 6 dBi on stable powerboats, 9 dBi only on large
  stable platforms or shore. Treat specific beamwidth numbers as approximate
  unless a datasheet pattern is cited.
- **Tuning.** A quarter-wave or half-wave whip cut for 156.8 MHz (ch. 16) is
  3 % off at 162 MHz; a typical marine whip has a 2:1 VSWR bandwidth of several
  MHz, so the penalty is a few tenths of a dB — usually negligible. Narrowband
  helical or loaded designs can be worse. "AIS-tuned" antennas centred on
  162 MHz are a modest optimisation, not a necessity; measure VSWR at 161.975/
  162.025 MHz with a VNA to decide.
- **Splitters.** An active splitter senses VHF transmit and disconnects the
  AIS; in the AIS-transmit direction it routes the transponder's 2–12.5 W to
  the antenna. Failure modes to list: (1) power loss → fail-safe relay gives
  VHF the antenna, AIS goes deaf/silent (and may alarm "VSWR"); (2) slow or
  chattering switching → VHF transmit leaks into the AIS front end (desense or
  damage); (3) receiver-only splitters wired to a transponder → transponder
  power into a passive splitter (damage, high VSWR alarms); (4) added
  insertion loss on VHF transmit (≈ 1 dB) — acceptable; (5) the LNA in
  "zero-loss" units can overload near strong transmitters (Chapter 31).
  Chapter 32 should note that a dedicated AIS antenna avoids all of these at
  the cost of one more cable and mast position, and that SN/Circ.227 says
  nothing about splitters (it assumes a dedicated mandatory AIS antenna).
- **Cable budget example.** 30 m of RG-58 at 162 MHz ≈ 6.1 dB; RG-213/214
  ≈ 2.8 dB; LMR-400 ≈ 1.5 dB. For a 12.5 W transmitter, RG-58 delivers ≈ 3.1 W
  to the antenna; LMR-400 ≈ 8.8 W. For receive, 4.6 dB difference is ≈ 25–40 %
  range in the two-ray/diffraction regime. SN/Circ.227's "RG214 or better" is
  therefore about loss *and* double screening.
- **Tiny devices.** AIS-SART/MOB/EPIRB-AIS antennas are electrically short
  helicals or whips a few tens of cm long, often floating at sea level; the
  standard specifies e.i.r.p., not conducted power, precisely because antenna
  efficiency and height are part of the device. Expect ranges of a few nmi to
  a ship antenna at 30 m (horizon from 1 m height ≈ 4 km + ship horizon
  ≈ 22 km → ≈ 26 km optical/radio horizon; detection usually limited by the
  1 W e.i.r.p. and sea clutter of the pattern). AtoN antennas on buoys are
  similarly low; IALA R0126/G1050 (see `r-standards-iala.md`) cover siting.
- **Shore stations.** Height buys horizon (4.12 √h): 30 m → 22.6 km own
  horizon; 100 m → 41 km. Collinear omnis (6–9 dBi) are standard; sector or
  Yagi antennas are used where coverage is one-sided (a coast) and where
  land-side interference must be rejected (Chapters 31/37). More height also
  means more distant interferers and more ducting receptions (Chapter 29).
- **Satellites.** Ship AIS is vertically polarised at the source but arrives
  at a LEO satellite with arbitrary polarisation after Faraday rotation at
  VHF and varying geometry; missions therefore use dipoles/monopoles with
  tolerance for polarisation mismatch or circularly polarised antennas, and
  multi-antenna receivers exploit polarisation/space diversity for
  decollision (see `r-loading.md`). Specific antenna designs per mission
  (AISSat-1, NORAIS, ORBCOMM OG2, Spire) are not verified here (verify in
  `r-satellite-ais.md`).
- **Testing.** VSWR sweep 150–170 MHz with a nanoVNA-class instrument at the
  transponder end of the feeder (includes cable); return loss > 14 dB (VSWR
  < 1.5:1) at 161.975/162.025 MHz is a good target; a flat 1.0:1 reading
  usually means the cable is lossy, not the antenna perfect. Then confirm with
  message statistics: own-ship reports seen by a shore receiver (MarineTraffic
  "my ship") and received-range histograms.

## Open questions / (verify)

- SN/Circ.245 content and date (15 December 2004; UPS recommendation) — read
  the circular (verify). Confirm whether SN/Circ.244 relates to AIS
  installation as NAVCEN implies (verify).
- Whether a consolidated "SN.1/Circ.227/Rev.1" exists (a 2022-era NCSR/MSC
  revision was rumoured) (verify); as of this session only Corr.1 (2008) and
  Corr.2 (2017) were seen in secondary sources.
- COMSAR.1/Circ.32/Rev.3 — obtain the circular itself to confirm §5.2.8
  wording and date (verify).
- Cable attenuation figures from manufacturer datasheets (Times Microwave
  LMR-400/240; Belden RG-213/RG-58/RG-8X) (verify).
- Splitter specifications from current Garmin/Vesper SP160 and Digital Yacht
  SPL2000 datasheets, including switching time and LNA gain (verify).
- Whether IEC 61993-2 or 62287-1 specify any antenna-port VSWR alarm threshold
  or splitter requirements (verify).
- Vendor pattern data for 3/6/9 dBi marine whips to replace the approximate
  beamwidths above (verify).
- NMEA 0400 current version and its AIS antenna clauses (verify).

## Candidate figures and worked examples

1. **Mast layout figure (Ch. 32):** VHF and AIS antennas stacked with 2 m
   vertical separation; radar beam exclusion ≥ 3 m; 2 m horizontal clearance
   from conductive structures; GNSS antenna ≥ 3 m from S-band radar/Inmarsat —
   all from SN/Circ.227 §2.2–2.3; call out the 5 m/10 m discrepancy.
2. **Elevation-pattern vs heel figure:** 2 dBi dipole vs 6 dBi vs 9 dBi
   collinear, boat heeled 0°/15°/25°, with the far-ship horizon direction
   marked (patterns computed or redrawn from a cited datasheet).
3. **VSWR vs frequency figure:** a 156.8 MHz-cut whip measured 150–170 MHz;
   loss penalty at 162 MHz in dB (original nanoVNA capture for Ch. 42).
4. **Cable-loss table at 162 MHz:** dB per 10 m and per 30 m for RG-58, RG-8X,
   RG-213/214, LMR-240, LMR-400; delivered power from 12.5 W; receive range
   impact.
5. **Worked example — splitter vs dedicated antenna:** link budget both ways
   including 1 dB TX insertion loss and 12 dB RX LNA; show when the LNA helps
   (long lossy cable) and when it hurts (strong local transmitters).
6. **Tiny-device horizon sketch (Ch. 68):** 1 m antenna height to 30 m ship
   antenna = ~26 km geometric; typical detection ranges far shorter;
   explain e.i.r.p.
7. **Shore-station height vs horizon table (Ch. 37):** 10/30/60/100/200 m.
8. **Checklist box (Ch. 32):** SN/Circ.227 installer checklist condensed
   (location, separation, cable type, bend radius, grounding, GNSS).

## Recommended use by chapter

- **Ch. 27:** dipole 2.15 dBi reference; cable-loss table; e.i.r.p. vs
  conducted power definitions using the SART 1 W e.i.r.p. example.
- **Ch. 31:** separation rules (2 m vertical; 5/10 m horizontal; 3 m from
  radar beam) and the 20 s click as a diagnostic.
- **Ch. 32:** the whole dossier — types, roll argument, tuning, splitters and
  their failure modes, cables, installation checklist, VNA testing, by
  platform (large ship, small craft, tiny devices, shore, satellite).
- **Ch. 36:** antenna/feeder faults (water ingress, connector corrosion,
  splitter failure) and how they present (VSWR alarm, one-way visibility).
- **Ch. 37:** shore antenna choice and height; sector antennas for
  interference rejection.
- **Ch. 39:** polarisation and multi-antenna receivers; defer specifics to
  `r-satellite-ais.md`.
- **Ch. 42:** build/tune a half-wave dipole or J-pole for 162 MHz; VSWR
  measurement; FM notch placement (with `r-noise.md`).
- **Ch. 68:** burst-device antennas and e.i.r.p.
- **App. B:** SN/Circ.227 (2003) + SN/Circ.245 (2004) + Corr.1/2; COMSAR.1/
  Circ.32/Rev.3; NMEA 0400.
