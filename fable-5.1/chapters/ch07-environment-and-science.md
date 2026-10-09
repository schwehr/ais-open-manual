# Chapter 7 — Environment and science: Whale Alert, ship strikes, noise, emissions, tsunamis, currents

> **Part I — Why AIS? Uses and users.** How maritime tracking signals evolved from tactical bridge collision avoidance into an observational foundation for marine conservation, acoustic monitoring, atmospheric emissions inventories, and physical oceanography.

**In this chapter.** You will learn how the Automatic Identification System (AIS) serves as an essential tool for marine conservation and ocean science. We trace endangered cetacean protection, examining acoustic buoy arrays in Boston's Traffic Separation Scheme, the Right Whale AIS Project, and mobile systems like Whale Alert and Whale Safe. You will examine ship-strike physics, hydrodynamic lethality curves, and AIS data roles in establishing Areas to Be Avoided and shifting navigation channels. We cover marine emissions modeling, walking through the Ship Traffic Emission Assessment Model (STEAM) and the Fourth IMO Greenhouse Gas Study. You will explore underwater radiated noise mapping, acoustic propagation, and voluntary slowdown initiatives in Haro Strait and California sanctuaries. Finally, we investigate how commercial vessels serve as opportunistic scientific instruments for physical oceanography, measuring open-ocean tsunami waves and surface current dynamics.

## 7.1 Marine mammals and ship strikes

The collision of commercial ships with large cetaceans—termed a **ship strike**—is a leading cause of anthropogenic mortality for endangered baleen whales (Silber et al. 2012). The North Atlantic right whale (*Eubalaena glacialis*) is critically vulnerable, with fewer than 400 individuals along North America's eastern seaboard. Because right-whale foraging grounds and migratory corridors intersect high-density shipping approaches to ports like Boston and New York, traffic overlap creates acute extinction pressure.

Before mandatory Class A transponders under [SOLAS](ch16-laws-and-treaties.md) Chapter V, vessel monitoring in whale habitats relied on sporadic aerial surveys, bridge logbooks, and visual lookouts. Universal carriage on vessels $\ge 300$ gross tonnage (**GT**) transformed marine spatial planning, enabling researchers to quantify traffic density, speed distributions, and transit patterns across critical habitat (Wiley et al. 2011).

```
+-------------------------------------------------------------------------+
|                  ENDANGERED CETACEAN PROTECTION CHAIN                   |
+-------------------------------------------------------------------------+
|  1. ACOUSTIC SENSING                                                    |
|     Auto-detection hydrophone buoys (Cornell/WHOI) detect whale calls   |
|     Acoustic pitch-tracks classified; detection confidence score > 0.8  |
+-------------------------------------------------------------------------+
                                   | Iridium / Satellite Uplink
                                   v
+-------------------------------------------------------------------------+
|  2. CENTRALIZED TELEMETRY & PROCESSING                                   |
|     Shore server correlates detections across buoy arrays                |
|     Trigger Dynamic Management Area (DMA) / Acoustic Slow Zone          |
+-------------------------------------------------------------------------+
                                   |
         +-------------------------+-------------------------+
         |                                                   |
         v (Cellular / IP)                                   v (VHF Data Link)
+----------------------------------+        +----------------------------------+
|  3a. IP / MOBILE NOTIFICATION    |        |  3b. SHORE AIS BASE TRANSMISSION |
|  - Whale Alert (iOS/Android)     |        |  - Message 8 Area Notice (FI 22) |
|  - Whale Safe Dashboard          |        |  - Broadcast over AIS 1 / AIS 2  |
|  - Real-time Slow Zone alerts    |        |  - Received by Class A / ECDIS   |
+----------------------------------+        +----------------------------------+
                                   |
                                   v
+-------------------------------------------------------------------------+
|  4. BRIDGE MITIGATION & COMPLIANCE                                      |
|     - Watch officer informed via ECDIS symbol, MKD text, or iPad app    |
|     - Vessel throttles down to <= 10.0 knots                            |
|     - Lethal collision probability reduced by up to 80-90%             |
|     - AIS kinematic reports (Msg 1-3) confirm compliance to regulators  |
+-------------------------------------------------------------------------+
```

### 7.1.1 Spatial segregation: shifting the Boston Traffic Separation Scheme

The most permanent way to prevent ship strikes is spatial segregation: separating commercial traffic from known whale concentrations. In the early 2000s, scientists at Stellwagen Bank National Marine Sanctuary (**SBNMS**), working with the National Oceanic and Atmospheric Administration (**NOAA**), the International Fund for Animal Welfare (**IFAW**), and the US Coast Guard (**USCG**), analyzed Massachusetts Bay traffic.

Pairing 25 years of whale sightings with radar and early AIS data, researchers discovered that the **Traffic Separation Scheme** (**TSS**) into Boston traversed peak whale feeding aggregations on northern Stellwagen Bank.

The United States submitted a proposal to the International Maritime Organization (**IMO**) to modify the TSS (Silber et al. 2012). Taking effect 1 July 2007:
- The northern leg of the traffic lanes was rotated approximately 12 degrees to the north into deeper water with lower whale densities.
- The modified lane narrowed the traffic corridor, concentrating vessels away from feeding hotspots.
- The shift added 3.75 nautical miles (6.95 km) to Boston transits (10 to 22 minutes of steaming time).

Retrospective analyses showed this adjustment cut right-whale strike risk in the sanctuary by 58%, and by 81% for all baleen whales combined (Wiley et al. 2011; Silber et al. 2012).

### 7.1.2 Areas to Be Avoided and Seasonal Management Areas

