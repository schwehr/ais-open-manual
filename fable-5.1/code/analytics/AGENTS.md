# `code/analytics/`

Worked analytics examples for "The AIS Handbook", an open, citable handbook on
the maritime Automatic Identification System. The scripts here back the
data-processing chapters (cleaning, trajectories, receiver coverage estimation
and coverage-normalised density maps; chapters 45, 47, 48 and 50 are cited in
the docstrings) and the generator for the repository's redistributable
synthetic sample data set.

Everything operates on `data/samples/synthetic_harbor.nmea` (TAG-blocked
`!AIVDM` sentences) and its companion `data/samples/synthetic_harbor_truth.csv`,
both produced by `make_samples.py`. The scripts depend on the TAG-block parser in
`code/decode/tagblock.py` and on third-party libraries (`pyais`, `pandas`,
`numpy`, `geopandas`, `movingpandas`, `duckdb`).

## Files

| File | Summary |
|---|---|
| `make_samples.py` | Generates the fully synthetic 60-minute harbour-approach scenario (2026-01-15 12:00Z near 42.35N, -70.9W): 4 Class A ships (Msg 1 every 10 s, Msg 5 every 6 min), 3 Class B craft (Msg 18 every 30 s, Msg 24 A/B every 6 min), 1 base station (Msg 4 every 10 s) and 2 AtoN (Msg 21 every 3 min), encoded with `pyais.encode.encode_dict` and wrapped in `\s:SYNTH01,c:<unix>*hh\` TAG blocks. Writes `data/samples/synthetic_harbor.nmea` and `synthetic_harbor_truth.csv` (`mmsi,time,lat,lon,sog,cog,heading,class`). Seeds `random` with 1371. |
| `moving_pandas_pipeline.py` | Raw NMEA → decoded table → cleaned → MovingPandas trajectories → stops. Exposes `decode_file()` (pyais `FileReaderStream`, receiver time from TAG block `c:`), `clean()` (keeps types 1/2/3/18/19/27, drops `INVALID_MMSI` = {0, 1193046, 123456789, 111111111, 999999999}, out-of-range lat/lon, duplicates, and fixes implying > 60 kn), and `trajectories()` (`TrajectoryCollection` keyed by MMSI, speed in kn). Optional second argument writes the cleaned positions to parquet. |
| `coverage_estimate.py` | Empirical receiver detection-probability curve vs range ("expected vs observed"): for each Class A vessel-minute, expected reports come from the ITU-R M.1371 SOG-dependent interval (10 s ≤14 kn, 6 s ≤23 kn, 2 s above, 180 s at anchor/moored); observed/expected summed per range bin (default 5 nmi). `--truth` compares received counts against the truth CSV. Prints a bias caveat at the end. |
| `duckdb_density.py` | DuckDB SQL density map: bins positions (types 1/2/3/18/19, excluding MMSI 0 and 1193046) on a 0.02° grid, counts reports and distinct vessels, and divides by a range-based detection-probability model (1 inside 15 nmi, linear to 0 at 35 nmi, floored at 0.05) to produce `reports_corrected`. Prints the top `--limit` cells (default 15). |

## Notes for agents

- Run from the repository root; the usage lines in each docstring assume that,
  e.g. `python code/analytics/coverage_estimate.py data/samples/synthetic_harbor.nmea --rx 42.36 -70.95`.
  `make_samples.py` resolves the repo root as `parents[2]` of its own path and
  writes into `data/samples/`.
- Import chain: `coverage_estimate.py` and `duckdb_density.py` insert their own
  directory on `sys.path` and import `decode_file` from
  `moving_pandas_pipeline.py`, which in turn inserts `../decode` on `sys.path`
  and imports `parse_line` from `tagblock.py`. Renaming or moving any of these
  breaks the others.
- The receiver is at (42.36, -70.95), 30 m, which is also the base station
  position (MMSI 3669712). Pass it as `--rx 42.36 -70.95` to the coverage and
  density scripts.
- The soft-coverage model in `make_samples.received()` (p = 1 inside 15 nmi,
  linear to 0 at 35 nmi) is deliberately mirrored in the `p_detect` expression
  in `duckdb_density.py`'s SQL and is what `coverage_estimate.py` is meant to
  recover; keep them consistent if you change one. The SQL comment notes the
  model should be replaced by a measured curve for real data.
- Intentional data-quality defects in the sample: ship 366999701 transmits
  MMSI 0 for seconds 600–899, and one Class B unit uses the default MMSI
  1193046. `clean()` and the DuckDB query filter these out; the truth CSV
  records the MMSI actually transmitted (0 during the defect window).
- `coverage_estimate.py` only uses Class A position reports (types 1–3) and
  does not call `clean()`, so the MMSI-0 reports count toward the curve.
- `duckdb_density.py` relies on DuckDB's replacement scan of the local Python
  variable `df`; the `# noqa: F841` is intentional—do not "fix" the unused
  variable.
- `moving_pandas_pipeline.py` globally suppresses warnings and wraps stop
  detection in a try/except so a missing/incompatible `movingpandas` only
  skips that step.
- There are no tests in this directory; `code/tests/` exists at the sibling
  level. Verify changes by regenerating samples and running the three analysis
  scripts end to end.
