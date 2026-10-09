# Chapter 66 — Other ways to track ships

> **Part X — Adjacent and complementary systems; the future.** Maritime surveillance extends far beyond cooperative VHF transponders into satellite-polled registries, coastal and over-the-horizon radars, spaceborne synthetic aperture radar and optical sensors, commercial radio-frequency geolocation constellations, underwater acoustics, and global port state intelligence.

**In this chapter.** You will learn how to track ships when the Automatic Identification System (**AIS**) is absent, disabled, manipulated, or out of range. We survey the full spectrum of non-AIS maritime tracking technologies, analyzing their physical architectures, reporting regimes, and access models. You will examine the cooperative closed-channel networks—specifically the global Vessel Monitoring System (**VMS**) for fisheries and Long-Range Identification and Tracking (**LRIT**) under SOLAS Regulation V/19-1—that transmit point-to-point via satellite without public VHF broadcast. We then dive into active and passive non-cooperative sensors: coastal microwave radar, High-Frequency Surface-Wave Radar (**HFSWR**), spaceborne Synthetic Aperture Radar (**SAR**), high-resolution optical earth observation, spaceborne Radio Frequency (**RF**) emitter geolocation, underwater acoustics, and port state administrative databases. Finally, you will explore multi-sensor track correlation algorithms, spatial-temporal gating, and the operational trade-offs of multi-source maritime domain awareness.

## 66.1 The limits of cooperative broadcast surveillance

The Automatic Identification System is a cooperative, unauthenticated, line-of-sight VHF broadcast protocol ([Chapter 01](ch01-what-ais-is.md)). Ships broadcast their identity, position, course, speed, and voyage metadata on international channels AIS 1 (161.975 MHz) and AIS 2 (162.025 MHz) ([Chapter 28](ch28-rf-encoding-physical-layer.md)). When functioning as intended, AIS delivers dense situational awareness for collision avoidance and coastal traffic management.

However, relying exclusively on AIS creates critical surveillance vulnerabilities:
1. **Voluntary and unauthenticated transmissions:** AIS lacks cryptographic authentication ([Chapter 64](ch64-authentication-future-security.md)). Transmitted data can be manipulated, falsified, or silenced by flipping a bridge breaker ([Chapter 58](ch58-threat-model.md) and [Chapter 59](ch59-spoofing.md)).
2. **Carriage exemptions:** Thousands of vessels legally operate without AIS. SOLAS Chapter V Regulation 19 mandates Class A transponders only for commercial cargo ships of 300 gross tonnage (**GT**) or more on international voyages, 500 GT or more on domestic voyages, and all passenger vessels regardless of size ([Chapter 16](ch16-laws-and-treaties.md)). Small commercial craft, artisanal and medium fishing vessels in many jurisdictions, recreational boats, and naval combatants are largely exempt.
3. **RF propagation and coverage constraints:** Line-of-sight VHF signals attenuate beyond the 4/3-Earth radio horizon ($d \approx 4.12(\sqrt{h_{\text{rx}}} + \sqrt{h_{\text{tx}}})\text{ km}$) ([Chapter 27](ch27-rf-basics.md)). In the open ocean, reception depends on Low Earth Orbit (**LEO**) satellite payloads ([Chapter 39](ch39-satellite-ais.md)), which suffer from packet collisions in dense maritime choke points ([Chapter 30](ch30-network-loading-packet-loss.md)).

To establish comprehensive Maritime Domain Awareness (**MDA**), coast guards, fisheries protection agencies, defense forces, and ocean analysts integrate AIS with external tracking layers. These alternate methods divide into two broad categories:
- **Cooperative closed systems:** Vessel-carried transponders that report position over private, encrypted, or state-controlled satellite and cellular channels.
- **Non-cooperative detection systems:** Remote sensors (radar, optical, SAR, RF direction finders, and acoustic hydrophones) that detect, locate, and characterize vessels without requiring their active cooperation or consent.

```
+--------------------------------------------------------------------------------------------------+
|                            THE MARITIME TRACKING SPECTRUM                                        |
+--------------------------------------------------------------------------------------------------+
|                                                                                                  |
|   COOPERATIVE SYSTEMS                               NON-COOPERATIVE SYSTEMS                      |
|                                                                                                  |
|   +-----------------------+                         +-----------------------+                    |
|   | Public Broadcast      |                         | Active Sensors        |                    |
|   | - AIS (Class A, B)    |                         | - Coastal X/S Radar   |                    |
|   | - VDES Terrestrial/Sat|                         | - HF Surface Wave OTH |                    |
|   +-----------------------+                         | - Spaceborne SAR      |                    |
|               |                                     +-----------------------+                    |
|               v                                                 |                                |
|   +-----------------------+                                     v                                |
|   | Closed Telemetry      |                         +-----------------------+                    |
|   | - LRIT (SOLAS V/19-1) |                         | Passive Sensors       |                    |
|   | - VMS (Fisheries)     |                         | - Spaceborne RF Geo   |                    |
|   | - WMO VOS Weather Rep |                         | - EO / Optical Sats   |                    |
|   | - Satcom / Inmarsat   |                         | - Acoustic Hydrophones|                    |
|   +-----------------------+                         +-----------------------+                    |
|               |                                                 |                                |
|               +-----------------------+-------------------------+                                |
|                                       |                                                          |
|                                       v                                                          |
|                         [ MULTI-SENSOR TRACK FUSION ]                                            |
|                           - Spatial-Temporal Gating                                              |
|                           - Kinematic & Identity Association                                     |
|                           - Anomaly & Dark-Fleet Flagging                                        |
+--------------------------------------------------------------------------------------------------+
```

---

## 66.2 Closed cooperative satellite telemetry: VMS and LRIT

Unlike AIS, which broadcasts unencrypted packets omnidirectionally to anyone with an antenna, closed cooperative systems transmit position reports point-to-point over commercial satellite links directly to authorized government data centers.

### 66.2.1 Vessel Monitoring Systems (VMS)

The Vessel Monitoring System (**VMS**) is a regulatory framework mandated by national fisheries authorities and Regional Fisheries Management Organizations (**RFMOs**) to monitor commercial fishing fleets. In the United States, the National Oceanic and Atmospheric Administration (**NOAA**) National Marine Fisheries Service (**NMFS**) mandates type-approved VMS units under 50 CFR Part 600. In Europe, Council Regulation (EC) No 1224/2009 Article 9 requires all Community fishing vessels exceeding 12 meters in length overall (and modernized under Regulation (EU) 2023/2842) to operate satellite-tracking devices.

A shipboard VMS terminal—often referred to as an Automatic Location Communicator (**ALC**) or Mobile Transceiver Unit (**MTU**)—integrates an internal GNSS receiver with a secure satellite transmitter. Common transceivers include Inmarsat-C terminals, Iridium satellite modems (such as the Iridium 9602/9603 Short Burst Data modems), and Thuraya marine terminals.

