#!/usr/bin/env python3
"""Decode the same NMEA corpus with several decoders and diff the results (Chapter 44).

Decoders tried: pyais (always), libais (if importable), gpsdecode (if on PATH).
Usage: python code/decode/compare_decoders.py data/samples/synthetic_harbor.nmea
"""
from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from tagblock import parse_line  # noqa: E402

COMMON = ["mmsi", "lat", "lon", "sog", "cog", "heading"]


def with_pyais(sentences):
    from pyais.stream import IterMessages
    out = []
    for m in IterMessages([s.encode() for s in sentences]):
        d = m.decode().asdict()
        out.append({"type": d.get("msg_type"), "mmsi": d.get("mmsi"), "lat": d.get("lat"), "lon": d.get("lon"),
                    "sog": d.get("speed"), "cog": d.get("course"), "heading": d.get("heading")})
    return out


def with_libais(sentences):
    try:
        import ais  # libais
        import ais.stream
    except ImportError:
        return None
    out = []
    for msg in ais.stream.decode(iter(s + "\n" for s in sentences)):
        out.append({"type": msg.get("id"), "mmsi": msg.get("mmsi"), "lat": msg.get("y"), "lon": msg.get("x"),
                    "sog": msg.get("sog"), "cog": msg.get("cog"), "heading": msg.get("true_heading")})
    return out


def with_gpsdecode(sentences):
    exe = shutil.which("gpsdecode")
    if not exe:
        return None
    p = subprocess.run([exe], input="\n".join(sentences) + "\n", text=True, capture_output=True)
    out = []
    for line in p.stdout.splitlines():
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        out.append({"type": d.get("type"), "mmsi": d.get("mmsi"), "lat": d.get("lat"), "lon": d.get("lon"),
                    "sog": d.get("speed"), "cog": d.get("course"), "heading": d.get("heading")})
    return out


def approx_equal(a, b, tol=1e-4):
    if a is None or b is None:
        return a == b
    try:
        return abs(float(a) - float(b)) <= tol
    except (TypeError, ValueError):
        return a == b


def main(path):
    sentences = [parse_line(l)[1] for l in open(path) if l.strip()]
    results = {"pyais": with_pyais(sentences), "libais": with_libais(sentences), "gpsdecode": with_gpsdecode(sentences)}
    ref = results["pyais"]
    print(f"{len(sentences)} sentences")
    for name, res in results.items():
        if res is None:
            print(f"{name:10s} not available")
            continue
        import collections
        by_type = dict(sorted(collections.Counter(r["type"] for r in res).items(), key=lambda kv: kv[0] or 0))
        print(f"{name:10s} decoded {len(res)} messages by type {by_type}")
        if name != "pyais" and len(res) == len(ref):
            diffs = 0
            for a, b in zip(ref, res):
                for k in COMMON:
                    if not approx_equal(a[k], b[k]):
                        # libais encodes 'not available' heading as 511 like the spec; pyais too — differences are real
                        diffs += 1
                        if diffs <= 5:
                            print(f"   diff type={a['type']} {k}: pyais={a[k]} {name}={b[k]}")
            print(f"   field differences vs pyais: {diffs}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "data/samples/synthetic_harbor.nmea"))
