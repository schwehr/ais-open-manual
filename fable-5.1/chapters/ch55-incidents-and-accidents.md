# Chapter 55 — AIS-assisted incidents and accidents

> **Part VIII — Charts, bridge systems, and mariners.** How over-reliance, sensor misinterpretation, filtering artifacts, and unverified data from the Automatic Identification System have caused or compounded major maritime casualties, and how forensic analysis and AIS search-and-rescue beacons establish accountability and preserve human life at sea.

**In this chapter.** You will learn how the Automatic Identification System (**AIS**) interacts with bridge watchkeeping psychology, navigation workflows, and maritime casualty dynamics. You will examine the legal baseline of Rule 7 of the International Regulations for Preventing Collisions at Sea (**COLREGs**) and analyze how improper reliance on AIS data generates "AIS-assisted" and "VHF-assisted" collisions. You will trace specific failure mechanisms: heading-not-available confusions, course-over-ground (**COG**) versus true heading discrepancies, dimension and antenna offset errors, and target filtering that conceals Class B craft. You will dissect landmark casualties—including *Baltic Ace* / *Corvus J*, *Sanchi* / *CF Crystal*, *Costa Concordia*, MV *Sewol*, USS *Fitzgerald* and USS *John S. McCain*, the *Dali* bridge strike, and *Ever Given*—evaluating the role AIS played in each emergency. Furthermore, you will investigate the operational life-saving capabilities of AIS Search and Rescue Transmitters (**AIS-SART**) and Man Overboard (**AIS-MOB**) devices. Finally, you will implement automated Python verification checks to detect sentinel and degraded AIS kinematic parameters before they mislead bridge teams.

## 55.1 The anatomy of AIS-assisted collisions

The integration of the Automatic Identification System (**AIS**) into ship bridges under Chapter V of the International Convention for the Safety of Life at Sea (**SOLAS**) was designed to improve situational awareness and automate vessel identification ([Chapter 1](ch01-what-ais-is.md)). However, maritime casualty investigation boards—including the UK Marine Accident Investigation Branch (**MAIB**), the US National Transportation Safety Board (**NTSB**), the German Federal Bureau of Maritime Casualty Investigation (**BSU**), and the Australian Transport Safety Bureau (**ATSB**)—have documented a recurring hazard: collisions and groundings induced or compounded by improper reliance on AIS data.

In maritime literature, this mirrors the mid-twentieth-century emergence of "radar-assisted collisions," where mariners equipped with early radar maintained excessive speed in fog under false confidence. The modern "AIS-assisted incident" occurs when an Officer of the Watch (**OOW**) substitutes an electronic transponder feed for fundamental seamanship, systematic radar plotting, and visual lookout.

Three primary vulnerabilities drive this failure mode:

1. **Automation bias and display complacency:** Navigators perceive AIS target symbols, labels, and vectors on Electronic Chart Display and Information Systems (**ECDIS**) or radar screens as ground truth. Unlike primary radar targets—which fluctuate in signal return, suffer sea clutter, and require tracking filters—AIS targets appear crisp and stable. When bridge watchstanders treat these broadcasts as infallible without cross-checking raw radar returns or visual bearings, corrupt or delayed data propagates into command decisions.
2. **"VHF/AIS-assisted" negotiations:** AIS broadcasts reveal approaching vessels' names and call signs (Messages 1–3 and 5; [Chapter 22](ch22-message-catalog.md)). Rather than executing clear helm alterations under COLREG steering rules, watchstanders increasingly call targets by name on VHF radio. These verbal exchanges waste critical tactical minutes, suffer from language barriers, generate ambiguous agreements (such as "passing green-to-green"), and breed false assumptions while closing at combined speeds above 30 knots.
3. **Sensor-to-broadcast latency:** Watchkeepers evaluate collision risk using Closest Point of Approach (**CPA**) and Time to Closest Point of Approach (**TCPA**) calculated from AIS dynamic reports. While Class A transponders broadcast every 2 to 10 seconds under way ([Chapter 21](ch21-link-layer-tdma.md)), course alterations, rate of turn, and speed adjustments take time to pass through smoothing filters, creating dangerous lag relative to optical bearing lines on a pelorus.

```
       [ GNSS / Gyrocompass / Sensors ]
                     │
                     ▼
           [ Class A Transponder ]
                     │  (VHF Broadcast: Messages 1-3, 5)
                     ▼
             [ AIS Receiver ]
                     │  (IEC 61162 / NMEA Stream)
                     ▼
             [ Bridge ECDIS / Radar ]
                     │  (Filtering, Vector Math, CPA/TCPA)
                     ▼
             [ Officer of the Watch ]  <─── Automation Bias
                     │
         ┌───────────┴───────────┐
         ▼                       ▼
  [ COLREG Non-Compliance ]   [ Informal VHF Hailing ]
  • Delayed helm action       • Linguistic ambiguity
  • Small successive turns    • Tactical time lost
         │                       │
         └───────────┬───────────┘
                     ▼
        [ Close-Quarters / Collision ]
```

### 55.1.1 Statutory obligations under COLREG Rule 7

The International Regulations for Preventing Collisions at Sea 1972 (**COLREGs**) govern collision avoidance. Rule 7 (*Risk of collision*) establishes strict requirements:

- **Rule 7(a):** "Every vessel shall use all available means appropriate to the prevailing circumstances and conditions to determine if risk of collision exists."
- **Rule 7(b):** "Proper use shall be made of radar equipment if fitted and operational, including long-range scanning... and radar plotting or equivalent systematic observation."
- **Rule 7(c):** "Assumptions shall not be made on the basis of scanty information, especially scanty radar information."