Operational mechanics of VMS:
- **Reporting cadence:** Transmissions occur at fixed intervals, typically once every 1 to 2 hours in standard regimes, increasing automatically to 15 or 30 minutes when crossing into marine protected areas (**MPAs**) or regulated fishing zones.
- **Polling and geofencing:** Fisheries Monitoring Centres (**FMCs**) can remotely "poll" the ALC on demand or upload dynamic geofence boundaries that trigger burst transmissions upon boundary entry or exit.
- **Tamper resistance:** Regulatory type-approval requires tamper-evident enclosures, backup batteries, and automatic notification alerts sent to the FMC if external DC shipboard power is severed or antenna cables are disconnected.
- **Data confidentiality:** VMS data is treated as strictly proprietary commercial information or state intelligence. Regulators protect VMS feeds to prevent competitors from stealing proprietary fishing spots. Unlike AIS, VMS positions are not broadcast over VHF and are inaccessible to public aggregators or commercial vessels, except where progressive nations (such as Peru, Indonesia, Chile, and Ecuador) have voluntarily partnered with Global Fishing Watch to publish national VMS registries.

### 66.2.2 Long-Range Identification and Tracking (LRIT)

Following the maritime security enhancements enacted after September 11, 2001, the International Maritime Organization adopted Resolution MSC.202(81) on May 19, 2006. This resolution introduced Regulation 19-1 into SOLAS Chapter V, establishing the **LRIT** system, which formally entered into force on January 1, 2008.

LRIT applies internationally to:
- Passenger ships, including high-speed craft, on international voyages.
- Cargo ships of 300 gross tonnage and upwards on international voyages.
- Mobile offshore drilling units (**MODUs**).

Unlike AIS, which was developed under the technical auspices of ITU-R and IEC for tactical collision avoidance, LRIT is an administrative security and domain awareness architecture governed by IMO Resolution MSC.263(84) as revised.

Technical architecture of LRIT:
- **Shipboard equipment:** Ships transmit automated position reports using existing satellite terminals—overwhelmingly GMDSS-compliant Inmarsat-C or Iridium satcom installations. The terminal automatically transmits the ship's identity, latitude, longitude, and UTC timestamp.
- **Reporting rate:** The standard default interval is 6 hours (four reports per day). However, an authorized administration can instruct the terminal remotely to increase its reporting frequency up to once every 15 minutes during security incidents or search and rescue operations.
- **Data flow:** Position reports travel via satellite to an Application Service Provider (**ASP**), which validates the transmission and routes it to a National, Regional, or Cooperative LRIT Data Centre (**DC**).
- **The International LRIT Data Exchange (IDE):** Operating under IMO governance, the IDE acts as a central clearinghouse. When a port state or coastal state requests tracking information for approaching traffic, the IDE validates the request against the LRIT Business Rules and coordinates data delivery.
- **Entitlement model:** SOLAS Regulation V/19-1 defines strict access rights:
  - **Flag states** may receive tracking reports from ships flying their flag anywhere on Earth.
  - **Port states** may receive reports from foreign ships that have declared intention to enter their ports, regardless of distance.
  - **Coastal states** may receive reports from foreign vessels transiting within a distance not exceeding 1,000 nautical miles (1,852 km) of their baseline, provided the vessel is not within another state's internal waters.

Because LRIT operates over commercial satellite uplinks directly to state data centers, ships cannot see other ships' LRIT transmissions. It provides no tactical collision avoidance utility, but it gives national governments a confidential, planetary-scale surveillance picture that functions independently of whether a ship is broadcasting AIS.

> **Definitions that bite.**
> **AIS vs. LRIT vs. VMS:**
> - **AIS:** Broadcast, unencrypted, public, autonomous VHF link. Range is line-of-sight (~20–30 nmi surface, ~2,500 km footprint to LEO satellites). High cadence (2 s to 3 min). Open to anyone with an antenna.
> - **LRIT:** Point-to-point, confidential, state-governed satellite link. Global coverage. Coarse cadence (typically 6-hourly). Accessible only to SOLAS contracting governments under strict jurisdictional rules. Mandated for commercial ships $\ge 300\text{ GT}$.
> - **VMS:** Point-to-point, proprietary/confidential fisheries management link via satellite or cellular. Regional or national coverage. Medium cadence (15 min to 2 hours). Mandated for commercial fishing vessels by fisheries authorities.

---

## 66.3 Ancillary telemetry: VOS weather reports and satcom metadata

In addition to formal statutory tracking systems, commercial ships routinely generate ancillary digital footprints across meteorological and telecommunications networks.

### 66.3.1 Voluntary Observing Ships (VOS)

Under the World Meteorological Organization (**WMO**) and the Intergovernmental Oceanographic Commission (**IOC**), the Voluntary Observing Ship (**VOS**) scheme coordinates commercial merchant vessels to record and transmit marine surface meteorological observations. Governed by WMO-No. 47 (*International List of Selected, Supplementary and Auxiliary Ships*), participating vessels transmit coded synoptic weather reports (traditionally in WMO FM 13-XIV SHIP code, and increasingly in BUFR table-driven formats).

Each observation contains:
- Vessel radio call sign or masked identification string.
- Precise latitude, longitude, and observation time.
- Barometric pressure, sea surface temperature, air temperature, wind speed, wind direction, wave height, and swell characteristics.

These reports are transmitted at standard synoptic hours (00:00, 06:00, 12:00, and 18:00 UTC) over Inmarsat-C, email, or web interfaces to National Meteorological Services (such as NOAA in the United States or the UK Met Office). Because these observations are distributed across the WMO Global Telecommunication System (**GTS**) to feed global numerical weather models, they provide an independent, unclassified record of vessel location across remote oceanic basins.

### 66.3.2 Satellite communications metadata

Modern merchant vessels maintain continuous IP connectivity via satellite communications, including Inmarsat FleetBroadband, Iridium Certus, high-throughput geostationary VSAT systems (KVH, Marlink, Speedcast), and LEO broadband constellations (Starlink Maritime, Eutelsat OneWeb) ([Chapter 67](ch67-mobile-phones-at-sea.md)).

While payloads are encrypted, satellite transceivers continuously exchange radio-frequency link maintenance telemetry with satellite ground stations:
- **Spot-beam identifiers:** In multi-beam satellite networks, a terminal's active IP session is assigned to a specific geographic spot beam. Even without GNSS coordinates, a ship's presence is localized to the spot beam's footprint (typically 200 km to 800 km diameter).
- **Timing advance and round-trip delay:** Space-ground synchronization protocols measure the propagation delay between satellite and terminal. In systems with known satellite ephemeris, round-trip time (**RTT**) defines an isochronous range ring on the Earth's surface.
- **Doppler shift:** In LEO communications networks, terminal frequency offsets provide Doppler frequency curves that constrain the terminal's surface velocity and latitude.

