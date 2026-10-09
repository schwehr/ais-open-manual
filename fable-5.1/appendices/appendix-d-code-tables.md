# Appendix D — Code tables

This appendix compiles the canonical enumerations, code tables, bit-level sentinel values, identity numbering formats, application identifier registries, and network interface mnemonics that govern the Automatic Identification System (AIS). Cross-references link each table to its theoretical analysis in [Chapter 13](../chapters/ch13-mmsi-deep-dive.md) (MMSI architecture), [Chapter 22](../chapters/ch22-message-catalog.md) (VDL message catalog), [Chapter 23](../chapters/ch23-asm-binary-payloads.md) (application-specific messages), [Chapter 25](../chapters/ch25-gnss-and-ais.md) (GNSS and EPFD sensing), [Chapter 26](../chapters/ch26-interfaces-and-logging.md) (NMEA 0183 and NMEA 2000 interfaces), and [Chapter 68](../chapters/ch68-special-purpose-ais.md) (AtoN, locating beacons, and AMRDs).

---

## D.1 Maritime Identification Digits (MID) by region

The **Maritime Identification Digit** (**MID**) is a three-digit decimal code ($X_1 X_2 X_3$) allocated by the International Telecommunication Union (**ITU**) Radiocommunication Bureau in accordance with Article 19 and Appendix 42 of the ITU Radio Regulations and Recommendation ITU-R M.585-10. The initial digit ($X_1$) defines the geographic region of the allocating administration ($2 \le X_1 \le 7$):

- **2**: Europe
- **3**: North America, Central America, and Caribbean
- **4**: Asia (excluding Southeast Asia) and Middle East
- **5**: Oceania, Australasia, and Southeast Asia
- **6**: Africa and Indian Ocean territories
- **7**: South America

When an administration exhausts 80% of its existing MID numbering capacity, it may petition the ITU Radiocommunication Bureau for an additional MID allocation (ITU-R M.585-10 Annex 3 §1(d)). Administrations administering major open ship registries or extensive domestic fleets consequently hold multiple MIDs.

The following master table registers the MID allocations across global maritime administrations and sovereign territories as published by the ITU:

### Table D.1: ITU Maritime Identification Digits (MID)

