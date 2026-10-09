# Chapter 69 — "AIS 2.0", VDES, and other channels: what is real

> **Part X — Adjacent and complementary systems; the future.** Navigational VHF spectrum is evolving beyond legacy 9.6 kbit/s broadcasts toward the multi-component VHF Data Exchange System, clearing application congestion while preserving core safety links.

**In this chapter.** You will learn what the VHF Data Exchange System (**VDES**) actually is, dissecting its four constituent subsystems—legacy **AIS**, Application-Specific Messages (**ASM**), terrestrial VHF data exchange (**VDE-TER**), and satellite VHF data exchange (**VDE-SAT**)—and separating international standards from commercial "AIS 2.0" marketing. We trace the spectrum allocations codified in Radio Regulations Appendix 18 across WRC-15 and WRC-19, analyzing contiguous channel aggregation up to 100 kHz, higher-order modulations from $\pi/4$-QPSK up to 16-QAM, and the mathematical derivation of advertised "32×" throughput gains. You will inspect the orbital performance and link budgets of pioneering VDE-SAT missions including NorSat-2, Sternula-1, and YMIR-1, and examine the May 2026 International Maritime Organization (**IMO**) regulatory milestones (Resolutions MSC.583(111), MSC.592(111), and MSC.593(111)) governing voluntary carriage under SOLAS Chapter V entering into force on 1 January 2028. Finally, you will explore historical and secondary channels used across the maritime mobile band—including long-range AIS channels 75 and 76, AMRD safety allocations, DSC channel 70 management, and regional channel assignment commands via Message 22—equipping you to design resilient coastal and shipboard systems.

---

## 69.1 Deconstructing "AIS 2.0": marketing vs. international standards

In maritime trade press, conference keynotes, and commercial brochures, the phrase **"AIS 2.0"** appears frequently as a catch-all label for next-generation maritime radio. Commercial space startups, equipment vendors, and digital service providers promise high-speed ship-to-shore connectivity, seamless internet-of-things (**IoT**) tracking, real-time electronic chart distribution, and encrypted messaging under this banner. 

In official regulatory and standardization bodies, however, "AIS 2.0" does not exist. 

The International Telecommunication Union Radiocommunication Sector (**ITU-R**), the International Maritime Organization (**IMO**), the International Electrotechnical Commission (**IEC**), and the International Association of Marine Aids to Navigation and Lighthouse Authorities (**IALA**) do not recognize any standard, specification, or protocol bearing the designation "AIS 2.0." The standardized system is the **VHF Data Exchange System (VDES)**, defined comprehensively in Recommendation ITU-R M.2092.

The distinction is not merely semantic; it represents a fundamental architectural boundary:
1. **Legacy AIS is retained, not replaced:** Under ITU-R M.2092-2 and IMO Resolution MSC.592(111), the legacy Automatic Identification System defined in Recommendation ITU-R M.1371 is embedded intact as one of four functional components of VDES. AIS does not undergo a breaking protocol revision. Its 9,600 bit/s Gaussian Minimum Shift Keying (**GMSK**) waveform, its 26.67 ms slot structure, its carrier sense and self-organizing access schemes ([Chapter 21](ch21-link-layer-tdma.md)), and its dedicated channels AIS 1 and AIS 2 remain unchanged.
2. **VDES protects safety of navigation:** The motivation for creating VDES was not to deprecate AIS, but to save it from choking on its own success. The proliferation of binary Application-Specific Messages (**ASM**)—including meteorological observations, oceanographic telemetry, lock schedules, and route exchanges ([Chapter 23](ch23-asm-binary-payloads.md))—threatened to saturate the VHF Data Link (**VDL**) in high-density waterways like the English Channel and the Malacca Strait ([Chapter 30](ch30-network-loading-packet-loss.md)). VDES segregates data-heavy messaging onto dedicated spectrum, offloading traffic from the primary safety channels.
3. **Carriage remains backward-compatible:** A SOLAS Class A vessel carrying a traditional AIS transponder built to IEC 61993-2 remains fully visible to, and capable of tracking, a vessel fitted with a state-of-the-art VDES transponder.

> **Definitions that bite.**
> - **VDES (VHF Data Exchange System):** The overarching radiocommunication architecture governed by Recommendation ITU-R M.2092, integrating AIS, ASM, VDE-TER, and VDE-SAT into a coordinated maritime mobile band framework.
> - **"AIS 2.0":** A commercial marketing term used by vendors to promote VDES equipment, software, or satellite connectivity services. It has no formal definition in ITU, IMO, IEC, or IALA documents.
> - **VDE (VHF Data Exchange):** The wideband data communications portion of VDES, comprising terrestrial (VDE-TER) and satellite (VDE-SAT) components using advanced digital modulations ($\pi/4$-QPSK, 8-PSK, 16-QAM). VDE excludes the narrowband GMSK AIS and ASM channels.
> - **ASM (Application-Specific Messages):** In legacy AIS, ASM refers to binary payload structures (Messages 6, 8, 25, and 26) transmitted on AIS 1 and AIS 2. In VDES, ASM refers specifically to the dedicated duplex channels (ASM 1 and ASM 2) set aside to carry these payloads away from the collision-avoidance link.

---

## 69.2 The four functional components of VDES

Recommendation ITU-R M.2092 establishes VDES as an integrated maritime communication system operating across the maritime VHF band (156.025 MHz to 162.025 MHz). To balance high-throughput digital exchange with safety-of-life backward compatibility, M.2092 partitions VDES into four distinct functional subsystems.

```
+-----------------------------------------------------------------------------------+
|                        VHF DATA EXCHANGE SYSTEM (VDES)                            |
|                            (ITU-R Rec. M.2092-2)                                  |
+-------------------------+-------------------------+-------------------------------+
|    NARROWBAND SAFETY    |    NARROWBAND BINARY    |       WIDEBAND DATA (VDE)     |
|   (25 kHz, 9.6 kbit/s)  |   (25 kHz, 9.6 kbit/s)  |    (25 / 50 / 100 kHz raster) |
+-------------------------+-------------------------+---------------+---------------+
|       AIS COMPONENT     |      ASM COMPONENT      |    VDE-TER    |    VDE-SAT    |
|     (ITU-R Rec. M.1371) |   (Channels ASM 1/2)    | (Terrestrial) |  (Satellite)  |
|                         |                         |               |               |
| • Ship-to-ship safety   | • Met/Hydro telemetry   | • High-speed  | • Global two- |
| • Pos reports (Msg 1-3) | • Virtual AtoN reports  |   shore data  |   way data    |
| • SOTDMA link layer     | • Route exchange        | • S-100 sync  | • Polar/ocean |
| • 161.975 / 162.025 MHz | • 161.950 / 162.000 MHz | • QPSK/16-QAM | • QPSK mod    |
+-------------------------+-------------------------+---------------+---------------+
```

### 69.2.1 The AIS component
The AIS component within VDES consists of the legacy protocol specified in Recommendation ITU-R M.1371. It operates on two international simplex frequencies:
- **AIS 1 (Channel 2087):** 161.975 MHz
- **AIS 2 (Channel 2088):** 162.025 MHz

Both channels use 25 kHz channel bandwidth and 9,600 bit/s GMSK modulation ($BT = 0.4$ transmit, $BT = 0.5$ receive). The AIS subsystem handles ship-to-ship collision avoidance, automated position reporting (Messages 1, 2, and 3 for Class A; Messages 18 and 19 for Class B), base station broadcasts (Message 4), SAR locating, and Aids to Navigation broadcasts (Message 21). Under VDES rules, general data communications and binary messaging are systematically migrated away from these two channels to preserve their capacity for safety-critical tracking.

