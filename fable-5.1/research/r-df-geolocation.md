# Dossier: Direction finding and independent geolocation of AIS transmitters

**Purpose.** This dossier gathers what can be confirmed, as of October 2026,
about locating an AIS transmitter *without trusting the position it reports*:
shipboard and shore VHF direction finders used for search and rescue and VTS
(RHOTHETA RT-500-M; Rohde & Schwarz digital direction finders), multi-receiver
time-difference-of-arrival (TDOA) radiolocation of AIS bursts using existing
base-station networks (Papi et al. 2014/2015, EC JRC), single-satellite Doppler
and multi-satellite TDOA/FDOA geolocation (Guo 2014; Ellis, Van Rheeden &
Dowla 2020; HawkEye 360; Unseenlabs; Kleos), and the cheaper plausibility
checks that approximate geolocation (received-power/range-ring tests, radar
correlation). It feeds **Chapter 35** (Direction finding and independent
geolocation) primarily, and supplies material to **Chapter 30** (multi-receiver
networks), **Chapter 39** (satellite reception, Doppler), **Chapter 47**
(spoofed-segment handling), **Chapter 59** (spoofing detection), **Chapter 62**
(GNSS-interference localisation by TDOA), **Chapter 66** (RF geolocation as an
alternative tracking source), and **Chapter 68** (SART/MOB homing).

> Research-session note. Bibliographic facts marked *high* were confirmed via
> Crossref API records for the DOIs listed. Vendor and company facts marked
> *medium* come from search summaries of vendor pages, press releases and
> launch manifests; several vendor pages (he360.com, JRC publications
> repository) returned 403/login during the session and were not read
> directly. Accuracy claims for commercial systems are vendor statements
> unless a paper is cited.

## Key questions

1. What does a VHF direction finder actually measure on an AIS burst (26.67 ms,
   GMSK, 9,600 bit/s), and which DF methods (Watson-Watt, Doppler, correlative
   interferometer) are fast enough to bear a single slot?
2. Which DF products are marketed for maritime SAR/VTS, what bands and
   accuracies do they claim, and do any decode AIS to associate bearings with
   MMSIs?
3. How well does TDOA from a network of ordinary shore base stations locate an
   AIS transmitter — what accuracy was demonstrated, with how many stations,
   and what timing reference was required?
4. How do satellites geolocate AIS (and other) emitters: single-satellite
   Doppler curves vs formation-flying TDOA/FDOA; what accuracy is claimed;
   which companies fly it; what public case studies exist?
5. What are the cheap approximations (received-power vs reported range;
   detection by a receiver whose horizon excludes the reported position;
   radar/AIS correlation) and how do they fail?
6. How is independent geolocation used operationally — catching spoofers,
   relocating off-position AtoN, SAR homing — and what are the legal/privacy
   considerations?

## Primary sources located

