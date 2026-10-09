# Dossier: RF forensics and transmitter fingerprinting of AIS stations

**Purpose.** This dossier records what can be confirmed, as of October 2026,
about identifying an AIS transmitter — its manufacturer, model, or the
individual unit — from physical-layer and protocol-layer evidence rather than
from the MMSI it claims. It covers the general specific-emitter-identification
(SEI) / radio-frequency-fingerprinting (RFF) literature (Brik et al. 2008;
Danev, Zanetti & Čapkun 2012; Sankhe et al. 2019), the ADS-B work that is the
closest analogue (Strohmeier & Martinovic 2015; Strohmeier, Lenders &
Martinovic 2015; Leonardi et al. 2017), the AIS-specific SEI papers now in the
IEEE literature (Qian et al. 2021; Deng et al. 2023; Li et al. 2025; Jiang &
Sha 2025; Zhang et al. 2025 on GMSK eye-diagram deviations), the first open
AIS physical-layer dataset with per-message RF metadata (AIS-TSH, Faroe
Islands, 2025/2026), and the protocol-level "behavioural" fingerprints that
require no IQ capture (message mix, timing habits, sentinel usage, NMEA
quirks). It separates what is *published*, what is *plausible*, and what is
*unproven*, and sketches a reproducible lab protocol. It feeds **Chapter 34**
(RF forensics and transmitter fingerprinting) primarily, and supplies material
to **Chapter 28** (modulation parameters that vary between units),
**Chapter 33** (OEM lineages that fingerprints may reveal), **Chapter 35**
(Doppler/oscillator-offset confound), **Chapter 47** (identity resolution),
**Chapter 59** (spoof detection), **Chapter 64** (physical-layer
authentication as a future control), **Chapter 19** (privacy), and
**Chapter 68** (ADS-B kinship).

> Research-session note. Bibliographic facts marked *high* were confirmed via
> Crossref API records for the DOIs listed (title, venue, year, volume,
> pages, authors). Content claims (feature sets, accuracies, dataset sizes)
> marked *medium* come from abstracts or search summaries; papers were not
> read in full. Where the search engine supplied a DOI that disagreed with
> Crossref, Crossref was used (e.g., Deng et al. 2023 is 10.1109/TIFS.2023.3266627,
> not …3267597 as one summary stated).

## Key questions

1. Which hardware impairments survive GMSK modulation at 9,600 bit/s and a
   VHF channel well enough to be measured per burst: carrier frequency
   offset (CFO) and drift, modulation index / frequency deviation, Gaussian
   filter BT, I/Q imbalance, power-amplifier ramp-up/ramp-down shape, phase
   noise, spurious, symbol-clock offset?
2. What has been *demonstrated* for AIS: on how many transmitters, with what
   receivers, over what time span, at what accuracy, and did it generalise
   across days and channels?
3. Can one tell the *manufacturer/platform* (e.g., an SRT-based module vs a
   Saab or Furuno design) from the waveform or from protocol behaviour, as
   distinct from identifying an individual unit?
4. What protocol-level fingerprints exist (message-type mix per class,
   Message 5/24 cadence, comm-state habits, use of sentinels, ROT encoding
   behaviour, text-field padding, NMEA fragmentation and TAG-block habits of
   the shore receiver) and how stable are they?
5. What open data and tools exist (AIS-TSH; AIS-catcher per-message power/ppm
   output; GNU Radio flowgraphs) to reproduce results?
6. What are the privacy and legal implications of unit-level identification
   of (largely mandated) transmitters?
7. What is unproven or over-claimed, and how should the chapter say so?

## Primary sources located

