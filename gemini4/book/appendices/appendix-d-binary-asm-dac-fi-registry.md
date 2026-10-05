# Appendix D: International & Regional Binary Application-Specific Messages (DAC/FI) Registry

> **Purpose:** This appendix provides the authoritative engineering lookup registry for AIS Binary Application-Specific Messages (ASMs) transmitted inside **ITU-R M.1371-5 Messages 6, 8, 25, and 26**. Every entry lists the **Designated Area Code (`DAC`, 10 bits)**, **Functional Identifier (`FI`, 6 bits)**, combined 16-bit **`AppID` (`(DAC << 6) | FI`)**, valid **Message Envelope(s)**, **Official Title**, **Governing Standard/Circular**, **Bit-Length Specification** (including the 56-bit Message 8 or 88-bit Message 6 header), **Operational Status**, and the corresponding C++ decoder module in **Kurt Schwehr's [`libais`](https://github.com/schwehr/libais)**.

---

## D.1 Computing the 16-Bit Application Identifier (`AppID`)

In ITU-R M.1371-5, the 16-bit Application Identifier (`AppID`) is packed MSB-first as a 10-bit `DAC` (`0–1023`) followed immediately by a 6-bit `FI` (`0–63`):

$$\text{AppID}_{16} = (\text{DAC} \ll 6) \mid \text{FI} = 64 \times \text{DAC} + \text{FI}$$

| Message Envelope | `DAC` 0-Based Bit Slice | `FI` 0-Based Bit Slice | Binary Payload Start Bit | Max Total Bits (Slots) |
|---|---|---|---|---|
| **Message 6 (Addressed)** | `72–81` (`10 bits`) | `82–87` (`6 bits`) | `88` | `1,008 bits` (`5 slots`) |
| **Message 8 (Broadcast)** | `40–49` (`10 bits`) | `50–55` (`6 bits`) | `56` | `1,008 bits` (`5 slots`) |
| **Message 25 (1-Slot, Broadcast + `AppID`)** | `40–49` (`10 bits`) | `50–55` (`6 bits`) | `56` | `168 bits` (`1 slot`) |
| **Message 25 (1-Slot, Addressed + `AppID`)** | `72–81` (`10 bits`) | `82–87` (`6 bits`) | `88` | `168 bits` (`1 slot`) |
| **Message 26 (Multi-Slot, Broadcast + `AppID`)** | `40–49` (`10 bits`) | `50–55` (`6 bits`) | `56` | `1,064 bits` (`5 slots`, trailing 20-bit Comm State) |

---

## D.2 International (`DAC = 1`) Binary ASM Registry (ITU-R M.1371, IMO SN/Circ.236 & SN.1/Circ.289)

`DAC = 1` is reserved globally for international messages standardized by the **International Telecommunication Union (ITU-R)** and the **International Maritime Organization (IMO)**.

### Table D.1: Complete Registry of `DAC = 1` (International / IMO) Application-Specific Messages

