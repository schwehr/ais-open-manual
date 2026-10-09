# Chapter 37 — Shore collection: options, siting, and places to avoid

> **Part VI — Receiving and collecting.** Siting choices determine whether a shore station provides continuous coastal surveillance or suffers from desensitization, shadow zones, and seasonal data loss.

**In this chapter.** You will learn how to design, evaluate, site, and maintain coastal Automatic Identification System (**AIS**) shore collection stations. You will survey candidate physical hosting options, comparing commercial communication towers, lighthouses, tall buildings, academic facilities, and volunteer residential setups. You will execute rigorous site surveys spanning radio horizon calculations, local radio-frequency noise audits, lightning dissipation grounding, and backup power architecture. You will evaluate high-risk electromagnetic environments, calculating receiver blocking and intermodulation distortion from collocated NOAA Weather Radio transmitters, high-power broadcast FM stations, paging transmitters, marine radar scanners, and electrical switchyards. You will examine the statutory boundary between receive-only sensor nodes and certified base stations under international and national radio regulations. You will apply terrain-diffraction and statistical propagation models—including Longley–Rice and ITU-R Recommendation P.1546—to predict genuine coverage boundaries while accounting for maritime tropospheric ducting. Finally, you will establish operational maintenance protocols to detect silent desensitization, feedline corrosion, and clock drift.

## 37.1 The role of shore collection in the AIS architecture

Terrestrial shore collection forms the backbone of coastal vessel traffic management, maritime domain awareness, and port logistics. While satellite AIS constellations provide oceanic tracking across high seas ([Chapter 39](ch39-satellite-ais.md)), satellite reception suffers from orbital revisit latencies, Doppler-induced frequency shifts, and message collisions over dense waterways ([Chapter 30](ch30-network-loading-packet-loss.md)). Shore collection stations operate continuously within line of sight, capturing high-cadence position reports (Message Types 1, 2, 3, 18) and voyage declarations (Message Types 5, 24) with millisecond-level time resolution.

Shore collection sites serve two distinct operational paradigms:
1. **Certified Base Stations:** Operated by maritime administrations, coast guards, or Vessel Traffic Services (**VTS**) authorities under IEC 62320-1 and Recommendation ITU-R M.1371-6. They participate actively in the Time Division Multiple Access (**TDMA**) frame by transmitting base station reports (Message 4), managing slot reservations (Fixed Access TDMA, or **FATDMA**), issuing channel management commands (Message 22), interrogating vessels (Message 15), and broadcasting Application-Specific Messages (**ASM**, [Chapter 23](ch23-asm-binary-payloads.md)).
2. **Passive Receive-Only Nodes:** Deployed by commercial data aggregators, scientific research institutions, port pilots, and volunteer networks. These stations lack transmit hardware and do not participate in link-layer scheduling. Their sole objective is the uncorrupted demodulation of raw VHF Data Link (**VDL**) bursts and the encapsulation of payload bits into NMEA 0183 `!AIVDM` sentences or structured JSON streams forwarded over IP networks ([Chapter 26](ch26-interfaces-and-logging.md)).

Regardless of whether a station is a government installation or an inexpensive software-defined radio (**SDR**) connected to a single-board computer, both are bound by the same physical laws of radio wave propagation, front-end dynamic range, and ambient radio-frequency (**RF**) noise. Siting is the single most critical factor determining data quality, range, and continuity.

---

## 37.2 Siting survey fundamentals

A successful shore deployment begins with a thorough site survey. Siting decisions balance elevated geometric visibility against exposure to destructive RF noise and environmental hazards.

```
       +-------------------------------------------------------+
       |                  Siting Survey Stages                 |
       +-------------------------------------------------------+
                                  |
         +------------------------+------------------------+
         |                                                 |
         v                                                 v
+------------------+                             +-------------------+
| Geometric Horizon|                             | RF Noise Survey   |
| - Antenna height |                             | - 24-hr waterfall |
| - 4/3-Earth model|                             | - P.372 baselines |
| - DEM shadowing  |                             | - Intermod audit  |
+------------------+                             +-------------------+
         |                                                 |
         +------------------------+------------------------+
                                  |
                                  v
                   +-----------------------------+
                   | Infrastructure & Hardening  |
                   | - Single-point grounding    |
                   | - Lightning dissipation     |
                   | - Battery / PoE redundancy  |
                   | - Out-of-band backhaul      |
                   +-----------------------------+
```

### 37.2.1 Radio horizon and geometric coverage

VHF signals at 161.975 MHz (**AIS 1**) and 162.025 MHz (**AIS 2**) propagate via line-of-sight space waves and ground-reflected waves. Under standard atmospheric refraction, vertical gradients in temperature, pressure, and humidity bend radio waves downward toward the Earth. This standard refraction is modeled by replacing the true Earth radius $a \approx 6{,}371\text{ km}$ with an equivalent Earth radius $k \cdot a$, where standard refraction factor $k = 4/3 \approx 1.333$.

Under the 4/3-Earth convention (Recommendation ITU-R P.526-16), distance $d_{\text{los}}$ from antenna height $h_1$ (in meters) to the horizon over smooth seawater is:
$$d_{\text{los}} = \sqrt{2 \cdot k \cdot a \cdot h_1} = \sqrt{2 \times \frac{4}{3} \times 6{,}371 \times 10^3\text{ m} \times \frac{h_1}{10^3\text{ m}}} \approx 4.12 \sqrt{h_1}\text{ km}$$

Between a shore station at height $h_1$ and a shipboard antenna at height $h_2$, maximum theoretical line-of-sight distance $d_{\text{max}}$ combines both horizons:
$$d_{\text{max}} = 4.12 \left( \sqrt{h_1} + \sqrt{h_2} \right)\text{ km}$$
In nautical miles ($1\text{ nmi} = 1.852\text{ km}$):
$$d_{\text{max}} \approx 2.22 \left( \sqrt{h_1} + \sqrt{h_2} \right)\text{ nmi}$$

Table 37.1 gives horizon distances across shore elevations assuming a commercial vessel with antenna height $h_2 = 16\text{ m}$ ($4.12 \sqrt{16} = 16.48\text{ km} \approx 8.9\text{ nmi}$) and small craft with height $h_2 = 4\text{ m}$ ($4.12 \sqrt{4} = 8.24\text{ km} \approx 4.4\text{ nmi}$).

Table 37.1: Radio horizon distances for candidate shore site elevations.

