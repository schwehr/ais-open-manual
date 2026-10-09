# Chapter 32 — Antennas for every application

> **Part V — Radio.** The antenna systems, transmission lines, and spatial siting rules that translate AIS radio-frequency energy between shipboard transponders, shore stations, satellites, and the open sea.

**In this chapter.** You will learn how antenna design, radiation patterns, transmission lines, and spatial siting dictate the performance of the Automatic Identification System (**AIS**). We examine core VHF topologies—including half-wave dipoles, quarter-wave monopoles, 5/8-wave radiators, collinear whips, J-poles, and Yagi-Uda arrays—demonstrating how elevation beamwidth compression degrades links on rolling vessels. You will evaluate the trade-offs of tuning antennas for 162 MHz versus voice channels, and analyze active antenna splitters alongside their critical failure modes. We review the physical installation requirements established by IMO SN/Circ.227 and COMSAR circulars, detailing isolation geometry, radar beam exclusion zones, and coaxial cable loss at 162 MHz. Furthermore, we investigate antenna constraints across commercial ships, small craft, sub-watt search-and-rescue burst devices, coastal shore stations, and orbital satellites. Finally, we provide step-by-step procedures for testing installations using vector network analyzers, establishing quantitative return-loss thresholds, and diagnosing RF physical-layer degradation.

## 32.1 Wavelength, polarization, and fundamental antenna types

Marine AIS operates in the upper portion of the maritime mobile Very High Frequency (**VHF**) band allocated under Appendix 18 of the Radio Regulations (ITU 2020). The standard channels are:
- **AIS 1:** 161.975 MHz
- **AIS 2:** 162.025 MHz

Taking the center frequency as 162.000 MHz, the free-space carrier wavelength $\lambda$ is governed by the speed of light $c$:
$$\lambda = \frac{c}{f} = \frac{299{,}792{,}458\text{ m/s}}{162{,}000{,}000\text{ Hz}} \approx 1.8506\text{ m}$$

At roughly 1.85 m (6.07 ft), resonant conductors—such as half-wave sections of 0.925 m (36.4 in) and quarter-wave sections of 0.463 m (18.2 in)—form the physical basis of marine AIS antennas.

International standards mandate **vertical polarization** for all terrestrial maritime VHF links. The electric field vector oscillates perpendicular to the sea surface, coupling efficiently with conducting hulls and seawater while providing omnidirectional azimuth radiation from vertical spars.

### 32.1.1 The half-wave center-fed dipole

The center-fed **half-wave dipole** is the fundamental reference for maritime VHF. In free space, its physical length spans $\lambda / 2 \approx 0.925\text{ m}$. Accounting for conductor velocity factor and end effect (3% to 5% shortening):
$$L_{\text{dipole}} \approx 0.95 \times \frac{\lambda}{2} \approx 0.88\text{ m to } 0.90\text{ m}$$

In free space, a thin half-wave dipole exhibits a radiation resistance of $73\ \Omega$ at resonance and delivers an isotropic gain of:
$$G = 2.15\text{ dBi} = 0.0\text{ dBd}$$
where **dBi** is referenced to an isotropic radiator, and **dBd** is referenced to a lossless half-wave dipole ($G_{\text{dBi}} = G_{\text{dBd}} + 2.15\text{ dB}$).

Mounted vertically, the dipole's azimuth pattern is circular (omnidirectional). In elevation, the pattern yields a broad half-power beamwidth (**HPBW**) of approximately $78^\circ$ ($\pm 39^\circ$). This broad elevation beam provides exceptional tolerance to vessel roll and heel.

### 32.1.2 The quarter-wave ground plane

Where a metallic counterpoise exists (a steel wheelhouse roof or aluminum arch), a **quarter-wave monopole** ($\lambda / 4 \approx 0.463\text{ m}$) can be installed. By image theory, an infinite ground plane synthesizes the upper half of a dipole:
- Input impedance drops to $R_{\text{in}} \approx 73 / 2 \approx 36.5\ \Omega$.
- Total power radiates into the upper hemisphere, yielding a directivity of $5.15\text{ dBi}$.

Real shipboard ground planes are finite and irregular. On a steel wheelhouse, feedpoint impedance measures 35 to 45 $\Omega$. With artificial quarter-wave wire radials angled downward at $45^\circ$, the impedance rises to $50\ \Omega$ while depressing the elevation lobe toward the horizon.

### 32.1.3 The 5/8-wave radiator and stacked collinear arrays

A **5/8-wave antenna** ($\frac{5}{8}\lambda \approx 1.156\text{ m}$) achieves approximately 3 dBd (5.15 dBi) gain over ground by flattening the vertical pattern toward the horizon. Because a $5/8\lambda$ whip is capacitive at its base, an inductive base-loading coil is required to cancel reactance and match $50\ \Omega$.

**Collinear arrays** connect two or more half-wave radiating elements end-to-end, separated by $180^\circ$ phasing coils:
- A two-element collinear ("6 dBi" marine whip, 2.4 m long) narrows elevation HPBW to approximately $\pm 15^\circ$ ($30^\circ$ total).
- A multi-element collinear ("9 dBi" whip, 4.5 to 5.5 m long) compresses elevation HPBW to roughly $\pm 8^\circ$ to $\pm 10^\circ$ ($16^\circ$–$20^\circ$ total).

### 32.1.4 End-fed vertical sleeves and the J-pole

To feed a vertical half-wave element from its base without distorting the pattern:
1. **Coaxial Sleeve Dipole:** The upper quarter-wave is a center-conductor extension; the lower quarter-wave is a metallic sleeve over the coax shield, isolated with a ferrite choke.
2. **J-Pole Antenna:** A half-wave radiator end-fed via an integrated quarter-wave matching stub. The shorted base provides a direct DC ground, offering high static-drain protection for coastal sites.

### 32.1.5 Directional antennas: Yagi-Uda arrays

For shore-based Vessel Traffic Services (**VTS**) or coastal monitoring stations, omnidirectional reception collects unwanted inland radio noise. A directional **Yagi-Uda array** consists of a driven element, a reflector, and directors along a boom:
- A 3-element Yagi provides 7 to 8 dBi forward gain and $> 15\text{ dB}$ front-to-back (**F/B**) ratio.
- A 5-element Yagi achieves 10 to 11 dBi gain and $> 20\text{ dB}$ F/B ratio, focusing sensitivity over shipping channels while rejecting landward interference.

