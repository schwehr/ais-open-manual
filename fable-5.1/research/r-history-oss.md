# Dossier: Open-source AIS software — repository archaeology

**Purpose.** This dossier records what the original repositories, package
registries and project documents actually say about the origin, authorship,
licence, release cadence and status of the open-source AIS decoders, encoders
and SDR receivers named in [PLAN.md](../PLAN.md). It is the evidence base for
**Chapter 44** (open-source decoding/encoding software: a history) and feeds
**Chapter 11** (growth 2004–2015: "open-source decoders (aisparser, noaadata,
gpsd, libais 2010 ⟨H⟩)"), **Chapter 12** (2015–present), **Chapter 22**
(message catalog: gpsd AIVDM document and shared test vectors), **Chapter 23**
(ASM: `ais-areanotice-py` as reference implementation), **Chapter 33**
(SDR receive/transmit software), **Chapter 60** (receiver robustness; which
parsers exist to be attacked), **Appendix A** (timeline) and **Appendix E**
(software catalog). Dates below were taken by cloning each repository on
2026-10-04 and reading `git log --reverse`; registry dates come from the PyPI,
crates.io and npm JSON APIs read the same day. "First commit" means the oldest
commit in the current public history, which for several projects is an import
from an earlier Subversion repository and therefore *later* than the project's
true start; where an earlier start is documented (changelogs, copyright
headers) it is recorded separately.

## Key questions

1. For each named project: who started it, when (first commit vs. documented
   earlier start), in what language, under which licence, with what release
   cadence, and is it maintained as of October 2026?
2. Which projects derive from which (code lineage: AISDecoder → rtl-ais;
   noaadata → libais; BitVector → noaadata/bitvector-modern; gpsd AIVDM doc →
   most later decoders)?
3. When did gpsd gain AIVDM support (`driver_aivdm.c`) and how has the
   "AIVDM/AIVDO protocol decoding" document evolved?
4. What was written *because of* a specific event (libais and the Deepwater
   Horizon spill; the Trend Micro "AIS BlackToolkit" and the 2013/2014 security
   research)?
5. Which projects are actually "open source" by licence, and which are
   source-available but non-commercial (AISmessages) or unlicensed (gr-ais has
   per-file GPL headers but no top-level LICENSE; trendmicro/ais has none at
   the top level)?
6. What is the state of the Rust, Go, Node, .NET and Perl ecosystems?
7. What shared test corpora exist (gpsd regression files, libais/pyais tests)
   that Chapter 44's comparison table can use?

## Primary sources located

