# Chapter 33 — Hardware and SDR for receive and transmit

> **Part V — Radio.** The physical architecture, RF silicon, commercial transponder ecosystem, software-defined radio pipelines, and statutory type-approval regimes that translate marine AIS between digital bits and VHF electromagnetic waves.

**In this chapter.** You will learn how Automatic Identification System (**AIS**) hardware is engineered, manufactured, regulated, and decoded across commercial maritime, dedicated receiver, and software-defined radio (**SDR**) platforms. We examine the commercial Original Equipment Manufacturer (**OEM**) landscape, revealing how a small cadre of technology houses—most notably SRT Marine Systems—supplies core RF modules, transceivers, and firmware rebranded across global consumer and commercial marine marques. We dissect dedicated receiver architectures based on integrated sub-gigahertz transceivers such as the Silicon Labs Si4362, tracing the signal path through hardware filtering, Gaussian Minimum Shift Keying (**GMSK**) demodulation, Non-Return-to-Zero Inverted (**NRZI**) decoding, and High-Level Data Link Control (**HDLC**) deframing. We survey SDR receiver hardware and the lineage of open-source demodulators from early discriminator-audio decoders to multi-algorithm engines like AIS-catcher. We analyze transmit-capable SDR tools and their critical security implications under strict regulatory boundaries. Finally, we provide step-by-step procedures for navigating Federal Communications Commission (**FCC**) equipment authorization exhibits to conduct non-destructive RF hardware teardowns and evaluate statutory type approval.

## 33.1 The transponder market and the OEM supply chain

To an observer perusing a marine electronics catalog, the AIS transponder marketplace appears vast and fragmented. Dozens of brands—including Raymarine, Simrad, B&G, Lowrance, McMurdo, Ocean Signal, ACR Electronics, Digital Yacht, Comar Systems, and Si-Tex—offer lines of Class A and Class B transponders.

However, an examination of underlying RF hardware and statutory regulatory filings reveals that the supply chain is highly concentrated. Designing, certifying, and manufacturing an AIS transponder requires specialized RF engineering expertise and capital-intensive compliance testing. Consequently, the commercial market relies heavily on a handful of specialized design houses that develop turnkey transceiver platforms, which are subsequently packaged, white-labeled, and distributed by retail marques.

### 33.1.1 SRT Marine Systems and turnkey white-labeling

The dominant supplier of turnkey AIS transponder modules and white-label platforms across commercial and recreational marine sectors is **SRT Marine Systems plc** (formerly Software Radio Technology), based in Midsomer Norton, Bath, United Kingdom. SRT's corporate architecture divides into *Systems* (delivering coastal surveillance infrastructure to coast guards and fishery protection authorities) and *Transceivers* (manufacturing core AIS radio hardware).

On its commercial transceivers portal, SRT describes its business model:
> "Select from our standard OEM product platforms which are easily rebranded and certified under your own name."

In addition to ready-to-brand transponders, SRT manufactures surface-mount transceiver modules soldered directly onto host motherboards, enabling manufacturers to integrate certified AIS capability into multi-function displays (**MFD**), marine VHF radiotelephones, uncrewed surface vessels (**USV**), and nanosatellites. 

To serve the retail market directly, SRT operates its own retail brand, **em-trak Marine Electronics**, supported by a global dealer network of over 4,000 reseller partners. When an electronics brand desires an AIS transponder without investing years in discrete RF design and environmental qualification, it licenses an SRT core engine. The exterior plastics and connectors may be customized, but the core printed circuit board (**PCB**), frequency synthesizer, power amplifier, baseband processor, and core firmware originate in Somerset.

### 33.1.2 Independent design houses and integrated manufacturers

While SRT accounts for a substantial fraction of white-labeled Class B and light-commercial Class A units, several independent engineering houses maintain proprietary transponder designs:

- **Saab TransponderTech (Sweden):** Direct technological lineage of Håkan Lans and Swedish GP&C trials of the 1990s (see [Chapter 9](ch09-prehistory-and-stdma.md) and [Chapter 10](ch10-standardization-1996-2004.md)). Saab designs high-reliability Class A transponders, base stations, and airborne tracking systems (Saab R4 and R5) in-house.
- **Kongsberg Maritime (Norway):** Develops high-specification Class A transponders (Kongsberg AIS 300) and coastal base stations for dynamic positioning and offshore vessels.
- **Furuno Electric and Japan Radio Company (JRC) (Japan):** Bridge integration giants developing proprietary Class A transponders (Furuno FA-170, JRC JHS-183) for Integrated Navigation Systems (**INS**), radar consoles, and Electronic Chart Display and Information Systems (**ECDIS**).
- **Alltek Marine Electronics Corp. (AMEC) (Taiwan):** Engineers finished products (Camino Class A, WideLink Class B) and OEM modules supplied to regional marine brands.
- **Vesper Marine / Garmin (New Zealand / USA):** Vesper pioneered low-power Class B transponders and smartAIS. In 2020, Vesper launched *Cortex*, an integrated VHF, Class B SOTDMA transponder, and remote monitoring hub. On January 3, 2022, Garmin acquired Vesper Marine, utilizing its proprietary core to drive Garmin's transponder lines.
- **Weatherdock AG (Germany) and True Heading (Sweden):** European specialist houses developing proprietary Class B transponders, personal AIS search and rescue locator beacons (**AIS-MOB**), and Aids to Navigation (**AtoN**) transceivers.

### 33.1.3 Representative transponder classes and models

Table 33.1 summarizes representative transponder models across commercial and recreational tiers as established in international operations as of 2026.

