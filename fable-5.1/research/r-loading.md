# Dossier: Network loading, packet loss and collisions — VDL capacity, congestion rules, Class B behaviour under load, satellite detection probability, decollision and partial-packet recovery

**Purpose.** This dossier gathers what could be confirmed, as of 5 October
2026, about how the AIS VHF data link (VDL) behaves as it fills: the capacity
arithmetic from the slot structure and reporting intervals in ITU-R M.1371-6;
the standard's own congestion-resolution rules (intentional slot reuse,
assignment, Class B "SO" modified intervals, Class B "CS" abandonment); what is
known about measured terrestrial loading; the satellite footprint collision
problem and the detection-probability literature (Høye/Eriksen, Cervera/Ginesi,
Clazzer/Munari); receiver techniques that recover more from colliding or
corrupted bursts (coherent/Viterbi receivers, multi-antenna, successive
interference cancellation, partial-CRC-assisted correction); and the patent
landscape sketch. It is the primary dossier for **Chapter 30** and feeds
**Chapter 21** (link layer and slot reuse), **Chapter 20** (reporting
intervals), **Chapter 36** (Class B slot starvation as a failure mode),
**Chapter 39** (satellite AIS decollision), **Chapter 48** (detection
probability as a spatial-statistics input), **Chapter 61** (slot-flooding
attacks: what the congestion rules do under adversarial load), and
**Appendix I** (SOTDMA slot simulator).

> Research-session note. M.1371-6 facts were read from the text extracted from
> the itu.int PDF (printed page numbers given). Paper metadata were verified via
> the Crossref API; abstracts quoted are Crossref-deposited. Two patents were
> looked up on Google Patents; one page loaded (CNES), one did not (503) and is
> marked (verify). No measured terrestrial slot-occupancy study with named
> locations was located and verified in this session — see Open questions.

## Key questions

1. What is the raw capacity (slots/min/channel, bits/slot) and how many
   stations of each class, at each reporting interval, fit before the link is
   "full"?
2. What does M.1371 define as congestion and what does it tell stations to do
   (intentional slot reuse rules, 120 NM, candidate set of 4, base-station
   protection, assignment by Messages 16/23, FATDMA)?
3. How does Class B "SO" react to load (50 %/65 % free-slot thresholds), and how
   does Class B "CS" (10 candidate periods, abandon) — i.e., what is "Class B
   starvation" in standard terms?
4. What measured loading data exist for busy waterways, and who publishes them?
5. What is the satellite collision problem quantitatively (ships in footprint,
   reporting interval, observation time) and what do the canonical papers
   conclude?
6. What survives corruption: CRC-only error detection, so what can receivers
   do — coherent demodulation, Viterbi with constraints, partial-CRC-assisted
   correction, multi-user/multi-antenna detection, successive interference
   cancellation, Doppler/time/space separation, multi-receiver combining?
7. Which patents cover satellite decollision and what is their status?
8. How do shore networks deduplicate, and how should a packet-loss model for
   Chapter 48 be built?

## Primary sources located