| Source | Identifier / edition / year | URL | What it covers | Access |
|---|---|---|---|---|
| gpsd git repository | gitlab.com/gpsd/gpsd, cloned 2026-10-04 | https://gitlab.com/gpsd/gpsd | `driver_aivdm.c`, `www/AIVDM.adoc`, `NEWS`, release tags | free |
| gpsd "AIVDM/AIVDO protocol decoding" | E. S. Raymond, v1.58, 24 June 2023 (file header in HEAD) | https://gpsd.gitlab.io/gpsd/AIVDM.html | De-facto public description of AIS payloads; change history; credits | free |
| gpsd `NEWS` | entries 2.39 (2009-03-18) and 2.90 (2009-12-04) | in repository | When AIS shipped in a release | free |
| schwehr/libais | GitHub, first commit 2010-04-28 (svn import) | https://github.com/schwehr/libais | C++/Python decoder; LICENSE (Apache-2.0) | free |
| libais on PyPI | first upload 2012-04-30 (0.7); last 0.17, 2018-01-17 | https://pypi.org/pypi/libais/json | release history | free |
| schwehr/noaadata | GitHub, first git commit 2010-09-09 "copied from 0.44 in svn"; `ChangeLog.html` back to 0.3 (2006-12-12) | https://github.com/schwehr/noaadata | Pure-Python research decoder/encoder; changelog is the primary source for 2006–2010 and for the libais/DWH link | free |
| schwehr/ais-areanotice-py | GitHub, first commit 2009-06-02 (svn) | https://github.com/schwehr/ais-areanotice-py | IMO SN.1/Circ.289 reference implementation | free |
| schwehr/bitvector-modern | GitHub, first commit 2015-03-30 ("Version 3.3.2") | https://github.com/schwehr/bitvector-modern | Fork of Avi Kak's BitVector; PSF licence | free |
| BitVector on PyPI | Avi Kak; 3.5.0 | https://pypi.org/pypi/BitVector/json | upstream of bitvector-modern | free |
| bcl/aisparser | GitHub, import 2010-12-27; headers "Copyright 2006-2008" | https://github.com/bcl/aisparser | Brian C. Lane's AIS Parser SDK (C, Java, Python bindings); BSD-style LICENSE | free |
| M0r13n/pyais | GitHub, first commit 2019-10-04 | https://github.com/M0r13n/pyais | Pure-Python decoder/encoder; MIT | free |
| pyais on PyPI | first upload 2019-11-14; 85 releases to 3.3.0 (2026-10-04) | https://pypi.org/pypi/pyais/json | release cadence | free |
| jvde-github/AIS-catcher | GitHub, first commit 2021-04-26 | https://github.com/jvde-github/AIS-catcher | SDR AIS receiver; GPL-3.0 | free |
| dgiardini/rtl-ais | GitHub repo created 2015-06-04; history contains Kyle Keen commits from 2013-12 | https://github.com/dgiardini/rtl-ais | RTL-SDR AIS receiver; LICENCE file credits AISDecoder (Astra Paging/AISHub, 2013) | free |
| rubund/gnuais | GitHub (2012) mirroring svn from 2008-09-22 | https://github.com/rubund/gnuais | Sound-card AIS demodulator/decoder; GPL-2 | free |
| bistromath/gr-ais | GitHub, first commit 2011-03-30 | https://github.com/bistromath/gr-ais | GNU Radio AIS receiver (Nick Foster); per-file GPLv3+ headers | free |
| trendmicro/ais | GitHub, first commit 2014-12-12 | https://github.com/trendmicro/ais | "AIS BlackToolkit": `gr-aistx`, `AIVDM_Encoder.py`, `AiS_TX.grc` | free |
| f4exb/sdrangel | GitHub; commit 1ac835260 (2021-05-07) | https://github.com/f4exb/sdrangel | AIS mod/demod/feature plugins; GPL-3.0 | free |
| dma-ais/AisLib | GitHub, first commit 2012-11-01 | https://github.com/dma-ais/AisLib | Danish Maritime Authority Java library; Apache-2.0 | free |
| ktuukkan/marine-api | GitHub (svn history from 2010-03-06); AIS added 2015-01-26 | https://github.com/ktuukkan/marine-api | Java NMEA 0183 library incl. AIS; LGPL-3.0 | free |
| tbsalling/aismessages | GitHub, first commit 2011-03-17 | https://github.com/tbsalling/aismessages | Java decoder; CC BY-NC-SA 4.0 (non-commercial) | free (source-available) |
| crates.io `ais` | created 2020-04-18; 0.12.0 | https://crates.io/api/v1/crates/ais | Rust AIS parser (squidpickles) | free |
| crates.io `nmea-parser` | created 2020-10-07; 0.11.0 | https://crates.io/api/v1/crates/nmea-parser | Rust NMEA 0183 + AIS parser (Timo Saarinen) | free |
| crates.io `nmea-kit` | created 2026-04-06; 0.8.9 | https://crates.io/api/v1/crates/nmea-kit | Newer bidirectional NMEA/AIS crate | free |
| BertoldVdb/go-ais | GitHub, first commit 2019-02-04 | https://github.com/BertoldVdb/go-ais | Go decoder/encoder; MIT | free |
| andmarios/aislib | GitHub, first commit 2015-01-31 | https://github.com/andmarios/aislib | Go decoder; GPL-3.0 | free |
| npm `ggencoder` | created 2014-11-06; 1.0.12 | https://registry.npmjs.org/ggencoder | GeoGate AIS/NMEA encoder/decoder (Fulup Ar Foll); Apache-2.0 | free |
| npm `ais-decoder` | created 2017-05-03; 1.3.5 | https://registry.npmjs.org/ais-decoder | Node AIS decoder; ISC | free |
| ais-dotnet/Ais.Net | GitHub created 2019-07-21 | https://github.com/ais-dotnet/Ais.Net | .NET decoder (endjin); AGPL-3.0 | free |
| OpenCPN/OpenCPN | GitHub; "Initial commit of OpenCPN Version 2.1.0" 2010-06-29 | https://github.com/OpenCPN/OpenCPN | Chartplotter with AIS decoding; GPL-2.0 | free |
| GitHub REST API | `/repos/{owner}/{repo}` read 2026-10-04 | https://api.github.com | `created_at`, licence detection, stars | free |

## Verified facts

Confidence: **high** = read directly from repository history, file contents or
registry API; **medium** = from project documentation or a single secondary
source; **low** = inferred.

### gpsd (C; BSD-style licence)

