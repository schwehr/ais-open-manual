# Chapter 54 — Tide, water level, weather, and marine-state transmissions

> **Part VIII — Charts, bridge systems, and mariners.** How physical oceanographic and meteorological sensor networks broadcast real-time water levels, tidal currents, bridge air gaps, and weather observations across the VHF Data Link, and why bridge integration remains incomplete.

**In this chapter.** You will learn how the Automatic Identification System (**AIS**) serves as an over-the-air digital carrier for physical oceanographic, meteorological, and hydrological data. We trace the technical architecture of environmental transmissions from legacy International Maritime Organization (**IMO**) SN/Circ.236 Application-Specific Messages (**ASMs**) to modern IMO SN.1/Circ.289 standards, regional specifications like United States Coast Guard (**USCG**) Designated Area Code (**DAC**) 367, European Inland AIS DAC 200, and the St. Lawrence Seaway system. You will examine bit-level encodings for water levels, current profiles, wind velocity, barometric pressure, and bridge air gaps. We analyze how shore networks such as the National Oceanic and Atmospheric Administration (**NOAA**) Physical Oceanographic Real-Time System (**PORTS**) ingest and broadcast observations. We evaluate the pervasive display gaps on type-approved Electronic Chart Display and Information Systems (**ECDIS**), sensor integration on Aids to Navigation (**AtoN**), data quality assurance, the World Meteorological Organization (**WMO**) Voluntary Observing Ship (**VOS**) program, and the operational migration toward International Hydrographic Organization (**IHO**) S-100 product specifications S-104 and S-111.

## 54.1 Environmental data on the VHF Data Link: operational rationale and architecture

Navigators operating in constrained coastal fairways, river channels, and shallow ports face hydrodynamic variations where static chart soundings are insufficient. Real-time water levels vary with astronomical tides, meteorological surges, and seasonal river discharge. Under-keel clearance (**UKC**) margins for deep-draft tankers and container vessels frequently fall below 1.0 m in dredged channels, while overhead air gaps beneath bridge spans vary with tidal amplitude. Concurrently, tidal current shears exert lateral forces that complicate steerage and berthing.

Traditionally, mariners acquired environmental updates via scheduled radiotelephone broadcasts from coastal Vessel Traffic Services (**VTS**), recorded telephone services, or dial-in telemetry. These methods impose operational drawbacks: they require manual transcription during high-workload pilotage, broadcast at coarse 30-to-60-minute intervals that mask rapid squalls or tidal reversals, consume voice spectrum, and cannot drive chart display calculations automatically.

With the standardization of AIS under Recommendation ITU-R M.1371 ([Chapter 21](ch21-link-layer-tdma.md)), hydrographic authorities recognized that the **VHF Data Link** (**VDL**) could deliver machine-readable physical oceanographic and meteorological observations directly to shipboard navigation systems. Transmitted as **Application-Specific Messages** (**ASMs**) via AIS Message 8 (broadcast) or Message 6 (addressed), these packets link shore sensor networks directly to bridge displays ([Chapter 23](ch23-asm-binary-payloads.md)).

```text
+-----------------------+     +-----------------------+     +-----------------------+
|  Acoustic Doppler     |     |  Acoustic / Pressure  |     |  Meteorological Mast  |
|  Current Profiler     |     |  Tide Gauge           |     |  Anemometer / Baro    |
|  (ADCP, seabed/buoy)  |     |  (NOAA PORTS / Gauges)|     |  Air temp / Humidity  |
+-----------+-----------+     +-----------+-----------+     +-----------+-----------+
            |                             |                             |
            +---------------------+       |       +---------------------+
                                  |       |       |
                                  v       v       v
                      +---------------------------------------+
                      |     Sensor Telemetry & QA/QC Engine   |
                      |  (NOAA CO-OPS / Port Authority Server)|
                      +-------------------+-------------------+
                                          |
                                          | IP Backhaul (3-min polling cycle)
                                          v
                      +---------------------------------------+
                      |       AIS Data Formatter / Daemon     |
                      |  - Encodes DAC/FI bit payload         |
                      |  - Packages IEC 61162-1 !AIVDM string |
                      +-------------------+-------------------+
                                          |
                                          | RS-422 / Ethernet IEC 61162-450
                                          v
                      +---------------------------------------+
                      |      Shore AIS Base Station / AtoN    |
                      |  - Schedules FATDMA slots (Msg 20)    |
                      |  - Modulates GMSK 9.6 kbps on AIS 1/2 |
                      +-------------------+-------------------+
                                          |
                                          | 161.975 / 162.025 MHz (VDL)
                                          v
                      +---------------------------------------+
                      |       Shipboard AIS Transponder       |
                      |  - Demodulates Message 8 (DAC/FI)     |
                      |  - Outputs !AIVDM on Presentation Port|
                      +-------------------+-------------------+
                                          |
                         +----------------+----------------+
                         |                                 |
                         v                                 v
            +-------------------------+       +-------------------------+
            | Type-Approved ECDIS     |       | Portable Pilot Unit     |
            | (Display gaps common;   |       | (PPU) Laptop / Tablet   |
            | text-only or unsupported|       | (Full dynamic rendering,|
            | on legacy bridge units) |       | UKC / air gap graphics) |
            +-------------------------+       +-------------------------+
```

The general transmission architecture incorporates:
- **In-situ sensor instrumentation:** Bottom-mounted Acoustic Doppler Current Profilers (**ADCPs**), acoustic and microwave radar tide gauges, meteorological towers, bridge air-gap laser sensors, and water quality conductivity-temperature instruments.
- **Telemetry and Quality Assurance / Quality Control (QA/QC):** Shore base computing centers poll field sensors at regular intervals (typically 3 to 6 minutes), execute automated algorithmic data verification (range, step, rate-of-change, and sensor redundancy checks), and reject aberrant spikes.
- **Encoding engines:** Validated sensor values are serialized into specific binary bitfields matching the governing Designated Area Code (**DAC**) and Function Identifier (**FI**).
- **Physical transmission:** The serialized bit payload is encapsulated in NMEA 0183 / IEC 61162-1 binary broadcast encapsulation sentences (`!AIVDM` or `$ABM`) and injected into a coastal AIS base station or limited base station. The base station transmits the packet across pre-reserved Fixed Access Time Division Multiple Access (**FATDMA**) slots announced via AIS Message 20 ([Chapter 21](ch21-link-layer-tdma.md)).

## 54.2 The message lineage: from SN/Circ.236 to SN.1/Circ.289

The international standardization of environmental data over AIS followed an evolutionary trajectory marked by expanding payload capacity, shifting datums, and field alignment adjustments.

### 54.2.1 Legacy IMO SN/Circ.236 (2004)

In May 2004, the IMO Maritime Safety Committee issued **SN/Circ.236**, entitled *Guidance on the Use of the Specification of Application-Specific Messages to the Maritime Mobile Service* (IMO SN/Circ.236 2004). Among seven trial messages, Circ.236 established:
- **DAC 001, FI 11:** *Meteorological and Hydrological Data* (broadcast via AIS Message 8).

Message 8 FI 11 encapsulated a comprehensive fixed-length environmental report into a multi-slot VDL packet spanning 352 payload bits (plus 56 bits of Message 8 header, yielding 408 bits or two TDMA slots). It reported geographic coordinates (latitude and longitude encoded to 0.001 arc-minutes), UTC day/hour/minute, wind speed, gust, wind direction, air temperature, relative humidity, dew point, atmospheric pressure, visibility, water level, water level trend, current speed and direction across three distinct depth strata, wave height, wave period, wave direction, swell height/period/direction, sea state, water temperature, precipitation type, salinity, and ice accretion.