| Antenna Topology | Physical Height (m) | Nominal Gain (dBi) | Elevation HPBW | Recommended Application |
|---|---|---|---|---|
| **Quarter-Wave Monopole** | 0.46 | 2.5–3.5 | $\approx 45^\circ$ | Workboats, steel cabs |
| **Half-Wave Dipole / Sleeve** | 0.90–1.0 | 2.15 | $\approx 78^\circ$ | Sailboats, rolling craft, Class A standard |
| **5/8-Wave Ground Plane** | 1.2 | 4.5–5.2 | $\approx 36^\circ$ | Coastal stations, calm-water craft |
| **Collinear Array (2-element)** | 2.0–2.5 | 5.5–6.0 | $\approx 30^\circ$ | Stable commercial ships, VTS bases |
| **Collinear Array (multi-element)**| 4.5–5.5 | 8.5–9.0 | $\approx 16^\circ$ | Shore base stations, rigid towers only |
| **J-Pole** | 1.4 | 2.2 | $\approx 75^\circ$ | Coast monitoring, static drain |
| **5-Element Yagi-Uda** | 1.8 (boom) | 10.0–11.0 | $\approx 50^\circ$ | Coastal sector coverage, noise rejection |

---

## 32.2 Gain, radiation pattern, and vessel motion

Antenna gain does not amplify signals; it redistributes RF energy. An omnidirectional whip achieves gain exclusively by flattening its vertical elevation pattern into a narrow disk aimed at the horizon.

```
Elevation Patterns and Vessel Motion
=============================================================================
A. Level Platform (0° Heel / Roll):
   Both antennas radiate directly toward distant horizon targets.
   Low-Gain Dipole (2.15 dBi, broad HPBW ±39°):
              \            /
     ----------================---------- Horizon (Target Vessel)
              /            \
   High-Gain Collinear (9 dBi, narrow HPBW ±8°):
     ----------================---------- Horizon (Target Vessel)

B. Vessel Heeled or Rolled 20°:
   Low-Gain Dipole (2.15 dBi):
         \            /
   -------================------- Horizon (Target Vessel still inside lobe)
         /            \
   High-Gain Collinear (9 dBi):
               ====== (Beam pointing into the sky: +20°)
   ------------------------------ Horizon (Null / -15 dB down; Target Lost)
        ====== (Opposite lobe pointing into sea: -20°)
```

### 32.2.1 The geometry of heel, pitch, and roll

When a vessel encounters sea conditions, it experiences rotational displacement across three axes:
- **Heel:** A sustained list from sail pressure, cargo bias, or high-speed turning.
- **Roll:** Dynamic oscillation about the longitudinal axis, frequently reaching $15^\circ$ to $25^\circ$ in Sea State 4.
- **Pitch:** Angular oscillation about the transverse axis in swells.

A 9 dBi collinear whip has an elevation beamwidth of barely $\pm 8^\circ$. When a vessel heels or rolls by $20^\circ$:
1. On the high side, the lobe points $20^\circ$ into the sky. At the horizon ($0^\circ$), radiated power drops 15 to 25 dB into pattern nulls.
2. On the low side, the lobe fires into the sea, dissipating power into water.
3. Across bow and stern, polarization tilts, inducing cross-polarization fading.

The vessel's AIS signal drops below receiver thresholds ($-107\text{ dBm}$ under IEC 61993-2) on surrounding ships, triggering "target lost" alarms precisely when collision risks peak in heavy seas.

> **Rule of thumb.** Antenna gain limits by vessel platform.
> - **Sailing craft and dynamic vessels (< 20 m):** Use unity-gain half-wave dipoles ($\le 3\text{ dBi}$). The broad $\pm 39^\circ$ beam maintains link margin at $30^\circ$ heel.
> - **Stable power craft and commercial tugs (20–60 m):** Use moderate-gain collinear whips ($\le 6\text{ dBi}$, HPBW $\approx \pm 15^\circ$).
> - **Deep-draft ships (> 100 m):** Roll angles rarely exceed a few degrees; 6 dBi whips are acceptable, though 3 dBi dipoles remain standard for reliability.
> - **High-gain arrays ($\ge 9\text{ dBi}$):** Restrict strictly to rigid land towers and coastal VTS bases. Never install a 9 dBi whip on a floating mast.

---

## 32.3 Tuning: 162 MHz AIS vs. 156 MHz marine voice

The maritime VHF band spans 156.025 MHz to 162.025 MHz—a fractional bandwidth of 3.8%. Standard marine VHF voice antennas are tuned for Channel 16 (156.800 MHz). AIS 1 (161.975 MHz) and AIS 2 (162.025 MHz) sit 5.2 MHz higher.

```
Marine VHF Band Impedance Characteristic
=============================================================================
VSWR
 ^
3.0|                       Standard Marine Voice Antenna
   |                           (Resonant at 156.8 MHz)
2.5|                                                    AIS 1/2 (162 MHz)
   |                                                         /
2.0|--------------------------------------------------------*--- (VSWR = 2.0:1)
   |                 Ch. 16                                /
1.5|                   \                                  /
   |       *            \                                /
1.0+-------+------------+-------------------------------+----+--------->
         156.0        156.8                           162.0 162.05   MHz
```

### 32.3.1 VSWR and mismatch loss

When feedpoint impedance $Z_L$ mismatches transmission line impedance $Z_0$ ($50\ \Omega$), reflections occur:
$$\Gamma = \frac{Z_L - Z_0}{Z_L + Z_0}, \quad \text{VSWR} = \frac{1 + |\Gamma|}{1 - |\Gamma|}$$
$$\text{Return Loss (dB)} = -20 \log_{10}|\Gamma|, \quad \text{Mismatch Loss (dB)} = -10 \log_{10}(1 - |\Gamma|^2)$$

| VSWR | Reflection Coeff. $|\Gamma|$ | Return Loss (dB) | Reflected Power (%) | Mismatch Loss (dB) |
|---|---|---|---|---|
| **1.00:1** | 0.000 | $\infty$ | 0.0% | 0.000 |
| **1.20:1** | 0.091 | 20.8 | 0.8% | 0.036 |
| **1.50:1** | 0.200 | 14.0 | 4.0% | 0.177 |
| **1.80:1** | 0.286 | 10.9 | 8.2% | 0.370 |
| **2.00:1** | 0.333 | 9.54 | 11.1% | 0.512 |
| **3.00:1** | 0.500 | 6.02 | 25.0% | 1.249 |