| Category | Model | OEM / Origin | Power | Link Engine | Primary I/O | Standard |
|---|---|---|---|---|---|---|
| **Class A** | Saab R5 SUPREME | Saab | 12.5 W / 1 W | SOTDMA | IEC 61162-1/-2, LAN | IEC 61993-2 |
| **Class A** | Furuno FA-170 | Furuno | 12.5 W / 1 W | SOTDMA | NMEA 0183, Pilot Plug | IEC 61993-2 |
| **Class A** | em-trak A200 | SRT | 12.5 W / 1 W | SOTDMA | NMEA 0183, NMEA 2000 | IEC 61993-2 |
| **Class B CS** | em-trak B100 | SRT | 2 W | CSTDMA | NMEA 0183, NMEA 2000 | IEC 62287-1 |
| **Class B SO** | Garmin Cortex M1 | Vesper / Garmin | 5 W / 1 W | SOTDMA | NMEA 2000, Wi-Fi | IEC 62287-2 |
| **Class B SO** | Raymarine AIS700 | SRT (OEM) | 5 W / 1 W | SOTDMA | NMEA 2000, Splitter | IEC 62287-2 |
| **AtoN (Type 3)** | Tideland Nova-65 | SRT / Tideland | 1 W / 12.5 W | FATDMA/RATDMA | RS-232, Telemetry | IEC 62320-2 |
| **AIS-SART** | Ocean Signal MOB1 | Ocean Signal / ACR | ~1 W e.i.r.p. | Pre-scheduled | Integrated GNSS, DSC | IEC 61097-14 |

*Table 33.1: Representative AIS transponders across commercial, recreational, AtoN, and SAR categories.*

---

## 33.2 Inside the box: architecture and RF front-ends

Every marine AIS transponder must satisfy four core physical-layer requirements:
1. Simultaneously monitor two discrete VHF channels spaced 50 kHz apart (**AIS 1** at 161.975 MHz and **AIS 2** at 162.025 MHz), plus an optional third receiver for DSC Channel 70 (156.525 MHz).
2. Transmit GMSK-modulated bursts at specified power (1 W, 2 W, 5 W, or 12.5 W) within rigid TDMA slots of $26.67\text{ ms}$ (256 bits at $9{,}600\text{ bit/s}$).
3. Switch between reception and high-power transmission in $< 1\text{ ms}$, maintaining steep out-of-band spectral suppression.
4. Maintain carrier frequency stability within $\pm 500\text{ Hz}$ across marine operating temperatures from $-15^\circ\text{C}$ to $+55^\circ\text{C}$.

### 33.2.1 The transmit/receive RF switch and receiver protection

Operating through a single shared antenna requires a fast transmit/receive (**T/R**) switch capable of handling up to $+41\text{ dBm}$ (12.5 W Class A) with minimal receive insertion loss ($< 0.5\text{ dB}$). PIN diode switches provide over $40\text{ dB}$ of isolation when forward-biased during transmission, reflecting power away from sensitive receiver inputs. During reception, reverse-biased diodes allow sub-microvolt signals to reach the preselector.

International standards mandate hardware protection mechanisms:
- **Mismatch Protection:** Under ITU-R M.1371-6 and IEC 61993-2, the power amplifier must withstand open-circuit and short-circuit conditions. Directional couplers monitor reflected power and fold back amplifier bias if the VSWR exceeds $3:1$.
- **Hardware Transmitter Shutdown:** Under Annex 2 §2.14 of ITU-R M.1371-6, an independent hardware timer must forcefully disconnect transmitter power if a transmission continuously exceeds $2.0\text{ seconds}$, preventing software hangs from jamming the data link.

### 33.2.2 Dual-channel receiver topologies

IEC 61993-2 and IEC 62287 mandate two completely independent parallel receivers; time-multiplexing a single receiver between channels is prohibited because TDMA packets arrive simultaneously on both frequencies.

Class A transponders use discrete superheterodyne channels:
1. **Preselection:** A multi-pole helical or SAW filter centered at 162 MHz attenuates high-power voice VHF (156–157.425 MHz) and coastal FM broadcast signals (88–108 MHz).
2. **LNA Stage:** Low-noise amplification ($NF < 2.5\text{ dB}$) with high third-order intercept ($IIP_3 > +5\text{ dBm}$) suppresses intermodulation.
3. **Downconversion:** A high-linearity mixer downconverts to intermediate frequencies (21.4 MHz or 455 kHz) for ceramic filtering and quadrature discriminator demodulation.

Class B transponders typically use integrated direct-conversion or low-IF transceiver ICs, digitizing near-DC I/Q streams for demodulation inside an ARM processor.

> **Definitions that bite.**
> **Sensitivity vs. Usable Dynamic Range:** High bench sensitivity (e.g., $-115\text{ dBm}$) is meaningless if the front end lacks dynamic range. In a crowded harbor, an AIS receiver must decode a faint $-107\text{ dBm}$ transmission from a distant craft alongside a $+41\text{ dBm}$ Class A blast from a nearby vessel on the adjacent 50 kHz channel. Receivers with modest sensitivity but high $IIP_3$ ($> +10\text{ dBm}$) consistently outperform sensitive units that saturate under strong out-of-band energy.

---

## 33.3 Dedicated receivers: from Si4362 to network appliances

Vessel monitoring stations, coastal networks, academic researchers, and recreational navigators often deploy **receive-only** hardware across three engineering tiers: single-chip embedded receivers, marine multiplexers, and coastal network receivers.

### 33.3.1 The Silicon Labs Si4362 architecture (The dAISy family)

The **dAISy** family developed by Wegmatt LLC illustrates dedicated receiver design. Rather than implementing an SDR pipeline on a host processor, dAISy utilizes the **Silicon Labs Si4362** sub-gigahertz ISM transceiver IC:
- **RF Input:** 50 $\Omega$ SMA or BNC connector with impedance matching and an optional front-end LNA.
- **Demodulation:** Configured for 25 kHz channel bandwidth, $BT = 0.4$, and $\Delta f = \pm 2.4\text{ kHz}$. The Si4362 detects the 24-bit preamble ($0101\dots$), locks its bit clock, and streams raw bits to an Atmel microcontroller.
- **Firmware Baseband:** Open-source firmware (`astuder/dAISy`) handles NRZI decoding, HDLC deframing, bit-unstuffing, CRC-16 checking, and NMEA 0183 `!AIVDM` encapsulation over USB/UART.