| Source | Identifier / edition / year | URL | What it covers | Access |
|---|---|---|---|---|
| Brik, Banerjee, Gruteser & Oh | MobiCom 2008, pp. 116–127, DOI 10.1145/1409944.1409959 | https://doi.org/10.1145/1409944.1409959 | "Wireless device identification with radiometric signatures" (PARADIS) — the canonical modulation-domain RFF paper (frequency error, I/Q offset, magnitude/phase error, SYNC correlation) | Paid |
| Danev, Zanetti & Čapkun | *ACM Computing Surveys* 45(1):1–29, Nov 2012, DOI 10.1145/2379776.2379782 | https://doi.org/10.1145/2379776.2379782 | Survey and taxonomy of physical-layer device identification (transient vs modulation-based; attacks on fingerprinting) | Paid |
| Sankhe, Belgiovine, Zhou, Riyaz, Ioannidis & Chowdhury | IEEE INFOCOM 2019, pp. 370–378, DOI 10.1109/INFOCOM.2019.8737463 | https://doi.org/10.1109/INFOCOM.2019.8737463 | ORACLE — CNN on raw IQ for radio identification; established the deep-learning RFF paradigm and its channel-sensitivity caveats | Paid |
| Strohmeier & Martinovic | ACM CPS-SPC 2015, pp. 1–9, DOI 10.1145/2808705.2808712 | https://doi.org/10.1145/2808705.2808712 | "On Passive Data Link Layer Fingerprinting of Aircraft Transponders" — protocol/timing-level fingerprints of Mode S/ADS-B transponders (closest analogue to AIS protocol fingerprinting) | Paid |
| Strohmeier, Lenders & Martinovic | DIMVA 2015, LNCS, pp. 67–77, DOI 10.1007/978-3-319-20550-2_4 | https://doi.org/10.1007/978-3-319-20550-2_4 | PHY-layer intrusion detection for ADS-B (RSS/timing hypothesis tests) | Paid |
| Leonardi, Di Gregorio & Di Fausto | *Aerospace* 4(4):51, 30 Oct 2017, DOI 10.3390/aerospace4040051 | https://doi.org/10.3390/aerospace4040051 | Aircraft classification from ADS-B message phase patterns (RFF on PPM; manufacturer-level classification) | Free |
| Qian, Qi, Kuai, Han, Sun & Hong | *IEEE TIFS* 16:2872–2884, 2021, DOI 10.1109/TIFS.2021.3068010 | https://doi.org/10.1109/TIFS.2021.3068010 | "Specific Emitter Identification Based on Multi-Level Sparse Representation in Automatic Identification System" | Paid |
| Deng, Hong, Qi, Wang & Sun | *IEEE TIFS* 18:2303–2317, 2023, DOI 10.1109/TIFS.2023.3266627 | https://doi.org/10.1109/TIFS.2023.3266627 | "A Lightweight Transformer-Based Approach of Specific Emitter Identification for the Automatic Identification System" | Paid |
| Li, Shao, Deng, Hong, Qi & Sun | *IEEE TCCN* 11:1649–1663, June 2025, DOI 10.1109/TCCN.2024.3476491 | https://doi.org/10.1109/TCCN.2024.3476491 | "A Self-Supervised-Based Approach of Specific Emitter Identification for the Automatic Identification System" (label-scarce SEI) | Paid |
| Jiang & Sha | *IEEE TAES*, Feb 2025, DOI 10.1109/TAES.2024.3452706 | https://doi.org/10.1109/TAES.2024.3452706 | "Radio Frequency Fingerprint Identification Using Conditional Generative Adversarial Network for SAT-AIS" (satellite-received AIS) | Paid |
| Zhang, Zheng, Liu & Lin | *IEEE TVT* 74:10452–10466, July 2025, DOI 10.1109/TVT.2025.3543481 | https://doi.org/10.1109/TVT.2025.3543481 | "Radio Frequency Fingerprint Identification of GMSK Modulated Signals Based on Eye Diagram Traces Deviation" — explicit GMSK features (CFO, modulation offset, I/Q offset) | Paid |
| Yang, Son, Kumar Chowdhury & Shin | OCEANS 2024 Halifax, DOI 10.1109/OCEANS55160.2024.10753797 | https://doi.org/10.1109/OCEANS55160.2024.10753797 | "Ship Matching Issues Using AIS and Satellite Radio Frequency Data" (associating RF detections with AIS tracks) | Paid |
| Yang & Chowdhury | *J. Mar. Sci. Eng.* 13(2):191, Jan 2025, DOI 10.3390/jmse13020191 | https://doi.org/10.3390/jmse13020191 | Frequency-based matching accuracy between satellite RF detections and AIS | Free |
| Kristmundsson, Svoostein et al. | *IEEE Data Descriptions*, 2026, DOI 10.1109/IEEEDATA.2026.3676933 | https://doi.org/10.1109/IEEEDATA.2026.3676933 | "Descriptor: AIS Signal and Channel Dataset From Tórshavn Harbor and Surrounding Islands (Faroe Islands) (AIS-TSH)" — 76 days (9 Jul–23 Sep 2025), 7.8 M messages, 547 vessels, RTL-SDR v3 + AIS-catcher v0.61, per-message received power (dBFS) and frequency offset (ppm) | Free (dataset via pure.fo) |
| Iphar, Ray & Napoli | *ESWA* 147:113219, 2020, DOI 10.1016/j.eswa.2020.113219 | https://doi.org/10.1016/j.eswa.2020.113219 | Data-integrity rules usable as protocol-level behavioural fingerprints | Paid |
| Balduzzi, Pasta & Wilhoit | ACSAC 2014, pp. 436–445, DOI 10.1145/2664243.2664257 | https://doi.org/10.1145/2664243.2664257 | Attacker model whose SDR-generated bursts a fingerprinting system must distinguish from real transponders | Paid |
| AIS-catcher | README (read 2026-10-05) | https://raw.githubusercontent.com/jvde-github/AIS-catcher/main/README.md | Open receiver that exposes per-message signal level and ppm offset (used by AIS-TSH); multiple demodulator models | Free |
| gpsd, "AIVDM/AIVDO protocol decoding" | E. S. Raymond with K. Schwehr (verify current URL) | https://gpsd.gitlab.io/gpsd/AIVDM.html | Catalogue of encoder quirks and non-conformances observed in the wild (protocol-level fingerprints) | Free |
| ITU-R M.1371-5, Annex 2 | 2014 | https://www.itu.int/rec/R-REC-M.1371 | Nominal PHY parameters (GMSK BT 0.4 Tx, modulation index 0.5, 9,600 bit/s, ramp-up 8 bits, training sequence 24 bits, frequency tolerance) against which deviations are measured | Free |