| Source | Identifier / edition / year | URL | What it covers | Access |
|---|---|---|---|---|
| Rec. ITU-R M.1371-6 | 02/2026 | https://www.itu.int/dms_pubrec/itu-r/rec/m/R-REC-M.1371-6-202602-I!!PDF-E.pdf | Annex 1 Tables 1–2 reporting intervals; Annex 2 §A2-3.1.6 slot states, §A2-4.4 congestion resolution, §A2-3.2.2 packet; Annex 6 Table 41 and §A6-4.3.3.1 CSTDMA access; §A6-4.4.4 | Free |
| IALA Recommendation R0124 (A-124) *The AIS Service*, App. 18 "VDL load management" | Ed. 2.2 (2012) per `r-standards-iala.md` (medium) | iala.int (see `r-standards-iala.md`) | Shore-side VDL load monitoring and management guidance | Free (registration) |
| Høye, G. K., Eriksen, T., Meland, B. J., Narheim, B. T., "Space-based AIS for global maritime traffic monitoring" | *Acta Astronautica* 62(2–3):240–245, 2008; DOI 10.1016/j.actaastro.2007.07.001 | https://doi.org/10.1016/j.actaastro.2007.07.001 | Satellite AIS feasibility; ship-count vs detection-probability model | Paid |
| Eriksen, T., Høye, G., Narheim, B., Meland, B. J., "Maritime traffic monitoring using a space-based AIS receiver" | *Acta Astronautica* 58(10):537–549 (pages (verify)), 2006; DOI 10.1016/j.actaastro.2005.12.016 | https://doi.org/10.1016/j.actaastro.2005.12.016 | Earlier FFI feasibility paper | Paid |
| Høye, Eriksen, Meland, Narheim, "Space-based AIS for global maritime traffic monitoring" (conference) | *Small Satellites for Earth Observation*, 2005; DOI 10.1515/9783110919806.401 | https://doi.org/10.1515/9783110919806.401 | Conference precursor | Paid |
| Cervera, M. A., Ginesi, A., Eckstein, K., "Satellite-based vessel Automatic Identification System: A feasibility and performance analysis" | *Int. J. Satell. Commun. Netw.* 29(2):117–142, 2011; DOI 10.1002/sat.957 | https://doi.org/10.1002/sat.957 | ESA system simulator; constellation sizing vs detection probability | Paid |
| Cervera & Ginesi, "On the performance analysis of a satellite-based AIS system" | SPSC 2008; DOI 10.1109/spsc.2008.4686715 | https://doi.org/10.1109/spsc.2008.4686715 | Earlier analysis | Paid |
| Burzigotti, P., Ginesi, A., Colavolpe, G., "Advanced receiver design for satellite-based automatic identification system signal detection" | *Int. J. Satell. Commun. Netw.* 30(2):52–63, 2012; DOI 10.1002/sat.1007 (conf. version ASMS 2010, 10.1109/asms-spsc.2010.5586907) | https://doi.org/10.1002/sat.1007 | Coherent receiver, collision handling | Paid |
| Colavolpe, Foggi, Ugolini, Lizarraga, Cioni, "A highly efficient receiver for satellite-based Automatic Identification System signal detection" | ASMS/SPSC 2014, pp. 120–127; DOI 10.1109/asms-spsc.2014.6934533 | https://doi.org/10.1109/asms-spsc.2014.6934533 | Receiver design | Paid |
| Prévost, Coulon, Bonacci, LeMaitre, Millerioux, Tourneret, "Extended constrained Viterbi algorithm for AIS signals received by satellite" | ESTEL 2012; DOI 10.1109/estel.2012.6400111 | https://doi.org/10.1109/estel.2012.6400111 | Exploiting bit-stuffing/CRC structure in the trellis | Paid |
| Prévost et al., "Joint phase-recovery and demodulation-decoding of AIS signals received by satellite" | ICASSP 2013, pp. 4913–4917; DOI 10.1109/icassp.2013.6638595 | https://doi.org/10.1109/icassp.2013.6638595 | Receiver | Paid |
| Prévost et al., "Partial CRC-assisted error correction of AIS signals received by satellite" | ICASSP 2014, pp. 1951–1955; DOI 10.1109/icassp.2014.6853939 | https://doi.org/10.1109/icassp.2014.6853939 | Using the 16-bit CRC for limited error *correction* | Paid |
| Picard, Oularbi, Flandin, Houcke, "An adaptive multi-user multi-antenna receiver for satellite-based AIS detection" | ASMS/SPSC 2012, pp. 273–280; DOI 10.1109/asms-spsc.2012.6333088 | https://doi.org/10.1109/asms-spsc.2012.6333088 | Multi-antenna separation of colliding bursts | Paid |
| Zhou, van der Veen, van Leuken, "Multi-user LEO-satellite receiver for robust space detection of AIS messages" | ICASSP 2012, pp. 2529–2532; DOI 10.1109/icassp.2012.6288431 | https://doi.org/10.1109/icassp.2012.6288431 | Multi-user detection | Paid |
| Gallardo & Sorger, "Coherent receiver for AIS satellite detection" | ISCCSP 2010; DOI 10.1109/isccsp.2010.5463417 (also ISCC 2010 "Multiple decision feedback equalizer…", 10.1109/iscc.2010.5546731) | https://doi.org/10.1109/isccsp.2010.5463417 | Receiver | Paid |
| Clazzer, F., Munari, A., Berioli, M., Blasco, F. L., "On the characterization of AIS traffic at the satellite" | OCEANS 2014 Taipei; DOI 10.1109/oceans-taipei.2014.6964425 | https://doi.org/10.1109/oceans-taipei.2014.6964425 | Traffic model at the satellite | Paid |
| Clazzer & Munari, "Analysis of capture and multi-packet reception on the AIS satellite system" | OCEANS 2015 Genova; DOI 10.1109/oceans-genova.2015.7271399 | https://doi.org/10.1109/oceans-genova.2015.7271399 | Capture effect and MPR | Paid |
| Clazzer, Munari, Giorgi, "Asynchronous random access schemes for the VDES satellite uplink" | OCEANS 2017 Aberdeen; DOI 10.1109/oceanse.2017.8084618 | https://doi.org/10.1109/oceanse.2017.8084618 | VDE-SAT uplink access | Paid |
| Eisler, Dobias, MacNeil, "A Surveillance Application of Satellite AIS – Utilizing a Parametric Model for Probability of Detection" | ICORES 2017, pp. 211–218; DOI 10.5220/0006108302110218 | https://doi.org/10.5220/0006108302110218 | Parametric Pd model for operational use | Free (SciTePress) (verify) |
| US 9,246,575 B2, "Method for detecting AIS messages" | Inventors Antoine de Latour, Michel Faup; assignee CNES; priority 2011-09-05; application 13/598,011; published as US 2013/0058271 A1; granted 2016-01-26 | https://patents.google.com/patent/US9246575B2/en | Correlating received data with hypothetical fragmentary messages built from a transmitter database (known MMSI/position) to detect AIS in collisions | Free |
| US 2008/0304597 A1 (Peach, R.) | Application publication; grant number (verify) | https://patents.google.com/patent/US20080304597A1/en (503 at read time) | COM DEV-era AIS detection/decoding from space (per search summary) | Free |
| Harati-Mokhtari, A., Wall, A., Brooks, P., Wang, J., "Automatic Identification System (AIS): Data Reliability and Human Error Implications" | *J. Navigation* 60(3):373–389, 2007; DOI 10.1017/S0373463307004298 | https://doi.org/10.1017/S0373463307004298 | Data-quality baseline (feeds Ch. 36/47 rather than loading, listed for cross-reference) | Paid |

