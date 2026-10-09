# Chapter 60 — Malicious payloads and receiver robustness: can AIS crash things?

> **Part IX — Security.** A rigorous analysis of parser vulnerabilities, memory safety hazards, reassembly flaws, and hardening strategies across maritime AIS receivers, chartplotters, and aggregation pipelines.

**In this chapter.** You will learn how untrusted radio-frequency and network-ingested AIS streams interact with software parsers, chartplotters, and downstream operational bridge networks. We analyze the complete attack surface—from NMEA 0183 sentence tokenizers and 6-bit ASCII armoring decoders to multi-fragment state machines, binary Application-Specific Message (**ASM**) parsers, free-text field handlers, and chart rendering engines. You will examine real-world software flaws across open-source and commercial implementations (including `gpsd`, OpenCPN, `libais`, and marine Electronic Chart Display and Information Systems (**ECDIS**)), review fuzz testing methodologies using modern coverage-guided tools, and evaluate denial-of-service vectors stemming from message flooding and alarm storms. Finally, you will explore the international compliance frameworks governing maritime cyber resilience—specifically IEC 60945, IEC 61162-460, and IACS Unified Requirements E26 and E27—and apply a concrete hardening checklist to secure software pipelines against malicious inputs.

## 60.1 The software attack surface: from radio demodulation to chart renderer

An Automatic Identification System (**AIS**) transmission is an unauthenticated bitstream received over a broadcast radio link or ingested from an unauthenticated network socket ([Chapter 58](ch58-threat-model.md)). When an antenna intercepts a VHF Gaussian Minimum Shift Keying (**GMSK**) waveform on AIS 1 (161.975 MHz) or AIS 2 (162.025 MHz), the transceiver demodulates the signal, strips the preamble and start flag (`0x7E`), un-stuffs zeros, verifies the 16-bit High-Level Data Link Control (**HDLC**) Cyclic Redundancy Check (**CRC**), and formats the payload into an ASCII sentence conforming to IEC 61162-1 / NMEA 0183 ([Chapter 26](ch26-interfaces-and-logging.md)). From that moment, the untrusted data travels through multiple software tiers:

```
+-----------------------------------------------------------------------------+
| 1. RF Physical & Data Link Layer                                            |
|    - GMSK Demodulation -> Bit un-stuffing -> HDLC CRC-16 check              |
+-----------------------------------------------------------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------+
| 2. NMEA 0183 / IEC 61162-1 Sentence Framing Layer                           |
|    - Start delimiter ('!', '$') -> Comma tokenization                       |
|    - Field length validation -> Checksum XOR verification                   |
+-----------------------------------------------------------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------+
| 3. Armoring & Reassembly Layer                                              |
|    - 6-bit ASCII de-armoring -> Multi-fragment state machine                |
|    - Sequential message ID tracking -> Fill-bit alignment & truncation      |
+-----------------------------------------------------------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------+
| 4. Protocol Message Decoder Layer                                           |
|    - Message Type dispatcher (1-27) -> Fixed-field bit extraction           |
|    - Free-text 6-bit string decoding -> ASM bit unpacking (DAC / FI)       |
+-----------------------------------------------------------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------+
| 5. Application & Display Layer                                              |
|    - Track database state update -> Kinematic plausibility filtering        |
|    - CPA/TCPA alarm calculation -> ECDIS / Web SVG / OpenGL rendering       |
+-----------------------------------------------------------------------------+
```

Historically, maritime software assumed that serial inputs (RS-422 at 38,400 baud) originated from trusted local hardware. Today, low-cost Software-Defined Radios (**SDRs**), crowd-sourced aggregation feeds, and Ethernet bridge networks invalidate that assumption.

> **Threat model.**
> - **Primary Assets:** Memory integrity and execution control of navigation computers; availability of bridge target displays (ECDIS, Radar/ARPA); operational responsiveness of Vessel Traffic Services (**VTS**) consoles; integrity of global commercial aggregation pipelines.
> - **Threat Actors:** Remote actors transmitting malicious RF waveforms via SDR within VHF line of sight; hostile actors injecting synthesized NMEA streams into unauthenticated TCP/UDP aggregator feeds; compromised bridge network peripherals pivoting onto IEC 61162-450 Ethernet backbones.
> - **Attacker Capabilities:**
>   - *Synthesized RF broadcast:* Broadcasting malformed bit sequences designed to exploit parser flaws in transponder microcode, pilot plugs, or listening receivers.
>   - *Feed injection:* Transmitting high-rate malformed, deeply nested, or boundary-violating sentences into aggregator ingest ports.
>   - *Target state corruption:* Broadcasting crafted static text strings (Messages 5, 12, 14, 19, 21) or Application-Specific Messages (Messages 6, 8, 25, 26) containing shell metacharacters, format strings, SQL fragments, or oversized byte runs.
> - **Impact:** Process crash or kernel panic of shipboard ECDIS, rendering charts blank during hazardous navigation; arbitrary remote code execution (**RCE**); denial of service (**DoS**) via CPU exhaustion; alert desensitization via induced alarm storms.
> - **Mitigations:** Memory-safe parsing languages (Rust, Go) or fuzzed C/C++ libraries; strict state-machine reassembly timeouts; process sandboxing; enforcement of IEC 61162-460 firewalls between navigation and administrative networks.

### 60.1.1 The sentence tokenizer and delimiter vulnerabilities
The initial processing stage is the sentence tokenizer. Under IEC 61162-1 and NMEA 0183 v4.11, an AIS sentence begins with an ASCII exclamation mark (`!`) or dollar sign (`$`), followed by a two-character talker identifier (`AI` or `AB`), a three-character sentence formatter (`VDM` or `VDO`), comma-delimited fields, an asterisk delimiter (`*`), and a two-character hexadecimal XOR checksum (Raymond 2023aivdm).

A standard `!AIVDM` sentence exhibits seven comma-separated fields:
```
!AIVDM,count,num,seq,chan,payload,fill*hh<CR><LF>
```

Parsers implemented in C or C++ frequently use `strsep()`, `strtok()`, or pointer arithmetic. Common implementation failures at this entry point include:
- **Null-byte truncation and unterminated strings:** If the parser assumes a null-terminated string (`\0`) but the buffer delivers partial reads, missing line breaks (`<CR><LF>`), or embedded null bytes, standard string functions read off buffer ends.
- **Malformed delimiter sequences:** Consecutive commas (`!AIVDM,,,,,,*00`), missing asterisks, or extra delimiter tokens induce off-by-one errors when assigning field pointers.
- **Checksum validation bypass:** Many parsers skip checksum verification to tolerate noisy connections, allowing corrupted or truncated payloads to pass into deep decoding subroutines.

### 60.1.2 6-bit ASCII armoring: table boundaries and bit-shift bugs
AIS payloads cannot travel across serial lines as raw 8-bit binary because control bytes and reserved delimiters disrupt sentence framing. Recommendation ITU-R M.1371 and IEC 61162-1 specify 6-bit ASCII armoring ([Chapter 26](ch26-interfaces-and-logging.md)). Each ASCII character represents 6 bits. The mapping subtracts 48 from the ASCII byte; if greater than 40, an additional 8 is subtracted:
$$b = (c - 48) - ((c - 48 > 40) \ ? \ 8 : 0)$$

