# `code/security/`

Companion code for the security / spoofing-and-anomaly material of *The AIS
Handbook* (an open, citable handbook on the maritime Automatic Identification
System). The script here implements the kinematic and receiver-coverage
plausibility checks described in Chapter 59 and is meant to be run against
decoded AIS tracks (e.g. the repository's synthetic sample NMEA data) to
produce a per-vessel triage score.

The directory depends on sibling code in `code/analytics/` (decoding via
`moving_pandas_pipeline.decode_file` and great-circle distance via
`coverage_estimate.haversine_nmi`); it is a thin analysis layer on top of that
pipeline, not a standalone decoder.

## Files
| File | Summary |
|---|---|
| `kinematic_checks.py` | CLI that decodes an NMEA file, groups position reports (message types 1/2/3/18/19) by MMSI, and computes per-track flags: implied speed vs. a hull-class cap (45 kn Class A, 60 kn Class B), implied-vs-reported SOG mismatch (>5 kn), turn rate >10°/s, "teleports" (>1 nmi in <60 s), fixes beyond 60 nmi from the receiver, max range, and invalid/placeholder MMSIs (0, 1193046, 123456789, or outside 200000000–799999999). Sums the flags into an integer `score` and prints a table sorted by score. |

## Notes for agents
- Run from the repository root so the relative data path resolves:
  `python code/security/kinematic_checks.py data/samples/synthetic_harbor.nmea --rx 42.36 -70.95`.
  `--rx LAT LON` (receiver position) is required.
- Imports are resolved by inserting `code/analytics/` onto `sys.path` at
  runtime (`pathlib.Path(__file__).resolve().parents[1] / "analytics"`); keep
  that relative layout intact if moving files. Requires `numpy` and `pandas`.
- Expected decoded DataFrame columns: `type`, `mmsi`, `lat`, `lon`, `t`
  (tz-aware UTC timestamps), `sog`, `cog`. Class is inferred from message
  type (18/19 → "B", otherwise "A").
- Time deltas are floored at 1 s (`np.maximum(np.diff(t), 1.0)`) to avoid
  division by zero; COG differences are wrapped to ±180°.
- Scoring thresholds: speed violations >0, turn violations >2, teleports >0,
  beyond-range >0, invalid MMSI, and SOG mismatches on more than 20% of fixes
  each add 1 point. The docstring and output text stress this is triage, not
  proof — a score ≥2 "deserves a second look"; confirm with DF/TDOA, SAR, or
  an independent receiver before calling anything spoofed. Preserve that
  framing in any edits or prose referencing this script.
- The docstring lists a fifth check (static-field changes mid-track:
  name/callsign/dimensions) that is **not** implemented in `analyze()`; only
  the kinematic, range, and MMSI checks exist in code.
- There are no tests in this directory; see `code/tests/` for the repository's
  test layout if adding coverage.