In admiralty law, AIS is an aid to navigation; it does **not** satisfy Rule 7(b) requirements for radar plotting. AIS relies on third-party broadcast integrity over an unauthenticated VHF link.

**IMO Resolution A.1106(29)** (*Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems*) cautions in Section 40:

> "The potential of AIS as an anti-collision aid is recognized... but the user must be aware that AIS is an aid to navigation and does not replace radar/ARPA, visual lookout, or standard collision avoidance procedures."

Paragraph 44 of Resolution A.1106(29) directly addresses the VHF negotiation trap:

> "The use of VHF radio in collision avoidance should be avoided. Valuable time has been wasted without agreement and mutual understanding not achieved. AIS may provide identity information, but this should not be used to initiate collision-avoidance negotiations via VHF."

Despite these warnings, accident investigations show watchstanders repeatedly violating Rule 7, substituting VHF calls for timely rudder action.

## 55.2 Technical failure mechanisms in casualty sequences

When technical inconsistencies arise in broadcast AIS streams, bridge displays that ingest data without validation mislead navigators.

### 55.2.1 Heading-not-available and COG confusion

In ITU-R M.1371 dynamic reports (Messages 1–3), **true heading** and **Course Over Ground (COG)** represent fundamentally different physical quantities:

- **True heading:** The angular orientation of the ship's bow relative to true north, supplied by the transmitting heading device (**THD**; gyrocompass or GNSS attitude sensor). Encoded in bits 63–71 of Messages 1–3 (range 0°–359°), with **511** indicating *heading not available*.
- **Course Over Ground (COG):** The direction of motion of the vessel's center of mass relative to the earth, derived from GNSS fixes. Encoded in bits 42–53 in units of 0.1° (range 0.0°–359.9°), with **3600** indicating *COG not available*.

> **Definitions that bite.**
>
> **Heading vs. Course Over Ground (COG).**
> True heading dictates physical aspect—visual silhouette and sidelights seen under COLREG Rules 14 (Head-on) and 15 (Crossing). COG defines trajectory over ground. In strong cross-currents, tidal races, or beam winds, heading and COG diverge substantially (drift angle or leeway). When a heading interface fails or is unconfigured, the unit broadcasts heading 511. Many ECS plotters render the ship's graphic outline aligned with its COG vector when heading 511 is received. An OOW observing this synthetic hull misjudges the target's aspect, assumes a crossing situation is safe, and triggers a collision.

### 55.2.2 Static and voyage parameter corruption

Static parameters broadcast in Message 5 every 6 minutes exhibit frequent configuration errors (Harati-Mokhtari et al. 2007; Bailey et al. 2008):

- **Ship dimensions and antenna offsets:** Message 5 encodes offsets $(A, B, C, D)$ from hull perimeters to the GNSS antenna. When technicians invert bow/stern values ($A \leftrightarrow B$) or enter default zeros, the vessel's graphical centroid on ECDIS is displaced by 150 to 300 meters from its true steel envelope. In narrow channels, this offset obscures margins, leading to allisions with berths and bridge piers.
- **Navigational status errors:** Messages 1–3 bits 38–41 convey operational status (0 = *Under way using engine*, 1 = *At anchor*, 5 = *Moored*). Because status requires manual toggling on the transponder's Minimum Keyboard and Display (**MKD**), ships frequently broadcast *At anchor* while transiting fairways at 18 knots. Bridge collision-warning systems configured to suppress alarms for anchored craft fail to warn watchstanders of an approaching collision hazard.

### 55.2.3 Class B invisibility and display target filtering

The division into **Class A** (SOLAS commercial vessels $\ge 300\text{ GT}$ and passenger ships; 12.5 W SOTDMA) and **Class B** (small craft; 2 W or 5 W CSTDMA/SOTDMA; [Chapter 20](ch20-architecture-and-station-classes.md)) generates acute bridge risks.

In congested coastal waters, hundreds of Class B transponders broadcast simultaneously. To manage display clutter, radar/ECDIS software allows watchstanders to apply **target filtering**:

1. Range rings (suppressing targets beyond 6 nmi).
2. Speed filters (suppressing targets moving slower than 2 kn).
3. Class-based filtering (suppressing Class B targets or sleeping icons).

Although IEC 62388 mandates that any target triggering a CPA/TCPA alarm must display regardless of filter settings, non-compliant displays omit suppressed targets in background checks. Furthermore, small craft with low antenna heights (1–3 m) and 2 W transmitters suffer line-of-sight propagation loss ([Chapter 29](ch29-propagation-modeling.md)), causing intermittent reception on large ships whose antennas sit 40 meters up. An OOW relying on filtered ECDIS operates under the false assumption that blank water is empty.

### 55.2.4 Radio silence and "dark" ships

Naval combatants, law enforcement craft, and illicit operators routinely suppress AIS broadcasts. SOLAS V/19.2.4.7 permits masters to deactivate AIS when security is compromised. In peacetime, merchant navigators become so accustomed to AIS target overlays that they suffer cognitive blindness to radar echoes lacking AIS triangles. When a naval vessel transits dark through shipping lanes, merchant watchstanders fail to detect it, anticipating an automated alert that never sounds.

## 55.3 Landmark casualty analyses

Marine casualty investigation reports reveal how technical and human factors intersect in major maritime accidents.

### 55.3.1 Baltic Ace / Corvus J (2012): VHF negotiations and North Sea collision