## Verified facts

| Fact | Source | Confidence |
|---|---|---|
| Brik et al. (2008) "Wireless device identification with radiometric signatures", MobiCom '08, pp. 116–127 | Crossref | high |
| Danev, Zanetti & Čapkun (2012) survey, *ACM CSUR* 45(1):1–29 | Crossref | high |
| Sankhe et al. (2019) ORACLE, IEEE INFOCOM 2019, pp. 370–378 | Crossref | high |
| Strohmeier & Martinovic (2015) passive data-link-layer fingerprinting of aircraft transponders, CPS-SPC '15, pp. 1–9 | Crossref | high |
| Strohmeier, Lenders & Martinovic (2015) PHY-layer intrusion detection for airborne communication, DIMVA 2015, LNCS pp. 67–77 | Crossref | high |
| Leonardi, Di Gregorio & Di Fausto (2017) *Aerospace* 4(4):51 | Crossref | high |
| Qian et al. (2021) multi-level sparse representation SEI for AIS, *IEEE TIFS* 16:2872–2884 | Crossref | high |
| Deng et al. (2023) lightweight Transformer SEI for AIS, *IEEE TIFS* 18:2303–2317 | Crossref | high |
| Li et al. (2025) self-supervised SEI for AIS, *IEEE TCCN* 11:1649–1663 | Crossref | high |
| Jiang & Sha (2025) cGAN RFF for SAT-AIS, *IEEE TAES* | Crossref | high |
| Zhang et al. (2025) GMSK eye-diagram-trace-deviation RFF, *IEEE TVT* 74:10452–10466 | Crossref | high |
| Zhang et al. extract carrier frequency offset, modulation offset and I/Q offset as GMSK fingerprint features | Search summary of abstract | medium |
| AIS-TSH descriptor is in *IEEE Data Descriptions* (2026), DOI 10.1109/IEEEDATA.2026.3676933; first authors Kristmundsson and Svoostein | Crossref | high |
| AIS-TSH: 76 days continuous (9 Jul–23 Sep 2025), 7.8 million messages, 547 unique vessels, detections to ≈101 nmi; RTL-SDR v3, vertically polarised VHF antenna 60 m above sea level, fixed 20 dB gain (AGC off), channels 161.975/162.025 MHz, AIS-catcher v0.61; each record carries received power (dBFS) and frequency offset (ppm); intended uses include spoofing/interference detection from physical-layer indicators | Search summary of pure.fo dataset pages | medium |
| Yang et al. (2024, OCEANS Halifax) and Yang & Chowdhury (2025, *JMSE* 13:191) study matching satellite RF detections to AIS tracks, including frequency-based matching | Crossref | high |
| Recent AIS SEI papers report high closed-set accuracies (a 2026 Transformer variant quotes up to 96.31 % on a transient-state dataset) | Search summary (paper not located via Crossref in session) | low — (verify) |
| AIS-catcher exposes per-message signal level and ppm frequency offset in its output, which AIS-TSH relies on | AIS-TSH summary; AIS-catcher README feature list | medium |
| M.1371 nominal PHY: GMSK, BT 0.4 (transmit), modulation index 0.5, 9,600 bit/s, NRZI, 24-bit training sequence, 8-bit ramp-up | ITU-R M.1371 (see r-rf-phy for clause cites) | high |

