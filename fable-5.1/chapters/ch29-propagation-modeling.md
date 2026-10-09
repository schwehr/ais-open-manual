# Chapter 29 — Propagation modeling and AIS as a propagation probe

> **Part V — Radio.** The physical reality of maritime VHF: propagation models over sea and irregular terrain, atmospheric ducting mechanisms, open-source prediction engines, and using global AIS transmissions as opportunistic probes of the troposphere.

**In this chapter.** You will learn how maritime Very High Frequency (**VHF**) radio waves at 162 MHz propagate across coastal waters, open oceans, and littoral terrain. We derive the geometry of the four-thirds Earth effective radius model and the dual-terminal radio horizon equation. We examine the classic two-ray ground reflection model over seawater, demonstrating how tidal variations and sea roughness induce multipath fading and cause received signal power to decay at 40 dB per decade. We evaluate the standard propagation model hierarchy: free-space attenuation (Recommendation **ITU-R P.525**), spherical-Earth and knife-edge diffraction (Recommendation **ITU-R P.526**), point-to-area empirical field-strength prediction (Recommendation **ITU-R P.1546**), path-specific terrain diffraction (Recommendation **ITU-R P.1812**), the general wide-range terrestrial model (Recommendation **ITU-R P.2001**), and the Longley–Rice Irregular Terrain Model (**ITM**). We analyze atmospheric refraction and ducting mechanisms—evaporation ducts, surface ducts, and elevated trapping layers—explaining why coastal AIS receivers record bursts from vessels 300 to 600 km away. Finally, you will explore how AIS position reports serve as an opportunistic, wide-area propagation probe to validate radio models, detect tropospheric ducting, and monitor coastal weather phenomena.

## 29.1 Terrestrial VHF over sea: line of sight, 4/3-Earth, and the radio horizon

Maritime Automatic Identification System (**AIS**) transponders broadcast in the international maritime VHF band on two dedicated channels: AIS 1 (161.975 MHz) and AIS 2 (162.025 MHz), corresponding to a wavelength $\lambda \approx 1.85$ m (see [Chapter 27](ch27-rf-basics.md) and [Chapter 28](ch28-rf-encoding-physical-layer.md)). In a non-refracting homogeneous atmosphere, radio waves travel in straight lines, and the geometric line of sight (**LOS**) between an elevated antenna and the sea surface is constrained strictly by Earth's physical curvature.

However, the Earth's lower atmosphere is not homogeneous. Atmospheric pressure, temperature, and water vapor partial pressure decrease with altitude. Because the refractive index of air $n$ depends on these thermodynamic parameters, $n$ decreases with height throughout the troposphere. Radio refractivity $N$ is defined in Recommendation ITU-R P.453-14 as:

$$N = (n - 1) \times 10^6 = \frac{77.6}{T} \left( p + 4810 \frac{e}{T} \right)$$

where $p$ is total pressure in hPa, $T$ is temperature in K, and $e$ is water vapor partial pressure in hPa. In a standard reference atmosphere (ITU-R P.453-14), the vertical refractivity gradient near the surface is approximately $dN/dh \approx -39$ N-units/km.

Because refractive index decreases with altitude, phase velocity ($v = c/n$) is higher at the upper edge of an advancing wavefront than at its lower edge. This velocity gradient continuously bends the wavefront downward toward Earth's surface. 

To simplify path calculations without tracing curved rays over a sphere of radius $a \approx 6,371$ km, radio engineers map the geometry into straight rays over a fictitious sphere of effective Earth radius $a_e = k \cdot a$. The effective Earth radius factor $k$ relates to the vertical refractivity gradient:

$$k = \frac{1}{1 + a \frac{dn}{dh}} \approx \frac{1}{1 + 6.371 \times 10^{-3} \frac{dN}{dh}}$$

Substituting the standard gradient of $-39$ N-units/km yields:

$$k \approx \frac{1}{1 + 6.371 \times 10^{-3} (-39)} \approx \frac{4}{3} \approx 1.333$$

This is the standard **4/3-Earth convention**, yielding an effective Earth radius $a_e \approx 8,495$ km.

The distance $d_1$ from an antenna at height $h_1$ (meters) to the tangent horizon point is:

$$d_1 = \sqrt{2 a_e \frac{h_1}{1000}} = \sqrt{16.99 \cdot h_1} \approx 4.12 \sqrt{h_1} \text{ km}$$

When two elevated terminals—such as a coastal station with antenna height $h_1$ and a ship with antenna height $h_2$—communicate across the sea, the total mutual radio horizon distance $d_{\text{horiz}}$ is:

$$d_{\text{horiz}} \approx 4.12 \left( \sqrt{h_1} + \sqrt{h_2} \right) \text{ km} \approx 2.22 \left( \sqrt{h_1} + \sqrt{h_2} \right) \text{ nmi}$$

> **Definitions that bite.** The radio horizon is not the optical horizon. For a visual observer at sea level, optical refraction gives an effective factor $k \approx 1.06$ to $1.10$, yielding an optical horizon of $3.57 \sqrt{h}$ to $3.8 \sqrt{h}$ km. The VHF radio horizon ($k \approx 1.33$) extends roughly 10% to 15% farther ($4.12 \sqrt{h}$ km) because water vapor contributes far more to electrical permittivity at radio frequencies than at visible optical frequencies. Neither horizon is an absolute barrier: diffraction bleeds signals over the horizon, while atmospheric trapping layers can extend reception hundreds of kilometers beyond both.

Table 29.1 summarizes mutual radio horizon distances across representative maritime geometries under standard 4/3-Earth conditions.

| Station 1 ($h_1$) | Station 2 ($h_2$) | Horizon (km) | Horizon (nmi) | Operational Context |
|---|---|---|---|---|
| Inflatable skiff (1.5 m) | Inflatable skiff (1.5 m) | 10.1 km | 5.4 nmi | Small craft tactical rendezvous |
| Patrol cutter (10 m) | Fishing trawler (6 m) | 23.1 km | 12.5 nmi | Coastal fishery inspection |
| Container ship (30 m) | Pilot boat (5 m) | 31.8 km | 17.2 nmi | Harbor approach coordination |
| Container ship (30 m) | Tanker masthead (40 m) | 48.6 km | 26.2 nmi | Open-ocean ship-to-ship encounter |
| Coastal mast (50 m) | Container ship (30 m) | 51.7 km | 27.9 nmi | Standard VTS coastal coverage |
| Lighthouse cliff (100 m) | Tanker masthead (40 m) | 67.3 km | 36.3 nmi | Regional surveillance station |
| Mountain site (500 m) | Tanker masthead (40 m) | 118.2 km | 63.8 nmi | Strategic surveillance base station |

