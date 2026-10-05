# Authoring & Technical Style Guide: The Maritime Automatic Identification System (AIS) Handbook

## 1. Purpose and Audience
This handbook is designed to serve simultaneously as:
1. **An Accessible Operational Reference** for mariners, Vessel Traffic Services (VTS) operators, search-and-rescue planners, and maritime policy analysts.
2. **A Deep Engineering & Mathematical Reference** for RF/DSP engineers, embedded hardware designers, open-source software developers (`libais`, `gpsd`, `pyais`, Rust parsers, `MovingPandas`, `Blender`), spatial statisticians, and cybersecurity researchers.

## 2. Mandatory 8-Part Chapter Structure
Every chapter (`ch01` through `ch30`) MUST include the following eight structural components (adapted naturally to the chapter's domain):
1. **Operational & Conceptual Overview:** Clear, jargon-decoded introduction explaining *what* the subsystem does, *why* it exists, and how mariners, engineers, and analysts interact with it.
2. **Historical Context & Evolution (`schwehr/gis-history` Integration):** Chronological lineage connecting early navigation, geodesy, radio physics, computing, and maritime casualties to modern AIS standards and open-source software milestones.
3. **Deep Technical & Mathematical Foundations:** Explicit equations, bit-width tables, link-budget derivations, state-machine Mermaid diagrams, or statistical estimators.
4. **Hardware, Standards, & Software Ecosystem:** Specific ITU-R, IMO, IEC, IALA, IHO, RTCM, and NMEA clauses alongside open-source and proprietary implementations.
5. **Security, Adversarial Abuse, & Failure Modes:** Real-world hardware degradation, software parser vulnerabilities, operator pitfalls, RF interference, or spoofing/jamming attack vectors.
6. **Practical Engineering / Code Walkthrough:** Complete, runnable code examples (Python, C++, Rust, DuckDB SQL, Blender `bpy`, or Linux/SDR configuration files).
7. **Key Takeaways & Operational Checklist:** Concise engineering and operational verification checklist.
8. **Cited References & Primary Sources:** Full bibliographic citations with URLs/DOIs, court citations, patent numbers, and standard identifiers.

## 3. Mathematical, Bit-Level, and Geodetic Conventions
* **Bit Indexing:** Always specify whether bit indices are **0-based MSB-first** (`libais` and `gpsd` `AIVDM.txt` convention, where a 1-slot message spans bits `0..167`) or **1-based MSB-first** (ITU-R M.1371 tables, `1..168`). Over the air (HDLC), bytes are transmitted LSB-first, whereas unpacked 6-bit NMEA ASCII payloads are concatenated MSB-first.
* **Signed Integer Fields:** All signed integers in ITU-R M.1371 (e.g., 28-bit Longitude, 27-bit Latitude, 8-bit Rate of Turn) use **standard two's complement**. Always state the "not available" sentinel value explicitly (e.g., `181.0°` = `0x6791AC0` for Longitude; `91.0°` = `0x3412140` for Latitude; `-128` = `0x80` for ROT).
* **RF Units:** Distinguish clearly between isotropic gain ($\text{dBi}$) and dipole-relative gain ($\text{dBd}$), where:
  $$\text{Gain (dBi)} = \text{Gain (dBd)} + 2.15\text{ dB}$$
* **Coordinate Systems:** Raw AIS positions are referenced to **WGS84** ($\lambda, \phi$). When performing metric geometry, spatial statistics, or 3D visualization in **Blender**, always project into an appropriate equal-area CRS or centered local tangent plane (**East-North-Up [ENU]**) to eliminate cosine-latitude distortion and single-precision `float32` vertex jitter.
