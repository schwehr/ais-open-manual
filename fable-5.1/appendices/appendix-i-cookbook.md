# Appendix I — "Try it" cookbook

This appendix serves as the definitive, executable code recipe reference for *The AIS Handbook*. All scripts referenced across the handbook chapters reside in the repository's `code/` directory and are actively tested against synthetic test corpora in CI. Each entry in this cookbook pairs a script with a one-paragraph recipe describing its operational objective and engineering context, exact command invocation, and verified expected standard output.

---

## I.1 Recipe index

The companion codebase provides runnable solutions spanning bitstream decoding, RF link-budget calculation, discrete-event TDMA simulation, kinematic anomaly detection, spatial analytics, and 3D visualization.

### Table I.1: The AIS Handbook Code Recipes

| Recipe Script | Primary Domain | Chapter Context | External Dependencies | Input Data / Arguments |
|---|---|---|---|---|
| `code/decode/tagblock.py` | Sentence Parsing | [Chapter 24](../chapters/ch24-timing.md), [Chapter 26](../chapters/ch26-interfaces-and-logging.md), [Chapter 42](../chapters/ch42-home-receiver.md) | Standard library | Pipe raw NMEA text via stdin |
| `code/decode/compare_decoders.py` | Multi-Decoder Audit | [Chapter 22](../chapters/ch22-message-catalog.md), [Chapter 44](../chapters/ch44-open-source-decoders-history.md) | `pyais`, `libais` | Sample NMEA file path |
| `code/rf/linkbudget.py` | RF Link Engineering | [Chapter 27](../chapters/ch27-rf-basics.md), [Chapter 32](../chapters/ch32-antennas.md), [Chapter 37](../chapters/ch37-shore-collection-siting.md), [Chapter 38](../chapters/ch38-collection-at-sea.md) | Standard library (`math`) | Power, antenna gains, heights, range |
| `code/rf/propagation_compare.py` | Empirical RF Validation | [Chapter 29](../chapters/ch29-propagation-modeling.md) | `pyais` | NMEA log, receiver coordinates |
| `code/rf/gmsk_demo.py` | Physical Layer DSP | [Chapter 28](../chapters/ch28-rf-encoding-physical-layer.md), [Chapter 34](../chapters/ch34-rf-forensics-fingerprinting.md) | `numpy` | Target SNR, samples-per-symbol, output path |
| `code/tdma/sotdma_sim.py` | Protocol Simulation | [Chapter 21](../chapters/ch21-link-layer-tdma.md), [Chapter 30](../chapters/ch30-network-loading-packet-loss.md), [Chapter 61](../chapters/ch61-timing-and-network-attacks.md) | Standard library (`random`, `collections`) | Vessel counts, reporting intervals, sweep flag |
| `code/analytics/make_samples.py` | Corpus Generation | [Chapter 43](../chapters/ch43-demonstration-programs.md), [Chapter 47](../chapters/ch47-data-quality-track-reconstruction.md) | `pyais` | Output files in `data/samples/` |
| `code/analytics/coverage_estimate.py` | Sensor Auditing | [Chapter 48](../chapters/ch48-spatial-statistics.md) | `pyais` | NMEA log, receiver location, ground truth CSV |
| `code/analytics/duckdb_density.py` | Spatial Grid Aggregation | [Chapter 2](../chapters/ch02-uses-of-ais-data.md), [Chapter 48](../chapters/ch48-spatial-statistics.md), [Chapter 50](../chapters/ch50-big-data-architecture.md) | `duckdb`, `pyais` | NMEA log, receiver coordinates, display limit |
| `code/analytics/moving_pandas_pipeline.py` | Trajectory Reconstruction | [Chapter 45](../chapters/ch45-processing-software.md), [Chapter 47](../chapters/ch47-data-quality-track-reconstruction.md) | `pandas`, `geopandas`, `movingpandas`, `pyais` | NMEA log, optional output parquet path |
| `code/security/kinematic_checks.py` | Anomaly / Spoof Triage | [Chapter 12](../chapters/ch12-2015-to-present.md), [Chapter 57](../chapters/ch57-autonomous-ships.md), [Chapter 59](../chapters/ch59-spoofing.md), [Chapter 62](../chapters/ch62-gnss-jamming-spoofing.md) | `pyais` | NMEA log, receiver coordinates |
| `code/viz/blender_ais_animation.py` | Kinematic 3D Animation | [Chapter 45](../chapters/ch45-processing-software.md), [Chapter 56](../chapters/ch56-vdr-forensics.md) | `bpy` (optional CLI mode without `bpy`) | Ground truth CSV, blend output, render frame |
| `code/viz/blender_coverage_satpass.py` | Orbital Pass Visualization | [Chapter 39](../chapters/ch39-satellite-ais.md), [Chapter 48](../chapters/ch48-spatial-statistics.md) | `bpy` (optional CLI mode without `bpy`) | Optional `.blend` scene output |
| `code/figures/make_figures.py` | Vector Figure Generation | [Chapter 1](../chapters/ch01-what-ais-is.md), [Chapter 21](../chapters/ch21-link-layer-tdma.md), [Chapter 28](../chapters/ch28-rf-encoding-physical-layer.md), [Chapter 30](../chapters/ch30-network-loading-packet-loss.md) | Standard library | Generates SVGs into `figures/chNN/` |

