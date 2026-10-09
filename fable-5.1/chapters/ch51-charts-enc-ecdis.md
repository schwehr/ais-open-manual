# Chapter 51 — Nautical charts, ENC vs ECDIS vs ECS vs RNC, and AIS on the display

> **Part VIII — Charts, bridge systems, and mariners.** How official vector charts and commercial chartplotters depict the marine domain, and how dynamic AIS broadcast targets are filtered, tracked, associated with radar, and portrayed on the bridge conning display.

**In this chapter.** You will learn how electronic navigation charts are structured, certified, and integrated with live Automatic Identification System (**AIS**) broadcasts on ship bridges and piloting software. You will examine the statutory, technical, and operational boundaries separating Electronic Navigational Charts (**ENCs**), Raster Navigational Charts (**RNCs**), type-approved Electronic Chart Display and Information Systems (**ECDIS**), and uncertified Electronic Chart Systems (**ECSs**). You will trace the transition from paper charts to International Hydrographic Organization (**IHO**) S-57 and next-generation S-100/S-101 vector models. You will explore how International Electrotechnical Commission (**IEC**) standards govern AIS target symbology, operational states (sleeping, activated, selected, dangerous, and lost), heading and velocity vectors, and Closest Point of Approach (**CPA**) and Time to Closest Point of Approach (**TCPA**) collision alarms. Finally, you will evaluate radar-AIS target association, physical and virtual AIS Aids to Navigation (**AtoN**), pilot plug interfaces, and bridge alarm fatigue.

## 51.1 The evolution of electronic chart displays

For centuries, marine navigation centered on paper nautical charts. Navigators plotted dead-reckoning tracks with parallel rulers, transferred radar ranges with dividers, and hand-corrected soundings from Notices to Mariners. Satellite radionavigation—specifically the Global Positioning System (**GPS**) in the late 20th century—disrupted this craft. Watchstanders received continuous coordinates, but manually plotting positions on paper every few minutes introduced lag and cognitive friction.

The industry digitized charts in response. Early systems scanned paper charts into raster images. These **Raster Navigational Charts** (**RNCs**) preserved traditional cartography, but were inert bitmaps. A computer could not query pixels to distinguish deep water from drying reef, could not suppress soundings to declutter channels, and could not trigger automated grounding alarms when tracks crossed shallow contours.

To enable automated safety checking and dynamic display adaptation, hydrographers developed vector charts, codified internationally as **Electronic Navigational Charts** (**ENCs**). In an ENC, geographic features—rocks, buoys, depth contours, traffic lanes, anchorages—are stored as discrete database records with coordinates, geometric primitives, and structured attributes. When rendered by a compliant display processor, vector charts can be filtered by scale, rotated to match vessel heading, queried with a cursor click, and continuously interrogated by anti-grounding algorithms.

AIS introduced in the early 2000s added real-time cooperative traffic to electronic charts. Watchstanders no longer had to divide attention between paper charts, stand-alone radar, and text-based AIS Minimum Keyboard and Display (**MKD**) units ([Chapter 20](ch20-architecture-and-station-classes.md)). Live targets could be rendered directly over charted bathymetry and aids. Yet combining static hydrography with live broadcasts introduces risks: cartographic errors, geodetic datum mismatches, latencies, sensor dropouts, and screen clutter can deceive bridge officers.

## 51.2 The chart taxonomy: ENC, RNC, ECDIS, and ECS

In maritime operations and admiralty law, chart-related acronyms carry precise statutory definitions. Confusing these terms leads to regulatory non-compliance, insurance disputes, and casualties.

> **Definitions that bite.**
> - **ENC (Electronic Navigational Chart):** An official vector database conforming to IHO S-57 (or S-101) issued by or on the authority of a national hydrographic office. An ENC contains all cartographic data necessary for safe navigation and receives regular digital updates.
> - **RNC (Raster Navigational Chart):** A digital raster facsimile of an official paper chart, conforming to IHO S-61, produced by or under the authority of a national hydrographic office.
> - **ECDIS (Electronic Chart Display and Information System):** A navigation system that, with adequate back-up arrangements, complies with IMO performance standards (MSC.232(82) or MSC.530(106)) and has been certified against IEC 61174. Operating with official ENCs, an ECDIS satisfies SOLAS Chapter V chart carriage rules.
> - **ECS (Electronic Chart System):** Any digital chart navigation system that does not meet the statutory, certification, or redundancy requirements of an IMO ECDIS. An ECS does not satisfy SOLAS chart carriage requirements.
> - **ENDS (Electronic Navigational Data Service):** An umbrella regulatory concept introduced in IMO Resolution MSC.530(106) defining a special-purpose digital database compiled from official charts and publications conforming to IHO standards.

### 51.2.1 S-57 vector structure and S-52 presentation

Official ENCs in service today are formatted according to IHO Special Publication S-57 Edition 3.1.0 (November 2000). Encapsulated using ISO/IEC 8211 transfer syntax, hydrography is organized into feature and spatial components:
- **Feature records:** Represent real-world entities identified by acronyms (e.g., `DEPARE` for depth area, `LIGHTS` for a marine light, `BOYSPP` for a special-purpose buoy). Features carry attributes such as `VALSOU` (depth sounding value), `COLOUR`, and `SIGPER` (light period).
- **Spatial records:** Define geometry using 2D or 3D coordinates referenced to the World Geodetic System 1984 (**WGS-84**) datum. Spatial primitives include isolated nodes (points), connected nodes, edges (lines), and faces (polygons).

Crucially, S-57 is purely a data exchange format; it contains no instructions detailing *how* symbols, colours, or line styles appear on screen. Visual rendering is governed by an entirely separate standard: IHO Special Publication S-52, *Specifications for Chart Content and Display Aspects of ECDIS*, and its companion *Presentation Library* (PresLib Edition 4.0.4).

Separating data (S-57) from presentation (S-52) ensures hydrographic offices produce objective vector data while type-approved ECDIS renders standardized symbology, calibrated palettes, and predictable priority layers. S-52 defines three display categories:
1. **Display Base:** Minimum chart information that cannot be removed from the display under any operational condition (coastline, own-ship safety contour, isolated dangers in safe water, traffic schemes, scale, and orientation). It is not intended for safe route planning or monitoring on its own.
2. **Standard Display:** Default display presented when an ECDIS powers on. It adds drying lines, aids to navigation, fairway boundaries, landmarks, and ferry routes.
3. **All Other Information (Custom Display):** Optional layers that watchstanders can selectively toggle: spot soundings, submarine cables, depth contour labels, seabed characteristics, and magnetic variation.