The single-channel dAISy alternated between channels, capturing ~50% of packets. The **dAISy 2+** incorporates dual Si4362 ICs and an active RF splitter for simultaneous dual-channel reception ($-113\text{ dBm}$ sensitivity at 20% PER with LNA). The **dAISy-catcher** couples this RF front end directly with AIS-catcher software.

### 33.3.2 Commercial and network receiver appliances

Consumer appliances like the **Quark-elec QK-A026/A026+** integrate dual-channel receivers with GNSS and NMEA multiplexers, broadcasting target telemetry over NMEA 2000 CAN, USB, and Wi-Fi.

Industrial coastal receivers like the **Comar SLR-350N** feature high-linearity front ends and native Ethernet controllers to stream `!AIVDM` sentences directly to VTS centers or maritime aggregators. At the high end, **Shine Micro** transceivers (e.g., SM161R-2 and SM1680 Octopus) employ Enhanced Signal Processing (**ESP**) and multi-channel phase-synchronous receiver arrays to decode overlapping bursts from beyond line-of-sight.

---

## 33.4 SDR hardware for AIS reception

Software-Defined Radio (**SDR**) digitizes wideband RF spectrum directly into complex In-Phase and Quadrature (**I/Q**) samples, delegating filtering, demodulation, and protocol parsing to software.

Because AIS 1 (161.975 MHz) and AIS 2 (162.025 MHz) are separated by 50 kHz, an SDR tuned to **162.000 MHz** with a modest sampling rate of $200\text{ kS/s}$ captures both channels simultaneously.

### 33.4.1 Comparing SDR hardware platforms

Table 33.2 evaluates common SDR platforms utilized for maritime AIS reception.

| Platform | Native ADC | Max Rate | Stability | Duplex | Cost (2026) | Practical Assessment |
|---|---|---|---|---|---|---|
| **RTL-SDR (RTL2832U)** | 8-bit | ~2.4 MS/s | 1–2 ppm TCXO | RX only | $30–$45 | Hobby feed standard; limited dynamic range (~48 dB). |
| **Airspy Mini / R2** | 12-bit | 6 / 10 MS/s | 0.5 ppm TCXO | RX only | $100–$170 | High dynamic range (~70 dB); outstanding harbor rejection. |
| **Airspy HF+ Discovery**| 18-bit DDC | 768 kS/s | 0.5 ppm TCXO | RX only | $170 | Exceptional dynamic range and intermodulation resistance. |
| **SDRplay RSP1B** | 14-bit | 10 MS/s | 0.5 ppm TCXO | RX only | $120–$150 | Built-in broadcast notch filters; excellent VHF reception. |
| **HackRF One** | 8-bit | 20 MS/s | 0.5–20 ppm | Half Duplex | $300–$350 | Wide coverage; 8-bit ADC; TX capable for lab research. |
| **LimeSDR / Mini** | 12-bit | 30.72 MS/s | 1 ppm TCXO | Full Duplex | $200–$400 | Full-duplex transceiver; flexible for lab PHY research. |
| **Ettus USRP (B200)** | 12-bit | 56 MS/s | 2.0 ppm TCXO | Full Duplex | $1,200–$1,800| Academic reference standard; extreme bandwidth. |
| **PlutoSDR (ADALM)** | 12-bit | 61.44 MS/s | 25 ppm | Full Duplex | $200–$250 | Requires firmware unlock down to 70 MHz for AIS band. |

*Table 33.2: Comparison of software-defined radio hardware platforms for AIS applications.*

### 33.4.2 Physical constraints: ADC bit depth and frequency stability

Two hardware characteristics dictate SDR performance in operational coastal settings:

1. **ADC Resolution and Dynamic Range:** Governed by $\text{Dynamic Range (dB)} \approx 6.02 \times N + 1.76$. An 8-bit ADC yields an effective dynamic range of $42\text{–}45\text{ dB}$. When strong harbor signals arrive at $-30\text{ dBm}$, lowering front-end gain pushes faint $-95\text{ dBm}$ signals below the quantization floor. In contrast, 12-bit and 14-bit converters provide $> 70\text{ dB}$ of dynamic range, capturing faint signals alongside strong local carriers without saturation.
2. **Frequency Stability:** Standard $\pm 30\text{ ppm}$ crystal oscillators drift by $\pm 4.8\text{ kHz}$ at 162 MHz over marine temperatures, pushing signals into channel filter skirts. Modern SDRs utilize $1\text{ ppm}$ TCXOs, restricting frequency error to $\pm 162\text{ Hz}$, well within the M.1371-6 budget.

---

## 33.5 Software decoders: lineage and operation

Open-source demodulation software has progressed through four historical generations:
1. **Audio Discriminators (2008–2010):** `gnuais` processed 48 kHz discriminator audio from scanners, performing zero-crossing detection and HDLC parsing into MySQL.
2. **GNU Radio OOT Modules (2011–2014):** `gr-ais` established digital I/Q pipelines for early SDRs, executing matched filtering, clock recovery, and NMEA UDP streaming.
3. **Lightweight C Daemons (2013–2018):** `rtl-ais` combined `librtlsdr` with Christian Gagneraud's *AISDecoder*, enabling dual-channel decoding at 24 kHz on Raspberry Pi hardware.
4. **Multi-Model Parallel Engines (2021–Present):** `AIS-catcher` runs multiple demodulator algorithms concurrently across multi-core processors, choosing the first engine to pass CRC-16 checks.

