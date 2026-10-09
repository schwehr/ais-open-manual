# Dossier: Interfaces and logging — NMEA 0183 AIS sentences, TAG blocks, IEC 61162-450, NMEA 2000 PGNs, and logging formats in the wild

**Purpose.** This dossier records what could be confirmed, as of 5 October 2026,
about how AIS data leaves a transponder or receiver and how it is logged: the
`!AIVDM`/`!AIVDO` sentence anatomy and 6-bit "armoring", talker IDs, the other
AIS sentence formatters, NMEA 4.10 TAG blocks and their checksum, the
IEC 61162-450 Ethernet ("LWE") wrapper and the 61162-460 security add-on, the
NMEA 2000 AIS PGNs (via the reverse-engineered canboat database), and the file
and stream formats used by USCG NAIS/Marine Cadastre, the Danish Maritime
Authority, Kystverket, Finnish Digitraffic, gpsd, AIS-catcher, and Global Fishing
Watch. It feeds **Chapter 26** (Interfaces and logging) as its primary target,
plus **Chapter 22** (where NMEA payload meets message bits), **Chapter 41**
(providers and open feeds), **Chapter 42** (home receiver logging), **Chapter 44**
(decoder behaviours: padding, multi-fragment reassembly), **Chapter 47**
(timestamp reconciliation and data cleaning), **Chapter 50** (ingest
architecture), **Chapter 56** (VDR/forensic alignment of logs), **Chapter 60**
(malformed-input robustness), and **Appendix D** (talker IDs, PGN table).

> Research-session note. Facts marked *high* were read in this session from the
> gpsd `AIVDM.adoc` (v1.58, 24 June 2023) and `NMEA.adoc` (12 July 2025)
> sources, nmea.org, the IEC webstore abstracts, canboat v8.3.0 YAML files, the
> Marine Cadastre data dictionary PDF, the DMA README (via Wayback), Kystverket
> and Digitraffic pages, the AIS-catcher documentation, and the Fraunhofer FKIE
> IEC 61162-450 Wireshark dissector. The NMEA 0183, NMEA 2000 and IEC 61162 texts
> themselves are paid and were **not** read; anything attributed to them is via a
> secondary source and marked. A fuller working file with verbatim quotes is in
> the session scratch (`interfaces_research.md`).

## Key questions

1. What exactly is in an `!AIVDM`/`!AIVDO` sentence, field by field, and what
   do the talker IDs mean?
2. How does 6-bit armoring work, and what are the classic decoder bugs (fill
   bits, over-length payloads, multi-fragment reassembly)?
3. What other AIS sentences exist on the presentation interface (ABM, BBM, ABK,
   ACA, ACS, AIR, LRF/LRI/LR1-3, SSD, VSD, TXT, ALR, VER, AIQ) and which standard
   defines them?
4. What is a TAG block, what are its keys, how is its checksum computed, and in
   what unit is `c:`?
5. How does IEC 61162-450 wrap sentences on Ethernet (`UdPbC\0`, multicast
   groups, SFI in `s:`), and what does 61162-460 add?
6. Which NMEA 2000 PGNs carry AIS, with which fields, and under what licence?
7. What do real logs look like: NAIS "extended AIVDM", Marine Cadastre CSV,
   DMA CSV, Kystverket/Digitraffic streams, gpsd JSON, AIS-catcher JSON, GFW
   tag-blocked NMEA — and what is lost in each?
8. What are the best practices (UTC receiver time, receiver id, keep raw,
   keep both timestamps)?

## Primary sources located