### 69.2.2 The ASM component
The Application-Specific Message (**ASM**) component provides dedicated spectrum for structured binary data exchange, relieving the AIS channels of non-navigational burdens. It operates across two dedicated 25 kHz channels:
- **ASM 1 (Channel 2027):** 161.950 MHz
- **ASM 2 (Channel 2028):** 162.000 MHz

The physical layer of ASM remains identical to AIS: 9,600 bit/s GMSK with standard TDMA framing (2,250 slots per minute). However, transponders supporting VDES transmit Messages 6 (addressed binary), 8 (broadcast binary), 25 (single-slot binary), and 26 (multi-slot binary with communications state) exclusively on ASM 1 and ASM 2 unless instructed otherwise by regional channel commands.

By migrating environmental observations (water levels, tidal currents, wind vectors), lock management data, berthing reservations, and synthetic AtoN telemetry to ASM 1 and 2, coastal authorities can expand smart-port and e-navigation deployments without increasing VDL packet loss on AIS 1 and 2.

### 69.2.3 Terrestrial VHF Data Exchange (VDE-TER)
**VDE-TER** is the terrestrial wideband communication subsystem of VDES. Designed for high-capacity ship-to-shore, shore-to-ship, and ship-to-ship communications within line-of-sight coastal waters (typically 20 to 30 nautical miles from a shore base station), VDE-TER introduces modern digital communication techniques into maritime VHF:
- **Scalable channel aggregation:** VDE-TER channels can be operated as single 25 kHz channels or aggregated into contiguous 50 kHz or 100 kHz blocks.
- **Advanced modulations:** Rather than constant-envelope GMSK, VDE-TER utilizes linear digital modulations, including Quadrature Phase Shift Keying ($\pi/4$-QPSK), 8-ary Phase Shift Keying (**8-PSK**), and 16-ary Quadrature Amplitude Modulation (**16-QAM**).
- **Adaptive modulation and coding (AMC):** Link performance adapts dynamically to channel signal-to-noise ratio (**SNR**), switching coding rates and modulation depths to maximize throughput while maintaining target bit error rates.
- **Link-layer architecture:** VDE-TER uses scheduled Carrier Sense Multiple Access (**CSMA**) and centrally controlled reservation schemes managed by coastal base stations, supporting seamless IP data transfer, route exchange, and electronic chart updates.

### 69.2.4 Satellite VHF Data Exchange (VDE-SAT)
**VDE-SAT** extends the high-speed data capabilities of VDES beyond coastal line-of-sight to global ocean coverage through Low Earth Orbit (**LEO**) satellite constellations. Operating in dedicated segments of Appendix 18 spectrum, VDE-SAT provides:
- **Uplink (ship-to-satellite):** Ships transmit reporting data, sensor logs, and operational telemetry to overhead satellites.
- **Downlink (satellite-to-ship):** Orbiting satellites broadcast maritime safety information (**MSI**), search and rescue notices, weather routing updates, ice charts, and S-100 navigational data layers directly to shipboard VDES transponders.

Because orbital Doppler shifts, multi-satellite visibility, and vast satellite footprints (exceeding 2,500 km in diameter) preclude autonomous SOTDMA slot reservations, VDE-SAT incorporates specialized physical and link layer mechanisms. These include robust forward error correction (**FEC**), expanded guard times, and power-flux density (**PFD**) limits designed to protect co-channel terrestrial VHF services from orbital interference.

---

## 69.3 Spectrum allocations and the Appendix 18 channel plan

The radio spectrum supporting maritime communications is governed globally by the ITU **Radio Regulations (RR)**. Appendix 18 of the Radio Regulations contains the international table of transmitting frequencies in the VHF maritime mobile band (156.000 MHz to 162.050 MHz).

Carving out sufficient contiguous spectrum for VDES required more than a decade of complex diplomatic and technical negotiations across two World Radiocommunication Conferences: **WRC-15** in Geneva and **WRC-19** in Sharm el-Sheikh.

```
       APPENDIX 18 VDES FREQUENCY PLAN (LOWER AND UPPER LEGS)

  LOWER LEG (Ship Transmit / Terrestrial & Satellite Uplink):
  157.1875 MHz                                                  157.3375 MHz
  +-----------+-----------+-----------+-----------+-----------+-----------+
  |  Ch 1024  |  Ch 1084  |  Ch 1025  |  Ch 1085  |  Ch 1026  |  Ch 1086  |
  | 157.200   | 157.225   | 157.250   | 157.275   | 157.300   | 157.325   |
  | (25 kHz)  | (25 kHz)  | (25 kHz)  | (25 kHz)  | (25 kHz)  | (25 kHz)  |
  +-----------+-----------+-----------+-----------+-----------+-----------+
  |<-------------- VDE-TER Lower (100 kHz) ------------->|<-- VDE-SAT Up --->|

  UPPER LEG (Coast Transmit / Direct Ship-to-Ship / Satellite Downlink):
  161.7875 MHz                                                  162.0375 MHz
  +-----------+-----------+-----------+-----------+-----------+-----------+-----+-----+-----+-----+
  |  Ch 2024  |  Ch 2084  |  Ch 2025  |  Ch 2085  |  Ch 2026  |  Ch 2086  | 2027| 2087| 2028| 2088|
  | 161.800   | 161.825   | 161.850   | 161.875   | 161.900   | 161.925   |161.9|161.9|162.0|162.0|
  | (25 kHz)  | (25 kHz)  | (25 kHz)  | (25 kHz)  | (25 kHz)  | (25 kHz)  | 50  | 75  | 00  | 25  |
  +-----------+-----------+-----------+-----------+-----------+-----------+-----+-----+-----+-----+
  |<-------------- VDE-TER Upper (100 kHz) ------------->|<- VDE-SAT Dn ->| ASM1| AIS1| ASM2| AIS2|
```

### 69.3.1 Regulatory history: WRC-12, WRC-15, and WRC-19
Historically, Appendix 18 channels 24, 84, 25, 85, 26, and 86 were assigned as international public correspondence duplex channels. As commercial marine radiotelephony shifted to satellite communications, these VHF channels experienced low utilization.
- **WRC-12:** Began exploratory studies on maritime mobile spectrum utilization and the growing saturation of AIS 1 and AIS 2.
- **WRC-15:** Adopted Resolution 360 (Rev. WRC-15), which formally designated channels 2027 (ASM 1) and 2028 (ASM 2) for application-specific messages. WRC-15 also established the terrestrial channel plan for VDE-TER, merging channels 24, 84, 25, and 85 into candidate broadband blocks. However, consensus could not be reached regarding satellite downlink power levels, deferring VDE-SAT allocations to the next conference cycle.
- **WRC-19:** Under Agenda Item 1.9.2, WRC-19 finalized the regulatory framework for VDE-SAT. The conference allocated channels 1026 and 1086 for ship-to-satellite uplinks and channels 2026 and 2086 for satellite-to-ship downlinks under Appendix 18 footnote *w)*, establishing strict power-flux density limits to protect terrestrial mobile receivers.

### 69.3.2 Appendix 18 numbering and channel arithmetic
Under the Appendix 18 numbering scheme, maritime channels in the 1000 series indicate the lower leg (former ship transmit leg, centered around 157 MHz), while the 2000 series designates the upper leg (former coast transmit leg, centered around 161 MHz). Four-digit simplex channels represent 25 kHz single frequencies:
- The base duplex pair 24 consists of ship transmit on 157.200 MHz and coast transmit on 161.800 MHz.
- In simplex notation, $1024 = 157.200\text{ MHz}$ and $2024 = 161.800\text{ MHz}$.
- Interleaved channels sit 12.5 kHz offset: channel 84 sits at $157.225\text{ MHz}$ ($1084$) and $161.825\text{ MHz}$ ($2084$).

