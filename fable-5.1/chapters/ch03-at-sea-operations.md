# Chapter 3 — At-sea operations where AIS is especially helpful

> **Part I — Why AIS? Uses and users.** A tactical assessment of how maritime VHF digital broadcasts transform specialized ship-handling, pilotage, fleet coordination, towing, offshore safety, and bridge-to-bridge communications in real ocean environments.

**In this chapter.** You will learn how real-world at-sea operations exploit the Automatic Identification System (AIS) to resolve operational friction, accelerate cooperative maneuvers, and mitigate catastrophic marine casualties. We analyze fourteen specialized domains: harbor and deep-sea pilotage via Portable Pilot Units (PPUs); commercial towing and pushing operations involving complex tow configurations; offshore supply, dynamic positioning (DP) staging, and safety zones; anchorage allocation and swing-circle monitoring; high-risk ship-to-ship (STS) lightering and bunkering; icebreaker-led convoys and sub-zero track-following; canal and lock approaches; mobile fishing gear and drifting net marking; hydrographic surveying and dredging fairways; cable laying and seismic streamer escorting; commercial diving and remotely operated vehicle (ROV) support; offshore yacht racing safety; naval tactical formation keeping; and Search and Rescue (SAR) datum buoy operations. Finally, you will explore the most ubiquitous yet under-appreciated operational benefit of AIS: bridge-to-bridge voice hailing by verified vessel name.

## 3.1 The tactical mariner's digital asset

The core specification of the Universal Shipborne Automatic Identification System (**AIS**), defined by the International Maritime Organization in Resolution MSC.74(69) (IMO 1998) and technical recommendation ITU-R M.1371 (ITU-R M.1371-5 2014), designates ship-to-ship collision avoidance as its foundational operational purpose. While macroscopic data aggregations power global trade analytics ([Chapter 5](ch05-traders-finance-nowcasting.md)) and fisheries surveillance ([Chapter 6](ch06-fisheries-iuu-dark-fleets.md)), tactical mariners experience AIS as an immediate, high-fidelity navigational sensor mounted on the bridge conning console or plugged directly into a pilot's transit tablet ([Chapter 20](ch20-architecture-and-station-classes.md); [Chapter 51](ch51-charts-enc-ecdis.md)).

At sea, operational friction stems from uncertainty: incomplete radar visibility around blind headlands, ambiguous target kinematics during manual tracking sweeps, language barriers across multinational bridge teams, and anonymous radar blips in dense traffic fairways. AIS penetrates these ambiguities by broadcasting self-organized, unauthenticated, line-of-sight Time Division Multiple Access (**TDMA**) packets on two dedicated marine VHF frequencies: AIS 1 (161.975 MHz) and AIS 2 (162.025 MHz) ([Chapter 21](ch21-link-layer-tdma.md); [Chapter 28](ch28-rf-encoding-physical-layer.md)).

By coupling continuous kinematic vectors—Speed Over Ground (**SOG**), Course Over Ground (**COG**), Rate of Turn (**ROT**), and True Heading (**HDG**)—with static identity parameters (vessel name, call sign, Maritime Mobile Service Identity [**MMSI**], dimensions, and operational status), AIS transforms cooperative marine maneuvers. Below, we examine the specific operational environments where AIS provides decisive tactical utility.

---

## 3.2 Pilotage and Portable Pilot Units (PPUs)

Marine pilots board vessels in open roadsteads, often in adverse weather, to navigate confined waterways, river bars, and complex port infrastructure. Because visiting vessels display wide variations in bridge ergonomics, gyrocompass calibration, and Electronic Chart Display and Information System (**ECDIS**) configuration ([Chapter 51](ch51-charts-enc-ecdis.md)), modern pilots rely on carry-on **Portable Pilot Units** (**PPUs**).

```
+--------------------------------------------------------------------------+
|                        VESSEL WHEELHOUSE CONNING CONSOLE                 |
|                                                                          |
|   +-------------------+    IEC 61162-2 / RS-422    +-----------------+   |
|   | Ship AIS Class A  |--------------------------->| Pilot Plug      |   |
|   | Transponder       |       38,400 baud          | AMP 206486-1    |   |
|   +-------------------+                            +--------+--------+   |
|                                                             |            |
+-------------------------------------------------------------|------------+
                                                              | Standard
                                                              | Pinout
                                                              v
                                                     +-----------------+
                                                     | Pilot Cable /   |
                                                     | Wi-Fi / BT Puck |
                                                     +--------+--------+
                                                              | NMEA 0183
                                                              | Stream
                                                              v
                                                     +-----------------+
                                                     | Portable Pilot  |
                                                     | Unit (PPU)      |
                                                     | Tablet / Chart  |
                                                     +-----------------+
```

Under IMO SN/Circ.227 (IMO 2003) and national mandates such as US Coast Guard regulations in 33 CFR § 164.46(g) (USCG 2015), vessels subject to compulsory pilotage must provide an accessible **pilot plug** mounted at the primary conning position. This standard sub-miniature circular connector (AMP 206486-1 shell or standard 5-pin terminal) breaks out the Class A transponder's bidirectional IEC 61162-2 / RS-422 interface at 38,400 baud ([Chapter 26](ch26-interfaces-and-logging.md)). 

By coupling a wireless Wi-Fi or Bluetooth transmitter puck to the pilot plug, the pilot immediately injects real-time `!AIVDM` (received target targets) and `!AIVDO` (own-ship dynamic reports) data streams into their PPU charting software. The PPU combines the ship's AIS output with differential or Real-Time Kinematic (**RTK**) GNSS correction sensors deployed on the bridge wings. 

This hybrid architecture provides the pilot with millimeter-accurate berthing velocity vectors and predictive swept-path hydrodynamic envelopes. During blind transits in thick fog through twisting dredged channels—such as the Houston Ship Channel or the Saint Lawrence Seaway—the pilot tracks not merely an isolated point coordinate, but the exact charted geometric hull envelope of meeting vessels broadcast via Message 5 dimension offsets $(A, B, C, D)$ ([Chapter 22](ch22-message-catalog.md)).

---

## 3.3 Towing, pushing, and articulated tug-barge (ATB) operations

Commercial tug operations represent some of the most geometrically complex maneuvers at sea. A towing vessel may pull a barge on a 300 m hawser astern, push an inland flotilla of thirty barges measuring 300 m in length ahead, or lock into the notched stern of an Articulated Tug-Barge (**ATB**) unit operating as a single composite hull.