A typical center-fed tubular marine whip has a 2:1 VSWR bandwidth of 8 to 12 MHz. At 162.0 MHz, VSWR typically measures $1.6:1$ to $1.9:1$. A VSWR of $1.8:1$ introduces only $0.37\text{ dB}$ mismatch loss—reflecting 8.2% of incident power. On a 12.5 W Class A transmission, delivered power drops by barely 1 W, an imperceptible loss in maritime line-of-sight channels.

### 32.3.2 When dedicated 162 MHz antennas are required

Dedicated 162 MHz antennas are necessary in three specific situations:
1. **Narrowband Base-Loaded Whips:** Short helical whips (< 0.5 m) exhibit narrow bandwidth (< 3 MHz). At 162 MHz, VSWR can exceed $3.5:1$, reflecting over 30% of power.
2. **Class A Power Foldback:** Recommendation ITU-R M.1371-6 Annex 2 §A2-2.14 mandates that transponders survive open and short circuits. Internal directional couplers trigger automatic power foldback when VSWR exceeds 3:1, cutting transmit power from 12.5 W to 1 W. A poor antenna match risks triggering foldback permanently.
3. **Coastal Shore Infrastructure:** At shore stations monitoring weak signals over diffraction paths, 0.5 dB loss contracts detection coverage. Shore antennas should achieve VSWR $< 1.2:1$ across 161.975–162.025 MHz.

---

## 32.4 Active and passive VHF/AIS splitters

To avoid installing a second antenna at the masthead, small craft often share one antenna between voice VHF and AIS via an antenna **splitter**.

```
Active Transponder Splitter Architecture
=============================================================================
                      +-----------------------------------+
                      |        Active Splitter Unit       |
                      |                                   |
                      |      +---------------------+      |
To Masthead VHF       |  +-->| LNA (+12 dB Gain)   |----->+---> To AIS RX Port
Antenna (50 Ohm) ---->+--+   +---------------------+      |
                      |  |                                |
                      |  |   +---------------------+      |
                      |  +-->| High-Speed RF Relay |<-----+<--- From AIS TX (12.5W)
                      |      | (Normally to VHF)   |      |
                      |      +----------+----------+      |
                      |                 ^                 |
                      |   RF Power      |                 |
                      |   Sense Circuit |                 |
                      |                 |                 |
                      +-----------------+-----------------+
                                        ^
                                        |
To VHF Radiotelephone (25W TX / RX) ----+
```

### 32.4.1 Passive splitters

Passive splitters use hybrid transformers or resistive networks:
- Inherent **3.0 dB power division loss** plus dielectric losses ($\approx 3.5\text{ dB}$ total loss).
- Port isolation is limited to 15 to 20 dB.
- **Never use passive splitters with transponders.** A 12.5 W AIS burst (+41 dBm) leaking into an adjacent receiver port delivers over 100 mW (+20 dBm), burning out the front-end amplifier of the voice radio.

> **Definitions that bite.** Passive splitter versus active transponder splitter.
> Passive splitters are designed solely for receive-only devices. AIS transponders require an **active transponder splitter** equipped with carrier sensing, electromechanical or solid-state RF relays, and hardware transmit interlocking.

### 32.4.2 Active transponder splitters and failure modes

Active splitters incorporate RF power detectors, high-speed switching, and a low-noise amplifier (**LNA**):
1. **Voice Radio Priority:** The unpowered default state connects the antenna directly to the voice radio via spring-loaded contacts, ensuring emergency Channel 16 availability.
2. **Transmit Interlocking:** When the voice radio transmits (25 W), RF sensors switch within microseconds, grounding or isolating the AIS port. When AIS transmits (26.67 ms burst), the relay transfers antenna connection to the transponder.
3. **Receive Amplification:** An internal LNA boosts AIS signals by 10 to 12 dB to compensate for internal insertion loss.

**Critical Splitter Failure Modes:**
- **Power Failure Ghosting:** If the splitter loses DC power, it defaults to the voice radio. The AIS transponder is left open-circuited. Transmissions trigger high-VSWR alarms, shut down, and the vessel stops broadcasting AIS without warning to the bridge crew.
- **Relay Chatter and Wear:** Switching thousands of times daily pits relay contacts, causing intermittent insertion loss of 1 to 10 dB.
- **Receiver Desensitization:** Limited relay isolation (30 to 40 dB) allows 25 W voice transmissions to leak into the AIS receiver at $-5\text{ dBm}$, blinding it across surrounding slots.
- **LNA Intermodulation:** In dense ports, strong coastal transmitters drive the broadband LNA into non-linear saturation, generating third-order intermodulation products that deafen AIS reception (see [Chapter 31](ch31-noise-and-interference.md)).

IMO SN/Circ.227 mandates dedicated antennas for Class A installations. Active splitters are legally restricted to leisure and non-SOLAS voluntary craft.

---

## 32.5 Shipboard installation: IMO SN/Circ.227 and COMSAR circulars

IMO **SN/Circ.227** (2003), amended by **SN.1/Circ.245** (2004), establishes the baseline for shipboard AIS installations. In the US, 33 CFR § 164.46 mandates compliance with SN/Circ.227 or NMEA 0400.

```
Shipboard Mast Siting Geometry (SN/Circ.227 & COMSAR.1/Circ.32/Rev.3)
=============================================================================
                  (Top of Mast)
                        |
                     [ AIS ] VHF Antenna (Omnidirectional)
                        |
                        |   Vertical Separation >= 2.0 m
                        |   (Null-to-Null Alignment: Preferred)
                        |
                     [ VHF ] Voice Antenna
                        |
      ==================+=================== Cross-Tree / Yardarm
             |                         |
             |                         |
             | <--- Horizontal ------> |
             |      Separation:        |
             |      >= 5 m (COMSAR)    |
             |      >= 10 m (SN/Circ.227)
             |                         |
    [ Conductive Mast ]           [ Radar Array ]
    (Clearance >= 2 m)                 |
                                       +--- Radar Transmit Beam
                                            (Clearance >= 3 m outside beam)
```

### 32.5.1 Siting rules under SN/Circ.227

Section 2.2.1 of SN/Circ.227 mandates:
- **360° Unobstructed Horizon:** The antenna must maintain a clear view of the horizon in all directions.
- **Conductive Structure Clearance:** Maintain a **minimum of 2 meters horizontal clearance** from conductive structures (steel masts, booms, stays). Flush mounting against a mast causes 10 to 20 dB azimuthal shadowing. SN/Circ.227 notes:
  > "Digital communication is more sensitive than analogue/voice communication to interference created by reflections in obstructions like masts and booms."
