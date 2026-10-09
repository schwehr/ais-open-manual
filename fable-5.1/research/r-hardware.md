# Dossier: Hardware and SDR for AIS receive and transmit

**Purpose.** This dossier maps the AIS equipment landscape as it can be
confirmed in October 2026: the transponder market and its OEM structure (SRT
Marine Systems as module/OEM supplier and owner of em-trak; Garmin's 2022
acquisition of Vesper Marine), the main Class A and Class B brands and
representative models, dedicated receivers (Wegmatt dAISy family, Comar,
Shine Micro, Quark-elec), software-defined radio (SDR) hardware and the
open-source receiver software that runs on it (AIS-catcher, rtl-ais, gr-ais,
gnuais, SDRangel), the transmit-capable research tools and their legal status
(Trend Micro's AIS BlackToolkit / gr-aistx; SDRangel's AIS modulator), and the
type-approval regime (FCC Part 80 certification and equipment class "AIS";
USCG type approval; EU MED wheelmark for Class A; IEC 61993-2 / 62287 test
standards). It feeds **Chapter 33** (Hardware and SDR for receive and transmit)
primarily, and supplies material to **Chapter 15** (type approval in the
standards chain), **Chapter 20** (station classes and power), **Chapter 28**
(demodulator design notes), **Chapter 42** (home receiver tiers), **Chapter 44**
(SDR software history), **Chapter 59/60** (transmit tools in the threat model),
**Chapter 12** (market consolidation), and **Appendix F** (hardware catalogue).

> Research-session note. Facts marked *high* were read directly from the
> cited URL during this session (2026-10-05) — project READMEs were fetched
> raw from GitHub; vendor pages were fetched where they rendered. Facts marked
> *medium* come from search summaries quoting vendor or regulator pages not
> opened directly. Model lists are illustrative, not exhaustive; every model
> number should be re-checked against the vendor page before print.

## Key questions

1. Who actually designs and builds AIS transponders, and how concentrated is
   the supply chain behind the many retail brands?
2. What are the representative Class A, Class B CS, Class B SO ("B+"), AtoN,
   SART/MOB and receive-only products, with the parameters a buyer or analyst
   needs (power, GNSS, interfaces, approvals)?
3. Which SDRs are suitable for AIS reception, what are their relevant limits
   (bandwidth, bit depth, frequency stability), and which software decodes AIS
   from them?
4. Which tools can *transmit* AIS, what exactly do they contain, and what is
   their legal status? (The book must describe, not instruct.)
5. How does type approval work (FCC Part 80 / USCG / EU MED / IEC tests), who
   does the testing, and what does it cost? (Cost data is sparse; record what
   can be confirmed.)
6. What public artefacts (FCC ID exhibits, test reports, teardowns) let an
   author describe the inside of a transponder without vendor cooperation?
7. Which hardware facts matter for the failure-mode and fingerprinting
   chapters (common RF chipsets, shared firmware lineages)?

## Primary sources located