Where lanes cannot rotate, authorities employ seasonal and dynamic routing under IMO Resolution A.1106(29), creating **Areas to Be Avoided** (**ATBAs**) and speed restrictions.

In December 2008, NOAA enacted the Vessel Speed Rule (50 CFR 224.105; 73 FR 60173; NOAA 2008). It established mandatory **Seasonal Management Areas** (**SMAs**) along the US East Coast. In active SMAs, vessels $\ge 65\text{ ft}$ (19.8 m) length overall (**LOA**) must steam at 10.0 knots or less during defined calendar windows.

> **Definitions that bite.** "Speed Over Ground" vs. "Speed Through the Water." Under 50 CFR 224.105, compliance is judged against **Speed Over Ground** (**SOG**) from GNSS (AIS Messages 1–3). However, strike lethality depends on hydrodynamic **Speed Through the Water** (**STW**). Steaming at 9.0 kn through a 3.0 kn opposing current gives an SOG of 6.0 kn (compliant) but delivers 9.0 kn strike impact energy. Running with a 3.0 kn current at 9.0 kn STW produces 12.0 kn SOG, generating an automated AIS enforcement violation despite minimal drag. Watchstanders must manage both metrics carefully.

NOAA also established **Dynamic Management Areas** (**DMAs**) and Acoustic Slow Zones. When three or more right whales are detected, NOAA creates a temporary 15-day DMA, requesting mariners slow to 10 kn or route around. While SMAs carry mandatory civil penalties, DMAs have operated under voluntary compliance, motivating continuous AIS monitoring.

### 7.1.3 The lethality curve: why 10 knots matters

The 10-knot limit reflects a hydrodynamic threshold in blunt-force trauma and propeller-strike mechanics. Vanderlaan and Taggart (2007) analyzed strike records to derive empirical lethality as a function of speed:

$$P_{\text{lethality}}(v) = \frac{1}{1 + e^{-(\alpha + \beta v)}}$$

Logistic fits show that lethality escalates rapidly above 10 kn:
- At speeds $v \le 10\text{ kn}$, mortality probability ($P_{\text{lethality}}$) is approximately $0.20$ to $0.35$.
- At $v = 15\text{ kn}$, $P_{\text{lethality}}$ climbs to roughly $0.80$.
- At $v \ge 18\text{ kn}$, lethality approaches unity ($P_{\text{lethality}} \to 1.00$).

Vessel kinetic energy scales quadratically ($E_k = \frac{1}{2} m v^2$). Slowing a 50,000 GT ship from 20 kn to 10 kn drops impact energy by 75%, reduces suction pressure drawing whales toward propellers, and gives watchstanders and whales critical evasion time.

## 7.2 Real-time whale mitigation: acoustic buoys and Whale Alert

Because right whales shift habitats following copepod (*Calanus finmarchicus*) blooms, dynamic protection requires real-time sensing.

### 7.2.1 The Right Whale AIS Project in Massachusetts Bay

The operational pioneer was the **Right Whale AIS Project** (**RAP**) in Boston approaches (2008–2012; McGillivary, Schwehr & Fall 2009). The project was mandated by regulatory licensing of the **Northeast Gateway Deepwater Port**, an offshore liquefied natural gas (**LNG**) terminal near Stellwagen Bank.

To protect whales from LNG shuttle carriers, operator Excelerate Energy funded an acoustic network:
1. **Auto-detection buoys:** The Cornell Bioacoustics Research Program (**BRP**) and Woods Hole Oceanographic Institution (**WHOI**) moored acoustic auto-detection buoys along Boston TSS lanes.
2. **Onboard pitch-tracking:** Each buoy housed a continuous hydrophone, digital signal processor running an automated "up-call" detector, and Iridium transceiver, relaying detection packets to Cornell.
3. **AIS injection:** Telemetry was validated and relayed to a USCG shore station, which broadcasted **AIS Message 8** (Binary Broadcast Message) area notices across the maritime VHF data link (**VDL**).
4. **Bridge display:** In theory, Class A transponders received Message 8, displaying whale-warning symbols on Electronic Chart Display and Information Systems (**ECDIS**) or Minimum Keyboard and Display (**MKD**).

In practice, shore-to-ship AIS faced severe bridge display obstacles ([Chapter 23](ch23-asm-binary-payloads.md); [Chapter 43](ch43-demonstration-programs.md)). Commercial ECDIS units lacked decoders for Application-Specific Messages (**ASMs**), as IMO guidance (SN.1/Circ.289; SN.1/Circ.290) was non-mandatory. Most displays ignored Message 8 or logged raw hex strings.

### 7.2.2 Whale Alert and Whale Safe: the transition to IP delivery

Faced with bridge display limitations, the team—expanding to include NOAA, IFAW, EarthNC, and Conserve.IO—pivoted in 2012 to mobile internet, releasing the **Whale Alert** mobile app.

Whale Alert aggregated acoustic buoy detections, NOAA and Canadian aerial surveys, active SMA/DMA boundaries, and mariner sightings. Displayed over cellular or satellite IP, it provided real-time acoustic alarms on bridge tablets. Whale Alert was formally presented to the US Congress in 2012 as an operational breakthrough in mobile ocean conservation (Schwehr 2012).

In September 2020, the Benioff Ocean Initiative (UC Santa Barbara) launched **Whale Safe** in the Santa Barbara Channel and San Francisco approaches. Whale Safe combined:
1. **Acoustic hydrophones:** Continuous ocean-bottom listening for blue, fin, and humpback vocalizations.
2. **Dynamic habitat models:** Oceanographic models projecting whale presence from satellite sea-surface data.
3. **AIS fleet tracking:** Tracking commercial vessels via terrestrial AIS to publish daily corporate slow-speed compliance scorecards.

