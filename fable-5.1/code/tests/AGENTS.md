# `code/tests/`

Smoke tests for the runnable code snippets that accompany "The AIS Handbook",
an open, citable handbook on the maritime Automatic Identification System.
The handbook ships worked examples under `code/` (decoding, analytics, RF link
budgets, GMSK modulation, SOTDMA simulation, security checks, Blender
visualisation), and this directory holds the single pytest module that
exercises them end to end against the synthetic sample data in
`data/samples/`.

The tests are deliberately lightweight: they import a few library-style
modules directly and run the rest as command-line scripts via `subprocess`,
asserting on exit codes and on a handful of expected strings or numbers in the
output. Their purpose is to catch snippets that no longer run, not to be an
exhaustive unit-test suite.

## Files

| File | Summary |
|---|---|
| `test_code.py` | Pytest module with 13 smoke tests covering `code/decode` (`tagblock`, `moving_pandas_pipeline`, `compare_decoders.py`), `code/rf` (`linkbudget`, `gmsk_demo.py`), `code/tdma` (`sotdma_sim`), `code/analytics` (`coverage_estimate.py`, `duckdb_density.py`), `code/security/kinematic_checks.py`, and `code/viz` Blender scripts. Uses `data/samples/synthetic_harbor.nmea` and `synthetic_harbor_truth.csv` as fixtures. |

## Notes for agents

- Run from the repository root with `pytest -q code` (as stated in the module
  docstring). `ROOT` is computed as `parents[2]` of the test file, so the file
  must stay at `code/tests/test_code.py` for path resolution to work.
- The module prepends `code/decode`, `code/analytics`, `code/rf`, and
  `code/tdma` to `sys.path` and imports `tagblock`, `moving_pandas_pipeline`,
  `linkbudget`, and `sotdma_sim` directly. Renaming those modules or their
  functions (`format_tag`, `parse_line`, `decode_file`, `clean`,
  `trajectories`, `fspl_db`, `radio_horizon_km`, `two_ray_db`, `run`) will
  break the tests.
- Script-based tests invoke `code/rf/gmsk_demo.py`,
  `code/analytics/coverage_estimate.py`, `code/analytics/duckdb_density.py`,
  `code/security/kinematic_checks.py`, `code/decode/compare_decoders.py`,
  `code/viz/blender_ais_animation.py`, and `code/viz/blender_coverage_satpass.py`
  with `cwd=ROOT` and `sys.executable`. They assert on specific stdout
  substrings (`"CRC ok=True"`, `"p_detect"`, `"against truth"`,
  `"reports_corrected"`, `"1193046"`, `"pyais"`, `"tracks"`,
  `"footprint radius"`); changing a script's printed output requires updating
  the corresponding assertion.
- Several assertions encode properties of the synthetic sample data:
  more than 1900 decoded messages including types 1, 4, 5, 18, 21 and 24;
  six vessels remaining after cleaning (MMSI `0` and `1193046` are expected to
  be dropped); and MMSI `1193046` being flagged by the kinematic checks.
  Regenerating `data/samples/synthetic_harbor.nmea` may require revisiting
  these numbers.
- Numeric RF checks expect `radio_horizon_km(30, 50) ≈ 51.7`,
  `fspl_db(10) ≈ 96.6` (tolerance 0.2), and two-ray loss greater than free
  space at 50 km.
- The receiver position `42.36, -70.95` is passed as `--rx` to the analytics
  and security scripts.
- `test_blender_headless_if_available` is skipped unless a `blender` binary is
  on `PATH`; when present it writes `.cache/ais_anim.blend` under the repo
  root. The other Blender test confirms the scripts run (and print a summary)
  without `bpy` installed.
- Tests depend on third-party packages used by the snippets (e.g. pandas /
  MovingPandas, DuckDB, pyais, pytest); make sure the handbook's Python
  environment is installed before running.
