# `book/00-front-matter` — Directory Guide for Agents

## Overview
This directory contains the front-matter reference documents for *Automatic Identification System (AIS): The Open Manual*. It establishes the foundational terminology, historical timeline, and mathematical/engineering conventions used consistently across all eight parts and forty chapters of the manual.

## Subdirectories
None. This is a leaf directory under `book/`.

## Files in This Directory

- **`acronyms-and-glossary.md`**
  - Comprehensive A–Z glossary defining more than 150 maritime, RF, GNSS, hydrographic, protocol, analytics, and cybersecurity terms and acronyms.
  - Covers core AIS and VDES protocol entities (`AIVDM`/`AIVDO`, `ASM`, `CSTDMA`, `FATDMA`, `ITDMA`, `RATDMA`, `SOTDMA`, `DAC`, `FI`, `MMSI`, `MID`, `ROT`, `SOG`, `COG`, `HDG`), physical-layer RF engineering (`GMSK`, `BT`, `LNA`, `SAW`, `VSWR`, `SINAD`), navigation & charting (`ARPA`, `CPA`/`TCPA`, `ECDIS`, `ENC`, `IHO S-52/S-57/S-63/S-100`, `VDR`, `VTS`), 3D forensic visualization (`Blender`, `bpy`, `ENU`), open-source software (`libais`, `AIS-catcher`, `rtl_ais`, `MovingPandas`), maritime trade analytics (`BMAP`, `TPC`, `DWT`), and RF/cyber intelligence (`EAIS`, `SEI`, `SIC`, `TDOA`/`FDOA`, `SS7`/`Diameter`).

- **`ais-and-gis-history-timeline.md`**
  - Chronological master timeline (~206 BCE to 2028+) tracing the co-evolution of maritime navigation, radio engineering, geographic information systems (GIS), and the Automatic Identification System.
  - Synthesizes historical records from `schwehr/gis-history`, Kimbra Cutlip's Global Fishing Watch history, USCG Jorge Arroyo archives, and ITU/IMO/IALA/IEC standards across six eras:
    1. **Era I (~206 BCE – 1799):** Ancient celestial/magnetic navigation, Mercator projection (1569), and John Harrison's H1–H4 marine chronometers (1730–1761).
    2. **Era II (1800 – 1945):** Bowditch (1802), wireless telegraphy, the *RMS Titanic* disaster (1912) and first SOLAS Convention (1914), marine radar, and WWII hyperbolic TDOA radionavigation chains (Gee, Decca, LORAN-A/C).
    3. **Era III (1946 – 1987):** Shannon information theory (1948), IALA foundation (1957), Cesium-133 atomic clocks & UTC (1972), GPS Block I (1978) & GLONASS (1982), NMEA 0183 (1983), and WGS84 (1984).
    4. **Era IV (1988 – 2000):** Håkan Lans's Swedish STDMA patent `SE 8803166` (1988), the *Exxon Valdez* grounding (1989) and US Oil Pollution Act of 1990 (OPA-90), the 1990s prototype wars (UK 4S DSC polling vs. Panama Canal CTAN vs. Swedish/Finnish SOTDMA), ITU-R M.1371-0 (1998), termination of GPS Selective Availability (May 2000), and IMO SOLAS Chapter V Regulation 19 mandatory AIS carriage adoption (December 2000).
    5. **Era V (2001 – 2015):** Post-9/11 pivot to maritime domain awareness (MTSA 2002, USCG NAIS), Blender GPL open-source release (2002) and UNH/CCOM 3D maritime visualization (`noaadata` + `Blender`), USPTO March 30, 2010 reexamination cancelling all 19 claims of Lans's US Patent 5,506,587, the April 2010 *Deepwater Horizon* disaster and Kurt Schwehr's creation of C++/Python `libais`, orbital Satellite AIS (S-AIS), and ITU-R M.2092-0 VDES (2015).
    6. **Era VI (2016 – 2028+):** USCG 2016 Final Rule, Global Fishing Watch launch (2016), MovingPandas/GeoParquet/DuckDB analytics, the *Ever Given* Suez grounding (2021), Paolo et al. *Nature* global SAR dark-vessel study (2024), the *MV Dali* Francis Scott Key Bridge collapse (March 2024), IALA's transition to an Intergovernmental Organization (August 2024), and the IHO S-100 & SOLAS VDES phase-in (2026–2028).

- **`notation-and-conventions.md`**
  - Defines the strict mathematical, bit-indexing, RF, and coordinate-frame conventions enforced throughout the manual and its accompanying test suite:
    1. **Bit Ordering & Indexing:** Distinguishes over-the-air HDLC LSB-first byte transmission (with bit-stuffing) from unpacked NMEA 0183 `!AIVDM` 6-bit MSB-first bit vectors, and provides side-by-side 0-based (`libais`/`pyais`) and 1-based (`ITU-R M.1371`) bit interval notation.
    2. **Integer Encoding, Scaling & Sentinels:** Formalizes unsigned (`uintW`) and two's complement signed (`intW`) extraction equations, physical scaling factors, and mandatory ITU-R M.1371 "not available" sentinel values (`181.0°` longitude, `91.0°` latitude, `1023` SOG, `3600` COG, `511` HDG, `-128` ROT, `60–63` UTC second, `0` draught) that must be filtered before spatial or kinematic calculations.
    3. **RF & Electromagnetic Conventions:** Standardizes logarithmic power ($\text{dBW}$ vs. $\text{dBm}$), isotropic vs. dipole antenna gain ($\text{dBi} = \text{dBd} + 2.15\text{ dB}$), impedance mismatch/VSWR equations, and the $25\text{ kHz}$ AIS channel thermal noise floor ($-130.0\text{ dBm}$ at $290\text{ K}$).
    4. **Coordinate Reference Frames:** Specifies WGS84 (`EPSG:4326`), Local Tangent Plane East-North-Up (ENU) projection (essential to prevent IEEE 754 `float32` vertex jitter in Blender `bpy` 3D scenes), and the 2D/3D rigid-body transformation from GNSS antenna reference point offsets ($A, B, C, D$) to the geometric hull center.