Under the International Regulations for Preventing Collisions at Sea (**COLREGs**), Rule 24 dictates distinct towing shapes and light configurations. However, at night, in heavy seas, or under restricted visibility, an approaching ship's radar frequently detects only the steel superstructure of the towed barge while failing to acquire the low-profile tug ahead, or conversely detects the tug while the low-freeboard hawser and barge remain invisible in sea clutter.

```
       A                               B
<-------------><--------------------------------------------->
+--------------+---------------------------------------------+
| TUG          | PUSHED BARGE FLOTILLA                       |
| (MMSI:       | Total length broadcast in Message 5:        |
|  367445000)  | Dim A = 280 m, Dim B = 35 m                 |
+--------------+---------------------------------------------+
               ^
          GNSS Antenna
```

AIS resolves this hazard when transponders are correctly configured:
1. **Navigational Status Encoding:** Class A transponders broadcast Navigational Status `03` ("Restricted in ability to manoeuvre") or `12` ("Towing and pushing") in Messages 1, 2, and 3 ([Chapter 22](ch22-message-catalog.md)).
2. **Dimension Offsets for Flotillas:** In pushing operations, the master updates the ship's static parameters (Message 5) so that Dimension $A$ (distance from GNSS antenna to bow) reflects the combined length of the tug and the pushed flotilla ahead.
3. **Dedicated Auxiliary Transponders:** For tows astern exceeding 200 m, operators increasingly fit autonomous Class B or Aid to Navigation (**AtoN**) transponders to the tail of the tow, alerting surrounding traffic that the navigable water between the two AIS targets is obstructed by a heavy steel towline.

> **Definitions that bite.**
> **Navigation Status 12 ("Reserved for regional use" vs "Towing and pushing").** In ITU-R M.1371-4 and earlier revisions, code `12` was designated as "reserved for regional use." Under ITU-R M.1371-5 (Table 45), code `12` is explicitly defined as "under way by engines and towing/pushing (regional use)." Watchstanders using legacy ECDIS displays may see targets broadcasting code `12` rendered with an undefined "question mark" icon or defaulting to standard power-driven status rather than the restricted maneuverability symbology prescribed by IEC 62288.

---

## 3.4 Offshore supply, dynamic positioning (DP), and safety zones

Offshore drilling rigs, production platforms, and floating production storage and offloading (**FPSO**) vessels are protected by statutory safety zones—typically a 500 m perimeter established under national outer continental shelf legislation. Vessels operating within this perimeter, such as Platform Supply Vessels (**PSVs**) and Anchor Handling Tug Supply (**AHTS**) craft, rely on Dynamic Positioning (**DP**) systems to maintain position without physical mooring lines (IMCA 2022).

In dense offshore energy basins (such as the Gulf of Mexico, the North Sea, or offshore Campos Basin), dozens of supply vessels loiter awaiting offloading slots. AIS provides essential tactical surveillance:
- **Safety Zone Incursion Monitoring:** Modern rig management systems interface with coastal AIS receivers and platform radars to trigger audible alarms the instant an unauthorized vessel's projected CPA breaches the 500 m perimeter.
- **DP Reference and Wake Hazards:** DP vessels holding station inches from platform risers are exceptionally vulnerable to heavy surface displacement wakes generated by passing high-speed vessels. Monitoring approaching vessels via AIS allows DP operators to anticipate hydraulic surge forces or command standby thrusters before hydrodynamic wash destabilizes the vessel.
- **Specialized Navigational Status:** FPSO units and drillships often broadcast Navigational Status `07` ("Engaged in fishing", often miskeyed) or `03` ("Restricted in ability to manoeuvre"), warning passing transit traffic that subsea umbilicals and mooring spreads radiate outward thousands of meters across the seafloor.

---

## 3.5 Anchorage management and swing-circle monitoring

Harbor anchorages represent high-density parking grounds where deeply laden commercial ships swing freely around ground tackle under the alternating influences of reversing tidal streams and sudden wind squalls.

```
                    High Tide (Flood)
                        North
                          ^
                          |   Heading: 005°
                     [ Tanker A ]
                          |
                          o (Anchor dropped)
                         /
                        /
                       /  Heading: 185°
                [ Tanker A ]
                     v
             Low Tide (Ebb) / Wind Shift
```

When anchored, a vessel's Class A transponder automatically switches its reporting interval from 10 seconds to 3 minutes when SOG drops below 3 knots (IMO 2015, Res. A.1106(29)). AIS aids anchorage management in three key areas:
1. **Staging and Drop Point Selection:** Entering vessels inspect the real-time AIS display to locate open swing circles, identifying which anchored vessels are partially loaded, awaiting bunker barges, or preparing to heave anchor based on their declared Navigational Status `01` ("At anchor") versus `00` ("Under way using engine").
2. **Anchor Dragging Detection:** An anchored vessel caught in a storm can drag anchor imperceptibly across muddy bottoms. While radar guard rings can fail over flat water, automated AIS tracking algorithms detect drag kinematics: an anomalous combination of low ground speed ($\text{SOG} > 0.8\text{ kn}$ [1.5 km/h]), non-zero Rate of Turn, and an erratic course vector misaligned with prevailing wind or tidal vectors.
3. **VTS Berth Assignment Verification:** Port authorities monitor designated anchorage sectors to ensure deep-draught bulkers do not swing into designated shallow-draught safety corridors or foul submarine cable protection zones ([Chapter 4](ch04-vts-and-ports.md)).

---

## 3.6 Ship-to-ship (STS) lightering and bunkering operations

Ship-to-ship (**STS**) petroleum and chemical transfers involve maneuvering two large commercial vessels into direct physical contact while underway at slow speed (typically 4–6 knots) or anchored in designated offshore lightering areas (OCIMF 2013). 

During the rendezvous and approach phase, the maneuvering ship must execute a parallel mooring alongside the constant-heading base tanker. AIS telemetry is vital during the initial closure phase:
- **Heading versus Course Matching:** The approaching master continuously cross-references the base vessel's True Heading (`HDG`) against its Course Over Ground (`COG`). A significant discrepancy indicates severe hydrodynamic leeway or cross-current shear, allowing the mooring master to adjust approach vectors before pneumatic fenders make contact.
- **Relative Speed Matching:** Matched speeds ($\Delta \text{SOG} < 0.2\text{ kn}$) prevent dangerous longitudinal shear forces that could tear mooring lines or rupture floating transfer hoses.
- **Monitoring Moored Pairs:** Once moored alongside, the combined pair presents an immense hydrodynamic profile. AIS transponders on both vessels remain active, alerting surrounding traffic via dynamic broadcast that the composite formation is maneuvering as a single constrained unit.