While satcom providers protect commercial metadata under subscriber privacy agreements, telecommunications metadata can be subpoenaed in maritime investigations, casualty inquiries, and sanctions enforcement actions.

---

## 66.4 Active non-cooperative tracking: coastal radar, HFSWR, and spaceborne SAR

When a vessel operates completely dark—transmitting neither AIS, VMS, nor radio communications—surveillance must rely on active electromagnetic sensors that bounce radio waves off the vessel's hull.

### 66.4.1 Coastal microwave radar and VTS

Coastal Vessel Traffic Services (**VTS**) systems rely on shore-based marine radars as their primary non-cooperative tactical sensor ([Chapter 04](ch04-vts-and-ports.md)). These installations use pulsed or frequency-modulated continuous-wave (**FMCW**) radar operating in marine X-band (9.2–9.5 GHz, $\lambda \approx 3.2\text{ cm}$) or S-band (2.9–3.1 GHz, $\lambda \approx 10\text{ cm}$) per IEC 62388 and IMO Resolution MSC.192(79).

Microwave radar characteristics:
- **Coverage:** Strictly line-of-sight. For a radar scanner elevated at height $h_{\text{radar}}$ and a vessel target with superstructure height $h_{\text{target}}$, the maximum detection range $R_{\text{max}}$ is governed by 4/3-Earth atmospheric refraction:
  $$R_{\text{max}} \approx 4.12 \left(\sqrt{h_{\text{radar}}} + \sqrt{h_{\text{target}}}\right) \text{ km}$$
  A radar atop a 100-meter headland tracking a tanker with a 25-meter superstructure achieves a theoretical horizon of approximately $61.8\text{ km}$ ($33.4\text{ nmi}$).
- **Target tracking:** Automated Radar Plotting Aids (**ARPA**) and modern VTS tracking software extract radar target plots and execute track initiation, Kalman filtering, and velocity vector calculation.
- **Target association:** Radar returns provide spatial position and kinematic velocity, but carry no intrinsic vessel identity. VTS systems continuously cross-reference radar tracks against decoded AIS targets. When an active radar track has no corresponding AIS position within a predefined kinematic correlation gate, the VTS software generates an "Uncorrelated Radar Target" or "Dark Target" alarm.

### 66.4.2 High-Frequency Surface-Wave Radar (HFSWR)

Standard microwave radar cannot bend over the physical curvature of the Earth. To track ships far beyond the horizon without deploying aircraft or satellites, coastal nations deploy **High-Frequency Surface-Wave Radar** (**HFSWR**).

HFSWR exploits vertical polarization in the High Frequency (**HF**) band (3–30 MHz, $\lambda \approx 10\text{–}100\text{ m}$). At these frequencies, electromagnetic waves interact with the conductive saline ocean surface, establishing a surface wave that clings to the Earth's curvature.
- **Operational range:** HFSWR arrays achieve continuous coastal surveillance out to 150 nmi to 200 nmi (278 km to 370 km) from shore.
- **Resolution:** Because HF wavelengths are large, spatial resolution is coarse compared to microwave radar. Azimuthal resolution is constrained by antenna array aperture length, typically yielding range cells of 1 km to 3 km and bearing uncertainties of $1^\circ$ to $2^\circ$.
- **Detection physics:** HFSWR target detection relies on Doppler processing to isolate vessel return echoes from the massive background Bragg scattering produced by ocean surface gravity waves. Target echoes appear as Doppler peaks shifted away from the first-order sea clutter peaks.
- **Deployment:** HFSWR networks operate along critical maritime frontiers, including Canada's Atlantic coast, the German Bight (WERA radar system), the Mediterranean coast, and the South China Sea.

### 66.4.3 Spaceborne Synthetic Aperture Radar (SAR)

For global, all-weather, day-and-night tracking across remote oceans, spaceborne **Synthetic Aperture Radar** (**SAR**) is the preeminent sensor. Spaceborne SAR satellites emit coherent microwave pulses down to Earth and measure the amplitude and phase of backscattered radiation.

Prominent operational SAR constellations include:
- **C-band ($\sim 5.4\text{ GHz}$):** European Space Agency Copernicus Sentinel-1A/1C; Canadian Space Agency RADARSAT-2 and RADARSAT Constellation Mission (**RCM**).
- **X-band ($\sim 9.6\text{ GHz}$):** Airbus TerraSAR-X / TanDEM-X; COSMO-SkyMed; ICEYE (commercial micro-satellite constellation); Capella Space.
- **L-band ($\sim 1.27\text{ GHz}$):** JAXA ALOS-2 / ALOS-4.

```
+-----------------------------------------------------------------------------+
|                     SPACEBORNE SAR SHIP DETECTION                           |
+-----------------------------------------------------------------------------+
|                                                                             |
|            [ SAR SATELLITE (e.g., Sentinel-1) ]                             |
|                  \                       ^                                  |
|                   \ Active Radar Pulse   | Specular Ocean Backscatter       |
|                    \                     | & Double-Bounce Echo             |
|                     v                    |                                  |
|     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~       |
|     Ocean Surface: Roughness causes distributed, low-to-medium backscatter  |
|                                                                             |
|                            [ VESSEL HULL ]                                  |
|                             |___|____/                                      |
|                             \_______/                                       |
|                                                                             |
|     Ship Reflection Mechanics:                                              |
|     1. Corner-Reflector Effect: Superstructure & deck create double-bounce  |
|        dielectric reflections, appearing as extremely bright pixels.        |
|     2. Ship Wake: Kelvin wake and turbulent centerline track disturb surface|
|        capillary waves, visible as dark or bright linear scars.             |
|     3. Azimuth Doppler Shift: Target radial velocity v_r causes apparent    |
|        displacement Delta_x along the flight path:                          |
|             Delta_x = (R * v_r) / V_sat                                     |
+-----------------------------------------------------------------------------+
```

Vessel detection on SAR imagery relies on distinct physical signatures:
1. **Bright point backscatter:** Steel hulls and angular superstructure corners act as dihedral and trihedral corner reflectors. They reflect microwave energy directly back toward the satellite receiver, creating brilliant clusters of high-intensity pixels that contrast sharply against the darker background of surrounding sea clutter.
2. **Constant False Alarm Rate (CFAR) algorithms:** Automated detection engines run adaptive CFAR filters (such as Cell-Averaging CFAR, Order-Statistic CFAR, or deep learning convolutional neural networks) across the image to identify ship candidates while suppressing ocean clutter caused by wind waves.
3. **Ship wake analysis:** Fast-moving vessels create hydrodynamic Kelvin wakes, turbulent hull scars, and internal wave patterns. In addition to confirming vessel presence, wake angles allow analysts to determine speed and heading.
4. **Azimuth Doppler displacement:** Because SAR synthetic aperture synthesis depends on precise Doppler phase histories, a moving target with a non-zero radial velocity $v_r$ relative to the satellite experiences an azimuth displacement $\Delta x_{\text{az}}$ in the processed image:
   $$\Delta x_{\text{az}} = \frac{R \cdot v_r}{V_{\text{sat}}}$$
   where $R$ is slant range and $V_{\text{sat}}$ is satellite orbital velocity. A ship steaming at 15 knots towards a SAR sensor can appear displaced several hundred meters away from its hydrodynamic wake. Correcting for this Doppler shift is essential when matching SAR detections to broadcast AIS tracks.