## Notes and quotes

**Two families of fingerprint.** The survey literature (Danev et al. 2012)
splits physical-layer identification into *transient-based* (the turn-on
ramp before the modulation settles) and *modulation-based* (steady-state
impairments such as CFO, I/Q imbalance, phase noise, EVM). AIS is unusually
friendly to both: every burst starts with a specified 8-bit ramp-up and a
24-bit training sequence (M.1371 Annex 2), so a receiver always has an
aligned transient and a known preamble to measure against. Deep-learning
approaches (ORACLE 2019 onward; Qian 2021, Deng 2023, Li 2025 for AIS) feed
raw IQ to a network and let it find the features; the trade-off, documented
since ORACLE, is sensitivity to channel and receiver changes — a model
trained on one SDR, one antenna, one week may not transfer.

**What is published for AIS specifically.** The IEEE papers above establish
that *closed-set* identification of a modest number of AIS transmitters from
IQ captures is achievable with high accuracy, and that work is moving to the
hard cases: few labels (self-supervised, Li 2025), satellite-received bursts
with low SNR and Doppler (Jiang & Sha 2025), and explicit engineering
features that are interpretable (eye-diagram deviations, Zhang 2025). The
chapter should quote their stated accuracies with the dataset size and
conditions, and should say plainly that none of them demonstrates
*open-set*, fleet-scale, cross-season identification of thousands of ships
from ordinary shore receivers. That is the plausible-but-unproven zone.

**Manufacturer vs unit.** Leonardi et al. (2017) showed for ADS-B that phase
patterns cluster by transponder *type*, i.e., manufacturer/model-level
classification is easier and more stable than unit-level. For AIS the same
is likely because most transponders are built on a small number of OEM
platforms (see r-hardware: SRT modules rebranded; Saab, Kongsberg, Furuno,
JRC designs). Platform-level fingerprints would come from the Gaussian
filter implementation (BT realised as 0.38 vs 0.42), the ramp shape, the
modulation index tolerance, and the symbol clock. No paper located in this
session reports a manufacturer-level AIS classifier; mark as plausible,
unproven, and an excellent student project.