S-52 also enforces standardized colour tables calibrated to preserve night vision on the bridge: `DAY`, `DUSK`, and `NIGHT` palettes. To prevent dynamic AIS and radar overlays from clashing with charted aids, S-52 reserves specific colour tokens. For example, colour token `RESBL` (a distinctive blue) is explicitly reserved for AIS and Vessel Traffic Services (**VTS**) vector lines, text, and target outlines.

```
       +-------------------------------------------------------+
       |         Official Hydrographic Office (HO)             |
       |       Produces S-57 Edition 3.1 Vector Cells          |
       |  (ISO/IEC 8211: Features [BOYSPP, DEPARE], WGS-84)    |
       +-------------------------------------------------------+
                                  |
                                  v
+---------------------------------------------------------------------+
|                  Type-Approved ECDIS (IEC 61174)                     |
|                                                                     |
|  +---------------------------+       +---------------------------+  |
|  |   IHO S-52 Presentation   |       |    IEC 62288 Symbology    |  |
|  |         Library           |       |                           |  |
|  | (Symbols, Colour Palettes |       |  (AIS sleeping/active,    |  |
|  |  DAY/NIGHT, Token RESBL)  |       |   CPA/TCPA alarms, vectors) |  |
|  +---------------------------+       +---------------------------+  |
|               \                                   /                 |
|                v                                 v                  |
|    +-----------------------------------------------------------+    |
|    |      Harmonized Navigational Conning Display Screen       |    |
|    |   [Chart Base] + [Safety Contour] + [AIS Target Overlay]  |    |
|    +-----------------------------------------------------------+    |
+---------------------------------------------------------------------+
```

### 51.2.2 The demise of raster charts: NOAA's paper chart sunset

For decades, maritime administrations maintained parallel paper charts, RNCs, and ENCs. In the United States, the National Oceanic and Atmospheric Administration (**NOAA**) Office of Coast Survey transformed this pipeline. Updating raster cells required manual patching, and managing hundreds of scales across overlapping charts diverted resources from high-resolution vector models. In November 2019, NOAA announced a five-year program to sunset all raster and paper chart production.

The program concluded in December 2024 with the cancellation of NOAA Chart 18649 (Entrance to San Francisco Bay), terminating a portfolio of 1,007 paper charts. NOAA transitioned entirely to a standardized, seamless gridded ENC database scheme (the Rescheme project), replacing arbitrary chart footprints with rectangular metric ENC cells organized across systematic usage bands. For mariners requiring hard-copy backups, NOAA launched the NOAA Custom Chart (**NCC**) application, a cloud-based engine that extracts vector features directly from the live ENC database and renders customized, printable PDF charts on demand.

### 51.2.3 SOLAS Chapter V and ECDIS carriage requirements

Under Regulation 19.2 of SOLAS Chapter V, all passenger ships of 500 gross tonnage (**GT**) and upward, and all cargo ships of 3,000 GT and upward on international voyages, are subject to mandatory ECDIS carriage. The phase-in schedule began in July 2012 for passenger ships and tankers and concluded in July 2018 for existing cargo ships.

To legally navigate paperless, a vessel must satisfy three conditions:
1. **Type-Approved Hardware and Software:** The installed ECDIS must be type-approved against IEC 61174, satisfying IMO Resolution MSC.232(82) or MSC.530(106).
2. **Official, Up-to-Date ENCs:** The vessel must navigate using official ENCs maintained with weekly Notice to Mariners updates from authorized Regional ENC Coordinating Centres (**RENCs**).
3. **Mandatory Redundancy / Independent Backup:** The vessel must carry an approved independent backup under SOLAS Regulation V/19.2.1.5: a second independent type-approved ECDIS (with independent power and GNSS) or an approved portfolio of updated paper charts covering the voyage.

When an ECDIS operates in **Raster Chart Display System** (**RCDS**) mode—navigating where official ENC coverage is unavailable and official RNCs must be loaded—it ceases to satisfy full SOLAS chart carriage requirements on its own, mandating an appropriate portfolio of paper charts.

## 51.3 Bridge systems: ECDIS vs ECS vs small-craft chartplotters

The operational landscape divides bridge displays into three tiers based on hardware integrity, software certification, and interface rigor.

| Parameter | Type-Approved ECDIS | Commercial ECS | Small-Craft Chartplotter |
| :--- | :--- | :--- | :--- |
| **Primary Standard** | IEC 61174 / MSC.232(82) / MSC.530(106) | ISO 19379 / RTCM 10900.7 | Proprietary manufacturer specs |
| **Chart Data Format** | Official S-57 / S-101 ENCs only | Official ENCs or commercial formats | Proprietary vector formats |
| **SOLAS Compliance** | Full (with approved backup) | Non-compliant (supplementary only) | Non-compliant |
| **AIS Symbology** | Strictly IEC 62288 / SN.1/Circ.243 | Partially IEC 62288 or custom | Highly customized, non-standard |
| **Operating System** | Hardened, locked industrial OS | Commercial OS (Windows, Android, iOS) | Embedded RTOS or proprietary Linux |
| **Sensor Interfaces** | Redundant IEC 61162 serial/Ethernet | Serial NMEA 0183, USB, Wi-Fi | NMEA 0183, NMEA 2000, Wi-Fi |
| **Alarm Management** | IEC 62923-1/-2 BAM centralized | Standalone audio beeps / popups | Simple visual alerts / single tone |

### 51.3.1 Hardware integrity and software locking

A type-approved ECDIS is an industrial appliance tested under IEC 60945:
- **Thermal and vibration resilience:** Hardware operates from $-15^\circ\text{C}$ to $+55^\circ\text{C}$ on enclosed bridges, surviving ship vibrations and power bus transients.
- **Display luminescence and colour calibration:** Displays maintain chromaticity coordinates across daylight, dusk, and night regimes, keeping red buoys, green beacons, and blue AIS vectors distinct.
- **Operating system lockdown:** Under IEC 61174, the operating system is locked against unauthorized software, malware insertion, and background service interruptions.

In contrast, commercial ECS software often runs on commercial off-the-shelf (**COTS**) laptops, ruggedized tablets, or uncertified marine monitors. While ECS platforms provide flexibility for tugs, workboats, fishing vessels, and marine pilots, they lack statutory type approval and cannot legally replace paper charts on SOLAS-mandated vessels.

## 51.4 AIS on the display: symbology and operational states

When an AIS receiver captures Message 1, 2, 3, 18, or 19 position reports over the VHF Data Link (**VDL**), it outputs formatted `!AIVDM` sentences across an IEC 61162 interface to the ECDIS processor ([Chapter 26](ch26-interfaces-and-logging.md)). The ECDIS parses these packets, reconciles coordinates with its geodetic projection model, and renders the target over the vector chart.

Target portrayal is governed by **IEC 62288** (*Presentation of navigation-related information on shipborne navigational displays*) and IMO Circular **SN.1/Circ.243/Rev.2**.