```
Standard Troposphere vs. 4/3-Earth Geometry
=============================================================================
  Actual Physical Path (Curved Ray):
  Transmitter (h1)                                         Receiver (h2)
        \                                                       /
         \~~~~~ Curved Wavefront (dn/dh = -39 N-units/km) ~~~~~/
    -------\-------------------------------------------------/------- Sea Surface
            \____________________ a = 6,371 km _____________/

  Equivalent 4/3-Earth Model (Straight Ray):
  Transmitter (h1)                                         Receiver (h2)
        \                                                       /
         \----------------- Straight Line Path ----------------/
    ------\---------------------------------------------------/------
           \__________________ a_e = 8,495 km _______________/
```

## 29.2 The two-ray model over sea: Fresnel zones, lobing, and tidal effects

When two maritime transponders operate within line of sight, free-space path loss alone does not dictate received signal power. Radiation from a vertical dipole expands spherically: one component travels directly from transmitter to receiver, while another reflects off the sea surface.

Recommendation ITU-R P.525-5 defines basic free-space path loss (**FSPL**) between isotropic radiators:

$$\text{FSPL} = 20 \log_{10}(d_{\text{km}}) + 20 \log_{10}(f_{\text{MHz}}) + 32.44 \text{ dB}$$

At the AIS carrier frequency $f = 162.0$ MHz, this yields:

$$\text{FSPL}_{162} = 20 \log_{10}(d_{\text{km}}) + 76.62 \text{ dB}$$

Over seawater, the direct ray interferes vectorially with the sea-surface reflection. At 162 MHz, seawater exhibits relative permittivity $\varepsilon_r \approx 70$ to $80$ and conductivity $\sigma \approx 4$ to $5$ S/m. For vertical polarization at grazing angles $\psi \approx \frac{h_1 + h_2}{d} \ll 1^\circ$ (well below the $4^\circ$ to $6^\circ$ pseudo-Brewster angle), the surface reflection coefficient is $\Gamma_v \approx -1 = 1 \cdot e^{j \pi}$.

The path length difference $\Delta r$ between reflected and direct rays over flat Earth is $\Delta r \approx \frac{2 h_1 h_2}{d}$. Adding the $180^\circ$ reflection phase shift yields a total phase difference $\Delta \phi = \frac{4\pi h_1 h_2}{\lambda d} + \pi$. The resulting received field ratio is:

$$\left| \frac{E_{\text{rx}}}{E_0} \right| = 2 \left| \sin\left( \frac{2\pi h_1 h_2}{\lambda d} \right) \right|$$

This sinusoidal interference generates **multipath lobing**:
1. **Constructive peaks:** Where $\frac{2\pi h_1 h_2}{\lambda d} = \frac{\pi}{2}, \frac{3\pi}{2}, \dots$, the received field doubles ($|E_{\text{rx}}| = 2 E_0$), providing $+6$ dB power gain over free space.
2. **Destructive nulls:** Where $\frac{2\pi h_1 h_2}{\lambda d} = \pi, 2\pi, \dots$, the two rays cancel destructively, creating sharp signal nulls.

As distance $d$ increases past the outermost lobe, the small-angle approximation $\sin\theta \approx \theta$ applies:

$$\left| \frac{E_{\text{rx}}}{E_0} \right| \approx \frac{4\pi h_1 h_2}{\lambda d} \implies P_{\text{rx}} \approx P_{\text{tx}} G_{\text{tx}} G_{\text{rx}} \frac{h_1^2 h_2^2}{d^4}$$

In logarithmic decibel form, the asymptotic two-ray path loss is:

$$L_{\text{2-ray}} = 40 \log_{10}(d) - 20 \log_{10}(h_1) - 20 \log_{10}(h_2) \text{ dB}$$

This is the classic **40 dB per decade roll-off** ($1/d^4$ power decay). While free space attenuates at 20 dB per decade, grazing reflection doubles the rate of signal decay once beyond the outer interference lobe.

```
Multipath Interference Lobes over Seawater (162 MHz)
=============================================================================
Received
Power (dBm)
   |
-30|    /\        /\
   |   /  \      /  \
-50|  /    \    /    \
   | /      \  /      \        Free Space (20 dB/decade)
-70|/        \/        \--------------------------------------------
   |                    \
-90|                     \       Two-Ray Asymptote (40 dB/decade)
   |                      \-----------------------------------------
-110                      \ \      Receiver Sensitivity Floor (-107 dBm)
   +------------------------------------------------------------------------>
   0        5        10        15        20        25        30     Distance (nmi)
             [ Lobing Region ]              [ Asymptotic 1/d^4 Region ]
```

### 29.2.1 Sea state and tidal modulation

Real ocean surfaces are agitated by wind and swell. The Rayleigh roughness parameter $R_a = \frac{4\pi \sigma_h \sin\psi}{\lambda}$ determines whether reflection is specular or diffuse. When $R_a \ll 1$ (calm water), reflection is specular and nulls remain deep. In rough seas ($R_a > 1$), diffuse scattering degrades phase coherence; deep nulls fill in, while constructive peaks are attenuated.

Furthermore, coastal tides dynamically alter antenna elevations. In areas with large tidal ranges (e.g., Bay of Fundy, Bristol Channel), the effective heights $h_1(t)$ and $h_2(t)$ oscillate cyclically. Because null positions depend strictly on the product $h_1 h_2$, rising and falling tides sweep interference nulls across fixed paths, causing periodic 10- to 20-minute signal fades for anchored vessels or fixed offshore platforms.

> **Worked example.** A shore station ($h_1 = 30$ m) receives a Class A transponder ($h_2 = 15$ m) at $f = 162.0$ MHz ($\lambda = 1.851$ m).
>
> 1. *Radio horizon:*
>    $$d_{\text{horiz}} = 4.12 \left( \sqrt{30} + \sqrt{15} \right) = 4.12 (5.477 + 3.873) = 38.52 \text{ km} \approx 20.8 \text{ nmi}$$
> 2. *Outermost constructive peak:*
>    $$d_{\text{peak}} = \frac{4 h_1 h_2}{\lambda} = \frac{4 \times 30 \times 15}{1.851} \approx 972.5 \text{ m} \approx 0.52 \text{ nmi}$$
> 3. *Outermost destructive null:*
>    $$d_{\text{null}} = \frac{2 h_1 h_2}{\lambda} = \frac{2 \times 30 \times 15}{1.851} \approx 486.2 \text{ m} \approx 0.26 \text{ nmi}$$
> 4. *Path loss at 20 km ($d = 20,000$ m):*
>    - Free space:
>      $$\text{FSPL} = 20 \log_{10}(20) + 20 \log_{10}(162.0) + 32.44 = 102.65 \text{ dB}$$
>    - Two-ray:
>      $$L_{\text{2-ray}} = 40 \log_{10}(20,000) - 20 \log_{10}(30) - 20 \log_{10}(15) = 118.98 \text{ dB}$$
> 5. *Received power link budget at 20 km:*
>    Class A transponder radiates $P_{\text{tx}} = 12.5$ W ($+41.0$ dBm). Assuming antenna gains $G_{\text{tx}} = 2.15$ dBi, $G_{\text{rx}} = 5.0$ dBi, and line losses $L_{\text{cable}} = 2.5$ dB:
>    $$P_{\text{rx}} = +41.0 + 2.15 + 5.0 - 2.5 - 118.98 = -73.33 \text{ dBm}$$
>    Against the Class A sensitivity threshold of $-107.0$ dBm (ITU-R M.1371-6 Table 7), the link retains a $33.67$ dB fade margin.

