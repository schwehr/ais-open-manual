# Appendix F — Hardware catalog

This appendix provides a comprehensive technical catalog of hardware platforms, radio-frequency subsystems, antenna infrastructure, and software-defined radio (SDR) devices deployed across the maritime Automatic Identification System (AIS) ecosystem. It consolidates verified equipment specifications from international type-approval registries, manufacturer technical manuals, and laboratory teardown filings.

For operational and architectural contexts of these devices, see:
- [Chapter 20](../chapters/ch20-architecture-and-station-classes.md) for station classes, operational reporting intervals, and power allocations.
- [Chapter 26](../chapters/ch26-interfaces-and-logging.md) for digital presentation interfaces, NMEA 0183 (`!AIVDM`/`!AIVDO`), NMEA 2000 CAN bus parameter groups, and Ethernet networks.
- [Chapter 27](../chapters/ch27-rf-basics.md) and [Chapter 28](../chapters/ch28-rf-encoding-physical-layer.md) for radio physics, receiver sensitivity, and GMSK modulation characteristics.
- [Chapter 31](../chapters/ch31-noise-and-interference.md) for RF desensitization, local noise, and co-site interference.
- [Chapter 32](../chapters/ch32-antennas.md) for antenna patterns, feeder lines, masthead siting rules (IMO SN/Circ.227), and active/passive VHF splitters.
- [Chapter 33](../chapters/ch33-hardware-and-sdr.md) for the transponder supply chain, OEM white-labeling, Silicon Labs Si4362 sub-GHz receivers, and SDR architectures.
- [Chapter 36](../chapters/ch36-failure-modes.md) for hardware failure mechanisms, antenna feeder degradation, and GPS receiver faults.
- [Chapter 42](../chapters/ch42-home-receiver.md) for low-cost coastal monitoring stations and hobbyist hardware setups.
- [Chapter 68](../chapters/ch68-special-purpose-ais.md) for special-purpose autonomous stations, aids to navigation (AtoN Types 1–3), and search and rescue locating transmitters (AIS-SART, MOB, EPIRB-AIS).
- [Appendix B](../appendices/appendix-b-standards-register.md) for the statutory standards register governing equipment testing (IEC 61993-2, IEC 62287-1/2, IEC 62320-1/2, IEC 61097-14).

---

## 1. Shipborne transponders (Class A, Class B CS, Class B SO)

The commercial transponder market exhibits significant supply chain consolidation. A large fraction of consumer and commercial retail brands (such as Raymarine, Garmin, Simrad, B&G, and ACR) re-house or license core RF transceiver modules developed by specialist original equipment manufacturers (OEMs), predominantly SRT Marine Systems plc (FCC grantee code `UYW` / `YYG`) or integrated Japanese and European marine electronics specialists (Furuno, JRC, Saab TransponderTech).

Table F.1 details representative shipborne transponders across Class A, Class B Carrier-Sense TDMA (CS), and Class B Self-Organizing TDMA (SO / B+) categories.

