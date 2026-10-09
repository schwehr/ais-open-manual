# Chapter 2 — The many uses of AIS data

> **Part I — Why AIS? Uses and users.** A taxonomy and technical assessment of how a tactical collision-avoidance broadcast became the central observational infrastructure for global ocean operations, commerce, science, and policy.

**In this chapter.** You will learn how raw maritime VHF broadcasts evolved beyond navigational safety into a universal planetary sensor network. We establish an operational taxonomy spanning thirteen maritime domains: safety and collision avoidance, Vessel Traffic Services (VTS) and port logistics, search and rescue (SAR), maritime security and law enforcement, fisheries regulation and illicit activity monitoring, environmental protection, oceanographic and atmospheric science, global trade nowcasting and commodity finance, hydrographic surveying and chart production, marine spatial planning and offshore energy, critical subsea infrastructure defense, maritime journalism and open-source intelligence (OSINT), and humanitarian emergency operations. For each application, you will evaluate the exact broadcast message types required, update latency tolerances, data quality thresholds, and operational failure modes. You will examine the transition from historical coastal voice reports to automated geospatial machine-learning pipelines, execute a spatial traffic density normalization query in DuckDB, and review concrete procedures for screening degraded or intentionally manipulated telemetry.

## 2.1 The accidental global sensor

The Automatic Identification System (**AIS**) is the quintessential accidental planetary sensor network. Codified by the International Maritime Organization (**IMO**) in Regulation 19 of SOLAS Chapter V (IMO 2000), the protocol was designed to solve three local problems: autonomous ship-to-ship collision avoidance, automated reporting to coastal Vessel Traffic Services (**VTS**), and coastal vessel tracking within line-of-sight VHF radio range (ITU-R M.1371-5 2014; Cutlip 2017). Transmissions were broadcast unencrypted and unauthenticated over maritime VHF channels using decentralized Self-Organizing Time Division Multiple Access (**SOTDMA**).

Nobody designing the protocol anticipated that Low Earth Orbit (**LEO**) satellites would capture these line-of-sight bursts from space (Høye et al. 2008), or that commodity GPU clusters would ingest tens of billions of position reports annually to map global trade, enforce sanctions, track illicit fishing, and monitor ecological sanctuaries (Kroodsma et al. 2018; Cerdeiro et al. 2020; Paolo et al. 2024).

This expansion created a structural tension between **tactical mariners** and **macro-scale data analysts**. For the bridge watchstander ([Chapter 1](ch01-what-ais-is.md); [Chapter 53](ch53-mariner-training.md)), AIS is a digital lookout: latency must not exceed seconds, relative geometric vectors must remain reliable, and coverage dropouts can lead directly to collisions. For an economist nowcasting gross domestic product (Cerdeiro et al. 2020) or an oceanographer estimating acoustic noise fields (Jalkanen et al. 2009), latency of hours or days is acceptable, but coverage bias, kinematic noise, and identity spoofing demand systematic statistical filtering.

This chapter maps the complete taxonomy of AIS data applications across five technical axes: required message sets, latency budgets, coverage requirements, data quality tolerances, and failure consequences.

## 2.2 Operational taxonomy of AIS applications

The diverse user base of AIS spans naval commands, artisanal fishers, commodity trading desks, and marine biologists. Table 2.1 details thirteen application sectors, mapping their technical constraints and failure penalties.

| Sector | Primary Users | Messages | Latency | Coverage | Quality Bar | Failure Consequences |
|---|---|---|---|---|---|---|
| **Safety of Navigation** | Bridge officers, pilots | 1, 2, 3, 18, 19 | 1–10 s | Coastal VHF (10–30 nmi) | Kinematic validity; valid HDG | Collision, grounding ([Chapter 55](ch55-incidents-and-accidents.md)) |
| **VTS & Port Ops** | Port authorities, pilots | 1, 2, 3, 4, 5, 12, 20 | 2–30 s | Coastal base stations | Valid MMSI, draught, dimensions | Berth collisions, channel blockages ([Chapter 4](ch04-vts-and-ports.md)) |
| **Search & Rescue** | Coast guards, JRCCs, aircraft | 1, 2, 3, 9, 14, 21 | <30 s | Coastal VHF, airborne, satellite | Reliable positions, SART MMSI | Diverted rescue craft, expanded datum ([Chapter 68](ch68-special-purpose-ais.md)) |
| **Security & Enforcement** | Navies, coast guards, customs | 1, 2, 3, 5, 18, 24 | Seconds–min | Terrestrial, satellite, radar | Cross-sensor fusion; anti-spoofing | Undetected breaches, sanctions evasion ([Chapter 8](ch08-security-and-national-security-uses.md)) |
| **Fisheries & IUU** | Fisheries agencies, RFMOs | 1, 2, 3, 5, 18, 24 | Minutes–hrs | High-seas satellite constellations | Continuous track; speed profiles | Depleted fisheries, poaching in MPAs ([Chapter 6](ch06-fisheries-iuu-dark-fleets.md)) |
| **Environmental Protection**| Regulators, sanctuary managers | 1, 2, 3, 5, 8 (ASMs) | Real-time–batch | Coastal networks, satellite feeds| Dimensions, STW; ASM integrity | Whale strikes, acoustic pollution ([Chapter 7](ch07-environment-and-science.md)) |
| **Ocean Science** | Oceanographers, modelers | 1, 2, 3, 8 (met/hydro)| Hours–weeks | Global oceanic archives | Timestamping, drift validation | Erroneous current models, biased reanalyses |
| **Trade & Logistics** | Commodity desks, macro funds | 1, 2, 3, 5 | Minutes–daily | Global satellite and port feeds | Destination parsing, draught changes | Erroneous inventory nowcasts ([Chapter 5](ch05-traders-finance-nowcasting.md)) |
| **Hydrography** | Hydrographic offices (NOAA, UKHO)| 1, 2, 3, 5, 18 | Batch (annual) | Coastal water archives | Density de-biasing, draught filters | Shallow hazards, obsolete routing ([Chapter 51](ch51-charts-enc-ecdis.md)) |
| **Marine Spatial Planning** | Planners, wind farm developers| 1, 2, 3, 5, 18, 19 | Batch (annual) | Multi-year EEZ archives | Vessel class and coverage normalization| Siting turbines in fairways, spatial conflict |
| **Subsea Cable Defense** | Telecom and pipeline operators | 1, 2, 3, 5, 18 | Real-time (<60 s)| Coastal VHF, low-latency LEO | SOG tracking (<1.5 kn), geofencing | Severed fiber cables, pipeline ruptures |
| **Journalism & OSINT** | Investigative journalists | 1, 2, 3, 5, 18, 24 | Minutes–days | Aggregated global feeds | Multi-source checks, spoofing circles | Retracted reporting, false accusations |
| **Humanitarian SAR** | NGOs, civilian rescue vessels | 1, 2, 3, 5, 14, 19 | Real-time (<60 s)| Coastal terrestrial and satellite | Reliable rescue craft tracks | Unassisted capsizing, interdiction impasses |