## 29.3 Diffraction over the spherical Earth and terrain: P.526, knife-edges, and shadow zones

Beyond the mutual radio horizon ($d > d_{\text{horiz}}$), direct and surface-reflected rays are physically blocked by the Earth's bulge. Signals bend into the geometric shadow region via **diffraction**.

Recommendation **ITU-R P.526-16** specifies methods for computing diffraction loss over a smooth spherical Earth and irregular obstacles. For smooth-Earth diffraction beyond the horizon, the residue series approximation shows that at 162 MHz over seawater, diffraction attenuation increases rapidly at approximately **0.8 to 1.2 dB per kilometer** immediately past the radio horizon. This steep cliff explains why standard terrestrial AIS tracking drops precipitously within 10 to 20 km beyond the horizon.

When coastal terrain obstacles (islands, promontories, breakwaters) obstruct the path, ITU-R P.526-16 applies knife-edge diffraction. The first Fresnel zone radius $R_1$ at distance $d_1$ and $d_2$ ($d = d_1 + d_2$) is:

$$R_1 = \sqrt{\frac{\lambda d_1 d_2}{d_1 + d_2}}$$

For a mid-path obstacle between stations separated by 40 km ($d_1 = d_2 = 20$ km) at 162 MHz ($\lambda = 1.85$ m), $R_1 \approx 136.0$ m. If an obstacle penetrates this clearance, diffraction loss occurs even if optical line of sight is clear. The dimensionless Fresnel–Kirchhoff parameter $\nu = h_{\text{obs}} \frac{\sqrt{2}}{R_1}$ determines knife-edge loss $J(\nu)$:
- Grazing obstacle ($\nu = 0$): $J(0) \approx 6.0$ dB loss.
- 50 m obstruction crest ($\nu \approx 0.52$): $J(\nu) \approx 10.5$ dB loss.
- Deep fjords or high headlands: knife-edge losses exceed 25 to 45 dB, creating deep coastal shadow zones.

## 29.4 The ITU-R propagation model ladder: P.1546, P.1812, and P.2001

To plan coastal radio networks, maritime administrations employ standardized empirical and deterministic propagation models.

```
+-----------------------------------------------------------------------------+
| Recommendation ITU-R P.525-5: Calculation of Free-Space Attenuation         |
+-----------------------------------------------------------------------------+
                                      |
                                      v
+-----------------------------------------------------------------------------+
| Recommendation ITU-R P.526-16: Propagation by Diffraction                   |
+-----------------------------------------------------------------------------+
                                      |
                                      v
+-----------------------------------------------------------------------------+
| Recommendation ITU-R P.1546-6: Point-to-Area Field Strength Predictions    |
| Empirical curves (30–4000 MHz), land/sea/mixed paths, 50%, 10%, 1% time     |
+-----------------------------------------------------------------------------+
                                      |
                                      v
+-----------------------------------------------------------------------------+
| Recommendation ITU-R P.1812-8: Path-Specific Point-to-Area Model           |
| Detailed terrain DEM profile, clutter, local ducting statistics             |
+-----------------------------------------------------------------------------+
                                      |
                                      v
+-----------------------------------------------------------------------------+
| Recommendation ITU-R P.2001-6: General Wide-Range Terrestrial Model        |
| 30 MHz–50 GHz continuous CDF: LOS, diffraction, troposcatter, and ducting   |
+-----------------------------------------------------------------------------+
```

### 29.4.1 Recommendation ITU-R P.1546-6

Recommendation **ITU-R P.1546-6** is the regulatory baseline for coastal coverage planning and VHF coordination. It provides empirical field-strength curves across frequencies (100–2,000 MHz), path categories (land, cold sea, warm sea), and time percentages ($50\%$, $10\%$, $1\%$). Over sea paths, low surface roughness and persistent humidity gradients produce substantially higher field strengths than over land. The $1\%$ and $10\%$ time curves capture seasonal coastal ducting, modeling over-the-horizon field strengths that cause distant co-channel interference.

### 29.4.2 Recommendation ITU-R P.1812-8 and P.2001-6

Recommendation **ITU-R P.1812-8** is a path-specific point-to-area model that integrates digital elevation model (**DEM**) terrain profiles with local radiometeorological parameters ($N_0, \Delta N$). It models line of sight, subpath diffraction, spherical/knife-edge terrain diffraction, tropospheric scatter, and surface ducting along specific Great Circle radials.

Recommendation **ITU-R P.2001-6** is the most advanced general-purpose terrestrial model maintained by the ITU (30 MHz to 50 GHz). P.2001 models the continuum of propagation mechanisms simultaneously: free-space loss, spherical and irregular terrain diffraction, forward troposcatter, and ducting/layer reflection. It outputs complete cumulative distribution functions (**CDFs**) of path loss from $0.001\%$ to $99.999\%$ of time, providing a unified framework for both link availability and interference prediction.

## 29.5 Open-source terrain engines: ITM, Longley–Rice, SPLAT!, and Signal Server

For coastal AIS station deployment, engineers rely on automated software engines to calculate horizon masks and terrain shadowing (see [Chapter 37](ch37-shore-collection-siting.md)).

### 29.5.1 The Longley–Rice Irregular Terrain Model (ITM)

The **Longley–Rice model**, formally the ITS Irregular Terrain Model (**ITM**), was developed by Anita Longley, Philip Rice, and George Hufford at NTIA/ITS (Hufford, Longley & Kissick 1982; Hufford 1999). ITM operates in point-to-point mode (using an explicit DEM elevation profile) or area prediction mode (parameterized by terrain roughness $\Delta h$). It incorporates statistical variability across time ($q_T$), location ($q_L$), and situation ($q_S$). The open-source reference code is maintained by NTIA on GitHub (`NTIA/itm` in modern C++).

### 29.5.2 SPLAT!, Signal Server, and Maritime Limitations

