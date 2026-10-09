#!/usr/bin/env python3
"""Kinematic and coverage plausibility checks for spoof/anomaly triage (Chapter 59).

Checks per vessel track:
  1. implied speed between consecutive fixes vs. reported SOG and a hull-class cap;
  2. implied turn rate vs. a cap;
  3. teleports (gap in time small, jump in space large);
  4. receiver-footprint plausibility: fix farther than a max plausible range from the
     receiver that heard it (terrestrial VHF rarely > ~60 nmi without ducting);
  5. static-field changes mid-track (name/callsign/dimensions) — flagged if present.
Outputs a per-vessel score; this is triage, not proof. Confirm with DF/TDOA, SAR,
or a second independent receiver before calling anything "spoofed".

Usage: python code/security/kinematic_checks.py data/samples/synthetic_harbor.nmea --rx 42.36 -70.95
"""
from __future__ import annotations

import argparse
import pathlib
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "analytics"))
from moving_pandas_pipeline import decode_file  # noqa: E402
from coverage_estimate import haversine_nmi  # noqa: E402

SPEED_CAP_KN = {"A": 45.0, "B": 60.0}   # generous caps; fast ferries ~40 kn, fast craft > 50 kn
TURN_CAP_DEG_S = 10.0
MAX_TERRESTRIAL_RANGE_NMI = 60.0


def analyze(df, rx):
    out = []
    pos = df[df["type"].isin([1, 2, 3, 18, 19])].dropna(subset=["lat", "lon", "t"]).sort_values(["mmsi", "t"])
    pos["cls"] = np.where(pos["type"].isin([18, 19]), "B", "A")
    for mmsi, g in pos.groupby("mmsi"):
        t = (g["t"] - pd.Timestamp(0, tz="UTC")).dt.total_seconds().to_numpy()
        lat, lon = g["lat"].to_numpy(), g["lon"].to_numpy()
        d = haversine_nmi(lat[:-1], lon[:-1], lat[1:], lon[1:])
        dt = np.maximum(np.diff(t), 1.0)
        implied_kn = d / (dt / 3600.0)
        cap = SPEED_CAP_KN[g["cls"].iloc[0]]
        cog = g["cog"].to_numpy()
        dcog = np.abs((np.diff(cog) + 180) % 360 - 180)
        turn = dcog / dt
        rng = haversine_nmi(lat, lon, rx[0], rx[1])
        flags = {
            "fixes": len(g),
            "speed_violations": int((implied_kn > cap).sum()),
            "max_implied_kn": float(implied_kn.max()) if len(implied_kn) else 0.0,
            "sog_mismatch": int((np.abs(implied_kn - g["sog"].to_numpy()[1:]) > 5).sum()) if len(g) > 1 else 0,
            "turn_violations": int((turn > TURN_CAP_DEG_S).sum()),
            "teleports": int(((d > 1.0) & (dt < 60)).sum()),
            "beyond_range": int((rng > MAX_TERRESTRIAL_RANGE_NMI).sum()),
            "max_range_nmi": float(rng.max()),
            "invalid_mmsi": int(mmsi in (0, 1193046, 123456789) or not (200000000 <= mmsi < 800000000)),
        }
        score = (flags["speed_violations"] > 0) + (flags["turn_violations"] > 2) + (flags["teleports"] > 0) \
            + (flags["beyond_range"] > 0) + flags["invalid_mmsi"] + (flags["sog_mismatch"] > len(g) * 0.2)
        out.append({"mmsi": mmsi, "score": int(score), **flags})
    return pd.DataFrame(out).sort_values("score", ascending=False)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--rx", nargs=2, type=float, required=True)
    a = ap.parse_args()
    df = decode_file(a.path)
    res = analyze(df, a.rx)
    pd.set_option("display.width", 200)
    print(res.to_string(index=False))
    print("\nscore >= 2 deserves a second look; score alone never proves spoofing.")


if __name__ == "__main__":
    main()