## Verified facts

| Fact | Source | Confidence |
|---|---|---|
| Frame = 1 min = 2,250 slots per channel; slot = 26.667 ms = 256 bits at 9,600 bit/s; two channels (AIS 1/AIS 2) → 4,500 slots/min. Default packet 168 data bits; up to 5 consecutive slots per transmission. | M.1371-6 Table 6/12, §A2-3.2.2.11 (see `r-rf-phy.md`, `r-link-layer.md`) | high |
| Class A nominal reporting intervals (Table 1): at anchor/moored ≤ 3 kn → 3 min; at anchor/moored > 3 kn → 10 s; 0–14 kn → 10 s; 0–14 kn changing course → 3⅓ s; 14–23 kn → 6 s; 14–23 kn changing course → 2 s; > 23 kn → 2 s. Semaphore station → 2 s. | M.1371-6 Annex 1 Table 1, p. 9 | high |
| Other stations (Table 2): Class B "SO" ≤ 2 kn → 3 min; 2–14 kn → 30 s; 14–23 kn → 15 s (modified 30 s); 14–23 kn changing course → 5 s (modified 15 s); > 23 kn → 5 s (modified 15 s). Class B "CS" ≤ 2 kn → 3 min; > 2 kn → 30 s (15 s when > 14 kn). SAR aircraft 10 s (2 s when manoeuvring). AtoN 3 min; mobile AtoN > 2 kn 30 s. Base station 10 s (3⅓ s when stations sync to it). | M.1371-6 Annex 1 Table 2 and notes, pp. 9–10 | high |
| Class B "SO" uses the *modified* reporting interval "only when the last four consecutive frames each have less than 50 % Free slots" and returns to normal only when "65 % or more of the slots of each of the last four consecutive frames are free". | M.1371-6 Table 2 note (3), p. 10 | high |
| Slot states: Free (incl. slots reserved by stations beyond 120 NM, and SOTDMA reservations unused for three frames); Internal; External; Garbled (no decodable message and RSSI > 16 dB above background; distinguished only by repeaters). | M.1371-6 §A2-3.1.6 (text at p. 22) | high |
| Congestion definition and remedies: "When the data link is loaded to such a level that no free slots are available for transmission" → (a) intentional slot reuse by own station (§A2-4.4.1) or (b) assignment by base station (§A2-4.4.2). | M.1371-6 §A2-4.4, p. 56 | high |
| Intentional slot reuse: only with own position available; when the candidate set has fewer than 4 slots, reuse to bring it to 4; reused slots taken from the most distant station(s) within the SI; never from stations with no position; base-station slots only if the base station is > 120 NM away; a reused-from station is excluded from further reuse for one frame; the process "may report less than four slots". | M.1371-6 §A2-4.4.1, p. 56 | high |
| Assignment for congestion: a base station may assign report rate (Rr) to all mobiles *except Class A*; for Class A it may redirect slots to FATDMA-reserved slots; an assigned interval below 5 s is not required. | M.1371-6 §A2-4.4.2 and base-station operation text, pp. 56–57 | high |
| Class B "CS" access (Table 41): RI 5 s–10 min; transmission interval TI = RI/3 or 10 s, whichever is less, centred on the nominal transmission time; 10 candidate periods randomly placed in TI; test carrier sense in each; "Transmission should be abandoned if all 10 CPs are 'used'". | M.1371-6 Annex 6 Table 41, §A6-4.3.3.1, pp. 93–94 | high |
| Class B "CS" congestion: the CSTDMA algorithm "guarantees that the time period intended for transmission does not interfere with transmissions made by stations complying with Annex 2. Additional congestion resolution methods are not required and should not be used." | M.1371-6 §A6-4.4.4, p. 101 | high |
| CS detection threshold floor −107 dBm, cap −77 dBm (noise + 10 dB); a Class B CS therefore defers to any Annex-2 burst it can hear above that threshold in the 833–1,979 µs window. | M.1371-6 §A6-4.3.1.2–1.3, p. 87 | high |
| No FEC, interleaving or scrambling; 16-bit CRC over the data field only; "CRC errors should result in no further action by the AIS station". | M.1371-6 Table 4, §A2-3.2.2.6, §A2-3.2.3 | high |
| Message 27 is shortened to 96 data bits with a 96-bit guard to tolerate satellite footprint delay spread up to 1,000 km altitude, nominal interval 3 min, alternating 75/76. | M.1371-6 Annex 3 Table 22, §A3-2.3 | high |
| Burst devices (AIS-SART etc.) ignore the slot map: 8 messages at 75-slot spacing once per minute; the standard calls this "disruptive to the VDL". | M.1371-6 Annex 8 §A8-1, §A8-5 | high |
| Cervera, Ginesi & Eckstein (2011) abstract: the paper "outlines technical challenges like the high rate of message collisions from ships in the field of view of a satellite", uses "a computer-based system simulator", and finds that "a relatively small constellation of LEO satellites can guarantee good ship position detection probability as well as a reporting time interval of a few hours". | Crossref-deposited abstract, DOI 10.1002/sat.957 | high |
| Høye et al. 2008 is *Acta Astronautica* 62(2–3):240–245 (Crossref). Its detection-probability expression as a function of ships in the field of view, reporting interval and observation time is the basis of later work, but the exact formula was not read in this session. | Crossref record | high (metadata); formula (verify) |
| The satellite receiver literature 2010–2014 (Gallardo & Sorger 2010; Burzigotti et al. 2012; Picard et al. 2012; Zhou et al. 2012; Prévost et al. 2012/2013/2014; Colavolpe et al. 2014) addresses coherent demodulation, constrained Viterbi decoding using bit-stuffing/CRC structure, partial-CRC-assisted error correction, and multi-antenna multi-user detection for colliding AIS bursts. | Crossref records (titles/venues) | high (existence); content from titles/abstracts only |
| Clazzer et al. characterised AIS traffic at the satellite (OCEANS 2014) and analysed capture and multi-packet reception (OCEANS 2015); the same DLR group proposed asynchronous random access for the VDES satellite uplink (OCEANS 2017). | Crossref records | high (existence) |
| US 9,246,575 B2 (CNES; de Latour & Faup; priority 2011-09-05; granted 2016-01-26) claims detecting AIS messages in satellite data by correlating with "a hypothetical fragmentary message" built from "a database of AIS transmitters" (i.e., using known MMSI/position fields as a long known-data sequence). | Google Patents page read 2026-10-05 | high |
| The search summary attributing US 9,246,575 to exactEarth is wrong — the assignee is CNES. | Same | high |