Prominent tools wrap ITM to generate coverage maps from SRTM elevation data:
- **SPLAT!:** Open-source (GPLv2) command-line tool by John A. Magliacane (KD2BD) that wraps ITM for coverage contours and obstruction analysis.
- **Signal Server:** Multithreaded open-source (AGPLv3) propagation server by Alex Farrant / Cloud-RF, exposing ITM and ITU-R P.1812 engines via a REST API.
- **Radio Mobile:** Freeware tool by Roger Coudé (VE2DBE) combining ITM with elevation and land-cover databases.

**Critical limitation over water:** ITM models standard diffraction and troposcatter, but **contains zero mechanisms for atmospheric ducting or evaporation layers**. Over open sea ($\Delta h = 0$), ITM collapses to standard smooth-Earth diffraction, predicting that AIS signals vanish ($> 200$ dB loss) beyond 80 km. While excellent for siting coastal antennas against landward hills, ITM cannot predict over-the-horizon maritime reception.

Table 29.2 compares primary propagation models used in maritime VHF engineering.

| Model / Engine | Standards Reference | Input Requirements | Models Ducting? | Open Source? | Primary Maritime Role |
|---|---|---|---|---|---|
| **Two-Ray Flat Sea** | EM Theory | $h_1, h_2, d, f$ | No | Yes (script) | Inshore LOS link budgets ($< 20$ nmi) |
| **ITU-R P.526-16** | ITU-R P.526 | Heights, obstacle profile | No | Open algorithm | Headland / island knife-edge diffraction |
| **ITU-R P.1546-6** | ITU-R P.1546 | Path type, time %, $h_{\text{eff}}$ | Statistically (1%, 10%) | Open algorithms | Coastal VTS coverage & interference |
| **ITU-R P.1812-8** | ITU-R P.1812 | Terrain DEM, $\Delta N, N_0$ | Yes (statistical) | Open algorithms | Path-specific coastal engineering |
| **ITU-R P.2001-6** | ITU-R P.2001 | Terrain profile, climate data | Yes (trapping & scatter) | Open C/MATLAB | Full CDF statistical loss prediction |
| **ITM (Longley–Rice)**| Hufford (1982, 1999)| Terrain DEM, climate type | **No** | Yes (NTIA C++) | Landward terrain shadowing & siting |
| **SPLAT!** | Magliacane / ITM | SRTM DEM, station coords | **No** | Yes (GPLv2) | CLI horizon masks & LOS maps |
| **Signal Server** | Farrant / Cloud-RF | DEM tiles, ITM/P.1812 | Optional (P.1812 mode) | Yes (AGPLv3) | Automated server-side coverage pipelines |

## 29.6 Atmospheric refraction and ducting: evaporation ducts, surface ducts, and elevated layers

To classify anomalous refraction, Recommendation ITU-R P.453-14 defines the **modified refractivity** $M$:

$$M(h) = N(h) + \left( \frac{h}{a} \right) \times 10^6 \approx N(h) + 157 \cdot h_{\text{km}}$$

Differentiating with respect to height yields $\frac{dM}{dh} = \frac{dN}{dh} + 157$ M-units/km:
- **Sub-refraction ($dM/dh > 157$):** Warm, moist air under cold, dry air bends rays upward, truncating the radio horizon.
- **Standard refraction ($dM/dh \approx 118$):** Standard 4/3-Earth downward curvature.
- **Super-refraction ($0 \le dM/dh < 118$):** Rays bend downward faster than standard, extending horizon range.
- **Trapping / Ducting ($dM/dh < 0$):** Downward ray curvature exceeds Earth's physical curvature ($1/\rho > 1/a$). Electromagnetic energy is trapped within an atmospheric boundary layer, propagating with low waveguide attenuation.

```
Refractivity Profiles and Ray Paths
=============================================================================
Height (h)
   |
   |      Sub-refraction         Standard               Trapping (Ducting)
   |      (dM/dh > 157)          (dM/dh ~ 118)          (dM/dh < 0)
   |           /                     |                        \
   |          /                      |                         \   Trapping
   |         /                       |                          \   Layer
   +-------+-------------------------+----------------------------+---------->
   0                                                            Modified
                                                                Refractivity M
Ray Tracing:
              Sub-refraction:               Standard:               Ducting:
               / (Bends UP)                  --- (Bends Down)        ~~~~~~~~~ (Trapped)
              /                             /                       ----------- Sea
```

### 29.6.1 Ducting categories and the 162 MHz trapping condition

Tropospheric ducts fall into three categories:
1. **Evaporation ducts:** Formed by rapid vertical humidity gradients directly above the sea surface (5 to 25 m thick). Permanent over warm waters.
2. **Surface ducts:** Formed by temperature inversions (e.g., warm continental air flowing over cold water, or radiative cooling) extending from the surface up to several hundred meters.
3. **Elevated ducts:** Formed by subsidence inversions in anticyclonic systems, floating between 200 m and 2,000 m above sea level.

A duct acts as a leaky waveguide with a minimum trapping frequency $f_{\text{min}} \propto d_{\text{duct}}^{-3/2}$ (ITU-R P.453-14). 
- In shallow evaporation ducts (10–15 m thick), $f_{\text{min}}$ is between 1 GHz and 3 GHz. **Marine radar (3 GHz and 9 GHz) is strongly trapped in evaporation ducts, but VHF AIS at 162 MHz is not trapped.**
- To trap 162 MHz ($\lambda = 1.85$ m), a duct must be **at least 40 to 60 meters thick** with a strong refractivity inversion ($\Delta M \ge 20$ to $30$).
- Extreme over-the-horizon AIS receptions ($> 200$ km) are caused by **deep surface ducts and elevated subsidence trapping layers**, not shallow evaporation ducts (Sirkova 2023; Rautiainen et al. 2026).

> **Case file.** In June 2023, Sanjin Valčić and David Brčić published an experimental software-defined radio (**SDR**) study in the Northern Adriatic Sea (*Journal of Marine Science and Engineering*). Operating a coastal SDR receiver over 24 hours, they decoded 159,965 packets across 115 targets with an overall packet error rate of $54.3\%$. The receiver consistently decoded valid bursts from vessels hundreds of nautical miles away—an order of magnitude beyond the nominal 20 to 30 nmi horizon. By correlating observations with synoptic weather charts and ruling out ionospheric sporadic-E and troposcatter, they confirmed that an advective marine surface duct channeled 162 MHz signals along the Adriatic basin.

## 29.7 Long-range anomalous reception: evidence from 500+ km observations

Long-range AIS receptions beyond 500 km have been thoroughly verified by modern scientific campaigns.

### 29.7.1 The Utö island Baltic campaign (Rautiainen et al. 2026)