On 5 December 2012, in heavy weather with gale-force winds and snow squalls, the Bahamas-flagged car carrier ***Baltic Ace*** (23,498 GT, 1,417 vehicles) collided with the Cyprus-flagged container ship ***Corvus J*** (6,370 GT) in the North Sea near the North Hinder Junction (BMA 2016; BSU 2019).

*Baltic Ace* was transiting eastbound at 19 knots; *Corvus J* was steaming southwest at 15 knots on crossing courses. *Baltic Ace* was the give-way vessel under COLREG Rule 15, obligated to keep clear. Rather than making a bold alteration to starboard, the bridge watch of *Baltic Ace* identified *Corvus J* via AIS and initiated VHF radio contact. Multiple ambiguous transmissions ensued regarding passing intentions. *Baltic Ace* then executed a late turn to port across *Corvus J*'s bow. *Corvus J* struck *Baltic Ace*'s starboard side at an 80° angle, breaching the vehicle deck. *Baltic Ace* lost electrical power and sank within 15 minutes, killing 11 of her 24 crew.

The BMA safety report cited over-reliance on VHF radio communications for collision avoidance and failure to follow COLREGs as root causes.

> **Case file.**
>
> **The *Baltic Ace* / *Corvus J* disaster (5 December 2012).**
> - **Vessels:** MV *Baltic Ace* (ro-ro car carrier, 23,498 GT) and MV *Corvus J* (container ship, 6,370 GT).
> - **Location:** North Hinder Junction, North Sea.
> - **Conditions:** Wind Beaufort force 8, severe sea state, snow squalls, restricted visibility.
> - **Outcome:** Hull breached, sinking in 35 m of water within 15 minutes; 11 fatalities; total vessel loss.
> - **AIS/VHF failure:** Both bridge teams identified each other via AIS and engaged in protracted VHF radio dialogue to negotiate passing arrangements instead of complying with COLREG Rules 15 and 16. Ambiguous communications culminated in *Baltic Ace* altering course to port across the bow of the stand-on vessel.

### 55.3.2 Sanchi / CF Crystal (2018): Electronic target complacency

On 6 January 2018, the Panamanian-flagged Suezmax tanker ***Sanchi*** (85,462 GT, carrying 136,000 tonnes of condensate) collided with the Hong Kong-flagged bulk carrier ***CF Crystal*** (41,073 GT) in the East China Sea (MSA 2018).

The vessels closed on steady crossing bearings for 26 minutes prior to collision (*Sanchi* at 10.4 kn; *CF Crystal* at 13.2 kn). Under Rule 15, *Sanchi* was the give-way vessel. VDR and AIS reconstruction proved neither bridge team took evasive action until seconds before impact. On *Sanchi*, the OOW failed to maintain a lookout under Rule 5. On *CF Crystal*, the watchstander observed *Sanchi*'s AIS vector on the bridge display but misjudged the crossing geometry, making minor 2°–3° adjustments to port—violating Rule 17.

*CF Crystal*'s bow penetrated *Sanchi*'s cargo tanks, igniting an inferno. *Sanchi* burned for eight days before exploding and sinking; all 32 crew perished. The accident report cited target complacency: active AIS vectors created a false sense of safety, leading officers on both ships to assume the other would maneuver clear.

### 55.3.3 Costa Concordia (2012): The unannounced sail-past

On 13 January 2012, the 114,147 GT cruise ship ***Costa Concordia*** grounded on Le Scole rocks off Giglio Island, Italy, suffering a 53-meter hull breach that caused flooding, capsize, and 32 deaths (MIT 2013).

The master diverted from the voyage plan to perform an unapproved close-range "sail-past" salute. AIS played a vital post-casualty forensic role. Because the transponder remained active through grounding and beaching, shore networks captured the vessel's speed decay, sharp port swing, and wind drift. Coastal VTS operators cross-referenced the anomalous AIS track with radar, establishing objective evidence that exposed the master's false claims of a routine electrical failure.

### 55.3.4 MV Sewol (2014): Tracking gaps and dynamic casualty forensics

On 16 April 2014, the South Korean ferry ***Sewol*** (6,825 GT) capsized in the Maenggol Channel, claiming 304 lives (KMST 2014). Overloaded and carrying deficient ballast, the ship lost stability during a turn, rolled past its angle of vanishing stability, and sank.

A **36-second AIS transmission gap** (08:48:37 to 08:49:13 KST) during the turn fueled public allegations of tracking tampering. Technical investigations proved the hiatus resulted from extreme structural heel: the violent roll tripped generators and blacked out the main switchboard, de-energizing the transponder until emergency battery circuits stabilized bridge telemetry. Once restored, AIS records accurately captured the runaway centrifugal turn.

### 55.3.5 USS Fitzgerald and USS John S. McCain (2017): Peacetime radio silence

In 2017, the US Navy suffered two fatal collisions involving guided-missile destroyers operating in dense Asian corridors:

- On 17 June 2017, **USS *Fitzgerald*** collided with container ship MV *ACX Crystal* off Japan, killing seven sailors (NTSB 2020).
- On 21 August 2017, **USS *John S. McCain*** collided with tanker MV *Alnic MC* in the Singapore Strait, killing ten sailors (NTSB 2019).

In both incidents, the destroyers transited with AIS silenced under military doctrine. The NTSB identified this radio silence as a major factor. Commercial watchstanders navigate congested straits by integrating AIS target vectors onto ARPA screens. Operating dark deprived merchant watchkeepers of the digital cue they rely upon to detect and track crossing traffic. In response, the US Navy mandated that surface warships activate Class A AIS when transiting commercial traffic lanes and straits ([Chapter 8](ch08-security-and-national-security-uses.md)).

