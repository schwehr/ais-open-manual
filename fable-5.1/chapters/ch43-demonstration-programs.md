# Chapter 43 — Demonstration programs and testbeds

> **Part VI — Receiving and collecting.** Shore-to-ship digital data links transformed from laboratory concepts into operational realities through regional testbeds, exposing the sharp architectural friction between constrained VHF broadcast channels and modern maritime data delivery.

**In this chapter.** You will learn how pioneering Automatic Identification System (**AIS**) demonstration programs and regional testbeds shaped the evolution of Application-Specific Messages (**ASMs**) and e-Navigation services from 2002 to the present. We trace the operational lineage of shore-originated AIS binary broadcasts, beginning with the bilateral St. Lawrence Seaway mandate of 2003 and the United States Coast Guard (**USCG**) Research & Development Center (**RDC**) trials in Tampa Bay. You will analyze the sensor-to-bridge architecture of the Right Whale AIS Project in Massachusetts Bay and discover why environmental alerting migrated from AIS Message 8 payloads to cellular applications like Whale Alert. We review major European e-Navigation projects—EfficienSea, ACCSEAS, MONALISA, and the Sea Traffic Management (**STM**) Validation Project—demonstrating how route exchange transitioned from VHF data links to IP-based maritime cloud infrastructures. Finally, we dissect the statutory success of European River Information Services (**RIS**) Inland AIS, examine Korea's national LTE-Maritime network, analyze VHF Data Exchange System (**VDES**) and R-Mode trials, and examine the technical and economic factors that limited broad commercial uptake of AIS binary messaging.

## 43.1 The St. Lawrence Seaway AIS mandate: the first North American testbed

The Saint Lawrence Seaway was the first North American waterway to mandate universal AIS carriage on commercial transit vessels. Under joint US and Canadian regulations by the Saint Lawrence Seaway Development Corporation (**SLSDC**, now the Great Lakes St. Lawrence Seaway Development Corporation, **GLS**) and Canada's St. Lawrence Seaway Management Corporation (**SLSMC**), carriage took effect on March 25, 2003 (68 FR 9551, Feb. 28, 2003; 33 CFR § 401.20). This rule predated general US domestic carriage under 33 CFR § 164.46 by over a year and preceded IMO SOLAS Chapter V regulation 19 deadlines for many commercial vessel classes.

Under 33 CFR § 401.20, commercial vessels requiring pre-clearance that are $300\text{ GT}$ or greater, have a length overall (**LOA**) exceeding $20\text{ m}$, or carry more than 50 passengers for hire must operate an approved Class A transponder. Commercial tugs, dredges, and floating plants greater than $8\text{ m}$ LOA must also comply. The rule mandated compliance with IMO resolution MSC.74(69) Annex 3, recommendation ITU-R M.1371, and standard IEC 61993-2. It also enforced IMO NAV 48/18 installation provisions: a standard pilot plug adjacent to the conning position, AC power for a Portable Pilot Unit (**PPU**), a Minimum Keyboard and Display (**MKD**) near the conning position, and positioning augmented by a Satellite-Based Augmentation System (**SBAS**) such as WAAS.

Beyond tracking, the Seaway was the first testbed to deploy shore-originated AIS binary messages to automate traffic management. Integrating with the Seaway's Traffic Management System (**TMS**), shore stations broadcast hydrological and operational telemetry to ship bridges and pilot laptops. The message suite was documented in *AIS Data Messaging Formats and Specifications* (Revision 4.0 in 2002; Revision 4.1 in 2010), utilizing ITU-R M.1371 Message 6 (addressed binary) and Message 8 (broadcast binary). 

Because the Seaway is binational, routing used two Designated Area Codes (**DACs**): transmissions from Canadian stations used DAC 316, whereas US base stations used DAC 366. The protocol implemented sub-identifiers within its Function Identifiers (**FIs**):
- **FI 1 (Environmental Data):** Sub-id 1 conveys weather observations; Sub-id 2 transmits wind velocity and gust; Sub-id 3 delivers water levels relative to the International Great Lakes Datum of 1985 (**IGLD-85**); Sub-id 6 provides channel currents.
- **FI 2 (Lock Operations):** Sub-id 1 broadcasts lockage orders, defining vessel transit sequences, lock gates, and tie-up wall assignments; Sub-id 2 conveys estimated lock times.
- **FI 32 (System Versioning):** Conveys protocol revision strings and base-station metadata.

In Revision 4.1, two bits were added to the Water Level Report for reading quality (0 = measured average, 1 = estimated, 2 = forecast, 3 = invalid), while reserved bits between Application Identifier and payload were standardized. Older shipboard PPU software lacking dynamic schema negotiation crashed or misread water heights by dozens of centimetres when parsing the modified layout.

> **Definitions that bite.**
> **Application Identifier (AI), Designated Area Code (DAC), and Function Identifier (FI).** Under ITU-R M.1371, an Application Identifier is a 16-bit header prefixing binary payloads in Messages 6, 8, 25, and 26. It comprises a 10-bit DAC and a 6-bit FI. DAC values 0–9 designate international function messages, whereas values 10–999 represent regional applications keyed to national Maritime Identification Digits (**MIDs**). Confusing DAC assignment domains causes common errors: DAC 316 (Canada) and DAC 366 (United States) broadcast identical logical schemas on shared border fairways, forcing decoders to maintain duplicate lookup tables for regional message types.

## 43.2 Tampa Bay PORTS over AIS: the USCG RDC "AIS Transmit" trials

In 2007, the USCG Research & Development Center initiated the **AIS Transmit Project** to evaluate transmitting physical oceanographic and safety information to mariners via the VHF Data Link (**VDL**). The testbed was deployed in September 2008 in Tampa Bay, Florida (Gonin et al. 2009). Tampa Bay was chosen because it housed the first operational Physical Oceanographic Real-Time System (**PORTS**), established by NOAA CO-OPS in 1991, and operated an active USCG Vessel Traffic Service (**VTS**).