Despite its technical breadth, field experience revealed design deficiencies in SN/Circ.236 FI 11:
1. **Rigid monolithic structure:** Every transmission carried every field. If an offshore sensor station possessed only a tide gauge and an anemometer, the remaining oceanographic fields (ADCP strata, wave characteristics, salinity, ice) still had to be broadcast filled with "not available" sentinels, squandering VDL slot capacity.
2. **Datum ambiguities:** The water level field lacked explicit vertical datum tagging. Receivers could not programmatically distinguish whether an indicated water level of +1.5 m was referenced to Mean Lower Low Water (**MLLW**), Lowest Astronomical Tide (**LAT**), ordnance datum, or an ellipsoidal model.
3. **Sensor-type blindness:** The message did not indicate sensor provenance (e.g., ultrasonic gauge versus barometric pressure gauge versus hydro-model forecast).
4. **Resolution limits:** Several scaling factors lacked the granular resolution demanded by commercial pilots performing precision docking maneuvers.

Consequently, when the IMO overhauled binary messages in 2010, SN/Circ.236 FI 11 was formally deprecated.

### 54.2.2 IMO SN.1/Circ.289 (2010): The dual-standard era

In June 2010, the IMO published **SN.1/Circ.289**, *Guidance on the Use of AIS Application-Specific Messages*, superseding Circ.236 (IMO SN.1/Circ.289 2010). Rather than relying on a single environmental message, Circ.289 introduced two distinct international structures under international DAC 001:
- **DAC 001, FI 31:** *Meteorological and Hydrographic Data* (monolithic point broadcast).
- **DAC 001, FI 26:** *Environmental* (modular multi-record report).

#### Circ.289 FI 31: Modern monolithic met/hydro broadcast
FI 31 retains the single-station comprehensive snapshot concept of FI 11 but refines bit widths, resolution, and sentinel values. Encapsulated in AIS Message 8, FI 31 occupies 360 payload bits (416 bits total including the 56-bit Message 8 transport header), fitting cleanly into a two-slot TDMA transmission. 

Key technical adjustments between legacy FI 11 and Circ.289 FI 31 include:
- **Position accuracy flag:** A 1-bit indicator (bit 56) explicitly documents whether sensor coordinates derive from differential GNSS (< 10 m) or autonomous positioning.
- **Atmospheric pressure scaling:** FI 11 transmitted pressure offset by 800 hPa ($p_{\text{raw}} = p_{\text{actual}} - 800$), whereas FI 31 transmits pressure offset by 799 hPa ($p_{\text{raw}} = p_{\text{actual}} - 799$), covering a range of 800 to 1200 hPa with a 9-bit field.
- **Water level encoding:** The water level field was expanded from 9 bits in FI 11 (0.1 m resolution, offset by 10.0 m) to 12 bits in FI 31 ($0.01\text{ m}$ resolution, offset by $10.0\text{ m}$), enabling centimeter-level tidal reporting across a range of $-10.00\text{ m}$ to $+30.00\text{ m}$.
- **Ice code expansion:** Refined classification covering sea ice, glaze, and vessel icing risk.

#### Circ.289 FI 26: Modular sensor reports
Recognizing that fixed towers, floating buoys, and bridge structures host radically disparate sensor suites, Circ.289 FI 26 established a modular sub-record framework. Following a 56-bit transmission header, the payload carries 1 to 5 concatenated 112-bit sensor records: Type 0 (*Site Location*), Type 1 (*Station ID*, 14 six-bit ASCII chars), Type 2 (*Wind*), Type 3 (*Water Level* & forecast), Type 4 (*Current Flow 2D* across 3 depths), Type 5 (*Current Flow 3D* vector components), Type 6 (*Horizontal Current* profile), Type 7 (*Sea State* & swell), Type 8 (*Salinity* & CTD), Type 9 (*Weather* & baro), and Type 10 (*Air Gap* bridge clearance).

This modular architecture allows a shore station monitoring a bridge to broadcast a two-slot Message 8 combining Report Type 0 (location), Report Type 3 (water level), and Report Type 10 (air gap), without transmitting empty wave or current fields.

## 54.3 Regional variants: USCG DAC 367, St. Lawrence Seaway, and Inland AIS

Because international standardization through IMO and ITU cycles requires multi-year lead times, national navigation authorities deployed operational regional ASMs tailored to localized waterways.

### 54.3.1 USCG DAC 366 and DAC 367 (Environmental Message)

The United States Coast Guard Research and Development Center (**USCG RDC**), in partnership with NOAA Center for Operational Oceanographic Products and Services (**CO-OPS**), conducted pilot transmissions under Maritime Identification Digit (**MID**) DAC 366 beginning in 2007 (Schwehr and Alexander 2007; Gonin et al. 2009). The initial trial deployed **DAC 366, FI 33** (Environmental Message). 

As regional message definitions stabilized, the USCG transitioned civil hydrographic messages to **DAC 367** to separate experimental and civil safety broadcasts from legacy military and law enforcement encrypted operations on DAC 366 ([Chapter 23](ch23-asm-binary-payloads.md)). The current operational specification is **DAC 367, FI 33 (Environmental Message, Release Version 3)**.

DAC 367 FI 33 expands upon the IMO Circ.289 FI 26 design:
- It maintains the 112-bit sensor record slice architecture.
- It expands the maximum record count from 5 to 8 records per transmission, permitting up to a 5-slot TDMA packet (952 bits maximum).
- It introduces an enhanced **Wind Report Type 11** containing a user-configurable averaging period (1 to 60 minutes) and gust duration.
- It incorporates rigorous vertical datum enumerations in the Water Level report (Table 54.1), resolving the datum ambiguity that undermined legacy broadcasts.

| Code | Datum Name | Operational Application |
| :---: | :--- | :--- |
| `0` | Mean Lower Low Water (MLLW) | Standard US chart sounding datum |
| `1` | IGLD-85 | Great Lakes and St. Lawrence hydraulic reference |
| `2` | Mean Water Level (MWL) | Mean surface elevation |
| `3` | Lowest Astronomical Tide (LAT) | International chart datum (IHO standard) |
| `4` | Mean Sea Level (MSL) | Mean level over tidal epoch |
| `5` | NAVD88 | North American Vertical Datum of 1988 |
| `6` | NGVD29 | Legacy geodetic datum |
| `7`–`30`| Regional / Reserved | Local harbor and pool datums |
| `31`| Unknown / Not Available | Default sentinel |

### 54.3.2 St. Lawrence Seaway: DAC 316 and 366

The Saint Lawrence Seaway Development Corporation (**SLSDC**, now GLS) and St. Lawrence Seaway Management Corporation (**SLSMC**) mandated commercial AIS carriage in March 2003, predating general US domestic rules (SLSDC 2010; [Chapter 43](ch43-demonstration-programs.md)). Operating in narrow channels and locks, the Seaway deployed bilateral messages registered under Canada (DAC 316) and the US (DAC 366).

Structured around sub-identifiers on Messages 6 and 8, the Seaway protocol broadcasts:
- **FI 1, Sub-ID 1 (Weather Station):** Wind velocity, temperature, and pressure at canal approaches.
- **FI 1, Sub-ID 3 (Water Level):** Real-time elevations referenced to **IGLD-85** across lock reaches.
- **FI 1, Sub-ID 6 (Water Flow):** Cross-current and down-channel flow rates.
- **FI 2, Sub-ID 1 & 2 (Lockage Order & Estimated Lock Times):** Traffic scheduling directing lock queues.

Because commercial lake carriers operate with under-keel margins measured in inches, real-time AIS water levels directly govern permissible vessel draft.

