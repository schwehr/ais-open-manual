# Chapter 44 — Open-source AIS decoding and encoding software: a history

> **Part VII — Decoding, software, and data engineering.** The origins, architectural evolution, licensing landscape, and engineering trade-offs of the open-source software libraries, daemons, and SDR engines that parse and emit maritime data link messages.

**In this chapter.** You will learn how open-source software emerged to decode and encode Automatic Identification System (**AIS**) messages from raw bitstreams, sound-card audio, and software-defined radio in-phase and quadrature (**IQ**) samples. We trace the technical history of foundational projects from the mid-2000s through 2026: Brian C. Lane's `aisparser`, Kurt Schwehr's XML-codegen `noaadata` and C++ `libais`, Eric S. Raymond's `gpsd` AIVDM driver and de-facto reference document, the Danish Maritime Authority's Java `AisLib`, SDR breakthroughs in `gnuais`, `gr-ais`, and `rtl-ais`, modern high-performance SDR demodulators like `AIS-catcher`, and modern multi-language decoders in Python (`pyais`), Rust (`ais`, `nmea-parser`, `nmea-kit`), Go (`go-ais`), Node.js, and .NET. You will examine the structural mechanics of 6-bit ASCII payload armoring, bit-level deserialization, multi-fragment sentence reassembly, Application-Specific Message (**ASM**) dictionaries, and encoder construction. Finally, through a comparative conformance benchmark across public test vectors, you will master the operational traps of differing sentinels, inconsistent field scales, and unvalidated inputs across maritime software stacks.

## 44.1 The origins of open maritime decoding

When the International Maritime Organization (**IMO**) mandated the Automatic Identification System under Regulation 19 of Chapter V of the Safety of Life at Sea (**SOLAS**) convention in 2000, maritime telemetry was dominated by proprietary marine electronics. Transponders exchanged GMSK radio packets over maritime VHF channels 87B (161.975 MHz) and 88B (162.025 MHz) using Self-Organizing Time Division Multiple Access (**SOTDMA**), outputting decoded data across serial bridge lines using the National Marine Electronics Association (**NMEA**) 0183 standard as codified in IEC 61162-1.

For early researchers, academic oceanographers, vessel traffic service operators, and software developers, working with AIS data presented a severe barrier. The core physical and link-layer protocol specifications published by the International Telecommunication Union Radiocommunication Sector (**ITU-R**) in Recommendation **ITU-R M.1371** were initially difficult to obtain or locked behind institutional firewalls. More restrictively, the presentation interface specifications—governing how receivers encapsulating radio bursts into ASCII-armored `!AIVDM` and `!AIVDO` sentences—were published in proprietary, copyrighted standards sold by the NMEA and the International Electrotechnical Commission (**IEC**). Commercial vessel traffic management software systems, such as Transas Navi-Harbour, Norcontrol, and Saab TransponderTech, were closed, costly, and tightly coupled to proprietary hardware interfaces.

The open-source AIS software movement was born from the necessity to break this closed ecosystem. Rather than purchasing multi-thousand-dollar industrial black-box decoders, computer scientists and marine researchers began reverse-engineering and codifying the binary structures of maritime data packets. The earliest efforts occurred in academic research labs and amateur radio communities. These pioneers transformed a protocol designed exclusively for specialized bridge displays and coastal radar consoles into a globally accessible telemetry commons.

```
1998–2002: Closed Proprietary Systems (Transas, Norcontrol, Saab; paid IEC/NMEA standards)
   │
   ├── 2006: aisparser (Brian C. Lane; C, BSD) — earliest C parser SDK
   ├── 2006: noaadata-py (Kurt Schwehr; UNH CCOM; Python/XML codegen, Apache-2.0)
   ├── 2008: gnuais (Ruben Undheim; C sound-card discriminator demodulator, GPL-2.0)
   ├── 2009: gpsd driver_aivdm.c & AIVDM.adoc reference (Eric S. Raymond & Kurt Schwehr)
   ├── 2009: ais-areanotice-py (Schwehr; reference ASM implementation for IMO SN.1/Circ.289)
   ├── 2010: libais (Schwehr; C++/Python, Apache-2.0; written for Deepwater Horizon spill ⟨H⟩)
   ├── 2011: gr-ais (Nick Foster; GNU Radio SDR receiver, GPL-3.0)
   ├── 2012: AisLib (Danish Maritime Authority; Java enterprise pipeline, Apache-2.0)
   ├── 2013: rtl-ais (Kyle Keen / Astra Paging AISDecoder; low-cost RTL2832U SDR)
   ├── 2014: Trend Micro AIS BlackToolkit (Marco Balduzzi et al.; ACSAC 2014 research)
   ├── 2019: pyais (Leon Morten Richter; pure Python, bidirectional encode/decode, MIT)
   ├── 2019–2020: Memory-safe language boom (go-ais, Rust crates ais & nmea-parser, Ais.Net)
   └── 2021–2026: AIS-catcher (jvde-github; multi-platform C++ SDR engine, 200k+ msg/s)
```

## 44.2 First generation: aisparser and the C libraries

The earliest standalone open-source library dedicated to decoding NMEA AIS sentences was the **AIS Parser SDK** (`aisparser`), created by **Brian C. Lane**. Lane began developing `aisparser` around 2006 in C, releasing it under a permissive 3-clause BSD-style license. The project's public version control history was later imported into GitHub in December 2010.

Lane designed `aisparser` to provide a portable, zero-overhead C engine capable of running on resource-constrained embedded microcontrollers and POSIX systems alike. The library defined core data structures for the primary operational message types:
- Position reports: Message 1, 2, and 3
- Base station reports: Message 4
- Static and voyage-related data: Message 5
- Binary addressed and broadcast packets: Messages 6 and 8
- Standard SAR aircraft reports: Message 9
- Class B position reports: Messages 18 and 19
- Aids to navigation: Message 21
- Class B static data reports: Messages 24A and 24B

Structurally, `aisparser` introduced the classic stateful sentence assembly pattern. Because standard NMEA 0183 sentences enforce an 82-character maximum line length, payloads exceeding 372 payload bits—such as 424-bit Message 5 announcements or multi-slot binary messages—must be split across multiple sentence fragments. The `aisparser` engine maintained a context structure tracking the expected sentence count, sequential message identifier, and running bit-buffer. Once all fragments arrived, the library extracted the 6-bit armored ASCII payload, stripped pad bits, and parsed raw integers into typed C struct members.

Lane provided language bindings for Java and Python, as well as Windows DLL builds and auxiliary command-line utilities. Contributors, including Kurt Schwehr and Steven Bennett, expanded its message coverage and fixed bit-twiddling defects. However, as the ITU-R standard expanded through revisions M.1371-3, M.1371-4, and M.1371-5, `aisparser` was not systematically updated to support long-range satellite frames (Message 27), complex ASM sub-areas, or single-slot AtoNs. By September 2026, the project repository was explicitly marked by its maintainer as unmaintained, serving primarily as historical foundation code for subsequent C decoders.

## 44.3 Academic research, XML codegen, and libais