*Table 2.1: Technical characteristics, latency, and operational constraints across maritime AIS application domains.*

## 2.3 Navigation, safety, and traffic management

### 2.3.1 Tactical collision avoidance and bridge operations
On the bridge of a commercial vessel, AIS functions as an adjunct to primary radar and visual lookouts. Under the International Regulations for Preventing Collisions at Sea (**COLREGs**), mariners must use all available means to determine if risk of collision exists. Transponders continuously broadcast dynamic position reports (Messages 1, 2, and 3 for Class A; Messages 18 and 19 for Class B) containing latitude, longitude, Speed Over Ground (**SOG**), Course Over Ground (**COG**), and True Heading (**HDG**). 

Integrated bridge navigation systems and Electronic Chart Display and Information Systems (**ECDIS**) ingest these packets via NMEA 0183 (`!AIVDM` sentences) or IEC 61162-450 Ethernet streams ([Chapter 26](ch26-interfaces-and-logging.md); [Chapter 51](ch51-charts-enc-ecdis.md)). The ECDIS computes Closest Point of Approach (**CPA**) and Time to Closest Point of Approach (**TCPA**):

$$\text{CPA} = \min_{t \ge 0} \|\mathbf{p}_A(t) - \mathbf{p}_B(t)\|$$

where $\mathbf{p}_A(t)$ and $\mathbf{p}_B(t)$ represent projected Cartesian coordinates of ship $A$ and ship $B$ based on velocity vectors $(\mathbf{v}_A, \mathbf{v}_B)$. 

Unlike raw radar echoes, which require multiple antenna sweeps for an Automatic Radar Plotting Aid (**ARPA**) to establish a tracking filter, an AIS broadcast delivers immediate kinematic vectors. Furthermore, VHF signals propagate around headlands via knife-edge diffraction, revealing approaching traffic hidden behind blind bends before radar can acquire line of sight. AIS broadcasts the vessel's call sign, name, and MMSI. In congested waterways, watchstanders no longer broadcast ambiguous VHF voice calls ("vessel on my port bow steering west"); they directly hail the target by name over VHF Channel 13 or 16 ([Chapter 3](ch03-at-sea-operations.md)).

### 2.3.2 Vessel Traffic Services (VTS) and port optimization
VTS centers operate under IMO Resolution A.1158(32) to monitor and coordinate vessel movement in hazardous coastal corridors and port approaches ([Chapter 4](ch04-vts-and-ports.md)). Prior to AIS, VTS operators tracked traffic using shore radar supplemented by compulsory VHF voice check-in points. Integrating AIS base stations directly into VTS operations desks transformed traffic management:
- **Automated identification:** As a vessel enters a VTS coverage zone, its MMSI, dimensions, and declared destination (Message 5) immediately link to local port databases.
- **Dynamic fairway geofencing:** VTS software enforces automated guard zones around dredged navigation channels, traffic separation schemes (**TSS**), and restricted anchorages. An alarm triggers if a deep-draught bulk carrier strays outside a channel prism or if a tanker's SOG exceeds harbor speed limits.
- **Just-In-Time (JIT) port arrivals:** High-density ports utilize real-time speed profiles to coordinate lock transits, tug assignments, line handlers, and pilot boarding times, minimizing offshore anchorage idle time and associated bunker fuel consumption.

### 2.3.3 Search and Rescue (SAR) datum calculations
When a maritime disaster occurs, Joint Rescue Coordination Centers (**JRCCs**) employ the Search and Rescue Computer Aided Operations System (**SARCOPS**) or equivalent drift-modeling tools to compute the search **datum**—the probable drift area of survivors or lifeboats under prevailing winds and sea currents. AIS contributes to SAR operations through two distinct mechanisms:
1. **Search asset tracking and surface drift measurement:** Commercial ships responding to automated distress calls are tracked in real time. Their dead-reckoning drift while on scene provides empirical surface current observations that refine SAR drift calculations.
2. **Dedicated SAR transponders:** AIS Search and Rescue Transmitters (**AIS-SARTs**, Message 14 and 1) broadcast distinctive 970-series MMSI identifiers (`970XXXXXX`), painting a coded circle on nearby ship radar displays and ECDIS consoles, directing rescuers straight to liferafts ([Chapter 68](ch68-special-purpose-ais.md)).

## 2.4 Monitoring, surveillance, and enforcement

### 2.4.1 Fisheries enforcement, IUU detection, and dark fleets
Historically, fisheries authorities relied solely on proprietary Vessel Monitoring Systems (**VMS**), which transmitted periodic satellite position reports directly to national flag-state enforcement agencies. Because VMS data remained confidential, civil society and international inspectors could not evaluate high-seas fishing activity. The advent of satellite AIS transformed fisheries transparency.

In a landmark analysis processing over 22 billion AIS positions, Kroodsma et al. (2018) demonstrated that industrial fishing operations cover more than 55% of the ocean's surface area. Using deep convolutional neural networks applied to AIS kinematic parameters, researchers classified vessel gear types (longliners, purse seiners, trawlers, squid jiggers) and detected discrete fishing behavior based on distinctive maneuvering patterns: trawlers pulling nets exhibit low sustained speeds (2–4 kn [3.7–7.4 km/h]), while longliners exhibit zig-zag patterns with alternating setting and hauling phases.

This analytical capability exposed widespread Illegal, Unreported, and Unregulated (**IUU**) fishing ([Chapter 6](ch06-fisheries-iuu-dark-fleets.md)):
- **Encroachment into Marine Protected Areas (MPAs):** Vessels operating inside no-take marine reserves or national EEZs can be detected automatically (March et al. 2021).
- **At-sea transshipment:** Refrigerator cargo vessels ("reefers") rendezvous with fishing vessels on the high seas to offload catch and replenish provisions, obscuring catch origins. Algorithmic analysis of AIS tracks identifies loitering events where two vessels maintain identical coordinates and speeds ($\Delta \text{dist} < 100\text{ m}, \text{SOG} < 2\text{ kn}$) for hours in international waters.
- **The "dark fleet":** Vessels engaged in illicit operations frequently deactivate their transponders or manipulate their broadcast coordinates (Paolo et al. 2024). Cross-referencing satellite Synthetic Aperture Radar (**SAR**) imagery with real-time AIS feeds identifies non-broadcasting "dark vessels," focusing patrol cutter and maritime aircraft interdictions.

