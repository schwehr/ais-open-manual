# Chapter 39: Regional Application-Specific Message Subtypes, Part 1: European Inland AIS (`DAC = 200`) and UK/Ireland GLA (`DAC = 232 / 235`)

## 39.1 Operational & Engineering Context of European Inland AIS (`DAC = 200`)

### 1. Operational & Conceptual Overview
When the International Telecommunication Union (ITU) standardized the Automatic Identification System (ITU-R M.1371) for SOLAS ocean-going merchant vessels in the late 1990s, its data types were engineered for open-sea collision avoidance and coastal Vessel Traffic Services (VTS). On the high seas, knowing a container ship's length and beam to the nearest integer meter ($1\text{ m}$ resolution in Message 5) and its draught to the nearest decimeter ($0.1\text{ m}$ resolution) is entirely adequate when vessels pass each other at distances of $0.5\text{ NM}$ to $2.0\text{ NM}$ ($926\text{ m}$ to $3,704\text{ m}$).

On the interconnected inland waterways of Europe—spanning more than $41,000\text{ km}$ of navigable rivers, canals, and locks across the Rhine, Danube, Elbe, Main, Moselle, Seine, Rhone, and the Dutch/Belgian delta—those maritime tolerances are operationally unusable and physically dangerous. European inland navigation operates in a tightly constrained three-dimensional hydraulic corridor where horizontal lock clearances are measured in **centimeters**, vertical under-keel clearances over rocky shoals are measured in **centimeters**, vertical air draughts under historic low-arch bridges are measured in **centimeters**, and vessels dynamically re-configure their hull geometry multiple times per voyage by coupling and uncoupling pushed barges (*Schubleichter*).

To bridge the gap between ocean-going SOLAS AIS and the safety requirements of inland navigation, European river commissions and regulatory bodies established **Inland AIS** under Designated Area Code **`DAC = 200`**. Rather than discarding ITU-R M.1371, Inland AIS transponders operate on the exact same VHF frequencies ($\text{AIS 1} = 161.975\text{ MHz}$, $\text{AIS 2} = 162.025\text{ MHz}$) and SOTDMA/CSTDMA link layer, transmitting standard Class A Position Reports (Messages 1, 2, and 3) and Static/Voyage Reports (Message 5) for full backward compatibility with sea-going ships in mixed traffic zones such as the Port of Rotterdam, the Port of Antwerp, the Westerschelde, and the Lower Elbe toward Hamburg. Alongside those standard messages, Inland AIS transponders and shore-side **River Information Services (RIS)** base stations exchange seven specialized Application-Specific Messages (ASMs) via Addressed Binary Message 6 and Broadcast Binary Message 8 under `DAC = 200`:

| `DAC` | `FI` | Carrier Msg | Bit Length | `libais` Class | Title & Operational Role |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`200`** | **`10`** | Msg 8 | `168 bits` | `Ais8_200_10` | **Inland Ship Static and Voyage Related Data:** 8-char ENI number, `0.1 m` convoy length/beam, 4-digit ERI type (`8000–8490`), ADN hazardous blue cones (`0–3`), `0.01 m` centimeter draught, load status, and sensor quality flags. |
| **`200`** | **`21`** | Msg 6 | `248 / 256 bits` | `Ais6_200_21` | **ETA at Lock / Bridge / Terminal:** Ship-to-shore addressed request giving full 20-char ISRS location code (including `0.1 km` river hectometer), ETA, tug count, and `0.01 m` present static air draught. |
| **`200`** | **`22`** | Msg 6 | `232 / 248 bits` | `Ais6_200_22` | **RTA at Lock / Bridge / Terminal:** Shore-to-ship addressed reply from the RIS lockmaster assigning a Recommended Time of Arrival (RTA) and lock/bridge operational status (`0–3`). |
| **`200`** | **`23`** | Msg 8 | `256 bits` | `Ais8_200_23` | **EMMA Meteorological Warning:** Shore-to-ship weather hazard broadcast modeled on European Multiservice Meteorological Awareness (EMMA) warnings across a river bounding box. |
| **`200`** | **`24`** | Msg 8 | `168 bits` | `Ais8_200_24` | **Water Level:** Shore-to-ship broadcast carrying real-time centimeter-precision water level offsets (`-81.91 m` to `+81.91 m`) for up to four hydrometric river gauges per country. |
| **`200`** | **`40`** | Msg 8 | `168 bits` | `Ais8_200_40` | **Signal Status:** Shore-to-ship broadcast replicating physical CEVNI/RPR light-matrix traffic signals at locks, movable bridges, and narrow one-way gorge sections. |
| **`200`** | **`55`** | Msg 6 / 8 | `168 / 136 bits` | `Ais8_200_55` | **Number of Persons on Board:** Emergency manifest separating Crew (`8b`), Passengers (`13b`), and Hotel/Catering Shipboard Personnel (`8b`) for river cruise ships and ferries. |

In the second half of this chapter (Section 39.4), we examine the closely related regional Aid-to-Navigation (AtoN) telemetry message deployed by the **United Kingdom and Ireland General Lighthouse Authorities (GLA)** under **`DAC = 232` and `DAC = 235`, `FI = 10`** (`Ais8_235_10` / `Ais6_235_10`). Together, `DAC = 200` and `DAC = 235` represent the two highest-volume non-IMO regional binary message ecosystems in European waters.

---