Public reporting improved commercial fleet compliance in the Santa Barbara Channel from below 30% to over 70%.

## 7.3 Quantifying underwater radiated noise

Commercial shipping has caused chronic increases in low-frequency **underwater radiated noise** (**URN**). Large commercial vessels radiate acoustic energy in the 10 Hz to 1,000 Hz band (McKenna et al. 2012), overlapping mysticete whale communication and foraging bands.

### 7.3.1 Propeller cavitation and acoustic source levels

The dominant source of shipping noise is **propeller cavitation**. As blades rotate, suction-side pressure drops below water vaporization pressure, forming vapor cavities. When cavities collapse downstream, they generate broadband shock waves and blade-rate tonals:

$$f_{\text{bpf}} = \frac{N_{\text{blades}} \times \text{RPM}}{60}$$

Above cavitation inception speed, acoustic source levels rise rapidly. Empirical measurements by McKenna et al. (2012) and Merchant et al. (2012) parameterize source levels ($SL$, dB re $1\,\mu\text{Pa}^2\,\text{m}^2\,\text{Hz}^{-1}$ at 1 m) as:

$$SL(f, v) = SL_0(f) + C_v \cdot 10 \log_{10}\left(\frac{v}{v_{\text{ref}}}\right)$$

where $SL_0(f)$ is baseline source level at $v_{\text{ref}}$, and $C_v$ ranges between 1.5 and 3.0. A container ship cruising at 22 kn exhibits source levels above $185\text{ dB re }1\,\mu\text{Pa}\text{ at }1\text{ m}$; slowing to 11 kn drops acoustic output by 5 to 10 dB—a 70% to 90% reduction in radiated acoustic energy.

### 7.3.2 Mapping ambient noise fields with AIS

To map chronic shipping noise across regional basins, researchers combine AIS feeds with parabolic equation (**PE**) sound propagation models (Erbe, MacGillivray & Williams 2012; Erbe et al. 2014):
1. **Vessel positions:** AIS Messages 1–3 give SOG ($v$) and position; Message 5 provides vessel dimensions and type.
2. **Source level assignment:** Baseline spectra $SL(f, v)$ are assigned per vessel class.
3. **Transmission loss ($TL$):** Computed across bathymetry, sediment parameters, and sound speed profiles:
   $$TL(r, z, f) = 15 \log_{10}(r) + \alpha(f) \cdot r + A_{\text{bottom}}$$
4. **Spatial superposition:** Total sound pressure level ($SPL$) is integrated across all $N$ active ships:
   $$SPL(f) = 10 \log_{10} \left( \sum_{i=1}^N 10^{\frac{SL_i(f, v_i) - TL_i}{10}} \right)$$

### 7.3.3 The ECHO Program in Haro Strait

The Vancouver Fraser Port Authority's **ECHO** Program demonstrated AIS-guided noise mitigation in Haro Strait and Boundary Pass, critical foraging waters for endangered Southern Resident Killer Whales (**SRKW**). High-frequency echolocation clicks (15–50 kHz) used to hunt Chinook salmon are masked by vessel noise.

Beginning in 2017, ECHO established voluntary commercial slowdowns to 11.5 kn for bulk carriers and 14.5 kn for container ships. Seafloor hydrophones installed by Ocean Networks Canada recorded noise levels matched to AIS tracks. With commercial participation exceeding 80%, median ambient noise dropped by 2.5 to 3.0 dB, halving acoustic power in the strait.

## 7.4 Ship emissions inventories and atmospheric modeling

Maritime transport contributes roughly 3% of global greenhouse gas (**GHG**) emissions, releasing over one billion metric tons of $\text{CO}_2\text{e}$ annually, alongside localized burdens of $\text{SO}_x$, $\text{NO}_x$, $\text{CO}$, and particulate matter ($\text{PM}_{2.5}$, black carbon) (Jalkanen et al. 2009; Faber et al. 2020).

Traditional top-down inventories relied on national bunker fuel sales from the International Energy Agency (**IEA**). These models could not locate where exhaust was released, were skewed by bunkering hubs, and ignored speed-dependent engine loads. Global AIS tracking enabled bottom-up, voyage-by-voyage modeling.

### 7.4.1 The Ship Traffic Emission Assessment Model (STEAM)

The standard for bottom-up marine emissions is **STEAM**, developed by Jalkanen et al. (2009, 2012) at the Finnish Meteorological Institute. STEAM couples AIS tracks with naval architectural registries (e.g., IHS Fairplay).

```
+-----------------------------------------------------------------------+
|                 STEAM BOTTOM-UP EMISSIONS PIPELINE                    |
+-----------------------------------------------------------------------+
|  1. AIS TELEMETRY (Messages 1, 2, 3, 5)                                |
|     Latitude, Longitude, SOG (v), Heading, Draught (T), Timestamp (t) |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|  2. NAVAL ARCHITECTURE DATABASE (IHS / S&P Fairplay)                  |
|     Match IMO number -> Length (L), Beam (B), Design Speed (v_design),|
|     Installed Power (P_MCR), Engine Stroke, Fuel Injection Type       |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|  3. HYDRODYNAMIC RESISTANCE & PROPULSION POWER                        |
|     Calculate wetted hull area, wave resistance, and total power:     |
|     P_req = P_MCR * (v / v_design)^3  (or Holtrop-Mennen resistance)  |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|  4. INSTANTANEOUS ENGINE LOAD & SFOC CORRECTION                       |
|     EL_ME = P_req / P_MCR                                             |
|     Apply non-linear Specific Fuel Oil Consumption curve SFOC(EL_ME)  |
+-----------------------------------------------------------------------+
                                   |
                                   v
+-----------------------------------------------------------------------+
|  5. EMISSION FACTOR APPLICATION (Tier I/II/III & Fuel Type)           |
|     Emission Rate E_k = P_req * SFOC(EL) * EF_k(EL)                   |
|     Integrate over voyage time step: Mass_k = E_k * dt                |
+-----------------------------------------------------------------------+
```

