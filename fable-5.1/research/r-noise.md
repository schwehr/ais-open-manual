# Dossier: Noise and interference sources for AIS, aboard and ashore — LED lighting, switch-mode supplies, radar, adjacent VHF/NWR, FM broadcast, EMC limits, and measurement

**Purpose.** This dossier records what could be confirmed, as of 5 October
2026, about the interference environment of a 162 MHz AIS receiver: the
shipboard sources that have produced official safety alerts (LED lighting with
switch-mode drivers), the standards that bound shipboard emissions (IEC 60945;
RTCM 13700.0; FCC Part 15 for comparison), the receiver immunity figures in
ITU-R M.1371-6 that define "how much is too much" (blocking, adjacent-channel,
intermodulation), the shore-side neighbours that matter for collection sites
(NOAA Weather Radio at 162.400–162.550 MHz, FM broadcast, paging/public-safety,
radar), and practical measurement/mitigation. It is the primary dossier for
**Chapter 31** and feeds **Chapter 27** (noise floor and sensitivity margin),
**Chapter 32** (antenna separation), **Chapter 36** (interference as a failure
mode), **Chapter 37** (places to avoid when siting shore receivers), and
**Chapter 42** (FM notch/LNA choices for a home receiver).

> Research-session note. M.1371-6 figures were read from the itu.int PDF text.
> RTCM 13700.0's title/date were read from rtcm.org. 47 CFR 15.109 was read from
> Cornell LII (eCFR API returned empty). The USCG Marine Safety Alert 13-18 PDF
> is hosted at dco.uscg.mil but returned 403 to this session's fetcher; its
> content is reported here from multiple secondary restatements (AMSA, IMCA,
> trade press) seen in search summaries and is marked accordingly. IEC 60945
> limits are from test-house restatements (search summaries), not the paid
> standard text. NOAA NWR facts are from weather.gov via search summary.

## Key questions

1. What interference sources on a ship have been shown to degrade AIS/VHF
   reception, and what is the official evidence (alerts, standards)?
2. What emission limits apply to shipboard electronics (IEC 60945 protected
   band 156–165 MHz; RTCM 13700.0), and how do they compare with generic
   limits (FCC Part 15) that consumer LED products meet?
3. What immunity does an AIS receiver have by specification (M.1371-6 Tables 7
   and 36: adjacent-channel 70 dB, co-channel 10 dB, intermodulation 74 dB /
   −36 dBm, blocking 86 dB / −23 dBm), and what do those numbers mean in dBm
   at the antenna port?
4. How close is NOAA Weather Radio (162.400–162.550 MHz, up to 1 kW) to AIS 2
   (162.025 MHz) and when does it matter?
5. What about radar (S/X-band) overload, FM broadcast intermodulation, pagers,
   cellular, Inmarsat/VSAT, power lines, VFDs/inverters/chargers?
6. How to measure (spectrum analyser, SDR waterfall, the USCG squelch test) and
   mitigate (filters, separation, grounding, cable routing, LNA placement)?
7. Which shore sites to avoid (Chapter 37) and why?

## Primary sources located

| Source | Identifier / edition / year | URL | What it covers | Access |
|---|---|---|---|---|
| USCG Marine Safety Alert 13-18, "Potential Interference of VHF-FM Radio and AIS Reception by Light Emitting Diode (LED) Lighting" (title per secondary restatements) | August 2018 | https://www.dco.uscg.mil/Portals/9/DCO%20Documents/5p/CG-5PC/INV/Alerts/1318.pdf (403 to this session) | LED-driver EMI degrading VHF/DSC/AIS; squelch test procedure; report to NAVCEN | Free |
| USCG MSIB 03-22 (April 2022) announcing RTCM 13700.0 | 03-22 | USCG MSIB index (verify URL) | Points industry to the RTCM EMC standard | Free |
| RTCM 13700.0, "Standard for Electromagnetic Compatibility Requirements for Light Emitting Diode (LED) Devices and Other Electrical and Electronic Equipment in the Vicinity of Shipboard Antennas for the Protection of Onboard Receivers" | April 13, 2022 | https://www.rtcm.org/publications (listing read 2026-10-05) | EMC test requirements for above-deck LED and other equipment | Paid (RTCM) |
| RTCM 11701.0, "Standard for Installed Maritime VHF Radiotelephone Equipment Operating in High Level Electromagnetic Environments" (RTCM Paper 87-99/SC117-STD) | — | https://www.rtcm.org/publications | Tests for installed VHF radios "in areas where they might be susceptible to interference from other radio frequency devices, such as pagers" | Paid (RTCM) |
| IEC 60945, *Maritime navigation and radiocommunication equipment and systems – General requirements – Methods of testing and required test results* | Ed. 4.0, 2002 (corrigendum 2008 (verify)) | https://webstore.iec.ch/ | EMC emission/immunity, environmental tests; protected band 156–165 MHz radiated-emission limit | Paid |
| Rec. ITU-R M.1371-6 Tables 7 and 36 | 02/2026 | see `r-rf-phy.md` | Receiver immunity requirements | Free |
| 47 CFR 15.109 (Radiated emission limits, unintentional radiators) | eCFR current | https://www.law.cornell.edu/cfr/text/47/15.109 (read 2026-10-05) | Class B: 150 µV/m at 3 m for 88–216 MHz; Class A: 150 µV/m at 10 m | Free |
| Rec. ITU-R P.372 | P.372-18 (09/2026) | https://www.itu.int/rec/R-REC-P.372/en | Man-made/galactic noise vs frequency and environment | Free |
| NOAA Weather Radio All Hazards | weather.gov NWR pages; station list | https://www.weather.gov/nwr/ ; https://www.weather.gov/nwr/sites | Seven frequencies 162.400–162.550 MHz; transmitter powers up to 1,000 W | Free |
| IMO COMSAR.1/Circ.32/Rev.3 §5.2.8 (as quoted in M.1371-6) | — | quoted at M.1371-6 p. 15 | AIS/VHF antenna separation (2 m vertical / 5 m horizontal) | Free |