| Shore Site Location | Elevation $h_1$ (m) | Shore Horizon (km / nmi) | Ship Horizon ($h_2=16\text{ m}$) | Craft Horizon ($h_2=4\text{ m}$) |
|---|---|---|---|---|
| Sea-level Harbor Office | 5 | 9.2 km / 5.0 nmi | 25.7 km / 13.9 nmi | 17.5 km / 9.4 nmi |
| Coastal Residence Roof | 15 | 16.0 km / 8.6 nmi | 32.4 km / 17.5 nmi | 24.2 km / 13.1 nmi |
| Lighthouse Gallery | 45 | 27.6 km / 14.9 nmi | 44.1 km / 23.8 nmi | 35.9 km / 19.4 nmi |
| Commercial Telecom Mast | 100 | 41.2 km / 22.2 nmi | 57.7 km / 31.1 nmi | 49.4 km / 26.7 nmi |
| Coastal Headland Ridge | 250 | 65.1 km / 35.2 nmi | 81.6 km / 44.1 nmi | 73.4 km / 39.6 nmi |
| Mountain Clifftop Site | 600 | 100.9 km / 54.5 nmi | 117.4 km / 63.4 nmi | 109.2 km / 58.9 nmi |

Elevating the antenna extends geometric horizon. However, extreme elevation introduces two hazards:
- **Expanded RF Footprint:** A receiver at 600 m intercepts distant co-channel transmissions, terrestrial commercial land-mobile radios, and industrial EMI, elevating the noise floor.
- **Elevation Pattern Tilt and Nulls:** High-gain collinear antennas concentrate RF energy into a narrow vertical beamwidth. An omnidirectional collinear antenna with $6\text{ dBi}$ gain (vertical beamwidth $\approx 16^\circ$) on an 800 m headland shoots over close vessels. Near-shore craft fall into deep vertical pattern nulls.

### 37.2.2 RF noise surveys and site qualification

Ambient radio noise limits receiver sensitivity. Under Recommendation ITU-R P.372-18, external noise figure $F_a$ varies by over 20 dB between quiet rural shorelines and congested commercial container ports.

Before permanently mounting an antenna, conduct a quantitative RF noise survey:
1. **Calibration:** Deploy a portable spectrum analyzer or high-dynamic-range SDR attached to a calibrated half-wave dipole tuned to 162 MHz.
2. **24-Hour Waterfall Recording:** Record continuous spectra across 150–175 MHz for 24 hours to capture nighttime industrial cycles and floodlighting.
3. **Max-Hold Analysis:** Compute max-hold and average power spectral density to identify intermittent interferers within $\pm 2\text{ MHz}$ of the AIS channels.
4. **Noise Floor Assessment:** If ambient noise within 25 kHz channel bandwidth exceeds $-115\text{ dBm}$, the site will suffer desensitization. Clean rural sites exhibit noise floors near $-122\text{ dBm}$ to $-124\text{ dBm}$.

> **Try it.** Compute line-of-sight radio horizons and expected received power levels over distance using the book's RF link-budget tool (`code/rf/linkbudget.py`):
> ```bash
> . .venv/bin/activate
> python code/rf/linkbudget.py --ptx 12.5 --gtx 2.15 --grx 3.0 --htx 15.0 --hrx 45.0 --d 30
> ```
> Expected output:
> ```
> {'d_km': 30.0, 'd_nmi': 16.198704103671705, 'fspl_db': 106.2, 'two_ray_db': 122.5, 'loss_used_db': 122.5, 'p_rx_dbm': -78.9, 'margin_vs_-107dBm': 28.1, 'horizon_km': 43.6}
> ```

### 37.2.3 Physical infrastructure: power, network, access, and grounding

Remote coastal sites require robust infrastructure:
- **Electrical Power:** Commercial stations use an online double-conversion Uninterruptible Power Supply (**UPS**) backed by a diesel generator. Autonomous remote nodes require solar photovoltaic (**PV**) arrays sized for winter solstice insolation and deep-cycle lithium-iron-phosphate ($\text{LiFePO}_4$) battery banks providing five days of autonomy. Power over Ethernet (**PoE**; IEEE 802.3at/bt) delivers DC power over shielded Category 6A Ethernet directly to masthead enclosures.
- **Network Backhaul:** Stations require continuous low-latency upstream IP data paths. Deploy dual backhaul architectures: primary optical fiber or wireless Ethernet bridges supplemented by commercial cellular (4G/5G LTE) or satellite links.
- **Physical Access and Environmental Sealing:** Salt-fog exposure causes rapid galvanic corrosion. Antenna mounts, hardware, and enclosures must be constructed from marine-grade 316 stainless steel or anodized aluminum. Coaxial connectors must be sealed with self-amalgamating polyisobutylene tape overwrapped with UV-resistant electrical tape. Enclosures require NEMA 4X or IP66 ingress protection with gore-tex pressure-equalization breathers to prevent internal condensation.
- **Lightning Protection and Single-Point Grounding:** Exposed clifftop and tower antennas are prime lightning targets. All installations must follow a strict **single-point grounding** topology. Install a gas-discharge tube (**GDT**) or quarter-wave stub coaxial lightning arrestor where the feedline penetrates the equipment building or mast enclosure. Bond the arrestor casing directly to the station master ground bus using $16\text{ mm}^2$ (AWG 6) solid copper strapping, connected to low-impedance ground rods. Never create multiple unbonded ground rods; earth potential differences during a strike drive surge currents directly through receiver circuitry.

---

## 37.3 Shore hosting options

Siting options range from fortified communications installations to volunteer residential rooftops, with distinct engineering trade-offs.

```
+-------------------+--------------------+--------------------+--------------------+
| Hosting Type      | Elevation / Range  | RF Environment     | Cost & Access      |
+-------------------+--------------------+--------------------+--------------------+
| Dedicated Towers  | High (30–120 m)    | Harsh / Paging/LMR | Expensive / Escort |
| Lighthouses/ATON  | Optimal coastal    | Generally clean    | Agency permission  |
| Tall Buildings    | High (30–200 m)    | Dense urban noise  | Roof lease / HVAC  |
| Universities      | Moderate-high      | Variable / Wi-Fi   | Academic approval  |
| Volunteer Homes   | Low (5–20 m)       | Quiet or LED-noisy | Zero / Fragile     |
+-------------------+--------------------+--------------------+--------------------+
```

### 37.3.1 Dedicated communications towers

Commercial cellular and broadcast towers offer immense height ($30\text{ to } 120\text{ m}$) and structural engineering. 
- **Advantages:** Unobstructed $360^\circ$ views, professional lightning suppression, commercial UPS and generator power, and secure perimeter fencing.
- **Disadvantages:** Tower lease costs can be substantial ($500 to $2,000 per month). Rigging work requires certified tower climbers. Towers host high-power Land Mobile Radio (**LMR**), paging, and cellular base stations whose out-of-band emissions can paralyze an unprotected AIS receiver.

### 37.3.2 Lighthouses and Aids to Navigation (ATON) structures

Lighthouses and coastal ATON structures represent ideal AIS siting locations.
- **Advantages:** Positioned on exposed promontories and harbor entrances to provide maximum visibility to mariners. Surrounding RF noise is typically exceptionally clean, as lighthouses are distant from urban industrial centers.
- **Disadvantages:** Managed by maritime authorities (such as US Coast Guard or Trinity House) or historical trusts. Gaining authorization for non-governmental hardware is difficult. Offshore lighthouses require helicopter or boat access for maintenance.