### 54.3.3 European Inland AIS: DAC 200

In European inland waterways governed by CCNR and CESNI, river navigation requires continuous monitoring of water stage and bridge clearances. Standard Inland AIS defines regional **DAC 200** messages (CESNI Inland AIS 2021):
- **DAC 200, FI 24 (Water Level):** Single-slot broadcast carrying gauge heights for up to four stations simultaneously, each with an 11-bit gauge ID and 14-bit signed elevation in centimeters ($0.01\text{ m}$ resolution).
- **DAC 200, FI 26 (Water Level v0):** Modernized replacement with expanded country codes and reference plane definitions.
- **DAC 200, FI 25 (Present Bridge Clearance):** Real-time air gap telemetry beneath fixed spans across the Rhine, Danube, and connecting waterways.

## 54.4 Physical oceanographic integration: NOAA PORTS and real-world pipelines

The United States National Oceanic and Atmospheric Administration (**NOAA**) operates the Physical Oceanographic Real-Time System (**PORTS**), an integrated environmental sensor network deployed across critical commercial seaports (NOAA PORTS 2023). PORTS ingests telemetry from hundreds of coastal stations, verifying water levels, currents, bridge clearances, winds, waves, water temperature, and atmospheric parameters.

In 2007–2009, NOAA CO-OPS, the USCG RDC, and VTS Tampa Bay initiated the first continuous municipal PORTS-over-AIS transmission testbed (Gonin et al. 2009). The engineering architecture developed for Tampa Bay established the standard design for national deployment:

1. **Sensor Ingestion:** Instruments at harbor channels (e.g., Sunshine Skyway Bridge, Port Manatee, Egmont Key) sample at 1 Hz, computing 6-minute rolling averages.
2. **Central QA/QC Processing:** Observations stream via satellite (GOES) or IP telemetry to NOAA CO-OPS operational servers. Automated validation algorithms check sensor thresholds, historical trends, and multi-sensor parity.
3. **The Fetcher / Formatter Daemon:** A dedicated coastal daemon polls the CO-OPS real-time data server via secure HTTP or socket connections every 3 minutes.
4. **Binary Serialization:** The daemon serializes current measurements into binary frames. In modern implementations, it constructs USCG DAC 367 FI 33 or IMO Circ.289 FI 31 structures.
5. **NMEA Injection:** The binary string is packed into `!AIVDM` / `$ABM` sentence pairs and transmitted over an authenticated network socket (or serial RS-422 interface) to the VTS AIS base station.
6. **VDL Transmission:** The base station modulates the packet on AIS Channel 1 (161.975 MHz) or Channel 2 (162.025 MHz) using pre-allocated FATDMA slots.

> **Worked example.**  
> Consider an environmental monitoring station at an estuary entrance reporting a water level of $+1.84\text{ m}$ relative to MLLW with a falling trend, surface water current velocity of $2.4\text{ kn}$ setting along bearing $142^\circ\text{ True}$, air temperature $+16.4^\circ\text{C}$, barometric pressure $1018\text{ hPa}$ (steady), and sustained wind speed $18\text{ kn}$ from $045^\circ\text{ True}$.
> 
> *Step 1: Water level encoding (IMO SN.1/Circ.289 FI 31).*  
> Per Circ.289 FI 31, the water level field occupies 12 bits with a scaling of $0.01\text{ m}$ and an offset of $+10.00\text{ m}$:
> $$\text{Raw Value} = \frac{\text{Value (m)} + 10.00}{0.01} = \frac{1.84 + 10.00}{0.01} = \frac{11.84}{0.01} = 1184$$
> Converted to 12-bit binary: `0100 1010 0000` (binary $1184$).  
> The water level trend is encoded in 2 bits: `00` = steady, `01` = decreasing (falling), `10` = increasing (rising), `11` = not available. Here, `trend` = `01`.
> 
> *Step 2: Surface current encoding.*  
> Speed occupies 8 bits with $0.1\text{ kn}$ scaling:
> $$\text{Raw Speed} = \frac{2.4}{0.1} = 24 = \text{`0001 1000`}_2$$
> Direction occupies 9 bits ($0^\circ$–$359^\circ$; $360$ = not available):
> $$\text{Raw Direction} = 142 = \text{`0 1000 1110`}_2$$
> 
> *Step 3: Atmospheric pressure encoding.*  
> Atmospheric pressure in FI 31 occupies 9 bits with an offset of $799\text{ hPa}$:
> $$\text{Raw Pressure} = 1018 - 799 = 219 = \text{`0 1101 1011`}_2$$
> Tendency in 2 bits: steady = `00`.
> 
> *Step 4: Air temperature encoding.*  
> Air temperature occupies 11 bits signed, with $0.1^\circ\text{C}$ resolution:
> $$\text{Raw Temperature} = \frac{+16.4}{0.1} = 164 = \text{`000 1010 0100`}_2$$
> 
> Packing these fields into sequential bit boundaries produces a continuous bitstream that is split into 6-bit ASCII words for over-the-air NMEA encapsulation.

## 54.5 Display gaps on the bridge: the ECDIS presentation problem

Despite robust transmission of hydrographic and meteorological data over the VDL, the practical utility of ASMs across bridge systems has historically encountered a major failure point: **the shipboard presentation barrier**.

Under IMO performance standards for ECDIS (Resolution MSC.232(82)) and the associated testing standard IEC 61174 (*ECDIS Operational and Performance Requirements*), type-approval mandates the decoding and graphical presentation of core navigation messages—specifically Class A and Class B position reports (Messages 1, 2, 3, 18, 19), voyage static data (Message 5), and Aids to Navigation (Message 21) (IEC 61174 2015). **Application-Specific Messages (Messages 6 and 8) were never mandated as compulsory display layers in early ECDIS standards.**

```text
+------------------------------------------------------------------------+
|                      Shipboard Bridge Navigation Stack                 |
|                                                                        |
|  +---------------------------+         +----------------------------+  |
|  |   VHF Antenna & Feeder    |         |    GPS / DGNSS Receiver    |  |
|  +-------------+-------------+         +-------------+--------------+  |
|                |                                     |                 |
|                v                                     v                 |
|  +------------------------------------------------------------------+  |
|  |                 Class A AIS Transponder (IEC 61993-2)            |  |
|  |  - Demodulates VDL bursts; verifies CRC-CCITT                     |  |
|  |  - Encapsulates payload into NMEA 0183 !AIVDM sentences          |  |
|  +-----------------------------+------------------------------------+  |
|                                |                                       |
|                                | High-Speed Serial RS-422 (38.4 kbps)  |
|                                | or IEC 61162-450 Ethernet Multicast   |
|                                v                                       |
|  +------------------------------------------------------------------+  |
|  |                     ECDIS Processor (IEC 61174)                  |  |
|  |                                                                  |  |
|  |   Core Tracking Pipeline        Application-Specific Messages    |  |
|  |   (Mandated by IEC 62288):      (Optional / Unimplemented):      |  |
|  |   - Msg 1/2/3 Target Vectors    - Msg 8 FI 31 (Met/Hydro)        |  |
|  |   - Msg 5 Static & Voyage       - Msg 8 FI 26 (Air Gap / Tide)   |  |
|  |   - Msg 21 AtoN Symbols         - USCG DAC 367 FI 33             |  |
|  |             |                               |                    |  |
|  |             v                               v                    |  |
|  |     [ FULL GRAPHICAL ]            [ DROPPED SILENTLY  ]          |  |
|  |     [ VECTOR OVERLAY ]            [ OR BURIED IN TEXT ]          |  |
|  |                                   [ DIAGNOSTIC MENUS  ]          |  |
|  +------------------------------------------------------------------+  |
+------------------------------------------------------------------------+
```