Instantaneous required power ($P_{\text{req}}$, kW) scales cubically with velocity:

$$P_{\text{req}} = \frac{P_{\text{MCR}}}{\eta_{\text{prop}}} \left( \frac{v}{v_{\text{design}}} \right)^3$$

where $P_{\text{MCR}}$ is Maximum Continuous Rating, $v$ is speed through water, $v_{\text{design}}$ is design speed, and $\eta_{\text{prop}}$ is propulsive efficiency ($0.65$–$0.75$). Advanced STEAM versions apply the **Holtrop–Mennen** method for draught and sea-state resistance.

The main engine load factor ($EL_{\text{ME}} = P_{\text{req}} / P_{\text{MCR}}$) governs Specific Fuel Oil Consumption ($SFOC$, $\text{g}/\text{kW}\cdot\text{h}$). Optimal thermal efficiency occurs between 70% and 85% MCR ($SFOC \approx 165\text{--}175\text{ g}/\text{kW}\cdot\text{h}$); below 20% load, $SFOC$ exceeds $220\text{ g}/\text{kW}\cdot\text{h}$.

Auxiliary engine ($P_{\text{AE}}$) and boiler ($P_{\text{boiler}}$) loads are inferred from operational modes: cruising ($v \ge 5\text{ kn}$), maneuvering ($1 \le v < 5\text{ kn}$), or hotelling ($v < 1\text{ kn}$). Segment emissions for species $k$ over $\Delta t$ are integrated as:

$$\Delta M_k = \left( P_{\text{req}} \cdot EF_{k,\text{ME}}(EL) + P_{\text{AE}} \cdot EF_{k,\text{AE}} + P_{\text{boiler}} \cdot EF_{k,\text{boiler}} \right) \cdot \Delta t$$

Emission factors follow stoichiometric fuel conversions for $\text{CO}_2$, MARPOL Annex VI limits for $\text{SO}_x$, and IMO Tiers I–III for $\text{NO}_x$.

### 7.4.2 The Fourth IMO Greenhouse Gas Study 2020

The *Fourth IMO GHG Study 2020* (Faber et al. 2020) analyzed multi-year global satellite and terrestrial AIS datasets, establishing key industry benchmarks:
- **Global shipping emissions:** Total GHG emissions increased 9.6% from 977 million metric tons of $\text{CO}_2\text{e}$ in 2012 to 1,076 million metric tons in 2018.
- **Global share:** Shipping's share of global anthropogenic GHG emissions rose from 2.76% to 2.89%.
- **Carbon intensity divergence:** International shipping carbon intensity improved by ~11% per transport work unit from operational slow steaming, but overall emissions rose due to cargo volume growth.
- **Methane slip:** AIS tracking revealed a 150% surge in unburned methane emissions (**methane slip**) from low-pressure dual-fuel LNG engines between 2012 and 2018.

## 7.5 AIS as an opportunistic oceanographic sensor

Commercial merchant vessels tracked by AIS constitute an autonomous planetary fleet of opportunistic scientific instruments.

### 7.5.1 Detecting offshore tsunamis using ship navigation records

Global tsunami warnings are constrained by sparse deep-ocean buoys; the global Deep-ocean Assessment and Reporting of Tsunamis (**DART**) network maintains fewer than 60 stations worldwide.

Daisuke Inazu and colleagues proved that offshore ships tracked by AIS record open-ocean tsunami wavefields in real time (Inazu et al. 2018). In deep water ($h > 1,000\text{ m}$), tsunamis travel at $c = \sqrt{g h} \approx 200\text{ m/s}$. Vertical displacement ($\eta$) in open water is small ($0.5$–$1.0\text{ m}$), but horizontal water particle velocity ($u_{\text{tsu}}$) penetrates the water column:

$$u_{\text{tsu}} = \eta \sqrt{\frac{g}{h}}$$

For depth $h = 200\text{ m}$ and wave height $\eta = 1.0\text{ m}$, horizontal velocity is $u_{\text{tsu}} \approx 0.22\text{ m/s} \approx 0.43\text{ kn}$, accelerating past $1.0\text{ m/s}$ in shallow bays.

A steaming vessel acts as a fluid drag body. Velocity Over Ground ($\mathbf{v}_G$, from SOG and COG) is the vector sum of water velocity and external currents:

$$\mathbf{v}_G = \mathbf{v}_W + \mathbf{u}_{\text{bg}} + \mathbf{u}_{\text{tsu}} + \mathbf{u}_{\text{wind}}$$

Because engine RPM and heading ($\psi$) remain steady on open transits, tsunami wave pulses induce sharp, coherent kinematic deflections. Analyzing coastal AIS records from the 11 March 2011 Great East Japan Earthquake ($M_w 9.1$), Inazu et al. (2018) extracted horizontal tsunami waveforms matching hydrodynamic models ($r > 0.85$), proving AIS can provide early tsunami warnings 10 to 30 minutes before coastal landfall.

### 7.5.2 Surface ocean currents and eOdyn

