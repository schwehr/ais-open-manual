# Chapter 6 — Fisheries, IUU fishing, and dark fleets

> **Part I — Why AIS? Uses and users.** How satellite and terrestrial AIS data transformed international fisheries management from closed state reporting into planetary monitoring, exposing illegal, unreported, and unregulated fishing, high-seas transshipments, and non-broadcasting dark fleets.

**In this chapter.** You will learn how raw maritime VHF broadcasts and orbital receiver constellations are harnessed to monitor industrial fishing effort, detect illicit operations, and expose vessels that conceal their movements. We examine kinematic signatures across commercial fishing gear types, tracing how one-dimensional convolutional neural networks and sequence models classify trawlers, longliners, and squid jiggers from tracking telemetry. You will analyze algorithmic methodologies for uncovering high-seas transshipments between fishing vessels and refrigerated cargo reefers, and evaluate statistical frameworks for differentiating intentional transponder deactivation from RF packet collisions. We explore how multi-sensor fusion combining Synthetic Aperture Radar, optical imagery, and nighttime radiometry exposes non-broadcasting dark vessels. Finally, you will contrast AIS transparency with proprietary Vessel Monitoring Systems, review international legal mandates including European Union regulations and the Port State Measures Agreement, and execute an AIS gap-triage workflow on sample telemetry.

## 6.1 The fisheries visibility revolution

For most of maritime history, industrial fishing on the high seas remained invisible to the public. Under traditional international law established by the United Nations Convention on the Law of the Sea (**UNCLOS**), high-seas fishing was governed primarily by flag-state authority ([Chapter 16](ch16-laws-and-treaties.md)). Coastal states managed their 200-nautical-mile Exclusive Economic Zones (**EEZs**), but monitoring relied on expensive patrol craft, intermittent aerial surveillance, and mandatory national **Vessel Monitoring Systems** (**VMS**).

VMS networks provided dedicated satellite positioning, but their operational architecture was deliberately fragmented. Transponders transmitted encrypted, tamper-evident position reports over commercial satellite links (such as Inmarsat-C, Argos, or Iridium) directly to a national **Fisheries Monitoring Centre** (**FMC**). Under domestic confidentiality statutes and competitive protections, FMCs rarely shared feeds with neighboring states, regional fisheries management organizations (**RFMOs**), or scientific bodies. A foreign fleet could deplete transboundary stocks or loiter outside an EEZ without the adjacent coastal state receiving actionable telemetry.

The advent of space-based Automatic Identification System (**satellite AIS**) reception in 2008 fundamentally altered this opacity ([Chapter 39](ch39-satellite-ais.md)). Although the International Maritime Organization (**IMO**) originally codified AIS in Chapter V of SOLAS for tactical collision avoidance and coastal Vessel Traffic Services (**VTS**) ([Chapter 1](ch01-what-ais-is.md); [Chapter 4](ch04-vts-and-ports.md); Cutlip 2017), researchers recognized that unencrypted VHF signals broadcast into space could be ingested and analyzed globally.

```
       +-----------------------------------------------------------+
       |                  VMS vs. Broadcast AIS                   |
       +-----------------------------+-----------------------------+
       | Property                    | National VMS  | Open AIS    |
       +-----------------------------+---------------+-------------+
       | Transport                   | Sat-uplink    | Marine VHF  |
       | Encryption                  | Encrypted     | None (open) |
       | Primary Recipient           | National FMC  | Any listener|
       | Public Visibility           | Confidential  | Global      |
       | Reporting Frequency         | 1-4 hours     | 2s - 3 min  |
       | Global Multi-vessel Fusion  | Fragmented    | Planetary   |
       +-----------------------------+---------------+-------------+
```

When computational platforms began aggregating billions of raw AIS messages, they revealed an operational landscape of staggering scale. In their foundational study, Kroodsma et al. (2018) processed more than 22 billion AIS position reports collected between 2012 and 2016. Their analysis demonstrated that industrial fishing vessels operated across more than 55% of the ocean surface—a footprint exceeding four times terrestrial agriculture. More than 70,000 industrial fishing vessels were identified, broadcasting over 37 million hours of fishing effort in 2016 alone.

This transparency arrived amid severe ecological crises. Illegal, Unreported, and Unregulated (**IUU**) fishing accounts for an estimated 11 to 26 million metric tons of catch annually, representing an economic drain of $10 billion to $23.5 billion from coastal economies (Agnew et al. 2009). Catch reconstructions further indicate that global catches have been under-reported by over 50% relative to official Food and Agriculture Organization (**FAO**) statistics since 1950 (Pauly & Zeller 2016). By converting open broadcast telemetry into verifiable spatial metrics, AIS emerged as the primary empirical baseline for combating IUU exploitation, auditing marine protected areas, and illuminating clandestine maritime fleets.

## 6.2 Quantifying fishing effort from AIS telemetry

### 6.2.1 Kinematic signatures across gear types

Estimating fishing effort from raw AIS broadcasts requires converting kinematic streams into behavioral classifications. A vessel does not broadcast an AIS message declaring "I am deploying nets." Instead, dynamic reports (Messages 1, 2, and 3 from Class A transponders; Messages 18 and 19 from Class B units) provide periodic observations of latitude ($\phi$), longitude ($\lambda$), Speed Over Ground (**SOG**, $v$), Course Over Ground (**COG**, $\theta$), and True Heading (**HDG**, $\psi$) ([Chapter 22](ch22-message-catalog.md)).

Commercial fishing gear types display distinct navigational behaviors dictated by the physics of their gear:

- **Trawlers:** Trawlers tow nets through the water column (pelagic) or along the seabed (demersal). Engine drag holds towing speed within a narrow corridor—typically 2.0 to 4.5 kn (3.7 to 8.3 km/h). Turns while towing are wide and sweeping to prevent net collapse. While transiting, trawlers steam at 9 to 13 kn (16.7 to 24.1 km/h) along linear headings.
- **Drifting Longliners:** Longliners deploy mainline cables extending 20 to 100 km (11 to 54 nmi), carrying thousands of baited hooks. Setting occurs at steady speeds of 6 to 9 kn (11.1 to 16.7 km/h) along linear transects. Hauling requires steaming slowly along the gear line at 2 to 4 kn (3.7 to 7.4 km/h), frequently stopping or reversing to land catch, producing a jagged track with high course variance.
- **Purse Seiners:** Purse seiners target schooling pelagic fish (such as tuna) by encircling them with a net wall. After searching at 9 to 14 kn (16.7 to 25.9 km/h), the vessel executes a rapid circular loop ($\sim 500\text{ to }1,000\text{ m}$ diameter) to surround the school, slows to near zero while winching the bottom of the net closed, and remains stationary for several hours during brailing.
- **Squid Jiggers:** Squid jiggers target nocturnal cephalopods using mechanical jigging reels and overhead lamps (100 to 300 kW). During night fishing hours, they drift passively with currents or deploy sea anchors, maintaining speeds between 0.2 and 1.5 kn (0.4 and 2.8 km/h). During daylight, they execute short repositioning transits or lie stationary.

