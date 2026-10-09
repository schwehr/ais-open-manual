#!/usr/bin/env python3
"""Compare received-range statistics from a log against two-ray / free-space predictions (Chapter 29).

For each Class A position report, compute range to the receiver and the predicted
received power under free-space and two-ray models; then bin by range and show the
fraction of *expected* reports actually received (from coverage_estimate) next to
the predicted margin. Where the empirical curve falls off faster than the margin
predicts, suspect terrain/structure shadowing, noise, or antenna problems; where it
falls off slower, suspect ducting or an optimistic noise floor.

Usage: python code/rf/propagation_compare.py data/samples/synthetic_harbor.nmea --rx 42.36 -70.95 --hrx 30 --htx 20
"""
from __future__ import annotations

import argparse
import pathlib
import sys

import numpy as np

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "analytics"))
from linkbudget import fspl_db, two_ray_db, dbm, radio_horizon_km, KM_PER_NMI  # noqa: E402
from moving_pandas_pipeline import decode_file  # noqa: E402
from coverage_estimate import haversine_nmi, nominal_interval_s  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--rx", nargs=2, type=float, required=True)
    ap.add_argument("--hrx", type=float, default=30.0)
    ap.add_argument("--htx", type=float, default=20.0)
    ap.add_argument("--ptx", type=float, default=12.5)
    ap.add_argument("--gains", type=float, default=5.0, help="sum of antenna gains dBi")
    ap.add_argument("--losses", type=float, default=2.5, help="cable losses dB")
    ap.add_argument("--sens", type=float, default=-107.0, help="receiver sensitivity dBm")
    ap.add_argument("--bin-nmi", type=float, default=5.0)
    a = ap.parse_args()

    df = decode_file(a.path)
    pos = df[df["type"].isin([1, 2, 3])].dropna(subset=["lat", "lon", "t"]).copy()
    pos["range_nmi"] = haversine_nmi(pos["lat"], pos["lon"], a.rx[0], a.rx[1])
    pos["minute"] = pos["t"].dt.floor("min")
    pos["exp"] = 60.0 / pos.apply(lambda r: nominal_interval_s(r["sog"], r["status"]), axis=1)
    per = pos.groupby(["mmsi", "minute"]).agg(obs=("t", "size"), exp=("exp", "mean"), rng=("range_nmi", "mean")).reset_index()
    per["bin"] = (per["rng"] // a.bin_nmi) * a.bin_nmi
    g = per.groupby("bin").agg(obs=("obs", "sum"), exp=("exp", "sum"))
    horizon = radio_horizon_km(a.htx, a.hrx) / KM_PER_NMI
    print(f"radio horizon (h_tx={a.htx} m, h_rx={a.hrx} m): {horizon:.1f} nmi")
    print(" range_nmi   p_obs   Prx_fspl  Prx_2ray  margin_2ray  note")
    for b, r in g.iterrows():
        d_km = (b + a.bin_nmi / 2) * KM_PER_NMI
        p_fs = dbm(a.ptx) + a.gains - a.losses - fspl_db(d_km)
        p_2r = dbm(a.ptx) + a.gains - a.losses - max(fspl_db(d_km), two_ray_db(d_km, a.htx, a.hrx))
        margin = p_2r - a.sens
        p_obs = min(1.0, r.obs / r.exp)
        note = ""
        if b + a.bin_nmi / 2 > horizon and p_obs > 0.5:
            note = "beyond horizon yet received: ducting/diffraction?"
        elif margin > 15 and p_obs < 0.5:
            note = "margin ok but poor reception: shadowing/noise/antenna?"
        print(f"{b:5.0f}–{b + a.bin_nmi:<5.0f} {p_obs:6.2f} {p_fs:9.1f} {p_2r:9.1f} {margin:11.1f}  {note}")


if __name__ == "__main__":
    main()