---

## 3.7 Icebreaker escort and Arctic/Baltic convoy management

In polar and sub-polar waters, winter navigation depends on icebreaker escorts through consolidated pack ice and pressure ridges. Convoy navigation through frozen fairways imposes extreme demands on situational awareness: visibility is frequently curtailed by blowing snow, polar night, and freezing fog, while radar returns from broken ice rubbles obliterate small vessel targets in backscatter clutter.

```
+--------------------+      500–1,500 m      +--------------------+
| Icebreaker         |======================>| Escorted Bulker    |
| (Leader)           |    Cleared Channel    | (Follower)         |
| SOG: 6.5 kn        |                       | SOG: 6.4 kn        |
| ROT: +12°/min      |                       | Rate of Turn Match |
+--------------------+                       +--------------------+
```

During close escort operations:
- **Convoy Spacing and Deceleration Alarms:** Escorted merchant vessels follow within 500 to 1,500 m of the icebreaker's stern to remain inside the freshly carved channel before moving ice closes the track. If the icebreaker strikes an impenetrable multi-year ice ridge, its forward momentum can drop from 8 knots to dead stop within dozens of meters. AIS broadcasts instantaneous decelerations in dynamic position reports, triggering immediate closure rate alarms on the follower's bridge long before visual observation reveals the halt.
- **Convoy Tactical Ordering:** In multi-vessel convoys, ice pilots assign transit sequences based on vessel ice class, displacement, and engine power. AIS allows the command icebreaker to monitor the speed maintenance and spacing of five to ten trailing ships across tens of miles of ice track.
- **Channel Waypoint Promulgation:** Icebreakers equipped with Application-Specific Messaging (**ASM**) capability can broadcast recommended ice routing waypoints directly to convoy participants via binary messages ([Chapter 23](ch23-asm-binary-payloads.md)).

---

## 3.8 Canal and lock transits

Transiting restricted waterways such as the Panama Canal, Suez Canal, Kiel Canal, or Saint Lawrence Seaway requires millimeter-level precision. In these corridors, vessels operate with minimal under-keel clearance (**UKC**) and are constrained by the hydrodynamic phenomena of shallow water: squat, bank suction, and canal cushion effects.

In the Saint Lawrence Seaway and Panama Canal, specialized AIS networks govern lock sequencing:
- **Lock Queue Management:** In the Saint Lawrence Seaway, AIS Message 8 binary payloads convey automated lock transit schedules, water levels, and bridge clearance metrics directly to bridge teams ([Chapter 43](ch43-demonstration-programs.md)).
- **Passing Coordination in Canal Cuts:** In narrow cuts (such as the Gaillard Cut in the Panama Canal), two passing Panamax or Neopanamax vessels experience severe lateral hydrodynamic repulsion between their bows followed by attraction between their sterns. Pilots use PPU-coupled AIS to precisely synchronize meeting locations in straight channel sections rather than tight bends.
- **Lock Approach Alignment:** When easing a 300 m vessel into a 33 m wide concrete lock chamber, AIS-derived Rate of Turn and transverse drift velocities (computed from bow and stern GNSS offsets) give docking masters real-time lateral speeds in centimeters per second, preventing costly impacts with lock approach walls.

---

## 3.9 Fishing gear and drifting net marking

Commercial fishing vessels deploy longlines spanning up to 50 nautical miles (93 km), driftnets drifting over vast pelagic corridors, and anchored pot strings representing hundreds of thousands of dollars in capital equipment.

To prevent merchant vessels from running down gear and fouling propellers, fishers increasingly deploy AIS-based gear markers:
- **Aid to Navigation (AtoN) Transponders:** Officially, marking fixed or drifting hazards is accomplished using AIS AtoN transponders broadcasting Message 21 ([Chapter 20](ch20-architecture-and-station-classes.md); [Chapter 68](ch68-special-purpose-ais.md)), displaying standard physical or virtual buoy symbols on neighboring chart displays.
- **Autonomous Maritime Radio Devices (AMRD):** Under ITU Radio Regulations and ITU-R M.2135, specialized low-power transmitters (AMRD Group B) mark nets and buoys on designated VHF frequencies (such as Channel 2006 at 160.900 MHz) rather than congesting international distress and safety channels.
- **Gear Avoidance:** Passing merchant mariners monitor clustered fishing transponders to identify the orientation of driftnets, allowing them to make minor course alterations 10 nautical miles in advance rather than risking expensive propeller entanglements.

---

## 3.10 Dredging, hydrographic survey, and marine construction

Dredgers, survey launches, and heavy marine construction barges present atypical maneuvering characteristics. A trailing suction hopper dredger operates at low speeds (1–3 knots) with suction pipes deployed deep into the seabed sediment; a cutter suction dredger is tethered to spud poles and swing anchors; a hydrographic survey vessel must run rigidly straight survey lines without deviating for passing traffic.

AIS facilitates coexistence in busy fairways:
- **Restricted Maneuverability Awareness:** These craft continuously broadcast Navigational Status `03` ("Restricted in ability to manoeuvre"), alerting passing containerships that the dredger cannot comply with standard give-way obligations under COLREGs Rule 18.
- **Fairway Encroachment Alerts:** Port VTS centers use AIS tracks from dredging units to define dynamic moving safety zones around operations, broadcasting synthetic AIS AtoN markers ([Chapter 20](ch20-architecture-and-station-classes.md)) that redirect approaching commercial traffic into temporary bypass channels.
- **Survey Line Deconfliction:** When survey launches run bathymetric swaths across harbor entrance channels, their predictable AIS course tracks enable inbound pilot vessels to coordinate passing times without requiring the survey team to abort expensive sounding passes.

---

## 3.11 Cable laying, pipe laying, and seismic streamer ops

Subsea infrastructure operations represent operations with extreme physical spatial footprints:
- **Seismic Survey Streamers:** A 3D/4D seismic exploration vessel tows an array of up to twelve or sixteen hydrophone streamers, each extending 6 to 12 kilometers behind the stern and spanning a total spread width of over 1.5 kilometers.
- **Subsea Pipelay and Heavy Construction:** Pipelay vessels tension pipe strings to the seabed using dynamic positioning or multi-point anchor spreads that radiate 2 kilometers from the hull.