> **Try it.**
> Capture live AIS telemetry using `AIS-catcher` with an RTL-SDR dongle:
> ```bash
> AIS-catcher -s 162M -p 0 -v 2 -u 127.0.0.1 10110
> ```
> *Expected console output:*
> ```text
> [AIS-catcher v0.60] Decoding on 161.975 MHz and 162.025 MHz
> Found 1 device(s): RTL-SDR v4 (SN: 00000001)
> Tuned to 162.000 MHz, sampling rate 1.536 MS/s
> [Ch A] !AIVDM,1,1,,A,13aEO:0P000040jN502k20?00810,0*26 (MMSI: 244670000, Class A, SOG: 10.2 kn)
> [Ch B] !AIVDM,1,1,,B,403Ovi9u@000,0*72 (MMSI: 003669999, Base Station)
> Total packets decoded: 2 | Channel A: 1 | Channel B: 1 | CRC errors: 0
> ```

---

## 33.6 SDR for transmit: research tools, safety, and legal reality

Transmit-capable SDRs (HackRF, LimeSDR, USRP, PlutoSDR) can synthesize modulated RF bursts. In the literature, tools such as the **Trend Micro AIS BlackToolkit** (Balduzzi, Pasta & Wilhoit 2014) and the **SDRangel modais plugin** demonstrate software synthesis of M.1371 frames. This accessibility introduces severe navigational hazards requiring defensive mitigations.

> **Threat model.**
> - **Attacker Profile:** Rogue actor or experimenter operating within VHF line-of-sight of shipping lanes.
> - **Attacker Capability:** Commercial SDR (HackRF, LimeSDR, USRP) with a 5–25 W VHF amplifier and marine antenna, broadcasting arbitrary ITU-R M.1371 frames.
> - **Attack Vectors and Impact:**
>   1. *Ghost Vessel Spoofing:* Fabricating Class A position reports, triggering false CPA collision alarms on bridge ECDIS.
>   2. *Search and Rescue Disruption:* Radiating false AIS-SART distress beacons (MMSI `970xxxxxx`), diverting SAR resources.
>   3. *AtoN Tampering:* Broadcasting false Message 21 reports to digitally displace harbor entrance buoys.
>   4. *Slot Jamming:* Rapidly pulsing across TDMA slots on AIS 1 and AIS 2, blinding local coastal receivers.
> - **Defensive Mitigations:**
>   - Physical-layer direction finding (RDF) and multi-receiver TDOA triangulation ([Chapter 35](ch35-direction-finding-geolocation.md)).
>   - Radar-AIS cross-correlation on bridge systems; alert suppression for uncorroborated targets.
>   - Kinematic anomaly detection in shore VTS ingestion pipelines ([Chapter 59](ch59-spoofing.md), [Chapter 60](ch60-malicious-payloads-robustness.md)).

> **Legal note.**
> **Transmitting on marine AIS frequencies without statutory licensing and type-approved equipment is unlawful across virtually all jurisdictions.**
> - **United States:** Under **33 CFR § 164.46(i)**, broadcasts from AIS Class A or B devices on land, aircraft, or non-self-propelled vessels are prohibited without FCC authorization. Uncertified transmission on 161.975/162.025 MHz violates the Communications Act and **47 CFR Part 80**, carrying administrative forfeitures exceeding $20,000 per day, equipment seizure, and criminal liability.
> - **International Operations:** Marine VHF safety spectrum is governed by ITU Radio Regulations Appendix 18. Open-air transmission is lawful only for licensed stations using factory-sealed, type-approved equipment.
> - **Laboratory Requirements:** Experimental waveform testing must occur strictly within a shielded RF enclosure, or routed through coaxial attenuators into a dummy load or spectrum analyzer, keeping RF leakage below $-57\text{ dBm}$.

---

## 33.7 Type approval and testing

Because mariners and automated collision systems rely upon AIS for safety of life at sea, transponders cannot be sold based on self-declaration. They are subject to statutory type approval.

### 33.7.1 The standards hierarchy

Type approval follows an unbroken chain of international authority:
1. **IMO Performance Standards:** Resolution MSC.74(69) Annex 3 dictates the operational mandate for universal shipborne AIS under SOLAS Chapter V.
2. **ITU Technical Recommendations:** Recommendation ITU-R M.1371 defines physical modulation, channelization, slot timing, and protocol framing.
3. **IEC Test Specifications:** The IEC operationalizes requirements into testable laboratory standards:
   - **IEC 61993-2:** Class A shipborne transponders.
   - **IEC 62287-1:** Class B Carrier-Sense (CS) transponders.
   - **IEC 62287-2:** Class B Self-Organizing (SO) transponders.
   - **IEC 62320-1 / -2 / -3:** AIS Base Stations, AtoN stations, and repeaters.
   - **IEC 61097-14:** AIS Search and Rescue Transponders (AIS-SART).
   - **IEC 60945:** General environmental and EMC testing for maritime navigation equipment.

### 33.7.2 The laboratory test campaign

Manufacturers submit production-representative units to accredited testing facilities—such as BSH, TÜV SÜD, or Nemko. 

Testing spans several weeks across rigorous domains:
- **RF Physical Layer:** Verifying transmit power ($\pm 1.5\text{ dB}$), frequency accuracy ($\pm 500\text{ Hz}$ across $-15^\circ\text{C}$ to $+55^\circ\text{C}$), transmission rise time ($< 1\text{ ms}$), adjacent-channel power ($< -60\text{ dBc}$), and receiver sensitivity ($20\%\text{ PER at } -107\text{ dBm}$).
- **TDMA Protocol:** Hardware simulators test slot allocation, GNSS sync fallback, and contention windows under artificial traffic saturation.
- **IEC 60945 Environmental:** Dry heat ($+70^\circ\text{C}$ storage), damp heat cycling, cold operational exposure ($-15^\circ\text{C}$), multi-axis vibration tables, acoustic limits, and electrostatic discharge resistance (up to $8\text{ kV}$ contact / $15\text{ kV}$ air).
- **Power Supply:** Continuous operation across $10.8\text{ V}$ to $31.2\text{ V}$ nominal swings, high-voltage transients, and dropouts.