| DAC | FI | `AppID` (Dec / Hex) | Msg Type | Official Message Title | Governing Circular / Standard | Total Bit Length (Incl. Header) | Operational Status & `libais` Module |
|---|---|---|---|---|---|---|---|
| `1` | `0` | `64` (`0x0040`) | `6`, `8` | **Text Telegram using 6-Bit ASCII** | ITU-R M.1371-5 Annex 2 | `104–1,008` (Msg 6)<br/>`72–1,008` (Msg 8) | **Active** (`ais6.cpp`, `ais8_1_0.cpp`) — Carries 11-bit Ack/Seq + free 6-bit text. |
| `1` | `2` | `66` (`0x0042`) | `6` | **Interrogation for a Specific FM (FI)** | ITU-R M.1371-5 Annex 2 | `104` (`1 slot`) | **Active** (`ais6.cpp`) — Requests target MMSI to reply with requested `DAC + FI`. |
| `1` | `3` | `67` (`0x0043`) | `6` | **Capability Interrogation** | ITU-R M.1371-5 Annex 2 | `104` (`1 slot`) | **Active** (`ais6.cpp`) — Queries supported FIs of a target `DAC` on a vessel. |
| `1` | `4` | `68` (`0x0044`) | `6` | **Capability Interrogation Reply** | ITU-R M.1371-5 Annex 2 | `232` (`2 slots`) | **Active** (`ais6.cpp`) — 128-bit bitmap (2 bits per FI `0..63`) reporting supported FIs. |
| `1` | `5` | `69` (`0x0045`) | `6` | **Application Ack to an Addressed Binary Message** | ITU-R M.1371-5 / SN.1/Circ.289 | `136` (`1 slot`) | **Active** (`ais6.cpp`) — Application-layer ACK returning `ack_dac`, `ack_fi`, and 11-bit `seq_num`. |
| `1` | `11` | `75` (`0x004B`) | `8` | **Meteorological and Hydrographic Data (Trial v1)** | IMO SN/Circ.236 (2004) | `352` (`2 slots`) | **Deprecated / Discontinued (Jan 1, 2013)** (`ais8_1_11.cpp`) — Superseded by `DAC=1, FI=31`; had inverted Lat/Lon order and $0.1\text{ m}$ tide steps. |
| `1` | `12` | `76` (`0x004C`) | `6` | **Dangerous Cargo Indication (Trial)** | IMO SN/Circ.236 (2004) | `360` (`2 slots`) | **Withdrawn (Jan 1, 2013)** (`ais6.cpp`) — Replaced by shore-based FAL/Single Window reporting (`FI=25`). |
| `1` | `13` | `77` (`0x004D`) | `8` | **Fairway Closed (Trial)** | IMO SN/Circ.236 (2004) | `472` (`3 slots`) | **Withdrawn (Jan 1, 2013)** (`ais8_1_13.cpp`) — Superseded by `DAC=1, FI=22` (Area Notice `notice_type=18`). |
| `1` | `14` | `78` (`0x004E`) | `6`, `8` | **Tidal Window (Trial v1)** | IMO SN/Circ.236 (2004) | `376` (`2 slots`, 3 windows) | **Deprecated (Jan 1, 2013)** (`ais8_1_14.cpp`) — Superseded by `DAC=1, FI=32`. |
| `1` | `15` | `79` (`0x004F`) | `6` | **Extended Ship Static and Voyage Related Data (Trial)** | IMO SN/Circ.236 (2004) | `112` (`1 slot`) | **Deprecated (Jan 1, 2013)** (`ais8_1_15.cpp`) — Reported air draught ($0.1\text{ m}$); superseded by `DAC=1, FI=24`. |
| `1` | `16` | `80` (`0x0050`) | `6`, `8` | **Number of Persons on Board** | IMO SN/Circ.236 & SN.1/Circ.289 | `136` (Msg 6) / `104` (Msg 8) (`1 slot`) | **Active** (`ais8_1_16.cpp`) — 13-bit count (`0–8,190`, `8191`=N/A) for SAR operations. |
| `1` | `17` | `81` (`0x0051`) | `8` | **VTS-Generated / Synthetic Targets (Trial v1)** | IMO SN/Circ.236 (2004) | `120 + 120N` ($N \in 1..4$, `1–3 slots`) | **Deprecated (Jan 1, 2013)** (`ais8_1_17.cpp`) — Superseded by `DAC=1, FI=29` (Target Description). |
| `1` | `18` | `82` (`0x0052`) | `6` | **Clearance Time to Enter Port** | IMO SN.1/Circ.289 (2010) | `360` (`2 slots`) | **Active** (`ais6.cpp`) — Port clearance timestamp, berth name, and position. |
| `1` | `19` | `83` (`0x0053`) | `8` | **Marine Traffic Signal** | IMO SN.1/Circ.289 (2010) | `216` (`2 slots`) | **Active** (`ais8_1_19.cpp`) — Station name, position, IALA signal status (`1–7`), next signal, and time. |
| `1` | `20` | `84` (`0x0054`) | `6` | **Berthing Data** | IMO SN.1/Circ.289 (2010) | `392` (`2 slots`) | **Active** (`ais6.cpp`) — Berth length, water depth ($0.1\text{ m}$), mooring position, services availability, and berth name. |
| `1` | `21` | `85` (`0x0055`) | `8` | **Weather Observation Report from Ship** | IMO SN.1/Circ.289 (2010) | `360` (`2 slots`) | **Active** (`ais8_1_21.cpp`) — Subtype `0`: Shipboard Met/Hydro sensor report; Subtype `1`: WMO FM 13 synoptic report. |
| `1` | `22` | `86` (`0x0056`) | `6`, `8` | **Area Notice** | IMO SN.1/Circ.289 (2010) | `111 + 87N` (Msg 8, $N \in 1..9$, `2–5 slots`) | **Active** (`ais8_1_22.cpp` / `ais-area-notice`) — Dynamic circles, rectangles, sectors, polylines, polygons, and text. |
| `1` | `23` | `87` (`0x0057`) | `8` | **Environmental** (RTCM / IMO Multi-Sensor Report) | IMO SN.1/Circ.289 (adapted from RTCM SC-121) | `56 + 112N` ($N \in 1..8$ Sensor Reports) | **Active** (`ais8_1_26.cpp` family) — Modular 112-bit sensor blocks (Site Loc, Wind, Water Level, 2D/3D Current, Waves, Salinity, Weather, Air Gap). |
| `1` | `24` | `88` (`0x0058`) | `8` | **Extended Ship Static and Voyage Related Data** | IMO SN.1/Circ.289 (2010) | `168` (`1 slot`) | **Active** (`ais8_1_24.cpp`) — Static draught, **Air Draught** ($0.1\text{ m}$, `0–819.0 m`), Last Port, Next 2 Ports (UN/LOCODE), SOLAS equipment status, Ice Class, and Shaft HP. |
| `1` | `25` | `89` (`0x0059`) | `6` | **Dangerous Cargo Indication** | IMO SN.1/Circ.289 (2010) | `168 + 17N` ($N \in 0..48$) | **Active** (`ais6.cpp`) — Total dangerous cargo tonnage/units and cargo category array. |
| `1` | `26` | `90` (`0x005A`) | `6`, `8` | **Environmental** (IMO SN.1/Circ.289 Consolidated Sensor Array) | IMO SN.1/Circ.289 (2010) | `56 + 112N` (Msg 8) / `88 + 112N` (Msg 6), $N \in 1..8$ | **Active** (`ais8_1_26.cpp`) — Packs 1 to 8 self-describing 112-bit `SensorReport` records (`report_type` `0..11`, incl. `type=2` Water Level & `type=9` Air Gap/Draught). |
| `1` | `27` | `91` (`0x005B`) | `6`, `8` | **Route Information** | IMO SN.1/Circ.289 (2010) | `149 + 55N` (Msg 8, $N \in 1..16$ waypoints) | **Active** (`ais8_1_27.cpp`) — Broadcasts recommended, mandatory, or own-ship intended route waypoints. |
| `1` | `28` | `92` (`0x005C`) | `6` | **Route Information (Addressed)** | IMO SN.1/Circ.289 (2010) | `181 + 55N` (Msg 6, $N \in 1..16$ waypoints) | **Active** (`ais6.cpp`) — Addressed VTS-to-ship route advice or clearance. |
| `1` | `29` | `93` (`0x005D`) | `8` | **Text Description** | IMO SN.1/Circ.289 (2010) | `72–1,008` (`1–5 slots`) | **Active** (`ais8_1_29.cpp`) — Links long free-text descriptions to a prior ASM via 10-bit `link_id`. |
| `1` | `30` | `94` (`0x005E`) | `8` | **VTS-Generated / Synthetic Targets (v2)** | IMO SN.1/Circ.289 (2010) | `56 + 128N` ($N \in 1..7$ targets) | **Active** (`ais8_1_30.cpp`) — Shore radar/EO target broadcast onto VDL by VTS. |
| `1` | `31` | `95` (`0x005F`) | `8` | **Meteorological and Hydrographic Data (v2)** | IMO SN.1/Circ.289 (2010) | **`360`** (`2 slots`, exact $60 \times 6$ bits) | **Active** (`ais8_1_31.cpp`) — Global standard for tide ($0.01\text{ m}$), currents, wind, waves, air/water temp, pressure, visibility, salinity, and ice. |
| `1` | `32` | `96` (`0x0060`) | `6`, `8` | **Tidal Window (v2)** | IMO SN.1/Circ.289 (2010) | `112 + 93N` (Msg 6) / `80 + 93N` (Msg 8), $N \in 1..3$ | **Active** (`ais8_1_32.cpp`) — Safe tidal transit windows (`from_hour/min`, `to_hour/min`, current speed/dir) at up to 3 channel waypoints. |
| `1` | `40` | `104` (`0x0068`) | `8` | **Number of Persons on Board (Extended)** | IMO / IALA e-Nav Trial | `168` (`1 slot`) | **Trial** — Extended breakdown of crew, passengers, and infants. |

