# Appendix B: Maritime Identification Digits (MID) and MMSI Prefix Lookup Table

> **Purpose:** This appendix provides the complete lookup reference for decoding any 9-digit **Maritime Mobile Service Identity (MMSI)** (`User ID`, `bits[8:38]`) into its **ITU-R M.585-9 station category**, **subtype**, and **Flag State / Geographical Administration** via the 3-digit **Maritime Identification Digits (`MID`, `201`–`775`)** maintained by the International Telecommunication Union (ITU Radiocommunication Bureau, Table of Maritime Identification Digits).

---

## B.1 Master MMSI Prefix & Structural Pattern Reference (ITU-R M.585-9 & M.2135-0)

Always zero-pad the 30-bit unsigned integer (`bits[8:38]`) to **exactly 9 decimal digits** (`D1 D2 D3 D4 D5 D6 D7 D8 D9`, e.g., `f"{mmsi:09d}"`) before evaluating prefix patterns.

| Prefix / Digit Pattern | Station Category | Position of `MID` (1-Based Digits) | Subtype / Trailing-Digit Semantics | Typical AIS Message Types | Standard Clause |
|---|---|---|---|---|---|
| **`MIDxxxxxx`**<br/>($D_1 \in \{2..7\}$) | **1. Standard Ship Station** | Digits `1–3`<br/>($D_1 D_2 D_3 \in [201, 775]$) | • `MIDxxx000`: Inmarsat global direct-dial tier<br/>• `MIDxxxx00`: Regional / Inmarsat-C tier<br/>• `MIDxxxxx0` / `MIDxxxxxx`: General Class A/B | `1, 2, 3, 5, 18, 19, 24, 27` | ITU-R M.585-9 Annex 1 §1 |
| **`0MIDxxxxx`**<br/>($D_1 = 0, D_2 \in \{2..7\}$) | **2. Group Ship Station Call** | Digits `2–4`<br/>($D_2 D_3 D_4 \in [201, 775]$) | `xxxxx` = 5-digit Fleet, Company, or Coast Guard Group ID (e.g., `036699999` USCG Group) | `6, 12, 16, 23` (Addressed / Group) | ITU-R M.585-9 Annex 1 §2 |
| **`00MIDxxxx`**<br/>($D_1 D_2 = 00, D_3 \in \{2..7\}$) | **3. Coast Station / Base Station** | Digits `3–5`<br/>($D_3 D_4 D_5 \in [201, 775]$) | `xxxx` = 4-digit Shore VTS, Coast Radio, or AIS Base Station / Repeater ID | `4, 11, 16, 17, 20, 22, 23` | ITU-R M.585-9 Annex 1 §3 |
| **`111MIDxxx`**<br/>($D_1 D_2 D_3 = 111$) | **4. SAR Aircraft** | Digits `4–6`<br/>($D_4 D_5 D_6 \in [201, 775]$) | • `111MID1xx` ($D_7 = 1$): **Fixed-Wing SAR Aircraft**<br/>• `111MID5xx` ($D_7 = 5$): **Rotary-Wing SAR Helicopter**<br/>• Other $D_7$: Specialized SAR Aircraft / UAV | `9` (SAR Aircraft Position Report) | ITU-R M.585-9 Annex 1 §4 |
| **`8MIDxxxxx`**<br/>($D_1 = 8, D_2 \in \{2..7\}$) | **11. Handheld VHF DSC Radio / Regional Inland Craft** | Digits `2–4`<br/>($D_2 D_3 D_4 \in [201, 775]$) | `xxxxx` = 5-digit non-ship-associated VHF handheld transceiver with GNSS / diver radio | DSC Ch 70 / Class B `18, 24` | ITU-R M.585-9 Annex 3 |
| **`970xxyyyy`**<br/>($D_1 D_2 D_3 = 970$) | **7. AIS-SART** (Search & Rescue Transmitter) | *None* (Global free-form) | • `xx` ($D_4 D_5 \in [01, 99]$): 2-digit CIRM/ITU Manufacturer ID<br/>• `yyyy` ($D_6..D_9 \in [0000, 9999]$): Unit Serial # | `1` (`NavStatus = 14`), `14` (`"SART ACTIVE"`) | ITU-R M.585-9 Annex 2 §1; IEC 61097-14 |
| **`972xxyyyy`**<br/>($D_1 D_2 D_3 = 972$) | **8. AIS-MOB** (Man Overboard Device) | *None* (Global free-form) | • `xx` ($D_4 D_5$): 2-digit Manufacturer ID<br/>• `yyyy` ($D_6..D_9$): 4-digit Unit Serial # | `1` (`NavStatus = 14`), `14` (`"MOB ACTIVE"`) | ITU-R M.585-9 Annex 2 §2; IEC 63269 |
| **`974xxyyyy`**<br/>($D_1 D_2 D_3 = 974$) | **9. EPIRB-AIS** (406 MHz EPIRB + AIS Homing) | *None* (Global free-form) | • `xx` ($D_4 D_5$): 2-digit Manufacturer ID<br/>• `yyyy` ($D_6..D_9$): 4-digit Unit Serial # | `1` (`NavStatus = 14`), `14` (`"EPIRB ACTIVE"`) | ITU-R M.585-9 Annex 2 §3; MSC.471(101) |
| **`979zzzzzz`**<br/>($D_1 D_2 D_3 = 979$) | **10. AMRD Group B** (Autonomous Maritime Radio Device) | *None* (Global free-form) | `zzzzzz` ($D_4..D_9$): 6-digit Non-Navigation Buoy / Fishing Gear / Drifter ID ($\le 1\text{ W}$ on Ch 2006 $160.900\text{ MHz}$) | `18, 24` (Part A `"AMRD"`) on $160.900\text{ MHz}$ | ITU-R M.585-9 Annex 4; ITU-R M.2135-0 |
| **`98MIDxxxx`**<br/>($D_1 D_2 = 98, D_3 \in \{2..7\}$) | **5. Craft Associated with a Parent Ship** | Digits `3–5`<br/>($D_3 D_4 D_5 \in [201, 775]$) | `xxxx` = Lifeboat, Fast Rescue Boat, Daughter Craft, or Yacht Tender (Msg 24 Part B `bits[132:162]` holds Mother-Ship MMSI) | `18, 19, 24` | ITU-R M.585-9 Annex 1 §5 |
| **`99MIDxxxx`**<br/>($D_1 D_2 = 99, D_3 \in \{2..7\}$) | **6. Aid to Navigation (AtoN)** | Digits `3–5`<br/>($D_3 D_4 D_5 \in [201, 775]$) | • `99MID1xxx` ($D_6 = 1$): **Physical AtoN** (Real or Synthetic)<br/>• `99MID6xxx` ($D_6 = 6$): **Virtual AtoN**<br/>• Other $D_6$: Mobile/Regional AtoN | `21` (AtoN Report), `6, 8` (Met/Hydro) | ITU-R M.585-9 Annex 1 §6; IALA A-126 |