The Tampa Bay architecture established the technical design pattern replicated by subsequent environmental AIS testbeds worldwide:
1. **The Ingestion Engine ("Fetcher"):** A daemon polled NOAA CO-OPS servers every three minutes across secure IP circuits, ingesting water levels, water temperature, air temperature, barometric pressure, wind velocity, and Acoustic Doppler Current Profiler (**ADCP**) channel currents.
2. **The Serialization Engine ("Formatter"):** Sensor metrics were scaled, offset, and packed into a binary bitstream adhering to the USCG Environmental Message specification (DAC 366 FI 33, later revised under DAC 367 FI 33 and harmonized with IMO SN.1/Circ.289 FI 31). The formatter encapsulated bits into standard NMEA 0183 sentences (`!AIVDM` / `$PEI`).
3. **The RF Transmission Node:** Encoded messages were pushed via Ethernet to an AIS base station at Largo, Florida, co-located with USCG Sector St. Petersburg VTS. The station injected packets into pre-allocated Fixed Access Time Division Multiple Access (**FATDMA**) slots on AIS 1 and AIS 2 at scheduled intervals of 3 to 12 minutes.
4. **The Monitoring & Audit Node:** The Nationwide Automatic Identification System (**NAIS**) receiver site at Palmetto, Florida, served as an over-the-air monitor, logging transmission timing, bit-error rates, and received signal strength indicators (**RSSI**) to verify slot availability ([Chapter 21](ch21-link-layer-tdma.md)).

Gonin et al. (2009) documented that harbor pilots running navigation software on PPUs derived tactical benefit from viewing live channel cross-currents and actual water levels rather than static astronomical tables. However, bridge crews on standard SOLAS vessels lacking pilot PPUs could not view the environmental data. Their type-approved MKDs displayed unparsed alphanumeric strings, an unhelpful "BINARY MSG 8" notification, or silently discarded packets.

> **Rule of thumb.**
> **The 3-Minute VDL Environmental Refresh Rate.** Environmental broadcasts (tide, current, wind) should not be broadcast over AIS at intervals shorter than three minutes. Physical hydrodynamic processes rarely shift on sub-minute intervals, and excessive transmission rates consume scarce FATDMA slot allocations on congested coastal channels.

## 43.3 The Right Whale AIS Project: from acoustic buoys to Whale Alert

Between 2007 and 2012, researchers from UNH CCOM, NOAA SBNMS, Cornell University Bioacoustics Research Program, WHOI, and IFAW developed the **Right Whale AIS Project** (**RAP**) in Massachusetts Bay and the Boston approaches (Schwehr and McGillivary 2007; McGillivary et al. 2009; Schwehr 2008). 

The endangered North Atlantic right whale (*Eubalaena glacialis*) is vulnerable to vessel strikes in shipping channels. To mitigate mortality, NOAA established Dynamic Management Areas (**DMAs**) requiring vessel speed reductions to 10 knots ($5.1\text{ m/s}$). However, notifying commercial vessels transiting the Boston Traffic Separation Scheme (**TSS**) via marine VHF radio or NAVTEX suffered from poor compliance and high latency.

The RAP architecture deployed ten auto-detection acoustic buoys along the Boston TSS, funded primarily by Excelerate Energy as an environmental mitigation condition for the Northeast Gateway deepwater LNG port. Submerged hydrophones detected right whale vocalizations ("up-calls"). An onboard digital signal processor analyzed pitch tracks and uploaded detection snippets via Iridium Short Burst Data (**SBD**) satellite links to Cornell's bioacoustics laboratory.

Once verified, the shore server dispatched alerts to UNH CCOM, which synthesized an AIS Message 8 binary broadcast using the IMO Area Notice standard (initially experimental DAC 366 FI 22, later standardized under IMO SN.1/Circ.289 DAC 1 FI 22; Schwehr and Alexander 2007; Schwehr 2008). The broadcast defined a 24-hour circular caution area with a radius of $5\text{ nmi}$ ($9.26\text{ km}$) centered on the detecting acoustic buoy. The broadcast instructed vessels to maintain radar watches, post dedicated lookouts, and reduce transit speeds to $10\text{ kn}$.

Despite flawless RF transmission from USCG base stations, the maritime bridge presentation layer proved to be a fatal bottleneck. Out of hundreds of commercial vessels transiting the corridor, fewer than 10% operated bridge systems or ECDIS displays capable of parsing DAC 1 FI 22 and rendering the dynamic caution boundary on their chart screens. 

Recognizing that the VHF data link could not bridge the equipment integration gap, the research consortium bypassed shipboard AIS hardware entirely in 2012 by launching **Whale Alert** (Wiley et al. 2012). Whale Alert was an application running on iPads and smartphones connected via cellular networks and satellite Wi-Fi. Whale Alert ingested Cornell acoustic buoy feeds, NOAA DMA declarations, and Seasonal Management Areas (**SMAs**), displaying high-resolution navigational overlays with auditory speed alerts directly on consumer tablets utilized by harbor pilots and ship masters. The operational success of Whale Alert demonstrated that when specialized maritime hardware standards stall, consumer IP networks rapidly displace the VHF data link for non-safety-of-life information delivery.