---

## D.3 European Inland AIS (`DAC = 200`) Registry (CCNR / CESNI ES-TRIN)

`DAC = 200` is assigned across European inland waterways (Rhine, Danube, Elbe, Main, Moselle, Seine, and Benelux canals) under the **CESNI ES-TRIN (European Standard laying down Technical Requirements for Inland Navigation vessels)** and **EU River Information Services (RIS) Directive 2005/44/EC**.

### Table D.2: Registry of `DAC = 200` (European Inland AIS) Application-Specific Messages

| DAC | FI | `AppID` (Dec / Hex) | Msg Type | Official Inland AIS Message Title | Governing Standard | Total Bit Length (Incl. Header) | Key Fields, Status & `libais` Module |
|---|---|---|---|---|---|---|---|
| `200` | `10` | `12810` (`0x320A`) | `8` | **Inland Ship Static and Voyage Related Data** | CESNI ES-TRIN / CCNR Inland AIS | `168` (`1 slot`) | **Active (Mandatory)** (`ais8_200.cpp`) — 8-char European Vessel ID (`ENI`), Length ($0.1\text{ m}$), Beam ($0.1\text{ m}$), **ERI Ship/Convoy Type** (`8000–8690`), **Hazardous Cargo Blue Cones (`0–3`)**, Static Draught ($0.01\text{ m}$), Loaded/Unloaded state, and sensor quality flags. |
| `200` | `21` | `12821` (`0x3215`) | `6` | **ETA at Lock / Bridge / Terminal** | CESNI ES-TRIN / CCNR Inland AIS | `248` (`2 slots`) | **Active** (`ais6.cpp`) — Ship-to-shore report of Country Code (2 chars), UN Location/Facility Code (5 chars), Terminal/Lock Section (5 chars), ETA (`month, day, hour, min`), Assisting Tugs (`0–7`), and **Air Draught** ($0.01\text{ m}$, `0–40.00 m`). |
| `200` | `22` | `12822` (`0x3216`) | `6` | **RTA (Requested Time of Arrival) at Lock / Bridge / Terminal** | CESNI ES-TRIN / CCNR Inland AIS | `232` (`2 slots`) | **Active** (`ais6.cpp`) — Shore-to-ship VTS/lock response assigning an official RTA (`month, day, hour, min`) and Lock/Bridge Status (`0`=operational, `1`=limited, `2`=closed). |
| `200` | `23` | `12823` (`0x3217`) | `8` | **EMMA Warning (European Multiservice Meteorological Awareness)** | CESNI ES-TRIN / CCNR Inland AIS | `256` (`2 slots`) | **Active** (`ais8_200.cpp`) — Start/End UTC Date & Time, Start/End River Hectometer (`km * 10`), Weather Type (`1`=wind, `2`=rain, `3`=snow/ice, `4`=thunderstorm, `5`=fog, `6`=low temp, `7`=high temp, `8`=flood), Min/Max Value, Classification (`1`=slight, `2`=medium, `3`=strong), and Wind Direction. |
| `200` | `24` | `12824` (`0x3218`) | `8` | **Water Level** | CESNI ES-TRIN / CCNR Inland AIS | `168` (`1 slot`) | **Active** (`ais8_200.cpp`) — 2-char ISO Country Code (`DE`, `NL`, `AT`, `FR`) + up to **4 Gauge Records** (each 11-bit Gauge ID + 14-bit signed Water Level in $0.01\text{ m}$ steps relative to gauge datum). |
| `200` | `40` | `12840` (`0x3228`) | `8` | **Signal Status** | CESNI ES-TRIN / CCNR Inland AIS | `168` (`1 slot`) | **Active** (`ais8_200.cpp`) — Signal Station Position (Lon/Lat), Signal Form (`1–4`), Orientation (`0–359°`), Direction of Impact (`1`=upstream, `2`=downstream, `3`=both), and 30-bit Light Status Array (9 signals $\times 3\text{ bits}$: red/green/white/yellow/flashing). |
| `200` | `44` | `12844` (`0x322C`) | `6` | **Waste Discharge / Reception Notification** | CCNR / CDNI Inland Convention | `168` (`1 slot`) | **Regional Trial** — Electronic bilge/waste reception notification on the Rhine. |
| `200` | `55` | `12855` (`0x3237`) | `6`, `8` | **Number of Persons on Board (Inland)** | CESNI ES-TRIN / CCNR Inland AIS | `168` (`1 slot`) | **Active** (`ais8_200.cpp`) — 13-bit Passengers (`0–8,190`), 8-bit Crew (`0–254`), and 8-bit Support Personnel (`0–254`) for river cruise ships and ferries. |