Traditional satellite radar altimetry samples sea-surface heights along narrow nadir tracks with 10-to-35-day repeat cycles, missing sub-mesoscale ocean eddies ($<100\text{ km}$, $<7\text{ days}$).

In 2016, French oceanographic firm **eOdyn**, founded by Yann Guichoux, introduced "Omni-Situ" surface current retrieval (Guichoux, Lennon & Thomas 2016). The framework models horizontal forces on floating hulls:

$$\mathbf{F}_{\text{total}} = \mathbf{F}_{\text{thrust}} + \mathbf{F}_{\text{hydro}} + \mathbf{F}_{\text{aero}} + \mathbf{F}_{\text{wave}} \approx 0$$

Wind drag ($\mathbf{F}_{\text{aero}}$) is calculated using weather prediction wind vectors and vessel profile geometry. Hydrodynamic hull drag ($\mathbf{F}_{\text{hydro}}$) is parameterized against dimensions and draught from Message 5. The angular difference between Heading ($\psi$) and COG ($\theta$) reveals leeway drift and current shear. Inverting thousands of merchant ship tracks resolves gridded 2D surface current fields at 0.1° and daily resolution.

### 7.5.3 Disaster response: the Deepwater Horizon oil spill

When the *Deepwater Horizon* rig exploded on 20 April 2010, emergency response required coordinating over 400 vessels around the Macondo wellhead (Schwehr & McGillivary 2007).

Kurt Schwehr developed open-source `libais` in 2010 to decode massive AIS telemetry feeds for NOAA's **Environmental Response Management Application** (**ERMA**). Ingested AIS tracks were fused with satellite radar oil boundaries, underwater glider tracks, and dispersant flight paths. AIS verified that skimmers steamed at effective recovery speeds (1 to 2 kn) and established operational exclusion zones around controlled burns.

> **Case file.** *The Macondo Response Fleet and ERMA Integration (2010).* During the 87-day *Deepwater Horizon* response, unified command tracked over 4,000 "Vessels of Opportunity" using AIS. Small fishing craft received portable Class B transponders. Real-time telemetry processed through `libais` prevented collisions within the 5-mile relief drilling exclusion zone and provided evidence for subsequent claims litigation regarding boom deployment locations.

## Then & now

- **1989** ⟨H⟩ — *Exxon Valdez* disaster leads to the US Oil Pollution Act of 1990 (OPA-90), establishing tanker tracking trials that helped shape AIS.
- **2002** ⟨+⟩ — SOLAS Chapter V Regulation 19 mandates Class A transponders on international vessels $\ge 300\text{ GT}$ (IMO 2000).
- **2007** ⟨+⟩ — On 1 July, the IMO rotates the Boston TSS by 12 degrees north, cutting right-whale collision risk by 58% (Wiley et al. 2011; Silber et al. 2012).
- **2008** ⟨+⟩ — The Right Whale AIS Project deploys acoustic auto-detection buoys in Boston TSS, broadcasting whale alerts via AIS Message 8 (McGillivary, Schwehr & Fall 2009).
- **2008** ⟨+⟩ — NOAA issues the Vessel Speed Rule (50 CFR 224.105), mandating 10.0-knot Seasonal Management Areas along the US Atlantic coast (NOAA 2008).
- **2009** ⟨+⟩ — Jalkanen et al. publish the STEAM model, establishing bottom-up emissions modeling using AIS tracks (Jalkanen et al. 2009).
- **2010** ⟨H⟩ — *Deepwater Horizon* oil spill; Kurt Schwehr creates `libais` to process response vessel telemetry for NOAA ERMA.
- **2010** ⟨+⟩ — IMO issues circular SN.1/Circ.289, establishing international Application-Specific Messages including environmental Area Notices.
- **2012** ⟨H⟩ — Whale Alert mobile app launched, delivering acoustic and regulatory whale alerts to bridge tablets over mobile IP.
- **2016** ⟨+⟩ — eOdyn proves sea-surface current vectors can be inverted from merchant vessel drift (Guichoux, Lennon & Thomas 2016).
- **2017** ⟨+⟩ — Port of Vancouver launches the ECHO Program in Haro Strait, documenting underwater noise reductions from voluntary slowdowns.
- **2018** ⟨+⟩ — Inazu et al. demonstrate that commercial vessels tracked by AIS record open-ocean tsunami wavefield currents (Inazu et al. 2018).
- **2020** ⟨+⟩ — Whale Safe platform launches in Santa Barbara Channel, tracking corporate speed compliance in whale slow zones.
- **2020** ⟨+⟩ — IMO publishes the *Fourth IMO GHG Study 2020*, using satellite AIS datasets for global shipping emissions baselines (Faber et al. 2020).

## On the wire

### The Right Whale Area Notice payload

Under IMO SN.1/Circ.289, environmental hazard alerts, whale management zones, and acoustic slow zones are broadcast as an **Application-Specific Message** (**ASM**) using **Message 8** (Binary Broadcast Message). The payload uses Designated Area Code (**DAC**) 1 (International) with Function Identifier (**FI**) 22 (Area Notice), or regional allocations such as USCG DAC 367.

A typical single-slot Area Notice broadcast alerting mariners to an active right-whale slow zone has the following bit layout:

```
+-------------------------------------------------------------------------+
|                  AIS MESSAGE 8: AREA NOTICE (FI 22)                     |
+-------------------+---------+-------------------------------------------+
| Field             | Bits    | Description / Value                       |
+-------------------+---------+-------------------------------------------+
| Message ID        | 0..5    | Constant 8 (Binary Broadcast Message)     |
| Repeat Indicator  | 6..7    | 0 (Default)                               |
| Source MMSI       | 8..37   | 003669999 (USCG Coastal Base Station)     |
| Spare             | 38..39  | 0                                         |
| DAC               | 40..49  | 0000000001 (DAC = 1, International)       |
| FI                | 50..54  | 010110 (FI = 22, Area Notice)             |
| Area Version      | 55..60  | 1                                         |
| Area Type         | 61..67  | 0110101 (Area Type 53: Whale Slow Zone)   |
| Scale Factor      | 68..70  | Scale multiplier for sub-areas            |
| Link ID           | 71..80  | Unique identification number for zone     |
| Duration          | 81..98  | Active alert duration in minutes          |
| Sub-Area Shape    | 99..101 | 000 = Circle / Point; 001 = Rectangle     |
| Center Latitude   | 102..125| 24-bit signed integer (1/10000 minute)    |
| Center Longitude  | 126..150| 25-bit signed integer (1/10000 minute)    |
| Radius / Precision| 151..162| Radius in decameters (e.g. 5 nmi = 9260 m)|
+-------------------+---------+-------------------------------------------+
```

When an approaching vessel receives this transmission, the transponder outputs an `!AIVDM` sentence:

```text
!AIVDM,1,1,,B,8030oP@000000000000000000000,2*1A
```

ECDIS units with ASM presentation software display a circular boundary polygon overlaid on the electronic vector chart with an auditory alert: `WHALE SLOW ZONE: MANDATORY 10 KN SPEED LIMIT IN EFFECT`.

> **Try it.** This Python script demonstrates how researchers audit vessel speed compliance inside a circular whale slow zone using decoded AIS kinematic data.

```python
import math

def haversine_distance_nmi(lat1, lon1, lat2, lon2):
    R_earth_nmi = 3440.065
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = (math.sin(delta_phi / 2.0) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2)
    return R_earth_nmi * 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

def audit_compliance(mmsi, lat, lon, sog, z_lat, z_lon, z_radius_nmi):
    dist = haversine_distance_nmi(lat, lon, z_lat, z_lon)
    in_zone = dist <= z_radius_nmi
    return {
        "mmsi": mmsi,
        "dist_nmi": round(dist, 2),
        "in_zone": in_zone,
        "sog": sog,
        "violation": in_zone and (sog > 10.0)
    }

# Stellwagen Bank Zone (42.35 N, 70.40 W, Radius 5.0 nmi)
z_lat, z_lon, radius = 42.3500, -70.4000, 5.0

v1 = audit_compliance(367111000, 42.3650, -70.4120, 9.8, z_lat, z_lon, radius)
v2 = audit_compliance(211222000, 42.3410, -70.3850, 18.4, z_lat, z_lon, radius)

print(f"Vessel {v1['mmsi']}: InZone={v1['in_zone']}, SOG={v1['sog']} kn, Violation={v1['violation']}")
print(f"Vessel {v2['mmsi']}: InZone={v2['in_zone']}, SOG={v2['sog']} kn, Violation={v2['violation']}")
```

Expected output:
```text
Vessel 367111000: InZone=True, SOG=9.8 kn, Violation=False
Vessel 211222000: InZone=True, SOG=18.4 kn, Violation=True
```

## Validation, uncertainty & data quality

Scientific and regulatory analyses of AIS data face notable data quality challenges:

### Errors and their propagation

1. **Heading sensor failure and default flags:** True Heading ($\psi$, bits 63–71 in Messages 1–3) is essential for hydrodynamic resistance and current decomposition. When gyrocompasses fail, transponders broadcast sentinel `511` ("not available"). Inazu's tsunami current inversion breaks down if $\psi$ is unavailable.
2. **Speed Over Ground quantization:** SOG is encoded as a 10-bit integer ($0.1\text{ kn}$ resolution). Below 2.0 kn, quantization introduces up to 10% relative error in velocity, propagating into uncertainties in auxiliary load and skimming operations.
3. **Draught misreporting:** Draught is entered manually into Message 5 in units of 0.1 m. Watchstanders often leave loaded draught unchanged during ballast legs or enter placeholders ($0.0\text{ m}$). Draught errors introduce $\pm 25\%$ error into bottom-up STEAM emission estimates.
4. **Satellite reception latency and slot contention:** In dense corridors, RF packet collisions cause terrestrial and orbital packet loss exceeding 40% to 70% ([Chapter 30](ch30-network-loading-packet-loss.md)). Linear interpolation across hours-long gaps creates tracks cutting across land and distorts gridded emissions.

### Concrete validation procedures

A four-stage validation pipeline is recommended for scientific workflows:

```
Raw AIS Stream
      |
      v
[ 1. Kinematic Plausibility Filter ]  --> Discard if SOG > 45 kn, Acceleration > 2.5 m/s^2,
      |                                  or Great-Circle jump requires supersonic speed
      v
[ 2. Static Registry Harmonization ]   --> Match MMSI/IMO with S&P Fairplay / IHS database.
      |                                  Correct impossible length, beam, and draught values
      v
[ 3. Gyrocompass & Sensor Audit ]      --> Discard Heading = 511 for current/tsunami models;
      |                                  flag angular difference |COG - Heading| > 45 deg
      v
[ 4. Trajectory Interpolation ]        --> Employ cubic spline or kinematic dead-reckoning
                                         rather than linear interpolation across gaps > 15 min
```