| Manufacturer / Model | Class & Link Scheme | OEM Platform / Origin | RF Output Power | GNSS Receivers & Constellations | Host & Network Interfaces | Type Approvals & Certifications | Notes & Distinguishing Architecture |
|---|---|---|---|---|---|---|---|
| **Saab R5 SUPREME** | Class A (SOTDMA) | Saab TransponderTech (Sweden) | 12.5 W / 1 W switchable | GPS, GLONASS, BeiDou, Galileo (internal 72-ch engine) | 3× IEC 61162-2 (38.4k), 3× IEC 61162-1 (4.8k), 10/100 Ethernet, Pilot Plug | EU MED Wheelmark, USCG 165.155 , FCC Part 80, CCS | Split-box architecture (transponder unit separate from 7-inch color Control and Display Unit; dual-redundant power inputs). |
| **Furuno FA-170** | Class A (SOTDMA) | Furuno Electric (Japan) | 12.5 W / 1 W switchable | GPS, GLONASS, Galileo, SBAS (72 channels) | 6× IEC 61162-1/2 ports, front-panel Pilot Plug, LAN (IEC 61162-450) | EU MED Wheelmark, USCG 165.155 , FCC Part 80, JG | Dedicated 4.3-inch color LCD; ECDIS/radar target symbol output; integrated backup battery management. |
| **JRC JHS-183** | Class A (SOTDMA) | Japan Radio Co. (Japan) | 12.5 W / 1 W switchable | GPS (12-ch multi-channel parallel engine) | 4× NMEA 0183 (IEC 61162-1), 1× high-speed port (IEC 61162-2), Pilot Plug | EU MED Wheelmark, USCG 165.155 , FCC Part 80, ClassNK | Dual-chassis design with separate 4.5-inch monochrome display unit; high-immunity dual-synthesizer front end. |
| **em-trak A200** | Class A (SOTDMA) | SRT Marine Systems (UK, FCC ID `UYW-424-0016`) | 12.5 W / 1 W switchable | GPS, GLONASS (internal 72-ch high-sensitivity) | NMEA 0183 (38.4k / 4.8k), NMEA 2000 (Micro-C CAN), USB, Pilot Plug, Wi-Fi | EU MED Wheelmark, USCG 165.155, FCC Part 80 (Equipment Class AIS) | Compact IP67 all-in-one chassis with 5-inch sunlight-readable color display; SRT Apollo platform architecture. |
| **em-trak B100** | Class B CS (CSTDMA) | SRT Marine Systems (UK, FCC ID `UYW-411-0001`) | 2 W (33 dBm conducted) | GPS (50 channels, internal LNA) | NMEA 0183 dual baud (4.8k/38.4k), NMEA 2000, USB (virtual COM), SD card logging | FCC Part 80 (Certified), USCG 165.156, CE RED | Classic recreational Class B transponder; passive listening carrier-sense engine; silent mode hardware switch input. |
| **em-trak B953** | Class B SO (SOTDMA) | SRT Marine Systems (UK, FCC ID `UYW-430-0005`) | 5 W / 1 W switchable | GPS, GLONASS, Galileo, BeiDou (internal antenna or ext) | NMEA 0183, NMEA 2000, USB, Bluetooth 4.0, Wi-Fi | FCC Part 80, USCG 165.156 , CE RED | Built-in zero-loss active VHF antenna splitter; autonomous slot reservation (SOTDMA); high-speed reporting up to 5 s. |
| **Garmin Cortex M1** | Class B SO (SOTDMA) | Vesper Marine / Garmin (New Zealand) | 5 W / 1 W switchable | Multi-GNSS (GPS, GLONASS, SBAS; 10 Hz update) | NMEA 2000, NMEA 0183, Wi-Fi, Ethernet, 5-channel GPIO sensor inputs | FCC Part 80, USCG, CE RED | Unified marine hub integrating Class B SOTDMA transponder, Class D VHF radiotelephone, and remote vessel cloud telemetry. |
| **Raymarine AIS700** | Class B SO (SOTDMA) | SRT Marine Systems OEM (FCC ID `UYW-430-0001`) | 5 W / 1 W switchable | GPS, GLONASS (72 channels) | NMEA 0183, NMEA 2000 (SeaTalkng), USB | FCC Part 80, USCG, CE RED | Integrated active VHF splitter routing shared masthead whip to transponder and VHF voice radio; dedicated silent mode lead. |
| **Vesper WatchMate Vision2**| Class B CS (CSTDMA) | Vesper Marine (New Zealand) | 2 W (33 dBm conducted) | GPS (50 channels, 5 Hz engine) | NMEA 0183, NMEA 2000, USB, Wi-Fi (802.11 b/g) | FCC Part 80, USCG 165.156, CE RED | Standalone 5.7-inch color touchscreen display; advanced collision avoidance filter engine (CPA/TCPA target priorities). |
| **Digital Yacht AIT5000** | Class B SO (SOTDMA) | Digital Yacht (UK) | 5 W / 1 W switchable | GPS, GLONASS, Galileo (internal 72-ch) | NMEA 0183, NMEA 2000, USB, Wi-Fi (multiplexing raw NMEA and target feeds) | FCC Part 80, CE RED | Incorporates patented ZeroLoss active VHF antenna splitter; wireless NMEA multiplexer for tablet navigation apps. |

*Table F.1: Specifications of representative commercial Class A and recreational Class B transponders.*

---

## 2. Dedicated AIS receivers and coastal appliances

Dedicated AIS receivers dispense with VHF transmission hardware, operating as dual-channel or single-channel listening appliances. Commercial and coastal units employ high-linearity superheterodyne or direct-conversion front ends to withstand high RF environments near container terminals and maritime radar installations. Low-cost and open-hardware designs leverage highly integrated sub-GHz ISM radio transceivers—most notably the Silicon Labs Si4362/Si4463 family—governed by low-power microcontrollers executing open firmware.

Table F.2 compares dedicated commercial, hobbyist, and base-station receive appliances.