| Fact | Source | Confidence |
|---|---|---|
| First commit of `driver_aivdm.c`: `4996fc1c`, 2009-03-09, Eric S. Raymond, "The shell of an AIVDM driver." | `git log --follow -- driver_aivdm.c` in gitlab.com/gpsd/gpsd | high |
| Second commit 2009-03-10 `d43e0891` "Second stage of AIVDM decoding"; by 2009-03-12 (`80195adf`) "All AIVDM type 1-3 fields except latitude and turn rate now decode correctly." | same | high |
| First commit of the AIVDM document: `0ee03891`, 2009-03-10, "First cut at describing AIVDM." (as `www/AIVDM.txt`); messages 1–5 fully described by 2009-03-11 (`9916ecac`) | `git log --follow -- www/AIVDM.adoc` | high |
| `rtcmdecode` was renamed `gpsdecode` on 2009-03-13 (`daf596d2`) | `git log -- gpsdecode.c` | high |
| JSON output of AIVDM began 2009-06-05 (`15a5fd5d` "First cut at JSON dumping of AIVDM") | git log | high |
| `driver_aivdm.c` is present in tag `release-2.39` (2009-03-18) — i.e., AIS code shipped nine days after the first commit, though 2.39's NEWS entry does not mention AIS | `git ls-tree release-2.39`; NEWS | high |
| NEWS for 2.90 (2009-12-04): "GPSD-NG, the new JSON-based command protocol, is now deployed; as a consequence, AIS is now fully supported in both daemon and client." | NEWS | high |
| NEWS for 2.91 (2010-03-01): TCP/IP AIS feeds "such as AISHub" can be a data source; xgps rewritten in Python "now displays AIS information"; "Support for AIS message types 25 and 26." NEWS for 2.93 (2010-04-16): "Support for JSON dumping and parsing of AIS message types 25 and 26" | NEWS lines 538–552 and 512–513 | high |
| The document was renamed `.txt` → `.adoc` on 2018-11-19 by Gary E. Miller (`8127c8f9`) | git log | high |
| The document header in HEAD reads "v1.58, 24 June 2023"; author Eric S. Raymond; still edited in 2026 (last three commits 2026-03-27/28 by contributor "наб") | `www/AIVDM.adoc` | high |
| 337 commits touch the document (with `--follow`); by year: 2009: 93, 2010: 25, 2011: 102, 2012: 22, 2013: 35, 2014: 12, 2015: 11, 2016: 4, 2018: 1, 2019: 4, 2020: 3, 2021: 12, 2023: 3, 2024: 4, 2026: 6 | `git log --format=%ad --follow` | high |
| Document "Change history" begins: "Version 1.0 was the initial release covering messages 1-3, 4, and 5. Version 1.1 adds message breakdowns for 9 and 18, explanation of the Repeat Indicator field, and the explanation of USCG extended AIVDM." Later: 1.53 adds reference to the IALA ASM registry; 1.54 adds subarea fields of IMO289 Area Notice; 1.55 adds a table of contents. | `www/AIVDM.adoc` §Change history | high |
| The document credits Kurt Schwehr (UNH CCOM) for the Repeat Indicator field, USCG extended AIVDM, information from IEC-PAS and ITU-1371-3, Message 24 ("whose Python toolkit decodes it"), Messages 25–26, and Message 21 bit flags; it also notes "Some of what this document explains about the quirks of real-world encoders comes from examples provided by Kurt Schwehr." | `www/AIVDM.adoc` §Information Sources and message sections | high |
| The document states Message 27 was "described in ITU1371-4 and added here after that became a freely available download." | same | high |
| gpsd licence: BSD-style (file `COPYING`/`LICENSE`; "GPSD project copyrights are assigned to the project lead, currently Eric S. Raymond") | `COPYING` | high |

### libais (C++ with Python bindings; Apache-2.0)

| Fact | Source | Confidence |
|---|---|---|
| Oldest commit `61caae9`, 2010-04-28, author "schwehr" (Subversion import; svn UUID `a19cddd1-…`), message "something that actually works!" | `git log --reverse` | high |
| 2010-05-03 `1531d7c`: "message 1-5 are able to decode in python" | same | high |
| noaadata `ChangeLog.html` entry 0.44 (2010-05-21): "Started working on the new and separate libais C++ library for AIS with C-Python bridge for Deepwater Horizon" and "This version corresponds to working on libais-0.1 to libais-0.2" | noaadata/ChangeLog.html | high |
| Deepwater Horizon explosion was 2010-04-20 — eight days before the first libais commit (date of the blowout from general knowledge; cite the official report in ch. 7/11 (verify citation)) | — | medium |
| LICENSE: "Copyright 2010 Kurt Schwehr. Licensed under the Apache License, Version 2.0" | LICENSE | high |
| GitHub repository created 2010-09-06; 761 commits; top authors Kurt Schwehr (google.com 484, svn 70, gmail 66), Egil Moeller (49), Kevin Wurster of SkyTruth (38) | GitHub API; `git shortlog` | high |
| Tags: v0.7 2012-04-30, v0.8 2012-05-12, v0.9 2012-10-19, v0.10/0.11 2012-10-29, v0.12 2012-11-05, v0.13 2012-11-18, v0.15 2015-06-16 | `git for-each-ref` | high |
| PyPI: first upload 2012-04-30 (0.7); 11 releases; last 0.17 on 2018-01-17 | PyPI JSON | high |
| Last commit 2026-06-30 ("ci: add Python 3.14 and drop Python 3.12 support") — maintained but no PyPI release since 2018 | git log; PyPI | high |
| A web-search summary describes libais as "LGPL v3" — this is **wrong**; the LICENSE file is Apache-2.0. Expect this error in secondary sources. | LICENSE vs. search result | high |

### noaadata (Python; Apache-2.0 since the GitHub era)