---

## I.2 Protocol decoding and interface recipes

### Recipe 1: NMEA 4.10 TAG block parsing and formatting (`code/decode/tagblock.py`)

NMEA 4.10 TAG blocks provide standardized sentence-level encapsulation for line-reception timestamps, source station identifiers, sentence grouping tokens, and line counts preceding raw `!AIVDM`/`!AIVDO` payloads ([Chapter 26](../chapters/ch26-interfaces-and-logging.md)). The script `code/decode/tagblock.py` implements a zero-dependency parser and serializer that validates the mandatory XOR checksum between enclosing backslashes, extracts UNIX timestamps (`c:` parameter in seconds or milliseconds), source station tags (`s:`), destination identifiers (`d:`), and grouping tokens (`g:`), returning structured `TagBlock` records alongside isolated payload sentences.

```bash
echo '\s:BOS_TWR,n:42,c:1768478400*15\!AIVDM,1,1,,A,15MwpU@01prtlJ0H9J@<Can00000,0*25' | python code/decode/tagblock.py
```

Expected output:
```text
TagBlock(unix_time=1768478400.0, destination=None, group=None, line_count=42, relative_time=None, source='BOS_TWR', text=None, checksum_ok=True, raw='s:BOS_TWR,n:42,c:1768478400*15') !AIVDM,1,1,,A,15MwpU@01prtlJ0H9J@<Can00000,0*25
```

### Recipe 2: Multi-engine cross-decoder auditing (`code/decode/compare_decoders.py`)

Production data processing pipelines frequently encounter malformed, proprietary, or non-standard NMEA sentences where divergent decoder implementations yield conflicting results or silent payload drops ([Chapter 44](../chapters/ch44-open-source-decoders-history.md)). The script `code/decode/compare_decoders.py` ingests an identical NMEA corpus and executes concurrent decoding across `pyais`, `libais`, and `gpsdecode` (when installed on the host system PATH), cataloging total decoded sentences, breakdown by ITU-R M.1371 message type, and identifying bitstream boundary discrepancies such as multi-sentence reassembly variations.

```bash
python code/decode/compare_decoders.py data/samples/synthetic_harbor.nmea
```

Expected output:
```text
2019 sentences
pyais      decoded 1986 messages by type {1: 1130, 4: 361, 5: 33, 18: 361, 21: 41, 24: 60}
libais     decoded 1953 messages by type {1: 1130, 4: 361, 18: 361, 21: 41, 24: 60}
gpsdecode  not available
```

---

## I.3 Radio frequency and physical layer recipes

### Recipe 3: Radio horizon and link-budget evaluation (`code/rf/linkbudget.py`)

Evaluating coastal base station placement and vessel tracking performance requires rigorous line-of-sight and link-budget calculations parameterized for maritime VHF frequencies (161.975 MHz and 162.025 MHz) ([Chapter 27](../chapters/ch27-rf-basics.md), [Chapter 37](../chapters/ch37-shore-collection-siting.md)). The script `code/rf/linkbudget.py` calculates the effective 4/3-Earth refracted radio horizon ($d = 4.12 \cdot (\sqrt{h_1} + \sqrt{h_2})\text{ km}$), free-space path loss (FSPL), and flat-sea two-ray ground reflection loss, evaluating received power ($P_{\text{rx}}$) and operating link margin against standard Class A receiver sensitivity thresholds ($-107\text{ dBm}$).