| Manufacturer / Model | Receiver Architecture | Sensitivity | Frequency & Channels | Host & Network Interfaces | Power Supply | Ingress & Form Factor | Application & Distinguishing Features |
|---|---|---|---|---|---|---|---|
| **Wegmatt dAISy 2+** | Silicon Labs Si4362 sub-GHz IC + Microchip MCU | −113 dBm @ 20% PER (with LNA) | 161.975 & 162.025 MHz (simultaneous dual-ch) | USB (CDC virtual COM), 3.3V UART serial header | USB bus powered (5V, ~50 mA) | Extruded aluminum enclosure, SMA-F | Open-source firmware (`astuder/dAISy`); reference dual-channel open-hardware edge receiver. |
| **Wegmatt dAISy HAT** | Dual Silicon Labs Si4362 ICs + Microchip MCU | −113 dBm @ 20% PER | 161.975 & 162.025 MHz (simultaneous dual-ch) | Raspberry Pi 40-pin GPIO header (UART `/dev/ttyAMA0`) | 3.3V / 5V from Pi header (< 60 mA) | Raspberry Pi HAT form factor, SMA-F | Direct stackable receiver for headless Raspberry Pi nodes; hardware jumper selection for UART channels. |
| **Quark-elec QK-A026+**| Dual-channel SDR / downconverter IC | −112 dBm | 161.975 & 162.025 MHz (simultaneous dual-ch) | NMEA 0183 (in/out), NMEA 2000, Wi-Fi, USB | 12V / 24V DC (9.6–32 V), ~120 mA | IPX4 plastic enclosure, BNC-F | Integrated multi-GNSS receiver and NMEA multiplexer; broadcasts combined NMEA 0183/2000 data over Wi-Fi AP/station. |
| **Comar SLR-350N** | Superheterodyne dual-channel receiver | −115 dBm | 161.975 & 162.025 MHz (simultaneous dual-ch) | 10/100 Base-T Ethernet (RJ-45), USB, NMEA 0183 (38.4k) | 9–30 V DC (approx. 2.5 W) | Rugged die-cast aluminum chassis, BNC-F | Professional coastal monitoring appliance; streams raw `!AIVDM` sentences over TCP/IP or UDP to remote VTS servers. |
| **Shine Micro SM161R-2**| Dual-channel receiver with DSP filtering | −118 dBm (high sensitivity) | 161.975 & 162.025 MHz (simultaneous dual-ch) | RS-232, RS-422, USB, Ethernet (optional adapter) | 9–36 V DC (approx. 3.0 W) | Flanged industrial metal enclosure, BNC-F | High-linearity commercial maritime receiver; Enhanced Signal Processing (ESP) algorithm for degraded RF links. |
| **Shine Micro SM1680 "Octopus"**| Multi-channel phase-synchronous receiver array | −121 dBm per channel | 161.975 & 162.025 MHz (multi-channel array) | High-speed Ethernet (Gigabit), UDP broadcast, RS-422 | 100–240 V AC or 12–24 V DC | 19-inch 1U rack-mount industrial chassis, N-F | Long-range base station and coastal surveillance; beamforming array decoding overlapping bursts from beyond line-of-sight. |
| **Digital Yacht AIS100**| Dual-channel synthesized receiver | −105 dBm | 161.975 & 162.025 MHz (simultaneous dual-ch) | NMEA 0183 output (38,400 baud, 2-wire differential) | 12V / 24V DC (< 50 mA) | Compact plastic enclosure, BNC-F | Entry-level black-box receiver designed for direct connection to marine chartplotters and MFDs via standard NMEA. |
| **SRT Marine Neon** | Dual-channel Class A/B receiver module | −115 dBm | 161.975 & 162.025 MHz + DSC 156.525 MHz | TTL UART / RS-232, SPI, GPIO | 3.3V DC regulated (< 150 mW) | SMT surface-mount soldered module | Core OEM receiver module for integration into marine instrumentation, oceanographic buoys, and tracking units. |

*Table F.2: Dedicated AIS receivers, coastal appliances, and modular radio engines.*

---

## 3. Software-defined radio (SDR) platforms for AIS

Software-Defined Radio (SDR) receivers digitize RF bandwidth across the VHF maritime spectrum, transferring demodulation, bit synchronization, and HDLC framing to host software such as **AIS-catcher**, **rtl-ais**, or GNU Radio (`gr-ais`). The critical hardware figures of merit for AIS SDRs are:
1. **Analog-to-Digital Converter (ADC) Resolution:** Governs dynamic range ($\approx 6.02 \times N + 1.76\text{ dB}$). In busy commercial anchorages, strong local Class A signals (+41 dBm radiating nearby) generate $-30\text{ dBm}$ inputs at the antenna terminal. An 8-bit ADC provides only $\sim 48\text{ dB}$ of effective dynamic range, blinding the receiver to distant, weaker targets ($-95\text{ dBm}$) in the same passband. Higher bit depths (12 to 14 bits) yield $> 70\text{ dB}$ of instantaneous dynamic range.
2. **Frequency Stability (TCXO):** Standard quartz crystals drift up to $\pm 30\text{ ppm}$ ($\pm 4.8\text{ kHz}$ at 162 MHz), pushing the GMSK spectrum across channel filter skirts. Modern SDRs incorporate $0.5\text{–}1.0\text{ ppm}$ Temperature-Compensated Crystal Oscillators (TCXO), restricting frequency error to $< 162\text{ Hz}$.

Table F.3 provides a technical comparison of SDR hardware deployed for AIS research and coastal monitoring.