> **Worked example.** *Error propagation in cubic propulsion emissions.* Consider a container ship with design speed $v_{\text{design}} = 22.0\text{ kn}$ and $P_{\text{MCR}} = 50,000\text{ kW}$. A watchstander reports an SOG of $16.0\text{ kn}$. However, the ship steams through an opposing current of $2.0\text{ kn}$, making speed through water $v_{\text{STW}} = 18.0\text{ kn}$.
>
> 1. Naive power from SOG:
>    $$P_{\text{SOG}} = 50,000 \times \left( \frac{16.0}{22.0} \right)^3 = 19,230\text{ kW}$$
> 2. True power required through water:
>    $$P_{\text{STW}} = 50,000 \times \left( \frac{18.0}{22.0} \right)^3 = 27,385\text{ kW}$$
> 3. Systematic bias:
>    $$\text{Underestimation} = \frac{27,385 - 19,230}{27,385} = 29.8\%$$
>
> Neglecting a 2.0-knot current causes a 29.8% underestimation of power and emissions for that transit leg.

## Software

**Open source:**
- **libais** (Apache-2.0): High-performance C++ library with Python bindings developed by Kurt Schwehr. Created for *Deepwater Horizon* response tracking; parses standard and binary messages. *Caveat:* Largely in maintenance mode; does not parse newer VDES payloads.
- **STEAM** (Research code / Finnish Meteorological Institute): Atmospheric emissions inventory engine modeling $\text{NO}_x$, $\text{SO}_x$, $\text{CO}_2$, and particulate emissions from ship tracks. *Caveat:* Requires commercial ship registries (e.g., IHS Fairplay) for naval architecture data.
- **MovingPandas** (BSD-3-Clause): Python trajectory analysis package on GeoPandas and Shapely, offering trajectory smoothing and stop-detection. *Caveat:* Memory-bound on multi-gigabyte AIS datasets.

**Free but closed:**
- **Whale Alert** (Free mobile app; NOAA / IFAW / Conserve.IO): Mobile mapping app delivering real-time whale slow zones, acoustic detections, and regulatory notices to bridge tablets. *Caveat:* Requires cellular or satellite IP data connectivity.
- **Whale Safe Portal** (Free web dashboard; Benioff Ocean Initiative / UCSB): Analytics platform tracking ship speeds in California sanctuaries, scoring fleet compliance. *Caveat:* Geographically restricted to California waters.

**Commercial:**
- **eOdyn Omni-Situ** (Commercial service; eOdyn): Cloud platform deriving 2D ocean currents and wave characteristics from AIS vessel drift. *Caveat:* Proprietary algorithms; requires commercial data licensing.

## Standards & guides

- **IMO Resolution MSC.74(69), Annex 3 (1998):** *Recommendation on Performance Standards for Universal Shipborne Automatic Identification System (AIS).* Governs transponder operational standards.
- **ITU-R Recommendation M.1371-5 (2014):** *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile frequency band.* Defines TDMA framing and Messages 1–27.
- **IMO Circular SN.1/Circ.289 (2010):** *Guidance on the use of AIS Application-Specific Messages.* Defines international DAC/FI message formats, including Area Notices (FI 22).
- **IMO Circular SN.1/Circ.290 (2010):** *Guidance for the presentation and display of AIS application-specific messages information.* Outlines display guidance for bridge ECDIS.
- **US 50 CFR 224.105 (2008):** *Speed restrictions to protect North Atlantic right whales.* Mandatory 10.0-knot speed limits for ships $\ge 65\text{ ft}$ in Seasonal Management Areas.
- **IMO Resolution A.1106(29) (2015):** *Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems (AIS).* Governs bridge operational use.

## Pitfalls

1. **Conflating Speed Over Ground with Speed Through the Water:** 50 CFR 224.105 mandates compliance based on GNSS SOG, but physical strike lethality and engine emissions depend strictly on speed through water.
2. **Ignoring default heading flags (Heading = 511):** Processing pipelines that fail to filter heading sentinels (`511`) will distort acoustic directivity and ocean current models.
3. **Linear interpolation across satellite AIS data gaps:** Interpolating straight geographic lines across multi-hour satellite gaps underestimates transit distance and misplaces tracks across land.
4. **Relying on manual draught reports in Message 5:** Static draught is entered manually and rarely updated between legs, introducing errors into hull displacement calculations.
5. **Treating voluntary slow zones as mandatory regulations:** Conflating voluntary DMAs with mandatory SMAs leads analysts to misreport compliant mariners as legal violators.
6. **Neglecting auxiliary and boiler emissions:** Focusing exclusively on main engines ignores auxiliary generators and boilers, which produce up to 50% of emissions in port.
7. **Spatial coverage bias in ambient noise mapping:** Terrestrial AIS receivers have coastal ranges of 15–30 nmi; uncorrected coastal feeds create artificial quiet zones offshore.
8. **Neglecting ship draft in tsunami current models:** Tsunami currents affect deep-draft bulkers differently than shallow-draft tugs; failing to model vessel hull profiles distorts inverted current amplitudes.
9. **Confusing message creation time with ingest timestamp:** Satellite receivers batch packets before downlinking; real-time alert systems must timestamp bursts upon RF arrival, not ground receipt.
10. **Overlooking low-load engine penalties:** Below 20% engine load, diesel thermal efficiency drops sharply, increasing unburned hydrocarbon and particulate emission rates.

## Key takeaways