This omission produced severe operational fragmentation:
1. **Silent packet discarding:** Many type-approved ECDIS units simply drop incoming Message 8 packets that contain unknown DAC/FI values, treating them as unhandled protocol extensions.
2. **Text-only diagnostic presentation:** Systems that decode Message 8 often dump raw numerical values into deeply nested diagnostic text menus (e.g., sub-menus labeled "AIS Special Messages" or "Target Diagnostics"). A mariner navigating through a narrow channel cannot browse text menus to locate the water level.
3. **Absence of standard symbology:** Until recent revisions of IEC 62288 (*Presentation of Navigation-Related Information on Shipborne Navigational Displays*), there were no standardized, harmonized screen symbols or dynamic vector overlays for real-time current shears or bridge air-gap clearance indicators (IEC 62288 2021).
4. **Lack of dynamic tide integration:** Standard ECDIS engines calculate chart sounding depth using the static depth attributes compiled into the vector ENC cell (`DRVAL1`, `VALSOU`), with no hook to adjust the displayed safety depth contour using incoming AIS water level broadcasts.

> **Definitions that bite.**  
> **Air Gap vs. Air Draught.**  
> *Air draught* (or masthead height) is the vertical distance from a vessel's operational waterline to the highest fixed point on the ship (typically radar masts, communications antennas, or crane booms).  
> *Air gap* (or vertical bridge clearance) is the physical distance between the instantaneous water surface and the lowest structural member of an overhead obstruction (e.g., bridge span, overhead power cable).  
> Confusion between these terms in ASM displays has led watch officers to invert the clearance calculation:
> $$\text{Clearance Margin} = \text{Air Gap}_{\text{actual}} - \text{Air Draught}_{\text{vessel}}$$
> If an AIS message reports an "air draught" field that the display software mistakes for available "air gap," a ship risks an overhead allision.

### 54.5.1 The Portable Pilot Unit (PPU) workaround

Because certified shipboard bridge displays lagged behind over-the-air standards, maritime pilots filled the operational void with **Portable Pilot Units** (**PPUs**). A pilot boards a commercial vessel carrying a self-contained navigation computer (ruggedized laptop or tablet) running specialized hydrographic software (such as Qastor, SEAiq, or Transas Pilot). 

The pilot connects the PPU to the vessel's AIS pilot plug (via an RS-422 cable or Wi-Fi/Bluetooth bridge) or utilizes an independent portable AIS receiver. PPU software architectures were designed to parse regional and international ASMs (including IMO Circ.289, USCG DAC 367, and Seaway DAC 316). The PPU displays dynamic water-level contours, real-time current velocity vectors color-coded across channel reaches, and live bridge clearance indicators directly on high-resolution bathymetric chart layers.

## 54.6 AtoN-carried sensors: autonomous oceanographic platforms

Environmental AIS transmissions originate not only from major shore base stations but increasingly from autonomous, buoy-mounted **AIS Aids to Navigation** (**AIS AtoN**) transponders ([Chapter 20](ch20-architecture-and-station-classes.md)).

Marine lighthouse authorities, offshore wind farm operators, and port authorities install integrated oceanographic sensor packages directly on physical navigation buoys. An AIS AtoN station possesses a unique Maritime Mobile Service Identity (**MMSI**) beginning with the regional prefix `99` (e.g., `993671001` per ITU-R M.585; [Chapter 13](ch13-mmsi-deep-dive.md)).

An environmental buoy executes two interleaved AIS reporting tasks:
1. **Aids to Navigation Report (Message 21):** Transmits buoy position, type of aid, name, and position accuracy flag, marking the physical hazard or channel edge.
2. **Environmental Binary Broadcast (Message 8):** Broadcasts real-time water temperature, wave height, current speed, or meteorological parameters collected by onboard sensors.

```text
+------------------------------------------------------------------------+
|             Physical AIS AtoN Environmental Station (Type 3)           |
|                                                                        |
|  +-----------------------------+     +------------------------------+  |
|  | Solar Array / Battery Bank  |     | Met Mast: Sonic Anemometer   |  |
|  | Power Management Unit       |     | Temp / Pressure / Humidity   |  |
|  +--------------+--------------+     +--------------+---------------+  |
|                 |                                   |                  |
|                 +-------------------+---------------+                  |
|                                     |                                  |
|                                     v                                  |
|  +------------------------------------------------------------------+  |
|  |           Subsurface Oceanographic Instrumentation               |  |
|  |  - Downward-looking ADCP (current profile across water column)   |  |
|  |  - Moored wave sensor (accelerometer/inertial wave orbital motion|  |
|  |  - Conductivity / Salinity probe (CTD)                           |  |
|  +----------------------------------+-------------------------------+  |
|                                     |                                  |
|                                     | RS-232 / NMEA 0183 Serial        |
|                                     v                                  |
|  +------------------------------------------------------------------+  |
|  |          Embedded AtoN Controller / Payload Serializer           |  |
|  |  - Gathers instantaneous readings; executes vector averaging     |  |
|  |  - Formats IMO Circ.289 FI 31 or FI 26 binary payload            |  |
|  |  - Generates $EBI / $ABM sentence blocks                         |  |
|  +----------------------------------+-------------------------------+  |
|                                     |                                  |
|                                     | Internal Bus                     |
|                                     v                                  |
|  +------------------------------------------------------------------+  |
|  |         Type 3 AIS AtoN Transceiver (IEC 62320-2)                |  |
|  |  - Operates in SOTDMA or RATDMA mode                             |  |
|  |  - Message 21: AtoN position & status (cadence: 3 minutes)       |  |
|  |  - Message 8: Met/Hydro binary payload (cadence: 6–12 minutes)   |  |
|  |  - Power consumption: < 1.5 W average across operating cycle      |  |
|  +------------------------------------------------------------------+  |
+------------------------------------------------------------------------+
```

AtoN-carried environmental stations operate under strict constraints:
- **Power budget limitations:** Solar buoys must survive winter low-light periods. While Message 21 consumes minimal power, transmitting multi-slot Message 8 packets every few minutes drains battery reserves. AtoN controllers throttle report rates dynamically (e.g., dropping from 6-minute to 15- or 30-minute intervals if voltage drops below $11.8\text{ V}$).
- **Sensor motion dynamics:** Buoy roll, pitch, and heave impart severe accelerations to masthead anemometers. Uncorrected sensors report false gusts induced by wave action; modern buoy controllers use internal inertial gyros and accelerometers to decouple buoy kinematics from true wind and current vectors prior to broadcast.

## 54.7 Shipboard weather reporting: WMO VOS over AIS

Environmental transmissions on the VDL are not solely shore-to-ship. The **World Meteorological Organization** (**WMO**) oversees the **Voluntary Observing Ship** (**VOS**) program, coordinating merchant vessels that collect weather observations for National Meteorological Services (WMO Pub 47 2021).

While traditional VOS reports relied on manual logging sent via Inmarsat-C or HF radio, IMO SN.1/Circ.289 standardized **DAC 001, FI 21 (Weather Observation Report from Ship)** to automate ship-to-shore transmission over AIS Message 8. Spanning 360 payload bits (two TDMA slots), FI 21 encapsulates:
- Position coordinates, accuracy flag, and UTC timestamp (day, hour, minute).
- Vessel COG, SOG, and true heading (enabling shore systems to decouple vessel motion from true wind vectors).
- Wind speed, gusts, and true direction.
- Atmospheric pressure, tendency, and 3-hour pressure trend.
- Air temperature, dew point, relative humidity, and sea surface temperature.
- WMO present/past weather codes, horizontal visibility, cloud cover/genus/base, and wave/swell vectors.