```bash
python code/rf/linkbudget.py
```

Expected output:
```text
radio horizon for h_tx=30.0 m, h_rx=50.0 m: 51.7 km (27.9 nmi)
 d_km  d_nmi  FSPL  2-ray  used   Prx_dBm  margin
    5    2.7  90.6   84.4   90.6    -47.1    59.9
   10    5.4  96.6   96.5   96.6    -53.2    53.8
   20   10.8 102.7  108.5  108.5    -65.1    41.9
   30   16.2 106.2  115.6  115.6    -72.1    34.9
   40   21.6 108.7  120.6  120.6    -77.1    29.9
   50   27.0 110.6  124.4  124.4    -81.0    26.0
   60   32.4 112.2  127.6  127.6    -84.1    22.9
   80   43.2 114.7  132.6  132.6    -89.1    17.9
  100   54.0 116.6  136.5  136.5    -93.0    14.0
```

Executing a point-to-point calculation for a specific geometry ($P_{\text{tx}} = 12.5\text{ W}$, $G_{\text{tx}} = 2.15\text{ dBi}$, $G_{\text{rx}} = 3.0\text{ dBi}$, $h_{\text{tx}} = 30\text{ m}$, $h_{\text{rx}} = 50\text{ m}$, $d = 30\text{ km}$):

```bash
python code/rf/linkbudget.py --ptx 12.5 --gtx 2.15 --grx 3.0 --htx 30 --hrx 50 --d 30
```

Expected output:
```text
{'d_km': 30.0, 'd_nmi': 16.198704103671705, 'fspl_db': 106.2, 'two_ray_db': 115.6, 'loss_used_db': 115.6, 'p_rx_dbm': -71.9, 'margin_vs_-107dBm': 35.1, 'horizon_km': 51.7}
```

### Recipe 4: Empirical vs theoretical path-loss comparison (`code/rf/propagation_compare.py`)

Validating real-world coastal receiver performance demands reconciling empirical packet reception rates against deterministic electromagnetic propagation models ([Chapter 29](../chapters/ch29-propagation-modeling.md)). The script `code/rf/propagation_compare.py` ingests a raw NMEA log, computes geodesic distances between transmitting Class A vessels and receiver coordinates, bins observed packet reception rates against reporting intervals, and aligns them directly with free-space and two-ray path loss predictions to diagnose receiver shadowing, co-channel interference, or degraded antenna performance.

```bash
python code/rf/propagation_compare.py data/samples/synthetic_harbor.nmea --rx 42.36 -70.95
```

Expected output:
```text
radio horizon (h_tx=20.0 m, h_rx=30.0 m): 22.1 nmi
 range_nmi   p_obs   Prx_fspl  Prx_2ray  margin_2ray  note
    0–5       0.60     -46.5     -47.6        59.4  
    5–10      0.70     -56.0     -66.7        40.3  
   10–15      0.73     -60.5     -75.5        31.5  
   15–20      0.64     -63.4     -81.4        25.6  
   20–25      0.32     -65.6     -85.8        21.2  margin ok but poor reception: shadowing/noise/antenna?
   25–30      0.27     -67.3     -89.2        17.8  margin ok but poor reception: shadowing/noise/antenna?
   30–35      0.16     -68.8     -92.1        14.9  
```

### Recipe 5: GMSK burst synthesis and coherent demodulation (`code/rf/gmsk_demo.py`)

Understanding physical layer demodulation in software-defined radios requires inspecting bit stuffing, NRZI encoding, Gaussian pre-modulation filtering ($BT = 0.4$ or $0.3$), FM modulation, and non-coherent/coherent bit slicing ([Chapter 28](../chapters/ch28-rf-encoding-physical-layer.md), [Chapter 34](../chapters/ch34-rf-forensics-fingerprinting.md)). The script `code/rf/gmsk_demo.py` provides a pure NumPy physical-layer synthesis and demodulation pipeline that constructs a standard 256-bit TDMA burst, inserts the 24-bit training sequence, applies CRC-16-CCITT framing, transmits over an AWGN baseband channel, and demodulates the baseband samples to verify bit error rates and CRC validity.