```
   Sleeping Target         Activated Target          Dangerous Target
        /\                       /\                        / \
       /  \                     / | \                     / ! \
      /    \                   /  |  \                   /_____\
     /______\                 /___|___\                  (Flashing Red)
                            (Course Vector)
                                
   Selected Target            Lost Target           Physical AIS AtoN
     +------+                     /\                       /\
     |  /\  |                    /  \                     /  \
     | /  \ |                   / \/ \                   [    ]
     |/____\|                  /  /\  \                   \  /
     +------+                 /_______ \                   \/
    (Data Box Active)        (Strikethrough)          (Diamond on mark)
```

### 51.4.1 Target operational states under IEC 62288

To manage cognitive load and prevent screen saturation, IEC 62288 establishes five discrete operational states for mobile AIS targets:

1. **Sleeping Target:** Rendered as an equilateral, isosceles triangle pointing along reported True Heading (or COG). Drawn with fine, solid lines in standard palette colour (token `RESBL`). It displays no velocity vector, no turn indicator, and no text labels, denoting vessels presenting no immediate collision hazard.
2. **Activated Target:** When entering an acquisition zone or selected manually, the triangle expands in line thickness and displays two vectors:
   - **Velocity Vector:** Projected forward from the apex along Course Over Ground (**COG**), with length proportional to Speed Over Ground (**SOG**) multiplied by vector time (e.g., a 6-minute vector displays position in six minutes).
   - **Heading and Turn Indicator:** A short perpendicular tick extending from the heading line in the direction of Rate of Turn (**ROT**), indicating dynamic rudder action.
3. **Selected Target:** Occurs when clicked or queried. A square frames the target triangle, and an adjacent window populates with verified telemetry: MMSI, vessel name, call sign, navigational status, range, bearing, COG, SOG, CPA, and TCPA.
4. **Dangerous Target (CPA/TCPA Alarm):** If projected trajectories violate preset Closest Point of Approach (**CPA**) and Time to Closest Point of Approach (**TCPA**) limits, the target flashes as an enlarged red triangle. An audible bridge alarm sounds until the collision hazard resolves.
5. **Lost Target:** If an activated AIS target ceases transmitting across a timeout threshold (typically 3 to 5 reporting intervals), a bold diagonal cross is drawn through the triangle, and a visual alert notifies the watchstander.

### 51.4.2 True scaled outlines vs. point symbols

At wide chart scales ($1:50000$ or $1:100000$), an AIS target is rendered as a point-symbol triangle. However, at high-resolution docking or harbour scales ($1:5000$ or $1:2000$), point symbols become dangerously misleading: a single point icon cannot convey whether the vessel is a 15-metre tug or a 400-metre container ship swinging across a fairway.

Under IEC 62288, when the vessel's physical hull dimensions exceed a screen threshold (typically $> 5\text{ mm}$ on screen), the ECDIS renders the target as a **scaled vessel outline**. The ECDIS derives this outline by combining static dimensions from Message 5 or Message 24 ($A$, $B$, $C$, and $D$ offsets from the GNSS antenna reference point to bow, stern, port, and starboard sides) with True Heading and dynamic GNSS coordinates. The rendered polygon reflects the true spatial footprint of the ship relative to dredged channel boundaries, bridge piers, and dock walls.

> **Definitions that bite.** *COG vs. Heading.* Watchstanders frequently confuse **Course Over Ground** with **Heading**. Course Over Ground represents the direction of motion across the seabed, incorporating wind drift and ocean current. Heading represents the orientation of the ship's centerline from its gyrocompass. In strong cross-currents, heading and COG can diverge by $20^\circ$ or more. An ECDIS renders Heading as a solid line extending from the bow apex, while the COG vector extends along the motion track. Conflating the two leads to disastrous misjudgments of an approaching ship's aspect.

## 51.5 Collision avoidance: CPA, TCPA, and radar-AIS target association

The primary tactical utility of displaying AIS on a bridge conning display is automated collision risk calculation. By continuously comparing own-ship kinematics against every received AIS position report, the ECDIS computes two fundamental collision avoidance metrics:
- **Closest Point of Approach (CPA):** Minimum distance separating vessels if neither alters course or speed, in nautical miles (**nmi**).
- **Time to Closest Point of Approach (TCPA):** Time remaining until vessels reach that minimum separation distance, in minutes.

### 51.5.1 The kinematics of CPA and TCPA calculation

Let own-ship position be $\mathbf{r}_0 = (x_0, y_0)$ with velocity $\mathbf{v}_0 = (u_0, v_0)$:
$$u_0 = \text{SOG}_0 \sin(\text{COG}_0), \quad v_0 = \text{SOG}_0 \cos(\text{COG}_0)$$
Similarly, let target position be $\mathbf{r}_t = (x_t, y_t)$ with velocity $\mathbf{v}_t = (u_t, v_t)$:
$$u_t = \text{SOG}_t \sin(\text{COG}_t), \quad v_t = \text{SOG}_t \cos(\text{COG}_t)$$

Relative position $\mathbf{r} = \mathbf{r}_t - \mathbf{r}_0 = (\Delta x, \Delta y)$ and relative velocity $\mathbf{v}_{\text{rel}} = \mathbf{v}_t - \mathbf{v}_0 = (\Delta u, \Delta v)$ define relative motion. Separation distance at future time $t$ is:
$$D(t) = \|\mathbf{r} + \mathbf{v}_{\text{rel}} t\| = \sqrt{(\Delta x + \Delta u \cdot t)^2 + (\Delta y + \Delta v \cdot t)^2}$$

Differentiating $D^2(t)$ with respect to $t$ and setting the derivative to zero yields the time of closest approach:
$$t_{\text{CPA}} = -\frac{\mathbf{r} \cdot \mathbf{v}_{\text{rel}}}{\|\mathbf{v}_{\text{rel}}\|^2} = -\frac{\Delta x \Delta u + \Delta y \Delta v}{\Delta u^2 + \Delta v^2}$$

If $t_{\text{CPA}} < 0$, the vessels are diverging; if $t_{\text{CPA}} \ge 0$, they are converging. Substituting $t_{\text{CPA}}$ back into the relative displacement equation yields separation distance at CPA:
$$D_{\text{CPA}} = \|\mathbf{r}_{\text{CPA}}\| = \sqrt{\left(\Delta x + \Delta u \cdot t_{\text{CPA}}\right)^2 + \left(\Delta y + \Delta v \cdot t_{\text{CPA}}\right)^2}$$