| MID | Allocating Administration / Territory | ITU Region | Notes / Secondary Allocations |
|:---:|:---|:---|:---|
| **201** | Albania (Republic of) | Europe (2) | |
| **202** | Andorra (Principality of) | Europe (2) | Landlocked state |
| **203** | Austria | Europe (2) | Danube inland fleet |
| **204** | Azores (Portugal) | Europe (2) | Autonomous Region of Azores |
| **205** | Belgium | Europe (2) | |
| **206** | Belarus (Republic of) | Europe (2) | Inland waterways |
| **207** | Bulgaria (Republic of) | Europe (2) | Black Sea / Danube |
| **208** | Vatican City State | Europe (2) | Holy See |
| **209**, **210**, **212** | Cyprus (Republic of) | Europe (2) | Major European open registry |
| **211** | Germany (Federal Republic of) | Europe (2) | Primary German register |
| **213** | Georgia | Europe (2) | Black Sea ports |
| **214** | Moldova (Republic of) | Europe (2) | Giurgiulești port registry |
| **215** | Malta | Europe (2) | Second allocation (see also 229, 248, 249, 256) |
| **216** | Armenia (Republic of) | Europe (2) | |
| **218** | Germany (Federal Republic of) | Europe (2) | Second allocation |
| **219**, **220** | Denmark | Europe (2) | Includes Danish International Register (DIS) |
| **224**, **225** | Spain | Europe (2) | Includes Canary Islands Special Register |
| **226**, **227**, **228** | France | Europe (2) | Includes RIF register |
| **229** | Malta | Europe (2) | Additional allocation |
| **230** | Finland | Europe (2) | Includes Åland Islands |
| **231** | Faroe Islands (Denmark) | Europe (2) | Faroese register (FAS) |
| **232**, **233**, **234**, **235** | United Kingdom of Great Britain and Northern Ireland | Europe (2) | UK Ship Register (Red Ensign Group) |
| **236** | Gibraltar (United Kingdom) | Europe (2) | British Overseas Territory |
| **237** | Greece | Europe (2) | Major global merchant fleet |
| **238** | Croatia (Republic of) | Europe (2) | Adriatic ports |
| **239**, **240**, **241** | Greece | Europe (2) | Additional allocations |
| **242** | Morocco | Europe (2) | Regional allocation under ITU RR |
| **243** | Hungary | Europe (2) | Inland waterways |
| **244**, **245**, **246** | Netherlands (Kingdom of the) | Europe (2) | European territory |
| **247** | Italy | Europe (2) | Primary Italian register |
| **248**, **249** | Malta | Europe (2) | Additional allocations |
| **250** | Ireland | Europe (2) | Irish Maritime Administration |
| **251** | Iceland | Europe (2) | |
| **252** | Liechtenstein (Principality of) | Europe (2) | Landlocked state |
| **253** | Luxembourg | Europe (2) | European maritime register |
| **254** | Monaco (Principality of) | Europe (2) | Yacht register |
| **255** | Madeira (Portugal) | Europe (2) | International Shipping Register of Madeira (MAR) |
| **256** | Malta | Europe (2) | Primary Maltese open registry allocation |
| **257**, **258**, **259** | Norway | Europe (2) | Norwegian Ordinary (NOR) and International (NIS) |
| **261** | Poland (Republic of) | Europe (2) | Baltic register |
| **262** | Montenegro | Europe (2) | Adriatic Sea |
| **263** | Portugal | Europe (2) | Mainland register |
| **264** | Romania | Europe (2) | Black Sea / Danube |
| **265**, **266** | Sweden | Europe (2) | Swedish Transport Agency |
| **267** | Slovak Republic | Europe (2) | Inland register |
| **268** | San Marino (Republic of) | Europe (2) | Maritime navigation register |
| **269** | Switzerland (Confederation of) | Europe (2) | Swiss Maritime Navigation Office |
| **270** | Czech Republic | Europe (2) | Inland register |
| **271** | Turkey | Europe (2) | Turkish International Ship Registry |
| **272** | Ukraine | Europe (2) | Black Sea / Sea of Azov |
| **273** | Russian Federation | Europe (2) | European ports / Baltic / Black Sea |
| **274** | North Macedonia (Republic of) | Europe (2) | Inland lakes |
| **275** | Latvia (Republic of) | Europe (2) | Maritime Administration of Latvia |
| **276** | Estonia (Republic of) | Europe (2) | Estonian Transport Administration |
| **277** | Lithuania (Republic of) | Europe (2) | Klaipėda port |
| **278** | Slovenia (Republic of) | Europe (2) | Port of Koper |
| **279** | Serbia (Republic of) | Europe (2) | Danube inland navigation |
| **301** | Anguilla (United Kingdom) | North/Central America (3) | British Overseas Territory |
| **303** | United States of America (Alaska) | North/Central America (3) | Dedicated regional allocation |
| **304**, **305** | Antigua and Barbuda | North/Central America (3) | International ship register |
| **306** | Curaçao (Kingdom of the Netherlands) | North/Central America (3) | Caribbean Netherlands |
| **307** | Aruba (Kingdom of the Netherlands) | North/Central America (3) | Autonomous country within Kingdom |
| **308**, **309** | Bahamas (Commonwealth of the) | North/Central America (3) | Major global open registry |
| **310** | Bermuda (United Kingdom) | North/Central America (3) | Red Ensign Group |
| **311** | Bahamas (Commonwealth of the) | North/Central America (3) | Additional allocation |
| **312** | Belize | North/Central America (3) | IMMARBE open registry |
| **314** | Barbados | North/Central America (3) | Ships' Registry |
| **316** | Canada | North/Central America (3) | Transport Canada / CCG |
| **319** | Cayman Islands (United Kingdom) | North/Central America (3) | Red Ensign Group yacht/commercial |
| **321** | Costa Rica | North/Central America (3) | |
| **323** | Cuba | North/Central America (3) | |
| **325** | Dominica (Commonwealth of) | North/Central America (3) | Maritime registry |
| **327** | Dominican Republic | North/Central America (3) | |
| **329** | Guadeloupe (France) | North/Central America (3) | French Overseas Department |
| **330** | Grenada | North/Central America (3) | |
| **331** | Greenland (Denmark) | North/Central America (3) | Autonomous territory |
| **332** | Guatemala (Republic of) | North/Central America (3) | |
| **334** | Honduras (Republic of) | North/Central America (3) | Merchant marine directorate |
| **336** | Haiti (Republic of) | North/Central America (3) | |
| **338** | United States of America | North/Central America (3) | Primary coastal allocation |
| **339** | Jamaica | North/Central America (3) | Maritime Authority of Jamaica |
| **341** | Saint Kitts and Nevis (Federation of) | North/Central America (3) | International ship registry |
| **343** | Saint Lucia | North/Central America (3) | |
| **345** | Mexico | North/Central America (3) | SEMAR / SCT |
| **347** | Martinique (France) | North/Central America (3) | French Overseas Department |
| **348** | Montserrat (United Kingdom) | North/Central America (3) | British Overseas Territory |
| **350** | Nicaragua | North/Central America (3) | |
| **351**–**357** | Panama (Republic of) | North/Central America (3) | Largest open ship registry worldwide |
| **358** | Puerto Rico (United States) | North/Central America (3) | US territory |
| **359** | El Salvador (Republic of) | North/Central America (3) | |
| **361** | Saint Pierre and Miquelon (France) | North/Central America (3) | French Overseas Collectivity |
| **362** | Trinidad and Tobago | North/Central America (3) | |
| **364** | Turks and Caicos Islands (UK) | North/Central America (3) | British Overseas Territory |
| **366**, **367**, **368**, **369** | United States of America | North/Central America (3) | Commercial, government, and USCG |
| **370**, **371**, **372**, **373**, **374** | Panama (Republic of) | North/Central America (3) | Secondary block allocations |
| **375**, **376**, **377** | Saint Vincent and the Grenadines | North/Central America (3) | International open registry |
| **378** | British Virgin Islands (United Kingdom) | North/Central America (3) | Red Ensign Group |
| **379** | United States Virgin Islands (USA) | North/Central America (3) | US territory |
| **401** | Afghanistan | Asia/Middle East (4) | Landlocked state |
| **403** | Saudi Arabia (Kingdom of) | Asia/Middle East (4) | Red Sea / Persian Gulf |
| **405** | Bangladesh (People's Republic of) | Asia/Middle East (4) | Bay of Bengal ports |
| **408** | Bahrain (Kingdom of) | Asia/Middle East (4) | Arabian Gulf |
| **412**, **413**, **414** | China (People's Republic of) | Asia/Middle East (4) | China Maritime Safety Administration |
| **416** | Taiwan (Province of China) | Asia/Middle East (4) | Maritime ports |
| **417** | Sri Lanka (Democratic Socialist Rep.) | Asia/Middle East (4) | Colombo port hub |
| **419** | India (Republic of) | Asia/Middle East (4) | Directorate General of Shipping |
| **422** | Iran (Islamic Republic of) | Asia/Middle East (4) | Ports and Maritime Organization |
| **423** | Azerbaijan (Republic of) | Asia/Middle East (4) | Caspian Sea fleet |
| **424** | Iraq (Republic of) | Asia/Middle East (4) | Persian Gulf / Basra |
| **425** | Israel (State of) | Asia/Middle East (4) | Mediterranean / Red Sea |
| **428** | Israel (State of) | Asia/Middle East (4) | Additional allocation |
| **431**, **432** | Japan | Asia/Middle East (4) | Japan Coast Guard / MLIT |
| **434** | Turkmenistan | Asia/Middle East (4) | Caspian Sea |
| **436** | Kazakhstan (Republic of) | Asia/Middle East (4) | Caspian Sea ports |
| **437** | Uzbekistan (Republic of) | Asia/Middle East (4) | Landlocked state |
| **438** | Jordan (Hashemite Kingdom of) | Asia/Middle East (4) | Port of Aqaba |
| **440**, **441** | Korea (Republic of) | Asia/Middle East (4) | Ministry of Oceans and Fisheries |
| **443** | State of Palestine | Asia/Middle East (4) | Recognized under ITU RR |
| **445** | Democratic People's Rep. of Korea | Asia/Middle East (4) | North Korea |
| **447** | Kuwait (State of) | Asia/Middle East (4) | Arabian Gulf |
| **450** | Lebanon | Asia/Middle East (4) | Eastern Mediterranean |
| **451** | Kyrgyzstan (Republic of) | Asia/Middle East (4) | Landlocked state |
| **453** | Macao (Special Admin. Region of China) | Asia/Middle East (4) | Marine and Water Bureau |
| **455** | Maldives (Republic of) | Asia/Middle East (4) | Indian Ocean archipelago |
| **457** | Mongolia | Asia/Middle East (4) | International ship register |
| **459** | Nepal (Federal Democratic Rep. of) | Asia/Middle East (4) | Landlocked state |
| **461** | Oman (Sultanate of) | Asia/Middle East (4) | Arabian Sea / Gulf of Oman |
| **463** | Pakistan (Islamic Republic of) | Asia/Middle East (4) | Karachi / Gwadar |
| **466** | Qatar (State of) | Asia/Middle East (4) | LNG carrier fleet |
| **468** | Syrian Arab Republic | Asia/Middle East (4) | Eastern Mediterranean |
| **470** | United Arab Emirates | Asia/Middle East (4) | Dubai / Fujairah hub |
| **471** | United Arab Emirates | Asia/Middle East (4) | Additional allocation |
| **472** | Tajikistan (Republic of) | Asia/Middle East (4) | Landlocked state |
| **473**, **475** | Yemen (Republic of) | Asia/Middle East (4) | Red Sea / Gulf of Aden |
| **477** | Hong Kong (SAR of China) | Asia/Middle East (4) | Hong Kong Shipping Register |
| **501** | Adelie Land (France) | Oceania/SE Asia (5) | French Southern and Antarctic Lands |
| **503** | Australia | Oceania/SE Asia (5) | Australian Maritime Safety Authority |
| **506** | Myanmar (Union of) | Oceania/SE Asia (5) | Andaman Sea / Bay of Bengal |
| **508** | Brunei Darussalam | Oceania/SE Asia (5) | Borneo |
| **510** | Micronesia (Federated States of) | Oceania/SE Asia (5) | Pacific Islands |
| **511** | Palau (Republic of) | Oceania/SE Asia (5) | International ship registry |
| **512** | New Zealand | Oceania/SE Asia (5) | Maritime New Zealand |
| **514**, **515** | Cambodia (Kingdom of) | Oceania/SE Asia (5) | Gulf of Thailand |
| **516** | Christmas Island (Indian Ocean) | Oceania/SE Asia (5) | Australian external territory |
| **518** | Cook Islands | Oceania/SE Asia (5) | Maritime Cook Islands registry |
| **520** | Fiji (Republic of) | Oceania/SE Asia (5) | South Pacific hub |
| **523** | Cocos (Keeling) Islands | Oceania/SE Asia (5) | Australian territory |
| **525** | Indonesia (Republic of) | Oceania/SE Asia (5) | Major archipelagic state |
| **529** | Kiribati (Republic of) | Oceania/SE Asia (5) | Kiribati Ship Registry |
| **531** | Lao People's Democratic Republic | Oceania/SE Asia (5) | Mekong river navigation |
| **533** | Malaysia | Oceania/SE Asia (5) | Port Klang / Malacca Strait |
| **536** | Northern Mariana Islands (USA) | Oceania/SE Asia (5) | US Commonwealth territory |
| **538** | Marshall Islands (Republic of the) | Oceania/SE Asia (5) | Top global commercial ship registry |
| **540** | New Caledonia (France) | Oceania/SE Asia (5) | French Pacific territory |
| **542** | Niue | Oceania/SE Asia (5) | Open ship registry |
| **544** | Nauru (Republic of) | Oceania/SE Asia (5) | Central Pacific |
| **546** | French Polynesia | Oceania/SE Asia (5) | French territory |
| **548** | Philippines (Republic of the) | Oceania/SE Asia (5) | MARINA / Coast Guard |
| **553** | Papua New Guinea | Oceania/SE Asia (5) | Coral Sea / Bismarck Sea |
| **555** | Pitcairn Island (United Kingdom) | Oceania/SE Asia (5) | British Overseas Territory |
| **557** | Solomon Islands | Oceania/SE Asia (5) | Western Pacific |
| **559** | American Samoa (USA) | Oceania/SE Asia (5) | US unincorporated territory |
| **561** | Samoa (Independent State of) | Oceania/SE Asia (5) | South Pacific |
| **563**, **564**, **565**, **566** | Singapore (Republic of) | Oceania/SE Asia (5) | Major global shipping hub / MPA |
| **567** | Thailand | Oceania/SE Asia (5) | Marine Department |
| **570** | Tonga (Kingdom of) | Oceania/SE Asia (5) | South Pacific |
| **572** | Tuvalu | Oceania/SE Asia (5) | Tuvalu Ship Registry |
| **574** | Viet Nam (Socialist Republic of) | Oceania/SE Asia (5) | East Sea / coastal fleet |
| **576**, **577** | Vanuatu (Republic of) | Oceania/SE Asia (5) | Vanuatu Maritime Services |
| **578** | Wallis and Futuna Islands (France) | Oceania/SE Asia (5) | French Pacific territory |
| **601** | Egypt (Arab Republic of) | Africa (6) | Suez Canal Authority |
| **603** | Algeria (People's Democratic Rep.) | Africa (6) | Mediterranean ports |
| **605** | Tunisia | Africa (6) | North Africa |
| **607** | Libya (State of) | Africa (6) | Mediterranean |
| **608** | Guinea-Bissau (Republic of) | Africa (6) | West Africa |
| **609** | Madagascar (Republic of) | Africa (6) | Indian Ocean |
| **610** | Equatorial Guinea (Republic of) | Africa (6) | Gulf of Guinea |
| **611** | Congo (Democratic Republic of the) | Africa (6) | Congo river / Atlantic |
| **612** | Central African Republic | Africa (6) | Landlocked state |
| **613** | Cameroon (Republic of) | Africa (6) | Gulf of Guinea |
| **615** | Congo (Republic of the) | Africa (6) | Pointe-Noire port |
| **616** | Comoros (Union of the) | Africa (6) | Comoros maritime registry |
| **617** | Cabo Verde (Republic of) | Africa (6) | Atlantic archipelago |
| **618** | Antarctica | Africa (6) | Assigned under ITU RR |
| **619** | Côte d'Ivoire (Republic of) | Africa (6) | Abidjan port |
| **620** | Comoros (Union of the) | Africa (6) | Additional allocation |
| **621** | Djibouti (Republic of) | Africa (6) | Bab-el-Mandeb strait |
| **622** | Egypt (Arab Republic of) | Africa (6) | Additional allocation |
| **624** | Ethiopia (Federal Democratic Rep.) | Africa (6) | Landlocked; red sea trade |
| **625** | Eritrea | Africa (6) | Red Sea coast |
| **626** | Gabon (Gabonese Republic) | Africa (6) | Gulf of Guinea |
| **627** | Ghana | Africa (6) | West Africa |
| **629** | Gambia (Republic of the) | Africa (6) | River Gambia |
| **630** | Guinea-Bissau (Republic of) | Africa (6) | Additional allocation |
| **631** | Equatorial Guinea (Republic of) | Africa (6) | Additional allocation |
| **632** | Guinea (Republic of) | Africa (6) | West Africa |
| **633** | Burkina Faso | Africa (6) | Landlocked state |
| **634** | Kenya (Republic of) | Africa (6) | Mombasa port |
| **635** | Kerguelen Islands (France) | Africa (6) | French international register (TAAF) |
| **636**, **637** | Liberia (Republic of) | Africa (6) | Top global commercial ship registry |
| **638** | South Sudan (Republic of) | Africa (6) | Landlocked state |
| **642** | Mauritania (Islamic Republic of) | Africa (6) | Atlantic fisheries |
| **644** | Mali (Republic of) | Africa (6) | Landlocked state |
| **645** | Mauritius (Republic of) | Africa (6) | Indian Ocean hub |
| **647** | Mozambique (Republic of) | Africa (6) | East Africa |
| **649** | Niger (Republic of the) | Africa (6) | Landlocked state |
| **650** | Nigeria (Federal Republic of) | Africa (6) | NIMASA maritime authority |
| **654** | Saint Helena (United Kingdom) | Africa (6) | South Atlantic territory |
| **655** | Sao Tome and Principe | Africa (6) | Gulf of Guinea |
| **656** | Seychelles (Republic of) | Africa (6) | Indian Ocean open register |
| **657** | Senegal (Republic of) | Africa (6) | Dakar port |
| **659** | Sierra Leone (Republic of) | Africa (6) | International ship registry |
| **660** | Somalia (Federal Republic of) | Africa (6) | Horn of Africa |
| **661** | Eswatini (Kingdom of) | Africa (6) | Landlocked state |
| **662** | Sudan (Republic of the) | Africa (6) | Port Sudan |
| **663** | Senegal (Republic of) | Africa (6) | Additional allocation |
| **664** | Tanzania (United Republic of) | Africa (6) | Includes Zanzibar register |
| **665** | Chad (Republic of) | Africa (6) | Landlocked state |
| **666** | Togo (Togolese Republic) | Africa (6) | Port of Lomé |
| **667** | Zambia (Republic of) | Africa (6) | Landlocked state |
| **668** | Uganda (Republic of) | Africa (6) | Lake Victoria navigation |
| **669** | Zimbabwe (Republic of) | Africa (6) | Landlocked state |
| **670** | Chad (Republic of) | Africa (6) | Additional allocation |
| **671** | Malawi | Africa (6) | Lake Malawi navigation |
| **672** | Rwanda (Republic of) | Africa (6) | Lake Kivu |
| **674** | South Africa (Republic of) | Africa (6) | SAMSA maritime authority |
| **675** | Seychelles (Republic of) | Africa (6) | Additional allocation |
| **676** | Congo (Democratic Republic of the) | Africa (6) | Additional allocation |
| **677** | Tanzania (United Republic of) | Africa (6) | Additional allocation |
| **678** | Sao Tome and Principe | Africa (6) | Additional allocation |
| **679** | South Africa (Republic of) | Africa (6) | Cape route surveillance |
| **701** | Argentine Republic | South America (7) | Prefectura Naval Argentina |
| **710** | Brazil (Federative Republic of) | South America (7) | Marinha do Brasil |
| **720** | Bolivia (Plurinational State of) | South America (7) | Inland / international register |
| **725** | Chile | South America (7) | DIRECTEMAR maritime authority |
| **730** | Colombia (Republic of) | South America (7) | DIMAR maritime authority |
| **735** | Ecuador | South America (7) | Includes Galápagos surveillance |
| **740** | Falkland Islands (Malvinas) (UK) | South America (7) | British Overseas Territory |
| **745** | Guiana (French Department of) | South America (7) | French Overseas Department |
| **750** | Guyana | South America (7) | Atlantic coast |
| **755** | Paraguay (Republic of) | South America (7) | Inland Paraná-Paraguay waterway |
| **760** | Peru | South America (7) | DICAPI maritime authority |
| **765** | Suriname (Republic of) | South America (7) | Atlantic ports |
| **770** | Uruguay (Eastern Republic of) | South America (7) | Río de la Plata |
| **775** | Venezuela (Bolivarian Republic of) | South America (7) | INEA maritime institute |

---

## D.2 MMSI formatting and identity patterns

The 30-bit User ID field in AIS position reports accommodates nine decimal digits ($000000000$ to $999999999$). Under Recommendation ITU-R M.585-10, this numerical space is partitioned into structural prefixes to identify vessel categories, administrative groups, coastal stations, search and rescue assets, navigational aids, and autonomous locating devices.

### Table D.2: MMSI and Maritime Identity Structural Formats (ITU-R M.585-10)

| Station Category | Format Pattern | Capacity per MID | Governing Standard Clause | Operational Meaning and Constraints |
|:---|:---|:---:|:---|:---|
| **Individual ship station** | $\text{MID} X_4 X_5 X_6 X_7 X_8 X_9$ | 1,000,000 | ITU-R M.585-10, Annex 1 §1 | Standard commercial and recreational vessels. $2 \le \text{MID}[0] \le 7$. $X_i \in [0, 9]$. |
| **Group ship station** | $0 \text{ MID } X_5 X_6 X_7 X_8 X_9$ | 100,000 | ITU-R M.585-10, Annex 1 §2 | Multi-ship fleet addressing (company fleets, fishing flotillas, naval formations). |
| **Coast station / base station** | $0 0 \text{ MID } X_6 X_7 X_8 X_9$ | 10,000 | ITU-R M.585-10, Annex 1 §1 | Terrestrial coastal stations, VTS centers, AIS base stations. Optional $X_6$: $1 = \text{coast}$, $2 = \text{port}$, $3 = \text{pilot}$, $4 = \text{repeater}$, $5 = \text{base}$. |
| **All Coast Stations (universal)** | $0 0 9 9 9 0 0 0 0$ | Global (1) | ITU-R M.585-10, Annex 1 §1 | Universal broadcast address to all listening coast stations (VHF only). |
| **SAR aircraft (fixed-wing/helo)** | $1 1 1 \text{ MID } X_7 X_8 X_9$ | 1,000 | ITU-R M.585-10, Annex 1 §3 | Search and rescue aircraft broadcasting Message 9. Optional $X_7$: $1 = \text{fixed-wing}$, $5 = \text{helicopter}$. |
| **SAR aircraft group** | $1 1 1 \text{ MID } 0 0 0$ | 1 per MID | ITU-R M.585-10, Annex 1 §3 | Broadcast addressing all SAR aircraft belonging to an administration. |
| **Handheld DSC VHF with GNSS** | $8 \text{ MID } X_5 X_6 X_7 X_8 X_9$ | 100,000 | ITU-R M.585-10, Annex 2 §1 | Portable maritime handheld transceivers. Must be accessible to Rescue Coordination Centers 24/7. |
| **Craft associated with parent ship** | $9 8 \text{ MID } X_6 X_7 X_8 X_9$ | 10,000 | ITU-R M.585-10, Annex 1 §5 | Tenders, lifeboats, daughter craft. Digits $X_6..X_9$ typically link to parent ship MMSI. Includes Class 1/2 EPIRBs. |
| **Aid to Navigation (AIS AtoN)** | $9 9 \text{ MID } X_6 X_7 X_8 X_9$ | 10,000 | ITU-R M.585-10, Annex 1 §4 | Navigational marks broadcasting Message 21/28. $X_6$: $1 = \text{physical/synthetic}$, $6 = \text{virtual}$, $8 = \text{mobile AtoN}$. |
| **AIS-SART (Search and Rescue)** | $9 7 0 X_5 X_6 Y_1 Y_2 Y_3 Y_4$ | 10,000 per CIRM code | ITU-R M.585-10, Annex 2 §2 | Survival craft locating transponder (IEC 61097-14). $X_5 X_6$: CIRM manufacturer ID ($01..99$). $Y_i$: serial number. |
| **MOB-AIS (Man Overboard)** | $9 7 2 X_5 X_6 Y_1 Y_2 Y_3 Y_4$ | 10,000 per CIRM code | ITU-R M.585-10, Annex 2 §2 | Personal survivor locating beacon (ETSI EN 303 098). $X_5 X_6$: CIRM manufacturer ID. $Y_i$: serial number. |
| **EPIRB-AIS (Emergency Beacon)** | $9 7 4 X_5 X_6 Y_1 Y_2 Y_3 Y_4$ | 10,000 per CIRM code | ITU-R M.585-10, Annex 2 §2 | 406 MHz EPIRB fitted with AIS transmitter (IEC 61097-2). $X_5 X_6$: CIRM manufacturer code. $Y_i$: serial number. |
| **AMRD Group B (Non-navigational)**| $9 7 9 Y_1 Y_2 Y_3 Y_4 Y_5 Y_6$ | 1,000,000 | ITU-R M.585-10, Annex 2 §5 | Autonomous maritime radio devices (fishing buoys, oceanographic drifters) on Ch 2006 per ITU-R M.2135. |
| **12-character extended identity** | $9 7 T X_5 X_6 M P_1 P_2 Y_1 Y_2 Y_3 Y_4$ | $2.6 \times 10^7$ per type | ITU-R M.585-10, Annex 2 §3 | Anti-exhaustion format for $97T$. $M \in [A..Z]$, $P_1 P_2 \in [01..99]$. Carried in linked Message 14. |

---

## D.3 Navigational status codes

The 4-bit **Navigational Status** field occupies bits 38–41 in Class A position reports (Messages 1, 2, and 3) and bits 70–73 in long-range satellite reports (Message 27). The enumeration is governed by Recommendation ITU-R M.1371-6 Table 46:

### Table D.3: Navigational Status Codes (ITU-R M.1371-6 Table 46)

| Code (Dec) | 4-bit Binary | Standard Meaning (ITU-R M.1371-6) | Operational Definition and Mariner Usage | COLREGS Rule Reference |
|:---:|:---:|:---|:---|:---:|
| **0** | `0000` | Under way using engine | Vessel is moving under mechanical propulsion or drifting with engine available | Rule 3(i) |
| **1** | `0001` | At anchor | Vessel is riding at anchor within designated anchor watch circle | Rule 35(f) |
| **2** | `0010` | Not under command (NUC) | Through exceptional circumstance, vessel cannot manoeuvre as required | Rule 3(f), Rule 27(a) |
| **3** | `0011` | Restricted manoeuvrability (RAM) | From nature of her work, vessel's ability to manoeuvre is restricted | Rule 3(g), Rule 27(b) |
| **4** | `0100` | Constrained by her draught | Power-driven vessel whose draught severely restricts available water depth | Rule 3(h), Rule 28 |
| **5** | `0101` | Moored | Securely made fast to shore structure, wharf, pier, buoy, or dolphins | General practice |
| **6** | `0110` | Aground | Vessel hull is touching or lodged upon the seabed or shoal | Rule 35(g) |
| **7** | `0111` | Engaged in fishing | Vessel fishing with nets, lines, or trawls that restrict manoeuvrability | Rule 3(d), Rule 26 |
| **8** | `1000` | Under way sailing | Vessel propelled exclusively by sail alone; auxiliary engine off | Rule 3(c), Rule 25 |
| **9** | `1001` | Reserved for future amendment (HSC) | Reserved for High-Speed Craft dangerous goods / hazardous cargo amendments | Regional / IMO |
| **10** | `1010` | Reserved for future amendment (WIG) | Reserved for Wing-in-Ground craft flight mode amendments | Regional / IMO |
| **11** | `1011` | Power-driven vessel towing astern | Regional inland navigation status (Europe / CESNI); tow astern | European Inland / CESNI |
| **12** | `1012` | Power-driven vessel pushing / alongside | Regional inland navigation status (Europe / CESNI); pushing or alongside | European Inland / CESNI |
| **13** | `1101` | Reserved for future use | Unassigned reserved code | N/A |
| **14** | `1110` | AIS-SART / MOB / EPIRB active | Active emergency locating beacon (replaces undefined default during distress) | GMDSS emergency |
| **15** | `1111` | Undefined (default) | Default value when unconfigured; also set during transponder factory testing | N/A |

---

## D.4 Type of ship and cargo codes

The 8-bit **Type of Ship and Cargo** field is broadcast in Class A Static Data (Message 5, bits 232–239) and Class B Static Data (Message 24 Part B, bits 8–15). Recommendation ITU-R M.1371-6 Table 51 expanded this enumeration to populate previously reserved codes (1–19, 38, 39, 45, 46, 65–67, 75–78, 85, 86). Both legacy interpretations (ITU-R M.1371-5 / gpsd) and modern ITU-R M.1371-6 allocations are documented below.

The second digit (units digit, values 1–4) across commercial cargo, tanker, passenger, and other vessel classes encodes the carriage of dangerous goods under IMO regulations:
- **1**: Carrying Dangerous Goods (**DG**), Harmful Substances (**HS**), or Marine Pollutants (**MP**), IMO hazard category **X** (formerly Category A).
- **2**: Carrying DG, HS, or MP, IMO hazard category **Y** (formerly Category B).
- **3**: Carrying DG, HS, or MP, IMO hazard category **Z** (formerly Category C).
- **4**: Carrying DG, HS, or MP, IMO hazard category **OS** (Other Substances; formerly Category D).

### Table D.4: Type of Ship and Cargo Codes (ITU-R M.1371-6 Table 51 vs Legacy)

| Code (Dec) | Standard Designation (ITU-R M.1371-6 Table 51) | Legacy Meaning (ITU-R M.1371-5 / gpsd v1.58) | Operational Notes / Vessel Subtype |
|:---:|:---|:---|:---|
| **0** | Not available (default) | Not available (default) | Unprogrammed or unknown vessel classification |
| **1** | Research vessel | Reserved for future use | Oceanographic, seismic, or hydrographic survey vessel |
| **2** | Training ship | Reserved for future use | Maritime academy or institutional training ship |
| **3** | Government-owned vessel | Reserved for future use | Non-military state service (customs, fishery research) |
| **4** | Icebreaker | Reserved for future use | Dedicated polar/subpolar icebreaking vessel |
| **5** | Buoy tender | Reserved for future use | Aids to navigation tender or service craft |
| **6** | Cable layer | Reserved for future use | Submarine telecommunications / power cable installation |
| **7** | Pipe layer | Reserved for future use | Subsea oil/gas pipeline construction vessel |
| **8** | Reserved for future use | Reserved for future use | Reserved |
| **9** | Special purpose vessel (n.a.i.) | Reserved for future use | Special purpose ship, no additional info |
| **10** | Reserved for future use | Reserved for future use | Reserved |
| **11** | FPSO / FSO | Reserved for future use | Floating Production Storage and Offloading unit |
| **12** | Fish factory vessel | Reserved for future use | Pelagic processing ship / mother ship |
| **13** | Fish-farm support vessel | Reserved for future use | Aquaculture maintenance and harvest support |
| **14** | Offshore supply vessel (OSV) | Reserved for future use | Platform supply vessel (PSV) or anchor handler (AHTS) |
| **15–16**| Reserved for future use | Reserved for future use | Reserved |
| **17** | Construction vessel | Reserved for future use | Offshore wind / marine civil engineering crane vessel |
| **18** | Crew boat | Reserved for future use | High-speed offshore personnel transport |
| **19** | Support vessel (n.a.i.) | Reserved for future use | General offshore support craft |
| **20** | Wing-in-Ground (WIG) craft | Wing-in-Ground (WIG) craft | All craft of this type |
| **21** | WIG, Category X (hazardous) | WIG, Category A | Dangerous goods category X |
| **22** | WIG, Category Y (hazardous) | WIG, Category B | Dangerous goods category Y |
| **23** | WIG, Category Z (hazardous) | WIG, Category C | Dangerous goods category Z |
| **24** | WIG, Category OS | WIG, Category D | Dangerous goods category OS |
| **25–28**| WIG, Reserved | WIG, Reserved | Reserved |
| **29** | WIG, No additional info | WIG, No additional info | Operating without cargo specification |
| **30** | Fishing | Fishing | Commercial fishing vessel (trawler, seiner, liner) |
| **31** | Towing | Towing | Standard tug engaged in towing |
| **32** | Towing, length >200 m or breadth >25 m | Towing, length >200 m or breadth >25 m | Severe navigation restriction due to tow dimensions |
| **33** | Dredging or underwater operations | Dredging or underwater operations | Suction dredger, cutterhead, subsea trenching |
| **34** | Diving operations | Diving operations | Commercial or naval dive support craft |
| **35** | Military ops / naval auxiliary | Military operations | Naval surface combatant or auxiliary ship |
| **36** | Sailing vessel | Sailing vessel | Commercial or recreational sailing craft |
| **37** | Pleasure craft | Pleasure craft | Private yacht or recreational motorboat |
| **38** | Trawler | Reserved for future use | Specifically designated commercial fishing trawler |
| **39** | Patrol vessel | Reserved for future use | Coast guard, fisheries protection, or border patrol |
| **40** | High-Speed Craft (HSC) | High-Speed Craft (HSC) | General fast craft complying with IMO HSC Code |
| **41** | HSC, Category X | HSC, Category A | Fast craft carrying category X cargo |
| **42** | HSC, Category Y | HSC, Category B | Fast craft carrying category Y cargo |
| **43** | HSC, Category Z | HSC, Category C | Fast craft carrying category Z cargo |
| **44** | HSC, Category OS | HSC, Category D | Fast craft carrying category OS cargo |
| **45** | HSC passenger vessel | Reserved for future use | Fast passenger catamaran / monohull ferry |
| **46** | HSC ro-ro passenger | Reserved for future use | Fast passenger and vehicle ro-ro ferry |
| **47–48**| HSC, Reserved | HSC, Reserved | Reserved |
| **49** | HSC, No additional info | HSC, No additional info | Fast craft, unconfigured cargo details |
| **50** | Pilot vessel | Pilot vessel | Harbor or deep-sea pilot boarding cutter |
| **51** | Search and Rescue (SAR) vessel | Search and Rescue vessel | Lifeboat, SAR cutter, emergency salvage tug |
| **52** | Tug | Tug | Harbor assist or coastal tug |
| **53** | Port tender | Port tender | Harbor launch, workboat, or mooring tender |
| **54** | Anti-pollution equipment | Anti-pollution equipment | Oil spill recovery, chemical skimmer, fireboat |
| **55** | Law enforcement | Law enforcement | Marine police, harbor patrol, customs launch |
| **56–57**| Spare - local vessel | Spare - local vessel | Reserved for local port authority assignment |
| **58** | Medical transport | Medical transport | Hospital ship or ambulance launch (Geneva Conv.) |
| **59** | Noncombatant ship under Geneva Conv.| Noncombatant ship under Geneva Conv.| Neutral ship participating in humanitarian relief |
| **60** | Passenger ship | Passenger ship | General passenger transport |
| **61** | Passenger ship, Category X | Passenger ship, Category A | Carrying category X hazardous substances |
| **62** | Passenger ship, Category Y | Passenger ship, Category B | Carrying category Y hazardous substances |
| **63** | Passenger ship, Category Z | Passenger ship, Category C | Carrying category Z hazardous substances |
| **64** | Passenger ship, Category OS | Passenger ship, Category D | Carrying category OS substances |
| **65** | Cruise ship | Reserved for future use | Dedicated passenger cruise liner |
| **66** | Passenger ferry | Reserved for future use | Conventional passenger / Ro-Pax ferry |
| **67** | Excursion vessel | Reserved for future use | Coastal sightseeing / day-passenger boat |
| **68** | Passenger, Reserved | Passenger, Reserved | Reserved |
| **69** | Passenger, No additional info | Passenger, No additional info | Passenger vessel, unconfigured cargo details |
| **70** | Cargo ship | Cargo ship | General dry cargo or breakbulk freighter |
| **71** | Cargo ship, Category X | Cargo ship, Category A | Dedicated hazardous chemical/cargo carriage |
| **72** | Cargo ship, Category Y | Cargo ship, Category B | Hazardous industrial carriage |
| **73** | Cargo ship, Category Z | Cargo ship, Category C | Harmful cargo carriage |
| **74** | Cargo ship, Category OS | Cargo ship, Category D | Other substances carriage |
| **75** | Bulk carrier | Reserved for future use | Capesize, Panamax, Handymax bulk carrier |
| **76** | Container ship | Reserved for future use | Cellular container ship |
| **77** | Ro-ro cargo vessel | Reserved for future use | Pure Car Truck Carrier (PCTC) / ro-ro freighter |
| **78** | Landing craft | Reserved for future use | Commercial or landing craft utility (LCU) |
| **79** | Cargo, No additional info | Cargo, No additional info | Cargo vessel, general unconfigured status |
| **80** | Tanker | Tanker | Liquid bulk carrier |
| **81** | Tanker, Category X | Tanker, Category A | Chemical tanker carrying category X chemicals |
| **82** | Tanker, Category Y | Tanker, Category B | Chemical tanker carrying category Y chemicals |
| **83** | Tanker, Category Z | Tanker, Category C | Oil / product tanker carrying category Z cargo |
| **84** | Tanker, Category OS | Tanker, Category D | Tanker carrying clean products / OS |
| **85** | Non-hazardous tanker | Reserved for future use | Water tanker, wine/vegetable oil carrier |
| **86** | Integrated / Articulated Tug-Barge | Reserved for future use | ATB or ITB petroleum unit |
| **87–88**| Tanker, Reserved | Tanker, Reserved | Reserved |
| **89** | Tanker, No additional info | Tanker, No additional info | Liquid tanker, unconfigured cargo details |
| **90** | Other type of ship | Other type of ship | Non-standard hull or floating plant |
| **91** | Other, Category X | Other, Category A | Floating plant carrying category X cargo |
| **92** | Other, Category Y | Other, Category B | Floating plant carrying category Y cargo |
| **93** | Other, Category Z | Other, Category C | Floating plant carrying category Z cargo |
| **94** | Other, Category OS | Other, Category D | Floating plant carrying category OS cargo |
| **95–98**| Other, Reserved | Other, Reserved | Reserved |
| **99** | Other, No additional info | Other, No additional info | Unclassified craft, no additional details |
| **100–199**| Regional waterway codes | Regional waterway codes | Reserved for regional inland waterway authorities |
| **200–255**| Reserved for future use | Reserved for future use | International reserved space |

---

## D.5 Electronic Position Fixing Device (EPFD) codes

The 4-bit **Type of EPFD** field indicates the sensor origin of the transmitted navigation coordinates. It appears in Base Station Reports (Message 4, bits 134–137), Class A Static Data (Message 5, bits 270–273), UTC Inquiries (Message 11), Class B Extended Position Reports (Message 19), AtoN Reports (Message 21, bits 268–271), and Class B Static Data (Message 24 Part B, bits 160–163). Governed by Recommendation ITU-R M.1371-6 Table 50:

### Table D.5: EPFD Type Codes (ITU-R M.1371-6 Table 50)

| Code (Dec) | 4-bit Binary | Standard EPFD Sensor Description | Operational and Diagnostic Significance |
|:---:|:---:|:---|:---|
| **0** | `0000` | Undefined (default) | Positioning source unclassified, manual entry, or failed |
| **1** | `0001` | **GPS** | Primary United States Navstar Global Positioning System |
| **2** | `0010` | **GLONASS** | Russian GLObal NAvigation Satellite System |
| **3** | `0011` | **Combined GNSS** | Multi-constellation receiver fix (e.g. GPS + GLONASS / Galileo) |
| **4** | `0100` | **Loran-C** | Terrestrial long-range hyperbolic radionavigation system |
| **5** | `0101` | **Chayka** | Russian terrestrial low-frequency radionavigation system |
| **6** | `0110` | **Integrated navigation system (INS)** | Bridge multi-sensor Kalman filter engine (ECDIS/IBS) |
| **7** | `0111` | **Surveyed** | Centimeter-accurate geodetic survey coordinates (fixed base/AtoN) |
| **8** | `1000` | **Galileo** | European Union civilian satellite constellation |
| **9** | `1001` | **BeiDou (BDS)** | Chinese BeiDou Navigation Satellite System (added in M.1371-6) |
| **10–11** | `1010–1011`| Reserved for future use | Unallocated |
| **12** | `1100` | **Integrated PNT system** | Resilient multi-source Positioning, Navigation and Timing (MSC.401(95)) |
| **13** | `1101` | **Inertial Navigation System (INS)** | Self-contained autonomous gyro-accelerometer inertial platform |
| **14** | `1110` | **Terrestrial radio navigation** | Terrestrial ranging systems (e.g. R-Mode, eLoran) |
| **15** | `1111` | **Internal GNSS** | **Emergency fallback:** transponder internal backup GNSS receiver active |

---

## D.6 Aids to Navigation (AtoN) type codes

The 5-bit **Type of Aids to Navigation** field in AIS Message 21 (bits 38–42) and Message 28 (bits 38–42) categorizes physical, synthetic, and virtual aids in accordance with Recommendation ITU-R M.1371-6 Table 72 and IALA Recommendation R0126 (formerly A-126). Message 28 additionally specifies specialized environmental and hazard types (codes 32–50):

### Table D.6: Aids to Navigation Type Codes (ITU-R M.1371-6 Table 72 & Message 28 Table 85)

| Code (Dec) | 5-bit Binary | Standard AtoN Designation | Physical Structure / Mooring Category | IALA Maritime Buoyage System Meaning |
|:---:|:---:|:---|:---|:---|
| **0** | `00000` | Default, Type of AtoN not specified | Unclassified mark | General navigational aid without classification |
| **1** | `00001` | Reference point | Survey / Geodetic mark | Charted fixed reference location |
| **2** | `00010` | RACON | Radar transponder beacon | Radar-responsive navigational beacon or MAtoN |
| **3** | `00011` | Fixed structure off-shore | Fixed marine installation | Offshore oil/gas platform, wind turbine, weather mast |
| **4** | `00100` | Emergency Wreck Marking Buoy | Floating buoy | Alternating blue/yellow light marking recent hazard |
| **5** | `00101` | Light, without sectors | Fixed structure | Omnidirectional lighthouse or minor light beacon |
| **6** | `00110` | Light, with sectors | Fixed structure | Sector light defining safe transit fairway channels |
| **7** | `00111` | Leading Light Front | Fixed structure | Front range marker for visual transit alignment |
| **8** | `01000` | Leading Light Rear | Fixed structure | Rear range marker for visual transit alignment |
| **9** | `01001` | Beacon, Cardinal N | Fixed beacon | Pass to the north of this mark |
| **10** | `01010` | Beacon, Cardinal E | Fixed beacon | Pass to the east of this mark |
| **11** | `01011` | Beacon, Cardinal S | Fixed beacon | Pass to the south of this mark |
| **12** | `01100` | Beacon, Cardinal W | Fixed beacon | Pass to the west of this mark |
| **13** | `01101` | Beacon, Port hand | Fixed beacon | Lateral port mark (IALA Region A red, Region B green) |
| **14** | `01110` | Beacon, Starboard hand | Fixed beacon | Lateral starboard mark (Region A green, Region B red) |
| **15** | `01111` | Beacon, Preferred Channel port | Fixed beacon | Preferred channel to starboard (Region A/B rules) |
| **16** | `10000` | Beacon, Preferred Channel stbd | Fixed beacon | Preferred channel to port (Region A/B rules) |
| **17** | `10001` | Beacon, Isolated danger | Fixed beacon | Hazard with navigable water completely surrounding |
| **18** | `10010` | Beacon, Safe water | Fixed beacon | Mid-channel, fairway entrance, or land-fall mark |
| **19** | `10011` | Beacon, Special mark | Fixed beacon | Spoil ground, cable area, recreation, or military zone |
| **20** | `10100` | Cardinal Mark N | Floating buoy | Pass to north; black double cone points up |
| **21** | `10101` | Cardinal Mark E | Floating buoy | Pass to east; cones point away from each other |
| **22** | `10110` | Cardinal Mark S | Floating buoy | Pass to south; black double cone points down |
| **23** | `10111` | Cardinal Mark W | Floating buoy | Pass to west; cones point point-to-point |
| **24** | `11000` | Port hand Mark | Floating buoy | Lateral port mark |
| **25** | `11001` | Starboard hand Mark | Floating buoy | Lateral starboard mark |
| **26** | `11010` | Preferred Channel port hand | Floating buoy | Bifurcation mark; preferred fairway to starboard |
| **27** | `11011` | Preferred Channel starboard hand| Floating buoy | Bifurcation mark; preferred fairway to port |
| **28** | `11100` | Isolated danger | Floating buoy | Moored directly on or over underwater hazard |
| **29** | `11101` | Safe water | Floating buoy | Fairway buoy or mid-channel mark (red/white stripes) |
| **30** | `11110` | Special mark | Floating buoy | Yellow buoy marking specialized marine perimeter |
| **31** | `11111` | Light Vessel / LANBY / Rig | Floating structure | Light vessel, large automated navigational buoy, rig |
| **32** | *(Msg 28)* | Ocean Data Acquisition System | Specialized buoy (ODAS) | Oceanographic meteorological sensor buoy |
| **33** | *(Msg 28)* | Water sampling / monitoring | Specialized buoy | Environmental water quality monitoring station |
| **34** | *(Msg 28)* | Research equipment | Research station | Ocean acoustic or subsea research array marker |
| **35** | *(Msg 28)* | Towed cable / pipe marker | Mobile marker | Surface marker indicating submerged towed arrays |
| **36** | *(Msg 28)* | Towed vessel or object | Mobile marker | Navigational marker affixed to unpowered tow |
| **37** | *(Msg 28)* | Flotsam marker (large) | Floating hazard | Drifting container or large navigational obstruction |
| **38** | *(Msg 28)* | Flotsam marker (small) | Floating hazard | Small drifting navigation hazard |
| **39** | *(Msg 28)* | Navigation hazard | General hazard | Unclassified hazard to navigation |
| **40** | *(Msg 28)* | Synthetic target marker | Synthetic projection | Digital marker projecting a radar/sonar target |
| **41** | *(Msg 28)* | Protected species marker | Environmental marker | Whale safety zone, seal colony, or coral reef |
| **42** | *(Msg 28)* | Military operation target marker | Exercise marker | Naval surface exercise target or firing buoy |
| **43** | *(Msg 28)* | Dangerous object | Safety hazard | Unexploded ordnance or floating mine warning |
| **44** | *(Msg 28)* | Pollution spill marker | Environmental marker | Hydrocarbon spill perimeter or dispersant zone |
| **45** | *(Msg 28)* | Search and Rescue datum mark | Emergency SAR datum | Computed search datum buoy deployed by SAR aircraft |
| **46** | *(Msg 28)* | Datum mark | General datum | Hydrographic or oceanographic calculation datum |
| **47** | *(Msg 28)* | Operating underwater | Subsea activity | Submarine operations or commercial diving tether |
| **48** | *(Msg 28)* | Underwater operations marker | Subsea activity | Remotely Operated Vehicle (ROV) or diver station |
| **49** | *(Msg 28)* | Military restricted area | Security zone | Naval exclusion zone or firing perimeter |
| **50** | *(Msg 28)* | Dynamic area | Dynamic fairway | Moving safety fairway or seasonal protection zone |

---

## D.7 Application-Specific Messages (ASM): DAC and FI registry snapshot

Under Recommendation ITU-R M.1371-6 Annex 4, Application-Specific Messages broadcast arbitrary structured telemetry via Messages 6, 8, 25, and 26. Every ASM payload begins with a 16-bit **Application Identifier** (**AI**), consisting of a 10-bit **Designated Area Code** (**DAC**) and a 6-bit **Function Identifier** (**FI**):
- **$\text{DAC} = 0$**: Reserved for laboratory test and developmental applications.
- **$\text{DAC} = 1$–$9$**: International Application Identifiers (**IAI**), maintained and published by the IMO (SN.1/Circ.289).
- **$\text{DAC} = 10$–$999$**: Regional Application Identifiers (**RAI**), derived directly from national Maritime Identification Digits (**MIDs**).
- **$\text{DAC} = 1000$–$1023$**: Reserved for future international expansion.

The official global ASM register is maintained by IALA at `http://www.iala-aism.org/asm` (mirrored at `https://www.e-navigation.nl/asm`). The following snapshot registers the standardized international (DAC 1), European Inland (DAC 200), St. Lawrence Seaway (DAC 316/366), and United States (DAC 366/367) function messages:

### Table D.7: Application Identifier (DAC / FI) Register Snapshot

| DAC | FI | Msg | Application Title | Registrant | Standard / Reference | Status | Permitted As From |
|:---:|:---:|:---:|:---|:---|:---|:---:|:---:|
| **1** | **0** | 6 / 8 | Text telegram (6-bit ASCII) | ITU-R | ITU-R M.1371-6 Table 24 | In force | 01/01/1998 |
| **1** | **1** | 6 | Application acknowledgement | ITU-R | ITU-R M.1371-1 | **Discontinued**| 01/01/1998 |
| **1** | **2** | 6 | Interrogation on specific IFM | ITU-R | ITU-R M.1371-6 Table 24 | In force | 01/01/2001 |
| **1** | **3** | 6 | Capability interrogation | ITU-R | ITU-R M.1371-6 Table 24 | In force | 01/01/2001 |
| **1** | **4** | 6 | Capability reply (64-FI bitmap) | ITU-R | ITU-R M.1371-6 Table 32 | In force | 01/01/2001 |
| **1** | **5** | 6 | Application acknowledgement | ITU-R | ITU-R M.1371-6 Table 33 | In force | 01/01/2001 |
| **1** | **11**| 8 | Meteorological and hydrographic data | IMO | IMO SN/Circ.236 | **Deprecated**  | 01/12/2004 |
| **1** | **12**| 6 | Dangerous cargo indication | IMO | IMO SN/Circ.236 | **Deprecated**  | 01/12/2004 |
| **1** | **13**| 8 | Fairway closed | IMO | IMO SN/Circ.236 | **Deprecated**  | 01/12/2004 |
| **1** | **14**| 6 | Tidal window | IMO | IMO SN/Circ.236 | **Deprecated**  | 01/12/2004 |
| **1** | **15**| 8 | Extended ship static & voyage data | IMO | IMO SN/Circ.236 | **Deprecated**  | 01/12/2004 |
| **1** | **16**| 6 | Number of persons on board | IMO | IMO SN.1/Circ.289 | In force | 01/06/2010 |
| **1** | **17**| 8 | VTS-generated / synthetic targets | IMO | IMO SN.1/Circ.289 | In force | 01/06/2010 |
| **1** | **18**| 6 | Clearance time to enter port | IMO | IMO SN.1/Circ.289 | In force | 01/06/2010 |
| **1** | **19**| 8 | Marine traffic signal | IMO | IMO SN.1/Circ.289 | In force | 01/06/2010 |
| **1** | **20**| 6 | Berthing data | IMO | IMO SN.1/Circ.289 | In force | 01/06/2010 |
| **1** | **21**| 8 | Weather observation report from ship | IMO | IMO SN.1/Circ.289 | In force | 01/06/2010 |
| **1** | **22**| 8 | Area notice broadcast | IMO | IMO SN.1/Circ.289 | In force | 04/03/2011 |
| **1** | **23**| 6 | Area notice addressed | IMO | IMO SN.1/Circ.289 | In force | 04/03/2011 |
| **1** | **24**| 8 | Extended ship static & voyage data | IMO | IMO SN.1/Circ.289 | In force | 01/06/2010 |
| **1** | **25**| 6 | Dangerous cargo indication | IMO | IMO SN.1/Circ.289 | In force | 01/06/2010 |
| **1** | **26**| 8 | Environmental information | IMO | IMO SN.1/Circ.289 | In force | 01/06/2010 |
| **1** | **27**| 8 | Route information broadcast | IMO | IMO SN.1/Circ.289 | In force | 01/06/2010 |
| **1** | **28**| 6 | Route information addressed | IMO | IMO SN.1/Circ.289 | In force | 01/06/2010 |
| **1** | **29**| 8 | Text description broadcast | IMO | IMO SN.1/Circ.289 | In force | 01/06/2010 |
| **1** | **30**| 6 | Text description addressed | IMO | IMO SN.1/Circ.289 | In force | 01/06/2010 |
| **1** | **31**| 8 | Meteorological & hydrographic data | IMO | IMO SN.1/Circ.289 | In force | 01/06/2010 |
| **1** | **32**| 6 | Tidal window | IMO | IMO SN.1/Circ.289 | In force | 01/06/2010 |
| **200**| **1** | 8 | Control message | EU / CCNR | Inland AIS Standard | In force | 15/09/2017 |
| **200**| **10**| 8 | Inland ship static & voyage data | EU / CCNR | Inland AIS Standard | In force | 10/10/2007 |
| **200**| **11**| 8 | Convoy / flotilla configuration | EU / CCNR | Inland AIS Standard | In force | 15/12/2014 |
| **200**| **21**| 6 | Estimated time of arrival (ETA) | EU / CCNR | Inland AIS Standard | In force | 10/10/2007 |
| **200**| **22**| 6 | Requested time of arrival (RTA) | EU / CCNR | Inland AIS Standard | In force | 10/10/2007 |
| **200**| **23**| 8 | EMMA water warning | EU / CCNR | Inland AIS Standard | **Discontinued**| 10/10/2007 |
| **200**| **24**| 8 | Water level | EU / CCNR | Inland AIS Standard | **Deprecated**  | 10/10/2007 |
| **200**| **25**| 8 | Present bridge clearance (v1) | EU / CCNR | Inland AIS Standard | In force | 18/10/2021 |
| **200**| **26**| 8 | Water level (v0) | EU / CCNR | Inland AIS Standard | In force | 18/10/2020 |
| **200**| **40**| 8 | Signal status | EU / CCNR | Inland AIS Standard | **Replaced**    | 10/10/2007 |
| **200**| **41**| 8 | Signal station status | EU / CCNR | Inland AIS Standard | In force | 24/11/2016 |
| **200**| **55**| 6 | Number of persons on board | EU / CCNR | Inland AIS Standard | In force | 10/10/2007 |
| **316**| **1** | 6 | St. Lawrence Seaway Met/Hydro (sub 1–6)| SLSMC / GLPA | Seaway AIS Specification | In force | 09/03/2002 |
| **316**| **2** | 6 | Seaway lock schedule (sub 1–2) | SLSMC / GLPA | Seaway AIS Specification | In force | 09/03/2002 |
| **366**| **1** | 6 | St. Lawrence Seaway Met/Hydro (sub 1–6)| USCG / SLSDC | Seaway AIS Specification | In force | 09/03/2002 |
| **366**| **2** | 6 | Seaway lock schedule (sub 1–2) | USCG / SLSDC | Seaway AIS Specification | In force | 09/03/2002 |
| **366**| **22**| 8 | Area notice (draft specification) | USCG RDC | Draft USCG Spec | **Deprecated**  | 01/01/2008 |
| **367**| **22**| 8 | Geographic area notice (v2) | USCG RDC | USCG AIS ASM Spec | In force | 15/06/2013 |
| **367**| **29**| 8 | Text message (v1) | USCG RDC | USCG AIS ASM Spec | In force | 15/06/2013 |
| **367**| **33**| 8 | Environmental sensor report (v3) | USCG RDC | USCG AIS ASM Spec | In force | 15/06/2013 |
| **367**| **35**| 8 | Water level observation (v2) | USCG RDC | USCG AIS ASM Spec | In force | 15/06/2013 |

---

## D.8 NMEA 0183 and IEC 61162-1 talker IDs and sentence formatters

Shipboard serial interfaces operating at 38,400 baud (IEC 61162-2 / NMEA 0183-HS) encapsulate incoming radio packets into `!AIVDM` sentences and bridge configurations into `$AI...` sentences.

### Table D.8-A: NMEA 0183 / IEC 61162-1 Talker Identifiers

| Talker Mnemonic | Originating AIS Station Description | Standard Reference | Status |
|:---:|:---|:---|:---:|
| `AI` | Mobile AIS station (Class A or Class B shipborne transponder) | NMEA 0183 / IEC 61162-1 | Universal standard |
| `AB` | Shore-based AIS base station | NMEA 4.00+ / IEC 62320-1 | In force |
| `AD` | Dependent AIS base station | NMEA 4.00+ / IEC 62320-1 | In force |
| `AN` | Aid to Navigation AIS station (physical or virtual AtoN) | NMEA 4.00+ / IEC 62320-2 | In force |
| `AR` | AIS receiving station (receive-only coastal installation) | NMEA 4.00+ | In force |
| `AS` | Limited base station (provisional NMEA talker mnemonic) | NMEA 4.00+ | In force |
| `AT` | AIS transmitting station (transmit-only directed service) | NMEA 4.00+ | In force |
| `AX` | AIS repeater station | NMEA 4.00+ | In force |
| `BS` | AIS base station | NMEA 3.01 / Legacy | **Deprecated** (use `AB`) |
| `SA` | Physical shore AIS station (provisional NMEA talker mnemonic) | NMEA 4.00+ | In force |

### Table D.8-B: AIS Presentation Interface Sentence Formatters

| Formatter | Mnemonic Title | Direction | Operational Purpose |
|:---:|:---|:---:|:---|
| `VDM` | VHF Data-link Message | Outbound (Rx) | Delivers radio packets received from *other* stations |
| `VDO` | VHF Data-link Own-vessel message | Outbound (Rx) | Delivers packets broadcast or queued by *own ship's* transponder |
| `ABM` | Addressed Binary Message | Inbound (Tx) | Commands transponder to transmit addressed Message 6/12 |
| `BBM` | Broadcast Binary Message | Inbound (Tx) | Commands transponder to transmit broadcast Message 8/14/26 |
| `ABK` | Addressed Binary Acknowledgement | Outbound (Rx) | Transponder reports completion/timeout of ABM/BBM requests |
| `ACA` | AIS Regional Channel Assignment | Bidirectional | Queries or configures regional operational VHF channels |
| `ACS` | Channel Management Source | Outbound (Rx) | Identifies the originator (base station MMSI) of ACA parameters |
| `AIR` | Interrogation Request | Inbound (Tx) | Commands transponder to poll another vessel via Message 15 |
| `AIQ` | Query Sentence | Inbound (Tx) | Polls transponder internal registers for specific sentence output |
| `LRF` | Long-Range Function | Inbound (Tx) | Directs long-range polling request (satellite/Inmarsat-C) |
| `LRI` | Long-Range Interrogation | Inbound (Tx) | Requests long-range identification, position, and course data |
| `LR1` | Long-Range Reply 1 | Outbound (Rx) | Delivers transponder identification and coordinate replies |
| `LR2` | Long-Range Reply 2 | Outbound (Rx) | Delivers speed, course, and ETA replies |
| `LR3` | Long-Range Reply 3 | Outbound (Rx) | Delivers voyage destination and draught replies |
| `SSD` | Ship Static Data | Inbound (Tx) | Sets vessel name, call sign, dimensions, and antenna offsets |
| `VSD` | Voyage Static Data | Inbound (Tx) | Sets draught, hazardous cargo, destination UN/LOCODE, and ETA |
| `TXT` | Text Transmission | Outbound (Rx) | Emits bridge alerts, antenna VSWR faults, and self-test text |
| `ALR` | Set Alarm State | Outbound (Rx) | Reports Bridge Alert Management (BAM) failure conditions |
| `VER` | Version Sentence | Outbound (Rx) | Reports equipment model, software version, and hardware serial |

### Table D.8-C: NMEA 4.10 / IEC 62320-1 TAG Block Parameters

| Tag Key | Parameter Name | Format Constraints | Operational Significance | Standard |
|:---:|:---|:---|:---|:---:|
| `c` | Timestamp (UNIX epoch) | Numeric integer string | Exact time of radio reception. Seconds ($<10^{11}$) or ms ($\ge10^{11}$). | NMEA 4.10 / IEC 62320-1 |
| `d` | Destination identifier | Alphanumeric ($\le15$ chars) | Identifies target station or network sink | NMEA 4.10 |
| `g` | Sentence grouping | `index-total-groupid` | Tracks multi-fragment reassembly (e.g. `1-2-73874`) | NMEA 4.10 |
| `n` | Line sequence counter | Positive integer | Monotonically incrementing line counter to catch serial packet drops | NMEA 4.10 |
| `r` | Relative time | Numeric string | Milliseconds elapsed from local reference epoch | NMEA 4.10 |
| `s` | Source station identifier | Alphanumeric ($\le15$ chars) | Receiving coastal base station ID (e.g. `r003669945`, `AI0001`) | NMEA 4.10 / IEC 62320-1 |
| `t` | Text remark | Alphanumeric string | Free-text engineering notation | NMEA 4.10 |

---

## D.9 NMEA 2000 Parameter Group Numbers (PGNs)

On marine CAN-bus networks (CAN 2.0B at 250 kbit/s, ISO 11783 / SAE J1939 framing), AIS data is exchanged using Parameter Group Numbers (**PGNs**) rather than ASCII text. Because AIS messages exceed 8 bytes, payloads are transmitted using the J1939 **Fast Packet** multi-packet framing mechanism. The canonical PGN definitions reverse-engineered by the open-source **canboat** project (v8.3.0) are registered below:

### Table D.9: NMEA 2000 AIS Parameter Group Numbers (PGNs)

| PGN (Dec) | PGN (Hex) | Transmission Mode | Min Length | canboat Canonical Title | Underlying AIS Message |
|:---:|:---:|:---:|:---:|:---|:---:|
| **129038** | `0x1F806` | Fast Packet | 28 bytes | AIS Class A Position Report | Messages 1, 2, 3 |
| **129039** | `0x1F807` | Fast Packet | 26 bytes | AIS Class B Position Report | Message 18 |
| **129040** | `0x1F808` | Fast Packet | 54 bytes | AIS Class B Extended Position Report | Message 19 (deprecated) |
| **129041** | `0x1F809` | Fast Packet | 76 bytes | AIS Aids to Navigation (AtoN) Report | Message 21 |
| **129792** | `0x1FAF0` | Fast Packet | Variable | AIS DGNSS Broadcast Binary Message | Message 17 |
| **129793** | `0x1FAF1` | Fast Packet | 11 bytes | AIS UTC and Date Report | Message 4 |
| **129794** | `0x1FAF2` | Fast Packet | 75 bytes | AIS Class A Static & Voyage Related Data | Message 5 |
| **129795** | `0x1FAF3` | Fast Packet | Variable | AIS Addressed Binary Message | Message 6 |
| **129796** | `0x1FAF4` | Single Frame | 8 bytes | AIS Acknowledge | Messages 7, 13 |
| **129797** | `0x1FAF5` | Fast Packet | Variable | AIS Binary Broadcast Message | Message 8 |
| **129798** | `0x1FAF6` | Fast Packet | 23 bytes | AIS SAR Aircraft Position Report | Message 9 |
| **129799** | `0x1FAF7` | Single Frame | 8 bytes | Radio Frequency / Mode / Power | Message 22 local |
| **129800** | `0x1FAF8` | Single Frame | 8 bytes | AIS UTC / Date Inquiry | Message 10 |
| **129801** | `0x1FAF9` | Fast Packet | Variable | AIS Addressed Safety Related Message | Message 12 |
| **129802** | `0x1FAFA` | Fast Packet | Variable | AIS Safety Related Broadcast Message | Message 14 |
| **129803** | `0x1FAFB` | Fast Packet | Variable | AIS Interrogation | Message 15 |
| **129804** | `0x1FAFC` | Fast Packet | Variable | AIS Assignment Mode Command | Message 16 |
| **129805** | `0x1FAFD` | Fast Packet | Variable | AIS Data Link Management Message | Message 20 |
| **129806** | `0x1FAFE` | Fast Packet | Variable | AIS Channel Management | Message 22 |
| **129807** | `0x1FAFF` | Fast Packet | Variable | AIS Class B Group Assignment | Message 23 |
| **129809** | `0x1FB01` | Fast Packet | 26 bytes | AIS Class B Static Data (Part A - Name) | Message 24 Part A |
| **129810** | `0x1FB02` | Fast Packet | 44 bytes | AIS Class B Static Data (Part B - Dims/Call) | Message 24 Part B |
| **129811** | `0x1FB03` | Fast Packet | Variable | AIS Single-Slot Binary (Deprecated) | Message 25 (legacy) |
| **129812** | `0x1FB04` | Fast Packet | Variable | AIS Multi-Slot Binary (Deprecated) | Message 26 (legacy) |
| **129813** | `0x1FB05` | Fast Packet | 16 bytes | AIS Long-Range Broadcast Message | Message 27 |
| **129814** | `0x1FB06` | Fast Packet | Variable | AIS Single-Slot Binary Message | Message 25 |
| **129815** | `0x1FB07` | Fast Packet | Variable | AIS Multi-Slot Binary with Comm State | Message 26 |
| **129816** | `0x1FB08` | Single Frame | 8 bytes | AIS Binary Acknowledge | Message 7/13 (binary) |

*(Note: PGN 129808 is assigned by NMEA to DSC Digital Selective Calling Call Information, not AIS).*

---

## D.10 Master bit-level sentinel values

When physical sensors fail, cables disconnect, or bridge operators omit optional voyage parameters, AIS transponders insert standardized numerical bit patterns signifying "not available." Software pipelines must intercept these sentinel values prior to performing arithmetic operations to prevent severe track corruption.

### Table D.10: Master Bit-Level Sentinel Register

| Message Field | Bit Width | Binary Representation | Integer Value | Engineering Interpretation | Silent Failure Consequence if Ignored |
|:---|:---:|:---|:---:|:---|:---|
| **Latitude** | 27 bits | `010000100100001010000000000` | $+54,600,000$ | $+91.0^\circ$ (Not available) | Vessel plots at the North Pole |
| **Longitude** | 28 bits | `0110011110010001101011000000`| $+108,600,000$| $+181.0^\circ$ (Not available) | Vessel plots beyond the antimeridian |
| **Latitude (Msg 27)** | 17 bits | `01101010101001000` | $+54,600$ | $+91.0^\circ$ (Not available) | Polar displacement in satellite feeds |
| **Longitude (Msg 27)**| 18 bits | `011010100000111000` | $+108,600$ | $+181.0^\circ$ (Not available) | Antimeridian displacement in satellite feeds |
| **Speed Over Ground** | 10 bits | `1111111111` | $1,023$ | $102.3\text{ kn}$ (Not available) | Distorts fleet average velocity models |
| **SOG Saturation** | 10 bits | `1111111110` | $1,022$ | $102.2\text{ kn}$ or higher | Truncates high-speed military/HSC kinematics |
| **Speed Over Ground (27)**| 6 bits| `111111` | $63$ | Not available | Corrupts satellite velocity analytics |
| **Course Over Ground**| 12 bits | `111000100000` | $3,600$ | $360.0^\circ$ (Not available) | Distorts directional polar plots |
| **COG Invalid Range** | 12 bits | `111000100001`–`111111111111` | $3,601$–$4,095$| Strictly forbidden | Parser buffer corruption |
| **Course Over Ground (27)**| 9 bits| `111111111` | $511$ | Not available | Distorts satellite trajectory reconstruction |
| **True Heading** | 9 bits | `111111111` | $511$ | $511^\circ$ (Not available) | Creates artificial north-northeast clustering |
| **Rate of Turn (ROT)**| 8 bits | `10000000` | $-128$ | Not available (No turn info) | Causes spurious $720^\circ/\text{min}$ turns |
| **ROT (No TI right)** | 8 bits | `01111111` | $+127$ | Turning right $>5^\circ/30\text{ s}$; no TI | Squaring formula yields $+708^\circ/\text{min}$ error |
| **ROT (No TI left)** | 8 bits | `10000001` | $-127$ | Turning left $>5^\circ/30\text{ s}$; no TI | Squaring formula yields $-708^\circ/\text{min}$ error |
| **UTC Second** | 6 bits | `111100` | $60$ | Timestamp not available | Ingest engine drops fix timing |
| **UTC Second** | 6 bits | `111101` | $61$ | Manual positioning input mode | Fails to detect lost GPS receiver feed |
| **UTC Second** | 6 bits | `111110` | $62$ | Dead reckoning positioning mode | Ingest engine treats estimated fix as live GPS |
| **UTC Second** | 6 bits | `111111` | $63$ | Positioning system inoperative | Ingest engine treats frozen coordinates as valid |
| **ETA Month** | 4 bits | `0000` | $0$ | Month not available | Parsing dates yields invalid calendar months |
| **ETA Day** | 5 bits | `00000` | $0$ | Day not available | Ingestion crashes on `day=0` in `datetime` |
| **ETA Hour** | 5 bits | `11000` | $24$ | Hour not available | Ingestion crashes on `hour=24` |
| **ETA Minute** | 6 bits | `111100` | $60$ | Minute not available | Ingestion crashes on `minute=60` |
| **Static Draught** | 8 bits | `00000000` | $0$ | Draught not available | Fails under-keel clearance models |
| **Draught Maximum** | 8 bits | `11111111` | $255$ | $25.5\text{ m}$ or greater | Saturated deep-draught tanker limit |
| **Ship Dimensions** | 30 bits | All zeros ($A=B=C=D=0$) | $0$ | Dimensions not available | Hull bounding box collapses to a single point |
| **6-bit ASCII Text** | 6 bits | `000000` | $0$ (`@`) | Unused text padding sentinel | Corrupts vessel names with trailing `@@@@@@` |
| **Class B CS Comm State**| 19 bits| `1100000000000000110` | $393,222$ | Hard-coded CSTDMA signature | Parser misidentifies CS as malfunctioning SOTDMA |

---

## References

- canboat (2026). *CANboat: Open-source NMEA 2000 and CAN Bus Decoder Engine* (Version 8.3.0). URL: https://github.com/canboat/canboat (accessed 2026-10-06).
- International Association of Marine Aids to Navigation and Lighthouse Authorities (2021). *The Use of the Automatic Identification System (AIS) in Marine Aids to Navigation Services* (IALA Recommendation R0126, Edition 2.0). Saint-Germain-en-Laye: IALA.
- International Electrotechnical Commission (2016). *Maritime navigation and radiocommunication equipment and systems – Automatic identification systems (AIS) – Part 2: AIS AtoN stations – Operational and performance requirements, methods of testing and required test results* (Standard No. IEC 62320-2:2016, Edition 2.0). Geneva: IEC.
- International Electrotechnical Commission (2024). *Maritime navigation and radiocommunication equipment and systems – Digital interfaces – Part 1: Single talker and multiple listeners* (Standard No. IEC 61162-1:2024, Edition 6.0). Geneva: IEC.
- International Maritime Organization (1998). *Recommendation on Performance Standards for a Universal Shipborne Automatic Identification System (AIS)* (Resolution MSC.74(69), Annex 3). London: IMO.
- International Maritime Organization (2010). *Guidance on the Use of AIS Application-Specific Messages* (SN.1/Circ.289). London: IMO.
- International Telecommunication Union (2014). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band* (Recommendation ITU-R M.1371-5). Geneva: ITU Radiocommunication Sector.
- International Telecommunication Union (2023). *Technical characteristics of autonomous maritime radio devices operating in the frequency band 156–162.05 MHz* (Recommendation ITU-R M.2135-1). Geneva: ITU Radiocommunication Sector.
- International Telecommunication Union (2024). *Radio Regulations* (Edition 2024). Geneva: ITU.
- International Telecommunication Union (2026). *Assignment and use of identities in the maritime mobile service* (Recommendation ITU-R M.585-10). Geneva: ITU Radiocommunication Sector.
- International Telecommunication Union (2026). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band* (Recommendation ITU-R M.1371-6). Geneva: ITU Radiocommunication Sector.
- National Marine Electronics Association (2023). *Standard for Interfacing Marine Electronic Devices* (NMEA 0183 Version 4.30). Severna Park, MD: NMEA.
- Raymond, E. S. & Schwehr, K. (2023). *AIVDM/AIVDO Protocol Decoding* (Version 1.58). GPSD Project. URL: https://gpsd.gitlab.io/gpsd/AIVDM.html (accessed 2026-10-06).