> **Legal note.** `code/rf/gmsk_demo.py` emits complex baseband sample arrays to memory or binary disk files only (`.cf32`/`.npy`). It must never be connected to physical radio transmitters without competent regulatory licensing and type certification.

```bash
python code/rf/gmsk_demo.py --snr-db 20
```

Expected output:
```text
burst bits=235 (slot budget 256), SNR=20.0 dB, raw BER=0.0000, CRC ok=True
```

---

## I.4 Link layer and TDMA simulation recipes

### Recipe 6: SOTDMA slot reservation and CSTDMA starvation simulation (`code/tdma/sotdma_sim.py`)

The self-organizing TDMA protocol synchronizes maritime transmissions into 2,250 slots per minute per channel, where Class A transceivers negotiate slot allocations up to eight frames in advance, while Class B CSTDMA units must carrier-sense the channel immediately prior to transmission ([Chapter 21](../chapters/ch21-link-layer-tdma.md), [Chapter 30](../chapters/ch30-network-loading-packet-loss.md)). The script `code/tdma/sotdma_sim.py` implements a discrete-event simulator modeling nominal slot selection, candidate slot intervals, carrier-sense contention windows, intentional slot reuse, and synthetic slot jamming. Running with `--sweep` reproduces the canonical channel saturation curve where Class B deferrals skyrocket before Class A packet collisions emerge.

```bash
python code/tdma/sotdma_sim.py --sweep
```

Expected output:
```text
n_A  occupancy  A_loss  B_defer
  50  0.100     0.000   0.000
 100  0.168     0.000   0.000
 200  0.327     0.000   0.000
 300  0.487     0.000   0.051
 400  0.637     0.024   0.319
 500  0.724     0.157   0.549
 600  0.774     0.305   0.687
```

A baseline run with default parameters ($n_A = 100$, $n_B = 25$):

```bash
python code/tdma/sotdma_sim.py
```

Expected output:
```text
{'a_tx': 985, 'a_collided': 0, 'b_tx': 280, 'b_deferred': 0, 'slots_used': 1265, 'slots_jammed': 0, 'occupancy': 0.112, 'a_loss_rate': 0.0, 'b_defer_rate': 0.0}
```

---

## I.5 Data engineering and spatial analytics recipes

### Recipe 7: Synthetic harbor corpus generation (`code/analytics/make_samples.py`)

Reproducible benchmarking of AIS decoding, data cleaning, and kinematic verification algorithms requires public test datasets with completely known ground truth free of copyright, proprietary, or licensing encumbrances ([Chapter 43](../chapters/ch43-demonstration-programs.md), [Chapter 47](../chapters/ch47-data-quality-track-reconstruction.md)). The script `code/analytics/make_samples.py` programmatically generates a multi-vessel harbor scenario spanning 60 minutes across Boston Harbor, synthesizing TAG-blocked NMEA `!AIVDM` sentences across ITU Messages 1, 4, 5, 18, 21, and 24 alongside an exact per-report ground truth CSV ledger with known anomalous transmitters (MMSI 0, invalid MID 1193046, and speed outliers).

```bash
python code/analytics/make_samples.py
```

Expected output:
```text
wrote 2019 sentences, 1802 truth rows
```

### Recipe 8: Detection probability and sensor coverage estimation (`code/analytics/coverage_estimate.py`)

Empirical coastal sensor coverage maps cannot be constructed from raw message counts alone due to severe spatial sampling biases induced by traffic bottlenecks and speed-dependent reporting intervals ([Chapter 48](../chapters/ch48-spatial-statistics.md)). The script `code/analytics/coverage_estimate.py` processes raw NMEA streams to compute dynamic vessel reporting expectations based on ITU-R M.1371 Speed Over Ground (SOG) intervals (e.g., 10 s for 0–14 kn, 6 s for 14–23 kn, 2 s for $>23\text{ kn}$), comparing expected report counts against observed messages per range bin to derive rigorous detection probability curves ($P_{\text{detect}}$) both with and without ground truth CSV data.