### 37.3.3 Tall buildings and urban waterfront structures

In commercial ports, rooftop mounting on waterfront skyscrapers, grain elevators, or port offices is common.
- **Advantages:** Readily available grid power, interior climate-controlled equipment rooms, and existing high-speed corporate fiber backhaul.
- **Disadvantages:** Urban rooftops are severe sources of man-made noise. Variable-frequency motor drives (**VFDs**) controlling elevators, massive HVAC chillers, rooftop cellular arrays, and dirty switch-mode building power pollute the spectrum. Cable runs from rooftop masts to basement network closets can exceed 100 meters.

### 37.3.4 Academic and research institutions

Marine laboratories, oceanography departments, and coastal universities frequently host AIS collection hardware to support oceanographic research.
- **Advantages:** Free or low-cost mounting space, high-bandwidth academic networks, and a pool of skilled technical staff capable of maintaining software pipelines.
- **Disadvantages:** University IT networks enforce strict firewalls, periodic port closures, and authentication hurdles that can disrupt long-running UDP or TCP sockets. Campus construction can lead to unannounced outages.

### 37.3.5 Volunteer and crowd-sourced residential setups

Crowd-sourced networks (MarineTraffic, AISHub, VesselFinder) rely extensively on residential hosts living along shorelines.
- **Advantages:** Geographic scaling at zero capital infrastructure cost to network operators. Thousands of coastal enthusiasts deploy low-cost SDRs or dedicated receivers in attics and on chimneys.
- **Disadvantages:** Uncontrolled quality of service. Volunteer stations suffer from residential Wi-Fi drops, accidental power disconnections, uncalibrated antenna installations, and unshielded consumer electronics. Replacing a domestic halogen bulb with a cheap LED fixture can instantly degrade a station's reception radius without the host realizing the cause.

---

## 37.4 Places to avoid: the high-risk RF landscape

An AIS receiver has a nominal input sensitivity of $-107\text{ dBm}$ (ITU-R M.1371-6). A receiver input power level of just $-20\text{ dBm}$ represents an interfering signal roughly 87 dB above sensitivity. High-power coastal RF installations generate field strengths capable of overloading low-noise amplifiers (**LNAs**), driving mixers into saturation, and generating destructive intermodulation products.

```
150 MHz         156.8 MHz        161.975  162.025   162.400 - 162.550 MHz      174 MHz
   |                |               |        |                 |                  |
[ Paging / LMR ] [ VHF Ch 16 ]  [ AIS 1 ] [ AIS 2 ]    [ NOAA Weather Radio ] [ Public Safety ]
   |                |               |        |                 |                  |
   +----------------+---------------+--------+-----------------+------------------+
                     <--- 50 kHz --->|
                                     |<-- 375 kHz --->|
```

### 37.4.1 NOAA Weather Radio (NWR) transmitters

In the United States, NOAA operates the NOAA Weather Radio All Hazards network across seven VHF frequencies:
$$\{162.400,\ 162.425,\ 162.450,\ 162.475,\ 162.500,\ 162.525,\ 162.550\}\text{ MHz}$$
These continuous FM transmitters broadcast at effective radiated powers (**ERP**) up to 1,000 W ($+60\text{ dBm}$).

The lowest NWR channel (162.400 MHz) is separated from **AIS 2** (162.025 MHz) by a mere **375 kHz**. While 375 kHz is comfortably outside the standard $\pm 25\text{ kHz}$ adjacent-channel selectivity mask, it lies squarely within the receiver's front-end preselection passband and within the $< 5\text{ MHz}$ blocking band defined by IEC 62320-1 and ITU-R M.1371-6 Annex 6.

> **Worked example.** Consider an AIS receiver deployed on a tower 1.0 km away from a 1,000 W (+60 dBm) NOAA Weather Radio transmitter operating on 162.400 MHz. Assume the NWR antenna has an omnidirectional gain of $+5\text{ dBi}$, and the AIS collection antenna has a gain of $+3\text{ dBi}$ with $1.5\text{ dB}$ of feedline loss.
>
> 1. Calculate the Free Space Path Loss (**FSPL**) at 162 MHz over distance $d = 1.0\text{ km}$:
>    $$\text{FSPL} = 32.44 + 20 \log_{10}(f_{\text{MHz}}) + 20 \log_{10}(d_{\text{km}}) = 32.44 + 20 \log_{10}(162) + 20 \log_{10}(1) \approx 76.6\text{ dB}$$
> 2. Determine the interfering power $P_{\text{rx, NWR}}$ incident at the AIS receiver front end:
>    $$P_{\text{rx, NWR}} = P_{\text{tx}} + G_{\text{tx}} - \text{FSPL} + G_{\text{rx}} - L_{\text{cable}} = +60\text{ dBm} + 5\text{ dBi} - 76.6\text{ dB} + 3\text{ dBi} - 1.5\text{ dB} \approx -10.1\text{ dBm}$$
> 3. Compare with ITU-R M.1371-6 Class A receiver blocking limits ($-23\text{ dBm}$ to $-15\text{ dBm}$):
>    The incoming $-10.1\text{ dBm}$ carrier exceeds the receiver's blocking threshold by 5 to 13 dB. An unfiltered SDR or wideband receiver will suffer total front-end gain compression, driving the noise floor up across the entire 162 MHz band and blinding the station to all but the closest vessels. At 10 km, the received level drops by $20\text{ dB}$ to $-30.1\text{ dBm}$, which a high-tier receiver can tolerate without desensitization.

### 37.4.2 High-power FM broadcast transmitters (88–108 MHz)

Commercial FM broadcast stations radiate tens or hundreds of kilowatts of effective radiated power. Although situated 54 to 74 MHz below AIS, strong FM signals present severe hazards to SDR-based collection stations (such as RTL-SDR dongles) that lack tuned front-end preselectors:
- **Wideband LNA Overload:** Cheap SDR front ends utilize wideband silicon tuners (e.g., Rafael Micro R820T2) with internal automatic gain control (**AGC**). Massive FM carriers drive the LNA into hard saturation, dropping the digital gain and suppressing weak 162 MHz AIS pulses.
- **Second- and Third-Order Intermodulation:** Two strong FM broadcast carriers $f_1$ and $f_2$ mix across non-linear amplifier stages. Third-order intermodulation products of the form $2f_1 - f_2$ or second-order harmonics fall directly into the maritime VHF band, creating phantom carriers and elevated noise floors.

### 37.4.3 Paging and land-mobile radio (LMR) networks (150–174 MHz)

Commercial VHF paging transmitters operate between 152 MHz and 159 MHz, transmitting high-power bursts (500 W or more). Because paging transmits intermittently, interference manifests as periodic packet loss. RTCM standard 11701.0 explicitly addresses this, establishing VHF immunity requirements for intense paging environments. Siting an AIS receiver near a paging antenna without cavity filtering causes intermittent desensitization whenever a page is keyed.