A full type-approval campaign routinely requires tens of thousands to over one hundred thousand dollars in engineering lab fees, excluding internal design iterations.

### 33.7.3 National certification: USCG, FCC, and the EU Wheelmark

Following successful laboratory testing, manufacturers submit certified reports to statutory authorities:
- **United States:** Under **47 CFR § 80.231** and § 80.1101, applicants submit test reports to the Coast Guard Office of Design and Engineering Standards (**USCG CG-ENG-4**). The USCG reviews findings and issues an acceptance letter certifying maritime compliance. The applicant then files for FCC certification, attaching the USCG letter to receive a grant under Equipment Class "AIS".
- **European Union:** For SOLAS Class A units under Directive 2014/90/EU (MED), a Notified Body conducts Module B type-examination and Module D/E production audits before granting use of the **Wheelmark** logo. Class B units fall under the Radio Equipment Directive (**RED** 2014/53/EU) for CE marking.

---

## 33.8 Public teardown: reading an FCC ID

Because manufacturers protect detailed schematics under trade-secret exemptions, reverse engineers and security researchers often ask how to inspect internal AIS hardware without destructive physical teardowns. The solution lies in the public **Federal Communications Commission Office of Engineering and Technology (FCC OET)** database.

Under Title 47 CFR, transponders marketed in the United States must receive an FCC Grant of Certification. Manufacturers upload technical exhibits. While applicants can request confidentiality for proprietary schematics, the FCC mandates that **Internal Photographs**, **External Photographs**, **Test Setup Photographs**, and **User Manuals** remain unredacted public records upon certification.

> **Worked example.**
> **Deconstructing an AIS Transponder via the FCC OET Database**
> 1. **Extracting the FCC ID:** Locate the regulatory label on the rear of the device. For example, an em-trak B100 Class B transponder carries the marking:
>    $$\text{FCC ID: }\mathbf{UYW\text{-}4110003A}$$
> 2. **Parsing the Identifier:**
>    - The first three characters—$\mathbf{UYW}$—represent the **Grantee Code**. Searching the FCC database reveals that `UYW` is registered to **SRT Marine Systems plc** in the United Kingdom. This confirms that despite retail branding, the physical device is an SRT design.
>    - The remaining characters—$\mathbf{4110003A}$—represent the unique **Product Equipment Code**.
> 3. **Querying the FCC EAS Portal:** Open the FCC Equipment Authorization System portal (`apps.fcc.gov/oetcf/eas/reports/GenericSearch.cfm`). Enter Grantee Code `UYW` and Product Code `4110003A`.
> 4. **Analyzing Public Exhibits:**
>    - *Internal Photos Exhibit:* Macro PCB photography reveals silicon components: ARM microcontroller, dual RF downconversion mixers, PIN diode T/R switch, GNSS module, and power amplifier stages.
>    - *Test Report Exhibit:* Test lab measurements verify empirical RF performance: conducted output power ($33.0\text{ dBm}$ / $2.0\text{ W}$), carrier frequency error across temperature ($\Delta f = +84\text{ Hz}$, well within $\pm 500\text{ Hz}$), occupied bandwidth ($10.4\text{ kHz}$ at $99\%$), and spurious emissions down to $-45\text{ dBm}$.

By utilizing this public regulatory archive, maritime systems engineers can objectively determine the true manufacturing lineage, silicon architecture, and empirical RF performance of virtually any commercial AIS transponder in global distribution.

---

## Then & now

The technological trajectory of AIS hardware highlights how a system conceived around discrete analog radio circuits in the 1990s was radically democratized by digital signal processing and software-defined radio.

- ⟨H⟩ **1990–1996:** Early STDMA trials conducted by the Swedish Maritime Administration rely on bulky GP&C 4S transponders combining discrete crystal-controlled VHF radios with external GPS-receivers and industrial PC controller boards.
- ⟨H⟩ **1998:** The IMO adopts Resolution MSC.74(69), establishing universal shipborne Class A performance standards; initial hardware transponders are massive rack-mounted bridge units costing thousands of dollars.
- ⟨+⟩ **2001:** IEC publishes IEC 61993-2 (Edition 1.0), formalizing commercial Class A type approval and establishing the standard Minimum Display and Keyboard (**MKD**) user interface.
- ⟨+⟩ **2006:** IEC publishes IEC 62287-1, inaugurating the low-power (2 W) Class B Carrier-Sense (CS) market and enabling compact, consumer-grade transponders for recreational craft.
- ⟨H⟩ **2008:** Ruben Undheim releases `gnuais`, proving that AIS bursts can be demodulated on standard PC sound cards from scanner discriminator audio without specialized receiver hardware.
- ⟨+⟩ **2011:** Nick Foster releases `gr-ais`, introducing the first open-source software-defined radio AIS receiver pipeline as an out-of-tree block for GNU Radio.
- ⟨H⟩ **2012:** Eric Fry and Antti Palosaari uncover the raw I/Q digitization mode of the Realtek RTL2832U DVB-T dongle; Steve Markgraf releases `rtl-sdr`, initiating the ultra-low-cost ($20) SDR revolution.
- ⟨+⟩ **2013:** Wegmatt launches the dAISy family, demonstrating dual-channel AIS decoding on a low-cost sub-gigahertz ISM transceiver IC (Silicon Labs Si4362).
- ⟨+⟩ **2014:** Marco Balduzzi, Alessandro Pasta, and Kyle Wilhoit present the "AIS BlackToolkit" at ACSAC, demonstrating SDR-based transmission and message manipulation using commercial-off-the-shelf USRP hardware.
- ⟨+⟩ **2017:** IEC publishes IEC 62287-2, establishing Class B SOTDMA ("Class B SO" / "B+"), elevating small-craft transmit power to 5 W with reserved TDMA slot allocations.
- ⟨+⟩ **2021:** Release of `AIS-catcher` by `jvde-github`, demonstrating parallel multi-model DSP demodulation across modern SDR hardware, establishing a new open-source standard for coastal tracking.
- ⟨+⟩ **2022:** Garmin acquires Vesper Marine, absorbing its proprietary software-defined VHF/AIS *Cortex* architecture and signaling corporate consolidation across transponder design houses.