> **Worked example.** *Calculating CPA and TCPA between converging vessels.*
> 
> *Scenario:*
> - **Own ship:** Position $37.8000^\circ\text{ N}, 122.4000^\circ\text{ W}$; $\text{SOG}_0 = 15.0\text{ kn}$; $\text{COG}_0 = 090.0^\circ$ (East).
> - **Target ship:** Position $37.8500^\circ\text{ N}, 122.3000^\circ\text{ W}$; $\text{SOG}_t = 12.0\text{ kn}$; $\text{COG}_t = 210.0^\circ$ (SSW).
> 
> *Step 1: Cartesian relative position.*
> - Mean latitude $\phi_m = 37.8250^\circ$.
> - $\Delta x = (-122.3000 - (-122.4000)) \times 60 \times \cos(37.8250^\circ) = 4.739\text{ nmi}$ (East).
> - $\Delta y = (37.8500 - 37.8000) \times 60 = 3.000\text{ nmi}$ (North).
> 
> *Step 2: Velocity components.*
> - Own ship: $u_0 = 15.0 \sin(90^\circ) = 15.000\text{ kn}$; $v_0 = 15.0 \cos(90^\circ) = 0.000\text{ kn}$.
> - Target ship: $u_t = 12.0 \sin(210^\circ) = -6.000\text{ kn}$; $v_t = 12.0 \cos(210^\circ) = -10.392\text{ kn}$.
> - Relative: $\Delta u = -21.000\text{ kn}$; $\Delta v = -10.392\text{ kn}$; $\|\mathbf{v}_{\text{rel}}\| = 23.431\text{ kn}$.
> 
> *Step 3: TCPA.*
> - $\mathbf{r} \cdot \mathbf{v}_{\text{rel}} = (4.739)(-21.000) + (3.000)(-10.392) = -130.695\text{ nmi}\cdot\text{kn}$.
> - $t_{\text{CPA}} = -(-130.695) / (23.431)^2 = 0.23806\text{ h} = 14.28\text{ min}$.
> 
> *Step 4: CPA distance.*
> - $\Delta x_{\text{CPA}} = 4.739 + (-21.000)(0.23806) = -0.260\text{ nmi}$.
> - $\Delta y_{\text{CPA}} = 3.000 + (-10.392)(0.23806) = 0.526\text{ nmi}$.
> - $D_{\text{CPA}} = \sqrt{(-0.260)^2 + (0.526)^2} = 0.59\text{ nmi}$.
> 
> *Conclusion:* Target crosses ahead at CPA $0.59\text{ nmi}$ in $14.3\text{ min}$, triggering dangerous target alarms where threshold $\text{CPA} \le 1.0\text{ nmi}$ and $\text{TCPA} \le 15.0\text{ min}$.

> **Try it.** Verify collision metrics using Python:
> ```python
> import math
> 
> def calculate_cpa(lat1, lon1, sog1, cog1, lat2, lon2, sog2, cog2):
>     mid_lat = math.radians((lat1 + lat2) / 2.0)
>     dx = (lon2 - lon1) * 60.0 * math.cos(mid_lat)
>     dy = (lat2 - lat1) * 60.0
>     u1, v1 = sog1 * math.sin(math.radians(cog1)), sog1 * math.cos(math.radians(cog1))
>     u2, v2 = sog2 * math.sin(math.radians(cog2)), sog2 * math.cos(math.radians(cog2))
>     du, dv = u2 - u1, v2 - v1
>     v_rel_sq = du**2 + dv**2
>     if v_rel_sq < 1e-9:
>         return math.hypot(dx, dy), 0.0
>     tcpa_h = -(dx * du + dy * dv) / v_rel_sq
>     tcpa_min = tcpa_h * 60.0
>     cpa_dist = math.hypot(dx + du * tcpa_h, dy + dv * tcpa_h)
>     return cpa_dist, tcpa_min
> 
> dist, tcpa = calculate_cpa(37.80, -122.40, 15.0, 90.0, 37.85, -122.30, 12.0, 210.0)
> print(f"CPA: {dist:.2f} nmi, TCPA: {tcpa:.1f} min")
> # Expected output:
> # CPA: 0.59 nmi, TCPA: 14.3 min
> ```

### 51.5.2 Radar and AIS target association (IEC 62388)

Modern Integrated Navigation Systems (**INS**) combine two independent sensor streams for traffic tracking:
1. **Radar / ARPA (IEC 62388):** Non-cooperative microwave reflections measuring range and bearing from physical pulse echoes, independent of target configuration. Radar is vulnerable to sea clutter, rain attenuation, aspect fading, and track loss during maneuvers.
2. **AIS (IEC 61993-2):** Cooperative VHF broadcasts delivering vessel identity, dimensions, status, rate of turn, and GNSS kinematics without tracking lag. AIS is vulnerable to GNSS faults, gyrocompass failure, uncalibrated antenna offsets, and spoofing.

When both sensors detect the same vessel, rendering both an ARPA tracked circle and an AIS triangle creates visual doubles. To eliminate this ambiguity, **IEC 62388** and **IEC 62288** establish mathematical criteria for **target association**.

Under IEC 62388 Clause 9.3, a radar tracking processor evaluates target pairs against three dynamic gating thresholds:
- **Spatial separation gate:** Positional difference between radar range/bearing and AIS position must fall within a dynamic gating ellipse, accounting for radar beamwidth, range resolution, and antenna offsets ($A, B, C, D$).
- **Kinematic velocity gate:** Difference between radar-calculated course/speed and AIS-reported COG/SOG must not exceed predefined velocity tolerance gates.
- **Vector alignment gate:** Directional vectors must converge within specified angular bounds over a configured observation window (typically 30 to 60 seconds).

When two tracks satisfy all three criteria, the ECDIS fuses them into a single **associated target symbol**: an AIS triangle enclosing a small circle.

```
       Radar Return (ARPA Circle)       AIS Report (Triangle)
                   O                             /\
                    \                           /  \
                     \                         /____\
                      \                         /
                       +------- Spatial Gate --+
                                    |
                                    v
                     Associated Target Symbol (Enclosed)
                                  / \
                                 / O \
                                /_____\
                             (Single Track)
```

Crucially, IEC 62388 requires an explicit hierarchy for vector rendering. The watchstander can configure the display to default to radar vectors (echo physics) or AIS vectors (GNSS kinematics). If a target turns sharply, the radar echo tracks physical movement immediately, whereas AIS latency or rate-of-turn sensor lag may temporarily distort the AIS vector until the next packet arrives. If tracks diverge beyond gating bounds, the system instantly disassociates the targets, rendering them once again as separate radar and AIS symbols accompanied by an operational alert.

## 51.6 AIS Aids to Navigation (AtoN) depiction