At the Center for Coastal and Ocean Mapping (**CCOM**) at the University of New Hampshire (**UNH**), **Kurt Schwehr** pioneered a radically different architectural trajectory. Working in close collaboration with the United States Coast Guard (**USCG**) and the National Oceanic and Atmospheric Administration (**NOAA**), Schwehr required software capable of parsing high-throughput coastal receiver streams, generating Application-Specific Messages for physical oceanographic sensor telemetry (NOAA PORTS water levels and tidal currents), and broadcasting right-whale protective zones in Massachusetts Bay.

### 44.3.1 noaadata-py and XML-driven code generation

In December 2006, Schwehr established the `noaadata` project. Documented in its changelog beginning with version 0.3 on 2006-12-12, `noaadata` was an ambitious pure-Python research platform. Rather than hand-writing bit-masking routines for dozens of complex packet layouts, Schwehr pioneered declarative, XML-driven code generation.

Each AIS message type and binary application-specific message was defined in structured XML schema files. These schemas specified the exact field name, bit offset, bit width, signedness, scaling factor, and valid range. A Python code generator parsed these XML definitions to synthesize serialization, deserialization, and database ingestion classes. To manage bit-level stream manipulation in Python, `noaadata` bundled Avinash Kak's `BitVector` library (originally version 1.3, later maintained as the modernized fork `bitvector-modern`).

While `noaadata` proved extraordinarily flexible for prototyping novel environmental messages and validating experimental Coast Guard transmissions, pure-Python bit-vector manipulation suffered from performance limitations when handling millions of messages from national monitoring networks. Schwehr maintained `noaadata` as explicit research code, warning users in the project README and in communications with other developers that it was designed for rapid scientific experimentation rather than hardened real-time bridge production.

### 44.3.2 Deepwater Horizon and the creation of libais

On 20 April 2010, the *Deepwater Horizon* drilling rig exploded in the Gulf of Mexico, causing the largest marine oil spill in history. Responding federal agencies, oceanographers, and containment fleets faced an unprecedented operational challenge: coordinating hundreds of skimming vessels, supply barges, containment tugs, and research aircraft operating across thousands of square miles of open sea.

Tracking this dynamic marine armada required real-time ingestion and analysis of nationwide AIS telemetry from the US Coast Guard Nationwide Automatic Identification System (**NAIS**). Pure-Python decoders like `noaadata` were overwhelmed by the massive, firehose-volume telemetry streams generated across the Gulf.

Eight days after the blowout, on 28 April 2010, Kurt Schwehr committed the first lines of **`libais`** to Subversion (SVN commit `61caae9`, bearing the commit message *"something that actually works!"*). Documented in the `noaadata` changelog for version 0.44 (2010-05-21), Schwehr created `libais` as a standalone C++ decoding engine specifically to process NAIS streams for the Deepwater Horizon disaster response ⟨H⟩.

Released under the permissive Apache-2.0 license, `libais` was engineered for maximum decoding throughput:
1. **Direct Memory Bitstreams:** Payload characters are translated from 6-bit armored ASCII directly into contiguous binary arrays without intermediate heap allocations.
2. **Deterministic Struct Unpacking:** Core message fields are extracted using bit-shift arithmetic and immediately mapped into statically typed C++ classes.
3. **Robust ASM Sub-Area Handling:** `libais` implemented comprehensive decoders for IMO circulars (SN/Circ.236 and SN.1/Circ.289), including complex geometric shapes (circles, rectangles, polygons) used in marine environmental protection.
4. **Zero-Overhead Python C-Extension:** A thin CPython bridge exposed decoded messages as native Python dictionaries (`ais.decode()`), combining C++ execution speed with Python data science workflows.

`libais` quickly became the workhorse decoder for large-scale maritime analytics. It was adopted by non-governmental monitoring organizations like **Global Fishing Watch** (**GFW**) and **SkyTruth**, integrated into academic data pipelines, and packaged on PyPI. While `libais` lacks native multi-sentence NMEA reassembly (requiring callers to buffer and concatenate multi-sentence payload strings prior to calling `decode`), its single-message throughput exceeded 400,000 messages per second on contemporary CPU cores.

Schwehr also developed **`ais-areanotice-py`** (initiated in June 2009), which served as the international reference implementation for the binary Area Notice messages standardized in **IMO SN.1/Circ.289**.

## 44.4 gpsd and the de-facto reference standard

In March 2009, **Eric S. Raymond** (**ESR**), lead maintainer of the ubiquitous open-source GPS daemon **`gpsd`**, set out to add native AIS support. On 2009-03-09, Raymond committed the initial skeleton of `driver_aivdm.c` (commit `4996fc1c`). Just nine days later, basic AIS decoding shipped in `gpsd` release 2.39 (2009-03-18). By December 2009 (release 2.90), `gpsd` deployed **GPSD-NG**, a structured JSON-based daemon protocol that emitted decoded AIS messages as clean, typed JSON objects.

### 44.4.1 The AIVDM/AIVDO protocol decoding document

Raymond discovered that while ITU-R M.1371 specified over-the-air radio transmission formats, comprehensive public documentation explaining how those packets were mapped into NMEA 0183 `!AIVDM` sentences was almost non-existent outside of paywalled IEC and NMEA standards.

On 2009-03-10—one day after his initial commit to `driver_aivdm.c`—Raymond created a text document titled *"AIVDM/AIVDO Protocol Decoding"* (`AIVDM.txt`, later converted to AsciiDoc as `AIVDM.adoc`). Raymond's explicit goal was to synthesize all available public sources, manufacturer implementation notes, and practical field observations into an open, authoritative reference for developers of open-source maritime software.

Working in technical dialogue with Kurt Schwehr, Raymond continuously expanded the document:
- Schwehr contributed critical clarifications regarding the Repeat Indicator field, USCG extended AIVDM logging metadata, bit flags in Message 21 (AtoN), and the full bit layouts of Messages 24, 25, and 26.
- Raymond analyzed live telemetry forwarded from **AISHub**, identifying edge cases, undocumented manufacturer quirks, and common transponder firmware bugs.
- Over 330 commits were made to the document between 2009 and 2026. The document remains actively maintained under a BSD-style license.

Because official standards were expensive and restrictive, Raymond and Schwehr's document became the undisputed lingua franca of maritime software engineering. Virtually every open-source AIS library created after 2009—including `pyais`, `go-ais`, the Rust crates, and .NET implementations—explicitly cites the `gpsd` AIVDM document as its primary specification.

### 44.4.2 The gpsd shared test corpus

To ensure regression safety across `gpsd` releases, Raymond assembled a comprehensive test suite in `test/sample.aivdm`. This corpus gathered 118 real-world sentences contributed by Kurt Schwehr, Mike Greene, Neal Arundale, and AISHub feeds. Each sentence was paired with a bit-accurate expected JSON output file (`test/sample.aivdm.chk`).

This test suite became an inadvertent global standard. Because it was distributed under liberal BSD terms and captured rare message types (interrogations, channel assignments, and long-range broadcasts), authors of subsequent decoders utilized `sample.aivdm` to validate their own parsers.