### 2. Historical Context & Regulatory Lineage
The governance of European inland navigation predates the modern nation-state and the International Maritime Organization (IMO) by more than a century:
1. **The Central Commission for the Navigation of the Rhine (CCNR, *Zentralkommission für die Rheinschifffahrt*, 1815 / 1868):** Established at the Congress of Vienna in 1815 and codified by the **Mannheim Act of 17 October 1868**, the CCNR is the oldest extant international organization in the world. It exercises binding regulatory authority over the Rhine from Basel (Switzerland) to the North Sea (Hook of Holland), enforcing the *Rhine Police Regulations* (*Rheinschifffahrtspolizeiverordnung*, RPN / RPR).
2. **The Danube Commission (*Donaukommission*, 1948) and UNECE:** The Belgrade Convention of 1948 governs navigation along the $2,415\text{ km}$ navigable length of the Danube from Kelheim (Germany) to Sulina (Romania) on the Black Sea, while the **United Nations Economic Commission for Europe (UNECE)** Working Party on Inland Water Transport (`SC.3`) maintains the pan-European *European Code for Inland Waterways* (**CEVNI**) and **Resolution No. 63** (*International Standard for Tracking and Tracing on Inland Waterways*).
3. **The River Information Services (RIS) Directive (2005/44/EC):** Following a series of severe collisions and hazardous-cargo incidents in fog along the Rhine and Westerschelde—and culminating later in the **13 January 2011 capsizing of the acid tanker *Waldhof*** ($110\text{ m} \times 10.5\text{ m}$, carrying $2,377\text{ tonnes}$ of concentrated sulfuric acid) in the treacherous Binger Loch / Loreley gorge at Rhine-km $553.8$, which blocked hundreds of vessels for three weeks—the European Parliament enacted **Directive 2005/44/EC** on harmonized River Information Services.
4. **CESNI and the *Inland AIS Test Standard*:** In 2015, the EU and the CCNR created the **European Committee for Drawing Up Standards in the Field of Inland Navigation (CESNI, *Comité Européen pour l'Élaboration de Standards dans le Domaine de la Navigation Intérieure*)**. CESNI maintains the **ES-RIS** (*European Standard for River Information Services*) and the **CESNI *Inland AIS Test Standard* (Edition 2021/2023)**, which binds transceiver manufacturers (Nauticast, CNS Systems, Saab, True Heading, ACR/Class A Inland) to strict bit-level conformance for `DAC = 200`.

---

### 3. Why Ocean-Going ITU-R M.1371 Message 5 Was Inadequate for Inland Waterways
Three physical and regulatory realities forced CCNR, UNECE, and CESNI to design `DAC = 200` as an extension to ITU-R M.1371 Message 5:

#### A. Centimeter-Scale Lock Clearance & Under-Keel Precision
In ITU-R M.1371 Message 5, vessel dimensions (`Dimension to Bow` $A$, `Dimension to Stern` $B$, `Dimension to Port` $C$, `Dimension to Starboard` $D$) are quantized to **$1\text{ m}$ integers**, and `Maximum Present Static Draught` is quantized to **$0.1\text{ m}$ ($10\text{ cm}$) steps**.

Consider a standard Class Va **Large Rhine Vessel (*Großmotorgüterschiff*, GMS)** built to the maximum dimensions of standard European waterway locks (such as the Upper Rhine locks, Neckar locks, or Main-Danube Canal locks):
* **Standard Lock Chamber Width ($W_{\text{lock}}$):** $11.45\text{ m}$ ($12.00\text{ m}$ nominal masonry width minus $0.55\text{ m}$ of fender timbers and guide rails).
* **Standard GMS Hull Beam ($B_{\text{ship}}$):** $11.40\text{ m}$ (or $11.45\text{ m}$ with rub-rail allowance).
* **Lateral Clearance per Side ($\Delta y$):**
  $$\Delta y = \frac{W_{\text{lock}} - B_{\text{ship}}}{2} = \frac{11.45\text{ m} - 11.40\text{ m}}{2} = 0.025\text{ m} = 2.5\text{ cm}$$

With only **$2.5\text{ cm}$ ($1\text{ inch}$) of lateral water cushion** on port and starboard—causing strong hydrodynamic piston effects as displaced water squeezes backward past the hull—rounding $11.40\text{ m}$ to $11\text{ m}$ or $12\text{ m}$ in Message 5 makes automated lock-chamber packing impossible. When a lockmaster packs a $190.0\text{ m} \times 24.0\text{ m}$ twin-width Rhine lock chamber with four vessels side-by-side and bow-to-stern, the lock-planning solver requires **`0.1 m` ($10\text{ cm}$) length and beam resolution** (`DAC = 200, FI = 10`).

Similarly, on free-flowing stretches such as the Middle Rhine (*Gebirgsstrecke* at Kaub, Rhine-km $546.3$) or the Straubing–Vilshofen reach of the Danube, every **$1\text{ cm}$ ($0.01\text{ m}$) of immersion depth** on a $110\text{ m} \times 11.40\text{ m}$ freighter corresponds to a waterplane displacement of:
$$\Delta m_{1\text{ cm}} = \rho_{\text{fresh}} \cdot L \cdot B \cdot C_{WP} \cdot (0.01\text{ m}) \approx 1.000\text{ t/m}^3 \cdot 110.0\text{ m} \cdot 11.40\text{ m} \cdot 0.90 \cdot 0.01\text{ m} \approx 11.29\text{ tonnes/cm}$$
A $10\text{ cm}$ (`0.1 m`) quantization step in Message 5 represents **$113\text{ tonnes}$ of cargo uncertainty**—and constitutes the difference between safely clearing a rocky sill with $20\text{ cm}$ of under-keel clearance (UKC) or grounding the vessel. Consequently, `DAC = 200, FI = 10` encodes static draught in **`0.01 m` ($1\text{ cm}$) steps** (`11 bits`, `0.00–20.47 m`), and `DAC = 200, FI = 21` encodes present static air draught in **`0.01 m` ($1\text{ cm}$) steps** (`12 bits`, `0.00–40.00 m`) so vessels can pass beneath low canal bridges with `< 10 cm` of overhead clearance after ballasting or lowering their telescoping hydraulic wheelhouse (*Hubsteuerhaus*).

#### B. Articulated & Pushed Barge Convoys (*Schubverbände* and *Koppelverbände*)
Inland push-boats (*Schubboote*, such as the $4,500\text{ kW}$ *Herkules* class on the Lower Rhine between Rotterdam and Duisburg) routinely push **4-barge (`193.0 m × 22.80 m`) or 6-barge (`269.5 m × 22.80 m` or `193.0 m × 34.20 m`) formations** carrying up to $16,000\text{ tonnes}$ of iron ore or coal. Self-propelled motor cargo vessels also lash one to three unpowered barges alongside or ahead to form a **coupled convoy (*Koppelverband*)**.

IMO's 2-digit Ship Type code in Message 5 (`0–99`, where `70–79` = Cargo and `80–89` = Tanker) cannot distinguish a single $85\text{ m}$ motor freighter from a $269\text{ m}$ six-barge pushed convoy or a high-speed hydrofoil river ferry. Therefore, `DAC = 200, FI = 10` replaces the 2-digit IMO ship type with the **14-bit 4-digit UNECE/ERI (Electronic Reporting International) Vessel and Convoy Classification (`8000–8490`)**. Furthermore, the Inland AIS transponder must dynamically update both the **overall convoy dimensions** ($L_{\text{convoy}}, B_{\text{convoy}}$ in `FI = 10`) and the **GNSS antenna reference offsets** ($A, B, C, D$ in Message 5, covering the entire convoy bounding box) whenever barges are coupled or dropped off at a fleet anchorage.

#### C. ADN Hazardous Cargo "Blue Cones / Blue Lights"
On ocean-going vessels, Message 5 Ship Type digits `X1` through `X4` (`71–74`, `81–84`) broadly reference MARPOL/IBC/IGC pollution hazard categories (`A, B, C, D`). On European inland waterways, dangerous goods transport is governed by the **European Agreement concerning the International Carriage of Dangerous Goods by Inland Waterways (ADN)** alongside the CEVNI/RPR police regulations.

Under ADN Chapter 7 and CEVNI Article 3.14, inland vessels carrying dangerous goods must display **physical blue cones by day and blue all-round lights by night**, visible from all directions:
* **`0` Blue Cones / Lights:** Non-dangerous cargo or ADN substances not requiring special separation.
* **`1` Blue Cone / Light:** **Flammable substances** (e.g., gasoline, diesel, ethanol, benzene, LNG fuel/cargo). Vessels must maintain $\ge 10\text{ m}$ separation from other vessels when moored and cannot enter a lock chamber simultaneously with passenger vessels.
* **`2` Blue Cones / Lights:** **Toxic or corrosive substances** (e.g., ammonia, acrylonitrile, fuming sulfuric acid, chlorine). Vessels must maintain $\ge 50\text{ m}$ separation from other vessels and $\ge 100\text{ m}$ from residential areas when moored.
* **`3` Blue Cones / Lights:** **Explosive substances** (ADN Class 1). Vessels must maintain $\ge 100\text{ m}$ separation from all other vessels and infrastructure, and require exclusive single-vessel lockages.

By broadcasting the exact `0, 1, 2, or 3` blue-cone state in the 3-bit `Hazcargo` field of `DAC = 200, FI = 10`, every nearby vessel's Inland ECDIS display renders 1, 2, or 3 blue triangles directly atop the vessel target symbol, and RIS lock-scheduling software automatically enforces ADN lock-chamber segregation rules.

---

## 39.2 Vessel & Lock-Passage Subtypes (`DAC = 200, FI = 10, 21, 22, 55`)

### 39.2.1 `DAC = 200, FI = 10`: Inland Ship Static and Voyage Related Data (Msg 8, `168 bits`, `Ais8_200_10`)

#### 1. How It Works (Bit-Level Mechanics & Mathematical Scaling)
`DAC = 200, FI = 10` is broadcast in a single-slot **Message 8 (`168 bits` = 28 NMEA 6-bit characters, fill bits = `0`)** immediately following every transmission of ITU-R M.1371 Message 5 (every $6\text{ minutes}$, or immediately upon any parameter change).

| Bit Range (0-Based `libais`) | Python Slice | Bit Range (1-Based ITU) | Width (Bits) | Field Name (`libais` identifier) | Data Type / Scaling | Operational Range & Sentinel Values |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `0..5` | `[0:6]` | `1..6` | `6` | Message ID (`message_id`) | Unsigned int | Always `8` (Broadcast Binary Message) |
| `6..7` | `[6:8]` | `7..8` | `2` | Repeat Indicator (`repeat_indicator`) | Unsigned int | `0..3` (`0` = default, `3` = do not repeat) |
| `8..37` | `[8:38]` | `9..38` | `30` | Source MMSI (`mmsi`) | Unsigned int | 9-digit vessel MMSI (`000000000`–`999999999`) |
| `38..39` | `[38:40]` | `39..40` | `2` | Spare (`spare`) | Unsigned int | Always `0` |
| `40..49` | `[40:50]` | `41..50` | `10` | Designated Area Code (`dac`) | Unsigned int | Always `200` (European Inland AIS) |
| `50..55` | `[50:56]` | `51..56` | `6` | Function Identifier (`fi`) | Unsigned int | Always `10` (Inland Ship Static & Voyage Data) |
| **`56..103`** | **`[56:104]`** | **`57..104`** | **`48`** | **European Vessel ID (`eu_id` / ENI)** | **8 $\times$ 6-bit ASCII** | **8-digit Unique European Vessel Identification Number (`"00000000"`–`"99999999"`); `"@@@@@@@@"` or `"00000000"` = not available** |
| **`104..116`** | **`[104:117]`** | **`105..117`** | **`13`** | **Length of Ship / Convoy (`length`)** | **Unsigned int, `0.1 m`** | **`1`–`8000` $\rightarrow$ `0.1 m` to `800.0 m`; `0` = not available / default; `8001..8191` reserved** |
| **`117..126`** | **`[117:127]`** | **`118..127`** | **`10`** | **Beam of Ship / Convoy (`beam`)** | **Unsigned int, `0.1 m`** | **`1`–`1000` $\rightarrow$ `0.1 m` to `100.0 m`; `0` = not available / default; `1001..1023` reserved** |
| **`127..140`** | **`[127:141]`** | **`128..141`** | **`14`** | **Ship / Combination Type (`ship_type`)** | **Unsigned int (ERI)** | **4-digit ERI code `8000`–`8490`; `0` = not available / default** |
| **`141..143`** | **`[141:144]`** | **`142..144`** | **`3`** | **Hazardous Cargo (`haz_cargo`)** | **Unsigned enum** | **`0` = 0 blue cones/lights; `1` = 1 blue cone/light; `2` = 2 blue cones/lights; `3` = 3 blue cones/lights; `4` = B-flag; `5` = unknown / default; `6..7` = reserved** |
| **`144..154`** | **`[144:155]`** | **`145..155`** | **`11`** | **Maximum Present Static Draught (`draught`)** | **Unsigned int, `0.01 m`** | **`1`–`2000` $\rightarrow$ `0.01 m` to `20.00 m` (max bit value `2047` = `20.47 m`); `0` = not available / default** |
| **`155..156`** | **`[155:157]`** | **`156..157`** | **`2`** | **Loaded / Unloaded Status (`loaded`)** | **Unsigned enum** | **`0` = not available / default; `1` = loaded; `2` = unloaded; `3` = reserved** |
| **`157`** | **`[157:158]`** | **`158`** | **`1`** | **Speed Quality Flag (`speed_qual`)** | **Boolean flag** | **`0` = low (GNSS SOG default); `1` = high (Doppler/radar speed log)** |
| **`158`** | **`[158:159]`** | **`159`** | **`1`** | **Course Quality Flag (`course_qual`)** | **Boolean flag** | **`0` = low (GNSS COG default); `1` = high** |
| **`159`** | **`[159:160]`** | **`160`** | **`1`** | **Heading Quality Flag (`heading_qual`)** | **Boolean flag** | **`0` = low / uncalibrated; `1` = high (type-approved gyro or GNSS compass)** |
| `160..167` | `[160:168]` | `161..168` | `8` | Spare (`spare2`) | Unsigned int | Always `0` |

##### Mathematical Scaling Equations
From the raw integer fields $N_L \in [0, 8191]$, $N_B \in [0, 1023]$, and $N_T \in [0, 2047]$:
$$L_{\text{convoy}}\text{ (m)} = \begin{cases} \text{None} & \text{if } N_L = 0 \text{ or } N_L > 8000 \\ 0.1 \times N_L & \text{if } 1 \le N_L \le 8000 \end{cases}$$
$$B_{\text{convoy}}\text{ (m)} = \begin{cases} \text{None} & \text{if } N_B = 0 \text{ or } N_B > 1000 \\ 0.1 \times N_B & \text{if } 1 \le N_B \le 1000 \end{cases}$$
$$T_{\text{static}}\text{ (m)} = \begin{cases} \text{None} & \text{if } N_T = 0 \text{ or } N_T > 2000 \\ 0.01 \times N_T & \text{if } 1 \le N_T \le 2000 \end{cases}$$

##### Key ERI Ship and Convoy Classification Codes (`bits[127:141]`)
Unlike IMO 2-digit codes (`0–99`), the 14-bit ERI code encodes specific European hull and convoy topologies:

| ERI Code | Vessel / Convoy Designation | Standard IMO Msg 5 Mapping (`0–99`) | Typical Rhine/Danube Dimensions |
| :--- | :--- | :--- | :--- |
| **`8000`** | Vessel, type unknown | `99` (Other) | Variable |
| **`8010`** | **Motor freighter** (*Gütermotorschiff*, GMS) | `79` (Cargo, all ships of this type) | $85.0\text{ m} \times 9.50\text{ m}$ to $135.0\text{ m} \times 11.45\text{ m}$ |
| **`8020`** | **Motor tanker** (*Tankmotorschiff*, TMS, liquid cargo) | `89` (Tanker, all ships of this type) | $110.0\text{ m} \times 11.45\text{ m}$ |
| **`8021`** | Motor tanker, dry cargo (e.g., pneumatic cement/ash) | `79` (Cargo) | $85.0\text{ m} \times 9.50\text{ m}$ |
| **`8030`** | Container vessel (inland cellular barge) | `79` (Cargo) | $135.0\text{ m} \times 14.20\text{ m}$ or $17.10\text{ m}$ (4–5 TEU wide) |
| **`8040`** | Gas tanker (inland LPG / LNG / propylene carrier) | `89` (Tanker) | $110.0\text{ m} \times 11.45\text{ m}$ |
| **`8050`** | **Motor freighter, tug** (coupled motor freighter + barges, *Koppelverband*) | `79` (Cargo) | $172.0\text{ m} \times 11.45\text{ m}$ to $193.0\text{ m} \times 22.80\text{ m}$ |
| **`8060`** | **Motor tanker, tug** (coupled tanker convoy) | `89` (Tanker) | $185.0\text{ m} \times 11.45\text{ m}$ |
| **`8160`** | Tank barge (dumb liquid barge) | `89` (Tanker) | $76.5\text{ m} \times 11.40\text{ m}$ (Europa IIa) |
| **`8210`** | **Pushed convoy, 1 barge** (*Schubverband*, 1 lighter) | `79` (Cargo) | $110.0\text{ m} \times 11.40\text{ m}$ |
| **`8220`** | **Pushed convoy, 2 barges** | `79` (Cargo) | $185.0\text{ m} \times 11.40\text{ m}$ or $110.0\text{ m} \times 22.80\text{ m}$ |
| **`8240`** | **Pushed convoy, 4 barges** | `79` (Cargo) | $193.0\text{ m} \times 22.80\text{ m}$ |
| **`8260`** | **Pushed convoy, 6 barges** (Lower Rhine *Sechser-Schubverband*) | `79` (Cargo) | $269.5\text{ m} \times 22.80\text{ m}$ or $193.0\text{ m} \times 34.20\text{ m}$ |
| **`8290`** | **Pushed tanker convoy** (1 or more tank barges) | `89` (Tanker) | $185.0\text{ m} \times 11.40\text{ m}$ |
| **`8410`** | Tug, one or more tows | `31` (Towing) | Variable |
| **`8430`** | **Pushboat, single** (*Schubboot* running light without barges) | `31` / `52` (Tug) | $20.0\text{ m} \times 9.50\text{ m}$ to $40.0\text{ m} \times 15.0\text{ m}$ |
| **`8440`** | **Passenger ship, ferry, cruise ship, red cross ship** | `69` (Passenger) | $110.0\text{ m} \times 11.45\text{ m}$ or $135.0\text{ m} \times 11.45\text{ m}$ |
| **`8441`** | Ferry (cross-river cable or free-running ferry) | `69` (Passenger) | $35.0\text{ m} \times 12.0\text{ m}$ |
| **`8443`** | **Cruise ship (cabin vessel / *Flusskreuzfahrtschiff*)** | `69` (Passenger) | $135.0\text{ m} \times 11.45\text{ m}$ |
| **`8450`** | Service vessel, police patrol, waterway authority (*WSD / Rijkswaterstaat*) | `55` (Law enforcement) | $18.0\text{ m} \times 4.80\text{ m}$ |

#### 2. Engineering Issues, Quirks, & Parser Edge Cases
1. **ENI vs. IMO Number Confusion:** Since 1 April 2007, every European inland vessel over $20\text{ m}$ is assigned an 8-digit **European Vessel Identification Number (ENI, *Europäische Schiffsnummer*)** in the `eu_id` field (`bits[56:104]`). The first three digits identify the issuing authority (`040–048` and `050–058` = Germany, `020–039` = Netherlands, `060–065` = Belgium, `018` = France, `070` = Switzerland, `030` = Austria). If the vessel *also* holds a 7-digit sea-going IMO number, the ENI begins with `9` followed by the 7-digit IMO number (e.g., `91234567`). However, many poorly configured Inland AIS units place the 8-digit ENI (stripped of its leading zero) inside the 30-bit `imo_num` field of Message 5, causing ocean-going parsers that run the IMO Modulo-10 check-digit verification to reject the Message 5 record as corrupted!
2. **Dimension Discrepancy Between Message 5 and `FI = 10`:** When a skipper couples or uncouples a pushed barge on the water, they update the convoy dimensions on the Inland AIS Pilot Plug / Inland ECDIS keyboard. Some legacy firmware versions update `length` and `beam` in `DAC = 200, FI = 10` (`0.1 m` resolution) immediately, while failing to recalculate the integer `A, B, C, D` GNSS antenna offsets in Message 5—or conversely, setting Message 5 dimensions to `0` while populating `FI = 10`. High-integrity fusion engines must always prefer `FI = 10` `length` and `beam` for hull size while cross-checking $A+B \approx \text{round}(L_{\text{convoy}})$ and $C+D \approx \text{round}(B_{\text{convoy}})$.
3. **Hazardous Cargo Dual Encoding:** In Message 5, the second digit of the IMO Ship Type (`71–74` or `81–84`) is derived from `5 - haz_cargo` (`1` blue cone $\rightarrow$ IMO `X3`, `2` blue cones $\rightarrow$ IMO `X2`, `3` blue cones $\rightarrow$ IMO `X1`). If a skipper sets `haz_cargo = 5` (unknown) in `FI = 10`, Message 5 reverts to `79` or `89`.

#### 3. Relationships to Other AIS Messages
Per the CESNI *Inland AIS Test Standard*, `DAC = 200, FI = 10` is **strictly coupled to ITU-R M.1371 Message 5**:
* Whenever an Inland AIS mobile station transmits Message 5 (every $6\text{ minutes}$ or upon static data change), it **must** broadcast `Message 8 (DAC = 200, FI = 10)` within the same minute (typically in the next available autonomous SOTDMA slot $1\text{ to }4\text{ seconds}$ later).
* Furthermore, while ocean-going Class A units adjust their Message 1/2/3 dynamic reporting interval (`2 s` to `180 s`) autonomously via SOTDMA based on speed and rate of turn, Inland AIS units operating in dense river sectors (e.g., Waal, Port of Rotterdam, or Middle Rhine) have their reporting interval overridden via **ITU-R M.1371 Message 23 (*Group Assignment Command*)** broadcast by shore-side RIS base stations (`Station Type = 6` [Inland Waterways], typically commanding a fixed `5 s` or `10 s` reporting interval regardless of vessel speed).

#### 4. Operational Uses & Adversarial Abuses
* **Operational Uses:** Automated lock-chamber geometry planning; bridge collision prevention; ADN dangerous-cargo separation monitoring at ports and overnight moorings (*Übernachtungshäfen*); automatic cross-checking of vessel ENI against hull certificates in the **European Hull Data Base (EHDB)**.
* **Adversarial Abuses & Compliance Evasion:**
  * *"Blue-Cone Scrubbing":* Tanker operators carrying ADN 1-cone or 2-cone cargoes occasionally set `haz_cargo = 0` in `FI = 10` to illegally moor at non-ADN city quays or slip into a lock chamber alongside a passenger vessel instead of waiting for a segregated dangerous-goods lockage.
  * *"Draft Under-Reporting":* During low-water surcharges (*Kleinwasserzuschlag*, KWZ) on the Rhine, unscrupulous operators have been caught manually entering a shallower `draught` in `FI = 10` (e.g., `210` = $2.10\text{ m}$ instead of actual $2.45\text{ m}$) to evade waterway police (*Wasserschutzpolizei*) inspection on shallow reaches.

#### 5. Where and When Used
Mandatory 24/7 across all EU and CCNR/Danube inland waterways (`Rhine`, `Waal`, `Lek`, `Maas`, `Scheldt`, `Albert Canal`, `Mittelland Canal`, `Elbe`, `Oder`, `Main`, `Main-Danube Canal`, `Moselle`, `Neckar`, `Saar`, `Seine`, `Rhone`, and the entire `Danube` from Germany through Austria, Slovakia, Hungary, Croatia, Serbia, Bulgaria, and Romania) for all commercial vessels $\ge 20\text{ m}$ in length or where $L \times B \times T \ge 100\text{ m}^3$, plus all tugs, push-boats, passenger vessels, and ADN dangerous-cargo vessels.

#### 6. Software & Hardware Ecosystem Support
* **Inland ECDIS:** Native primary target data source in **Periskal Radar Overlay / Inland ECDIS**, **Tresco Navigis**, **Argonics ArgoTrackPilot**, **Stentec WinGPS Inland**, ** ChartWorld SevenCs Orbis**, and **OpenCPN** (with Inland AIS / `ais-vd` plugins).
* **Open-Source Parsers:** Fully supported in `libais` (`Ais8_200_10` in `src/libais/ais8_200.cpp`), `gpsd` (`driver_ais.c` `dac=200, fid=10`), and `pyais` (`MessageType8_DAC200_FI10`). Note that standard SOLAS ocean-going ECDIS consoles (e.g., unmodified Furuno or JRC deep-sea configurations without the Inland option enabled) ignore `DAC = 200, FI = 10` and display only the coarse $1\text{ m}$ Message 5 dimensions.

---

### 39.2.2 `DAC = 200, FI = 21` (ETA) and `FI = 22` (RTA): Closed-Loop Lock & Bridge Passage Negotiation (Msg 6, `Ais6_200_21` & `Ais6_200_22`)

#### 1. How It Works (Bit-Level Mechanics & ISRS Location Code Structure)
On canalized rivers such as the Moselle (14 locks between Koblenz and Neuves-Maisons), the Main (34 locks), the Main-Danube Canal (16 locks overcoming a $406\text{ m}$ summit elevation), and the Danube (18 locks between Kelheim and Iron Gate II), lock passage times dominate voyage duration and fuel burn. If three $185\text{ m}$ pushed convoys race at full throttle ($16\text{ km/h}$) toward a single-chamber lock that is currently cycling in the opposite direction, two of those convoys will burn hundreds of liters of diesel only to idle for $90\text{ minutes}$ at the lock approach dolphin (*Vorhafen*).

To eliminate lock queuing and enable **Just-In-Time (JIT) green steaming**, Inland AIS implements a bidirectional **Addressed Binary Message 6 handshake** between the vessel (`FI = 21`, *ETA at Lock/Bridge/Terminal*) and the shore-side RIS lockmaster system (`FI = 22`, *RTA — Recommended Time of Arrival at Lock/Bridge/Terminal*):

```mermaid
sequenceDiagram
    participant Ship as Inland Vessel (MMSI 211000123)<br/>Inland ECDIS / TrackPilot
    participant Base as RIS Shore Base Station<br/>(MMSI 002111200)
    participant Lock as Lock Management System (LMS)<br/>(ISRS: DE DUISB 00100 L0001 07805)

    Note over Ship: 15 km upstream of lock, calculates ETA & Air Draught
    Ship->>Base: Msg 6 (DAC=200, FI=21: ETA at Lock/Bridge/Terminal)<br/>ISRS="DEDUISB00100L000107805", ETA=14:20 UTC, Tugs=0, AirDraught=6.45 m
    Base->>Ship: Msg 7 (Binary Acknowledge for Msg 6 SeqNum)
    Base->>Lock: Forward ETA + FI=10 Convoy Dimensions (185.0 m x 11.40 m, 1 Blue Cone)
    Note over Lock: LMS optimizes chamber packing & ADN separation;<br/>Chamber available at 14:42 UTC (Status = 0: Operational)
    Lock->>Base: Schedule Slot Assigned: RTA = 14:42 UTC
    Base->>Ship: Msg 6 (DAC=200, FI=22: RTA at Lock/Bridge/Terminal)<br/>ISRS="DEDUISB00100L000107805", RTA=14:42 UTC, Status=0 (Operational)
    Ship->>Base: Msg 7 (Binary Acknowledge for Msg 6 SeqNum)
    Note over Ship: Inland ECDIS reduces throttle from 15.5 km/h to 11.8 km/h,<br/>saving 38% fuel and arriving exactly as lock gates open
```

##### The 20-Character ISRS Location Code (`132 bits` = `22` $\times$ 6-bit ASCII characters across 5 fields)
Both `FI = 21` and `FI = 22` identify the target lock, bridge, or terminal using the standardized **20-character International Ship Reporting Standard (ISRS) Location Code** (plus 2 extra ASCII characters in the 5-character hectometer field, totaling `22` 6-bit ASCII characters = `132 bits` from bit `88` to bit `219`):
1. **Block 1 — UN Country Code (`bits[88:100]`, 2 chars, 12b):** ISO 3166-1 alpha-2 country code (e.g., `"DE"`, `"NL"`, `"AT"`, `"BE"`, `"FR"`).
2. **Block 2 — UN Location Code (`bits[100:130]`, 5 chars, 30b):** The 3-character UN/LOCODE city identifier (`"RTM"`, `"DUI"`, `"VIE"`) padded with spaces or sub-location characters (`"DUISB"`).
3. **Block 3 — Fairway Section Code (`bits[130:160]`, 5 chars, 30b):** National alphanumeric code identifying the specific river or canal (`"00100"` = Rhine).
4. **Block 4 — Terminal / Object Code (`bits[160:190]`, 5 chars, 30b):** Identifies the specific lock chamber, bridge span, or terminal berth (`"L0001"` = North Lock Chamber).
5. **Block 5 — Fairway Hectometer (`bits[190:220]`, 5 chars, 30b):** 5-digit ASCII numeric string `"00000"`–`"99999"` representing the **river kilometer in `0.1 km` (hectometer) units** (e.g., `"07805"` = River km $780.5$; `"@@@@@"` = not available).

##### Bit-Level Layout of `DAC = 200, FI = 21` (*ETA at Lock / Bridge / Terminal*, Msg 6, `248 / 256 bits`, `Ais6_200_21`)

| Bit Range (0-Based `libais`) | Python Slice | Bit Range (1-Based ITU) | Width (Bits) | Field Name (`libais` identifier) | Data Type / Scaling | Operational Range & Sentinel Values |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `0..5` | `[0:6]` | `1..6` | `6` | Message ID (`message_id`) | Unsigned int | Always `6` (Addressed Binary Message) |
| `6..7` | `[6:8]` | `7..8` | `2` | Repeat Indicator (`repeat_indicator`) | Unsigned int | `0..3` |
| `8..37` | `[8:38]` | `9..38` | `30` | Source MMSI (`mmsi`) | Unsigned int | Vessel MMSI transmitting the ETA |
| `38..39` | `[38:40]` | `39..40` | `2` | Sequence Number (`seq`) | Unsigned int | `0..3` (matched by Msg 7 Binary Ack) |
| `40..69` | `[40:70]` | `41..70` | `30` | Destination MMSI (`dest_mmsi`) | Unsigned int | RIS Shore Base Station MMSI |
| `70` | `[70:71]` | `71` | `1` | Retransmit Flag (`retransmit`) | Boolean | `0` = original, `1` = retransmitted |
| `71` | `[71:72]` | `72` | `1` | Spare (`spare`) | Unsigned int | Always `0` |
| `72..81` | `[72:82]` | `73..82` | `10` | Designated Area Code (`dac`) | Unsigned int | Always `200` |
| `82..87` | `[82:88]` | `83..88` | `6` | Function Identifier (`fi`) | Unsigned int | Always `21` (ETA at Lock/Bridge/Terminal) |
| **`88..99`** | **`[88:100]`** | **`89..100`** | **`12`** | **UN Country Code (`country`)** | **2 $\times$ 6-bit ASCII** | **ISO 3166-1 alpha-2 (`"DE"`, `"NL"`, etc.); `"@@"` = N/A** |
| **`100..129`** | **`[100:130]`** | **`101..130`** | **`30`** | **UN Location Code (`locode`)** | **5 $\times$ 6-bit ASCII** | **UN/LOCODE suffix; `"@@@@@"` = N/A** |
| **`130..159`** | **`[130:160]`** | **`131..160`** | **`30`** | **Fairway Section (`section`)** | **5 $\times$ 6-bit ASCII** | **National waterway code; `"@@@@@"` = N/A** |
| **`160..189`** | **`[160:190]`** | **`161..190`** | **`30`** | **Object / Terminal Code (`terminal`)** | **5 $\times$ 6-bit ASCII** | **Lock/bridge/terminal ID; `"@@@@@"` = N/A** |
| **`190..219`** | **`[190:220]`** | **`191..220`** | **`30`** | **Fairway Hectometer (`hectometre`)** | **5 $\times$ 6-bit ASCII** | **Numeric string `"00000"`–`"99999"` in `0.1 km` steps; `"@@@@@"` = N/A** |
| **`220..223`** | **`[220:224]`** | **`221..224`** | **`4`** | **ETA Month (`eta_month`)** | **Unsigned int** | **`1`–`12`; `0` = not available (`13..15` reserved)** |
| **`224..228`** | **`[224:229]`** | **`225..229`** | **`5`** | **ETA Day (`eta_day`)** | **Unsigned int** | **`1`–`31`; `0` = not available** |
| **`229..233`** | **`[229:234]`** | **`230..234`** | **`5`** | **ETA Hour (`eta_hour`)** | **Unsigned int (UTC)** | **`0`–`23`; `24` = not available (`25..31` reserved)** |
| **`234..239`** | **`[234:240]`** | **`235..240`** | **`6`** | **ETA Minute (`eta_minute`)** | **Unsigned int (UTC)** | **`0`–`59`; `60` = not available (`61..63` reserved)** |
| **`240..242`** | **`[240:243]`** | **`241..243`** | **`3`** | **Assisting Tugs (`tugs`)** | **Unsigned int** | **`0`–`6` assisting tugs; `7` = unknown / default** |
| **`243..254`** | **`[243:255]`** | **`244..255`** | **`12`** | **Max Present Static Air Draught (`air_draught`)** | **Unsigned int, `0.01 m`** | **`1`–`4000` $\rightarrow$ `0.01 m` to `40.00 m`; `0` = not available (`4001..4095` reserved)** |
| `255` | `[255:256]` | `256` | `1` | Spare (`spare2`) | Unsigned int | `0` (Note: `libais` accepts `248`–`256` bit frames) |

##### Bit-Level Layout of `DAC = 200, FI = 22` (*RTA at Lock / Bridge / Terminal*, Msg 6, `232 / 248 bits`, `Ais6_200_22`)

| Bit Range (0-Based `libais`) | Python Slice | Bit Range (1-Based ITU) | Width (Bits) | Field Name (`libais` identifier) | Data Type / Scaling | Operational Range & Sentinel Values |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `0..87` | `[0:88]` | `1..88` | `88` | Addressed Msg 6 Header | Standard | `Message ID = 6`, `DAC = 200`, `FI = 22` |
| `88..219` | `[88:220]` | `89..220` | `132` | ISRS Location Code + Hectometer | 22 $\times$ 6-bit ASCII | Identical 5-block structure (`country`, `locode`, `section`, `terminal`, `hectometre`) as `FI = 21` |
| **`220..223`** | **`[220:224]`** | **`221..224`** | **`4`** | **RTA Month (`rta_month`)** | **Unsigned int** | **`1`–`12`; `0` = not available** |
| **`224..228`** | **`[224:229]`** | **`225..229`** | **`5`** | **RTA Day (`rta_day`)** | **Unsigned int** | **`1`–`31`; `0` = not available** |
| **`229..233`** | **`[229:234]`** | **`230..234`** | **`5`** | **RTA Hour (`rta_hour`)** | **Unsigned int (UTC)** | **`0`–`23`; `24` = not available** |
| **`234..239`** | **`[234:240]`** | **`235..240`** | **`6`** | **RTA Minute (`rta_minute`)** | **Unsigned int (UTC)** | **`0`–`59`; `60` = not available** |
| **`240..241`** | **`[240:242]`** | **`241..242`** | **`2`** | **Lock / Bridge / Terminal Status (`status`)** | **Unsigned enum** | **`0` = Operational; `1` = Limited operation; `2` = Out of order / Closed; `3` = Not available** |
| `242..247` | `[242:248]` | `243..248` | `6` | Spare (`spare2`) | Unsigned int | `0` (byte-aligned to `248 bits` in CESNI; `232 bits` in early CCNR drafts) |

#### 2. Engineering Issues, Quirks, & Parser Edge Cases
* **The `248-bit` vs. `256-bit` (`FI = 21`) and `232-bit` vs. `248-bit` (`FI = 22`) Framing Bug:** In the original 2006 CCNREdition 1.0 specification, `FI = 21` and `FI = 22` had discrepancies between the sum of their field widths (`255 bits` for `FI = 21`, `242 bits` for `FI = 22`) and the summary table header lengths (`248 bits` and `232 bits`, which had been calculated before the `30-bit` Fairway Section field or `16-bit` IAI header was finalized!). In `libais` (`src/libais/ais6.cpp`), the constructor checks `bs.size() != 248` or `232`, which can reject valid CESNI `256-bit` (`FI = 21`) and `248-bit` (`FI = 22`) payloads unless range-checked (`248 <= bits <= 256` and `232 <= bits <= 248`). Robust parsers must always accept both legacy and CESNI-padded bit lengths.
* **ASCII Hectometer vs. Binary Integer:** Unlike every other numeric metric in AIS, `hectometre` (`bits[190:220]`) is encoded as **five 6-bit ASCII characters** (e.g., `"07805"`) rather than a binary integer, because it forms the fifth 5-character block of the 20-character ISRS code (`UN/LOCODE` extension). Parsers must strip trailing spaces or `@` characters before dividing by $10.0$ to obtain river kilometers ($780.5\text{ km}$).

#### 3. Relationships to Other AIS Messages
* `FI = 21` and `FI = 22` are **Addressed Binary Messages (Message 6)** and therefore trigger automatic link-layer **Message 7 (*Binary Acknowledge*)** responses from the receiving station's SOTDMA stack.
* While Message 5 contains a global voyage `ETA` and `Destination` for the final port of call (e.g., Basel or Linz), `FI = 21` and `FI = 22` operate at the **intermediate tactical waypoint level** (each successive lock or lifting bridge along the route).

#### 4. Operational Uses & Adversarial Abuses
* **Operational Uses:** Lock-slot reservation on the Moselle, Danube (Austria *DoRIS* / Slovakia / Hungary), and Dutch *Rijkswaterstaat* IVS Next network; automated bridge-opening requests on Dutch and Belgian canals based on the vessel's reported `air_draught` (`0.01 m` resolution).
* **Adversarial Abuses:** Because `FI = 21` and `FI = 22` are unauthenticated on VHF, an attacker could spoof an addressed `FI = 22` message with `status = 2` (*Out of order / Closed*) from a shore base MMSI, tricking approaching vessels into anchoring or diverting, or spoof `FI = 21` requests with artificially early ETAs to hog lock slots.

#### 5. Where and When Used
Used along canalized European waterways equipped with RIS Lock Management Systems—most heavily in the Netherlands (*Rijkswaterstaat*), Belgium (*De Vlaamse Waterweg*), Austria (*via donau* / DoRIS), and the German Moselle/Main-Danube corridors.

#### 6. Software & Hardware Ecosystem Support
Supported in `libais` (`Ais6_200_21`, `Ais6_200_22`), `gpsd`, `pyais`, and commercial Inland ECDIS navigation suites (Periskal, Tresco, Argonics) that integrate with the onboard Inland AIS Pilot Plug via the proprietary **`$PIWWSSD` / `$PIWWIVD`** or **IEC 61162-1 `ABM` / `VDM`** sentences.

---

### 39.2.3 `DAC = 200, FI = 55`: Number of Persons on Board (Msg 6 / Msg 8, `168 / 136 bits`, `Ais8_200_55`)

#### 1. How It Works (Bit-Level Mechanics & Comparison with IMO `DAC = 1, FI = 16`)
European rivers host more than **400 luxury river cruise vessels (*Flusskreuzfahrtschiffe*)**—typically $110.0\text{ m}$ or $135.0\text{ m}$ long, carrying $150\text{ to }220\text{ passengers}$, $40\text{ to }55\text{ hotel/catering staff}$, and $8\text{ to }12\text{ nautical crew}$—as well as day-excursion ships carrying up to $1,000\text{ passengers}$ through the Rhine Gorge, Amsterdam canals, and Budapest/Vienna Danube reaches.

Whereas IMO's international `DAC = 1, FI = 16` (*Number of Persons on Board*, Chapter 37) provides only a single **13-bit total person count (`0–8191`)**, European inland search-and-rescue (SAR) authorities require an explicit breakdown of **nautical crew**, **passengers**, and **onboard hotel/catering personnel** because nautical crew are trained in emergency firefighting and vessel handling, whereas hotel staff and passengers must be evacuated first.

`DAC = 200, FI = 55` can be transmitted either as an **Addressed Message 6 (`168 bits` total)** to a RIS center upon request, or as a **Broadcast Message 8 (`136 bits` unpadded or `168 bits` 1-slot padded)**:

| Bit Range (Msg 8 `0`-Based) | Bit Range (Msg 6 `0`-Based) | Width (Bits) | Field Name (`libais` identifier) | Data Type / Scaling | Operational Range & Sentinel Values |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `0..55` | `0..87` | `56` / `88` | Binary Message Header | Standard | `Message ID = 8` (56b) or `6` (88b), `DAC = 200`, `FI = 55` |
| **`56..63`** | **`88..95`** | **`8`** | **Number of Crew on Board (`crew`)** | **Unsigned int** | **`0`–`254` nautical crew members; `255` = unknown / default** |
| **`64..76`** | **`96..108`** | **`13`** | **Number of Passengers on Board (`passengers`)** | **Unsigned int** | **`0`–`8190` passengers; `8191` = unknown / default** |
| **`77..84`** | **`109..116`** | **`8`** | **Number of Shipboard Personnel (`yet_more_personnel`)** | **Unsigned int** | **`0`–`254` hotel, catering, & service staff; `255` = unknown / default** |
| `85..135` (`..167`) | `117..167` | `51` (`83`) | Spare (`spare2`) | Unsigned int | Always `0` (`51 bits` yields `168 bits` in Msg 6 and `136 bits` in Msg 8) |

#### 2. Engineering Issues, Quirks, & Parser Edge Cases
* **The `51-bit` Spare Offset (`136 bits` vs. `168 bits`):** Notice the arithmetic: in Addressed Message 6 (`88-bit` header), `88 + 8 + 13 + 8 = 117 bits`, so adding **`51 bits` of spare padding** brings the frame to an exact 1-slot **`168 bits`**. When the specification authors copied the `51-bit` spare field directly into the Broadcast Message 8 table (`56-bit` header), the sum became `56 + 29 + 51 = 136 bits`! Some transponders transmit `136 bits` for Message 8 (`Ais8_200_55`), while others pad all the way to `168 bits` (`83 bits` of spare). Both `libais` and custom parsers must accept `136` to `168` bits for `Ais8_200_55`.

#### 3. Relationships to Other AIS Messages, 4. Uses & Abuses, 5. Where/When Used, & 6. Software Support
* **Relationships:** Inland counterpart to IMO `DAC = 1, FI = 16` (`Ais6_1_16` / `Ais8_1_16`), and may be polled via **ITU-R M.1371 Message 15 (*Interrogation*)** or **Addressed Binary Poll (`DAC = 200, FI = 56`)**.
* **Uses & Abuses:** Used by waterway police and rescue coordination centers during passenger vessel groundings, bridge allisions, or onboard fires (such as the 2019 *Viking Idun* collision on the Western Scheldt or Rhine cruise vessel evacuations). Because passenger counts are sensitive commercial and privacy data, CESNI recommends transmitting `FI = 55` via **Addressed Message 6** to the local RIS authority rather than continuous unencrypted Message 8 broadcast.
* **Software Support:** Supported in `libais` (`Ais8_200_55`), `gpsd`, `pyais`, and RIS shore management suites.

---

## 39.3 Waterway Environment, Hydrometric Gauges, and Signal Status (`DAC = 200, FI = 23, 24, 40`)

### 39.3.1 `DAC = 200, FI = 23`: EMMA Meteorological Warning (Msg 8, `256 bits`, `Ais8_200_23`)

#### 1. How It Works (Bit-Level Mechanics & EMMA Weather Encoding)
Unlike ocean-going vessels that receive meteorological data via `DAC = 1, FI = 31` (*Meteorological and Hydrological Data*, a point-sensor observation at a specific offshore buoy or lighthouse), European inland skippers navigate narrow river valleys prone to sudden micro-climatic hazards: violent **Föhn or thunderstorm squalls** across Lake Constance and the Upper Rhine, dense **radiation fog** (*Flussnebel*) that instantly halts non-radar navigation and triggers CEVNI narrow-channel rules, **ice drift** (*Eisgang*) on the Elbe and Danube, and **flash-flood waves** (*Hochwasserwelle*) that shut down navigation completely once the Highest Navigable Water Level (**HSW**, *Höchster Schifffahrtswasserstand*) is exceeded.

`DAC = 200, FI = 23` broadcasts **polygon/bounding-box weather warnings** standardized by **Meteoalarm / EMMA (European Multiservice Meteorological Awareness)** in a 2-slot **Broadcast Message 8 (`256 bits`)**:

| Bit Range (0-Based `libais`) | Python Slice | Bit Range (1-Based ITU) | Width (Bits) | Field Name (`libais` identifier) | Data Type / Scaling | Operational Range & Sentinel Values |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `0..55` | `[0:56]` | `1..56` | `56` | Broadcast Msg 8 Header | Standard | `Message ID = 8`, `DAC = 200`, `FI = 23` |
| `56..63` | `[56:64]` | `57..64` | `8` | Start Year (`start_year`) | Unsigned int | `1`–`255` $\rightarrow$ Year `2000 + val` (`0` = default / N/A) |
| `64..67` | `[64:68]` | `65..68` | `4` | Start Month (`start_month`) | Unsigned int | `1`–`12` (`0` = N/A) |
| `68..72` | `[68:73]` | `69..73` | `5` | Start Day (`start_day`) | Unsigned int | `1`–`31` (`0` = N/A) |
| `73..80` | `[73:81]` | `74..81` | `8` | End Year (`end_year`) | Unsigned int | `1`–`255` $\rightarrow$ Year `2000 + val` (`0` = N/A) |
| `81..84` | `[81:85]` | `82..85` | `4` | End Month (`end_month`) | Unsigned int | `1`–`12` (`0` = N/A) |
| `85..89` | `[85:90]` | `86..90` | `5` | End Day (`end_day`) | Unsigned int | `1`–`31` (`0` = N/A) |
| `90..94` | `[90:95]` | `91..95` | `5` | Start Hour (`start_hour`) | Unsigned int (UTC) | `0`–`23` (`24` = N/A) |
| `95..100` | `[95:101]` | `96..101` | `6` | Start Minute (`start_minute`) | Unsigned int (UTC) | `0`–`59` (`60` = N/A) |
| `101..105` | `[101:106]` | `102..106` | `5` | End Hour (`end_hour`) | Unsigned int (UTC) | `0`–`23` (`24` = N/A) |
| `106..111` | `[106:112]` | `107..112` | `6` | End Minute (`end_minute`) | Unsigned int (UTC) | `0`–`59` (`60` = N/A) |
| **`112..139`** | **`[112:140]`** | **`113..140`** | **`28`** | **Start Longitude (`start_lon`)** | **Signed int, $10^{-3}\text{ min}$** | **$\pm 180^\circ$ (`val / 60,000.0`); `10860000` (`181°`) = N/A** |
| **`140..166`** | **`[140:167]`** | **`141..167`** | **`27`** | **Start Latitude (`start_lat`)** | **Signed int, $10^{-3}\text{ min}$** | **$\pm 90^\circ$ (`val / 60,000.0`); `5460000` (`91°`) = N/A** |
| **`167..194`** | **`[167:195]`** | **`168..195`** | **`28`** | **End Longitude (`end_lon`)** | **Signed int, $10^{-3}\text{ min}$** | **$\pm 180^\circ$ (`val / 60,000.0`); `10860000` (`181°`) = N/A** |
| **`195..221`** | **`[195:222]`** | **`196..222`** | **`27`** | **End Latitude (`end_lat`)** | **Signed int, $10^{-3}\text{ min}$** | **$\pm 90^\circ$ (`val / 60,000.0`); `5460000` (`91°`) = N/A** |
| **`222..225`** | **`[222:226]`** | **`223..226`** | **`4`** | **Weather Type (`type`)** | **Unsigned enum** | **`0` = N/A; `1` = Wind (`m/s`); `2` = Rain (`mm/h`); `3` = Snow/Ice (`cm`); `4` = Thunderstorm; `5` = Fog (visibility `m`); `6` = Low Temp (`°C`); `7` = High Temp (`°C`); `8` = Flood; `9` = Forest Fire** |
| **`226..234`** | **`[226:235]`** | **`227..235`** | **`9`** | **Minimum Value (`min`)** | **Signed 9-bit int** | **`-255` to `+255` (units per `type`); `-256` (`0x100`) = N/A** |
| **`235..243`** | **`[235:244]`** | **`236..244`** | **`9`** | **Maximum Value (`max`)** | **Signed 9-bit int** | **`-255` to `+255` (units per `type`); `-256` (`0x100`) = N/A** |
| **`244..247`** | **`[244:248]`** | **`245..248`** | **`4`** | **Warning Intensity (`classification`)** | **Unsigned enum** | **`0` = Unknown; `1` = Slight (Yellow); `2` = Moderate (Orange); `3` = Severe (Red)** |
| **`248..251`** | **`[248:252]`** | **`249..252`** | **`4`** | **Wind Direction (`wind_dir`)** | **Unsigned enum** | **`0` = N/A; `1` = N; `2` = NE; `3` = E; `4` = SE; `5` = S; `6` = SW; `7` = W; `8` = NW** |
| `252..255` | `[252:256]` | `253..256` | `4` | Spare (`spare2`) | Unsigned int | Always `0` |

#### 2. Engineering Issues, 3. Relationships, 4. Uses & Abuses, 5. Where/When Used, & 6. Software Support
* **Coordinate Scaling Quirk ($1/1,000\text{ min}$ in `28/27 bits`!):** Look closely at bits `112..221` of `FI = 23`: although `start_lon`/`end_lon` occupy **28 bits** and `start_lat`/`end_lat` occupy **27 bits** (the exact bit widths of standard $1/10,000\text{ min}$ positions in Messages 1/2/3!), the CESNI specification defines their scaling as **$1/1,000\text{ minute}$** ($\text{divisor} = 60,000.0$ instead of $600,000.0$)! This is one of the most notorious traps in AIS software engineering: a parser that blindly applies the standard `28-bit` divisor ($600,000$) will plot `FI = 23` weather zones at **one-tenth of their true longitude and latitude** (off the coast of Ghana in the Gulf of Guinea!).
* **Relationships:** Complements IMO `DAC = 1, FI = 31` (`Ais8_1_31` point weather telemetry) and `DAC = 1, FI = 22` (`Ais8_1_22` Area Notice).
* **Software Support:** Supported in `libais` (`Ais8_200_23`), `gpsd`, `pyais`, and Inland ECDIS displays.

---

### 39.3.2 `DAC = 200, FI = 24`: Water Level (Msg 8, `168 bits`, `Ais8_200_24`)

#### 1. How It Works (Bit-Level Mechanics & Hydrometric Gauge Math)
On free-flowing rivers such as the Rhine, Elbe, and middle/lower Danube, water levels fluctuate by up to **$8\text{ meters}$** between summer droughts and spring snowmelt floods. Every inland skipper calculates their maximum permissible vessel draught $T_{\max}$ over the shallowest bottleneck of their planned route (such as the famous **Kaub gauge** at Rhine-km $546.3$ or **Maxau**, **Ruhrort**, **Pfelling**, and **Wildungsmauer**) using the fundamental inland hydrometric equation:

$$D_{\text{channel}}(t) = D_{\text{EqWL}} + \Delta H_{\text{gauge}}(t) = D_{\text{EqWL}} + \left(W_{\text{gauge}}(t) - W_{\text{EqWL}}\right)$$
$$T_{\max}(t) = D_{\text{channel}}(t) - \text{UKC}_{\text{safety}}$$

where:
* $D_{\text{EqWL}}$ is the guaranteed charted **Fairway Depth at Equivalent Water Level** (*Fahrrinnentiefe bei Gleichwertigem Wasserstand [GlW]* on the Rhine, or *Low Navigable Water Level [RNW]* on the Danube; e.g., $D_{\text{EqWL}} = 1.90\text{ m}$ at Kaub).
* $W_{\text{gauge}}(t)$ is the current staff-gauge reading (*Pegelstand*) in centimeters, and $W_{\text{EqWL}}$ is the gauge reading corresponding to GlW/RNW (e.g., $W_{\text{EqWL}} = 78\text{ cm}$ at Kaub).
* $\Delta H_{\text{gauge}}(t) = W_{\text{gauge}}(t) - W_{\text{EqWL}}$ is the **Water Level Difference to Reference Level** (in `0.01 m` centimeter steps), broadcast directly in **`DAC = 200, FI = 24`**!

A single 1-slot **Message 8 (`168 bits`)** broadcasts the real-time centimeter water levels of **up to 4 river gauges simultaneously**:

| Bit Range (0-Based `libais`) | Python Slice | Bit Range (1-Based ITU) | Width (Bits) | Field Name (`libais` identifier) | Data Type / Scaling | Operational Range & Sentinel Values |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `0..55` | `[0:56]` | `1..56` | `56` | Broadcast Msg 8 Header | Standard | `Message ID = 8`, `DAC = 200`, `FI = 24` |
| **`56..67`** | **`[56:68]`** | **`57..68`** | **`12`** | **UN Country Code (`country`)** | **2 $\times$ 6-bit ASCII** | **ISO 3166-1 alpha-2 (`"DE"`, `"NL"`, `"AT"`, `"HU"`)** |
| **`68..78`** | **`[68:79]`** | **`69..79`** | **`11`** | **Gauge ID #1 (`gauge_id[0]`)** | **Unsigned int** | **`1`–`2047` national gauge index; `0` = unused slot** |
| **`79..92`** | **`[79:93]`** | **`80..93`** | **`14`** | **Water Level Diff #1 (`level[0]`)** | **14-bit signed, `0.01 m`** | **`-8191` to `+8191` $\rightarrow$ `-81.91 m` to `+81.91 m`; `-8192` (`0x2000`) = N/A** |
| **`93..103`** | **`[93:104]`** | **`94..104`** | **`11`** | **Gauge ID #2 (`gauge_id[1]`)** | **Unsigned int** | **`1`–`2047`; `0` = unused slot** |
| **`104..117`** | **`[104:118]`** | **`105..118`** | **`14`** | **Water Level Diff #2 (`level[1]`)** | **14-bit signed, `0.01 m`** | **`-81.91 m` to `+81.91 m`; `-8192` = N/A** |
| **`118..128`** | **`[118:129]`** | **`119..129`** | **`11`** | **Gauge ID #3 (`gauge_id[2]`)** | **Unsigned int** | **`1`–`2047`; `0` = unused slot** |
| **`129..142`** | **`[129:143]`** | **`130..143`** | **`14`** | **Water Level Diff #3 (`level[2]`)** | **14-bit signed, `0.01 m`** | **`-81.91 m` to `+81.91 m`; `-8192` = N/A** |
| **`143..153`** | **`[143:154]`** | **`144..154`** | **`11`** | **Gauge ID #4 (`gauge_id[3]`)** | **Unsigned int** | **`1`–`2047`; `0` = unused slot** |
| **`154..167`** | **`[154:168]`** | **`155..168`** | **`14`** | **Water Level Diff #4 (`level[3]`)** | **14-bit signed, `0.01 m`** | **`-81.91 m` to `+81.91 m`; `-8192` = N/A** |

#### 2. Engineering Issues, Quirks, & Parser Edge Cases
* **Sign-Magnitude vs. Two's Complement in `level[i]` (`14 bits`):** This is one of the most critical hardware/software divergence points in `DAC = 200`. While ITU-R M.1371 mandates standard two's complement for all signed integers, the wording of the CESNI *Inland AIS Test Standard* states for the 14-bit Water Level Difference: *"Bit 0 [MSB]: `0` = positive, `1` = negative, Bits 1–13: `0` to `8191` (`-81.91` to `+81.91 m`)"*. Notice how `libais` (`src/libais/ais8_200.cpp`) explicitly implements this **1-bit sign + 13-bit magnitude** rule:
  ```cpp
  const int pos = !bs[offset + 11]; // MSB = 0 is positive, MSB = 1 is negative
  const int raw_level = bs.ToUnsignedInt(offset + 12, 13);
  level[i] = (pos ? raw_level : -1 * raw_level) / 100.0f;
  ```
  Wait: some shore stations encode negative water levels (below GlW/RNW during drought!) using **1-bit sign + 13-bit magnitude**, while others use **14-bit two's complement**! When decoding negative gauge levels, parsers should cross-check magnitude sanity (`|ΔH| < 15.0 m`; if a two's complement decode yields `-79.50 m` on the Rhine, the transmitter used sign-magnitude for `-2.42 m`, and vice versa!).

