# `code/viz/`

Headless Blender (`bpy`) scripts that turn AIS concepts from "The AIS Handbook"
into 3D scenes and animations: one animates cleaned vessel trajectories as
scaled hull proxies, the other visualises a shore receiver's radio-horizon disc
next to a moving LEO satellite footprint. They accompany the handbook's
visualisation and coverage chapters (the docstrings cite Chapters 39, 45, 48
and 56) and are meant to be run from the repository root with
`blender --background --python ...`.

Both scripts degrade gracefully when `bpy` is not importable: they parse their
arguments, compute and print the derived numbers (track count / scene origin,
or horizon and footprint radii), and exit 0 without building a scene. This lets
them be imported and smoke-tested with plain Python outside Blender.

## Files
| File | Summary |
|---|---|
| `blender_ais_animation.py` | Reads a track CSV (columns `mmsi,time,lat,lon,cog,heading,class`), projects positions to a local equirectangular tangent plane in metres about a scene origin (default: mean lat/lon, or `--origin LAT LON`), and keyframes one cube "hull" per MMSI with LINEAR interpolation. Hull size comes from `DEFAULT_DIMS` by class (A: 120×20 m, B: 10×3.5 m); yaw uses heading unless it is empty/511, else COG. Saves a `.blend` (`--out`) and optionally renders the middle frame to `--render`. |
| `blender_coverage_satpass.py` | Builds a scene in kilometre units with a `ReceiverHorizon` disc of radius `4.12*(sqrt(h_rx)+sqrt(h_ship))` km and a `SatelliteFootprint` disc of radius `R*lambda` (spherical-Earth horizon from `--alt-km`, default 600 km) that translates along a straight ground track at 7.56 km/s over `--seconds` at `--fps`. Prints the two radii and saves to `--out`. |

## Notes for agents
- Invocation: `blender --background --python code/viz/<script>.py -- <args>`. `parse_args` strips everything up to and including `--` when run inside Blender, and drops `argv[0]` when run with plain `python`; keep that dual-mode behaviour if you add arguments.
- The example CSV referenced in `blender_ais_animation.py`'s docstring is `data/samples/synthetic_harbor_truth.csv`. `load_tracks` requires `time` to be ISO-8601 (`datetime.fromisoformat`) and `mmsi`, `lat`, `lon`, `cog` to be present; `heading` and `class` are optional (class defaults to `"A"`).
- Units differ between the two scripts: the animation script works in **metres** (local tangent plane, `R = 6371000`), the coverage script in **kilometres** (`R_EARTH_KM = 6371.0`, 1 Blender unit = 1 km). Do not feed raw lat/lon degrees to Blender (float32 precision).
- Frame mapping in the animation script is `frame = int((t - t0) / seconds_per_frame) + 1`; `--seconds-per-frame` defaults to 10. Keyframes are forced to `LINEAR` to avoid Bézier overshoot between sparse Class B fixes — preserve this.
- Yaw convention: `radians(90 - heading_or_cog)` because Blender's +X is east and rotation is counter-clockwise positive.
- Known quirk: in `build_scene`, `hull.scale` is assigned twice in a row (`(L/2, B/2, …)` then `(L, B, …)`); only the second assignment takes effect.
- Both scripts delete every object in the current Blender file before building (`bpy.data.objects.remove`), so never point them at a `.blend` you care about.
- There are no tests in this directory; the `bpy = None` fallback is what makes the modules importable from `code/tests/` or a REPL without Blender installed.
