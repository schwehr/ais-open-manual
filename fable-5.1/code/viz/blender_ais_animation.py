#!/usr/bin/env python3
"""Blender (bpy) headless script: animate cleaned AIS trajectories with scaled hull proxies (Chapters 45, 56).

Run:
  blender --background --python code/viz/blender_ais_animation.py -- \
      --csv data/samples/synthetic_harbor_truth.csv --out /tmp/ais_anim.blend --render /tmp/ais_frame.png

Design notes (see Chapter 45):
  * Blender works in float32 metres; we project to a local tangent plane (equirectangular about the
    scene origin) so precision stays sub-metre within ~100 km. Do NOT feed raw degrees to Blender.
  * Hull proxies use Message 5 dimensions (to_bow+to_stern × to_port+to_starboard) when available; the
    truth CSV lacks them, so a default by class is used.
  * Orientation uses heading when valid (not 511), else COG. This is the same rule a bridge display uses.
  * Time remapping: scene frame = (t - t0) / seconds_per_frame. Keyframes use LINEAR interpolation to avoid
    Bézier overshoot between sparse Class B fixes — a classic animation artefact that misleads viewers.
"""
import argparse
import csv
import math
import sys
from collections import defaultdict
from datetime import datetime

try:
    import bpy  # type: ignore
except ImportError:  # allows import for tests outside Blender
    bpy = None

DEFAULT_DIMS = {"A": (120.0, 20.0), "B": (10.0, 3.5)}  # length, beam (m)


def parse_args(argv):
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]   # inside Blender: args after '--'
    elif argv and argv[0].endswith(".py"):
        argv = argv[1:]                       # plain python: drop script name
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--out", default="ais_anim.blend")
    ap.add_argument("--render", default=None)
    ap.add_argument("--seconds-per-frame", type=float, default=10.0)
    ap.add_argument("--origin", nargs=2, type=float, default=None, help="lat lon of scene origin (default: mean)")
    return ap.parse_args(argv)


def load_tracks(path):
    tracks = defaultdict(list)
    with open(path) as fh:
        for r in csv.DictReader(fh):
            t = datetime.fromisoformat(r["time"]).timestamp()
            hdg = float(r["heading"]) if r.get("heading") not in (None, "", "511") else None
            tracks[r["mmsi"]].append((t, float(r["lat"]), float(r["lon"]), float(r["cog"]), hdg, r.get("class", "A")))
    for v in tracks.values():
        v.sort()
    return tracks


def to_local(lat, lon, lat0, lon0):
    R = 6371000.0
    x = math.radians(lon - lon0) * R * math.cos(math.radians(lat0))
    y = math.radians(lat - lat0) * R
    return x, y


def build_scene(tracks, origin, spf):
    scene = bpy.context.scene
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    t0 = min(v[0][0] for v in tracks.values())
    t1 = max(v[-1][0] for v in tracks.values())
    scene.frame_start, scene.frame_end = 1, int((t1 - t0) / spf) + 1
    lat0, lon0 = origin
    # ground plane
    bpy.ops.mesh.primitive_plane_add(size=200000, location=(0, 0, -0.5))
    for mmsi, pts in tracks.items():
        cls = pts[0][5]
        L, B = DEFAULT_DIMS.get(cls, DEFAULT_DIMS["A"])
        bpy.ops.mesh.primitive_cube_add(size=1)
        hull = bpy.context.active_object
        hull.name = f"MMSI_{mmsi}"
        hull.scale = (L / 2, B / 2, max(2.0, B / 4))
        hull.scale = (L, B, max(4.0, B / 2))
        for t, lat, lon, cog, hdg, _ in pts:
            x, y = to_local(lat, lon, lat0, lon0)
            frame = int((t - t0) / spf) + 1
            hull.location = (x, y, 0.0)
            yaw = math.radians(90.0 - (hdg if hdg is not None else cog))  # Blender +X east, CCW positive
            hull.rotation_euler = (0.0, 0.0, yaw)
            hull.keyframe_insert("location", frame=frame)
            hull.keyframe_insert("rotation_euler", frame=frame)
        if hull.animation_data and hull.animation_data.action:
            for fc in hull.animation_data.action.fcurves:
                for kp in fc.keyframe_points:
                    kp.interpolation = "LINEAR"
    # camera and light
    bpy.ops.object.camera_add(location=(0, -30000, 25000), rotation=(math.radians(50), 0, 0))
    scene.camera = bpy.context.active_object
    bpy.ops.object.light_add(type="SUN", location=(0, 0, 10000))
    return scene


def main():
    a = parse_args(sys.argv)
    tracks = load_tracks(a.csv)
    if a.origin:
        origin = tuple(a.origin)
    else:
        lats = [p[1] for v in tracks.values() for p in v]
        lons = [p[2] for v in tracks.values() for p in v]
        origin = (sum(lats) / len(lats), sum(lons) / len(lons))
    if bpy is None:
        print("bpy not available — run inside Blender. Parsed", len(tracks), "tracks; origin", origin)
        return 0
    scene = build_scene(tracks, origin, a.seconds_per_frame)
    bpy.ops.wm.save_as_mainfile(filepath=a.out)
    if a.render:
        scene.render.filepath = a.render
        scene.frame_set(scene.frame_end // 2)
        bpy.ops.render.render(write_still=True)
    print(f"saved {a.out}; frames {scene.frame_start}-{scene.frame_end}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