| Fact | Source | Confidence |
|---|---|---|
| ChangeLog earliest entries: 0.3 – 2006-12-12; 0.4/0.5 – 2006-12-18; 0.6 – 2006-12-20; 0.7 – 2007-01-04 … 0.43 – 2009-08-22; 0.44 – 2010-05-21; 0.45 – 2012-03-02; 0.46 – 2014-12-18 | `ChangeLog.html` | high |
| Early entries include "Now includes BitVector.py version 1.3 (with permission) to make deployment easier", "Added initial prototype for Right Whale notice", "Started working on N-AIS processing scripts" | `ChangeLog.html` (0.3–0.6 block) | high |
| 0.24 (2007-Apr-07): "Improved setup.py … towards US Hydro 2007 conference release"; 0.30 (2007-Nov-07) "Pre eNavigation 2007 release" | `ChangeLog.html` | high |
| First git commit `8afda7f` 2010-09-09 "copied from 0.44 in svn" (author address `schwehr@snipe.ccom.nh`) | git log | high |
| LICENSE: "Copyright 2006-2011 Kurt Schwehr. Copyright 2012-2014 Google. This version is released under the Apache 2.0 license." | LICENSE | high |
| README: "Python library for talking to NOAA co-ops data servers and generating AIS waterlevel messages. WARNING: This is research code." | README.md | high |
| 200 commits; single tag v0.46 (2015-05-24); still receiving bot commits in 2026-10; **not on PyPI** (query returned nothing) | git; PyPI | high |
| gpsd AIVDM doc: "Kurt Schwehr warns that this is research code rather than a production tool." | `www/AIVDM.adoc` | high |

### ais-areanotice-py (Python; Apache-2.0)

| Fact | Source | Confidence |
|---|---|---|
| Oldest commit `4a8047b` 2009-06-02 (svn, same UUID as libais) "whales, auv's and buoys" | git log | high |
| README: "reference implementation of the AIS Binary Messages described in the IMO Circular 289 specification … IMO, Guidance on the Use of AIS Application-Specific Messages, SN.1/Circ.289, Ref. T2-OSS/2.7.1, 2 June 2010." and "This library started for just the area notice (aka Zone) to support the Rightwhale AIS Project (RAP)." | README.md | high |
| LICENSE: Copyright 2006-2011 Kurt Schwehr, 2012-2015 Google; Apache-2.0 | LICENSE | high |
| 354 commits; no tags; not on PyPI under `ais-areanotice`; last commit 2026-09-30 (dependabot) | git; PyPI | high |

### bitvector-modern (Python; PSF licence)

| Fact | Source | Confidence |
|---|---|---|
| First commit `441c8d1` 2015-03-30 "Version 3.3.2" (Kurt Schwehr, google.com) — an import of Avi Kak's BitVector 3.3.2 | git log | high |
| README: "This is a fork from Avi Kak's BitVector 3.5.0." LICENSE: Python Software Foundation License v2 | README.md; LICENSE | high |
| Upstream BitVector on PyPI: author Avinash Kak (Purdue); 3.5.0; last release 2021-05-30 | PyPI JSON | high |
| Role: BitVector is the bit-packing layer noaadata bundled from 2006 ("BitVector.py version 1.3 (with permission)"); bitvector-modern is the maintained fork. First tags v0.0.1 (2026-07-07) … v0.0.7 (2026-07-31); 354 commits | noaadata ChangeLog; git | high |

### aisparser (C with Java/Python bindings; BSD-style)

| Fact | Source | Confidence |
|---|---|---|
| Source headers: "Copyright 2006-2008 by Brian C. Lane" — project predates GitHub | `c/src/*.c` | high |
| GitHub import `fa32a00` 2010-12-27 "Initial Import of AIS Parser SDK" (author address bcl@redhat.com) | git log | high |
| LICENSE: 3-clause BSD-style ("AIS Parser SDK, Copyright (c) 2010-2014, Brian C. Lane, All rights reserved") | LICENSE | high |
| 50 commits; tags v1.0.0 and v1.10 both 2019-03-17; contributors include Kurt Schwehr (18 commits) and Steven Bennett | git | high |
| README (2026-09-27 commit): "This codebase is essentially unmaintained at this point (2026)" | README | high |
| Directory layout: `c/`, `java/`, `python/`, `dll/`, `contrib/` | `ls` | high |

### pyais (Python; MIT)

| Fact | Source | Confidence |
|---|---|---|
| First commit 2019-10-04 by "M0r13n" (git author name later Leon Morten Richter) | git log | high |
| LICENSE: MIT, "Copyright (c) 2019 M0r13n" | LICENSE | high |
| PyPI: first upload 2019-11-14; 85 releases; 3.3.0 uploaded 2026-10-04 | PyPI JSON | high |
| Tags: v0.0.1/v0.0.6 2019-11-14, 1.0.0 2019-11-21 … v3.3.0 2026-10-04 (82 tags) | git | high |
| 497 commits; README: "AIS message encoding and decoding. 100% pure Python."; supports encode as well as decode; reads TCP/IP sockets "encoded according to IEC 62320-1" | README.md | high |

### AIS-catcher (C++; GPL-3.0)