### 2.4.2 Security, border defense, and sanctions monitoring
Coast guards and naval operational commands ingest global AIS feeds into multi-sensor maritime domain awareness architectures ([Chapter 8](ch08-security-and-national-security-uses.md)). Analysts track vessels departing sanctioned terminals and identify deceptive shipping practices:
- **Flag hopping:** Frequent alterations of the country of registry and declared vessel name across Message 5 broadcasts.
- **GNSS spoofing circles:** Transponders broadcasting false positions that trace mathematically impossible geometric circles or mimic airport runways while the vessel is engaged in a clandestine ship-to-ship oil transfer miles away ([Chapter 59](ch59-spoofing.md); [Chapter 62](ch62-gnss-jamming-spoofing.md)).
- **Draught manipulation:** Monitoring static draught broadcasts before and after rendezvous events verifies cargo transfers even when the transponder has been intermittently deactivated.

> **Case file.** In October 2023, the Balticconnector subsea natural gas pipeline connecting Finland and Estonia was ruptured alongside parallel telecommunications cables in the Gulf of Finland. Regional maritime authorities and naval investigators cross-referenced pipeline telemetry with historical AIS positional feeds. Investigators matched the exact timeline and acoustic signatures of the pressure loss to the track of the container ship *Newnew Polar Bear*. Telemetry revealed the vessel maintained continuous forward motion while dragging its six-tonne anchor along the seabed for hundreds of nautical miles. Finnish authorities subsequently located and recovered the detached anchor beside the severed pipeline, matching paint scrapings and seabed drag furrows directly to the vessel's AIS track history.

### 2.4.3 Critical subsea infrastructure defense
Submarine telecommunication cables transmit over 95% of international internet traffic, while subsea pipelines convey vital oil and gas supplies across shallow continental shelves. Over 80% of cable damage events stem from surface maritime activities—specifically commercial vessels dragging anchor during severe weather or bottom trawlers towing heavy fishing gear across charted cable reserves.

Infrastructure protection centers employ automated AIS geofencing to protect seabed assets:
- **Corridor monitoring:** Software maintains vector buffers (500 m to 1 nmi [0.9–1.85 km]) around digitized cable and pipeline routes.
- **Kinematic anchoring detection:** Algorithms monitor vessels exhibiting SOG drops below 1.5 kn (2.8 km/h) in adverse weather conditions or displaying navigation status `1` ("At anchor") within a pipeline exclusion zone.
- **Predictive Closest Point of Approach (CPA):** When a vessel's projected velocity vector indicates an imminent corridor breach, automated alerting triggers coastal radar sweeps, marine VHF hailing calls to the bridge watch, or the dispatch of standby offshore patrol craft before the anchor snags the seabed asset.

## 2.5 Environmental protection and marine science

### 2.5.1 Marine mammal protection and ship strike mitigation
Collisions between large commercial vessels and cetaceans represent a major source of anthropogenic mortality for endangered whale populations, notably the North Atlantic right whale (*Eubalaena glacialis*). Because right whales frequently feed in shallow coastal waters near major shipping lanes, regulatory agencies and marine conservationists utilize AIS data to model, enforce, and verify protection zones (Wiley et al. 2011; [Chapter 7](ch07-environment-and-science.md)).

In the Boston harbor approaches through Massachusetts Bay, oceanographers and software engineers established the Right Whale AIS Project (**RAP**) (Schwehr and McGillivary 2007; McGillivary, Schwehr and Fall 2009). Near-real-time acoustic detection buoys deployed along the Traffic Separation Scheme detected right whale vocalizations. When an acoustic buoy identified whale calls within its listening radius, the detection software automatically composed an AIS Application-Specific Message (**ASM**, Message 8) broadcasting a dynamic circular "whale notice" zone. Vessels operating an AIS-integrated chart system received the warning directly on their ECDIS displays, alerting watchstanders to reduce vessel speed to 10 kn (18.5 km/h) or post additional lookouts. This operational pipeline demonstrated automated delivery of oceanographic hazard notices over the maritime VHF data link, pioneering techniques later deployed via mobile broadband in Whale Alert.

### 2.5.2 Atmospheric emissions modeling and acoustic footprints
Global commercial shipping generates substantial quantities of sulfur oxides ($\text{SO}_x$), nitrogen oxides ($\text{NO}_x$), and carbon dioxide ($\text{CO}_2$). Historically, international emissions inventories relied on top-down estimations based on global bunker fuel sales figures. 

The availability of high-resolution AIS tracking enabled bottom-up, physics-based emissions calculations. The Ship Traffic Emission Assessment Model (**STEAM**) developed by Jalkanen et al. (2009) established the methodological standard. STEAM ingests high-frequency AIS positional tracks, matches MMSI and IMO numbers against ship registry technical specifications (engine model, rated kilowatt output, design speed, propeller type), and calculates instantaneous power demand required to overcome hull hydrodynamic resistance at observed SOG:

$$P_{\text{inst}} = \frac{P_{\text{installed}}}{\eta} \left( \frac{\text{SOG}}{\text{Design Speed}} \right)^3 + P_{\text{auxiliary}}$$

Applying fuel-specific emissions factors to modeled engine load allows environmental researchers and regulatory bodies to construct kilometer-resolution emission inventories across international waters, evaluating real-world compliance of vessels transiting Emission Control Areas (**ECAs**).

Similarly, underwater radiated noise (**URN**) generated by commercial ship propellers and machinery elevates background acoustic levels in the 10 Hz to 1 kHz band, disrupting cetacean echolocation and communication. Marine acousticians integrate AIS traffic density tracks with hydrodynamic sound propagation models to map regional acoustic footprints, quantifying cumulative anthropogenic noise budgets across marine sanctuaries.

### 2.5.3 Oceanographic sensing and oil spill tracking
Beyond tracking ships, AIS data can be inverted to derive physical oceanographic parameters. When a ship's heading ($\text{HDG}$) and Speed Through Water ($\text{STW}$) from onboard dual-axis Doppler velocity logs are broadcast in Message 5 or dynamic sentences, the difference between observed ground track $(\text{COG}, \text{SOG})$ and water-referenced vectors $(\text{HDG}, \text{STW})$ reveals the local surface current velocity vector:

$$\mathbf{v}_{\text{current}} = \mathbf{v}_{\text{ground}} - \mathbf{v}_{\text{water}}$$

Schwehr and McGillivary (2007) established methods for using commercial ship AIS broadcasts during oil spill emergencies. By correlating the drift of distressed or anchored vessels with hydrodynamic transport models, emergency response teams refine spill boundary trajectories, track dispersant application vessels, and enforce safety exclusion zones around marine pollution incidents.

## 2.6 Commerce, logistics, and macroeconomic nowcasting

### 2.6.1 Commodity tracking and macroeconomic indicators
Seaborne trade accounts for over 80% of global merchandise trade by volume. Traditional international macroeconomic indicators—such as customs import/export declarations and national trade balance ledgers—lag real-world activity by weeks or months. 

Financial analysts, central banks, and international institutions now construct real-time macroeconomic indicators directly from raw AIS streams ([Chapter 5](ch05-traders-finance-nowcasting.md)). In a study for the International Monetary Fund, Cerdeiro et al. (2020) demonstrated that satellite AIS tracks could nowcast world seaborne trade volumes from scratch. By identifying port calls, extracting vessel deadweight tonnage (**DWT**), and tracking changes in static draught ($d$) between departure and arrival ports:

$$\Delta \text{Payload} \approx \text{TPC} \times (d_{\text{departure}} - d_{\text{arrival}})$$

where $\text{TPC}$ represents metric tons per centimeter immersion characteristic of the vessel's hull geometry, economists estimate bilateral physical cargo flows across dry bulk, liquid tanker, and container fleets in real time. During the COVID-19 pandemic, these automated AIS algorithms detected the collapse and subsequent rebound of global manufacturing output weeks before official quarterly trade statistics were published by national agencies.

### 2.6.2 Supply chain bottlenecks and fleet utilization
Commodity trading desks track the precise distribution of global petroleum and grain inventories at sea. By monitoring real-time tanker positions, traders calculate floating storage volumes: tankers remaining stationary ($\text{SOG} < 0.5\text{ kn}$) in offshore lightering zones indicate commercial contango conditions. Automated queuing metrics calculate real-time transit delays through the Suez Canal, Panama Canal, and Malacca Strait, allowing logistics providers to dynamically re-route container fleets.

## 2.7 Hydrography, mapping, and marine infrastructure

### 2.7.1 Hydrographic survey prioritization and chart verification
National hydrographic offices, including the United States National Oceanic and Atmospheric Administration (**NOAA**), the United Kingdom Hydrographic Office (**UKHO**), and Germany's Federal Maritime and Hydrographic Agency (**BSH**), maintain millions of square kilometers of nautical charts ([Chapter 51](ch51-charts-enc-ecdis.md)). Conducting high-resolution multibeam sonar bathymetric surveys is resource-intensive and expensive.

Hydrographers ingest multi-year AIS traffic databases to prioritize survey operations. Overlaying historical deep-draught vessel corridors onto legacy bathymetric charts reveals shallow anomalies or poorly surveyed rocks located near commercial shipping corridors. When hydrographic offices establish new two-way routes or adjust Traffic Separation Schemes at the IMO, AIS spatial density maps verify whether mariners actually comply with charted lanes or adopt non-standard navigational shortcuts.

### 2.7.2 Marine spatial planning and offshore energy development
The rapid expansion of offshore wind farms, tidal energy arrays, and marine protected areas has created intense competition for ocean space. Marine Spatial Planning (**MSP**) agencies require empirical baseline data to balance ecological protection, offshore energy construction, and traditional shipping corridors. Planners process satellite and coastal AIS data to generate multi-year traffic density heatmaps. These rasters establish statistical safety buffer zones around proposed offshore wind turbine foundations, ensuring that wind turbine installations do not infringe upon established international maritime traffic channels.

## 2.8 Journalism, humanitarian operations, and novel domains

### 2.8.1 Open-source intelligence (OSINT) and investigative journalism
Commercial ship tracking platforms (MarineTraffic, FleetMon, Spire, Kpler) have democratized access to maritime movements, turning AIS into a foundational tool for investigative journalism and open-source intelligence (**OSINT**):
- **Sanctions evasion reporting:** Investigative reporters trace covert petroleum transfers by identifying dark rendezvous windows, forged MMSIs, and sudden flag state registrations.
- **Environmental crime exposure:** News organizations utilize AIS tracking to uncover illegal sand dredging, hazardous waste dumping, and unauthorized fishing in protected coastal shoals.

> **Definitions that bite.**
> **Dark ship vs. Lost packet:** A vessel whose AIS transmissions do not appear on a commercial tracking map is routinely characterized in news reports as "a dark ship intentionally evading detection." In reality, an absence of position reports in a data feed can result from four entirely distinct phenomena: (1) intentional transponder power shutdown by the crew; (2) radio-frequency slot collision and receiver desensitization in high-density waterways where satellite receivers suffer extreme packet loss ([Chapter 30](ch30-network-loading-packet-loss.md); [Chapter 39](ch39-satellite-ais.md)); (3) terrestrial shore-station network outages or commercial provider ingestion pipeline filters; or (4) a legitimate master's decision under SOLAS Regulation V/19.2.4 to switch off AIS when navigating in waters threatened by piracy. Equating satellite packet absence directly with deliberate illicit activity is an analytical error.

### 2.8.2 Humanitarian rescue operations and migrant tracking
In the Mediterranean Sea, humanitarian non-governmental organizations (**NGOs**) operate civilian search and rescue vessels assisting unseaworthy migrant craft crossing from North Africa to southern Europe. AIS data plays a central operational and forensic role:
- **Coordination of rescue assets:** Watchstanders in Rome or Madrid observe responding civilian and commercial rescue vessels, coordinating on-scene SAR efforts.
- **Forensic incident reconstruction:** Following maritime interdictions, distress capsizings, or contested pushback encounters, international human rights investigators analyze historical AIS logs to establish precise timestamps, geometric positions, vessel speeds, and radar horizons, verifying or refuting official government accounts.

### 2.8.3 Academic machine learning and GNSS interference sensing
In computer science and transport engineering, global AIS archives represent the preeminent public benchmark for spatio-temporal trajectory mining, vessel path prediction, and anomaly detection algorithms (Tu et al. 2018; [Chapter 49](ch49-analytics-and-ml.md)). 