The VDES channel assignment is organized as follows:
- **VDE-TER Lower Leg:** Channels 1024, 1084, 1025, 1085 (157.1875–157.2875 MHz). Used for terrestrial ship-to-shore transmission. Can be aggregated into a single 50 kHz or 100 kHz contiguous channel.
- **VDE-TER Upper Leg:** Channels 2024, 2084, 2025, 2085 (161.7875–161.8875 MHz). Used for terrestrial shore-to-ship or ship-to-ship transmission. Aggregates up to 100 kHz.
- **VDE-SAT Uplink:** Channels 1026 (157.300 MHz) and 1086 (157.325 MHz). Transmitted from ships to satellites.
- **VDE-SAT Downlink:** Channels 2026 (161.900 MHz) and 2086 (161.925 MHz). Broadcast from satellites to ships.
- **ASM Channels:** Channel 2027 (ASM 1, 161.950 MHz) and Channel 2028 (ASM 2, 162.000 MHz).
- **AIS Channels:** Channel 2087 (AIS 1, 161.975 MHz) and Channel 2088 (AIS 2, 162.025 MHz).

---

## 69.4 Physical layer, modulations, and data rates: the "32×" claim

A standard claim in marketing literature is that VDES delivers **"32 times the speed of AIS."** Understanding where this number originates—and what its operational caveats are—requires examining the physical layer characteristics defined in ITU-R M.2092-2.

### 69.4.1 Comparing AIS and VDE-TER physical parameters
Legacy AIS is constrained by 1990s RF hardware assumptions: it utilizes constant-envelope GMSK modulation inside a strict 25 kHz mask, achieving a raw symbol rate of 9,600 baud at 1 bit per symbol, resulting in an unencoded gross data rate of 9.6 kbit/s.

VDE-TER employs multi-carrier or single-carrier filtered linear modulations combined with root-raised cosine (**RRC**) pulse shaping and aggressive Forward Error Correction (**FEC**) using Turbo codes or Low-Density Parity-Check (**LDPC**) codes.

| Parameter | AIS (ITU-R M.1371) | ASM (ITU-R M.2092) | VDE-TER Narrow (25 kHz) | VDE-TER Wide (100 kHz) | VDE-SAT Downlink |
|---|---|---|---|---|---|
| **Channel Bandwidth** | 25 kHz | 25 kHz | 25 kHz | 100 kHz | 50 kHz or 100 kHz |
| **Modulation** | GMSK ($BT=0.4$) | GMSK ($BT=0.4$) | $\pi/4$-QPSK, 8-PSK, 16-QAM | $\pi/4$-QPSK, 8-PSK, 16-QAM | QPSK / $\pi/4$-QPSK |
| **Gross Symbol Rate** | 9.6 kbaud | 9.6 kbaud | 19.2 kbaud | 76.8 kbaud | 38.4 kbaud (50 kHz) |
| **Bits per Symbol** | 1 bit | 1 bit | 2, 3, or 4 bits | 2, 3, or 4 bits | 2 bits |
| **Coding Rate ($R$)** | None (CRC only) | None (CRC only) | $R = 1/2, 3/4$ | $R = 1/2, 3/4$ | $R = 1/2$ FEC |
| **Gross Link Rate** | 9.6 kbit/s | 9.6 kbit/s | Up to 76.8 kbit/s | Up to 307.2 kbit/s | Up to 76.8 kbit/s |
| **Access Scheme** | SOTDMA / CSTDMA | SOTDMA / CSTDMA | CSMA / Scheduled TDMA | CSMA / Scheduled TDMA | Slotted ALOHA / TDMA |

> **Worked example.** The arithmetic of "32× AIS".
> 
> Vendors derive the "32×" throughput multiple by dividing the maximum unencoded gross burst rate of VDE-TER on a 100 kHz aggregated channel by the gross link rate of legacy AIS:
> $$\text{Gross Speedup} = \frac{307.2\text{ kbit/s}}{9.6\text{ kbit/s}} = 32.0$$
> 
> How does VDE-TER achieve 307.2 kbit/s?
> 1. **Bandwidth expansion (4×):** Four contiguous 25 kHz channels (1024, 1084, 1025, 1085) are merged into one 100 kHz broadband channel. At a pulse-shaping factor of $\alpha \approx 0.3$, the channel accommodates a symbol rate of $R_s = 76.8\text{ kbaud}$ ($4 \times 19.2\text{ kbaud}$).
> 2. **Modulation depth (4×):** 16-QAM encodes 4 bits per symbol ($\log_2(16) = 4$).
> 3. **Combined gross bit rate:**
>    $$\text{Rate}_{\text{gross}} = 76.8\text{ kbaud} \times 4\text{ bits/symbol} = 307.2\text{ kbit/s}$$
> 
> **The operational reality:**
> 16-QAM is an unrobust modulation in maritime multipath environments. To close the link under fading and sea clutter, VDE-TER applies a rate $R = 3/4$ or $R = 1/2$ FEC code. With rate $3/4$ Turbo coding, net throughput drops to:
> $$\text{Rate}_{\text{net}} = 307.2 \times 0.75 = 230.4\text{ kbit/s}$$
> If a ship experiences deep fading near the radio horizon and falls back to robust $\pi/4$-QPSK with rate $1/2$ coding, throughput is:
> $$\text{Rate}_{\text{robust}} = 76.8\text{ kbaud} \times 2\text{ bits/symbol} \times 0.5 = 76.8\text{ kbit/s}$$
> Furthermore, VDE-TER is a shared TDMA channel managed by shore base stations; 307.2 kbit/s is the total cell burst capacity, not an uncontended pipeline for an individual vessel.

---

## 69.5 VDE-SAT in orbit: satellites, payloads, and realities

While terrestrial VDE-TER trials demonstrated high data rates in harbor environments, the satellite component (**VDE-SAT**) required proving that VHF digital signals could penetrate the ionosphere, survive severe Doppler shifts, and communicate reliably with micro-spacecraft in Low Earth Orbit (**LEO**).

```
+-----------------------------------------------------------------------------------------+
|                                TABLE OF VDE-SAT MISSIONS                                |
+-------------+---------------------+--------------+-------------+------------------------+
| Satellite   | Operator / Nation   | Launch Date  | Status      | Payload & Details      |
+-------------+---------------------+--------------+-------------+------------------------+
| NorSat-2    | Space Norway / SFL  | 14 Jul 2017  | Operational | Kongsberg Seatex VDES; |
|             | Norway / Canada     | (Soyuz-2.1a) | in orbit    | First VDE payload flown|
+-------------+---------------------+--------------+-------------+------------------------+
| Sternula-1  | Sternula / Aalborg  | 03 Jan 2023  | Re-entered  | MARIOT project 6U;     |
|             | Denmark             | (Falcon 9)   | 07 Jan 2025 | Commercial demo; DMI   |
+-------------+---------------------+--------------+-------------+------------------------+
| NorSat-TD   | Norwegian Space Ag. | 15 Apr 2023  | Re-entered  | Upgraded Kongsberg     |
|             | Norway / SFL        | (Falcon 9)   | May 2025    | VDES payload; laser terminal |
+-------------+---------------------+--------------+-------------+------------------------+
| YMIR-1      | AAC Clyde / Saab    | 11 Nov 2023  | Operational | Saab R6 VDES payload;  |
|             | Sweden / ORBCOMM    | (Falcon 9)   | in orbit    | Bi-directional testing |
+-------------+---------------------+--------------+-------------+------------------------+
```