**Protocol-level fingerprints need no SDR.** From decoded data alone one can
observe: the ratio of Message 1/2/3 (which comm-state the unit uses when;
ITDMA vs SOTDMA habits), Message 5 and 24A/24B cadence and whether 24B is
sent at all, whether the unit ever sets timestamp 60–63, ROT behaviour
(−128 vs 0 vs ±127 for units without a rate sensor), heading 511 patterns,
text-field padding characters (`@` vs spaces), dimension/reference-point
encodings, and — for shore receivers rather than ships — NMEA fragmentation,
sequential-message-id use, and TAG-block style. Strohmeier & Martinovic
(2015) did exactly this for Mode S/ADS-B transponders and showed that
data-link-layer behaviour identifies transponder types. The gpsd AIVDM
document is a decade-long catalogue of such quirks for AIS and should be
mined (with care about currency). Iphar et al. (2020) formalise integrity
rules that double as behavioural features.

**Confounds the chapter must state.** (1) *Doppler vs CFO*: for a moving ship
seen from shore the Doppler at 162 MHz is tiny (≈ ±5 Hz at 20 kn (verify
arithmetic in ch. 35)), but from a satellite it is thousands of hertz, so
satellite RFF must remove Doppler first (Jiang & Sha 2025). (2) *Receiver
fingerprint*: an RTL-SDR's own oscillator offset and drift add to the
transmitter's; AIS-TSH fixed gain and logged ppm to make this tractable, but
cross-receiver transfer remains the central unsolved problem. (3)
*Temperature and ageing*: crystal offsets drift over hours and years;
"fingerprint drift" is an acknowledged research topic. (4) *Channel*:
multipath over sea and antenna pattern vs aspect angle change the received
waveform; transient features are more robust than amplitude features.
(5) *Class and power*: 12.5 W Class A vs 2 W Class B CS vs 5 W Class B SO
produce different SNR regimes at the same range.