- **Radar Beam Exclusion:** Mount the antenna **at least 3 meters away from and out of the transmitting beam** of radar scanners and satellite terminals to prevent front-end burnout.

### 32.5.2 Separation: the 2 m, 5 m, and 10 m rules

Mutual coupling between the 25 W voice radio and the AIS antenna causes acoustic interference in bridge speakers (a soft clicking sound every 20 seconds, per SN/Circ.227 §2.1) and desensitizes receivers:
- **Vertical Stacking (Preferred):** Mount the AIS antenna **directly above or below the primary VHF voice antenna, with zero horizontal separation and $\ge 2\text{ m}$ vertical separation**. Axial nulls provide 40 to 45 dB of isolation.

> **Definitions that bite.** Same-level separation: 5 meters or 10 meters?
> When antennas must be mounted on the same horizontal plane:
> - **IMO SN/Circ.227 §2.2.1:** Mandates at least **10 meters** separation.
> - **IMO COMSAR.1/Circ.32/Rev.3 §5.2.8 (quoted in ITU-R M.1371-6 Table 7 note):** Mandates at least **5 meters** separation.
>
> SN/Circ.227 was drafted specifically for AIS to eliminate receiver digital desensitization. Installers should enforce the strict 10 m rule of SN/Circ.227, treating 5 m as an absolute minimum compromise under COMSAR.

### 32.5.3 GNSS antenna siting

Under SN/Circ.227 §2.3:
- Unobstructed hemispherical sky view.
- At least **3 meters** from high-power radar beams, Inmarsat domes, and the AIS VHF whip.
- GNSS cables must maintain $\ge 1\text{ m}$ separation from high-power transmitter feeders, crossing at $90^\circ$. Net gain at the receiver connector must satisfy $+10\text{ to } +20\text{ dB}$.

---

## 32.6 Coaxial cable selection and feeder loss at 162 MHz

IMO SN/Circ.227 §2.2.2 establishes cable standards:
> "The cable should be kept as short as possible to minimize attenuation of the signal. Double screened coaxial cables equal or better than RG214 are recommended."
> "The outer screen of the coaxial cable should be grounded at one end (to the ship's hull)... Minimum bend radius must be at least 5 times the outside diameter of the cable."

### 32.6.1 Attenuation characteristics at 162 MHz

Common coaxial cables exhibit marked differences in loss:
- **RG-58C/U:** Low-cost, 5.0 mm diameter utility cable with solid polyethylene dielectric. Attenuation is $20.3\text{ dB}$ per 100 m ($6.2\text{ dB}$ per 100 ft).
- **RG-8X:** 6.1 mm diameter with foamed polyethylene. Attenuation is $15.4\text{ dB}$ per 100 m ($4.7\text{ dB}$ per 100 ft).
- **RG-213/U:** 10.3 mm military-spec cable. Attenuation is $9.2\text{ dB}$ per 100 m ($2.8\text{ dB}$ per 100 ft).
- **RG-214/U:** The IMO baseline. 10.8 mm cable featuring **double silver-plated copper braided shields** ($> 85\text{ dB}$ isolation). Attenuation is $9.8\text{ dB}$ per 100 m ($3.0\text{ dB}$ per 100 ft).
- **LMR-240:** 6.1 mm low-loss cable with foil and braid shields. Attenuation is $9.8\text{ dB}$ per 100 m ($3.0\text{ dB}$ per 100 ft).
- **LMR-400:** 10.3 mm ultra-low-loss cable. Attenuation is only $4.9\text{ dB}$ per 100 m ($1.5\text{ dB}$ per 100 ft).

| Cable Type | Outer Diameter (mm) | Dielectric | Shielding | Loss (dB/10 m) | Loss (dB/30 m) | Shielding (dB) |
|---|---|---|---|---|---|---|
| **RG-58C/U** | 4.95 | Solid PE | Single Braid (95%) | 2.03 | 6.09 | > 40 |
| **RG-8X** | 6.15 | Foamed PE | Single Braid (95%) | 1.54 | 4.62 | > 45 |
| **RG-213/U** | 10.29 | Solid PE | Single Braid (97%) | 0.92 | 2.76 | > 55 |
| **RG-214/U** | 10.80 | Solid PE | Double Silver Braid | 0.98 | 2.94 | > 85 |
| **LMR-240** | 6.10 | Foamed PE | Foil + Braid | 0.98 | 2.94 | > 90 |
| **LMR-400** | 10.29 | Foamed PE | Foil + Braid | 0.49 | 1.47 | > 90 |

> **Worked example.** Impact of coaxial feeder selection on delivered transmitter power.
> On a 30-meter cable run from a 12.5 W (+40.97 dBm) Class A transponder:
> 1. **RG-58C/U ($6.09\text{ dB}$ loss):**
>    $$P_{\text{ant}} = 40.97\text{ dBm} - 6.09\text{ dB} = 34.88\text{ dBm} \approx 3.08\text{ W}$$
>    Over 75% of power is lost as heat. Delivered power is barely 3 W.
> 2. **RG-214/U ($2.94\text{ dB}$ loss):**
>    $$P_{\text{ant}} = 40.97\text{ dBm} - 2.94\text{ dB} = 38.03\text{ dBm} \approx 6.35\text{ W}$$
>    Delivered power more than doubles.
> 3. **LMR-400 ($1.47\text{ dB}$ loss):**
>    $$P_{\text{ant}} = 40.97\text{ dBm} - 1.47\text{ dB} = 39.50\text{ dBm} \approx 8.91\text{ W}$$
>    Delivered power reaches nearly 9 W.
>
> On receive, a 4.62 dB reduction in link margin between RG-58 and LMR-400 contracts two-ray tracking range ($d^{-4}$, see [Chapter 27](ch27-rf-basics.md)) by roughly 23% to 30%.

---

## 32.7 Platform-specific antenna configurations

```
AIS Antenna Form Factors Across Five Domains
=============================================================================
A. Large Commercial Vessel      B. Sailing Yacht           C. Search & Rescue
   (Tanker / Bulker)               (Masthead vs Rail)         (AIS-SART / MOB)
         | radome                        |                          |
         | collinear                     | dipole/whip              | 1/4-wave helical
         | (3-6 dBi)                     | (2-3 dBi)                | (1 W e.i.r.p.)
   ======+======                   ======+======               =====+=====
   Steel Wheelhouse                Masthead (Heeled)           Lifejacket / Sea Surface

D. Shore Base Station / VTS     E. Low-Earth-Orbit Satellite
   (Coastal Tower / Lighthouse)    (600 km Altitude CubeSat)
         |                                 / \
         | Heavy-Duty Omnidirectional     /   \ Crossed Dipoles / Turnstile
         | or 5-Element Yagi             /  O  \ (Circular Polarization)
   ======+======                        +-------+
   Rigid Steel Lattice Tower            Spacecraft Body (Nadir-Facing)
```