| Source | Identifier / edition / year | URL | What it covers | Access |
|---|---|---|---|---|
| SRT Marine Systems plc, "Transceivers" | corporate page, accessed 2026-10-05 | https://srt-marine.com/transceivers/ | OEM & technology transceiver solutions ("standard OEM product platforms which are easily rebranded and certified under your own name"); AIS transceiver modules; AIS AtoN; em-trak as SRT's own retail brand with "4,000+ reseller partners" | Free |
| Garmin, Vesper Marine acquisition | press release / support notice, 3 Jan 2022 | https://www.garmin.com/ (newsroom; support transition notice) | Garmin acquired Vesper Marine (Auckland, NZ), maker of Cortex and smartAIS; terms undisclosed | Free |
| AIS-catcher README | jvde-github/AIS-catcher, main branch, read 2026-10-05 | https://raw.githubusercontent.com/jvde-github/AIS-catcher/main/README.md | Supported SDRs (RTL-SDR incl. ShipXplorer dongle and RTL-SDR Blog v4, Airspy Mini/R2/HF+, HackRF, HydraSDR, SDRplay, SoapySDR, file/network ZMQ/RTL-TCP/SpyServer); GPL-3.0; copyright 2021–2026; disclaimer on legality of reception; dAISy-catcher hardware with Wegmatt; aiscatcher.org community | Free |
| rtl-ais README | dgiardini/rtl-ais, master, read 2026-10-05 | https://raw.githubusercontent.com/dgiardini/rtl-ais/master/README.md | `rtl_ais` command; defaults 161.975/162.025 MHz; frequencies must be within 1.2 MHz; 24 kHz sample rate; UDP/TCP NMEA output on port 10110; built on librtlsdr | Free |
| SDRangel AIS modulator plugin readme | f4exb/sdrangel, `plugins/channeltx/modais/readme.md`, read 2026-10-05 | https://raw.githubusercontent.com/f4exb/sdrangel/master/plugins/channeltx/modais/readme.md | GUI controls: FM deviation, BT bandwidth, message type, MMSI, status, lat/lon, COG/SOG/heading, repeat, TX; UDP input of NMEA | Free |
| Trend Micro "ais" repository | github.com/trendmicro/ais, read 2026-10-05 (HTML) | https://github.com/trendmicro/ais | "Toolkit for research purposes in AIS. See the website for the paper." Contains `AiS_TX.py`, `AiS_TX.grc`, `AIVDM_Encoder.py`, `gr-aistx` ("AIS BlackToolkit") | Free |
| Balduzzi, Pasta & Wilhoit | ACSAC '14, pp. 436–445, DOI 10.1145/2664243.2664257 | https://doi.org/10.1145/2664243.2664257 | Security evaluation of AIS; the paper behind the transmit toolkit; SDR-based spoofing, hijacking, availability attacks | Paid (ACM) / preprint on Trend Micro site |
| gr-ais | github.com/bistromath/gr-ais (Nick Foster) | https://github.com/bistromath/gr-ais | GNU Radio OOT AIS receiver (NRZI, HDLC, NMEA output); SoapySDR/file/UDP input | Free |
| gnuais | github.com/rubund/gnuais; sourceforge project page | https://github.com/rubund/gnuais ; https://gnuais.sourceforge.net/ | Audio-input AIS decoder for Linux (discriminator audio), MySQL output, `gnuaisgui` | Free |
| Wegmatt LLC (dAISy) | site, read 2026-10-05 | https://wegmatt.com/ | dAISy USB, dAISy 2+, dAISy HAT product manuals; US distributor for Uputronics filtered preamps; firmware on GitHub (astuder/dAISy) | Free |
| Wegmatt dAISy-catcher manual | PDF linked from AIS-catcher README | https://wegmatt.com/files/dAISy-catcher%20AIS%20Receiver%20Manual.pdf | Dual-channel dedicated receiver that feeds AIS-catcher over serial/USB/Pi HAT | Free |
| USCG NAVCEN AIS FAQ | accessed 2026-10-05 | https://www.navcen.uscg.gov/ais-frequently-asked-questions | "Only those … certified to meet stringent standards" are AIS; US Class B not user-configurable (47 CFR 80.231); USCG type-approval list via CGMIX EQList "Shipborne AIS"; FCC OET search "Equipment Class—AIS"; AIS AtoN require FCC/NTIA certification with USCG consultation | Free |
| 47 CFR 80.231 | eCFR | https://www.ecfr.gov/current/title-47/chapter-I/subchapter-D/part-80/subpart-F/section-80.231 | Technical requirements for Class B AIS equipment (IEC 62287 reference; static data programming restrictions) | Free |
| FCC OET Equipment Authorization Search | database | https://apps.fcc.gov/oetcf/eas/reports/GenericSearch.cfm | Grants, test reports, internal photos, user manuals by FCC ID; equipment class "AIS" | Free |
| EU MED 2014/90/EU and current Implementing Regulation | Directive 2014/90/EU; item "MED/4.32 Universal AIS" (verify item number — older lists used 4.14) | https://eur-lex.europa.eu/ | Class A AIS is MED equipment (wheelmark via notified body, Module B type-examination); Class B is outside MED and falls under RED 2014/53/EU | Free |
| IEC 61993-2 | Ed. 3.0, 2018 (verify edition) | https://webstore.iec.ch/ | Class A test standard | Paid |
| IEC 62287-1 / 62287-2 | Class B CS / Class B SO test standards (editions (verify)) | https://webstore.iec.ch/ | Class B test standards | Paid |
| Shine Micro, Comar Systems, Quark-elec product pages | vendor pages (not opened) | https://www.shinemicro.com/ ; https://comarsystems.com/ ; https://www.quark-elec.com/ | Dedicated receivers (RadarPlus series; SLR-350N/R400N network receiver; QK-A026/A026+) | Free |