The legal armored character space consists of ASCII `0` through `W` (`0x30` to `0x57`), mapping to values 0 through 39, and ASCII `` ` `` through `w` (`0x60` to `0x77`), mapping to values 40 through 63. Characters between `0x58` (`X`) and `0x5F` (`_`), as well as bytes below `0x30` or above `0x77`, are strictly illegal.

When a parser unpacks armored characters into a bit buffer, severe vulnerabilities arise:
1. **Invalid table indexing:** Using raw character bytes as indices into a static 64-entry lookup table (`table[char]`) without bounds verification causes out-of-bounds reads on illegal characters or negative signed `char` conversions.
2. **Integer overflow during bit-packing:** Unpacking 6-bit chunks into machine words requires bitwise shifts (`<<`) and OR operations (`|`). On over-length payload strings, signed 16-bit accumulators tracking bit counts can overflow negative, bypassing downstream bounds checks.

### 60.1.3 Multi-fragment reassembly state machines
Single-slot AIS messages contain up to 168 payload bits, fitting within a single 82-character NMEA sentence. However, multi-slot transmissions—such as Message 5 (static/voyage data, 424 bits across 2 slots), Message 21 (AtoN, up to 360 bits), or multi-slot ASMs (Messages 6 and 8, up to 1,008 bits across up to 5 slots)—must be fragmented across up to five sequential sentences ([Chapter 23](ch23-asm-binary-payloads.md)).

The NMEA framing header manages fragmentation via `count` (total sentences, 1–9), `num` (current sequence number, 1–9), and `seq` (sequential message identifier, 0–9, or null for single sentences). Reassembling fragments requires a state machine that introduces distinct vulnerabilities:
- **Out-of-order and interleaved arrival:** Dual-channel receivers (AIS 1 and AIS 2) can receive fragments of different multi-part messages interleaved in time. A single global reassembly buffer corrupts both messages.
- **State exhaustion:** If an attacker broadcasts fragment 1 of 5 (`!AIVDM,5,1,3,A,...`) and never transmits fragments 2–5, decoders lacking reassembly timeouts retain partial buffers indefinitely, exhausting heap memory.
- **Index mismatch and buffer overflow:** Sizing buffers for expected length without validating that `num <= count`, or permitting `num == 0` (violating 1-based indexing), allows out-of-bounds buffer writes.

### 60.1.4 Application-Specific Messages (ASM) and dynamic binary decoding
Application-Specific Messages ([Chapter 23](ch23-asm-binary-payloads.md)) carry specialized binary payloads identified by a 16-bit Application Identifier (**AI**), comprising a 10-bit Designated Area Code (**DAC**) and a 6-bit Function Identifier (**FI**).

Because ASMs encode complex structures—such as meteorological and hydrographic data (IMO SN.1/Circ.289 FI 31) or regional waterway clearances—decoders unpack variable-width bitfields. If an incoming message reports an unknown DAC/FI, a robust parser must preserve the raw payload or return gracefully. Historical parsers frequently routed unknown DAC/FI combinations into generic decoders that assumed fixed lengths, causing buffer under-reads and null-pointer dereferences.

### 60.1.5 Free-text fields, control characters, and injection attacks
AIS carries human-readable text strings in Message 5 (names, call signs, destinations), Messages 12/14 (Safety-Related Messages), and Message 21 (AtoN names). Text fields use 6-bit ASCII defined by ITU-R M.1371 (Annex 2, Table 47), which cannot represent lowercase characters or control bytes below `0x20`.

However, when parsers unpack 6-bit text into C strings or JSON objects, critical vulnerabilities can emerge:
- **Missing null-terminators:** ITU-R M.1371 pads unused trailing characters with `@` symbols (`000000_2`). Parsers must strip trailing `@` padding and append an ASCII `\0`. If a decoder fails to insert the null terminator and copies the buffer via `strcpy()` or `printf("%s")`, adjacent memory leaks or stack corruption occurs.
- **Downstream injection:** When bridge displays, chartplotters, or web dashboards pass vessel names or destinations into shell commands, SQL queries, or HTML DOM elements, injection vulnerabilities manifest: SQL injection in tracking databases, Cross-Site Scripting (XSS) in web dashboards, or format string bugs in logging routines.

### 60.1.6 Downstream chart renderers and GUI rendering engines
Once decoded, target objects are passed to graphical display software—such as shipboard ECDIS, radar tracking displays, or open-source packages (e.g., OpenCPN). Rendering software maintains a spatial target list, calculating relative motion vectors, Closest Point of Approach (**CPA**), and Time to Closest Point of Approach (**TCPA**).

Target rendering engines present significant attack surfaces:
- **Geometric exceptions:** When targets assert radical coordinates—such as latitudes at $\pm 90^\circ$, coordinates wrapping across the International Date Line ($180^\circ \text{E/W}$), or invalid heading values ($511$)—unclamped Mercator projections or trigonometry trigger floating-point exceptions (`NaN`, divide-by-zero) or infinite GUI refresh loops.
- **Resource exhaustion:** Transmitting thousands of synthetic targets with erratic vectors forces rendering engines to recalculate vectors and repaint overlays dozens of times per second, freezing the user interface.

---

## 60.2 Known vulnerabilities and historical case studies

The vulnerability landscape of maritime navigation software has transitioned from academic theory into documented CVEs and industrial security findings. The historical track record shows that maritime parsers and navigation suites have repeatedly suffered from memory corruption and architectural fragility.

### 60.2.1 The GPSD daemon: CVE-2013-2038 and parsing robustness
`gpsd` is the standard open-source service daemon monitoring GPS receivers, AIS receivers, and marine sensors, translating hardware protocols into a consolidated JSON API. In May 2013, vulnerability analysis revealed a critical flaw in `gpsd`'s NMEA 0183 and AIS processing pipeline, designated as **CVE-2013-2038** (NVD 2013). 

The vulnerability resided in input validation routines when processing malformed sentences. Specifically, crafted packets lacking standard terminators or containing corrupted field sequences caused `gpsd` to enter an invalid state or execute an uncontrolled memory dereference, resulting in an immediate daemon crash (Denial of Service). Because `gpsd` forms the sensor ingestion backbone for Linux-based maritime appliances and coastal receiver stations, a crashing bug can be triggered remotely by transmitting malformed packets over RF or injecting them into network-accessible TCP/UDP ports. Following CVE-2013-2038, the `gpsd` maintainers systematically overhauled the AIVDM decoding architecture, incorporating strict boundary assertions and fuzzing harnesses (Raymond 2023aivdm).

### 60.2.2 OpenCPN: chartplotter vulnerabilities and CVE-2025-56814
OpenCPN is the leading open-source navigational chartplotter and bridge display application, deployed across thousands of commercial vessels, workboats, and recreational yachts. In early 2025, security researchers discovered a critical remote vulnerability in OpenCPN v5.12.0, tracked as **CVE-2025-56814** (NVD 2025). 

The flaw involved improper input sanitization and command injection within the application's underlying execution wrappers (`wxExecute()`). When processing unsanitized external strings, the application permitted shell metacharacters to break out of internal command contexts, allowing arbitrary command execution on the host operating system with the privileges of the active OpenCPN user. This vulnerability underscored the persistent hazard of passing untrusted external data into operating system execution routines without rigorous lexical filtering.

### 60.2.3 libais: memory safety and CVE-2026-56770
`libais` is a specialized, high-performance C++ decoding library (with Python bindings) authored by Kurt Schwehr, specifically engineered to decode ITU-R M.1371 messages and complex regional ASMs. Despite a robust architecture focused on strict bitfield extraction, the library's multi-fragment reassembly state machine in `VdmStream::AddLine` became the subject of security analysis, resulting in **CVE-2026-56770** (NVD 2026). 

The vulnerability centered on CWE-129 (Improper Validation of Array Index):
- When processing incoming multi-sentence `!AIVDM` fragments, `VdmStream::AddLine` parsed the sequential message identifier (the third field, `seq`).
- When presented with a crafted sentence containing an empty, invalid, or out-of-range sequential message identifier, internal indexing logic failed to validate the resulting slot index before accessing an internal `std::vector` of reassembly states.
- The resulting out-of-bounds vector access triggered immediate memory segmentation faults (`SIGSEGV`) and process termination.

This flaw demonstrated that even specialized, mathematically rigorous decoders are vulnerable to denial-of-service crashes if the state machine governing sentence reassembly does not treat every field in the NMEA envelope as untrusted input.

### 60.2.4 Commercial ECDIS and integrated bridge systems: Pen Test Partners research
Proprietary, type-approved commercial Electronic Chart Display and Information Systems (**ECDIS**) installed on SOLAS-mandated commercial ships suffer from systemic vulnerabilities that are frequently more severe than those found in open-source projects. Physical and reverse-engineering research conducted by cybersecurity consultancy **Pen Test Partners** on commercial type-approved ECDIS units revealed widespread structural deficiencies (Pen Test Partners 2020ecdis):
1. **Outdated operating systems:** Commercial ECDIS platforms in active service routinely run legacy operating systems—including Windows XP Embedded and Windows 7 Embedded—lacking modern OS-level exploit mitigations such as Address Space Layout Randomization (**ASLR**), Data Execution Prevention (**DEP**), or Control Flow Guard (**CFG**).
2. **Exposed maintenance interfaces:** Many commercial units leave local configuration utilities, USB service ports, and web-based administrative consoles unauthenticated or protected only by universal default passwords hardcoded in vendor manuals.
3. **Bridge serial-to-IP vulnerabilities:** Integrated bridge systems connect legacy RS-422 NMEA serial devices to Ethernet backbones via serial-to-IP terminal servers, broadcasting unencrypted UDP or TCP NMEA datagrams across bridge Local Area Networks (**LANs**).
4. **Input parsing failures in proprietary display software:** Proprietary chart display executables routinely fail to validate target buffer lengths. When fed oversized vessel names or malformed NMEA sentences, commercial ECDIS units crash completely, producing a blank screen or a frozen error dialog on the bridge console.

> **Case file.**
> Between 2017 and 2020, security researchers with Pen Test Partners demonstrated that commercial, type-approved ECDIS units from major marine manufacturers could be compromised directly through unauthenticated bridge interfaces and malicious NMEA sentence injection (Pen Test Partners 2020ecdis). 
> 
> By injecting crafted NMEA sentences simulating a vessel position offset into the bridge network, researchers caused an active ECDIS display to shift its own-ship plotted position by several hundred meters into an adjacent shipping lane. Crucially, because the ECDIS was configured to output sensor feedback back to the vessel's AIS transponder, the transponder immediately began re-broadcasting the false, offset position over VHF channels AIS 1 and AIS 2 to all surrounding vessels and coastal VTS radars. 
> 
> The researchers further demonstrated that by flooding the bridge network with malformed target sentences containing oversized character strings, they could trigger a total application crash of both the primary and secondary (backup) ECDIS units simultaneously. Because both units shared identical hardware, identical operating system images, and the same unsegmented network feed, the failure was instantaneous and total, leaving the bridge team without electronic charting in restricted waters.

---

## 60.3 Fuzzing maritime software: methodologies, harnesses, and corpora

Fuzz testing (fuzzing) feeds semi-random, malformed, and boundary-testing inputs into software to detect unhandled exceptions, memory corruption, assertion failures, and resource leaks. Securing an AIS ingestion pipeline requires targeted fuzzing across two distinct architectural boundaries:
1. **The Sentence Level:** Fuzzing the raw ASCII NMEA 0183 parser, delimiter tokenizer, checksum calculator, and fragment state machine.
2. **The Bitfield Level:** Fuzzing un-armored binary message decoders, field unpackers, and ASM application dispatchers.

Modern coverage-guided fuzzers—primarily **libFuzzer** and **AFL++**—compile target C/C++ code with compiler instrumentation measuring code block coverage in real time. When a generated input triggers an execution path through a previously unreached code branch, the engine saves that input into the mutation seed corpus.

```
+--------------------+      +--------------------+      +--------------------+
|  Seed Corpus       | ---> |  Mutation Engine   | ---> |  Target Parser     |
| (Valid AIVDM msgs) |      | (Bit-flips, inserts|      | (libFuzzer/AFL++)  |
+--------------------+      +--------------------+      +--------------------+
                                                                   |
          +--------------------------------------------------------+
          |
          v
+--------------------+      +--------------------+
|  Crash Detected?   | YES  |  Sanitizer Report  |
| (ASan/UBSan/MSan)  | ---> | (Heap buffer OOB,  |
+--------------------+      |  Null dereference) |
          | NO              +--------------------+
          v
+--------------------+
| New Code Coverage? | YES  +--------------------+
| (Edge transition)  | ---> | Add to Seed Corpus |
+--------------------+      +--------------------+
```

Fuzz targets must be compiled with LLVM Sanitizers: AddressSanitizer (ASan) to catch heap/stack out-of-bounds reads and use-after-free bugs; UndefinedBehaviorSanitizer (UBSan) for integer overflows and misaligned shifts; and MemorySanitizer (MSan) for uninitialized memory reads. 

**OSS-Fuzz** is Google's continuous fuzzing infrastructure for open-source software. The `gpsd` project was integrated into OSS-Fuzz to ensure continuous regression testing across its suite of hardware and protocol drivers. Specialized fuzz harnesses exercise the packet parser (`FuzzPacket`) and driver subsystems (`FuzzDrivers`), with every commit automatically built with sanitizers and fuzzed at scale.

> **Try it.**
> You can test how the `libais` parser installed in this repository handles malformed and boundary-violating inputs using Python. Run the following test script in your shell:
> 
> ```python
> import ais
> 
> # A valid Type 1 Position Report payload and fill bits
> valid_payload = "15N265001w>r=vHMg0wn5?wf0000"
> valid_fill = 0
> 
> print("Decoding valid Type 1 message:")
> res = ais.decode(valid_payload, valid_fill)
> print(f"  MMSI: {res['mmsi']}, SOG: {res['sog']:.1f} kn, Lat: {res['y']:.4f}, Lon: {res['x']:.4f}")
> 
> # Test boundary violations and invalid fill parameters
> test_cases = [
>     ("Truncated payload (1 character)", "1", 0),
>     ("Invalid fill bits (> 5)", valid_payload, 7),
>     ("Negative fill bits", valid_payload, -1),
>     ("Oversized payload (528 characters)", valid_payload + "w" * 500, 0),
>     ("Illegal characters (outside 6-bit armor)", "15N265001w???wf0000", 0),
> ]
> 
> print("\nTesting malformed inputs against libais:")
> for desc, payload, fill in test_cases:
>     try:
>         ais.decode(payload, fill)
>         print(f"  [UNEXPECTED SUCCESS] {desc}")
>     except Exception as e:
>         print(f"  [REJECTED] {desc} -> {type(e).__name__}: {e}")
> ```
> 
> **Expected output:**
> ```text
> Decoding valid Type 1 message:
>   MMSI: 367035924, SOG: 12.7 kn, Lat: 51.9650, Lon: 208.4522
> 
> Testing malformed inputs against libais:
>   [REJECTED] Truncated payload (1 character) -> DecodeError: Ais1_2_3: AIS_ERR_BAD_BIT_COUNT
>   [REJECTED] Invalid fill bits (> 5) -> DecodeError: Ais1_2_3: AIS_ERR_BAD_BIT_COUNT
>   [REJECTED] Negative fill bits -> DecodeError: Ais1_2_3: AIS_ERR_BAD_BIT_COUNT
>   [REJECTED] Oversized payload (528 characters) -> DecodeError: Ais1_2_3: AIS_ERR_MSG_TOO_LONG
>   [REJECTED] Illegal characters (outside 6-bit armor) -> DecodeError: ais.decode: unknown message -  
> ```

---

## 60.4 Denial of service: message flooding and alarm storms

Software exploitation does not require executing shellcode to endanger a vessel. Disabling a bridge display or overwhelming a bridge watchstander with sensory overload constitutes an equally hazardous operational denial of service.

### 60.4.1 RF slot starvation vs. software ingestion flooding
Denial of service against AIS manifests across two distinct domains:
1. **RF Physical Link Starvation:** At the radio frequency layer, an attacker using an SDR can broadcast high-power continuous carriers or transmit continuous dummy bursts across all 4,500 slots per minute of the Self-Organizing Time Division Multiple Access (**SOTDMA**) frame ([Chapter 21](ch21-link-layer-tdma.md); [Chapter 61](ch61-timing-and-network-attacks.md)), starving legitimate transponders of slot reservations.
2. **Software Ingestion Flooding:** At the network and parser layer, an attacker transmits an overwhelming volume of syntactically valid or semi-valid NMEA sentences into an AIS receiver port, chartplotter network daemon, or coastal aggregator.

An operational transponder serial interface operates at 38,400 baud, constraining throughput to approximately 3,840 bytes per second (~45 NMEA sentences/s). However, network-connected receivers and AIS-over-IP converters operate over 100 Mbps or 1 Gbps Ethernet (IEC 61162-450). If an attacker floods a chartplotter's UDP listening port with 50,000 NMEA sentences per second, software architectures that allocate heap memory per sentence or parse sentences synchronously on the main GUI thread experience instant resource exhaustion: socket buffers overflow, CPU utilization spikes to 100%, and GUI redraws freeze.

```
Attacker Flood: 50,000 pkts/s UDP
               |
               v
    [IEC 61162-450 Network]
               |
               v
+-------------------------------+
| Bridge Chartplotter / ECDIS   |
|                               |
|  - Socket Buffer: OVERFLOW    | ---> [Drops Legitimate Transponder Data]
|  - CPU Utilization: 100%      | ---> [GUI Redraw Freezes]
|  - Target Table: RAM Exhausted| ---> [Application Crashes / System Halts]
+-------------------------------+
```

### 60.4.2 The alarm storm attack: exploiting CPA/TCPA and Bridge Alert Management
Under IMO standards, ECDIS and marine radars must incorporate automated collision-alerting algorithms. When an incoming AIS target's projected trajectory violates predefined safety parameters—specifically Closest Point of Approach (**CPA**) and Time to Closest Point of Approach (**TCPA**)—the bridge system triggers an audible buzzer, a flashing red warning icon, and Bridge Alert Management (**BAM**) alert sentences (`!ALR` or IEC 62923-1 `!ALF`/`!ALC`).

An adversary can exploit this safety mechanism by broadcasting synthesized AIS targets configured specifically to trigger false collision emergencies (Balduzzi, Pasta & Wilhoit 2014; Trend Micro 2014ais).

```
+-----------------------------------------------------------------------------+
| Attacker synthesizes 100 phantom targets converging on Own-Ship Position   |
+-----------------------------------------------------------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------+
| Transmitted via SDR over VHF or injected into bridge NMEA feed              |
+-----------------------------------------------------------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------+
| Bridge ECDIS / Radar processes CPA / TCPA vectors                           |
|   - 100 simultaneous targets violate: CPA < 0.5 nmi, TCPA < 5 min           |
+-----------------------------------------------------------------------------+
                                       |
                                       v
+-----------------------------------------------------------------------------+
| BRIDGE ALARM STORM TRIGGERED                                                |
|   - 100 continuous audible alarms sound simultaneously                      |
|   - Bridge Alert Management system queue saturated                          |
|   - Watchstander experiences acute cognitive overload and alarm fatigue     |
|   - Watchstander silences or disables the alarm system entirely             |
+-----------------------------------------------------------------------------+
```

When 50 or 100 simulated phantom vessels suddenly appear on the display converging on own-ship, the bridge console erupts into continuous audible alarms. Under BAM requirements, the watch officer must individually acknowledge each alert on the console. The operational consequences are severe: cognitive saturation distracting from visual lookouts, alarm fatigue leading crews to silence collision alerting, and induced erratic maneuvering into shallow water or real traffic.

---

## 60.5 Standards, certification, and maritime cyber resilience

The vulnerability of shipboard navigation software to malformed inputs and network flooding led international regulatory bodies to develop binding cybersecurity standards for marine electronics.

### 60.5.1 IEC 60945 and IEC 61162-460
IEC 60945 (2002) governs general requirements and testing methods for marine avionics. Clause 4.4 specifies that software must avoid crashes due to operator errors or line noise, include automated recovery (watchdog timers restarting within 60 seconds), and retain critical parameters across restarts. 

To secure bridge Ethernet networks (IEC 61162-450), the IEC introduced **IEC 61162-460** (2020), which mandates:
- **Network Segmentation and 460-Gateways:** Critical navigational networks (Zone 1: ECDIS, Radar, Steering Control) must be isolated from administrative and communication networks (Zone 2/3) via certified **460-Gateways** or **460-Forwarders**.
- **Traffic Whitelisting & Inspection:** 460-Gateways enforce stateful packet filtering, permitting only authorized IEC 61162-450 multicast sentences and blocking unexpected UDP/TCP traffic.
- **Ingestion Rate Limiting:** Compliant interfaces enforce hardware- or kernel-level rate limiting on multicast streams to prevent network flooding from consuming CPU on listening displays.
- **Integrity Logging:** Security-relevant events (dropped malformed packets, unauthorized attempts, interface resets) are logged to tamper-resistant audit logs.

### 60.5.2 IACS Unified Requirements E26 and E27
In 2023, the International Association of Classification Societies (**IACS**) adopted two Unified Requirements that transformed maritime cybersecurity from voluntary guidance into mandatory condition-of-class requirements (IACS 2023e26; IACS 2023e27):

| Standard | Scope | Primary Target | Mandatory Requirements |
|---|---|---|---|
| **IACS UR E26** | Cyber resilience of the entire vessel | Shipyards, System Integrators, Shipowners | Holistic vessel architecture; Zones and Conduits design; network segmentation between OT and IT; incident recovery plans; mandated for vessels contracted after 1 July 2024. |
| **IACS UR E27** | Cyber resilience of on-board systems and equipment | Marine Equipment Manufacturers (OEMs) | Individual component security: secure boot, role-based access control, security event logging, robustness testing against malformed inputs (fuzzing), vulnerability disclosure processes. |

*Table 60.1: Summary of IACS Unified Requirements E26 and E27.*

Under **UR E27**, any navigation system submitted for class approval must demonstrate robustness against malformed and unexpected communication inputs. Manufacturers must subject protocol parsers to formal boundary testing (fuzzing) as part of type-approval certification.

---

## 60.6 Coordinated vulnerability disclosure in maritime systems

Reporting software vulnerabilities in the maritime sector has historically been fraught with friction due to multi-decade vessel lifecycles (25–30 years), statutory type-approval re-certification barriers (modifying certified binaries invalidates approvals under the European Marine Equipment Directive or USCG rules), and physical access constraints at sea.

To structure vulnerability reporting, security researchers and maritime vendors increasingly align with established international standards:
- **ISO/IEC 29147:2018:** *Information technology — Security techniques — Vulnerability disclosure*. Defines guidelines for vendors to receive, verify, and acknowledge vulnerability reports from external researchers, including the publication of advisories.
- **ISO/IEC 30111:2019:** *Information technology — Security techniques — Vulnerability handling processes*. Specifies internal operational procedures for engineering teams to investigate, triage, remediate, and verify security flaws.

Government agencies—notably the Cybersecurity and Infrastructure Security Agency (**CISA**) and national Computer Emergency Response Teams (**CERTs**)—act as intermediaries between independent researchers and marine electronics vendors to facilitate coordinated vulnerability disclosure (**CVD**).

> **Legal note.**
> Security auditing and vulnerability research on maritime radio and navigation systems are strictly governed by international and domestic criminal laws.
> - **Radio Transmission Laws:** In virtually all jurisdictions, transmitting unauthorized, synthesized, or spoofed AIS waveforms over the air across maritime VHF frequencies (161.975 MHz and 162.025 MHz) is a severe criminal offense under national telecommunications statutes (e.g., Title 47 of the United States Code / Communications Act of 1934; the UK Wireless Telegraphy Act 2006). Over-the-air testing risks interference with live safety-of-life maritime communications. All RF fuzzing and transmit research must be conducted exclusively inside RF-shielded enclosures (Faraday cages) or over direct, heavily attenuated coaxial cable loops connected directly to dummy loads.
> - **Computer Crime Statutes:** Injecting malformed packets into commercial vessel tracking APIs, coastal VTS receiver networks, or operational bridge Ethernet backbones without explicit, written authorization constitutes unauthorized computer access under laws such as the US Computer Fraud and Abuse Act (**CFAA**, 18 U.S.C. § 1030), the UK Computer Misuse Act 1990, and equivalent international statutes.
> - **Safe Harbor Research:** Legitimate security auditing must be performed strictly on privately owned, isolated test hardware, using coordinated disclosure frameworks conforming to ISO/IEC 29147 and CISA CVD guidelines.

---

## 60.7 The parser hardening checklist

Securing an AIS decoding pipeline against malicious payloads, crashes, and denial-of-service vectors requires defense-in-depth across the software engineering lifecycle. Software engineers and system integrators must enforce the following hardening checklist:

```
[ ] 1. Architectural Memory Safety
    [ ] Transition performance-critical decoders to memory-safe languages (Rust, Go)
        where possible.
    [ ] When implementing in C/C++, enforce compiler hardening:
        - Compile with -Wall -Wextra -Werror -pedantic
        - Enable stack protectors: -fstack-protector-strong
        - Enable FORTIFY_SOURCE=3
        - Enforce Position Independent Executables (-fPIE -pie) and Full RELRO (-Wl,-z,relro,-z,now)

[ ] 2. Sentence-Level Input Validation
    [ ] Enforce hard length limits on incoming raw sentences (maximum 82 characters).
    [ ] Verify NMEA XOR checksum before passing buffer to any tokenizer or parsing routine.
    [ ] Reject sentences containing invalid framing delimiters, consecutive commas,
        or unprintable ASCII characters.

[ ] 3. 6-Bit ASCII Armoring Hardening
    [ ] Verify that all payload characters fall strictly within legal armored ranges:
        ASCII 0x30..0x57 ('0'..'W') or 0x60..0x77 ('`'..'w').
    [ ] Explicitly reject illegal range 0x58..0x5F ('X'..'_') and characters < 0x30 or > 0x77.
    [ ] Validate fill-bit field value: must be an integer between 0 and 5 inclusive.

[ ] 4. Multi-Fragment State Machine Protection
    [ ] Enforce strict fragment sequence validation: current fragment number must strictly
        equal previous fragment + 1.
    [ ] Verify that total fragment count does not exceed protocol limits (maximum 5 for ASMs,
        maximum 2 for standard messages).
    [ ] Implement isolated, per-session reassembly pools keyed by (talker_id, channel, seq_id).
    [ ] Enforce strict reassembly timeouts (e.g., purge incomplete multi-fragment buffers
        after 1.5 seconds) to prevent state exhaustion attacks.
    [ ] Enforce a global cap on concurrent partial reassembly sessions.

[ ] 5. Protocol Message Unpacking
    [ ] Verify that total extracted bit count matches the exact expected bit length of the
        identified Message Type before field unpacking.
    [ ] Ensure bitfield extraction routines clamp bit-shifts to register boundaries (< 32 or < 64).
    [ ] For Application-Specific Messages (Messages 6, 8, 25, 26), safely reject or encapsulate
        unrecognized DAC/FI combinations without attempting fixed-field unpacking.

[ ] 6. Free-Text and String Sanitization
    [ ] Ensure 6-bit unpacked strings are explicitly null-terminated in destination buffers.
    [ ] Strip trailing '@' padding characters cleanly.
    [ ] Perform strict lexical encoding/escaping before forwarding text fields to downstream
        databases, web dashboards, or GUI renderers (prevent SQLi, XSS, and command injection).

[ ] 7. Ingestion Rate Limiting & Resource Quotas
    [ ] Implement token-bucket or sliding-window rate limiting on all incoming network sockets
        (drop bursts exceeding expected physical channel capacities).
    [ ] Restrict parser thread execution privileges via OS sandboxing (Linux seccomp-bpf,
        capsicum, or pledge).
    [ ] Isolate parsing processes into unprivileged system containers or non-root user accounts.

[ ] 8. Continuous Verification & Fuzzing
    [ ] Maintain continuous integration fuzz testing using libFuzzer / AFL++ integrated with
        AddressSanitizer and UndefinedBehaviorSanitizer.
    [ ] Curate and maintain a comprehensive seed corpus covering edge cases and historical crashers.
```

---

## Then & now

- **2002:** ⟨H⟩ IMO SOLAS carriage requirement for AIS enters into force; initial transponder software assumes benign serial input from honest navigators; physical hardware costs serve as the primary security barrier.
- **2004:** ⟨H⟩ IMO publishes SN/Circ.236 defining international Application-Specific Messages; early proprietary decoders hardcode fixed field lengths, crashing on undocumented binary payloads.
- **2010:** ⟨H⟩ IMO publishes SN.1/Circ.289 expanding ASM definitions; open-source decoders emerge without formal memory-safety auditing or boundary fuzzing.
- **2013:** ⟨+⟩ Trend Micro researchers (Balduzzi, Wilhoit, Pasta) present "AIS Exposed" at Hack in the Box Kuala Lumpur, demonstrating RF packet injection, software crashes, and protocol manipulation using low-cost SDR hardware (Balduzzi, Pasta & Wilhoit 2014).
- **2013:** ⟨+⟩ Vulnerability CVE-2013-2038 disclosed in `gpsd`, highlighting remote denial-of-service vulnerabilities in maritime sensor and AIS parsing routines.
- **2016:** ⟨+⟩ IEC publishes IEC 61162-450 establishing high-speed Ethernet interconnection on ship bridges; bridge networks transition from isolated serial lines to shared IP backbones.
- **2018:** ⟨+⟩ Google OSS-Fuzz integrates `gpsd` for continuous coverage-guided fuzz testing, automating memory corruption detection across maritime sentence parsers.
- **2020:** ⟨+⟩ IEC releases IEC 61162-460, mandating security gateways, traffic isolation, and stateful packet filtering for Ethernet-connected bridge navigation systems.
- **2020:** ⟨+⟩ Pen Test Partners publishes research demonstrating complete compromise, position spoofing, and application crashes on commercial type-approved ECDIS units via unauthenticated bridge NMEA interfaces (Pen Test Partners 2020ecdis).
- **2024:** ⟨+⟩ IACS Unified Requirements E26 and E27 enter into force for newbuild vessels on 1 July 2024, mandating formal cybersecurity resilience, secure development lifecycles, and software robustness testing across onboard computer systems and marine electronics.
- **2025:** ⟨+⟩ Vulnerability CVE-2025-56814 disclosed in OpenCPN v5.12.0, revealing command execution hazards when external inputs interact with chartplotter system execution layers.
- **2026:** ⟨+⟩ Vulnerability CVE-2026-56770 disclosed in `libais`, demonstrating out-of-bounds memory indexing hazards during multi-fragment NMEA reassembly.

---

## On the wire

To understand how parser vulnerabilities manifest, we examine the precise byte-level and bit-level composition of incoming NMEA 0183 sentences, 6-bit armored payloads, and multi-fragment reassembly sequences.

### 60.8.1 The Anatomy of an Armored Sentence
Consider an authentic single-fragment Type 1 Position Report received over the air:

```text
!AIVDM,1,1,,B,15N265001w>r=vHMg0wn5?wf0000,0*1B
```

Breaking down each field on the wire:
1. `!`: Start of sentence delimiter (ASCII `0x21`).
2. `AIVDM`: Talker identifier `AI` + sentence formatter `VDM` (received VHF Data Link message).
3. `1`: Total number of sentences in this message sequence ($count = 1$).
4. `1`: Sentence number of this sequence ($num = 1$).
5. `` (null): Sequential message identifier ($seq = \text{null}$; omitted for single-sentence messages).
6. `B`: Radio channel on which the packet was received (Channel B = 162.025 MHz).
7. `15N265001w>r=vHMg0wn5?wf0000`: Armored 6-bit data payload (28 characters = 168 bits).
8. `0`: Number of fill bits ($fill = 0$; payload bit count is an exact multiple of 6).
9. `*1B`: Checksum delimiter (`*`) followed by the two-digit hexadecimal XOR checksum (`1B`).

### 60.8.2 Hexadecimal Checksum Calculation
The checksum validates transmission integrity across the physical line. It is computed as the bitwise XOR of the 8-bit ASCII values of all characters strictly between the starting `!` (or `$`) and the terminating `*`:

$$\text{Checksum} = \bigoplus_{i=1}^{L} \text{ASCII}(c_i)$$

For the sentence above, the characters covered are:
`A I V D M , 1 , 1 , , B , 1 5 N 2 6 5 0 0 1 w > r = v H M g 0 w n 5 ? w f 0 0 0 0 , 0`

Calculating the running XOR:
- `'A'` ($0x41$) $\oplus$ `'I'` ($0x49$) = $0x08$
- $0x08$ $\oplus$ `'V'` ($0x56$) = $0x5E$
- Continuing across all 40 characters yields the exact byte $0x1B$, represented in ASCII hex as `1B`. A parser that skips this check will ingest corrupted sentences whose field delimiters may be misaligned.

### 60.8.3 6-Bit De-Armoring Walk-Through
Each character in the 28-character payload represents 6 bits. Tracing the first four characters: `'1'`, `'5'`, `'N'`, `'2'`:

| Character | ASCII Hex | ASCII Dec | Conversion Formula | 6-Bit Value (Dec) | 6-Bit Binary | Extracted Protocol Bits |
|---|---|---|---|---|---|---|
| `'1'` | `0x31` | 49 | $49 - 48 = 1$ | 1 | `000001` | Bits 0..5 (Message Type) |
| `'5'` | `0x35` | 53 | $53 - 48 = 5$ | 5 | `000101` | Bits 6..11 (Repeat & MMSI high) |
| `'N'` | `0x4E` | 78 | $78 - 48 = 30$ | 30 | `011110` | Bits 12..17 (MMSI mid) |
| `'2'` | `0x32` | 50 | $50 - 48 = 2$ | 2 | `000010` | Bits 18..23 (MMSI mid) |

Unpacking the resulting 24-bit stream:
$$\text{Bitstream} = \underbrace{000001}_{\text{'1'}} \ \underbrace{000101}_{\text{'5'}} \ \underbrace{011110}_{\text{'N'}} \ \underbrace{000010}_{\text{'2'}} = 000001000101011110000010_2$$

Extracting message header fields:
- **Message Type (Bits 0..5):** $000001_2 = 1$ (Type 1: Scheduled Class A Position Report).
- **Repeat Indicator (Bits 6..7):** $00_2 = 0$ (Default, no repeat).
- **MMSI (Bits 8..37):** Starts with bits 8..23 ($0101011110000010_2$). Continuing through the full payload extracts MMSI `367035924`.

### 60.8.4 Worked Example: Multi-Fragment Reassembly Failure and Out-of-Bounds Indexing
To observe how CVE-2026-56770 manifests on the wire, consider a malicious multi-fragment sequence designed to exploit index validation in `VdmStream::AddLine`:

```text
!AIVDM,2,1,,B,55?43:02>d1w<h`00000000000000000000000160000000000000000,0*34
```

Here, an attacker transmits fragment 1 of 2 for a Message 5 static report. Field 3 (`seq`) is empty (`,,`).
Under IEC 61162-1, multi-fragment sentences **must** contain a sequential message identifier (`1` to `9`) so the receiver can correlate fragments. When the parser encounters an empty `seq` token:
1. The parser initializes `seq_id` to a sentinel value (e.g., `-1`).
2. The code attempts to index an internal state array: `session = reassembly_sessions[seq_id]`.
3. In C++, accessing `std::vector::operator[]` with a negative signed integer or an unchecked cast to unsigned integer (`static_cast<size_t>(-1) = 18446744073709551615`) attempts to dereference memory far outside heap bounds.
4. The kernel intercepts the invalid page access and immediately kills the process with `SIGSEGV` (signal 11), crashing the AIS ingestion pipeline.

---

## Validation, uncertainty & data quality

In a hostile or noisy communications environment, distinguishing between genuine atmospheric bit corruption and deliberate malicious payload injection requires structured validation procedures.

### 60.9.1 Error taxonomy: physical noise vs. adversarial injection
Errors encountered by an AIS parser originate from three distinct mechanisms:

| Error Mechanism | Root Cause | Typical Signature | Parser Behavior |
|---|---|---|---|
| **Thermal RF Noise & Multipath** | Atmospheric fading, weak signal, co-channel interference | Flipped bits; fails 16-bit HDLC CRC at transceiver level; discarded before NMEA generation. | Dropped by hardware baseband. |
| **Serial / Baud Rate Mismatch** | Framing errors on RS-422 line, electrical noise, buffer overruns | Truncated strings, missing `<CR><LF>`, random unprintable ASCII bytes. | Rejected by NMEA sentence framing & XOR checksum check. |
| **Adversarial Payload Injection** | Deliberately synthesized RF waveform or injected network packet | Valid NMEA framing, perfect XOR checksum, valid 6-bit armor, but contains boundary-violating bit lengths, invalid DAC/FI, or memory exploit tokens. | **Bypasses transport checks; targets application logic.** |

*Table 60.2: Comparison of physical transmission errors and adversarial payloads.*

### 60.9.2 Concrete validation procedure
To achieve high data quality and ensure receiver robustness, every incoming sentence must traverse a strict five-stage validation pipeline:

```
[Raw Serial/Socket Stream]
             |
             v
[Stage 1: Envelope Validation]
  - Length check: 10 <= len <= 82 bytes
  - Delimiter check: Starts with '!' or '$', ends with <CR><LF>
  - Checksum check: Recompute XOR between delimiter and '*' -> Match?
             | (PASS)
             v
[Stage 2: Armoring & Lexical Validation]
  - Token count: Exactly 7 comma-separated fields
  - Fill bit check: 0 <= fill <= 5
  - Payload alphabet: Every byte in [0x30..0x57] or [0x60..0x77]
             | (PASS)
             v
[Stage 3: State-Machine Reassembly]
  - If count == 1: Bypass reassembly
  - If count > 1: Validate 1 <= num <= count <= 5; Validate seq in [0..9]
  - Session lookup: Match (talker, channel, seq) within 1.5 s window
             | (PASS: Complete bitstream assembled)
             v
[Stage 4: Bitfield Structural Validation]
  - Bit length check: (char_count * 6) - fill == expected_message_bits
  - MMSI sanity check: 200000000 <= MMSI <= 775999999 (or valid AtoN/SAR MID)
  - Range clamping: Clamping coordinates (-90 to +90, -180 to +180)
             | (PASS)
             v
[Stage 5: Kinematic Plausibility Validation]
  - Acceleration check: Speed change < 10 kn/s
  - Velocity check: Speed over ground < 60 kn (displacement) / < 102.2 kn (planing)
  - Position continuity: Distance delta / time delta <= Max vessel speed
```

### 60.9.3 Quantitative error metrics and reporting
Robust receiving stations and shore aggregators must compute and expose continuous data quality metrics:
- **Packet Drop Ratio ($PDR$):**
  $$PDR = \frac{N_{\text{corrupt}} + N_{\text{dropped}}}{N_{\text{total}}} \times 100\%$$
  Under benign conditions, $PDR$ over serial links is $< 0.01\%$. A sudden surge in $PDR$ exceeding $5\%$ indicates active serial line degradation or an ongoing packet flooding attack.
- **Malformed Sentence Rate ($MSR$):** The number of sentences failing Stage 1 or Stage 2 validation per minute. In clean operational environments, $MSR = 0$. Any sustained non-zero value should trigger an administrative security audit.
- **Orphan Fragment Ratio ($OFR$):** The ratio of uncompleted multi-fragment reassembly sessions to total multi-fragment messages:
  $$OFR = \frac{N_{\text{expired\_sessions}}}{N_{\text{fragment\_sequences}}} \times 100\%$$
  An $OFR > 2\%$ indicates either severe RF packet loss on one radio channel or an intentional state-exhaustion denial-of-service attack.

---

## Software

### Open source
- **`libais` (v0.17):** A C++ library with Python bindings for decoding ITU-R M.1371 AIS messages and regional binary ASMs. Provides high decoding throughput and comprehensive message support. *Caveat:* Multi-fragment reassembly in `VdmStream` historically required careful state-index validation (e.g., CVE-2026-56770).
- **`gpsd` (v3.25):** The standard Linux GPS and maritime sensor management service daemon. Features robust NMEA 0183 and AIVDM sentence parsers continuously audited via Google OSS-Fuzz. *Caveat:* Runs as a monolithic multi-protocol daemon, meaning a parser flaw in an auxiliary driver can compromise the core service.
- **OpenCPN (v5.10+):** The premiere open-source chartplotter and navigational display suite. Provides interactive AIS target plotting, CPA/TCPA calculations, and collision alerting. *Caveat:* Extensive C++ codebase with complex GUI execution wrappers that require vigilant maintenance against command injection and rendering stalls (e.g., CVE-2025-56814).
- **`pyais` (v2.x):** A pure-Python AIS decoding library with full support for standard messages and multi-part sentence reassembly. Highly readable and memory-safe due to Python's runtime environment. *Caveat:* Significantly lower decoding throughput compared to compiled C/C++ libraries, making it susceptible to CPU starvation under high-volume sentence flooding.

### Free but closed
- **Bonaire AIS Dispatcher:** A widely used utility for receiving, filtering, and multiplexing NMEA AIS UDP/TCP data streams between receivers and shore servers. *Caveat:* Proprietary binary without public source code; security updates and fuzz testing coverage cannot be independently verified.

### Commercial
- **Wärtsilä Navi-Sailor / Transas ECDIS:** Industry-standard type-approved commercial ECDIS platform installed across international commercial merchant fleets. Provides integrated navigation, radar overlay, and AIS target tracking. *Caveat:* Proprietary embedded software ecosystem with lengthy patch deployment cycles subject to statutory type-approval re-certification.
- **Furuno FEA / FMD ECDIS Series:** High-reliability commercial integrated navigation systems conforming to IMO carriage requirements. *Caveat:* Relies on tightly integrated proprietary bridge networks; firmware updates require authorized service technician attendance in port.

---

## Standards & guides

- **International Telecommunication Union (2014):** *Recommendation ITU-R M.1371-5: Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile frequency band*. Governs physical, link, and message layer structures across the maritime VHF data link.
- **International Electrotechnical Commission (2002):** *IEC 60945:2002: Maritime navigation and radiocommunication equipment and systems — General requirements — Methods of testing and required test results*. Governs general environmental, operational, and software robustness baselines for marine avionics.
- **International Electrotechnical Commission (2016):** *IEC 61162-1:2016: Maritime navigation and radiocommunication equipment and systems — Digital interfaces — Part 1: Single talker and multiple listeners*. Governs NMEA 0183 serial sentence framing, field formatting, and checksum calculations.
- **International Electrotechnical Commission (2018):** *IEC 61162-450:2018: Maritime navigation and radiocommunication equipment and systems — Digital interfaces — Part 450: Multiple talkers and multiple listeners — Ethernet interconnection*. Governs high-speed multicast sentence transmission over shipboard Ethernet backbones.
- **International Electrotechnical Commission (2020):** *IEC 61162-460:2020: Maritime navigation and radiocommunication equipment and systems — Digital interfaces — Part 460: Multiple talkers and multiple listeners — Ethernet interconnection — Safety and security*. Mandates security gateways, network isolation, rate limiting, and traffic filtering between bridge navigation zones.
- **International Association of Classification Societies (2023):** *IACS Unified Requirement E26 Rev.1: Cyber resilience of ships*. Establishes mandatory ship-wide cybersecurity integration and zone segmentation for newbuild vessels contracted on or after 1 July 2024.
- **International Association of Classification Societies (2023):** *IACS Unified Requirement E27 Rev.1: Cyber resilience of on-board systems and equipment*. Mandates product-level cyber resilience, secure development lifecycles, and malformed input robustness testing for all onboard marine electronics.
- **International Organization for Standardization & International Electrotechnical Commission (2018):** *ISO/IEC 29147:2018: Information technology — Security techniques — Vulnerability disclosure*. Establishes international standards for coordinated vulnerability reporting between researchers and vendors.
- **International Organization for Standardization & International Electrotechnical Commission (2019):** *ISO/IEC 30111:2019: Information technology — Security techniques — Vulnerability handling processes*. Establishes international guidelines for vendor vulnerability triage, investigation, and patch lifecycle management.

---

## Pitfalls

- **Skipping NMEA checksum verification:** Disabling XOR checksum validation to accommodate poor connections $\rightarrow$ allows truncated, noise-corrupted, or deliberately manipulated sentences to reach deep parsing logic $\rightarrow$ always compute and enforce the two-character hexadecimal checksum prior to field extraction.
- **Assuming null-terminated inputs:** Relying on `\0` string terminators when reading from serial or network buffers $\rightarrow$ partial reads or embedded nulls cause `strtok()` or `strcpy()` to read out of bounds $\rightarrow$ enforce explicit length limits and use bounded memory functions (`snprintf`, `strlcpy`).
- **Unchecked array indexing during ASCII de-armoring:** Directly indexing a 64-element decoding table using the raw input character code $\rightarrow$ characters outside legal ranges or negative signed characters cause out-of-bounds heap/stack reads $\rightarrow$ strictly validate that characters fall within `0x30..0x57` or `0x60..0x77` before table lookup.
- **Global reassembly buffers for multi-fragment sentences:** Using a single global buffer to reassemble multi-part messages $\rightarrow$ dual-channel reception (AIS 1 and AIS 2) or multiple transmitters interleave fragments, corrupting messages $\rightarrow$ isolate reassembly state machines into sessions keyed by talker ID, channel, and sequence ID.
- **Unbounded state machine timeouts:** Maintaining incomplete multi-fragment buffers indefinitely while waiting for missing fragments $\rightarrow$ an attacker transmitting orphan fragment 1s exhausts host memory $\rightarrow$ enforce strict reassembly timeouts (e.g., 1.5 seconds) and cap maximum concurrent reassembly contexts.
- **Passing unsanitized text to downstream shells or databases:** Forwarding 6-bit unpacked strings directly into shell commands, SQL queries, or web GUIs $\rightarrow$ allows command injection, SQL injection, or Cross-Site Scripting $\rightarrow$ sanitize, escape, and parameterize all external string inputs before consumption.
- **Synchronous network ingestion on GUI display threads:** Processing incoming NMEA network streams directly on the primary chart rendering thread $\rightarrow$ high-volume UDP packet floods freeze screen redraws and lock user controls $\rightarrow$ decouple network I/O and protocol decoding onto background worker threads with bounded input queues.
- **Unclamped geographic coordinates in chart renderers:** Passing raw coordinates directly to trigonometric projection algorithms without range validation $\rightarrow$ invalid coordinates ($\pm 91^\circ$ or $181^\circ$) trigger floating-point exceptions (`NaN`, divide-by-zero) or infinite GUI refresh loops $\rightarrow$ clamp coordinates strictly to $[-90.0, +90.0]$ and $[-180.0, +180.0]$ before projection.
- **Permitting arbitrary fill-bit values:** Accepting fill-bit fields greater than 5 $\rightarrow$ induces bit-shift underflows or negative bit lengths during payload unpacking $\rightarrow$ enforce strict validation: $fill \in [0, 5]$.
- **Failing to rate-limit bridge network traffic:** Connecting unauthenticated serial-to-Ethernet forwarders directly to bridge navigation LANs without 460-Gateways $\rightarrow$ exposes critical ECDIS units to broadcast packet storms and denial-of-service crashes $\rightarrow$ install certified IEC 61162-460 filtering gateways between operational zones.

---

## Key takeaways

- **AIS is an untrusted bitstream:** Operating without transport encryption or cryptographic authentication, every byte received over VHF radio or network feeds must be treated as hostile input.
- **The parser attack surface is multi-tiered:** Security vulnerabilities span NMEA sentence tokenization, 6-bit ASCII armoring, multi-fragment state machine reassembly, binary ASM decoding, and GUI chart rendering.
- **Real-world systems have suffered memory and injection flaws:** Documented vulnerabilities across `gpsd` (CVE-2013-2038), OpenCPN (CVE-2025-56814), `libais` (CVE-2026-56770), and commercial ECDIS units confirm that maritime navigation software is vulnerable to crashes and remote exploitation.
- **Denial of service endangers life at sea:** Ingestion floods can freeze chartplotter displays, while crafted phantom targets can trigger bridge alarm storms, inducing severe cognitive fatigue or causing crews to disable collision alerting.
- **Fuzzing is an engineering prerequisite:** Coverage-guided fuzzing with libFuzzer or AFL++, combined with LLVM AddressSanitizer and UndefinedBehaviorSanitizer, is essential to discover boundary-violating defects before deployment.
- **IACS UR E26 and E27 mandate cyber resilience:** Ships contracted after 1 July 2024 must enforce network zone segmentation and equipment-level robustness against malformed communication inputs.
- **RF testing must remain shielded:** Over-the-air transmission of spoofed or malformed AIS waveforms violates international radio regulations and endangers maritime safety; all active testing must occur inside Faraday enclosures or over closed coaxial lines.
- **Hardening requires defense in depth:** Securing maritime ingestion pipelines demands strict length checks, bounded tokenizers, isolated reassembly state machines, rigorous string sanitization, and architectural network rate limiting.

---

## References

- Balduzzi, M., Pasta, A. & Wilhoit, K. (2014). A Security Evaluation of AIS Automated Identification System. *Proceedings of the 30th Annual Computer Security Applications Conference (ACSAC '14)*, 436–445. doi:10.1145/2664243.2664257
- Balduzzi, M., Wilhoit, K. & Pasta, A. (2014). *A Security Evaluation of AIS: A Weak Link in Maritime Security?* (Research White Paper). Tokyo: Trend Micro Inc. https://documents.trendmicro.com/assets/white_papers/wp-a-security-evaluation-of-ais.pdf
- Goudossis, A. & Katsikas, S. K. (2019). Towards a secure maritime architecture: A survey of security vulnerabilities in maritime communications. *International Journal of Information Security*, 18(6):767–787. doi:10.1007/s10207-019-00438-6
- International Association of Classification Societies (2023). *IACS Unified Requirement E26: Cyber resilience of ships* (Rev.1). London: IACS.
- International Association of Classification Societies (2023). *IACS Unified Requirement E27: Cyber resilience of on-board systems and equipment* (Rev.1). London: IACS.
- International Electrotechnical Commission (2002). *IEC 60945:2002: Maritime navigation and radiocommunication equipment and systems — General requirements — Methods of testing and required test results*. Geneva: IEC.
- International Electrotechnical Commission (2016). *IEC 61162-1:2016: Maritime navigation and radiocommunication equipment and systems — Digital interfaces — Part 1: Single talker and multiple listeners*. Geneva: IEC.
- International Electrotechnical Commission (2018). *IEC 61162-450:2018: Maritime navigation and radiocommunication equipment and systems — Digital interfaces — Part 450: Multiple talkers and multiple listeners — Ethernet interconnection*. Geneva: IEC.
- International Electrotechnical Commission (2020). *IEC 61162-460:2020: Maritime navigation and radiocommunication equipment and systems — Digital interfaces — Part 460: Multiple talkers and multiple listeners — Ethernet interconnection — Safety and security*. Geneva: IEC.
- International Organization for Standardization & International Electrotechnical Commission (2018). *ISO/IEC 29147:2018: Information technology — Security techniques — Vulnerability disclosure*. Geneva: ISO/IEC.
- International Organization for Standardization & International Electrotechnical Commission (2019). *ISO/IEC 30111:2019: Information technology — Security techniques — Vulnerability handling processes*. Geneva: ISO/IEC.
- International Telecommunication Union (2014). *Recommendation ITU-R M.1371-5: Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile frequency band*. Geneva: ITU.
- Kessler, G. C., Craiger, J. P. & Haass, J. (2018). A taxonomy of maritime cybersecurity vulnerabilities, risks, and mitigations. *The Journal of Ocean Technology*, 13(4):16–29.
- National Vulnerability Database (2013). *CVE-2013-2038 Detail: GPSD NMEA0183 / AIS Denial of Service Vulnerability*. NIST National Vulnerability Database. https://nvd.nist.gov/vuln/detail/CVE-2013-2038
- National Vulnerability Database (2025). *CVE-2025-56814 Detail: OpenCPN Command Injection Vulnerability*. NIST National Vulnerability Database. https://nvd.nist.gov/vuln/detail/CVE-2025-56814
- National Vulnerability Database (2026). *CVE-2026-56770 Detail: libais Out-of-Bounds Vector Access Vulnerability*. NIST National Vulnerability Database. https://nvd.nist.gov/vuln/detail/CVE-2026-56770
- Pen Test Partners (2020). *Hacking ECDIS: Navigational Systems and Bridge Network Compromise*. Pen Test Partners Maritime Cyber Security Research. https://www.pentestpartners.com/security-blog/hacking-ecdis/
- Raymond, E. S. (2023). *AIVDM/AIVDO Protocol Decoding* (Version 1.58). GPSD Project Documentation. https://gpsd.gitlab.io/gpsd/AIVDM.html