---

## D.4 Canadian & US St. Lawrence Seaway, Great Lakes, and USCG / NOAA (`DAC = 316` & `DAC = 366`) Registry

In North America, **`DAC = 316` (Canada)** and **`DAC = 366` (United States)** are used by:
1. The bi-national **St. Lawrence Seaway Traffic Management System (SLSMC / GLS)** between Montreal and Lake Erie, and
2. The **United States Coast Guard (USCG)** and **NOAA PORTS®** across US coastal harbors, approaches, and marine sanctuaries.

### Table D.3: Registry of `DAC = 316` (Canada) and `DAC = 366` (United States) Binary ASMs

| DAC | FI | `AppID` (Dec / Hex) | Msg Type | Official Message Title | Governing Authority / Standard | Total Bit Length (Incl. Header) | Key Fields, Status & `libais` Module |
|---|---|---|---|---|---|---|---|
| `316` / `366` | `1` | `20225` / `23425` (`0x4F01` / `0x5B81`) | `8` | **St. Lawrence Seaway: Meteorological / Wind Information** | SLSMC / GLS Seaway AIS Spec | `216` (`2 slots`) | **Active** (`ais8_366.cpp`) — Up to 2 weather station reports per message: UTC time, 12-char Station ID, 10-min Average Wind Speed/Direction, and Peak Gust Speed/Direction. |
| `316` / `366` | `1` | `20225` / `23425` (`0x4F01` / `0x5B81`) | `6` | **St. Lawrence Seaway: Lockage Order (Schedule)** | SLSMC / GLS Seaway AIS Spec | `552` (`3 slots`) | **Active** — Addressed to vessels approaching a Seaway lock; contains 6-char Lock ID, UTC timestamp, and up to 6 scheduled vessels (15-char Vessel Name, Direction, and ETA). |
| `316` / `366` | `2` | `20226` / `23426` (`0x4F02` / `0x5B82`) | `8` | **St. Lawrence Seaway: Water Level** | SLSMC / GLS Seaway AIS Spec | `216` (`2 slots`) | **Active** (`ais8_366.cpp`) — Up to 6 gauge reports per message: Station ID, Water Level ($0.01\text{ m}$ steps), and Reference Datum (`0`=Chart Datum, `1`=IGLD 1985). |
| `316` / `366` | `2` | `20226` / `23426` (`0x4F02` / `0x5B82`) | `6` | **St. Lawrence Seaway: Vessel Lock ETA & Clearance** | SLSMC / GLS Seaway AIS Spec | `280` (`2 slots`) | **Active** — Addressed lock clearance time and dynamic maximum permissible draught. |
| `316` / `366` | `3` | `20227` / `23427` (`0x4F03` / `0x5B83`) | `8` | **St. Lawrence Seaway: Hydrological / Water Flow** | SLSMC / GLS Seaway AIS Spec | `216` (`2 slots`) | **Active** — Dam and reach discharge flow rates in $\text{m}^3/\text{s}$ (`0–16,382 m³/s`) at up to 6 stations. |
| `316` / `366` | `32` | `20256` / `23456` (`0x4F20` / `0x5BA0`) | `8` | **St. Lawrence Seaway: Version & System Status** | SLSMC / GLS Seaway AIS Spec | `136` (`1 slot`) | **Active** — Broadcasts Seaway ASM protocol version and VTS sector health. |
| `366` | `22` | `23446` (`0x5B96`) | `6`, `8` | **USCG Area Notice (`ais-area-notice`)** | USCG / RTCM 12301.1 / Whale Alert | `111 + 87N` (Harmonized)<br/>`111 + 93N` (Pre-2013 Legacy) | **Active** (`ais8_366_22.cpp` / `ais-area-notice`) — USCG dynamic right-whale slow zones, SAR areas, and security zones. Harmonized with IMO `DAC=1, FI=22` (87-bit sub-areas). |
| `366` | `26` / `31` | `23450` / `23455` (`0x5B9A` / `0x5B9F`) | `8` | **USCG / NOAA PORTS® Environmental & Air Gap** | RTCM Standard 12301.1 / NOAA CO-OPS | `56 + 112N` (`FI=26`) or `360` (`FI=31`) | **Active** (`noaadata` / `ais8_1_26.cpp` / `ais8_1_31.cpp`) — 6-minute real-time tide gauges, ADCP currents, bridge air gap, and harbor meteorology. |
| `366` | `56` | `23480` (`0x5BB8`) | `6`, `8` | **USCG Encrypted AIS (EAIS) — Blue Force Position Report** | USCG / DoD Tactical Spec | `256` / `328` (`2 slots`) | **Active (Restricted/Encrypted)** (`ais8_366_56.cpp`) — Carries IV + AES/Type-1 encrypted cutter/patrol boat position vector and authentication tag. |
| `366` | `57` | `23481` (`0x5BB9`) | `6`, `8` | **USCG Encrypted AIS (EAIS) — Blue Force Static / Identity** | USCG / DoD Tactical Spec | `328`–`424` (`2–3 slots`) | **Active (Restricted/Encrypted)** — Encrypted tactical call sign, hull name, and mission status for Command21 / SeaVision / GCCS-M. |