Beyond vessel tracking, AIS is utilized by lighthouse authorities and coast guards to broadcast the positions, status, and identities of Aids to Navigation (**AtoN**) using AIS Message 21 ([Chapter 22](ch22-message-catalog.md) and [Chapter 68](ch68-special-purpose-ais.md)).

Under IALA Recommendation R0126 and IEC 62288, AIS AtoN broadcasts fall into three operational categories:
1. **Physical AIS AtoN:** An actual transceiver mounted on a physical buoy, beacon, or lighthouse, transmitting Message 21 confirming its position, operational status, and off-station state.
2. **Synthetic AIS AtoN:** A physical aid without an onboard transmitter whose position and status are monitored remotely and broadcast over the VDL by a coastal base station.
3. **Virtual AIS AtoN:** A digital aid with *no physical structure* in the water. A base station transmits Message 21 specifying coordinates to mark emergent hazards (e.g., newly discovered wrecks or temporary fairway diversions).

### 51.6.1 Cartographic collision: S-52 vs IEC 62288

Depicting AIS AtoNs on an ECDIS creates a cartographic collision between static hydrographic features (S-52) and dynamic broadcast overlays (IEC 62288).

In an S-57 ENC, buoys and beacons are encoded as static features (`BOYSPP`, `BOYLAT`, `BCNLAT`) with detailed attributes. S-52 renders these features using traditional nautical chart symbols (e.g., a magenta diamond for a buoy).

When an AIS Message 21 is received for that buoy, IEC 62288 renders the aid as a green diamond with an open center placed over the reported coordinates:
- For a **physical AtoN**, the green diamond encloses the charted S-52 buoy symbol. If the buoy drags anchor, the S-52 symbol remains frozen at charted coordinates while the green diamond moves dynamically with an `AtoN Off-Position` alarm.
- For a **virtual AtoN**, IEC 62288 mandates that a small letter "V" be displayed inside or adjacent to the green diamond, informing the conning officer that no physical seamark exists in the water.

```
       Physical AIS AtoN                    Virtual AIS AtoN
              /\                                  /\
             /  \                                /  \
            [ S  ]                              [ V  ]
             \  /                                \  /
              \/                                  \/
     (Encloses Charted Mark)            (No Physical Seamark Exists)
```

Virtual AtoNs present severe navigational hazards. If an authority marks a shoal using a virtual buoy, mariners navigating on older plotters or un-updated software that cannot decode Message 21 will see *nothing* on their displays. Conversely, watchstanders who navigate purely visually may alter course expecting to see a lighted mark, only to run aground in darkness.

## 51.7 Pilot plugs, Portable Pilot Units (PPUs), and small craft

AIS display technology extends beyond fixed bridge consoles into portable commercial piloting systems and recreational marine electronics.

### 51.7.1 The AIS pilot plug interface

Under IMO MSC/Circ.982 and SN/Circ.227, every Class A AIS installation on a SOLAS vessel must provide an **AIS Pilot Plug** near the primary conning position: a standardized AMP 206486-1 connector with a 5-pin layout providing differential RS-422 data at 38,400 bit/s under IEC 61162-2:
- **Pin 1:** Transmit A (`TxA`)
- **Pin 2:** Transmit B (`TxB`)
- **Pin 3:** Shield
- **Pin 4:** Receive A (`RxA`)
- **Pin 5:** Receive B (`RxB`)

When a pilot boards a commercial ship, they connect a **Portable Pilot Unit** (**PPU**)—a ruggedized tablet running hydrographic software (such as Qastor or SEAiq) paired with a wireless bridge adapter plugged into the pilot plug.

The PPU allows pilots to navigate using trusted software independent of ship bridge consoles. High-precision PPUs incorporate dual-antenna Real-Time Kinematic (**RTK**) GNSS pods and rate sensors on bridge wings, transmitting RTK corrections and heading to the tablet to monitor docking velocities with millimeter-per-second precision.

> **Case file.** *The Francis Scott Key Bridge Allision (Containership Dali).*
> On 26 March 2024, the Singapore-flagged 9,962 TEU container ship *Dali* suffered catastrophic electrical blackouts while outbound from the Port of Baltimore, leading to allision with Pier 17 of the Francis Scott Key Bridge and the collapse of the bridge truss.
> 
> As documented in the National Transportation Safety Board (**NTSB**) preliminary report (DCA24MM031), boarding maritime pilots utilized a Portable Pilot Unit connected to the vessel's navigation infrastructure. During the blackout of the ship's main switchboard, fixed radar and ECDIS consoles lost power and restarted into boot sequences. However, the pilot's standalone, battery-powered PPU continued operating uninterrupted on the conning bridge, logging high-rate positioning, heading, and course data that provided investigators with crucial forensic telemetry during the seconds when bridge consoles were dark.

### 51.7.2 Recreational chartplotters and ECS limitations

On small craft and recreational yachts, navigation displays are uncertified **Electronic Chart Systems** (**ECSs**) or Multi-Function Displays (**MFDs**) from manufacturers such as Garmin, Raymarine, Navico, and Furuno.

While modern MFDs boast bright touchscreens, their AIS integration departs from international standards:
- **Non-standard symbology:** Plotters often replace IEC 62288 target triangles with boat silhouettes or arrow icons that obscure true heading and rate-of-turn indicators.
- **Aggressive target filtering:** Leisure plotters frequently enable background filtering, hiding Class B targets or suppressing targets beyond two miles without clear warnings.
- **Unvalidated cartography:** Plotters often display proprietary crowd-sourced bathymetry rather than official ENCs, omitting temporary dredging operations or shoaling notices.

## 51.8 The human factor: alarm fatigue and display clutter

Integrating AIS onto electronic charts significantly enhances situational awareness, but introduces acute failure modes: display clutter and alarm fatigue.

### 51.8.1 Display clutter in congested waterways

In confined channels—such as the Dover Strait or Singapore Strait—an AIS receiver routinely tracks 500 to 1,500 active targets simultaneously ([Chapter 30](ch30-network-loading-packet-loss.md)). If every target displays velocity vectors, ship names, heading lines, and predictor paths, the screen degrades into an unreadable mass of overlapping graphics.

Under such conditions, charted hazards—isolated rocks, clearing lines, shallow contours—become obscured beneath overlapping target symbols. Watchstanders suffer cognitive overload, losing ability to prioritize collision threats among hundreds of moored vessels.

To combat clutter, IEC 61174 and IEC 62288 mandate **target filtering controls**. An ECDIS allows operators to configure sleeping targets to disappear beyond a specific range, hide distant Class B transponders, or suppress text labels until queried. However, improper filters introduce deadly blind spots: an inattentive watchstander configuring a 3-mile range filter completely suppresses an approaching container ship steaming at 24 knots that will close that distance in seven minutes.