| Source | Identifier / edition / year | URL | What it covers | Access |
|---|---|---|---|---|
| Papi, Tarchi, Vespe, Oliveri, Borghese, Aulicino & Vollero | *IET Radar, Sonar & Navigation* 9(5):568–580, June 2015, DOI 10.1049/iet-rsn.2014.0292 | https://doi.org/10.1049/iet-rsn.2014.0292 | TDOA radiolocation + EKF tracking of AIS signals using existing base stations; discrepancies between claimed and estimated origin "of the order of hundreds of metres" | Paid (open copy via JRC repository, login required) |
| Papi, Tarchi, Vespe, Oliveri & Aulicino | IEEE SSP 2014, pp. 504–507, DOI 10.1109/SSP.2014.6884686 | https://doi.org/10.1109/SSP.2014.6884686 | Earlier conference version of the TDOA method | Paid |
| Guo, S. | SPIE Proc. 2014, "Space-based detection of spoofing AIS signals using Doppler frequency", DOI 10.1117/12.2050448 | https://doi.org/10.1117/12.2050448 | Single-satellite Doppler consistency test for satellite-received AIS | Paid |
| Ellis, Van Rheeden & Dowla | *IEEE Access* 8, 2020, "Use of Doppler and Doppler Rate for RF Geolocation Using a Single LEO Satellite", DOI 10.1109/ACCESS.2020.2965931 | https://doi.org/10.1109/ACCESS.2020.2965931 | Theory and accuracy of single-LEO Doppler/Doppler-rate geolocation (general RF; applies to AIS) | Free (IEEE Access) |
| Androjna, Perkovič, Pavic & Mišković | *Applied Sciences* 11(11):5015, 2021, DOI 10.3390/app11115015 | https://doi.org/10.3390/app11115015 | "AIS Data Vulnerability Indicated by a Spoofing Case-Study" — Elba Island 2019 spoofing event; uses received signal level and multi-station reception as evidence | Free |
| Kruger, M. | FUSION 2019, "Detection of AIS Spoofing in Fishery Scenarios", DOI 10.23919/FUSION43075.2019.9011328 | https://doi.org/10.23919/FUSION43075.2019.9011328 | Spoofing detection in fisheries context (includes physical-layer/propagation plausibility) | Paid |
| d'Afflisio, Braca & Willett | *IEEE Trans. AES* 57(4):2093–2108, 2021, DOI 10.1109/TAES.2021.3083466 | https://doi.org/10.1109/TAES.2021.3083466 | Statistical framework for malicious AIS spoofing and stealth deviations (track-level, complements RF geolocation) | Paid |
| Gattis, Cydejko & Akos | *GPS Solutions*, 2026, DOI 10.1007/s10291-026-02061-5 | https://doi.org/10.1007/s10291-026-02061-5 | Baltic Sea GNSS jamming/spoofing emitter detection and localisation in real time by TDOA (methodological sibling for ch. 62) | Paid |
| RHOTHETA Elektronik, RT-500-M | product page (navigation only rendered) | https://www.rhotheta.de/products/rt-500-m/ | Wide-band SAR direction finder, 118–470 MHz incl. marine band 156.000–162.025 MHz, 121.5/243 MHz, Cospas-Sarsat 406 MHz | Free |
| Rohde & Schwarz direction finders (DDF series) | product family pages | https://www.rohde-schwarz.com/ | Digital DF (correlative interferometer) used in coastal surveillance/VTS; vendor-quoted ~2° RMS class accuracy for VHF marine DF systems | Free |
| HawkEye 360 | company pages; "Tracking the Romina" resource (403 during session) | https://www.he360.com/ | Formation-flying clusters (Pathfinder launched 3 Dec 2018 on SSO-A); TDOA/FDOA geolocation; "DarkRF" (RF detections without AIS); Romina 2020 case | Free (marketing) |
| Unseenlabs | company pages; eoPortal entry on BRO | https://unseenlabs.com/ ; https://www.eoportal.org/ | BRO (Breizh Reconnaissance Orbiter) single-satellite RF geolocation; BRO-1 launched 19 Aug 2019 on Rocket Lab "Look Ma, No Hands"; 25 satellites by Oct 2026 (company statement) | Free |
| Kleos Space | ASX announcements; company site | https://kleos.space/ | Scouting Mission KSM1 (4 satellites, Nov 2020), Vigilance KSF1 (2021), Patrol KSF2 (2022); July 2023 bankruptcy announcement later paused; status unresolved | Free |
| ITU-R M.1371-5 | 2014 | https://www.itu.int/rec/R-REC-M.1371 | Slot timing (26.67 ms), training sequence, ramp-up; the timing reference a TDOA system exploits | Free |
| Kessler, Craiger & Haass | *TransNav* 12(3):429–437, 2018, DOI 10.12716/1001.12.03.01 | https://doi.org/10.12716/1001.12.03.01 | Taxonomy that places geolocation among detection controls | Free |

## Verified facts