### 69.5.1 NorSat-2: the pathfinder
Launched on 14 July 2017 aboard a Soyuz-2.1a from Baikonur, **NorSat-2** was a 16 kg microsatellite developed by the University of Toronto Institute for Aerospace Studies Space Flight Laboratory (**UTIAS/SFL**) for Space Norway and the Norwegian Space Centre. It carried the world's first VDES satellite payload, engineered by Kongsberg Seatex, equipped with a custom deployable crossed-Yagi antenna tuned to the maritime VHF band.

NorSat-2 demonstrated the physical feasibility of receiving VDE-SAT uplinks from terrestrial test stations in Norway and broadcasting downlinks back to surface receivers. It proved that Doppler compensation algorithms on the ground could synchronize with LEO passes at speeds exceeding 7.5 km/s ($\approx \pm 4\text{ kHz}$ Doppler shift at 160 MHz).

### 69.5.2 Sternula-1 and the MARIOT project
On 3 January 2023, SpaceX Transporter-6 placed **Sternula-1** into orbit. Built by Space Inventor for Danish satellite operator Sternula, the 6U CubeSat served as the commercial demonstration platform for the Danish MARIOT (**Maritime IoT**) consortium, which included GateHouse SatCom, Satlab, and the Danish Meteorological Institute (**DMI**).

Sternula-1 validated the delivery of digital weather charts and navigational warnings directly to ships in Arctic waters off Greenland. Due to high atmospheric drag during the 2024–2025 solar maximum, Sternula-1 naturally decayed and re-entered the atmosphere on 7 January 2025, having proven commercial message handling.

### 69.5.3 YMIR-1 and the AOS consortium
On 11 November 2023, the **YMIR-1** satellite launched aboard a Falcon 9 from Vandenberg Space Force Base. Developed by AAC Clyde Space in partnership with Saab and ORBCOMM under the AOS consortium, YMIR-1 integrated Saab's next-generation R6 VDES payload. YMIR-1 demonstrated automated, bi-directional store-and-forward messaging over VDE-SAT, connecting shipboard transponders directly to cloud logistics networks without intermediary satellite ground stations.

> **Rule of thumb.** Satellite downlinks and AIS receivers.
> 
> *No satellite has ever broadcast legacy M.1371 AIS position reports downward to mariners' bridges as an operational navigation service.*
> 
> Satellites receive terrestrial AIS broadcasts (known as **SAT-AIS**; [Chapter 39](ch39-satellite-ais.md)), but they do not re-transmit Message 1, 2, or 3 downlinks on AIS 1 or AIS 2. Transmitting AIS downlinks from orbit would cause catastrophic packet collisions across vast 5,000-kilometer satellite visibility circles, blinding shipboard transponders within thousands of local SOTDMA cells simultaneously. VDE-SAT downlinks occur strictly on dedicated Appendix 18 channels (2026/2086) using power-flux density limits, ensuring that orbital downlinks cannot disrupt bridge collision-avoidance displays.

---

## 69.6 IMO carriage status: MSC 111, SOLAS Chapter V, and 2028

A frequent source of confusion among shipowners and maritime software developers is whether VDES is mandatory, and if so, when.

### 69.6.1 The outcomes of MSC 111 (May 2026)
At the 111th session of the IMO Maritime Safety Committee (**MSC 111**), held from 13 to 22 May 2026, the IMO completed the formal integration of VDES into the international maritime safety framework:
1. **Resolution MSC.583(111):** Adopted formal amendments to Chapter V of the International Convention for the Safety of Life at Sea (**SOLAS**), specifically Regulation 19 (*Carriage requirements for shipborne navigational systems and equipment*), and corresponding codes (1994 and 2000 HSC Codes).
2. **Resolution MSC.592(111):** Formally introduced VDES into the IMO regulatory framework, establishing that references to "AIS" throughout IMO conventions may be satisfied by the AIS component of an approved VDES station.
3. **Resolution MSC.593(111):** Established the international *Performance Standards for Shipborne VHF Data Exchange System (VDES)*.
4. **MSC.1/Circ.1699:** Issued the *Guidelines for the Onboard Operational Use of Shipborne VDES*.

### 69.6.2 Voluntary alternative, not a mandatory carriage requirement
The critical legal reality established by MSC 111 is that **VDES is not mandated under SOLAS.**

Under Resolution MSC.583(111), which enters into force on **1 January 2028** under tacit acceptance:
- Shipowners are **permitted** to fit an approved VDES mobile station as a **voluntary alternative** to fulfill the mandatory AIS carriage requirement under SOLAS Regulation V/19.2.4.
- Because an approved VDES unit incorporates a fully compliant Class A AIS subsystem, fitting VDES satisfies all carriage requirements for AIS.
- However, fitting a legacy Class A transponder remains completely lawful. No vessel is compelled to decommission an operating AIS unit or install VDES equipment.
- As Resolution MSC.592(111) explicitly notes, advanced functionalities provided by VDES (such as VDE-TER broadband or VDE-SAT satellite data) are non-navigational additions; they are not considered a legal substitute for the continuous broadcast of AIS safety data.

### 69.6.3 Type-approval testing: IEC 63514
To enable shipborne VDES installations to receive statutory certification, the International Electrotechnical Commission developed **IEC 63514** (*Maritime navigation and radiocommunication equipment and systems — VHF Data Exchange System (VDES) — Shipborne mobile station — Operational and performance requirements, methods of test and required test results*). 

Supervised by IEC Technical Committee 80 (Working Group 15), IEC 63514 translates ITU-R M.2092-2 and IMO Resolution MSC.593(111) into concrete test procedures:
- Environmental and EMC testing per IEC 60945.
- Radio frequency testing for multi-carrier emissions, adjacent channel power ratios (**ACPR**), and intermodulation under multi-band operation.
- TDMA and CSMA timing compliance across merged 25, 50, and 100 kHz bandwidths.
- Dual Ethernet network interfaces conforming to IEC 61162-450 (Lightweight Ethernet).

---

## 69.7 Other channels used for AIS and maritime data

Although AIS is universally associated with 161.975 MHz and 162.025 MHz, the protocol family operates across several other VHF channels designated by international treaty.

```
+-----------------------------------------------------------------------------------------+
|                    SPECIALIZED CHANNELS IN THE AIS & VDES ECOSYSTEM                     |
+---------------+---------------+--------------------+------------------------------------+
| Channel No.   | Frequency     | Regulatory Role    | Operational Usage                  |
+---------------+---------------+--------------------+------------------------------------+
| Ch 75         | 156.775 MHz   | Long-Range Uplink  | Guard band to Ch 16; carries       |
|               |               | (App 18 note s)    | Message 27 satellite uplink bursts |
+---------------+---------------+--------------------+------------------------------------+
| Ch 76         | 156.825 MHz   | Long-Range Uplink  | Guard band to Ch 16; paired with   |
|               |               | (App 18 note s)    | Ch 75 for satellite Message 27     |
+---------------+---------------+--------------------+------------------------------------+
| Ch 70         | 156.525 MHz   | Digital Selective  | DSC Channel Management; commands   |
|               |               | Calling (DSC)      | regional frequency switching       |
+---------------+---------------+--------------------+------------------------------------+
| Ch 2006       | 160.900 MHz   | AMRD Group B       | Autonomous Maritime Radio Devices; |
|               |               | (ITU-R M.2135-1)   | fishing net buoys, non-safety tags |
+---------------+---------------+--------------------+------------------------------------+
| Ch 2027/2028  | 161.950 MHz   | ASM 1 and ASM 2    | VDES Application-Specific Messages |
|               | 162.000 MHz   | (App 18 note w)    | (Messages 6, 8, 25, 26)            |
+---------------+---------------+--------------------+------------------------------------+
| Ch 2087/2088  | 161.975 MHz   | AIS 1 and AIS 2    | Primary AIS safety & tracking;     |
|               | 162.025 MHz   | (App 18)           | SOTDMA position & static reports   |
+---------------+---------------+--------------------+------------------------------------+
```