```
+-----------------------------------------------------------------------+
|  IEC 62923-1 Bridge Alert Management (BAM) Classification Hierarchy   |
+-----------------------------------------------------------------------+
|                                                                       |
|  [EMERGENCY ALARM]  -> Highest priority; immediate danger to life/ship|
|                                                                       |
|  [ALARM]            -> Requires immediate attention/action to avoid   |
|                        imminent danger (e.g., CPA/TCPA violation,     |
|                        imminent shallow contour grounding).           |
|                        Audible + flashing red symbol.                 |
|                                                                       |
|  [WARNING]          -> Requires immediate knowledge, not necessarily  |
|                        immediate action (e.g., Target Lost,           |
|                        Differential GNSS lost). Audible / yellow.     |
|                                                                       |
|  [CAUTION]          -> Awareness of an abnormal condition; no action  |
|                        required immediately (e.g., poor sensor DOP,   |
|                        Class B transmission deferral). Silent visual. |
|                                                                       |
+-----------------------------------------------------------------------+
```

### 51.8.2 Alarm fatigue and Bridge Alert Management (BAM)

The most severe operational challenge associated with bridge AIS displays is **alarm fatigue**. In early ECDIS and radar installations, every sensor failure, timeout, and proximity calculation triggered an unharmonized audible buzzer.

In busy waters, an ECDIS could generate dozens of audible alarms every hour: anchor swings within normal chain scope, "Target Lost" warnings for Class B fishing boats dropping behind headlands, and CPA/TCPA alerts for moored vessels along parallel wharves. Faced with continuous audible alarms, watchstanders develop psychological numbness, reflexively silencing alarms without reading alert text or turning audio buzzers to zero.

To resolve this crisis, the IMO adopted Resolution **MSC.302(87)**, standardized internationally as **IEC 62923-1** and **IEC 62923-2** (*Bridge Alert Management*). Under BAM:
- Bridge alarms are centralized across a hierarchy categorized into **Alarms** (immediate action required), **Warnings** (immediate knowledge required), and **Cautions** (awareness of abnormal conditions).
- Nuisance alarms are strictly curbed: an ECDIS certified under IEC 62923 is prohibited from sounding audible alarms for lost sleeping targets or non-threatening moored vessels.
- Standardized Alert Acknowledge (`ACK`) and Alert Command (`ACN`) sentences allow watchstanders to acknowledge alerts at a central console.

## Then & now

- ⟨H⟩ **1986:** The North Sea Hydrographic Commission establishes a study group to investigate digital electronic chart displays, leading to the creation of the IHO Committee on ECDIS (**COE**).
- ⟨+⟩ **1995:** The IMO adopts Resolution A.817(19), establishing the first international Performance Standards for Electronic Chart Display and Information Systems (**ECDIS**).
- ⟨H⟩ **November 1996:** The IHO publishes Edition 3.0 of Special Publication S-57 (*IHO Transfer Standard for Digital Hydrographic Data*), freezing the core vector data structure for maritime hydrography.
- ⟨+⟩ **November 2000:** The IHO releases S-57 Edition 3.1.0, introducing enhanced object catalogues and encapsulation rules that serve as the foundation for modern operational ENCs.
- ⟨+⟩ **July 2002:** SOLAS Chapter V amendments enter into force, mandating the carriage of Automatic Identification Systems (**AIS**) on commercial vessels over 300 GT, sparking the need to display dynamic targets over nautical charts.
- ⟨+⟩ **December 2006:** The IMO adopts Resolution MSC.232(82), establishing revised ECDIS performance standards that incorporate mandatory radar and AIS target overlay capabilities.
- ⟨+⟩ **July 2012:** Mandatory SOLAS ECDIS carriage enters into force under a staged six-year implementation schedule spanning 2012 to 2018.
- ⟨+⟩ **October 2014:** The IHO issues S-52 Edition 6.1.1 and Presentation Library Edition 4.0.0, overhauling chart symbol libraries, introducing colour calibration checks, and reserving colour token `RESBL` for AIS targets.
- ⟨+⟩ **August 2015:** The IEC publishes IEC 61174 Edition 4.0, formalizing type-approval test specifications for ECDIS handling of AIS overlays, route transfers, and Bridge Alert Management interfaces.
- ⟨+⟩ **November 2022:** The IMO adopts Resolution MSC.530(106), defining next-generation performance standards for **S-100 ECDIS**, introducing the concept of Electronic Navigational Data Services (**ENDS**), and setting voluntary transition dates for 2026 and mandatory adoption for new ship installations on 1 January 2029.
- ⟨+⟩ **December 2024:** NOAA completes the five-year sunset of its entire portfolio of 1,007 traditional paper and raster nautical charts, transitioning the United States exclusively to gridded electronic navigational charts and digital custom chart generation.

## Validation, uncertainty & data quality

Errors on an electronic chart display arise from three distinct sources: hydrographic source survey limitations, cartographic encoding ambiguities, and dynamic sensor telemetric latency.

### The hydrographic baseline: CATZOC and S-57 data quality

Bridge watchstanders often mistakenly treat an official ENC as ground truth with infinite precision. In reality, vector chart data aggregates historical hydrographic surveys dating from Victorian lead-lines to modern multi-beam sonar sweeps.

In S-57 ENCs, bathymetric data quality is encoded in the `M_QUAL` meta-feature using the **Category of Zone of Confidence** (**CATZOC**) attribute:
- **CATZOC A1:** Position accuracy $\pm 5\text{ m}$; full seafloor ensonification; depth accuracy $\pm (0.50 + 0.01 \times \text{depth})\text{ m}$. Safe with minimal under-keel clearance.
- **CATZOC A2:** Position accuracy $\pm 20\text{ m}$; full seafloor coverage; depth accuracy $\pm (1.00 + 0.02 \times \text{depth})\text{ m}$.
- **CATZOC B:** Position accuracy $\pm 50\text{ m}$; full seafloor search not achieved; depth accuracy $\pm (1.00 + 0.02 \times \text{depth})\text{ m}$.
- **CATZOC C:** Position accuracy $\pm 500\text{ m}$; depth accuracy $\pm (2.00 + 0.05 \times \text{depth})\text{ m}$; depth anomalies likely.
- **CATZOC D:** Position accuracy $> 500\text{ m}$; depths unreliable; uncharted shoals may exist.
- **CATZOC U:** Data unassessed.

If an ECDIS renders an AIS target over a shallow reef in a CATZOC C or D area, the true physical location of that reef could be displaced by 500 metres from its rendered position. Calculating under-keel clearance or passing distances against charted contours without checking the underlying CATZOC rating leads directly to grounding casualties.

### Sensor latency and dynamic vector uncertainty

Dynamic AIS target vectors displayed on an ECDIS carry intrinsic mathematical uncertainty. An AIS position report broadcast over the VDL is not instantaneous; it represents a discrete sampling of vessel state at a specific epoch $t_0$.