Navigating in the vicinity of a seismic spread is fraught with peril: if an errant merchant vessel crosses the streamer tail, the vessel's hull and propeller will sever millions of dollars worth of geophysical sensor arrays.
- **Streamer Tailbuoy Marking:** Seismic operators mount AIS Class B or specialized AtoN transponders to each individual streamer tailbuoy. The resulting display paints a complete geometric fan on surrounding ships' ECDIS displays, showing the exact lateral and longitudinal extent of the submerged gear.
- **Escort and Guard Vessels:** Fast chase and guard boats patrol the perimeter of the seismic array. Their bridge teams continuously compute CPAs against passing commercial traffic via AIS. If an approaching containership shows an intercept trajectory, the guard boat intercepts the vessel, calling it by verified name over VHF radio to request an immediate diversion.

---

## 3.12 Commercial diving, salvage, and ROV support

Subsea diving and Remotely Operated Vehicle (**ROV**) interventions are conducted under rigorous safety limits. Divers working at depth on saturation spreads or surface air umbilicals are exceptionally vulnerable to differential pressure surges, dropped objects, and thruster-induced water turbulence.

Vessels engaged in diving operations display the International Code of Signals flag "Alpha" and broadcast Navigational Status `03` on AIS.
- **Vessel Approach Exclusion:** Commercial diving standards mandate that passing vessels remain clear of dive stations by a specified minimum radius (often 500 m to 1 nautical mile). AIS guard zones establish automated alarms that sound the instant an encroaching vessel enters this safety radius, giving dive supervisors time to halt operations, lock divers inside diving bells, or recover personnel to the deck.
- **ROV Tracking:** Tethered subsea crawlers and ROVs operating near offshore wind turbine foundations or submerged shipwrecks are monitored relative to surface support ships, ensuring supply vessels do not drop anchors into active dive sectors.

---

## 3.13 Offshore yacht racing and small-craft safety

Offshore yacht racing events—such as the solo, non-stop round-the-world **Vendée Globe** or the grueling **Rolex Sydney Hobart Yacht Race**—pit lightweight racing craft against extreme Southern Ocean storms, floating debris, and heavy international shipping traffic.

Over the past two decades, race organizers have made AIS carriage compulsory:
- **World Sailing Regulations:** Under the World Sailing Offshore Special Regulations (OSR § 3.29.7) (World Sailing 2024), competing yachts in Category 0, 1, 2, and 3 offshore races must carry an active Class A or Class B transponder connected to a dedicated masthead or high-elevation VHF antenna.
- **Mandatory AIS in Major Races:** The Notice of Race for the Rolex Sydney Hobart Yacht Race (CYCA 2024) mandates both active boat-level AIS transponders and personal AIS Man Overboard (**MOB**) beacons for all competing crew members. In the Vendée Globe, skippers operate Class A transponders continuously, allowing race directors, commercial mariners, and fellow competitors to track hull positions across remote oceanic sectors where terrestrial radar and VHF communications do not exist.
- **Sleep Management and Collision Alarms:** Solo skippers depend on AIS receiver guard rings coupled to loud cockpit alarms to wake them when commercial vessels breach safe CPA limits while the skipper is asleep below deck.
- **Personal AIS-MOB Recovery:** If a crew member falls overboard at night in heavy seas, an automated AIS-MOB transponder integrated into their inflatable lifejacket activates, broadcasting a 972-series MMSI (`972XXXXXX`) and dynamic position bursts directly to the yacht's chartplotter, guiding the short-handed crew directly back to the casualty.

---

## 3.14 Naval tactical maneuvers and formation keeping

Naval surface combatants operate under distinct operational doctrines compared to the commercial merchant fleet. Warships routinely execute close-formation steaming, replenishment at sea (**RAS**), and tactical grid maneuvers.

Historically, warships disabled AIS under the discretion granted to sovereign craft by SOLAS Chapter V, Regulation 19.2.4 (IMO 2000; [Chapter 8](ch08-security-and-national-security-uses.md); [Chapter 63](ch63-military-encrypted-ais.md)), fearing that continuous transmission would compromise operational security (**OPSEC**). However, operating silently inside congested commercial fairways led to catastrophic accidents:
- **The 2017 Destroyer Collisions:** In June and August 2017, the guided-missile destroyers USS *Fitzgerald* (DDG-62) and USS *John S. McCain* (DDG-56) collided with commercial merchant ships (*ACX Crystal* and *Alnic MC*, respectively) in high-density Asian waters, resulting in the tragic deaths of seventeen US Navy sailors. The investigations revealed that operating without AIS broadcast deprived commercial watchstanders of essential situational awareness.
- **Tactical Doctrine Shift:** Following these disasters, Naval Surface Forces issued strict operational directives requiring naval vessels to activate commercial AIS broadcasts whenever transiting Traffic Separation Schemes (**TSS**) and high-density commercial corridors.
- **Formation Keeping and Joint Operations:** While tactical warships communicate over encrypted Link 16 or tactical data networks during combat exercises, auxiliary support vessels, coast guard cutters, and multinational coalition ships utilize commercial AIS during peacetime humanitarian and maritime interdiction patrols to coordinate search grids and maintain spacing without saturating military tactical radio frequencies.

---

## 3.15 Search and Rescue (SAR) datum marking and search patterns

In maritime Search and Rescue, locating survivors drifting on the high seas is a race against time, hypothermia, and expanding geometric uncertainty. When a vessel founders or a distress alert is received, Joint Rescue Coordination Centers (**JRCCs**) compute the initial **datum**—the estimated geographic location of the distress incident—and project its drift over time under prevailing surface currents and local leeway winds.