#### 3. Relationships, 4. Uses & Abuses, 5. Where/When Used, & 6. Software Support
* **Relationships:** Inland counterpart to IMO `DAC = 1, FI = 31` water-level field and St. Lawrence Seaway `DAC = 316, FI = 2` (Chapter 40).
* **Operational Uses:** Directly drives dynamic shallow-water depth contours (*Tiefenlinien*) in **Inland ECDIS Mode 1 (Navigation Mode)**, coloring shoals red in real time when $D_{\text{channel}}(t) < T_{\text{static}} + \text{UKC}$.
* **Adversarial Abuses:** Spoofing a falsified `FI = 24` message with artificially high $\Delta H_{\text{gauge}} = +1.50\text{ m}$ during low water could lure a heavily laden freighter onto a rocky sill (such as the *Jungferngrund* near Oberwesel); conversely, spoofing a flood level above **HSW** could halt commercial navigation along a river sector.
* **Where/When Used:** Broadcast every $10\text{ to }15\text{ minutes}$ by RIS shore base stations in Austria (*DoRIS*), Germany (*PEGELONLINE* / WSV testbeds), Hungary, Slovakia, and the Netherlands.

---

### 39.3.3 `DAC = 200, FI = 40`: Signal Status (Msg 8, `168 bits`, `Ais8_200_40`)