| Platform | Native ADC Bit Depth | Maximum Sample Rate | Frequency Stability (Oscillator) | Duplex Mode | Tuning Range | Cost Tier (2026) | Optimal AIS Role & Evaluation |
|---|---|---|---|---|---|---|---|
| **RTL-SDR Blog v4** | 8-bit (Realtek RTL2832U) | ~2.4 MS/s (stable) | 1.0 ppm TCXO | RX only | 500 kHz – 1.76 GHz | Budget ($35) | Reference hobbyist hardware; built-in bias-tee and aluminum shielding; limited dynamic range in dense ports. |
| **Airspy Mini** | 12-bit | 6 MS/s / 3 MS/s | 0.5 ppm TCXO | RX only | 24 MHz – 1.8 GHz | Mid-range ($100) | High dynamic range (~70 dB); outstanding rejection of out-of-band pager and FM broadcast signals. |
| **Airspy R2** | 12-bit | 10 MS/s / 2.5 MS/s | 0.5 ppm TCXO | RX only | 24 MHz – 1.8 GHz | Mid-range ($170) | Wideband capture; excellent phase noise characteristics; ideal for multi-channel coastal research. |
| **Airspy HF+ Discovery**| 18-bit DDC architecture | 768 kS/s | 0.5 ppm TCXO | RX only | 0.5 kHz–31 MHz, 60–260 MHz | Mid-range ($170) | Extreme dynamic range and intermodulation resistance; optimal for severe co-site interference environments. |
| **SDRplay RSP1B** | 14-bit | 10 MS/s | 0.5 ppm TCXO | RX only | 1 kHz – 2.0 GHz | Mid-range ($130) | Integrated broadcast notch filters (VHF FM / DAB); steel casing; exceptional front-end selectivity. |
| **HackRF One** | 8-bit (Maxim MAX5864) | 20 MS/s | 20 ppm (ext clock in) | Half Duplex (TX/RX) | 1 MHz – 6 GHz | Research ($300) | Wideband transceiver; 8-bit ADC limits reception dynamic range; widely used in lab transmit security research. |
| **LimeSDR Mini v2** | 12-bit (LMS7002M) | 30.72 MS/s | 1.0 ppm TCXO | Full Duplex (1T1R) | 10 MHz – 3.8 GHz | Research ($350) | Full-duplex laboratory transceiver; flexible FPGA-based signal preprocessing; bench PHY testing. |
| **Ettus USRP B200 / B210**| 12-bit (AD9364 / AD9361) | 56 MS/s (61.44 MS/s) | 2.0 ppm TCXO (GPSDO opt) | Full Duplex (2T2R B210)| 70 MHz – 6 GHz | Professional ($1.2k–$2.2k)| Academic and defense gold standard; ultra-linear transceiving; high-precision timestamping and sync. |
| **Analog Devices ADALM-Pluto**| 12-bit (AD9363) | 61.44 MS/s | 25 ppm (modded 0.5 ppm)| Full Duplex (1T1R) | 325–3800 MHz (70–6000 mod)| Educational ($220) | Requires software unlock to tune below 325 MHz to reach 162 MHz; compact portable transceiver. |

*Table F.3: SDR hardware architectures evaluated for maritime VHF data link reception and PHY research.*

---

## 4. Antennas, feeder cables, and active RF splitters

AIS performance depends strictly on antenna elevation, pattern geometry, line losses, and co-site decoupling.
- **Physical Wavelength:** At 162.000 MHz, free-space wavelength $\lambda = 1.851\text{ m}$ ($c/f$). A half-wave dipole measures $0.925\text{ m}$; a quarter-wave whip measures $0.463\text{ m}$ (before applying standard $\sim 5\%$ velocity factor reduction for metal radiators).
- **Gain vs. Vessel Dynamics:** High-gain collinear antennas (6 to 9 dBi) achieve gain by compressing their vertical beamwidth to $\pm 15^\circ$ or $\pm 10^\circ$. On rolling sailboats or heeling power craft, this beam points into the sea and sky, causing catastrophic packet loss. Craft subject to angular motion must use broad-beam antennas ($\le 3\text{ dBi}$).
- **Installation Geometry (IMO SN/Circ.227 & COMSAR.1/Circ.32/Rev.3):** Antennas must maintain $360^\circ$ clear horizons. Vertical collinear stacking ($\ge 2\text{ m}$ vertical separation) is the gold standard because dipole nulls align along the mast axis. Where antennas must share the same horizontal level, SN/Circ.227 specifies a separation of at least $10\text{ m}$, whereas COMSAR.1/Circ.32/Rev.3 quotes at least $5\text{ m}$.
- **Active Splitters:** IMO SN/Circ.227 mandates dedicated antennas for SOLAS Class A vessels. Active splitters are legally restricted to voluntary small craft. They incorporate electromechanical relays defaulting to the VHF radiotelephone upon DC power loss, an RF carrier-sensing trigger for instantaneous AIS disengagement, and an internal low-noise amplifier (LNA) providing $+10\text{ to }+12\text{ dB}$ gain to offset splitter losses.

Table F.4 details commercial and marine antennas, active transponder splitters, and coaxial cable specifications.