### 32.7.1 Large commercial ships

On SOLAS ships, antennas are mounted on the main mast or monkey island, elevated $\ge 2\text{ m}$ above the deck. Encased in foam-filled fiberglass radomes (1.2 to 2.4 m), center-fed dipoles or stacked brass sleeves withstand 100 kn winds, stack gas, and heavy salt spray. Terminations use sealed N-connectors wrapped with self-amalgamating tape.

### 32.7.2 Small craft and sailing vessels

Sailing craft balance height against survivability:
- **Masthead:** Siting at 15 m extends line-of-sight horizon to $16.0\text{ km}$ ($8.6\text{ nmi}$), but requires 25 to 30 m of cable and risks total communication loss if dismasted.
- **Stern Rail:** Siting at 2.5 m contracts line-of-sight to $6.5\text{ km}$ ($3.5\text{ nmi}$), but requires < 5 m of cable and survives rig failure.
- **Recommended Practice:** Place the voice VHF radio at the masthead, and install a dedicated 2.15 dBi AIS whip on the stern arch. If dismasted, a patch lead connects the voice radio to the stern antenna.

### 32.7.3 Miniature burst devices: AIS-SART, MOB-AIS, and EPIRB-AIS

Governed by IEC 61097-14 and [Chapter 68](ch68-special-purpose-ais.md), emergency locating devices utilize compact antennas:
- **Integrated Antennas:** Flexible quarter-wave stainless whips, sprung tape blades in lifejackets, or 15 cm top-loaded helicals.
- **The Meaning of 1 W e.i.r.p.:** Recommendation ITU-R M.1371-6 Annex 8 mandates **1 W equivalent isotropically radiated power** (**e.i.r.p.**, $+30\text{ dBm}$). Because an electrically short floating antenna exhibits negative gain ($-3\text{ to } -6\text{ dBi}$), internal transmitters deliver $+33\text{ to } +36\text{ dBm}$ (2 to 4 W conducted) into the matching network to radiate 1 W e.i.r.p.
- **Horizon Limits:** Floating at 1 m height, an AIS-SART has an optical horizon of $4.1\text{ km}$. To a ship antenna at 30 m ($22.6\text{ km}$), theoretical horizon is $26.7\text{ km}$ ($14.4\text{ nmi}$). Sea clutter and swell shadowing restrict real-world detection to 2 to 5 nmi.

### 32.7.4 Coastal shore stations

Shore stations operated by coast guards or VTS networks prioritize coverage and selectivity:
- **Elevation:** Stations atop headlands (100 to 300 m) achieve radio horizons beyond 40 to 70 km (22 to 38 nmi).
- **Antenna Hardware:** High-gain 8 to 9 dBi collinear arrays on rigid towers.
- **Sectorization:** Coastal sites use 3-element or 5-element Yagi arrays pointing seaward, exploiting 20 dB front-to-back nulls to reject urban land noise.

### 32.7.5 Satellite AIS: polarization and the space environment

Receiving AIS in Low Earth Orbit (500–800 km, see [Chapter 39](ch39-satellite-ais.md)) introduces ionospheric constraints:
- **Faraday Rotation:** Terrestrial vertical signals passing through the ionosphere rotate in polarization:
  $$\Omega \propto \frac{1}{f^2} \int N_e \, \vec{B} \cdot d\vec{s}$$
  At 162 MHz, rotation can exceed $360^\circ$, causing $> 20\text{ dB}$ cross-polarization fade on linear antennas.
- **Circular Polarization:** Satellites deploy **circularly polarized antennas** (crossed dipoles, turnstiles, or quadrifilar helices), accepting arbitrary linear polarizations with a fixed 3.0 dB polarization mismatch loss.

---

## 32.8 Installation verification with a Vector Network Analyzer (VNA)

A marine installation cannot be certified simply because the transponder powers on. Full verification requires swept $S_{11}$ measurement with a **Vector Network Analyzer** (**VNA**).

```
Vector Network Analyzer (VNA) Verification Setup
=============================================================================
+---------------+
| Handheld VNA  | (Port 1 / S11)
| (NanoVNA /    +====[ Calibrated Coax Patch ]====+
|  FieldFox)    |                                 |
+---------------+                                 |
                                                  v
[ AIS Transponder ]                             [ Coaxial Feeder Cable ]
(DISCONNECTED!)                                 (Runs to masthead)
                                                  |
                                                  v
                                                [ Masthead AIS Antenna ]
                                                (Radiating into open air)
```

### 32.8.1 Step-by-step measurement procedure

1. **Disconnect the Transponder:** Disconnect the feeder cable from the transponder. **Never transmit into a VNA.**
2. **Perform SOL Calibration:** Calibrate the instrument across **150.0 MHz to 170.0 MHz** using precision Short, Open, and Load standards.
3. **Connect to Feeder:** Attach the test lead to the vessel's transmission line.
4. **Log $S_{11}$ Return Loss and VSWR:** Record return loss and VSWR at **161.975 MHz** and **162.025 MHz**.
5. **Inspect Resonance:** Identify the resonant minimum frequency. AIS-tuned whips resonate between 161 and 163 MHz; voice whips resonate near 156.8 MHz.

### 32.8.2 Diagnosing physical faults

- **The Lossy Cable Trap:** A flat 25 dB return loss across 150–170 MHz without a resonant dip indicates a waterlogged cable, where two-way loss dissipates reflections:
  $$\text{Measured RL} = \text{Antenna RL} + 2 \times \text{One-Way Cable Loss}$$
- **Pinched Cable:** Crushed coax creates periodic ripples in the return loss trace.
- **Water in Connectors:** Moisture shifts the resonant frequency downward, often dragging resonance below 150 MHz.