## Verified facts

| Fact | Source | Confidence |
|---|---|---|
| Class A receiver requirements: sensitivity 20 % PER at −107 dBm; 1 % PER at −77 dBm and at −7 dBm (high-level behaviour); adjacent-channel selectivity 20 % PER at 70 dB; co-channel 10 dB; spurious response rejection 70 dB; intermodulation response rejection 74 dB; blocking 86 dB. | M.1371-6 Annex 2 Table 7, pp. 14–15 | high |
| Class B "CS" receiver: wanted signal −101 dBm with unwanted at −111 dBm (co-channel), −31 dBm (adjacent channel and spurious), −36 dBm (intermodulation), −23 dBm blocking (< 5 MHz offset) and −15 dBm (> 5 MHz offset). | M.1371-6 Annex 6 Table 36, p. 86 | high |
| Class B "CS" carrier-sense threshold tracks background noise over ≥ 30 dB (−107 to −77 dBm) — so a raised noise floor directly raises the level at which a Class B defers. | M.1371-6 §A6-4.3.1.3 | high |
| M.1371-6 quotes COMSAR.1/Circ.32/Rev.3 §5.2.8: AIS antenna directly above or below the primary VHF antenna with ≥ 2 m vertical separation and no horizontal separation; if on the same level, ≥ 5 m apart. | M.1371-6 Table 7 note, p. 15 | high |
| 47 CFR 15.109(a): unintentional radiators (other than Class A digital devices) ≤ 150 µV/m at 3 m for 88–216 MHz (= 43.5 dBµV/m); 15.109(b): Class A digital devices ≤ 150 µV/m at 10 m for 88–216 MHz. | Cornell LII text of 47 CFR 15.109, read 2026-10-05 | high |
| IEC 60945 Ed. 4.0 (2002) radiated-emission limit in the protected band 156–165 MHz is 24 dBµV/m quasi-peak at 3 m (general limit 54 dBµV/m for 30 MHz–2 GHz at 3 m). | Test-house restatements via search summaries (2026-10-05) | medium (not read from the standard) |
| Hence a device that merely meets FCC Part 15 Class B (43.5 dBµV/m at 3 m) may exceed the IEC 60945 marine protected-band limit by ≈ 19.5 dB. | Arithmetic from the two rows above | high (arithmetic); medium (60945 figure) |
| RTCM 13700.0 exists with the title above and date April 13, 2022; RTCM 11701.0 addresses installed VHF radios in high-level EM environments "such as pagers". | https://www.rtcm.org/publications (read 2026-10-05) | high |
| USCG Marine Safety Alert 13-18 (August 2018) reported poor VHF-FM/DSC/AIS reception near LED lighting (navigation, search, flood, interior/exterior lights), attributed to switching power supplies, with cases where rescue coordination centres could not contact vessels; it gives a squelch-threshold test (LEDs off → set squelch at threshold on a quiet channel → LEDs on → noise = interference) and asks for reports to NAVCEN. | Multiple secondary restatements in search summaries (AMSA, IMCA, Practical Sailor, National Fisherman) | medium (primary PDF not fetched) |
| NOAA Weather Radio uses seven frequencies: 162.400, 162.425, 162.450, 162.475, 162.500, 162.525, 162.550 MHz; transmitter power up to 1,000 W (sites range roughly 5–1,000 W). | weather.gov NWR pages via search summary (2026-10-05) | medium |
| The lowest NWR frequency (162.400 MHz) is 375 kHz above AIS 2 (162.025 MHz) and 425 kHz above AIS 1 — i.e., well outside the ±25 kHz adjacent-channel test but inside the < 5 MHz blocking region. | Arithmetic | high |
| ITU-R P.372-18 (09/2026) is the current radio-noise recommendation. | itu.int index page | high |