## Notes and quotes

- **Capacity arithmetic (for the chapter's worked example).** One channel
  offers 2,250 slots/min. A Class A at 10 s uses 6 slots/min; at 2 s, 30
  slots/min; at anchor, ⅓ slot/min (plus Message 5 every 6 min = 2 slots,
  i.e., ⅓ slot/min). Ignoring base stations, AtoNs and binary traffic, a cell
  of 150 under-way Class A ships at 10 s on each channel alternately uses
  150 × 6 / 2 = 450 slots/min/channel = 20 %. The link is self-organising, so
  "full" is not a cliff: beyond roughly 50 % the candidate set shrinks, slot
  reuse begins, and distant stations' slots are reused first — the *cell
  shrinks* rather than failing. The Class B "SO" 50 %/65 % hysteresis in Table 2
  is the standard's own operational definition of "loaded".
- **Quote (§A2-4.4.1):** "The intentionally reused slots should be taken from
  the most distant station(s) within the SI. Slots allocated or used by base
  stations should not be used unless the base station is located over 120 NM
  from the own station."
- **Class B starvation, precisely.** A Class B "CS" has no slot map; it picks
  10 random candidate periods inside a window of at most 10 s around its
  nominal time and must find one whose first 1.1 ms is below (noise + 10 dB).
  Under heavy Class A load most periods are "used" and the report is
  *abandoned* for that interval (Table 41 rule 3) — it is not deferred and does
  not accumulate. The shore observer sees Class B cadence stretch from 30 s to
  minutes; the ship's own display shows nothing wrong. This is the mechanism
  behind "Class B is invisible in busy ports" and belongs in Ch. 30 and Ch. 36.
- **Class B "SO" degrades differently:** it keeps a slot map and merely halves
  its rate when < 50 % slots are free for four frames — so in congested water a
  "B+" unit is more visible than a "CS" unit. Good *Definitions that bite* box.
- **Why satellites collide.** A LEO footprint ~5,000 km across sees thousands
  of ships; each terrestrial cell self-organised independently, so slot
  choices are uncorrelated between cells and overlap at the satellite. Add
  ±(several) kHz Doppler and up to ~2,000 km differential path (~7 ms), and
  bursts arrive misaligned to the slot grid. Message 27's 96-bit guard and
  3-min cadence are the protocol-side answer; receiver-side answers are the
  2010–2014 literature above.
- **What can be recovered.** With CRC-only protection, the standard receiver
  discards any burst with a bit error. The literature shows three levers:
  (1) better demodulation (coherent GMSK, phase recovery) lowers the raw BER;
  (2) decoder-side structure — bit stuffing constrains the trellis (Prévost
  2012), and the 16-bit CRC can correct a small number of errors if candidate
  error patterns are enumerated (Prévost 2014) at the cost of false accepts;
  (3) multi-user separation — multiple antennas/polarisations (Picard 2012;
  Zhou 2012), capture effect and multi-packet reception (Clazzer & Munari
  2015), and *known-data correlation* using MMSI/position priors (CNES patent
  US 9,246,575). Terrestrial networks add a fourth lever: spatial diversity
  across receivers with deduplication by (MMSI, payload, time window).
- **Shore-network dedup.** Not covered by M.1371; practice is deduplication on
  identical payload within a window of a few seconds with receiver-id
  retained in TAG blocks (see `r-messages.md` / Ch. 26). Keep the first copy's
  receiver time and the count of receivers — the count is a free coverage
  signal for Ch. 48.
- **Security hand-off (Ch. 61).** The rules above bound a slot-flooding
  attacker: Class A victims shrink their cell and reuse the attacker's slots
  (if it reports a position) rather than going silent; Class B "CS" victims go
  silent first; base-station slots are protected unless > 120 NM. Burst
  devices are the standard's own example of a disruptive access scheme.

## Open questions / (verify)

- **Measured terrestrial load figures.** No peer-reviewed or official report
  with named-location slot-occupancy percentages (Singapore Strait, Dover,
  Bosporus, Shanghai, Mississippi) was located and verified. Candidates to
  pursue: IALA R0124 App. 18 (VDL load management) and IALA ENAV committee
  input papers; HELCOM AIS Expert Working Group reports; EMSA; USCG RDC
  reports (search the DTIC/NTRL catalogue for "AIS VDL loading"); Korean
  journal papers (a koreascience.kr hit appeared in a search summary,
  unverified); port-authority VTS vendor case studies (verify all).
- Exact Høye 2008 detection-probability formula and the headline numbers
  (ships-in-view thresholds for 90 %/99 % detection over a pass) (verify by
  reading the paper).
- Eriksen et al. 2006 page range (verify).
- US 2008/0304597 A1 (Peach): confirm assignee (COM DEV?), title, and whether
  it was granted (verify); search for exactEarth/COM DEV, ORBCOMM, Spire,
  Kongsberg/FFI and DLR decollision patents by assignee on Google Patents
  (verify each before listing in Ch. 18/30).
- Whether any manufacturer publishes measured Class B "CS" delivery ratios
  versus VDL load (type-approval tests in IEC 62287-1 include a loaded-VDL
  scenario — confirm the load level used) (verify).
- IEC 61993-2 test for "VDL load > 90 %" behaviour mentioned in a search
  summary — confirm clause and load level (verify).
- A clean open-source SOTDMA/CSTDMA simulator to cite (several GitHub projects
  exist; none verified in this session) (verify).
- Eisler et al. 2017 (ICORES) open-access status and the parametric model's
  form (verify).

## Candidate figures and worked examples

1. **Capacity ladder (Ch. 30):** stacked bar of slots/min/channel consumed by
   N Class A at 2/6/10 s, M Class B at 30 s, K AtoN at 3 min, base stations at
   10 s with FATDMA reservations; mark the 50 % and 65 % Class B "SO" thresholds.
2. **Worked example — a busy anchorage:** 300 Class A at anchor (3 min) + 60
   under way at 10 s + 120 Class B CS at 30 s + 2 base stations + 20 AtoN →
   slots/min on each channel; show it is ~13 % — then redo for a strait with
   250 ships under way at 6 s to show ~56 % and trigger the Class B "SO" rule.
3. **Slot-reuse cartoon (Ch. 21/30):** a station's SI with candidate set < 4,
   showing which external slots become candidates (most distant first, base
   stations excluded inside 120 NM).
4. **CSTDMA timing figure (Ch. 30/36):** nominal time, TI = min(RI/3, 10 s),
   10 random CPs, carrier-sense window 833–1,979 µs, abandon after 10 "used".
5. **Satellite collision geometry (Ch. 39):** footprint circle with several
   terrestrial cells; Venn of slot overlap; Doppler and delay axes; where
   Message 27's 96-bit guard sits.
6. **Detection-probability curves:** P(detect ship in one pass) vs ships in
   footprint for reporting intervals 2/6/10 s and observation times 5–15 min,
   computed with a simple independent-collision model (state assumptions;
   compare qualitatively to Høye 2008 once the formula is verified).
7. **Recovery-technique table (Ch. 30):** technique | where (sat/shore) |
   gain | cost/false-accept risk | representative paper/patent.
8. **Packet-loss model skeleton (Ch. 48):** P(received) = P(range) ×
   P(no collision | load) × P(no CRC error | SNR) × P(not deduped away);
   each factor's data source.
9. **Try it (App. I):** SOTDMA/CSTDMA slot simulator in Python producing the
   curves in items 1, 2 and 6.

## Recommended use by chapter

- **Ch. 20:** Tables 1–2 reporting intervals verbatim (with the Class B "SO"
  modified-interval note and the Class B "CS" 15 s > 14 kn case).
- **Ch. 21:** §A2-3.1.6 slot states and §A2-4.4.1 intentional reuse rules;
  cross-reference `r-link-layer.md` for candidate-slot selection detail.
- **Ch. 30:** capacity ladder; congestion rules; Class B behaviours; satellite
  collision problem; recovery techniques with the verified paper list; the
  CNES patent as the "known-data correlation" example; packet-loss model.
- **Ch. 36:** Class B "CS" abandonment as a silent failure mode; how to detect
  it from shore (cadence histogram vs. speed).
- **Ch. 39:** Høye 2008, Eriksen 2006, Cervera 2011 as the founding analyses;
  Burzigotti/Prévost/Picard/Colavolpe/Clazzer for receiver design; Message 27
  rationale.
- **Ch. 48:** detection-probability factorisation; receiver-count from dedup
  as a coverage signal; warn that satellite Pd depends on regional density.
- **Ch. 61:** what the congestion rules imply about slot-flooding and
  fake-position attackers; burst devices as a legitimate "disruptive" scheme.
- **Ch. 18:** US 9,246,575 (CNES) verified; other satellite-AIS patents (verify).
- **App. I:** slot simulator.