Furthermore, because commercial Class A AIS transponders broadcast the position, velocity, and timing derived from their internal GNSS receivers, global AIS monitoring networks function as distributed sensors for radio frequency interference. By mapping geographic clusters where dozens of ships simultaneously report invalid GNSS positions, zero satellites tracked, or positions jumping abruptly to municipal airports, space-weather scientists and electronic warfare analysts map the locations of terrestrial GNSS jamming and spoofing transmitters ([Chapter 62](ch62-gnss-jamming-spoofing.md)).

## Then & now

How the collection, processing, and application of maritime tracking data evolved over six decades:

- ⟨H⟩ 1965 — Benny Pettersson experiences a severe typhoon in Kobe harbor, planting the intellectual seed for an automated ship identification and collision-avoidance transponder.
- ⟨H⟩ 1973 — The Air Traffic Control Radar Beacon System (**ATCRBS**) demonstrates automated transponder coordination for aviation safety.
- ⟨H⟩ 1989 — The tanker *Exxon Valdez* runs aground on Bligh Reef in Prince William Sound, driving maritime nations toward mandatory electronic surveillance and coastal Vessel Traffic Services.
- ⟨H⟩ 1990 — Swedish Maritime Administration funds Håkan Lans and GP&C to develop autonomous Time Division Multiple Access radio transponders for aviation and maritime positioning.
- ⟨H⟩ 1998 — ITU adopts Recommendation ITU-R M.1371-0, standardizing the TDMA radio physical layer and core message layouts.
- ⟨H⟩ 2000 — IMO adopts revised SOLAS Chapter V (Resolution MSC.99(73)), mandating universal Class A AIS carriage for international voyage vessels above 300 GT.
- ⟨+⟩ 2002 — St. Lawrence Seaway implements the world's first mandatory operational AIS network with shore-to-ship Application-Specific Messages (lock schedules, water levels, wind).
- ⟨H⟩ 2002 — IMO Diplomatic Conference accelerates the global AIS carriage mandate to 2004 in response to post-9/11 maritime security imperatives.
- ⟨H⟩ 2004 — AIS Class A carriage mandate enters full legal effect across the global merchant shipping fleet.
- ⟨+⟩ 2006 — IEC standardizes Class B transponders (IEC 62287-1), opening broadcast tracking to small commercial craft, fishing boats, and pleasure vessels.
- ⟨+⟩ 2007 — MarineTraffic begins crowdsourcing terrestrial AIS receiver feeds over the public internet, democratizing ship tracking.
- ⟨+⟩ 2007 — Schwehr & McGillivary publish methods for utilizing AIS broadcasts in environmental disaster tracking and oil spill responses.
- ⟨+⟩ 2008 — First space-based AIS satellite tests (NTS-1) prove maritime VHF transmissions can be detected and decoded from Low Earth Orbit.
- ⟨+⟩ 2008 — Stellwagen Bank National Marine Sanctuary and USCG deploy the Right Whale AIS Project (RAP) in Massachusetts Bay.
- ⟨+⟩ 2009 — Jalkanen et al. publish the Ship Traffic Emission Assessment Model (STEAM), introducing physics-based atmospheric emission modeling from AIS.
- ⟨+⟩ 2010 — Kurt Schwehr releases `libais`, establishing high-performance open-source decoding of AIS bit payloads in C++ and Python.
- ⟨+⟩ 2012 — The Whale Alert mobile platform launches, transitioning acoustic cetacean hazard notices from VHF AIS ASMs to mobile broadband networks.
- ⟨+⟩ 2016 — Global Fishing Watch launches its public tracking platform, making high-seas industrial fishing effort transparent worldwide.
- ⟨+⟩ 2018 — Kroodsma et al. publish the first global footprint of industrial fisheries in *Science*, processing 22 billion AIS positions with deep convolutional neural networks.
- ⟨+⟩ 2020 — Cerdeiro et al. at the IMF publish real-time global trade nowcasting methods, estimating macroeconomic export volumes from raw ship kinematics.
- ⟨+⟩ 2021 — China enacts the Data Security Law and Personal Information Protection Law; terrestrial crowdsourced coastal AIS feeds from mainland ports sharply decline.
- ⟨+⟩ 2023 — Balticconnector pipeline rupture in the Gulf of Finland demonstrates the use of forensic AIS telemetry in investigating subsea critical infrastructure damage.
- ⟨+⟩ 2024 — Paolo et al. in *Nature* combine satellite AIS with orbital Synthetic Aperture Radar and optical imagery, quantifying the global scale of non-broadcasting dark vessels and offshore infrastructure.

## On the wire

The fundamental atomic data unit of vessel-tracking analytics is the **dynamic position report** (Message Types 1, 2, and 3 for Class A transponders). Understanding how these 168-bit payloads encode spatial parameters is essential for evaluating quantization error and computational fidelity.

Consider a Class A vessel broadcasting an uncompressed 168-bit dynamic report over VHF maritime frequency 161.975 MHz (AIS Channel A). The raw radio burst is received by a coastal receiver or satellite SDR and converted into a standard NMEA 0183 `!AIVDM` sentence:

```text
!AIVDM,1,1,,A,13aEO:0P00021bjd:K300?wn0000,0*11
```

Here is the bit-level anatomy of the payload:

| Field | Bit Length | Raw Value | Physical Decoded Value | Description |
|---|---|---|---|---|
| **Message Type** | 6 | `1` | 1 | Standard Scheduled Class A Position Report |
| **Repeat Indicator** | 2 | `0` | 0 | Do not repeat |
| **MMSI** | 30 | `244670000` | 244670000 | Netherlands flagged commercial vessel |
| **Navigational Status** | 4 | `0` | 0 | "Under way using engine" |
| **Rate of Turn (ROT)** | 8 | `0` | 0°/min | Not turning |
| **Speed Over Ground (SOG)**| 10 | `102` | 10.2 kn (18.9 km/h) | Resolution 0.1 kn; raw value / 10 |
| **Position Accuracy** | 1 | `0` | Low (>10 m) | Unaugmented autonomous GNSS |
| **Longitude** | 28 | `2548800` | 4.248000° E | Resolution 0.0001 min ($1/10000$ min) |
| **Latitude** | 27 | `31146000` | 51.910000° N | Resolution 0.0001 min ($1/10000$ min) |
| **Course Over Ground (COG)**| 12 | `850` | 85.0° | Resolution 0.1°; raw value / 10 |
| **True Heading (HDG)** | 9 | `84` | 84° | Resolution 1°; 511 indicates unavailable |
| **Time Stamp** | 6 | `35` | 35 s | Second of the UTC minute when burst occurred |
| **Maneuver Indicator** | 2 | `0` | 0 | Not available |
| **Spare** | 3 | `0` | - | Reserved |
| **RAIM Flag** | 1 | `0` | RAIM not in use | Receiver Autonomous Integrity Monitoring |
| **Radio Status** | 19 | `...` | SOTDMA state | Slot timeout and sub-message allocation |