| Product / Category | Manufacturer / Model | Electrical & Mechanical Type | Frequency & Bandwidth | Gain & Beamwidth | RF Connectors & Impedance | Approvals & Applications |
|---|---|---|---|---|---|---|
| **Commercial Ship Antenna** | Shakespeare 396-1-AIS | 1/2-wave end-fed coaxial sleeve whip | 156–162 MHz (optimized 162) | 3 dBi (broad vertical lobe) | SO-239 (UHF-F), 50 $\Omega$ | Commercial Class A ships; heavy fiberglass construction for severe marine exposure. |
| **Performance Gain Whip** | Shakespeare 5225-XP-AIS | Stacked collinear element array (2.4 m) | 161.975 & 162.025 MHz (< 1.5:1 VSWR) | 6 dBi (narrower vertical lobe) | Silver-plated PL-259 / SO-239 | Motoryachts, workboats, and stable platforms; high-gain coastal tracking. |
| **Sailboat Masthead Whip** | Glomex RA106SLSPB | 1/2-wave stainless steel whip (0.9 m) | 156–162 MHz | 3 dBi (wide vertical lobe) | SO-239 / Glomex fast-fit | Sailing vessels subject to severe heel; low windage, high flexibility. |
| **Coastal Base Station Antenna**| Celwave / RFS BA6012 | Collinear omnidirectional array (brass/copper) | 156–163 MHz (< 1.5:1 VSWR) | 6 dBd (8.15 dBi), omni | N-Female, 50 $\Omega$ | Heavy-duty shore station and VTS base stations; withstands 200 km/h wind loads. |
| **Coastal Sector Yagi** | Telewave ANT150Y10 | 7-element directional Yagi array | 150–174 MHz tunable | 10 dBd (12.15 dBi), 54° beam | N-Female, 50 $\Omega$ | Directional coastal surveillance; monitors shipping lanes while rejecting inland RF noise. |
| **Active Transponder Splitter**| Vesper SP160 | Active RF relay switch with LNA | VHF Voice + AIS (156–162 MHz) | AIS RX: +12 dB gain; TX loss: < 1 dB | 3× SO-239 (Ant, VHF, AIS), 12/24V DC | Leisure Class B transponders; fail-safe relay to voice radio; VHF TX priority. |
| **Active Transponder Splitter**| Digital Yacht SPL2000 | Active RF power-sensing relay switch | VHF Voice + AIS + AM/FM radio | ZeroLoss (3 dB pre-amp boost) | 3× BNC / PL-259, 12V/24V DC | Fail-safe operation; routes single masthead whip to transponder, VHF radio, and stereo. |
| **Receiver-Only Splitter** | Shakespeare 5257-S | Passive inductive/resistive network | Marine VHF band | −3.5 dB insertion loss | 3× PL-259 | **Receiver only.** Prohibited for transponders (lacks relay; burns out radio front ends). |
| **Coaxial Feeder (Baseline)** | RG-214/U | Double silver-plated copper braided coax | Up to 1 GHz (10.8 mm OD) | Loss: 9.8 dB / 100 m @ 162 MHz | Shielding: > 85 dB | SN/Circ.227 recommended baseline for SOLAS Class A transponders. |
| **Coaxial Feeder (Low-Loss)** | Times Microwave LMR-400 | Solid BCCAI, closed-cell foamed PE | Up to 6 GHz (10.3 mm OD) | Loss: 4.9 dB / 100 m @ 162 MHz | Shielding: > 90 dB (foil + braid)| Premium low-loss feeder for long mast runs and shore station receiver arrays. |
| **Coaxial Feeder (Thin Utility)**| RG-58C/U | Tinned copper braid, solid PE dielectric | Up to 1 GHz (4.95 mm OD) | Loss: 20.3 dB / 100 m @ 162 MHz | Shielding: > 40 dB | Low-cost utility cable; acceptable only for short runs (< 5 m); severe attenuation on masts. |

*Table F.4: Marine VHF antennas, active splitters, and coaxial cable characteristics.*

---

## 5. Aids to navigation, base stations, and SAR locating hardware

Autonomous coastal infrastructure and emergency locating beacons operate under strict international performance and testing regimes:
- **AIS Base Stations (IEC 62320-1):** Dual-channel transceivers operating under SOTDMA or Fixed Access TDMA (FATDMA). They broadcast system timing frames (Message 4), channel management directives (Message 22), slot reservations (Message 20), and application-specific meteorological/hydrological warnings.
- **AIS Aids to Navigation (IEC 62320-2):** Segmented into three distinct hardware architectures:
  - *Type 1 (Transmit-only):* Lacks a VHF receiver; broadcasts solely on pre-reserved FATDMA slots synchronized via internal GNSS. Minimal power draw for remote solar buoys.
  - *Type 2 (Transmit + Control Receiver):* Incorporates a single VHF receiver for remote configuration and diagnostic polling; transmits via FATDMA.
  - *Type 3 (Autonomous Transceiver):* Houses dual VHF receivers; autonomously assesses slot availability using Random Access TDMA (RATDMA) and FATDMA; capable of message repetition and polling responses.
- **Search and Rescue Beacons (IEC 61097-14, ETSI EN 303 098):** AIS-SART, personal Man Overboard (MOB), and EPIRB-AIS devices transmit an 8-message burst sequence once per minute (4 messages on 161.975 MHz and 4 on 162.025 MHz), generating the standard safety text alert `SART ACTIVE` (Message 14) and position broadcasts (Message 1). Radiated power is specified as $1\text{ W e.i.r.p.}$, incorporating antenna efficiency.

Table F.5 catalogues representative base stations, AtoN units, and locating beacons.

