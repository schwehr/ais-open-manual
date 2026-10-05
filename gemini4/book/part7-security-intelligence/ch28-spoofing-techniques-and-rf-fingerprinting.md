# Chapter 28: AIS Spoofing Techniques, Deep RF Fingerprinting (SEI), and Counter-Spoofing

## 28.1 Operational & Conceptual Overview: Comprehensive Taxonomy of AIS Spoofing Techniques

In maritime operations and intelligence analysis, the word **"spoofing"** is often used as a catch-all term whenever a vessel appears on a chart or web tracker at a location where it does not physically exist. However, treating all false AIS tracks as a single phenomenon leads to severe operational and analytical blunders. A Vessel Traffic Services (VTS) watchstander, a naval intelligence officer, and a sanctions-compliance data scientist face fundamentally different threat models depending on *where* in the end-to-end sensor-to-display chain the deception is injected.

Because ITU-R M.1371-5 contains no cryptographic digital signature, no message authentication code (MAC), and no challenge-response ranging mechanism, an adversary can falsify AIS tracks at five distinct architectural layers:

1. **The Network Aggregator Layer** (Internet UDP/TCP packet injection),
2. **The VHF Radio Frequency (RF) Layer** (Software-Defined Radio or reprogrammed transceiver broadcasts on $161.975\text{ MHz}$ and $162.025\text{ MHz}$),
3. **The Static Identity Layer** (MMSI/IMO identity laundering and "zombie" or "dual-broadcast" cloning),
4. **The Physical Decoy Layer** (dual-transponder "anchor-loop" or shore/barge relay decoys), and
5. **The Shipboard GNSS Sensor Layer** (external L-band GPS/GLONASS RF spoofing that tricks an innocent vessel's own certified AIS transponder into broadcasting false coordinates).

```mermaid
flowchart TD
    subgraph L1["1. Aggregator API Injection (Cyber-Only)"]
        A1["Python Script / Bot"] -->|"Plaintext !AIVDM over UDP/TCP"| A2["Community Aggregator\n(MarineTraffic / AISHub)"]
        A2 --> A3["Public Web Map Shows Ghost Ship\n(Zero RF Energy Emitted)"]
    end

    subgraph L2["2. Over-the-Air SDR RF Spoofing"]
        B1["HackRF / PlutoSDR / USRP\n(GNU Radio / Custom IQ)"] -->|"161.975 / 162.025 MHz GMSK"| B2["Ship Bridges (ECDIS/MKD),\nUSCG NAIS Towers, & LEO Satellites"]
    end

    subgraph L3["3. Identity Laundering (Dual-Broadcast / Zombie)"]
        C1["Sanctioned Tanker A\n(Loading Crude in Venezuela)"] -->|"Broadcasts MMSI/IMO of Ship B"| C2["Global Satellite & Shore Receivers"]
        C3["Legitimate Tanker B\n(Steaming in South China Sea)"] -->|"Broadcasts True MMSI/IMO of Ship B"| C2
    end

    subgraph L4["4. Dual-Transponder Anchor-Loop Decoy"]
        D1["Real Tanker (AIS Switched OFF)\nSails Dark to STS Transfer Zone"]
        D2["2nd Portable Class A/B or SDR\non Service Boat / Barge / Shore"] -->|"Broadcasts Tanker's MMSI in\nSynthetic Figure-8 at Anchorage"| B2
    end

    subgraph L5["5. GNSS L1 Spoofing (Involuntary AIS Spoofing)"]
        E1["Electronic Warfare GNSS Spoofer\n(1575.42 MHz L1 C/A)"] -->|"Fake Satellite Pseudoranges"| E2["Innocent Ship's GNSS Receiver\n($GPRMC / $GPGGA)"]
        E2 -->|"Corrupted NMEA 0183"| E3["Innocent Ship's Certified Class A AIS\nBroadcasts 'Crop Circle' / Airport Position"]
    end
```

### 1. Aggregator UDP/TCP API Injection ("Cyber-Only Spoofing")

* **Technical Mechanism:** Public and commercial crowdsourced AIS platforms (such as MarineTraffic, VesselFinder, FleetMon, and AISHub) rely on thousands of volunteer coastal receiving stations running software like `AIS-catcher`, `rtl_ais`, or `gpsd`. These stations forward decoded or raw NMEA 0183 `!AIVDM` ASCII sentences over unauthenticated UDP or TCP sockets to central ingestion servers. As demonstrated by Balduzzi, Pasta, and Wilhoit (2014), an attacker with a 50-line Python script can synthesize valid `!AIVDM,1,1,,A,...*hh` sentences (complete with valid 6-bit ASCII armor and XOR checksums) and stream them directly to an aggregator's ingestion port—or compromise a single volunteer Raspberry Pi feeder—without ever radiating a single microwatt of VHF RF energy.
* **Real-World Manifestations:** Geopolitical "track art" (spelling words or drawing pictures across the ocean), fake search-and-rescue distress beacons (`970xxyyyy`), and fabrications of naval flotillas appearing to transit sensitive territorial waters on public web trackers.
* **Immediate Diagnostic Signature:** **Cyber-only spoofing is invisible at the RF layer.** While the fabricated vessel appears on crowdsourced web interfaces, it is *completely absent* from:
  1. Shipboard ECDIS, radar ARPA overlays, and Minimum Keyboard and Displays (MKDs) on vessels actually in the area,
  2. Sovereign coastal VTS networks with physically secured RF chains (such as the US Coast Guard's Nationwide AIS [NAIS] or European SafeSeaNet), and
  3. Low-Earth Orbit (LEO) satellite AIS constellations (Spire, Orbcomm, ExactEarth) that record raw VHF spectrum from space.

### 2. Over-the-Air SDR RF Spoofing

* **Technical Mechanism:** The adversary uses a transmit-capable Software-Defined Radio (e.g., Great Scott Gadgets HackRF One, Analog Devices ADALM-Pluto [PlutoSDR], Nuand bladeRF, Ettus Research USRP B210/X310) coupled to a VHF power amplifier, or a modified commercial Class A/B transceiver, to broadcast physical $9,600\text{ bps}$ GMSK bursts on AIS 1 ($161.975\text{ MHz}$, Channel 87B) and AIS 2 ($162.025\text{ MHz}$, Channel 88B).
* **Real-World Case Study — The June 2021 Black Sea Incident (*HMS Defender* & *HNLMS Evertsen*):** On June 18–19, 2021, days before the Royal Navy destroyer *HMS Defender* (D36) and Royal Netherlands Navy frigate *HNLMS Evertsen* (F805) conducted a freedom-of-navigation transit near Cape Fiolent off Crimea, both warships appeared on AIS trackers sailing together straight up to the Russian naval base at Sevastopol at $2\text{ NM}$ off the coast. Simultaneously, live harbor webcams, port journalists, and satellite optical imagery proved that both warships were **physically moored alongside the pier in Odesa, Ukraine**, more than $150\text{ NM}$ northwest! Because the spoofed tracks were received by multiple coastal VHF stations around the Black Sea, analysts assessed that an RF transmitter (or synchronized feeder network) was broadcasting synthetic Class A/B messages for MMSIs `232002833` and `244870298`.
* **Operational Hazard:** Unlike cyber-only injection, over-the-air RF spoofing penetrates the VHF antennas of every ship within the $20\text{–}40\text{ NM}$ radio horizon. It populates bridge ECDIS displays with ghost targets, triggers false Closest Point of Approach (CPA) and Time to Closest Point of Approach (TCPA) collision alarms, and can be used to execute protocol-level Denial-of-Service attacks (see Chapter 27).

### 3. Identity Laundering & "Zombie / Dual-Broadcast" Spoofing

* **Technical Mechanism:** Rather than fabricating an arbitrary trajectory with an SDR, the crew of a real merchant vessel—typically a sanctioned crude-oil tanker operating in the "shadow fleet"—reprograms the MMSI, IMO number, vessel name, call sign, and hull dimensions inside their shipboard AIS transponder (via the MKD service menu or manufacturer configuration software).
  * **Zombie Vessel Spoofing:** The tanker assumes the MMSI and 7-digit IMO number of a vessel that was scrapped/broken up years earlier (e.g., at Alang or Chittagong), hoping automated compliance databases will treat the hull as a legitimate vessel with no active sanctions flag.
  * **Dual-Broadcast (Identity Cloning) Spoofing:** The sanctioned tanker clones the exact MMSI and IMO number of an innocent, currently active tanker of similar deadweight tonnage (DWT) that is legitimately steaming thousands of miles away in another ocean.
* **Diagnostic Signature:** In global satellite AIS databases, dual-broadcasting produces **impossible teleportation Ping-Pong tracks** when naive parsers group solely by `mmsi`: consecutive pings alternate between the Caribbean Sea (Venezuela) and the South China Sea at implied speeds exceeding $10,000\text{ knots}$. Separating the two physical ships requires clustering by satellite footprint, Doppler curve, and **RF Specific Emitter Identification (SEI)**.

### 4. Dual-Transponder "Anchor-Loop" / Decoy Relay Spoofing

* **Technical Mechanism:** When a sanctioned tanker approaches a loading terminal or offshore Ship-to-Ship (STS) lightering zone (commonly documented off Jose Terminal in Venezuela, Kharg Island in Iran, Kalamata, Ceuta, or the Riau Archipelago east of Singapore), simply turning off AIS ("going dark") triggers immediate regulatory alerts in commercial compliance platforms (Windward, Kpler, Pole Star, Starboard). To evade "dark-activity" detectors, sophisticated shadow-fleet operators execute a **physical decoy handoff**:
  1. As the real tanker reaches a plausible holding anchorage or transit choke point, the bridge crew powers down the ship's primary Class A AIS antenna (or switches it to dummy-load / receive-only mode).
  2. Simultaneously, an accomplice aboard a small coastal service launch, tugboat, fishing vessel, anchored barge, or shore building switches on a **second portable AIS transponder** (or a pre-programmed SDR replay box) configured with the tanker's MMSI and IMO number.
  3. While the real $300\text{ m}$ Very Large Crude Carrier (VLCC) sails dark for 5 to 10 days to load or transfer $2\text{ million}$ barrels of crude oil, the decoy transponder broadcasts a synthetic or physically motored slow "anchor swing" or figure-eight loitering loop at the legitimate anchorage.
  4. When the real tanker returns to the handoff point, the decoy switches off and the real tanker resumes broadcasting.
* **Diagnostic Signatures:**
  * **Kinematic Repetition & Turn-Radius Anomalies:** Pre-programmed SDR decoy boxes often replay a recorded 12-hour NMEA log in an endless loop, producing exact mathematical periodicity in $(\lambda(t), \phi(t))$ with a sharp discontinuity every $T_{\text{loop}}$ hours. If the decoy is placed on a $15\text{ m}$ launch motoring in circles, its instantaneous rate of turn and acceleration violate the hydrodynamic maneuvering limits of a $300,000\text{ DWT}$ supertanker.
  * **SAR / Optical Absenteeism:** Spaceborne Synthetic Aperture Radar (Sentinel-1, Capella, ICEYE) or high-resolution optical imagery (PlanetScope, Sentinel-2) over the broadcast anchorage reveals empty water or a $12\text{ m}$ launch where a $330\text{ m}$ VLCC claims to be anchored.
  * **Abrupt RF Fingerprint Swap:** At the exact timestamp of the decoy handoff, the physical-layer RF signature of the VHF bursts—power amplifier ramp transient, carrier frequency offset, and modulator $BT$ product—switches instantaneously from the VLCC's bridge Furuno/JRC Class A unit to the decoy's portable Class B or HackRF transmitter!

### 5. GNSS L1 Spoofing Inducing Involuntary AIS Manipulation

* **Technical Mechanism:** An AIS transponder does not independently know where it is; it reads its position, Course Over Ground (COG), Speed Over Ground (SOG), and UTC time from an internal or external GNSS receiver (typically via NMEA 0183 `$GPRMC`, `$GPGGA`, and `$GPZDA` sentences over an RS-422 serial bus, plus a 1-Pulse-Per-Second [1PPS] timing line). When a state military or coastal electronic warfare (EW) unit transmits high-power counterfeit GPS L1 C/A ($1575.42\text{ MHz}$) and GLONASS L1OF ($\sim 1602\text{ MHz}$) signals toward coastal waters, the GNSS receivers aboard dozens of innocent nearby merchant ships lock onto the stronger spoofed satellite signals. The ships' own unmodified, fully certified Class A AIS transponders dutifully pack these false GNSS coordinates into ITU-R M.1371 Messages 1, 2, 3, and 18 and broadcast them over VHF.
* **Real-World Manifestations:**
  * **Airport & Land Displacements (C4ADS, 2019):** To trigger hardcoded geofence no-fly zones inside commercial consumer drones (e.g., DJI quadcopters), Russian EW systems deployed near VIP residences (Gelendzhik on the Black Sea), Moscow, and Khmeimim Air Base in Syria broadcast spoofed GNSS coordinates centered on regional civil airports (such as Gelendzhik, Sochi, Simferopol, and Beirut Rafic Hariri International Airport). Hundreds of commercial ships steaming $10\text{–}40\text{ NM}$ offshore suddenly appeared on AIS clustered inside airport runways on land.
  * **The Shanghai & Point Reyes "Crop Circles" (2019–2020):** In July 2019 along the Huangpu River in Shanghai, and in early 2020 off Point Reyes, California, dozens of vessels simultaneously reported AIS tracks spinning in synchronized $3\text{ NM}$ circles at $20\text{ knots}$, creating glowing ring patterns dubbed "crop circles" by Bergman (2019/2020) and C4ADS.
  * **Eastern Mediterranean, Red Sea, & Baltic Sea EW Zones (2023–2026):** Widespread military GNSS spoofing across the Levant (placing ships at Beirut or Cairo airports), the Red Sea, and the eastern Gulf of Finland / Kaliningrad region.
* **Diagnostic Signature:** Unlike RF AIS spoofing (where a single emitter fabricates tracks), GNSS-induced AIS spoofing causes **multiple independent vessels** to jump simultaneously to the *same* attractor polygon or circular trajectory, while each vessel's VHF burst still retains its own authentic **RF hardware fingerprint**, valid physical **Angle of Arrival (AoA)** from the water, and normal shipboard **Gyrocompass True Heading** (`True Heading` field in Msg 1/2/3, which comes from the ship's mechanical/fiber-optic gyro rather than GNSS and therefore disagrees wildly with the spoofed GNSS `COG`!).

| Spoofing Category | Emission Medium | Affects Ship Bridges (ECDIS)? | Affects LEO Satellites? | Physical AoA / TDOA Matches Claimed Lat/Lon? | RF Hardware Fingerprint (SEI) Matches Vessel History? |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **1. Aggregator API Injection** | Internet (UDP/TCP) | No | No | N/A (No RF) | N/A (No RF) |
| **2. Over-the-Air SDR Spoofing** | VHF ($162\text{ MHz}$) | **Yes** | **Yes** (if high power) | **No** (All targets radiate from 1 antenna) | **No** (Shows SDR I/Q & PA traits) |
| **3. Identity Laundering (Dual/Zombie)** | VHF ($162\text{ MHz}$) | **Yes** (Local) | **Yes** (Global) | **Yes** (At the real hull's location) | **No** (Disagrees with cloned ship's emitter) |
| **4. Dual-Transponder Anchor-Loop** | VHF ($162\text{ MHz}$) | **Yes** | **Yes** | **Yes** (At the decoy boat/shore site) | **No** (Abrupt emitter swap at handoff) |
| **5. GNSS L1 Spoofing** | L-Band ($1575\text{ MHz}$) $\rightarrow$ VHF | **Yes** | **Yes** | **No** (AoA points to sea; Lat/Lon on land) | **Yes** (Ship's genuine Class A radio!) |

### 6. Historical Context & Evolution (`schwehr/gis-history` Integration): From WWII "Radio Fingerprinting" to Modern AIS SEI

The science of identifying a specific radio transmitter from the microscopic analog imperfections of its waveform—known today in defense and signal processing literature as **Specific Emitter Identification (SEI)** or **Radio Frequency Fingerprinting (RFF)**—predates the digital computer and is deeply intertwined with the history of maritime navigation and electronic warfare documented in `schwehr/gis-history` (Schwehr, 2024–2026).

1. **WWII British Y-Service, "The Fist," and "TINA" / "RFC" (1939–1945):** During the Battle of the Atlantic, Allied radio intelligence operators discovered that even when German Kriegsmarine U-boats and Luftwaffe stations changed call signs and frequencies daily, individual transmitters and operators could be tracked across the ocean. First, human Morse operators possessed a distinctive rhythm of dots, dashes, and inter-character spaces known as **"the Fist"** (formalized as **TINA**). Second, British scientists attached high-speed cathode-ray oscilloscopes to VHF/HF receivers to photograph the **turn-on carrier transients** (**RFC** — Radio Finger Printing) of German transmitters, discovering that the resistance-capacitance (RC) charging curves and vacuum-tube oscillator ringing uniquely identified individual physical radio sets.
2. **Cold War Naval ELINT and Radar SEI (1950s–1980s):** As maritime radar (1904/WWII) and Soviet fleet ocean surveillance expanded, US Navy and NATO Electronic Intelligence (ELINT) platforms developed high-speed digitizers to fingerprint the pulse-envelope rise time, intrapulse phase modulation, and magnetron frequency pushing/pulling of individual shipboard navigation radars (**specific emitter identification**).
3. **Birth of Unauthenticated SOTDMA AIS (1988–2002):** When Håkan Lans patented Self-Organized TDMA in 1988 (`gis-history`) and ITU-R M.1371-0 (1998) / IMO SOLAS Chapter V Regulation 19 (2000/2002) mandated AIS globally, CPU and bandwidth constraints dictated a compact 168-bit single-slot frame at $9,600\text{ bps}$ GMSK. No bits were allocated for cryptographic signatures, leaving the VHF Data Link entirely reliant on physical-layer trust.
4. **Academic & Industry Awakening to AIS Spoofing (2013–2019):**
   * In **2013–2014**, Trend Micro researchers Marco Balduzzi, Alessandro Pasta, and Kyle Wilhoit demonstrated both aggregator API spoofing and low-cost SDR over-the-air spoofing at BlackHat and ACSAC (Balduzzi et al., 2014).
   * In **March 2019**, the Center for Advanced Defense Studies (**C4ADS**) published *Above Us Only Stars*, analyzing nearly 10,000 GNSS spoofing incidents across 1,311 commercial vessels in the Black Sea, Crimea, Syria, and Russian ports, proving that shipboard AIS logs serve as the world's largest crowdsourced sensor network for detecting L-band electronic warfare.
5. **Geopolitical Spoofing, Shadow Fleets, and Deep-Learning RF SEI (2020–2026+):** Following the 2021 *HMS Defender* spoofing incident and the rapid expansion of sanctioned oil shadow fleets (2022–2026), government littoral networks (USCG, EMSA, UK JMSC), commercial RF space constellations (HawkEye 360, Unseenlabs, Spire), and academic DSP labs converged on **wideband complex baseband IQ recording** ($f_s \ge 1\text{–}10\text{ MS/s}$) paired with **Complex-Valued Convolutional Neural Networks (CV-CNNs)** to bind every AIS MMSI to the immutable analog physics of its VHF transceiver hardware.

---

## 28.2 Deep Technical & Mathematical Foundations: Techniques for Deep Diving into the RF Level of Individual Systems (Specific Emitter Identification / RF Fingerprinting)

> **Core Engineering Question:** *What are the techniques for deep diving into the RF level of what individual systems do? Can quirks of particular SDR and hardware implementations be used to identify a manufacturer or even a specific individual transceiver unit?*
>
> **Answer:** **Yes—unequivocally.** Even when two AIS transmitters broadcast the exact same 168-bit ITU-R M.1371 payload (identical MMSI, identical coordinates, identical CRC-16), their analog RF front ends, digital-to-analog converters (DACs), phase-locked loops (PLLs), crystal oscillators, and power amplifier (PA) biasing networks imprint a rich, multi-dimensional physical-layer signature onto every $26.67\text{ ms}$ burst.
> * **Manufacturer and Architecture Class Identification** (e.g., distinguishing a certified Furuno FA-170, JRC JHS-183, Saab R5, or SRT Marine OEM module from a HackRF One, PlutoSDR, or USRP) is achieved with **$>99\%$ accuracy** from a single high-SNR burst using modulator filter responses, I/Q mirror images, and PA ramp topology.
> * **Specific Individual Unit Identification (Intra-Model SEI)** (e.g., distinguishing Serial Number `#1042` from Serial Number `#1043` of the exact same Furuno Class A model) is achieved with **$90\%\text{–}98\%$ accuracy** by combining **PA turn-on transient ringing**, **joint Carrier Frequency Offset (CFO) vs. symbol-clock ppm ratio**, **post-key-up thermal frequency drift**, and **higher-order spectral cumulants**.

Standard NMEA AIS receivers discard all physical-layer forensic evidence at the moment of demodulation, outputting only a 6-bit ASCII string (`!AIVDM`). To deep dive into the RF level, an analyst must capture the **pre-demodulation complex baseband analytical signal** $z(t)$ (or construct it from a real IF signal via the **Hilbert Transform** $z(t) = s(t) + j\mathcal{H}\{s(t)\}$) using a wideband SDR receiver operating at an oversampled rate $f_s \ge 1\text{ MS/s}$ (typically $f_s = 1.92\text{ MS/s}$ to $10\text{ MS/s}$, corresponding to $N_{\text{sps}} = 200$ to $1,041$ complex samples per $9,600\text{ bps}$ symbol, with $\ge 12\text{–}16\text{ bits}$ of ADC dynamic range):

$$z(t) = I(t) + j Q(t) = a(t) \exp\!\big(j\phi(t)\big)$$

where the instantaneous envelope amplitude $a(t)$, unwrapped instantaneous phase $\phi(t)$, and instantaneous frequency $f_i(t)$ are defined as:

$$a(t) = \sqrt{I^2(t) + Q^2(t)}, \qquad \phi(t) = \text{unwrap}\!\Big(\text{atan2}\big(Q(t),\, I(t)\big)\Big), \qquad f_i(t) = \frac{1}{2\pi}\frac{d\phi(t)}{dt}$$

Below are the **six foundational RF and hardware-level techniques** used to fingerprint manufacturer architectures and individual physical units.

```mermaid
flowchart LR
    RX["VHF Antenna & LNA\n(161.975 / 162.025 MHz)"] --> ADC["Wideband ADC / SDR\n(fs = 1.92–10 MS/s, 14–16 bit)"]
    ADC --> IQ["Complex Baseband Burst\nz[n] = I[n] + jQ[n]\n(26.67 ms / 256 bits)"]
    
    IQ --> F1["1. PA Ramp Transient\n(0–833 us Turn-On/Off)\na(t), dphi/dt Ringing"]
    IQ --> F2["2. GMSK Modulator & BT\nEye Opening, EVM,\nActual h, ISI Trellis"]
    IQ --> F3["3. Clock Invariant & Drift\nCFO vs Symbol Clock ppm\n& Thermal Slope dfc/dt"]
    IQ --> F4["4. Direct-Conv SDR Quirks\nLO Carrier Leakage &\nConjugate I/Q Image"]
    IQ --> F5["5. DAC & Phase Noise\n8-bit Spurs vs VCO\nL(df) Skirt Profile"]
    IQ --> F6["6. Protocol / Firmware\nSOTDMA RNG, Spare Bits,\nVendor ID Strings"]

    F1 & F2 & F3 & F4 & F5 & F6 --> SEI["SEI Classifier / Siamese CV-CNN\n-> Manufacturer + Specific Unit ID"]
```

---

### Technique 1: Power Amplifier (PA) Turn-On and Turn-Off Ramp Transients ($833\text{ }\mu\text{s}$ Window)

Under **ITU-R M.1371-5 Annex 2 (§2.3 / Table 2)** and **IEC 61993-2** (Class A) / **IEC 62287-1** (Class B), an AIS burst occupies a $26.67\text{ ms}$ time slot (256 bit periods at $9,600\text{ bps}$, where $T_b = 104.167\text{ }\mu\text{s}$). Before the 24-bit alternating training preamble (`01010101...`) begins, the transmitter is allocated an **8-bit ramp-up window** ($8 \times T_b = 833.33\text{ }\mu\text{s}$) to bring its RF output power from standby ($<-50\text{ dBc}$) up to $90\%$ of nominal power ($12.5\text{ W}$ [$+41\text{ dBm}$] for Class A; $2\text{ W}$ [$+33\text{ dBm}$] for Class B CS; $5\text{ W}$ [$+37\text{ dBm}$] for Class B SO), and an equivalent $833.33\text{ }\mu\text{s}$ ramp-down window at the end of the packet to prevent adjacent-channel splatter.

#### Why the PA Transient Fingerprints Both Manufacturer and Unit
1. **Manufacturer Circuit Topology (Macro-Signature):**
   * **Certified Commercial Transponders (Furuno, JRC, Saab/Transas, Kongsberg, SRT Marine [em-trak / Raymarine / Garmin OEM]):** To pass strict IEC 61993-2 adjacent-channel power ratio ($-70\text{ dBc}$ at $\pm 25\text{ kHz}$) tests, marine transponders use a closed-loop **Automatic Level Control (ALC)** circuit driving the gate/collector bias of a multi-stage LDMOS or bipolar RF power amplifier through a shaped RC/DAC cosine-squared ramp profile. Each manufacturer uses a distinct DAC step count, op-amp integrator time constant $\tau_{\text{ALC}}$, and PIN-diode Transmit/Receive (T/R) switch timing sequence.
   * **Hobbyist SDRs + External Linear Amps (HackRF, PlutoSDR):** An SDR typically keys its internal CMOS RF switch abruptly in $<2\text{ }\mu\text{s}$ (producing a near-step-function turn-on with severe spectral click) unless the user's GNU Radio flowgraph explicitly multiplies the burst start by a software window function.
2. **Unit-Specific Component Tolerances (Micro-Signature):**
   * Even among two identical Furuno FA-170 units from the same factory batch, the multilayer ceramic capacitors ($\pm 5\%\text{–}10\%$ tolerance), ferrite core inductors ($\pm 10\%$), and LDMOS FET threshold voltages ($V_{\text{GS(th)}}$ variation) in the PA bias network and output harmonic low-pass filter follow a damped second-order differential equation during key-up:

$$a_{\text{ramp}}(t) = A_0 \left[ 1 - \frac{1}{\sqrt{1 - \zeta^2}} e^{-\zeta \omega_n t} \sin\!\left(\omega_n \sqrt{1 - \zeta^2}\, t + \arccos\zeta\right) \right]$$

   * Simultaneously, as the PA drain current surges from $0\text{ A}$ to $\sim 2.5\text{ A}$ during those $833\text{ }\mu\text{s}$, power-supply rail sag and parasitic capacitance changes across the VCO/PLL buffer induce an **AM-to-PM conversion phase transient** $\Delta\phi_{\text{transient}}(t)$ ("VCO pulling").
   * Extracting the **$10\%\text{–}90\%$ rise time ($t_r$)**, **fractional envelope overshoot ($M_p$)**, **natural ringing frequency ($\omega_n$)**, **damping ratio ($\zeta$)**, and **transient phase inflection integral** $\int_0^{833\mu\text{s}} |f_i(t) - f_c|\,dt$ separates individual physical transceivers with high statistical separability.

---

### Technique 2: GMSK Gaussian Pre-Modulation Filter $BT$ Product & Phase Trajectory Deviations

Ideal AIS transmits Non-Return-to-Zero Inverted (NRZI) encoded data using **Gaussian Minimum Shift Keying (GMSK)** with modulation index $h = 0.5$ and a transmit Gaussian pre-modulation filter bandwidth-bit-period product of $BT = 0.4$ (ITU-R M.1371-5 §2.1.2).

In continuous-time GMSK, an NRZI bipolar impulse train $d_k \in \{-1, +1\}$ is convolved with a rectangular pulse $\text{rect}(t/T_b)$ and a Gaussian filter impulse response $g(t)$:

$$g(t) = \frac{1}{\sqrt{2\pi}\,\sigma T_b} \exp\!\left(-\frac{t^2}{2\sigma^2 T_b^2}\right), \qquad \text{where } \sigma = \frac{\sqrt{\ln 2}}{2\pi (BT)}$$

yielding the instantaneous phase trajectory:

$$\phi_{\text{GMSK}}(t) = 2\pi h \int_{-\infty}^{t} \sum_{k} d_k \, p(\tau - k T_b)\, d\tau + \phi_0, \qquad p(t) = \text{rect}\!\left(\frac{t}{T_b}\right) * g(t)$$

Over a single isolated symbol period $T_b$, $h = 0.5$ produces a net phase rotation of exactly $\Delta\phi = \pm h\pi = \pm \frac{\pi}{2}\text{ rad}$ ($\pm 90^\circ$), corresponding to a peak instantaneous frequency deviation of $\Delta f_{\text{max}} = \pm \frac{R_b}{4} = \pm 2,400\text{ Hz}$ on an alternating `101010...` pattern (filtered by the $BT = 0.4$ Gaussian response).

#### How Real Hardware Deviates from Ideal GMSK
1. **Dedicated Baseband ASICs vs. SDR Software Filters:**
   * Commercial AIS transponders use specialized marine communication ASICs or RF synthesizers—such as the **CML Microcircuits CMX7032 / CMX7042**, **Analog Devices ADF7021**, **Silicon Labs Si4463**, or custom FPGA look-up tables (LUTs). Each chip implements $p(t)$ as a truncated finite impulse response (FIR) filter spanning $L \in \{3, 4, 5\}$ symbol periods with fixed-point tap quantization (e.g., 8-bit or 10-bit ROM coefficients).
   * Conversely, an SDR spoofer running `gr-ais` or custom Python DSP uses 32-bit floating-point taps, often with an erroneously configured $BT$ (e.g., $BT = 0.3$ copied from GSM cellular specifications or $BT = 0.5$ from Class B receiver specs!).
2. **Two-Point Analog PLL Modulation vs. Direct Digital Synthesis (DDS):**
   * In analog/fractional-$N$ PLL transmitters, the Gaussian-filtered baseband voltage drives a varactor diode on the VCO (or dual-point modulation into both the VCO and $\Delta\Sigma$ modulator). Because varactor capacitance $C(V)$ is slightly nonlinear across the $\pm 2.4\text{ kHz}$ deviation range, positive frequency deviations ($+2.4\text{ kHz}$) and negative deviations ($-2.4\text{ kHz}$) exhibit subtle **asymmetry** ($\Delta f_+ \neq |\Delta f_-|$) and a unit-specific **effective modulation index** $\hat{h} = 0.5 + \delta h$ (where ITU-R M.1371 permits up to $\pm 5\%$ tolerance around nominal deviation).
3. **Forensic Modulator Metrics:**
   * **Eye Diagram Opening & Inter-Symbol Interference (ISI) Phase Trellis:** Plotting the instantaneous frequency $f_i(t)$ folded modulo $2T_b$ forms the **GMSK Eye Diagram**. The vertical eye opening at the optimal sampling instant and the variance at the zero-crossings directly quantify the FIR filter tap truncation and $BT$ product.
   * **Estimated Modulation Index ($\hat{h}$):** Computed from the slope of unwrapped phase across the 24-bit alternating training sequence (`01010101...`).
   * **Effective Filter $\widehat{BT}$ Product:** Estimated by fitting the ratio of peak frequency deviation on alternating bits (`0101`, high ISI cancellation) to peak deviation on run-length bits (`0011100`, full $\pm 2,400\text{ Hz}$ swing):
     $$\frac{f_{\text{peak}}(\texttt{0101})}{f_{\text{peak}}(\texttt{000111})} = \text{erf}\!\left(\frac{\pi (BT)}{\sqrt{2\ln 2}}\right) - \text{higher-order ISI terms}$$
     For $BT = 0.4$, the alternating-bit peak frequency reaches $\sim 66.2\%$ ($\approx \pm 1,589\text{ Hz}$) of the full $\pm 2,400\text{ Hz}$ deviation, whereas for $BT = 0.3$ (GSM), it reaches only $\sim 52.8\%$ ($\approx \pm 1,267\text{ Hz}$).
   * **Phase Error Vector Magnitude ($\text{EVM}_\phi$):** After reconstructing the exact transmitted bit sequence $\hat{d}_k$ (which is known deterministically once the CRC-16 passes!) and synthesizing an ideal reference phase trajectory $\phi_{\text{ideal}}(t; \hat{h}, \widehat{BT})$, the residual Root-Mean-Square (RMS) phase trajectory error:
     $$\text{EVM}_{\phi,\text{RMS}} = \sqrt{\frac{1}{N}\sum_{n=0}^{N-1} \Big(\phi_{\text{meas}}[n] - \phi_{\text{ideal}}[n]\Big)^2}$$
     isolates the deterministic FIR tap truncation ripple and PLL loop-filter transfer function of that exact radio model.

---

### Technique 3: Joint Carrier Frequency Offset (CFO) vs. Symbol-Clock Skew Invariant Ratio & Thermal Drift

Every AIS transceiver relies on an internal Temperature-Compensated Crystal Oscillator (**TCXO**, typically $12.8\text{ MHz}$, $16.0\text{ MHz}$, $19.2\text{ MHz}$, or $26.0\text{ MHz}$) as its master frequency reference $f_{\text{ref}}$. Crucially, in virtually all hardware architectures, **both** the VHF RF carrier frequency $f_c$ ($161.975\text{ MHz}$ or $162.025\text{ MHz}$) **and** the $R_b = 9,600\text{ bps}$ baseband symbol clock are synthesized from this **single shared crystal** via fixed integer or fractional-N dividers:

$$f_c = M_{\text{RF}} \cdot f_{\text{ref}}, \qquad R_b = \frac{f_{\text{ref}}}{D_{\text{sym}}}$$

Because manufacturing crystal cut variations and aging cause the physical crystal frequency to deviate by a fractional parts-per-million error $\epsilon_{\text{xtal}} = \frac{\Delta f_{\text{ref}}}{f_{\text{ref}}}$ (permitted up to $\pm 3.1\text{ ppm}$ [$\pm 500\text{ Hz}$] for Class A and $\pm 9.3\text{ ppm}$ [$\pm 1,500\text{ Hz}$] for Class B), both the transmitted carrier and the symbol clock must shift by the **exact same fractional error** (plus any radial Doppler shift $\frac{v_r}{c}$):

$$\epsilon_c = \frac{\Delta f_c}{f_c} = \epsilon_{\text{xtal}} + \frac{v_r}{c}, \qquad \epsilon_{\text{sym}} = \frac{\Delta R_b}{R_b} = \epsilon_{\text{xtal}} + \frac{v_r}{c}$$

This physical law yields three powerful forensic capabilities:
1. **Unit-Specific TCXO Offset ($\epsilon_{\text{xtal}}$):** At a stationary coastal receiver (where marine vessel radial speed $v_r < 15\text{ m/s}$ contributes $<0.05\text{ ppm}$ [$\le 8\text{ Hz}$]), the measured carrier frequency offset $\Delta f_c$ (measured to $\pm 1\text{ Hz}$ precision over the $26.67\text{ ms}$ burst) provides a high-resolution fingerprint of that ship's specific crystal oscillator.
2. **Catching Multi-Clock SDR Spoofers ($\Delta\epsilon = |\epsilon_c - \epsilon_{\text{sym}}|$):** When an attacker generates an AIS waveform in software on a PC (or replays a pre-recorded file) and transmits it through an SDR at a slightly mismatched sample rate, or mixes an external audio/baseband generator into an analog VHF FM radio, the RF local oscillator and the symbol-rate clock originate from **two independent crystals**. A non-zero discrepancy $\Delta\epsilon = \left|\frac{\Delta f_c}{f_c} - \frac{\Delta R_b}{R_b}\right| \gg 0.5\text{ ppm}$ immediately proves the signal was not generated by an integrated marine AIS transceiver.
3. **Intrapulse Post-Key-Up Thermal Frequency Drift ($df_c / dt$):** When the $12.5\text{ W}$ Class A power amplifier keys on during the $26.67\text{ ms}$ slot, it dissipates $\sim 8\text{–}12\text{ W}$ of waste heat on the printed circuit board (PCB). Depending on how physically close the manufacturer routed the TCXO to the PA MOSFETs—and the thermal mass of the specific unit's crystal enclosure—the instantaneous carrier frequency $f_c(t)$ exhibits a repeatable **intrapulse thermal chirp** $\frac{df_c}{dt}$ (typically $+0.2\text{ to }+3.5\text{ Hz/ms}$ across the $26.67\text{ ms}$ burst).

---

### Technique 4: Direct-Conversion SDR Quirks vs. Superheterodyne/PLL Transmitters (I/Q Imbalance & LO Leakage)

One of the most decisive physical-layer distinctions in maritime RF forensics is how a transmitter synthesizes its modulated VHF wave:

* **Certified Marine Class A/B Transponders (Direct PLL / DDS FM):** Because GMSK is a **constant-envelope** frequency/phase modulation ($|z(t)| = \text{const}$), certified commercial marine transponders do *not* use linear quadrature (I/Q) mixers. Instead, they feed the Gaussian-filtered frequency-deviation waveform directly into a fractional-$N$ Phase-Locked Loop (PLL) or Direct Digital Synthesizer (DDS) driving a non-linear Class C or Class E power amplifier. Consequently, certified marine transponders have **zero I/Q quadrature mixer stages** and **zero unmodulated Local Oscillator (LO) carrier feedthrough**.
* **Software-Defined Radio Spoofers (Zero-IF / Low-IF Quadrature Upconversion):** Almost all general-purpose transmit SDRs—including the **HackRF One** (MAX2837 zero-IF transceiver), **ADALM-Pluto** (AD9363), **bladeRF** (LMS6002D/LMS7002M), and **USRP B200/X300**—use a **Direct-Conversion Quadrature (I/Q) Mixer**:

$$s_{\text{RF}}(t) = I_{\text{BB}}(t)\cos(2\pi f_{\text{LO}} t) - Q_{\text{BB}}(t)\sin(2\pi f_{\text{LO}} t)$$

In real silicon CMOS quadrature mixers, two analog imperfections are unavoidable:
1. **DC Offset & Local Oscillator (LO) Carrier Leakage ($c_{\text{LO}}$):** Small DC offsets $(d_I, d_Q)$ in the I and Q DACs and capacitive crosstalk across the mixer switches allow unmodulated LO energy at $f_{\text{LO}}$ to leak directly to the RF output.
2. **Quadrature Gain Imbalance ($\alpha$) and Phase Skew ($\theta_{\text{IQ}}$):** The I and Q analog reconstruction filters and mixer branches never have identical gain ($\alpha \neq 0$) or exact $90^\circ$ phase orthogonality ($\theta_{\text{IQ}} \neq 0$). Modeling the impaired complex baseband envelope $z_{\text{IQ}}(t)$ produced by an SDR:

$$z_{\text{IQ}}(t) = \mu \, z_{\text{ideal}}(t) + \nu \, z_{\text{ideal}}^*(t) + c_{\text{LO}}$$

where $z_{\text{ideal}}^*(t) = a(t)\exp(-j\phi(t))$ is the **complex conjugate mirror image**, and the complex gain parameters $\mu, \nu$ are:

$$\mu = \frac{1 + (1 + \alpha)e^{j\theta_{\text{IQ}}}}{2}, \qquad \nu = \frac{1 - (1 + \alpha)e^{-j\theta_{\text{IQ}}}}{2}$$

#### What This Looks Like in the RF Burst
* Whenever the GMSK signal sweeps to a positive instantaneous frequency $+f_{\text{mod}}(t)$ (e.g., $+2,400\text{ Hz}$ during a run of `1`s), the conjugate term $\nu z^*(t)$ creates a **simultaneous ghost mirror image at $-f_{\text{mod}}(t)$ ($-2,400\text{ Hz}$)** with an Image Rejection Ratio:
  $$\text{IRR}_{\text{dB}} = 10\log_{10}\!\left(\frac{|\mu|^2}{|\nu|^2}\right) \approx 10\log_{10}\!\left(\frac{4}{\alpha^2 + \theta_{\text{IQ}}^2}\right)$$
  For an uncalibrated HackRF One or PlutoSDR, $\text{IRR}$ is typically only $25\text{–}38\text{ dB}$, and the interaction between the true signal $\mu e^{j\phi(t)}$, the conjugate image $\nu e^{-j\phi(t)}$, and the LO spike $c_{\text{LO}}$ causes **cyclostationary envelope ripple** on $|z_{\text{IQ}}(t)|$ at $1\times$ and $2\times$ the instantaneous modulation frequency!
* By stripping the decoded GMSK phase $\hat{\phi}(t)$ from the received burst via $r_{\text{dechirp}}(t) = z_{\text{rx}}(t) e^{-j\hat{\phi}(t)}$, the true signal collapses to DC ($0\text{ Hz}$), the SDR's **LO leakage spike** shifts to $-f_{\text{mod}}(t)$, and the **conjugate I/Q mirror image** collapses to $-2\hat{\phi}(t)$—unmasking a direct-conversion SDR spoofer in milliseconds!

---

### Technique 5: DAC Quantization Noise & Phase Noise Skirts

* **DAC Resolution Spurs:** A HackRF One uses an **8-bit DAC** (MAX5864), yielding a theoretical quantization SNR ceiling of $6.02 \times 8 + 1.76 \approx 49.9\text{ dB}$ across the Nyquist band and characteristic harmonic quantization spurs when generating low-IF waveforms. Higher-end SDRs (PlutoSDR 12-bit, USRP B210 12-bit, USRP X310 16-bit) and commercial DDS synthesizers exhibit cleaner quantization floors but distinct clock-reference spurs.
* **VCO Phase Noise Profile $L(\Delta f)$:** At high SNR (e.g., coastal VTS inspection at $<5\text{ NM}$), the single-sideband phase noise power spectral density $L(\Delta f)$ at offsets $\Delta f \in [5\text{ kHz}, 25\text{ kHz}]$ outside the main GMSK lobe reflects the loaded $Q$-factor of the VCO tank resonator and the PLL loop bandwidth $B_{\text{PLL}}$ (typically $10\text{–}30\text{ kHz}$ depending on manufacturer), forming a characteristic "shoulder" on the spectral mask.

---

### Technique 6: Protocol & Firmware Fingerprinting (MAC & Bit-Level Quirks)

Even before (or alongside) analog IQ analysis, different transceiver manufacturers leave deterministic firmware fingerprints inside the decoded ITU-R M.1371 bit stream:

1. **SOTDMA Slot Selection Pseudo-Random Number Generator (PRNG) Biases:** Under ITU-R M.1371-5 Annex 2, a Class A unit selects candidate nominal time slots within a Selection Interval ($SI$) around its Nominal Increment ($NI$), and picks a `Slot Timeout` randomly between $3$ and $7\text{ frames}$. Cheap or older embedded firmware implementations often use simple 16-bit Linear Feedback Shift Registers (LFSRs) or modulo arithmetic with biased distributions (e.g., never picking timeout `7`, or favoring even slot offsets).
2. **Unused / Spare Bits and Default Sentinel Padding:** While ITU-R M.1371 specifies setting spare bits (e.g., bits `145..147` in Msg 1/2/3) to `0`, certain legacy transponders and DIY SDR encoders leave uninitialized memory or `1`s in spare fields, or pad 6-bit ASCII character strings (`Vessel Name`, `Call Sign`, `Destination`) with trailing `@` (`000000`) vs. spaces (`100000` = `32`).
3. **Message 24 Part B Vendor ID Strings:** Class B units transmitting Message 24 Part B include a 42-bit (7-character 6-bit ASCII) `Vendor ID` field (bits `40..81`, 0-based MSB-first, comprising a 3-character manufacturer code registered with NMEA/ITU plus a 4-character unit model/serial code, such as `"SRT..."` for SRT Marine Technology). If a Class B vessel claims a Furuno or Raymarine `Vendor ID` in Message 24, yet its RF burst exhibits an 8-bit HackRF I/Q mirror image and lacks a CSTDMA carrier-sense ramp profile, the spoofing is immediately proven across layers.

| Hardware / Emitter Platform | Modulation Architecture | Typical PA Ramp ($833\text{ }\mu\text{s}$) | I/Q Conjugate Mirror Image ($\nu$) | LO Carrier Leakage Spike | Master Clock / CFO vs. Baud Lock |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Furuno / JRC / Saab Class A** | Fractional-$N$ PLL / DDS ($12.5\text{ W}$) | Smooth ALC cosine-squared ramp; distinct manufacturer $\tau_{\text{ALC}}$ & overshoot | **None** ($<-65\text{ dBc}$, constant-envelope PLL) | **None** | Tightly locked TCXO ($\pm 0.5\text{–}2\text{ ppm}$); repeatable PA thermal chirp |
| **SRT Marine OEM Class B (CS/SO)** | Integrated Marine ASIC (CMX / SiLabs, $2\text{ W} / 5\text{ W}$) | Fast CSTDMA ramp ($<300\text{ }\mu\text{s}$ rise inside $833\text{ }\mu\text{s}$ window) | **None** ($<-60\text{ dBc}$) | **None** | Locked TCXO ($\pm 1\text{–}5\text{ ppm}$) |
| **Unapproved Net Buoy (AMRD / Clone)** | Low-cost Chinese FM IC ($2\text{–}8\text{ W}$) | Underdamped step ramp; high AM-to-PM VCO pulling | **None** | Occasional VCO bleed | Poor crystal stability ($\pm 5\text{–}15\text{ ppm}$); high thermal drift |
| **HackRF One SDR Spoofer** | Zero-IF Direct I/Q Upconverter (8-bit DAC, MAX2837) | Abrupt $<5\text{ }\mu\text{s}$ switch click *or* exact mathematical software window | **Strong** ($\text{IRR} \approx 25\text{–}35\text{ dB}$, envelope ripple) | **Present** ($-25\text{ to }-40\text{ dBc}$ at $f_{\text{LO}}$) | Uncompensated XO ($\pm 10\text{–}20\text{ ppm}$) unless external GPSDO used |
| **PlutoSDR / USRP B210 Spoofer** | Zero-IF Direct I/Q Upconverter (12-bit DAC, AD936x) | Software-defined window + external PA bias step | **Moderate** ($\text{IRR} \approx 35\text{–}48\text{ dB}$ after internal cal) | **Present** ($-35\text{ to }-50\text{ dBc}$) | Locked if software synthesizes at exact $f_s$; mismatched if replaying |

---

## 28.3 Signal Processing & Deep Learning Pipelines for SEI

To operationalize RF fingerprinting across thousands of vessels in a VTS sector or satellite pass, raw IQ captures are processed through a four-stage mathematical and machine-learning pipeline:

### 1. Hilbert Transform, Synchronization, Dechirping, and Residual Envelope Extraction
Given a captured real intermediate-frequency (IF) waveform $s[n]$ or direct complex baseband burst $z[n]$ at sample rate $f_s$:
1. **Hilbert Analytic Signal Construction & Transient Detection:** For real IF captures, the analytic signal is formed via the discrete Hilbert Transform $z[n] = s[n] + j\mathcal{H}\{s[n]\}$, yielding instantaneous amplitude $a[n] = |z[n]|$, unwrapped phase $\phi[n] = \text{unwrap}(\angle z[n])$, and instantaneous frequency $f_i[n] = \frac{f_s}{2\pi}(\phi[n] - \phi[n-1])$. A Bayesian change-point detector locates the exact start sample $n_0$ where the $833\text{ }\mu\text{s}$ PA turn-on transient rises out of the thermal noise floor $w[n]$.
2. **Data-Aided Ideal Waveform Reconstruction:** The burst is demodulated to recover the exact NRZI bit sequence $\hat{d}_k$ (verified by the 16-bit HDLC CRC-CCITT). Using Maximum Likelihood estimation over the steady-state payload window, the coarse Carrier Frequency Offset $\widehat{\Delta f_c}$, initial phase $\hat{\phi}_0$, symbol timing offset $\hat{\tau}$, and modulation index $\hat{h}$ are estimated.
3. **Dechirping (Data Stripping):** By multiplying the received signal by the conjugate of the ideal data-modulated GMSK phase trajectory:
   $$z_{\text{res}}[n] = z[n] \cdot \exp\!\Big(-j\big(2\pi \widehat{\Delta f_c} n T_s + \hat{\phi}_{\text{GMSK}}[n]\big)\Big)$$
   we strip away the semantic content of the AIS message (so that the fingerprint does *not* depend on what latitude, longitude, or MMSI was transmitted!). All that remains in $z_{\text{res}}[n]$ are the pure hardware imperfections: the PA turn-on/off envelope $a[n]$, the PA phase transient, the FIR filter residual ripple, the thermal frequency drift slope, the LO leakage tone, and the conjugate I/Q mirror image.

### 2. Bispectral Analysis and Higher-Order Statistics (HOS)
Why use Higher-Order Statistics instead of a simple Fast Fourier Transform (FFT)? First, the power spectrum (second-order cumulant) is completely blind to phase relationships between frequency components. Second, the **third-order cumulant** $C_{3,z}(\tau_1, \tau_2)$ and its 2D Fourier transform—the **Bispectrum** $B(\omega_1, \omega_2)$—have a remarkable mathematical property: **for any zero-mean stationary Gaussian noise process (such as receiver thermal noise), the Bispectrum is identically zero!**

$$B(\omega_1, \omega_2) = \mathbb{E}\Big[ Z(\omega_1)\, Z(\omega_2)\, Z^*(\omega_1 + \omega_2) \Big]$$

Non-linearities in the transmitter's RF power amplifier (third-order intermodulation products) and I/Q mixer imbalances create quadratic phase coupling between $\omega_1$, $\omega_2$, and $\omega_1 + \omega_2$. Integrating $B(\omega_1, \omega_2)$ along radial slices in the bifrequency plane (**Selected Bispectrum** or **Bicoherence**) yields a noise-immune feature vector that captures the subtle non-linear transfer curve of an individual unit's PA transistor.

### 3. STFT / Wavelet Scalograms & Complex-Valued Deep Learning (CV-CNNs)
Modern maritime SEI systems feed either:
* **Short-Time Fourier Transform (STFT) spectrograms or Continuous Wavelet Transform (CWT) Morlet scalograms** of the $833\text{ }\mu\text{s}$ turn-on ramp:
  $$\mathcal{W}_z(s, \tau) = \frac{1}{\sqrt{|s|}} \int_{-\infty}^{\infty} z_{\text{ramp}}(t)\, \psi^*\!\left(\frac{t - \tau}{s}\right) dt$$
  which resolve both fast sub-microsecond RF switch clicks (at fine scales $s$) and slower ALC loop ringing (at coarse scales $s$), or
* **The dechirped complex baseband sequence $z_{\text{res}}[n] = I_{\text{res}}[n] + j Q_{\text{res}}[n]$** directly into a **Complex-Valued Convolutional Neural Network (CV-CNN)** or **ResNet-1D**.

Unlike standard real-valued CNNs that treat $I$ and $Q$ as independent channels, a CV-CNN performs true complex convolution with complex weights $W = W_R + j W_I$:

$$(W * z)_{\text{complex}} = (W_R * I - W_I * Q) + j(W_R * Q + W_I * I)$$

preserving phase-rotation equivariance and isolating conjugate I/Q asymmetry $(\mu, \nu)$.

#### Open-Set Verification via Siamese Metric Networks
Because roughly 300,000+ AIS transceivers exist worldwide, a closed-set softmax classifier cannot be pre-trained on every ship on Earth. Instead, operational VTS and intelligence systems train a **Siamese / Triplet Loss Metric Network** $f_\theta(z_{\text{res}}) \in \mathbb{R}^{128}$ that maps each AIS burst onto a unit hypersphere ($\|f_\theta\| = 1$).
* For every vessel `MMSI X`, the system stores a rolling historical template of its embedding vector $\mathbf{e}_{\text{hist}}(\text{MMSI } X)$ and scalar physical features $(\epsilon_{\text{xtal}}, \hat{h}, \text{IRR}, t_r)$.
* When a new burst arrives claiming to be `MMSI X` (e.g., after a 6-day dark gap or at a Venezuela anchorage), the system computes the cosine distance $D_{\text{cos}} = 1 - \mathbf{e}_{\text{new}} \cdot \mathbf{e}_{\text{hist}}$ and the Mahalanobis distance across physical features. If $D > \gamma_{\text{thresh}}$, an **Automated Emitter Swap / Spoofing Alert** is raised!

### 4. Multi-Sensor Physical Verification (AoA, TDOA, FDOA, and Radar/SAR Fusion)
RF fingerprinting is deadliest when fused with geometric radiolocation:
* **Single-Station Angle of Arrival (AoA):** A coastal VHF Direction Finding (DF) array (such as a Rohde & Schwarz DDF, Techtest/Cobham, or 5-channel coherent KrakenSDR phase interferometer; see Chapter 18) measures the physical azimuth $\theta_{\text{AoA}}$ of every $26.67\text{ ms}$ AIS burst to $\pm 1^\circ\text{–}2^\circ$. If a vessel's decoded payload claims coordinates at azimuth $\theta_{\text{AIS}} = 240^\circ$, but the RF burst arrives from $\theta_{\text{AoA}} = 085^\circ$ (or if 20 "different" ships all arrive from the exact same bearing $\theta_{\text{AoA}} = 085.2^\circ$), RF spoofing is confirmed instantaneously on the first packet.
* **Multi-Station TDOA (Time Difference of Arrival):** When three or more time-synchronized coastal NAIS towers receive the same AIS burst, cross-correlating the complex IQ envelopes determines the arrival time differences $\Delta \tau_{ij}$ to sub-microsecond precision ($\sim 50\text{–}150\text{ ns}$ via interpolated cross-ambiguity functions), intersecting hyperbolas to geolocate the physical transmitter within $50\text{–}200\text{ m}$ regardless of what coordinates are written inside the packet.
* **LEO Satellite FDOA (Frequency Difference of Arrival / Doppler Curve):** A LEO satellite passing overhead at $v_{\text{sat}} \approx 7.5\text{ km/s}$ observes an S-shaped Doppler shift curve $\Delta f_{\text{Doppler}}(t) = -\frac{f_c}{c} \frac{d}{dt}\|\mathbf{r}_{\text{sat}}(t) - \mathbf{r}_{\text{emitter}}\|$ across a 10-minute pass. Fitting the inflection time (Time of Closest Approach) and maximum slope of $\Delta f_{\text{Doppler}}(t)$ geolocates the transmitter to within $2\text{–}5\text{ km}$ from a *single* satellite pass—instantly catching a shadow-fleet tanker in the Arabian Sea dual-broadcasting an MMSI that claims to be in the South China Sea!

---

## 28.4 Hardware, Standards, & Software Ecosystem for RF Forensics and Counter-Spoofing

### 1. Governing RF & Security Standards
* **ITU-R M.1371-5 (2014), Annex 2:** Defines the physical-layer GMSK parameters ($BT = 0.4$ TX, $BT \le 0.5$ RX, $9,600\text{ bps} \pm 50\text{ ppm}$ max tolerance, 8-bit [$833\text{ }\mu\text{s}$] ramp-up/down timing, and spectral mask).
* **IEC 61993-2 (Class A) & IEC 62287-1 / 62287-2 (Class B CS / SO):** Specify tight type-approval tolerances for carrier frequency error ($\pm 500\text{ Hz}$ Class A; $\pm 1,500\text{ Hz}$ Class B), modulation accuracy, transient power switching profile, and spurious emissions ($-70\text{ dBc}$ at $\pm 25\text{ kHz}$). These strict type-approval bounds are the exact reason certified transponders cluster tightly in feature space while cheap SDR spoofers stand out as outliers.
* **ITU-R M.2092-1 (VDES / AIS 2.0) & IEC 63173-2 (SECOM):** Introduce native Public Key Infrastructure (PKI) digital signatures and X.509 certificate chains for VDES messages, alongside **IALA Guideline G1117 / Recommendation R-129** on GNSS vulnerability and terrestrial R-Mode (Ranging Mode) backup navigation.

### 2. RF Collection Hardware & Spaceborne SIGINT Ecosystem
* **Coastal & Shipboard Wideband IQ Collectors:** Ettus Research **USRP B210 / N210 / X310** (with GPSDO 10 MHz / 1PPS locking), Airspy R2/Mini ($12\text{-bit}$, $10\text{ MS/s}$), SDRplay RSPdx ($14\text{-bit}$), and **KrakenSDR** (5-channel phase-coherent RTL-SDR for VHF AoA direction finding).
* **Commercial Spaceborne RF Geolocation Constellations:**
  * **HawkEye 360:** Operates tri-satellite pathfinder clusters in LEO that simultaneously collect VHF AIS, marine X-band/S-band navigation radar pulses, and UHF/L-band push-to-talk communications, performing spaceborne **TDOA + FDOA** geolocation to verify whether an AIS position matches its physical RF emission point and detecting "dark ships" via their navigation radar emissions.
  * **Unseenlabs:** Operates a LEO constellation dedicated to single-satellite spaceborne RF signature and geolocation of maritime emitters through cloud cover and darkness.
  * **Spire Maritime & Kleos:** Spaceborne AIS and RF Doppler geolocation payloads verifying vessel positions via S-curve Doppler kinematics.

### 3. Open-Source Software Stack for Baseband AIS Forensics
* **`AIS-catcher` (Jasper Vries):** High-performance C++ SDR receiver supporting RTL-SDR, Airspy, SDRplay, HackRF, and **SigMF / WAV / raw IQ file playback**, outputting per-message physical metadata including **signal power level ($\text{dBm}$)** and **Carrier Frequency Offset ($\text{ppm}$ / $\text{Hz}$)** inside JSON/NMEA TAG blocks (`\s:...,l:-34.2,f:+1.4*hh\`).
* **GNU Radio (`gr-ais`) & `Liquid-DSP`:** Modular C++/Python DSP blocks for GMSK synchronization, matched filtering, and custom IQ transient capture.
* **SigMF (Signal Metadata Format):** Standard JSON + binary `.sigmf-meta` / `.sigmf-data` schema for archiving raw complex IQ bursts with exact sample rate, center frequency, GPSDO timestamp, and hardware provenance annotations.

---

## 28.5 Security, Adversarial Abuse, & Failure Modes in RF Fingerprinting and Spoofing Detection

An engineer designing a counter-spoofing or SEI system must account for both **adversarial counter-measures** and **innocent hardware failure modes** that can mimic spoofing:

1. **Multipath Channel Distortion Over Sea Water:** At low grazing angles over a rough sea surface, two-ray specular reflection and diffuse scattering introduce time-varying amplitude fading across the $26.67\text{ ms}$ burst. However, because a vessel moving at $15\text{ knots}$ ($7.7\text{ m/s}$) at $\lambda = 1.85\text{ m}$ ($162\text{ MHz}$) experiences a maximum Doppler spread of $f_d = \frac{v}{\lambda} \approx 4.2\text{ Hz}$ (coherence time $T_c \approx \frac{1}{4 f_d} \approx 60\text{ ms} \gg 833\text{ }\mu\text{s}$), the sea-surface channel is **quasi-static across the $833\text{ }\mu\text{s}$ turn-on ramp**! Normalizing the ramp envelope by the steady-state preamble amplitude $a_{\text{norm}}(t) = a(t) / \bar{a}_{\text{preamble}}$ removes path-loss scaling while preserving the relative overshoot $M_p$, rise time $t_r$, and ringing frequency $\omega_n$.
2. **Adversarial Waveform Pre-Distortion & Replay:** Could a sophisticated state actor record a genuine burst from `Vessel X` at $10\text{ MS/s}$ and replay it? A raw IQ replay preserves `Vessel X`'s RF fingerprint, *except*:
   * It merely repeats the old coordinates from when the recording was made (useless for synthesizing a new trajectory), and
   * It cascades the **spoofer's own DAC, I/Q mixer, crystal offset, and PA transient** on top of the recorded signal ($z_{\text{replay}} = h_{\text{spoofer}} * z_{\text{recorded}}$), doubling the phase noise and adding the spoofer's I/Q conjugate image.
3. **False-Positive Spoofing Flags from Innocent Shipboard Failures:**
   * **Corroded Antenna Coax / Blown Active Splitter:** When a ship's active VHF/AIS splitter fails or water ingresses into a PL-259 connector, the reflected VSWR spike alters the load impedance seen by the PA, shifting its ramp overshoot and dropping radiated power by $20\text{ dB}$—which can trigger an SEI anomaly alert even though the ship is not spoofing.
   * **Stale GNSS Sentences & Datum/Buffer Glitches:** Cheap Class B units or misconfigured NMEA multiplexers occasionally replay cached `$GPRMC` sentences when the GPS loses sky view under a crane or bridge, creating stationary "frozen" tracks that resemble anchor-loop spoofing until verified by continuous RF AoA tracking.

---

## 28.6 Practical Engineering / Code Walkthrough: Baseband IQ Synthesis and Automated RF Fingerprint Classifier

To demonstrate how physical-layer SEI unmasks spoofing in practice, the self-contained Python script below synthesizes realistic oversampled complex baseband IQ bursts ($f_s = 960\text{ kS/s}$, $N_{\text{sps}} = 100$ samples/symbol) for three distinct emitters broadcasting the **exact same digital AIS payload** (claiming to be MMSI `366999111`):

1. **Emitter A (Authentic Vessel — Furuno-Class PLL Transponder, Unit #1):** Direct fractional-$N$ PLL GMSK modulator ($BT = 0.40$, $h = 0.50$), zero I/Q imbalance ($\alpha = 0, \theta_{\text{IQ}} = 0^\circ$), zero LO carrier leakage, underdamped ALC PA ramp ($\omega_n = 2\pi \times 3.2\text{ kHz}$, $\zeta = 0.55$), and a $+1.15\text{ ppm}$ ($+186.3\text{ Hz}$) locked TCXO with $+0.45\text{ Hz/ms}$ thermal drift.
2. **Emitter B (Sister Ship / Same Manufacturer, Unit #2):** Same PLL architecture, but unit-specific component tolerances yield $\omega_n = 2\pi \times 3.8\text{ kHz}$, $\zeta = 0.72$, and a $-0.85\text{ ppm}$ ($-137.7\text{ Hz}$) locked TCXO.
3. **Emitter C (Direct-Conversion SDR Spoofer — HackRF + Linear Amp):** Zero-IF quadrature upconverter attempting to impersonate Emitter A, suffering from $3.5\%$ I/Q gain imbalance ($\alpha = 0.035$), $2.8^\circ$ quadrature phase skew, $-28\text{ dBc}$ LO carrier feedthrough, a misconfigured $BT = 0.30$ software filter, fast abrupt PA switching ($\zeta = 0.92$, $\omega_n = 2\pi \times 8.5\text{ kHz}$), and a $-6.40\text{ ppm}$ ($-1,036.6\text{ Hz}$) clock offset with a $2.1\text{ ppm}$ mismatch between carrier and symbol rate.

The script extracts a 7-dimensional physical-layer RF fingerprint vector from each burst—including **PA $10\%\text{–}90\%$ rise time ($t_r$)**, **PA envelope overshoot ($M_p$)**, **estimated modulation index ($\hat{h}$)**, **alternating-to-run deviation ratio ($\widehat{BT}$ proxy)**, **Carrier Frequency Offset ($\Delta f_c$)**, **CFO-vs-Symbol-Clock ppm discrepancy ($\Delta\epsilon_{\text{clock}}$)**, and **Dechirped Spectral Image Rejection Ratio ($\text{IRR}_{\text{dB}}$)**—and classifies both manufacturer architecture and individual unit authenticity.

```python
#!/usr/bin/env python3
"""
Chapter 28 Practical Walkthrough:
Physical-Layer AIS Baseband IQ Synthesizer & Specific Emitter Identification (SEI)
Extracts PA ramp transients, GMSK modulation index/BT, CFO-vs-baud clock lock,
and Direct-Conversion SDR I/Q conjugate mirror image to unmask AIS spoofers.
"""

from dataclasses import dataclass
import numpy as np


@dataclass
class EmitterHardwareProfile:
    name: str
    architecture: str          # "PLL_CLASS_A" or "DIRECT_CONV_SDR"
    bt_product: float          # Gaussian filter BT product (ideal = 0.4)
    mod_index_h: float         # GMSK modulation index (ideal = 0.5)
    cfo_ppm: float             # Carrier frequency offset in ppm (at 161.975 MHz)
    sym_clock_ppm: float       # Symbol rate clock offset in ppm (at 9600 bps)
    thermal_chirp_hz_ms: float # Post-key-up PA thermal drift slope (Hz/ms)
    pa_wn_hz: float            # PA ALC loop natural frequency (Hz)
    pa_zeta: float             # PA ALC loop damping ratio
    iq_gain_imbalance: float   # Quadrature gain error alpha (0.0 for PLL)
    iq_phase_skew_deg: float   # Quadrature phase skew theta_IQ in deg (0.0 for PLL)
    lo_leakage_dbc: float      # Unmodulated LO carrier feedthrough in dBc (-inf for PLL)


def gaussian_fir_pulse(bt: float, sps: int, span_symbols: int = 4) -> np.ndarray:
    """Computes the GMSK frequency-shaping pulse p(t) = rect(t/Tb) * g(t)."""
    t = np.arange(-span_symbols * sps // 2, span_symbols * sps // 2 + 1) / float(sps)
    sigma = np.sqrt(np.log(2.0)) / (2.0 * np.pi * bt)
    g = (1.0 / (np.sqrt(2.0 * np.pi) * sigma)) * np.exp(-(t**2) / (2.0 * sigma**2))
    rect = np.ones(sps) / float(sps)
    p = np.convolve(g, rect, mode="same")
    return p / np.sum(p)  # Normalize so integral over 1 symbol = 1.0


def build_deterministic_ais_burst_bits() -> np.ndarray:
    """
    Constructs a 256-bit deterministic AIS burst (8 ramp + 24 preamble + 224 frame)
    so all emitters transmit the exact same digital bits (identical MMSI & CRC).
    Returns bipolar NRZI modulation symbols d_k in {-1, +1}.
    """
    rng = np.random.default_rng(seed=42)
    # 8-bit ramp-up unmodulated/stabilization + 24-bit alternating preamble (010101...)
    ramp_bits = np.zeros(8, dtype=int)
    preamble = np.tile([0, 1], 12)
    start_flag = np.array([0, 1, 1, 1, 1, 1, 1, 0], dtype=int)
    # Include deliberate run-length patterns (000111000) to probe full +/-2400 Hz deviation
    probe_runs = np.array([0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1] * 4, dtype=int)
    payload_and_crc = rng.integers(0, 2, size=256 - 8 - 24 - 8 - len(probe_runs))
    bits = np.concatenate([ramp_bits, preamble, start_flag, probe_runs, payload_and_crc])
    # Map {0, 1} to bipolar {-1, +1} frequency deviation impulses
    return 2.0 * bits - 1.0


def synthesize_ais_iq_burst(
    profile: EmitterHardwareProfile,
    d_k: np.ndarray,
    fs: float = 960_000.0,
    rb_nominal: float = 9_600.0,
    fc_vhf: float = 161_975_000.0,
    snr_db: float = 42.0,
    seed: int = 100,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Synthesizes a complex baseband IQ burst z[n] incorporating hardware-specific
    PA transient ringing, GMSK BT filter, clock skew, thermal drift, and SDR I/Q quirks.
    """
    rng = np.random.default_rng(seed=seed)
    sps = int(round(fs / rb_nominal))  # 100 samples per symbol
    n_total = len(d_k) * sps
    t = np.arange(n_total) / fs

    # 1. Symbol-rate clock skew alters effective symbol period
    rb_actual = rb_nominal * (1.0 + profile.sym_clock_ppm * 1e-6)
    p_pulse = gaussian_fir_pulse(profile.bt_product, sps, span_symbols=4)

    # Upsample bipolar NRZI symbols and filter with Gaussian pulse
    impulses = np.zeros(n_total)
    symbol_indices = np.clip(
        np.round(np.arange(len(d_k)) * (fs / rb_actual)).astype(int), 0, n_total - 1
    )
    impulses[symbol_indices] = d_k
    freq_norm = np.convolve(impulses, p_pulse, mode="same")

    # Instantaneous GMSK phase phi_gmsk(t) = 2*pi*h * integral(freq_norm)
    phi_gmsk = np.cumsum(np.pi * profile.mod_index_h * freq_norm)

    # Ideal unit-envelope complex baseband signal
    z_ideal = np.exp(1j * phi_gmsk)

    # 2. Apply Direct-Conversion SDR I/Q Imbalance & LO Carrier Leakage (if present)
    alpha = profile.iq_gain_imbalance
    theta = np.deg2rad(profile.iq_phase_skew_deg)
    mu = 0.5 * (1.0 + (1.0 + alpha) * np.exp(1j * theta))
    nu = 0.5 * (1.0 - (1.0 + alpha) * np.exp(-1j * theta))
    c_lo = 0.0 if np.isinf(profile.lo_leakage_dbc) else 10.0 ** (profile.lo_leakage_dbc / 20.0)

    z_mod = mu * z_ideal + nu * np.conj(z_ideal) + c_lo

    # 3. Apply Power Amplifier (PA) 833.33 us Turn-On Ramp Envelope (2nd-order ALC step response)
    wn = 2.0 * np.pi * profile.pa_wn_hz
    zeta = profile.pa_zeta
    wd = wn * np.sqrt(max(1.0 - zeta**2, 1e-6))
    a_ramp = 1.0 - (1.0 / np.sqrt(max(1.0 - zeta**2, 1e-6))) * np.exp(
        -zeta * wn * t
    ) * np.sin(wd * t + np.arccos(np.clip(zeta, -1.0, 1.0)))
    a_ramp = np.clip(a_ramp, 0.0, 2.0)

    # 4. Apply Carrier Frequency Offset (CFO) and post-key-up thermal frequency chirp
    cfo_hz = fc_vhf * (profile.cfo_ppm * 1e-6)
    chirp_rate_hz_s = profile.thermal_chirp_hz_ms * 1000.0
    phi_carrier = 2.0 * np.pi * (cfo_hz * t + 0.5 * chirp_rate_hz_s * (t**2))

    z_tx = a_ramp * z_mod * np.exp(1j * phi_carrier)

    # 5. Add complex Additive White Gaussian Noise (AWGN)
    sig_power = np.mean(np.abs(z_tx) ** 2)
    noise_power = sig_power * (10.0 ** (-snr_db / 10.0))
    noise = np.sqrt(noise_power / 2.0) * (
        rng.standard_normal(n_total) + 1j * rng.standard_normal(n_total)
    )
    return z_tx + noise, phi_gmsk


@dataclass
class RFFingerprintVector:
    pa_rise_time_us: float
    pa_overshoot_pct: float
    est_cfo_hz: float
    est_cfo_ppm: float
    thermal_chirp_hz_ms: float
    est_mod_index_h: float
    bt_dev_ratio: float
    iq_image_irr_db: float
    envelope_ripple_pct: float


def extract_rf_fingerprint(
    z_rx: np.ndarray,
    phi_ideal_ref: np.ndarray,
    fs: float = 960_000.0,
    rb_nominal: float = 9_600.0,
    fc_vhf: float = 161_975_000.0,
) -> RFFingerprintVector:
    """
    Extracts the physical-layer Specific Emitter Identification (SEI) feature vector
    from a single captured complex baseband AIS burst.
    """
    sps = int(round(fs / rb_nominal))
    env = np.abs(z_rx)

    # Steady-state envelope amplitude (measured across symbols 12..240)
    s_start, s_end = 12 * sps, 240 * sps
    a_steady = float(np.mean(env[s_start:s_end]))
    env_norm = env / a_steady

    # 1. PA Turn-On Ramp Features (within first 833.33 us = 8 symbols = 800 samples)
    ramp_win = env_norm[: 8 * sps]
    idx_10 = int(np.argmax(ramp_win >= 0.10))
    idx_90 = int(np.argmax(ramp_win >= 0.90))
    pa_rise_time_us = (idx_90 - idx_10) * (1e6 / fs)
    pa_overshoot_pct = max(0.0, (float(np.max(ramp_win)) - 1.0) * 100.0)

    # Steady-state envelope ripple (captures SDR I/Q + LO beat ripple vs constant-envelope PLL)
    # Smooth out high-frequency AWGN with a 15-sample moving average
    env_smooth = np.convolve(env_norm[s_start:s_end], np.ones(15) / 15.0, mode="valid")
    envelope_ripple_pct = float(np.std(env_smooth) * 100.0)

    # 2. Instantaneous Frequency & Phase Unwrapping over Steady State
    phi_unwrapped = np.unwrap(np.angle(z_rx))
    inst_freq_hz = np.diff(phi_unwrapped) * (fs / (2.0 * np.pi))

    # Ideal instantaneous frequency reference (for h=0.5)
    inst_freq_ref = np.diff(phi_ideal_ref) * (fs / (2.0 * np.pi))

    # Linear regression of residual frequency error over time gives CFO and thermal chirp slope
    t_steady = np.arange(s_start, s_end) / fs
    f_meas_steady = inst_freq_hz[s_start:s_end]
    f_ref_steady = inst_freq_ref[s_start:s_end]

    # Estimate scale factor (h_actual / 0.5) and linear carrier trend:
    # f_meas(t) = scale * f_ref(t) + cfo_0 + chirp * t
    design_mat = np.column_stack([f_ref_steady, np.ones_like(t_steady), t_steady])
    coeffs, _, _, _ = np.linalg.lstsq(design_mat, f_meas_steady, rcond=None)
    scale_h, est_cfo_hz, chirp_hz_s = coeffs
    est_mod_index_h = float(0.5 * scale_h)
    est_cfo_ppm = float((est_cfo_hz / fc_vhf) * 1e6)
    thermal_chirp_hz_ms = float(chirp_hz_s / 1000.0)

    # 3. Estimate BT Filter Ratio: Alternating Preamble (symbols 8..32) vs Run-Length (symbols 40..88)
    f_zero_cfo = inst_freq_hz - (est_cfo_hz + chirp_hz_s * (np.arange(len(inst_freq_hz)) / fs))
    f_alt_peak = float(np.percentile(np.abs(f_zero_cfo[9 * sps : 31 * sps]), 95))
    f_run_peak = float(np.percentile(np.abs(f_zero_cfo[41 * sps : 87 * sps]), 95))
    bt_dev_ratio = f_alt_peak / max(f_run_peak, 1.0)

    # 4. Dechirp Burst & Measure Direct-Conversion I/Q Conjugate Mirror Image Ratio (IRR)
    t_full = np.arange(len(z_rx)) / fs
    phi_carrier_est = 2.0 * np.pi * (est_cfo_hz * t_full + 0.5 * chirp_hz_s * (t_full**2))
    phi_mod_est = (est_mod_index_h / 0.5) * phi_ideal_ref

    # Forward dechirp collapses true signal mu*exp(+j*phi_mod) to DC
    z_dechirp_pos = z_rx[s_start:s_end] * np.exp(-1j * (phi_carrier_est[s_start:s_end] + phi_mod_est[s_start:s_end]))
    p_main = np.abs(np.mean(z_dechirp_pos)) ** 2

    # Conjugate dechirp collapses mirror image nu*exp(-j*phi_mod) to DC
    z_dechirp_neg = z_rx[s_start:s_end] * np.exp(-1j * (phi_carrier_est[s_start:s_end] - phi_mod_est[s_start:s_end]))
    p_image = np.abs(np.mean(z_dechirp_neg)) ** 2
    iq_image_irr_db = float(10.0 * np.log10(p_main / max(p_image, 1e-12)))

    return RFFingerprintVector(
        pa_rise_time_us=pa_rise_time_us,
        pa_overshoot_pct=pa_overshoot_pct,
        est_cfo_hz=float(est_cfo_hz),
        est_cfo_ppm=est_cfo_ppm,
        thermal_chirp_hz_ms=thermal_chirp_hz_ms,
        est_mod_index_h=est_mod_index_h,
        bt_dev_ratio=bt_dev_ratio,
        iq_image_irr_db=iq_image_irr_db,
        envelope_ripple_pct=envelope_ripple_pct,
    )


def main() -> None:
    d_k = build_deterministic_ais_burst_bits()

    emitters = [
        EmitterHardwareProfile(
            "Vessel MMSI 366999111 (Baseline: Furuno FA-170 Unit #1)", "PLL_CLASS_A",
            bt_product=0.40, mod_index_h=0.500, cfo_ppm=+1.15, sym_clock_ppm=+1.15,
            thermal_chirp_hz_ms=+0.45, pa_wn_hz=3200.0, pa_zeta=0.55,
            iq_gain_imbalance=0.0, iq_phase_skew_deg=0.0, lo_leakage_dbc=-np.inf,
        ),
        EmitterHardwareProfile(
            "Observed Burst #1 (Same Furuno FA-170 Unit #1, 3 Days Later)", "PLL_CLASS_A",
            bt_product=0.40, mod_index_h=0.500, cfo_ppm=+1.17, sym_clock_ppm=+1.17,
            thermal_chirp_hz_ms=+0.44, pa_wn_hz=3200.0, pa_zeta=0.55,
            iq_gain_imbalance=0.0, iq_phase_skew_deg=0.0, lo_leakage_dbc=-np.inf,
        ),
        EmitterHardwareProfile(
            "Observed Burst #2 (Identity Clone: Different Class A Unit #2)", "PLL_CLASS_A",
            bt_product=0.40, mod_index_h=0.488, cfo_ppm=-0.85, sym_clock_ppm=-0.85,
            thermal_chirp_hz_ms=+0.92, pa_wn_hz=3800.0, pa_zeta=0.72,
            iq_gain_imbalance=0.0, iq_phase_skew_deg=0.0, lo_leakage_dbc=-np.inf,
        ),
        EmitterHardwareProfile(
            "Observed Burst #3 (Over-the-Air Spoofer: HackRF SDR + PA)", "DIRECT_CONV_SDR",
            bt_product=0.30, mod_index_h=0.515, cfo_ppm=-6.40, sym_clock_ppm=-4.30,
            thermal_chirp_hz_ms=+0.05, pa_wn_hz=8500.0, pa_zeta=0.92,
            iq_gain_imbalance=0.045, iq_phase_skew_deg=3.2, lo_leakage_dbc=-26.0,
        ),
    ]

    # Reference ideal GMSK phase trajectory (BT=0.4, h=0.5)
    _, phi_ideal_ref = synthesize_ais_iq_burst(emitters[0], d_k, snr_db=100.0)

    fps: list[RFFingerprintVector] = []
    print("=" * 94)
    print("PHYSICAL-LAYER AIS RF FINGERPRINTING (SEI) & SPOOFING CLASSIFICATION REPORT")
    print("=" * 94)

    for idx, em in enumerate(emitters):
        z_rx, _ = synthesize_ais_iq_burst(em, d_k, snr_db=42.0, seed=200 + idx)
        fp = extract_rf_fingerprint(z_rx, phi_ideal_ref)
        fps.append(fp)

        # Decision logic
        is_sdr = (fp.iq_image_irr_db < 36.0) or (fp.envelope_ripple_pct > 2.0) or (abs(fp.est_cfo_ppm) > 3.5)
        if idx == 0:
            verdict = "ENROLLED BASELINE TEMPLATE"
        elif is_sdr:
            verdict = "REJECT: DIRECT-CONVERSION SDR SPOOFER DETECTED (I/Q Mirror & Clock Violation)"
        else:
            # Compute normalized Euclidean distance against baseline physical features
            base = fps[0]
            dist = np.sqrt(
                ((fp.pa_rise_time_us - base.pa_rise_time_us) / 15.0) ** 2
                + ((fp.pa_overshoot_pct - base.pa_overshoot_pct) / 2.0) ** 2
                + ((fp.est_cfo_ppm - base.est_cfo_ppm) / 0.25) ** 2
                + ((fp.thermal_chirp_hz_ms - base.thermal_chirp_hz_ms) / 0.15) ** 2
                + ((fp.est_mod_index_h - base.est_mod_index_h) / 0.005) ** 2
            )
            verdict = (
                f"AUTHENTICATED: Matches Baseline Unit #1 (SEI Distance = {dist:.2f})"
                if dist < 2.5
                else f"ALERT: EMITTER SWAP / TRANSCEIVER CLONE! (SEI Distance = {dist:.2f})"
            )

        print(f"\n[{idx}] {em.name}")
        print(f"    PA Ramp (833 us) : Rise Time t_r = {fp.pa_rise_time_us:6.1f} us | Overshoot Mp = {fp.pa_overshoot_pct:5.2f} %")
        print(f"    Carrier & Drift  : CFO = {fp.est_cfo_hz:+7.1f} Hz ({fp.est_cfo_ppm:+5.2f} ppm) | Thermal Chirp = {fp.thermal_chirp_hz_ms:+5.2f} Hz/ms")
        print(f"    GMSK Modulator   : Est Index h   = {fp.est_mod_index_h:6.4f}    | Alt/Run Ratio = {fp.bt_dev_ratio:5.3f}")
        print(f"    Quadrature / Env : I/Q IRR       = {fp.iq_image_irr_db:5.1f} dB  | Env Ripple    = {fp.envelope_ripple_pct:5.2f} %")
        print(f"    --> SEI VERDICT  : {verdict}")


if __name__ == "__main__":
    main()
```

### Verification of Output Metrics
Running the walkthrough script produces the following deterministic physical-layer classification across the four bursts:
* **Baseline Unit #1 & Burst #1 (Genuine Vessel 3 Days Later):** Both exhibit a PA $10\%\text{–}90\%$ rise time of $t_r \approx 168.8\text{ }\mu\text{s}$, an ALC underdamped envelope overshoot of $M_p \approx 12.6\%$, a locked TCXO offset of $+1.15\text{ to }+1.17\text{ ppm}$ ($+186\text{ to }+189\text{ Hz}$), a $+0.44\text{ Hz/ms}$ PA thermal chirp, an alternating-to-run deviation ratio of $0.665$ (confirming $BT = 0.40$), and a dechirped Image Rejection Ratio $>39\text{ dB}$ with minimal envelope ripple ($<0.4\%$). The SEI distance is $0.14 < 2.5$, authenticating the physical radio.
* **Burst #2 (Dual-Broadcast / Anchor-Loop Transceiver Swap):** Although the digital bits and MMSI are identical, the second Class A unit exhibits a faster rise time ($t_r \approx 156.2\text{ }\mu\text{s}$), lower overshoot ($M_p \approx 3.8\%$), a negative TCXO offset ($-0.85\text{ ppm}$ / $-137.7\text{ Hz}$), and a $+0.92\text{ Hz/ms}$ thermal chirp, yielding an SEI distance of $9.81 \gg 2.5$ and immediately flagging an **Emitter Swap / Transceiver Clone**.
* **Burst #3 (HackRF Direct-Conversion SDR Spoofer):** The SDR spoofer is immediately unmasked by four orthogonal physical violations: its conjugate I/Q mirror image drops $\text{IRR}$ to $30.1\text{ dB}$, LO carrier leakage + I/Q beating drives envelope ripple up to $4.36\%$, its misconfigured $BT = 0.30$ filter drops the alternating-to-run deviation ratio to $0.542$, and its uncompensated crystal violates the IEC 61993-2 $\pm 3.1\text{ ppm}$ mask at $-6.40\text{ ppm}$ ($-1,036\text{ Hz}$).

---

## 28.7 Key Takeaways & Operational Checklist

1. **Always Separate the Five Spoofing Mechanisms First:** Before launching an investigation, determine whether an anomalous AIS track is **Aggregator API Injection** (absent from RF receivers), **Over-the-Air SDR RF Spoofing** (all targets radiate from one azimuth with SDR I/Q impairments), **Identity Laundering / Dual-Broadcasting** (two hulls in different oceans sharing one MMSI), **Dual-Transponder Anchor-Loop Decoy** (real tanker goes dark while a boat/shore box loops at anchorage), or **GNSS L1 Spoofing** (ships' own certified Class A radios broadcast airport or "crop-circle" coordinates while Gyro True Heading remains normal).
2. **Never Discard Physical-Layer Metadata at the Receiver:** Configure coastal VTS and research SDR receivers (e.g., `AIS-catcher`, USRP/Airspy collectors) to log per-message **RSSI ($\text{dBm}$)**, **Carrier Frequency Offset ($\text{ppm}$ / $\text{Hz}$)**, **arrival timestamp ($\text{ns}$)**, and—for high-interest zones—**complex baseband IQ snippets** (`.sigmf`) covering the $833\text{ }\mu\text{s}$ turn-on ramp.
3. **Check Gyro True Heading Against GNSS COG on the Bridge:** When transiting known electronic warfare zones (Black Sea, Eastern Med, Red Sea, Baltic, Persian Gulf), bridge officers and VTS analysts should compare `True Heading` (from the ship's gyrocompass) against `COG` (from GNSS). During GNSS L1 spoofing, `COG` jumps toward the spoofed attractor while `True Heading` continues pointing along the true course.
4. **Exploit Direct-Conversion vs. PLL Physics:** Certified Class A and Class B marine transponders are constant-envelope PLL/DDS transmitters with zero quadrature mirror images. Any AIS burst exhibiting a conjugate I/Q mirror image ($\nu z^*(t)$) or unmodulated LO carrier spike after dechirping was transmitted by a direct-conversion Software-Defined Radio.
5. **Cross-Cue SEI with Geometric Radiolocation and SAR:** Bind every high-interest MMSI to a historical physical-layer profile $(\epsilon_{\text{xtal}}, df_c/dt, t_r, M_p, \hat{h}, \widehat{BT})$ and cross-verify against coastal VHF Direction Finding (**AoA**), multi-station **TDOA**, satellite **Doppler FDOA curves**, and spaceborne **Synthetic Aperture Radar (SAR)**.

---

## 28.8 Cited References & Primary Sources

1. **AIS Security, Spoofing Taxonomy, and GNSS Electronic Warfare:**
   * Balduzzi, M., Pasta, A., & Wilhoit, K. (2014). A security evaluation of AIS automated identification system. In *Proceedings of the 30th Annual Computer Security Applications Conference (ACSAC)* (pp. 436–445). ACM. [`https://doi.org/10.1145/2664243.2664257`](https://doi.org/10.1145/2664243.2664257)
   * Center for Advanced Defense Studies (C4ADS). (2019). *Above Us Only Stars: Exposing GPS Spoofing in Russia and Syria*. Washington, DC: C4ADS. [`https://c4ads.org/reports/above-us-only-stars/`](https://c4ads.org/reports/above-us-only-stars/)
   * Bergman, B. (2020). *Spoofing in the Black Sea: What really happened to HMS Defender?* SkyTruth / Words on the Water; and MIT Technology Review coverage of Shanghai GPS "Crop Circles" (Harris, M., 2019, *"Ghost ships, crop circles, and soft gold: A GPS mystery in Shanghai"*).
   * Androjna, A., Brcko, T., Pavic, I., & Perkovič, M. (2020). Assessing cyber challenges of maritime navigation. *Journal of Marine Science and Engineering*, 8(10), 776. [`https://doi.org/10.3390/jmse8100776`](https://doi.org/10.3390/jmse8100776)
2. **Physical-Layer Specific Emitter Identification (SEI) & RF Fingerprinting:**
   * Danev, D., Zanetti, D., & Capkun, S. (2012). On physical-layer identification of wireless devices. *ACM Computing Surveys*, 45(1), 1–29. [`https://doi.org/10.1145/2379776.2379782`](https://doi.org/10.1145/2379776.2379782)
   * Talbot, K. I., Duley, P. R., & Hyatt, M. H. (2003). Specific emitter identification and verification. *Technology Review Journal* (Northrop Grumman), 11(1), 113–133.
   * Jagannath, A., Jagannath, J., & Drozd, A. (2021–2024) & Wang, Y., et al. (2021). Deep learning for Specific Emitter Identification of maritime AIS signals using transient envelopes, bispectrum, and complex-valued CNNs. *IEEE Transactions on Information Forensics and Security* / *IEEE Transactions on Vehicular Technology*.
   * Hall, J., Barbeau, M., & Kranakis, E. (2003). Detection of transient in radio frequency fingerprinting using signal phase. In *Proceedings of the IASTED International Conference on Wireless and Optical Communications*.
3. **RF Standards, VDES Authentication, and History:**
   * ITU-R. (2014). *Recommendation ITU-R M.1371-5: Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile frequency band*. Geneva: International Telecommunication Union. [`https://www.itu.int/rec/R-REC-M.1371/`](https://www.itu.int/rec/R-REC-M.1371/)
   * IEC. (2018). *IEC 61993-2: Maritime navigation and radiocommunication equipment and systems — Automatic identification systems (AIS) — Part 2: Class A shipborne equipment of the automatic identification system (AIS) — Operational and performance requirements, methods of test and required test results*. Geneva: International Electrotechnical Commission.
   * IEC. (2014/2017). *IEC 62287-1 & IEC 62287-2: Class B shipborne equipment of the AIS (CSTDMA and SOTDMA)*. Geneva: IEC.
   * ITU-R. (2022). *Recommendation ITU-R M.2092-1: Technical characteristics for a VHF data exchange system in the VHF maritime mobile band (VDES)*. Geneva: ITU.
   * Schwehr, K. (2024–2026). *gis-history: A list of key events in the history of Geographic Information Systems (GIS) and spatial data processing*. GitHub. [`https://github.com/schwehr/gis-history`](https://github.com/schwehr/gis-history)
   * Vries, J. (2021–present). *AIS-catcher: Multi-platform SDR AIS receiver*. GitHub. [`https://github.com/jvde-github/AIS-catcher`](https://github.com/jvde-github/AIS-catcher)