| Fact | Source | Confidence |
|---|---|---|
| First commits 2021-04-26 ("Initial commit") by jvde-github | git log | high |
| README: "Copyright (C) 2021 - 2026 jvde.github at gmail.com. All rights reserved. Licensed under GNU General Public License v3.0." (author publishes under a handle; real name not asserted here (verify)) | README.md | high |
| Tags: 0.05 2021-05-11, 0.06 2021-06-26, 0.07 2021-07-07 … v0.69 2026-06-14, v0.70 2026-06-19; 104 tags | git | high |
| 7,416 commits (2,266 by a GitHub Action bot baking web assets); last commit 2026-10-03 | git | high |
| GitHub description: "AIS receiver for RTL SDR dongles, Airspy R2, Airspy Mini, Airspy HF+, HackRF, SDRplay and SoapySDR"; 787 stars | GitHub API | high |

### rtl-ais (C; GPL-2 per source headers (verify top-level))

| Fact | Source | Confidence |
|---|---|---|
| Oldest commits are Kyle Keen's: 2013-12-11 "Heatmap utility", 2013-12-23 `c041f92` "rtl_ais: prototype" | git log | high |
| LICENCE file: "Copyright (C) 2012 by Kyle Keen … rtl-ais uses code from AISDecoder Copyright (C) 2013 Astra Paging Ltd / AISHub (info@aishub.net)" | LICENCE | high |
| GitHub repository dgiardini/rtl-ais created 2015-06-04; tags v0.1 2015-07-03, v0.2 2016-08-18, v0.3 2018-07-26 | GitHub API; git | high |
| 190 commits; top authors dgiardini (89), Kyle Keen (36), Frederic Guilbault (18), Bryan Klofas (17); last commit 2026-08-05 (merge of "multi-udp-fanout") | git | high |
| GitHub description: "A simple AIS tuner and generic dual-frequency FM demodulator" | GitHub API | high |

### gnuais (C; GPL-2)

| Fact | Source | Confidence |
|---|---|---|
| Oldest commit 2008-09-22 by "rubund" (Ruben Undheim), svn message "Start prosjekt"; Heikki Hannikainen ("hessuh") contributing from 2008-10-22 | git log | high |
| AUTHORS: Ruben Undheim, Heikki Hannikainen, Sakari Nylund, Tomi Manninen | AUTHORS | high |
| Tags 0.1.0 2008-12-20, 0.1.1 2009-01-28, 0.2.0 2009-03-24 … debian/0.3.3-6 2016-12-03 | git | high |
| COPYING: GPL v2; last commit 2016-12-03 (Debian packaging); GitHub last push 2023-11 — effectively dormant | COPYING; git; GitHub API | high |

### gr-ais (C++/Python GNU Radio OOT; GPLv3+ per file headers)

| Fact | Source | Confidence |
|---|---|---|
| First GitHub commit 2011-03-30 Nick Foster; second commit "Deleted old SVN stuff" — indicates an earlier Subversion history (CGRAN era), start date not recoverable from this repo (verify) | git log | high (commit) / low (pre-2011 date) |
| No top-level LICENSE file; `lib/*.cc` headers carry GPL "either version 3, or (at your option) any later version"; GitHub API reports licence `null` | `grep`; GitHub API | high |
| 80 commits; last commit 2026-09-06 ("Add README.md"); README states it is "An AIS receiver for GNU Radio 3.10 … coherent Viterbi demodulation, NRZI decoding, and HDLC deframing with CRC checks." | git; README.md | high |
| Contributors include Alexandru Csete (OZ9AEC) | `git shortlog` | high |

### trendmicro/ais ("AIS BlackToolkit"; includes gr-aistx)

| Fact | Source | Confidence |
|---|---|---|
| First commit 2014-12-12 by Fernando Mercês; 18 commits; last 2020-08-20 | git log | high |
| README lists: `AiS_TX.grc` (GRC transmitter), `AiS_TX.py`, `AIVDM_Encoder.py` ("AIVDM encoder supporting the main message types"), `AIVDM_pre.pl` (by Gary C. Kessler), `gr-aistx.tgz` ("AIS Frame Builder block for GnuRadio"), `unpacker.c`, `unpacker.pl` | README | high |
| `gr-aistx/` contains a `GPL` file; source headers are the GNU Radio template "Copyright 2013 <+YOU OR YOUR COMPANY+>"; no top-level repo licence | tree; headers | high |
| GitHub description: "Toolkit for research purposes in AIS. See the website for the paper." (the paper is Balduzzi, Pasta & Wilhoit, ACSAC 2014 — cite from r-security-threats) | GitHub API | high |
| Contributors include "embyte" (5 commits) and a Shine Micro address | `git shortlog` | high |

### SDRangel AIS plugins (C++; GPL-3.0)

| Fact | Source | Confidence |
|---|---|---|
| Commit `1ac835260`, 2021-05-07, Jon Beniston: "Add AIS mod, demod and feature." (adds `plugins/channelrx/demodais`, `plugins/channeltx/modais`, `plugins/feature/ais`) | git log | high |
| First release containing it: v6.12.0, tagged 2021-05-11 | `git merge-base --is-ancestor`; tag date | high |
| SDRangel LICENSE: GPL-3.0; repository created 2015-08-30 | LICENSE; GitHub API | high |

### Java