## Verified facts

| Fact | Source | Confidence |
|---|---|---|
| SRT Marine Systems plc (Midsomer Norton, Bath, UK) sells "OEM & Technology Transceiver Solutions" and describes "standard OEM product platforms which are easily rebranded and certified under your own name", plus AIS transceiver modules for integration "from an existing navigation device to a drone or satellite" | https://srt-marine.com/transceivers/ (read) | high |
| em-trak is SRT's own brand for dealer/distributor resale, "4,000+ reseller partners" | Same page | high |
| SRT's two business lines are Systems (government MDA) and Transceivers | Same page; SRT annual reports | high |
| Garmin announced the acquisition of Vesper Marine (Auckland) on 3 Jan 2022; terms undisclosed; Vesper's Cortex VHF/AIS hub continued under Garmin | Garmin newsroom / support notice via search summary | medium-high |
| AIS-catcher: C++ dual-channel SDR AIS receiver; GPL-3.0; copyright 2021–2026; supports RTL-SDR (incl. RTL-SDR Blog v4 and ShipXplorer dongle), Airspy Mini/R2/HF+, HackRF, HydraSDR, SDRplay, SoapySDR, and file/network input (ZMQ, RTL-TCP, SpyServer); outputs NMEA via screen/UDP/HTTP/TCP; built-in web server; community map at aiscatcher.org | AIS-catcher README (read raw) | high |
| AIS-catcher's README states it is a hobby project "not … designed for reliability" and must not be relied upon for navigation or safety of life; it warns that legality of AIS reception varies by administration | Same README | high |
| AIS-catcher recommends the "dAISy-catcher", a dual-channel dedicated receiver developed with Wegmatt, connecting over serial/USB or as a Raspberry Pi HAT | Same README | high |
| rtl-ais defaults: left 161.975 MHz, right 162.025 MHz, both within 1.2 MHz; 24 kHz sample rate (down to 12 kHz); NMEA to 127.0.0.1:10110 by default; depends on librtlsdr/libusb/pthread; builds on Linux/Windows/macOS | rtl-ais README (read raw) | high |
| SDRangel includes an AIS modulator (channel TX plugin "modais") with controls for FM deviation, BT bandwidth, message type, MMSI, nav status, lat/lon, COG/SOG/heading, repeat and TX, and accepts NMEA over UDP | SDRangel modais readme (read raw) | high |
| Trend Micro's `trendmicro/ais` repository is described as "Toolkit for research purposes in AIS" and contains `AiS_TX.py`, `AiS_TX.grc`, `AIVDM_Encoder.py` and `gr-aistx` (the "AIS BlackToolkit") | GitHub page (read) | high |
| Balduzzi, Pasta & Wilhoit, "A security evaluation of AIS automated identification system", ACSAC 2014, pp. 436–445, DOI 10.1145/2664243.2664257 | Crossref record | high |
| The original gr-aistx targets GNU Radio 3.6/3.7 and does not build on 3.9+ without modification; it was written for USRP sinks | Search summary of GitHub issues/StackOverflow | medium |
| gr-ais (bistromath, Nick Foster) is a GNU Radio out-of-tree module that outputs `!AIVDM` sentences; gnuais is an audio-input decoder with `gnuaisgui`, packaged in Debian | Search summary of GitHub/SourceForge/Debian pages | medium |
| Wegmatt (dAISy) publishes manuals for dAISy USB, dAISy 2+ and dAISy HAT, hosts firmware on GitHub (astuder/dAISy), and is US distributor for Uputronics filtered preamplifiers | https://wegmatt.com/ (read) | high |
| dAISy receivers are built on the Silicon Labs Si4362 sub-GHz receiver IC; Wegmatt quotes dAISy Mini sensitivity −113 dBm @ 20 % PER with LNA, −103 dBm without | Search summary of Wegmatt product/manual pages | medium |
| Quark-elec QK-A026 is a dual-channel AIS receiver with GPS and Wi-Fi/NMEA multiplexer, sensitivity ≈ −105 dBm (A026+ ≈ −112 dBm) | Search summary of vendor page | medium |
| Comar SLR-350N (also R400N) is a network AIS receiver with Ethernet and USB, NMEA 0183 at 38,400 baud, 9–30 V DC | Search summary of vendor page | medium |
| Shine Micro RadarPlus receivers (e.g., SM161R-2) are dual-channel with proprietary "Enhanced Signal Processing"; the SM1680 "Octopus" is a long-range phase-synchronous array | Search summary of vendor page | medium |
| In the US, Class B AIS devices "are not user configurable" (47 CFR 80.231); Class A static data is password-protected; USCG type-approved units have a built-in integrity tester | NAVCEN FAQ (read) | high |
| USCG type approvals are listed in CGMIX EQList under approval-series name "Shipborne AIS"; FCC certifications are searchable by equipment class "AIS" on the OET Equipment Authorization site | NAVCEN FAQ (read) | high |
| AIS AtoN stations in the US (other than USCG) need FCC or NTIA type certification and licensing, granted only after USCG consultation (CG forms 2554/4143) | NAVCEN FAQ (read) | high |
| USCG charges no fee for type approval; manufacturers pay for independent laboratory testing; approval series 165.155 (Class A) and 165.156 (Class B) | Search summary (USCG CG-ENG pages) | medium |
| SRT's FCC grantee code is UYW; em-trak-branded devices also appear under grantee code YYG | Search summary of fcc.report / fccid.io listings | medium |
| EU: Class A AIS is MED equipment requiring notified-body type-examination and the wheelmark; Class B is outside MED and is CE-marked under the Radio Equipment Directive 2014/53/EU | Search summary of EUR-Lex / notified-body pages | medium |
| Representative current models (2026): Saab R5 (Class A); Kongsberg AIS 300 (Class A); Furuno FA-170 (Class A); JRC JHS-183 (Class A); AMEC Camino-701 (A) / WideLink B600 (B); McMurdo SmartFind M6 (B); Ocean Signal ATA100 (A) / ATB1 (B); ACR AISLink CA2 (A) / CB2 (B); Raymarine AIS700 (B SO); Icom MA-510TR (B); Si-Tex SAS-300 (B); Weatherdock easyAIS; True Heading CTRX; Vesper/Garmin Cortex (B SO) | Search summary of vendor/dealer pages | medium (each model number (verify)) |