```
       +-----------------------------------------------------------+
       |             Kinematic Profiles by Gear Type               |
       +------------------+-------------------+--------------------+
       | Gear Type        | Fishing SOG (kn)  | Track Geometry     |
       +------------------+-------------------+--------------------+
       | Demersal Trawler | 2.5 - 4.5         | Linear/low turn    |
       | Pelagic Longline | 2.0 - 4.0 (haul)  | Serrated / zigzag  |
       | Purse Seiner     | 0.0 - 2.0 (set)   | Circular loop stop |
       | Squid Jigger     | 0.2 - 1.5 (night) | Passive drift      |
       +------------------+-------------------+--------------------+
```

### 6.2.2 Deep learning and convolutional classifiers

Early efforts to detect fishing behavior relied on static kinematic thresholds, such as classifying any vessel speed between 2 and 4 kn as active trawling (de Souza et al. 2016). However, rigid thresholds produce high false-positive rates when vessels encounter adverse weather, enter congested channels, or drift in offshore currents.

To overcome these limits, Global Fishing Watch developed a deep learning architecture using **one-dimensional Convolutional Neural Networks** (**1D CNNs**) operating directly on trajectory sequences (Kroodsma et al. 2018). The pipeline segments a vessel's telemetry into contiguous temporal windows.

The network architecture operates in two stages:
1. **Vessel Characterization Model:** Evaluates multi-week sequences of kinematic features to predict vessel gear class (trawler, longliner, purse seiner) and dimensions (length, tonnage). The feature matrix includes normalized time deltas ($\Delta t$), geodesic distance steps ($\Delta d$), SOG ($v$), course changes ($\Delta \theta$), and geographic positions.
2. **Fishing Detection Model:** Evaluates a sliding temporal window centered on each AIS fix to assign a continuous score $p_{\text{fishing}} \in [0.0, 1.0]$. The receptive field of the 1D convolutions spans tens of hours, allowing stacked convolutional kernels to extract hierarchical multi-scale motion primitives:
   - Low-level layers capture short-term accelerations, decelerations, and sharp turns.
   - Intermediate layers detect multi-hour operational patterns, such as alternating set-and-haul cycles or encirclement loops.
   - Dense terminal layers combine extracted spatial-temporal features to output a pointwise probability of fishing activity.

Subsequent iterations have integrated transformer models with self-attention mechanisms ([Chapter 49](ch49-analytics-and-ml.md)), capturing long-range dependencies across days of intermittent observations.

> **Try it.** Detect potential fishing activity and AIS telemetry gaps from decoded NMEA records using standard kinematic thresholds:
>
> ```python
> import math
> from pyais.stream import FileReaderStream
> 
> def haversine(lat1, lon1, lat2, lon2):
>     R = 6371.0  # km
>     phi1, phi2 = math.radians(lat1), math.radians(lat2)
>     dphi = math.radians(lat2 - lat1)
>     dlam = math.radians(lon2 - lon1)
>     a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlam/2)**2
>     return 2 * R * math.asin(math.sqrt(a))
> 
> vessels = {}
> for msg in FileReaderStream("data/samples/synthetic_harbor.nmea"):
>     t = None
>     if msg.tag_block is not None:
>         msg.tag_block.init()
>         t = float(msg.tag_block.receiver_timestamp)
>     try:
>         dec = msg.decode()
>         if dec.msg_type in (1, 2, 3, 18, 19):
>             mmsi = dec.mmsi
>             if mmsi not in vessels:
>                 vessels[mmsi] = []
>             vessels[mmsi].append((t, dec.lat, dec.lon, getattr(dec, "speed", 0.0)))
>     except Exception:
>         pass
> 
> for mmsi, pts in sorted(vessels.items()):
>     pts.sort()
>     for i in range(1, len(pts)):
>         t_gap = pts[i][0] - pts[i-1][0]
>         if t_gap > 180:  # Gaps exceeding 3 minutes
>             d_km = haversine(pts[i-1][1], pts[i-1][2], pts[i][1], pts[i][2])
>             speed_kn = (d_km / 1.852) / (t_gap / 3600.0)
>             print(f"MMSI: {mmsi} | Gap: {t_gap:.0f}s | Dist: {d_km:.2f} km ({d_km/1.852:.2f} nmi) | Implied SOG: {speed_kn:.1f} kn")
> ```
>
> Expected output:
> ```text
> MMSI: 244999703 | Gap: 200s | Dist: 1.49 km (0.81 nmi) | Implied SOG: 14.5 kn
> MMSI: 366999701 | Gap: 310s | Dist: 1.91 km (1.03 nmi) | Implied SOG: 12.0 kn
> ```

## 6.3 At-sea transshipment: the maritime laundering chain

### 6.3.1 The mechanics of high-seas rendezvous

Industrial distant-water fishing fleets often remain at sea for months or years without returning to port. This sustained oceanic presence is supported by specialized auxiliary vessels: **refrigerated cargo vessels** (commonly termed **carrier vessels** or **reefers**), bunker tankers, and crew tenders.

At-sea **transshipment** involves transferring marine catch from a catcher vessel to a reefer on the high seas or within an EEZ. The reefer provides frozen storage, provisions, fuel, and bait, allowing catching vessels to maximize fishing time without spending weeks steaming to port.

```
       +-------------------+              +-------------------+
       |  Fishing Catcher  |              | Refrigerated Reefer|
       |  (e.g., Longline) |              | (Carrier Vessel)  |
       +---------+---------+              +---------+---------+
                 \                                  /
                  \   Rendezvous / Cargo Transfer  /
                   \                              /
                    v                            v
               +--------------------------------------+
               | Sustained Close-Proximity Loitering |
               | Distance: < 100 - 500 meters         |
               | Speed:    < 2.0 knots                |
               | Duration: > 2 - 24 hours             |
               +--------------------------------------+
```

While transshipment is lawful when authorized, it represents a primary vulnerability in ocean governance:
1. **Laundering illicit catch:** Catches taken illegally (inside closed marine reserves or exceeding quotas) can be commingled inside the hold of a carrier vessel alongside legally harvested fish, erasing provenance before reaching land.
2. **Obscuring catch origins:** When a reefer unloads at a processing hub, inspectors receive aggregated manifests that make it extraordinarily difficult to tie consignments back to catching logbooks.
3. **Facilitating labor exploitation:** Isolating crew members aboard catching vessels on the high seas for years without port visits creates high vulnerability to forced labor, debt bondage, and human trafficking (Harris & Haubursin 2025).

### 6.3.2 Algorithmic rendezvous detection

Detecting transshipment events from AIS requires identifying spatial-temporal convergences between vessels operating far from shore (Miller et al. 2018; Boerder, Miller & Worm 2018). The core detection pipeline flags two distinct behavioral states:

1. **Two-Vessel Rendezvous:** Occurs when both the catching vessel and the carrier vessel broadcast active AIS telemetry while maneuvering together. The algorithm filters for pairs of vessels meeting three joint criteria:
   - **Spatial proximity:** Geodesic distance remains below a strict threshold ($\Delta d \le 100\text{ to }500\text{ m}$) for a sustained interval.
   - **Kinematic matching:** Both vessels maintain low relative velocities ($\text{SOG} \le 2.0\text{ kn}$) characteristic of drifting together with fenders deployed.
   - **Temporal persistence:** The encounter persists for a minimum duration, typically $\Delta t \ge 2\text{ hours}$ (often extending beyond 24 hours for hold offloads).
   - **Distance from shore:** The event occurs outside protected anchorages or designated port limits ($d_{\text{coast}} > 20\text{ nmi}$ [37 km]), distinguishing high-seas rendezvous from routine harbor mooring.

2. **Carrier Loitering Events:** Occurs when a carrier vessel exhibits the kinematic hallmarks of a rendezvous, but no corresponding catcher vessel broadcasts AIS. The reefer drifts at speeds below 2.0 kn for $\ge 4\text{ hours}$ in high-seas fishing grounds. These loitering events frequently represent unilateral transshipments with dark vessels whose transponders are intentionally disabled or unequipped with AIS.

Global analyses of transshipment behavior reveal massive spatial clustering (Boerder, Miller & Worm 2018). Major hotspots include the northwest Pacific Ocean, the southwest Atlantic off the Patagonian Shelf, the equatorial Pacific, and waters surrounding West Africa. Carrier vessels operating under flags of convenience routinely service distant-water fleets, offloading thousands of tons of tuna, squid, and demersal fish into global trade streams.

> **Definitions that bite.**
>
> - **Transshipment vs. Transfer:** *Transshipment* refers specifically to transferring fish or fisheries products between vessels. Fuel bunkering or gear transfers are legally distinct operations. An algorithmic encounter cannot observe what crosses the rail; verifying whether fish moved requires cross-referencing RFMO authorizations or landing declarations.
> - **Loitering Event:** A single-vessel anomaly where a carrier drifts at slow speeds ($<2\text{ kn}$) far from shore for several hours. While indicative of meeting dark vessels, loitering also occurs during engine repairs or foul weather.

## 6.4 The dark fleet: intentional AIS disabling vs. reception physics

### 6.4.1 Mechanics and incentives for going dark

When a vessel turns off its AIS transponder, it enters the non-broadcasting or **dark fleet**. The master or crew simply flips the circuit breaker on the bridge, cuts the VHF antenna feed, or unplugs the transponder's NMEA power cable ([Chapter 36](ch36-failure-modes.md)).

Operational incentives for intentionally disabling AIS span licit competitive motives and illicit evasive strategies:

1. **Protecting proprietary fishing grounds:** In lucrative fisheries, broadcasting real-time coordinates exposes productive fishing spots to competitors, prompting skippers to disable AIS to protect search investments (Welch et al. 2022).
2. **Preventing piracy or robbery:** In high-risk corridors (such as the Gulf of Guinea), vessels switch off AIS to avoid broadcasting positions to pirate skiffs, an action explicitly sanctioned under safety guidelines (IMO Resolution A.1106(29)).
3. **Poaching across maritime boundaries:** Vessels operating near marine reserves disable transponders prior to crossing the maritime boundary, conduct illegal sets within protected waters, and power the transponder back on upon returning to the high seas.
4. **Evading sanctions and quotas:** Fleets harvesting species restricted by international treaties or UN sanctions intentionally sever AIS connectivity to prevent catch attribution.

In an exhaustive survey of global AIS disabling events across industrial fishing fleets, Welch et al. (2022) identified more than 55,000 suspected intentional disabling events totaling nearly 5 million hours of obscured activity. Disabling was heavily concentrated along four geographic fronts: the maritime boundaries of Argentina, the EEZs of West African nations, the northwest Pacific near the Russian and Japanese EEZs, and the perimeter of the Galápagos Marine Reserve.

> **Case file.** The Galápagos squid fleet border confrontation.
>
> In the summer of 2020, international attention focused on a distant-water fleet comprising roughly 300 industrial vessels—predominantly Chinese-flagged squid jiggers and refrigerated reefers—amassing along the southern boundary of the Galápagos Marine Reserve. The Galápagos EEZ is an ecological sanctuary designated as a UNESCO World Heritage site, home to vulnerable shark, turtle, and marine mammal populations.
>
> Satellite AIS tracking revealed hundreds of vessels lined up precisely along the outer edge of Ecuador's 200-nautical-mile EEZ border. Ecuadorian naval authorities reported that dozens of vessels repeatedly dropped off satellite AIS feeds for hours or days at a time while operating directly adjacent to the boundary line.
>
> Analyzing these telemetry gaps required separating orbital receiver blind spots from deliberate deactivations. Investigations by Global Fishing Watch, independent ocean journalists (Harris & Haubursin 2025), and naval tracking centers established that vessels deactivated transponders while drifting near the boundary, obscuring whether individual jiggers drifted across the line into Ecuadorian waters during night fishing sets. The incident catalyzed multinational naval patrols, triggered diplomatic protests, and accelerated the adoption of satellite Synthetic Aperture Radar to police marine boundaries independently of transponder broadcasts.

### 6.4.2 Separating deliberate gaps from RF packet collisions

The central analytical challenge in dark fleet detection is proving that an AIS signal gap was caused by human intervention rather than electromagnetic propagation failures or orbital reception limits. An analyst cannot assume that every multi-hour absence of AIS telemetry indicates an illicit voyage.

As detailed in [Chapter 30](ch30-network-loading-packet-loss.md) and [Chapter 39](ch39-satellite-ais.md), satellite AIS receivers in Low Earth Orbit (**LEO**) suffer from severe RF packet collisions. Because a LEO satellite footprint covers a circular area thousands of kilometers in diameter, hundreds of decentralized SOTDMA operational cells broadcast simultaneously on VHF Channels 87B and 88B. In high-density shipping regions, thousands of overlapping bursts arrive at the satellite antenna concurrently, destroying message packets at the physical receiver. A vessel can transmit continuously, yet orbital satellites may fail to decode a clean message for hours.

To distinguish deliberate switch-offs from reception artifacts, analysts employ rigorous statistical and spatial criteria (Welch et al. 2022):