Under IEC 61993-2, Class A reporting intervals vary dynamically based on navigational status and speed:
- At anchor or moored: every 3 minutes (or 10 seconds if moving $> 3\text{ kn}$).
- Underway at $0$ to $14\text{ kn}$: every 10 seconds (every 3.3 seconds if altering course).
- Underway at $14$ to $23\text{ kn}$: every 6 seconds (every 2 seconds if altering course).
- Underway at $> 23\text{ kn}$: every 2 seconds.

Between reporting epochs, an ECDIS either holds targets stationary or extrapolates position via dead reckoning along reported COG and SOG. If a container ship steaming at 24 kn ($12.35\text{ m/s}$) initiates a hard rudder turn after transmitting an AIS burst, the ECDIS projects its position along its old straight-line track for 2 to 10 seconds. In 6 seconds, the vessel displaces over 74 metres from its projected line. If the AIS packet is lost to RF packet collision or interference, extrapolation error compounds linearly until the next packet arrives.

Furthermore, dynamic AIS coordinates are generated by the target's internal Electronic Position Fixing System (**EPFS**). Standard single-frequency GPS carries a 95% horizontal positioning error of approximately $3\text{ to }5\text{ m}$. If the transmitting vessel has improperly configured its GNSS antenna offset dimensions ($A, B, C, D$), the rendered hull box can be displaced by hundreds of metres, leading to catastrophic errors during close-quarters overtaking in dredged channels.

## Software

**Open source:**
- **OpenCPN:** Open-source chart navigation software supporting S-57 ENCs, encrypted S-63 ENCs, raster charts, and AIS overlays via serial and network links. Caveat: ECS only; not type-approved against IEC 61174; cannot satisfy SOLAS carriage.
- **libislands (and s57dec):** Open-source libraries parsing ISO/IEC 8211 encapsulated S-57 data cells into geometric primitives and tables. Caveat: Does not implement S-52 Presentation Library conditional display rules or colour palettes.
- **pyais:** Python library decoding NMEA 0183 `!AIVDM` and `!AIVDO` sentences into structured payloads for maritime GIS pipelines. Caveat: Bit decoder only; provides no spatial indexing or cartographic rendering.

**Free but closed:**
- **NOAA Custom Chart (NCC):** Cloud service rendering printable high-resolution PDF nautical charts on demand from NOAA live ENC vector data. Caveat: Produces static raster PDF charts without dynamic AIS targets or automated digital updates.

**Commercial:**
- **Furuno FEA / FMD Series ECDIS:** Type-approved commercial ECDIS complying with IEC 61174 and IEC 62288, featuring radar-AIS target association and BAM alert handling. Caveat: Proprietary industrial hardware with locked operating system environments.
- **Wärtsilä Navi-Sailor (Transas) ECDIS:** Type-approved ECDIS providing route monitoring, hydrographic data management, and tactical AIS overlays. Caveat: Requires proprietary security dongles and paid annual chart subscriptions.
- **Qastor / SEAiq Pilot:** Professional Portable Pilot Unit software running on ruggedized tablets, interfacing directly with shipboard pilot plugs. Caveat: Requires commercial enterprise licensing and external pilot plug or RTK sensor feeds.

## Standards & guides

- **IMO Resolution A.817(19) (1995):** *Performance Standards for ECDIS*. First-generation ECDIS statutory baseline.
- **IMO Resolution MSC.232(82) (2006):** *Revised Performance Standards for ECDIS*. Classical ECDIS baseline, mandating radar and AIS overlays.
- **IMO Resolution MSC.530(106) (2022, amended 2024 by Rev.1):** *Performance Standards for ECDIS*. Baseline for S-100 ECDIS, ENDS, and dual-fuel operation.
- **IMO Resolution MSC.191(79) / MSC.466(101) (2004/2019):** *Presentation of Navigation-Related Information*. Harmonizes radar, ECDIS, and conning layouts.
- **IMO Circular SN.1/Circ.243/Rev.2 (2019):** *Presentation of Navigation-Related Symbols, Terms and Abbreviations*. Standardizes navigation symbols and AIS target states.
- **IHO S-57 (Edition 3.1.0, 2000):** *Transfer Standard for Digital Hydrographic Data*. Governs ENC feature catalogues and ISO/IEC 8211 encapsulation.
- **IHO S-52 (Edition 6.1.1, 2014):** *Specifications for Chart Content and Display Aspects of ECDIS*. Governs display rules and Presentation Library symbology.
- **IHO S-66 (Edition 2.0.0, 2024):** *Facts about Electronic Charts and Carriage Requirements*. Authoritative guide distinguishing ENC, RNC, ECDIS, and ECS.
- **IEC 61174:2015 (Edition 4.0):** *ECDIS -- Operational and Performance Requirements, Methods of Testing and Required Test Results*. Type-approval test standard.
- **IEC 62288:2021 (Edition 3.0):** *Presentation of Navigation-Related Information on Shipborne Displays*. Governs target symbology and operational states.
- **IEC 62388:2013 (Edition 2.0):** *Shipborne Radar*. Establishes mathematical gating criteria for radar and AIS target association.
- **IEC 62923-1:2018:** *Bridge Alert Management*. Centralizes bridge alert hierarchies and eliminates nuisance alarms.

## Pitfalls

- **Confusing ECDIS with ECS:** Assuming that installing commercial chartplotter software on a laptop or wheelhouse tablet satisfies SOLAS Chapter V chart carriage rules. An ECS lacks statutory type approval, redundant power isolation, and fail-safe sensor testing.
- **Treating the safety contour as an absolute line:** Believing that an ECDIS safety contour represents a perfectly surveyed underwater boundary. Depth contours in an ENC are derived from discrete historical soundings; navigating dangerously close to a contour in low-CATZOC waters risks immediate grounding.
- **Conflating COG vectors with Heading lines:** Misinterpreting an AIS target's Course Over Ground vector as the direction the ship is pointing. In heavy cross-currents or drift conditions, heading and COG diverge substantially, leading to flawed collision avoidance maneuvers under COLREGs.
- **Relying on AIS targets while ignoring untracked craft:** Assuming that every vessel in the vicinity appears on the ECDIS screen. Warships, non-mandatory fishing boats, and wooden or fiberglass leisure vessels frequently do not carry or transmit AIS.
- **Overlooking antenna offset misconfiguration:** Trusting rendered scaled vessel outlines during close docking maneuvers without verifying the transmitting ship's Message 5 antenna dimension offsets. An inverted $A/B$ dimension can shift a 400 m hull outline hundreds of metres from its true physical footprint.
- **Disabling alarms due to fatigue:** Silencing or disabling CPA/TCPA audible alarms on an ECDIS due to continuous nuisance alerts in congested waterways, eliminating the bridge's automated fail-safe protection against high-speed collision threats.
- **Excessive target filtering:** Configuring aggressive AIS display filters (such as hiding targets beyond 3 nmi) to declutter the display, inadvertently masking fast-closing container ships or approaching pilot launches.
- **Blind trust in Virtual AIS AtoNs:** Navigating solely by electronic chart display and assuming a virtual AIS buoy represents a physical structure in the water, leading to disorientation during visual watchkeeping or when piloting unequipped vessels.
- **Navigating on unauthorized or outdated charts:** Running commercial vector charts that have not received official weekly Notice to Mariners updates, missing critical newly charted wrecks, dredging zones, or temporary navigational restrictions.
- **Assuming radar and AIS fusion is infallible:** Believing that target association under IEC 62388 never misidentifies targets. In dense clusters, adjacent radar echoes can associate with the wrong AIS tracks, swapping target identities and producing corrupted velocity vectors.

