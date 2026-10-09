# Chapter 52 — AIS and the S-100 family

> **Part VIII — Charts, bridge systems, and mariners.** How the Universal Hydrographic Data Model transforms nautical charting, dynamic maritime safety information, and route exchange, redefining the role of AIS and VDES across the bridge navigation stack.

**In this chapter.** You will learn how the International Hydrographic Organization (**IHO**) S-100 universal hydrographic data model framework restructures maritime data exchange and transforms how the Automatic Identification System (**AIS**) and the VHF Data Exchange System (**VDES**) interact with bridge navigation displays. We examine the transition from legacy S-57 Electronic Navigational Charts (**ENCs**) and S-52 display specifications to the modular, register-driven S-100 architecture and S-101 next-generation ENCs. You will trace how dynamic maritime safety information, water level data, surface current vectors, marine aids to navigation, and digital route plans are mapped into operational S-100 product specifications including S-104, S-111, S-124, S-125, S-201, and S-421. We evaluate the regulatory timeline established by International Maritime Organization (**IMO**) Resolution MSC.530(106) and MSC.530(106)/Rev.1 governing dual-fuel Electronic Chart Display and Information Systems (**ECDIS**). Finally, you will analyze the physical and logical bandwidth constraints governing S-100 data delivery across VHF Data Link (**VDL**) application-specific messages and emerging terrestrial and satellite VDES data bearers.

## 52.1 The S-100 framework: architecture and governance

Digital hydrography and bridge navigation long rested on a single specification: IHO **S-57** (*IHO Transfer Standard for Digital Hydrographic Data*). Adopted in Edition 3.0 in 1996 and frozen in Edition 3.1 in 2000, S-57 served as the exchange format for vector Electronic Navigational Charts (**ENCs**) on type-approved Electronic Chart Display and Information Systems (**ECDIS**) (IHO S-57 2000). However, S-57 suffered from structural limitations: rigid object catalogs bound to the base standard, lack of mechanisms for high-volume dynamic data (gridded bathymetry, water levels, currents, transient warnings), and encapsulation restricted to ISO/IEC 8211.

To overcome these barriers, the IHO Hydrographic Services and Standards Committee (**HSSC**) initiated the **S-100** *Universal Hydrographic Data Model* in 2001 (developed by TSMAD and maintained by the **S-100 Working Group**, **S-100WG**). Released as Edition 1.0.0 in 2010, S-100 provides an extensible geospatial framework aligned with the ISO 19100 geographic standards (ISO 19106, 19109, 19115) (IHO S-100 2025).

```text
                      +------------------------------------------+
                      |        IHO Geospatial Information        |
                      |            Registry (KHOA)               |
                      |  - Feature Concept Dictionary (FCD)      |
                      |  - Portrayal Register                    |
                      |  - Product Specification Register        |
                      +---------------------+--------------------+
                                            |
                                            v
+----------------------------------------------------------------------------------------+
|                          S-100 Framework Parts (Ed. 5.2.1)                             |
|  Part 1: Conceptual Schema (UML)       Part 9: Portrayal (Lua & XSLT)                  |
|  Part 3: General Feature Model (GFM)   Part 10: Encodings (10a 8211, 10b GML, 10c HDF5)|
|  Part 5: Feature Catalogues (XML)      Part 15: Encryption & Data Protection           |
|  Part 8: Imagery & Gridded Data        Part 17: Discovery Metadata                     |
+-------------------------------------------+--------------------------------------------+
                                            |
         +----------------------------------+----------------------------------+
         |                                  |                                  |
         v                                  v                                  v
+------------------+              +-------------------+              +------------------+
|   IHO Domain     |              |    IALA Domain    |              | IEC TC 80 / WMO  |
|  (S-101..S-199)  |              |  (S-201..S-299)   |              |  (S-401..S-421)  |
| - S-101 Base ENC |              | - S-201 AtoN DB   |              | - S-411 Sea Ice  |
| - S-102 Bathy    |              | - S-212 VTS Data  |              | - S-412 Met-Wave |
| - S-104 Tides    |              | - S-230 ASM Spec  |              | - S-421 Route    |
| - S-111 Currents |              | - S-240 DGNSS     |              |   (IEC 63173-1)  |
| - S-124 MSI/Warn |              +-------------------+              +------------------+
| - S-125 AtoN Nav |                        |                                  |
+--------+---------+                        +-----------------+----------------+
         |                                                    |
         +--------------------------+-------------------------+
                                    |
                                    v
         +----------------------------------------------------+
         |       Interoperability & Portrayal Engine          |
         |         S-98 Interoperability Level 0-4            |
         |         S-100 ECDIS (IMO Res. MSC.530(106))        |
         +--------------------------+-------------------------+
                                    |
            +-----------------------+-----------------------+
            |                                               |
            v                                               v
+-----------------------+                       +-----------------------+
|  VHF Data Link (VDL)  |                       |  VDES Physical Layers |
|  - AIS 1 / AIS 2      |                       |  - ASM 1 / ASM 2      |
|  - Message 21 (AtoN)  |                       |  - VDE-TER (307 kbps) |
|  - ASM (FI 31 / 367)  |                       |  - VDE-SAT (Downlink) |
+-----------------------+                       +-----------------------+
```

### 52.1.1 Registers, catalogues, and parts

The structural backbone of S-100 is the **IHO Geospatial Information Registry** (**GI Registry**), hosted and operated by the Korea Hydrographic and Oceanographic Agency (**KHOA**) under the authority of the IHO Secretariat. The GI Registry maintains web-accessible registries:
- **Feature Concept Dictionary (FCD) Register:** An international repository of hydrographic concepts specifying feature names, definitions, and distinct attributes. Domains register concepts without affecting existing catalogs.
- **Portrayal Register:** Houses graphical symbols, fill patterns, line styles, viewing rules, and rendering instructions.
- **Product Specification Register:** Tracks official versioning, development status, and metadata schemas across participating organizations.

S-100 separates conceptual data definition from physical delivery format. Under S-100 Edition 5.2.1 (December 2025), the standard is partitioned into 19 formal parts:
- **Part 1 (Conceptual Schema):** Governs Unified Modeling Language (**UML**) profiles.
- **Part 3 (General Feature Model - GFM):** Establishes the core meta-model defining features, information types, associations, and geometries.
- **Part 5 (Feature Catalogue):** Formalizes an XML schema for distributing machine-readable feature catalogs.
- **Part 8 (Imagery and Gridded Data):** Defines spatial representations for regular and irregular gridded structures, bathymetric surfaces, and multi-dimensional matrices.
- **Part 9 and 9a (Portrayal):** Replaces static lookup tables with XML portrayal catalogs executing dynamic formatting rules written in **Lua**.
- **Part 10 (Encoding Formats):** Defines concrete serializations: Part 10a (ISO/IEC 8211 for vector ENCs), Part 10b (GML under ISO 19136), and Part 10c (HDF5 for high-volume grids and time series).
- **Part 15 (Data Protection Scheme):** Extends digital encryption, PKI authentication, and cryptographic signatures across all S-100 datasets, succeeding legacy **S-63**.
- **Part 16 and 16a (Interoperability):** Coordinates layered display, priority stacking, and feature suppression of concurrent S-100 layers.
- **Part 17 (Discovery Metadata):** Standardizes cataloging and metadata structures for automated web distribution and machine-to-machine exchange.