A common software engineering pitfall in spatial trajectory analysis stems from the **coordinate quantization** implemented in ITU-R M.1371-5. Latitude and longitude are stored as two's complement signed integers in units of $1/10000$ of a minute of arc:

$$\text{Scale Factor} = \frac{1}{600,000}^{\circ} \approx 1.66667 \times 10^{-6 \circ}$$

At the equator, this represents a spatial discretization step of approximately $0.185\text{ m}$. In high-latitude waters ($60^{\circ}\text{ N}$), longitudinal precision contracts to approximately $0.093\text{ m}$. Floating-point processing pipelines that convert these values to 32-bit single-precision floats (`float32`) discard bit-level precision, inducing artificial spatial jitter into closest-point-of-approach calculations. Analytics engines must maintain coordinates as 64-bit IEEE 754 doubles (`float64`).

## Validation, uncertainty & data quality

Because AIS was designed as a local tactical radio broadcast rather than an auditable database feed, raw telemetry streams are riddled with sensor inaccuracies, configuration mistakes, and structural reception biases. Any analytical pipeline that blindly ingests raw `!AIVDM` streams will produce contaminated research and flawed operational decisions (Harati-Mokhtari et al. 2007; Fournier et al. 2018).

Data consumers must account for four distinct error categories:

### 1. Static metadata corruption (Human error)
Static and voyage parameters (Message 5 for Class A, Message 24 for Class B) are entered manually by the ship's crew via the Minimal Keyboard and Display (**MKD**). Studies indicate that 15% to 40% of vessels broadcast erroneous static data at any given time (Harati-Mokhtari et al. 2007):
- **Default dimensions:** Hundreds of vessels broadcast dimensions of $0 \times 0\text{ m}$, $1 \times 1\text{ m}$, or default manufacturer test values ($255 \times 63\text{ m}$).
- **Invalid draught:** Vessels frequently broadcast a draught of $0.0\text{ m}$, draughts exceeding the ship's physical length, or static load draughts that remain unchanged after offloading cargo.
- **Unformatted destination strings:** The 20-character destination field is free text. A destination like Rotterdam might be typed as `ROTTERDAM`, `NL RTM`, `ROTT`, `R'DAM`, `ROT`, or contain voyage commentary like `ARMED GUARDS ON BOARD` or `FOR ORDERS`.

### 2. Kinematic anomalies and sensor dropouts
- **Heading vs. COG discrepancies:** In strong cross-currents, leeway causes Course Over Ground to deviate naturally from True Heading. However, transponders with uncalibrated gyrocompass interfaces often broadcast fixed headings (`511` = not available, or permanent frozen angles like $0^\circ$) while COG changes continuously.
- **Speed extremes:** GNSS multi-path interference or interface baud-rate buffer overflows can generate momentary SOG spikes of $102.2\text{ kn}$ (the saturation value indicating $\ge 102.2\text{ kn}$) or impossible acceleration profiles.

### 3. Space-based reception bias (The high-density chokepoint problem)
Low Earth Orbit satellites carry AIS payloads at altitudes between 400 and 800 km. An orbital antenna's footprint covers a surface circular field of view spanning several thousand kilometers in diameter. Within this massive footprint, thousands of ships compete for the same 2,250 TDMA time slots available per minute on VHF channels 87B and 88B ([Chapter 21](ch21-link-layer-tdma.md)). In high-density chokepoints—such as the South China Sea, the English Channel, and the Malacca Strait—simultaneous broadcasts arrive at the satellite antenna in the same time slot. This co-channel packet collision destroys the packets, causing orbital detection rates to plummet below 5% for Class B and below 30% for Class A transponders ([Chapter 30](ch30-network-loading-packet-loss.md); [Chapter 39](ch39-satellite-ais.md)). Analysts must never confuse a lack of satellite AIS detections in high-density corridors with an absence of ships.

### 4. Detection probability normalization
When generating spatial density maps from shore-based receivers, the observed report count is a function of both true vessel traffic and the receiver's range-dependent detection probability ($P_{\text{detect}}$). A receiver located on an elevated headland detects almost 100% of transmissions within 15 nmi (27.8 km), but coverage decays towards the VHF radio horizon (30–40 nmi [55–74 km]). To prevent density maps from merely displaying receiver antenna patterns, raw cell counts must be normalized against a detection probability curve.

> **Worked example.**
> A spatial grid cell $C_k$ at a range of 24.2 nmi (44.8 km) from a coastal receiver records 23 position reports during a 1-hour observation window. Using a verified empirical range-attenuation model where detection probability is $P_{\text{detect}} = 1.0$ inside 15 nmi, and decreases linearly to $0.0$ at 35 nmi:
>
> $$P_{\text{detect}}(r) = \max\left(0.05, \min\left(1.0, 1.0 - \frac{r - 15}{35 - 15}\right)\right)$$
>
> For range $r = 24.2\text{ nmi}$:
>
> $$P_{\text{detect}}(24.2) = 1.0 - \frac{24.2 - 15}{20} = 1.0 - \frac{9.2}{20} = 1.0 - 0.46 = 0.54$$
>
> The raw observed count of 23 reports must be normalized to reflect true traffic:
>
> $$\text{Reports}_{\text{corrected}} = \text{round}\left(\frac{\text{Reports}_{\text{observed}}}{P_{\text{detect}}}\right) = \text{round}\left(\frac{23}{0.54}\right) = \text{round}(42.59) = 43\text{ reports}$$
>
> Failure to normalize by $P_{\text{detect}}$ would underestimate vessel presence in the outer cell by nearly 50%.

> **Try it.** The script `code/analytics/duckdb_density.py` executes this range-dependent detection probability correction directly against an AIS database using DuckDB. Run the script on the sample dataset `data/samples/synthetic_harbor.nmea`:
>
> ```bash
> . .venv/bin/activate
> python code/analytics/duckdb_density.py data/samples/synthetic_harbor.nmea --rx 42.36 -70.95
> ```
>
> Expected output:
> ```text
>  cell_lat  cell_lon  reports  vessels  range_nmi  p_detect  reports_corrected
>     42.28    -70.74       47        2       10.6      1.00               47.0
>     42.28    -70.72       42        2       11.5      1.00               42.0
>     42.24    -70.68       39        1       14.0      1.00               39.0
>     42.26    -70.70       38        1       12.8      1.00               38.0
>     42.30    -70.76       35        1        9.4      1.00               35.0
>     42.20    -70.62       35        1       17.6      0.87               40.0
>     42.32    -70.92       31        2        2.6      1.00               31.0
>     42.32    -70.80       26        1        7.4      1.00               26.0
>     42.28    -70.92       25        1        4.5      1.00               25.0
>     42.24    -70.94       25        1        6.7      1.00               25.0
>     42.30    -70.92       24        1        3.6      1.00               24.0
>     42.32    -70.78       24        1        8.1      1.00               24.0
>     42.26    -70.92       23        1        5.6      1.00               23.0
>     42.30    -70.42       23        2       24.2      0.54               43.0
>     42.32    -70.90       21        2        3.2      1.00               21.0
> ```