| Manufacturer / Model | Equipment Classification | Operational Architecture | RF Output Power | Position & Timing Engine | Interfaces & Protocols | Compliance & Approvals |
|---|---|---|---|---|---|---|
| **Saab R40 AIS Base Station** | AIS Base Station | Dual VHF receivers + SOTDMA transmitter | 12.5 W / 2 W selectable | Integrated GPS timing receiver (1 PPS) | Dual Ethernet (IEC 61162-450), 4× RS-422, SNMP | IEC 62320-1, IALA R0124, CE, FCC |
| **Kongsberg AIS BS610** | AIS Base Station / VDL receiver | Full SOTDMA/FATDMA transceiver unit | 12.5 W / 1 W selectable | Internal GNSS (GPS/GLONASS) engine | Redundant Ethernet, RS-422, NMEA 0183 | IEC 62320-1, RED, USCG compliant |
| **Tideland Signal Nova-65** | AIS AtoN Station | Type 1 / Type 3 modular configuration | 1 W / 12.5 W configurable | Internal GPS / Galileo engine | RS-232, RS-485, Modbus sensor telemetry| IEC 62320-2, IALA G1050, USCG, CE |
| **Sealite SL-AIS-C** | AIS AtoN Station | Type 1 or Type 3 architecture | 1 W / 12.5 W configurable | Ultra-low-power GPS engine | RS-232 configuration port, lantern sync | IEC 62320-2, IALA Recommendation R0126 |
| **Resideo / Ocean Signal S100** | AIS-SART | Survival craft locating transmitter | 1 W e.i.r.p. nominal | Internal 66-channel GPS engine | Visual strobe, operational test buzzer | IMO SOLAS, IEC 61097-14, MED Wheelmark, FCC |
| **Ocean Signal rescueME MOB1** | AIS-MOB Beacon | Personal survivor locating device | ~1 W e.i.r.p. AIS + integrated DSC | Integrated multi-GNSS (66-ch engine) | NFC setup, high-intensity LED strobe | ETSI EN 303 098, RTCM 11901.1, CE, FCC |
| **McMurdo Smartfind S5A** | AIS-SART | Search and rescue transponder | 1 W e.i.r.p. nominal | Internal multi-channel GPS engine | Lanyard, mounting pole, LED test light | IEC 61097-14, MED Wheelmark, USCG, FCC |
| **ACR GlobalFix V5** | EPIRB with AIS | Dual 406 MHz + AIS beacon + 121.5 MHz | 5 W (406 MHz), 1 W e.i.r.p. (AIS) | Internal GNSS + Return Link Service (RLS) | Optical & infrared strobes, NFC mobile | Cospas-Sarsat, IEC 61097-2 Ed.4, FCC, MED |

*Table F.5: Specifications of representative AIS base stations, AtoN transceivers, and SAR locating devices.*

---

## 6. Transmit-capable research tools and laboratory signal generators

Software-defined radios capable of transmitting on marine VHF frequencies (161.975 MHz and 162.025 MHz) present significant regulatory, operational, and ethical challenges. The broadcast architecture of AIS is unauthenticated (see [Chapter 58](../chapters/ch58-threat-model.md) and [Chapter 59](../chapters/ch59-spoofing.md)), making the data link vulnerable to spoofing, ghost ship injection, and slot-denial attacks. 

In essentially all maritime administrations, transmitting on AIS frequencies without a valid vessel or coastal station license and non-type-approved hardware violates federal and international law (e.g., US Communications Act of 1934 and 47 CFR Part 80; European RED Directive). Legitimate transmission research is strictly restricted to RF-shielded enclosures, coaxial dummy loads, and anechoic chambers during type-approval bench testing under IEC 61993-2.

Table F.6 summarizes transmit-capable software modules, SDR research toolkits, and industrial bench signal generators.

| Platform / Toolkit | Primary Author / Maintainer | Hardware Target | Frequency Range & Modulation | Transmit Functionality & Architecture | Regulatory Status & Operational Scope |
|---|---|---|---|---|---|---|
| **AIS BlackToolkit (`gr-aistx`)**| Marco Balduzzi et al. (Trend Micro) | USRP (UHD), HackRF One | 161.975 / 162.025 MHz, GMSK (BT=0.4, 9.6 kbps)| Out-of-tree GNU Radio block; generates AIVDM bitstreams, CRC-16, and GMSK burst envelopes | Open-source research tool (ACSAC 2014); for use strictly in RF-isolated test environments. |
| **SDRangel (`modais` plugin)**| Edouard Griffiths (F4EXB) et al. | HackRF, LimeSDR, USRP, BladeRF, Pluto | VHF maritime band (156–174 MHz), GMSK | Maintains full GUI channel modulator; accepts NMEA UDP payloads, injects Messages 1, 4, 5, 18, 21 | Open source (GPL-3.0); general-purpose SDR TX suite; transmission without license is unlawful. |
| **GNU Radio Out-of-Tree TX Blocks**| Open-source community | USRP, LimeSDR, HackRF, ADALM-Pluto | VHF maritime band (tunable GMSK sink) | Flowgraphs combining NRZI encoding, bit stuffing, CRC generation, and Gaussian shaping filters | Educational and research experimentation; restricted to wired RF attenuators and dummy loads. |
| **Rohde & Schwarz SMBV100B / SMW200A**| Rohde & Schwarz (Germany) | Vector Signal Generator (commercial test bench) | 8 kHz to 6 GHz (ultra-low phase noise) | Arbitrary waveform generator (ARB); automated ITU-R M.1371 / IEC 61993-2 conformance test suites | Type-approval laboratory test standard; calibrated signal generation for receiver compliance testing. |
| **Aeroflex / Cobham IFR 7200 / 3920B**| Cobham Aerospace (Aeroflex) | Dedicated Radio Test Set | VHF/UHF tactical & maritime bands | Specialized AIS transponder test personality; measures RF power, frequency error, burst timing, and PER | Calibrated benchtop test set used by certified marine service technicians and type-approval labs. |

*Table F.6: Software-defined transmit research tools and laboratory signal generators.*

---

## 7. Type-approval test standards and regulatory equipment classes