### 55.3.6 The Dali Key Bridge allision (2024): Telemetry under electrical blackout

On 26 March 2024, container ship ***Dali*** (95,128 GT) suffered complete electrical blackout leaving Baltimore, losing propulsion and steering (NTSB 2024). Drifting under channel currents, the ship struck Pier 17 of the Francis Scott Key Bridge at 6.8 knots. The truss collapsed, killing six roadway workers.

AIS dynamic telemetry recorded the vessel's speed decay, drift, and yawing angle. Concurrently, the pilot issued an urgent VHF Mayday, prompting police to close bridge access spans and saving motorists before the collapse.

### 55.3.7 Ever Given (2021): Hydrodynamics, bank suction, and S-AIS replay

On 23 March 2021, the 20,124 TEU container ship ***Ever Given*** grounded in the Suez Canal, blocking international trade for six days (PMA 2023).

Operating at 12–13 knots in high crosswinds, the vessel experienced severe **bank suction** and **cushion** forces. Conflicting hard-rudder commands exacerbated an oscillatory yaw before the bulbous bow wedged into the eastern bank. Satellite AIS tracking recorded the ship's swinging track and stranding in real time. Investigation confirmed no mechanical failure occurred; excessive speed, sail area, hydrodynamic canal forces, and rudder overcorrection caused the stranding.

### 55.3.8 Achieve / Talis (2020) and CMA CGM Florida / Chou Shan (2013)

Two MAIB investigations highlight how AIS displays degrade bridge performance:

- ***Achieve* / *Talis* (MAIB Report 14/2021):** On 8 November 2020, cargo ship *Talis* collided in fog with trawler *Achieve* off Tynemouth. *Achieve* was a wooden vessel without AIS. The OOW on *Talis* relied on AIS to monitor traffic and lost critical minutes attempting to validate a faint radar return with non-existent AIS data, causing delayed action that sank the trawler.
- ***CMA CGM Florida* / *Chou Shan* (MAIB Report 11/2014):** On 19 March 2013, container ship *CMA CGM Florida* collided with bulk carrier *Chou Shan* in the East China Sea. The OOW fixated on an AIS target list sorted by CPA to weave through fishing craft, failing to notice the bulk carrier crossing from port to starboard until collision.

## 55.4 The other side: Lives saved by AIS-SART and AIS-MOB

While improper operational use of AIS has contributed to collisions, the radio technology has saved hundreds of lives in Search and Rescue (**SAR**) roles.

Prior to 2010, maritime survivors relied on 406 MHz COSPAS-SARSAT satellite beacons and 9 GHz X-band radar SARTs. Radar SARTs suffer from sea clutter, wave shielding, and short line-of-sight range (typically 5 nmi).

### 55.4.1 AIS Search and Rescue Transmitters (AIS-SART)

Under IMO Resolution MSC.246(83) and **IEC 61097-14**, the **AIS-SART** was adopted as a mandatory GMDSS alternative to radar SARTs for lifeboats and life rafts.

When activated, an AIS-SART broadcasts an ITU-R M.1371 **Message 1** burst (8 transmissions per minute across 161.975 and 162.025 MHz; [Chapter 20](ch20-architecture-and-station-classes.md)). It utilizes a dedicated MMSI format:

$$\text{MMSI} = 970\text{YYXXXX}$$

where `970` is the ITU SART prefix, `YY` is the manufacturer code, and `XXXX` is the device serial number.

On radar and ECDIS displays (IEC 62288 and IEC 62388), an AIS-SART renders as a distinctive **circle with an inscribed cross** ($\bigoplus$). The display activates audible and visual alarms, presenting the life raft's GNSS coordinates, SOG, and drift track up to 8–12 nmi to surface vessels and over 30 nmi to SAR aircraft.

### 55.4.2 Personal AIS Man Overboard devices (AIS-MOB)

In commercial fishing and yachting, wearable **AIS-MOB** devices (**RTCM 11901.1**) address the critical danger of cold-water survival.

Integrated into lifejackets, an AIS-MOB beacon triggers upon water immersion, broadcasting with prefix:

$$\text{MMSI} = 972\text{YYXXXX}$$

Many units concurrently transmit a Digital Selective Calling (**DSC**) distress alert (VHF Channel 70) to the mother ship. The victim's live position appears immediately on the ship's chartplotter, providing a direct range and bearing vector. Studies by US Sailing and the Cruising Club of America (**CCA**) show AIS-MOB devices have reduced crew-overboard recovery times from hours to under 15 minutes.

| Feature | Radar SART (9 GHz) | AIS-SART (SOLAS) | AIS-MOB (Wearable) |
|---|---|---|---|
| **Governing standard** | IEC 61097-1 | IEC 61097-14 | RTCM 11901.1 / IEC 62287 |
| **Operating frequency** | 9.2–9.5 GHz | 161.975 & 162.025 MHz | 161.975 & 162.025 MHz |
| **MMSI format** | None (pulse) | $970\text{YYXXXX}$ | $972\text{YYXXXX}$ |
| **Display symbol** | 12 radar blips | Circle with cross ($\bigoplus$) | Circle with cross or MOB |
| **Position accuracy** | Radar resolution | GNSS fix ($\le 5\text{ m}$) | GNSS fix ($\le 5\text{ m}$) |
| **Aircraft detection** | Limited | $> 30\text{ nmi}$ (1,000 ft altitude) | $> 10\text{ nmi}$ (aircraft altitude) |
| **Primary user** | Survival craft | Life rafts / lifeboats | Individual crew lifejackets |