## Software

The software ecosystem for AIS data processing spans local bridge utilities, high-throughput streaming decoders, and distributed cloud analytics engines:

**Open source:**
- **`libais`:** High-performance C++ decoder with Python bindings authored by Kurt Schwehr. Decodes standard messages and international ASMs (SN.1/Circ.289). *Caveat:* Requires native C++ compilation.
- **`pyais`:** Pure Python decoder supporting NMEA AIVDM/AIVDO sentences and JSON serialization. *Caveat:* Python decoding throughput is slower than compiled C/Rust when processing gigabyte feeds.
- **`MovingPandas`:** Spatial-temporal trajectory library built on GeoPandas. Provides smoothing, stop detection, and aggregation. *Caveat:* In-memory architecture limits processing to RAM capacity.
- **`DuckDB`:** Embedded analytical SQL database engine optimized for columnar analytical queries on Parquet and CSV files. *Caveat:* Lacks native spatial indexing without the `spatial` extension.

**Free but closed:**
- **QGIS with Maritime Plugins:** Desktop GIS supporting spatial visualization of vessel track archives and GeoParquet layers. *Caveat:* Requires pre-processing to convert raw NMEA into spatial tables.
- **NOAA Marine Cadastre Vessel Traffic Viewer:** Web portal providing annual vessel density rasters and track data in US waters. *Caveat:* Historical data only; no real-time feeds.

**Commercial:**
- **Spire Maritime (Kpler):** Global satellite constellation and terrestrial AIS provider offering low-latency API streams and arrival models. *Caveat:* Expensive licensing; proprietary deduplication algorithms.
- **MarineTraffic / FleetMon (Kpler):** Terrestrial crowdsourced receiver network with satellite feeds, web mapping, and port arrival nowcasts. *Caveat:* Strict API query limits; variable crowdsourced coverage.
- **Global Fishing Watch (GFW):** Open-access data platform providing satellite AIS tracking and ML models dedicated to fisheries transparency. *Caveat:* Specialized for fishing rather than cargo logistics.

## Standards & guides

- **IMO Resolution MSC.74(69), Annex 3:** *Recommendation on Performance Standards for a Universal Shipborne Automatic Identification System (AIS)* (1998). Establishes operational requirements for shipborne AIS.
- **IMO Resolution MSC.99(73):** *Amendments to SOLAS Chapter V, Regulation 19* (2000). Mandates Class A AIS carriage on ships $\ge 300\text{ GT}$ on international voyages, $\ge 500\text{ GT}$ on domestic voyages, and all passenger ships.
- **IMO Resolution A.1106(29):** *Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems (AIS)* (2015). Operational handbook for bridge officers; authorizes turning off AIS when security is threatened.
- **IMO SN.1/Circ.289:** *Guidance on the Use of AIS Application-Specific Messages* (2010). Specifies international bit layouts for met/hydro and navigational binary messages.
- **ITU-R Recommendation M.1371-5:** *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band* (2014). Governs physical layer, TDMA scheduling, and message structures.
- **IEC Standard 61993-2:** *Class A shipborne equipment of the automatic identification system (AIS)* (Edition 3.0, 2018). Mandates hardware certification and software interface compliance for Class A transponders.

## Pitfalls

1. **Treating AIS as an auditable registry rather than unauthenticated radio telemetry.** Many static fields are entered manually via MKD. Pipelines that do not validate static data against official registries ingest massive volumes of typos, truncated strings, and default placeholder values.
2. **Assuming a missing ship has deliberately "gone dark" for illicit purposes.** Satellites passing over high-density shipping chokepoints experience RF packet collisions that destroy up to 90% of broadcasts. Telemetry gaps in chokepoints reflect physics, not necessarily evasion.
3. **Calculating distances and CPA with planar approximations.** Applying Euclidean distance formulas to latitude and longitude produces severe distortion at higher latitudes. Pipelines must calculate geodesic distances using the haversine formula or the Karney ellipsoidal method.
4. **Disregarding speed-dependent reporting intervals in temporal aggregation.** A Class A ship at anchor broadcasts every 3 minutes, while a ship underway at 20 kn broadcasts every 2 seconds. Aggregations counting raw message rows over-represent moving vessels by up to 90x relative to anchored ships.
5. **Storing scaled latitude and longitude as 32-bit floats.** Converting raw $1/10000$ minute integers into 32-bit floats discards precision, inducing artificial spatial jumps of several meters. Trajectory pipelines must retain coordinates as 64-bit IEEE 754 doubles.
6. **Failing to normalize spatial density maps against receiver range.** Shore-based receivers experience range-dependent reception loss. Binned spatial heatmaps that do not divide raw report counts by an empirical detection curve depict receiver antenna gains rather than true traffic.
7. **Confusing Speed Over Ground (SOG) with Speed Through Water (STW).** AIS reports contain SOG derived from GNSS, not water speed. Calculating hydrodynamic efficiency or emissions without adjusting for currents introduces severe errors into models like STEAM.
8. **Interpreting GNSS multi-path and spoofing spikes as legitimate vessel speeds.** Unfiltered AIS feeds contain occasional single-point position jumps implying speeds of hundreds of knots. Ingestion software must apply kinematic speed-gating filters ($\text{SOG} \le 40\text{ kn}$; acceleration $\le 2\text{ m/s}^2$).
9. **Misinterpreting MMSI mid-digits and test codes.** Transponders broadcasting MMSIs of `0`, `111111111`, `123456789`, or `1193046` are misconfigured radios, unprogrammed test units, or corrupt data. These must be screened out prior to analysis.
10. **Relying on AIS as a sole look-out in navigation.** AIS is not radar. Wooden craft, fiberglass yachts, submarines, non-compliant skiffs, and navigation hazards do not broadcast AIS. Relying solely on an AIS display violates Rule 5 of the COLREGs and directly causes groundings and collisions.