- **AIS transformed marine spatial planning:** Historic vessel traffic data enabled empirical proof that rotating shipping lanes (such as the 2007 Boston TSS shift) can cut lethal whale strike risks by up to 80%.
- **Kinetic lethality scales non-linearly:** Capping vessel speeds at 10.0 knots reduces the probability of a ship strike resulting in whale mortality from over 80% to 20–30%.
- **Bridge display bottlenecks drove the transition to IP:** Early efforts to transmit dynamic whale notices via AIS Message 8 were hindered by lack of bridge ECDIS ASM decoders, leading to mobile apps like Whale Alert.
- **Slowing vessels suppresses underwater noise:** Propeller cavitation noise scales with speed; voluntary slowdown initiatives (like Haro Strait's ECHO Program) achieve 3 dB reductions in ambient noise, halving acoustic power.
- **Bottom-up emissions models surpass bunker estimates:** Pairing high-frequency AIS tracks with naval architectural registries allows models like STEAM and the Fourth IMO GHG Study to map global maritime air pollution.
- **Merchant ships act as oceanographic probes:** Deviations between GNSS Course Over Ground and gyrocompass Heading enable opportunistic detection of open-ocean tsunamis and global surface current mapping.
- **Disaster response relies on real-time tracking:** AIS provided the essential common operational picture during the *Deepwater Horizon* oil spill, coordinating recovery fleets and verifying containment operations.

## References

- Erbe, C., MacGillivray, A., Williams, R. (2012). Mapping cumulative noise from shipping to inform marine spatial planning. *The Journal of the Acoustical Society of America*, 132(5):EL423–EL428. doi:10.1121/1.4758779
- Erbe, C., Williams, R., Sandilands, D., Ashe, E. (2014). Identifying modeled ship noise hotspots for marine mammals of Canada's Pacific region. *PLOS ONE*, 9(3):e89820. doi:10.1371/journal.pone.0089820
- Faber, J., Hanayama, S., Zhang, S., Pereda, P., Comer, B., Hauer, T., Schim van der Loeff, W., Smith, T., et al. (2020). *Fourth IMO GHG Study 2020*. London: International Maritime Organization.
- Guichoux, Y., Lennon, M., Thomas, N. (2016). Sea surface currents calculation using vessel tracking data. In *Proceedings of the Maritime Knowledge Discovery and Anomaly Detection Workshop*. Ispra: Joint Research Centre, European Commission.
- Inazu, D., Ikeya, T., Waseda, T., Hibiya, T., Shigihara, Y. (2018). Measuring offshore tsunami currents using ship navigation records. *Progress in Earth and Planetary Science*, 5(1):38. doi:10.1186/s40645-018-0194-5
- International Maritime Organization (2010). *Guidance on the Use of AIS Application-Specific Messages*. IMO Circular SN.1/Circ.289. London: IMO.
- International Maritime Organization (2015). *Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems (AIS)*. IMO Resolution A.1106(29). London: IMO.
- International Telecommunication Union (2014). *Technical Characteristics for an Automatic Identification System Using Time Division Multiple Access in the VHF Maritime Mobile Frequency Band*. Recommendation ITU-R M.1371-5. Geneva: ITU.
- Jalkanen, J.-P., Brink, A., Kalli, J., Pettersson, H., Kukkonen, J., Stipa, T. (2009). A modelling system for the exhaust emissions of marine traffic and its application in the Baltic Sea area. *Atmospheric Chemistry and Physics*, 9(23):9209–9223. doi:10.5194/acp-9-9209-2009
- Jalkanen, J.-P., Johansson, L., Kukkonen, J., Brink, A., Kalli, J., Stipa, T. (2012). Extension of an assessment model of ship traffic exhaust emissions for particulate matter and carbon monoxide. *Atmospheric Chemistry and Physics*, 12(5):2641–2659. doi:10.5194/acp-12-2641-2012
- McGillivary, P. A., Schwehr, K. D., Fall, K. (2009). Enhancing AIS to improve whale-ship collision avoidance and maritime security. In *OCEANS 2009*, pages 1–9. IEEE. doi:10.23919/OCEANS.2009.5422116
- McKenna, M. F., Ross, D., Wiggins, S. M., Hildebrand, J. A. (2012). Underwater radiated noise from modern commercial ships. *The Journal of the Acoustical Society of America*, 131(1):92–103. doi:10.1121/1.3664100
- Merchant, N. D., Witt, M. J., Blondel, P., Godley, B. J., Smith, G. H. (2012). Assessing sound exposure from shipping in coastal waters using a single hydrophone and Automatic Identification System (AIS) data. *Marine Pollution Bulletin*, 64(7):1320–1329. doi:10.1016/j.marpolbul.2012.05.004
- National Oceanic and Atmospheric Administration (2008). Speed restrictions to protect North Atlantic right whales. *Code of Federal Regulations*, Title 50, Section 224.105 (50 CFR 224.105). 73 FR 60173.
- Schwehr, K., McGillivary, P. (2007). Marine ship Automatic Identification System (AIS) for enhanced coastal security capabilities: An oil spill tracking application. In *OCEANS 2007*, pages 1–9. IEEE. doi:10.1109/OCEANS.2007.4449386
- Silber, G. K., Vanderlaan, A. S. M., Arceredillo, A. T., Johnson, L., Taggart, C. T., Brown, M. W., Sagarminaga, R. (2012). The role of the International Maritime Organization in reducing maritime traffic impacts on whales. *Marine Policy*, 36(6):1221–1233. doi:10.1016/j.marpol.2012.02.013
- Vanderlaan, A. S. M., Taggart, C. T. (2007). Vessel collisions with whales: The probability of lethal injury based on vessel speed. *Marine Mammal Science*, 23(1):144–156. doi:10.1111/j.1748-7692.2006.00098.x
- Wiley, D. N., Thompson, M., Pace, R. M., Levenson, J. (2011). Modeling speed restrictions to mitigate lethal collisions between ships and whales in the Stellwagen Bank National Marine Sanctuary, USA. *Biological Conservation*, 144(9):2377–2381. doi:10.1016/j.biocon.2011.06.014