## Then & now

- ⟨H⟩ **1972** — COLREGs Rule 7 establishes the legal primacy of radar plotting and visual lookout over auxiliary electronic aids.
- ⟨H⟩ **1998** — First operational demonstrations of Self-Organizing TDMA ship-to-ship transponders in Scandinavia.
- ⟨+⟩ **2002** — Entry into force of IMO SOLAS Chapter V AIS carriage mandate for commercial ships.
- ⟨+⟩ **2005** — UK MAIB identifies the emergence of "VHF-assisted collisions" facilitated by AIS target naming.
- ⟨+⟩ **2006** — UK MCA issues Marine Guidance Note MGN 324 (M+F) on the hazards of VHF radio and AIS collision avoidance.
- ⟨+⟩ **2007** — Harati-Mokhtari et al. publish the first large-scale AIS data reliability study, documenting pervasive static data errors.
- ⟨+⟩ **2010** — Manila Amendments incorporate AIS into STCW; IMO adopts MSC.246(83) approving AIS-SART for GMDSS.
- ⟨+⟩ **2012** — Grounding of *Costa Concordia* and collision of *Baltic Ace* / *Corvus J* illustrate forensic utility and VHF-assisted hazards.
- ⟨+⟩ **2014** — Capsizing of MV *Sewol*; investigation resolves controversy surrounding a 36-second power-loss AIS data gap.
- ⟨+⟩ **2015** — IMO adopts Resolution A.1106(29), superseding A.917(22), prohibiting VHF collision avoidance negotiations.
- ⟨+⟩ **2017** — Fatal collisions of USS *Fitzgerald* and USS *John S. McCain* expose peacetime risks of naval AIS radio silence.
- ⟨+⟩ **2018** — Suezmax tanker *Sanchi* collision demonstrates the perils of electronic target complacency in crossing encounters.
- ⟨+⟩ **2021** — *Ever Given* stranding in the Suez Canal; satellite AIS tracking visualizes bank-suction oscillations worldwide.
- ⟨+⟩ **2024** — Container ship *Dali* strikes the Key Bridge; AIS logs record power-loss dynamics while pilot VHF calls avert highway casualties.

## Validation, uncertainty & data quality

Forensic casualty reconstruction and collision-avoidance algorithms must account for AIS uncertainty quantitatively:

1. **Dimensional reference errors:** Message 5 encodes antenna offsets $(A, B, C, D)$. For a container ship 366 m long and 51 m wide, inverted offsets ($A \leftrightarrow B$) displace the computed bow position by over 250 meters. Algorithms must verify:

   $$A + B = \text{Length} \quad \text{and} \quad C + D = \text{Breadth}$$

   If $A+B=0$ or $C+D=0$, default values are present and the physical ship boundary cannot be determined from AIS.
2. **Sentinel value screening:** When a heading sensor fails, the transponder broadcasts sentinel **511**. Bridge software must never treat 511 as $0^\circ$ True. Similarly, SOG **1023** indicates speed not available, and COG **3600** indicates course not available.
3. **Kinematic latency:** Between position reports, software estimates motion via dead reckoning. For a vessel turning at rate of turn $R$ ($\text{deg/min}$) and speed $V$ ($\text{kn}$), position uncertainty grows quadratically with elapsed time $\Delta t$:

   $$\sigma_{\text{pos}}(\Delta t) \approx \sigma_{\text{GNSS}} + V \cdot \Delta t \cdot \sin\left(\frac{1}{2} R \cdot \Delta t\right)$$

   When Class B vessels report only every 30 seconds while maneuvering, extrapolation error exceeds 50 meters, producing misleading CPA values.
4. **Validation checklist:**
   - Verify MMSI follows MID allocation tables (valid country code and station class).
   - Flag position reports with heading = 511 or COG = 3600.
   - Screen for unphysical acceleration ($> 1.0\ \text{m/s}^2$) or rate of turn ($> 10^\circ/\text{s}$).
   - Verify Class B targets are not suppressed when range $< 6\text{ nmi}$ and CPA $< 1.5\text{ nmi}$.

> **Try it.**
>
> You can audit raw AIS NMEA logs for collision-critical sensor defects—such as missing heading sentinels (511) or unconfigured static dimensions—using the Python `pyais` library. Run the following snippet on a sample harbor capture to isolate degraded targets:
>
> ```python
> import pyais
>
> def audit_ais_stream(filepath):
>     sentinels_511 = 0
>     class_b_count = 0
>     class_a_count = 0
>     with open(filepath, "r", encoding="utf-8") as f:
>         for line in f:
>             if "!AIVDM" not in line:
>                 continue
>             raw = line[line.index("!AIVDM"):].strip()
>             try:
>                 msg = pyais.decode(raw)
>                 t = msg.msg_type
>                 hdg = getattr(msg, "heading", None)
>                 if hdg == 511:
>                     sentinels_511 += 1
>                     if t == 18:
>                         class_b_count += 1
>                     elif t in (1, 2, 3):
>                         class_a_count += 1
>             except Exception:
>                 continue
>     print(f"Total Heading 511 Sentinels: {sentinels_511}")
>     print(f"  Class A (Defective Gyro/Interface): {class_a_count}")
>     print(f"  Class B (Uninstalled/Optional):     {class_b_count}")
>
> audit_ais_stream("data/samples/synthetic_harbor.nmea")
> ```
>
> **Expected output:**
> ```text
> Total Heading 511 Sentinels: 361
>   Class A (Defective Gyro/Interface): 0
>   Class B (Uninstalled/Optional):     361
> ```