#### 1. How It Works (Bit-Level Mechanics & CEVNI Light-Matrix Encoding)
European rivers use complex multi-lamp **CEVNI / RPR optical light signals (*Wahrschau- und Schleusensignale*)** to control entry into lock chambers, passage under movable bridges, and alternating one-way traffic through blind rocky bends (such as the **Rhine Gorge / Loreley *Wahrschauer* stations** at Oberwesel, Bankeck, and Bingen, or the **Grein / Struden gorge** on the Austrian Danube). In dense river fog, skippers cannot see the physical signal masts on the riverbank until they are within $50\text{ m}$—far too late to stop a $4,000\text{ tonne}$ downstream-bound convoy moving at $22\text{ km/h}$ over ground!

`DAC = 200, FI = 40` broadcasts the exact geographical location, mast geometry (`form`), orientation, traffic direction (`impact`), and individual bulb states (`9 lights × 3 bits = 27 bits` inside a `30-bit` field) in a single-slot **Message 8 (`168 bits`)**:

| Bit Range (0-Based `libais`) | Python Slice | Bit Range (1-Based ITU) | Width (Bits) | Field Name (`libais` identifier) | Data Type / Scaling | Operational Range & Sentinel Values |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `0..55` | `[0:56]` | `1..56` | `56` | Broadcast Msg 8 Header | Standard | `Message ID = 8`, `DAC = 200`, `FI = 40` |
| **`56..83`** | **`[56:84]`** | **`57..84`** | **`28`** | **Signal Longitude (`x` / `lon`)** | **Signed int, $10^{-4}\text{ min}$** | **$\pm 180^\circ$ (`val / 600,000.0`); `108600000` (`181°`) = N/A** |
| **`84..110`** | **`[84:111]`** | **`85..111`** | **`27`** | **Signal Latitude (`y` / `lat`)** | **Signed int, $10^{-4}\text{ min}$** | **$\pm 90^\circ$ (`val / 600,000.0`); `54600000` (`91°`) = N/A** |
| **`111..114`** | **`[111:115]`** | **`112..115`** | **`4`** | **Signal Form (`form`)** | **Unsigned enum** | **`0` = Unknown; `1`–`14` = CEVNI mast/matrix layout template** |
| **`115..123`** | **`[115:124]`** | **`116..124`** | **`9`** | **Orientation (`dir` / `orientation`)** | **Unsigned int, $1^\circ$** | **`0`–`359` degrees true beam direction; `360` = N/A** |
| **`124..126`** | **`[124:127]`** | **`125..127`** | **`3`** | **Impact Direction (`direction`)** | **Unsigned enum** | **`0` = Unknown; `1` = Upstream (*Bergfahrt*); `2` = Downstream (*Talfahrt*); `3` = Both directions; `4` = Left bank; `5` = Right bank** |
| **`127..156`** | **`[127:157]`** | **`128..157`** | **`30`** | **Light Status (`status`)** | **9 (or 10) $\times$ 3-bit octal codes** | **Each 3-bit group $L_k \in [0, 7]$: `0` = Dark/Off; `1` = White; `2` = Red; `3` = Green; `4` = Yellow; `5` = Flashing White; `6` = Flashing Red; `7` = Flashing Yellow/Green** |
| `157..167` | `[157:168]` | `158..168` | `11` | Spare (`spare2`) | Unsigned int | Always `0` |