In a milestone study published in *Nature*, Paolo et al. (2024) processed 2.0 petabytes of Sentinel-1 SAR imagery collected globally between 2017 and 2021. By matching SAR detections against global AIS databases, they revealed that approximately 72% to 76% of industrial fishing vessels worldwide were "dark"—completely unrepresented in public AIS feeds.

---

## 66.5 Passive non-cooperative tracking: optical, RF geolocation, and acoustics

Passive surveillance systems detect vessels by intercepting the electromagnetic or acoustic energy they emit or reflect.

### 66.5.1 High-resolution spaceborne optical sensors

Commercial Earth observation constellations provide high-resolution multispectral optical imagery capable of resolving fine physical details of ships at sea.
- **High-resolution providers:** Maxar Technologies (WorldView series, ground sampling distance [GSD] down to 30 cm), Airbus Defense & Space (Pleiades Neo, 30 cm GSD), and Planet Labs (SkySat, 50 cm GSD).
- **PlanetScope daily monitoring:** Planet operates over 130 PlanetScope "Dove" CubeSats in Sun-synchronous orbits, imaging the entire global landmass and coastal waters daily at 3-meter optical resolution.
- **Nighttime visible tracking (VIIRS):** The Day/Night Band (**DNB**) on the Visible Infrared Imaging Radiometer Suite aboard NOAA/NASA Suomi-NPP and NOAA-20 satellites detects low levels of visible light at night. VIIRS DNB reliably locates industrial fishing fleets that use high-intensity halogen or LED lamps to attract catch, such as squid jiggers operating around the Galápagos and Falkland Islands.

Optical limitations:
- Severe degradation from cloud cover, fog, and atmospheric haze.
- Daytime-only operation (with the exception of VIIRS nocturnal light tracking).
- Narrow swath widths for sub-meter sensors (typically 10 km to 20 km), requiring precise pre-tasking based on cueing from other surveillance layers.

### 66.5.2 Spaceborne RF emitter geolocation

Even when ships turn off AIS transponders to evade tracking, they routinely broadcast on other radio frequencies for navigation and communication:
- **Marine radar pulses:** Marine X-band (9.4 GHz) and S-band (3.0 GHz) navigation radars.
- **Bridge-to-bridge VHF voice:** Channel 16 (156.800 MHz) and tactical VHF voice channels.
- **Satellite communications uplinks:** Inmarsat, Iridium, and satellite phone transmissions.
- **Emergency and search-and-rescue beacons:** Emergency Position-Indicating Radiobeacons (**EPIRBs**) operating on 406.0–406.1 MHz.

Commercial constellations operated by **HawkEye 360** and **Unseenlabs** deploy microsatellites equipped with software-defined radio payloads to intercept and geolocate these emissions.
- **Cluster TDOA/FDOA:** HawkEye 360 flies clusters of three formation-flying satellites. By cross-correlating the exact time and frequency of arrival of a single RF burst across all three satellites, the ground system computes **Time Difference of Arrival** (**TDOA**) hyperbolae and **Frequency Difference of Arrival** (**FDOA**) Doppler curves ([Chapter 35](ch35-direction-finding-geolocation.md)). The intersection yields a precise geographic fix independently of any GNSS telemetry.
- **Monosatellite geolocation:** Unseenlabs operates a constellation of proprietary CubeSats (the Breizh Reconnaissance Orbiter series) using proprietary single-satellite RF localization techniques.

> **Case file.**
> **The *Romina* (2020):** In mid-2020, the Iranian-flagged Suezmax crude oil tanker *Romina* (IMO 9546057) departed Iran carrying Iranian crude. Upon approaching the Suez Canal and entering the eastern Mediterranean, the vessel disabled its Class A AIS transponder to conceal its voyage to sanctioned terminals in Syria. In October 2020, HawkEye 360 detected multiple tactical VHF Channel 16 transmissions in the waters off Baniyas, Syria. HawkEye 360's satellite cluster geolocated the RF emitter to an anchorage 10 km off the Baniyas oil terminal. Commercial high-resolution optical imagery tasking subsequently confirmed the physical presence of the tanker at the exact geolocated coordinates, engaged in unmooring and offloading crude. This operation demonstrated how spaceborne RF geolocation unmasks dark vessels during deliberate AIS blackouts.

```
+-----------------------------------------------------------------------------+
|               SPACEBORNE RF TDOA / FDOA GEOLOCATION                         |
+-----------------------------------------------------------------------------+
|                                                                             |
|      [ Satellite 1 ]          [ Satellite 2 ]          [ Satellite 3 ]      |
|             \                        |                        /             |
|              \ tau_1                 | tau_2                 / tau_3        |
|               \                      |                      /               |
|                \                     v                     /                |
|                 +---------------+----+--------------------+                 |
|                                 |                                           |
|     1. TDOA Hyperbolae:         v                                           |
|        Delta_tau_12 = tau_1 - tau_2  --> Surface Hyperbola H_12             |
|        Delta_tau_23 = tau_2 - tau_3  --> Surface Hyperbola H_23             |
|                                                                             |
|     2. FDOA Curves:                                                         |
|        Delta_f_12 = f_1 - f_2        --> Iso-Doppler Contours               |
|                                                                             |
|     3. Solution:                                                            |
|        Fix = H_12 (intersection) H_23 (intersection) Earth Geoid           |
|                                                                             |
|                                 |                                           |
|                                 v                                           |
|                       * Geolocation Fix *                                   |
|                        (Uncooperative Ship)                                 |
+-----------------------------------------------------------------------------+
```

### 66.5.3 Underwater acoustic tracking

Subsurface tracking systems monitor vessel acoustic emissions:
- **Sound sources:** Ship propulsion systems, diesel generators, propeller cavitation, and hydrodynamic hull displacement generate loud, low-frequency acoustic energy (typically 5 Hz to 1,000 Hz).
- **Hydrophone networks:** Fixed acoustic arrays, including the U.S. Navy's historic Sound Surveillance System (**SOSUS**), modern Integrated Undersea Surveillance System (**IUSS**), and scientific cabled observatories (such as Ocean Networks Canada), detect and track surface ships across entire ocean basins.
- **Acoustic signature classification:** Automated signal processing extracts blade-rate frequencies and cavitation profiles. By matching acoustic signatures against reference intelligence libraries, acoustic analysts can identify specific vessel classes and propulsion configurations without visual or radar contact.