A joint Finnish research team (Rautiainen et al. 2026) operated an experimental AIS station on Utö island in the Baltic Sea (59°46′50″ N, 21°22′23″ E), recording continuous data across two antennas (7 m and 30 m above sea level) alongside a 60 m meteorological mast instrumented with temperature and humidity sensors:
- **High OTH prevalence:** Over a full year, the 7 m antenna received over-the-horizon signals **34% of the time**, while the 30 m antenna recorded OTH reception **59% of the time**.
- **Extreme ranges:** Ships were regularly decoded at 300 to 500 km, with maximum receptions reaching **600 km** across the Baltic into Poland and Lithuania.
- **Duct height correlation:** When mast sensors measured a duct height $\ge 59$ m, OTH reception probability reached **90%** (7 m antenna) and **95%** (30 m antenna).
- **Reduced path-loss exponent:** Under ducting, received signal strength decayed slowly ($1/d$ cylindrical spreading) rather than suffering spherical diffraction loss ($> 1$ dB/km).

### 29.7.2 Ducting vs. Tropospheric Scatter

Dr. Irina Sirkova (2023) modeled 162 MHz maritime propagation using parabolic wave equations. She proved that troposcatter path loss over a 300 km sea path exceeds 210 to 230 dB, delivering received powers of $-165$ to $-185$ dBm (nearly 60 dB below receiver sensitivity). In contrast, trapping layers reduce path loss to 140–160 dB, delivering $-90$ to $-110$ dBm. Sirkova confirmed that **atmospheric ducting is the primary physical mechanism enabling maritime VHF packet decodes beyond 200 km**.

## 29.8 AIS as an opportunistic propagation probe

The global AIS network transforms commercial shipping into an opportunistic, wide-area atmospheric sensor array.

```
AIS Transponders as Tropospheric Probes
=============================================================================
  Calibrated Transmitters (12.5 W Class A)
  [Tanker] ----(GNSS Position, Known Power, Time Slot)----+
                                                          |
  [Cargo]  ----(GNSS Position, Known Power, Time Slot)----+---> [Coastal Receiver]
                                                          |           |
  [Ferries]----(GNSS Position, Known Power, Time Slot)----+           v
                                                              [Invert Refractivity]
                                                                      |
                                                                      v
                                                              Near-Real-Time Duct
                                                              Detection & Weather Map
```

### 29.8.1 Probe attributes and processing methodology

AIS provides unique probe characteristics:
1. **Calibrated power:** Class A transponders broadcast at nominal **12.5 W** ($\pm 1.5$ dB) per ITU-R M.1371-6 Table 5.
2. **Known coordinates:** Every position report provides GNSS latitude and longitude, yielding exact range and bearing.
3. **Deterministic intervals:** Underway Class A vessels report every 10 s (or 2–6 s maneuvering), allowing receivers to compute expected versus observed packet counts.
4. **Dense spatial sampling:** Hundreds of commercial vessels provide simultaneous crossing paths through the coastal boundary layer.

To monitor propagation conditions:
1. **Aggregate hourly range statistics:** Group Class A position reports into distance bins and track the **hourly 95th-percentile range ($R_{95}$)**. A surge in $R_{95}$ beyond $1.5 \times R_{\text{horiz}}$ reliably flags duct onset.
2. **Path-loss exponent fitting:** When using SDRs logging signal strength, fit $\text{RSS}(d) = P_0 - 10 \gamma \log_{10}(d)$. An exponent $\gamma \approx 4.0$ indicates standard diffraction, while $\gamma \le 2.5$ confirms active waveguide trapping.
3. **Refractivity field inversion:** Combining measured path losses across crossing radials enables numerical inversion of modified refractivity $M(x, z)$, providing near-real-time duct height maps without radiosondes.

> **Try it.** The Python script `code/rf/propagation_compare.py` compares empirical AIS reception statistics against theoretical free-space and two-ray models. Run it against the synthetic harbor sample log:
>
> ```bash
> . .venv/bin/activate
> python code/rf/propagation_compare.py data/samples/synthetic_harbor.nmea \
>     --rx 42.36 -70.95 --hrx 30 --htx 20
> ```
>
> Expected output:
> ```
> radio horizon (h_tx=20.0 m, h_rx=30.0 m): 22.1 nmi
>  range_nmi   p_obs   Prx_fspl  Prx_2ray  margin_2ray  note
>     0–5       0.60     -46.5     -47.6        59.4  
>     5–10      0.70     -56.0     -66.7        40.3  
>    10–15      0.73     -60.5     -75.5        31.5  
>    15–20      0.64     -63.4     -81.4        25.6  
>    20–25      0.32     -65.6     -85.8        21.2  margin ok but poor reception: shadowing/noise/antenna?
>    25–30      0.27     -67.3     -89.2        17.8  margin ok but poor reception: shadowing/noise/antenna?
>    30–35      0.16     -68.8     -92.1        14.9  
> ```
> Note how observed packet probability $p_{\text{obs}}$ falls steeply from $0.64$ at 15–20 nmi to $0.32$ across the 22.1 nmi radio horizon, despite theoretical two-ray link margins exceeding 20 dB. In coastal environments, diffraction loss and land clutter rapidly extinguish signals once past the horizon.

## Then & now

- **⟨H⟩ 1968:** ITS publishes the foundational Longley–Rice irregular terrain model, formalizing point-to-point and area diffraction algorithms across 20 MHz to 20 GHz for the US Department of Commerce.
- **⟨H⟩ 1982:** Hufford, Longley, and Kissick publish NTIA Report 82-100, standardizing ITM area prediction algorithms widely adopted by the FCC for broadcast planning.
- **⟨+⟩ 1998:** Recommendation ITU-R M.1371-0 establishes the AIS TDMA physical layer, budgeting a 24-bit buffer (accommodating 14 bits of distance delay, or 235.9 nmi one-way propagation) to protect adjacent slots (ITU-R M.1371-6 Annex 2 §A2-3.2.2.8.2).
- **⟨+⟩ 2001:** Recommendation ITU-R P.1546-1 supersedes CCIR 370 curves, providing the modern global regulatory basis for point-to-area field strength predictions over land, sea, and mixed paths.
- **⟨+⟩ 2008:** Høye et al. publish seminal models in *Acta Astronautica* demonstrating satellite AIS feasibility, shifting VHF propagation analysis from 2D horizons to 3D orbital cones.
- **⟨+⟩ 2012:** Recommendation ITU-R P.2001 is released, creating the first multi-mechanism terrestrial model capable of calculating continuous CDFs across diffraction, troposcatter, and ducting.
- **⟨+⟩ 2023:** Valčić and Brčić document 24-hour SDR AIS reception in the Northern Adriatic, demonstrating that coastal VHF ducting routinely yields message decodes hundreds of nautical miles beyond the geometric horizon.
- **⟨+⟩ 2026:** Rautiainen et al. publish a one-year experimental campaign at Utö island in the Baltic Sea (*Atmospheric Measurement Techniques*), proving that coastal VHF antennas experience over-the-horizon ducting up to 59% of the time, establishing AIS as an accurate, wide-area atmospheric probe.