```bash
python code/analytics/coverage_estimate.py data/samples/synthetic_harbor.nmea --rx 42.36 -70.95 --truth data/samples/synthetic_harbor_truth.csv
```

Expected output:
```text
range_bin_nmi  vessel_min  observed  expected  p_detect
       0–5           11        66       110      0.60
       5–10          44       259       372      0.70
      10–15          60       360       492      0.73
      15–20          47       256       402      0.64
      20–25          27        86       270      0.32
      25–30          33        89       330      0.27
      30–35           9        14        90      0.16

against truth: range_bin  truth_reports  received  p_true
       0–5           65        65     1.00
       5–10         261       261     1.00
      10–15         354       354     1.00
      15–20         287       261     0.91
      20–25         160        86     0.54
      25–30         232        89     0.38
      30–35          82        14     0.17

Note: the expected-vs-observed estimate is biased upward when vessels enter/leave a minute bin, and downward when the SOG-based interval is wrong (e.g., status 'at anchor' not set). Report both.
```

### Recipe 9: Coverage-normalized vessel density mapping with DuckDB (`code/analytics/duckdb_density.py`)

Visualizing maritime traffic density using raw AIS message frequency severely distorts vessel distribution by over-representing slow-moving craft near base stations while obscuring fast vessels operating at the receiver horizon ([Chapter 2](../chapters/ch02-uses-of-ais-data.md), [Chapter 50](../chapters/ch50-big-data-architecture.md)). The script `code/analytics/duckdb_density.py` utilizes embedded DuckDB SQL queries to bin decoded AIS records into a $0.02^\circ$ spatial grid, calculate geodesic range to the collection receiver, compute empirical detection probability decay, and normalize raw report tallies into reception-corrected traffic indices.

```bash
python code/analytics/duckdb_density.py data/samples/synthetic_harbor.nmea --rx 42.36 -70.95 --limit 5
```

Expected output:
```text
 cell_lat  cell_lon  reports  vessels  range_nmi  p_detect  reports_corrected
    42.28    -70.74       47        2       10.6      1.00               47.0
    42.28    -70.72       42        2       11.5      1.00               42.0
    42.24    -70.68       39        1       14.0      1.00               39.0
    42.26    -70.70       38        1       12.8      1.00               38.0
    42.20    -70.62       35        1       17.6      0.87               40.0
```

### Recipe 10: End-to-end trajectory cleaning and stop detection (`code/analytics/moving_pandas_pipeline.py`)

Translating raw, noisy AIS telemetric streams into research-grade vessel trajectories requires rigorous syntactic filtering, deduplication, speed-gating, coordinate validation, and spatio-temporal segmentation ([Chapter 45](../chapters/ch45-processing-software.md), [Chapter 47](../chapters/ch47-data-quality-track-reconstruction.md)). The script `code/analytics/moving_pandas_pipeline.py` executes an end-to-end Python pipeline using `pyais`, `pandas`, `geopandas`, and `movingpandas`, stripping invalid MMSIs (e.g., MMSI 0 or unassigned MIDs), filtering speed outliers ($>60\text{ kn}$), assembling continuous `TrajectoryCollection` objects, extracting vessel movement metrics, and detecting stationary stops ($\ge 5\text{ min}$ within $200\text{ m}$).

```bash
python code/analytics/moving_pandas_pipeline.py data/samples/synthetic_harbor.nmea
```

Expected output:
```text
cleaning report: {'position_reports': 1491, 'after_mmsi_filter_and_dedupe_and_speed': 1343, 'dropped': 148, 'vessels': 6}
6 trajectories
  mmsi=244999703 fixes=126 length_km=26.5 start=12:00:46 end=12:59:56 mean_sog_reported=14.5 kn mean_speed_derived=14.5 kn
  mmsi=316999704 fixes=301 length_km=37.1 start=12:00:09 end=12:59:59 mean_sog_reported=20.0 kn mean_speed_derived=20.1 kn
  mmsi=338123456 fixes=121 length_km=11.1 start=12:00:00 end=13:00:00 mean_sog_reported=6.0 kn mean_speed_derived=6.0 kn
  mmsi=338654321 fixes=120 length_km=13.8 start=12:00:20 end=12:59:50 mean_sog_reported=7.5 kn mean_speed_derived=7.5 kn
  mmsi=338999702 fixes=349 length_km=33.3 start=12:00:03 end=12:59:43 mean_sog_reported=18.0 kn mean_speed_derived=18.1 kn
  mmsi=366999701 fixes=326 length_km=22.3 start=12:00:00 end=13:00:00 mean_sog_reported=12.0 kn mean_speed_derived=12.0 kn
0 stops (>=5 min within 200 m)
```