---

## D.5 United Kingdom & Ireland General Lighthouse Authorities (`DAC = 232` & `DAC = 235`) Registry

In the United Kingdom and Ireland, the three **General Lighthouse Authorities (GLAs)**—**Trinity House** (England, Wales, Channel Islands, Gibraltar), the **Northern Lighthouse Board** (Scotland and Isle of Man), and the **Commissioners of Irish Lights** (Ireland)—use **`DAC = 232` and `DAC = 235`** over AIS Message 6 and Message 8 to monitor and control offshore buoys, racons, and lighthouses.

### Table D.4: Registry of `DAC = 232` and `DAC = 235` (UK & Ireland GLA) Binary ASMs

| DAC | FI | `AppID` (Dec / Hex) | Msg Type | Official GLA Message Title | Governing Authority | Total Bit Length (Incl. Header) | Bit-Level Telemetry Fields & `libais` Module |
|---|---|---|---|---|---|---|---|
| `232` / `235` | `10` | `14858` / `15050` (`0x3A0A` / `0x3ACA`) | `6`, `8` | **GLA Aid to Navigation (AtoN) Monitoring Data** | UK/Ireland GLA (Trinity House / NLB / CIL) | `136` (Msg 6) / `104` (Msg 8) (`1 slot`) | **Active** (`ais8_235_10.cpp`, `ais6.cpp`) —<br/>• **Analog Internal Voltage** (`10 bits`, $0.05\text{ V}$ steps, $0.05\text{–}51.15\text{ V}$)<br/>• **Analog External Voltage #1 & #2** (`2 x 10 bits`, solar/wind/battery bank in $0.05\text{ V}$ steps)<br/>• **Internal Status Bits** (`5 bits`: Racon status [`0–3`], Main Light status [`0`=No, `1`=ON, `2`=OFF, `3`=Error], Health alarm bit)<br/>• **External Digital Inputs** (`8 bits`: bilge flood, hatch tamper, reserve lantern, foghorn)<br/>• **Off-Position Status** (`1 bit`: `0`=On position, `1`=Drifted off station). |
| `232` / `235` | `20` | `14868` / `15060` (`0x3A14` / `0x3AD4`) | `6` | **GLA AtoN Remote Control & Configuration Command** | UK/Ireland GLA | `136`–`168` (`1 slot`) | **Active** — Addressed telecommand from GLA shore station to toggle emergency wreck lanterns, racon modes, or reporting intervals. |