## On the wire

AIS slot timing and link-layer framing directly reflect the physical limits of speed-of-light propagation across the sea surface. 

In the TDMA frame structure defined in Recommendation ITU-R M.1371-6 Annex 2 §A2-3.2, each 1-minute frame is partitioned into 2,250 slots. At 9,600 bit/s, each slot spans $26.667$ ms, or exactly **256 bit periods** (see [Chapter 21](ch21-link-layer-tdma.md) and [Chapter 28](ch28-rf-encoding-physical-layer.md)).

Table 29.3 details the bit-level structure of a standard 1-slot AIS transmission burst and its physical propagation timing budget.

| Field | Duration (bits) | Duration ($\mu$s) | Physical & Protocol Role | Standard Reference |
|---|---|---|---|---|
| **Ramp-up** | 8 bits | 833.3 $\mu$s | Transmitter power ramp-up to within $+1.5/-1.0$ dB of $P_{\text{ss}}$ | ITU-R M.1371-6 Table 6 |
| **Training sequence** | 24 bits | 2,500.0 $\mu$s | Alternating 0101 bit pattern for receiver clock synchronization | ITU-R M.1371-6 §A2-2.5 |
| **Start flag** | 8 bits | 833.3 $\mu$s | HDLC framing flag (`01111110`, 0x7E) | ITU-R M.1371-6 §A2-3.2.2.2 |
| **Data payload** | 168 bits | 17,500.0 $\mu$s | Message 1, 2, or 3 position report payload | ITU-R M.1371-6 Table 12 |
| **CRC (FCS)** | 16 bits | 1,666.7 $\mu$s | 16-bit CRC-CCITT (ISO/IEC 13239) error detection | ITU-R M.1371-6 §A2-3.2.2.6 |
| **End flag** | 8 bits | 833.3 $\mu$s | HDLC framing flag (`01111110`, 0x7E) | ITU-R M.1371-6 §A2-3.2.2.7 |
| **Buffer** | **24 bits** | **2,500.0 $\mu$s** | Absorbs bit stuffing (4b), sync jitter (6b), and **distance delay (14b)** | ITU-R M.1371-6 §A2-3.2.2.8 |
| **Total Slot** | **256 bits** | **26,666.7 $\mu$s** | Exactly 1 TDMA slot ($1/2250$ of a minute) | ITU-R M.1371-6 §A2-3.1.2 |

The **24-bit buffer** is the physical-layer mechanism that prevents speed-of-light delays from corrupting the TDMA network:
1. **Bit stuffing allowance (4 bits / 416.7 $\mu$s):** Accommodates worst-case HDLC zero-stuffing.
2. **Synchronization jitter (6 bits / 625.0 $\mu$s):** Accommodates GNSS timing offsets and transponder clock drift.
3. **Distance delay allowance (14 bits / 1,458.3 $\mu$s):** Radio waves travel at $c \approx 299,792$ km/s. Over 1,458.3 microseconds, a radio wave travels:

$$d = c \times t = 299,792 \text{ km/s} \times 1,458.33 \times 10^{-6} \text{ s} \approx 437.2 \text{ km} \approx 236.0 \text{ nmi}$$

Recommendation ITU-R M.1371-6 Annex 2 §A2-3.2.2.8.2 notes that this 14-bit budget protects propagation ranges in excess of **120 nmi (222 km)**. 

When extreme ducting enables reception from vessels 300 to 500 km away, propagation delay exceeds 1,458 $\mu$s. If a local vessel and a distant ducted vessel occupy adjacent TDMA slots, the delayed tail of the ducted burst bleeds across the buffer boundary into the opening bits of the next slot, corrupting the receiver's ramp-up and training sequence—a direct physical-layer consequence of anomalous propagation.

```
AIS TDMA Slot Timing & Distance Delay Buffer (256 Bits = 26.667 ms)
=============================================================================
| Ramp | Training | Start | Data Payload (168b) | CRC | End |    Buffer (24b)   |
| (8b) |  (24b)   | (8b)  |     (Messages 1-3)  | (16)| (8b)|                   |
+------+----------+-------+---------------------+-----+-----+-------------------+
                                                            | Stuff | Jitter| Delay |
                                                            | (4b)  |  (6b) | (14b) |
                                                            +-------+-------+-------+
                                                                            |
                                               Speed-of-light travel delay -+
                                               14 bits = 1,458 us = 236 nmi
```

## Validation, uncertainty & data quality

Quantifying propagation model errors and extracting scientific data from AIS receptions requires systematic error handling:

### Sources of Uncertainty

1. **Unknown vessel antenna heights:** Ships do not broadcast antenna heights. While length, beam, and vessel type are broadcast, whether a VHF antenna is mounted at 5 m (fishing boat) or 45 m (container ship) is unknown. Because two-ray received power scales as $h_1^2 h_2^2$, an unmodeled height variation between 10 m and 40 m introduces a **12 dB uncertainty** in link budgets.
2. **Transmission line and antenna gain variance:** While Class A transmitters maintain $12.5$ W within $\pm 1.5$ dB, antenna gains vary (0–6 dBi), and degraded feedlines or high VSWR routinely induce 3 to 10 dB of unmonitored loss on commercial vessels (see [Chapter 27](ch27-rf-basics.md) and [Chapter 32](ch32-antennas.md)).
3. **Class A vs. Class B power disparities:** Class A transponders radiate 12.5 W (+41 dBm), Class B SOTDMA units radiate 5.0 W (+37 dBm), and Class B CSTDMA units radiate 2.0 W (+33 dBm). Mixing station classes skews empirical path-loss analysis by 4 to 8 dB.
4. **Vessel dynamic motion:** Vessel pitch and roll alter antenna height and tilt vertical radiation patterns, introducing 3 to 6 dB of dynamic fading in heavy seas.

### Concrete Validation Procedure

To validate a coastal propagation model using an AIS receiver:
1. **Station filtering:** Filter raw NMEA logs to isolate **Class A position reports only** (Message types 1, 2, and 3). Discard Class B, SART, and base stations.
2. **Speed and status filtering:** Select commercial vessels underway at steady speeds (10–16 knots), where nominal reporting intervals are fixed at 10 seconds (6 reports per minute).
3. **Spatial binning:** Partition the maritime area into concentric range rings of width $\Delta R = 5$ km centered on the receiving antenna, segmented into $10^\circ$ azimuth sectors.
4. **Empirical detection probability calculation:** For each vessel $i$ in bin $b$ over $T = 1$ hour ($N_{\text{expected}} = 360$ messages):
   $$P_{\text{detection}}(b) = \frac{\sum_{i=1}^M N_{\text{observed}}(i)}{M \cdot N_{\text{expected}}}$$
   where $M$ is the count of distinct vessels operating within the bin.