**Spoof detection framing.** The security value is asymmetric: a
fingerprint can *reject* a burst that claims MMSI X but does not match X's
established fingerprint (useful against SDR injection, Balduzzi 2014), and
it can *link* bursts under different MMSIs to one physical unit ("MMSI
laundering", ch. 13/59). It cannot, by itself, tell you which ship a new
fingerprint belongs to. Chapter 64 should present physical-layer
authentication as a complement to, not a substitute for, cryptographic
authentication.

**Privacy and legal.** Unit-level identification of transponders carried by
small craft and fishing vessels is a form of device tracking that persists
across MMSI changes and ownership transfers; it also undermines any future
privacy-preserving identifier scheme. The chapter should carry a Legal note
(reception is lawful in most places; storing and publishing fingerprints of
private craft may engage data-protection law in the EU) and point to
Chapter 19.

**Reproducible lab protocol (sketch for Chapter 34).**
1. Capture: one calibrated SDR (TCXO; fixed gain; AGC off), 1–2 MS/s IQ
   around 162.0 MHz, GNSS-disciplined timestamps; log temperature.
2. Burst extraction: detect ramp-up, align on the 24-bit training sequence,
   decode to obtain MMSI and CRC status; keep only CRC-valid bursts.
3. Features (engineering): CFO from the preamble; frequency deviation and
   modulation index from the demodulated FM; estimated BT from the eye
   diagram (Zhang 2025); ramp-up/down duration and shape; power stability
   across the burst; symbol-clock offset; spurious/adjacent energy.
4. Protocol features: message mix, cadence, sentinel usage per MMSI.
5. Evaluation: split by *day* (not by burst) to test temporal stability;
   hold out a receiver if two are available; report open-set metrics
   (unknown-emitter rejection), not just closed-set accuracy.
6. Publish IQ excerpts only for the author's own transmitters or with
   consent; publish features and code (fits PLAN §7: no transmit code).

## Open questions / (verify)

- (verify) Read Qian 2021, Deng 2023, Li 2025, Jiang & Sha 2025, Zhang 2025
  in full: number of transmitters, capture hardware, train/test split
  (by time?), closed vs open set, reported accuracy; extract the feature
  tables.
- (verify) Locate the 2026 "GLFormer"/gated-local-attention AIS SEI paper
  referenced by search summaries (96.31 % transient-state accuracy) and
  confirm venue/DOI; otherwise omit.
- (verify) Whether any paper demonstrates *manufacturer-level* AIS
  classification; none found.
- (verify) AIS-TSH descriptor details (author list, licence, exact file
  format — "newline-delimited JSON in `aisdata.csv`" per the summary is
  internally odd) from the IEEE Data Descriptions article.
- (verify) AIS-catcher output fields for signal level and ppm (`-M`/JSON
  options) and their definitions.
- (verify) gpsd AIVDM document URL and the specific encoder quirks it lists
  by vendor (to avoid naming vendors without the source).
- (verify) Realised BT and modulation-index tolerances in IEC 61993-2 /
  62287 test limits (to show how much room manufacturers have to differ).
- (verify) Doppler magnitudes: shore (ship at 20 kn) vs LEO; compute and
  cross-check with ch. 35/39.
- (verify) Whether FCC test reports (occupied bandwidth, frequency error)
  show measurable differences between platforms that could seed a
  manufacturer-level feature set.
- (verify) Any public statement by a satellite-AIS provider about using RFF
  for identity verification (none located).

## Candidate figures and worked examples

1. **Anatomy of a burst for forensics**: ramp-up (8 bits) → training (24
   bits) → start flag → data → CRC → end flag → buffer; annotate which
   features come from which segment.
2. **Worked example — CFO and drift**: from AIS-TSH, plot per-MMSI ppm offset
   over 76 days for five vessels; show between-vessel separation vs
   within-vessel drift; discuss the receiver's own drift.
3. **Worked example — received power vs reported range**: AIS-TSH dBFS vs
   great-circle distance for Class A and Class B; fit a two-ray slope;
   highlight outliers as candidates for ch. 35 plausibility checks.
4. **Eye-diagram figure**: two synthetic GMSK bursts with BT 0.38 and 0.42
   overlaid (NumPy), showing the trace deviation feature of Zhang 2025 — no
   RF output, file only.
5. **Protocol-fingerprint table**: for N vessels from an open feed, message
   mix, Msg 5 interval, 24B presence, timestamp ≥60 rate, ROT sentinel
   usage, heading 511 rate; cluster and discuss.
6. **Figure — ADS-B analogue**: Leonardi 2017 phase-pattern clustering by
   transponder type, redrawn schematically with permission or as a
   conceptual diagram.
7. **Threat-model box**: attacker with SDR injects bursts under a real
   MMSI; defender with fingerprint database rejects on CFO/ramp mismatch;
   limits: attacker can replay/record and mimic coarse features.
8. **Try it**: Python that takes an IQ file, finds bursts via the training
   sequence, and prints CFO, burst length and power per burst (receive-side
   only).

## Recommended use by chapter

- **Ch. 34** — core chapter structured as: what survives the channel; the
  general SEI literature (Brik 2008; Danev 2012; ORACLE 2019); ADS-B
  analogue (Strohmeier 2015 ×2; Leonardi 2017); AIS results (Qian 2021;
  Deng 2023; Li 2025; Jiang & Sha 2025; Zhang 2025) with the published/
  plausible/unproven ladder; protocol-level fingerprints (gpsd quirks;
  Iphar 2020); confounds; lab protocol; privacy/legal boxes; AIS-TSH as the
  open dataset.
- **Ch. 28** — which PHY parameters have manufacturing tolerance (BT,
  modulation index, ramp) and are therefore fingerprint features.
- **Ch. 33** — OEM platform concentration as the reason manufacturer-level
  fingerprints might cluster strongly; FCC test reports as a feature seed.
- **Ch. 35** — oscillator offset vs Doppler; satellite RFF must de-Doppler.
- **Ch. 39** — SAT-AIS RFF (Jiang & Sha 2025); RF-to-AIS matching (Yang
  2024/2025).
- **Ch. 47** — linking tracks under different MMSIs to one unit; identity
  resolution with physical evidence.
- **Ch. 59/60** — rejecting SDR-injected bursts; limits against replay.
- **Ch. 64** — physical-layer authentication alongside VDES/cryptographic
  proposals.
- **Ch. 19** — persistent device tracking across MMSI changes.
- **Ch. 68** — ADS-B comparison table row: "fingerprinting literature".
- **App. G** — AIS-TSH dataset entry (licence, size, fields).
