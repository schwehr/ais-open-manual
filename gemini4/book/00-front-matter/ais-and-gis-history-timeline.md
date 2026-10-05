# Chronological Timeline of Navigation, Geodesy, GIS, and the Automatic Identification System (AIS)

> **Primary Sources:** Synthesized from Kurt Schwehr's [`https://github.com/schwehr/gis-history`](https://github.com/schwehr/gis-history), Kimbra Cutlip's Global Fishing Watch history ([*AIS for Safety and Tracking: A Brief History*, 2017](https://globalfishingwatch.org/article/ais-brief-history/)), USCG Jorge Arroyo historical archives, and ITU/IMO/IALA/IEC standardization records.

---

## 1. Ancient Navigation, Cartography, and Celestial Timekeeping (~206 BCE – 1799)

| Year | Event / Milestone | Technical & Maritime Significance |
|---|---|---|
| **~206 BCE** | **Magnetic Compass** (Han Dynasty China) | First directional reference independent of coastal landmarks or clear skies (`gis-history`). |
| **~140 BCE** | **Hipparchus** invents spherical trigonometry | Mathematical basis for great-circle orthodromic navigation and spherical coordinate transformations (`gis-history`). |
| **~150 CE** | **Ptolemy's *Geographia*** | Introduces systematic latitude ($\phi$) and longitude ($\lambda$) graticules and map projections (`gis-history`). |
| **1569** | **Gerardus Mercator** publishes conformal cylindrical projection | Rhumb lines (lines of constant compass heading / loxodromes) plot as straight lines—still the mathematical foundation of paper nautical charts and ECDIS Mercator modes (`gis-history`). |
| **1714** | **British Longitude Act** | Parliament offers up to £20,000 for a practical method to determine longitude at sea to within $0.5^\circ$ ($30\text{ NM}$ at the Equator) (`gis-history`). |
| **1731** | **Octant / Sextant** developed (John Hadley & Thomas Godfrey) | High-precision angular altitude measurement of celestial bodies above the sea horizon (`gis-history`). |
| **1735 – 1761** | **John Harrison's Marine Chronometers (H1–H4)** | Demonstrates that **accurate timekeeping is the prerequisite for accurate positioning** ($1\text{ s}$ clock error $\approx 0.25'$ longitude $\approx 463\text{ m}$ at the Equator)—a principle echoed in AIS's dependence on GNSS 1PPS UTC timing (`gis-history`). |
| **1791** | **Principal Triangulation of Great Britain** & **Ordnance Survey** | Birth of national geodetic triangulation networks (`gis-history`). |

---

## 2. Hydrography, Radio Waves, Radar, and Early Maritime Safety Law (1800 – 1945)

| Year | Event / Milestone | Technical & Maritime Significance |
|---|---|---|
| **1807** | **U.S. Survey of the Coast** established by Thomas Jefferson | Precursor to the U.S. Coast and Geodetic Survey and **NOAA** (`gis-history`). |
| **1830** | **U.S. Navy Depot of Charts and Instruments** | Precursor to the U.S. Naval Observatory (USNO) and Naval Oceanographic Office (`gis-history`). |
| **1873** | **International Meteorological Organization (IMO)** | Precursor to the WMO; establishes international marine synoptic weather reporting (`gis-history`). |
| **1884** | **International Meridian Conference** (Washington, DC) | Establishes the **Greenwich Prime Meridian ($0^\circ$ Longitude)** and universal solar day (`gis-history`). |
| **1903** | **GEBCO** (General Bathymetric Chart of the Oceans) | Initiated by Prince Albert I of Monaco (`gis-history`). |
| **1904** | **Christian Hülsmeyer demonstrates the Telemobiloscope (Radar)** | First patent and public demonstration in Cologne/Rotterdam of detecting ships in fog via reflected radio waves (`gis-history`). |
| **1912** | **Sinking of *RMS Titanic* (April 14–15, 1912)** | Spurs mandatory 24-hour shipboard radio watches and the International Ice Patrol (`gis-history`). |
| **1913** | **Reginald Fessenden & Alexander Behm** pioneer **Sonar** | Acoustic echo-ranging for icebergs and seabed depth (`gis-history`). |
| **1914** | **First International Convention for the Safety of Life at Sea (SOLAS)** | Signed in response to the *Titanic* disaster; **SOLAS Chapter V** (*Safety of Navigation*) later becomes the legal instrument mandating global AIS carriage (`gis-history`). |
| **1921** | **International Hydrographic Bureau (now IHO)** founded in Monaco | Standardizes international nautical charts, symbols, and later S-52/S-57/S-100 (`gis-history`). |
| **1927** | **North American Datum of 1927 (NAD27)** | Based on the Clarke 1866 ellipsoid (`gis-history`). |
| **1928** | **Universal Time (UT)** term adopted by the IAU | Standardized astronomical time scale (`gis-history`). |
| **1931** | **Simrad / Kongsberg Maritime** lineage founded | Major Norwegian marine electronics and later spaceborne/shore AIS pioneer (`gis-history`). |
| **1940 – 1942** | **Gee (1940), Decca Navigator (1942), LORAN-A (1942), and UTM (1942)** | WWII hyperbolic radio-navigation chains measure time-difference-of-arrival (TDOA) of synchronized master/slave radio pulses (`gis-history`). |

---

## 3. Information Theory, Atomic Time, Satellite Navigation, and Digital Buses (1946 – 1987)

| Year | Event / Milestone | Technical & Maritime Significance |
|---|---|---|
| **1948** | **Claude Shannon** publishes *A Mathematical Theory of Communication* | Establishes channel capacity, bit rate, and noise floor bounds; **IMO** convention adopted in Geneva (`gis-history`). |
| **1949 / 1955** | **First Atomic Clocks** (1949 ammonia; 1955 Louis Essen Cesium-133) | Enables nanosecond time transfer and GNSS satellite clocks (`gis-history`). |
| **1957** | **IALA** (International Association of Marine Aids to Navigation and Lighthouse Authorities) founded | Establishes VTS, buoyage, and AIS shore-network standards (`gis-history`). |
| **1958** | **Kalman Filter** (Rudolf Kálmán & Richard Bucy) & **USCG AMVER** | State-space recursive estimation used in every VTS and ECDIS radar+AIS tracker (`gis-history`). |
| **1960** | **Coordinated Universal Time (UTC)** begins | Synchronized global time scale; AIS divides every UTC minute into 2,250 time slots (`gis-history`). |
| **1963** | **CGIS (Canada Geographic Information System)** by Roger Tomlinson | First computerized Geographic Information System (`gis-history`). |
| **1969** | **Esri** founded; Soviet **CHAYKA** hyperbolic navigation (`gis-history`) | Commercial GIS software and low-frequency radio navigation. |
| **1970** | **Unix Epoch (`1970-01-01T00:00:00Z`)** & **NOAA** established | Unix epoch timestamps later form the `c:` field of NMEA TAG blocks (`gis-history`). |
| **1972** | **C Programming Language** (Dennis Ritchie) & **COLREGs 1972** | International Regulations for Preventing Collisions at Sea (Rules 5, 7, 8) (`gis-history`). |
| **1973 – 1978** | **Navstar GPS** approved (1973); **First GPS Block I satellite launched (Feb 22, 1978)** | Global spaceborne L-band positioning and microsecond UTC timing (`gis-history`). |
| **1974** | **SOLAS 1974 Convention** & **LORAN-C** designated for US civilian maritime use | Modern treaty framework for SOLAS Chapter V amendments (`gis-history`). |
| **1982** | **UNCLOS** signed at Montego Bay & **First GLONASS launch** | Defines territorial sea ($12\text{ NM}$), contiguous zone ($24\text{ NM}$), EEZ ($200\text{ NM}$), and innocent passage (`gis-history`). |
| **1983** | **PROJ** cartographic projections library started by Gerald Evenden (USGS) | Open-source coordinate transformation engine (`gis-history`). |
| **1984** | **NMEA 0183** released & **WGS84** geodetic datum established | Both the serial ASCII sentence bus (`$GP...` / `!AI...`) and the reference ellipsoid mandated for AIS are born in 1984 (`gis-history`). |

---

## 4. The Birth of STDMA, *Exxon Valdez*, Competing Prototypes, and AIS Standardization (1988 – 2000)

| Year | Event / Milestone | Technical & Maritime Significance |
|---|---|---|
| **Sept 9, 1988** | **Håkan Lans** files Swedish priority patent application for **STDMA** | Invents Self-Organizing Time Division Multiple Access, allowing transponders to autonomously coordinate slot reservations without a central master station (granted as **US Patent 5,506,587** in 1996). |
| **March 24, 1989** | ***Exxon Valdez* Oil Spill** on Bligh Reef, Prince William Sound, Alaska | Catastrophic grounding exposes the inability of shore VTS radar alone to positively identify and track tankers through rain/ice clutter and fjord shadows (`gis-history`). |
| **Aug 18, 1990** | **U.S. Oil Pollution Act of 1990 (OPA-90)** enacted | Mandates double hulls and requires vessels in Prince William Sound and VTS zones to carry automated position-reporting transponders. |
| **1991 – 1995** | **Linux** (1991), **Python** (1992), **R** (1993), **Blender initial release** (1994), **PROJ4 & OGC** (1994), **NumPy** (1995) | The core open-source scientific, geospatial, and 3D visualization software stack (`gis-history`). |
| **1991 – 1997** | **Three Competing Vessel Tracking Prototypes:**<br>1. **UK Dover Strait:** VHF DSC Ch 70 "4S" polling<br>2. **Panama Canal:** UHF CTAN<br>3. **Sweden/Finland:** Håkan Lans VHF **SOTDMA** | IALA, ITU, and IMO evaluate polling vs. self-organizing broadcast. DSC polling saturates at $>40$ ships; Håkan Lans's dual-channel VHF SOTDMA scales to hundreds of ships autonomously ([Cutlip, 2017](https://globalfishingwatch.org/article/ais-brief-history/)). |
| **1996** | **USCG Nationwide DGPS** operational; **US Patent 5,506,587** granted to Håkan Lans | Medium-frequency DGNSS beacons provide $1\text{–}3\text{ m}$ differential accuracy along coasts (`gis-history`). |
| **1998** | **ITU-R Recommendation M.1371-0** adopted; **IMO MSC.74(69) Annex 3**; USCG **PAWSS** modernizes **New Orleans VTS** | First international AIS technical standard ratified; USCG selects Lower Mississippi / New Orleans as the first operational AIS-based VTS ([Cutlip, 2017](https://globalfishingwatch.org/article/ais-brief-history/)). |
| **May 1, 2000** | **U.S. disables GPS Selective Availability (SA)** | Standalone civilian GPS accuracy jumps overnight from $\sim 100\text{ m}$ to $<10\text{ m}$, making unaugmented shipboard AIS accurate worldwide (`gis-history`). |
| **2000** | **GDAL** (Frank Warmerdam), **SQLite** (D. Richard Hipp), **NMEA 2000** | Foundational geospatial raster/vector and embedded database libraries (`gis-history`). |
| **Dec 2000** | **IMO adopts revised SOLAS Chapter V, Regulation 19** | Mandates AIS carriage on all new ships from July 1, 2002, with phased retrofit for existing ships $\ge 300\text{ GT}$ (international) and $\ge 500\text{ GT}$ (domestic). |

---

## 5. September 11, 2001, Global Rollout, Open-Source Software, and Spaceborne AIS (2001 – 2015)

| Year | Event / Milestone | Technical & Maritime Significance |
|---|---|---|
| **2001** | **SkyTruth** founded by John Amos; **PostGIS** first released | Satellite environmental watchdog and spatial PostgreSQL database (`gis-history`). |
| **Sept 11, 2001** | **9/11 Terrorist Attacks** on the United States | Dramatically accelerates AIS implementation; AIS transforms from a bridge collision-avoidance tool into a cornerstone of **Maritime Domain Awareness (MDA)** and homeland security ([Cutlip, 2017](https://globalfishingwatch.org/article/ais-brief-history/)). |
| **July 1, 2002** | **SOLAS Chapter V AIS Mandate Takes Effect** | Mandatory carriage begins for new vessels and passenger ships (`gis-history`). |
| **Oct 2002** | **Blender Released as Open Source (GPL)** | Ton Roosendaal / Blender Foundation open-sources **Blender** (`gis-history`), enabling Python (`bpy`) 3D scientific and maritime casualty visualization. |
| **Nov 25, 2002** | **U.S. Maritime Transportation Security Act of 2002 (MTSA)** | Mandates the USCG **Nationwide AIS (NAIS)** coastal receiver network and domestic vessel carriage; **QGIS** and **GEOS** also launch in 2002 (`gis-history`). |
| **2003** | **St. Lawrence Seaway Mandatory AIS** & **WAAS** operational | First inland waterway with mandatory AIS and automated lock/water-level binary messaging (`gis-history`). |
| **2004 – 2006** | **Norwegian FFI Space-Based AIS feasibility studies**; **TACSAT-2** & **Rubin** LEO experiments; **IEC 62287-1 Class B CSTDMA** (2006); **IMO adopts LRIT** (2006) | Proves that VHF AIS signals ($162\text{ MHz}$) penetrate the ionosphere and can be received from Low Earth Orbit ($500\text{–}800\text{ km}$), launching the Satellite AIS (S-AIS) industry. |
| **2006 – 2009** | **UNH CCOM/JHC (`noaadata` + `Blender` + `aisparser` + `gpsd`)** & **NOAA ERMA** (2006) | Kurt Schwehr develops **`noaadata`** and **`ais-area-notice`**, coupling Python AIS decoders with **Blender (`bpy`)** to render 3D vessel tracks over multibeam bathymetry and Stellwagen Bank right-whale zones; Brian C. Lane writes **`aisparser`**; Eric S. Raymond & Kurt Schwehr document **`AIVDM.txt`** in **`gpsd`** (`gis-history`). |
| **2009** | **EU Mandates AIS on Fishing Vessels $\ge 15\text{ m}$** | Phased in 2012–2014 ($24\text{ m}$, $18\text{ m}$, $15\text{ m}$), bringing thousands of European trawlers onto AIS. |
| **March 30, 2010** | **USPTO Cancels All Claims (1–19) of Håkan Lans's US Patent 5,506,587** | Following Ex Parte Reexamination (`90/008,299` & `90/008,522`), the USPTO cancels all claims of the foundational STDMA patent; the natural 20-year term expires in 2012/2013. |
| **April 20, 2010** | ***Deepwater Horizon* Blowout** & **Creation of `libais`** | Response vessels flood the Gulf of Mexico; pure-Python `BitVector` decoding is too slow for real-time ingestion into **NOAA ERMA**, prompting Kurt Schwehr to write **`libais`** in C++ (`gis-history`). |
| **July 2010** | **Norway Launches AISSat-1** | Dedicated polar-orbiting scientific/governmental AIS nanosatellite. |
| **2012** | **Whale Alert** presented to the U.S. Congress | Combines acoustic buoys, **AIS Area Notices (`ais-area-notice`)**, and mobile apps to protect North Atlantic Right Whales (`gis-history`). |
| **2013** | **"All the Ships"** talk & **GeoPandas** released | Kurt Schwehr's Google I/O / geospatial architecture work on processing global satellite AIS at scale (`gis-history`). |
| **2014** | **ITU-R M.1371-5** ratified; **Sentinel-1A SAR** launched; **Balduzzi et al.** publish *"A Security Evaluation of AIS"* | Adds Message 27 (Long-Range Satellite AIS on Ch 75/76); ESA launches open C-band SAR satellite; researchers demonstrate RF & software AIS spoofing (`gis-history`). |
| **2015** | **ITU-R M.2092-0 (VDES / "AIS 2.0")** published | Defines the VHF Data Exchange System combining AIS, ASM, VDE-TER, and VDE-SAT. |

---

## 6. Cloud Analytics, Dark-Fleet Unmasking, S-100, and VDES Transition (2016 – 2028+)

| Year | Event / Milestone | Technical & Maritime Significance |
|---|---|---|
| **March 2016** | **USCG Final Rule on AIS (33 CFR § 164.46)** takes effect | Expands mandatory US AIS carriage to all commercial vessels $\ge 65\text{ ft}$ (including fishing vessels) and towing vessels $\ge 26\text{ ft}$ with $>600\text{ hp}$. |
| **Sept 2016** | **Global Fishing Watch (GFW)** publicly launched | Founded by Oceana, SkyTruth, and Google; publishes Kroodsma et al. (2018, *Science*) mapping global fishing effort from billions of AIS positions (`gis-history`). |
| **2017** | ***USS Fitzgerald* & *USS John S. McCain* Collisions**; **NorSat-2** launched | Prompts US Navy review of Warship AIS (W-AIS) and Encrypted AIS (EAIS) doctrine; NorSat-2 tests space-to-ship ASM transmissions. |
| **2018** | **`MovingPandas`** (Anita Graser) & **`DuckDB`** started | Modern open-source trajectory analysis and in-process columnar SQL engine (`gis-history`). |
| **2019** | **C4ADS *Above Us Only Stars* Report** & **ITU-R M.2135 (AMRD)** | Exposes widespread state-level GNSS/AIS spoofing in the Black Sea/Russian ports; ITU regulates fishing-gear AIS pingers onto $160.900\text{ MHz}$ (Ch 2006). |
| **2020 – 2021** | **`GeoArrow`** (2020), **`GeoParquet`** (2021), ***Alexandra 1 / Ever Smart* [2021] UKSC 6**, ***Ever Given* Suez Grounding**, & **China PIPL/DSL AIS Restriction** | UK Supreme Court rules on AIS/VDR collision forensics; China restricts foreign access to terrestrial Chinese AIS feeds (`gis-history`). |
| **2023** | **NorSat-TD** & **Sternula-1** launch **VDES** satellite payloads; **UK Admiralty CPR Part 61 Reforms** | Operational two-way VDE-SAT satellite communications demonstrated in orbit. |
| **Jan 2024** | **Paolo et al. (*Nature*, 2024)** & ***MV Dali* Key Bridge Collapse (March 2024)** | GFW/Sentinel-1 SAR study reveals 75% of industrial fishing vessels and 25% of transport/energy vessels are "dark" (not broadcasting AIS); *Dali* VDR/AIS data drives instant NTSB & Blender 3D forensic reconstructions. |
| **Aug 2024** | **IALA transitions to an Intergovernmental Organization (IGO)** | Elevates IALA standards for VTS, AtoNs, and AIS shore networks to treaty-backed international status. |
| **2025** | **GFW / Johnny Harris *"Dark Zones"* Investigation** & **CVE-2025-66217** | Publicizes global shadow fleets, dark transshipments, and MPAs ([`https://youtu.be/2tuS1LLOcsI`](https://youtu.be/2tuS1LLOcsI)). |
| **2026 – 2028** | **IHO S-100 Operational ECDIS Phase-In (2026)** & **IMO SOLAS VDES Amendments Enter into Force (Jan 1, 2028)** | S-101/S-102/S-104/S-124/S-421 digital charting converges with two-way authenticated VDES (AIS 2.0). |