### 37.4.4 Marine and air traffic control (ATC) radar installations

Coastal radar installations operate at S-band (2.9–3.1 GHz), X-band (9.3–9.5 GHz), or L-band (1.2–1.4 GHz) with peak powers from 25 kW to megawatts.
- **Main-Beam Sweeps:** Although radar carrier frequencies are gigahertz away from VHF, a high-gain radar antenna rotating at 20 to 60 RPM sweeps its main beam directly across nearby shore towers. Peak RF electric fields within the radar's near field induce hundreds of millivolts into VHF antenna elements, causing periodic front-end clipping.
- **Power Supply and Modulator Spurious Noise:** High-power radar modulators and switching power supplies generate broadband impulse hash that couples into VHF feeders if physical separation is insufficient. Siting an AIS antenna directly inside the vertical sweep cone of a harbor surveillance radar must be avoided; maintain a minimum vertical separation of at least 3 meters above or below the radar turning gear.

### 37.4.5 High-voltage electrical substations and switchyards

Electrical substations, high-voltage lines (115–500 kV), and switchyards generate severe **corona discharge** and gap arcing in humid coastal air. Corona arcing creates broadband EMI from VLF to 300 MHz. Siting an AIS station adjacent to a high-voltage substation guarantees an elevated impulsive noise floor that degrades receiver sensitivity by 10 to 20 dB.

> **Rule of thumb.** Maintain strict physical and spectral separation buffers when planning shore installations:
> - **NOAA Weather Radio (NWR):** Maintain at least 5 km physical distance from a 1 kW NWR transmitter, or insert a minimum $30\text{ dB}$ notch cavity filter tuned to the specific NWR frequency.
> - **FM Broadcast:** Install a high-attenuation ($> 40\text{ dB}$) FM band-stop filter ahead of any active LNA or SDR receiver at all urban or elevated sites.
> - **Collocated Marine VHF Transmitters:** Maintain a minimum of 2.0 m vertical separation or 5.0 m horizontal separation from any 25 W marine voice VHF antenna to prevent desensitization during bridge voice calls.
> - **Radar Antennas:** Ensure the AIS antenna is mounted outside the $\pm 10^\circ$ vertical beamwidth of high-power marine radar scanners.

---

## 37.5 Licensing: receive-only vs. certified base stations

The regulatory framework governing a shore collection station depends entirely on whether the station incorporates transmit functionality.

> **Legal note.** Radio frequency transmission in the maritime mobile band is strictly regulated by international treaties and domestic communications law.
> - **Receive-Only Stations:** In the United States (under FCC Title 47 CFR Part 80) and throughout most international jurisdictions (aligned with ITU Radio Regulations), operating a passive, receive-only AIS listening post requires no radio station license. Any individual or organization is legally permitted to monitor public VHF maritime mobile channels, capture AIVDM sentences, and process tracking data, provided the station complies with local electromagnetic compatibility regulations and municipal building codes for antenna mast structures.
> - **Transmitting Base Stations:** Deploying an AIS Base Station that transmits—whether sending Message 4 time synchronizations, Message 22 channel management commands, Message 16 slot assignments, or Message 8 binary broadcasts—is strictly prohibited without formal administrative licensing, frequency coordination, and station type-approval under **IEC 62320-1**. In the United States, maritime base station authorizations are granted exclusively to approved public safety authorities, port operators, or licensed commercial coastal stations under 47 CFR Part 80 Subpart J. Unlicensed transmissions on 161.975 MHz or 162.025 MHz constitute federal violations carrying severe civil penalties, equipment forfeiture, and criminal liability.

Table 37.2 summarizes regulatory and technical distinctions between station classes.

Table 37.2: Regulatory, operational, and equipment requirements by station role.

| Characteristic | Passive Receive-Only Node | Certified AIS Base Station |
|---|---|---|
| Governing Standard | None (voluntary best practice) | IEC 62320-1, ITU-R M.1371-6, IALA R0124 |
| Radio Licensing | Unlicensed (reception is open) | Statutory coastal station license (FCC Part 80, Ofcom, etc.) |
| Hardware Cost | $50 to $1,500 | $15,000 to $60,000+ |
| VDL Transmission | None (forbidden) | FATDMA, RATDMA, Msgs 4, 15, 16, 17, 20, 22, 23 |
| Time Synchronization | NTP / System Clock (adequate) | Redundant GNSS 1PPS ($\pm 1\ \mu\text{s}$ strict UTC alignment) |
| Slot Management | None | Mandatory FATDMA cell planning and slot allocation |
| Reporting / Telemetry | Optional UDP/TCP forwarding | IEC 61162-1/2, SNMP, IALA inter-base station link |

---

## 37.6 Coverage prediction before installation

Deploying coastal infrastructure without prior computational propagation modeling frequently results in wasted capital expenditure, unexpected terrain shadowing, and unmonitored dead zones.

### 37.6.1 Terrain-diffraction models: ITM (Longley–Rice)

The **Irregular Terrain Model** (**ITM**), developed by the Institute for Telecommunication Sciences and documented by Hufford, Longley, and Kissick (1982), is the most widely deployed computational engine for point-to-point and area-coverage RF prediction. Operating from 20 MHz to 20 GHz, ITM ingests Digital Elevation Models (**DEMs**, such as 1-arc-second SRTM or USGS 3DEP data) to construct precise topographical elevation profiles between transmitter and receiver.

ITM models three primary propagation regimes:
1. **Line-of-Sight:** Computes free-space attenuation combined with specular ground reflection over knife-edge horizons.
2. **Diffraction:** Computes rounded-obstacle and double knife-edge diffraction loss using Fresnel-Kirchhoff diffraction theory when terrain breaches the first Fresnel zone.
3. **Forward Troposcatter:** Predicts weak signals scattered by atmospheric turbulence far beyond the radio horizon.

Open-source implementations of ITM—including **SPLAT!** (by John A. Magliacane) and **Signal Server** (Cloud-RF)—allow network planners to generate detailed coastal coverage heat maps. By specifying transmitter parameters (vessel mast height $15\text{ m}$, ERP $12.5\text{ W}$) and receiver parameters (shore antenna height, feeder loss, and target receiver threshold of $-107\text{ dBm}$), planners can map terrain shadowing caused by coastal islands, headlands, and fjord topography.

```
       +-------------------------------------------------------------+
       |               VHF Maritime Propagation Regimes              |
       +-------------------------------------------------------------+
       |                                                             |
Power  |  Line-of-Sight           Diffraction           Troposcatter |
(dBm)  |  (Two-Ray: 40 dB/dec)    (P.526 Knife-edge)    / Ducting    |
 -40   |  *--                                                        |
 -60   |     \                                                       |
 -80   |      \                                                      |
-100   |       \__                                                   |
-107   | - - - - -\ - - - - - - - - - - - - - - - - - - - - - - - -  | Receiver Sensitivity
-120   |           \_______                                          |
-140   |                   \---------------------------------------  |
       +-------------------------------------------------------------+
       0                Radio Horizon (4.12 \sqrt{h})              Distance (km)
```

