# AGENTS.md — `tests`

## Directory Overview
The `tests/` directory contains the automated Python `unittest` verification suite for *AIS: An Open Manual* (`TASK-801` through `TASK-803` plus repository-wide structural integrity checks). These tests validate both the structural completeness of all 40 chapters, 8 appendices, task backlogs, and BibTeX citations, as well as the core mathematical and bit-level algorithms taught in the book.

## Subdirectories
None (this is a leaf directory).

## Files in This Directory

### 1. `test_blender_ais_rigging.py`
- **Purpose:** Unit tests for 3D Blender (`bpy`) AIS casualty reconstruction and scene engineering (`TASK-803`; see Chapters 4, 23, and 25).
- **Key Functions & Test Cases:**
  - `geodetic_to_enu(lon_deg, lat_deg, h_m, lon0_deg, lat0_deg, h0_m)` & `to_float32(val)`: Transforms WGS84 coordinates into a local tangent-plane East-North-Up (ENU) frame and proves that while raw UTM coordinates (`~4,700,000.0 m`) suffer a complete `0.0 m` quantization stall under a $0.15\text{ m}$ displacement in IEEE 754 `float32`, centered ENU coordinates preserve $<0.0001\text{ m}$ accuracy (`test_float32_jitter_mitigation_with_local_enu`).
  - `compute_hull_antenna_rigging(to_bow, to_stern, to_port, to_starboard)` & `hull_point_enu(...)`: Computes overall length (`LOA`), `beam`, and geometric hull-center offset `(dx_center, dy_center)` from the GNSS antenna reference point (`A, B, C, D`), verifying that a $400\text{ m}$ ULCS container ship (`to_bow=350m, to_stern=50m`) turning $30^\circ$ in yaw sweeps its bow $175.0\text{ m}$ laterally even when the GNSS antenna position remains stationary (`test_antenna_offset_bow_sweep_during_turn`).
  - `compute_crabbing_leeway_deg(cog_deg, true_heading_deg)`: Tests signed $360^\circ$ wraparound crabbing/leeway angles (`COG - True Heading` in `[-180°, +180°]`) across $0^\circ / 360^\circ$ North (`test_crabbing_angle_wraparound`).

### 2. `test_book_integrity.py`
- **Purpose:** End-to-end repository integrity and completeness test suite (`TestBookIntegrity`).
- **Key Test Cases:**
  - `test_all_tasks_checked_off_in_tasks_md`: Verifies that `../TASKS.md` exists, has `0` unchecked tasks (`- [ ]`), and has all `80` tasks checked off (`- [x]`).
  - `test_all_book_readme_links_resolve`: Parses all relative markdown links in `../book/README.md` ($\ge 54$ links) and asserts that every target file exists on disk and exceeds $1,000\text{ bytes}$.
  - `test_all_40_chapters_and_8_appendices_exist_and_substantial`: Verifies that all `40` chapters (`book/part*/ch*.md`) exist, each contains $\ge 450\text{ lines}$ and fenced code/diagram blocks, and all `8` appendices (`book/appendices/appendix-*.md`) exist and exceed $10,000\text{ characters}$.
  - `test_master_bibliography_bibtex_and_appendix_h_parity`: Extracts all BibTeX keys ($\ge 80$ entries) from `../MASTER_BIBLIOGRAPHY.bib` and verifies 100% parity with `../book/appendices/appendix-h-master-bibliography.md`.

### 3. `test_nmea_and_bit_decoding.py`
- **Purpose:** Unit tests for NMEA 0183 framing, TAG blocks, 6-bit ASCII armor, two's-complement bit slicing, non-linear Rate of Turn (`ROT`), IMO modulo-10 check digits, and HDLC CRC-16 / bit-stuffing (`TASK-801`; see Chapters 7, 13, 14, 15, and 31).
- **Key Functions & Test Cases:**
  - `nmea_checksum`, `verify_nmea_sentence`, `armor_to_bits`, `bits_to_armor`, `extract_uint`, `extract_int`: Validates a canonical USCG NAIS TAG-block-wrapped `!AIVDM` Message 1 sentence (`\s:uscg-nais,c:1711430000*59\!AIVDM,1,1,,B,15M67FC000G?ufbE`FepT@3n00Sa,0*5C`), round-trips its 168-bit payload, decodes MMSI `366053209` and San Francisco Bay coordinates (`-122.341618°, 37.802118°`), and verifies two's-complement sentinels (`181.0° = 0x6791AC0` and `91.0° = 0x3412140`).
  - `decode_rot_ais_to_deg_per_min` & `encode_deg_per_min_to_rot_ais`: Verifies the ITU-R M.1371 non-linear square-root formula $\text{ROT}_{\text{AIS}} = \text{round}(4.733\sqrt{|\omega|})$ and its `-128` (`None`) and `±127` (`±inf`) sentinels.
  - `validate_imo_number`: Verifies the 7-digit IMO ship identification number modulo-10 check-digit rule (`IMO9074729` and *Ever Given* `9811000`).
  - `crc16_ccitt_ais`, `hdlc_bit_stuff`, & `hdlc_bit_unstuff`: Computes the 16-bit HDLC FCS (`0x1021`, init `0xFFFF`, inverted), enforces zero-insertion after five consecutive `1` bits so `"111111"` never occurs in the payload, and verifies lossless unstuffing.

### 4. `test_trajectory_spatial_stats.py`
- **Purpose:** Unit tests for continuous-time trajectory spatial statistics and Horvitz-Thompson inverse-detection-probability weighting (`TASK-802`; see Chapter 26).
- **Key Functions & Test Cases:**
  - `integrate_segment_grid_residence` & `accumulate_trajectory_residence`: Numerically integrates vessel residence time (in vessel-seconds) across a 2D equal-area grid (`cell_size = 1000.0 m`) and proves that two vessels crossing the exact same $1,000\text{ m}$ cell at $10\text{ m/s}$ ($100\text{ s}$ duration) at different reporting intervals ($\Delta t = 2\text{ s}$ [51 pings] vs. $\Delta t = 25\text{ s}$ [5 pings]) suffer a $10\times$ bias under naive ping counting but yield an identical $100.0\text{ vessel-seconds}$ under continuous trajectory integration (`test_reporting_rate_invariance_vs_naive_ping_bias`).
  - `horvitz_thompson_vessel_hours`: Implements the Horvitz-Thompson estimator $\hat{T}(c) = \sum (\Delta t_{\text{nom}} / (p_{\text{RF}} \cdot p_{\text{VDL}}))$ and verifies exact recovery of $3,600.0\text{ vessel-seconds}$ when $p_{\text{RF}} = 0.8$ and $p_{\text{VDL}} = 0.5$ (`p_det = 0.4`, `test_horvitz_thompson_packet_loss_correction`).