Coastal AIS shore stations harvest FI 21 broadcasts and inject them directly into numerical weather prediction models (e.g., NOAA NWS, ECMWF), transforming commercial fleets into dense, automated meteorological observation arrays without satellite airtime costs.

## 54.8 The future: the transition to S-100 (S-104 and S-111) and VDES

The operational limitations of legacy AIS binary messages—bandwidth bottlenecks, non-standardized displays, and lack of spatial granularity—drove the maritime community toward next-generation data frameworks ([Chapter 52](ch52-ais-and-s100.md); [Chapter 69](ch69-vdes-ais-2.md)).

```text
+------------------------------------------------------------------------+
|                          The Paradigm Shift                            |
|                                                                        |
|  Legacy AIS ASM Model (Point Observations):                            |
|                                                                        |
|       [ Shore Station / Buoy ]                                         |
|                  |                                                     |
|                  | AIS Message 8 (DAC 1 FI 31 / DAC 367)               |
|                  | Point observation: Lat, Lon, Water Level = +1.84 m  |
|                  v                                                     |
|       [ Bridge Display ] --> Shows isolated text or gauge icon         |
|                              No spatial interpolation across channel   |
|                                                                        |
|  --------------------------------------------------------------------  |
|                                                                        |
|  S-100 / VDES Paradigm (High-Resolution Hydrodynamic Grids):          |
|                                                                        |
|       [ Oceanographic Hydrodynamic Model (e.g., NOAA ADCIRC / FVCOM) ] |
|                  |                                                     |
|                  | Generates dynamic surface elevation & current mesh  |
|                  v                                                     |
|       [ S-104 (Water Level) & S-111 (Current) HDF5 Data Sets ]        |
|                  |                                                     |
|                  | High-Bandwidth Terrestrial/Satellite Bearer         |
|                  | (VDES ASM / VDE Channels or Shore IP / 5G)          |
|                  v                                                     |
|       [ Dual-Fuel S-100 ECDIS (IMO MSC.530(106)) ]                     |
|                  |                                                     |
|                  +---> Dynamic Water Level Adjusts Bathymetric Contours|
|                  +---> Real-Time Current Vectors Modulate Ship Drift   |
+------------------------------------------------------------------------+
```

Under the IHO **S-100 Universal Hydrographic Data Model** framework, two primary product specifications govern dynamic water-level and current data:
1. **S-104:** *Water Level Information for Surface Navigation* (IHO S-104 2023). S-104 provides gridded and point water-level forecasts and observations encoded in Hierarchical Data Format 5 (**HDF5**). When ingested by an S-100 ECDIS, S-104 data dynamically shifts charted soundings and safety contours in real time.
2. **S-111:** *Surface Currents* (IHO S-111 2023). Encoded in HDF5, S-111 delivers gridded vector fields defining speed and direction across waterway corridors, enabling chart displays to animate surface stream dynamics.

### 54.8.1 The bandwidth dilemma: AIS VDL vs. VDES

The primary obstacle to operational S-104 and S-111 deployment is data payload size: high-resolution HDF5 grids for dynamic waterways span 50 kilobytes to several megabytes.

Legacy AIS at 9.6 kbps cannot convey such volumes without inducing catastrophic TDMA slot collapse ([Chapter 30](ch30-network-loading-packet-loss.md)); a maximum 5-slot Message 8 delivers just 119 bytes of application data while consuming 133 ms of VDL airtime.

To resolve this limitation, the **VHF Data Exchange System** (**VDES**; ITU-R M.2092) segregates data traffic:
- Dedicated **ASM channels** (ASM 1 at 161.950 MHz, ASM 2 at 162.000 MHz) offload binary messages from AIS 1 and 2.
- Wideband **VDE channels** employ channel bonding and higher-order modulations (QPSK, 16-QAM) to achieve up to 307 kbps, streaming gridded S-104 and S-111 datasets directly to ships entering coastal pilotage zones.

## Then & now

- `⟨H⟩` **1990s:** Mariners relied on printed nautical tide tables, coastal radio stations broadcasting scheduled voice summaries on VHF Channel 16/12, or local phone lines to obtain water levels and bridge clearances.
- `⟨H⟩` **2002:** The St. Lawrence Seaway Development Corporation deployed the first operational shore-to-ship digital binary AIS messages (DAC 316/366) delivering water level (IGLD-85 datum) and wind data to transiting vessels months ahead of general carriage rules.
- `⟨H⟩` **2004:** The IMO adopted SN/Circ.236, defining the first international trial Application-Specific Message for meteorological and hydrographic data (DAC 1, FI 11).
- `⟨+⟩` **2007:** Schwehr and Alexander published the foundational binary message specification for hydrographic-related information at US Hydro 2007, pioneering modular oceanographic message encoding.
- `⟨+⟩` **2008:** The USCG RDC, NOAA CO-OPS, and VTS Tampa Bay initiated the first continuous municipal PORTS-over-AIS transmission testbed, broadcasting environmental data every 3 minutes from the Largo, Florida base station.
- `⟨+⟩` **2010:** The IMO published SN.1/Circ.289, formally deprecating Circ.236 FI 11 and establishing Circ.289 FI 31 (point met/hydro) and FI 26 (modular sensor reports).
- `⟨+⟩` **2011:** The USCG registered DAC 366 environmental messages with IALA, subsequently transitioning civil operations to DAC 367 (Release Version 3) to prevent collision with encrypted blue-force operations.
- `⟨+⟩` **2014:** The IMO Maritime Safety Committee issued MSC.1/Circ.1473, enacting a strict policy to restrict VDL ASM transmissions to preserve slot capacity for collision avoidance.
- `⟨+⟩` **2021:** European inland waterways transitioned to Standard Inland AIS Edition 2021/1 under CESNI, formalizing DAC 200 FI 25 bridge clearance and FI 26 water level protocols.
- `⟨+⟩` **2022:** The IMO adopted Resolution MSC.530(106), establishing performance standards for dual-fuel S-100 ECDIS capable of natively parsing dynamic S-104 water level and S-111 surface current hydrographic layers.
- `⟨+⟩` **2026:** Under MSC.530(106), voluntary deployment of S-100 ECDIS commences, transitioning dynamic water levels from isolated AIS text packets to interactive, real-time depth contour adjustments.

## On the wire

Environmental transmissions across the VHF Data Link rely on **AIS Message 8** (Binary Broadcast Message). Below, we trace the bit layout of an international **IMO SN.1/Circ.289 FI 31** (*Meteorological and Hydrographic Data*) transmission, which packs 360 payload bits (plus 56 bits of Message 8 header) into a two-slot TDMA frame.