---

## D.6 Other Notable Regional DAC/FI Allocations in the IALA ASM Collection

For completeness, Table D.5 lists additional regional Application-Specific Messages registered in the **IALA ASM Collection** and encountered in global satellite/coastal AIS archives:

### Table D.5: Selected Regional ASMs Across Europe, Asia-Pacific, and Panama

| DAC (MID) | FI | Jurisdiction / Authority | Msg Type | Message Title & Operational Purpose | Status |
|---|---|---|---|---|---|
| **`219` / `220`** | `1`, `2` | **Denmark** (Danish Maritime Authority) | `6`, `8` | Great Belt (Storebælt) & Øresund Bridge VTS clearance and pilotage telemetry | Active / Legacy |
| **`244` / `245` / `246`** | `10`, `24` | **Netherlands** (Rijkswaterstaat) | `8` | Port of Rotterdam / Westerschelde tidal surge and inland/coastal bridge status | Active |
| **`265` / `266`** | `1`, `11` | **Sweden** (Swedish Maritime Administration) | `8` | Baltic archipelago VTS wind/water-level gauges and icebreaker convoy status | Active / Transitioned to `DAC=1, FI=31` |
| **`351–357` / `370`** | `1`, `2` | **Panama** (Panama Canal Authority — ACP) | `6`, `8` | Panama Canal lock scheduling, Gaillard Cut traffic control, and locomotive tie-up | Active (Supplementing CTAN / PPU Wi-Fi) |
| **`412` / `413`** | `1`, `19`, `31` | **China** (China MSA) | `6`, `8` | Yangtze River & Three Gorges Lock scheduling, coastal VTS weather, and port notices | Active |
| **`503`** | `1`, `31` | **Australia** (AMSA / Reef VTS) | `6`, `8` | Great Barrier Reef & Torres Strait (**REEFVTS**) dynamic route monitoring and met-hydro | Active |
| **`563–566`** | `1`, `20` | **Singapore** (MPA Singapore) | `6`, `8` | Singapore Strait VTS anchorage allocation, pilot boarding, and bunkering telemetry | Active |