## 44.5 The sound-card and SDR revolution

Before 2011, decoding AIS required either a commercial marine receiver outputting NMEA strings over RS-232/RS-422, or an amateur radio scanner modified with a discriminator tap wired to a PC sound card.

### 44.5.1 The sound-card era: gnuais and AISDecoder

In September 2008, Norwegian developer **Ruben Undheim** launched **`gnuais`** (commit message *"Start prosjekt"*), with contributions from Heikki Hannikainen (**hessuh**, creator of APRS.fi). Released under the GPL-2.0, `gnuais` sampled raw audio from a computer sound card at 48 kHz. It executed a software demodulator:
1. Audio bandpass filtering centered on the 1,200 Hz and 2,200 Hz subcarrier tones (or direct audio frequency shifts).
2. Bell 202 / GMSK matched filtering and zero-crossing symbol recovery.
3. NRZI (Non-Return-to-Zero Inverted) bit decoding.
4. HDLC flag detection (`01111110`), bit-destuffing (removing inserted 0-bits following five consecutive 1-bits), and 16-bit CCITT cyclic redundancy check (**CRC**) validation.
5. Emitting standard `!AIVDM` sentences over stdout or a local socket.

Concurrently, Astra Paging Ltd and the vessel-tracking aggregator **AISHub** released **`AISDecoder`** around 2013. Designed to expand AISHub's global coastal receiving network, `AISDecoder` allowed volunteer coastal station operators to feed decoded NMEA packets into aggregation servers using low-cost discriminator-tapped VHF receivers.

### 44.5.2 Software-Defined Radio: gr-ais and rtl-ais

The maritime software landscape underwent a seismic shift in 2011–2013 with the discovery that commercial USB DVB-T television tuner dongles based on the Realtek **RTL2832U** chip could be repurposed as wideband software-defined radios.

In March 2011, **Nick Foster** published **`gr-ais`**, an out-of-tree module for **GNU Radio**. Written in C++ and Python, `gr-ais` implemented a coherent receiver chain:
- Dual-channel frequency translation capturing both 161.975 MHz and 162.025 MHz simultaneously.
- Coherent Viterbi demodulation for GMSK symbols.
- Preamble synchronization and HDLC deframing.

While `gr-ais` demonstrated high receiver sensitivity, running GNU Radio required substantial computational resources and complex dependency chains. In December 2013, **Kyle Keen** created **`rtl-ais`**, embedding demodulation algorithms adapted from Astra Paging's `AISDecoder` into a lightweight, standalone C binary. Later maintained by Davide Giardini, `rtl-ais` allowed a US$15 RTL-SDR dongle plugged into a low-power Raspberry Pi single-board computer to operate as a continuous dual-channel coastal AIS monitoring station.

### 44.5.3 The modern SDR state of the art: AIS-catcher

In April 2021, developer **jvde-github** released **`AIS-catcher`**. Written in modern C++ and distributed under the GPL-3.0, `AIS-catcher` redefined open-source maritime reception.

`AIS-catcher` abandoned conventional discriminator audio emulation in favor of highly optimized DSP algorithms tailored for modern CPU vector instructions (SIMD/SSE/AVX/NEON):
- **Coherent and Non-Coherent Demodulation:** Supports multiple demodulation engines, ranging from low-latency frequency discriminator filters to multi-stage coherent trellis decoders.
- **Hardware Abstraction:** Direct native driver support for RTL-SDR, Airspy, HackRF, SDRplay, BladeRF, and generic SoapySDR interfaces.
- **Extreme High Throughput:** Benchmarks show `AIS-catcher` decoding over 200,000 raw frames per second when processing prerecorded IQ archives, with receiver sensitivity rivaling or exceeding type-approved commercial base stations.
- **Modern Streaming Features:** Built-in web dashboards, native Prometheus metrics, zero-loss UDP/TCP streaming, and optional NMEA TAG block emission with microsecond-accurate reception timestamps.

Between 2021 and 2026, `AIS-catcher` achieved over 100 version releases, becoming the universal default SDR receiver engine for maritime data enthusiasts, marine research vessels, and commercial shore feeds.

In the same era, **Jon Beniston** introduced dedicated AIS modulation and demodulation feature plugins into **`SDRangel`** (commit `1ac835260` in May 2021, release 6.12.0), providing an integrated graphical SDR workstation for analyzing maritime RF signals.

## 44.6 Enterprise and multi-language decoders

As AIS data became central to global supply chain logistics, fisheries regulation, and maritime domain awareness, developers ported decoding algorithms to diverse programming ecosystems.

```
+---------------+------------------------+------------+---------------+-----------------------------------------------+
| Project       | Author / Origin        | Language   | License       | Primary Architectural Role                    |
+---------------+------------------------+------------+---------------+-----------------------------------------------+
| aisparser     | Brian C. Lane (2006)   | C          | BSD-3-Clause  | Earliest standalone C decoding SDK            |
| noaadata      | Kurt Schwehr (2006)    | Python     | Apache-2.0    | XML-codegen research toolkit; NOAA PORTS      |
| gpsd          | Eric S. Raymond (2009) | C          | BSD-style     | System GPS/AIS daemon; AIVDM.adoc reference   |
| ais-areanotice| Kurt Schwehr (2009)    | Python     | Apache-2.0    | IMO SN.1/Circ.289 reference ASM parser        |
| libais        | Kurt Schwehr (2010)    | C++/Python | Apache-2.0    | High-speed analytics engine; Deepwater Horizon|
| AisLib        | Danish Maritime Auth.  | Java       | Apache-2.0    | National coastal shore network & VTS platform |
| pyais         | Leon M. Richter (2019) | Python     | MIT           | 100% pure-Python bidirectional encode/decode  |
| AIS-catcher   | jvde-github (2021)     | C++        | GPL-3.0       | High-sensitivity multi-platform SDR receiver  |
| go-ais        | Bertold V. d. Bergh    | Go         | MIT           | High-throughput concurrent microservice parser|
| nmea-parser   | Timo Saarinen (2020)   | Rust       | Apache-2.0    | Memory-safe zero-panic embedded parser        |
| Ais.Net       | endjin (2019)          | C# (.NET)  | AGPL-3.0      | High-performance zero-allocation cloud ingest |
+---------------+------------------------+------------+---------------+-----------------------------------------------+
```

### 44.6.1 Java: AisLib and marine-api

In November 2012, the **Danish Maritime Authority** (**DMA**) released **`AisLib`** under the Apache-2.0 license. Developed by Kasper Nielsen and DMA engineers, `AisLib` was engineered for national coastal surveillance networks. Unlike lightweight desktop parsers, `AisLib` addressed enterprise infrastructure requirements:
- Native parsing of proprietary base station source-tagging sentences.
- High-efficiency multi-sensor duplicate filtering (dropping identical packets captured across overlapping shore towers).
- Complete bidirectional encoding for transmitting coastal safety messages (Messages 6, 8, 12, and 14).
- Extensive ASM handling for regional Baltic and North Sea e-Navigation trials.