> **Try it.** Link budget and margin evaluation for AIS installations.
> Calculate path loss and signal margin using the repository tool `code/rf/linkbudget.py`:
> ```bash
> # Activate repository virtual environment
> . /usr/local/google/home/schwehr/sdd-books/ais/fable/.venv/bin/activate
>
> # Evaluate Class A link at 25 km (12.5 W, 2.15 dBi antennas, h1=15 m, h2=30 m)
> PYTHONPATH=. python3 -c '
> import importlib.util
> spec = importlib.util.spec_from_file_location("linkbudget", "code/rf/linkbudget.py")
> lb = importlib.util.module_from_spec(spec)
> spec.loader.exec_module(lb)
>
> res = lb.link_budget(p_tx_w=12.5, g_tx_dbi=2.15, g_rx_dbi=2.15, 
>                      d_km=25.0, h_tx_m=15.0, h_rx_m=30.0, 
>                      cable_tx_db=1.5, cable_rx_db=1.5)
> print(f"Distance: {res[\"d_km\"]} km ({res[\"d_nmi\"]:.1f} nmi)")
> print(f"Path Loss (Used): {res[\"loss_used_db\"]} dB")
> print(f"Received Power: {res[\"p_rx_dbm\"]} dBm")
> print(f"Margin vs -107 dBm: {res[\"margin_vs_-107dBm\"]} dB")
> '
> ```
> Expected output:
> ```
> Distance: 25.0 km (13.5 nmi)
> Path Loss (Used): 122.9 dB
> Received Power: -80.6 dBm
> Margin vs -107 dBm: 26.4 dB
> ```

---

## Then & now

Evolution of maritime VHF antennas, standards, and diagnostics:

- `⟨H⟩` **1930s–1940s:** Early marine VHF radios use quarter-wave copper whips and open wire dipoles, manually tuned with tapped inductors.
- `⟨H⟩` **1970s:** CCIR standardizes maritime VHF around 25 kHz channel spacing and vertical polarization in Radio Regulations Appendix 18.
- `⟨H⟩` **1980s:** Fiberglass radomes encasing brass collinear elements replace bare metallic whips on commercial ships to combat marine corrosion.
- `⟨+⟩` **1998:** IMO Resolution **MSC.74(69)** adopts the universal AIS performance standard, deferring physical-layer requirements to ITU-R (IMO 1998).
- `⟨+⟩` **2001:** IEC publishes **IEC 61993-2 (Ed. 1.0)**, codifying the 20% packet error rate receiver sensitivity test at $-107\text{ dBm}$ and requiring transponders to survive continuous antenna open and short circuits.
- `⟨+⟩` **2003:** IMO issues **SN/Circ.227**, establishing installation standards: 2 m vertical stacking, 2 m conductive clearance, and double-screened cabling (IMO 2003).
- `⟨+⟩` **2004:** IMO issues **SN.1/Circ.245**, amending SN/Circ.227 to recommend dedicated uninterruptible power supply connections (IMO 2004).
- `⟨+⟩` **2006:** IEC publishes **IEC 62287-1**, standardizing Class B CSTDMA, spurring demand for active splitters on leisure craft.
- `⟨+⟩` **2007:** IMO COMSAR issues **COMSAR.1/Circ.32/Rev.3**, introducing the 5-meter horizontal antenna separation rule quoted in ITU-R M.1371 (IMO 2007).
- `⟨+⟩` **2010:** Spaceborne AIS is validated in orbit by satellites like AISSat-1, demonstrating circular polarization overcoming ionospheric Faraday rotation.
- `⟨+⟩` **2018:** IEC publishes **IEC 61993-2 (Ed. 3.0)**, modernizing Class A testing and Bridge Alert Management interfacing (IEC 2018).
- `⟨+⟩` **2020s:** Low-cost handheld Vector Network Analyzers (NanoVNA) democratize field RF diagnostics, replacing mechanical SWR meters with swept return-loss measurements.

---

## On the wire

Physical-layer antenna characteristics directly shape bit-level performance on the VHF Data Link.

Under Recommendation ITU-R M.1371-6 Annex 2, an AIS frame spans 256 bits at 9,600 bit/s, occupying a 26.67 ms slot:
1. **Ramp-Up:** 8 bits ($0.833\text{ ms}$)
2. **Training Sequence:** 24 bits ($2.500\text{ ms}$) of alternating $0101\dots$
3. **Start Flag:** 8 bits (`0x7E`)
4. **Data Payload:** 168 bits (Messages 1–3)
5. **FCS:** 16 bits (CRC-16-CCITT)
6. **End Flag:** 8 bits (`0x7E`)
7. **Buffer:** 24 bits ($2.500\text{ ms}$)

```
Bit-Level Frame Structure and Transmission Timing
=============================================================================
Slot: 256 bits = 26.667 ms (at 9,600 bit/s)
[ Ramp ][ Training ][ Flag ][ Payload ][  FCS  ][ Flag ][  Buffer  ]
 8 bits   24 bits    8 bits   168 bits   16 bits  8 bits   24 bits
 0.83 ms  2.50 ms    0.83 ms  17.50 ms   1.67 ms  0.83 ms  2.50 ms
----+--------+----------+--------+----------+--------+--------+------------+-->
   T0       TTS        T1       T2         T3       T4       T5           TG
```

Antenna mismatch distorts the power ramp masks specified in M.1371-6 Table 6. Reflected power shifts GMSK modulator phase, causing frequency deviation during the 24-bit training sequence to exceed the $2{,}400 \pm 240\text{ Hz}$ limit. This prevents receiving transponders from locking bit synchronization before the Start Flag ($T_2$), causing silent packet drops on the link.

---

## Validation, uncertainty & data quality

Antenna degradation propagates silently into vessel tracking systems, causing data corruption and false lost-target alarms.

```
RF Physical-Layer Degradation Propagation
=============================================================================
Physical Fault:
Corroded Connectors / High VSWR / Mast Shadowing
       |
       v
RF Signal Degradation:
Mismatch Loss / Amplifier Power Foldback / Azimuth Nulls
       |
       v
VDL Link Failure:
Pre-Sync Loss / PER > 20% / Cyclic Slot Drops
       |
       v
Downstream Data Corruption:
Track Fragmentation / False "Lost Target" Alarms / VTS Display Gaps
```

### Physical-layer uncertainty sources

1. **Connector Corrosion:** Salt spray penetrates unsealed fittings, generating passive intermodulation and fluctuating series resistance.
2. **Azimuth Shadowing:** Mounting adjacent to steel masts creates 10 to 20 dB blind sectors, fragmenting kinematic tracks.
3. **Measurement Masking:** High cable loss attenuates reflected power, presenting an artificially low VSWR to test meters.

### Concrete verification procedures