### B.1.1 Common Non-Standard & Anomalous MMSI Patterns Encountered in Raw AIS Feeds

| Pattern / Value | Observed Origin in the Wild | Recommended Decoder / Pipeline Action |
|---|---|---|
| **`000000000`**, **`111111111`**, **`123456789`**, **`999999999`**, **`888888888`** | Unconfigured factory-default transponders or installer keypad test sequences. | Flag `is_default_mmsi = True`; split tracks by spatial velocity gating ($v_{\text{implied}} \le v_{\max}$). |
| **`MID000000`** (e.g., `366000000`, `412000000`) | Partial installer entry where only the 3-digit country `MID` was entered. | Flag as unconfigured suffix (`suffix == "000000"`). |
| **`190xxxxxx`**, **`888xxxxxx`**, **`998xxxxxx`**, **`100xxxxxx`** | Uncertified commercial fishing net-buoys ("sun-buoys" / net pingers) transmitting illegally on AIS 1/2. | Classify as `UNCERTIFIED_NET_BUOY`; exclude from vessel collision/density statistics. |
| **`1000000000` – `1073741823`** (`0x3B9ACA00` – `0x3FFFFFFF`) | 10-digit unsigned 30-bit binary overflow caused by unflagged bit errors or `0x3FFFFFFF` all-ones memory initialization. | Reject prior to `CHAR(9)` string formatting; log as `UINT30_OVERFLOW`. |

---

## B.2 Complete ITU Maritime Identification Digits (`201`–`775`) Lookup Table

### B.2.1 Region `2xx`: Europe (Including Mediterranean and Russian Federation)

| MID | ISO Alpha-2 / Alpha-3 | Country / Geographical Area / Administration | Operational & Registry Notes |
|---|---|---|---|
| **`201`** | `AL` / `ALB` | **Albania** (Republic of) | Adriatic coastal & merchant fleet |
| **`202`** | `AD` / `AND` | **Andorra** (Principality of) | Landlocked administration |
| **`203`** | `AT` / `AUT` | **Austria** | Danube Inland AIS (`DAC 200`) & sea-going yachts |
| **`204`** | `PT` / `PRT` | **Portugal — Azores** | Autonomous Region of the Azores (see also `255` Madeira, `263` Portugal) |
| **`205`** | `BE` / `BEL` | **Belgium** | Antwerp/Zeebrugge VTS, North Sea & Rhine/Scheldt Inland AIS |
| **`206`** | `BY` / `BLR` | **Belarus** (Republic of) | Inland waterway fleet |
| **`207`** | `BG` / `BGR` | **Bulgaria** (Republic of) | Black Sea & Danube fleet |
| **`208`** | `VA` / `VAT` | **Vatican City State** | State of the Vatican City |
| **`209`** | `CY` / `CYP` | **Cyprus** (Republic of) | Major EU open registry (1st of 3 MIDs: `209`, `210`, `212`) |
| **`210`** | `CY` / `CYP` | **Cyprus** (Republic of) | Major EU open registry (2nd of 3 MIDs) |
| **`211`** | `DE` / `DEU` | **Germany** (Federal Republic of) | Primary German flag & Rhine/Elbe Inland AIS (see also `218`) |
| **`212`** | `CY` / `CYP` | **Cyprus** (Republic of) | Major EU open registry (3rd of 3 MIDs) |
| **`213`** | `GE` / `GEO` | **Georgia** | Black Sea ports (Batumi, Poti) |
| **`214`** | `MD` / `MDA` | **Moldova** (Republic of) | Giurgiulești Danube/Black Sea registry |
| **`215`** | `MT` / `MLT` | **Malta** | Largest EU ship registry by tonnage (1st of 5 MIDs: `215`, `229`, `248`, `249`, `256`) |
| **`216`** | `AM` / `ARM` | **Armenia** (Republic of) | Landlocked administration |
| **`218`** | `DE` / `DEU` | **Germany** (Federal Republic of) | Secondary German MID (originally allocated to GDR; unified with `211`) |
| **`219`** | `DK` / `DNK` | **Denmark** | Primary Danish & DIS (Danish International Register) MID (see also `220`) |
| **`220`** | `DK` / `DNK` | **Denmark** | Secondary Danish MID (see also `231` Faroe Islands, `331` Greenland) |
| **`224`** | `ES` / `ESP` | **Spain** | Primary Spanish MID (1st of 2: `224`, `225`) |
| **`225`** | `ES` / `ESP` | **Spain** | Secondary Spanish MID |
| **`226`** | `FR` / `FRA` | **France** | Primary metropolitan France & RIF registry (1st of 3: `226`, `227`, `228`) |
| **`227`** | `FR` / `FRA` | **France** | Metropolitan France (2nd of 3 MIDs) |
| **`228`** | `FR` / `FRA` | **France** | Metropolitan France (3rd of 3 MIDs) |
| **`229`** | `MT` / `MLT` | **Malta** | Malta Ship Registry (2nd of 5 MIDs) |
| **`230`** | `FI` / `FIN` | **Finland** | Baltic Sea, icebreakers, & Åland fleet |
| **`231`** | `FO` / `FRO` | **Faroe Islands** (Kingdom of Denmark) | Faroese International Ship Register (FAS) |
| **`232`** | `GB` / `GBR` | **United Kingdom** of Great Britain and Northern Ireland | UK Ship Register & MCA Coastguard (1st of 4 MIDs: `232`–`235`) |
| **`233`** | `GB` / `GBR` | **United Kingdom** of Great Britain and Northern Ireland | UK Ship Register (2nd of 4 MIDs) |
| **`234`** | `GB` / `GBR` | **United Kingdom** of Great Britain and Northern Ireland | UK Ship Register (3rd of 4 MIDs) |
| **`235`** | `GB` / `GBR` | **United Kingdom** of Great Britain and Northern Ireland | UK Ship Register & recreational Class B (4th of 4 MIDs) |
| **`236`** | `GI` / `GIB` | **Gibraltar** (United Kingdom) | Red Ensign Group Category 1 registry (Strait of Gibraltar) |
| **`237`** | `GR` / `GRC` | **Greece** | Major merchant fleet (1st of 4 MIDs: `237`, `239`, `240`, `241`) |
| **`238`** | `HR` / `HRV` | **Croatia** (Republic of) | Adriatic merchant, passenger, & charter fleet |
| **`239`** | `GR` / `GRC` | **Greece** | Greek merchant & coastal fleet (2nd of 4 MIDs) |
| **`240`** | `GR` / `GRC` | **Greece** | Greek merchant & coastal fleet (3rd of 4 MIDs) |
| **`241`** | `GR` / `GRC` | **Greece** | Greek merchant & coastal fleet (4th of 4 MIDs) |
| **`242`** | `MA` / `MAR` | **Morocco** (Kingdom of) | Allocated in `2xx` block due to Mediterranean/Strait of Gibraltar proximity |
| **`243`** | `HU` / `HUN` | **Hungary** | Danube Inland AIS (`DAC 200`) |
| **`244`** | `NL` / `NLD` | **Netherlands** (Kingdom of the) | Primary Dutch maritime & Rhine/Meuse Inland AIS (1st of 3: `244`–`246`) |
| **`245`** | `NL` / `NLD` | **Netherlands** (Kingdom of the) | Netherlands (2nd of 3 MIDs) |
| **`246`** | `NL` / `NLD` | **Netherlands** (Kingdom of the) | Netherlands (3rd of 3 MIDs; see also `306` Dutch Caribbean) |
| **`247`** | `IT` / `ITA` | **Italy** | Italian merchant fleet, ferries, & Guardia Costiera VTS |
| **`248`** | `MT` / `MLT` | **Malta** | Malta Ship Registry (3rd of 5 MIDs) |
| **`249`** | `MT` / `MLT` | **Malta** | Malta Ship Registry (4th of 5 MIDs) |
| **`250`** | `IE` / `IRL` | **Ireland** | Irish merchant, fishing, & Irish Coast Guard |
| **`251`** | `IS` / `ISL` | **Iceland** | North Atlantic fishing & coast guard fleet |
| **`252`** | `LI` / `LIE` | **Liechtenstein** (Principality of) | Landlocked administration |
| **`253`** | `LU` / `LUX` | **Luxembourg** | Luxembourg Public Maritime Register & Moselle/Rhine barges |
| **`254`** | `MC` / `MCO` | **Monaco** (Principality of) | Superyachts & Monaco coastal stations |
| **`255`** | `PT` / `PRT` | **Portugal — Madeira** | International Shipping Register of Madeira (MAR) |
| **`256`** | `MT` / `MLT` | **Malta** | Malta Ship Registry (5th of 5 MIDs) |
| **`257`** | `NO` / `NOR` | **Norway** | Norwegian Ordinary (NOR) & International (NIS) Registers (1st of 3: `257`–`259`) |
| **`258`** | `NO` / `NOR` | **Norway** | Norway (2nd of 3 MIDs) |
| **`259`** | `NO` / `NOR` | **Norway** | Norway offshore/fishing/coastal (3rd of 3 MIDs) |
| **`261`** | `PL` / `POL` | **Poland** (Republic of) | Baltic ports (Gdańsk, Gdynia, Szczecin) & Oder/Vistula |
| **`262`** | `ME` / `MNE` | **Montenegro** | Bar/Kotor Adriatic registry |
| **`263`** | `PT` / `PRT` | **Portugal** | Mainland Portugal registry (see also `204` Azores, `255` Madeira) |
| **`264`** | `RO` / `ROU` | **Romania** | Constanța Black Sea & Lower Danube Inland AIS |
| **`265`** | `SE` / `SWE` | **Sweden** | Birthplace of SOTDMA AIS (1st of 2 MIDs: `265`, `266`) |
| **`266`** | `SE` / `SWE` | **Sweden** | Sweden (2nd of 2 MIDs) |
| **`267`** | `SK` / `SVK` | **Slovak Republic** | Bratislava Danube Inland AIS |
| **`268`** | `SM` / `SMR` | **San Marino** (Republic of) | San Marino Ship Register |
| **`269`** | `CH` / `CHE` | **Switzerland** (Swiss Confederation) | Basel Rhine fleet & ocean-going Swiss merchant ships |
| **`270`** | `CZ` / `CZE` | **Czech Republic** | Elbe/Vltava Inland AIS & sea-going yachts |
| **`271`** | `TR` / `TUR` | **Türkiye** (Republic of) | Turkish Straits (Bosporus/Dardanelles) VTS & merchant fleet |
| **`272`** | `UA` / `UKR` | **Ukraine** | Black Sea, Sea of Azov, & Dnieper/Danube fleet |
| **`273`** | `RU` / `RUS` | **Russian Federation** | Russian Maritime Register, Northern Sea Route icebreakers, & river fleet |
| **`274`** | `MK` / `MKD` | **North Macedonia** (Republic of) | Lake Ohrid & inland craft |
| **`275`** | `LV` / `LVA` | **Latvia** (Republic of) | Riga, Ventspils, & Liepāja Baltic fleet |
| **`276`** | `EE` / `EST` | **Estonia** (Republic of) | Tallinn Gulf of Finland & Baltic fleet |
| **`277`** | `LT` / `LTU` | **Lithuania** (Republic of) | Klaipėda Baltic fleet |
| **`278`** | `SI` / `SVN` | **Slovenia** (Republic of) | Port of Koper northern Adriatic fleet |
| **`279`** | `RS` / `SRB` | **Serbia** (Republic of) | Belgrade Danube/Sava/Tisza Inland AIS |