## Notes and quotes

- **Immunity numbers in dBm.** M.1371 expresses most Class A immunity figures
  as ratios relative to a wanted signal; IEC 61993-2 test practice sets the
  wanted signal a few dB above sensitivity (−101 dBm in the Class B table). On
  that basis: adjacent-channel interferer ≈ −31 dBm; intermodulation pair ≈
  −27 to −36 dBm; blocking ≈ −15 to −23 dBm. A nearby 25 W marine VHF
  transmitter at 2 m vertical separation on the same mast can deliver roughly
  −10 to 0 dBm into the AIS antenna (coupling of 40–50 dB below 44 dBm), so the
  COMSAR separation rule is a *minimum*, and simultaneous VHF voice transmit
  routinely desensitises AIS receive on small craft. Use this as the worked
  example; state the coupling assumption explicitly.
- **Worked example — NWR at 1 km.** 1 kW (60 dBm) + ~5 dBi antenna = 65 dBm
  EIRP; free-space loss at 162 MHz over 1 km = 32.45 + 20 log₁₀(162) +
  20 log₁₀(1) ≈ 76.6 dB; a 2 dBi receive antenna sees ≈ −10 dBm — above the
  −15/−23 dBm Class B blocking levels and near the Class A 86 dB blocking
  figure. At 10 km the level drops to ≈ −30 dBm, which most receivers tolerate.
  Rule of thumb for Chapter 37: keep collection sites several km from NWR and
  other 150–175 MHz high-power transmitters, or add a cavity/notch.
- **Why LED drivers.** Constant-current buck converters switch at tens of kHz
  to a few MHz; harmonics and ringing from fast edges extend to VHF, radiated
  by the DC leads and the fixture. Navigation lights are by design at mast and
  rail positions — i.e., closest to the VHF/AIS antenna — which is why the 2018
  alert singled them out. RTCM 13700.0 is the industry's targeted fix: an EMC
  test for devices *in the vicinity of shipboard antennas*.
- **Quote attribution caution.** The USCG alert's exact wording should be
  quoted only after the PDF is retrieved; do not paraphrase as a quote.
- **The 60945 protected band is the key number.** Marine type-approved
  electronics are held to 24 dBµV/m at 3 m across 156–165 MHz; consumer
  electronics brought aboard (LED strips, USB chargers, inverters, plotters
  from non-marine suppliers, Starlink PSUs) are held only to ~43.5 dBµV/m.
  That ~20 dB gap is the single most useful fact for Chapter 31.
- **Radar.** S-band (2.9–3.1 GHz) and X-band (9.3–9.5 GHz) pulses do not
  overlap 162 MHz, but a 25 kW peak magnetron a few metres from a VHF antenna
  can overload an LNA or receiver front end (out-of-band blocking), and
  solid-state radars with switching PSUs can radiate VHF noise. No primary
  measurement report was located in this session; treat as engineering
  reasoning and cite M.1371 blocking figures as the yardstick (verify any
  specific incident before citing).
- **FM broadcast (88–108 MHz).** The classic urban problem for SDR-based
  receivers: strong FM carriers overload wideband front ends (RTL-SDR has no
  preselection) and produce intermodulation products; the fix is an FM
  band-stop ("notch") before the LNA. This is community knowledge (AIS-catcher
  wiki, RTL-SDR blog) rather than standards material; cite as such and show a
  before/after waterfall as original evidence in Chapter 42.
- **Pagers and public-safety.** RTCM 11701.0's own description names pagers as
  the historical interferer to installed VHF radios; paging bands (US 152–159
  MHz, 929–932 MHz) and VHF public-safety/land-mobile (150–174 MHz) share
  towers with the best AIS sites. Same mitigation: bandpass/cavity filters and
  a check with a spectrum analyser before committing to a site.