### 52.1.2 Multi-agency domain governance

S-100 serves as the foundation for the IMO **Common Maritime Data Structure** (**CMDS**) under e-navigation (IMO MSC.1/Circ.1595). The IHO allocated numerical ranges across international organizations: S-101–S-199 to IHO (hydrography: S-101 ENC, S-102 bathymetry, S-104 tides, S-111 currents, S-124 warnings, S-128 catalog, S-129 UKCM); S-201–S-299 to IALA (aids to navigation and VTS: S-201 AtoN, S-212 VTS, S-230 ASM, S-240 DGNSS); S-401–S-410 to IEHG (Inland ENC); S-411–S-420 to WMO (sea ice and marine weather); and S-421–S-430 to IEC TC 80 (bridge data interfaces, led by S-421 Route Plan).

> **Definitions that bite.** An **S-100 Product Specification** is not an electronic chart format. It is a domain-specific standard compiled under S-100 framework rules that specifies a discrete Feature Catalogue (XML), a Portrayal Catalogue (Lua scripts and SVG symbols), an Application Schema (UML), and an explicit encoding rule (ISO/IEC 8211, GML, or HDF5). An S-100 ECDIS does not run a single parser; it executes a modular runtime environment capable of compiling, verifying, decrypting, and harmonizing multiple distinct product specifications simultaneously.

## 52.2 S-101: Next-generation electronic navigational charts

The operational core of the S-100 ecosystem is **S-101**, the next-generation ENC product specification designed to supersede S-57 Edition 3.1. Developed over fifteen years by the S-100WG, the IHO approved S-101 Edition 2.0.0 on 27 December 2024 as the "first operational Edition" (baselined on S-100 Edition 5.2.0), transitioning S-101 from an experimental testbed into an internationally recognized production standard (IHO S-101 2024).

### 52.2.1 Technical improvements over S-57

While maintaining cartographic continuity, S-101 introduces core architectural improvements:
1. **Dynamic portrayal via Lua:** Rather than hard-coding symbol logic in ECDIS firmware per S-52 Presentation Library lookup tables, S-101 bundles machine-readable **Lua** scripts and SVG primitives directly in exchange sets, enabling symbol updates without firmware recertification.
2. **Complex and composite attributes:** S-101 replaces flat primitives with hierarchical complex attributes and multiplicity arrays, modeling multi-sector lights and complex schedules within single features.
3. **Information types and associations:** Non-spatial context (regulations, radio services, call signs) is modeled as **Information Types** linked to chart features via formal UML associations, eliminating text duplication.
4. **Enhanced update mechanics:** S-101 formalizes strict topological identifiers and delta-encoding in ISO/IEC 8211 records (Part 10a), preventing boundary corruption during automated updates.

### 52.2.2 Portrayal engine and S-98 interoperability

A critical hazard on modern navigation bridges is visual clutter resulting from uncoordinated data overlays. If an ECDIS naively stacks bathymetric grids (S-102), tidal depth contours (S-104), current streamlines (S-111), virtual aids to navigation (S-125), and live AIS targets on top of an ENC, critical navigation hazards, sounding labels, and collision avoidance vectors become unreadable.

To prevent screen clutter, IHO published **S-98** (*S-100 ECDIS and Interoperability Specification*, Edition 2.0.0, October 2025) (IHO S-98 2025). S-98 defines five **Interoperability Levels**:
- **Level 0 (Independent):** Isolated layer toggling.
- **Level 1 (Visual overlay):** Harmonized color palettes and non-essential feature suppression.
- **Level 2 (Replacement):** High-precision data replaces base features (e.g., S-102 bathymetry suppresses coarse S-101 soundings).
- **Level 3 (Topological composition):** Real-time sensor integration (e.g., S-104 water levels dynamically recalculate S-101 safety contours and UKC no-go areas).
- **Level 4 (Unified picture):** Dynamic sensor fusion combining live AIS/VDES tracks, S-111 surface currents, and S-421 route geometry into unified navigation corridors.

```text
+------------------------------------------------------------------------------------+
|                S-98 Interoperability Stacking Engine (Level 2 & 3)                 |
|                                                                                    |
| [Layer 5: Dynamic Sensors]    AIS / VDES Targets (IEC 62288) & Nav Warnings (S-124)|
|                                      |                                             |
| [Layer 4: Marine Aids]        AtoN Overlay (S-125 / S-201 Physical/Virtual)       |
|                                      |                                             |
| [Layer 3: Dynamic Physics]    Water Level (S-104) & Surface Currents (S-111)      |
|                                      v (Dynamically adjusts depths & safety buffer)|
| [Layer 2: High-Res Surface]   High-Density Bathymetry Grids (S-102)                |
|                                      v (Suppresses redundant S-101 spot soundings) |
| [Layer 1: Navigational Base]  S-101 Base ENC (Coastline, Hazards, Restricted Areas)|
+------------------------------------------------------------------------------------+
```

## 52.3 The Phase 1 product specifications: dynamic hydrography and safety

Under the *Roadmap for the S-100 Implementation Decade (2020–2030)* (Version 5.0, October 2025), the IHO Council established operational targets for **Phase 1** route-monitoring products (IHO 2025). Key operational specifications include: S-101 ENC (Ed. 2.0.0, Dec 2024; ISO/IEC 8211); S-102 Bathymetry (Ed. 3.0.0, Dec 2024; HDF5); S-104 Water Levels (Ed. 2.0.0, Dec 2024; HDF5); S-111 Currents (Ed. 2.0.0, Dec 2024; HDF5); S-124 Navigational Warnings (Ed. 2.0.0, Mar 2025; GML); S-125 AtoN (Ed. 1.0.0, Jun 2026; GML); S-128 Catalogues (Ed. 2.0.0, Mar 2025; XML/GML); S-129 UKCM (Ed. 2.0.0, Dec 2024; GML); S-201 AtoN Information (Ed. 2.0.0, May 2025; GML); and S-421 Route Plan (Ed. 1.0.0, Jun 2021; XML/GML). Several intersect directly with information historically carried over AIS Application-Specific Messages (**ASMs**).

### 52.3.1 S-124: Navigational warnings and digital MSI