---

## On the wire

Under ITU-R M.1371-6 Annex 2, an AIS packet is transmitted within an exact $26.67\text{ ms}$ TDMA slot. At $9{,}600\text{ bit/s}$, a single slot accommodates 256 bits:
1. **Ramp-Up (8 bits, $0.833\text{ ms}$):** Power amplifier ramps to saturated power ($+41\text{ dBm}$ Class A).
2. **Preamble (24 bits, $2.500\text{ ms}$):** Alternating ones and zeros ($01010101\dots$). In GMSK, this tone locks symbol timing recovery and settles receiver AGC.
3. **Start Flag (8 bits, $0.833\text{ ms}$):** HDLC flag `0x7E` ($01111110_2$) establishing byte synchronization.
4. **Data Payload & Stuffing:** Information bits (e.g., 168 bits for Message 1). The transmitter applies **HDLC bit-stuffing**: inserting a `0` after five consecutive `1`s ($\dots 111111 \dots \implies \dots 11111\mathbf{0}1 \dots$) to prevent false flags. The receiver discards stuffed zeros.
5. **CRC-16 (16 bits, $1.667\text{ ms}$):** CCITT polynomial $G(x) = x^{16} + x^{12} + x^5 + 1$ computed over unstuffed data bits. Mismatches discard the frame.
6. **Stop Flag (8 bits, $0.833\text{ ms}$):** HDLC flag `0x7E` terminating the frame.
7. **Buffer (24 bits, $2.500\text{ ms}$):** Guard interval absorbing bit-stuffing growth, transmitter power ramp-down ($< 1\text{ ms}$), and propagation delay ($1\text{ bit} \approx 31.2\text{ km} \approx 16.8\text{ nmi}$, permitting signals from $> 40\text{ nmi}$ without slot collision).

---

## Validation, uncertainty & data quality

### Errors and their propagation

1. **Clock Drift:** Master oscillator drift $> \pm 10\text{ ppm}$ shifts sample clocks relative to transmitter symbols. Over multi-slot Message 5 reports (424 bits), timing error drifts slicers toward transition boundaries, elevating BER from $10^{-5}$ to $> 10^{-2}$ and failing CRC checks.
2. **Phase Noise:** In unshielded SDRs, host USB noise mixes with adjacent carriers, raising the noise floor and masking faint targets.
3. **Buffer Overruns:** Heavy CPU load drops USB samples; losing 64 I/Q samples breaks phase continuity, causing packet loss.

### Concrete testing procedure: bench sensitivity and PER validation

Validating receiver performance requires a shielded bench setup:
1. **Signal Generation:** Configure a vector signal generator to output 1,000 standard Message 1 reports modulated with GMSK ($BT = 0.4$, symbol rate $= 9{,}600\text{ bit/s}$, deviation $\Delta f = \pm 2.4\text{ kHz}$).
2. **Calibrated Attenuation:** Route RF through a calibrated step attenuator directly into the receiver antenna port.
3. **Measurement:**
   - Test at $-77\text{ dBm}$ (high-level input). Verify Packet Error Rate $\text{PER} = (N_{\text{tx}} - N_{\text{rx}}) / N_{\text{tx}} \le 1\%$.
   - Attenuate in 1 dB steps to $-107\text{ dBm}$. Verify $\text{PER} \le 20\%$ per ITU-R M.1371-6 Table 7.
   - Attenuate to threshold; quality receivers decode down to $-112\text{ dBm}$ to $-114\text{ dBm}$.

---

## Software

### Open source
- **AIS-catcher** (`jvde-github/AIS-catcher`): C++ multi-model SDR receiver supporting RTL-SDR, Airspy, HackRF, and SDRplay with web UI and UDP/ZeroMQ feeds. *Caveat:* High CPU load if all models run simultaneously.
- **rtl-ais** (`dgiardini/rtl-ais`): Headless C receiver for RTL-SDR streaming NMEA over UDP. *Caveat:* Fixed 24 kHz pipeline yields lower sensitivity than matched-filter decoders.
- **gr-ais** (`bistromath/gr-ais`): GNU Radio OOT block by Nick Foster providing GMSK demodulation and HDLC deframing. *Caveat:* Requires maintenance for GNU Radio 3.10+.
- **gnuais** (`rubund/gnuais`): Classic C discriminator audio decoder logging to MySQL. *Caveat:* Dormant; requires physical radio modifications.
- **SDRangel** (`f4exb/sdrangel`): SDR suite with `demodais` and `modais` plugins. *Caveat:* Complex GUI configuration.
- **dAISy Firmware** (`astuder/dAISy`): Microcontroller firmware for Si4362 receivers implementing NRZI/HDLC decoding. *Caveat:* Hardware-specific to Si4362 registers.

### Free but closed
- **SDR# (SDRSharp)**: Windows SDR interface with community AIS plugins. *Caveat:* Closed source; unsuited to headless Linux servers.

### Commercial
- **Shine Micro ESP Firmware**: Proprietary baseband algorithms in commercial base stations. *Caveat:* Restricted to proprietary hardware.

---

## Standards & guides