In the broader marine electronics sphere, Kimmo Tuukkanen's **`marine-api`** (an LGPL-3.0 Java NMEA 0183 library established in 2010) gained native AIS parsing in January 2015, providing general-purpose navigation message handling for chartplotters and bridge systems. In contrast, Thomas Borg Salling's **`aismessages`** (2011) offered a clean Java decoder but adopted a restrictive Creative Commons Attribution-NonCommercial-ShareAlike (**CC BY-NC-SA 4.0**) license, excluding it from commercial deployments and standard OSI open-source distributions.

### 44.6.2 Python: The modern era of pyais

While `libais` dominated raw C++ performance, its lack of pure-Python packaging, absence of encoding capabilities, and aging build infrastructure created an opening for modern Python tooling. In October 2019, **Leon Morten Richter** released **`pyais`** under the MIT license.

Written in 100% modern Python (with zero C-compiler dependencies), `pyais` achieved rapid adoption through aggressive maintenance and rapid release cycles (surpassing 85 releases by 2026). Richter built `pyais` to support the full ITU-R M.1371 catalog (Messages 1–28), complete NMEA multi-sentence stream reassembly, TCP/UDP client abstractions conforming to IEC 62320-1 shore-station interfaces, and full bidirectional **encoding** of arbitrary AIS messages.

### 44.6.3 Memory safety: Rust and Go

The push toward memory-safe systems software in the late 2010s transformed maritime network infrastructure. Because AIS parsers directly ingest unauthenticated data from untrusted network sockets and open RF receivers, buffer overflows in C/C++ decoders represent serious security vulnerabilities.

On crates.io, the Rust community introduced several parsing libraries:
- **`ais`** (created by Kevin Rauwolf in 2017, published 2020): An Apache-2.0 crate focusing on strict no-panic deserialization of binary AIS payloads.
- **`nmea-parser`** (created by Timo Saarinen in 2020): An Apache-2.0 zero-allocation parser combining NMEA 0183 sentences, GNSS tracking, and AIS decoding.
- **`nmea-kit`** (2026): A bidirectional NMEA/AIS crate offering encoding and decoding pipelines.

In the Go ecosystem, **Bertold Van den Bergh** published **`go-ais`** in February 2019 under the MIT license. Optimized for high-throughput cloud streaming services, `go-ais` provides concurrent decoding and encoding conforming to ITU-R M.1371-5, featuring zero-copy streaming NMEA scanners. In the .NET world, consulting firm endjin sponsored **`Ais.Net`** (2019), an AGPL-3.0 library utilizing modern C# `Span<T>` memory primitives to achieve zero-allocation parsing in Azure cloud ingestion workers.

## 44.7 Encoding software: the neglected twin

While dozens of projects implement AIS *decoding*, software capable of *encoding* valid AIS payloads has historically been rare, fragmented, and technically challenging.

### 44.7.1 Why encoding is mathematically and structurally harder

Decoding an AIS sentence is a passive extraction process: a parser receives an armored ASCII string, strips framing, extracts bits, and scales integers to engineering units. Encoding requires the inverse—and must satisfy rigid protocol invariants:
1. **Coordinate Quantization:** Longitude must be converted to signed 28-bit integers representing $1/10{,}000$ of an arc-minute ($\text{val} = \text{round}(\text{lon} \times 600{,}000)$). Out-of-range floats must be clipped or mapped to sentinel values ($181^\circ \implies 0x6791AC0$).
2. **ROT Square-Root Transform:** Rate of turn cannot be stored linearly; an encoder must map turn velocity in degrees per minute to an 8-bit integer using the non-linear relationship $\text{ROT}_{\text{AIS}} = \text{round}(4.733 \times \sqrt{|\text{ROT}_{\text{sensor}}|}) \times \text{sign}$, saturated at $\pm126$, or assign $\pm127$ / $-128$ for turning thresholds and missing sensors.
3. **6-Bit Text Mapping:** Strings must be truncated, uppercased, converted to 6-bit ASCII codes via Table 45, and padded to full field length using the `@` character ($0b000000$).
4. **Armoring and Pad Arithmetic:** The unrolled bitstream must be sliced into 6-bit chunks, mapped into the ASCII range $48\text{--}119$ (skipping characters $88\text{--}95$), and padded with trailing zeros to reach a 6-bit boundary. The exact number of pad bits ($0\text{--}5$) must be calculated and emitted in the NMEA sentence footer.
5. **Multi-Fragment Splitting:** If the armored string exceeds the remaining space in an 82-byte NMEA line, the payload must be segmented cleanly across multiple sentences sharing a sequential message ID.

```
Raw Physical Telemetry (MMSI, Coordinates, Speed, Ship Name)
   │
   ▼
[Field Quantization & Sentinel Mapping] (Two's complement, 1/10,000 min, ROT sqrt transform)
   │
   ▼
[Bit Packing & BitVector Construction] (MSB-first packing into contiguous bit array)
   │
   ▼
[6-Bit Slicing & Fill-Bit Calculation] (Pad length to multiple of 6 bits: pad = (6 - (bits % 6)) % 6)
   │
   ▼
[ASCII Armoring (Table 45)] (Value + 48; if > 40, + 8; map to characters '0'..'W', '`'..'w')
   │
   ▼