## Notes and quotes

**The OEM structure.** The retail shelf shows dozens of AIS brands, but the
number of independent transponder *designs* is much smaller. SRT's own site
is explicit: "Select from our standard OEM product platforms which are easily
rebranded and certified under your own name." The book should describe this
accurately and neutrally and should *not* assert which specific retail brands
are SRT-based unless a public artefact proves it. Two public artefacts can:
(1) the FCC ID on the product label — the grantee code (first 3 or 5
characters) identifies the certification holder; (2) the FCC exhibit set
(test report, internal photos, block diagram) under that ID. Chapter 33 can
teach the method with one worked FCC-ID lookup rather than publishing a
speculative brand map.

**Who else designs transponders.** Saab TransponderTech (Sweden; R4/R5 line,
long lineage back to the GP&C/Swedish trials — see r-history), Kongsberg
(Norway), Furuno and JRC (Japan), AMEC (Taiwan), Weatherdock (Germany), True
Heading (Sweden), Vesper (NZ, now Garmin), Nauticast (Austria), and the
Navico/Simrad group. Ownership has churned (McMurdo → Orolia → Safran;
Ocean Signal within ACR Group) — all (verify) and should be dated "as of".

**Receive-only hardware tiers (for Chapter 42).** (i) RTL-SDR-class dongle +
AIS-catcher; (ii) dedicated receiver (dAISy family, Quark-elec, Comar) that
does the demodulation in a dedicated radio IC and emits NMEA; (iii) network
receivers and professional base-station receivers (Comar SLR-350N-class,
Shine Micro, and the receiver halves of Class A/base-station hardware from
Saab/Kongsberg/SRT). The Si4362-based dAISy design is a useful teaching
example because its firmware is public (astuder/dAISy on GitHub), so the book
can show where the GMSK demodulation, NRZI decoding and HDLC deframing happen.