| Source | Identifier / edition / year | URL | What it covers | Access |
|---|---|---|---|---|
| gpsd, *AIVDM/AIVDO protocol decoding* (E. S. Raymond; contributors incl. K. Schwehr) | v1.58, 24 June 2023 | https://gpsd.gitlab.io/gpsd/AIVDM.html (source: https://gitlab.com/gpsd/gpsd/-/raw/master/www/AIVDM.adoc) | Sentence layer, armoring table, talker IDs, padding pitfalls, TAG blocks, USCG extended AIVDM, JSON member names | Free |
| gpsd, *NMEA Revealed* | 12 July 2025 | https://gitlab.com/gpsd/gpsd/-/raw/master/www/NMEA.adoc | Checksum rule, 82-byte limit, NMEA version timeline, talker list | Free |
| gpsd, *gpsd_json* manual | current | https://gpsd.gitlab.io/gpsd/gpsd_json.html (source: https://gitlab.com/gpsd/gpsd/-/raw/master/man/gpsd_json.adoc) | `class:"AIS"` JSON output, scaling rules | Free |
| NMEA, *NMEA 0183* product page | v4.30 (Dec 2023) replaces v4.11 (2018) | https://www.nmea.org/nmea-0183.html | Edition, pricing, 0183-HS appendix | Free page; standard paid |
| NMEA, *NMEA 2000* and *OneNet* pages | NMEA 2000 v3.000; OneNet (IPv6) | https://www.nmea.org/nmea-2000.html ; https://www.nmea.org/nmea-onenet.html | Licensing, Appendix A&B PGNs, coexistence with 61162-450 | Free page; standards paid |
| IEC 61162-450:2024 | Ed. 3.0, published 2024-04-04 | https://webstore.iec.ch/en/publication/72731 | Scope abstract (shipboard Ethernet data transfer) | Paid (abstract free) |
| IEC 61162-460:2024 | Ed. 3.0, 2024-04-04 | https://webstore.iec.ch/en/publication/72732 | Security/safety add-on to -450 | Paid (abstract free) |
| IEC 61162-1:2024 | Ed. 6.0, 2024-04-04 | https://webstore.iec.ch/en/publication/72729 | Single talker/multiple listeners; "11 to a maximum of 79 characters" | Paid (abstract free) |
| canboat (open-source NMEA 2000 toolkit) | v8.3.0; Apache-2.0 | https://github.com/canboat/canboat (PGN YAMLs under `database/pgns/`; https://canboat.github.io/canboat/canboat.html) | Reverse-engineered PGN names and field lists | Free |
| Fraunhofer FKIE *maritime-dissector* (Wireshark) | repo | https://github.com/fkie-cad/maritime-dissector | `UdPbC\0` framing, TAG block parsing, 80-byte tag length check, checksum code | Free |
| NOAA/BOEM Marine Cadastre AIS data dictionary | "Updated: July 31, 2026" | https://coast.noaa.gov/data/marinecadastre/ais/data-dictionary.pdf ; https://github.com/ocm-marinecadastre/ais-vessel-traffic | CSV columns 2018–2024 and 2025+ | Free |
| Danish Maritime Authority, AIS data page and `!_README_information_CSV_files.txt` | README dated 2023-09-26 | https://www.dma.dk/safety-at-sea/navigational-information/ais-data ; http://web.ais.dk/aisdata/ (read via Wayback 2025-07-21; live host had an expired TLS cert) | 26-column CSV | Free |
| Kystverket (Norwegian Coastal Administration), *Access to AIS data* | page read 2026-10-05 | https://www.kystverket.no/en/sea-transport-and-ports/ais/access-to-ais-data/ | Open TCP feed 153.44.253.27:5631, IEC 62320-1 format, exclusions | Free |
| Fintraffic Digitraffic Marine | OpenAPI "tag: 2026.9.21-1" | https://www.digitraffic.fi/en/marine-traffic/ ; https://meri.digitraffic.fi/swagger/openapi.json | MQTT over WSS topics, JSON schemas, REST endpoints | Free |
| AIS-catcher documentation (jvde-github) | docs site read 2026-10-05 | https://docs.aiscatcher.org/ | Output modes, JSON fields, `-M T`, tag-block output, sentinel omission | Free |
| Global Fishing Watch `ais-tools` | README | https://github.com/GlobalFishingWatch/ais-tools | Tag block with ms `c:` and `T:`; libais-based decoding | Free |

## Verified facts

### NMEA 0183 `!AIVDM` / `!AIVDO`