AIS enhances SAR field operations through three distinct assets:
1. **AIS Search and Rescue Transmitters (AIS-SARTs):** Replacing older X-band radar SARTs, modern AIS-SARTs broadcast Message 1 and Message 14 bursts encoded with standard 970-series MMSIs (`970XXXXXX`). When activated in a liferaft, the transponder paints a circle with an inscribed "X" across all receiving radar and ECDIS displays within a 5 to 10 nautical mile radius, updating the survivor's exact drifting coordinate every minute ([Chapter 68](ch68-special-purpose-ais.md)).
2. **Self-Locating Datum Marker Buoys (SLDMB):** Air-dropped into the water at the initial distress site, oceanographic drift buoys equipped with AIS or satellite transmitters drift alongside the casualty, reporting real-time surface water current vectors that allow rescue coordinators to continuously update the search datum box.
3. **Coordinated Search Pattern Execution:** When multiple commercial ships of opportunity (enlisted via the AMVER system) converge on a search area, the On-Scene Coordinator (**OSC**) monitors the real-time AIS tracks of all search vessels. This verifies that expanding square, creeping line, or sector search patterns are executed without gaps or overlapping tracks.

---

## 3.16 Bridge-to-bridge calling by name: the single most under-appreciated use

Before the advent of AIS, resolving an ambiguous close-quarters encounter over VHF radiotelephone was fraught with peril. An officer on the bridge of a containership observing a crossing radar target would pick up the microphone on VHF Channel 13 or 16 and broadcast:

> *"Vessel on my port bow, distance four miles, steering easterly, this is the container vessel on your starboard side. What are your intentions?"*

In a crowded anchorage, congested strait, or coastal fairway, this transmission was disastrous:
- Multiple vessels occupied similar relative bearings.
- The wrong ship would respond, confirming an agreement never intended for them.
- Time was wasted clarifying identities while ships closed at combined speeds exceeding 30 knots.

```
       WITHOUT AIS                                     WITH AIS
"Vessel on my port bow,                          "Motor Tanker Pacific Dawn,
 distance 3 miles, steering 090...                this is Neptune Trader on your
 what are your intentions?"                       starboard bow. Propose port-to-port."
             |                                               |
             v                                               v
   [ Ambiguous target ]                             [ Identified target ]
   Three vessels reply;                             Single vessel replies;
   fatal misunderstandings.                         immediate clarity.
```

AIS completely transformed this operational dynamic. By displaying the vessel's verified **ship name**, **call sign**, and **MMSI** directly alongside the radar target or chart icon, the watchstander hails the exact target directly:

> *"Motor Tanker Pacific Dawn, call sign WDC4567, this is Neptune Trader on your starboard bow. Request a port-to-port passing."*

This capability—direct, unambiguous bridge-to-bridge voice calling by name—is widely recognized by master mariners and pilotage associations as the single most consequential tactical enhancement AIS introduced to maritime safety. It eliminates the deadly "who is who" dilemma in crowded waterways.

However, as demonstrated in subsequent accident investigations, direct VHF calling introduces its own insidious failure modes when mariners substitute informal radio agreements for the strict application of the COLREGs.

---

## Then & now

- `⟨H⟩` **Pre-2000:** Vessels relied exclusively on ARPA radar plotting and visual bearings to identify collision threats. Resolving ambiguous encounters required open VHF voice broadcasts describing coarse relative bearings ("vessel 4 miles on my port bow"), frequently answered by the wrong ship.
- `⟨+⟩` **2002:** Entry into force of SOLAS Chapter V, Regulation 19 carriage requirements mandates universal Class A transponders on all international voyages of 300 GT and above, establishing the first global rollout of automatic vessel identification (IMO 2000).
- `⟨H⟩` **2003:** Publication of IMO SN/Circ.227 standardizes the universal 9-pin/AMP conning position **pilot plug**, providing marine pilots with direct access to shipboard AIS and gyro data streams via portable computers (IMO 2003).
- `⟨+⟩` **2006:** IEC 62287-1 codifies Class B CSTDMA transponders, bringing digital identification to smaller fishing vessels, workboats, and recreational yachts operating outside SOLAS mandates.
- `⟨+⟩` **2010:** Adoption of the AIS-SART standard (IEC 61097-14) provides lifeboats and life rafts with active GPS-derived AIS homing beacons, supplementing legacy X-band radar transponders.
- `⟨+⟩` **2015:** Revision of the IMO Operational Guidelines under Resolution A.1106(29) provides updated operational guidance on reporting intervals, bridge integration, and explicit warnings against over-reliance on VHF collision-avoidance negotiations (IMO 2015).
- `⟨+⟩` **2017:** Following fatal collisions involving the destroyers USS *Fitzgerald* and USS *John S. McCain*, the US Navy reverses decades of operational silence, mandating that naval combatants activate AIS in commercial traffic corridors (US Navy 2017).
- `⟨+⟩` **2024:** World Sailing and major offshore racing bodies (such as the Rolex Sydney Hobart Yacht Race) mandate active AIS transponders and personal AIS-MOB units across all ocean racing categories (World Sailing 2024; CYCA 2024).

---

## Validation, uncertainty & data quality

Operational safety at sea depends on understanding the fundamental difference between what a sensor actually measures and what an AIS transponder broadcasts. AIS is not an autonomous radar; it is an unauthenticated, digital repeating relay that packages data supplied by external shipboard navigation sensors ([Chapter 25](ch25-gnss-and-ais.md)).

### Sensor Error Propagation and Lag

Errors propagate from shipboard transducers to the VHF data link along three paths:
1. **Heading Sensor Drift:** The Class A transponder samples True Heading (`HDG`) from the ship's gyrocompass or transmitting magnetic compass via IEC 61162-1 sentences (`$--HDT` or `$--THS`). If the master gyro drifts by $4^\circ$ or an uncertified magnetic sensor is used, the AIS broadcasts an erroneous heading. On an ECDIS display, this causes the vessel's hull vector and swept-path predictor to skew sideways, misleading pilots during close passing maneuvers in narrow dredged channels.
2. **GNSS Antenna Reference Point Offsets:** Message 5 encodes the vessel's dimensions and the exact horizontal position of the internal/external GNSS antenna using four offset fields: Dimension $A$ (distance to bow), $B$ (to stern), $C$ (to port), and $D$ (to starboard). On a 400 m ultra-large container vessel, if the shipyard technician inadvertently reverses offsets $A$ and $B$, the broadcast position reported on the VHF link will be displaced by 300 meters from the actual bridge conning position. During blind fog transits, this error places the ship's bow an entire ship-length ahead of its true physical location.
3. **Rate of Turn Sensor Quantization:** ROT is broadcast in Message 1, 2, and 3 using an 8-bit encoded field where $\text{ROT}_{\text{AIS}} = 4.733 \sqrt{\text{ROT}_{\text{sensor}}}$. If the vessel lacks an external rate-of-turn gyro, the transponder broadcasts code `-128` (0x80, "not available") or derives a noisy, lagging mathematical derivative from successive GNSS COG samples.