---

### B.2.2 Region `3xx`: North America, Central America, and the Caribbean

| MID | ISO Alpha-2 / Alpha-3 | Country / Geographical Area / Administration | Operational & Registry Notes |
|---|---|---|---|
| **`301`** | `AI` / `AIA` | **Anguilla** (United Kingdom) | Red Ensign Group Category 2 Caribbean registry |
| **`303`** | `US` / `USA` | **United States of America — Alaska** | Dedicated MID for vessels & USCG shore stations/AtoNs in **Alaska** (1st of 6 US MIDs) |
| **`304`** | `AG` / `ATG` | **Antigua and Barbuda** | Major Caribbean commercial/container feeder open registry (1st of 2: `304`, `305`) |
| **`305`** | `AG` / `ATG` | **Antigua and Barbuda** | Antigua and Barbuda (2nd of 2 MIDs) |
| **`306`** | `BQ` / `CW` / `SX` | **Curaçao, Sint Maarten, Bonaire, Sint Eustatius and Saba** | Kingdom of the Netherlands Caribbean territories |
| **`307`** | `AW` / `ABW` | **Aruba** (Kingdom of the Netherlands) | Aruba maritime administration |
| **`308`** | `BS` / `BHS` | **Bahamas** (Commonwealth of the) | Major global cruise, LNG, & tanker registry (1st of 3 MIDs: `308`, `309`, `311`) |
| **`309`** | `BS` / `BHS` | **Bahamas** (Commonwealth of the) | Bahamas Maritime Authority (2nd of 3 MIDs) |
| **`310`** | `BM` / `BMU` | **Bermuda** (United Kingdom) | Red Ensign Group Category 1 registry (LNG, cruise ships, tankers) |
| **`311`** | `BS` / `BHS` | **Bahamas** (Commonwealth of the) | Bahamas Maritime Authority (3rd of 3 MIDs) |
| **`312`** | `BZ` / `BLZ` | **Belize** | International Merchant Marine Registry of Belize (IMMARBE) |
| **`314`** | `BB` / `BRB` | **Barbados** | Barbados Maritime Ship Registry |
| **`316`** | `CA` / `CAN` | **Canada** | Canadian Coast Guard MCTS/VTS, St. Lawrence Seaway (`DAC 316`), & merchant/fishing fleet |
| **`319`** | `KY` / `CYM` | **Cayman Islands** (United Kingdom) | Premier global superyacht & Red Ensign Category 1 registry |
| **`321`** | `CR` / `CRI` | **Costa Rica** | Pacific & Caribbean coastal fleet |
| **`323`** | `CU` / `CUB` | **Cuba** | Cuban coastal & port fleet |
| **`325`** | `DM` / `DMA` | **Dominica** (Commonwealth of) | Dominica International Maritime Registry |
| **`327`** | `DO` / `DOM` | **Dominican Republic** | Caribbean port & coastal fleet |
| **`329`** | `GP` / `GLP` | **Guadeloupe** (French Department of) | French Antilles administration |
| **`330`** | `GD` / `GRD` | **Grenada** | Grenada coastal & yacht fleet |
| **`331`** | `GL` / `GRL` | **Greenland** (Kingdom of Denmark) | Arctic fishing, research, & passenger vessels |
| **`332`** | `GT` / `GTM` | **Guatemala** (Republic of) | Pacific (Puerto Quetzal) & Caribbean (Santo Tomás) |
| **`334`** | `HN` / `HND` | **Honduras** (Republic of) | Puerto Cortés & regional open registry |
| **`336`** | `HT` / `HTI` | **Haiti** (Republic of) | Haitian coastal fleet |
| **`338`** | `US` / `USA` | **United States of America (Domestic / Recreational)** | Primarily assigned by BoatUS / Sea Tow / US Power Squadrons to domestic non-SOLAS vessels (2nd of 6 US MIDs) |
| **`339`** | `JM` / `JAM` | **Jamaica** | Ship Registry of Jamaica (Kingston hub) |
| **`341`** | `KN` / `KNA` | **Saint Kitts and Nevis** (Federation of) | St. Kitts & Nevis International Ship Registry |
| **`343`** | `LC` / `LCA` | **Saint Lucia** | Caribbean coastal & yacht registry |
| **`345`** | `MX` / `MEX` | **Mexico** | PEMEX offshore Gulf of Mexico fleet & Pacific/Gulf ports |
| **`347`** | `MQ` / `MTQ` | **Martinique** (French Department of) | French Antilles administration |
| **`348`** | `MS` / `MSR` | **Montserrat** (United Kingdom) | British Overseas Territory |
| **`350`** | `NI` / `NIC` | **Nicaragua** | Pacific & Caribbean fishing/coastal fleet |
| **`351`** | `PA` / `PAN` | **Panama** (Republic of) | World's largest ship registry by vessel count (1st of 12 MIDs: `351`–`357`, `370`–`374`) |
| **`352`** | `PA` / `PAN` | **Panama** (Republic of) | Panama Maritime Authority (2nd of 12 MIDs) |
| **`353`** | `PA` / `PAN` | **Panama** (Republic of) | Panama Maritime Authority (3rd of 12 MIDs) |
| **`354`** | `PA` / `PAN` | **Panama** (Republic of) | Panama Maritime Authority (4th of 12 MIDs) |
| **`355`** | `PA` / `PAN` | **Panama** (Republic of) | Panama Maritime Authority (5th of 12 MIDs) |
| **`356`** | `PA` / `PAN` | **Panama** (Republic of) | Panama Maritime Authority (6th of 12 MIDs) |
| **`357`** | `PA` / `PAN` | **Panama** (Republic of) | Panama Maritime Authority (7th of 12 MIDs) |
| **`358`** | `PR` / `PRI` | **Puerto Rico** (United States) | US Commonwealth in the Caribbean |
| **`359`** | `SV` / `SLV` | **El Salvador** (Republic of) | Acajutla / La Unión Pacific fleet |
| **`361`** | `PM` / `SPM` | **Saint Pierre and Miquelon** (France) | French Overseas Collectivity off Newfoundland |
| **`362`** | `TT` / `TTO` | **Trinidad and Tobago** | Point Lisas / LNG & offshore energy support fleet |
| **`364`** | `TC` / `TCA` | **Turks and Caicos Islands** (United Kingdom) | Red Ensign Group Category 2 registry |
| **`366`** | `US` / `USA` | **United States of America** | Primary US commercial, FCC-licensed, & **USCG NAIS (`00366xxxx` / `99366xxxx`)** MID (3rd of 6 US MIDs) |
| **`367`** | `US` / `USA` | **United States of America** | US commercial, towing, fishing, & recreational fleet (4th of 6 US MIDs) |
| **`368`** | `US` / `USA` | **United States of America** | US commercial & recreational fleet (5th of 6 US MIDs) |
| **`369`** | `US` / `USA` | **United States of America** | US commercial, federal, & military auxiliary fleet (6th of 6 US MIDs) |
| **`370`** | `PA` / `PAN` | **Panama** (Republic of) | Panama Maritime Authority (8th of 12 MIDs) |
| **`371`** | `PA` / `PAN` | **Panama** (Republic of) | Panama Maritime Authority (9th of 12 MIDs) |
| **`372`** | `PA` / `PAN` | **Panama** (Republic of) | Panama Maritime Authority (10th of 12 MIDs) |
| **`373`** | `PA` / `PAN` | **Panama** (Republic of) | Panama Maritime Authority (11th of 12 MIDs) |
| **`374`** | `PA` / `PAN` | **Panama** (Republic of) | Panama Maritime Authority (12th of 12 MIDs) |
| **`375`** | `VC` / `VCT` | **Saint Vincent and the Grenadines** | Major Caribbean open registry (1st of 3 MIDs: `375`, `376`, `377`) |
| **`376`** | `VC` / `VCT` | **Saint Vincent and the Grenadines** | St. Vincent & the Grenadines (2nd of 3 MIDs) |
| **`377`** | `VC` / `VCT` | **Saint Vincent and the Grenadines** | St. Vincent & the Grenadines (3rd of 3 MIDs) |
| **`378`** | `VG` / `VGB` | **British Virgin Islands** (United Kingdom) | Red Ensign Group Category 1 yacht & commercial registry |
| **`379`** | `VI` / `VIR` | **United States Virgin Islands** (United States) | US territory in the Lesser Antilles |