---

## I.6 Maritime security and kinematic anomaly recipes

### Recipe 11: Multi-metric kinematic and coverage plausibility triage (`code/security/kinematic_checks.py`)

Automated detection of maritime GNSS spoofing, identity cloning, and transponder tampering requires evaluating multiple physical layers simultaneously rather than relying on isolated threshold alerts ([Chapter 12](../chapters/ch12-2015-to-present.md), [Chapter 59](../chapters/ch59-spoofing.md), [Chapter 62](../chapters/ch62-gnss-jamming-spoofing.md)). The script `code/security/kinematic_checks.py` applies a rule-based triage heuristic across four kinematic checks: implied speed between consecutive position reports exceeding hull-class limits, SOG-vs-implied speed mismatches, unphysical turn rates, spatial teleportation jumps, receiver footprint horizon violations, and ITU Table 1 invalid MMSI structures.

```bash
python code/security/kinematic_checks.py data/samples/synthetic_harbor.nmea --rx 42.36 -70.95
```

Expected output:
```text
     mmsi  score  fixes  speed_violations  max_implied_kn  sog_mismatch  turn_violations  teleports  beyond_range  max_range_nmi  invalid_mmsi
        0      1     28                 0       12.031859             0                0          0             0      16.324760             1
  1193046      1    120                 0        4.517441             0                0          0             0       5.134594             1
244999703      0    126                 0       14.544945             0                0          0             0      32.674542             0
316999704      0    301                 0       20.051188             0                0          0             0      26.229610             0
338123456      0    121                 0        6.018214             0                0          0             0       7.653746             0
338654321      0    120                 0        7.515078             0                0          0             0      12.274265             0
338999702      0    349                 0       18.043446             0                0          0             0      19.489121             0
366999701      0    326                 0       12.053396             0                0          0             0      18.276030             0

score >= 2 deserves a second look; score alone never proves spoofing.
```

---

## I.7 Visualization and reproduction recipes

### Recipe 12: 3D trajectory reconstruction with Blender (`code/viz/blender_ais_animation.py`)

Maritime accident investigation, VDR casualty reconstruction, and port operational reviews benefit substantially from 3D kinematic visualization with correctly scaled hull geometries ([Chapter 45](../chapters/ch45-processing-software.md), [Chapter 56](../chapters/ch56-vdr-forensics.md)). The script `code/viz/blender_ais_animation.py` ingests trajectory CSV logs, reprojects geographic WGS84 coordinates into an equirectangular Euclidean metric coordinate frame centered on the scenario origin, generates scaled box proxies reflecting vessel dimensions (from Message 5 static data), and animates keyframed translations and heading rotations. The script runs seamlessly in headless CLI mode when executed without `bpy` to validate track ingestion parameters.

```bash
python code/viz/blender_ais_animation.py --csv data/samples/synthetic_harbor_truth.csv
```

Expected output:
```text
bpy not available — run inside Blender. Parsed 8 tracks; origin (42.29832586015538, -70.64818942286348)
```

When executed within a complete Blender 4.x environment:

```bash
blender --background --python code/viz/blender_ais_animation.py -- \
    --csv data/samples/synthetic_harbor_truth.csv --out /tmp/ais_anim.blend --render /tmp/ais_frame.png
```

### Recipe 13: Satellite orbital pass and coverage footprint simulation (`code/viz/blender_coverage_satpass.py`)

Visualizing Low Earth Orbit (LEO) Satellite AIS collection requires understanding the geometric relationship between instantaneous sub-satellite footprints and terrestrial line-of-sight collection discs ([Chapter 39](../chapters/ch39-satellite-ais.md), [Chapter 48](../chapters/ch48-spatial-statistics.md)). The script `code/viz/blender_coverage_satpass.py` computes Earth-curvature radio horizons for shore receivers and constructs the dynamic field-of-view footprint circle for a satellite at 600 km altitude ($R_{\text{footprint}} \approx 2,663\text{ km}$), animating orbital passes and terrestrial coverage boundaries. In CLI mode without Blender installed, it outputs exact analytical horizon figures.