| Fact | Source | Confidence |
|---|---|---|
| `!AIVDM` = reports received from other stations; `!AIVDO` = own-ship data | gpsd AIVDM §Introduction | high |
| Fields: (1) formatter `!AIVDM`; (2) fragment count; (3) fragment number, one-based; (4) sequential message id for multi-sentence messages (empty for single); (5) channel `A`/`B` (also `1`/`2` seen in the wild, not defined by the standards); (6) armored payload; (7) fill bits 0–5; `*hh` checksum. Example `!AIVDM,1,1,,B,177KQJ5000G?tO`K>RA1wUbN0TKH,0*5C` | gpsd AIVDM §Sentence Layer | high |
| "AIS Channel A is 161.975Mhz (87B); AIS Channel B is 162.025Mhz (88B)" | gpsd AIVDM §Sentence Layer | high |
| Checksum: 8-bit XOR of all characters between the leading `!`/`$` and the `*`, two hex digits, MS nibble first | gpsd NMEA.adoc §NMEA encoding conventions; AIVDM §Sentence Layer | high |
| Maximum sentence length 82 bytes including `$`/`!` and CR LF (IEC 61162-1 abstract: "from about 11 to a maximum of 79 characters" between delimiter and CR LF) | gpsd NMEA.adoc; IEC webstore 72729 abstract | high |
| Payload split into fragments because of the 82-char limit; two-fragment Message 5 example `!AIVDM,2,1,3,B,55P5TL01VIaAL@7WKO@mBplU@<PDhh000000001S;AJ::4A80?4i@E53,0*3E` / `!AIVDM,2,2,3,B,1@0000000000000,2*55` | gpsd AIVDM §Sentence Layer | high |
| `!`-led sentences are generic encapsulation; fields 1–4, fill bits and checksum are fixed, payload may be anything | gpsd AIVDM §Sentence Layer | high |
| 6-bit armoring: ASCII value − 48; if result > 40 subtract 8. Valid characters `0`–`W` (48–87 → 0–39) and `` ` ``–`w` (96–119 → 40–63); `X`–`_` (88–95) unused. (gpsd's prose "begin with "0" (64) and end with "w" (87)" is a documentation slip; its table is correct) | gpsd AIVDM §Payload Armoring table | high |
| Most common wild error: pad reported 2 bits too small (Message 5 decodes as 426 bits not 424); gpsd recommends accepting payloads up to 5 bits over the theoretical length | gpsd AIVDM §Interaction with AIVDM padding | high |
| Format origin: "seems to have been set by IEC-PAS 61162-100" and harmonized with NMEA 0183 | gpsd AIVDM §Standards | medium (gpsd hedges) |
| NMEA version timeline: 4.00 Nov 2008; 4.10 July 2012; 4.11 Nov 2018 | gpsd NMEA.adoc version table | high (gpsd's table) |
| NMEA 0183 v4.30 published December 2023, "replaces Version 4.11 (2018 Release)"; NMEA 0183-HS (38.4 kbaud) is an appendix of 4.30; standard is copyrighted and sold only by NMEA (member US$1,150 … consumer-electronics US$10,000 tiers) | https://www.nmea.org/nmea-0183.html | high |

### Talker IDs (as listed by gpsd; canonical list is NMEA's "Talker Identifier Mnemonics" PDF — not fetched (verify))

| Talker | Meaning (gpsd AIVDM Table 1) | Confidence |
|---|---|---|
| AI | Mobile AIS station | high |
| AB | NMEA 4.0 base AIS station | high |
| AD | NMEA 4.0 dependent AIS base station | high |
| AN | NMEA 4.0 aid-to-navigation AIS station | high |
| AR | NMEA 4.0 AIS receiving station | high |
| AS | NMEA 4.0 limited base station | high (gpsd) / (verify) vs NMEA PDF |
| AT | NMEA 4.0 AIS transmitting station | high |
| AX | NMEA 4.0 repeater AIS station | high |
| BS | base AIS station (deprecated in NMEA 4.0) | high |
| SA | NMEA 4.0 physical shore AIS station | high |

### Other AIS sentence formatters

| Fact | Source | Confidence |
|---|---|---|
| The presentation-interface sentences commonly expanded as ABK (addressed and binary broadcast acknowledgement), ABM (addressed binary and safety-related message), ACA (AIS regional channel assignment), ACS (channel management information source), AIR (interrogation request), AIQ (query), BBM (broadcast binary message), LRF/LRI/LR1/LR2/LR3 (long-range function/interrogation/replies), SSD (ship static data), VSD (voyage static data), TXT (text transmission), ALR (set alarm state), VER (version) are defined in NMEA 0183 / IEC 61162-1 — **no free primary text listing their fields was reached in this session** | search only; Furuno FA-170 manual PDF link gated | low — mark every field layout (verify) until read from IEC 61162-1 Ed. 6 or a Class A manual |
| IEC 61162-1:2024 abstract: "For applications to shore based equipment of the automatic identification system (AIS) the IEC 62320 series applies" | IEC webstore 72729 | high |

### TAG blocks (NMEA 4.10)

| Fact | Source | Confidence |
|---|---|---|
| "Beginning with NMEA 4.10, the standard describes a way to intersperse 'tag blocks' with AIS sentences" | gpsd AIVDM §NMEA Tag Blocks | high |
| Format: opening `\`, comma-separated `key:value` fields (no backslashes), `*hh` checksum, closing `\`. Example `\g:1-2-73874,n:157036,s:r003669945,c:1241544035*4A\!AIVDM,1,1,,B,15N4cJ`005Jrek0H@9n`DW5608EP,0*13` | gpsd AIVDM §NMEA Tag Blocks | high |
| Checksum = XOR of the characters between the backslashes excluding `*hh`. Numerically verified this session: XOR of `g:1-2-73874,n:157036,s:r003669945,c:1241544035` = 0x4A; GFW example `\c:1599239526500,s:sdr-experiments,T:2020-09-04 18.12.06*5D\` = 0x5D; FKIE dissector computes the same way | own computation; FKIE `iec450.lua` | high |
| Keys (NMEA 4.10 / IEC 62320-1): `c` UNIX time "in seconds or milliseconds"; `d` destination (≤ 15 chars); `g` grouping `sentence-total-groupid`; `n` line count; `r` relative time; `s` source/station; `t` text (≤ 15 chars). IEC 62320-1 uses the same block format with an overlapping key set (`xGy`, `x`, `i`) | gpsd AIVDM table "NMEA 4.00 Field Types" | high |
| Without `g`, a tag block applies only to the next sentence | gpsd AIVDM | high |
| gpsd: "We're not yet sure what the time unit is" for `c`; "As of May 2014 no NMEA 4.10 relative time fields have been observed in the wild"; NMEA 4.10 has a configuration facility that can set time units and epoch (paid text) | gpsd AIVDM | high (that gpsd says so) |
| In practice `c:` is **milliseconds** in GFW tooling (`\c:1577762601537,s:my-station,T:2019-12-30 22.23.21*5D\…`) and **seconds** in the gpsd/NAIS example (`c:1241544035`) — consumers must sniff the magnitude | GFW ais-tools README; gpsd example | high |
| GFW writes multipart tag-blocked sentences on one line: `\tagblock\!AIVDM_part_one\tagblock\!AIVDM_part_two` | GFW ais-tools README | high |
| FKIE dissector flags tag blocks longer than 80 bytes ("allowed: 80 Byte") | FKIE `iec61162450nmea.lua` | medium (dissector's model; (verify) against the standard) |
| AIS-catcher can output NMEA with tag blocks (`msgformat NMEA_TAG` = `-o 7`); `-M T` adds receive timestamps | https://docs.aiscatcher.org/ console/output pages | medium (table flattened by HTML→text) |

### IEC 61162-450 / -460 (Ethernet)

| Fact | Source | Confidence |
|---|---|---|
| IEC 61162-450:2024, Ed. 3.0, published 2024-04-04; "specifies interface requirements and methods of test for high speed communication between shipboard navigation and radiocommunication equipment … on a shipboard Ethernet network" | IEC webstore 72731 | high |
| IEC 61162-460:2024, Ed. 3.0, 2024-04-04: "an add-on to IEC 61162-450 where higher safety and security standards are needed … does not introduce new application level protocol requirements" ; includes redundant-network requirements | IEC webstore 72732 | high |
| IEC 61162-1:2024 Ed. 6.0 and 61162-2:2024 published the same day | IEC webstore 72729/72730 | high |
| Earlier editions: 61162-450 Ed. 1.0 2011, Ed. 2.0 2018 | web summaries only | low (verify) |
| Datagram framing: 6-byte header token `UdPbC` + NUL, then TAG block(s) + sentence; binary file-transfer tokens `RrUdP`/`RaUdP`/`RpUdP` | FKIE dissector README and Lua | high (for the dissector's model) |
| UDP multicast transmission groups; commonly cited table MISC 239.192.0.1:60001, TGTD 239.192.0.2:60002 (targets incl. AIS), SATD 239.192.0.3:60003, NAVD 239.192.0.4:60004, …; `s:` carries the SFI (system function id), `n:` the line count | vendor-manual search summaries (JRC/Furuno/Brommeland) | medium — (verify) exact table against a readable installation manual or the standard |
| OneNet (NMEA) is IPv6 over IEEE 802.3 and "coexist[s] with … IEC 61162-450" on the same network | https://www.nmea.org/nmea-onenet.html | high |

### NMEA 2000 AIS PGNs (canboat v8.3.0 descriptions)

| PGN | canboat description | Confidence |
|---|---|---|
| 129038 | AIS Class A Position Report (Fast, priority 4, minLength 27) | high |
| 129039 | AIS Class B Position Report (Fast, 4, 26) | high |
| 129040 | AIS Class B Extended Position Report | high |
| 129041 | AIS Aids to Navigation (AtoN) Report | high |
| 129792 | AIS DGNSS Broadcast Binary Message | high |
| 129793 | AIS UTC and Date Report | high |
| 129794 | AIS Class A Static and Voyage Related Data (Fast, 6, 75) | high |
| 129795 | AIS Addressed Binary Message | high |
| 129796 | AIS Acknowledge | high |
| 129797 | AIS Binary Broadcast Message | high |
| 129798 | AIS SAR Aircraft Position Report | high |
| 129799 | Radio Frequency/Mode/Power | high |
| 129800 | AIS UTC/Date Inquiry | high |
| 129801 | AIS Addressed Safety Related Message | high |
| 129802 | AIS Safety Related Broadcast Message | high |
| 129803 | AIS Interrogation | high |
| 129804 | AIS Assignment Mode Command | high |
| 129805 | AIS Data Link Management Message | high |
| 129806 | AIS Channel Management | high |
| 129807 | AIS Class B Group Assignment | high |
| 129809 / 129810 | AIS Class B static data (msg 24 Part A / Part B) | high |
| 129811 / 129812 | AIS Single/Multi Slot Binary Message (Deprecated) | high |
| 129813 | AIS Long-Range Broadcast Message | high |
| 129814 / 129815 | AIS Single / Multi Slot Binary Message | high |
| 129816 | AIS Acknowledge (Binary) | high |
| (129808 is DSC, not AIS) | canboat file list | high |

Field lists (canboat YAML, names in order):

- **129038**: Message ID · Repeat Indicator · User ID (MMSI) · Longitude · Latitude · Position Accuracy · RAIM · Time Stamp · COG · SOG · Communication State (19 b) · AIS Transceiver information (5 b) · Heading · Rate of Turn · Nav Status · Special Maneuver Indicator · Reserved (2) · Spare (3) · Reserved (5) · Sequence ID. canboat note: a Garmin AIS 800 was reported omitting the trailing Sequence ID (canboat PR #848). (high)
- **129039**: … Communication State · AIS Transceiver information · Heading · Regional Application (8) · Regional Application B (2) · Unit type · Integrated Display · DSC · Band · Can handle Msg 22 · AIS mode · AIS communication state · Reserved (7) · Sequence ID. (high)
- **129794**: Message ID · Repeat · User ID · IMO number · Callsign (56 b) · Name (160 b) · Type of ship · Length · Beam · Position reference from Starboard · Position reference from Bow · ETA Date · ETA Time · Draft · Destination (160 b) · AIS version indicator · GNSS type (4 b) · DTE · Reserved · AIS Transceiver information · Reserved · Sequence ID. (high)
- **129809**: Message ID · Repeat · User ID · Name · AIS Transceiver information · Reserved · Sequence ID. (high)
- **129810**: Message ID · Repeat · User ID · Type of ship · Vendor ID (56 b) · Callsign · Length · Beam · Pos. ref. Starboard · Pos. ref. Bow · Mothership User ID · Reserved · Spare · GNSS type · AIS Transceiver information · Reserved · Sequence ID. (high)

| Licensing fact | Source | Confidence |
|---|---|---|
| "The NMEA 2000 database and implementation is copyrighted by the NMEA … Access is restricted to members and parties that pay for it … For this reason we have reverse engineered the NMEA 2000 database by network observation and assembling data from public sources." | canboat README | high |
| NMEA 2000 v3.000; PGNs in "Appendix A&B"; not sold via an online store; AIS & DSC among the PGN areas | https://www.nmea.org/nmea-2000.html | high |

### Logging formats in the wild

| Fact | Source | Confidence |
|---|---|---|
| **USCG "extended AIVDM"**: extra comma fields after the checksum, e.g. `!AIVDM,1,1,,B,15Cjtd0Oj;Jp7ilG7=UkKBoB0<06,0*63,s1234,d-119,T12.34567123,r003669958,1085889680` — `s` RSSI (0–65535), `d` dBm, `T` time of arrival in seconds from the UTC minute, `S` slot number (e.g. `S0042`), `r` station id (sometimes `b` for base), last field = C `time()` epoch seconds (always present). gpsd: "a semi-obsolescent logging format used by the USCG, which has never documented it well and plans to replace it with a new one based on NMEA 4.0" | gpsd AIVDM §U.S. Coast Guard Extended AIVDM | high |
| NAIS-style tag block uses `s:r003669945` (an `r`-prefixed station id) — the NMEA 4.10 replacement for the trailing-field format | gpsd example (inference) | medium |
| Marine Cadastre: data "originates from the U.S. Coast Guard's Nationwide Automatic Identification System"; AccessAIS orders ≈ 2 GB zipped CSV; bulk files 2009+; older geodatabase, newer CSV; experimental GeoParquet 2024/2025 | Marine Cadastre GitHub README | high |
| **Marine Cadastre CSV 2018–2024** columns: MMSI, BaseDateTime (UTC, `2017-02-01T20:05:07`), LAT, LON, SOG, COG, Heading, VesselName, IMO (`IMO9627980`), CallSign, VesselType, Status, Length, Width, Draft, Cargo, TransceiverClass (from 2018) | data-dictionary PDF | high |
| **Marine Cadastre 2025+** columns (lower-case): mmsi, base_date_time, longitude, latitude, sog (0–99.9), cog (0–359.9), heading (0–359), vessel_name, imo, call_sign, vessel_type, status, length (1–509 m), width (1–61), draft (1–24), cargo, transceiver (A|B) | data-dictionary PDF | high |
| **DMA CSV** (26 columns, README 2023-09-26): Timestamp ("from the AIS basestation", `31/12/2015 23:59:59`), Type of mobile, MMSI, Latitude (decimal comma, e.g. `57,8794`), Longitude, Navigational status (text), ROT, SOG, COG, Heading, IMO, Callsign, Name, Ship type, Cargo type, Width, Length, Type of position fixing device, Draught, Destination, ETA, Data source type, Size A (GPS→bow), Size B (→stern), Size C (→starboard), Size D (→port); daily `aisdk-YYYY-MM-DD.zip` | DMA README via Wayback; dma.dk page | high |
| **Kystverket** open feed: "153.44.253.27 port 5631"; "The AIS data stream is in standard IEC format IEC 62320-1"; excludes fishing vessels < 15 m and pleasure craft < 45 m; covers Norwegian EEZ + Svalbard/Jan Mayen zones | kystverket.no (EN and NO pages) | high |
| **Digitraffic**: MQTT over WebSockets `wss://meri.digitraffic.fi:443/mqtt`; topics `vessels-v2/<mmsi>/metadata`, `vessels-v2/<mmsi>/location`, `vessels-v2/status`; location JSON `{"time":1668075025,"sog":10.7,"cog":326.6,"navStat":0,"rot":0,"posAcc":true,"raim":false,"heading":325,"lon":20.345818,"lat":60.03802}`; metadata timestamp in ms vs location in s; REST `/api/ais/v1/vessels`, `/api/ais/v1/locations` with sentinels documented (sog 102.3, cog 360, heading 511, rot −128) and `timestampExternal` in ms | digitraffic.fi; openapi.json | high |
| **gpsd JSON**: objects with `"class":"AIS"`, `type`, `scaled`, `device`; lat/lon in decimal degrees, speed in knots, turn may be `nan`/`fastright`/`fastleft`, draught in metres; controlled-vocabulary fields dumped twice (`status` and `status_text`, protocol ≥ 3.9); Message 4 → `timestamp` ISO 8601; Message 5 → `eta` `MM-DDTHH:MMZ`; type 1–3 members: type, repeat, mmsi, status, turn, speed, accuracy, lon, lat, course, heading, second, maneuver, raim, radio | gpsd_json.adoc; AIVDM.adoc tables | high |
| **AIS-catcher**: `-o 0` none, `-o 1` plain NMEA, `-o 2` NMEA + metadata (default), `-o 3` JSON_NMEA, `-o 5` JSON_FULL ("largely compatible with gpsdecode"), `-o 7` NMEA_TAG; `-M D` signal power/ppm, `-M T` timestamps, `-M M` country from MMSI; `rxtime` `YYYYMMDDHHMMSS`; "not available" sentinels are **omitted** from JSON (181°/91°, 102.3 kn, 360°, 511, second 60, …) except `turn_unscaled` and the type-5 `eta` string; `-u host port` UDP (10110/10111 conventional) and `-P` TCP client | https://docs.aiscatcher.org/ | high |
| **GFW ais-tools**: Apache-2.0; "Uses https://github.com/schwehr/libais as the base decoder"; adds tag blocks with ms `c:`, `s:` station, non-standard `T:` human time; joins multipart | GFW README | high |
| GFW raw-message BigQuery schema: not public; **not confirmed** | — | low (verify) |
| Spire / ORBCOMM / exactEarth delivery formats: behind login; not confirmed (Spire Maritime 2.0 GraphQL per search summaries) | — | low (verify) |

## Notes and quotes

- gpsd on the sentence layer: "The payload size of each sentence is limited by
  NMEA 0183's 82-character maximum, so it is sometimes required to split a
  payload over several fragment sentences."
- gpsd on padding: "The most common error observed in the wild on AISHub is
  reporting a pad 2 bits too small … Type 5 messages, which then decode as 426
  bits rather than 424. Accordingly, we recommend that … decoders should accept
  messages that are up to 5 bits over their theoretically correct length."
- gpsd on the USCG legacy format: "a semi-obsolescent logging format used by the
  USCG, which has never documented it well and plans to replace it with a new one
  based on NMEA 4.0." The `T` field ("time of arrival in seconds from UTC 0",
  i.e. seconds into the current minute) plus `S` slot number are the only
  publicly described way NAIS logs exposed slot-level timing; these fields are
  gold for ch. 24/34 if an archive with them can be found (verify availability).
- canboat on provenance: "we have reverse engineered the NMEA 2000 database by
  network observation and assembling data from public sources." Field names and
  PGN titles in the book should therefore be labelled "per canboat", not "per
  NMEA".
- Digitraffic's own note: "the timestamp in the metadata message is in
  milliseconds while in the location message it is in seconds" — a textbook
  example of the units problem that the chapter must warn about for TAG block
  `c:` as well.
- Kystverket: "The AIS data stream is in standard IEC format IEC 62320-1" — i.e.
  a base-station-network presentation (TAG-blocked NMEA), not plain AIVDM.
- The DMA CSV uses a decimal **comma** in coordinates (README example `57,8794`)
  and a `DD/MM/YYYY HH:MM:SS` timestamp — two parsing traps for ch. 47.
- Marine Cadastre renamed and re-typed every column in 2025 (`BaseDateTime` →
  `base_date_time`, `TransceiverClass` → `transceiver`, Length/Width to
  integers) — pipelines spanning 2024/2025 must map both dictionaries.
- Three timestamps can coexist for one message: EPFS second (message time stamp
  field), receiver/base-station time (`c:` or trailing epoch), and provider
  ingest time (`timestampExternal`, `rxuxtime`). Only the second is in the
  message; the others depend on the receiver clock discipline (→ ch. 24/47).

## Open questions / (verify)

- (verify) Field layouts of ABM/BBM/ABK/ACA/ACS/AIR/AIQ/LRF/LRI/LR1-3/SSD/VSD/
  TXT/ALR/VER from IEC 61162-1 Ed. 6 (2024) or a Class A installation manual
  (Furuno FA-170 OME44900M was gated; try JRC JHS-183 or Saab R5 manuals).
- (verify) Normative unit and epoch of TAG block `c:` in NMEA 0183 v4.10/4.30,
  and the "configuration message" that can change them.
- (verify) Maximum TAG block length (FKIE dissector assumes 80 bytes).
- (verify) IEC 61162-450 transmission-group table (multicast addresses/ports,
  mnemonics MISC/TGTD/SATD/NAVD/VDRD/RCOM/TIME/PROP/USRx/BAM/CAM/NETA), whether
  `d:`/`g:` are mandatory, and the edition history (Ed. 1 2011? Ed. 2 2018?).
- (verify) Whether NMEA's current Talker Identifier PDF still lists `AS` and
  `SA` as gpsd describes (https://www.nmea.org/Assets/NMEA%200183%20Talker%20Identifier%20Mnemonics.pdf).
- (verify) Whether any public NAIS archive still carries the extended-AIVDM
  trailing fields (`T`, `S`, `r`) — needed for slot-timing figures.
- (verify) GFW public raw-message schema (if any) and Spire/ORBCOMM delivery
  formats; otherwise cite only ais-tools and the aggregated public datasets.
- (verify) Official NMEA titles of the AIS PGNs vs canboat's descriptions;
  completeness flags for the less-tested PGNs (129040/129041/129798/129813–816).
- (verify) IEC 62320-1 TAG block key set (`xGy`, `x`, `i`) — only via gpsd here.

## Candidate figures and worked examples

1. **Figure 26-1 — Anatomy of an `!AIVDM` sentence.** Colour-coded fields of
   `!AIVDM,1,1,,B,177KQJ5000G?tO`K>RA1wUbN0TKH,0*5C` with the checksum XOR
   shown step-by-step for the first few characters.
2. **Figure 26-2 — Armoring table.** The 64 characters with ASCII codes, the
   gap `X`–`_`, and the "−48, −8 if > 40" rule; show `w` → 63 and `W` → 39.
3. **Worked example — fill bits.** Message 5 (424 bits) → 71 characters = 426
   bits → fill = 2; show how a wrong fill of 0 yields the 426-bit symptom gpsd
   describes.
4. **Figure 26-3 — TAG block anatomy.** `\g:1-2-73874,n:157036,s:r003669945,c:1241544035*4A\` with the XOR computed to 0x4A; a second panel with GFW's ms-`c:` and `T:`.
5. **Worked example — two-fragment reassembly** keyed on (talker, channel,
   sequential id) and the failure modes when a multiplexer interleaves two
   receivers' fragments (ch. 36/44).
6. **Figure 26-4 — Three clocks.** EPFS second vs receiver `c:` vs provider
   ingest time on one Digitraffic message (`time` in s, metadata in ms).
7. **Figure 26-5 — 61162-450 datagram.** `UdPbC\0` + `\s:AI0001,n:123*hh\` +
   `!AIVDM…` inside a UDP multicast frame; mark the SFI and the (verify)
   group table.
8. **Table 26-A — Logging formats compared.** Columns: format, raw bits kept?,
   receiver id?, receiver time?, EPFS second kept?, slot/RSSI?, decimal
   separator, timestamp syntax — rows: USCG extended AIVDM, NMEA 4.10 TAG,
   Marine Cadastre CSV (2018–24 / 2025+), DMA CSV, Digitraffic JSON, gpsd JSON,
   AIS-catcher JSON_FULL, GFW tag-blocked NMEA.
9. **Table 26-B — NMEA 2000 AIS PGNs** (from the canboat list above) for
   Appendix D.
10. **Try it** — `tagblock.py` (already in `code/decode/`) validating the two
    checksums above; `gpsdecode` vs AIS-catcher `-o 5` on the same sentence to
    show sentinel omission vs explicit `nan`.

## Recommended use by chapter

- **Ch. 22:** armoring table and fill-bit arithmetic as the bridge from NMEA to
  bit fields; gpsd's "accept up to 5 bits over" rule.
- **Ch. 26 (primary):** all sections; lead with Figures 26-1/26-3; state plainly
  which standards are paid and which facts come from gpsd/canboat/vendors.
- **Ch. 36 / 44:** padding bug, fragment-reassembly hazards, Garmin AIS 800
  missing Sequence ID (canboat PR #848) as concrete interoperability cases.
- **Ch. 41:** Kystverket TCP feed, Digitraffic MQTT/REST, DMA daily zips,
  Marine Cadastre/AccessAIS — with their exclusions and formats.
- **Ch. 42:** AIS-catcher output modes, UDP 10110/10111 to OpenCPN, `-M T`
  timestamps, NMEA_TAG logging.
- **Ch. 47:** three-timestamp reconciliation; DMA decimal comma; Marine
  Cadastre 2025 schema change; Digitraffic ms-vs-s.
- **Ch. 50:** TAG block `s:`/`c:` as the minimal provenance envelope; keep raw
  NMEA alongside parsed Parquet.
- **Ch. 56:** USCG extended AIVDM `T`/`S` fields as slot-level forensic data if
  available.
- **Ch. 60:** malformed input classes to fuzz: bad fill, over-length payload,
  tag-block checksum mismatch, unterminated fragments.
- **Appendix D:** talker-ID table; PGN table (labelled "per canboat").