> **Worked example.**
>
> **Quantifying aspect error induced by Heading vs. COG confusion.**
>
> A bulk carrier is transiting a coastal fairway in the vicinity of a tidal race:
> - Current: setting $090^\circ$ True at $3.0\ \text{knots}$.
> - Ship true heading ($\theta_{\text{hdg}}$): $000^\circ$ True (bow pointed due North).
> - Speed through water ($V_{\text{stw}}$): $8.0\ \text{knots}$.
>
> The ship's kinematic velocity vector over ground is the vector sum of its water-track velocity and the tidal current:
>
> $$V_{\text{east}} = 8.0 \cdot \sin(0^\circ) + 3.0 \cdot \sin(90^\circ) = 0.0 + 3.0 = 3.0\ \text{knots}$$
>
> $$V_{\text{north}} = 8.0 \cdot \cos(0^\circ) + 3.0 \cdot \cos(90^\circ) = 8.0 + 0.0 = 8.0\ \text{knots}$$
>
> The vessel's Course Over Ground (COG) and Speed Over Ground (SOG) are:
>
> $$\text{COG} = \arctan2(V_{\text{east}}, V_{\text{north}}) = \arctan2(3.0, 8.0) \approx 20.56^\circ$$
>
> $$\text{SOG} = \sqrt{3.0^2 + 8.0^2} = \sqrt{9.0 + 64.0} = \sqrt{73.0} \approx 8.54\ \text{knots}$$
>
> The divergence between the vessel's physical aspect (heading $000^\circ$) and its ground-track vector (COG $020.6^\circ$) is:
>
> $$\Delta = |\text{COG} - \theta_{\text{hdg}}| = 20.6^\circ$$
>
> If an approaching vessel observes this target on an ECS display where heading is missing (sentinel 511) and the display software renders the ship's hull symbol aligned with its COG vector ($020.6^\circ$), the approaching watchstander observes an apparent aspect rotated over $20^\circ$ to starboard. Under COLREG Rule 14, an encounter that is physically nearly head-on appears electronically as a safe starboard-to-starboard crossing, prompting incorrect helm maneuvers that cause a collision.

## Software

**Open source:**
- **pyais** (Python): Pure-Python decoder for `!AIVDM`/`!AIVDO` sentences into structured models; useful for rapid screening of heading sentinels and static audits. *Caveat:* High-throughput streams require external multi-sentence reassembly buffers.
- **libais** (C++ with Python bindings): High-performance decoding engine built for billions of historical records conforming to ITU-R M.1371 bit specifications. *Caveat:* Strict validation requires well-formed input sentences without frame truncations.
- **OpenCPN** (C++): Open-source chartplotter supporting AIS overlays, CPA/TCPA alarms, and AIS-SART/MOB target rendering. *Caveat:* Community plugins and custom target filter settings can inadvertently suppress Class B targets.

**Free but closed:**
- **VesselFinder / MarineTraffic Free Portals:** Web and mobile tracking interfaces providing fused terrestrial and satellite ship positions. *Caveat:* Displayed positions can lag real-time broadcasts by minutes to hours, making them unsafe for tactical collision avoidance.

**Commercial:**
- **Transas / Wärtsilä Navi-Sailor ECDIS:** Type-approved bridge ECDIS featuring radar/AIS target association, trial maneuver simulation, and safety alarms conforming to IEC 62288. *Caveat:* Proprietary binary log formats require specialized vendor tools for forensic export.
- **Danelec Marine VDR Playback Suite:** Forensic software used by casualty investigators to synchronize multi-channel audio, radar imagery, and recorded AIS streams from VDR capsules. *Caveat:* Hardware dongle-protected and restricted primarily to accredited investigation bodies.

## Standards & guides

- **International Maritime Organization (IMO) Resolution A.1106(29)** (2015): *Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems (AIS)*. Authoritative guidance governing operational use, static updates, master switch-off discretion, and prohibition of VHF collision avoidance negotiations.
- **International Maritime Organization (IMO) Resolution MSC.246(83)** (2007): *Adoption of Performance Standards for Survival Craft AIS Search and Rescue Transmitters (AIS-SART)*. Establishes AIS-SART as a GMDSS survival craft device.
- **International Telecommunication Union Recommendation ITU-R M.1371-5** (2014): *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile frequency band*. Governs bit structures, reporting intervals, and sentinels for Messages 1–27.
- **International Electrotechnical Commission IEC 61993-2:2018**: *Class A shipborne equipment of the Automatic Identification System (AIS)*. Defines Class A hardware testing, sensor input interfaces, and failure alarms.
- **International Electrotechnical Commission IEC 62287-1:2017 & IEC 62287-2:2017**: *Class B shipborne equipment of the Automatic Identification System (AIS)*. Part 1 specifies CSTDMA; Part 2 specifies SOTDMA.
- **International Electrotechnical Commission IEC 62388:2013**: *Shipborne radar — Performance requirements, methods of testing and required test results*. Governs display presentation, target association, and mandatory safety alert behavior for fused radar and AIS targets.
- **International Electrotechnical Commission IEC 61097-14:2010**: *GMDSS — Part 14: AIS Search and Rescue Transmitter (AIS-SART)*. Governs technical parameters for 970YYXXXX beacons.
- **Radio Technical Commission for Maritime Services RTCM 11901.1** (2014): *Standard for Maritime Search and Rescue Electronic Devices: AIS-MOB*. Governs wearable 972YYXXXX man-overboard devices.
- **UK Maritime and Coastguard Agency Marine Guidance Note MGN 324 (M+F)** (2006): *Navigation: Watchkeeping Safety — Use of VHF Radio and AIS*. Foundational guidance on the legal and physical hazards of VHF-assisted collision avoidance.