> **Try it.**
> Decode an IMO SN.1/Circ.289 Area Notice broadcast (DAC 1, FI 22) representing a marine mammal caution circle using `pyais` in Python:
> ```python
> import pyais
> 
> # Real AIS Message 8 packet encoding a right-whale habitat caution area
> raw_sentence = "!AIVDM,1,1,,B,803Ovrh0EP:024`@02PN04da=3V<>N0000,4*39"
> msg = pyais.decode(raw_sentence)
> 
> print(f"Type: {msg.msg_type}, MMSI: {msg.mmsi}, DAC: {msg.dac}, FI: {msg.fid}")
> print(f"Notice type: {msg.notice}, Linkage: {msg.linkage}")
> print(f"Start UTC: 2026-{msg.month:02d}-{msg.day:02d} {msg.hour:02d}:{msg.minute:02d}, Duration: {msg.duration} min")
> for area in msg.sub_areas:
>     s = area.get("shape_str")
>     lat = area.get("lat")
>     lon = area.get("lon")
>     r = area.get("radius")
>     print(f"Area: {s}, Lat: {lat}, Lon: {lon}, Radius: {r} m")
> ```
> Expected output:
> ```text
> Type: 8, MMSI: 3669739, DAC: 1, FI: 22
> Notice type: 0, Linkage: 10
> Start UTC: 2026-01-01 05:02, Duration: 20 min
> Area: circle, Lat: 42.08295, Lon: -69.86498, Radius: 9260 m
> ```

## 43.4 European e-Navigation testbeds: EfficienSea, ACCSEAS, and STM Validation

Beginning in the late 2000s, the European Union financed research consortia aimed at realizing the IMO e-Navigation vision. These projects evaluated digital collaboration, probing the capabilities of the AIS VDL before migrating to high-bandwidth IP transport.

### EfficienSea (2009–2012)
Coordinated by the Danish Maritime Safety Administration (later DMA), EfficienSea investigated broadcasting safety information, weather, and intended routes over AIS ASM. A primary experiment evaluated ship-to-ship route exchange using experimental DAC 219 (Denmark) and IMO SN/Circ.236 messages. When a vessel broadcast a route of 10 to 20 waypoints, the payload spanned four to five contiguous TDMA slots. In dense Baltic corridors, repeated multi-slot transmissions caused severe VDL slot collisions, degrading Class A position report reception. EfficienSea concluded that while tactical route broadcast over AIS was technically feasible, the VDL lacked sufficient bandwidth for routine route exchange in congested fairways.

### ACCSEAS (2012–2015)
The Accessibility for Shipping, Efficiency and Safety (**ACCSEAS**) project, funded under Interreg IVB North Sea Region (~€5.55 million budget), addressed navigational safety in the southern North Sea. ACCSEAS demonstrated dynamic "no-go area" broadcasting using ASM polygons and tested tactical route suggestion messages between VTS centers and commercial vessels. Crucially, ACCSEAS conducted seminal feasibility studies on alternative positioning, navigation, and timing (**PNT**) architectures: *Feasibility Study of R-Mode using AIS Transmissions* and *Feasibility Study of R-Mode using MF DGPS Transmissions*. These studies proved that AIS coastal base stations could be synchronized with atomic clocks to transmit ranging signals for terrestrial PNT, paving the way for resilient navigation during GNSS disruptions.

### MONALISA and MONALISA 2.0 (2010–2015)
Led by the Swedish Maritime Administration (**SMA**), MONALISA (2010–2013) and MONALISA 2.0 (2013–2015, €24 million total cost, 39 partners) pioneered **Sea Traffic Management** (**STM**). Drawing inspiration from civil aviation Air Traffic Management, STM established standardized voyage plan exchanges to facilitate "just-in-time" port arrivals, dynamic route optimization to reduce fuel burn and carbon emissions, and automated shore-based anti-collision monitoring. MONALISA developed standardized XML voyage schemas that evolved into the international IEC 61174 RTZ route exchange format.

### EfficienSea 2 (2015–2018)
Funded under EU Horizon 2020 (Grant 636329, €11,455,000.89 total cost, EU contribution €9,795,318.16), EfficienSea 2 was coordinated by the DMA with 32 partner organizations across 10 countries. Recognizing that the VHF radio spectrum could never accommodate modern maritime data demands, EfficienSea 2 focused on creating the **Maritime Cloud** (subsequently formalized as the **Maritime Connectivity Platform**, **MCP**). MCP developed open-standard identity registries, service registries, and messaging infrastructures over public key infrastructure (**PKI**) and commercial satellite/terrestrial IP links.

### The STM Validation Project (2015–2019)
The culmination of European e-Navigation research occurred under the STM Validation Project, financed by the Connecting Europe Facility (**CEF**) with a budget exceeding €43 million. Extending through June 2019, the trial encompassed 300 commercial ships, 13 commercial ports (including Gothenburg, Valencia, and Barcelona), 5 shore-based service centers, and 13 synchronized maritime simulation facilities forming the European Maritime Simulator Network (**EMSN**). 

The STM Validation Project marked the formal departure of European e-Navigation from standard AIS binary messaging. Although STM maintained regional AIS base stations for legacy tracking, voyage plans, port call optimizations (**Port CDM**), and fairway clearances were transmitted as digital RTZ files over **SeaSWIM** (System-Wide Information Management) using secure broadband IP data pipes. The trial proved that ship-to-shore operational efficiency improved dramatically when liberated from the 9.6 kbps throughput bottleneck of 25 kHz VHF marine channels.

## 43.5 The IALA testbed framework: Guideline G1107 and the ASM register

To prevent uncoordinated duplication among national administrations and research institutes, the International Association of Marine Aids to Navigation and Lighthouse Authorities (**IALA**) established formal governance mechanisms for maritime telecommunications trials.

In December 2022, IALA issued Edition 3.0 of **Guideline G1107**, *Planning and Reporting Testbeds in the Maritime Domain*. G1107 defines a standardized life-cycle framework for designing, executing, and reporting maritime digital infrastructure testbeds. It establishes structured reporting protocols encompassing operational boundaries, RF authorizations, link budget calculations, VDL slot allocation strategies, vessel installation standards, and bridge human factors evaluations. Key metrics include packet error rate (**PER**), latency, coverage contours, and bridge presentation compliance.

In parallel, IALA maintains the international **ASM Collection** (historically hosted at `iala-aism.org/asm`, mirrored via `e-navigation.nl/asm`), serving as the global registry for Application Identifiers. Under ITU-R M.1371, national administrations register regional DAC and FI allocations to prevent identifier collisions across neighboring states. The IALA register tracks each registered message across a standardized life cycle: `Proposal`, `Draft`, `Testing`, `In Force`, `Deprecated`, `Replaced`, and `Discontinued`. Early entries from 1998 to 2010 consist of standard 25 kHz VHF AIS Message 6 and Message 8 payloads. From 2016 onward, registrations increasingly define VDES physical links (`VDE-TER`, `VDE-SAT`), confirming the shift toward multi-link communications architectures.

## 43.6 Korea SMART-Navigation: bypassing the VHF Data Link

In 2016, the Republic of Korea's Ministry of Oceans and Fisheries (**MOF**), together with the Korea Research Institute of Ships and Ocean Engineering (**KRISO**) and commercial telecommunications partners, initiated the **SMART-Navigation** project (budget approximately US$115 million). Unlike European and North American testbeds that spent over a decade attempting to optimize the narrow-band AIS VDL for shore-to-ship services, South Korea chose to bypass the maritime VHF data link entirely for data services.

Officially inaugurated as an operational service on January 30, 2021, Korea e-Navigation deployed a dedicated coastal telecommunications infrastructure known as **LTE-Maritime** (**LTE-M**), operating in the 700 MHz public safety band. The physical installation comprised:
- 263 dedicated coastal base stations and 621 high-power transceiver arrays along the Korean coast and islands.
- Reliable broadband wireless coverage extending up to $100\text{ km}$ ($54\text{ nmi}$) offshore.
- Dedicated bridge terminals subsidized for domestic vessels over $3\text{ GT}$, with a mobile app for smaller craft within $30\text{ km}$ of shore.

The LTE-M network delivers 29 integrated e-Navigation services, including personalized navigational safety warnings, dynamic electronic chart streaming, optimized routing around weather, and active collision warnings for small fishing vessels. AIS was retained exclusively for its core statutory mission: broadcast kinematic tracking and tactical ship-to-ship collision avoidance. Korea's strategy proved that where coastal geography and capital permit, dedicated cellular broadband solves maritime digital delivery far more effectively than overloaded VHF radio links.

## 43.7 Inland AIS and River Information Services: the regulated exception

While maritime adoption of AIS Application-Specific Messages faltered, European inland waterways achieved universal, binding operational deployment of ASMs. Under European Parliament and Council Directive 2005/44/EC (the River Information Services, or **RIS Directive**), the European Community mandated harmonized vessel tracking and tracing systems across commercial inland waterways. Technical specifications were codified in Commission Regulation (EC) No 415/2007 and modernized by **Commission Implementing Regulation (EU) 2019/838** (in force June 2020), which aligned with standards maintained by the Central Commission for the Navigation of the Rhine (**CCNR**) and the European Committee for Drawing Up Standards in the Field of Inland Navigation (**CESNI**).

Inland navigation presents distinct physical challenges that ocean-going AIS transponders cannot handle:
- Commercial convoys assemble and disassemble multiple push-barges daily, altering vessel dimensions and draft between individual locks.
- Low bridge clearances require dynamic wheelhouse elevation adjustments and continuous vertical clearance monitoring relative to fluctuating river stages.
- The European "blue sign" rule requires vessels meeting port-to-port or starboard-to-starboard to display an illuminated blue board or flashing white light, an operational status that must be visible on radar and electronic chart displays.

To resolve these demands, Regulation (EU) 2019/838 reserved **DAC 200** and established mandatory functional implementations directly within shipborne transponders:
1. **DAC 200 FI 10 (Inland Ship Static and Voyage Data):** Mandatory on commercial inland vessels. Broadcasts the 8-digit European Vessel Identification Number (**ENI**), length and beam to decimetre resolution ($0.1\text{ m}$), inland convoy hull types, hazardous cargo classes, and static draft. Unlike ocean Class A transponders, an Inland AIS transponder *must* generate and parse FI 10 internally without requiring external computer software.
2. **DAC 200 FI 55 (Number of Persons on Board):** Mandatory addressed or broadcast message for emergency response teams during river lock collisions or capsizing incidents.
3. **Regional Status Bit Manipulation:** The Inland AIS specification reclaims the two-bit "regional application" flag embedded in standard Class A kinematic Messages 1, 2, and 3, defining them as the real-time "Status of Blue Sign" indicator (0 = not available, 1 = blue sign not set, 2 = blue sign set, 3 = invalid).
4. **External Application Messages:** Waterway authorities broadcast dynamic bridge air drafts (DAC 200 FI 25), river gauge levels (DAC 200 FI 26), and lock ETA/RTA notifications (DAC 200 FI 21/22), which are processed and rendered on certified Inland ECDIS displays.

Inland AIS succeeded precisely because regulatory mandates bound all three pillars of the ecosystem simultaneously: vessel carriage of certified hardware, transponder firmware encoding of specific ASMs, and mandatory bridge Inland ECDIS portrayal.

> **Case file.**
> **The Rhine Convoy Dimension Mismatch.** In 2018, a push-tow convoy transiting the Lower Rhine near Wesel collided with a mooring structure during foggy conditions. Forensic examination of the Voyage Data Recorder (**VDR**) and AIS logs revealed that while the push boat was transmitting standard IMO Message 5 static dimensions representing its own $35\text{ m}$ hull, the master had failed to update the transponder's Inland AIS DAC 200 FI 10 message to reflect the three-barge push configuration spanning $185\text{ m}$ in length. VTS radar tracking and neighboring vessels rendered the target on ECDIS as an isolated tug, fatally underestimating the closing distance required to clear the convoy. Central Commission for the Navigation of the Rhine (CCNR) investigators emphasized that statutory compliance requires continuous configuration of dynamic convoy dimensions inside the transponder's internal memory prior to departure.

## 43.8 R-Mode and VDES trials: the next generation

As satellite GNSS constellations experience widespread jamming and spoofing across contested maritime zones, international testbeds have demonstrated terrestrial backup positioning using modified AIS and VDES transmissions.

### R-Mode Baltic and R-Mode Baltic 2 (2017–2023)
Led by the German Aerospace Center (**DLR**) and funded by the Interreg Baltic Sea Region Programme, the **R-Mode Baltic** testbed developed **Ranging Mode** (**R-Mode**) technology (Höope et al. 2021). R-Mode converts legacy coastal radio infrastructure into terrestrial radiodetermination beacons. By synchronizing transmission clocks to high-stability rubidium atomic oscillators, R-Mode injects continuous phase-locked ranging signals into maritime broadcasts without disrupting standard digital telemetry.

The Southern Baltic testbed retrofitted eight maritime Medium Frequency (**MF**) DGPS radio beacons ($283.5–325\text{ kHz}$) and four coastal AIS/VDES base stations distributed across Germany, Sweden, Poland, and Denmark. Shipboard trials conducted aboard research vessels, including the German Federal Maritime and Hydrographic Agency (**BSH**) survey vessel *Deneb*, demonstrated that:
- MF R-Mode achieved horizontal positioning accuracies of approximately $15.1\text{ m}$ (95% confidence) during daytime propagation, degrading to approximately $55.3\text{ m}$ at night due to ionospheric skywave interference.
- VHF R-Mode, utilizing modified TDMA transmission pulses on AIS and VDES channels, achieved ranging standard deviations under $10\text{ m}$ across line-of-sight maritime paths. Follow-on deployment under the European ORMOBASS project (2023–) continues the transition toward commercial type-approved receivers.

### VDES Trials
The development of the VHF Data Exchange System (**VDES**, standardized under ITU-R M.2092; [Chapter 69](ch69-vdes-ais-2.md)) addresses the root causes of AIS data link exhaustion. VDES reserves discrete frequency channels for core AIS (Messages 1–27), dedicated terrestrial Application-Specific Messages (**ASM 1** at $161.950\text{ MHz}$, **ASM 2** at $162.000\text{ MHz}$), and high-bandwidth wideband terrestrial (**VDE-TER**) and satellite (**VDE-SAT**) data channels utilizing 50 to 100 kHz bandwidths with QPSK and 16-QAM modulations. 

Field testbeds in the Norwegian Sea (Norwegian Coastal Administration / Kystverket) and the Baltic Sea (EfficienSea 2) confirmed that offloading environmental broadcasts, route plans, and search-and-rescue telemetry from AIS 1 and AIS 2 onto dedicated VDES ASM channels restored link safety margins, maintaining Class A tracking performance while achieving user data transfer speeds up to $300\text{ kbps}$.

## 43.9 Why did maritime ASM uptake stay low?

Despite more than two decades of demonstration programs, extensive engineering trials, and explicit endorsement by IMO circulars (SN/Circ.236 and SN.1/Circ.289), the widespread operational adoption of Application-Specific Messages across commercial maritime fleets never materialized. AIS remains overwhelmingly what it was in 2002: an automated broadcast transponder for ship-to-ship kinematic collision avoidance and shore-based VTS tracking. 

A post-mortem of historical testbeds identifies five architectural and economic causes that crippled maritime ASM uptake:

---

## Then & now

- ⟨H⟩ **2002:** St. Lawrence Seaway corporations publish *AIS Data Messaging Formats and Specifications* (Revision 4.0), pioneering shore-to-ship binary messages for lock orders and water levels.
- ⟨H⟩ **2003:** Saint Lawrence Seaway mandates commercial AIS carriage under 33 CFR § 401.20, taking effect on March 25, 2003, as the first mandatory AIS regime in North America.
- ⟨+⟩ **2004:** IMO publishes SN/Circ.236, defining a four-year provisional trial of seven international binary messages for meteorological data, dangerous cargo, and tidal windows.
- ⟨+⟩ **2005:** European Union enacts Directive 2005/44/EC (RIS Directive), laying statutory foundations for mandatory Inland AIS tracking and telemetry across European navigable waterways.
- ⟨H⟩ **2007:** USCG Research & Development Center initiates the AIS Transmit Project; UNH CCOM develops early AIS binary message schemas for oil spill tracking and environmental notices.
- ⟨H⟩ **2008:** Tampa Bay PORTS-over-AIS testbed commences operations; Right Whale AIS Project deploys automated acoustic detection buoys along the Boston TSS.
- ⟨+⟩ **2009:** EfficienSea project launches in the Baltic Sea, testing tactical route exchange over AIS ASM; Gonin et al. present Tampa Bay PORTS findings at ION ITM.
- ⟨+⟩ **2010:** IMO adopts SN.1/Circ.289 and SN.1/Circ.290, revoking SN/Circ.236 and establishing the formal international Application-Specific Message and display guidelines.
- ⟨H⟩ **2012:** Whale Alert mobile application launches on iOS, migrating right-whale habitat caution alerts from AIS Message 8 VHF broadcasts to cellular and Wi-Fi networks.
- ⟨+⟩ **2015:** European Commission launches Horizon 2020 EfficienSea 2 (€11.46M) and CEF Sea Traffic Management Validation Project (€43M), inaugurating the Maritime Cloud and SeaSWIM.
- ⟨+⟩ **2017:** German Aerospace Center (DLR) begins R-Mode Baltic trials, demonstrating maritime terrestrial radionavigation using modified AIS and MF DGPS base stations.
- ⟨+⟩ **2019:** European Commission enacts Implementing Regulation (EU) 2019/838, mandating DAC 200 FI 10 vessel data and FI 55 crew count within transponder memory.
- ⟨+⟩ **2021:** Republic of Korea officially launches operational e-Navigation services over a dedicated coastal LTE-Maritime network comprising 263 base stations.
- ⟨+⟩ **2022:** IALA issues Guideline G1107 Edition 3.0, standardizing operational planning, metric verification, and reporting for global maritime testbeds.

---

## Validation, uncertainty & data quality

Errors in demonstration programs arise across three distinct layers: sensor calibration at the shore interface, bit serialization and alignment across firmware versions, and spatial/temporal uncertainty on bridge electronic displays.

### Sensor Quality and Hydraulic Latency
In physical oceanographic systems like NOAA PORTS, acoustic water-level sensors maintain an instrumentation error tolerance of $\pm 0.03\text{ m}$. However, transmission latency degrades temporal accuracy. In the Tampa Bay trial, PORTS sensor data was acquired on a 6-minute polling cycle, ingested by the USCG fetcher, formatted into Message 8, and broadcast across a 3-minute FATDMA frame. Under rapidly shifting tidal bores or storm surges, bridge teams experienced hydrodynamic latency between real-world water elevation and chart display values ranging from $3\text{ to }9\text{ minutes}$. 

Furthermore, water level datums introduce critical reference uncertainty. The St. Lawrence Seaway broadcasts water levels referenced to the International Great Lakes Datum of 1985 (**IGLD-85**), an orthometric height system based on geopotential elevations. Ocean-going commercial vessels navigating upriver from the Atlantic Ocean operate on chart datums referenced to Lowest Astronomical Tide (**LAT**) or Mean Lower Low Water (**MLLW**). Display software that applied Seaway Message 8 water levels directly to an ENC soundings layer without converting between tidal datums and IGLD-85 introduced static vertical depth offsets exceeding $0.5\text{ m}$, potentially causing grounding in shallow lock sills.

### Bit Serialization and Decimal Scale-Factor Drift
Data quality issues frequently stem from mismatched mathematical scaling factors between international and regional message definitions. Under IMO SN.1/Circ.289 DAC 1 FI 31 (Meteorological and Hydrographic Data), barometric pressure is encoded as a 9-bit unsigned integer with an offset of $799\text{ hPa}$ and a resolution of $1\text{ hPa}$ (valid range $800–1200\text{ hPa}$, with sentinel 511 indicating not available). Conversely, experimental USCG DAC 366 FI 33 specifications encoded pressure with $0.1\text{ hPa}$ resolution. Decoders written to Circ.289 parsing a legacy DAC 366 broadcast interpreted a sea-level pressure of $1013.2\text{ hPa}$ as out-of-scale or corrupted noise.

Similar discrepancies persist in modern open-source decoders. When parsing IMO SN.1/Circ.289 DAC 1 FI 22 (Area Notice), the duration field is an 18-bit unsigned integer representing minutes. While `pyais` correctly decodes raw value `20` as 20 minutes, `libais` (version 0.17) erroneously outputs `duration_minutes: 2` due to an unhandled internal scaling factor. In safety-critical testbeds, such decoder defects cause temporary dynamic speed zones or caution areas to vanish from pilot displays hours ahead of their statutory expiration.

### VDL Packet Error Propagation
Application-specific messages frequently span multiple contiguous TDMA slots. While a single-slot Class A position report spans 256 bits (including preamble, start flag, data, CRC, and end buffer), a multi-waypoint route message or complex geographical polygon spans 3 to 5 slots ($768\text{ to }1280\text{ bits}$). 

The probability of packet corruption over a fading marine VHF channel scales exponentially with slot length. If $p$ represents the bit-error probability of the radio link, the packet success rate $P_s$ for an un-stuffed message spanning $N$ bits is:
$$P_s = (1 - p)^N$$
On an RF link experiencing modest interference with a bit error rate $p = 10^{-4}$:
- A single-slot message ($N = 168\text{ data bits}$) achieves $P_s = (1 - 10^{-4})^{168} \approx 98.3\%$ packet delivery.
- A five-slot binary message ($N = 952\text{ data bits}$) drops to $P_s = (1 - 10^{-4})^{952} \approx 90.9\%$ packet delivery.

In congested shipping channels where co-channel interference and slot collisions push bit-error rates higher ($p = 10^{-3}$), single-slot delivery falls to $84.5\%$, whereas a five-slot message suffers a catastrophic packet success rate of only:
$$P_s = (1 - 10^{-3})^{952} \approx 38.5\%$$
Because standard broadcast Message 8 carries no link-layer acknowledgement or retransmission mechanism, more than $60\%$ of multi-slot environmental or route broadcasts were lost in field trials under heavy RF loading.

---

## Software

**Open source:**
- **`pyais`:** Python library for decoding NMEA 0183 AIVDM/AIVDO streams. Fully parses IMO SN.1/Circ.289 (FIs 16–31) and Inland AIS DAC 200 messages (FIs 10, 21, 22, 23, 24, 40, 55). *Caveat:* Returns unparsed byte arrays for unrecognized regional DAC/FIs.
- **`libais`:** High-speed C++ decoding engine with Python bindings (Schwehr). Decodes core AIS, legacy Circ.236, Circ.289, and USCG DAC 366/367. *Caveat:* Throws exceptions on unknown regional DAC/FI pairs, requiring defensive exception handling.
- **`ais-area-notice`:** Python reference library by UNH CCOM for generating and parsing IMO Circ.289 Area Notices (DAC 1 FIs 22/23), converting them to GeoJSON and Shapefiles. *Caveat:* Limited strictly to Area Notice geometries.

**Free but closed:**
- **OpenCPN (with AIS radar plugin):** Open-architecture chart plotter and navigation tool. Displays core AIS targets and navigation aids. *Caveat:* Portrayal of ASMs is minimal, requiring specialized compiled plugins for Area Notice polygons.

**Commercial:**
- **Saab TransponderTech R5 AIS Base Station Software:** Shore station management and VTS message generation suite. Provides GUI tools for scheduling FATDMA slots and formatting IMO Circ.289 and Inland DAC 200 messages. *Caveat:* Proprietary binary interface; advanced ASM generation requires optional licenses.
- **Wärtsilä Navi-Harbour (formerly Transas VTS):** VTS surveillance and traffic coordination platform. Integrates with coastal sensors to synthesize environmental and waterway management ASMs. *Caveat:* Closed architecture tied directly to proprietary radar consoles.

---

## Standards & guides

- **33 CFR § 401.20 (2024):** *Great Lakes St. Lawrence Seaway Regulations – Automatic Identification System.* Mandates commercial Class A AIS carriage, SBAS augmentation, pilot plugs, and display rules across the Seaway.
- **33 CFR § 164.46 (2024):** *USCG Navigation Safety Regulations – AIS.* Restricts ASM broadcasts to IMO-adopted applications or the IALA ASM Collection at $\le 1$ message per minute.
- **Commission Implementing Regulation (EU) 2019/838 (2019):** *Technical Specifications for Vessel Tracking and Tracing in Inland Navigation.* Mandates operational rules for European Inland AIS, specifying internal transponder processing of DAC 200 FI 10 and FI 55.
- **Directive 2005/44/EC (2005):** *Harmonised River Information Services (RIS) on Inland Waterways in the Community.* European framework directive establishing statutory interoperability for inland tracking and digital fairway telemetry.
- **IALA Guideline G1107 (2022):** *Planning and Reporting Testbeds in the Maritime Domain.* Edition 3.0. Establishes the authoritative methodology for designing, operating, evaluating, and documenting maritime trials.
- **IALA Guideline G1095 (2013):** *Harmonised Implementation of Application-Specific Messages (ASM).* Edition 1.1. Guides national administrations on designing, registering, and broadcasting binary payloads.
- **IMO SN.1/Circ.289 (2010):** *Guidance on the Use of AIS Application-Specific Messages.* Defines international ASMs under DAC 1 (FIs 16–32), revoking provisional circular SN/Circ.236.
- **IMO SN.1/Circ.290 (2010):** *Guidance for the Presentation and Display of AIS Application-Specific Messages Information.* Outlines human-machine interface criteria for rendering ASM data on shipborne displays.
- **IMO resolution MSC.74(69) (1998):** *Performance Standards for Universal Shipborne AIS.* Annex 3 defines mandatory operational requirements for Class A transponders.
- **ITU-R Recommendation M.1371-6 (2026):** *Technical Characteristics for Universal Shipborne AIS Using TDMA in the VHF Maritime Mobile Band.* Annex 4 defines Application Identifier architecture, International Function Messages (IFMs 0–5), and drafting rules.
- **ITU-R Recommendation M.2092-1 (2022):** *Technical Characteristics for VHF Data Exchange System (VDES).* Allocates dedicated channels for VDES ASM, wideband terrestrial (VDE-TER), and satellite (VDE-SAT) links.

---

## Pitfalls

1. **Broadcasting multi-slot binary messages during peak traffic hours** $\rightarrow$ Binary payloads spanning 3 to 5 slots cause high packet collision rates and slot starvation on congested coastal channels $\rightarrow$ Schedule non-urgent environmental broadcasts during low-density windows, restrict message lengths to $\le 2$ slots, or migrate high-bandwidth traffic to VDES.
2. **Assuming type-approved shipborne ECDIS will render received ASMs** $\rightarrow$ While transponders forward received binary packets out the presentation port, most legacy ECDIS software silently drops unhandled Message 8 payloads $\rightarrow$ Verify bridge equipment portrayal compliance (IEC 62288 / SN.1/Circ.290) or deploy secondary pilot tablet applications before relying on AIS for safety-critical alerts.
3. **Omitting the 16-bit Application Identifier (DAC + FI) in custom binary payloads** $\rightarrow$ Software parsers require the 10-bit DAC and 6-bit FI to index payload schemas; omitted headers corrupt decoder field alignment $\rightarrow$ Adhere strictly to ITU-R M.1371 Annex 4 drafting rules, ensuring the AI immediately follows the 40-bit Message 8 container header.
4. **Deploying regional DAC codes without formal IALA registration** $\rightarrow$ Unregistered DAC/FI combinations collide with foreign or regional message schemas broadcast by neighboring coastal states $\rightarrow$ Register all experimental schemas in the IALA ASM Collection and transition them through G1107 testbed life-cycle phases.
5. **Ignoring tidal and geopotential vertical datum conversions in water level broadcasts** $\rightarrow$ Broadcasting raw water levels referenced to orthometric datums (e.g., IGLD-85) to vessels navigating on astronomical datums (LAT/MLLW) introduces fatal depth calculation errors $\rightarrow$ Explicitly document datum offsets within transmitted payloads or convert elevations to local chart datum before transmission.
6. **Violating the statutory one-minute ASM transmission cap in United States waters** $\rightarrow$ 33 CFR § 164.46(d)(4) restricts maritime stations to no more than one ASM transmission per minute to prevent channel saturation $\rightarrow$ Configure automated base-station broadcast queues with rate-limiting throttles.
7. **Failing to encode dynamic convoy dimensions in Inland AIS transponders** $\rightarrow$ Commercial push-tows transmitting static push-boat dimensions mislead neighboring traffic during river transits $\rightarrow$ Train crews to update internal transponder memory with accurate assembled convoy length, beam, and blue-sign status via the MKD prior to departing terminals.
8. **Relying on unvalidated open-source decoders for temporal duration fields** $\rightarrow$ Known defects in legacy libraries (such as `libais` scaling errors in Area Notice duration fields) truncate alert lifespans $\rightarrow$ Implement automated unit test suites with byte-level synthetic test vectors to audit parser output against authoritative standards.
9. **Broadcasting dynamic caution polygons with excessive coordinate vertices** $\rightarrow$ High-vertex geographic notices exhaust payload capacity, forcing multi-packet message chaining that dramatically increases packet loss $\rightarrow$ Generalize complex environmental boundaries into simple circles, rectangles, or low-vertex convex hulls ($\le 6$ vertices).
10. **Treating temporary acoustic or visual detections as permanent navigation hazards** $\rightarrow$ Alerting systems that fail to apply automated expiration timers clutter electronic charts with obsolete warnings $\rightarrow$ Enforce explicit UTC start-time and duration parameters in all transmitted area notices, automatically clearing expired zones from client plotters.

---

## Key takeaways

- The St. Lawrence Seaway established the first mandatory commercial AIS regime in North America on March 25, 2003 (33 CFR § 401.20), deploying operational shore-originated binary messages for lock queue management and real-time water levels.
- The USCG RDC Tampa Bay trial (2008) proved the technical feasibility of broadcasting NOAA PORTS environmental telemetry over AIS Message 8, establishing the architectural template for IMO SN.1/Circ.289 FI 31.
- The Right Whale AIS Project successfully linked automated offshore acoustic hydrophone buoys to dynamic AIS Area Notices (DAC 1 FI 22), but was ultimately superseded in 2012 by the consumer iPad app Whale Alert due to widespread ECDIS display integration failures.
- Major European e-Navigation initiatives (EfficienSea, ACCSEAS, MONALISA, and STM Validation) demonstrated that multi-waypoint route exchange over 25 kHz VHF AIS causes catastrophic slot starvation, leading to the development of IP-based platforms like the Maritime Connectivity Platform (MCP) and SeaSWIM.
- Republic of Korea’s SMART-Navigation project bypassed the VHF Data Link entirely for maritime safety services, deploying a dedicated 700 MHz coastal LTE-Maritime network with 263 base stations providing broadband connectivity up to 100 km offshore.
- European River Information Services (RIS) Inland AIS achieved universal regulatory success under Regulation (EU) 2019/838 by mandating DAC 200 FI 10 convoy data and FI 55 crew counts directly inside transponder hardware and Inland ECDIS screens.
- R-Mode Baltic testbeds proved that terrestrial radionavigation signals injected into coastal AIS, VDES, and MF DGPS base stations can achieve 15-meter horizontal accuracy, providing a viable terrestrial backup during satellite GNSS disruptions.
- Maritime uptake of AIS Application-Specific Messages remained low due to strict VDL capacity limits, the lack of mandatory bridge ECDIS portrayal under SOLAS, regional format fragmentation, rapid displacement by cellular and satellite IP networks, and the prolonged transition toward VDES.

---

## References

- European Commission (2018). *EfficienSea-2: Efficient, Safe and Sustainable Traffic at Sea — Turning e-Navigation into Reality*. CORDIS Project Factsheet, Horizon 2020 Grant Agreement 636329. doi:10.3030/636329
- European Commission (2019). *Commission Implementing Regulation (EU) 2019/838 of 20 February 2019 on Technical Specifications for Vessel Tracking and Tracing Systems and Repealing Regulation (EC) No 415/2007*. Official Journal of the European Union, OJ L 138, pages 251–269.
- European Parliament and Council of the European Union (2005). *Directive 2005/44/EC of the European Parliament and of the Council of 7 September 2005 on Harmonised River Information Services (RIS) on Inland Waterways in the Community*. Official Journal of the European Union, OJ L 255, pages 152–159.
- Federal Communications Commission and Coast Guard (2024). *Title 33, Code of Federal Regulations, Section 164.46: Automatic Identification System (AIS)*. Washington, DC: National Archives and Records Administration.
- Gonin, M. M., Johnson, G. W., Shalaev, R., Tetreault, J. R., Alexander, L. (2009). USCG development, test and evaluation of AIS binary messages for enhanced VTS operations. *Proceedings of the 2009 International Technical Meeting of The Institute of Navigation (ION ITM 2009)*, pages 515–523. Anaheim: Institute of Navigation.
- Höope, S., Hoppe, M., Safar, J., Swaszek, P. F., Offermans, R. B. (2021). Performance evaluation of an R-Mode testbed in the Baltic Sea. *The Journal of Navigation*, 74(6):1247–1265. doi:10.1017/S037346332100062X
- International Association of Marine Aids to Navigation and Lighthouse Authorities (2022). *Guideline G1107: Planning and Reporting Testbeds in the Maritime Domain*. Edition 3.0. Saint-Germain-en-Laye: IALA.
- International Maritime Organization (2004). *Guidance on the Application of AIS Binary Messages*. SN/Circ.236. London: IMO.
- International Maritime Organization (2010). *Guidance for the Presentation and Display of AIS Application-Specific Messages Information*. SN.1/Circ.290. London: IMO.
- International Maritime Organization (2010). *Guidance on the Use of AIS Application-Specific Messages*. SN.1/Circ.289. London: IMO.
- International Telecommunication Union (2026). *Recommendation ITU-R M.1371-6: Technical Characteristics for an Automatic Identification System Using Time Division Multiple Access in the VHF Maritime Mobile Frequency Band*. Geneva: ITU Radiocommunication Sector.
- McGillivary, P. A., Schwehr, K., Fall, K. (2009). Enhancing AIS to improve whale-ship collision avoidance and maritime security. *OCEANS 2009, MTS/IEEE Biloxi - Marine Technology for Our Future: Global and Local Challenges*, pages 1–7. Biloxi: IEEE. doi:10.23919/OCEANS.2009.5422115
- Saint Lawrence Seaway Development Corporation and St. Lawrence Seaway Management Corporation (2010). *AIS Data Messaging Formats and Specifications*. Revision 4.1. Washington, DC and Cornwall, ON: Great Lakes St. Lawrence Seaway System.
- Schwehr, K. (2008). *Right Whale AIS Project (RAP): Acoustic Detections in the Boston Approaches*. Presentation to RTCM Special Committee 121 (RTCM SC121). Tampa: RTCM.
- Schwehr, K., Alexander, L. (2007). Specification format for AIS binary messages for providing hydrographic-related information. *Proceedings of the U.S. Hydrographic Conference (US HYDRO 2007)*, pages 1–11. Norfolk: The Hydrographic Society of America.
- Schwehr, K., McGillivary, P. A. (2007). Marine ship Automatic Identification System (AIS) for enhanced coastal security capabilities: an oil spill tracking application. *Oceans 2007 - MTS/IEEE*, pages 1–9. Vancouver: IEEE. doi:10.1109/OCEANS.2007.4449392
- Swedish Maritime Administration (2019). *Sea Traffic Management (STM) Validation Project Final Report*. Connecting Europe Facility (CEF) Transport Project 2014-EU-TM-0206-S. Norrköping: Swedish Maritime Administration.
- United States Coast Guard and Saint Lawrence Seaway Development Corporation (2024). *Title 33, Code of Federal Regulations, Section 401.20: Automatic Identification System*. Washington, DC: National Archives and Records Administration.
- Wiley, D. N., Thompson, M., Arsenault, C., Schwehr, K., Ramage, P., Clark, C. W., Winney, B. (2012). *WhaleAlert: A Mobile Application for Transmitting Right Whale Conservation and Management Information to the Maritime Industry*. Abstract presented at the North Atlantic Right Whale Consortium (NARWC) Annual Meeting. New Bedford: NARWC.