### 69.7.1 Long-range AIS: Channels 75 and 76
Under ITU Radio Regulations Appendix 18 footnote *s)*, channels 75 (156.775 MHz) and 76 (156.825 MHz)—originally established as protective guard bands flanking VHF distress channel 16 (156.800 MHz)—are allocated for satellite detection of long-range AIS transmissions.

As detailed in Recommendation ITU-R M.1371-6 (Annex 3), Class A transponders broadcast **Message 27** on channels 75 and 76. Message 27 is an abbreviated 96-bit position burst designed specifically for low-overhead satellite reception in open ocean waters ([Chapter 39](ch39-satellite-ais.md)). By transmitting Message 27 on channels 75 and 76 with a nominal 3-minute interval, ships remain trackable across vast oceanic areas without consuming capacity on coastal AIS 1 and 2.

### 69.7.2 AMRD Group B: Channel 2006
The proliferation of cheap, low-power AIS transmitters attached to fishing gear and fish aggregating devices (**FADs**) presented a grave safety risk to international navigation, cluttering bridge displays with thousands of phantom vessels ([Chapter 68](ch68-special-purpose-ais.md)).

In response, ITU-R finalized Recommendation **M.2135-1** in February 2023, partitioning Autonomous Maritime Radio Devices into:
- **Group A:** Safety-of-navigation devices (such as approved man-overboard MOB beacons conforming to ETSI EN 303 098), which transmit on AIS 1 and AIS 2.
- **Group B:** Non-safety maritime devices (such as fishing net locators). M.2135-1 explicitly directs Group B transmitters to **Channel 2006 (160.900 MHz)**. 

Broadcasting on 160.900 MHz allows fishing vessels equipped with multichannel receivers to monitor their nets while keeping commercial radar and ECDIS screens completely clean of fishing gear clutter.

### 69.7.3 Digital Selective Calling (DSC): Channel 70
Under early editions of ITU-R M.1371 (Editions 1 through 5, Annex 3), coastal administrations were empowered to perform regional channel management over **DSC Channel 70 (156.525 MHz)**. 

A coastal base station could broadcast an ITU-R M.493 expansion symbol sequence commanding shipboard AIS transponders to switch operating frequencies within designated coordinate boundaries. In practice, DSC channel management proved operationally brittle and difficult to maintain; modern transponders execute channel management almost exclusively via over-the-air **Message 22** broadcasts on AIS 1 and 2. Consequently, M.1371-6 deleted the legacy DSC channel-management annex, consolidating frequency control into standard AIS message handling.

---

## 69.8 Regional frequency reallocation: Message 22 mechanics

Recommendation ITU-R M.1371 (Annex 7, Message 22) provides an automated mechanism allowing coastal administrations to reconfigure the VHF operational frequencies and bandwidth of all transponders entering sovereign waters.

```
       MESSAGE 22 CHANNEL MANAGEMENT BIT STRUCTURE (168 BITS)
 0        5 6  7 8                 37 38 39 40            51 52            63
+----------+----+--------------------+--+--+----------------+----------------+
| Msg ID   |Rep | Transponder MMSI   |Sp|Sp| Channel A      | Channel B      |
| (6 bits) |(2b)| (30 bits)          |1b|1b| (12 bits)      | (12 bits)      |
+----------+----+--------------------+--+--+----------------+----------------+
 64      67 68 69 70               87 88               105 106            123
+----------+--+--+--------------------+-------------------+------------------+
| Tx/Rx    |Tx|Pw| North-East Lat     | North-East Lon    | South-West Lat   |
| Mode (4b)|1b|1b| (18 bits)          | (18 bits)         | (18 bits)        |
+----------+--+--+--------------------+-------------------+------------------+
 124            141 142 143 144 145      147 148          167
+------------------+---+---+---+------------+----------------+
| South-West Lon   |Add|BwA|BwB| Transition | Spare bits     |
| (18 bits)        |1b |1b |1b | Zone (3b)  | (20 bits)      |
+------------------+---+---+---+------------+----------------+
```

### 69.8.1 Message 22 field anatomy
Message 22 can be transmitted as an addressed command to an individual vessel (using the target MMSI and setting the `Addressed` flag to 1) or as a geographic broadcast defining a rectangular switching bounding box:
- **Channel A and Channel B (12 bits each):** Define the operational frequency pair using Appendix 18 four-digit designators (e.g., `2087`, `2019`, `2078`).
- **Tx/Rx Mode (4 bits):** Controls transceiver operational state ($0 = \text{TxA/TxB, RxA/RxB}$; $1 = \text{TxA, RxA/RxB}$; $2 = \text{TxB, RxA/RxB}$; $3 = \text{Rx only}$).
- **Power (1 bit):** Forces low power ($1\text{ W}$, bit set to 1) or normal high power ($12.5\text{ W}$, bit set to 0).
- **Geographic Boundary (72 bits):** Defines the northeast and southwest corners of the switching zone, quantized to 0.1 minute of arc.
- **Transition Zone Size (3 bits):** Defines an external buffer zone extending 1 to 8 nautical miles outside the geographic perimeter. Within this perimeter, transponders monitor both legacy and new regional frequencies to guarantee continuous visibility while crossing borders.

### 69.8.2 The USCG Message 22 confusion incident
Regional frequency switching provides tremendous flexibility, but misconfiguration introduces catastrophic failure modes.

> **Case file.** The USCG 2010 Message 22 frequency-lock incident.
> In 2010, the United States Coast Guard Navigation Center (**NAVCEN**) issued an urgent maritime safety advisory regarding widespread AIS tracking failures in North American coastal zones. 
> 
> Several coastal base stations had transmitted Message 22 broadcasts instructing vessels within harbor approaches to shift their secondary channel to regional simplex frequencies to alleviate port congestion. Due to firmware defects in early Class A transponders manufactured prior to rigorous IEC 61993-2 testing:
> 1. Transponders successfully switched from Channel 2088 (AIS 2) to the regional frequency upon entering the defined geographic box.
> 2. However, upon departing the designated box and returning to open ocean waters, the transponders failed to clear the regional channel assignment from memory.
> 3. Transponders remained permanently tuned to regional simplex channels thousands of miles into the open Atlantic and Pacific oceans, completely deaf to AIS 2 traffic and failing to report on international safety frequencies.
> 
> The incident compelled national administrations to mandate persistent memory timeouts (reverting to default channels 2087 and 2088 after 500 minutes if no renewing Message 22 is received) and reinforced the maritime principle: *never alter core safety channels without automated fail-safe reversion.*

---

## 69.9 Migration realities: what to design for now

For maritime software engineers, electronics manufacturers, and regulatory authorities, navigating the decade between 2026 and 2035 requires designing systems capable of bridging legacy AIS with multi-channel VDES.