## Pitfalls

1. **Initiating VHF collision avoidance negotiations based on AIS names:** Identifying an approaching target via AIS and hailing them on VHF Channel 16 to negotiate passing → Ambiguous verbal agreements and wasted tactical minutes replace standard COLREG actions → Comply with COLREG Rules 14–16 using decisive helm alterations; never substitute verbal negotiations for steering rules.
2. **Confusing Course Over Ground (COG) with True Heading:** A target experiences significant drift or broadcasts heading sentinel 511 → The watchkeeper mistakes the COG vector for the ship's physical heading, misjudging crossing geometry → Check whether heading or COG is displayed; if heading is 511, assess target aspect visually or via radar plotting.
3. **Filtering out Class B targets on bridge radar/ECDIS:** Applying sleep filters or suppressing Class B targets to reduce screen clutter in busy coastal waters → Small fishing vessels, workboats, and yachts become invisible on digital displays → Maintain active radar surveillance, never disable CPA/TCPA alarms for sleeping targets, and maintain a visual lookout.
4. **Target complacency and automation bias:** Assuming that because an approaching AIS vector indicates a safe CPA, no monitoring is needed → The target alters course or telemetry lags while the watchkeeper ceases monitoring (as in *Sanchi*) → Regularly verify CPA predictions against physical compass bearings on a pelorus.
5. **Relying on unverified static dimensions in tight channels:** An approaching vessel carries inverted antenna offsets ($A \leftrightarrow B$) entered at commissioning → The ECDIS renders the ship's hull symbol offset by 200 meters from its physical position → Maintain clearance margins using visual lookout and raw radar returns rather than digital bounding boxes.
6. **Assuming a dark ship does not exist:** Peacetime naval vessels or non-compliant craft navigate with AIS silenced → The watchkeeper relies exclusively on AIS target alarms and misses a raw radar return or visual running light → Configure ARPA auto-acquisition zones and maintain a continuous visual lookout.
7. **Trusting stale navigational status broadcasts:** A transiting ship broadcasts status 1 (*At anchor*) because the crew forgot to update the transponder upon departure → Bridge software suppresses collision alarms for "anchored" craft → Never assume a vessel is stationary based on navigational status; verify SOG and raw radar Doppler vectors.
8. **Misinterpreting AIS-SART or AIS-MOB emergency symbols:** Failing to recognize a red circle with an inscribed cross ($\bigoplus$) or MMSI beginning with 970/972 as an active distress beacon → Emergency response is delayed while attempting commercial VHF contact → Train bridge teams to immediately recognize 970/972 MMSIs and initiate SAR maneuvering protocols.
9. **Neglecting update-rate latency during high-speed maneuvering:** A fast vessel maneuvers, but its position reports arrive at 10-second intervals and bridge filters smooth the vector over several minutes → The OOW miscalculates the evasive maneuver in progress → Monitor the target's rate of turn (ROT) indicator and verify immediate aspect changes visually.
10. **Treating AIS as a substitute for mandatory radar plotting:** Using AIS vectors to assess collision risk without acquiring targets on ARPA radar → Scanty AIS data violates COLREG Rule 7(b) and lacks independent physical validation → Always acquire crossing and close-quarters targets on marine ARPA radar.

## Key takeaways

- AIS is an aid to navigation; under COLREG Rule 7, it does not replace visual lookout (Rule 5) or systematic radar plotting (Rule 7(b)).
- "VHF/AIS-assisted collisions" occur when navigators use AIS target identification to negotiate informal VHF radio agreements instead of executing timely, rule-compliant helm maneuvers.
- When an AIS target's heading interface is absent or disabled, heading broadcasts sentinel **511**; displaying this target aligned with its COG vector distorts its physical aspect and crossing geometry.
- Large divergences between heading and COG occur in tidal races, high leeway, and drifting conditions, requiring watchkeepers to distinguish between where a ship points and where it travels over ground.
- Suppressing or filtering Class B targets on bridge displays creates critical blind spots, leading directly to fatal collisions with small craft and fishing vessels.
- Peacetime naval operations conducted in AIS radio silence demonstrated that commercial watchkeepers suffer cognitive blindness when expected AIS data feeds are absent.
- Major maritime casualties—including *Baltic Ace*, *Sanchi*, *Costa Concordia*, *Sewol*, *Dali*, and *Ever Given*—demonstrate that while AIS misuse can cause disasters, recorded telemetry provides objective forensic truth.
- Dedicated AIS search-and-rescue beacons (AIS-SART, MMSI prefix 970; AIS-MOB, MMSI prefix 972) provide real-time GNSS homing vectors, cutting rescue times from hours to minutes and saving hundreds of lives.

## References