## Key takeaways

- AIS is an accidental global sensor: designed as a local, unencrypted VHF collision-avoidance link, it has evolved into global observational infrastructure for logistics, economics, enforcement, and science.
- The system spans thirteen domains, from sub-second bridge collision avoidance and VTS operations to macroeconomic trade nowcasts and benthic infrastructure defense.
- Latency and data quality requirements diverge by use case: bridge operations demand sub-second real-time delivery with zero kinematic tolerance, whereas economic models tolerate hours of latency but require statistical de-biasing.
- Dynamic tracking messages encode position to $1/10000$ of a minute of arc, requiring 64-bit floating point representations to prevent quantization precision loss.
- Satellite AIS reception suffers severe packet degradation in congested chokepoints due to TDMA slot collisions; absence of satellite reception is not conclusive proof of illicit evasion.
- Static voyage data contains high human error rates due to manual bridge data entry; analysts must clean, normalize, and cross-reference records against maritime registries.
- Physical emissions and acoustic models (such as STEAM) combine dynamic AIS speed tracking with vessel engineering specifications to generate kilometer-scale impact inventories.
- Spatial density analysis must correct for range-dependent detection probabilities to ensure heatmaps represent genuine vessel movements rather than antenna coverage footprints.

## References

1. Cerdeiro, D. A., Komaromi, A., Liu, Y. & Saeed, M. (2020). *World Seaborne Trade in Real Time: A Proof of Concept for Building AIS-based Nowcasts from Scratch* (IMF Working Paper WP/20/57). Washington, DC: International Monetary Fund.
2. Cutlip, K. (2017). *AIS for Safety and Tracking: A Brief History*. Washington, DC: Global Fishing Watch. https://globalfishingwatch.org/article/ais-brief-history/ (accessed 2026-10-06).
3. Fournier, M., Hilliard, R. C., Zhang, W. & Pelot, R. (2018). Use of Satellite AIS Data to Derive Vessel Movement Patterns and Identify Hotspots for Navigational Risk Assessment. *Ocean Engineering*, 162:210–223. doi:10.1016/j.oceaneng.2018.05.027.
4. Harati-Mokhtari, A., Wall, A., Brooks, P. & Wang, J. (2007). Automatic Identification System (AIS): Data Reliability and Human Error Implications. *The Journal of Navigation*, 60(3):373–389. doi:10.1017/S037346330700429X.
5. Høye, G. K., Eriksen, T., Meland, B. J. & Narheim, A. (2008). Space-based AIS for global maritime surveillance. *Acta Astronautica*, 62(2–3):240–245. doi:10.1016/j.actaastro.2007.07.001.
6. International Electrotechnical Commission (2018). *Maritime navigation and radiocommunication equipment and systems – Automatic Identification Systems (AIS) – Part 2: Class A shipborne equipment of the automatic identification system (AIS) – Operational and performance requirements, methods of test and required test results* (Standard No. IEC 61993-2:2018). Edition 3.0. Geneva: IEC.
7. International Maritime Organization (1998). *Recommendation on Performance Standards for a Universal Shipborne Automatic Identification System (AIS)* (Resolution MSC.74(69), Annex 3). Adopted 12 May 1998. London: IMO.
8. International Maritime Organization (2000). *Adoption of Amendments to the International Convention for the Safety of Life at Sea, 1974, as Amended (SOLAS Chapter V)* (Resolution MSC.99(73)). Adopted 5 December 2000. London: IMO.
9. International Maritime Organization (2010). *Guidance on the Use of AIS Application-Specific Messages* (Circular SN.1/Circ.289). London: IMO.
10. International Maritime Organization (2015). *Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems (AIS)* (Resolution A.1106(29)). Adopted 2 December 2015. London: IMO.
11. International Telecommunication Union (2014). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band* (Recommendation ITU-R M.1371-5). Geneva: ITU Radiocommunication Sector.
12. Jalkanen, J.-P., Brink, A., Kalli, J., Pettersson, H., Kukkonen, J. & Stipa, T. (2009). A modelling system for the exhaust emissions of marine traffic and its application in the Baltic Sea area. *Atmospheric Chemistry and Physics*, 9(23):9209–9223. doi:10.5194/acp-9-9209-2009.
13. Kroodsma, D. A., Mayorga, J., Hochberg, T., Miller, N. A., Boerder, K., Ferretti, F., Wilson, A., Bergman, B., White, T. D., Block, B. A., Woods, P., Sullivan, B., Costello, C. & Worm, B. (2018). Tracking the Global Footprint of Fisheries. *Science*, 359(6378):904–908. doi:10.1126/science.aao5646.
14. March, D., Metcalfe, K., Tintoré, J. & Godley, B. J. (2021). Tracking the global footprint of marine protected areas using AIS vessel data. *Biological Conservation*, 256:109040. doi:10.1016/j.biocon.2021.109040.
15. McGillivary, P. A., Schwehr, K. D. & Fall, K. (2009). Enhancing AIS to Improve Whale-Ship Collision Avoidance and Maritime Security. In *MTS/IEEE OCEANS 2009*, pages 1–9. Biloxi, MS: IEEE.
16. Paolo, F. S., Kroodsma, D. A., Raynor, J., Hochberg, T., Davis, P., Cleary, J., Marsaglia, L., Orofino, S., Thomas, C. & Halpin, P. N. (2024). Satellite mapping reveals extensive industrial activity at sea. *Nature*, 625(7993):85–91. doi:10.1038/s41586-023-06825-8.
17. Schwehr, K. D. & McGillivary, P. A. (2007). Marine Ship Automatic Identification System (AIS) for Enhanced Coastal Security Capabilities: An Oil Spill Tracking Application. In *MTS/IEEE OCEANS 2007*, pages 1–9. Vancouver, BC: IEEE. doi:10.1109/OCEANS.2007.4449285.
18. Tu, E., Yang, G., Mao, Z., Rasit, M., Mao, Y. & Ge, X. (2018). Exploiting AIS Data for Intelligent Maritime Navigation: A Comprehensive Survey from Data to Methodology. *IEEE Transactions on Intelligent Transportation Systems*, 19(8):2614–2635. doi:10.1109/TITS.2017.2764951.
19. Wiley, D. N., Hatch, L., Thompson, M., Pittman, S., Hughes, K. & Ware, C. (2011). Modeling speed restrictions to mitigate lethal collisions between ships and whales in the Stellwagen Bank National Marine Sanctuary. *Biological Conservation*, 144(9):2377–2381. doi:10.1016/j.biocon.2011.06.013.