## Key takeaways

- Electronic chart navigation relies on vector ENCs (IHO S-57 / S-101), which separate digital spatial database records from visual rendering rules (IHO S-52 / S-100).
- To legally satisfy SOLAS Chapter V paperless chart carriage requirements, a vessel must navigate using a type-approved ECDIS (IEC 61174) running official, up-to-date ENCs with an approved independent backup. Uncertified systems are legally classified as ECSs and cannot replace paper charts.
- NOAA officially terminated its entire 1,007-chart portfolio of traditional paper and raster nautical charts in December 2024, transitioning the United States entirely to digital ENCs and custom printable charts.
- Under IEC 62288 and IMO SN.1/Circ.243/Rev.2, AIS targets transition through five standardized operational states: sleeping, activated, selected, dangerous (violating CPA/TCPA thresholds), and lost.
- AIS target symbology uses equilateral triangles; at large chart scales, the ECDIS renders true scaled vessel outlines derived from static Message 5 antenna offset dimensions.
- Target association algorithms (IEC 62388) mathematically fuse non-cooperative radar tracks with cooperative AIS broadcasts using spatial, kinematic, and vector gating ellipses to prevent confusing screen doubles.
- AIS Message 21 enables the portrayal of physical, synthetic, and virtual Aids to Navigation; virtual AtoNs mark emergent hazards without physical buoy structures but are completely invisible to mariners lacking modern AIS displays.
- Licensed pilots interface their independent Portable Pilot Units (PPUs) directly into shipboard Class A AIS installations via the standardized RS-422 pilot plug conning port.
- Unchecked AIS targets cause acute bridge screen clutter and alarm fatigue, necessitating strict target filtering and centralized Bridge Alert Management under IEC 62923.
- Next-generation S-100 ECDIS (IMO Resolution MSC.530(106)) introduces the Electronic Navigational Data Service (ENDS) framework, mandating dual-fuel S-57/S-101 processing for new ship installations beginning 1 January 2029.

## References

- Harati-Mokhtari, A., Wall, A., Brooks, P., Wang, J. (2007). Automatic Identification System (AIS): Data Reliability and the Human Element Implications. *The Journal of Navigation*, 60(1):87–96.
- International Association of Marine Aids to Navigation and Lighthouse Authorities (2021). *The Use of AIS in Marine Aids to Navigation Services* (Recommendation R0126, Edition 2.0). Saint-Germain-en-Laye: IALA.
- International Electrotechnical Commission (2013). *IEC 62388:2013: Shipborne Radar -- Performance Requirements, Methods of Testing and Required Test Results* (Edition 2.0). Geneva: IEC.
- International Electrotechnical Commission (2015). *IEC 61174:2015: Electronic Chart Display and Information System (ECDIS) -- Operational and Performance Requirements, Methods of Testing and Required Test Results* (Edition 4.0). Geneva: IEC.
- International Electrotechnical Commission (2018). *IEC 62923-1:2018: Bridge Alert Management -- Part 1: Operational and Performance Requirements, Methods of Testing and Required Test Results* (Edition 1.0). Geneva: IEC.
- International Electrotechnical Commission (2021). *IEC 62288:2021: Presentation of Navigation-Related Information on Shipborne Navigational Displays* (Edition 3.0). Geneva: IEC.
- International Hydrographic Organization (2000). *IHO Transfer Standard for Digital Hydrographic Data* (Special Publication S-57, Edition 3.1.0). Monaco: IHO.
- International Hydrographic Organization (2014). *Specifications for Chart Content and Display Aspects of ECDIS* (Special Publication S-52, Edition 6.1.1). Monaco: IHO.
- International Hydrographic Organization (2014). *IHO ECDIS Presentation Library* (Special Publication S-52 Annex A, Edition 4.0.4). Monaco: IHO.
- International Hydrographic Organization (2024). *Facts about Electronic Charts and Carriage Requirements* (Special Publication S-66, Edition 2.0.0). Monaco: IHO.
- International Hydrographic Organization (2024). *Electronic Navigational Chart (ENC) Product Specification* (Product Specification S-101, Edition 2.0.0). Monaco: IHO.
- International Hydrographic Organization (2025). *Universal Hydrographic Data Model* (Special Publication S-100, Edition 5.2.1). Monaco: IHO.
- International Maritime Organization (2004). *Performance Standards for the Presentation of Navigation-Related Information on Shipborne Navigational Displays* (Resolution MSC.191(79)). London: IMO.
- International Maritime Organization (2006). *Adoption of the Revised Performance Standards for Electronic Chart Display and Information Systems (ECDIS)* (Resolution MSC.232(82)). London: IMO.
- International Maritime Organization (2015). *Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems (AIS)* (Resolution A.1106(29)). London: IMO.
- International Maritime Organization (2019). *Guidelines for the Presentation of Navigation-Related Symbols, Terms and Abbreviations* (Circular SN.1/Circ.243/Rev.2). London: IMO.
- International Maritime Organization (2022). *Performance Standards for Electronic Chart Display and Information Systems (ECDIS)* (Resolution MSC.530(106)). London: IMO.
- Marine Accident Investigation Branch (2004). *Report on the Investigation of the Grounding of Attilio Ievoli on the Lymington Bank in the Western Approaches to the Solent on 3 June 2004* (Report No. 24/2004). Southampton: MAIB.
- National Oceanic and Atmospheric Administration (2024). *Farewell to Traditional Nautical Charts*. Silver Spring: NOAA Office of Coast Survey.
- National Transportation Safety Board (2024). *Contact of Containership Dali with the Francis Scott Key Bridge and Subsequent Bridge Collapse* (Preliminary Report DCA24MM031). Washington, D.C.: NTSB.