- **Measurement.** (1) The USCG squelch test with the ship's own VHF; (2) an
  SDR waterfall centred on 162.0 MHz with ±1 MHz span, noting the noise-floor
  rise when each suspect load is switched; (3) the Class B "CS" background
  level (if the transponder exposes it) as a built-in noise meter; (4) for
  shore sites, a 24-h max-hold scan 130–180 MHz and a wideband 30–1,000 MHz
  scan for strong blockers.
- **Mitigation list for the chapter:** separation (vertical first), ferrites
  on LED/PSU leads, replace drivers with RTCM 13700.0/IEC 60945-compliant
  fixtures, bandpass or cavity filter ahead of any LNA, LNA at the antenna not
  the receiver, single-point ground, keep coax away from power bundles,
  double-shielded coax (LMR-400-class), and for SDRs an FM notch plus a
  162 MHz SAW/helical filter.

## Open questions / (verify)

- Retrieve USCG Marine Safety Alert 13-18 PDF (dco.uscg.mil) and quote the
  title and test procedure verbatim; confirm the exact issue date in August
  2018 (verify).
- Locate USCG MSIB 03-22 PDF and its date (April 2022 per search summary)
  (verify).
- IEC 60945 Ed. 4.0: confirm the 24 dBµV/m (156–165 MHz) and 54 dBµV/m (30
  MHz–2 GHz) limits, detector and bandwidth, from the standard or an
  authoritative test lab document; check for any Ed. 5 activity (verify).
- RTCM 13700.0: obtain the limit lines and test distances to compare with
  IEC 60945 (verify).
- NOAA NWR: confirm "up to 1,000 W" from an official page and obtain the
  station list with powers (https://www.weather.gov/nwr/sites) (verify).
- Any peer-reviewed or agency measurement of LED/inverter EMI spectra at
  156–165 MHz (ABYC, Practical Sailor tests, USCG RDC) (verify).
- Specific documented cases of radar-induced AIS desensitisation (MAIB/NTSB
  reports or vendor bulletins) (verify; none located).
- Whether IEC 61993-2 specifies the wanted-signal level used for Class A
  immunity tests (assumed −101 dBm above) (verify).

## Candidate figures and worked examples

1. **Spectrum neighbourhood figure (Ch. 31/37):** 150–175 MHz line with
   marine VHF channels, AIS 1/2, ASM 1/2, 75/76, DSC 70, NWR 162.400–162.550,
   US paging/land-mobile blocks; annotate the ±25 kHz adjacent-channel and
   < 5 MHz blocking regions around AIS 2.
2. **Limits comparison bar chart:** IEC 60945 protected band (24 dBµV/m @ 3 m)
   vs 60945 general (54) vs FCC Part 15 Class B (43.5 @ 3 m) vs Class A
   (150 µV/m @ 10 m).
3. **Worked example — VHF transmit desense:** 25 W at 2 m vertical separation;
   coupling assumptions; compare with M.1371 blocking.
4. **Worked example — NWR at 1 km / 10 km** (above).
5. **Worked example — noise-floor rise → range loss:** a 6 dB noise-floor
   increase at the receiver costs 6 dB of link margin; with 20 dB/decade
   (free space) that is ~50 % range, with 40 dB/decade (two-ray) ~30 %; tie to
   Ch. 27.
6. **Before/after waterfall (Ch. 42):** RTL-SDR at 162 MHz with and without FM
   notch in an urban site (original capture).
7. **Checklist box (Ch. 31):** USCG squelch test steps; SDR noise survey steps.
8. **Table — sources × signature × mitigation:** LED drivers, SMPS/USB
   chargers, VFDs/inverters, battery chargers, radar, own VHF transmit, NWR,
   FM broadcast, pagers/land-mobile, cellular, VSAT/Inmarsat (mostly L/Ku-band
   but PSU noise), power lines/arcing.

## Recommended use by chapter

- **Ch. 27:** sensitivity (−107 dBm) and the immunity table as the receiver's
  "budget"; P.372 for ambient noise by environment.
- **Ch. 31:** the whole dossier; lead with the 2018 USCG alert and RTCM
  13700.0 as the regulatory arc (2018 alert → 2022 standard); the 60945 vs
  Part 15 gap; worked examples 3–5; measurement and mitigation lists.
- **Ch. 32:** COMSAR separation rule; LNA placement; filter choices.
- **Ch. 36:** interference as a silent failure (Class B threshold rise, lost
  range) and how to detect it from message statistics.
- **Ch. 37:** places to avoid (NWR, FM, paging/public-safety colocations,
  radar), with the 1 km/10 km arithmetic.
- **Ch. 42:** FM notch + 162 MHz bandpass recommendations; squelch test.
- **App. B:** IEC 60945 Ed. 4.0 (2002); RTCM 13700.0 (2022); RTCM 11701.0.