```
       THE DECADE OF TRANSITION: COEXISTENCE MATRIX (2026–2035)

  +----------------------+-----------------------+-----------------------+
  | Application Layer    | Legacy Vessels        | VDES-Equipped Vessels |
  |                      | (Class A / Class B)   | (IEC 63514 Certified) |
  +----------------------+-----------------------+-----------------------+
  | Position Reporting   | AIS 1 / AIS 2         | AIS 1 / AIS 2         |
  | (Collision Avoid)    | (9.6 kbit/s GMSK)     | (9.6 kbit/s GMSK)     |
  +----------------------+-----------------------+-----------------------+
  | Met/Hydro & Port Ops | Saturated on AIS 1/2  | Offloaded to ASM 1/2  |
  | (Binary Messages)    | (Dropped under load)  | (2027 / 2028 duplex)  |
  +----------------------+-----------------------+-----------------------+
  | High-Speed Shore IP  | Inmarsat / 4G / 5G    | VDE-TER Coastal Link  |
  | (S-100, Routes)      | (Costly satellite)    | (Up to 307.2 kbit/s)  |
  +----------------------+-----------------------+-----------------------+
  | Global Ocean IoT     | None / LRIT / Sat-AIS | VDE-SAT Orbital Link  |
  | (Sensor Reporting)   | (Receive-only Sat)    | (Two-way messaging)   |
  +----------------------+-----------------------+-----------------------+
```

### 69.9.1 Coexistence principles
1. **Never assume VDES carriage:** Until at least 2035, the vast majority of commercial and recreational vessels will continue operating standard Class A and Class B transponders. Any shore-to-ship safety alert or navigational hazard broadcast requiring universal reception must be transmitted on AIS 1 and 2.
2. **Dual-stack shore collection:** Modern coastal shore stations and Vessel Traffic Services must deploy multi-channel software-defined radio (**SDR**) architectures capable of monitoring 161.975 MHz, 162.025 MHz, 161.950 MHz, and 162.000 MHz simultaneously. Shore processing pipelines should ingest both legacy `!AIVDM` sentences and modern VDES NMEA extensions.
3. **Graceful degradation:** S-100 digital hydrographic services ([Chapter 52](ch52-ais-and-s100.md)) should be architected with VDES as a primary high-bandwidth coastal conduit, falling back to compressed ASM summaries over legacy channels when communicating with non-VDES vessels.

---

## Then & now

| Dimension | Legacy AIS (1998–2015) | The VDES Era (2015–Present) |
|---|---|---|
| **Primary Standard** | Recommendation ITU-R M.1371 (Annexes 1–9) ⟨H⟩ | Recommendation ITU-R M.2092-2 supported by M.1371-6 ⟨+⟩ |
| **Operational Bandwidth** | $2 \times 25\text{ kHz}$ fixed simplex frequencies ⟨H⟩ | Up to 100 kHz aggregated contiguous blocks in App 18 ⟨+⟩ |
| **Peak Burst Rate** | 9.6 kbit/s gross per channel ⟨H⟩ | 307.2 kbit/s gross (16-QAM VDE-TER terrestrial) ⟨+⟩ |
| **Modulation Schemes** | Gaussian Minimum Shift Keying (GMSK) only ⟨H⟩ | GMSK, $\pi/4$-QPSK, 8-PSK, and 16-QAM with AMC ⟨+⟩ |
| **Application Messages** | Competed directly with position reports on AIS 1/2 ⟨H⟩ | Migrated to dedicated channels ASM 1 and ASM 2 ⟨+⟩ |
| **Satellite Integration** | Receive-only (SAT-AIS uplink) detection ⟨H⟩ | Bi-directional VDE-SAT uplink and downlinks ⟨+⟩ |
| **IMO Regulatory Basis** | Mandatory carriage under SOLAS V/19.2.4 (MSC.74) ⟨H⟩ | Voluntary alternative to AIS under Res. MSC.583(111) ⟨+⟩ |
| **Bridge Ethernet** | Serial RS-422 / NMEA 0183 (IEC 61162-1/2) ⟨H⟩ | Dual Gigabit Ethernet (IEC 61162-450) mandatory ⟨+⟩ |

---

## On the wire

The link-layer operational mechanics of channel management and multi-channel VDES transceivers are expressed in standard international NMEA 0183 and IEC 61162-1 sentences. Here we examine how a coastal base station commands a regional frequency shift using Message 22.

### Bit-level breakdown of Message 22 NMEA payload
Consider an operational Base Station broadcast commanding vessels entering a port approach to shift their secondary channel from AIS 2 to regional channel 2019 (161.550 MHz):

```
!AIVDO,1,1,,A,F5Mwqgj1qv<7uWP1O?s<P2q2P000,0*11
```

```
Hex / 6-bit ASCII: F 5 M w q g j 1 q v < 7 u W P 1 O ? s < P 2 q 2 P 0 0 0
Binary bitstream (168 bits total):
000000: 010110 000101 011101 111001 110011 100111 101010 000001 110011 111110
000060: 011100 000111 111101 100111 011000 000001 011111 001111 110100 011100
000120: 011000 000010 110011 000010 011000 000000 000000 000000
```

Tracing the field definitions per Recommendation ITU-R M.1371-6 (Annex 7):
- **Bits 0–5 (Message ID):** `010110` = 22 (Message 22, Channel Management).
- **Bits 6–7 (Repeat Indicator):** `00` = 0 (original transmission).
- **Bits 8–37 (Source MMSI):** `010101110111100111001110011110` = 366999999 (USCG Base Station).
- **Bits 38–39 (Spare):** `00` = Reserved.
- **Bits 40–51 (Channel A):** `000001110011` = 2078 (Simplex frequency 161.525 MHz).
- **Bits 52–63 (Channel B):** `111110011100` = 2019 (Simplex frequency 161.550 MHz).
- **Bits 64–67 (Tx/Rx Mode):** `0000` = Tx A / Tx B, Rx A / Rx B (standard dual operation).
- **Bit 68 (High/Low Power):** `0` = False (retain normal 12.5 W high power).
- **Bits 69–86 (NE Latitude):** `000111111101100111` = 32,615 $\rightarrow$ $32,615 / 600 = 38.0^\circ\text{ N}$.
- **Bits 87–104 (NE Longitude):** `011000000001011111` (signed) $\rightarrow$ $-122.0^\circ\text{ W}$.
- **Bits 105–122 (SW Latitude):** $37.0^\circ\text{ N}$.
- **Bits 123–140 (SW Longitude):** $-123.0^\circ\text{ W}$.
- **Bit 141 (Addressed):** `0` = False (geographic broadcast zone).
- **Bit 142 (Bandwidth A):** `0` = Default 25 kHz.
- **Bit 143 (Bandwidth B):** `0` = Default 25 kHz.
- **Bits 144–146 (Transzone):** `101` = 5 nautical mile transitional boundary buffer.

> **Try it.** Parsing and verifying Message 22 in Python.
> 
> You can parse, inspect, and validate Message 22 channel management commands using `pyais` in the book virtual environment:
> 
> ```python
> import pyais
> 
> sentence = "!AIVDO,1,1,,A,F5Mwqgj1qv<7uWP1O?s<P2q2P000,0*11"
> msg = pyais.decode(sentence)
> 
> print(f"Message Type : {msg.msg_type}")
> print(f"Source MMSI  : {msg.mmsi}")
> print(f"Channel A    : {msg.channel_a}")
> print(f"Channel B    : {msg.channel_b}")
> print(f"Bounding Box : {msg.sw_lat}N, {msg.sw_lon}W to {msg.ne_lat}N, {msg.ne_lon}W")
> print(f"Buffer Zone  : {msg.zonesize} nmi")
> ```
> 
> Expected output:
> ```text
> Message Type : 22
> Source MMSI  : 366999999
> Channel A    : 2078
> Channel B    : 2019
> Bounding Box : 37.0N, -123.0W to 38.0N, -122.0W
> Buffer Zone  : 5 nmi
> ```

---

## Validation, uncertainty & data quality

Transitioning to multi-channel VDES introduces complex physical-layer and system-level validation challenges that do not exist in traditional single-frequency AIS monitoring.