1. **Local Satellite Reception Probability ($P_{\text{det}}$):** The baseline probability of detecting an active transponder within a specific geographic grid cell ($1^\circ \times 1^\circ$) and time window is computed across surrounding non-fishing commercial traffic. If nearby merchant ships are delivering dozens of messages per hour to LEO satellites while a fishing vessel vanishes completely for 12 hours, the probability that the gap was caused by RF packet collision approaches zero.
2. **Kinematic Boundary Analysis:** If a vessel's telemetry disappears in open ocean and reappears 18 hours later at coordinates consistent with steady steaming along its last known COG and SOG, the dropout is consistent with a satellite orbit gap. Conversely, if a vessel vanishes at the edge of an MPA and reappears 24 hours later at the exact same location, having executed complex unobserved maneuvers, intentional deactivation is inferred.
3. **Class A vs. Class B Disparities:** Class B transponders broadcast at lower RF output power (2 W for CSTDMA; 5 W for SOTDMA) compared to Class A units (12.5 W) and do not receive TDMA slot reservation priority ([Chapter 20](ch20-architecture-and-station-classes.md)). Class B satellite reception rates are inherently lower, demanding wider statistical confidence intervals before asserting intentional disabling.

## 6.5 Satellite multi-sensor fusion: hunting dark vessels from orbit

When a vessel extinguishes its AIS transponder, maritime authorities must turn to orbital earth observation sensors that do not rely on cooperative radio broadcasts. Spaceborne **Synthetic Aperture Radar** (**SAR**), high-resolution **optical imagery**, and **nighttime radiometry** provide independent empirical detections that can be fused with AIS telemetry to expose dark fleets.

```
       +-----------------------------------------------------------+
       |               Orbital Sensor Fusion Pipeline              |
       +-----------------------------------------------------------+
               |                           |
               v                           v
     Orbital SAR Imagery          Nighttime Radiometry
    (Sentinel-1 C-Band SAR)       (VIIRS Day/Night Band)
               |                           |
               +-------------+-------------+
                             |
                             v
               Deep Learning Vessel Detection
               (Bounding Boxes, Length, CFAR)
                             |
                             v
               Co-temporal AIS Telemetry Matching
               (Spatial-Temporal Association Window)
                             |
              +--------------+--------------+
              |                             |
              v                             v
       Correlated Targets             Dark Targets
     (AIS Broadcast Match)         (No AIS Transmitted)
              |                             |
              v                             v
      Verified Shipping /           Non-Broadcasting Fleet:
      Compliant Fisheries          Target for Interdiction
```

### 6.5.1 Synthetic Aperture Radar (SAR)

Spaceborne SAR sensors (such as Sentinel-1, TerraSAR-X, ICEYE, and Capella Space) emit active microwave pulses (typically C-band at $\sim 5.4\text{ GHz}$ or X-band at $\sim 9.6\text{ GHz}$) and measure backscattered energy reflected from the ocean surface ([Chapter 66](ch66-other-ways-to-track-ships.md)).

Because open water acts as a specular reflector scattering microwave energy away from the sensor, undisturbed sea surfaces appear dark in radar imagery. In contrast, metallic ship hulls act as corner reflectors, returning intense microwave energy back to the satellite, creating brilliant point-source targets. Crucially, SAR operates independently of solar illumination and penetrates cloud cover, fog, and rain.

Automated pipelines identify vessel candidates using **Constant False Alarm Rate** (**CFAR**) algorithms or deep learning object-detection networks (such as YOLO or Faster R-CNN) trained on SAR backscatter patches. These models extract target center coordinates, estimated vessel length ($L$), beam ($W$), and orientation.

### 6.5.2 Nighttime radiometry (VIIRS)

Nighttime visible and near-infrared sensors—specifically the **Visible Infrared Imaging Radiometer Suite** (**VIIRS**) aboard NOAA-20 and Suomi NPP satellites—detect artificial light emissions on the ocean surface via the Day/Night Band (**DNB**).

While traditional merchant ships emit minimal upward light, industrial squid jiggers and light-luring purse seiners illuminate the ocean with hundreds of kilowatts of lighting to attract phototactic squid and baitfish. These bright light sources appear in nighttime satellite passes as intensely luminous spatial clusters. VIIRS imagery captures thousands of megawatts of fishing illumination in the Sea of Japan, the Patagonian Shelf, and the Arabian Sea, pinpointing fleets operating with transponders powered off.

### 6.5.3 Multi-sensor association algorithms

To determine whether an orbital detection is compliant or dark, the system executes automated spatial-temporal correlation against historical and interpolated AIS feeds:

1. **Temporal gating:** For an orbital satellite pass at timestamp $t_{\text{sat}}$, the pipeline extracts all vessel AIS tracks within the footprint spanning $[t_{\text{sat}} - \Delta t, t_{\text{sat}} + \Delta t]$.
2. **Kinematic interpolation:** Coordinates at the exact second of satellite imaging are estimated using Hermite spline interpolation or dead reckoning from surrounding fixes ([Chapter 47](ch47-data-quality-track-reconstruction.md)).
3. **Spatial association:** The algorithm solves a bipartite matching problem between observed orbital targets ($O_i$) and interpolated AIS positions ($A_j$):
   
   $$\text{Dist}(O_i, A_j) \le \delta_{\text{pos}} + v_{\text{max}} \cdot |t_{\text{sat}} - t_{\text{AIS}}|$$
   
4. **Dark classification:** Any orbital target exceeding a minimum size threshold (e.g., $L \ge 20\text{ m}$) that cannot be matched to a broadcasting AIS transponder is classified as a **dark vessel**.

In a historic breakthrough applying this methodology across five years of Sentinel-1 radar and optical passes, Paolo et al. (2024) mapped industrial activity across all global coastal waters from 2017 to 2021. Their findings revealed that **approximately 72% to 76% of the world's industrial fishing vessels were not publicly tracked via AIS**. This untracked dark fleet was intensely concentrated across South Asia, Southeast Asia, and Africa. Even among transport and energy sector vessels, 21% to 30% were missing from public tracking databases.

A prominent application of multi-sensor fusion occurred in the Sea of Japan. In an investigation led by Park et al. (2020), researchers fused AIS, Sentinel-1 SAR, high-resolution optical imagery from Planet Labs, and nighttime VIIRS data to expose illegal fishing in North Korean waters. The analysis uncovered over 900 Chinese-origin industrial pair trawlers and lighting vessels operating in North Korean waters in 2017, and over 700 in 2018, in direct violation of United Nations Security Council sanctions (Resolution 2397). The illicit fleet harvested an estimated 164,000 metric tons of Pacific flying squid valued at over $440 million, displacing small-scale local fishers and forcing unequipped domestic wooden boats into hazardous Russian waters, resulting in hundreds of fatal maritime strandings.

## 6.6 Distant-water fleets and geopolitical dimensions

The modern industrial fishing landscape is dominated by distant-water fishing fleets (**DWFs**) operated by a small group of flag states: mainland China, Taiwan, South Korea, Japan, and Spain. Among these, China's distant-water fleet is by far the largest, operating an estimated 2,500 to 3,000 vessels across all major ocean basins.

These fleets operate along specific oceanic corridors dictated by marine productivity and regional governance vacuums:

1. **The Patagonian Shelf (Southwest Atlantic):** Beyond Argentina's 200-nautical-mile EEZ lies the "Mile 201" fishing zone. Because there is no comprehensive Regional Fisheries Management Organization governing the high seas of the Southwest Atlantic, hundreds of foreign squid jiggers and trawlers operate in a legal vacuum. Fleets loiter precisely along the EEZ contour, cutting AIS transponders to execute clandestine night incursions into Argentina's EEZ.
2. **The Galápagos and Peru Corridor (Southeast Pacific):** Massive aggregations of Chinese squid jiggers track the seasonal migration of jumbo flying squid from international waters off Peru to the equatorial perimeter of the Galápagos Islands. Supported by factory reefers and oil tankers, these vessels remain deployed for up to two years without touching South American ports.
3. **West Africa (Gulf of Guinea):** Foreign industrial trawlers operate under opaque bilateral licensing agreements or charter arrangements with local shell companies. Vessels routinely fish inside nearshore zones reserved exclusively for artisanal fishers, devastating local artisanal canoes and destroying benthic ecosystems while broadcasting falsified MMSI identifiers or disabling AIS entirely.

The geopolitical enforcement gap stems from flag-state jurisdiction under Article 94 of UNCLOS. Unless a coastal state catches a foreign vessel red-handed inside its EEZ, enforcement authority on the high seas rests solely with the vessel's flag state. Developing coastal nations frequently lack the naval patrol assets, satellite reconnaissance funding, and diplomatic leverage required to interdict distant-water fleets, creating systemic dependence on multilateral data-sharing partnerships.

## 6.7 Legal frameworks and regulatory mandates

### 6.7.1 The European Union: Directive 2002/59/EC and Regulation 1224/2009

The European Union has enacted some of the world's most prescriptive legal mandates governing fishing-vessel tracking, establishing distinct statutory tiers for safety broadcasts and fisheries control.

Under **Directive 2002/59/EC**, as amended by Directive 2009/17/EC and Directive 2011/15/EU, the European Parliament and Council established mandatory AIS carriage for fishing vessels based on overall length (**LOA**):

- **Article 6a:** Mandates that any fishing vessel exceeding 15 meters in length overall flying the flag of an EU Member State, operating in EU territorial waters, or landing catch in an EU port must be fitted with an IMO-compliant Class A AIS transponder.
- **Carriage Phase-in Schedule (Annex II, Part I):**
  - New-build fishing vessels $> 15\text{ m}$: Mandatory from 30 November 2010.
  - Existing fishing vessels $24\text{ m} \le \text{LOA} < 45\text{ m}$: Mandatory by 31 May 2012.
  - Existing fishing vessels $18\text{ m} \le \text{LOA} < 24\text{ m}$: Mandatory by 31 May 2013.
  - Existing fishing vessels $15\text{ m} < \text{LOA} < 18\text{ m}$: Mandatory by 31 May 2014.

Parallel to maritime safety directives, **Council Regulation (EC) No 1224/2009** (the EU Fisheries Control Regulation) formalized the integration of AIS into fisheries compliance:
- **Article 10(1):** Fishing vessels exceeding 15 meters LOA must maintain their Class A AIS transponder in continuous operation at all times.
- **Article 10(3):** Authorizes national fisheries control authorities to cross-check open AIS telemetry against confidential VMS data, electronic logbook reports (**ERS**), and sales notes to detect fraud and unauthorized incursions.
- **Article 9:** Operates a separate, mandatory satellite VMS regime for all fishing vessels $\ge 12\text{ m}$ LOA, reporting at intervals not exceeding two hours directly to national FMCs.

In December 2023, the EU published **Regulation (EU) 2023/2842**, overhauling the Control Regulation. Entering into force in January 2024 (with operational enforcement phased through 2026), the new regulation mandates electronic tracking for *all* fishing vessels without exception, extending satellite or cellular tracking to small-scale artisanal fleets under 12 meters, while tightening sanctions for unauthorized AIS deactivation.

### 6.7.2 The FAO Port State Measures Agreement (PSMA)

Enacted under the United Nations Food and Agriculture Organization (**FAO**), the **Agreement on Port State Measures** (**PSMA**) entered into force on 5 June 2016 and represents the foremost international treaty targeting IUU fishing.

The core mechanism of the PSMA is closing commercial ports to illegal operators. Under the treaty, foreign fishing vessels and carrier reefers seeking port entry must submit advance formal notifications (Annex A declarations) detailing vessel identity, flag state, fishing authorizations, catch on board, and tracking history. If the port state detects evidence of IUU fishing, transponder tampering, or unauthorized transshipment, it must deny port entry, prohibit landing or transshipping catch, and notify the vessel's flag state and regional RFMOs. AIS tracking archives provide port inspectors with the historical voyage reconstructions necessary to audit Annex A declarations before granting dockage.

### 6.7.3 The Joint Analytical Cell (JAC)

To operationalize satellite surveillance for resource-constrained coastal nations, a coalition of maritime intelligence organizations established the **Joint Analytical Cell** (**JAC**) in May 2022. Founded by **Global Fishing Watch**, **Trygg Mat Tracking** (**TMT**), and the **International Monitoring, Control and Surveillance** (**IMCS**) Network—with analytical collaboration from **Skylight** and **C4ADS**—the JAC functions as an operational intelligence fusion hub.