| Fact | Source | Confidence |
|---|---|---|
| Papi et al. 2015 is in *IET RSN* vol. 9, issue 5, pp. 568–580, June 2015, DOI 10.1049/iet-rsn.2014.0292, seven authors (Papi, Tarchi, Vespe, Oliveri, Borghese, Aulicino, Vollero) | Crossref record | high |
| The method combines TDOA radiolocation with an extended Kalman filter tracking in geodetic coordinates, uses existing ground AIS base stations with overlapping coverage and no additional sensors, and was validated on anonymised real data; discrepancies between broadcast position and estimated signal origin were identified "in the order of hundreds of meters" | JRC publication abstract via search summary (repository required login) | medium |
| A 2014 IEEE SSP conference paper (pp. 504–507, DOI 10.1109/SSP.2014.6884686) precedes the journal version | Crossref record | high |
| Guo (2014) published "Space-based detection of spoofing AIS signals using Doppler frequency" in SPIE Proceedings, DOI 10.1117/12.2050448 | Crossref record | high |
| Ellis, Van Rheeden & Dowla (2020) published single-LEO Doppler/Doppler-rate RF geolocation theory in *IEEE Access*, DOI 10.1109/ACCESS.2020.2965931 | Crossref record | high |
| Androjna et al. (2021) documented a spoofing case study (Elba Island, 2019) in *Applied Sciences* 11:5015, DOI 10.3390/app11115015 | Crossref record; search summary for case content | high (bib) / medium (content) |
| Kruger (2019) "Detection of AIS Spoofing in Fishery Scenarios", FUSION 2019, DOI 10.23919/FUSION43075.2019.9011328 | Crossref record | high |
| d'Afflisio, Braca & Willett (2021) *IEEE TAES* 57:2093–2108, DOI 10.1109/TAES.2021.3083466 | Crossref record | high |
| Gattis, Cydejko & Akos (2026) *GPS Solutions*, DOI 10.1007/s10291-026-02061-5, real-time TDOA localisation of Baltic GNSS interference emitters | Crossref record | high |
| RHOTHETA RT-500-M covers 118–470 MHz including 88 marine channels 156.000–162.025 MHz, 121.5 MHz and 243 MHz emergency frequencies, and Cospas-Sarsat 406 MHz with beacon decoding; it is marketed for SAR | Search summary of RHOTHETA/dealer pages (product page itself rendered only navigation) | medium |
| Rohde & Schwarz markets digital direction finders using the correlative-interferometer method for VHF/UHF, deployed in coastal surveillance/VTS, with vendor-quoted accuracy around 2° RMS for marine-band systems | Search summary of R&S pages | medium |
| HawkEye 360 (Herndon, Virginia; founded 2015) launched its first three-satellite "Pathfinder" cluster on 3 Dec 2018 on Spaceflight's SSO-A (Falcon 9, Vandenberg); geolocation uses TDOA and FDOA across formation-flying satellites | Search summary of he360.com and launch coverage | medium |
| HawkEye 360 publicised tracking the Iranian tanker *Romina* in 2020 after it disabled AIS near Suez, by geolocating VHF Channel 16 emissions near Baniyas, Syria, fused with SAR/EO imagery; the company brands RF detections without matching AIS as "DarkRF" | Search summary of he360.com/GeospatialWorld coverage (he360 resource page returned 403) | medium |
| Unseenlabs' BRO-1 (6U CubeSat) launched 19 Aug 2019 on Rocket Lab Electron "Look Ma, No Hands"; the company states single-satellite ("monosatellite") geolocation capability and a 25-satellite constellation as of Oct 2026 | Search summaries of Rocket Lab/Spaceflight Now and company statements | medium |
| Kleos Space launched Scouting Mission KSM1 (four satellites) in Nov 2020, Vigilance (KSF1) in 2021, Patrol (KSF2) in 2022; announced a bankruptcy filing in Luxembourg in July 2023, later reported paused; as of 2024 it stated no filing had been lodged | Search summary of company/ASX statements and trade press | medium |

## Notes and quotes

**Why geolocation is the strongest spoofing control.** Every other
spoof-detection method in this book (track plausibility, Doppler consistency,
received power, timing) is a *consistency* test that a careful adversary can
satisfy. Geolocating the actual emitter is an *independent measurement*; the
adversary cannot change physics, only move the transmitter. Chapter 35 should
be framed around that distinction and then be honest about accuracy and
coverage limits.

**What a DF set sees of an AIS burst.** An AIS transmission occupies one
26.67 ms slot (M.1371: 2,250 slots/min/channel). Classic Watson-Watt and
Doppler DF sets can produce a bearing from a few milliseconds of carrier, so
single-slot bearings are feasible; correlative-interferometer sets (R&S DDF
class) are also designed for short bursts. The practical issue is
*association*: a DF bearing has no MMSI. Associating a bearing with a decoded
message requires either a receiver co-located with the DF that time-stamps the
slot, or software that pairs the burst time with the DF's time-tagged bearing.
No commercial DF product confirmed in this session advertises on-board AIS
decoding; the RT-500-M explicitly decodes Cospas-Sarsat 406 MHz beacon IDs but
is marketed for voice/beacon homing in the marine band. Mark the AIS-decoding
question (verify) and ask vendors.