### RF phase noise and Error Vector Magnitude (EVM)
Legacy GMSK decoders rely on FM discriminators or simple zero-crossing detectors where amplitude variations are irrelevant. In contrast, VDE-TER and VDE-SAT utilize linear modulations (up to 16-QAM) where amplitude and phase fidelity are critical. 

Transmitter performance is validated using **Error Vector Magnitude (EVM)**, defined as the root-mean-square ratio of the error vector between ideal constellation symbol locations and measured received symbols:
$$\text{EVM}_{\text{RMS}} = \sqrt{\frac{\frac{1}{N}\sum_{k=1}^N |S_{\text{meas}}[k] - S_{\text{ideal}}[k]|^2}{P_{\text{ref}}}} \times 100\%$$

Under IEC 63514 and ITU-R M.2092-2:
- 16-QAM transmissions require an $\text{EVM}_{\text{RMS}} \le 6.0\%$ across the entire burst. An uncalibrated power amplifier suffering from 1.5 dB of compression will distort outer constellation points, driving EVM above 12% and inducing severe packet drop rates on VDE-TER channels while standard AIS 1/2 GMSK broadcasts remain completely unaffected.

### Channel aggregation group delay and phase distortion
Aggregating four 25 kHz channels into a single 100 kHz contiguous passband requires exceptionally flat group delay across RF filters. If a receiver's intermediate frequency (**IF**) or software filter introduces more than 5 microseconds of differential group delay across the 100 kHz band edge:
- Inter-symbol interference (**ISI**) corrupts outer subcarriers.
- Bit error rates rise exponentially above the FEC threshold, collapsing the effective terrestrial link range from 25 nmi down to less than 8 nmi.

### Intermodulation in dense VHF environments
Shipboard transponders must transmit and receive simultaneously across closely spaced frequencies. The frequency separation between VDE-TER channels (157.200–161.850 MHz) and the ship's primary voice VHF radio (e.g., Channel 16 at 156.800 MHz) is less than 0.4 MHz. 

Without high-rejection cavity filters or circulators:
- A 25 W voice VHF transmission induces severe front-end receiver desensitization (**blocking**) in the VDES transponder.
- Non-linear mixing generates 3rd-order intermodulation products ($2f_1 - f_2$) falling directly into the VDE-SAT downlink channels (161.900/161.925 MHz), inducing transient tracking blindness.

---

## Software

**Open source:**
- **libais** (C++ / Python): The premier open-source library for decoding binary AIS messages. Supports extraction of Message 22 channel management parameters and Message 27 long-range packets. Caveat: does not process wideband VDE-TER/VDE-SAT physical waveforms or QAM constellations.
- **pyais** (Python): Pure-Python AIS decoding and encoding engine. Fully parses Message 22 channel management structures and multi-line binary payloads. Caveat: link-layer and bit-level decoding only; lacks an RF software-defined radio frontend.
- **GNU Radio** (C++ / Python toolkit): Open-source SDR processing framework with out-of-tree blocks for $\pi/4$-QPSK, 8-PSK, and 16-QAM burst demodulation. Caveat: requires extensive custom configuration and high-performance SDR hardware (USRP, HackRF) to handle 100 kHz Appendix 18 multi-channel streaming.

**Free but closed:**
- **Kongsberg VDES Test & Evaluation Suite**: Diagnostic Windows tool distributed to maritime administrations and research partners for logging VDES RF metrics, constellation diagrams, and EVM values during coastal trials. Caveat: tied to proprietary Kongsberg base station hardware.

**Commercial:**
- **Saab R6 Supreme VDES Toolset**: Software suite accompanying the Saab R6 Class A / VDES transponder. Manages dual IEC 61162-450 Ethernet streams, logs VDE-TER IP session states, and displays satellite pass link budgets. Caveat: proprietary software locked to commercial hardware keys.
- **CML Microcircuits DE9941 Demonstration Software**: Evaluation platform designed for the CMX994 / VDES1000 SDR chipset family, providing full-stack physical-layer control from RF registers up to MAC framing. Caveat: intended strictly for hardware design engineers, not operational bridge integration.

---

## Standards & guides

- **International Telecommunication Union (ITU):**
  - *Recommendation ITU-R M.2092-2 (02/2026)*: "Technical characteristics for a VHF data exchange system in the maritime mobile service." The governing international standard defining VDES components, channelization, physical layer waveforms, and MAC protocols.
  - *Recommendation ITU-R M.1371-6 (02/2026)*: "Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band." Governs the AIS component embedded within VDES.
  - *Radio Regulations (Edition 2024), Appendix 18*: "Table of transmitting frequencies in the VHF maritime mobile band." Formally establishes the international frequency allocations and footnotes ($s$, $w$) for AIS, ASM, VDE-TER, and VDE-SAT.
  - *Recommendation ITU-R M.2135-1 (02/2023)*: "Technical characteristics of autonomous maritime radio devices operating in the frequency band 156–162.05 MHz." Governs the segregation of AMRD Group B devices to Channel 2006.

- **International Maritime Organization (IMO):**
  - *Resolution MSC.583(111) (Adopted 21 May 2026)*: "Amendments to the International Convention for the Safety of Life at Sea, 1974, as Amended" (SOLAS Chapter V). Permits voluntary carriage of VDES as an alternative to AIS, entering into force 1 January 2028.
  - *Resolution MSC.592(111) (Adopted 21 May 2026)*: "Introduction of the VHF Data Exchange System (VDES) into the IMO Regulatory Framework."
  - *Resolution MSC.593(111) (Adopted 21 May 2026)*: "Performance Standards for Shipborne VHF Data Exchange System (VDES)."
  - *MSC.1/Circ.1699 (May 2026)*: "Guidelines for the Onboard Operational Use of Shipborne VDES."

- **International Electrotechnical Commission (IEC):**
  - *IEC 63514 Ed. 1.0 (in preparation)*: "Maritime navigation and radiocommunication equipment and systems — VHF Data Exchange System (VDES) — Shipborne mobile station — Operational and performance requirements, methods of test and required test results."
  - *IEC 61162-450:2024 (Ed. 3.0)*: "Maritime navigation and radiocommunication equipment and systems — Digital interfaces — Part 450: Multiple talkers and multiple listeners — Ethernet interconnection."

- **International Association of Marine Aids to Navigation and Lighthouse Authorities (IALA):**
  - *Guideline G1117 (Ed. 2.0)*: "VHF Data Exchange System (VDES) Overview."
  - *Guideline G1192 (2024)*: "VDES Authentication." Outlines public-key cryptographic mechanisms to authenticate legacy AIS transmissions via VDES data links.
  - *Guideline G1193 (2024)*: "VDES Signal Measurement." Standardizes test metrics and reporting procedures for VDES field trials.
  - *Recommendation R1007*: "VDES Shore Infrastructure."

---

## Pitfalls