Navigational warnings have long relied on plain text via 518 kHz **NAVTEX** and satellite **SafetyNET** under **GMDSS**, requiring manual bridge plotting that risks error. **S-124** Edition 2.0.0 (March 2025, WWNWS-SC) standardizes machine-readable digital **Maritime Safety Information** (**MSI**) in GML (Part 10b) (IHO S-124 2025). Datasets encode warning classifications, exact geometry (points, lines, polygons), validity schedules, and mandatory restrictions. An S-100 ECDIS plots hazard polygons with standard warning symbology and evaluates them against the monitored route, triggering automated collision or exclusion alerts. Under the IHO Roadmap Annex 2, S-124 remains a **supplementary service** to statutory GMDSS radio services under SOLAS Chapter IV rather than an immediate replacement.

### 52.3.2 S-104 and S-111: Water levels and currents

Physical oceanography historically reached bridges via AIS Application-Specific Messages (e.g., Message 8, DAC 001, FI 31 per IMO SN.1/Circ.289), but was limited to discrete point-sensor telemetry (IMO 2010). In contrast, **S-104** (Water Level Information) and **S-111** (Surface Currents), approved in Edition 2.0.0 in December 2024 by TWCWG, deliver continuous hydrodynamic models encoded in **HDF5** (Part 10c) (IHO S-104 2024; IHO S-111 2024). S-104 structures regular spatial grids (`dataCodingFormat = 2`) across forecast steps relative to Chart Datum. When ingested, the S-98 engine dynamically recalculates shallow-water contours and UKC margins. S-111 provides gridded current vectors, enabling real-time drift calculations and streamlined flow visualization along active routes.

## 52.4 Aids to navigation: S-125, S-201, and AIS AtoN

The modeling of physical, synthetic, and virtual Aids to Navigation (**AtoN**) represents one of the most direct intersections between the S-100 framework and AIS. In legacy bridge operations, an AIS AtoN is experienced as an **AIS Message 21** (*Aids to Navigation Report*) received over 161.975 MHz or 162.025 MHz (ITU-R M.1371-5, Annex 8 §3.18). Message 21 broadcasts the AtoN's 9-digit MMSI ($99\text{MID}xxxx$), name, position, dimension offsets, positioning device type, and virtual AtoN flag (bit 269: $0 = \text{real/physical}$, $1 = \text{virtual}$).

In the S-100 architecture, AtoN data is governed by two complementary specifications developed through close coordination between IHO and IALA: **S-201** and **S-125**.

```text
+-----------------------------------------------------------------------------------+
|                        The Three Faces of an AIS AtoN                             |
|                                                                                   |
|  1. The Authority Asset (S-201 Ed. 2.0.0 GML)                                     |
|     - Model: PhysicalAISAidToNavigation, VirtualAISAidToNavigation               |
|     - Associations: Linked to RadioStation (AIS Base Station), maintenance logs,   |
|       power supply, mooring chain tension, operational authorization.             |
|     - Audience: Lighthouse authorities, coast guards, port engineers.             |
|                                                                                   |
|  2. The Radio Broadcast (AIS Message 21 / ITU-R M.1371-5)                         |
|     - Model: 272-bit binary RF burst on AIS 1 / AIS 2 (VDL)                       |
|     - Payload: MMSI (99xxxxxxx), Type (1..31), Name, Lat/Lon, Virtual Flag (bit 269)|
|     - Audience: All VHF receivers within line-of-sight RF range.                  |
|                                                                                   |
|  3. The Mariner Chart & Overlay (S-101 ENC / S-125 Ed. 1.0.0 GML)                  |
|     - Model: Navigational feature with Portrayal Catalogue rendering (S-52/S-100)|
|     - Attributes: Visual range, light characteristics, verified status, hazards.  |
|     - Audience: ECDIS bridge displays, pilot tablets (PPUs).                      |
+-----------------------------------------------------------------------------------+
```

### 52.4.1 The complementary roles of S-201 and S-125

Although both specifications model AIS AtoN features, their target architectures differ fundamentally:
1. **IALA S-201 (Aids to Navigation Information):** Approved in Edition 2.0.0 on 19 May 2025 as an operational standard, S-201 is an **authority-to-authority asset management exchange** (IALA S-201 2025). It is not designed for ECDIS navigation engines. S-201 captures the operational and engineering lifecycle of an AtoN: moorings, solar arrays, power sources, and maintenance logs. It models `PhysicalAISAidToNavigation`, `SyntheticAISAidToNavigation`, and `VirtualAISAidToNavigation` features, explicitly associating synthetic and virtual marks with the shore-side `RadioStation` (AIS base station) that transmits them.
2. **IHO/IALA S-125 (Marine Aids to Navigation):** Released as Edition 1.0.0 in June 2026 (cover dated December 2025) for testing, S-125 is the **mariner-facing digital navigational publication** designed for ECDIS and ECS (IHO/IALA S-125 2026). Maintained under NIPWG, S-125 serves as the digital *List of Lights*, stripping engineering telemetry to present verified navigational attributes: charted sectors, racon codes, and real-time operational status (e.g., buoy off-station, light extinguished).

### 52.4.2 Modeling physical, synthetic, and virtual AIS AtoN

Both S-201 and S-125 establish formal object models reflecting the three operational modalities of AIS navigational aids:
- **Physical AIS AtoN:** A physical navigation buoy or beacon equipped with an integrated AIS transponder (typically an autonomous, low-power IALA Type 1 or Type 3 AIS station). The transponder broadcasts Message 21 from its actual physical location. In S-125, the physical buoy feature (`BuoyLateral`, `BuoyCardinal`) maintains a direct aggregation link to a `PhysicalAISAidToNavigation` feature.
- **Synthetic AIS AtoN:** A physical navigational mark that does *not* carry an AIS transmitter. Instead, an AIS coastal base station ashore or a nearby monitored station broadcasts Message 21 using the charted coordinates of the physical buoy, setting the virtual flag to 0. S-201 and S-125 link the buoy feature to a `SyntheticAISAidToNavigation` feature, which in turn maintains an explicit association with the shore-side `RadioStation` responsible for the broadcast.
- **Virtual AIS AtoN:** No physical structure exists in the water. An AIS shore station broadcasts Message 21 with bit 269 set to 1, placing a digital mark on passing ships' navigation screens to indicate a newly discovered wreck, a shifting shoal, a temporary safety fairway, or an offshore construction exclusion zone. In S-125, a `VirtualAISAidToNavigation` feature represents this digital hazard, explicitly bound to the broadcasting `RadioStation` MMSI.