All maritime AIS transmitting equipment must successfully complete independent laboratory compliance testing before commercial deployment or shipboard installation. The regulatory hierarchy proceeds from broad international conventions down to national equipment grants:
1. **Statutory Mandate:** IMO SOLAS Chapter V, Regulation 19.2.4 mandates AIS carriage on all ships of 300 gross tonnage and upwards engaged on international voyages, cargo ships of 500 GT and upwards not on international voyages, and all passenger ships irrespective of size.
2. **Operational Performance Requirements:** IMO Resolution MSC.74(69), Annex 3 defines the operational capabilities for universal Class A AIS. Class B performance requirements are grounded in IMO MSC.140(76) .
3. **Radio Technical Characteristics:** Recommendation ITU-R M.1371-6 specifies the link layer TDMA access schemes, modulation index ($0.5$), Gaussian filter bandwidth ($BT = 0.4$ for Class A/B SO; $BT = 0.3$ for Class B CS), power tolerances ($\pm 1.5\text{ dB}$), and bit layouts.
4. **Laboratory Pass/Fail Standards:** International Electrotechnical Commission (IEC) Technical Committee 80 produces the exhaustive test suites:
   - **IEC 61993-2:** Class A shipborne equipment.
   - **IEC 62287-1:** Class B Carrier-Sense TDMA (CSTDMA) equipment.
   - **IEC 62287-2:** Class B Self-Organizing TDMA (SOTDMA) equipment.
   - **IEC 62320-1:** AIS Base Stations.
   - **IEC 62320-2:** AIS Aids to Navigation (AtoN).
   - **IEC 62320-3:** AIS Repeater Stations.
   - **IEC 61097-14:** AIS Search and Rescue Transponders (AIS-SART).
   - **IEC 60945:** General environmental, vibration, climatic, and electromagnetic compatibility (EMC) test methods.
5. **National and Regional Certification:**
   - **United States:** Equipment must achieve certification by the Federal Communications Commission (FCC) under 47 CFR Part 80, Equipment Class "AIS". Units intended for mandatory carriage must also secure USCG Type Approval (Approval Series 165.155 for Class A, 165.156 for Class B) through the USCG Office of Design and Engineering Standards (CG-ENG-1). Under 47 CFR § 80.231, Class B MMSI and static data cannot be programmed by end users and must be set by certified installers.
   - **European Union:** Commercial SOLAS equipment must obtain the Marine Equipment Directive (MED) Wheelmark approval (Directive 2014/90/EU) issued by a notified body via Module B (EC Type Examination) and Module D/E/F (production quality assurance). Recreational Class B transponders are certified under the Radio Equipment Directive (RED 2014/53/EU).

Table F.7 maps the type-approval test standards across all recognized AIS equipment classes.

| Equipment Class | Operational Access Scheme | Nominal Transmit Power | IEC Performance & Test Standard | US Regulatory Approvals | European Union Approvals | Primary Governed Hardware Attributes |
|---|---|---|---|---|---|---|
| **Class A Shipborne** | SOTDMA / ITDMA | 12.5 W / 1 W switchable | IEC 61993-2 (Ed. 3.0:2018) | FCC Part 80 (Class AIS) + USCG 165.155  | EU MED Wheelmark (Module B+D) | Dynamic slot scheduling, high-speed reporting, mandatory MKD display, dual IEC 61162 ports. |
| **Class B "CS"** | CSTDMA | 2 W (33 dBm conducted) | IEC 62287-1 (Ed. 3.0:2017) | FCC Part 80 (Class AIS) + USCG 165.156 | EU RED (CE mark) | Carrier-sense listen-before-talk; packet deferral; factory-locked MMSI programming. |
| **Class B "SO" (B+)** | SOTDMA | 5 W / 1 W switchable | IEC 62287-2 (Ed. 2.0:2017) | FCC Part 80 (Class AIS) + USCG 165.156  | EU RED (CE mark) | Autonomous slot reservation; dynamic reporting rate up to 5 s; higher RF output power. |
| **AIS Base Station** | SOTDMA / FATDMA | Configurable up to 12.5 W | IEC 62320-1 (Ed. 2.0:2015) | FCC Part 80 (Coastal Station licensing) | National spectrum authority approval | System master timing (Msg 4), slot reservation (Msg 20), channel management (Msg 22). |
| **AIS AtoN (Type 1)** | FATDMA only | 1 W / 12.5 W configurable | IEC 62320-2 (Ed. 2.0:2016) | FCC Part 80 + USCG Private Aid license | National lighthouse authority | Transmit-only solar buoy beacon; zero channel listening capability; strict FATDMA timing. |
| **AIS AtoN (Type 2)** | FATDMA (RX control) | 1 W / 12.5 W configurable | IEC 62320-2 (Ed. 2.0:2016) | FCC Part 80 + USCG Private Aid license | National lighthouse authority | FATDMA transmitter with control receiver for remote configuration and diagnostic queries. |
| **AIS AtoN (Type 3)** | RATDMA / FATDMA | 1 W / 12.5 W configurable | IEC 62320-2 (Ed. 2.0:2016) | FCC Part 80 + USCG Private Aid license | National lighthouse authority | Autonomous dual-channel transceiver; RATDMA slot selection; remote polling and chaining. |
| **AIS-SART** | Pre-scheduled 8-burst | 1 W e.i.r.p. nominal | IEC 61097-14 (Ed. 1.0:2010) | FCC Part 80 + USCG 160.155  | EU MED Wheelmark | 96-hour emergency beacon; bursts Message 1 and Message 14; 1 W radiated power budget. |
| **MOB-AIS** | Pre-scheduled burst | ~1 W e.i.r.p. nominal | ETSI EN 303 098 (V2.2.1) | FCC Part 95 / Part 80 (Class AIS) | EU RED (CE mark) | Personal survivor locator; integrated flashing strobe; water-immersion automatic activation. |
| **EPIRB-AIS** | Pre-scheduled burst | 5 W (406 MHz) + 1 W (AIS) | IEC 61097-2 (Ed. 4.0:2021) | FCC Part 80 + USCG 160.155 | EU MED Wheelmark | GMDSS emergency distress beacon; combines Cospas-Sarsat satellite alert with local AIS homing. |