### 37.6.2 Statistical empirical models: ITU-R Recommendation P.1546

While ITM excels at calculating dry-land diffraction over rugged mountain terrain, it exhibits structural limitations over water. Seawater is an almost perfect conducting reflector at 162 MHz ($\epsilon_r \approx 80$, $\sigma \approx 5\text{ S/m}$), producing two-ray phase cancellation within line of sight.

For coastal coverage planning, maritime administrations rely on **Recommendation ITU-R P.1546-6** (*Method for point-to-area predictions for terrestrial services in the frequency range 30 MHz to 4 000 MHz*). P.1546 is an empirical, curve-based statistical model derived from thousands of hours of experimental radio measurements over land, cold seas, and warm seas.

P.1546 provides field-strength curves parameterized by:
- Nominal transmission distance ($1\text{ to } 1{,}000\text{ km}$).
- Effective transmitting and receiving antenna heights.
- **Time Percentages (50%, 10%, 1%):** The 50% time curve defines median day-to-day operational coverage. The 10% and 1% curves model enhanced propagation conditions driven by atmospheric stability and temperature inversions, allowing engineers to predict when distant coastal stations will inject interfering signals into local cells.

### 37.6.3 The reality of maritime tropospheric ducting

Standard coverage prediction software assumes a standard, well-mixed atmosphere ($k = 4/3$). In actual coastal environments, this assumption is routinely violated.

Over seawater, temperature inversions and strong vertical humidity gradients create **tropospheric ducts**—thin atmospheric layers where the vertical refractivity gradient $dN/dh$ drops below $-157\text{ N-units/km}$ (Recommendation ITU-R P.453-14). When modified refractivity $M$ decreases with altitude ($dM/dh < 0$), VHF radio energy is trapped between the atmospheric boundary and the sea surface, propagating with minimal cylindrical attenuation.

Rautiainen et al. (2026) conducted an exhaustive, year-long experimental AIS propagation study from the Baltic island of Utö, comparing received signals from antennas at 7 m and 30 m against continuous meteorological tower refractivity profiles:
- Under standard atmospheric conditions, reliable AIS detection range was constrained strictly to the geometric radio horizon ($< 100\text{ km}$).
- During tropospheric ducting events, the shore stations routinely decoded continuous, high-volume AIS messages from commercial vessels over **600 km away**.
- Over-the-horizon anomalous reception occurred **34% of the entire year** at the 7 m antenna and **59% of the year** at the 30 m antenna.
- When elevated surface ducts reached heights of 59 m, over-the-horizon reception probability exceeded **90%**.

Computational models like ITM predict *minimum baseline geometric coverage*. They do not model tropospheric ducting. An engineer who designs a coastal network assuming a strict 30-nmi cutoff will find their database flooded with distant vessel reports during spring and summer ducting episodes, requiring algorithmic filtering in downstream analytics pipelines ([Chapter 48](ch48-spatial-statistics.md)).

---

## 37.7 Shore station hardware, filtering, and assembly

Translating site designs into physical stations requires high-quality RF plumbing.

```
+-----------+       +-------------------+       +-------------------+
|  Antenna  | ----> | Coaxial Lightning | ----> | High-Q Bandpass / |
| (Collinear|       |   Arrestor (GDT)  |       | Cavity Preselector|
|  or Dipole)       +-------------------+       +-------------------+
+-----------+                 |                           |
                              v                           v
                        Master Ground              +--------------+
                             Bus                   | Low-Noise    |
                                                   | Amp (LNA)    |
                                                   +--------------+
                                                          |
                                                          v
                                                   +--------------+
                                                   | AIS Receiver |
                                                   | (SDR / OEM)  |
                                                   +--------------+
```

### 37.7.1 Antenna selection and polar radiation patterns

Shore collection stations typically utilize one of two antenna topologies:
- **Omnidirectional Collinear Arrays (3 to 6 dBi gain):** Stacked, phased half-wave dipoles encased in a fiberglass radome. The vertical pattern is compressed toward the horizon, providing increased gain for distant vessels. Recommended for low- to moderate-elevation sites ($10\text{ to } 80\text{ m}$).
- **Half-Wave Center-Fed Dipoles (2.15 dBi gain):** Broad vertical half-power beamwidth ($\approx 78^\circ$). Indispensable for high-altitude clifftop installations ($> 200\text{ m}$) where narrow-beam collinear antennas overshoot close-in coastal traffic.

### 37.7.2 Coaxial transmission lines and feedline losses

At 162 MHz, signal attenuation across long coaxial cable runs directly degrades link margin. Table 37.3 illustrates attenuation of standard $50\ \Omega$ coaxial cables at 162 MHz over a 30-meter (100-foot) run.

Table 37.3: Coaxial feedline attenuation at 162 MHz (30-meter / 100-foot run).

| Cable Type | Outer Diameter (mm) | Attenuation at 162 MHz (dB / 30 m) | Relative Signal Power Retained (%) | Suitability |
|---|---|---|---|---|
| RG-58A/U | 4.95 | 5.8 dB | 26.3% | Unacceptable (patch leads only) |
| RG-213 / RG-8U | 10.3 | 2.9 dB | 51.3% | Marginal for short runs |
| LMR-400 | 10.3 | 1.5 dB | 70.8% | Standard for short/medium shore masts |
| 1/2" Cellflex / Heliax | 15.8 | 0.8 dB | 83.2% | Professional standard for tower runs |
| 7/8" Cellflex / Heliax | 27.8 | 0.4 dB | 91.2% | Long commercial tower runs (> 50 m) |

Using cheap RG-58 cable across a 30-meter mast drop discards nearly 74% of collected RF energy. Professional installations mandate double-shielded foam dielectric lines (such as Times Microwave LMR-400) or solid corrugated copper heliax cables.

### 37.7.3 Filtering and preselection

In any environment containing collocated transmitters, an external **bandpass filter** is mandatory.
- **Helical Bandpass Filters:** Multi-pole LC filters offering low insertion loss ($< 1.5\text{ dB}$) across 161–163 MHz and $30\text{ to } 40\text{ dB}$ attenuation across the FM broadcast band. Adequate for moderate residential and light commercial sites.
- **Resonant Helical Cavity Preselectors:** Silver-plated copper cavity resonators providing steep Chebyshev or elliptic bandpass characteristics. A professional 162 MHz bandpass cavity provides $> 35\text{ dB}$ of rejection at $\pm 1\text{ MHz}$ and $> 80\text{ dB}$ across the FM band, with in-band insertion loss under $0.8\text{ dB}$.
- **Notch (Band-Stop) Cavities:** Where a specific transmitter dominates (such as local NOAA Weather Radio at 162.400 MHz), install a high-Q notch cavity providing $30\text{ to } 45\text{ dB}$ attenuation while passing AIS 1 and AIS 2 virtually untouched.