#### 2. Engineering Issues, 3. Relationships, 4. Uses & Abuses, 5. Where/When Used, & 6. Software Support
* **Coordinate Precision Contrast (`1/10,000 min` vs. `FI = 23`'s `1/1,000 min`):** Unlike `FI = 23`, `FI = 40` uses standard **$1/10,000\text{ minute}$** precision ($\approx 0.18\text{ m}$) so that Inland ECDIS can plot the exact lock-chamber gate signal on the correct pier wall (North vs. South chamber).
* **Operational Uses & Abuses:** Enables zero-visibility fog approaches to locks and gorge sections. Spoofing `FI = 40` (`Red-Red` $\rightarrow$ `Green-Green`) is a severe physical-safety hazard, which is why Inland ECDIS regulations require skippers to visually verify physical lock lights before crossing the lock threshold.

---

## 39.4 United Kingdom & Ireland General Lighthouse Authorities (`DAC = 232 / 235, FI = 10`, Msg 6/8, `Ais8_235_10`)

### 1. Operational & Conceptual Overview
Around the stormy, tide-swept coasts of Great Britain, Ireland, and the Isle of Man, more than $1,200$ lighthouses, lightvessels, racons, and lighted offshore buoys are maintained by the three **General Lighthouse Authorities (GLAs)**:
1. **Trinity House** (England, Wales, the Channel Islands, and Gibraltar), founded by Royal Charter of Henry VIII in **1514**.
2. **The Northern Lighthouse Board (NLB)** (Scotland and the Isle of Man), established in **1786** and engineered by four generations of the **Stevenson family** (builders of Bell Rock, Skerryvore, and Muckle Flugga).
3. **The Commissioners of Irish Lights (CIL)** (the entire island of Ireland), tracing its lineage to **1786**.

While ITU-R M.1371 **Message 21 (*Aid-to-Navigation Report*, Chapter 36)** broadcasts an AtoN's position, type, dimensions, and an unstructured 8-bit `AtoN Status` page (`bits[251:259]`), GLA maintenance engineers need continuous **quantitative engineering telemetry** from solar-powered offshore buoys and unmanned rock lighthouses: exact **battery voltage**, **solar panel / wind turbine charging voltage**, **Racon health**, **main/standby LED lantern status**, **intrusion hatch switches**, and **bilge flood alarms**.

Instead of paying recurring satellite telemetry fees for every offshore buoy, the three GLAs standardized **`DAC = 235` (or `DAC = 232`), `FI = 10` (*GLA Aid to Navigation Monitoring Data*)** over VHF AIS (both MID `232` and `235` are assigned by the ITU to the United Kingdom; `235` is the primary operational code). Every GLA AIS-equipped buoy or lighthouse transmits Message 21 for mariners and periodically transmits `DAC = 235, FI = 10` (via Broadcast Message 8 or Addressed Message 6 to a GLA shore base station) for engineering telemetry.

---

### 2. Deep Technical & Bit-Level Specification (`DAC = 232 / 235, FI = 10`)
In Broadcast Message 8 form (`Ais8_235_10`), the core payload occupies **`104 bits`** (often zero-padded by transponders to a full 1-slot **`168-bit`** frame); in Addressed Message 6 form (`Ais6_235_10`), the `32-bit` larger header shifts all payload offsets by `+32 bits` (`88..135` = `136 bits`, or `168 bits` padded):

| Bit Range (Msg 8 `0`-Based) | Bit Range (Msg 6 `0`-Based) | Bit Range (Msg 8 `1`-Based) | Width (Bits) | Field Name (`libais` identifier) | Data Type / Scaling | Operational Range & Sentinel Values |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `0..55` | `0..87` | `1..56` | `56` / `88` | Binary Message Header | Standard | `Message ID = 8` or `6`, `DAC = 235` (or `232`), `FI = 10` |
| **`56..65`** | **`88..97`** | **`57..66`** | **`10`** | **Analogue Internal (`ana_int`)** | **Unsigned int, `0.05 V`** | **`1`–`1023` $\rightarrow$ `0.05 V` to `51.15 V` (internal battery bus); `0` = not available / unmonitored** |
| **`66..75`** | **`98..107`** | **`67..76`** | **`10`** | **Analogue External #1 (`ana_ext1`)** | **Unsigned int, `0.05 V`** | **`1`–`1023` $\rightarrow$ `0.05 V` to `51.15 V` (primary battery / solar array); `0` = N/A** |
| **`76..85`** | **`108..117`** | **`77..86`** | **`10`** | **Analogue External #2 (`ana_ext2`)** | **Unsigned int, `0.05 V`** | **`1`–`1023` $\rightarrow$ `0.05 V` to `51.15 V` (secondary / reserve battery); `0` = N/A** |
| **`86..87`** | **`118..119`** | **`87..88`** | **`2`** | **Racon Status (`racon`)** | **Unsigned enum** | **`0` = No Racon installed; `1` = Racon monitored, not operating; `2` = Racon operating normally; `3` = Racon error / fault** |
| **`88..89`** | **`120..121`** | **`89..90`** | **`2`** | **Light Status (`light`)** | **Unsigned enum** | **`0` = No light / unmonitored; `1` = Light ON; `2` = Light OFF (daytime normal); `3` = Light error / failed** |
| **`90`** | **`122`** | **`91`** | **`1`** | **Health Alarm (`health`)** | **Boolean flag** | **`0` = Good health; `1` = Alarm active (transponder or power fault)** |
| **`91..98`** | **`123..130`** | **`92..99`** | **`8`** | **Status Bits External (`stat_ext`)** | **8 discrete digital inputs (`DI7..DI0`)** | **Bitmask (`0` = OFF/Normal, `1` = ON/Active): emergency lantern, fog horn, hatch intrusion switch, bilge water sensor, regulator fault, etc.** |
| **`99`** | **`131`** | **`100`** | **`1`** | **Off Position Status (`off_pos`)** | **Boolean flag** | **`0` = On station; `1` = Off position / adrift (mooring chain parted!)** |
| `100..103` (`..167`) | `132..135` (`..167`) | `101..104` | `4` (`68`) | Spare (`spare2`) | Unsigned int | Always `0` (`104 bits` nominal in Msg 8, `136 bits` nominal in Msg 6, or `168 bits` slot-padded) |

##### Voltage Scaling Equations
Each 10-bit voltage integer $N_V \in [0, 1023]$ scales linearly with a step size of $\Delta V = 0.05\text{ V}$ ($50\text{ mV}$):
$$V\text{ (Volts)} = \begin{cases} \text{None} & \text{if } N_V = 0 \\ 0.05 \times N_V & \text{if } 1 \le N_V \le 1023 \quad (\text{Range: } 0.05\text{ V to } 51.15\text{ V}) \end{cases}$$

For a standard $12\text{ V}$ or $24\text{ V}$ lead-acid / $\text{LiFePO}_4$ marine AtoN battery bank, `0.05 V` resolution allows GLA shore engineers in Harwich (Trinity House), Edinburgh (NLB), and Dún Laoghaire (CIL) to track diurnal solar charging curves, detect sulfated cells during December winter storms, and dispatch a lighthouse tender (*Galaro*, *Patricia*, *Pharos*, or *Granuaile*) weeks before a buoy's main lantern goes dark.

---

### 3. Six-Dimension Analysis of `DAC = 232 / 235, FI = 10`
1. **Engineering Issues & Parser Edge Cases:**
   * **Variable Bit Length (`104`, `136`, or `168` bits):** Because `104 bits` is only $62\%$ of a 168-bit TDMA slot, some AtoN transponders (e.g., SRT Marine / em-trak AtoN units) emit a `104-bit` Message 8 (`18` 6-bit ASCII chars, `fill_bits = 4`), whereas others zero-pad the payload to `168 bits` (`28` chars, `fill_bits = 0`). In `libais` (`src/libais/ais8_235.cpp`), `bs.size() != 104` is checked strictly, so any 168-bit padded frame or Message 6 (`136-bit`) variant must be stripped of trailing spare bits or routed by message ID before invoking `Ais8_235_10`.
   * **Dual `DAC` (`232` vs. `235`):** Although `DAC = 235` is standard, some legacy GLA stations and test transponders transmit `DAC = 232, FI = 10` with the exact same bit layout. Parsers should bind both `(232, 10)` and `(235, 10)` to the same decoder class.
2. **Relationships to Other AIS Messages:**
   * Directly paired with **ITU-R M.1371 Message 21 (*Aid-to-Navigation Report*)**. Look at the 8-bit `AtoN Status` field (`bits[251:259]`) in Message 21 when transmitted by a UK/Irish buoy: the GLAs map bits `86..90` (`Racon [2b]`, `Light [2b]`, `Health [1b]`) of `DAC = 235, FI = 10` directly into the regional `AtoN Status` byte of Message 21!
3. **Operational Uses & Adversarial Abuses:**
   * **Operational Uses:** Zero-cost VHF telemetry of battery state-of-charge, solar regulator output, main/reserve lantern switching, Racon failure, bilge flooding, and security hatch intrusion across UK/Irish waters.
   * **Adversarial Abuses:** Because `stat_ext` carries physical intrusion hatch switches and `ana_int` reveals battery depletion, an adversary monitoring VHF can identify remote unlit buoys or unmanned rock stations whose batteries or intrusion sensors have failed; conversely, spoofing `light = 3` (Light Error) or `off_pos = 1` (Adrift) can trigger false Notice to Mariners (NtM) alerts and costly buoy-tender dispatches.
4. **Where and When Used:** Transmitted every $15\text{ to }60\text{ minutes}$ (or immediately upon status alarm edge transition) around the coasts of the UK, Ireland, the English Channel, the Irish Sea, the Scottish Hebrides/Orkneys/Shetlands, and the North Sea oil/gas and offshore wind farm perimeters.
5. **Software Support:** Supported in `libais` (`Ais8_235_10` in `src/libais/ais8_235.cpp`), `gpsd` (`dac=235, fid=10`), `pyais`, and GLA shore-side SCADA monitoring systems.

---

## 39.5 Complete Software Support Matrix & Runnable Python Decoder/Encoder

### 1. Cross-Ecosystem Software Support Matrix

| Subtype (`DAC, FI`) | Carrier Msg | Bit Width | `libais` (C++ / Python) | `gpsd` (`driver_ais.c`) | `pyais` | Inland ECDIS (Periskal / Tresco / Argonics) | SOLAS Deep-Sea ECDIS |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`200, 10` (Inland Static & Voyage)** | Msg 8 | `168` | Full (`Ais8_200_10`) | Full | Full | **Native Primary** (ENI, `0.1 m` hull, blue cones) | Ignored unless Inland mode unlocked |
| **`200, 21` (Lock/Bridge ETA)** | Msg 6 | `248 / 256` | Full (`Ais6_200_21`, checks `248b`) | Full | Full | **Native** (ISRS lock request & `0.01 m` air draught) | Ignored |
| **`200, 22` (Lock/Bridge RTA)** | Msg 6 | `232 / 248` | Full (`Ais6_200_22`, checks `232b`) | Full | Full | **Native** (JIT speed advisory & lock status) | Ignored |
| **`200, 23` (EMMA Met Warning)** | Msg 8 | `256` | Full (`Ais8_200_23`) | Full | Full | **Native** (weather hazard overlay) | Ignored |
| **`200, 24` (Water Level Gauges)** | Msg 8 | `168` | Full (`Ais8_200_24`) | Full | Full | **Native** (dynamic shoal contour calculation) | Ignored |
| **`200, 40` (Signal Status)** | Msg 8 | `168` | Full (`Ais8_200_40`) | Full | Full | **Native** (virtual CEVNI light matrix) | Ignored |
| **`200, 55` (Persons on Board)** | Msg 6 / 8 | `168 / 136` | Full (`Ais8_200_55`) | Full | Full | Supported (SAR manifest) | Ignored |
| **`232 / 235, 10` (UK/IE GLA AtoN)** | Msg 6 / 8 | `104 / 136 / 168` | Full (`Ais8_235_10`, checks `104b`) | Full | Full | Ignored | Ignored (GLA SCADA & VTS only) |

---

### 2. Practical Engineering Walkthrough: Complete Python Bit-Level Encoder & Decoder
The following self-contained, dependency-free Python 3 script encodes and forensically decodes all five primary regional binary schemas covered in this chapter (`DAC=200, FI=10`, `DAC=200, FI=21`, `DAC=200, FI=22`, `DAC=200, FI=24` with Rhine Kaub under-keel clearance math, and `DAC=235, FI=10` GLA buoy telemetry), handling both CESNI and legacy `libais` bit-length variants:

```python
#!/usr/bin/env python3
"""Forensic Bit-Level Encoder/Decoder for European Inland AIS (DAC=200)
and UK/Ireland GLA AtoN Telemetry (DAC=232/235, FI=10).
"""
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

AIS_CHARS = "@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_ !\"#$%&'()*+,-./0123456789:;<=>?"


def pack_bits(fields: List[Tuple[int, int]]) -> str:
    """Packs a list of (value, bit_width) tuples into a binary bitstring."""
    bits = []
    for val, width in fields:
        if val < 0:
            val = (1 << width) + val  # Two's complement
        bits.append(f"{val & ((1 << width) - 1):0{width}b}")
    return "".join(bits)


def encode_sixbit_ascii(text: str, num_chars: int) -> Tuple[int, int]:
    """Encodes an ASCII string into (integer_value, total_bits) of 6-bit AIS chars."""
    padded = text.upper().ljust(num_chars, "@")[:num_chars]
    val = 0
    for ch in padded:
        idx = AIS_CHARS.find(ch)
        val = (val << 6) | (0 if idx < 0 else idx)
    return val, num_chars * 6


def decode_sixbit_ascii(bitstr: str) -> str:
    """Decodes a 6-bit ASCII bitstring, stripping trailing '@' padding."""
    chars = []
    for i in range(0, len(bitstr), 6):
        idx = int(bitstr[i : i + 6], 2)
        chars.append(AIS_CHARS[idx])
    return "".join(chars).rstrip("@").strip()


def u_int(bitstr: str, start: int, end: int) -> int:
    return int(bitstr[start:end], 2)


def s_int(bitstr: str, start: int, end: int) -> int:
    width = end - start
    val = int(bitstr[start:end], 2)
    return val - (1 << width) if (val & (1 << (width - 1))) else val


def bits_to_nmea_payload(bitstr: str) -> Tuple[str, int]:
    """Converts a bitstring into an NMEA 0183 6-bit armored payload and fill bits."""
    fill = (6 - (len(bitstr) % 6)) % 6
    padded = bitstr + ("0" * fill)
    payload = []
    for i in range(0, len(padded), 6):
        val = int(padded[i : i + 6], 2)
        ascii_code = val + 48 if val < 40 else val + 56
        payload.append(chr(ascii_code))
    return "".join(payload), fill


def nmea_payload_to_bits(payload: str, fill_bits: int = 0) -> str:
    """Unpacks an NMEA 0183 6-bit armored payload into a MSB-first bitstring."""
    chunks = []
    for ch in payload:
        val = ord(ch) - 48
        if val > 40:
            val -= 8
        chunks.append(f"{val:06b}")
    full_bits = "".join(chunks)
    return full_bits[:-fill_bits] if fill_bits > 0 else full_bits


ERI_TYPES: Dict[int, str] = {
    8000: "Vessel, type unknown",
    8010: "Motor freighter (GMS)",
    8020: "Motor tanker (TMS, liquid cargo)",
    8030: "Inland container vessel",
    8040: "Inland gas tanker (LPG/LNG)",
    8050: "Coupled motor freighter convoy (Koppelverband)",
    8210: "Pushed convoy, 1 barge",
    8220: "Pushed convoy, 2 barges",
    8240: "Pushed convoy, 4 barges (Vierer-Schubverband)",
    8260: "Pushed convoy, 6 barges (Sechser-Schubverband)",
    8290: "Pushed tanker convoy",
    8430: "Pushboat, single",
    8440: "Passenger ship / Ferry",
    8443: "River cruise ship (Flusskreuzfahrtschiff)",
}

BLUE_CONES: Dict[int, str] = {
    0: "0 blue cones/lights (Non-ADN / No separation required)",
    1: "1 blue cone/light (ADN Flammable - 10 m mooring separation)",
    2: "2 blue cones/lights (ADN Toxic - 50 m mooring separation)",
    3: "3 blue cones/lights (ADN Explosive - 100 m separation, solo lockage)",
    4: "B-flag (National flammable cargo)",
    5: "Unknown / Not available",
}


def decode_dac200_fi10(bitstr: str) -> Dict[str, object]:
    """Decodes DAC=200, FI=10 (Inland Ship Static and Voyage Related Data, 168b)."""
    if len(bitstr) < 168:
        raise ValueError(f"Expected >=168 bits for DAC=200, FI=10; got {len(bitstr)}")
    raw_len = u_int(bitstr, 104, 117)
    raw_beam = u_int(bitstr, 117, 127)
    eri_code = u_int(bitstr, 127, 141)
    haz = u_int(bitstr, 141, 144)
    raw_draught = u_int(bitstr, 144, 155)
    loaded = u_int(bitstr, 155, 157)
    return {
        "mmsi": u_int(bitstr, 8, 38),
        "dac": u_int(bitstr, 40, 50),
        "fi": u_int(bitstr, 50, 56),
        "eni": decode_sixbit_ascii(bitstr[56:104]),
        "length_m": round(raw_len * 0.1, 1) if 1 <= raw_len <= 8000 else None,
        "beam_m": round(raw_beam * 0.1, 1) if 1 <= raw_beam <= 1000 else None,
        "eri_type_code": eri_code,
        "eri_type_desc": ERI_TYPES.get(eri_code, "Other ERI classification"),
        "blue_cones": haz,
        "blue_cones_desc": BLUE_CONES.get(haz, "Reserved"),
        "draught_m": round(raw_draught * 0.01, 2) if 1 <= raw_draught <= 2000 else None,
        "loaded_status": {0: "N/A", 1: "Loaded", 2: "Unloaded", 3: "Reserved"}[loaded],
        "speed_quality_high": bool(u_int(bitstr, 157, 158)),
        "course_quality_high": bool(u_int(bitstr, 158, 159)),
        "heading_quality_high": bool(u_int(bitstr, 159, 160)),
    }


def decode_dac200_fi21_fi22(bitstr: str) -> Dict[str, object]:
    """Decodes DAC=200, FI=21 (ETA) and FI=22 (RTA) at Lock/Bridge/Terminal."""
    fi = u_int(bitstr, 82, 88)
    country = decode_sixbit_ascii(bitstr[88:100])
    locode = decode_sixbit_ascii(bitstr[100:130])
    section = decode_sixbit_ascii(bitstr[130:160])
    terminal = decode_sixbit_ascii(bitstr[160:190])
    hecto_str = decode_sixbit_ascii(bitstr[190:220])
    river_km = round(int(hecto_str) * 0.1, 1) if hecto_str.isdigit() else None
    base = {
        "source_mmsi": u_int(bitstr, 8, 38),
        "dest_mmsi": u_int(bitstr, 40, 70),
        "dac": u_int(bitstr, 72, 82),
        "fi": fi,
        "isrs_code": f"{country}{locode}{section}{terminal}{hecto_str}",
        "river_km": river_km,
        "month": u_int(bitstr, 220, 224),
        "day": u_int(bitstr, 224, 229),
        "hour_utc": u_int(bitstr, 229, 234),
        "minute_utc": u_int(bitstr, 234, 240),
    }
    if fi == 21:
        raw_air = u_int(bitstr, 243, 255) if len(bitstr) >= 255 else u_int(bitstr, 243, 248)
        base["assisting_tugs"] = u_int(bitstr, 240, 243)
        base["air_draught_m"] = round(raw_air * 0.01, 2) if 1 <= raw_air <= 4000 else None
    elif fi == 22:
        st = u_int(bitstr, 240, 242)
        base["lock_status"] = {
            0: "Operational",
            1: "Limited operation",
            2: "Out of order / Closed",
            3: "N/A",
        }[st]
    return base


def decode_dac200_fi24(bitstr: str, sign_magnitude: bool = True) -> Dict[str, object]:
    """Decodes DAC=200, FI=24 (Water Level, 168b) for up to 4 river gauges."""
    country = decode_sixbit_ascii(bitstr[56:68])
    gauges = []
    for i in range(4):
        offset = 68 + i * 25
        gid = u_int(bitstr, offset, offset + 11)
        if gid == 0:
            continue
        if sign_magnitude:
            sign = -1 if u_int(bitstr, offset + 11, offset + 12) == 1 else 1
            mag = u_int(bitstr, offset + 12, offset + 25)
            raw_cm = sign * mag
        else:
            raw_cm = s_int(bitstr, offset + 11, offset + 25)
        gauges.append({"gauge_id": gid, "delta_ref_m": round(raw_cm * 0.01, 2)})
    return {"mmsi": u_int(bitstr, 8, 38), "country": country, "gauges": gauges}


def decode_dac235_fi10(bitstr: str) -> Dict[str, object]:
    """Decodes DAC=232/235, FI=10 (UK/Ireland GLA AtoN Monitoring Data)."""
    msg_id = u_int(bitstr, 0, 6)
    p = 88 if msg_id == 6 else 56
    v_int = u_int(bitstr, p, p + 10)
    v_ext1 = u_int(bitstr, p + 10, p + 20)
    v_ext2 = u_int(bitstr, p + 20, p + 30)
    racon = u_int(bitstr, p + 30, p + 32)
    light = u_int(bitstr, p + 32, p + 34)
    return {
        "mmsi": u_int(bitstr, 8, 38),
        "dac": u_int(bitstr, p - 16, p - 6),
        "fi": u_int(bitstr, p - 6, p),
        "internal_batt_v": round(v_int * 0.05, 2) if v_int > 0 else None,
        "external1_solar_v": round(v_ext1 * 0.05, 2) if v_ext1 > 0 else None,
        "external2_aux_v": round(v_ext2 * 0.05, 2) if v_ext2 > 0 else None,
        "racon_status": {0: "No Racon", 1: "Not operating", 2: "Operating", 3: "Fault"}[racon],
        "light_status": {0: "No light", 1: "ON", 2: "OFF (Day)", 3: "Failed"}[light],
        "health_alarm": bool(u_int(bitstr, p + 34, p + 35)),
        "external_digital_mask": f"0b{u_int(bitstr, p + 35, p + 43):08b}",
        "off_position_adrift": bool(u_int(bitstr, p + 43, p + 44)),
    }


if __name__ == "__main__":
    # 1. Encode & Decode DAC=200, FI=10: 4-barge pushed tanker convoy on the Rhine
    fi10_bits = pack_bits([
        (8, 6), (0, 2), (211456780, 30), (0, 2), (200, 10), (10, 6),
        encode_sixbit_ascii("04801234", 8),
        (1850, 13),  # 185.0 m convoy length
        (228, 10),   # 22.8 m convoy beam (2 barges wide)
        (8290, 14),  # Pushed tanker convoy
        (2, 3),      # 2 ADN Blue Cones (toxic cargo: 50 m mooring separation)
        (278, 11),   # 2.78 m static draught (1 cm precision!)
        (1, 2),      # Loaded
        (1, 1), (1, 1), (1, 1), (0, 8),
    ])
    payload_fi10, fill_fi10 = bits_to_nmea_payload(fi10_bits)
    print(f"DAC=200, FI=10 NMEA Payload ({len(fi10_bits)}b): !AIVDM,1,1,,A,{payload_fi10},{fill_fi10}*XX")
    print("Decoded FI=10:", decode_dac200_fi10(nmea_payload_to_bits(payload_fi10, fill_fi10)))

    # 2. Encode & Decode DAC=200, FI=24: Rhine Gauge at Kaub (Gauge ID 546, +0.92 m above GlW)
    fi24_bits = pack_bits([
        (8, 6), (0, 2), (2111200, 30), (0, 2), (200, 10), (24, 6),
        encode_sixbit_ascii("DE", 2),
        (546, 11), (0, 1), (92, 13),   # Kaub: +0.92 m above GlW (1.90 m + 0.92 m = 2.82 m depth)
        (591, 11), (1, 1), (18, 13),   # Oestrich: -0.18 m below GlW (sign-magnitude!)
        (0, 11), (0, 14), (0, 11), (0, 14),
    ])
    print("Decoded FI=24 (Rhine Gauges):", decode_dac200_fi24(fi24_bits))

    # 3. Encode & Decode DAC=235, FI=10: Trinity House Offshore Buoy Telemetry (104b)
    gla_bits = pack_bits([
        (8, 6), (0, 2), (992351122, 30), (0, 2), (235, 10), (10, 6),
        (256, 10),  # 12.80 V internal battery
        (284, 10),  # 14.20 V solar charging bus
        (252, 10),  # 12.60 V reserve battery
        (2, 2),     # Racon operating normally
        (1, 2),     # Main LED lantern ON
        (0, 1),     # Good health
        (0b00000100, 8),  # DI2 active
        (0, 1),     # On station (not adrift)
        (0, 4),
    ])
    print("Decoded DAC=235, FI=10 (GLA Buoy):", decode_dac235_fi10(gla_bits))
```

---

## 39.6 Key Takeaways & Operational Checklist

1. **Always Fuse `DAC = 200, FI = 10` with ITU-R M.1371 Message 5 on European Waterways:** Never rely solely on Message 5's $1\text{ m}$ integer hull dimensions or $0.1\text{ m}$ draught when analyzing traffic on the Rhine, Danube, Elbe, Moselle, or Dutch/Belgian waterways. Use `FI = 10` (`Ais8_200_10`) to obtain `0.1 m` convoy dimensions (`length`, `beam`), `0.01 m` centimeter draught (`draught`), 8-digit European Vessel ID (`eu_id` / ENI), 4-digit ERI convoy classification (`8000–8490`), and ADN dangerous-cargo blue-cone state (`0–3`).
2. **Beware the `FI = 23` ($1/1,000\text{ min}$) vs. `FI = 40` ($1/10,000\text{ min}$) Coordinate Scaling Trap:** Even though both `DAC = 200, FI = 23` (EMMA Meteorological Warning) and `DAC = 200, FI = 40` (Signal Status) use `28-bit` Longitude and `27-bit` Latitude fields, `FI = 23` scales coordinates in **$1/1,000\text{ minute}$** ($\div 60,000$), whereas `FI = 40` uses standard **$1/10,000\text{ minute}$** ($\div 600,000$).
3. **Handle Sign-Magnitude vs. Two's Complement in `DAC = 200, FI = 24` Water Levels:** Verify whether regional RIS base stations transmit negative gauge offsets (`level[0..3]`, below GlW/RNW reference level) using CESNI's **1-bit MSB sign + 13-bit magnitude** (`libais` behavior) or standard **14-bit two's complement**.
4. **Accept Both Legacy CCNR and Padded CESNI Bit Lengths:** Configure binary message parsers to accept `248–256 bits` for `Ais6_200_21`, `232–248 bits` for `Ais6_200_22`, `136–168 bits` for `Ais8_200_55`, and `104 / 136 / 168 bits` for UK/Ireland GLA `Ais8_235_10` / `Ais6_235_10` (across both `DAC = 232` and `DAC = 235`).

---

## 39.7 Cited References & Primary Sources

1. **CESNI (European Committee for Drawing Up Standards in the Field of Inland Navigation):** *European Standard for River Information Services (ES-RIS 2023/1)* and *Inland AIS Test Standard (Edition 2021/2023)*, Central Commission for the Navigation of the Rhine (CCNR), Strasbourg. [https://www.cesni.eu/](https://www.cesni.eu/)
2. **European Parliament & Council of the European Union:** *Directive 2005/44/EC of 7 September 2005 on harmonised river information services (RIS) on inland waterways in the Community*, together with *Commission Implementing Regulation (EU) 2019/838 on technical specifications for Vessel Tracking and Tracing systems (Inland AIS)*.
3. **UNECE (United Nations Economic Commission for Europe):** *Resolution No. 63: International Standard for Tracking and Tracing on Inland Waterways (VTT)* (`ECE/TRANS/SC.3/176/Rev.2`) and *European Agreement concerning the International Carriage of Dangerous Goods by Inland Waterways (ADN)*, Geneva.
4. **CCNR (Central Commission for the Navigation of the Rhine):** *Police Regulations for the Navigation of the Rhine (Rheinschifffahrtspolizeiverordnung — RheinSchPV / RPR)*, Article 3.14 (ADN Blue Cones/Lights) and Article 4.07 (Inland AIS carriage mandate).
5. **General Lighthouse Authorities of the United Kingdom and Ireland (Trinity House, Northern Lighthouse Board, Commissioners of Irish Lights):** *GLA AIS Aid-to-Navigation (AtoN) Monitoring Data Specification (`DAC = 232 / 235, FI = 10`)* and IALA Guideline G1114.
6. **Schwehr, K. (2010–2024):** `libais` C++ implementation of European Inland AIS (`src/libais/ais8_200.cpp`, `src/libais/ais6.cpp`) and UK/Ireland GLA AtoN telemetry (`src/libais/ais8_235.cpp`), GitHub (`schwehr/libais`).