[NMEA 0183 Framing & Sentence Splitting] (!AIVDM,total,num,seq,chan,payload,pad*hh\r\n)
```

Early open-source encoders were mostly isolated research scripts. Kurt Schwehr's `noaadata` and `ais-areanotice-py` included custom encoders to synthesize coastal water level notices and whale-protection zones. In commercial networks, the Danish Maritime Authority's `AisLib` provided production encoders for shore-to-ship broadcast coordination. In the modern landscape, `pyais` and `go-ais` offer fully generalized encoding APIs.

> **Definitions that bite.** **"Research code" versus "Production library."**
> In open-source maritime software, "open source" does not imply maintained, certified, or safe for navigational use. In 2006, Kurt Schwehr explicitly warned in the `noaadata` README: *"WARNING: This is research code. Do not expect things to work nicely."* Eric S. Raymond reiterated this warning in the `gpsd` AIVDM documentation. Twenty years later, Brian C. Lane updated `aisparser` with a blunt notice: *"This codebase is essentially unmaintained at this point (2026)."* 
> 
> Deploying research or unmaintained decoders into safety-critical bridge navigation systems or autonomous command loops violates marine engineering best practices. Research code frequently passes out-of-range sensor garbage directly to consumers, lacks fuzz-tested boundary protections, and silently truncates unrecognized message extensions.

## Then & now

- ⟨H⟩ **1998 (ITU-R M.1371-0):** The initial AIS standard was ratified; decoders were proprietary, closed-source C/C++ firmware embedded inside commercial marine transponders and coastal VTS installations.
- ⟨H⟩ **2006 (noaadata-py & aisparser):** Kurt Schwehr at UNH CCOM released `noaadata` using XML-driven codegen for marine research; Brian C. Lane authored `aisparser`, the earliest public C decoding SDK.
- ⟨+⟩ **2008 (gnuais):** Ruben Undheim launched `gnuais`, demonstrating software-based GMSK demodulation and HDLC packet extraction from discriminator-tapped sound cards under GPL-2.0.
- ⟨+⟩ **2009 (gpsd AIVDM):** Eric S. Raymond added `driver_aivdm.c` to `gpsd` and published the open `AIVDM.adoc` specification, providing the global engineering reference for maritime message parsing.
- ⟨H⟩ **2010 (libais):** Kurt Schwehr authored `libais` in C++ with Python bindings eight days after the Deepwater Horizon blowout to process massive USCG NAIS telemetry feeds for oil spill containment operations.
- ⟨+⟩ **2011 (gr-ais):** Nick Foster published `gr-ais`, introducing coherent software-defined radio reception of maritime AIS signals to the GNU Radio framework.
- ⟨+⟩ **2012 (AisLib):** The Danish Maritime Authority open-sourced `AisLib`, establishing an enterprise Java standard for national coastal network data aggregation and duplicate filtering.
- ⟨+⟩ **2013 (rtl-ais):** Kyle Keen and Davide Giardini released `rtl-ais`, combining Astra Paging's `AISDecoder` algorithms with low-cost RTL2832U DVB-T USB tuners.
- ⟨+⟩ **2014 (Trend Micro AIS BlackToolkit):** Security researchers Marco Balduzzi, Alessandro Pasta, and Kyle Wilhoit published software-defined transceivers demonstrating vulnerabilities across unauthenticated AIS networks.
- ⟨+⟩ **2019 (pyais & go-ais):** Modern multi-language decoders emerged; Leon Morten Richter introduced `pyais` in pure Python, while Bertold Van den Bergh published `go-ais` in Go.
- ⟨+⟩ **2020–2021 (Rust & AIS-catcher):** Memory-safe Rust crates (`ais`, `nmea-parser`) achieved widespread deployment; `AIS-catcher` established a new standard for high-sensitivity multi-platform SDR reception.
- ⟨+⟩ **2026 (Modern Protocol Evolution):** `pyais` and modern decoders integrated single-slot AtoN (Message 28) and VDES static capabilities from ITU-R M.1371-6, while legacy projects like `aisparser` formally reached unmaintained status.

## On the wire

To understand how software decoders translate raw serial text into structured maritime data, we analyze the byte and bit transformations across two canonical test sentences from the public `gpsd` and `libais` test corpora.

### Message 1: Class A position report

Consider the single-sentence Class A position report recorded from coastal waters:

```text
!AIVDM,1,1,,A,15RTgt0PAso;90TKcjM8h6g208CQ,0*4A
```

Breaking down the NMEA framing fields:
- `!AIVDM`: NMEA encapsulation formatter (packet received from an external station).
- `1`: Total sentence count for this message.
- `1`: Sentence sequence number.
- *(empty)*: Sequential message identifier (omitted for single-sentence messages).
- `A`: Radio channel (161.975 MHz).
- `15RTgt0PAso;90TKcjM8h6g208CQ`: 28-character armored payload string.
- `0`: Fill bits added to align payload with a 6-bit boundary.
- `*4A`: 8-bit XOR checksum over all characters between `!` and `*`.

Each ASCII character maps to a 6-bit integer via the armoring algorithm:
$$\text{val} = \text{ord}(c) - 48; \quad \text{if } \text{val} > 40: \text{val} -= 8$$

```
Character:      1       5       R       T       g       t       0       P
ASCII (hex):   0x31    0x35    0x52    0x54    0x67    0x74    0x30    0x50
6-bit Value:     1       5      34      36      47      60       0      32
Binary:       000001  000101  100010  100100  101111  111100  000000  100000
```

Extracting message fields from the unpacked bitstream:
1. **Message ID (bits 0–5, 6 bits):** `000001` $\implies 1$ (Class A Position Report).
2. **Repeat Indicator (bits 6–7, 2 bits):** `00` $\implies 0$ (original broadcast).
3. **MMSI (bits 8–37, 30 bits):** `000101 100010 100100 101111 111100` $\implies 371{,}798{,}000$ (Panamanian-flagged vessel).
4. **Navigational Status (bits 38–41, 4 bits):** `0000` $\implies 0$ ("Under way using engine").
5. **Rate of Turn (bits 42–49, 8 bits signed):** Hex `0x81` $\implies -127$ decimal. This is a critical protocol sentinel meaning *"turning left at greater than $5^\circ$ per 30 seconds, no turn indicator available."*
6. **Speed Over Ground (bits 50–59, 10 bits):** $123 \times 0.1 \implies 12.3\text{ knots}$.
7. **Position Accuracy (bit 60, 1 bit):** `1` $\implies$ High accuracy ($\le 10\text{ m}$, DGNSS/RAIM).
8. **Longitude (bits 61–88, 28 bits signed):** Signed integer $-74{,}037{,}230 \div 600{,}000 \implies -123.395383^\circ\text{ W}$.
9. **Latitude (bits 89–115, 27 bits signed):** Signed integer $+29{,}028{,}980 \div 600{,}000 \implies +48.381633^\circ\text{ N}$.
10. **Course Over Ground (bits 116–127, 12 bits):** $2240 \times 0.1 \implies 224.0^\circ$.
11. **True Heading (bits 128–136, 9 bits):** $215 \implies 215^\circ$.
12. **Time Stamp (bits 137–142, 6 bits):** $33 \implies 33\text{ seconds past the UTC minute}$.
13. **SOTDMA Communication State (bits 149–167, 19 bits):** Sync state 0, slot timeout 2, sub-message 1249 (allocating slot number 1249 for future transmission).

> **Try it.** **Direct payload decoding with pyais and libais.**
> Run this benchmark script inside the repository environment to inspect real decoded fields and compare execution behavior between pure-Python `pyais` and compiled C++ `libais`:
> 
> ```python
> import ais, pyais
> 
> sentence = "!AIVDM,1,1,,A,15RTgt0PAso;90TKcjM8h6g208CQ,0*4A"
> 
> # 1. Decode using pure-Python pyais
> msg_pyais = pyais.decode(sentence).asdict()
> print(f"pyais: MMSI={msg_pyais['mmsi']} SOG={msg_pyais['speed']} kn "
>       f"Pos=({msg_pyais['lat']:.6f}, {msg_pyais['lon']:.6f}) Turn={msg_pyais['turn']}")
> 
> # 2. Decode using compiled C++ libais
> body = sentence.split(",")[5]
> pad = int(sentence.split(",")[6].split("*")[0])
> msg_libais = ais.decode(body, pad)
> print(f"libais: MMSI={msg_libais['mmsi']} SOG={msg_libais['sog']:.1f} kn "
>       f"Pos=({msg_libais['y']:.6f}, {msg_libais['x']:.6f}) ROT={msg_libais['rot']:.1f}")
> ```
> 
> Expected output:
> ```text
> pyais: MMSI=371798000 SOG=12.3 kn Pos=(48.381633, -123.395383) Turn=-127.0
> libais: MMSI=371798000 SOG=12.3 kn Pos=(48.381633, -123.395383) ROT=-720.0
> ```
> Notice the critical semantic disagreement: `pyais` preserves the raw sentinel value `turn: -127.0`, whereas `libais` erroneously applies the mathematical inverse transform to the sentinel, reporting a physically impossible rotational rate of `-720.0 deg/min`.

### Message 5: Multi-sentence static and voyage-related data

Longer packets require multi-fragment reassembly. Consider this two-part Message 5 report from container vessel *EVER DIADEM*:

```text
!AIVDM,2,1,1,A,55?MbV02;H;s<HtKR20EHE:0@T4@Dn2222222216L961O5Gf0NSQEp6ClRp8,0*1C
!AIVDM,2,2,1,A,88888888880,2*25
```

The reassembly engine links the two sentences via sentence total `2`, sentence numbers `1` and `2`, and sequential ID `1`. The concatenated payload contains $71 \text{ characters} \times 6 \text{ bits} = 426\text{ bits}$. With $2\text{ fill bits}$ indicated in the second sentence footer, the true payload spans exactly $424\text{ bits}$ (the standard size for Message 5):
- **IMO Number (bits 40–69, 30 bits):** $9{,}134{,}270$.
- **Call Sign (bits 70–111, 42 bits, 7 chars):** `3FOF8@@` $\implies$ `"3FOF8"`.
- **Vessel Name (bits 112–231, 120 bits, 20 chars):** `EVER DIADEM@@@@@@@@@` $\implies$ `"EVER DIADEM"`.
- **Ship Type (bits 232–239, 8 bits):** $70 \implies$ Cargo ship.
- **Dimensions (bits 240–269, 30 bits):** Bow $A=225\text{ m}$, Stern $B=70\text{ m}$, Port $C=1\text{ m}$, Starboard $D=31\text{ m}$ (total length $295\text{ m}$, beam $32\text{ m}$).
- **ETA (bits 274–293, 20 bits):** Month 5, Day 15, Hour 14, Minute 0 $\implies$ May 15, 14:00 UTC.
- **Maximum Present Static Draught (bits 294–301, 8 bits):** $122 \times 0.1 \implies 12.2\text{ m}$.
- **Destination (bits 302–421, 120 bits, 20 chars):** `NEW YORK@@@@@@@@@@@@` $\implies$ `"NEW YORK"`.

## Validation, uncertainty & data quality

Because open-source decoders were developed independently across multiple decades, they exhibit substantial, subtle discrepancies when parsing identical bit patterns. Data engineering pipelines ingesting heterogeneous decoder outputs must account for these systematic variances.

```
+------------------------------------+-----------------------+-------------------------+-----------------------------------------+
| Protocol Field / Condition         | pyais (v3.2.3)        | libais (v0.17)          | gpsd / gpsdecode (v1.58 doc)            |
+------------------------------------+-----------------------+-------------------------+-----------------------------------------+
| ROT Sentinel -127 (Turning Left)   | turn: -127.0          | rot: -720.0             | turn: "fastleft" or -127                |
| ROT Sentinel -128 (No Turn Info)   | turn: -128.0          | rot: -731.4             | turn: nan                               |
| 1/10-minute coordinate fields      | Raw tenths / minutes  | Scaled decimal degrees  | Scaled decimal degrees                  |
| Message 27 Position Latency Flag   | gnss: False (bit=1)   | gnss: True (bit=1)      | Latency inverted / mapped               |
| Message 27 Non-standard (168 bits) | Decodes successfully  | AIS_ERR_BAD_BIT_COUNT   | Decodes with trailing padding flag      |
| Message 28 (Single-slot AtoN)      | Full decode (type 28) | Error: msg 28 unhandled | Unhandled in older daemons              |
| Inland AIS Draught (DAC 200 FI 10) | draught: 2.04 m       | draught: 20.4 m         | draught: 2.04 m (scaled 1/100 m)        |
| Unknown DAC/FI in Message 6 / 8    | Emits raw binary hex  | Throws DecodeError      | Emits raw binary data array             |
| Out-of-range latitude (> 90 deg)   | Passes unflagged      | Passes unflagged        | Emits unflagged (or drops target)       |
+------------------------------------+-----------------------+-------------------------+-----------------------------------------+
```

### 44.8.1 The Rate-of-Turn sentinel trap

The most pervasive mathematical error across maritime decoding software involves Rate of Turn (**ROT**). Recommendation ITU-R M.1371 Annex 7 Table 46 defines ROT as an 8-bit signed two's complement integer:
- Values $0$ to $\pm126$ correspond to turning rates calculated via the non-linear relationship:
$$\text{ROT}_{\text{AIS}} = 4.733 \times \sqrt{\text{ROT}_{\text{sensor}}}$$
- Value $+127$ indicates turning right at more than $5^\circ$ per 30 seconds with no TI (Turn Indicator) available.
- Value $-127$ indicates turning left at more than $5^\circ$ per 30 seconds with no TI available.
- Value $-128$ ($0x80$) is the default sentinel indicating *no turn information available*.

`libais` erroneously executes the inverse mathematical function on sentinels:
$$\text{ROT}_{\text{deg/min}} = -\left(\frac{127}{4.733}\right)^2 \approx -720.003^\circ/\text{min}$$
$$\text{ROT}_{\text{deg/min}} = -\left(\frac{128}{4.733}\right)^2 \approx -731.39^\circ/\text{min}$$

When downstream statistical models or automated track-cleaning algorithms ingest these fields without filtering, they register vessels executing impossible maneuvers at over two complete revolutions per minute. In contrast, `gpsd` outputs JSON with explicit `nan`, `"fastleft"`, or `"fastright"` strings, while `pyais` leaves raw integer sentinels for the application layer to resolve.

### 44.8.2 Coordinate scaling discrepancies in 1/10-minute messages

Messages designed for reduced-bandwidth links—including DGNSS broadcast (Message 17), channel management (Message 22), group assignment (Message 23), and long-range satellite frames (Message 27)—encode coordinates using 18 bits for longitude and 17 bits for latitude in units of **$1/10$ of an arc-minute** ($\approx 185.2\text{ m}$ resolution), rather than the $1/10{,}000$ of an arc-minute ($\approx 0.1852\text{ m}$) used in standard position reports (Messages 1–3, 18).

Software libraries handle these units with alarming inconsistency:
- When parsing Message 17 reference station positions, `libais` converts coordinates to decimal degrees ($29.13^\circ\text{E}, 59.9867^\circ\text{N}$).
- `pyais` divides raw integer values by $10$, producing minutes of arc ($1747.8', 3599.2'$).
- If downstream GIS software plots `pyais` coordinates directly as degrees, vessels and base stations are mapped thousands of miles outside Earth's coordinate envelope.

### 44.8.3 Non-standard message lengths and strictness

Real-world coastal and satellite receivers frequently capture packets that violate strict ITU-R bit-length specifications. A notable example is Message 27: standardized as a compact 96-bit packet, certain Class A and Class B transponders pad Message 27 transmissions out to 168 bits (the length of a standard 1-slot position report).

When presented with a 168-bit Message 27 packet:
- `pyais` successfully parses the first 96 bits and cleanly discards trailing pad bits.
- `libais` aborts decoding and raises an unhandled C++ exception (`AIS_ERR_BAD_BIT_COUNT`).
- In automated high-volume ingestion daemons, unhandled C++ exceptions in `libais` can terminate the host process unless explicitly wrapped in catch blocks.

### 44.8.4 Fuzzing and malformed input robustness

Because AIS was designed in an era without cryptographic authentication, coastal receivers and software decoders regularly encounter corrupted or deliberately malformed serial streams:
1. **Invalid ASCII Armoring Characters:** Corrupted radio packets that introduce bytes outside valid ranges ($48\text{--}87$ and $96\text{--}119$) must trigger immediate checksum or framing rejection.
2. **Buffer Over-Length Exploits:** Crafting NMEA lines exceeding 82 characters can trigger stack-smashing buffer overflows in legacy C libraries that utilize fixed-size line buffers without length checks.
3. **Unbounded Multi-Fragment Tables:** Flooding a receiver with thousands of incomplete fragment 1 sentences bearing unique sequential IDs exhausts memory in stateful reassembly engines that lack strict timeout and LRU eviction policies.

> **Threat model.** **Vulnerabilities in open-source maritime parsers.**
> - **Attacker Profile:** Rogue terrestrial RF transmitters, compromised coastal aggregator nodes, or malicious internet feed contributors.
> - **Attacker Capability:** Crafting arbitrary over-the-air RF bursts or feeding synthetically mutated NMEA 0183 sentences into public aggregation servers.
> - **Impact:** Denial of service via parser crashes, high-load memory exhaustion, or remote code execution on coastal surveillance servers and vessel bridge management computers.
> - **Mitigation:**
>   1. Migrate decoding engines to memory-safe languages (Rust, Go) or enforce rigorous bounds checking and fuzzing on legacy C/C++ libraries.
>   2. Isolate network-facing decoders inside unprivileged, sandboxed microVMs or containers.
>   3. Enforce strict sentence timeouts (e.g., discarding uncompleted multi-fragment messages after 5 seconds).
>   4. Reject sentences with invalid checksums or out-of-range armor characters prior to bitfield parsing.

> **Legal note.** **Transmission software, testbeds, and regulatory compliance.**
> While writing and running software to *receive* and *decode* AIS broadcasts is lawful worldwide, executing software that *modifies* or *transmits* AIS RF signals (such as GNU Radio transmitter flowgraphs or SDR modulator plugins) is strictly regulated. 
> 
> Under international maritime law (SOLAS Chapter V) and national telecommunications statutes (such as FCC Title 47 in the United States and equivalent European national radio regulations), transmitting uncertified AIS signals on VHF marine frequencies (161.975 MHz and 162.025 MHz) is a federal offense punishable by severe civil fines, equipment confiscation, and criminal prosecution. Open-source developers testing encoding or transmission software must operate exclusively into certified RF dummy loads, inside Faraday RF shielding enclosures, or across private, non-radiating cabled testbeds.

## Software

**Open source:**
- `AIS-catcher` (C++): State-of-the-art SDR receiver and message demodulator supporting RTL-SDR, Airspy, HackRF, and SoapySDR hardware. Caveat: Highly optimized DSP pipelines require careful parameter tuning to avoid CPU saturation on single-core embedded devices.
- `pyais` (Python): Pure-Python library supporting full decoding and encoding for Messages 1–28, multi-fragment reassembly, and network streaming. Caveat: Pure-Python execution speed is slower than compiled C/C++ when batch-processing multi-gigabyte historical archives.
- `libais` (C++ with Python bindings): High-throughput C++ decoding library created by Kurt Schwehr. Caveat: Does not provide automatic multi-sentence NMEA reassembly; does not decode Message 28 in release 0.17.
- `gpsd` (C): Widely deployed system GPS and navigation daemon supporting AIS decoding, logging, and JSON streaming. Caveat: Standard daemon JSON output collapses certain raw protocol sentinels into missing keys or NaN representations.
- `AisLib` (Java): Enterprise-grade maritime library created by the Danish Maritime Authority supporting coastal network ingestion, duplicate filtering, and bidirectional ASM handling. Caveat: Heavy enterprise Java dependency footprint.
- `go-ais` (Go): Fast, concurrent decoding and encoding library conforming to ITU-R M.1371-5. Caveat: Focuses primarily on VDL payload bits; requires external framing wrappers for complex proprietary NMEA extensions.
- `nmea-parser` (Rust): High-performance, zero-allocation Rust crate for parsing NMEA 0183 and AIS streams with compile-time memory safety. Caveat: Limited support for specialized regional inland ASM payloads.

**Free but closed:**
- `ShipPlotter` (Windows): Widely used legacy desktop software for decoding and displaying AIS targets from audio discriminator taps and serial inputs. Caveat: Proprietary, closed-source freemium license; lacks headless Linux daemon operation.

**Commercial:**
- `Transas Navi-Harbour / Wärtsilä VTS`: Enterprise-grade vessel traffic management platform used in commercial ports and coastal surveillance centers. Caveat: Extremely expensive proprietary software licensed exclusively for certified marine hardware.
- `GateHouse Maritime AIS Server`: Industrial coastal data aggregation and track reconstruction engine. Caveat: Closed enterprise software requiring dedicated server licensing.

## Standards & guides

- **Recommendation ITU-R M.1371-6** (2026): *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band*. Defines physical RF modulation, link-layer TDMA framing, and the complete bit-level message catalog (Messages 1–28).
- **Recommendation ITU-R M.1371-5** (2014): Preceding standard defining the classic 27-message catalog and Annex 8 message bit layouts implemented by most 2010s decoders.
- **Recommendation ITU-R M.1371-1** (2001): Foundational standard establishing initial SOTDMA broadcast rules and operational message definitions.
- **IEC 61162-1:2016 (Edition 5.0)**: *Maritime navigation and radiocommunication equipment and systems — Digital interfaces — Part 1: Single talker and multiple listeners*. Standardizes the `!AIVDM` and `!AIVDO` sentence structures, armoring tables, and checksum rules.
- **IEC 62320-1:2015 (Edition 2.0)**: *Maritime navigation and radiocommunication equipment and systems — Automatic identification system (AIS) — Part 1: AIS Base Stations*. Governs shore-station network interfaces and TAG block formats.
- **IEC 61993-2:2018 (Edition 3.0)**: *Class A shipborne equipment of the automatic identification system (AIS)*. Defines operational requirements and presentation interface behaviors.
- **IMO SN.1/Circ.289** (2010): *Guidance on the Use of AIS Application-Specific Messages*. The authoritative specification for international binary messages, including meteorological and hydrological data and Area Notices.

## Pitfalls

- **Confusing 6-bit ASCII with standard 7-bit/8-bit ASCII:** Using standard ASCII lookup tables to decode vessel names or callsigns $\implies$ produces corrupted gibberish; decoders must map characters strictly through the 6-bit lookup table defined in ITU-R M.1371 Table 45.
- **Applying inverse mathematical formulas to ROT sentinels:** Squaring raw ROT values $\pm127$ or $-128$ $\implies$ generates physically absurd turn rates exceeding $700^\circ/\text{min}$; decoders must intercept these values as discrete operational sentinels.
- **Dropping multi-fragment messages due to out-of-order interleaving:** Assuming sentence fragments from different vessels will never arrive interleaved over multiplexed network feeds $\implies$ corrupts reassembly buffers; stateful parsers must index fragment state machines by talker ID, radio channel, and sequential message ID.
- **Assuming open-source libraries validate coordinate ranges:** Relying on decoders to sanitize invalid latitude ($>90^\circ$) or longitude ($>180^\circ$) values $\implies$ permits corrupted sensor telemetry to pass directly into downstream databases and map projections; downstream pipelines must validate geometry explicitly.
- **Treating heading 511 as valid compass direction:** Failing to filter heading sentinel 511 $\implies$ skews navigational vector calculations and vessel alignment graphics; 511 indicates "heading not available."
- **Misinterpreting Carrier-Sense Class B communication state:** Assuming a constant value of $393{,}222$ in Message 18 indicates a malfunctioning radio transmitter $\implies$ this 19-bit pattern is the mandatory standard fill value for non-SOTDMA Class B units.
- **Ignoring 1/10-minute coordinate scaling in low-bandwidth messages:** Dividing Message 17, 22, 23, or 27 coordinates by $600{,}000$ instead of $600$ $\implies$ positions targets $1{,}000\times$ closer to the equator or prime meridian than their true geographic location.
- **Assuming all decoders assemble multi-sentence strings:** Passing raw NMEA lines directly to libraries like `libais` $\implies$ triggers unhandled decode errors; developers must provide separate NMEA reassembly layers when utilizing low-level C++ engines.
- **Uncontrolled memory growth in stateful fragment buffers:** Maintaining multi-sentence fragment buffers without strict TTL expiration $\implies$ leaks memory indefinitely when radio packet collisions prevent final fragments from arriving.
- **Silently dropping unhandled message types:** Utilizing older decoders that throw unhandled exceptions upon encountering Message 28 or modern ASM payloads $\implies$ causes unhandled crashes in continuous telemetry ingestion daemons.

## Key takeaways

- Open-source AIS software evolved from academic reverse-engineering and amateur radio projects to dismantle the barriers of proprietary, paywalled maritime marine standards.
- Brian C. Lane's `aisparser` (2006) established the foundational architecture for standalone C decoding libraries and multi-fragment state tracking.
- Kurt Schwehr's `noaadata` pioneered XML-driven code generation, while `libais` (created in April 2010 during the Deepwater Horizon response) provided the C++ performance engine powering modern maritime analytics.
- Eric S. Raymond's `gpsd` AIVDM driver and open documentation (`AIVDM.adoc`) established the de-facto global technical reference that enabled the modern multi-language decoding ecosystem.
- The SDR revolution—progressing from `gnuais` and `gr-ais` to `rtl-ais` and `AIS-catcher`—lowered the financial threshold of dual-channel coastal reception from thousands of dollars to under US$50.
- Decoders exhibit deep, silent discrepancies in Rate of Turn sentinels, 1/10-minute coordinate scaling, and non-standard payload padding; production pipelines must normalize these fields explicitly.
- Encoding AIS messages is mathematically and structurally more complex than decoding, requiring precise field quantization, non-linear ROT transformation, 6-bit ASCII armoring, and multi-fragment splitting.
- Modern memory-safe languages like Rust (`nmea-parser`, `ais`) and Go (`go-ais`) eliminate the buffer-overflow and memory-corruption risks inherent in processing unauthenticated radio streams with legacy C libraries.

## References

- Balduzzi, M., Pasta, A., Wilhoit, K. (2014). A Security Evaluation of AIS Automated Identification System. *Proceedings of the 30th Annual Computer Security Applications Conference* (ACSAC '14), 436–445. New York: ACM.
- Foster, N. (2011). *gr-ais: GNU Radio AIS receiver module*. https://github.com/bistromath/gr-ais. GPL-3.0-or-later.
- International Electrotechnical Commission (2015). *Maritime navigation and radiocommunication equipment and systems -- Automatic identification system (AIS) -- Part 1: AIS Base Stations -- Minimum operational and performance requirements, methods of testing and required test results* (IEC Standard No. 62320-1:2015, Ed. 2.0). Geneva: IEC.
- International Electrotechnical Commission (2016). *Maritime navigation and radiocommunication equipment and systems -- Digital interfaces -- Part 1: Single talker and multiple listeners* (IEC Standard No. 61162-1:2016, Ed. 5.0). Geneva: IEC.
- International Electrotechnical Commission (2018). *Maritime navigation and radiocommunication equipment and systems -- Automatic identification systems (AIS) -- Part 2: Class A shipborne equipment of the automatic identification system (AIS)* (IEC Standard No. 61993-2:2018, Ed. 3.0). Geneva: IEC.
- International Maritime Organization (2010). *Guidance on the Use of AIS Application-Specific Messages* (Circular SN.1/Circ.289). London: IMO.
- International Telecommunication Union (2001). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band* (Recommendation ITU-R M.1371-1). Geneva: ITU.
- International Telecommunication Union (2010). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band* (Recommendation ITU-R M.1371-4). Geneva: ITU.
- International Telecommunication Union (2014). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band* (Recommendation ITU-R M.1371-5). Geneva: ITU.
- International Telecommunication Union (2026). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band* (Recommendation ITU-R M.1371-6). Geneva: ITU.
- jvde-github (2021). *AIS-catcher: A multi-platform AIS receiver for SDR dongles*. https://github.com/jvde-github/AIS-catcher. GPL-3.0.
- Keen, K., Giardini, D. (2013). *rtl-ais: Real-time dual-channel software receiver for AIS using RTL-SDR*. https://github.com/dgiardini/rtl-ais. GPL-2.0.
- Lane, B. C. (2006). *AIS Parser SDK*. https://github.com/bcl/aisparser. 3-clause BSD.
- Nielsen, K., Danish Maritime Authority (2012). *AisLib: Java AIS processing library*. https://github.com/dma-ais/AisLib. Apache-2.0.
- Raymond, E. S., Schwehr, K. (2009). *AIVDM/AIVDO Protocol Decoding* (Version 1.58). https://gpsd.gitlab.io/gpsd/AIVDM.html.
- Richter, L. M. (2019). *pyais: Pure Python AIS message decoding and encoding library*. https://github.com/M0r13n/pyais. MIT.
- Schwehr, K. (2006). *noaadata: Python marine data research toolkit*. https://github.com/schwehr/noaadata. Apache-2.0.
- Schwehr, K. (2009). *ais-areanotice-py: Reference implementation of IMO SN.1/Circ.289 application-specific messages*. https://github.com/schwehr/ais-areanotice-py. Apache-2.0.
- Schwehr, K. (2010). *libais: C++ AIS decoding library with Python bindings*. https://github.com/schwehr/libais. Apache-2.0.