> **Worked example.** Consider a newly sunken wreck obstructing a fairway entrance. A coastal authority deploys an emergency virtual South Cardinal mark using an AIS base station (MMSI 002573000).
> - **On the wire (RF Link):** The base station transmits an AIS Message 21 on 161.975 MHz. The packet carries MMSI 992572001 (an official AtoN identity), AtoN Type 24 (South Cardinal), Position $59^\circ 15.200'\text{ N}, 010^\circ 25.100'\text{ E}$, and bit 269 set to 1 (`virtual_aton_flag = True`).
> - **In the Authority Database (S-201 GML):** The authority generates an S-201 record containing a `VirtualAISAidToNavigation` element with `id="VATON_2026_042"`. The record contains an `informationAssociation` pointing to a `RadioStation` feature with `mmsiNumber="002573000"`, capturing transmission slot allocation, channel selection (AIS 1/2), and operational logging.
> - **On the Mariner's Bridge (S-101 / S-125 Overlay):** The bridge ECDIS ingests the Message 21 via NMEA 0183 `!AIVDM` sentences. The ECDIS cross-references the broadcast against its active S-125 digital AtoN dataset. If S-125 confirms the virtual mark, the portrayal engine draws the standardized diamond symbol with a "V-AIS" annotation. If the vessel approaches within 1.0 nmi, the S-98 safety engine generates an audible hazard alert.

## 52.5 S-421: Route plan exchange

Navigation safety has historically been hindered by the inability of ships to communicate their intended route plans digitally to Vessel Traffic Services or to approaching vessels. Voice VHF radiotelephone negotiations ("I will pass you on two whistles") remain prone to linguistic misinterpretation, accent confusion, and spatial ambiguity, causing numerous catastrophic collisions.

To standardize route exchange, IEC TC 80 developed **S-421** (*Route Plan*), published as international standard **IEC 63173-1:2021** (IEC 2021). Baselined on the S-100 framework, S-421 replaces legacy proprietary route files and early RTZ (*Route Plan Exchange Format* under IEC 61174) with a standardized GML/XML structure modeling discrete waypoints, temporal constraints (ETAs, speed windows), hull passage parameters (draught, trim, air draught), and operational route status.