- Bahamas Maritime Authority (BMA) (2016). *Report of the Investigation into the Collision between MV Baltic Ace and MV Corvus J in the North Sea on 5 December 2012*. Nassau: BMA.
- Bailey, N., Ellis, N., and Sampson, H. (2008). *Training Needs Analysis for New Technologies in the Maritime Industry: AIS Case Study*. Cardiff: Seafarers International Research Centre (SIRC).
- Federal Bureau of Maritime Casualty Investigation (BSU) (2019). *Investigation Report 356/17: Serious Marine Casualty — Collision between M/V Baltic Ace and M/V Corvus J*. Hamburg: BSU.
- Harati-Mokhtari, A., Wall, A., Brooks, P., and Wang, J. (2007). Automatic Identification System (AIS): Data reliability and human error implications. *The Journal of Navigation*, 60(3):373–389.
- International Electrotechnical Commission (IEC) (2010). *IEC 61097-14:2010 — Global Maritime Distress and Safety System (GMDSS) — Part 14: AIS Search and Rescue Transmitter (AIS-SART) — Operational and Performance Requirements, Methods of Testing and Required Test Results*. Geneva: IEC.
- International Electrotechnical Commission (IEC) (2013). *IEC 62388:2013 — Maritime Navigation and Radiocommunication Equipment and Systems — Shipborne Radar — Performance Requirements, Methods of Testing and Required Test Results*. Geneva: IEC.
- International Electrotechnical Commission (IEC) (2017). *IEC 62287-1:2017 — Maritime Navigation and Radiocommunication Equipment and Systems — Class B Shipborne Equipment of the Automatic Identification System (AIS) — Part 1: Carrier-Sense Time Division Multiple Access (CSTDMA) Techniques*. Geneva: IEC.
- International Electrotechnical Commission (IEC) (2017). *IEC 62287-2:2017 — Maritime Navigation and Radiocommunication Equipment and Systems — Class B Shipborne Equipment of the Automatic Identification System (AIS) — Part 2: Self-Organising Time Division Multiple Access (SOTDMA) Techniques*. Geneva: IEC.
- International Electrotechnical Commission (IEC) (2018). *IEC 61993-2:2018 — Maritime Navigation and Radiocommunication Equipment and Systems — Automatic Identification Systems (AIS) — Part 2: Class A Shipborne Equipment of the Automatic Identification System (AIS)*. Geneva: IEC.
- International Maritime Organization (IMO) (2007). *Resolution MSC.246(83) — Adoption of Performance Standards for Survival Craft AIS Search and Rescue Transmitters (AIS-SART) for Use in Search and Rescue Operations*. London: IMO.
- International Maritime Organization (IMO) (2015). *Resolution A.1106(29) — Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems (AIS)*. London: IMO.
- International Telecommunication Union (ITU) (2014). *Recommendation ITU-R M.1371-5 — Technical Characteristics for an Automatic Identification System Using Time Division Multiple Access in the VHF Maritime Mobile Frequency Band*. Geneva: ITU.
- Korean Maritime Safety Tribunal (KMST) (2014). *Investigation Report on the Capsizing and Sinking of the Passenger Ship Sewol*. Sejong: Ministry of Oceans and Fisheries.
- Marine Accident Investigation Branch (MAIB) (2014). *Report on the Investigation of the Collision between the Container Vessel CMA CGM Florida and the Bulk Carrier Chou Shan in the East China Sea on 19 March 2013* (Report No. 11/2014). Southampton: MAIB.
- Marine Accident Investigation Branch (MAIB) (2017). *Report on the Investigation of the Collision between the Motor Launch Peggotty and the Ro-Ro Freight Ferry Petunia Seaways on the River Humber on 19 May 2016* (Report No. 4/2017). Southampton: MAIB.
- Marine Accident Investigation Branch (MAIB) (2021). *Report on the Investigation of the Collision between the Fishing Vessel Achieve and General Cargo Ship Talis Off Tynemouth, UK on 8 November 2020* (Report No. 14/2021). Southampton: MAIB.
- Maritime and Coastguard Agency (MCA) (2006). *Navigation: Watchkeeping Safety — Use of VHF Radio and AIS* (Marine Guidance Note MGN 324 (M+F)). Southampton: MCA.
- Maritime Safety Administration of the People's Republic of China (MSA) (2018). *Investigation Report on the Collision between the "SANCHI" and "CF CRYSTAL"*. Shanghai: Joint Investigation Team.
- Ministry of Infrastructures and Transports (MIT) (2013). *Cruise Ship Costa Concordia: Marine Casualty on January 13, 2012 — Report on the Safety Technical Investigation*. Rome: Marine Casualties Investigation Body.
- National Transportation Safety Board (NTSB) (2019). *Collision between US Navy Destroyer USS John S. McCain and Tanker Alnic MC, Singapore Strait, August 21, 2017* (Marine Accident Report NTSB/MAR-19/01). Washington, D.C.: NTSB.
- National Transportation Safety Board (NTSB) (2020). *Collision between US Navy Destroyer USS Fitzgerald and Philippine-Flag Container Ship ACX Crystal, Sagami Wan, Japan, June 17, 2017* (Marine Accident Report NTSB/MAR-20/02). Washington, D.C.: NTSB.
- National Transportation Safety Board (NTSB) (2024). *Preliminary Report: Contact of Containership Dali with Francis Scott Key Bridge and Subsequent Bridge Collapse* (Accident No. DCA24MM031). Washington, D.C.: NTSB.
- Panama Maritime Authority (PMA) (2023). *Marine Accident Investigation Report: Grounding of Ultra Large Container Ship Ever Given in the Suez Canal, Egypt on 23 March 2021*. Panama City: PMA.
- Radio Technical Commission for Maritime Services (RTCM) (2014). *RTCM 11901.1 — Standard for Maritime Search and Rescue Electronic Devices: AIS-MOB*. Arlington: RTCM.