- **International Maritime Organization (1998):** *Resolution MSC.74(69), Annex 3: Recommendation on Performance Standards for a Universal Shipborne Automatic Identification System (AIS)*. Mandates operational requirements under SOLAS.
- **International Telecommunication Union (2026):** *Recommendation ITU-R M.1371-6: Technical Characteristics for an Automatic Identification System Using Time Division Multiple Access in the VHF Maritime Mobile Frequency Band*. Defines physical layer, slot structure, and protocol framing.
- **International Electrotechnical Commission (2018):** *IEC 61993-2:2018 (Edition 3.0): Maritime Navigation and Radiocommunication Equipment and Systems — Automatic Identification Systems (AIS) — Part 2: Class A Shipborne Equipment*. Specifies operational, performance, and test methods for Class A transponders.
- **International Electrotechnical Commission (2017):** *IEC 62287-1:2017 (Edition 3.0): Maritime Navigation and Radiocommunication Equipment and Systems — Class B Shipborne Equipment — Part 1: Carrier-Sense TDMA (CSTDMA)*. Governs standard 2 W Class B transponders.
- **International Electrotechnical Commission (2017):** *IEC 62287-2:2017 (Edition 2.0): Maritime Navigation and Radiocommunication Equipment and Systems — Class B Shipborne Equipment — Part 2: Self-Organizing TDMA (SOTDMA)*. Governs 5 W Class B SOTDMA ("Class B SO") transponders.
- **International Electrotechnical Commission (2002):** *IEC 60945:2002 (Edition 4.0): Maritime Navigation and Radiocommunication Equipment and Systems — General Requirements — Methods of Testing and Required Test Results*. Mandates environmental, EMC, and vibration qualification.
- **Federal Communications Commission (2026):** *Title 47, Code of Federal Regulations, Part 80: Stations in the Maritime Services (specifically § 80.231 and § 80.1101)*. Governs equipment authorization and Class B programming restrictions in the United States.
- **United States Coast Guard (2026):** *Title 33, Code of Federal Regulations, Section 164.46: Automatic Identification System*. Prohibits unauthorized shore transmission and defines carriage mandates.

---

## Pitfalls

1. **Assuming Retail Brand Equals Independent Hardware Design**
   *The mistake:* Assuming multiple consumer marine brands provide hardware diversity.
   *Why it happens:* Differentiated bezels and marketing conceal identical OEM transceiver modules.
   *How to avoid:* Check the FCC ID on the label. Matching Grantee Codes (e.g., `UYW` for SRT) reveal shared internal hardware.
2. **Deploying Non-TCXO SDR Dongles for Coastal Reception**
   *The mistake:* Using generic $10 RTL-SDR dongles with uncompensated crystal oscillators.
   *Why it happens:* Prioritizing lowest initial cost over thermal stability.
   *How to avoid:* Standard crystals drift $\pm 30\text{ ppm}$ ($\pm 4.8\text{ kHz}$ at 162 MHz), losing packets. Deploy SDRs with $1\text{ ppm}$ or better TCXOs.
3. **Connecting a Transmit-Capable SDR to an Open Antenna**
   *The mistake:* Radiating synthetic AIS test bursts into an outdoor marine VHF antenna.
   *Why it happens:* Underestimating VHF range and strict legal protections of distress spectrum.
   *How to avoid:* Transmitting on AIS channels without authorization violates 33 CFR § 164.46(i). Test exclusively inside shielded RF enclosures or into dummy loads.
4. **Confusing Sensitivity with Dynamic Range in Harbor Environments**
   *The mistake:* Selecting an ultra-sensitive 8-bit SDR for a shore station near a port.
   *Why it happens:* Assuming bench sensitivity dictates operational harbor performance.
   *How to avoid:* Nearby $+41\text{ dBm}$ Class A transmissions saturate 8-bit ADCs, blinding them to distant craft. Deploy 12-bit to 16-bit SDRs with SAW preselection.
5. **Overlooking the Independent Hardware Transmitter Timeout**
   *The mistake:* Relying purely on microcontroller firmware interrupts to terminate RF bursts.
   *Why it happens:* Assuming firmware timers cannot hang.
   *How to avoid:* ITU-R M.1371-6 mandates a hardware timer cutting transmitter power if transmission exceeds 2.0 seconds. Validate by halting execution during transmission.
6. **Deploying Single-Channel Scanning Receivers for High-Density Operations**
   *The mistake:* Using single-channel receivers that alternate between AIS 1 and AIS 2.
   *Why it happens:* Single-channel hardware is cheaper to build.
   *How to avoid:* Moving craft alternate channels; scanning drops 50% of reports. Always deploy dual-channel parallel receivers.
7. **Attempting User Programming of Class B Static Data in the US**
   *The mistake:* Attempting to manually modify vessel MMSI via user menus on a US Class B transponder.
   *Why it happens:* Assuming Class B permits unrestricted user reconfiguration.
   *How to avoid:* Under 47 CFR § 80.231(b), programming is restricted to qualified installers. Devices permanently lock MMSI fields once initialized.
8. **Neglecting Front-End FM Broadcast Filtering**
   *The mistake:* Connecting an SDR to a wideband VHF antenna without band-stop filtering.
   *Why it happens:* Overlooking high-power FM broadcast transmitters (88–108 MHz) nearby.
   *How to avoid:* Intense FM broadcast signals generate intermodulation products across wideband front ends. Install an FM-notch filter or 162 MHz preselector.
9. **Exceeding Host CPU Capacity with Multi-Model Demodulators**
   *The mistake:* Enabling all advanced decoding engines in AIS-catcher on a low-power single-board computer.
   *Why it happens:* Underestimating processing requirements of coherent trellis decoders.
   *How to avoid:* CPU saturation drops USB samples, destroying decode rates. Match active decoder models to available processing cores.