**SDR considerations that matter for AIS.** The two AIS channels are 50 kHz
apart, so any SDR with ≥ 200 kHz usable bandwidth captures both in one pass
(rtl-ais even accepts a 24 kHz per-channel design). What differs between
devices is: ADC bit depth (8-bit RTL-SDR vs 12-bit Airspy/SDRplay vs 12–16-bit
USRP/Lime), which governs dynamic range when a 12.5 W Class A ship is nearby
and a weak distant target shares the channel; frequency stability (TCXO
variants of RTL-SDR are strongly preferred; AIS-catcher and rtl-ais both
expose a ppm correction); and front-end filtering (an FM-broadcast notch and a
162 MHz band-pass preamp — Uputronics, sold by Wegmatt — typically make more
difference than the SDR choice). Chapter 28 should show the AIS-catcher
"models" idea: several demodulator models are run in parallel and the best
decode is kept, which is why its README invites recordings where models
struggle.

**Transmit-capable tools — how to write about them.** Three code bases are
publicly known to generate AIS waveforms: Trend Micro's AIS BlackToolkit
(2013–2014; gr-aistx GNU Radio block, `AiS_TX.grc`, an AIVDM encoder); the
SDRangel AIS modulator (a maintained GUI plugin with message-type, MMSI and
position fields); and various ad-hoc GNU Radio flowgraphs. The book's policy
(PLAN §7) is no transmit code and no step-by-step instructions. What the
chapter *should* say: these exist, they are trivial to find, they show that
the cost of AIS spoofing is a US$ 100–300 SDR, and transmitting on 161.975/
162.025 MHz without a station licence and type-approved equipment is unlawful
in essentially every administration (US: 47 CFR Part 80; AIS equipment must be
FCC-certified; see r-law-us). The legitimate uses are RF-shielded lab testing
and type-approval test benches, where IEC 61993-2/62287 require AIS test
signal generators anyway.

**Type approval in one paragraph.** The chain is: IMO performance standard
(MSC.74(69) Annex 3 for Class A; MSC.140(76) for Class B (verify)) → ITU-R
M.1371 technical characteristics → IEC test standard (61993-2 Class A;
62287-1 Class B CS; 62287-2 Class B SO; 62320-x base/AtoN; 61097-14 SART) →
test by an accredited laboratory → national/regional approval: USCG type
approval (free of charge, lab testing paid by manufacturer) plus FCC
certification under Part 80 (equipment class "AIS"); EU MED wheelmark for
Class A via a notified body (Module B type-examination + production module),
RED/CE for Class B. Cost figures for a full IEC 61993-2 campaign are not
published by labs; vendor interviews or notified-body price lists would be
needed — mark (verify) and avoid a number unless sourced.

**Teardown artefacts.** FCC exhibits routinely include internal photographs
and block diagrams; some grantees request confidentiality for schematics. For
Chapter 33's "teardown notes", draw on FCC internal photos (citable by FCC ID)
and the public dAISy firmware, not on unpublished teardowns.

## Open questions / (verify)

- (verify) Which retail brands are SRT OEM platforms: confirm only via FCC ID
  grantee codes (UYW/YYG) or SRT investor presentations naming partners; do
  not infer from appearance.
- (verify) Garmin press-release URL and exact wording for the Vesper
  acquisition (3 Jan 2022).
- (verify) USCG approval series numbers 165.155/165.156 and whether Class B
  SO has a separate series.