```bash
python code/viz/blender_coverage_satpass.py
```

Expected output:
```text
receiver horizon 47.6 km; satellite footprint radius 2663 km at 600 km altitude
bpy not available — numbers only.
```

When executed within Blender:

```bash
blender --background --python code/viz/blender_coverage_satpass.py -- --out /tmp/satpass.blend
```

### Recipe 14: Automated reproducible SVG figure generation (`code/figures/make_figures.py`)

Technical handbooks require exact alignment between text equations, simulation parameters, and vector illustrations ([Chapter 1](../chapters/ch01-what-ais-is.md), [Chapter 21](../chapters/ch21-link-layer-tdma.md), [Chapter 28](../chapters/ch28-rf-encoding-physical-layer.md)). The script `code/figures/make_figures.py` regenerates all eleven vector diagrams directly into `figures/chNN/`, executing exact TDMA slot allocation formulas, GMSK burst bit allocations, free-space and two-ray path loss curves, VHF spectrum channel adjacent boundaries, and orbital satellite coverage geometries.

```bash
python code/figures/make_figures.py
```

Expected output:
```text
wrote .../figures/ch01/system-overview.svg
wrote .../figures/ch21/slot-map.svg
wrote .../figures/ch28/burst-structure.svg
wrote .../figures/ch27/path-loss.svg
wrote .../figures/ch27/radio-horizon.svg
wrote .../figures/ch31/spectrum-adjacency.svg
wrote .../figures/ch30/saturation.svg
wrote .../figures/ch39/footprint.svg
wrote .../figures/ch48/coverage-curve.svg
wrote .../figures/ch12/timeline.svg
wrote .../figures/ch42/signal-chain.svg
```

---

## References

- Balduzzi, M., Pasta, A. & Wilhoit, K. (2014). A Security Evaluation of AIS Automated Identification System. *Proceedings of the 30th Annual Computer Security Applications Conference* (ACSAC '14), 436–445. New York: ACM. doi:10.1145/2664243.2664257.
- Blender Online Community (2026). *Blender 4.x Reference Manual*. Amsterdam: Blender Foundation. URL: https://docs.blender.org/manual/en/latest/ (accessed 2026-10-06).
- Graser, A. (2019). MovingPandas: Efficient Analysis of Movement Data in Python. *GI_Forum*, 7(1):54–68. doi:10.1553/giscience2019_01_s54.
- International Electrotechnical Commission (2016). *Maritime navigation and radiocommunication equipment and systems – Digital interfaces – Part 1: Single talker and multiple listeners* (Standard No. IEC 61162-1:2016). Geneva: IEC.
- International Telecommunication Union (2014). *Technical characteristics for an automatic identification system using time division multiple access in the VHF maritime mobile band* (Recommendation ITU-R M.1371-5). Geneva: ITU Radiocommunication Sector.
- National Marine Electronics Association (2012). *Standard for Interfacing Marine Electronic Devices* (NMEA 0183 Version 4.10). Severna Park: NMEA.
- Raasveldt, M. & Mühleisen, H. (2024). *DuckDB: An in-process SQL OLAP database management system*. URL: https://duckdb.org (accessed 2026-10-06).
- Raymond, E. S. & Schwehr, K. (2023). *AIVDM/AIVDO Protocol Decoding* (Version 1.58). GPSD Project. URL: https://gpsd.gitlab.io/gpsd/AIVDM.html (accessed 2026-10-06).
- Richter, L. M. (2026). *pyais: Pure Python AIS Message Decoding and Encoding Library* (Version 3.3.0). URL: https://github.com/M0r13n/pyais (accessed 2026-10-06).
- Schwehr, K. (2018). *libais: C++ and Python Automatic Identification System Decoding Library* (Version 0.17). URL: https://github.com/schwehr/libais (accessed 2026-10-06).
- Seybold, J. S. (2005). *Introduction to RF Propagation*. Hoboken: John Wiley & Sons.