| Fact | Source | Confidence |
|---|---|---|
| **AisLib**: first commit 2012-11-01 Kasper Nielsen; LICENSE "Copyright (c) 2011 Danish Maritime Authority … Apache License, Version 2.0"; tags v2.0 2014-03-25 … v2.8.8 2026-08-31; 813 commits; README lists reading from serial/TCP/file, proprietary source-tagging sentences, doublet filtering, encoding, "Sending AIS messages #6, #8, #12 and #14", ASM handling | git; LICENSE; README | high |
| **marine-api**: history begins 2010-03-06 (SourceForge, Kimmo Tuukkanen); AIS parser added 2015-01-26 by "jol" ("First version of the AIS parser … message types: 1, 2, 3, 4, 5, 18, 19"); LGPL-3.0; tags 0.1 2010-08-21 … 0.12.0 2023-02-26; 1,001 commits | git; LICENSE | high |
| **AISmessages**: first commit 2011-03-17 Thomas Borg Salling; same-day commit "Introduced Attribution-NonCommercial-ShareAlike"; README: CC BY-NC-SA 4.0, "free for non-commercial use"; tags aismessages-1.00 2011-03-21 … 4.1.2 2025-11-19; 579 commits | git; README | high |

### Rust (crates.io)

| Fact | Source | Confidence |
|---|---|---|
| `ais`: crate created 2020-04-18; repo first commit 2017-11-28 (Kevin Rauwolf); Apache-2.0; max 0.12.0; 39,411 downloads; last crate update 2024-10-27; repo commit 2026-02-16 "Reassemble fragmented messages in slots with IDs" | crates.io API; git; Cargo.toml | high |
| `nmea-parser`: created 2020-10-07 (Timo Saarinen); "NMEA 0183 parser for AIS and GNSS sentences"; Apache-2.0; 0.11.0 (2024-06-13); 526,077 downloads; last repo commit 2024-06-13 | crates.io API; git | high |
| `nmea-kit`: created 2026-04-06; "Bidirectional NMEA 0183 parser and encoder with AIS decoding"; MIT OR Apache-2.0; 0.8.9; 2,413 downloads | crates.io API | high |
| No crates named `ais-parser` or `aisparser` exist | crates.io API (404) | high |

### Go, Node, .NET