### 37.7.4 Low-Noise Amplifiers (LNA) and masthead placement

Friis' formula for noise factor demonstrates that the total noise figure $F_{\text{sys}}$ of a cascaded receiving system is dominated by the first amplifier stage:
$$F_{\text{sys}} = F_1 + \frac{F_2 - 1}{G_1} + \frac{F_3 - 1}{G_1 G_2} + \dots$$
where $F_n$ and $G_n$ are the noise factor and linear gain of the $n$-th stage.

If a high-gain ($20\text{ dB}$), low-noise ($NF \approx 0.8\text{ dB}$) preamplifier is placed *after* a long coaxial run (where cable loss $L = 4\text{ dB}$), cable loss directly degrades system noise figure: $F_{\text{sys}} \approx L + F_{\text{LNA}} = 4.8\text{ dB}$.

If the LNA is mounted at the **masthead** immediately adjacent to the antenna (preceded only by lightning arrestor and preselection filter), it amplifies weak signals before feedline attenuation occurs:
$$F_{\text{sys}} \approx F_{\text{LNA}} + \frac{L - 1}{G_{\text{LNA}}} \approx 0.8\text{ dB} + \frac{2.51 - 1}{100} \approx 0.82\text{ dB}$$
Masthead preamplification completely overcomes downstream feedline loss. However, an unshielded masthead LNA deployed without an adequate preselection cavity will amplify out-of-band broadcast signals, driving both the LNA and downstream receiver into saturation.

---

## 37.8 Operational maintenance and remote health monitoring

Coastal collection stations are unattended sensors. Degradation is rarely binary; stations suffer silent failures that slowly corrupt data feeds without total link loss.

### 37.8.1 Automated health telemetry and watchdog pipelines

Robust stations implement automated monitoring pipelines tracking internal and RF health metrics:
1. **Hourly Message Counts:** Compute sliding-window statistics of total received packets, unique MMSIs, and message type distributions. A sudden drop in hourly message volume without corresponding changes in port traffic indicates local RF desensitization or feedline failure.
2. **Maximum Received Distance:** Track the 95th-percentile reception distance of Class A position reports hourly. If the station's maximum range collapses from 25 nmi down to 7 nmi, the front end has lost sensitivity.
3. **Internal Noise Floor and RSSI Telemetry:** Modern decoders (such as `AIS-catcher` using `-M D`) report estimated signal power in dBm and background noise levels for every decoded packet. Plotting background noise floors over time immediately reveals new localized interference sources.
4. **Hardware Health:** Monitor internal enclosure temperature, DC power supply voltages, PoE draw, and GNSS receiver carrier-to-noise ratios ($C/N_0$).

### 37.8.2 Physical inspection and preventative maintenance

Conduct biannual on-site physical audits:
- **VSWR Sweeps:** Connect a calibrated Vector Network Analyzer (**VNA**) at the equipment enclosure end of the main feedline. Sweep return loss across 150–170 MHz. An undamaged antenna and feedline system should exhibit return loss $> 15\text{ dB}$ ($\text{VSWR} < 1.43:1$) at 162 MHz. Return loss degrading below $10\text{ dB}$ ($\text{VSWR} > 1.92:1$) indicates moisture ingress into connectors, jacket cracking, or internal antenna corrosion.
- **Weatherproofing Audit:** Inspect polyisobutylene wrapping on outdoor N-type connectors. Sun exposure degrades inferior electrical tapes, allowing moisture to wick into the copper braid.
- **Grounding and Dissipation Audit:** Inspect copper ground bus strapping for galvanic oxidation. Measure earth ground resistance using a fall-of-potential ground resistance meter, ensuring ground impedance remains below $5\ \Omega$.

---

## Then & now

- **Early 2000s:** Initial shore collection relied on repurposed maritime voice VHF whip antennas mounted on harbor master roofs, feeding primitive single-channel scanning receivers or prototype base stations via long runs of lossy RG-58 cable ⟨H⟩.
- **Mid-2000s:** National coast guards chartered formal coastal collection architectures (e.g., USCG Nationwide Automatic Identification System Increment 1 achieving initial operational capability at 58 major ports in 2010), deploying dedicated dual-channel commercial base stations and tall telecommunications towers ⟨H⟩.
- **2010s:** The rise of crowd-sourced vessel tracking aggregators (MarineTraffic, AISHub) stimulated global volunteer deployments using modified USB TV dongles (RTL-SDR) running early open-source decoders (`rtl_ais`, `gnuais`), often severely impaired by urban FM broadcast interference and poor dynamic range ⟨+⟩.
- **2020s:** Modern shore collection utilizes multi-tier architectures: government VTS networks deploy type-approved IEC 62320-1 base stations with high-Q cavity filtering, while research and commercial aggregator networks deploy high-performance multi-model C++ SDR demodulators (`AIS-catcher`) and dedicated silicon receivers (e.g., Wegmatt dAISy-catcher) with integrated TCP/IP forwarders, JSON telemetry, and real-time noise-floor diagnostics ⟨+⟩.

---

## Validation, uncertainty & data quality

Errors in shore-collected AIS data originate from physical RF propagation impairments, front-end non-linearities, and spatial geometry. Understanding these uncertainties is essential for validating coastal tracking data.

```
       +-------------------------------------------------------+
       |             Sources of Shore Data Errors              |
       +-------------------------------------------------------+
                                  |
         +------------------------+------------------------+
         |                                                 |
         v                                                 v
+------------------+                             +-------------------+
| RF Degradation   |                             | Data Extraction   |
| - Feeder loss    |                             | - CRC validation  |
| - Front-end desens                             | - Timestamp skew  |
| - Intermodulation|                             | - Duplicate frames|
| - Tropospheric   |                             | - False spoofing  |
|   ducting        |                             |   anomalies       |
+------------------+                             +-------------------+
```

### Procedures for quantifying shore station reception quality

1. **Packet Error Ratio (PER) Evaluation:**
   Type-approved Class A transponders broadcast position reports at regular, deterministic intervals governed by vessel speed and rate of turn (e.g., every 10 seconds for a vessel underway at 14 knots; ITU-R M.1371-6). By isolating a single vessel transiting in clear line of sight, the receiver operator measures received packet count $N_{\text{rx}}$ against expected transmitted count $N_{\text{tx}}$ over observation window $\Delta t$:
   $$\text{PER} = 1 - \frac{N_{\text{rx}}}{N_{\text{tx}}}$$
   For a healthy shore station within its nominal radio horizon, $\text{PER}$ should remain below $5\%$. A $\text{PER} > 20\%$ inside the geometric horizon signifies severe local desensitization or slot collisions.