In May 2024, the IMO Maritime Safety Committee at its 108th session adopted **Resolution MSC.530(106)/Rev.1**, amending the S-100 ECDIS performance standards to formally incorporate standardized digital route plan exchange via S-421 (IMO 2024). Under this mandate, an S-100 ECDIS must be capable of importing, exporting, and verifying S-421 route plans. This establishes the structural framework for **ship-to-shore route exchange** (transmitting the ship's intended passage plan to coastal VTS centers for traffic de-confliction) and **shore-to-ship route optimization** (coastal authorities uploading optimized fairways, safety corridors, or speed-adjusted transit slots directly into shipboard navigation consoles).

## 52.6 IMO MSC.530(106) and the dual-fuel ECDIS timeline

The legal and commercial transition to the S-100 framework is governed by IMO **Resolution MSC.530(106)** (*Performance Standards for Electronic Chart Display and Information Systems (ECDIS)*), adopted on 7 November 2022 and amended by MSC.530(106)/Rev.1 on 24 May 2024 (IMO 2022; IMO 2024).

```text
   1996 - 2008              2009 - 2025              2026 - 2028               2029 Onward
+-----------------+      +-----------------+      +-----------------+      +-----------------+
| Res. A.817(19)  | ---> | Res. MSC.232(82)| ---> |   Transition    | ---> | MSC.530(106)    |
| Legacy ECDIS    |      | Classic ECDIS   |      |   (Dual Fuel)   |      | Mandatory S-100 |
| S-57 / S-52     |      | S-57 / S-52     |      | Voluntary S-100 |      | S-101 / S-100   |
|                 |      | PresLib 4.0     |      | S-57 or S-101   |      | Full S-98 Stack |
+-----------------+      +-----------------+      +-----------------+      +-----------------+
                                                  ^ 1 January 2026         ^ 1 January 2029
                                                    Voluntary S-100          Mandatory for
                                                    Type Approval            New Installations
```

### 52.6.1 The 2026 voluntary and 2029 mandatory milestones

Under Chapter V, Regulation 18.4 of the International Convention for the Safety of Life at Sea (**SOLAS**), shipboard navigation systems must conform to performance standards not inferior to those adopted by the IMO in effect on their date of installation. MSC.530(106) operational paras 2 and 3 establish an explicit phased schedule:
1. **Installations prior to 1 January 2026:** Continue to be governed by Resolution MSC.232(82) (or Resolution A.817(19) for pre-2009 systems). Existing vessels are not forced into mandatory retrofits.
2. **Installations from 1 January 2026 through 31 December 2028:** National maritime administrations may type-approve ECDIS conforming *either* to the legacy MSC.232(82) standard or to the new S-100 Annex specified in MSC.530(106)/Rev.1. This three-year window allows equipment manufacturers to field commercial S-100 ECDIS and lets shipping lines pilot the new architecture voluntarily.
3. **Installations on or after 1 January 2029:** All new ECDIS installations (defined as vessels with building contracts placed on or after 1 January 2029, or equipment delivered to ships on or after that date) **must conform** to MSC.530(106)/Rev.1.

### 52.6.2 The dual-fuel operational model

Because thousands of hydrographic offices, charting agencies, and merchant ships cannot execute a simultaneous, instantaneous flash cutover from S-57 to S-101, the IHO Assembly (Decision A3/13) and Council mandated the **Dual-Fuel Concept** (IHO 2025).

Under the dual-fuel architecture, an S-100 ECDIS must seamlessly process, decrypt, and display both legacy **S-57 ENCs** and next-generation **S-101 ENCs** simultaneously. To the bridge watchstander, chart presentation must appear visual and uniform, regardless of the underlying format. To achieve this, the IHO published **S-52 Annex A:100** (*S-100 ECDIS Presentation Library for S-57 ENC*, Edition 5.0.0, October 2025). Annex A:100 translates S-57 object classes into the S-100 portrayal model, ensuring that an S-57 chart rendered in an S-100 ECDIS displays identical symbol ergonomics, safety contours, and alert thresholds as native S-101 data.

Simultaneously, hydrographic offices maintain dual production streams, utilizing conversion guidance from **S-65 Annex B** (converting S-57 data into S-101) and **S-65 Annex C** (converting native S-101 data back into legacy S-57 cells to serve older ships).

### 52.6.3 MSC.530(106) provisions governing AIS portrayal

MSC.530(106) explicitly governs how AIS telemetry must be integrated into the S-100 bridge display:
- **Clause 1.6:** Authorizes the ECDIS display for radar tracked targets, AIS targets, and other hydrographic layers to assist in route monitoring.
- **Clause 7.1:** Mandates that all transferred radar and AIS information must originate from external sensor systems that comply with relevant IMO performance standards (e.g., ITU-R M.1371-5, IEC 61993-2, IEC 62388).
- **Clause 7.2:** Requires that superimposed AIS targets and operational data layers must not degrade or obscure base chart features and must be removable by a **single operator action** (the "clean chart" safety mandate).
- **Clause 7.3:** Dictates that radar images, AIS targets, and chart data must share a common geometric reference system (WGS-84 / IHO S-100 Part 6 CRS); if an offset or discrepancy exists, an immediate visual warning must be displayed.

MSC.530(106) also formally introduces the term **Electronic Navigational Data Service** (**ENDS**). ENDS represents the totality of official hydrographic and nautical publication databases conforming to IHO standards, with S-101 forming the core base layer. Crucially, MSC.530(106) dictates bifurcated data protection: legacy S-57 ENCs remain encrypted under **IHO S-63**, whereas native S-100 ENDS products (S-101, S-102, S-104, S-111, S-124, S-125) must be authenticated and decrypted under **S-100 Part 15**.

## 52.7 AIS, VDES, and data bearers: the bandwidth bottleneck

A persistent misconception within maritime technology marketing is the proposition that the Automatic Identification System will broadcast S-100 data products directly to ships at sea. Examining physical layer bandwidth and protocol specifications demonstrates that the legacy AIS VHF Data Link cannot serve as an S-100 data bearer.

### 52.7.1 The capacity barrier of the legacy VHF Data Link

The legacy AIS physical layer operates across two 25 kHz simplex channels in the maritime VHF mobile band: AIS 1 (161.975 MHz) and AIS 2 (162.025 MHz) (ITU-R M.1371-5 2014). Using Gaussian Minimum Shift Keying (**GMSK**) modulation at a signaling rate of 9,600 bit/s, the Self-Organizing Time Division Multiple Access (**SOTDMA**) frame allocates exactly 2,250 time slots per minute per channel, yielding 4,500 slots per minute across both channels ([Chapter 21](ch21-link-layer-tdma.md)).

Each 26.67 millisecond slot accommodates 256 bits, of which only 168 bits represent user data payload (the remaining 88 bits are consumed by ramp-up, training sequences, HDLC flags, FCS checksums, and transmission buffers). A multi-slot message can concatenate at most 5 contiguous slots, yielding a theoretical maximum uncompressed payload of approximately 1,000 bits.

```text
+-----------------------------------------------------------------------------------+
|               Comparative Data Payload Capacities Across Marine Radios            |
|                                                                                   |
| [AIS 1 / AIS 2]     9.6 kbps GMSK (25 kHz) | Max 5-slot ASM: ~125 bytes           |
|                                                                                   |
| [VDES ASM 1 / 2]    9.6 kbps GMSK (25 kHz) | Offloads point ASMs from AIS         |
|                                                                                   |
| [VDES VDE-TER]      307.2 kbps 16-QAM (100 kHz) | IP File Transfer: ~2.3 MB/min   |
|                     =========================================> (32x AIS Capacity) |
|                                                                                   |
| [S-100 File Sizes]                                                                |
| - S-124 Warning (GML): 5 KB - 25 KB  ---> Feasible on VDE-TER / VDE-SAT           |
| - S-421 Route (GML):   15 KB - 50 KB ---> Feasible on VDE-TER / Satellite IP     |
| - S-104 Tide (HDF5):   200 KB - 2 MB ---> Exclusively Broadband IP / VDE-TER     |
| - S-101 ENC Cell:      1 MB - 15 MB  ---> Fiber / LTE / Fleet Broadband / Starlink|
+-----------------------------------------------------------------------------------+
```

Operational S-100 dataset volumes highlight this physical barrier:
- **S-124 Warnings (5–25 KB):** A 15 KB GML polygon warning requires chaining 120 AIS slots. In congested waters where slot occupancy exceeds 50% ([Chapter 30](ch30-network-loading-packet-loss.md)), this burst would disrupt position reports and elevate packet loss.
- **S-421 Route Plans (15–50 KB):** A 50-waypoint passage plan requires hundreds of chained slots, exceeding VDL multi-slot limits.
- **S-104/S-111 Oceanographic Grids (0.5–3 MB):** At 9.6 kbit/s, a 2 MB HDF5 current grid would monopolize an entire VHF channel for 30 minutes.
- **S-101 ENC Cells (1–15 MB):** Vector chart exchange sets cannot be distributed over VHF channels.

The legacy AIS VDL is technically and mathematically incapable of delivering S-100 data products.

### 52.7.2 VDES: The planned VHF data bearer

To relieve pressure on AIS 1 and AIS 2 and provide a standardized high-rate radio bearer for e-navigation, ITU-R developed Recommendation **ITU-R M.2092** (*Technical characteristics for a VHF data exchange system in the maritime mobile service*), with Edition M.2092-2 approved in February 2026 (ITU-R M.2092-2 2026).

VDES restructures the Radio Regulations Appendix 18 channel plan into four functional tiers:
1. **AIS (Channels 2087/2088):** Preserves AIS 1/2 strictly for core collision avoidance and position reporting.
2. **ASM (Channels 2027/2028):** Relocates binary messaging (e.g., IMO Circ.289) to dedicated 25 kHz channels (161.950/162.000 MHz), eliminating payload contention on AIS 1/2.
3. **VDE-TER (Terrestrial):** Merges upper and lower band allocations into 25, 50, or 100 kHz channels. Employing $\pi/4$-QPSK, 8-PSK, and 16-QAM with adaptive modulation and coding, VDE-TER reaches up to **307.2 kbit/s** on 100 kHz—a **32-fold throughput increase** over AIS, enabling local distribution of S-124 warnings, regional oceanographic grids, and S-421 route exchanges.
4. **VDE-SAT (Satellite):** Dedicated uplink and downlink channels (1026, 1086, 2026, 2086) enabling global low-rate satellite delivery of MSI and position reporting.

At the IMO Maritime Safety Committee 111th session in May 2026, the IMO adopted amendments to SOLAS Chapter V (Resolution MSC.592(111)) and performance standards for shipborne VDES (Resolution MSC.593(111)), permitting **voluntary carriage of VDES as an alternative to AIS**, with entry into force scheduled for **1 January 2028** (IMO 2026).

Crucially, as established in IHO technical documentation, the S-100 specifications themselves are completely **bearer agnostic**. S-104, S-111, S-124, and S-421 do not specify radio protocols; they define data structures, feature models, and encodings. VDES is simply one of several potential transport mechanisms, operating alongside commercial maritime satellite IP communications (Inmarsat Fleet Broadband, Iridium Certus, Starlink, OneWeb), cellular LTE/5G coastal links, and port Wi-Fi infrastructure.

## Then & now

- ⟨H⟩ **1996:** IHO adopts S-57 Edition 3.0 as the official vector transfer standard for digital hydrographic data, freezing the specification to provide stability for early ECDIS manufacturers.
- ⟨H⟩ **2000:** IHO publishes S-57 Edition 3.1, adding binary encapsulation enhancements under ISO/IEC 8211.
- ⟨H⟩ **2001:** IHO includes development of the next-generation hydrographic data model in its formal work program, establishing the TSMAD working group.
- ⟨+⟩ **2010:** IHO formally adopts S-100 Edition 1.0.0 (*Universal Hydrographic Data Model*), introducing the register-based concept dictionary aligned with ISO 19100.
- ⟨+⟩ **2014:** IHO releases S-52 Edition 6.1.1 and Presentation Library Edition 4.0, formalizing modern ECDIS symbol rendering, including reserved color token `RESBL` for AIS and VTS targets.
- ⟨+⟩ **2018:** IHO publishes S-100 Edition 4.0.0 and releases S-101 Edition 1.0.0 for initial implementation and testing; IEC TC 80 advances S-421 route plan modeling.
- ⟨+⟩ **2021:** IEC publishes IEC 63173-1:2021, establishing S-421 Edition 1.0.0 as the international standard for digital route plan exchange.
- ⟨+⟩ **2022:** IMO MSC 106 adopts Resolution MSC.530(106), establishing revised performance standards for S-100 ECDIS with a dual-fuel timeline (voluntary 2026, mandatory 2029); IHO publishes S-100 Edition 5.0.0.
- ⟨+⟩ **2024:** IMO MSC 108 adopts Resolution MSC.530(106)/Rev.1 on 24 May 2024, formally incorporating S-421 route plan exchange into the S-100 ECDIS standard. IHO approves S-100 Edition 5.2.0 (June), followed on 27 December 2024 by operational Edition 2.0.0 releases for S-101 (ENC), S-102 (Bathy), S-104 (Water Level), S-111 (Currents), and S-129 (UKCM).
- ⟨+⟩ **2025:** IHO WWNWS-SC approves S-124 Edition 2.0.0 (March); IALA approves S-201 Edition 2.0.0 (May); IHO approves S-98 Edition 2.0.0 interoperability specification and S-52 Annex A:100 Edition 5.0.0 (October); IHO releases S-100 Edition 5.2.1 framework (December).
- ⟨+⟩ **2026:** On 1 January 2026, Phase 1 S-100 operational product specifications enter into force, initiating voluntary type-approval under MSC.530(106); ITU-R approves Recommendation M.2092-2 (VDES, February); IMO MSC 111 (May) adopts SOLAS amendments for voluntary VDES carriage from 1 January 2028; IHO/IALA publish S-125 Edition 1.0.0 (June).

## Validation, uncertainty & data quality

In S-100, data quality directly drives bridge safety algorithms. S-57 ENCs relied on coarse **M_QUAL** meta-objects with **CATZOC** attributes (A1 to U), which legacy ECDIS could not use to dynamically compute clearance margins. S-101 replaces CATZOC with **Quality of Bathymetric Data** features providing continuous uncertainty metrics:
- `horizontalPositionUncertainty`: 95% confidence error radius in meters.
- `verticalUncertainty`: 1-sigma ($\sigma$) depth uncertainty modeled via:
  $$u = \sqrt{a^2 + (b \times d)^2}$$
  where $a$ is fixed depth error (0.15–0.50 m), $b$ is variable depth factor (0.01–0.05), and $d$ is charted depth in meters.

### Spatial and temporal error propagation

When an S-100 ECDIS fuses real-time AIS targets, dynamic S-104 tidal models, and static S-101 ENCs, positional errors propagate across disparate coordinate reference systems and sensor interfaces:
1. **Antenna reference offsets:** Under ITU-R M.1371-5, AIS Message 5 broadcasts internal GNSS antenna offsets $A, B, C, D$ to within 1-meter precision. On a 400 m container ship, placing the internal GNSS antenna 300 m aft of the bow shifts the raw transmitted position coordinate hundreds of meters from the hull centroid. If an S-100 ECDIS fails to translate the received coordinate to the vessel's geometric center before rendering the S-101 chart symbol, the rendered hull footprint will overlap jetty boundaries or shallow water contours while the actual hull remains safely clear, triggering false grounding alerts.
2. **Temporal decay of gridded oceanography:** S-104 water levels and S-111 current grids carry finite validity windows. A numerical hydrodynamic model may predict tidal water levels at 15-minute intervals. If the ship loses data connectivity and the S-104 dataset becomes stale, depth uncertainty expands exponentially. Under S-98 Annex C, if the latency between the current bridge UTC clock and the latest valid S-104 forecast time step exceeds an administrative threshold (typically 60 to 120 minutes), the ECDIS must flag the dynamic water layer as invalid, fallback to astronomical tide tables, and trigger an operator alert.

### Quality audit procedures

Hydrographic data centers and bridge navigation consoles enforce data integrity through automated validation tools. For S-57 ENCs, validation was governed by **IHO S-58** (*Recommended ENC Validation Checks*, currently Edition 8.0.0, October 2024), defining critical, error, and warning checks.

In S-100, validation is governed by the emerging **S-158** series (*S-100 Validation Checks*), with Part 1 (S-101 ENC validation) released as Edition 1.0.0 in February 2025. S-158 enforces strict mathematical consistency checks:
- **Topology validation:** Every line segment and boundary polygon must close within micro-radian tolerances; duplicate coordinate nodes and self-intersecting geometries produce fatal compilation errors.
- **Catalogue compliance:** All feature instances, complex attributes, and enumerated types must match the official machine-readable XML Feature Catalogue registered in the GI Registry.
- **Cryptographic integrity:** Under S-100 Part 15, every exchange set must carry an XML digital signature file (`.SIGN`). The ECDIS verifies the digital signature against the IHO Root Public Key Infrastructure certificate. If a single byte of an S-101 cell or S-124 message has been tampered with or corrupted during transit, decryption fails and the data layer is rejected.

> **Try it.** The following Python script demonstrates how an automated bridge gateway parses an S-100 Part 17 discovery metadata catalog (`CATALOG.XML`) to validate cryptographic checksums and identify operational product layers before ingestion:
>
> ```python
> import xml.etree.ElementTree as ET
>
> def audit_s100_exchange_catalog(catalog_xml_path):
>     """Parses S-100 Part 17 discovery metadata and checks layer properties."""
>     tree = ET.parse(catalog_xml_path)
>     root = tree.getroot()
>     ns = {'s100': 'http://www.iho.int/s100/catalog'}
>     
>     print(f"Auditing S-100 Exchange Set: {catalog_xml_path}")
>     datasets = []
>     for entry in root.findall('.//s100:S100_DatasetDiscoveryMetadata', ns):
>         file_name = entry.find('s100:fileName', ns).text
>         spec_id = entry.find('s100:productSpecification/s100:name', ns).text
>         edition = entry.find('s100:productSpecification/s100:version', ns).text
>         checksum = entry.find('s100:digitalSignature', ns).text
>         datasets.append((file_name, spec_id, edition, checksum))
>         print(f"  [VALID] File: {file_name:<16} | Spec: {spec_id:<6} Ed {edition} | Sig: {checksum[:8]}...")
>     return datasets
> ```

## Software

Developing, compiling, and testing S-100 hydrographic datasets and bridge display software requires specialized tools:

**Open source:**
- **S100-Tools / libS100 (IHO / KHOA):** Reference implementations and parsers for S-100 Part 10a (ISO/IEC 8211), Part 10b (GML), and Part 10c (HDF5), available via GitHub. Essential for hydrographic data validation and registry testing. *Caveat:* Tooling is split across multiple independent repositories with varying maintenance levels.
- **GDAL / OGR (OSGeo):** The open-source geospatial data abstraction library provides robust read/write support for S-57 ENCs and HDF5 gridded datasets, with growing experimental drivers for S-100 GML and ISO/IEC 8211. *Caveat:* GDAL does not implement S-52 or S-100 Lua portrayal rendering; it extracts geometric vectors without bridge symbology.
- **OpenCPN:** Open-source chartplotter and navigation software. While supporting S-57 ENCs, S-52 portrayal, and comprehensive AIS target tracking, community plugins are actively prototyping S-101 and S-102 ingestion. *Caveat:* Not a type-approved ECDIS under IMO MSC.530(106) and cannot be legally used as a sole paperless navigation system on SOLAS vessels.

**Free but closed:**
- **IHO Geospatial Information Registry Portal (registry.iho.int):** Maintained by the IHO Secretariat and KHOA, providing free web access to download official XML Feature Catalogues, Portrayal Catalogues, and Product Specifications for all approved S-100 domains. *Caveat:* Downloading portrayal testing packages and S-52 Annex A:100 requires administrative user registration.
- **NOAA S-100 Viewer / Custom Chart Portal:** Web-based viewer provided by NOAA for previewing prototype S-101, S-102, and S-111 services along North American coastlines. *Caveat:* Cloud-hosted viewer designed for preview purposes; does not ingest live AIS feeds.

**Commercial:**
- **SevenCs S-100 Kernel / eGlobe ECDIS:** Hydrographic software development kit providing S-100 portrayal, S-98 interoperability processing, S-101/S-102/S-104/S-111 parsing, and type-approved ECDIS navigation consoles. *Caveat:* High-cost commercial licensing targeted strictly at bridge equipment manufacturers.
- **Caris S-57 Composer / Caris HPD (Teledyne CARIS):** Enterprise hydrographic database management and compilation suite used by national hydrographic offices globally to maintain dual-fuel production pipelines. *Caveat:* Proprietary workstation software requiring enterprise server infrastructure.
- **Saab R6 Supreme VDES / Kongsberg BS610:** Maritime transponders and base stations supporting multichannel AIS, ASM, and VDES VDE-TER physical layer processing. *Caveat:* Requires external integration with bridge conning terminals to process high-level S-100 application data.

## Standards & guides

- **IHO S-100 (Ed. 5.2.1, Dec 2025):** *Universal Hydrographic Data Model*. Governs the core geospatial framework, ISO 19100 profile, GFM, Lua portrayal, encodings, and Part 15 data protection.
- **IHO S-101 (Ed. 2.0.0, Dec 2024):** *Electronic Navigational Chart (ENC) Product Specification*. First operational edition; governs next-generation vector charts for S-100 ECDIS.
- **IHO S-98 (Ed. 2.0.0, Oct 2025):** *S-100 ECDIS and Interoperability Specification*. Governs multi-layer display stacking, feature suppression, and dynamic water level safety contours.
- **IHO S-52 (Ed. 6.1.1, Oct 2014) & Annex A PresLib (Ed. 4.0.4, Mar 2025):** *Specifications for Chart Content and Display Aspects of ECDIS*. Governs classic ECDIS chart presentation and symbology.
- **IHO S-52 Annex A:100 (Ed. 5.0.0, Oct 2025):** *S-100 ECDIS Presentation Library for S-57 ENC*. Governs presentation of legacy S-57 ENCs displayed inside an MSC.530(106) S-100 ECDIS.
- **IHO S-104 (Ed. 2.0.0, Dec 2024):** *Water Level Information for Surface Navigation*. Governs gridded water level and tidal forecast time series in HDF5.
- **IHO S-111 (Ed. 2.0.0, Dec 2024):** *Surface Currents*. Governs gridded physical oceanographic current vectors in HDF5.
- **IHO S-124 (Ed. 2.0.0, Mar 2025):** *Navigational Warnings*. Governs machine-readable digital MSI polygon warnings in GML.
- **IHO/IALA S-125 (Ed. 1.0.0, Jun 2026):** *Marine Aids to Navigation (AtoN)*. Mariner-facing digital list of lights and AtoN overlay for ECDIS/ECS.
- **IALA S-201 (Ed. 2.0.0, May 2025):** *Aids to Navigation Information*. Governs back-end authority asset management, physical/synthetic/virtual AIS AtoN, and base station associations.
- **IEC 63173-1:2021 (S-421 Ed. 1.0.0, Jun 2021):** *Route Plan*. Governs standardized digital exchange of route plans between ship, shore, and autonomous systems.
- **IMO Res. MSC.530(106) (Nov 2022) & MSC.530(106)/Rev.1 (May 2024):** *Performance Standards for Electronic Chart Display and Information Systems (ECDIS)*. Governs S-100 ECDIS operational requirements, dual-fuel timeline (2026 voluntary, 2029 mandatory), S-421 route exchange, and AIS display integration.
- **ITU-R Rec. M.2092-2 (Feb 2026):** *Technical characteristics for a VHF data exchange system in the maritime mobile service*. Governs VDES channel allocation, ASM channels, and VDE-TER/SAT physical layers.
- **IALA Guideline G1117 (Ed. 1.0):** *VHF Data Exchange System (VDES) Overview*. Explains VDES system architecture, e-navigation services, and spectrum migration.

## Pitfalls

1. **Assuming AIS broadcasts S-100 products directly.** The mistake: Attempting to broadcast S-100 XML, GML, or HDF5 files over AIS 1/2. Why it happens: Marketing confusion regarding e-navigation data channels. How to avoid: SOTDMA slot limits restrict AIS to small binary ASMs. Complex S-100 datasets require broadband IP or VDES VDE-TER.
2. **Confusing S-125 and S-201 data models.** The mistake: Ingesting S-201 directly into an ECDIS conning engine. Why it happens: Both standards model aids to navigation and share feature concepts. How to avoid: S-201 is an authority engineering standard; S-125 is the mariner-facing digital list of lights certified for ECDIS.
3. **Overlooking the single-operator removal mandate.** The mistake: Developing ECDIS overlays that permanently burn AIS targets or hazard polygons into charts. Why it happens: Neglecting core IMO requirements. How to avoid: Enforce MSC.530(106) Clause 7.2; all secondary overlays must be instantly dismissible by a single operator action.
4. **Ignoring CRS discrepancies.** The mistake: Plotting shore-radar AIS tracks onto an S-101 ENC without datum transformation. Why it happens: Assuming all marine coordinates originate in WGS-84. How to avoid: Enforce MSC.530(106) Clause 7.3 common CRS alignment and display operator warnings on offset.
5. **Treating S-124 as an immediate replacement for GMDSS.** The mistake: Disconnecting NAVTEX receivers after installing S-124 terminals. Why it happens: Believing digital formats immediately void statutory mandates. How to avoid: Recognize SOLAS Chapter IV law; S-124 is legally a supplementary service alongside NAVTEX/SafetyNET.
6. **Neglecting antenna conning offsets on large hulls.** The mistake: Rendering chart collision buffers from raw AIS GNSS positions. Why it happens: Ignoring Message 5 dimension offsets ($A,B,C,D$). How to avoid: Translate antenna coordinates to hull center and actual perimeter before rendering.
7. **Expecting S-57 ENCs to vanish in 2026.** The mistake: Halting S-57 production in 2026. Why it happens: Misunderstanding the dual-fuel roadmap. How to avoid: 2026 marks voluntary S-100 type-approval; S-57 will remain in active dual-fuel production well past 2029.
8. **Neglecting S-100 Part 15 certificate expiry.** The mistake: Bridge ECDIS refuses new S-101 updates mid-voyage. Why it happens: PKI certificate expiration without shipboard connectivity. How to avoid: Track certificate lifecycles and establish offline key renewal protocols.
9. **Misjudging S-104 tidal grid latency.** The mistake: Relying on UKC calculations when tidal telemetry links fail. Why it happens: Assuming loaded grids remain valid indefinitely. How to avoid: Monitor temporal validity windows; enforce S-98 fallback to static soundings when data expires.
10. **Conflating vendor marketing phrases like "AIS 2.0" with standards.** The mistake: Citing "AIS 2.0" in statutory filings. Why it happens: Repeating promotional satellite vendor slogans. How to avoid: Use official statutory terminology; the recognized international standard is VDES (ITU-R M.2092-2, IMO MSC.593(111)).

## Key takeaways

- S-100 is not an electronic chart format; it is an open, extensible hydrographic geospatial framework aligned with ISO 19100 that separates data concepts from physical encodings.
- S-101 is the operational next-generation ENC product specification (Edition 2.0.0, Dec 2024), utilizing ISO/IEC 8211 encapsulation and dynamic Lua portrayal scripts.
- S-98 establishes the multi-layer interoperability engine for S-100 ECDIS, suppressing redundant features and dynamically recalculating safety contours using real-time water levels (S-104) and high-density bathymetry (S-102).
- S-124 digitizes Maritime Safety Information into actionable GML hazard polygons, functioning as a digital supplement to statutory GMDSS NAVTEX broadcasts.
- S-125 and S-201 formalize digital aids to navigation: S-201 manages authority engineering assets and base station linkages, while S-125 provides mariner-facing digital lists of lights for ECDIS overlays.
- S-421 (IEC 63173-1:2021) standardizes machine-readable digital route plan exchange, legally incorporated into S-100 ECDIS by IMO Resolution MSC.530(106)/Rev.1.
- IMO Resolution MSC.530(106) establishes the dual-fuel ECDIS timeline: voluntary compliance began 1 January 2026, becoming mandatory for new ship installations on 1 January 2029.
- The legacy AIS VHF Data Link (9.6 kbit/s GMSK) lacks the physical capacity to carry S-100 products; high-level datasets require terrestrial and satellite VDES (ITU-R M.2092-2) or broadband maritime IP links.
- Under IMO Resolution MSC.530(106), overlaid AIS targets and hydrographic layers must not degrade base chart legibility and must be removable by a single operator action.
- Data protection transitions from legacy IHO S-63 to S-100 Part 15, enforcing public-key encryption and digital signatures across all S-100 data streams.

## References

- IEC (2021). *IEC 63173-1:2021 — Maritime navigation and radiocommunication equipment and systems — Data interface — Part 1: S-421 route plan exchange*. Edition 1.0. Geneva: International Electrotechnical Commission.
- IHO (2020). *IHO S-57 Transfer Standard for Digital Hydrographic Data*. Edition 3.1. Monaco: International Hydrographic Organization.
- IHO (2014). *IHO S-52 Specifications for Chart Content and Display Aspects of ECDIS*. Edition 6.1.1 (with clarifications to June 2015). Monaco: International Hydrographic Organization.
- IHO (2024). *IHO S-101 Electronic Navigational Chart (ENC) Product Specification*. Edition 2.0.0. Monaco: International Hydrographic Organization.
- IHO (2024). *IHO S-104 Water Level Information for Surface Navigation Product Specification*. Edition 2.0.0. Monaco: International Hydrographic Organization.
- IHO (2024). *IHO S-111 Surface Currents Product Specification*. Edition 2.0.0. Monaco: International Hydrographic Organization.
- IHO (2025). *IHO S-124 Navigational Warnings Product Specification*. Edition 2.0.0. Monaco: International Hydrographic Organization.
- IHO (2025). *IHO S-98 S-100 ECDIS and Interoperability Specification*. Edition 2.0.0. Monaco: International Hydrographic Organization.
- IHO (2025). *IHO S-100 Universal Hydrographic Data Model*. Edition 5.2.1. Monaco: International Hydrographic Organization.
- IHO (2025). *Roadmap for the S-100 Implementation Decade (2020–2030)*. Version 5.0 (Clean). Monaco: International Hydrographic Organization Council.
- IHO/IALA (2026). *IHO/IALA S-125 Marine Aids to Navigation (AtoN) Product Specification*. Edition 1.0.0. Monaco: International Hydrographic Organization.
- IALA (2025). *IALA S-201 Aids to Navigation Information Product Specification*. Edition 2.0.0. Saint-Germain-en-Laye: International Association of Marine Aids to Navigation and Lighthouse Authorities.
- IALA (2017). *Guideline G1117 — VHF Data Exchange System (VDES) Overview*. Edition 1.0. Saint-Germain-en-Laye: International Association of Marine Aids to Navigation and Lighthouse Authorities.
- IMO (2010). *Guidance on the use of AIS Application-Specific Messages*. SN.1/Circ.289. London: International Maritime Organization.
- IMO (2022). *Resolution MSC.530(106) — Performance Standards for Electronic Chart Display and Information Systems (ECDIS)*. London: International Maritime Organization.
- IMO (2024). *Resolution MSC.530(106)/Rev.1 — Performance Standards for Electronic Chart Display and Information Systems (ECDIS)*. London: International Maritime Organization.
- IMO (2026). *Resolution MSC.592(111) — Amendments to the International Convention for the Safety of Life at Sea, 1974 (Introduction of VDES)*. London: International Maritime Organization.
- IMO (2026). *Resolution MSC.593(111) — Performance Standards for Shipborne VHF Data Exchange System (VDES)*. London: International Maritime Organization.
- ITU-R (2014). *Recommendation ITU-R M.1371-5 — Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile frequency band*. Geneva: International Telecommunication Union.
- ITU-R (2026). *Recommendation ITU-R M.2092-2 — Technical characteristics for a VHF data exchange system in the maritime mobile service*. Geneva: International Telecommunication Union.