### Worked Example: Close-Quarters Kinematic Discrepancy

Consider two commercial vessels approaching head-on in restricted visibility with a nominal closing speed of 30 knots (15.4 m/s). 

```
Ship A (Container Vessel):
  Reported AIS SOG: 16.0 kn (8.23 m/s)
  Reported AIS COG: 000.0°
  Reported AIS HDG: 004.0° (4° leeway due to easterly beam gale)

Ship B (Tanker):
  Reported AIS SOG: 14.0 kn (7.20 m/s)
  Reported AIS COG: 180.0°
  Reported AIS HDG: 180.0°
```

If Ship A's Class A transponder is configured with a 10-second reporting interval, the vessel travels 82.3 meters between successive VHF packet transmissions. If the watch officer on Ship B relies exclusively on unfiltered AIS vector projections without cross-referencing ARPA radar echoes:
- Over a 30-second interval, latency and tidal set can displace the actual physical hull position by over 250 meters relative to the last received AIS symbol.
- If Ship A's antenna offset $A$ was improperly entered as 20 m instead of 320 m, Ship B's ECDIS projects a CPA of 150 meters (passing clear), while in physical reality the container vessel's flared bulbous bow will collide with the tanker.

### Real-Time Validation Procedure for Bridge Watchstanders

To mitigate data corruption and sensor failures, watchstanders and pilots must apply a systematic validation workflow:

1. **Heading vs. COG Consistency Check:** Compare broadcast `HDG` against `COG`. While slight drift ($1^\circ$–$3^\circ$) reflects hydrodynamic leeway caused by wind or cross-currents, a sustained divergence exceeding $15^\circ$ indicates a frozen gyro repeater or a transponder defaulting to `511` ("not available").
2. **Target Association with Radar:** Never alter course based on an AIS target icon that cannot be validated by a corresponding radar return or visual bearing (IEC 62388 radar-AIS target association). A ghost target without a radar echo indicates spoofing, multipath reflection, or an incorrectly assigned MMSI ([Chapter 59](ch59-spoofing.md)).
3. **Verify Reporting Cadence:** Monitor target age indicators on ECDIS. If an approaching target's last valid position report exceeds 30 seconds in coastal waters, flag the target as "lost" or degraded, and immediately revert to primary ARPA radar tracking.

---

> **Try it.**
> Decode raw NMEA 0183 sentences from a real shipboard pilot-plug data stream using Python and `pyais` to extract verified tactical kinematics and vessel dimensions. Run this script in the book's Python virtual environment:
>
> ```python
> import pyais
> 
> # Raw NMEA 0183 sentences recorded from an active ship conning position
> nmea_records = [
>     "!AIVDM,1,1,,A,15MwpU@01prtlJ0H9J@<Can00000,0*27",
>     "!AIVDM,2,1,0,B,55MwpUH29E41LAS7;?@pE1ADpF1A84@E80000016Bhj??4H80BhSlm3kP000,0*12",
>     "!AIVDM,2,2,0,B,00000000000,2*27",
> ]
> 
> # Decode dynamic position report (Message 1) and static voyage data (Message 5)
> pos_msg = pyais.decode(nmea_records[0])
> static_msg = pyais.decode(nmea_records[1], nmea_records[2])
> 
> print(f"Target Name: {static_msg.shipname.strip()} ({static_msg.callsign.strip()})")
> print(f"MMSI:        {pos_msg.mmsi} | Nav Status: {pos_msg.status.name}")
> print(f"Kinematics:  SOG = {pos_msg.speed:.1f} kn | COG = {pos_msg.course:.1f}° | HDG = {pos_msg.heading}°")
> print(f"Dimensions:  Length = {static_msg.to_bow + static_msg.to_stern} m | Beam = {static_msg.to_port + static_msg.to_starboard} m")
> print(f"Antenna Ref: Bow Offset (Dim A) = {static_msg.to_bow} m | Port Offset (Dim C) = {static_msg.to_port} m")
> ```
>
> Expected output:
> ```text
> Target Name: NEPTUNE TRADER (WDX1234)
> MMSI:        366999701 | Nav Status: UnderWayUsingEngine
> Kinematics:  SOG = 12.0 kn | COG = 315.0° | HDG = 315°
> Dimensions:  Length = 200 m | Beam = 30 m
> Antenna Ref: Bow Offset (Dim A) = 150 m | Port Offset (Dim C) = 15 m
> ```

---

> **Case file.**
> **The *Huayang Endeavour* and *Seafrontier* Collision (MAIB Report 7/2018).**
> On 1 July 2017 at 03:04 local time, the Hong Kong-registered bulk carrier *Huayang Endeavour* collided with the loaded oil tanker *Seafrontier* in the Dover Strait Traffic Separation Scheme. Both vessels were fitted with operational Class A AIS and modern ARPA radars. In the minutes leading to the collision, the bridge teams identified each other via AIS and established direct VHF radio communication on Channel 13 to coordinate an overtaking and crossing maneuver. 
> 
> The MAIB investigation concluded that the attempt to negotiate collision avoidance over VHF radio created conflicting mental models. The conversation was ambiguous, imprecise, and contrary to COLREGs Rules 14, 15, and 16. While bridge officers focused their attention on negotiating an unorthodox passing agreement over the radio, neither vessel took timely, decisive action in accordance with the rules of the road. By the time the misunderstanding was recognized, the ships were locked in a close-quarters situation, resulting in structural hull breaches. The MAIB forcefully reiterated that AIS-assisted VHF negotiations frequently convert safe passing situations into collisions.

---

> **Rule of thumb.**
> **The Two-Mile Rule for VHF Negotiations.** Never use VHF radiotelephone to negotiate collision-avoidance maneuvers when the Closest Point of Approach (CPA) is less than two nautical miles. At closing speeds typical of commercial shipping, verbal negotiations consume critical minutes, create false assumptions of agreement, and distract watchstanders from executing bold, standard maneuvers under the COLREGs. Use AIS to establish identity; use the rudder and engines to avoid collision.

---

## Software

The software tools supporting at-sea tactical operations reflect three commercial and operational tiers:

- **Open source:** 
  - **OpenCPN** (GPLv2+): Widely adopted open-source chartplotter and navigation tool running on Linux, Windows, macOS, and Android. It provides real-time AIS target tracking, programmable CPA/TCPA alarm rings, visual swept-path hulls, and AIS-SART homing overlays. *Caveat:* OpenCPN is not certified as an ECDIS under IMO/IEC standards; it cannot be legally used as a primary navigation display on SOLAS-regulated commercial ships.
  - **pyais** (MIT): High-performance Python library for decoding raw NMEA 0183 `!AIVDM`/`!AIVDO` sentences and IEC 61162-450 network packets. Supports Messages 1 through 27 and standard Application-Specific Messages. *Caveat:* Ingestion engines must implement external buffer management to handle fragmented multi-line sentences (e.g., Message 5) that arrive interleaved across noisy networks.
- **Free but closed:** 
  - **Navionics Boating App** (Garmin): Widely used mobile and tablet charting software featuring live AIS target overlays when connected via local Wi-Fi to onboard NMEA multiplexers or Class B transponders. *Caveat:* AIS display and target rendering are optimized for leisure craft; it lacks the granular sensor error alarms, ROT predictors, and antenna offset rendering required for professional pilotage.
- **Commercial:** 
  - **Wärtsilä Navi-Harbour / Transas Pilot PRO**: High-end commercial Portable Pilot Unit (PPU) software suite specifically designed for harbor and maritime pilots. It ingests dual-antenna RTK GNSS streams alongside pilot-plug AIS telemetry to render sub-decimeter docking predictions, dynamic lock clearances, and predictive swept-path hydrodynamic vectors. *Caveat:* Highly expensive commercial licensing and proprietary hardware dongles restrict access strictly to professional pilotage authorities.

---

## Standards & guides

- **IMO Resolution MSC.74(69), Annex 3 (1998):** *Recommendation on Performance Standards for a Universal Shipborne Automatic Identification System (AIS).* Establishes international functional requirements, mandating ship-to-ship collision avoidance, VTS reporting, and coastal surveillance capabilities.
- **IMO Resolution A.1106(29) (2015):** *Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems (AIS).* Primary operational standard for mariners; governs reporting intervals, manual data input obligations, operational limitations, and bridge procedures.
- **IMO SN/Circ.227 (2003):** *Guidelines for the Installation of a Shipborne Automatic Identification System (AIS).* Defines hardware installation criteria, antenna physical separation, power supplies, and conning-position pilot-plug pinout standards.
- **ITU-R Recommendation M.1371-5 (2014):** *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile frequency band.* Defines the technical foundation of the physical, link, and message layers across all station classes.
- **IEC 61993-2:2018 (Ed. 3.0):** *Maritime navigation and radiocommunication equipment and systems – Automatic Identification Systems (AIS) – Part 2: Class A shipborne equipment.* Prescribes test methods, performance benchmarks, and interface specifications for type-approved Class A transponders.
- **IEC 61162-1:2016 (Ed. 5.0):** *Digital interfaces – Part 1: Single talker and multiple listeners.* Standardizes the NMEA 0183 serial interface strings (`!AIVDM`, `!AIVDO`) connecting AIS units to bridge consoles and pilot plugs.
- **IALA Guideline G1028 (Ed. 1.3, 2004):** *The Selection and Presentation of Aids to Navigation Marks on Shipborne Navigational Displays.* Historical operational guide detailing the presentation of physical and synthetic AIS AtoN targets.
- **IALA Guideline G1082 (Ed. 1, 2011):** *An Overview of AIS.* Comprehensive technical summary of system architecture, operational services, and ship-handling interactions.
- **World Sailing Offshore Special Regulations (2024–2025):** Governing regulations for international offshore yacht racing; mandates Class A/B transponders and personal AIS-MOB devices across Categories 0–3.
- **US Code of Federal Regulations, 33 CFR § 164.46 (2015/2020):** United States statutory rules governing commercial AIS carriage thresholds, pilot plug electrical compliance, and operating procedures in US navigable waters.

---

## Pitfalls

1. **Confusing heading with Course Over Ground:** Interpreting `COG` as the vessel's physical heading $\rightarrow$ in cross-currents or heavy winds, a drifting vessel's heading and ground track can diverge by tens of degrees $\rightarrow$ always verify `HDG` on the ECDIS to determine where the target's bow is physically pointing before planning a close passing maneuver.
2. **The "VHF arrangement" trap:** Calling an approaching ship on VHF to agree on non-standard passing maneuvers rather than executing standard COLREG obligations $\rightarrow$ ambiguous verbal agreements lead to conflicting mental models and loss of situational awareness $\rightarrow$ adhere strictly to COLREGs Rules 14–17; use VHF only to confirm compliant intentions.
3. **Assuming every target has AIS:** Treating the AIS display as a complete, comprehensive picture of surrounding traffic $\rightarrow$ small craft, naval vessels, wooden fishing boats, and floating debris are often not equipped or transmitting $\rightarrow$ always maintain a vigilant visual lookout and continuous radar watch per COLREGs Rule 5.
4. **Ignoring antenna reference point offsets:** Assuming the broadcast GNSS coordinate corresponds to the center of the vessel's hull $\rightarrow$ on modern container ships and bulkers, the conning bridge and GNSS antenna may be located 300 m aft of the bow $\rightarrow$ inspect Message 5 dimensions ($A, B, C, D$) to verify the target's true physical envelope in narrow channels.
5. **Relying on stale Navigational Status:** Expecting the target's broadcast status (`01` At anchor, `00` Under way) to accurately reflect its real-time operational state $\rightarrow$ navigational status is a manual input frequently neglected by bridge teams upon heaving anchor $\rightarrow$ corroborate status flags against dynamic SOG, ROT, and engine exhaust plumes.
6. **Underestimating Class B update latency:** Anticipating that small craft and workboats fitted with Class B transponders will report at Class A cadences $\rightarrow$ Class B units report every 15 to 30 seconds when moving, and their packets can be starved during periods of high VDL slot congestion $\rightarrow$ expand CPA safety buffers when maneuvering near Class B targets.
7. **Neglecting gyrocompass repeater failure:** Trusting an AIS heading vector that matches neither the target's wake nor its radar trail $\rightarrow$ a failed or unsynchronized stepper motor in the ship's gyro repeater causes the transponder to broadcast frozen or wandering heading data $\rightarrow$ cross-reference target heading against observed radar history trails.
8. **Misinterpreting AIS-SART emergency icons:** Dismissing a 970-series target appearing on the screen as a normal commercial vessel $\rightarrow$ watchstanders unfamiliar with special MMSI schemes fail to recognize an active distress situation $\rightarrow$ train bridge teams to immediately identify 970-series identifiers as active emergency beacons and initiate SAR protocols.
9. **Pilot plug interface baud rate mismatch:** Connecting a PPU or data logger at standard NMEA 4,800 baud instead of high-speed 38,400 baud $\rightarrow$ the pilot plug operates under IEC 61162-2 high-speed specifications; a 4,800 baud terminal will receive garbled data or buffer overruns $\rightarrow$ ensure all pilot-plug serial devices are locked to 38,400 baud, 8 data bits, 1 stop bit, no parity.
10. **Over-reliance on target CPA/TCPA calculations during maneuvers:** Assuming that a safe calculated CPA will persist while one or both vessels are actively turning $\rightarrow$ standard ECDIS CPA/TCPA calculations assume constant velocity vectors $\rightarrow$ monitor rate of turn and visually verify maneuver completion before relaxing watch vigilance.