**TDOA with ordinary base stations (Papi et al.).** The attractive result is
that no new sensors are needed: shore AIS base stations with overlapping
coverage, if they time-stamp burst arrival precisely (GNSS-disciplined), yield
TDOA hyperbolae and hence a fix. At 9,600 bit/s the symbol period is 104 µs,
and 1 µs of timing error corresponds to 300 m of range difference, so the
"hundreds of metres" discrepancy resolution reported is consistent with
sub-microsecond timestamping. This gives Chapter 35 a clean worked example:
three stations, 1 µs timing, geometry, GDOP.

**Single-satellite Doppler.** A LEO satellite at ~7.5 km/s sees ±~4 kHz
Doppler on 162 MHz (verify the exact figure in r-propagation / ch. 39). Each
received AIS burst therefore carries a frequency offset that depends on where
the transmitter sits relative to the ground track. Guo (2014) proposed testing
the claimed position against the Doppler expected for it; Ellis et al. (2020)
give the general accuracy theory for Doppler and Doppler-rate geolocation from
one satellite. The limitation is that a single burst gives one Doppler value
(a cone of positions); several bursts along the pass are needed for a fix, and
transmitter oscillator offset (itself a fingerprinting feature — see
r-fingerprinting) is confounded with Doppler unless multiple passes are used.

**Formation-flying TDOA/FDOA (HawkEye 360) vs monosatellite (Unseenlabs).**
HawkEye 360 flies clusters of three satellites and solves TDOA/FDOA across
them; Unseenlabs states a single-satellite method. Both market "dark ship"
detection: RF emissions (radar, VHF voice, satcom, and AIS itself) geolocated
and compared with AIS. The *Romina* (2020) narrative is the most-cited public
case: AIS switched off, VHF Ch 16 emissions geolocated, confirmed by imagery.
The book should cite the company resource and trade coverage, label it a
vendor case study, and note that accuracies are vendor claims. Kleos
illustrates the commercial risk of the sector (2023 insolvency announcement,
subsequently paused).

**Cheap approximations and their failure modes.**
1. *Range ring:* a shore receiver with antenna height h has a radio horizon
   d ≈ 4.12(√h_rx + √h_tx) km (ch. 27). A report received from a ship that
   claims to be far beyond that horizon is suspicious — but ducting produces
   genuine 500 km receptions, so this is a flag, not proof (ch. 29).
2. *Received power vs claimed distance:* used in the Elba 2019 analysis
   (Androjna et al. 2021) and in the AIS-TSH dataset design (see
   r-fingerprinting); confounded by antenna height, sea state, and the
   12.5 W/2 W power classes.
3. *Multi-receiver consistency:* a message received by stations A and B but
   not by nearer station C argues the transmitter is not where it claims.
4. *Radar/AIS correlation:* the VTS standard method; fails for small targets
   below radar detection and when the spoofer places the ghost near a real
   radar contact.

**Operational uses.** (a) Spoofer hunting by authorities (combine DF bearing
with TDOA fix); (b) relocating an AtoN whose Message 21 position is wrong
(off-position flag absent) by DF from a tender; (c) SAR: AIS-SART and AIS-MOB
devices transmit their own GNSS position, so homing is normally by position,
with DF (121.5 MHz on combined beacons) as fall-back — check the device class;
(d) interference hunting (Gattis et al. 2026 for GNSS jammers in the Baltic
shows the same TDOA toolkit applied to the interference source rather than
the AIS transmitter).

**Legal note (for the chapter box).** Passive DF and TDOA of signals a vessel
is legally required to broadcast raise few issues for authorities. Private
networks performing geolocation at scale (satellite RF providers) sell what
is, in effect, emitter surveillance; the privacy chapter (19) should carry the
discussion, and Chapter 35 should link to it.

## Open questions / (verify)

- (verify) Papi et al. 2015: number of base stations used, timing reference
  (GNSS 1PPS?), achieved 1σ accuracy, and the exact quoted discrepancy
  figures. Obtain the paper (JRC repository JRC91867 or IET).