- (verify) Current MED item number for Class A AIS (4.14 vs 4.32) in the
  latest Commission Implementing Regulation.
- (verify) IEC 61993-2 current edition (Ed. 3.0:2018?) and 62287-1/-2 editions.
- (verify) Publicly stated prices for type-approval test campaigns (none
  found); consider an interview or a notified-body fee schedule.
- (verify) Shine Micro, Comar, Quark-elec model specifications from vendor
  datasheets (only search summaries seen).
- (verify) gr-ais commit history/dates and GNU Radio version support; gnuais
  authorship and first release year.
- (verify) rtl-ais lineage (reported to combine rtl_fm with the aisdecoder
  demodulator by Christian Gagneraud? — unconfirmed).
- (verify) Whether the HackRF/LimeSDR/PlutoSDR are used in published AIS
  transmit research beyond Balduzzi 2014 (USRP) — SDRangel supports many TX
  devices, but published AIS TX experiments are few.
- (verify) PlutoSDR official tuning range (325 MHz lower limit officially;
  firmware unlock to 70 MHz) before recommending it for 162 MHz work.

## Candidate figures and worked examples

1. **Market-structure diagram**: design houses (SRT, Saab, Kongsberg, Furuno,
   JRC, AMEC, Weatherdock, True Heading, Vesper/Garmin, Nauticast, Navico) →
   retail brands → certification bodies; annotate with "confirm via FCC ID".
2. **Worked example — reading an FCC ID**: take one em-trak/SRT device,
   show grantee code → grant → exhibits (test report sections: conducted
   power, frequency error, occupied bandwidth, spurious; internal photos).
3. **Table — SDRs for AIS**: RTL-SDR (8-bit, ~2.4 MS/s, TCXO variants),
   Airspy Mini/R2 (12-bit), SDRplay RSP (14-bit), HackRF One (8-bit, TX
   capable), LimeSDR (12-bit, TX), USRP B2xx (12-bit, TX), PlutoSDR (12-bit,
   TX; tuning limit note). Columns: bit depth, bandwidth, TCXO, TX, price
   class, AIS-catcher support (from README).
4. **Receiver tier bill of materials** for Chapter 42 (three tiers), priced
   "as of 2026" with sources.
5. **Try it**: `rtl_ais -n` and the equivalent AIS-catcher command line with
   ppm correction and UDP output; expected `!AIVDM` lines.
6. **Threat-model box** for transmit tools (attacker: anyone with a US$ 100
   SDR; capability: inject any M.1371 message; impact: ghost targets, false
   AtoN, false SART; mitigation: multi-receiver plausibility, DF, see ch. 35/
   59/60) — no code.
7. **Diagram**: type-approval chain IMO → ITU → IEC → lab → USCG/FCC or MED.

## Recommended use by chapter

- **Ch. 33** — core chapter: OEM structure (SRT quote), brand/model table
  (all (verify)), receiver tiers, SDR table, software list (AIS-catcher,
  rtl-ais, gr-ais, gnuais, SDRangel), transmit tools described with threat
  model and legal note, type-approval chain, FCC-ID teardown method.
- **Ch. 12** — Garmin–Vesper (Jan 2022) in the consolidation timeline.
- **Ch. 15 / App. B** — IEC 61993-2, 62287-1/-2, MED item, 47 CFR 80.231.
- **Ch. 20** — power classes and class differences; US Class B not user
  configurable.
- **Ch. 28** — AIS-catcher multi-model demodulation as a design example;
  dAISy firmware as a reference implementation of GMSK → NRZI → HDLC.
- **Ch. 42** — tiers (i)–(iii), FM notch + 162 MHz preamp advice, dAISy and
  dAISy-catcher.
- **Ch. 44** — rtl-ais, gr-ais, gnuais, AIS-catcher, SDRangel entries with
  licences and status.
- **Ch. 59/60** — Trend Micro toolkit and SDRangel modulator as evidence of
  attacker capability; Balduzzi 2014 citation.
- **Ch. 68** — AIS AtoN certification path in the US (FCC/NTIA + USCG
  consultation).
- **App. F** — hardware catalogue seeded from the model table.
