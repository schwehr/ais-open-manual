#!/usr/bin/env python3
"""Blender (bpy) headless script: animate a shore receiver footprint and a LEO satellite pass (Chapters 39, 48).

Run:
  blender --background --python code/viz/blender_coverage_satpass.py -- --out /tmp/satpass.blend

What it shows
  * A receiver at height h with its radio-horizon disc (d = 4.12*(sqrt(h)+sqrt(h_ship)) km) drawn to scale.
  * A satellite at 600 km altitude moving along a straight ground track at 7.56 km/s with a footprint
    disc of radius ~ R*acos(R/(R+alt)) (≈2,800 km for 600 km altitude) — the reason a single LEO pass sees
    thousands of ships at once and why slot collisions dominate satellite reception.
  * Scene units are kilometres (1 Blender unit = 1 km) so the two discs can share one view.
"""
import argparse
import math
import sys

try:
    import bpy  # type: ignore
except ImportError:
    bpy = None

R_EARTH_KM = 6371.0


def horizon_km(h1_m, h2_m):
    return 4.12 * (math.sqrt(h1_m) + math.sqrt(h2_m))


def footprint_radius_km(alt_km, min_elev_deg=0.0):
    # ground range to the horizon at min elevation (spherical Earth)
    e = math.radians(min_elev_deg)
    rho = math.asin(R_EARTH_KM / (R_EARTH_KM + alt_km))          # Earth angular radius seen from the satellite
    lam = math.pi / 2 - e - math.asin(math.cos(e) * math.sin(rho))  # Earth-central angle to the edge of coverage
    return R_EARTH_KM * lam


def parse_args(argv):
    if "--" in argv:
        argv = argv[argv.index("--") + 1:]   # inside Blender: args after '--'
    elif argv and argv[0].endswith(".py"):
        argv = argv[1:]                       # plain python: drop script name
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="satpass.blend")
    ap.add_argument("--rx-height-m", type=float, default=50.0)
    ap.add_argument("--ship-height-m", type=float, default=20.0)
    ap.add_argument("--alt-km", type=float, default=600.0)
    ap.add_argument("--seconds", type=float, default=600.0)
    ap.add_argument("--fps", type=int, default=24)
    return ap.parse_args(argv)


def main():
    a = parse_args(sys.argv)
    rh = horizon_km(a.rx_height_m, a.ship_height_m)
    fr = footprint_radius_km(a.alt_km)
    print(f"receiver horizon {rh:.1f} km; satellite footprint radius {fr:.0f} km at {a.alt_km:.0f} km altitude")
    if bpy is None:
        print("bpy not available — numbers only.")
        return 0
    scene = bpy.context.scene
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o, do_unlink=True)
    scene.render.fps = a.fps
    scene.frame_start, scene.frame_end = 1, int(a.seconds * a.fps)
    bpy.ops.mesh.primitive_plane_add(size=8000, location=(0, 0, -0.1))
    bpy.ops.mesh.primitive_circle_add(radius=rh, fill_type="NGON", location=(0, 0, 0))
    bpy.context.active_object.name = "ReceiverHorizon"
    bpy.ops.mesh.primitive_circle_add(radius=fr, fill_type="NGON", location=(-fr * 1.5, 0, 0.05))
    foot = bpy.context.active_object
    foot.name = "SatelliteFootprint"
    v_kms = 7.56
    for f in (scene.frame_start, scene.frame_end):
        t = (f - 1) / a.fps
        foot.location = (-fr * 1.5 + v_kms * t, 0, 0.05)
        foot.keyframe_insert("location", frame=f)
    bpy.ops.object.camera_add(location=(0, -9000, 6000), rotation=(math.radians(55), 0, 0))
    scene.camera = bpy.context.active_object
    bpy.ops.wm.save_as_mainfile(filepath=a.out)
    print("saved", a.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