```text
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  ID (6) | R (2)|          MMSI (30)                  |Sp(2)|
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|       DAC (10)        |    FI (6)     |       Longitude (25)  |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   ... Longitude (cont.)       |        Latitude (24)          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| ...Lat (cont.)|A(1)| Day(5)   | Hr(5) | Min(6)|  W-Spd(7)     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  W-Gust(7)    |    W-Dir (9)          |   W-GstDir(9)         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|   Air-Temp (11, signed)   | Humid(7)  |   Dew-Point (10)      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|    Pressure (9, +799) |Tr(2)|V>|  Vis(7)|   Water-Level (12)  |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|...WL(c)|Tr(2)| Cur-Spd(8)    |  Cur-Dir(9)           | CS2(8) |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|...CS2  |  CD2(9)              |CDep2(5)| Cur-Spd3(8)   | CD3..|
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|...CD3(9)      |CDep3(5)| Wave-Ht(8)   | W-Per(6)| Wave-Dir(9) |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|...W-Dir| Swl-Ht(8)     | Swl-Per(6)  | Swl-Dir(9)            |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|...SDir |SeaSt(4)| Water-Temp (10)     |Pr(3)|  Salinity (9)   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|...Sal  |Ice(2)| Spare (10 bits, set to 0)                     |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

**Table 54.2:** Functional Bit Allocation for IMO SN.1/Circ.289 Message 8 FI 31

| Bits | Width | Parameter Group | Resolution / Encoding | Sentinel / N/A |
| :---: | :---: | :--- | :--- | :--- |
| `0`–`39` | 40 | Transport Header | Msg ID 8 (6), Repeat (2), Source MMSI (30), Spare (2) | Standard M.1371 |
| `40`–`55` | 16 | Application ID | DAC `1` (10 bits), FI `31` (6 bits) | Circ.289 Met/Hydro |
| `56`–`105` | 50 | Position & Accuracy | Lon (25), Lat (24) in $0.001\text{ min}$; Acc flag (1) | `0x1A83800` / `0x7FFFFF` |
| `106`–`121` | 16 | Observation Time | UTC Day (5), Hour (5), Minute (6) | Day 0, Hr 24, Min 60 |
| `122`–`153` | 32 | Wind (Ave & Gust) | Speed (7, 7) in kn; Dir (9, 9) in deg True | Spd 127, Dir 360 |
| `154`–`181` | 28 | Atmosphere & Moisture | Air Temp (11, $0.1^\circ\text{C}$ signed); Humidity (7, %); Dew pt (10) | Temp $-102.4$, Hum 101 |
| `182`–`200` | 19 | Pressure & Visibility | Pressure (9, hPa $+799$); Trend (2); Vis (7, $0.1\text{ nmi}$) | Pres 0, Vis 12.7 |
| `201`–`214` | 14 | Water Level | Level (12, $0.01\text{ m}$, offset $+10.0\text{ m}$); Trend (2) | Level 4001 ($30.01\text{ m}$) |
| `215`–`273` | 59 | Currents (3 Strata) | Surface (17); Layer 2 (22); Layer 3 (20) [Speed, Dir, Depth] | Spd 25.5, Dir 360 |
| `274`–`319` | 46 | Waves & Swell | Wave Ht (8), Period (6), Dir (9); Swell Ht/Per/Dir (23) | Ht 25.5, Per 63 |
| `320`–`347` | 28 | Marine Environment | Sea State (4); Water Temp (10); Precip (3); Salinity (9); Ice (2) | Temp 50.1, Sal 51.0 |
| `348`–`415` | 68 | Padding / Spares | Reserved alignment bits set to `0` | Two TDMA slots total |

> **On the wire.**  
> Below is a real-world broadcast sentence captured from an Irish coastal monitoring station configured with an AIS AtoN transponder:
> ```text
> !AIVDO,1,1,5,A,8>jR06@0Gwli:QQUP3en?wvlFR06EuOwgwl?wnSwe7wvlOwwsAwwnSGmwvh0,0*51
> ```
> Let us walk through the sentence disassembly:
> 1. `!AIVDO`: Sentence header indicating an internal own-station broadcast transmission.
> 2. `1,1`: Single-sentence message encapsulation (fragment 1 of 1).
> 3. `5`: Sequential sentence message counter.
> 4. `A`: VHF Radio Channel A (AIS 1, 161.975 MHz).
> 5. `8>jR...vh0`: 6-bit ASCII payload (59 characters, representing 354 payload bits).
> 
> Unpacking the leading bits:
> - First 6 bits (`8` = ASCII 56, binary `001000` = decimal 8): **AIS Message ID 8** (Binary Broadcast).
> - Bits 6–7 (`>` = ASCII 62, value 30 = binary `011110`): Repeat indicator `0`.
> - Bits 8–37: MMSI `992509977`. The `99` prefix identifies an Aid to Navigation station; `250` is the Maritime Identification Digit (MID) for the Republic of Ireland.
> - Bits 40–49: DAC = `1` (International Maritime Organization).
> - Bits 50–55: FI = `31` (Circ.289 Meteorological and Hydrographic Data).
> - Bits 56–80 (Longitude): Value $-6.13407^\circ$.
> - Bits 81–104 (Latitude): Value $+53.29493^\circ$ (Dublin Bay approach).
> - Bits 105–121 (Timestamp): Day 29, 23:24 UTC.
> - Remaining sensor fields: All sensors report standard Circ.289 "not available" sentinels (wind speed = 127, air temp = $-102.4^\circ\text{C}$, water level = $30.01\text{ m}$, pressure = $1310\text{ hPa}$), demonstrating an unpopulated AtoN placeholder packet.

> **Try it.**  
> Decode the Circ.289 FI 31 NMEA sentence using the open-source Python library `pyais`:
> ```python
> import pyais
> 
> nmea = "!AIVDO,1,1,5,A,8>jR06@0Gwli:QQUP3en?wvlFR06EuOwgwl?wnSwe7wvlOwwsAwwnSGmwvh0,0*51"
> msg = pyais.decode(nmea)
> 
> print(f"Message ID: {msg.msg_type}")
> print(f"Source MMSI: {msg.mmsi}")
> print(f"DAC: {msg.dac}, FID: {msg.fid}")
> print(f"Position: {msg.lat:.5f} N, {msg.lon:.5f} E")
> print(f"UTC Time: Day {msg.day}, {msg.hour:02d}:{msg.minute:02d} UTC")
> print(f"Wind Speed: {msg.wspeed} kn (127 = N/A)")
> print(f"Water Level: {msg.waterlevel:.2f} m (30.01 = N/A)")
> ```
> Expected output:
> ```text
> Message ID: 8
> Source MMSI: 992509977
> DAC: 1, FID: 31
> Position: 53.29493 N, -6.13407 E
> UTC Time: Day 29, 23:24 UTC
> Wind Speed: 127 kn (127 = N/A)
> Water Level: 30.01 m (30.01 = N/A)
> ```

## Validation, uncertainty & data quality

Errors in environmental transmissions do not simply degrade situational awareness; they introduce quantifiable risk to vessel navigation. An undetected error in an AIS water level broadcast of $+0.5\text{ m}$ in an approach channel navigated by a loaded bulk carrier can induce grounding, catastrophic bottom tearing, and marine oil spills.

### 54.10.1 Sources of physical sensor and transmission error

Environmental data chains experience compounding error vectors across five primary domains:
1. **Hydrodynamic sensor offset:** Estuarine tide gauges experience hydrodynamic drawdown, wave setup, and density stratification in stilling wells, while radar gauges suffer structural thermal expansion.
2. **Datum mismatch:** A water level broadcast reporting $+1.2\text{ m}$ without explicit datum tagging creates dangerous ambiguity. If watch officers assume MLLW while the sensor references MSL or ellipsoidal height, uncorrected offsets of $0.5$ to $2.0\text{ m}$ corrupt under-keel calculations.
3. **Spatial decorrelation:** Headland anemometers at $+65\text{ m}$ elevation report higher speeds than surface winds at vessel bridge level ($+10\text{ m}$); unscaled readings distort aerodynamic drag assessments. Similarly, upriver tide gauges experience phase lag and attenuation relative to harbor entrances.
4. **Latency and staleness:** Sensor polling intervals, backhaul telemetry, and FATDMA schedules introduce latency. If backhaul telemetry drops, daemons without automated expiration continuously rebroadcast stale observations during critical tidal transitions.
5. **Deserialization errors:** While the 16-bit CRC-CCITT catches VDL burst errors with missed-detection probability $P_e \approx 2^{-16} \approx 1.5 \times 10^{-5}$, improper sign-bit handling in software corrupts negative temperatures and levels.

### 54.10.2 Quality control procedures and validation algorithms

Hydrographic networks like NOAA CO-OPS enforce automated QA/QC before base-station injection (NOAA PORTS 2023):
- **Gross range bounds:** Readings outside physical limits ($870$–$1085\text{ hPa}$; $-3.0$ to $+10.0\text{ m}$ MLLW) are substituted with standard "not available" sentinels.
- **Rate-of-change (step) test:** Consecutive 6-minute samples must not exceed hydraulic limits; a water level shift $> 0.3\text{ m}$ in 6 minutes flags acoustic lock loss or sensor failure.
- **Neighbor check:** Redundant sensors and adjacent channel stations are cross-compared to isolate localized drift.
- **Watchdog timeout:** Daemons enforce strict 12-to-18-minute expiration timers, purging cached values if telemetry fails.

### Data freshness rule of thumb

Never apply an AIS water level correction to an electronic chart sounding unless the broadcast transmission timestamp is less than 15 minutes old, the station location is within 5 nautical miles (9.3 km) of the vessel, and the vertical datum is explicitly confirmed to match the chart sounding datum.*

> **Threat model.**  
> - **Attacker profile:** Malicious actor with software-defined radio (**SDR**) capabilities (e.g., HackRF, USRP) within coastal VHF range ([Chapter 33](ch33-hardware-and-sdr.md); [Chapter 58](ch58-threat-model.md)).  
> - **Attack vector:** Transmission of forged AIS Message 8 binary broadcast packets claiming false DAC/FI identities (e.g., fabricating an IMO Circ.289 FI 31 packet or USCG DAC 367 FI 33 packet from a spoofed shore base station MMSI).  
> - **Capability & payload:** The attacker broadcasts false water level readings artificially elevated by $+1.5\text{ m}$ above actual physical tide, or false air-gap clearances beneath a commercial bridge.  
> - **Operational impact:** If an automated under-keel clearance system or bridge display ingests the spoofed data without cross-validation, a deep-draft vessel enters a shallow channel under the false assumption of adequate water depth, resulting in high-speed grounding or bridge allision ([Chapter 59](ch59-spoofing.md)).  
> - **Mitigations:**  
>   1. *Cryptographic signing:* Deployment of VDES with public-key digital signatures (IHO S-100 Part 15 / ITU-R M.2092).  
>   2. *Base station authentication:* Verification of transmitting MMSI against shore base station registries; rejecting ASMs originating from mobile Class A or Class B MMSIs.  
>   3. *Plausibility cross-checking:* Bridge software must validate received water levels against astronomical tide predictions computed locally on the ECDIS. Readings deviating by more than the maximum historical meteorological storm surge (e.g., $> 2.0\text{ m}$) must trigger high-priority bridge alarms.

> **Legal note.**  
> *Liability for environmental transmission errors.*  
> Under international maritime law and national tort frameworks (e.g., the United States Suits in Admiralty Act and Federal Tort Claims Act), government agencies transmitting hydrographic information owe a duty of reasonable care in the collection, formatting, and dissemination of navigation safety aids. However, published national guidelines uniformly specify that real-time environmental broadcasts over AIS constitute advisory aids to navigation and do not relieve the vessel master or pilot of the legal obligation under SOLAS Chapter V and Rule 7 of the International Regulations for Preventing Collisions at Sea (**COLREGs**) to utilize "all available means" to ascertain vessel safety. Manufacturers of navigation software that parse ASMs and present them on bridge displays face severe product liability exposure if software formatting errors invert sign bits (e.g., reporting a negative tide as a positive water level) or misidentify reference datums, directly contributing to a marine casualty.

## Software

**Open source:**
- `pyais` (Python, MIT License): Multi-platform decoding and encoding library supporting IMO SN.1/Circ.289 (FI 26, FI 31), legacy Circ.236 (FI 11), USCG DAC 367 (FI 33), and European Inland AIS DAC 200 (FI 24). Caveat: Does not validate physical plausibility of decoded fields; passes sentinels through as unmasked numerical floats unless explicitly handled by application code.
- `libais` (C++ with Python bindings, Apache 2.0 License): Foundational high-performance decoding library authored by Kurt Schwehr. Caveat: Contains legacy structural discrepancies on certain variable-length ASM payloads; development shifted primarily to maintenance mode.
- `OpenCPN` (C++, GPL v2+): Popular open-source chartplotter and navigational display. Supports AIS target decoding and displays basic AIS AtoN markers. Caveat: Lacks native graphical rendering for Circ.289 / DAC 367 environmental sensor vectors; requires third-party plugins to visualize real-time water levels.

**Free but closed:**
- `NOAA CO-OPS Data Retrieval Tools` (Web / REST API, Public Domain / US Government): Provides real-time and historical hydrographic data feeds, harmonic tidal predictions, and quality-controlled PORTS observations. Caveat: External web APIs require continuous IP connectivity, which is unavailable over raw marine VHF installations without satellite or cellular bridges.

**Commercial:**
- `Qastor` (QPS / Saab, Commercial): High-end Portable Pilot Unit navigation package used by commercial pilots worldwide. Natively ingests and renders IMO Circ.289, USCG DAC 367, and Seaway DAC 316 environmental messages, providing dynamic bathymetry and air-gap alerts. Caveat: High licensing cost; restricted to professional pilotage markets.
- `Transas Navi-Sailor / Wärtsilä Voyage ECDIS` (Commercial): Type-approved ECDIS platform. Supports select regional AIS binary message decoders depending on software version and customer licensing flags. Caveat: Legacy installed bridge base requires manufacturer firmware upgrades to parse modern S-100 dynamic layers.

## Standards & guides

- **IMO SN/Circ.236 (2004):** *Guidance on the Use of the Specification of Application-Specific Messages to the Maritime Mobile Service*. Initial trial standard defining DAC 1 FI 11 (now deprecated).
- **IMO SN.1/Circ.289 (2010):** *Guidance on the Use of AIS Application-Specific Messages*. The primary international baseline defining DAC 1 FI 31 (met/hydro), FI 26 (modular environmental), and FI 21 (ship weather).
- **IMO MSC.1/Circ.1473 (2014):** *Policy on the Use of AIS Application-Specific Messages*. Formal IMO policy restricting ASM traffic to protect VDL slot availability.
- **ITU-R M.1371-5 (2014):** *Technical Characteristics for an Automatic Identification System Using Time Division Multiple Access in the VHF Maritime Mobile Frequency Band*. Defines the physical layer, TDMA link layer, and transport structures for Messages 6, 8, 25, and 26.
- **IALA Guideline 1082 (2011):** *An Overview of AIS*. Technical guidance on base station and AtoN deployment, slot scheduling, and ASM operations.
- **IHO S-100 Edition 5.2.1 (2025):** *Universal Hydrographic Data Model*. The overarching geospatial data framework defining data registers, portrayal, and encryption for next-generation electronic charting.
- **IHO S-104 Edition 1.1.0 (2023):** *Water Level Information for Surface Navigation Product Specification*. Defines HDF5-encoded dynamic water levels for ECDIS integration.
- **IHO S-111 Edition 1.2.0 (2023):** *Surface Currents Product Specification*. Defines gridded and point current vector datasets for navigation displays.
- **IEC 61174 Edition 4.0 (2015):** *ECDIS - Operational and Performance Requirements, Methods of Testing and Required Test Results*. Governs bridge electronic chart systems and mandates message decoding compliance.
- **IEC 62288 Edition 3.0 (2021):** *Presentation of Navigation-Related Information on Shipborne Navigational Displays*. Defines standardized symbols, operational icons, and display ergonomics for bridge displays.

## Pitfalls

1. **Assuming all ECDIS units display environmental ASMs** → IEC 61174 type-approval did not historically mandate decoding Message 8 ASMs → Maintain redundant voice or PPU displays; do not rely solely on certified ECDIS for live environmental data.
2. **Neglecting the vertical datum of water level transmissions** → Legacy messages (Circ.236 FI 11) omitted datum tags, and mariners assume MLLW or LAT → Use modern messages with explicit datum identifiers (DAC 367 FI 33, S-104) and verify ENC sounding datum before applying tidal offsets.
3. **Treating "not available" sentinels as numerical values** → Unchecked bitfields decode sentinel `127` as a $127\text{ kn}$ wind or `4001` as a $+40.01\text{ m}$ surge → Explicitly map documented sentinels (`127`, `360`, `511`, `4001`) to null values in decoding routines.
4. **Inverting signed values during deserialization** → Using unsigned bit parsing on two's-complement fields turns negative temperatures and sub-datum water levels into large positive values → Enforce signed extraction on specified fields and validate against synthetic negative test vectors.
5. **Confusing bridge air gap with vessel air draught** → Inconsistent software labels lead watch officers to invert clearances ($	ext{Air Gap} - 	ext{Air Draught}$) → Clearly differentiate instantaneous vertical bridge opening from vessel masthead height.
6. **Overloading the VDL with high-frequency multi-slot messages** → Schedulers set 5-slot ASM bursts every 30 seconds, congesting TDMA cells → Limit environmental cadences to 6–12 minutes per MSC.1/Circ.1473 and migrate dense data to VDES.
7. **Broadcasting stale data across failed telemetry backhauls** → Transmission daemons without timeouts rebroadcast cached water levels after sensor outages → Implement a 12-to-18-minute watchdog that purges cached data and broadcasts sentinel values when telemetry drops.
8. **Ignoring spatial decorrelation of point observations** → Anemometers on high bluffs or tide gauges miles upriver do not reflect channel conditions → Scale elevation winds logarithmically and use hydrodynamic models rather than distant point gauges for precision pilotage.

## Key takeaways

- **AIS is an operational environmental carrier:** Application-Specific Messages broadcast across the VHF Data Link deliver physical oceanographic and meteorological sensor observations directly to vessels within radio range without requiring satellite or cellular connections.
- **The standards transitioned from monolithic to modular:** The maritime domain evolved from rigid, multi-slot monolithic reports (IMO SN/Circ.236 FI 11) to refined point broadcasts (IMO SN.1/Circ.289 FI 31) and flexible, modular sensor packets (IMO SN.1/Circ.289 FI 26; USCG DAC 367 FI 33).
- **Regional systems led practical implementation:** Systems such as the St. Lawrence Seaway (DAC 316/366), European Inland AIS (DAC 200), and US NOAA PORTS (DAC 367) deployed operational environmental broadcasts years before international bridge displays caught up.
- **The bridge presentation gap remains the primary bottleneck:** While transponders receive Message 8 environmental packets, legacy type-approved ECDIS units routinely drop them or bury them in diagnostic text menus due to historically narrow IEC 61174 display mandates.
- **Portable Pilot Units bridge the operational divide:** Maritime pilots overcome shipboard display deficiencies by using PPUs connected to pilot plugs to render real-time water levels, bridge clearances, and current vectors.
- **Buoy-mounted AtoN face severe power and motion constraints:** AIS AtoN units carrying oceanographic sensors must dynamically throttle transmission cadences to conserve solar battery banks and must mathematically decouple buoy heave and roll from wind and current vectors.
- **Commercial ships act as weather sensors via VOS:** IMO Circ.289 FI 21 enables automated shipboard weather stations to transmit surface weather observations to national meteorological services across the coastal VDL.
- **S-100 and VDES represent the future:** High-resolution dynamic water levels (S-104) and surface currents (S-111) require multi-megabyte HDF5 datasets that exceed legacy AIS VDL capacity, necessitating the transition to wideband VDES data channels and dual-fuel S-100 ECDIS.

## References

- CESNI (2021). *Standard Inland AIS — Edition 2021/1* (Standard CESNI/ES-RIS (2021)). Strasbourg: Comité Européen pour l'Élaboration de Standards dans le Domaine de la Navigation Intérieure.
- Gonin, I. M., Johnson, G. W., Shalaev, R., Tetreault, B., Alexander, L. (2009). USCG Development, Test and Evaluation of AIS Binary Messages for Enhanced VTS Operations. In *Proceedings of the 2009 International Technical Meeting of the Institute of Navigation*, pages 761–770. Anaheim, CA: Institute of Navigation.
- IALA (2011). *An Overview of AIS* (IALA Guideline 1082, Edition 1). Saint-Germain-en-Laye: International Association of Marine Aids to Navigation and Lighthouse Authorities.
- IALA (2019). *The Use of the Technical Standards for VHF Data Exchange System (VDES)* (IALA Guideline 1139). Saint-Germain-en-Laye: International Association of Marine Aids to Navigation and Lighthouse Authorities.
- IEC (2015). *Maritime Navigation and Radiocommunication Equipment and Systems — Electronic Chart Display and Information System (ECDIS) — Operational and Performance Requirements, Methods of Testing and Required Test Results* (IEC 61174:2015 Edition 4.0). Geneva: International Electrotechnical Commission.
- IEC (2021). *Maritime Navigation and Radiocommunication Equipment and Systems — Presentation of Navigation-Related Information on Shipborne Navigational Displays — General Requirements, Methods of Testing and Required Test Results* (IEC 62288:2021 Edition 3.0). Geneva: International Electrotechnical Commission.
- IHO (2023). *Water Level Information for Surface Navigation Product Specification* (Special Publication S-104 Edition 1.1.0). Monaco: International Hydrographic Organization.
- IHO (2023). *Surface Currents Product Specification* (Special Publication S-111 Edition 1.2.0). Monaco: International Hydrographic Organization.
- IHO (2025). *Universal Hydrographic Data Model* (Special Publication S-100 Edition 5.2.1). Monaco: International Hydrographic Organization.
- IMO (2004). *Guidance on the Use of the Specification of Application-Specific Messages to the Maritime Mobile Service* (Circular SN/Circ.236). London: International Maritime Organization.
- IMO (2010). *Guidance on the Use of AIS Application-Specific Messages* (Circular SN.1/Circ.289). London: International Maritime Organization.
- IMO (2014). *Policy on the Use of AIS Application-Specific Messages* (Circular MSC.1/Circ.1473). London: International Maritime Organization.
- ITU-R (2014). *Technical Characteristics for an Automatic Identification System Using Time Division Multiple Access in the VHF Maritime Mobile Frequency Band* (Recommendation ITU-R M.1371-5). Geneva: International Telecommunication Union.
- NOAA (2023). *Physical Oceanographic Real-Time System (PORTS): Program Description and Standards* (Special Publication NOS CO-OPS 090). Silver Spring, MD: National Oceanic and Atmospheric Administration.
- Schwehr, K., Alexander, L. (2007). Specification Format for AIS Binary Messages for Providing Hydrographic-Related Information. In *Proceedings of the U.S. Hydrographic Conference (US Hydro 2007)*. Norfolk, VA: The Hydrographic Society of America.
- SLSDC (2010). *AIS Data Messaging Formats and Specifications* (Technical Specification Revision 4.1). Washington, DC and Cornwall, ON: Saint Lawrence Seaway Development Corporation and St. Lawrence Seaway Management Corporation.
- WMO (2021). *International List of Selected, Supplementary and Auxiliary Ships* (Operational Publication WMO-No. 47). Geneva: World Meteorological Organization.