5. **Thresholding duct events:** Define the statistical baseline horizon $R_{\text{horiz}}$ based on receiver antenna height and an assumed mean vessel height of 20 m. Flag a ducting event whenever the 95th percentile detection range $R_{95} > 1.5 \times R_{\text{horiz}}$ for two or more consecutive hours.

## Software

### Open Source

- **`NTIA/itm` (C++):** Modern C++ reference implementation of the Longley–Rice Irregular Terrain Model v1.2.2 maintained by NTIA. Authoritative for terrain diffraction. Caveat: does not model over-water atmospheric ducting or evaporation layers.
- **SPLAT! (C / Linux):** Popular open-source (GPLv2) tool by John A. Magliacane (KD2BD) that wraps ITM to generate coverage heatmaps and line-of-sight analysis from SRTM elevation tiles. Caveat: open-water marine path predictions truncate strictly at the diffraction horizon.
- **Signal Server (C++ / Docker):** High-performance, multithreaded propagation engine (AGPLv3) by Alex Farrant / Cloud-RF. Integrates ITM and ITU-R P.1812 with a REST API. Caveat: high memory usage when caching worldwide high-resolution DEM tiles.
- **`ais-catcher` (C++):** High-performance open-source (GPLv3) AIS receiver for SDRs by Jasper van Baten. Accurately decodes weak bursts, logs fine-grained signal metrics (RSSI, SNR), and serves as an ideal propagation probe. Caveat: internal RSSI requires RF signal generator calibration for absolute power accuracy.

### Free but Closed

- **Radio Mobile / Radio Mobile Online:** Widely used propagation software developed by Roger Coudé (VE2DBE). Free for amateur radio and personal non-commercial use. Excellent link profiling and horizon charting. Caveat: proprietary license; commercial use requires a separate agreement.

### Commercial

- **EDX SignalPro:** Industry-standard wireless network planning suite by EDX Wireless. Features full implementations of ITU-R P.1546, P.1812, P.2001, and 3D clutter databases. Caveat: expensive commercial licensing targeted at telecommunications carriers.
- **Cloud-RF:** Commercial cloud platform providing hosted Signal Server engines, automated APIs, global lidar/DEM data, and web interfaces. Caveat: subscription usage pricing per calculation.

## Standards & guides

- **Recommendation ITU-R M.1371-6 (02/2026):** *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band.* Governs AIS RF power levels (Table 5), receiver sensitivity (Table 7), slot timing masks (Table 6), and the 14-bit propagation delay buffer (§A2-3.2.2.8.2).
- **Recommendation ITU-R P.525-5 (11/2024):** *Calculation of free-space attenuation.* Formulates basic transmission loss and isotropic power spreading baseline equations.
- **Recommendation ITU-R P.526-16 (11/2025):** *Propagation by diffraction.* Formulates spherical-Earth diffraction, residue series, knife-edge diffraction, and irregular terrain obstruction methods.
- **Recommendation ITU-R P.1546-6 (08/2019):** *Method for point-to-area predictions for terrestrial services in the frequency range 30 MHz to 4 000 MHz.* International standard for coastal VHF field-strength curves over land, cold sea, and warm sea paths across $50\%$, $10\%$, and $1\%$ time percentages.
- **Recommendation ITU-R P.1812-8 (09/2025):** *A path-specific propagation prediction method for point-to-area terrestrial services in the VHF and UHF bands.* Standards for terrain profile evaluation, diffraction, and anomalous coastal propagation.
- **Recommendation ITU-R P.2001-6 (09/2025):** *A general purpose wide-range terrestrial propagation model in the frequency range 30 MHz to 50 GHz.* Comprehensive wide-range multi-mechanism model for line of sight, diffraction, troposcatter, and ducting.
- **Recommendation ITU-R P.453-14 (08/2019):** *The radio refractive index: its formula and refractivity data.* Standardizes definitions for radio refractivity $N$, modified refractivity $M$, vertical gradients, and ducting climatology.
- **Recommendation ITU-R P.372-18 (09/2026):** *Radio noise.* Standardizes galactic, atmospheric, and man-made environmental noise levels in the VHF maritime band.
- **NTIA Report 82-100 (1982):** *A Guide to the Use of the ITS Irregular Terrain Model in the Area Prediction Mode.* Foundational documentation for the Longley–Rice ITM algorithm.

## Pitfalls

1. **Assuming AIS is strictly line-of-sight.** Treating the $4/3$-Earth radio horizon as a rigid boundary causes operators to misidentify valid over-the-horizon ship decodes as software malfunctions or spoofing attacks. Elevated antennas in coastal regions experience over-the-horizon ducting more than $50\%$ of the time during summer months.
2. **Relying on ITM/Longley–Rice for maritime range prediction.** ITM lacks physical ducting mechanisms and collapses over open water ($\Delta h = 0$), falsely predicting zero coverage beyond the diffraction horizon. Use ITU-R P.1546 or P.2001 for maritime paths.
3. **Confusing optical horizon with radio horizon.** Using optical horizon formulas ($3.57 \sqrt{h}$) underestimates VHF radio coverage by 15%, because water vapor refracts 162 MHz radio waves substantially more than visible light.
4. **Expecting evaporation ducts to trap 162 MHz AIS.** Applying microwave radar rules of thumb to VHF leads to faulty planning. Shallow evaporation ducts (10–20 m) easily trap 3 GHz and 9 GHz radar but cannot trap 162 MHz AIS ($\lambda = 1.85$ m), which requires deep surface ducts or elevated trapping layers $> 40$ to $60$ m thick.
5. **Ignoring the two-ray 40 dB/decade roll-off within line of sight.** Using free-space loss (20 dB/decade) for link budgets inside the horizon overestimates received signal power by 15 to 30 dB, failing to account for destructive sea-surface reflection.
6. **Neglecting tidal height modulation of multipath nulls.** Forgetting that large coastal tides (6 to 15 m) cyclically shift antenna heights causes unexplained periodic link dropouts on fixed coastal monitoring receivers.
7. **Mixing Class A and Class B in propagation studies.** Treating all AIS targets as identical 12.5 W transmitters skews empirical path-loss analysis. Class B transponders broadcast at 2 W or 5 W with lower antenna elevations, creating an apparent 6 to 12 dB drop in received power.
8. **Interpreting remote ducted packets as spoofed timestamps.** When distant ships are received via ducting at 300 to 500 km, propagation delays (up to 1.7 ms) can cause bursts to overlap adjacent TDMA slot boundaries, triggering false alarms in naive protocol validation engines.
9. **Uncalibrated SDR RSSI logging.** Using uncalibrated raw software-defined radio gain values as scientific received power measurements introduces $\pm 6$ dB of non-linear error across dynamic range. Always calibrate SDR front-ends with an RF signal generator.
10. **Overlooking terrain shadow zones behind coastal islands.** Placing coastal AIS shore stations behind offshore islands or headlands creates severe knife-edge diffraction losses exceeding 20 to 40 dB, blinding the station to shipping lanes just beyond the ridge.