| Fact | Source | Confidence |
|---|---|---|
| go-ais: first commit 2019-02-04 Bertold Van den Bergh; MIT; description "ITU-R M.1371-5 packet decoder and encoder written in Go"; v0.1.0 2021-06-12 … v0.4.0 2024-07-22; last commit 2024-10-23 "Add much faster streaming NMEA decoder" | git; GitHub API | high |
| aislib (Go): first commit 2015-01-31 Marios Andreopoulos; GPL-3.0; last commit 2019-02-01 | git | high |
| npm `ggencoder`: created 2014-11-06, Fulup Ar Foll (GeoGate), Apache-2.0, 1.0.12, modified 2026-09-14; GeoGate repo created 2014-11-06 | npm registry; GitHub API | high |
| npm `ais-decoder`: created 2017-05-03, author Doron Segal, ISC, 1.3.5, last modified 2022-06-13 (its description text is copied from ggencoder) | npm registry | high |
| Ais.Net (C#): GitHub created 2019-07-21; AGPL-3.0; "zero allocation AIS decoder … Sponsored by endjin" | GitHub API | high |

### OpenCPN (context)

| Fact | Source | Confidence |
|---|---|---|
| GitHub history: "Initial commit of OpenCPN Version 2.1.0 Build 624a" 2010-06-29 (David Register); "Improve AIS symbology" 2010-09-16; GPL-2.0 — AIS display existed before the GitHub import (verify pre-2010 SourceForge history) | git; GitHub API | high / medium |

## Notes and quotes

- **The gpsd document is the lingua franca.** Within three days of starting
  `driver_aivdm.c` (2009-03-09), Raymond began the public write-up
  (2009-03-10). Its stated goal: "This is a description of how to decode
  AIVDM/AIVDO sentences. It collects and integrates information from publicly
  available sources and is intended to assist developers of open-source
  software for interpreting these messages." (AIVDM.adoc, Introduction.) It is
  the reference most later decoders (pyais, the Rust crates, go-ais, Ais.Net)
  cite in their READMEs (verify each README citation during the Chapter 44
  comparison).
- **Raymond on sources:** "Together, the IALA Technical Clarifications … and
  the Coast Guard's AIS pages at NAVCEN describe AIS message payloads type 1-24
  almost completely." and "Message type 27 was described in ITU1371-4 and
  added here after that became a freely available download." — useful for
  Chapter 15's "what is free" discussion: the open-source ecosystem was built
  largely from IALA/NAVCEN secondary material until ITU made M.1371 free.
- **Raymond on test data:** "one of your challenges is finding enough AIS packet
  data to make an effective regression test … AIS Hub is a free, public AIS
  feed pool." Several gpsd message descriptions were derived from "sentences
  forwarded to me from AIS Hub by various sources."
- **libais and Deepwater Horizon — the primary-source wording** is in the
  noaadata changelog, 0.44 (2010-05-21): "Started working on the new and
  separate libais C++ library for AIS with C-Python bridge for Deepwater
  Horizon." The first libais commit (2010-04-28) carries the message
  "something that actually works!" — eight days after the 2010-04-20 blowout.
  Use this rather than blog recollections. ⟨H⟩ entry "libais 2010" is confirmed.
- **noaadata's lineage** runs 2006-12 (0.3) → 2010-05 (0.44, libais split) →
  2014-12 (0.46). Its own README is blunt: "This is research code. Do not
  expect things to work nicely." Raymond echoes this in the gpsd document.
- **ais-areanotice-py** README: "This library started for just the area notice
  (aka Zone) to support the Rightwhale AIS Project (RAP)." It is the only
  public implementation framed as a *reference* for SN.1/Circ.289 (chapter 23).
- **aisparser** is the oldest C library with a documented start (headers
  "Copyright 2006-2008"), but its public git history only begins 2010-12-27,
  and its 2026 README now reads "essentially unmaintained."
- **Sound-card era → SDR era.** gnuais (2008, audio discriminator input) and
  AISHub's AISDecoder (2013, code reused in rtl-ais) belong to the
  sound-card/discriminator generation; Kyle Keen's `rtl_ais` prototype
  (2013-12-23) and gr-ais (GitHub 2011; earlier SVN) begin the RTL-SDR/GNU Radio
  generation; AIS-catcher (2021-04-26) and SDRangel's plugins (2021-05-07,
  v6.12.0) arrive within two weeks of each other and define the current
  generation. rtl-ais's LICENCE file is the documentary link between the two
  eras ("uses code from AISDecoder Copyright (C) 2013 Astra Paging Ltd /
  AISHub").
- **Transmit tooling.** The Trend Micro repository's own README calls
  `AiS_TX.py` "the AIS transmitter in form of script kiddie script." For the
  handbook: name the toolkit, its date (2014-12-12) and purpose, but do not
  reproduce usage (STYLE_GUIDE §4, security content). SDRangel's `modais` is
  the other widely distributed modulator.
- **Licence landscape.** Apache-2.0: libais, noaadata, ais-areanotice-py,
  AisLib, `ais` and `nmea-parser` crates, ggencoder. MIT: pyais, go-ais.
  GPL: AIS-catcher (v3), SDRangel (v3), gnuais (v2), gr-ais (v3+, headers only),
  aislib-Go (v3), OpenCPN (v2). LGPL-3.0: marine-api. AGPL-3.0: Ais.Net.
  BSD-style: gpsd, aisparser. PSF: bitvector-modern. **Non-OSI**: AISmessages
  (CC BY-NC-SA 4.0). No top-level licence: trendmicro/ais, gr-ais.
- **Release cadence snapshot (as of October 2026).** pyais: 85 PyPI releases
  in ~7 years, 3.3.0 on 2026-10-04. AIS-catcher: 104 tags since 2021. AisLib:
  v2.8.8 2026-08-31. libais: last PyPI release 2018 (0.17) despite commits in
  2026. gpsd: AIVDM doc v1.58 (2023) with 2026 edits. Dormant: gnuais (2016),
  aislib-Go (2019), ais-decoder npm (2022), nmea-parser (2024), trendmicro/ais
  (2020).

## Open questions / (verify)

- gpsd: exact gpsd version in which `gpsdecode` first emitted AIS JSON (JSON
  dumping began 2009-06-05; 2.90 released 2009-12-04 — confirm 2.90). (verify)
- gr-ais: locate the CGRAN/Subversion start date; Nick Foster's own account
  (talk or blog) would fix the year (2008–2010 range). (verify)
- aisparser: any public release/announcement from 2006–2008 (Brian Lane's site
  brianlane.com) to date the project before the 2010 GitHub import. (verify)
- noaadata: did versions 0.1/0.2 exist before 2006-12-12 (the changelog starts
  at 0.3)? Check the earliest svn tag or the 2007 US Hydro paper. (verify)
- AIS-catcher author's name: the project publishes under the handle
  jvde-github; confirm whether the author has published a name before using it.
  (verify)
- AISDecoder (Astra Paging/AISHub, 2013): licence and original download URL
  (aishub.net page now 404s; try archive.org and the `freerange/ais-on-sdr`
  wiki referenced in rtl-ais README). (verify)
- SignalK's use of `ggencoder`: confirm from the signalk-server dependency
  list. (verify)
- Perl: no CPAN distribution for AIVDM decoding was located via MetaCPAN
  queries ("AIS NMEA AIVDM" returned only Net::GPSD3 results). Either confirm
  absence or find the module name. (verify)
- MATLAB and other ecosystems (e.g., `aisstream` clients, R packages) were not
  surveyed. (verify)
- OpenCPN: pre-GitHub (SourceForge, 2009) history and when AIS decoding first
  appeared. (verify)
- marine-api: identity of contributor "jol" who added the AIS parser in
  January 2015. (verify)
- ais-areanotice-py: GitHub `created_at` (API returned null during this pass,
  probably rate limiting); clone shows svn history from 2009-06-02. (verify)
- Shared test corpora: enumerate gpsd `test/daemon/*.log` AIS files, libais
  `test/`, pyais `tests/` fixture counts for Chapter 44's comparison. (verify)

## Candidate figures and worked examples

1. **Timeline strip (Figure 44.1 / App. A inset):** 2006-12 noaadata 0.3;
   2006–2008 aisparser; 2008-09 gnuais; 2009-03-09 gpsd `driver_aivdm.c`;
   2009-03-10 gpsd AIVDM doc; 2009-06 ais-areanotice-py; 2010-04-28 libais
   (Deepwater Horizon +8 days); 2011-03 gr-ais on GitHub; 2011-03 AISmessages;
   2012-11 AisLib; 2013-12 rtl_ais prototype; 2014-11 ggencoder; 2014-12 Trend
   Micro toolkit; 2015-01 marine-api AIS; 2019-02 go-ais; 2019-07 Ais.Net;
   2019-10 pyais; 2020-04 `ais` crate; 2020-10 `nmea-parser`; 2021-04-26
   AIS-catcher; 2021-05-07 SDRangel AIS; 2026-04 `nmea-kit`.
2. **Lineage diagram (Mermaid):** BitVector → noaadata → libais;
   noaadata/ais-areanotice-py ↔ gpsd AIVDM doc (information flow credited in
   the doc); AISDecoder (AISHub 2013) → rtl-ais; gnuais ← sound-card era;
   gpsd doc → pyais/go-ais/Rust crates/Ais.Net (verify READMEs).
3. **gpsd AIVDM doc activity histogram:** commits per year (93, 25, 102, 22,
   35, 12, 11, 4, 0, 1, 4, 3, 12, 0, 3, 4, 6 for 2009–2026) — shows the
   2009–2013 burst when ITU-R M.1371-3/-4 content was absorbed.
4. **Licence matrix table** (project × licence family × maintained?) for
   Appendix E.
5. **Worked example (Chapter 44 "Try it"):** decode one Message 1 and one
   two-sentence Message 5 with `gpsdecode`, `libais` (`ais.decode`), `pyais`
   (`decode`) and `AIS-catcher` file mode, and diff the field names/units —
   this is the seed of the Chapter 44 comparison table (TASKS Phase 2
   `code/decode/`).
6. **"Research code" box:** juxtapose the noaadata README warning, Raymond's
   repetition of it, and the aisparser 2026 "unmaintained" notice as a
   *Definitions that bite* on "open source ≠ maintained".

## Recommended use by chapter

- **Chapter 11 (Growth 2004–2015):** cite noaadata 0.3 (2006-12-12) as the
  earliest dated open-source Python AIS tool found; aisparser headers
  2006–2008; gnuais 2008; gpsd AIVDM 2009-03; libais 2010-04-28 with the
  changelog quote tying it to Deepwater Horizon ⟨H⟩; gr-ais 2011; AisLib 2012;
  rtl_ais 2013; Trend Micro toolkit 2014-12.
- **Chapter 12 (2015–present):** pyais (2019) and AIS-catcher (2021) as the
  current defaults; SDRangel 6.12.0 (2021-05-11); Rust/Go/.NET crates; the
  2026 "unmaintained" notice on aisparser; libais maintained but unreleased on
  PyPI since 2018.
- **Chapter 15 (standards narrative):** Raymond's statement that the public
  document was assembled from IALA clarifications and NAVCEN pages, with
  Message 27 added only after M.1371-4 became free — evidence for the cost of
  paywalled standards.
- **Chapter 22 (message catalog):** use the gpsd document's version history
  (1.0: messages 1–5; 1.1: 9, 18; 1.3: 6, 7, 12, 13; …) to show how message
  coverage in open source expanded; credit lines for Messages 21, 24, 25–26.
- **Chapter 23 (ASM):** ais-areanotice-py as the SN.1/Circ.289 reference
  implementation (README quote); AisLib's ASM handling and ability to send
  Messages 6/8/12/14; gpsd doc versions 1.53–1.54 adding the IALA ASM registry
  reference and Area Notice sub-areas.
- **Chapter 26 (interfaces/logging):** AisLib's "proprietary source tagging
  sentences" and doublet filtering; pyais's IEC 62320-1 socket reading.
- **Chapter 33 (hardware/SDR):** receive chain generations (gnuais → gr-ais /
  rtl-ais → AIS-catcher / SDRangel); transmit-capable code exists (gr-aistx,
  SDRangel modais) — name, date, and Legal note only.
- **Chapter 42 (home receiver):** AIS-catcher release cadence and hardware list
  from its GitHub description.
- **Chapter 44 (open-source history):** the whole dossier; the Verified-facts
  tables map directly onto the per-project sections and the comparison table.
- **Chapter 58/60 (security):** trendmicro/ais contents and date as the public
  artefact of the ACSAC 2014 work; the parser population (gpsd, libais, pyais,
  AIS-catcher, OpenCPN, AisLib) as the attack surface list for r-vulns.
- **Appendix A:** add the dated items above as ⟨+⟩ entries (libais 2010 remains
  ⟨H⟩).
- **Appendix E:** licence/status/last-release columns straight from the tables
  here, each stamped "as of October 2026".