The JAC combines satellite AIS analytics, SAR target correlation, vessel identity tracking (auditing flag changes and call-sign manipulation via TMT's FACT database), and beneficial ownership research. By synthesizing commercial and open-source intelligence, the cell provides coastal fisheries authorities across West Africa, the Pacific Island nations, and Latin America with actionable risk profiles, alerting patrol assets to dark-vessel incursions and prioritizing high-risk reefers for physical dockside inspections under the PSMA.

> **Legal note.**
>
> - **The "Keep It On" Mandate vs. Master's Discretion:** Under SOLAS Chapter V, Regulation 19.2.4.7, ships fitted with AIS "shall maintain AIS in operation at all times except where international agreements, rules or standards provide for the protection of navigational information." IMO Resolution A.1106(29) provides the operational interpretation: if the master considers continual operation a threat to vessel safety or security (e.g., in waters with imminent piracy risks), the transponder may be switched off. However, the action and its operational justification must be formally entered into the ship's official logbook, and reported to the relevant coastal authority when operating within a mandatory vessel reporting system.
> - **EU Jurisdictional Power:** In EU waters, Article 6a of Directive 2002/59/EC and Article 10 of Regulation 1224/2009 make continuous AIS operation mandatory for fishing vessels $> 15\text{ m}$. Switching off AIS without documented safety justifications constitutes a direct statutory violation, subjecting owners to administrative fines, catch confiscation, and revocation of fishing licenses.

## Then & now

- ⟨H⟩ 1989 — Tanker *Exxon Valdez* runs aground in Alaska, accelerating OPA-90 and automated vessel tracking development.
- ⟨H⟩ 1998 — IMO adopts Resolution MSC.74(69) Annex 3, establishing technical performance standards for shipborne AIS.
- ⟨H⟩ 2000 — IMO Resolution MSC.99(73) revises SOLAS Chapter V, Regulation 19, mandating Class A AIS carriage on all international passenger ships and cargo vessels $\ge 300\text{ GT}$.
- ⟨+⟩ 2002 — EU adopts Directive 2002/59/EC, establishing the Community vessel traffic monitoring system (SafeSeaNet).
- ⟨H⟩ 2004 — Accelerated international SOLAS AIS carriage mandate enters into force across global commercial shipping.
- ⟨+⟩ 2008 — First orbital demonstrations of satellite AIS reception confirm VHF bursts can be harvested from Low Earth Orbit.
- ⟨+⟩ 2009 — EU enacts Council Regulation (EC) No 1224/2009 and Directive 2009/17/EC, mandating Class A AIS for fishing vessels $> 15\text{ m}$ LOA.
- ⟨+⟩ 2012 — EU phased AIS mandate takes effect for fishing vessels $24\text{ m} \le \text{LOA} < 45\text{ m}$ (31 May 2012).
- ⟨+⟩ 2014 — Final phase of EU fishing AIS carriage mandate takes effect for vessels $15\text{ m} < \text{LOA} < 18\text{ m}$ (31 May 2014).
- ⟨+⟩ 2016 — FAO Agreement on Port State Measures (PSMA) enters into force (5 June 2016), empowering port states to deny port access to IUU vessels.
- ⟨+⟩ 2018 — Kroodsma et al. publish global footprint of industrial fisheries in *Science*, processing 22 billion AIS reports with 1D CNNs.
- ⟨+⟩ 2018 — Miller et al. and Boerder et al. publish global satellite analyses of at-sea transshipment between fishing vessels and reefers.
- ⟨+⟩ 2020 — Park et al. in *Science Advances* expose over 900 Chinese-origin dark industrial vessels fishing in North Korean waters.
- ⟨+⟩ 2022 — Welch et al. publish global geography of intentional AIS disabling in *Science Advances*; GFW, TMT, and IMCS establish JAC.
- ⟨+⟩ 2023 — EU adopts Regulation (EU) 2023/2842, expanding mandatory tracking across all commercial fishing vessels, including $< 12\text{ m}$.
- ⟨+⟩ 2024 — Paolo et al. in *Nature* combine satellite AIS with orbital SAR and optical imagery, revealing roughly 75% of industrial fishing vessels are not publicly tracked.
- ⟨+⟩ 2025 — Johnny Harris and Christophe Haubursin release *What's really happening in the ocean's "dark zones"*, highlighting dark fleets and labor abuse.

## On the wire

Fishing vessels transmit dynamic reports primarily via Message 1, 2, or 3 (Class A) or Message 18 (Class B), alongside static voyage reports (Message 5 and Message 24). Static reports carry critical identity fields including declared ship type, dimensions, and call sign.

Under ITU-R M.1371-5, Table 50, static `Ship Type` is encoded as an 8-bit integer ($[0, 255]$). For commercial fishing vessels, the standard designation is code `30`:

```
       +-----------------------------------------------------------+
       |             ITU-R M.1371-5 Vessel Type Codes              |
       +-----------+-----------------------------------------------+
       | Code (Dec)| Description                                   |
       +-----------+-----------------------------------------------+
       | 30        | Fishing (all gear types)                      |
       | 31        | Towing                                        |
       | 32        | Towing (length > 200m or breadth > 25m)       |
       | 70 - 79   | Cargo vessels (70: all; 71: reefer / hazard)  |
       | 80 - 89   | Tankers                                       |
       +-----------+-----------------------------------------------+
```

A crucial limitation of the AIS wire protocol is that code `30` encompasses *all* fishing vessels indiscriminately. The protocol contains no field to differentiate a stern trawler from a pelagic longliner, tuna purse seiner, or squid jigger. This wire-level omission is what necessitates machine-learning kinematic classification pipelines ([Chapter 49](ch49-analytics-and-ml.md)).

Furthermore, fishing vessels frequently abuse static fields. Transponders often broadcast generic placeholder strings in Message 5 (such as `"FISHING"` or `"VESSEL"`) or leave the IMO number field set to `0`, either because small vessels lack an IMO number or because operators deliberately obscure vessel identity ([Chapter 13](ch13-mmsi-deep-dive.md)).

> **On the wire.** Decoding a fishing vessel's static parameters.
>
> Consider a raw NMEA 0183 Message 5 payload broadcast by an industrial trawler:
>
> ```text
> !AIVDM,2,1,3,B,55?P:D02>j7C<5PD000h4pE@000000000000001600000Bp0000000000000,0*36
> !AIVDM,2,2,3,B,00000000000,2*23
> ```
>
> Decoding the 424-bit payload reveals:
> - **MMSI:** `367123450` (United States MID)
> - **IMO Number:** `0` (Unassigned or unentered)
> - **Call Sign:** `"WDF1234"`
> - **Vessel Name:** `"OCEAN HARVESTER@@@@@"`
> - **Ship Type:** `30` (Binary `00011110`: Fishing)
> - **Dimension to Bow ($A$):** $28\text{ m}$, Stern ($B$): $12\text{ m}$ (Overall Length: $40\text{ m}$)
> - **Dimension to Port ($C$):** $5\text{ m}$, Starboard ($D$): $5\text{ m}$ (Overall Beam: $10\text{ m}$)
> - **Draught:** $3.8\text{ m}$
>
> The wire broadcast confirms the vessel is a 40-meter fishing craft. However, whether the vessel is actively trawling or steaming between grounds can only be determined by analyzing the dynamic kinematic parameters broadcast in its accompanying Message 1 reports.

## Validation, uncertainty & data quality

Ingesting AIS for fisheries analytics introduces distinct errors that propagate through behavioral models, risk scores, and enforcement triage:

1. **Static Data Fraud and Registry Mismatches:** Fishing vessels exhibit high rates of unverified static data. Transponders frequently transmit invalid MMSIs (e.g., `123456789`, `000000000`, or default factory strings such as `1193046`), cloned identities where multiple hulls share a single MMSI across different oceans, or falsified ship names designed to confuse inspectors. Trajectory pipelines must cross-check broadcast MMSIs against official IMO registries and regional RFMO authorized vessel records.
2. **Kinematic Noise and Outlier Geolocation:** Multipath RF reflections, faulty GNSS antenna cabling, and low-cost Class B receivers introduce erroneous position spikes, with coordinates jumping thousands of kilometers for a single epoch. Automated pipelines must apply kinematic gating:
   
   $$v_{\text{implied}} = \frac{\text{GeodesicDist}(\mathbf{p}_t, \mathbf{p}_{t-1})}{\Delta t} \le v_{\text{max\_hull}}$$
   
   where $v_{\text{max\_hull}}$ is set to $25\text{ kn}$ ($46.3\text{ km/h}$) for fishing craft. Reports implying accelerations exceeding $2.0\text{ m/s}^2$ are purged.
3. **Orbital Density Falloff and Spatial Uncertainty:** In dense fishing grounds, satellite message reception probability ($P_{\text{det}}$) drops significantly. When calculating total fishing effort (hours fished per $0.1^\circ$ grid cell), raw observation counts severely underestimate effort in congested waters. Data systems must normalize effort using satellite pass coverage grids and empirical detection curves ([Chapter 48](ch48-spatial-statistics.md)).

```
+--------------------------------------------------------------------------+
|                 Fisheries Telemetry Validation Pipeline                  |
+--------------------------------------------------------------------------+
                                     |
                                     v
                        Raw AIS Message Ingestion
                                     |
                                     v
                   [Check 1: MMSI & Format Screening]
                    - Drop MID < 200 or > 775
                    - Screen default test IDs (1193046, 0)
                                     |
                                     v
                   [Check 2: Kinematic Plausibility]
                    - Geodesic speed gating (implied SOG <= 25 kn)
                    - Acceleration threshold (<= 2.0 m/s^2)
                                     |
                                     v
                   [Check 3: Coverage De-biasing]
                    - Match against orbital pass footprints
                    - Compute local detection probability P_det
                                     |
                                     v
                   [Check 4: Behavioral Classification]
                    - Sliding-window 1D CNN / Transformer model
                    - Pointwise fishing score p_fishing in [0, 1]
                                     |
                                     v
                        Verified Fisheries Metric
```

## Software

**Open source:**
- **pyais:** Python library for decoding raw NMEA 0183 and AIVDM/AIVDO message streams, including TAG blocks, multi-sentence payloads, and Class B messages ([Chapter 44](ch44-open-source-decoders-history.md)). *Caveat:* Pure Python implementation requires multiprocessing optimizations for planetary message streams.
- **MovingPandas:** Spatial-temporal trajectory analysis library built on GeoPandas and Shapely, featuring trajectory segmentation, stop detection, and movement clustering ([Chapter 45](ch45-processing-software.md)). *Caveat:* Memory-intensive; unsuited for raw global archives without distributed partitioning.
- **Global Fishing Watch Research Pipelines:** Publicly archived machine-learning repositories (available via GFW GitHub) providing 1D CNN architectures, vessel characterization pipelines, and fishing detection models. *Caveat:* Models depend on specific data preprocessing formats and cloud infrastructure.

**Free but closed:**
- **Global Fishing Watch Map:** Interactive web portal providing public global visualization of commercial fishing activity, carrier vessel encounters, and marine protected areas. *Caveat:* Aggregated public display features temporal latency; raw proprietary features require data-sharing agreements.
- **Skylight:** Maritime monitoring platform developed by the Allen Institute for AI (AI2), ingesting satellite imagery and AIS to alert enforcement agencies to dark vessels and MPA incursions. *Caveat:* Restricted access reserved for government agencies, NGOs, and verified researchers.

**Commercial:**
- **Spire Maritime:** Global satellite AIS provider operating a proprietary constellation of Low Earth Orbit nanosatellites with automated message deduplication, dynamic weather layering, and vessel APIs. *Caveat:* High commercial licensing fees; proprietary message deduplication algorithms.
- **Starboard Maritime Intelligence:** Commercial maritime domain awareness suite fusing satellite AIS, SAR, and RF geolocation for EEZ surveillance and biosecurity enforcement. *Caveat:* Commercial subscription model; closed proprietary analytical algorithms.

## Standards & guides

- **IMO Resolution MSC.74(69), Annex 3:** *Recommendation on Performance Standards for a Universal Shipborne Automatic Identification System (AIS)* (1998). Technical specifications for shipborne AIS units.
- **IMO Resolution MSC.99(73):** *Amendments to SOLAS Chapter V, Regulation 19* (2000). Universal AIS carriage requirements.
- **IMO Resolution A.1106(29):** *Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems (AIS)* (2015). Operational protocols and conditions for switching off transponders.
- **ITU-R Recommendation M.1371-5:** *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band* (2014). Governs RF modulation, TDMA framing, and bit layouts.
- **Directive 2002/59/EC:** *Community vessel traffic monitoring and information system* (amended by 2009/17/EC and 2011/15/EU). Mandatory Class A AIS carriage for fishing vessels $> 15\text{ m}$ LOA.
- **Council Regulation (EC) No 1224/2009:** *Community control system for ensuring compliance with the common fisheries policy* (amended by Regulation (EU) 2023/2842). Continuous AIS operation and cross-checking against VMS.
- **FAO Agreement on Port State Measures (PSMA):** *Agreement on Port State Measures to Prevent, Deter and Eliminate Illegal, Unreported and Unregulated Fishing* (2009; entered into force 2016). International standards for port inspections and pre-entry declarations.

## Pitfalls

1. **Assuming every AIS gap indicates deliberate illicit evasion.** Atmospheric ducting, local VHF interference, and satellite RF packet collisions regularly prevent message reception. Analysts must evaluate local detection probability ($P_{\text{det}}$) across surrounding traffic before asserting intentional transponder deactivation.
2. **Treating vessel type code `30` as a complete operational characterization.** The AIS wire protocol does not specify gear type. Assuming all vessels broadcasting code `30` operate identically introduces severe bias; pipelines must classify gear behavior using trajectory kinematics.
3. **Equating close-proximity encounters directly to fish transshipment.** AIS tracks indicate geometric proximity, not cargo contents. An encounter may represent fuel bunkering, provisioning, mechanical repair, or rafted drift during foul weather. Differentiating fish transshipment requires cross-referencing vessel types (reefer vs. tanker) and regulatory catch authorizations.
4. **Failing to filter synthetic and cloned MMSI identities.** Multiple illicit vessels frequently broadcast identical MMSIs to obscure fleet movements, creating impossible kinematic jumps between distant ocean basins. Ingestion software must track spatial continuity per MMSI and split tracks exhibiting simultaneous multi-region reports.
5. **Relying on static ship dimensions for tonnage estimations.** Transponder dimension fields ($A, B, C, D$) are manually entered via Minimum Keyboard and Display (**MKD**) units and frequently contain transposed numbers or default placeholders, skewing fishing capacity estimates.
6. **Ignoring Class A vs. Class B reception biases.** Class B transponders broadcast at lower RF power ($2\text{ W}$ or $5\text{ W}$) and lack slot reservation priority. Space-based satellite detection rates for Class B craft are substantially lower than for Class A vessels, leading to undercounting of smaller artisanal vessels.
7. **Using planar Euclidean distance calculations across high-latitude fishing grounds.** Calculating distances in degrees or planar projections introduces extreme distortions in polar and sub-polar fisheries. All distance calculations must use geodesic formulas.
8. **Interpreting carrier vessel loitering as definitive guilt.** A refrigerated carrier drifting slowly in international waters may be awaiting commercial orders, drifting in heavy weather, or conducting routine maintenance. Triage algorithms must flag loitering as an operational risk factor, not an unassisted conviction.

## Key takeaways

- Broadcast AIS transformed global fisheries oversight from closed, fragmented state VMS reporting into open, planetary monitoring.
- Commercial fishing gear types exhibit distinct kinematic signatures: trawlers maintain steady towing speeds ($2.0\text{--}4.5\text{ kn}$); longliners show alternating set-and-haul patterns; purse seiners execute circular encirclement maneuvers; squid jiggers drift passively at night.
- Deep learning pipelines (1D CNNs and sequence transformers) evaluate temporal trajectory windows to classify vessel gear and compute pointwise fishing probabilities without relying on rigid speed cutoffs.
- High-seas transshipment between fishing vessels and refrigerated reefers can launder illegal catch and obscure supply-chain provenance; algorithms identify transshipments by detecting sustained close proximity ($\Delta d \le 500\text{ m}$, $\text{SOG} \le 2\text{ kn}$, $\Delta t \ge 2\text{ h}$).
- Differentiating intentional AIS deactivation from RF packet collisions requires evaluating the local reception probability ($P_{\text{det}}$) derived from surrounding non-fishing traffic.
- Orbital multi-sensor fusion combining satellite AIS, Synthetic Aperture Radar (SAR), high-resolution optical imagery, and nighttime VIIRS radiometry exposes non-broadcasting dark vessels.
- Recent orbital surveys demonstrate that roughly 75% of the world's industrial fishing vessels are not publicly tracked via AIS.
- Legal frameworks—including European Union Directive 2002/59/EC, Council Regulation 1224/2009, and the FAO Port State Measures Agreement—mandate continuous transponder operation and empower port authorities to audit tracking histories before granting landing authorizations.

## References

- Agnew, D. J., Pearce, J., Pramod, G., Peatman, T., Watson, R., Beddington, J. R. & Pitcher, T. J. (2009). Estimating the Worldwide Extent of Illegal Fishing. *PLoS ONE*, 4(2):e4570. doi:10.1371/journal.pone.0004570.
- Boerder, K., Miller, N. A. & Worm, B. (2018). Global hot spots of transshipment of fish catch at sea. *Science Advances*, 4(7):eaat7159. doi:10.1126/sciadv.aat7159.
- Council of the European Union (2009). *Council Regulation (EC) No 1224/2009 establishing a Community control system for ensuring compliance with the rules of the common fisheries policy*. Official Journal of the European Union, L 343:1–50.
- Cutlip, K. (2017). *AIS for Safety and Tracking: A Brief History*. Washington, DC: Global Fishing Watch. https://globalfishingwatch.org/article/ais-brief-history/ (accessed 2026-10-06).
- de Souza, E. N., Boerder, K., Matwin, S. & Worm, B. (2016). Improving fishing pattern detection from satellite AIS using data mining and machine learning. *PLoS ONE*, 11(7):e0158248. doi:10.1371/journal.pone.0158248.
- European Parliament and Council of the European Union (2002). *Directive 2002/59/EC establishing a Community vessel traffic monitoring and information system and repealing Council Directive 93/75/EEC*. Official Journal of the European Communities, L 208:10–27.
- European Parliament and Council of the European Union (2009). *Directive 2009/17/EC amending Directive 2002/59/EC establishing a Community vessel traffic monitoring and information system*. Official Journal of the European Union, L 131:101–113.
- European Parliament and Council of the European Union (2023). *Regulation (EU) 2023/2842 amending Council Regulation (EC) No 1224/2009, and amending Council Regulations (EC) No 1967/2006 and (EC) No 1005/2008*. Official Journal of the European Union, L 2023/2842.
- Food and Agriculture Organization of the United Nations (2009). *Agreement on Port State Measures to Prevent, Deter and Eliminate Illegal, Unreported and Unregulated Fishing*. Rome: FAO.
- Harris, J. & Haubursin, C. (2025). *What's really happening in the ocean's "dark zones"*. YouTube video 2tuS1LLOcsI, channel @johnnyharris. https://www.youtube.com/watch?v=2tuS1LLOcsI.
- International Maritime Organization (1998). *Recommendation on Performance Standards for a Universal Shipborne Automatic Identification System (AIS)* (Resolution MSC.74(69), Annex 3). Adopted 12 May 1998. London: IMO.
- International Maritime Organization (2000). *Adoption of Amendments to the International Convention for the Safety of Life at Sea, 1974, as Amended (SOLAS Chapter V)* (Resolution MSC.99(73)). Adopted 5 December 2000. London: IMO.
- International Maritime Organization (2015). *Revised Guidelines for the Onboard Operational Use of Shipborne Automatic Identification Systems (AIS)* (Resolution A.1106(29)). Adopted 2 December 2015. London: IMO.
- International Telecommunication Union (2014). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band* (Recommendation ITU-R M.1371-5). Geneva: ITU Radiocommunication Sector.
- Kroodsma, D. A., Mayorga, J., Hochberg, T., Miller, N. A., Boerder, K., Ferretti, F., Wilson, A., Bergman, B., White, T. D., Block, B. A., Woods, P., Sullivan, B., Costello, C. & Worm, B. (2018). Tracking the global footprint of fisheries. *Science*, 359(6378):904–908. doi:10.1126/science.aao5646.
- Miller, N. A., Roan, A., Hochberg, T., Woods, P. J., Amos, T. & Kroodsma, D. A. (2018). Identifying Global Patterns of Transshipment Behavior. *Frontiers in Marine Science*, 5:240. doi:10.3389/fmars.2018.00240.
- Paolo, F. S., Kroodsma, D. A., Raynor, J., Hochberg, T., Davis, P., Cleary, J., Marsaglia, L., Orofino, S., Thomas, C. & Halpin, P. N. (2024). Satellite mapping reveals extensive industrial activity at sea. *Nature*, 625(7993):85–91. doi:10.1038/s41586-023-06825-8.
- Park, J., Lee, J., Seto, K., Hochberg, T., Wong, B. A., Miller, N. A., Takasaki, K., Kubota, H., Oozeki, Y., Jeon, S., Sandven, P., Shen, C. & Kroodsma, D. A. (2020). Illuminating dark fishing fleets in North Korea. *Science Advances*, 6(30):eabb1197. doi:10.1126/sciadv.abb1197.
- Pauly, D. & Zeller, D. (2016). Catch reconstructions reveal that global marine fisheries catches are higher than reported and declining. *Nature Communications*, 7:10244. doi:10.1038/ncomms10244.
- Welch, H., Clavelle, T., White, T. D., Cimino, M. A., Van Osdel, J., Hochberg, T., Kroodsma, D. & Hazen, E. L. (2022). Hot spots of unseen fishing vessels. *Science Advances*, 8(44):eabq2109. doi:10.1126/sciadv.abq2109.