2. **Validating 16-Bit Frame Check Sequences (FCS):**
   Every AIS burst incorporates a standard 16-bit Cyclic Redundancy Check (**CRC**) computed across payload bits using the CCITT polynomial:
   $$G(x) = x^{16} + x^{12} + x^5 + 1$$
   Hardware and software decoders must discard any burst failing CRC validation. Software decoders must never emit unverified candidate sentences into production logging pipelines, as bit flips in unvalidated packets generate corrupted MMSIs, wild position outliers, and erratic speeds over ground.

3. **Time-Tagging Precision and Network Latency:**
   Shore receivers must inject high-precision UTC timestamps into ingested sentences using NMEA 0183 TAG blocks (`\c:1712345678*hh\!AIVDM...`) immediately upon demodulation. If the host computer relies on un-synchronized system clocks or experiences high network buffer jitter ($> 500\text{ ms}$), downstream multi-station multilateration and Time Difference of Arrival (**TDOA**) geolocation algorithms ([Chapter 35](ch35-direction-finding-geolocation.md)) will fail. Stations must discipline system clocks via Network Time Protocol (**NTP**) synchronized to local Stratum-1 servers, maintaining clock uncertainty below $\pm 10\text{ ms}$.

4. **Worked Uncertainty Audit: Feeder Loss and Receiver Sensitivity:**
   Consider a shore station where an uninspected 30-meter coax run suffers water ingress, increasing feedline attenuation from $1.5\text{ dB}$ to $7.5\text{ dB}$ (a $6.0\text{ dB}$ penalty).
   - In a line-of-sight maritime environment governed by the two-ray ground reflection model, path loss rolls off at $40\text{ dB}$ per decade of distance ($P_{\text{rx}} \propto d^{-4}$).
   - A $6.0\text{ dB}$ loss in link margin reduces effective detection distance $d$ by:
     $$\Delta \log_{10}(d) = \frac{-6.0\text{ dB}}{40\text{ dB/decade}} = -0.15 \implies \frac{d_{\text{degraded}}}{d_{\text{nominal}}} = 10^{-0.15} \approx 0.708$$
   - The station's reliable reception radius collapses by nearly **30%**, shrinking its monitored geographical area ($\pi d^2$) by approximately **50%**.

---

## Software

- **AIS-catcher (Open Source, GPL-3.0):** High-performance C++ SDR receiver and multi-channel demodulator supporting RTL-SDR, Airspy, HackRF, and SDRplay. Features integrated web-based waterfall display, real-time RSSI and frequency-drift telemetry, and multi-destination UDP/TCP streaming. *Caveat:* Multi-model coherent decoding modes consume substantial CPU cycles when deployed on older single-board computers (such as Raspberry Pi 3).
- **SPLAT! (Open Source, GPL-2.0):** Terrestrial RF path analysis and coverage prediction application utilizing the Longley–Rice ITM model and USGS Digital Elevation Models. Generates line-of-sight and path-loss heat maps. *Caveat:* Assumes dry-land terrain diffraction; does not model maritime two-ray sea reflection or atmospheric ducting.
- **Radio Mobile (Free but Closed Source, Proprietary):** RF propagation planning software developed by Roger Coudé, implementing the Longley–Rice ITM engine for point-to-point and area coverage maps. *Caveat:* Windows-native legacy desktop interface; freeware license permits non-commercial and amateur use only.
- **Cloud-RF / Signal Server (Commercial with Open-Source Core, AGPL-3.0):** Multi-threaded radio propagation modeling engine integrating global high-resolution LIDAR and DEM datasets with an API-driven web interface. *Caveat:* Commercial cloud subscription required for high-resolution computing clusters and proprietary building clutter models.

---

## Standards & guides

- **IALA Recommendation R0124 (formerly A-124), Edition 2.2 (2012):** *The AIS Service.* Saint-Germain-en-Laye: IALA. Governs shore-based AIS network architectures, coverage planning (Appendix 3), base station co-location (Appendix 12), FATDMA slot management (Appendix 14), and channel management (Appendix 17).
- **IEC 62320-1:2015 (Edition 2.0):** *Maritime navigation and radiocommunication equipment and systems — Automatic identification system (AIS) — Part 1: AIS Base Stations — Minimum operational and performance requirements, methods of testing and required test results.* Geneva: IEC. Defines normative RF sensitivity, dynamic range, blocking immunity, and network interface standards for shore base stations.
- **Recommendation ITU-R M.1371-6 (2026):** *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile frequency band.* Geneva: ITU. Governs TDMA slot structure, physical modulation parameters, and receiver immunity baselines.
- **Recommendation ITU-R P.1546-6 (2019):** *Method for point-to-area predictions for terrestrial services in the frequency range 30 MHz to 4 000 MHz.* Geneva: ITU. Normative international empirical propagation curves over land, sea, and mixed paths.
- **Recommendation ITU-R P.2001-6 (2025):** *A general purpose wide-range terrestrial propagation model in the frequency range 30 MHz to 50 GHz.* Geneva: ITU. Comprehensive wide-range propagation model incorporating tropospheric ducting, refraction, and diffraction.
- **Recommendation ITU-R P.526-16 (2025):** *Propagation by diffraction.* Geneva: ITU. Mathematical foundations for spherical-earth and obstacle diffraction across radio horizons.
- **Recommendation ITU-R P.453-14 (2019):** *The radio refractive index: its formula and refractivity data.* Geneva: ITU. Governs refractivity gradients and maritime duct formation statistics.
- **Recommendation ITU-R P.372-18 (2026):** *Radio noise.* Geneva: ITU. Normative baselines for man-made, atmospheric, and galactic environmental radio noise.
- **RTCM Standard 11701.0 (1999):** *Standard for Installed Maritime VHF Radiotelephone Equipment Operating in High Level Electromagnetic Environments.* Arlington: RTCM. Testing protocols for VHF immunity against high-power paging transmitters.
- **RTCM Standard 13700.0 (2022):** *Standard for Electromagnetic Compatibility Requirements for Light Emitting Diode (LED) Devices and Other Electrical and Electronic Equipment in the Vicinity of Shipboard Antennas.* Arlington: RTCM. Stringent RF emission limits across the maritime VHF band.
- **USCG Marine Safety Alert 13-18 (2018):** *Potential Interference of VHF-FM Radio and AIS Reception from LED Lighting.* Washington, DC: USCG. Documents field evidence of receiver desensitization caused by unshielded electronics.
- **FCC Title 47 CFR Part 80 (2026):** *Stations in the Maritime Services.* Washington, DC: US Federal Communications Commission. Normative legal requirements governing maritime coastal base station licensing and operational compliance.

---

## Pitfalls