10. **Treating Unconfirmed AIS Targets as Definitive Navigational Hazards**
    *The mistake:* Designing automated collision avoidance that trusts AIS positions without radar validation.
    *Why it happens:* Assuming broadcast AIS data links are authenticated and tamper-proof.
    *How to avoid:* Low-cost SDRs make spoofing straightforward. Always cross-correlate AIS tracks with marine radar returns before maneuvering.

---

## Key takeaways

- **Extreme Supply Chain Concentration:** Despite dozens of retail brands in the commercial catalog, the global transponder hardware market is heavily concentrated around a small group of design houses, predominantly SRT Marine Systems.
- **The FCC ID Reverse-Engineering Path:** Any transponder certified in the United States can be non-destructively inspected via public FCC OET exhibits, using the Grantee Code to unmask the true OEM manufacturer.
- **Physical-Layer Rigidity:** Standard 1-slot AIS transmissions span exactly 256 bits ($26.67\text{ ms}$) at $9{,}600\text{ bit/s}$ using GMSK modulation ($BT = 0.4/0.5$, $h = 0.5$), requiring parallel dual-channel monitoring across 161.975 MHz and 162.025 MHz.
- **Dynamic Range Trumps Raw Sensitivity:** In congested ports, receiver performance is governed by ADC bit depth and intermodulation rejection rather than raw bench sensitivity; 12-bit to 16-bit SDRs dramatically outperform 8-bit dongles.
- **Frequency Stability is Mandatory:** Uncompensated crystal oscillators drift significantly across marine temperatures; reliable decoding requires TCXO stabilization rated at $1\text{ ppm}$ or better ($\le 162\text{ Hz}$ error).
- **Evolution of Open-Source Demodulators:** Open-source decoding has evolved from sound-card discriminator tools (`gnuais`) to lightweight daemons (`rtl-ais`) and modern multi-algorithm parallel DSP engines (`AIS-catcher`).
- **SDR Transmit Hazards and Strict Liability:** Open-source tools make AIS synthesis straightforward on low-cost SDR hardware, but unshielded transmission is a strict-liability criminal offense under international radio regulations and 33 CFR § 164.46(i).
- **Exhaustive Statutory Type Approval:** Commercial transponders require extensive environmental, EMC, and RF laboratory testing under IEC 61993-2/62287 before obtaining USCG/FCC certification or the European MED Wheelmark.

---

## References

- Balduzzi, M., Pasta, A., Wilhoit, K. (2014). A security evaluation of AIS automated identification system. In *Proceedings of the 30th Annual Computer Security Applications Conference (ACSAC '14)*, pages 436–445. New York: ACM. doi:10.1145/2664243.2664257
- Federal Communications Commission (2026). *Title 47, Code of Federal Regulations, Part 80: Stations in the Maritime Services*. Washington, DC: Office of the Federal Register.
- Garmin Ltd. (2022). *Garmin completes acquisition of Vesper Marine*. Corporate Press Release, January 3, 2022. Olathe, KS: Garmin Ltd.
- International Electrotechnical Commission (2002). *Maritime navigation and radiocommunication equipment and systems — General requirements — Methods of testing and required test results*. Standard IEC 60945:2002 (Edition 4.0). Geneva: IEC.
- International Electrotechnical Commission (2010). *Global maritime distress and safety system (GMDSS) — Part 14: AIS search and rescue transmitter (AIS-SART) — Operational and performance requirements, methods of testing and required test results*. Standard IEC 61097-14:2010. Geneva: IEC.
- International Electrotechnical Commission (2017). *Maritime navigation and radiocommunication equipment and systems — Class B shipborne equipment of the automatic identification system (AIS) — Part 1: Carrier-sense time division multiple access (CSTDMA) techniques*. Standard IEC 62287-1:2017 (Edition 3.0). Geneva: IEC.
- International Electrotechnical Commission (2017). *Maritime navigation and radiocommunication equipment and systems — Class B shipborne equipment of the automatic identification system (AIS) — Part 2: Self-organising time division multiple access (SOTDMA) techniques*. Standard IEC 62287-2:2017 (Edition 2.0). Geneva: IEC.
- International Electrotechnical Commission (2018). *Maritime navigation and radiocommunication equipment and systems — Automatic identification systems (AIS) — Part 2: Class A shipborne equipment of the universal automatic identification system (AIS) — Operational and performance requirements, methods of test and required test results*. Standard IEC 61993-2:2018 (Edition 3.0). Geneva: IEC.
- International Electrotechnical Commission (2021). *Maritime navigation and radiocommunication equipment and systems — Automatic identification systems (AIS) — Part 2: AIS AtoN stations — Operational and performance requirements, methods of test and required test results*. Standard IEC 62320-2:2016+AMD1:2021. Geneva: IEC.
- International Maritime Organization (1998). *Recommendation on Performance Standards for a Universal Shipborne Automatic Identification System (AIS)*. Resolution MSC.74(69), Annex 3. London: IMO.
- International Telecommunication Union (2020). *Radio Regulations, Appendix 18 (Rev. WRC-19): Table of Transmitting Frequencies in the VHF Maritime Mobile Band*. Geneva: ITU.
- International Telecommunication Union (2026). *Technical Characteristics for an Automatic Identification System Using Time Division Multiple Access in the VHF Maritime Mobile Frequency Band*. Recommendation ITU-R M.1371-6. Geneva: ITU-R.
- SRT Marine Systems plc (2026). *Transceiver OEM and Technology Solutions*. Corporate Technical Overview. Midsomer Norton, UK: SRT Marine Systems plc. URL: https://srt-marine.com/transceivers/
- United States Coast Guard (2026). *Title 33, Code of Federal Regulations, Section 164.46: Automatic Identification System*. Washington, DC: National Archives and Records Administration.
- Wegmatt LLC (2026). *dAISy 2+ Dual-Channel AIS Receiver Technical Manual*. Seattle, WA: Wegmatt LLC.