---

## 66.6 Administrative, intelligence, and port state tracking

Not all ship tracking relies on electromagnetic sensors. Massive administrative, commercial, and regulatory databases track vessels across physical ports of call.

### 66.6.1 Port State Control and customs manifests

Under international maritime law, sovereign coastal states exercise Port State Control (**PSC**) over foreign vessels calling at their ports. Regional PSC regimes—including the Paris Memorandum of Understanding (**Paris MoU**) in Europe and the Tokyo MoU in the Asia-Pacific—maintain shared inspection databases (such as THETIS, operated by EMSA).

These administrative systems record:
- Advance Notices of Arrival (**NOA**): SOLAS and national regulations (e.g., 33 CFR Part 160 in the United States) require commercial vessels to submit electronic NOA manifests 96 hours prior to entering a port. Manifests detail cargo, crew lists, hazardous materials, and previous ports of call.
- Customs and bill of lading databases: Global trade intelligence platforms (such as ImportGenius, Panjiva, and Kpler) process customs declarations, tracking cargo transfers, charterers, and consignees.

### 66.6.2 Equasis and S&P Global maritime registries

The definitive registry for global vessel identity is maintained by S&P Global Maritime (formerly IHS Markit and Lloyd's Register of Shipping), which manages the IMO Ship Identification Number Scheme on behalf of the IMO ([Chapter 13](ch13-mmsi-deep-dive.md)).

Complementing commercial intelligence, **Equasis** is a public, non-commercial maritime database established by the European Commission and the French Maritime Administration. Equasis consolidates safety audits, classification society survey records, P&I club coverage, flag changes, registered ownership structures, and PSC detention histories into a unified vessel record. Even when a ship changes its name, MMSI, or flag state, its seven-digit IMO number remains unalterable throughout its life cycle.

---

## 66.7 Multi-sensor fusion and the unmasking of dark fleets

No single tracking system provides complete, tamper-proof maritime situational awareness. Operational maritime intelligence centers combine all available surveillance layers into a fused Common Operating Picture (**COP**).

```
+-----------------------------------------------------------------------------------+
|                        MULTI-SENSOR TRACK FUSION PIPELINE                         |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [ Cooperative Broadcast ]   [ Cooperative Closed ]   [ Non-Cooperative Remote ]  |
|    - Terrestrial AIS           - Flag State LRIT        - Spaceborne SAR (S1)     |
|    - Satellite AIS             - Fisheries VMS          - Spaceborne Optical      |
|    - VDES Feeds                - WMO VOS Weather        - RF TDOA/FDOA (HawkEye)  |
|          |                           |                  - Coastal Radar (VTS)     |
|          |                           |                            |               |
|          +---------------------------+----------------------------+               |
|                                      |                                            |
|                                      v                                            |
|                      [ SPATIAL-TEMPORAL GATING ]                                  |
|                        - Mahalanobis Distance Filter                              |
|                        - Kinematic Speed-of-Advance Gating                        |
|                                      |                                            |
|                                      v                                            |
|                      [ TRACK HYPOTHESIS RESOLUTION ]                              |
|                        - Global Nearest Neighbor / MHT                            |
|                        - Identity Disambiguation (MMSI/IMO)                       |
|                                      |                                            |
|                 +--------------------+--------------------+                       |
|                 |                                         |                       |
|                 v                                         v                       |
|       [ CORRELATED TRACK ]                      [ UNCORRELATED CONTACT ]          |
|     AIS validated by SAR/RF                   "Dark Vessel" Anomaly               |
|     Multi-sensor confidence: HIGH             Trigger: Satellite Cueing / Patrol  |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

### 66.7.1 Spatial-temporal gating and track association

The core algorithmic challenge in multi-sensor fusion is determining whether a non-cooperative detection (a SAR bright point or an RF geolocation ellipse) matches an existing AIS track.

Let $\mathbf{x}_{\text{ais}}(t) = [x_{\text{ais}}, y_{\text{ais}}, \dot{x}_{\text{ais}}, \dot{y}_{\text{ais}}]^T$ represent the state vector of an AIS track projected into local East-North-Up (**ENU**) Cartesian coordinates at time $t$. If an external sensor records a detection at coordinates $\mathbf{z}_{\text{det}} = [x_{\text{det}}, y_{\text{det}}]^T$ at time $t_{\text{det}}$, the fusion engine projects the AIS track to time $t_{\text{det}}$ using kinematic extrapolation:
$$\hat{\mathbf{z}}_{\text{ais}}(t_{\text{det}}) = \mathbf{H} \mathbf{\Phi}(t_{\text{det}} - t) \mathbf{x}_{\text{ais}}(t)$$
where $\mathbf{\Phi}$ is the state transition matrix and $\mathbf{H}$ is the measurement observation matrix.

The innovation vector $\mathbf{y}$ and innovation covariance $\mathbf{S}$ are:
$$\mathbf{y} = \mathbf{z}_{\text{det}} - \hat{\mathbf{z}}_{\text{ais}}(t_{\text{det}})$$
$$\mathbf{S} = \mathbf{H} \mathbf{P}(t_{\text{det}}) \mathbf{H}^T + \mathbf{R}_{\text{det}}$$
where $\mathbf{P}(t_{\text{det}})$ is the extrapolated track covariance and $\mathbf{R}_{\text{det}}$ is the measurement error covariance matrix of the external sensor (e.g., the $90\%$ confidence ellipse of an RF fix or the spatial resolution cell of a SAR image).

The statistical association test calculates the squared **Mahalanobis distance** $d_M^2$:
$$d_M^2 = \mathbf{y}^T \mathbf{S}^{-1} \mathbf{y}$$

Under the hypothesis that the detection belongs to the AIS track, $d_M^2$ follows a chi-squared distribution $\chi_m^2$ with $m=2$ degrees of freedom. A detection is gated and considered a candidate match if $d_M^2 \le \gamma_{\text{gate}}$, where $\gamma_{\text{gate}}$ is selected from chi-squared distribution tables (e.g., $\gamma_{\text{gate}} = 9.21$ for a $99\%$ confidence gate). For dense harbors with multiple candidate targets, algorithms such as Multiple Hypothesis Tracking (**MHT**) or Joint Probabilistic Data Association Filters (**JPDAF**) resolve ambiguities across successive observation frames.

> **Try it.**
> Compute the Mahalanobis distance between an extrapolated AIS track and an unassociated SAR observation using Python and NumPy:
> ```python
> import numpy as np
>
> # 1. Extrapolated AIS position [East, North] in meters
> pos_ais = np.array([1000.0, 2500.0])
>
> # 2. Spaceborne SAR detection position [East, North]
> pos_sar = np.array([1120.0, 2420.0])
>
> # 3. Spatial innovation (difference)
> innovation = pos_sar - pos_ais  # [120 m, -80 m]
>
> # 4. Combined error covariance: AIS drift (50 m) + SAR resolution (70 m)
> S = np.diag([50.0**2, 70.0**2])
>
> # 5. Mahalanobis distance calculation
> d_squared = float(innovation.T @ np.linalg.inv(S) @ innovation)
> d_mahalanobis = float(np.sqrt(d_squared))
>
> print(f"Innovation: {innovation} meters")
> print(f"Mahalanobis d^2: {d_squared:.3f}")
> print(f"Candidate match (gate < 9.21): {d_squared <= 9.21}")
> ```
> Expected output:
> ```text
> Innovation: [ 120.  -80.] meters
> Mahalanobis d^2: 7.066
> Candidate match (gate < 9.21): True
> ```

---

## Then & now

- `⟨H⟩` **1912:** Following the loss of RMS *Titanic*, maritime radio telegraphy was mandated under the 1914 International Convention for the Safety of Life at Sea (**SOLAS**), relying on manual Morse code distress watches on 500 kHz.
- `⟨H⟩` **1940s:** Microwave cavity magnetron radar was deployed on combat ships, introducing non-cooperative electromagnetic surface detection for naval warfare and coastal harbor defense.
- `⟨+⟩` **1970s:** The U.S. Navy operationalized the Sound Surveillance System (**SOSUS**), establishing passive basin-scale ocean acoustic tracking of surface ships and submarines (Wenz 1962).
- `⟨+⟩` **1990s:** Fisheries authorities introduced satellite-based Vessel Monitoring Systems (**VMS**), utilizing Inmarsat-C polling to enforce national exclusive economic zone boundaries (FAO 1998).
- `⟨+⟩` **2002:** IMO SOLAS Regulation V/19 came into force, mandating the Automatic Identification System (**AIS**) on all commercial vessels $\ge 300\text{ GT}$ on international voyages.
- `⟨+⟩` **2006:** IMO Resolution MSC.202(81) adopted SOLAS Regulation V/19-1, creating the Long-Range Identification and Tracking (**LRIT**) system for confidential 6-hourly global satellite tracking.
- `⟨+⟩` **2008:** The European Space Agency and national space agencies launched the first spaceborne AIS reception experiments, pioneering global LEO satellite tracking of commercial fleets.
- `⟨+⟩` **2014:** The European Space Agency launched Copernicus Sentinel-1A, initiating systematic, free, planetary-scale C-band Synthetic Aperture Radar (**SAR**) surface surveillance.
- `⟨+⟩` **2018:** HawkEye 360 launched its Pathfinder satellite cluster on Spaceflight SSO-A, pioneering commercial spaceborne RF emitter TDOA/FDOA geolocation of non-cooperative ships.
- `⟨+⟩` **2024:** Global Fishing Watch published a planetary analysis in *Nature* (Paolo et al. 2024), fusing Sentinel-1 SAR imagery with global AIS data to prove that $\sim 75\%$ of commercial fishing vessels operate completely dark.

---

## Validation, uncertainty & data quality

Fusing disparate maritime tracking systems requires reconciling drastically different spatial, temporal, and legal error characteristics.

```
+---------------------------------------------------------------------------------------------------+
|                            TRACKING SOURCE CHARACTERISTICS                                        |
+---------------------------------------------------------------------------------------------------+
| Tracking System   | Cooperation | Update Interval   | Spatial Accuracy     | Global Coverage      |
+-------------------+-------------+-------------------+----------------------+----------------------+
| Terrestrial AIS   | Active      | 2 s to 3 min      | 5 m to 15 m (GNSS)   | Coastal (~30 nmi)    |
| Satellite AIS     | Active      | 15 min to hours   | 5 m to 15 m (GNSS)   | Global (footprint)   |
| LRIT (SOLAS)      | Active      | 6 hours (typical) | 5 m to 30 m (GNSS)   | Global (satellite)   |
| Fisheries VMS     | Active      | 1 to 2 hours      | 5 m to 30 m (GNSS)   | Regional / EEZ       |
| Coastal Radar     | Passive     | 1 s to 3 s        | 10 m to 100 m        | Coastal (~20–35 nmi) |
| HFSWR (OTH)       | Passive     | Minutes           | 1 km to 3 km         | Coastal (up to 200 nmi)|
| Spaceborne SAR    | Passive     | Days (revisit)    | 5 m to 20 m (pixel)  | Global (sampled)     |
| Commercial RF Geo | Passive     | Hours / On-demand | 500 m to 5 km (TDOA) | Global (constellation)|
| High-Res Optical  | Passive     | Days / Tasked     | 0.3 m to 3 m         | Targeted swathes     |
+---------------------------------------------------------------------------------------------------+
```

### Concrete validation procedures and error propagation

When evaluating non-AIS tracking data, analysts must execute rigorous error validation steps:

1. **Latency and temporal misalignment:** LRIT and VMS telemetry arrives with multi-hour reporting latencies. Projecting a 6-hour-old LRIT position forward for a ship steaming at 20 knots creates an uncertainty radius of 120 nautical miles (222 km). Extrapolated tracks must maintain an expanding circular error probable (**CEP**) boundary:
   $$R_{\text{uncertainty}}(t) = R_{\text{GNSS}} + v_{\text{max}} \cdot (t - t_{\text{last}})$$
2. **Azimuth Doppler shift in SAR:** As established in §66.4.3, target radial velocity shifts SAR detections in azimuth. A vessel moving at unknown velocity cannot be localized solely by its SAR bright point without wake analysis. If the wake is invisible (due to calm seas or slow speed), the azimuth uncertainty along the satellite flight path equals:
   $$\sigma_{\text{az}} = \frac{R \cdot \sigma_{v_r}}{V_{\text{sat}}}$$
   For a LEO SAR operating at $V_{\text{sat}} \approx 7,500\text{ m/s}$ and $R \approx 800\text{ km}$, a radial velocity uncertainty of $\pm 5\text{ m/s}$ ($\approx 9.7\text{ kn}$) produces an along-track position uncertainty of $\pm 533\text{ meters}$.
3. **Geometric Dilution of Precision (GDOP) in RF geolocation:** In spaceborne TDOA/FDOA geolocation, satellite cluster geometry dictates accuracy. When an emitter lies near the baseline vector between two satellites, the resulting TDOA hyperbolae become nearly parallel, causing the error ellipse to stretch into an elongated line tens of kilometers long. Analysts must discard or de-weight RF fixes with GDOP values exceeding 5.0.

> **Worked example.**
> A coastal surveillance center detects a non-cooperative radar contact $40\text{ nmi}$ offshore. The radar provides range $r = 74.08\text{ km} \pm 50\text{ m}$ ($1\sigma$) and azimuth $\theta = 110.0^\circ \pm 0.2^\circ$ ($1\sigma$). Concurrently, an AIS message received 180 seconds ago reported a container ship at range $73.50\text{ km}$, bearing $110.4^\circ$, heading $180^\circ$, steaming at $SOG = 18\text{ kn}$ ($9.26\text{ m/s}$).
> 
> *Step 1: Extrapolate AIS position.* Over $\Delta t = 180\text{ s}$, the ship travels along heading $180^\circ$ (due South) by distance:
> $$\Delta y = 9.26\text{ m/s} \times 180\text{ s} = 1,666.8\text{ m} \approx 1.67\text{ km}$$
> The projected AIS position in local ENU coordinates ($x = r \sin\theta, y = r \cos\theta$) moves South by $1.67\text{ km}$.
> 
> *Step 2: Calculate radar position error.*
> Azimuth uncertainty in linear distance:
> $$\sigma_{\text{cross}} = r \cdot \Delta\theta_{\text{rad}} = 74,080\text{ m} \times \left(0.2 \times \frac{\pi}{180}\right) = 74,080 \times 0.00349 = 258.6\text{ m}$$
> Range uncertainty: $\sigma_{\text{range}} = 50\text{ m}$.
> 
> *Step 3: Evaluate association gate.*
> The Euclidean separation between the extrapolated AIS position and the fresh radar contact is calculated. If the separation is $280\text{ m}$, and the total combined $1\sigma$ spatial uncertainty is:
> $$\sigma_{\text{total}} = \sqrt{\sigma_{\text{cross}}^2 + \sigma_{\text{range}}^2 + \sigma_{\text{extrap}}^2} = \sqrt{258.6^2 + 50^2 + 100^2} \approx 281.7\text{ m}$$
> The normalized distance is $d = 280 / 281.7 \approx 0.99\sigma$. The radar contact is positively associated with the container ship, confirming the vessel is broadcasting valid AIS.

---

## Software

### Open source

- **`sar-ship-detect` / OpenSAR:** Open-source Python and C++ implementations of Constant False Alarm Rate (**CFAR**) detectors (CA-CFAR, OS-CFAR) for Sentinel-1 GRD SAR imagery. Caveat: High false-alarm rates over choppy open water and near coastal land boundaries without high-resolution masking.
- **`pyephem` / `skyfield`:** Open-source Python orbital mechanics libraries for propagating satellite Two-Line Element (**TLE**) ephemerides. Useful for calculating satellite pass times and predicting SAR and optical coverage footprints. Caveat: Requires daily TLE updates from Space-Track to avoid orbital drift errors.
- **MovingPandas:** Trajectory analysis library based on GeoPandas ([Chapter 45](ch45-processing-software.md)) used to interpolate AIS, VMS, and radar point series into continuous temporal trajectories. Caveat: Memory-intensive when interpolating dense multi-day vessel datasets.

### Free but closed

- **ESA SNAP (Sentinel Application Platform):** The European Space Agency's desktop suite for processing Sentinel-1 SAR and Sentinel-2 optical data. Includes dedicated calibration, speckle filtering, and ship detection tools. Caveat: Resource-heavy; requires significant RAM (32+ GB) and storage to batch-process uncompressed Level-1 SAR products.
- **Equasis:** Web-based vessel safety database providing global access to Port State Control inspection histories, ship registries, and ownership structures. Caveat: Rate-limited; intended for manual browser queries rather than high-throughput programmatic API scraping.

### Commercial

- **HawkEye 360 Mission Space:** Cloud analytics platform delivering spaceborne RF emitter detection, TDOA/FDOA geolocation, and automated dark-vessel correlation. Caveat: Highly restricted commercial and defense licensing; high per-scene or subscription costs.
- **Windward:** Predictive maritime AI platform fusing global AIS, SAR, and satellite imagery with proprietary behavioral models to flag sanctions evasion and illicit transshipment. Caveat: Proprietary algorithms operate as a black box with limited visibility into underlying raw sensor weights.
- **Kpler / MarineTraffic:** Commercial maritime intelligence suite providing aggregated terrestrial and satellite AIS, port call data, and vessel specifications ([Chapter 41](ch41-networks-and-providers.md)). Caveat: Commercial tier segmentation restricts access to historical tracking and API access.

---

## Standards & guides

- **International Maritime Organization (IMO) Resolution MSC.202(81) (2006):** *Adoption of Amendments to the International Convention for the Safety of Life at Sea, 1974, as Amended (SOLAS Regulation V/19-1: Long-Range Identification and Tracking of Ships)*. Governs mandatory carriage and global reporting of LRIT.
- **IMO Resolution MSC.263(84) (2008):** *Revised Performance Standards and Functional Requirements for the Long-Range Identification and Tracking of Ships*. Defines the technical architecture of LRIT Application Service Providers, Data Centres, and the International Data Exchange.
- **Council Regulation (EC) No 1224/2009 / Regulation (EU) 2023/2842:** *Community Control System for Ensuring Compliance with the Rules of the Common Fisheries Policy*. Mandates satellite Vessel Monitoring Systems (**VMS**) for EU commercial fishing fleets.
- **Food and Agriculture Organization (FAO) Port State Measures Agreement (PSMA) (2009):** International treaty requiring port state inspection, advance notification, and tracking compliance to combat illegal, unreported, and unregulated (**IUU**) fishing.
- **International Electrotechnical Commission (IEC) 62388 Ed. 2.0 (2013):** *Maritime navigation and radiocommunication equipment and systems - Shipborne radar - Performance requirements, methods of testing and required test results*. Defines target tracking and radar/AIS correlation standards.
- **World Meteorological Organization (WMO) WMO-No. 47 (2021):** *International List of Selected, Supplementary and Auxiliary Ships*. Governs shipboard weather instrumentation, observation procedures, and call sign reporting for the Voluntary Observing Ship (**VOS**) network.

---

## Pitfalls

1. **Assuming an AIS gap proves illicit activity:** Power failures, antenna line faults, and severe satellite packet contention in congested waters cause legitimate AIS blackouts. Treating every gap as deliberate sanctions evasion or illegal fishing without cross-verifying satellite revisit density is a critical analytical failure.
2. **Ignoring azimuth Doppler displacement in SAR matching:** Spaceborne SAR images displace moving vessels in the azimuth direction by hundreds of meters. Matching a raw SAR bright point to an AIS track without calculating radial velocity compensation creates false "dark vessel" alerts.
3. **Equating VMS absence with non-compliance:** VMS data is confidential and routed directly to sovereign Fisheries Monitoring Centres. An analyst viewing public AIS feeds cannot see VMS tracks; a vessel appearing dark on commercial AIS may be fully compliant with national VMS reporting laws.
4. **Treating LRIT as a tactical collision-avoidance tool:** LRIT reports arrive at 6-hour intervals over satellite uplinks directly to state registries. It is impossible to use LRIT on a ship bridge for navigation or tactical collision assessment.
5. **Over-trusting RF geolocation ellipses under poor GDOP:** Spaceborne RF TDOA fixes stretch into massive linear error ellipses when satellite geometry is unfavorable. Accepting an RF fix without filtering by its 90% confidence semi-major axis causes erroneous track association.
6. **Failing to account for tidal currents in dead-reckoning extrapolation:** Projecting a vessel's position forward across hours of tracking silence without integrating tidal and oceanic current vectors produces cumulative errors exceeding several nautical miles.
7. **Confusing ship length in SAR with optical resolution:** High dielectric reflectivity causes superstructures to bloom on SAR imagery, often making a vessel appear significantly larger than its physical length overall.
8. **Neglecting wake aging in optical imagery:** A visible ship wake persists on the ocean surface for 10 to 30 minutes depending on sea state. Associating an optical wake with an AIS track requires projecting the track backward across the wake's dispersion timeline.
9. **Relying on vessel names rather than IMO numbers:** Ship operators routinely alter vessel names, call signs, and painted hull markings to obscure identity. Only the permanent seven-digit IMO number remains immutable across international registries.
10. **Treating coastal radar as an all-weather panacea:** Heavy rain squalls, sea clutter, and atmospheric ducting severely degrade microwave radar detection ranges, creating temporary blind spots in coastal VTS coverage.

---

## Key takeaways

- **AIS is only one piece of the puzzle:** Complete maritime situational awareness requires fusing open VHF broadcasts with confidential satellite telemetry, active coastal and spaceborne radar, and passive RF and optical sensors.
- **Closed cooperative systems protect state and commercial interests:** VMS (fisheries) and LRIT (SOLAS commercial shipping) provide global, tamper-resistant satellite tracking directly to government centers without broadcasting position to the public.
- **Spaceborne SAR unmasks the global dark fleet:** Synthetic Aperture Radar pierces clouds and darkness to detect steel hulls via corner-reflector backscatter, proving that over 70% of industrial fishing vessels operate without active AIS.
- **SAR requires Doppler velocity correction:** Radial target motion shifts SAR vessel detections along the satellite flight path by hundreds of meters; matching SAR bright points to AIS requires explicit azimuth velocity compensation.
- **RF geolocation catches silent emitters:** Spaceborne TDOA/FDOA constellations geolocate marine radar pulses, VHF voice communications, and satellite phones even when AIS transponders are completely disabled.
- **Multi-sensor fusion relies on statistical gating:** Correlating uncooperative radar or satellite detections with broadcast tracks requires rigorous spatial-temporal gating using Mahalanobis distance filters that account for sensor covariances.
- **Permanent identity resides in the IMO number:** Hull names, flags, and MMSIs are easily changed; the permanent seven-digit IMO number and records in databases like Equasis provide the definitive ground truth for vessel tracking.

---

## References

- Androjna, A., Perkovič, M., Pavic, I., Mišković, J. (2021). AIS Data Vulnerability Indicated by a Spoofing Case-Study. *Applied Sciences*, 11(11):5015. doi:10.3390/app11115015
- Council of the European Union (2009). *Council Regulation (EC) No 1224/2009 Establishing a Community Control System for Ensuring Compliance with the Rules of the Common Fisheries Policy*. Official Journal of the European Union, L 343.
- Ellis, K., Van Rheeden, D., Dowla, F. (2020). Use of Doppler and Doppler Rate for RF Geolocation Using a Single LEO Satellite. *IEEE Access*, 8:29659–29671. doi:10.1109/ACCESS.2020.2965931
- European Parliament and Council of the European Union (2002). *Directive 2002/59/EC Establishing a Community Vessel Traffic Monitoring and Information System*. Official Journal of the European Communities, L 208.
- European Parliament and Council of the European Union (2009). *Directive 2009/17/EC Amending Directive 2002/59/EC Establishing a Community Vessel Traffic Monitoring and Information System*. Official Journal of the European Union, L 131.
- Food and Agriculture Organization of the United Nations (2009). *Agreement on Port State Measures to Prevent, Deter and Eliminate Illegal, Unreported and Unregulated Fishing*. Rome: FAO Treaty Database.
- Gattis, J., Cydejko, J., Akos, D. (2026). Real-Time Detection and Localization of Baltic Sea GNSS Interference Emitters Using Time-Difference-of-Arrival. *GPS Solutions*, 30(2):45–58. doi:10.1007/s10291-026-02061-5
- Guo, S. (2014). Space-Based Detection of Spoofing AIS Signals Using Doppler Frequency. *Proceedings of SPIE*, 9253:92530O. doi:10.1117/12.2050448
- HawkEye 360 (2020). *Tracking the Romina: Uncovering Dark Vessels with Spaceborne Radio Frequency Geolocation*. Technical Report. Herndon, VA: HawkEye 360 Inc.
- International Electrotechnical Commission (2013). *Maritime navigation and radiocommunication equipment and systems - Shipborne radar - Performance requirements, methods of testing and required test results*. Standard IEC 62388, Ed. 2.0. Geneva: IEC.
- International Maritime Organization (2004). *Adoption of the Revised Recommendation on Performance Standards for Radar Equipment*. Resolution MSC.192(79). London: IMO.
- International Maritime Organization (2006). *Adoption of Amendments to the International Convention for the Safety of Life at Sea, 1974, as Amended (SOLAS Regulation V/19-1: Long-Range Identification and Tracking of Ships)*. Resolution MSC.202(81). London: IMO.
- International Maritime Organization (2008). *Revised Performance Standards and Functional Requirements for the Long-Range Identification and Tracking of Ships*. Resolution MSC.263(84). London: IMO.
- International Telecommunication Union (2014). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile frequency band*. Recommendation ITU-R M.1371-5. Geneva: ITU.
- Kruger, M. (2019). Detection of AIS Spoofing in Fishery Scenarios. In *2019 22th International Conference on Information Fusion (FUSION)*, pages 1–8. IEEE. doi:10.23919/FUSION43075.2019.9011328
- Paolo, F. S., Kroodsma, D. A., Raynor, J., Hochberg, T., Davis, P., Cleary, J., Marsaglia, L., Orofino, S., Thomas, C., Halpin, P. N. (2024). Satellite Mapping Reveals Extensive Industrial Activity at Sea. *Nature*, 625(7993):85–91. doi:10.1038/s41586-023-06825-8
- Papi, F., Tarchi, D., Vespe, M., Oliveri, F., Borghese, F., Aulicino, G., Vollero, A. (2015). Radiolocation and Tracking of Automatic Identification System Signals for Maritime Situational Awareness. *IET Radar, Sonar & Navigation*, 9(5):568–580. doi:10.1049/iet-rsn.2014.0292
- World Meteorological Organization (2021). *International List of Selected, Supplementary and Auxiliary Ships*. WMO-No. 47. Geneva: WMO.