1. **Deploying high-gain collinear antennas on cliffs.** Placing a 9 dBi collinear antenna atop a 500-meter headland compresses the main beam above or beyond nearby harbor traffic. Coastal craft directly below fall into deep vertical pattern nulls. Use a half-wave dipole or a downward-tilted array at high elevations.
2. **Mounting an unshielded LNA directly before a wideband SDR.** Connecting a low-noise amplifier ahead of an RTL-SDR without a high-Q bandpass filter causes front-end saturation from local FM broadcast, cellular, or land-mobile transmitters. The amplifier boosts out-of-band energy, blinding the receiver.
3. **Ignoring NOAA Weather Radio transmitter proximity.** Siting a station within 3 km of a 1,000 W NWR transmitter (162.400–162.550 MHz) without a tuned cavity notch filter drives the AIS receiver into severe front-end gain compression, degrading AIS 2 (162.025 MHz) sensitivity.
4. **Using lossy coaxial cable for long mast drops.** Running 30 meters of RG-58 cable between antenna and receiver introduces nearly 6 dB of attenuation at 162 MHz, wasting 75% of received RF power. Use high-grade LMR-400 or corrugated copper heliax cables.
5. **Relying on dry-land terrain models for sea prediction.** Assuming SPLAT! or ITM predicts maximum AIS range over water. ITM models terrain diffraction but ignores two-ray sea reflection and tropospheric ducting, which carries signals hundreds of kilometers beyond the horizon.
6. **Operating an unlicensed base station.** Transmitting Message 4 or slot allocations without statutory licensing and IEC 62320-1 certification violates communications law and disrupts VDL traffic.
7. **Neglecting single-point lightning grounding.** Connecting coaxial lightning arrestors to separate, unbonded ground rods creates dangerous earth potential differences during lightning strikes, shunting surge currents directly through receiver electronics.
8. **Failing to monitor noise floor telemetry.** Monitoring only packet counts without tracking average background RSSI and SNR allows silent local EMI to desensitize the station unnoticed.
9. **Inadequate outdoor connector weatherproofing.** Failing to wrap outdoor RF connectors in self-amalgamating tape allows moisture to penetrate the coaxial braid, causing chronic impedance mismatches, high VSWR, and severe signal loss.
10. **Unprotected network buffers and clock drift.** Forwarding AIVDM sentences across unreliable IP links without local timestamp tagging or NTP synchronization causes variable packet delay, corrupting downstream multi-station tracking and TDOA geolocation.

---

## Key takeaways

- **Siting dictates performance:** Antenna height governs the physical line-of-sight horizon ($d \approx 4.12 \sqrt{h}\text{ km}$), but unmanaged elevation exposes receivers to distant interference and elevation pattern nulls.
- **The RF neighborhood matters:** High-power FM broadcast stations, paging transmitters, and NOAA Weather Radio channels (375 kHz above AIS 2) can desensitize unprotected receivers without tripping hardware alarms.
- **Cavity preselection is essential:** In high-RF coastal environments, install high-Q bandpass or notch cavity filters to preserve dynamic range and prevent front-end intermodulation.
- **Receive is open, transmit is regulated:** Passive shore collection requires no radio license, but any transmitting base station mandates rigorous statutory licensing and IEC 62320-1 certification.
- **Maritime propagation is non-standard:** Coastal tropospheric ducting traps VHF signals, producing seasonal over-the-horizon reception exceeding 600 km for more than 30% of the year in regions like the Baltic and Mediterranean.
- **Feedline plumbing must be high-grade:** At 162 MHz, avoid lossy cables; deploy LMR-400 or corrugated heliax lines, weatherized with self-amalgamating tape and bonded to single-point lightning grounds.
- **Continuous telemetry prevents silent failure:** Monitor background noise floors, 95th-percentile reception range, and unique MMSI counts to catch localized EMI and hardware degradation before data loss becomes critical.

---

## References

- Hufford, G. A., Longley, A. G. & Kissick, W. A. (1982). *A Guide to the Use of the ITS Irregular Terrain Model in the Area Prediction Mode* (NTIA Report 82-100). Boulder, CO: National Telecommunications and Information Administration. doi:10.70220/zjkb4hxb
- IALA (2012). *The AIS Service* (IALA Recommendation R0124, Edition 2.2). Saint-Germain-en-Laye: International Association of Marine Aids to Navigation and Lighthouse Authorities.
- IEC (2015). *Maritime navigation and radiocommunication equipment and systems — Automatic identification system (AIS) — Part 1: AIS Base Stations — Minimum operational and performance requirements, methods of testing and required test results* (IEC Standard No. 62320-1:2015, Edition 2.0). Geneva: International Electrotechnical Commission.
- ITU-R (2019). *Method for point-to-area predictions for terrestrial services in the frequency range 30 MHz to 4 000 MHz* (Recommendation ITU-R P.1546-6). Geneva: International Telecommunication Union.
- ITU-R (2019). *The radio refractive index: its formula and refractivity data* (Recommendation ITU-R P.453-14). Geneva: International Telecommunication Union.
- ITU-R (2025). *A general purpose wide-range terrestrial propagation model in the frequency range 30 MHz to 50 GHz* (Recommendation ITU-R P.2001-6). Geneva: International Telecommunication Union.
- ITU-R (2025). *Propagation by diffraction* (Recommendation ITU-R P.526-16). Geneva: International Telecommunication Union.
- ITU-R (2026). *Radio noise* (Recommendation ITU-R P.372-18). Geneva: International Telecommunication Union.
- ITU-R (2026). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile frequency band* (Recommendation ITU-R M.1371-6). Geneva: International Telecommunication Union.
- Last, P., Hering-Bertram, C. & Linsen, C. (2015). How AIS antenna setup affects AIS signal quality. *Ocean Engineering*, 100:83–89. doi:10.1016/j.oceaneng.2015.03.017
- Rautiainen, L., Johansson, L., Lensu, M., Tyynelä, J., Jalkanen, J.-P., Hasu, V., Stenbäck, K., Lonka, H. & Laakso, A. (2026). Studying anomalous propagation over marine areas using an experimental AIS receiver set-up. *Atmospheric Measurement Techniques*, 19:2763–2785. doi:10.5194/amt-19-2763-2026
- RTCM (1999). *Standard for Installed Maritime VHF Radiotelephone Equipment Operating in High Level Electromagnetic Environments* (RTCM Standard 11701.0). Arlington, VA: Radio Technical Commission for Maritime Services.
- RTCM (2022). *Standard for Electromagnetic Compatibility Requirements for Light Emitting Diode (LED) Devices and Other Electrical and Electronic Equipment in the Vicinity of Shipboard Antennas for the Protection of Onboard Receivers* (RTCM Standard 13700.0). Arlington, VA: Radio Technical Commission for Maritime Services.
- United States Coast Guard (2018). *Potential Interference of VHF-FM Radio and AIS Reception from LED Lighting* (Marine Safety Alert 13-18). Washington, DC: USCG Office of Investigations and Casualty Analysis.
- United States Federal Communications Commission (2026). *Title 47, Part 80: Stations in the Maritime Services*. Washington, DC: Code of Federal Regulations.
- van de Ven, J. (2026). *AIS-catcher: A multi-platform AIS receiver for SDR and NMEA streams*. GitHub repository: https://github.com/jvde-github/AIS-catcher