1. **Believing "AIS 2.0" will replace legacy AIS transponders** → Commercial marketing implies an imminent protocol obsolescence → In reality, ITU-R M.2092 embeds M.1371 legacy AIS completely intact; standard Class A and Class B units remain fully compliant, visible, and functional.
2. **Assuming VDES carriage is legally mandatory from 2028** → Reading vendor press stating VDES "enters SOLAS in 2028" as a compulsory mandate → IMO Resolution MSC.583(111) permits VDES as a *voluntary alternative* to AIS; ships are never required to scrap functioning AIS units.
3. **Calculating user data rates directly from raw 307.2 kbit/s figures** → Neglecting forward error correction, TDMA framing, and adaptive fallback → Real-world net IP throughput on a 100 kHz VDE-TER link operating under fading conditions is typically 76.8 to 230.4 kbit/s, shared among all vessels in the cell.
4. **Expecting satellites to re-transmit AIS downlinks to ship displays** → Assuming satellite VDE-SAT broadcasts global shipping traffic to bridge ECDIS screens → Satellites receive terrestrial AIS uplinks (SAT-AIS), but operational downlinks on AIS 1/2 are strictly prohibited by physics and regulation to prevent destroying coastal TDMA slot maps.
5. **Ignoring Message 22 timeout fallbacks in custom receiver firmware** → Hardcoding regional frequency assignments into receiver channel registers without expiration logic → Transponders become permanently locked onto regional simplex frequencies, suffering total blindness when navigating outside the geographic zone.
6. **Deploying high-gain broadband antennas without testing port isolation** → Assuming any VHF antenna covering 156–162 MHz will support multi-channel VDES transceivers → High-power voice VHF transmissions on Channel 16 induce severe intermodulation and blocking across adjacent VDES receiver frontends without minimum 25 dB port isolation.
7. **Attempting 16-QAM decoding with low-cost 8-bit SDR dongles** → Assuming low-cost hardware can demodulate linear VDES signals → 16-QAM requires at least 12-bit ADC dynamic range and $<6\%$ EVM; cheap SDRs exhibit excessive phase noise and saturation under nearby maritime transmitters.
8. **Transmitting non-safety telemetry on AIS 1 and 2 in VDES-equipped ports** → Legacy habit of broadcasting large binary sensor strings on primary collision channels → Violates regional e-navigation rules; high-volume data payloads must be directed to channels 2027/2028 (ASM) or VDE-TER.
9. **Confusing AMRD Group A and Group B frequency allocations** → Configuring fishing net buoys to transmit on AIS 1 or AIS 2 → Illegal under international regulations; ITU-R M.2135-1 requires all Group B non-safety devices to broadcast exclusively on Channel 2006 (160.900 MHz).
10. **Treating VDE-SAT as a high-speed continuous internet connection** → Assuming VDES provides web browsing at sea like Starlink or Inmarsat Fleet Xpress → VDE-SAT is an optimized, low-bandwidth, message-oriented transport intended for electronic charts, weather layers, and telemetry.

---

## Key takeaways

- **"AIS 2.0" is a commercial branding phrase; VDES is the international standard.** Governing maritime bodies recognize only the VHF Data Exchange System (ITU-R M.2092-2).
- **Legacy AIS is retained without alteration.** AIS 1 (161.975 MHz) and AIS 2 (162.025 MHz) remain dedicated to 9,600 bit/s GMSK navigation safety and collision avoidance.
- **VDES comprises four distinct pillars:** Legacy AIS, Application-Specific Messages (ASM on channels 2027/2028), Terrestrial Data Exchange (VDE-TER), and Satellite Data Exchange (VDE-SAT).
- **The "32×" throughput multiple is a peak burst figure.** Derived by aggregating four 25 kHz channels into a 100 kHz block with 16-QAM ($307.2\text{ kbit/s} \div 9.6\text{ kbit/s}$), net shared capacity after FEC coding drops to 76.8–230.4 kbit/s.
- **SOLAS adoption is permissive, not mandatory.** Resolutions MSC.583(111) and MSC.592(111) permit voluntary carriage of VDES as an alternative to AIS starting 1 January 2028; legacy transponders remain fully legal indefinitely.
- **VDE-SAT downlinks operate only on dedicated frequencies.** Satellites broadcast downlinks strictly on channels 2026 and 2086 with strict power-flux density limits; they never broadcast AIS downlinks on AIS 1 or 2.
- **Multiple auxiliary channels support the ecosystem.** Long-range AIS uses channels 75 and 76 for satellite tracking; AMRD Group B fishing buoys are segregated to Channel 2006 (160.900 MHz); DSC channel 70 management has been superseded by Message 22.
- **Design for coexistence.** Maritime systems must support multi-channel SDR architectures monitoring AIS, ASM, and VDES streams while ensuring fail-safe fallback to legacy safety broadcasts.

---

## References

- European Electronic Communications Committee (2024). *The European Table of Frequency Allocations and Applications in the Frequency Range 8.3 kHz to 3000 GHz (ECA Table)* (ERC Report 25). Copenhagen: CEPT/ECC.
- GateHouse SatCom (2023). *Autonomous Maritime Data Exchange: The MARIOT Architecture and VDES Space Validation*. Aalborg: GateHouse White Paper Series.
- International Association of Marine Aids to Navigation and Lighthouse Authorities (2021). *VHF Data Exchange System (VDES) Overview* (Guideline G1117, Ed. 2.0). Saint-Germain-en-Laye: IALA.
- International Association of Marine Aids to Navigation and Lighthouse Authorities (2024). *VDES Authentication* (Guideline G1192, Ed. 1.0). Saint-Germain-en-Laye: IALA.
- International Association of Marine Aids to Navigation and Lighthouse Authorities (2024). *VDES Signal Measurement* (Guideline G1193, Ed. 1.0). Saint-Germain-en-Laye: IALA.
- International Electrotechnical Commission (2024). *Maritime navigation and radiocommunication equipment and systems — Digital interfaces — Part 450: Multiple talkers and multiple listeners — Ethernet interconnection* (IEC Standard 61162-450:2024, Ed. 3.0). Geneva: IEC.
- International Electrotechnical Commission (2026). *Maritime navigation and radiocommunication equipment and systems — VHF Data Exchange System (VDES) — Shipborne mobile station — Operational and performance requirements, methods of test and required test results* (IEC Standard 63514 Ed. 1.0, 3CD stage). Geneva: IEC.
- International Maritime Organization (2026). *Amendments to the International Convention for the Safety of Life at Sea, 1974, as Amended* (Resolution MSC.583(111)). London: IMO.
- International Maritime Organization (2026). *Introduction of the VHF Data Exchange System (VDES) into the IMO Regulatory Framework* (Resolution MSC.592(111)). London: IMO.
- International Maritime Organization (2026). *Performance Standards for Shipborne VHF Data Exchange System (VDES)* (Resolution MSC.593(111)). London: IMO.
- International Maritime Organization (2026). *Guidelines for the Onboard Operational Use of Shipborne VDES* (MSC.1/Circ.1699). London: IMO.
- International Telecommunication Union (2014). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band* (Recommendation ITU-R M.1371-5). Geneva: ITU.
- International Telecommunication Union (2023). *Technical characteristics of autonomous maritime radio devices operating in the frequency band 156–162.05 MHz* (Recommendation ITU-R M.2135-1). Geneva: ITU.
- International Telecommunication Union (2024). *Radio Regulations, Appendix 18 (REV. WRC-19): Table of Transmitting Frequencies in the VHF Maritime Mobile Band*. Geneva: ITU.
- International Telecommunication Union (2026). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band* (Recommendation ITU-R M.1371-6). Geneva: ITU.
- International Telecommunication Union (2026). *Technical characteristics for a VHF data exchange system in the maritime mobile service* (Recommendation ITU-R M.2092-2). Geneva: ITU.
- Kongsberg Seatex (2018). *NorSat-2 VDES Satellite Mission Initial In-Orbit Results and VDE-SAT Observations*. Trondheim: Kongsberg Discovery Technical Report.
- Saab TransponderTech (2024). *R6 Supreme VDES Transponder System: Integration and Operational Specification*. Linköping: Saab Group.
- United States Coast Guard Navigation Center (2010). *Special Notice on AIS Channel Management: Reversion to Default Frequencies Following Message 22 Operations*. Alexandria, VA: USCG NAVCEN.