During annual surveys (per IMO MSC.1/Circ.1252):
1. **Return Loss Criteria:**
   - **Pass:** $\text{RL} \ge 14\text{ dB}$ ($\text{VSWR} \le 1.50:1$) at 161.975 MHz and 162.025 MHz.
   - **Degraded:** $10\text{ dB} \le \text{RL} < 14\text{ dB}$ ($1.50:1 < \text{VSWR} \le 1.92:1$). Schedule inspection.
   - **Fail:** $\text{RL} < 10\text{ dB}$ ($\text{VSWR} > 1.92:1$). Replace antenna or cable.
2. **Cable Attenuation Test:**
   - Measure return loss with the far end terminated in a $50\ \Omega$ load ($\text{RL} > 25\text{ dB}$).
   - Disconnect the load (open circuit). Measured return loss equals twice one-way loss ($2 \times L_{\text{cable}}$). If round-trip loss exceeds 4.0 dB on runs under 30 m, replace cable.
3. **RSSI Coverage Logging:**
   - Log received signal strength over 24 hours. Azimuth notches $> 10\text{ dB}$ indicate mast blockage requiring antenna relocation.

---

## Software

Software tools for antenna modeling, physical-layer link budgeting, and VNA hardware control:

- **NEC-2 / 4NEC2**
  *Open source (GPLv2).* Method of Moments antenna simulation software. Models 3D radiation patterns and elevation beam compression over seawater.
  *Caveat:* Simulating solid bulkheads requires tedious wire-grid meshing.
- **NanoVNA-App / NanoVNA-Saver**
  *Open source (GPLv3).* Desktop software for controlling handheld NanoVNAs. Automates swept $S_{11}$ measurements and Time Domain Reflectometry (TDR) distance-to-fault analysis.
  *Caveat:* Requires disciplined Short-Open-Load calibration prior to each session.
- **openEMS**
  *Open source (GPLv3).* FDTD electromagnetic field solver for modeling mutual coupling between antennas.
  *Caveat:* High memory requirements and steep learning curve for curved geometries.
- **Ansys HFSS**
  *Commercial.* 3D full-wave electromagnetic simulator for full-ship mast placement.
  *Caveat:* Expensive proprietary licensing; requires detailed ship CAD models.
- **Times Microwave Coaxial Calculator**
  *Free but closed (Web utility).* Industry standard for calculating cable attenuation and power ratings.
  *Caveat:* Limited to proprietary manufacturer formulations.

---

## Standards & guides

- **IMO SN/Circ.227 (2003):** *Guidelines for the Installation of a Shipborne Automatic Identification System (AIS)*. Primary standard governing antenna siting, 2 m conductive clearance, 360° view, and double-screened cabling.
- **IMO SN.1/Circ.245 (2004):** *Amendments to SN/Circ.227*. Recommends uninterruptible power supply connections for shipborne AIS.
- **IMO COMSAR.1/Circ.32/Rev.3 (2007):** *Harmonization of GMDSS Requirements*. Codifies the 2 m vertical and 5 m horizontal separation rules.
- **Recommendation ITU-R M.1371-6 (2026):** *Technical Characteristics for AIS*. Governs power classes, open/short protection (§A2-2.14), burst device e.i.r.p. (Annex 8), and receiver performance.
- **ITU Radio Regulations Appendix 18 (2020):** *VHF Maritime Mobile Frequencies*. Allocates spectrum for AIS 1, AIS 2, ASM, and satellite channels.
- **IEC 61993-2:2018 (Ed. 3.0):** *Class A Shipborne Equipment*. Specifies $-107\text{ dBm}$ receiver sensitivity and open/short test procedures.
- **IEC 62287-1:2017 (Ed. 3.0):** *Class B Shipborne Equipment (CSTDMA)*. Governs voluntary craft transponder RF characteristics.
- **IEC 61097-14:2010 (Ed. 1.0):** *AIS Search and Rescue Transmitter (AIS-SART)*. Governs 1 W e.i.r.p. burst device radiated testing.
- **IALA Guideline G1050 (2005):** *Management and Monitoring of AIS Information*. Shore-side VDL monitoring and coverage auditing.
- **IALA Recommendation R0126 (Ed. 2.0, 2021):** *Use of AIS in Marine Aids to Navigation Services*. Siting on floating buoys and coverage planning.
- **Title 33 CFR § 164.46:** *USCG AIS Carriage Requirements*. Mandates installation compliance with SN/Circ.227 or NMEA 0400.

---

## Pitfalls

1. **Installing High-Gain Whips on Small Boats**
   *The mistake:* Fitting a 9 dBi whip on a sailboat or small trawler.
   *Why it happens:* Assuming higher datasheet gain always delivers greater range.
   *How to avoid:* Enforce a $\le 3\text{ dBi}$ ceiling on sailing vessels and rolling craft to maintain broad elevation beamwidth.
2. **Mounting Flush Against a Steel Mast**
   *The mistake:* Clamping a whip directly to a steel mast tube without stand-off brackets.
   *Why it happens:* Convenience and avoiding bracket fabrication.
   *How to avoid:* Maintain $\ge 2\text{ m}$ horizontal clearance from conductive structures per SN/Circ.227 §2.2.1.
3. **Placing Antennas in Radar Transmit Beams**
   *The mistake:* Mounting an AIS antenna directly in line with an X-band or S-band radar beam.
   *Why it happens:* Crowded bridge top space.
   *How to avoid:* Enforce $\ge 3\text{ m}$ separation and verify the antenna sits outside the radar's vertical beam.
4. **Using Cheap RG-58 for Long Mast Runs**
   *The mistake:* Pulling 30 m of RG-58 cable through a mast.
   *Why it happens:* Low cost and cable flexibility.
   *How to avoid:* Use double-screened RG-214 or LMR-400, keeping feeder attenuation under 1.5 to 2.0 dB.
5. **Using Passive Splitters on Transponders**
   *The mistake:* Connecting an AIS transponder to a passive resistive splitter.
   *Why it happens:* Confusing receive-only splitters with transponder splitters.
   *How to avoid:* Never use passive splitters with transponders; use dedicated antennas or certified active splitters.
6. **Ignoring Splitter Power Loss**
   *The mistake:* Connecting an active splitter to an unmonitored accessory breaker.
   *Why it happens:* The voice radio works when unpowered, masking that the transponder is disconnected.
   *How to avoid:* Power the splitter from the dedicated AIS supply so failure triggers a bridge alert.