*Table F.7: Regulatory standards, type-approval frameworks, and testing regimes across equipment classes.*

---

## References

- Balduzzi, M., Pasta, A. & Wilhoit, K. (2014). A security evaluation of AIS automated identification system. *Proceedings of the 30th Annual Computer Security Applications Conference (ACSAC 2014)*, 436–445. doi:10.1145/2664243.2664257
- European Parliament and Council of the European Union (2014). *Directive 2014/90/EU of 23 July 2014 on Marine Equipment (Marine Equipment Directive)*. Official Journal of the European Union, L 257:146–185.
- European Telecommunications Standards Institute (2021). *Maritime Navigation and Radiocommunication Equipment and Systems — Maritime Survivor Locating Devices (MSLD) Operating on the Frequencies 121.5 MHz and 161.975/162.025 MHz (AIS)* (ETSI EN 303 098 V2.2.1). Sophia Antipolis: ETSI.
- Federal Communications Commission (2026). *Stations in the Maritime Services* (47 CFR Part 80). Washington, DC: US Government Publishing Office.
- International Association of Marine Aids to Navigation and Lighthouse Authorities (2012). *The AIS Service* (IALA Recommendation R0124, Edition 2.2). Saint-Germain-en-Laye: IALA.
- International Association of Marine Aids to Navigation and Lighthouse Authorities (2021). *The Use of the Automatic Identification System (AIS) in Marine Aids to Navigation Services* (IALA Recommendation R0126, Edition 2.0). Saint-Germain-en-Laye: IALA.
- International Electrotechnical Commission (2002). *IEC 60945:2002: Maritime Navigation and Radiocommunication Equipment and Systems — General Requirements* (Edition 4.0). Geneva: IEC.
- International Electrotechnical Commission (2010). *IEC 61097-14:2010: GMDSS Part 14: AIS Search and Rescue Transmitter (AIS-SART)* (Edition 1.0). Geneva: IEC.
- International Electrotechnical Commission (2015). *IEC 62320-1:2015: Maritime Navigation and Radiocommunication Equipment and Systems — Automatic Identification Systems (AIS) — Part 1: AIS Base Stations* (Edition 2.0). Geneva: IEC.
- International Electrotechnical Commission (2016). *IEC 62320-2:2016: Maritime Navigation and Radiocommunication Equipment and Systems — Automatic Identification Systems (AIS) — Part 2: AIS AtoN Stations* (Edition 2.0). Geneva: IEC.
- International Electrotechnical Commission (2017). *IEC 62287-1:2017: Maritime Navigation and Radiocommunication Equipment and Systems — Class B Shipborne Equipment of the AIS — Part 1: Carrier-Sense TDMA (CSTDMA)* (Edition 3.0). Geneva: IEC.
- International Electrotechnical Commission (2017). *IEC 62287-2:2017: Maritime Navigation and Radiocommunication Equipment and Systems — Class B Shipborne Equipment of the AIS — Part 2: Self-Organising TDMA (SOTDMA)* (Edition 2.0). Geneva: IEC.
- International Electrotechnical Commission (2018). *IEC 61993-2:2018: Maritime Navigation and Radiocommunication Equipment and Systems — Automatic Identification Systems (AIS) — Part 2: Class A Shipborne Equipment* (Edition 3.0). Geneva: IEC.
- International Electrotechnical Commission (2021). *IEC 61097-2:2021: Global Maritime Distress and Safety System (GMDSS) — Part 2: Cospas-Sarsat EPIRB* (Edition 4.0). Geneva: IEC.
- International Maritime Organization (1998). *Recommendation on Performance Standards for a Universal Shipborne Automatic Identification System (AIS)* (Resolution MSC.74(69), Annex 3). London: IMO.
- International Maritime Organization (2003). *Guidelines for the Installation of a Shipborne Automatic Identification System (AIS)* (SN/Circ.227). London: IMO.
- International Telecommunication Union (2026). *Technical Characteristics for an Automatic Identification System Using Time Division Multiple Access in the VHF Maritime Mobile Band* (Recommendation ITU-R M.1371-6). Geneva: ITU-R.
- Studer, A. (2026). *dAISy Family of AIS Receivers: Technical Manual and Architecture*. Redmond, WA: Wegmatt LLC. URL: https://wegmatt.com/
- United States Coast Guard Navigation Center (2026). *AIS Frequently Asked Questions and Equipment Authorization*. Alexandria, VA: USCG NAVCEN. URL: https://www.navcen.uscg.gov/