---

### B.2.3 Region `4xx`: Asia and the Middle East

| MID | ISO Alpha-2 / Alpha-3 | Country / Geographical Area / Administration | Operational & Registry Notes |
|---|---|---|---|
| **`401`** | `AF` / `AFG` | **Afghanistan** | Landlocked administration |
| **`403`** | `SA` / `SAU` | **Saudi Arabia** (Kingdom of) | Red Sea (Jeddah/Yanbu) & Arabian Gulf (Ras Tanura/Dammam) tanker & offshore fleet |
| **`405`** | `BD` / `BGD` | **Bangladesh** (People's Republic of) | Chittagong port, river fleet, & shipbreaking approaches |
| **`408`** | `BH` / `BHR` | **Bahrain** (Kingdom of) | Arabian Gulf port & naval hub |
| **`410`** | `BT` / `BTN` | **Bhutan** (Kingdom of) | Landlocked administration |
| **`412`** | `CN` / `CHN` | **China** (People's Republic of) | Primary mainland China merchant, coastal, & distant-water fishing MID (1st of 3: `412`–`414`) |
| **`413`** | `CN` / `CHN` | **China** (People's Republic of) | Mainland China coastal, Yangtze river, & fishing fleet (2nd of 3 MIDs) |
| **`414`** | `CN` / `CHN` | **China** (People's Republic of) | Mainland China merchant & fishing fleet (3rd of 3 MIDs; see also `453` Macao, `477` Hong Kong) |
| **`416`** | `TW` / `TWN` | **Taiwan** (Province of China / Chinese Taipei) | Major container shipping (Evergreen, Yang Ming, Wan Hai) & distant-water longline fleet |
| **`417`** | `LK` / `LKA` | **Sri Lanka** (Democratic Socialist Republic of) | Colombo transshipment hub & Indian Ocean traffic separation scheme |
| **`419`** | `IN` / `IND` | **India** (Republic of) | Indian merchant fleet, offshore Mumbai High, & Indian Coast Guard |
| **`422`** | `IR` / `IRN` | **Iran** (Islamic Republic of) | Persian Gulf / Strait of Hormuz (IRISL & NITC tanker fleet) |
| **`423`** | `AZ` / `AZE` | **Azerbaijan** (Republic of) | Baku Caspian Sea tanker, ferry, & offshore oil/gas fleet |
| **`425`** | `IQ` / `IRQ` | **Iraq** (Republic of) | Basra / Al Basrah Oil Terminal & Umm Qasr |
| **`428`** | `IL` / `ISR` | **Israel** (State of) | Haifa, Ashdod, & Eilat maritime administration |
| **`431`** | `JP` / `JPN` | **Japan** | Primary Japanese merchant, coastal ferry, & Japan Coast Guard MID (1st of 2: `431`, `432`) |
| **`432`** | `JP` / `JPN` | **Japan** | Japan (2nd of 2 MIDs) |
| **`434`** | `TM` / `TKM` | **Turkmenistan** | Türkmenbaşy Caspian Sea fleet |
| **`436`** | `KZ` / `KAZ` | **Kazakhstan** (Republic of) | Aktau / Kashagan Caspian Sea offshore & tanker fleet |
| **`437`** | `UZ` / `UZB` | **Uzbekistan** (Republic of) | Amu Darya / inland administration |
| **`438`** | `JO` / `JOR` | **Jordan** (Hashemite Kingdom of) | Port of Aqaba (Gulf of Aqaba) |
| **`440`** | `KR` / `KOR` | **Korea (Republic of — South Korea)** | Major global shipbuilding, merchant, & fishing nation (1st of 2 MIDs: `440`, `441`) |
| **`441`** | `KR` / `KOR` | **Korea (Republic of — South Korea)** | South Korea (2nd of 2 MIDs) |
| **`443`** | `PS` / `PSE` | **Palestine** (State of) | Allocated per ITU Resolution 99 |
| **`445`** | `KP` / `PRK` | **Democratic People's Republic of Korea (North Korea)** | Nampo, Wonsan, & Chongjin fleet |
| **`447`** | `KW` / `KWT` | **State of Kuwait** | Kuwait Oil Tanker Company (KOTC) & Mina Al Ahmadi |
| **`450`** | `LB` / `LBN` | **Lebanon** | Beirut & Tripoli eastern Mediterranean fleet |
| **`451`** | `KG` / `KGZ` | **Kyrgyz Republic** | Issyk-Kul & inland administration |
| **`453`** | `MO` / `MAC` | **Macao, China** | Macao Special Administrative Region of China |
| **`455`** | `MV` / `MDV` | **Maldives** (Republic of) | Indian Ocean inter-atoll & pole-and-line tuna fleet |
| **`457`** | `MN` / `MNG` | **Mongolia** | Landlocked open ship registry (Ulaanbaatar Mongolia Ship Registry) |
| **`459`** | `NP` / `NPL` | **Nepal** (Federal Democratic Republic of) | Landlocked administration |
| **`461`** | `OM` / `OMN` | **Oman** (Sultanate of) | Strait of Hormuz (Musandam VTS), Sohar, Duqm, & Salalah |
| **`463`** | `PK` / `PAK` | **Pakistan** (Islamic Republic of) | Karachi, Port Qasim, Gwadar, & Gadani shipbreaking approaches |
| **`466`** | `QA` / `QAT` | **State of Qatar** | Ras Laffan LNG carrier & offshore North Field fleet |
| **`468`** | `SY` / `SYR` | **Syrian Arab Republic** | Latakia & Tartus eastern Mediterranean fleet |
| **`470`** | `AE` / `ARE` | **United Arab Emirates** | Jebel Ali (Dubai), Fujairah bunkering hub, & Abu Dhabi ADNOC fleet (1st of 2: `470`, `471`) |
| **`471`** | `AE` / `ARE` | **United Arab Emirates** | United Arab Emirates (2nd of 2 MIDs) |
| **`472`** | `TJ` / `TJK` | **Tajikistan** (Republic of) | Landlocked administration |
| **`473`** | `YE` / `YEM` | **Yemen** (Republic of) | Aden, Hodeidah, & Bab el-Mandeb (1st of 2 MIDs: `473`, `475`) |
| **`475`** | `YE` / `YEM` | **Yemen** (Republic of) | Yemen (2nd of 2 MIDs) |
| **`477`** | `HK` / `HKG` | **Hong Kong, China** | Major global container, bulk carrier, & tanker registry (Hong Kong Shipping Register) |
| **`478`** | `BA` / `BIH` | **Bosnia and Herzegovina** | Allocated in `4xx` series after exhaustion of initial `2xx` European slots |

---

### B.2.4 Region `5xx`: Oceania and Southeast Asia

| MID | ISO Alpha-2 / Alpha-3 | Country / Geographical Area / Administration | Operational & Registry Notes |
|---|---|---|---|
| **`501`** | `TF` / `ATF` | **Adélie Land** (French Southern and Antarctic Territories) | Antarctic research stations & Southern Ocean patrol |
| **`503`** | `AU` / `AUS` | **Australia** | AMSA (Australian Maritime Safety Authority), ReefVTS (Great Barrier Reef), & iron ore/LNG ports |
| **`506`** | `MM` / `MMR` | **Myanmar** (Union of) | Yangon & Andaman Sea coastal fleet |
| **`508`** | `BN` / `BRN` | **Brunei Darussalam** | Brunei LNG & South China Sea offshore energy fleet |
| **`510`** | `FM` / `FSM` | **Micronesia** (Federated States of) | Western Pacific EEZ & tuna transshipment |
| **`511`** | `PW` / `PLW` | **Palau** (Republic of) | Palau International Ship Registry (PISR — frequently seen in re-flagging analyses) |
| **`512`** | `NZ` / `NZL` | **New Zealand** | Maritime New Zealand, Cook Strait ferries, & Southern Ocean fleet |
| **`514`** | `KH` / `KHM` | **Cambodia** (Kingdom of) | Sihanoukville & Mekong fleet (1st of 2 MIDs: `514`, `515`) |
| **`515`** | `KH` / `KHM` | **Cambodia** (Kingdom of) | Cambodia (2nd of 2 MIDs) |
| **`516`** | `CX` / `CXR` | **Christmas Island** (Australia) | Indian Ocean Australian external territory |
| **`518`** | `CK` / `COK` | **Cook Islands** | Maritime Cook Islands (South Pacific yacht & commercial open registry) |
| **`520`** | `FJ` / `FJI` | **Fiji** (Republic of) | Suva / Lautoka South Pacific hub |
| **`523`** | `CC` / `CCK` | **Cocos (Keeling) Islands** (Australia) | Indian Ocean Australian external territory |
| **`525`** | `ID` / `IDN` | **Indonesia** (Republic of) | World's largest archipelagic fleet (Sunda, Lombok, Makassar, & Malacca Straits) |
| **`529`** | `KI` / `KIR` | **Kiribati** (Republic of) | Kiribati Ship Registry & Central Pacific tuna purse-seine/transshipment hub |
| **`531`** | `LA` / `LAO` | **Lao People's Democratic Republic** | Upper Mekong river fleet |
| **`533`** | `MY` / `MYS` | **Malaysia** | Port Klang, Tanjung Pelepas, Malacca Strait VTS, & Petronas LNG/offshore fleet |
| **`536`** | `MP` / `MNP` | **Northern Mariana Islands** (United States) | US Commonwealth in the Western Pacific (Saipan/Tinian) |
| **`538`** | `MH` / `MHL` | **Marshall Islands** (Republic of the) | Top-3 global commercial registry (tankers, bulkers, container ships, offshore rigs) |
| **`540`** | `NC` / `NCL` | **New Caledonia** (France) | Nouméa nickel carriers & Coral Sea fleet |
| **`542`** | `NU` / `NIU` | **Niue** | Niue Ship Registry |
| **`544`** | `NR` / `NRU` | **Nauru** (Republic of) | Central Pacific island state |
| **`546`** | `PF` / `PYF` | **French Polynesia** (France) | Tahiti / Papeete & Marquesas/Tuamotu inter-island fleet |
| **`548`** | `PH` / `PHL` | **Philippines** (Republic of the) | Manila, Subic, Batangas inter-island Ro-Ro ferries & merchant fleet |
| **`550`** | `TL` / `TLS` | **Timor-Leste** (Democratic Republic of) | Dili & Timor Sea fleet |
| **`553`** | `PG` / `PNG` | **Papua New Guinea** | Port Moresby, Lae, & Vitiaz Strait / Bismarck Sea fleet |
| **`555`** | `PN` / `PCN` | **Pitcairn Island** (United Kingdom) | South Pacific British Overseas Territory |
| **`557`** | `SB` / `SLB` | **Solomon Islands** | Honiara & Western Pacific tuna fleet |
| **`559`** | `AS` / `ASM` | **American Samoa** (United States) | Pago Pago tuna fleet & US South Pacific territory |
| **`561`** | `WS` / `WSM` | **Samoa** (Independent State of) | Apia South Pacific fleet |
| **`563`** | `SG` / `SGP` | **Singapore** (Republic of) | Singapore Registry of Ships (SRS) & MPA VTIS (1st of 4 MIDs: `563`–`566`) |
| **`564`** | `SG` / `SGP` | **Singapore** (Republic of) | Singapore Registry of Ships (2nd of 4 MIDs) |
| **`565`** | `SG` / `SGP` | **Singapore** (Republic of) | Singapore Registry of Ships (3rd of 4 MIDs) |
| **`566`** | `SG` / `SGP` | **Singapore** (Republic of) | Singapore harbor craft, bunker tankers, & merchant fleet (4th of 4 MIDs) |
| **`567`** | `TH` / `THA` | **Thailand** | Laem Chabang, Bangkok, & Gulf of Thailand fleet |
| **`570`** | `TO` / `TON` | **Tonga** (Kingdom of) | Nukuʻalofa & Tonga registry |
| **`572`** | `TV` / `TUV` | **Tuvalu** | Tuvalu Ship Registry (Funafuti) |
| **`574`** | `VN` / `VNM` | **Viet Nam** (Socialist Republic of) | Haiphong, Ho Chi Minh City, Cai Mep, & South China Sea fishing/merchant fleet |
| **`576`** | `VU` / `VUT` | **Vanuatu** (Republic of) | Vanuatu International Shipping Registry (1st of 2 MIDs: `576`, `577` — offshore supply/tugs) |
| **`577`** | `VU` / `VUT` | **Vanuatu** (Republic of) | Vanuatu International Shipping Registry (2nd of 2 MIDs) |
| **`578`** | `WF` / `WLF` | **Wallis and Futuna Islands** (France) | French Overseas Collectivity in the South Pacific |

---

### B.2.5 Region `6xx`: Africa

| MID | ISO Alpha-2 / Alpha-3 | Country / Geographical Area / Administration | Operational & Registry Notes |
|---|---|---|---|
| **`601`** | `ZA` / `ZAF` | **South Africa** (Republic of) | Durban, Richards Bay, Cape Town, Saldanha Bay, & SAMSA coastal network |
| **`603`** | `AO` / `AGO` | **Angola** (Republic of) | Luanda & deepwater Cabinda/Congo Basin FPSO & offshore support fleet |
| **`605`** | `DZ` / `DZA` | **Algeria** (People's Democratic Republic of) | Algiers, Oran, & Arzew/Skikda LNG & hydrocarbon fleet |
| **`607`** | `TF` / `ATF` | **Saint Paul and Amsterdam Islands** (France) | Southern Indian Ocean French territory |
| **`608`** | `SH` / `SHN` | **Ascension Island** (United Kingdom) | South Atlantic British Overseas Territory |
| **`609`** | `BI` / `BDI` | **Burundi** (Republic of) | Lake Tanganyika fleet |
| **`610`** | `BJ` / `BEN` | **Benin** (Republic of) | Port of Cotonou (Gulf of Guinea) |
| **`611`** | `BW` / `BWA` | **Botswana** (Republic of) | Landlocked administration |
| **`612`** | `CF` / `CAF` | **Central African Republic** | Oubangui river administration |
| **`613`** | `CM` / `CMR` | **Cameroon** (Republic of) | Douala / Kribi & emerging open registry (frequently monitored in sanctions compliance) |
| **`615`** | `CG` / `COG` | **Congo** (Republic of the) | Pointe-Noire offshore & coastal fleet |
| **`616`** | `KM` / `COM` | **Comoros** (Union of the) | Moroni / Comoros open registry |
| **`617`** | `CV` / `CPV` | **Cabo Verde** (Republic of) | Mindelo / Praia Atlantic crossroads & bunkering hub |
| **`618`** | `TF` / `ATF` | **Crozet Archipelago** (France) | Southern Ocean French EEZ |
| **`619`** | `CI` / `CIV` | **Côte d'Ivoire** (Republic of) | Port of Abidjan & San-Pédro |
| **`620`** | `KM` / `COM` | **Comoros** (Union of the) | Comoros (2nd of 2 MIDs: `616`, `620`) |
| **`621`** | `DJ` / `DJI` | **Djibouti** (Republic of) | Bab el-Mandeb / Gulf of Aden strategic port & International Djibouti Open Registry |
| **`622`** | `EG` / `EGY` | **Egypt** (Arab Republic of) | **Suez Canal Authority (SCA)** tugs/pilot boats, Alexandria, Port Said, & Red Sea fleet |
| **`624`** | `ET` / `ETH` | **Ethiopia** (Federal Democratic Republic of) | Ethiopian Shipping and Logistics (ESLSE) merchant fleet |
| **`625`** | `ER` / `ERI` | **Eritrea** | Massawa & Assab Red Sea ports |
| **`626`** | `GA` / `GAB` | **Gabonese Republic** | Port-Gentil / Libreville & Gabon International Ship Registry (rapidly expanded 2022–2026) |
| **`627`** | `GH` / `GHA` | **Ghana** | Tema & Takoradi ports |
| **`629`** | `GM` / `GMB` | **Gambia** (Republic of the) | Banjul / River Gambia |
| **`630`** | `GW` / `GNB` | **Guinea-Bissau** (Republic of) |Guinea-Bissau International Ship Registry (G-BISR) |
| **`631`** | `GQ` / `GNQ` | **Equatorial Guinea** (Republic of) | Malabo, Bata, & Gulf of Guinea offshore oil/LNG fleet |
| **`632`** | `GN` / `GIN` | **Guinea** (Republic of) | Conakry & Kamsar bauxite export transshipment tugs/barges |
| **`633`** | `BF` / `BFA` | **Burkina Faso** | Landlocked administration |
| **`634`** | `KE` / `KEN` | **Kenya** (Republic of) | Port of Mombasa & Lamu |
| **`635`** | `TF` / `ATF` | **Kerguelen Islands** (France) | French Southern and Antarctic Lands (*TAAF* — traditional home port for French RIF ships) |
| **`636`** | `LR` / `LBR` | **Liberia** (Republic of) | **Liberian Registry (LISCR)** — world's largest or second-largest registry by GT (1st of 2: `636`, `637`) |
| **`637`** | `LR` / `LBR` | **Liberia** (Republic of) | Liberian Registry (2nd of 2 MIDs) |
| **`638`** | `SS` / `SSD` | **South Sudan** (Republic of) | White Nile administration |
| **`642`** | `LY` / `LBY` | **Libya** | Tripoli, Benghazi, Misrata, & Es Sider/Zawiya oil terminals |
| **`644`** | `LS` / `LSO` | **Lesotho** (Kingdom of) | Landlocked administration |
| **`645`** | `MU` / `MUS` | **Mauritius** (Republic of) | Port Louis Indian Ocean bunkering, fishing, & merchant hub |
| **`647`** | `MG` / `MDG` | **Madagascar** (Republic of) | Toamasina & Mozambique Channel fleet |
| **`649`** | `ML` / `MLI` | **Mali** (Republic of) | Niger River inland administration |
| **`650`** | `MZ` / `MOZ` | **Mozambique** (Republic of) | Maputo, Beira, Nacala, & Rovuma Basin LNG fleet |
| **`654`** | `MR` / `MRT` | **Mauritania** (Islamic Republic of) | Nouadhibou iron-ore / Canary Current pelagic fishing ground |
| **`655`** | `MW` / `MWI` | **Malawi** | Lake Malawi passenger & cargo fleet |
| **`656`** | `NE` / `NER` | **Niger** (Republic of the) | Landlocked administration |
| **`657`** | `NG` / `NGA` | **Nigeria** (Federal Republic of) | Lagos/Apapa, Lekki, Bonny LNG, & Niger Delta offshore OSV/security fleet |
| **`659`** | `NA` / `NAM` | **Namibia** (Republic of) | Walvis Bay & Lüderitz Benguela Current fishing/diamond mining fleet |
| **`660`** | `RE` / `REU` | **Réunion** (French Department of) | Indian Ocean French Overseas Department (includes Mayotte coverage) |
| **`661`** | `RW` / `RWA` | **Rwanda** (Republic of) | Lake Kivu administration |
| **`662`** | `SD` / `SDN` | **Sudan** (Republic of the) | Port Sudan Red Sea terminal |
| **`663`** | `SN` / `SEN` | **Senegal** (Republic of) | Port of Dakar West African hub |
| **`664`** | `SC` / `SYC` | **Seychelles** (Republic of) | Port Victoria Indian Ocean tuna purse-seine & tanker registry |
| **`665`** | `SH` / `SHN` | **Saint Helena** (United Kingdom) | South Atlantic British Overseas Territory |
| **`666`** | `SO` / `SOM` | **Somalia** (Federal Republic of) | Mogadishu, Berbera, & Bosaso |
| **`667`** | `SL` / `SLE` | **Sierra Leone** | Sierra Leone International Ship Registry (SLMARAD) |
| **`668`** | `ST` / `STP` | **São Tomé and Príncipe** (Democratic Republic of) | Gulf of Guinea island registry |
| **`669`** | `SZ` / `SWZ` | **Eswatini** (Kingdom of) | Landlocked Southern African administration *(Note: fraudulent "Eswatini" registries have been flagged by IMO)* |
| **`670`** | `TD` / `TCD` | **Chad** (Republic of) | Lake Chad administration |
| **`671`** | `TG` / `TGO` | **Togolese Republic** | Port of Lomé (major West African transshipment & STS bunkering anchorage) & Togo International Registry |
| **`672`** | `TN` / `TUN` | **Tunisia** | Rades, Bizerte, Sfax, & Sicilian Channel VTS |
| **`674`** | `TZ` / `TZA` | **Tanzania** (United Republic of) | Dar es Salaam & **Zanzibar Tanzania International Register of Shipping (TZIRS)** (1st of 2: `674`, `677`) |
| **`675`** | `UG` / `UGA` | **Uganda** (Republic of) | Lake Victoria ferries & cargo craft |
| **`676`** | `CD` / `COD` | **Democratic Republic of the Congo** | Matadi / Banana Atlantic mouth & Congo River |
| **`677`** | `TZ` / `TZA` | **Tanzania** (United Republic of) | Tanzania (2nd of 2 MIDs) |
| **`678`** | `ZM` / `ZMB` | **Zambia** (Republic of) | Lake Tanganyika / Kariba administration |
| **`679`** | `ZW` / `ZWE` | **Zimbabwe** (Republic of) | Lake Kariba administration |

---

### B.2.6 Region `7xx`: South America

| MID | ISO Alpha-2 / Alpha-3 | Country / Geographical Area / Administration | Operational & Registry Notes |
|---|---|---|---|
| **`701`** | `AR` / `ARG` | **Argentine Republic** | Buenos Aires, Río de la Plata / Paraná grain export corridor, & Patagonian Shelf ("Mile 201") patrol |
| **`710`** | `BR` / `BRA` | **Brazil** (Federative Republic of) | Santos, Paranaguá, Tubarão/Ponta da Madeira Valemax iron-ore terminals, & Petrobras pre-salt FPSO/OSV fleet |
| **`720`** | `BO` / `BOL` | **Bolivia** (Plurinational State of) | Landlocked open registry (*Registro Internacional Boliviano de Buques* — RIBB) & Lake Titicaca / Paraguay-Paraná |
| **`725`** | `CL` / `CHL` | **Chile** | Valparaíso, San Antonio, Strait of Magellan / Beagle Channel pilotage, & Chilean salmon/copper fleet |
| **`730`** | `CO` / `COL` | **Colombia** (Republic of) | Cartagena, Barranquilla, Santa Marta (Caribbean) & Buenaventura (Pacific) |
| **`735`** | `EC` / `ECU` | **Ecuador** | Guayaquil, Esmeraldas, & **Galápagos Marine Reserve** monitoring fleet |
| **`740`** | `FK` / `FLK` | **Falkland Islands (Malvinas)** | South Atlantic squid jigger / trawler licensing & Stanley harbor |
| **`745`** | `GF` / `GUF` | **French Guiana** (French Department of) | Dégrad des Cannes & Kourou CSG spaceport sea-exclusion patrol |
| **`750`** | `GY` / `GUY` | **Guyana** | Georgetown & rapidly growing Stabroek Block offshore FPSO/OSV fleet |
| **`755`** | `PY` / `PRY` | **Paraguay** (Republic of) | World's third-largest inland barge/pusher-tug fleet along the *Hidrovía Paraná-Paraguay* |
| **`760`** | `PE` / `PER` | **Peru** | Callao, Chancay, & Humboldt Current industrial anchoveta purse-seine fleet |
| **`765`** | `SR` / `SUR` | **Suriname** (Republic of) | Paramaribo & offshore Guiana Basin fleet |
| **`770`** | `UY` / `URY` | **Uruguay** (Eastern Republic of) | Montevideo South Atlantic transshipment/fishing hub & Nueva Palmira |
| **`775`** | `VE` / `VEN` | **Venezuela** (Bolivarian Republic of) | Jose, Maracaibo, Amuay/Cardón PDVSA terminals, & Orinoco River corridor |

---

## B.3 Multi-MID Flag State Consolidation Index (SQL / Python Reference)

When aggregating fleet statistics by Flag State in SQL, DuckDB, or Python, grouping by raw `MID` splits multi-MID registries into up to 12 fragments. Use the following canonical mapping to consolidate all MIDs belonging to the same sovereign administration or open registry:

| Consolidated Flag Administration | Count of MIDs | Allocated ITU MID Codes |
|---|---|---|
| **Panama** | 12 | `351, 352, 353, 354, 355, 356, 357, 370, 371, 372, 373, 374` |
| **United States of America** *(Core)* | 6 | `303` *(Alaska)*, `338` *(Domestic)*, `366, 367, 368, 369` *(plus territories `358` PR, `379` VI, `536` MP, `559` AS)* |
| **Malta** | 5 | `215, 229, 248, 249, 256` |
| **United Kingdom** *(Mainland)* | 4 | `232, 233, 234, 235` *(plus Red Ensign Group: `236` GI, `301` AI, `310` BM, `319` KY, `348` MS, `364` TC, `378` VG, `555` PN, `608`/`665` SH, `740` FK)* |
| **Greece** | 4 | `237, 239, 240, 241` |
| **Singapore** | 4 | `563, 564, 565, 566` |
| **Cyprus** | 3 | `209, 210, 212` |
| **France** *(Metropolitan)* | 3 | `226, 227, 228` *(plus Overseas/TAAF: `329` GP, `347` MQ, `361` PM, `501`/`607`/`618`/`635` TF, `540` NC, `546` PF, `578` WF, `660` RE, `745` GF)* |
| **Netherlands** *(European)* | 3 | `244, 245, 246` *(plus Caribbean: `306` BQ/CW/SX, `307` AW)* |
| **Norway** | 3 | `257, 258, 259` |
| **Portugal** *(Total)* | 3 | `204` *(Azores)*, `255` *(Madeira MAR)*, `263` *(Mainland)* |
| **Bahamas** | 3 | `308, 309, 311` |
| **Saint Vincent and the Grenadines** | 3 | `375, 376, 377` |
| **China** *(Mainland)* | 3 | `412, 413, 414` *(plus SARs: `453` Macao, `477` Hong Kong)* |
| **Germany** | 2 | `211, 218` |
| **Denmark** *(Mainland)* | 2 | `219, 220` *(plus `231` Faroe Islands, `331` Greenland)* |
| **Spain** | 2 | `224, 225` |
| **Sweden** | 2 | `265, 266` |
| **Antigua and Barbuda** | 2 | `304, 305` |
| **Japan** | 2 | `431, 432` |
| **Korea (Republic of)** | 2 | `440, 441` |
| **United Arab Emirates** | 2 | `470, 471` |
| **Yemen** | 2 | `473, 475` |
| **Cambodia** | 2 | `514, 515` |
| **Vanuatu** | 2 | `576, 577` |
| **Comoros** | 2 | `616, 620` |
| **Liberia** | 2 | `636, 637` |
| **Tanzania** | 2 | `674, 677` |