7. **Violating Cable Bend Radius**
   *The mistake:* Kinking heavy coax around sharp bulkhead corners.
   *Why it happens:* Tight wireways.
   *How to avoid:* Maintain a bend radius $\ge 5 \times \text{OD}$ ($\ge 55\text{ mm}$ for RG-214/LMR-400).
8. **Inadequate Weatherproofing**
   *The mistake:* Sealing outdoor connectors with standard electrical tape alone.
   *Why it happens:* Underestimating moisture capillary action.
   *How to avoid:* Seal connections with vinyl tape, self-amalgamating tape, and UV-resistant sealant.
9. **The Lossy Cable Trap**
   *The mistake:* Interpreting a flat 1.05:1 VSWR on old cable as a perfect match.
   *Why it happens:* Extreme cable attenuation absorbs reflections.
   *How to avoid:* Verify round-trip loss with an open circuit before certifying antenna health.
10. **Violating Separation Rules**
    *The mistake:* Siting VHF voice and AIS antennas 2 m apart horizontally.
    *Why it happens:* Confusing vertical separation rules with horizontal rules.
    *How to avoid:* Stack vertically with $\ge 2\text{ m}$ separation; if horizontal, enforce 10 m (SN/Circ.227) or 5 m (COMSAR).

---

## Key takeaways

- **Wavelength Scale:** AIS operates at $\approx 162\text{ MHz}$ ($\lambda \approx 1.85\text{ m}$). Half-wave dipoles measure $\approx 0.90\text{ m}$; quarter-wave monopoles measure $\approx 0.46\text{ m}$.
- **Vertical Polarization:** Standardized to provide uniform $360^\circ$ azimuth radiation and optimize sea-surface propagation.
- **Gain Compromises Motion:** Antenna gain narrows vertical elevation beamwidth. High-gain whips ($\ge 6\text{–}9\text{ dBi}$) point into sky and sea when rolling; dynamic craft must use $\le 3\text{ dBi}$ dipoles.
- **Tuning Impact:** Antennas tuned for 156.8 MHz operate at 162 MHz with VSWR $< 1.9:1$ ($< 0.4\text{ dB}$ mismatch loss), which is generally acceptable; dedicated 162 MHz antennas are essential for coastal sites and preventing Class A power foldback.
- **Splitter Architecture:** Transponders require active splitters with fast RF sensing, failsafe relays, and receive LNAs. Dedicated antennas remain the most reliable choice.
- **Vertical Stacking Beats Spacing:** Vertical stacking with $\ge 2\text{ m}$ separation exploits axial nulls for $> 40\text{ dB}$ isolation. Same-level mounting requires $\ge 10\text{ m}$ (SN/Circ.227) or $\ge 5\text{ m}$ (COMSAR).
- **Radar Clearance:** Maintain $\ge 3\text{ m}$ separation from radar beams to prevent front-end burnout.
- **Feeder Selection:** RG-58 loses $> 75\%$ of power over 30 m; installations should use double-screened RG-214 or LMR-400.
- **Burst Device e.i.r.p.:** AIS-SART beacons specify 1 W e.i.r.p., requiring 2 to 4 W conducted transmitter power to overcome compact antenna inefficiencies.
- **VNA Diagnostics:** Swept $S_{11}$ measurements with a VNA identify faults that mechanical SWR meters conceal, particularly the lossy cable trap.

---

## References

- American Radio Relay League (2023). *The ARRL Antenna Book for Radio Communications*. 25th ed. Newington, CT: American Radio Relay League.
- International Association of Marine Aids to Navigation and Lighthouse Authorities (2005). *Management and Monitoring of AIS Information*. IALA Guideline G1050, Ed. 1.1. Saint-Germain-en-Laye: IALA.
- International Association of Marine Aids to Navigation and Lighthouse Authorities (2021). *The Use of the Automatic Identification System (AIS) in Marine Aids to Navigation Services*. IALA Recommendation R0126 (A-126), Ed. 2.0. Saint-Germain-en-Laye: IALA.
- International Electrotechnical Commission (2010). *Global Maritime Distress and Safety System (GMDSS) — Part 14: AIS Search and Rescue Transmitter (AIS-SART) — Operational and Performance Requirements, Methods of Testing and Required Test Results*. IEC 61097-14:2010. Geneva: IEC.
- International Electrotechnical Commission (2017). *Maritime Navigation and Radiocommunication Equipment and Systems — Class B Shipborne Equipment of the Automatic Identification System (AIS) — Part 1: Carrier-Sense Time Division Multiple Access (CSTDMA) Techniques*. IEC 62287-1:2017. Geneva: IEC.
- International Electrotechnical Commission (2018). *Maritime Navigation and Radiocommunication Equipment and Systems — Automatic Identification Systems (AIS) — Part 2: Class A Shipborne Equipment of the Universal Automatic Identification System (AIS) — Operational and Performance Requirements, Methods of Test and Required Test Results*. IEC 61993-2:2018. Geneva: IEC.
- International Maritime Organization (1998). *Recommendation on Performance Standards for a Universal Shipborne Automatic Identification System (AIS)*. Resolution MSC.74(69), Annex 3. London: IMO.
- International Maritime Organization (2003). *Guidelines for the Installation of a Shipborne Automatic Identification System (AIS)*. SN/Circ.227. London: IMO.
- International Maritime Organization (2004). *Amendments to the Guidelines for the Installation of a Shipborne Automatic Identification System (AIS) (SN/Circ.227)*. SN.1/Circ.245. London: IMO.
- International Maritime Organization (2007). *Harmonization of GMDSS Requirements for Radio Installations On Board SOLAS Ships*. COMSAR.1/Circ.32/Rev.3. London: IMO.
- International Maritime Organization (2015). *Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems (AIS)*. Resolution A.1106(29). London: IMO.
- International Telecommunication Union (2020). *Radio Regulations, Appendix 18 (Rev. WRC-19): Table of Transmitting Frequencies in the VHF Maritime Mobile Band*. Geneva: ITU.
- International Telecommunication Union (2026). *Technical Characteristics for an Automatic Identification System Using Time Division Multiple Access in the VHF Maritime Mobile Band*. Recommendation ITU-R M.1371-6. Geneva: ITU-R.
- Times Microwave Systems (2024). *Coaxial Cable Systems Engineering Handbook and Attenuation Charts*. Wallingford, CT: Times Microwave Systems.
- United States Coast Guard (2026). *Title 33, Code of Federal Regulations, Section 164.46: Automatic Identification System (AIS)*. Washington, DC: National Archives and Records Administration.