- (verify) Whether any commercial maritime DF (RHOTHETA, R&S, Taiyo, others)
  decodes AIS to tag bearings with MMSI, and whether any VTS integrates DF
  bearings with the AIS track table.
- (verify) R&S model numbers and quoted accuracies for marine-band DF
  (DDF205/DDF255/DDF550 family?) from a current datasheet.
- (verify) RHOTHETA RT-500-M bearing accuracy and whether the RT-1000 line is
  the VTS/ATC product (the search conflated R&S and RHOTHETA naming).
- (verify) HawkEye 360 publicly stated geolocation accuracy for VHF emitters;
  the *Romina* resource page text (403 during session).
- (verify) Unseenlabs' quoted geolocation accuracy and whether BRO detects
  AIS itself or only other emitters.
- (verify) Kleos Space's final corporate status (2024–2026).
- (verify) Doppler magnitude at 162 MHz for a ~500–600 km orbit (±3.5–4 kHz?);
  reconcile with r-propagation / ch. 39.
- (verify) Any published accuracy for AIS geolocation by Spire/exactEarth
  using Doppler across their constellation (none located).
- (verify) Elba 2019 case details in Androjna et al.: number of stations,
  received-level evidence, conclusion about transmitter location.

## Candidate figures and worked examples

1. **Worked example — three-station TDOA**: stations 30–50 km apart with
   GNSS-disciplined timestamps (±0.5 µs); draw the hyperbolae for one burst,
   compute the fix and the GDOP ellipse; then show a spoofed report 20 km from
   the fix. Reuse the 1 µs ≈ 300 m rule of thumb.
2. **Worked example — single-satellite Doppler**: for a 550 km orbit, plot
   expected Doppler at 162 MHz vs cross-track distance for one pass; mark a
   burst whose claimed position implies +2.1 kHz but which arrived at −1.3 kHz.
3. **Figure — DF association problem**: timeline of slots with DF bearings
   time-tagged; show how a co-located decoder pairs bearing to MMSI.
4. **Figure — range-ring plausibility**: receiver horizon circles for h = 10,
   50, 200 m vs a reported position; annotate the ducting caveat.
5. **Table — commercial RF-geolocation providers**: HawkEye 360 (cluster
   TDOA/FDOA; first launch Dec 2018), Unseenlabs (monosatellite; Aug 2019),
   Kleos (clusters; Nov 2020; insolvency 2023); columns: method, first
   launch, constellation size "as of", maritime product name, public case.
6. **Case file — *Romina* (2020)**: AIS off → VHF Ch 16 geolocation → imagery
   confirmation; cite HawkEye 360 and trade press; label as vendor case.
7. **Try it**: NumPy script that, given three receiver positions and arrival
   times, solves the TDOA fix by least squares and prints the residual; input
   file format mirrors AIS-catcher's per-message timestamp/receiver-id output.

## Recommended use by chapter

- **Ch. 35** — core chapter: DF physics for a 26.67 ms burst; products
  (RHOTHETA, R&S) with (verify) tags on accuracies; TDOA from base stations
  (Papi 2014/2015) with the worked example; satellite Doppler (Guo 2014;
  Ellis 2020) and cluster TDOA/FDOA (HawkEye 360), monosatellite (Unseenlabs),
  Kleos as a cautionary tale; cheap plausibility checks and their failure
  modes; operational uses; legal note.
- **Ch. 30** — multi-receiver networks as a by-product geolocation sensor;
  timestamp precision requirements for shore networks.
- **Ch. 39** — Doppler as both a decollision aid and a geolocation signal.
- **Ch. 47** — how to flag and quarantine spoofed segments using geolocation
  evidence when available.
- **Ch. 59** — geolocation as the strongest detection control; Elba 2019
  (Androjna 2021) and fisheries (Kruger 2019) cases.
- **Ch. 62** — TDOA localisation of GNSS jammers (Gattis 2026) as the same
  toolkit.
- **Ch. 66** — RF geolocation providers as an alternative ship-tracking source.
- **Ch. 68** — SART/MOB homing: position-first, DF as fall-back.
- **Ch. 19** — privacy of large-scale emitter geolocation.