---

## Key takeaways

- **AIS is a cooperative, tactical digital lookout:** It provides immediate kinematic and identity parameters that penetrate radar sea clutter, blind bends, and adverse weather, but it never replaces primary radar and visual lookouts.
- **Pilotage efficiency hinges on the pilot plug:** Standardized conning-position interfaces allow Portable Pilot Units (PPUs) to render millimeter-accurate swept-path envelopes and docking velocities.
- **Direct bridge-to-bridge calling by name eliminates ambiguity:** Knowing the exact name and call sign of an approaching vessel prevents chaotic, misaddressed VHF calls in crowded channels.
- **VHF radio negotiations must never supersede the COLREGs:** "VHF-assisted collisions" occur when officers substitute informal, ambiguous radio conversations for timely rudder and engine action.
- **Physical dimensions matter in confined waters:** On large commercial vessels, the distance between the GNSS antenna and the bow can exceed 300 meters; watchstanders must verify broadcast dimension offsets ($A, B, C, D$) during close-quarters encounters.
- **Towing, dredging, and offshore construction require specialized tracking:** Broadcasting correct Navigational Status codes and auxiliary gear markers alerts passing ships to unseen physical hazards such as long tows, dredge pipes, and seismic streamer spreads.
- **SAR operations rely on dedicated AIS homing:** Modern AIS-SARTs and AIS-MOB beacons paint unambiguous distress markers on bridge displays, accelerating survivor recovery.
- **Sensor integrity governs data validity:** AIS broadcasts reflect the health of connected gyrocompasses and GNSS units; always cross-reference AIS vectors with ARPA radar echoes and visual bearings.

---

## References

- Cruising Yacht Club of Australia (2024). *2024 Rolex Sydney Hobart Yacht Race Notice of Race*. Sydney: CYCA.
- International Association of Marine Aids to Navigation and Lighthouse Authorities (2004). *The Selection and Presentation of Aids to Navigation Marks on Shipborne Navigational Displays (AIS Volume 1, Part I -- Operational Issues)*. IALA Guideline G1028, Ed. 1.3. Saint-Germain-en-Laye: IALA.
- International Association of Marine Aids to Navigation and Lighthouse Authorities (2011). *An Overview of AIS*. IALA Guideline G1082, Ed. 1. Saint-Germain-en-Laye: IALA.
- International Electrotechnical Commission (2016). *Maritime navigation and radiocommunication equipment and systems -- Digital interfaces -- Part 1: Single talker and multiple listeners*. IEC Standard 61162-1:2016 (Ed. 5.0). Geneva: IEC.
- International Electrotechnical Commission (2018). *Maritime navigation and radiocommunication equipment and systems -- Automatic Identification Systems (AIS) -- Part 2: Class A shipborne equipment of the universal automatic identification system (AIS) -- Operational and performance requirements, methods of test and required test results*. IEC Standard 61993-2:2018 (Ed. 3.0). Geneva: IEC.
- International Marine Contractors Association (2022). *The Training and Experience of Key DP Personnel*. IMCA Guidance Document M 117 Rev. 3. London: IMCA.
- International Maritime Organization (1998). *Adoption of New and Amended Performance Standards for Navigational Equipment*. IMO Resolution MSC.74(69), Annex 3: *Recommendation on Performance Standards for a Universal Shipborne Automatic Identification System (AIS)*. London: IMO.
- International Maritime Organization (2000). *Adoption of Amendments to the International Convention for the Safety of Life at Sea, 1974, as Amended (SOLAS Chapter V, Regulation 19)*. IMO Resolution MSC.99(73). London: IMO.
- International Maritime Organization (2003). *Guidelines for the Installation of a Shipborne Automatic Identification System (AIS)*. IMO Circular SN/Circ.227. London: IMO.
- International Maritime Organization (2015). *Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems (AIS)*. IMO Resolution A.1106(29). London: IMO.
- International Telecommunication Union (2014). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile frequency band*. Recommendation ITU-R M.1371-5. Geneva: ITU-R.
- Marine Accident Investigation Branch (2018). *Report on the Investigation of the Collision between the Hong Kong Registered Bulk Carrier Huayang Endeavour and the Hong Kong Registered Oil Tanker Seafrontier in the Dover Strait on 1 July 2017*. MAIB Report No. 7/2018. Southampton: MAIB.
- National Transportation Safety Board (2015). *Collision of Towing Vessel Caribe Surf and Bulk Carrier Kriti Filoxenia, Corpus Christi Ship Channel, Texas, May 14, 2014*. NTSB Marine Accident Brief MAB-15/10. Washington, D.C.: NTSB.
- Oil Companies International Marine Forum & Chemical Distribution Institute (2013). *Ship to Ship Transfer Guide for Petroleum, Chemicals and Liquefied Gases*. 1st ed. Edinburgh: Witherby Seamanship International.
- United States Coast Guard (2015). *Title 33, Code of Federal Regulations, Section 164.46: Automatic Identification System*. 80 FR 5282. Washington, D.C.: Government Publishing Office.
- United States Navy (2017). *Comprehensive Review of Recent Surface Force Incidents*. Washington, D.C.: Department of the Navy.
- World Sailing (2024). *Offshore Special Regulations 2024--2025: Governing Offshore Racing for Monohulls & Multihulls*. London: World Sailing.