## Key takeaways

- VHF radio waves at 162 MHz are refracted downward by the vertical atmospheric refractivity gradient ($dN/dh \approx -39$ N-units/km), expanding the effective Earth radius by $4/3$ and establishing a mutual radio horizon of $d_{\text{horiz}} \approx 4.12(\sqrt{h_1} + \sqrt{h_2})$ km.
- Within unobstructed line of sight, specular reflection from seawater creates multipath interference, causing received signal power to decay asymptotically at 40 dB per decade ($1/d^4$), well below free-space expectations.
- Spherical-Earth diffraction attenuates signals sharply beyond the horizon at roughly 0.8 to 1.2 dB per kilometer, forming a steep cliff under standard atmospheric conditions.
- Standard terrain modeling tools based on ITM / Longley–Rice (such as SPLAT! and Signal Server) accurately model coastal terrain shadowing and horizon masks, but completely fail to model over-water atmospheric ducting.
- For maritime path predictions incorporating atmospheric ducting and enhanced coastal propagation, Recommendation ITU-R P.1546-6 and Recommendation ITU-R P.2001-6 are the authoritative international standards.
- Anomalous over-the-horizon propagation at 162 MHz is driven by deep surface ducts and elevated subsidence inversions ($> 40$ to $60$ m thick) where $dM/dh < 0$; shallow evaporation ducts cannot trap 162 MHz wavelengths.
- Long-term empirical studies (such as the 1-year Utö island Baltic campaign) prove that coastal receivers experience over-the-horizon ducting up to $59\%$ of the time, regularly decoding vessels at ranges exceeding 300 to 600 km.
- Global AIS broadcasts provide an opportunistic, continuous, calibrated propagation probe, enabling coastal stations to monitor atmospheric ducting and boundary layer weather phenomena in near-real time without dedicated radar sounders.

## References

- Grundhöfer, L., Rizzi, F. G., Gewies, S., Hoppe, M., Bäckstedt, J., et al. (2021). Positioning with medium frequency R-Mode. *NAVIGATION*, 68(4):829–841. doi:10.1002/navi.450
- Høye, G. K., Eriksen, T., Meland, B. J., Narheim, B. T. (2008). Space-based AIS for global maritime traffic monitoring. *Acta Astronautica*, 62(2–3):240–245. doi:10.1016/j.actaastro.2007.07.001
- Hufford, G. A., Longley, A. G., Kissick, W. A. (1982). *A Guide to the Use of the ITS Irregular Terrain Model in the Area Prediction Mode* (NTIA Report 82-100). Boulder, CO: National Telecommunications and Information Administration. doi:10.70220/zjkb4hxb
- Hufford, G. A. (1999). *The ITS Irregular Terrain Model, Version 1.2.2: The Algorithm* (NTIA Memorandum). Boulder, CO: National Telecommunications and Information Administration. doi:10.70220/9qncd6hb
- International Telecommunication Union (2019). *Recommendation ITU-R P.453-14: The radio refractive index: its formula and refractivity data*. Geneva: ITU. https://www.itu.int/rec/R-REC-P.453/en
- International Telecommunication Union (2019). *Recommendation ITU-R P.1546-6: Method for point-to-area predictions for terrestrial services in the frequency range 30 MHz to 4 000 MHz*. Geneva: ITU. https://www.itu.int/rec/R-REC-P.1546/en
- International Telecommunication Union (2024). *Recommendation ITU-R P.525-5: Calculation of free-space attenuation*. Geneva: ITU. https://www.itu.int/rec/R-REC-P.525/en
- International Telecommunication Union (2025). *Recommendation ITU-R P.526-16: Propagation by diffraction*. Geneva: ITU. https://www.itu.int/rec/R-REC-P.526/en
- International Telecommunication Union (2025). *Recommendation ITU-R P.1409-4: Propagation data and prediction methods required for the design of systems using high-altitude platform stations*. Geneva: ITU. https://www.itu.int/rec/R-REC-P.1409/en
- International Telecommunication Union (2025). *Recommendation ITU-R P.1812-8: A path-specific propagation prediction method for point-to-area terrestrial services in the VHF and UHF bands*. Geneva: ITU. https://www.itu.int/rec/R-REC-P.1812/en
- International Telecommunication Union (2025). *Recommendation ITU-R P.2001-6: A general purpose wide-range terrestrial propagation model in the frequency range 30 MHz to 50 GHz*. Geneva: ITU. https://www.itu.int/rec/R-REC-P.2001/en
- International Telecommunication Union (2026). *Recommendation ITU-R M.1371-6: Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band*. Geneva: ITU. https://www.itu.int/rec/R-REC-M.1371-6-202602-I/en
- International Telecommunication Union (2026). *Recommendation ITU-R P.372-18: Radio noise*. Geneva: ITU. https://www.itu.int/rec/R-REC-P.372/en
- Rautiainen, L., Johansson, L., Lensu, M., Tyynelä, J., Jalkanen, J.-P., Hasu, V., Stenbäck, E., Lonka, H., Laakso, A. (2026). Studying anomalous propagation over marine areas using an experimental AIS receiver set-up. *Atmospheric Measurement Techniques*, 19:2763–2785. doi:10.5194/amt-19-2763-2026
- Sirkova, I. (2023). Revisiting Enhanced AIS Detection Range under Anomalous Propagation Conditions. *Journal of Marine Science and Engineering*, 11(9):1838. doi:10.3390/jmse11091838
- Tang, H., Cha, H., Wei, M., Tian, B. (2018). A Study on the Propagation Characteristics of AIS Signals in the Evaporation Duct Environment. *2018 International Applied Computational Electromagnetics Society Symposium (ACES)*, pages 1–2. doi:10.23919/acess.2018.8669309
- Valčić, S., Brčić, D. (2023). On Detection of Anomalous VHF Propagation over the Adriatic Sea Utilising a Software-Defined Automatic Identification System Receiver. *Journal of Marine Science and Engineering*, 11(6):1170. doi:10.3390/jmse11061170
- Wirsing, K., Dammann, A., Raulefs, R. (2023). Direct Position Estimation for VDES R-Mode. *2023 IEEE/ION Position, Location and Navigation Symposium (PLANS)*, pages 724–728. doi:10.1109/plans53410.2023.10140053
