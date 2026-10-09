#!/usr/bin/env python3
"""Estimate receiver detection probability vs range from a log (Chapter 48).

Method ("expected vs observed"): for each Class A vessel and each minute, the
nominal reporting interval implies an expected number of position reports
(SOG-dependent per ITU-R M.1371 Table 1: 10 s at 0–14 kn, 6 s at 14–23 kn, 2 s
above 23 kn, 3 min at anchor). Observed/expected per range bin gives an
empirical detection probability curve. With the synthetic sample, the truth
file lets us check the estimate against the generator's soft-coverage model
(p = 1 inside 15 nmi, linear to 0 at 35 nmi).

Usage: python code/analytics/coverage_estimate.py data/samples/synthetic_harbor.nmea --rx 42.36 -70.95
"""
from __future__ import annotations

import argparse
import math
import pathlib
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from moving_pandas_pipeline import decode_file  # noqa: E402


def haversine_nmi(lat1, lon1, lat2, lon2):
    R = 3440.065
    p1, p2 = np.radians(lat1), np.radians(lat2)
    dp, dl = np.radians(lat2 - lat1), np.radians(lon2 - lon1)
    h = np.sin(dp / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dl / 2) ** 2
    return 2 * R * np.arcsin(np.sqrt(h))


def nominal_interval_s(sog_kn, status=0):
    if status in (1, 5):  # anchored / moored
        return 180.0
    if sog_kn is None or math.isnan(sog_kn):
        return 10.0
    if sog_kn <= 14:
        return 10.0
    if sog_kn <= 23:
        return 6.0
    return 2.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--rx", nargs=2, type=float, required=True, metavar=("LAT", "LON"))
    ap.add_argument("--bin-nmi", type=float, default=5.0)
    ap.add_argument("--truth", default=None, help="optional truth CSV to compare")
    a = ap.parse_args()

    df = decode_file(a.path)
    pos = df[df["type"].isin([1, 2, 3])].dropna(subset=["lat", "lon", "t"]).copy()
    pos["range_nmi"] = haversine_nmi(pos["lat"], pos["lon"], a.rx[0], a.rx[1])
    pos["minute"] = pos["t"].dt.floor("min")
    pos["expected_per_min"] = 60.0 / pos.apply(lambda r: nominal_interval_s(r["sog"], r["status"]), axis=1)
    per = pos.groupby(["mmsi", "minute"]).agg(observed=("t", "size"), expected=("expected_per_min", "mean"),
                                              range_nmi=("range_nmi", "mean")).reset_index()
    per["bin"] = (per["range_nmi"] // a.bin_nmi) * a.bin_nmi
    curve = per.groupby("bin").agg(observed=("observed", "sum"), expected=("expected", "sum"), vessel_minutes=("mmsi", "size"))
    curve["p_detect"] = (curve["observed"] / curve["expected"]).clip(upper=1.0)
    print("range_bin_nmi  vessel_min  observed  expected  p_detect")
    for b, r in curve.iterrows():
        print(f"{b:8.0f}–{b + a.bin_nmi:<5.0f} {int(r.vessel_minutes):8d} {int(r.observed):9d} {r.expected:9.0f} {r.p_detect:9.2f}")
    if a.truth:
        tr = pd.read_csv(a.truth)
        tr = tr[tr["class"] == "A"]
        tr["range_nmi"] = haversine_nmi(tr["lat"], tr["lon"], a.rx[0], a.rx[1])
        tr["bin"] = (tr["range_nmi"] // a.bin_nmi) * a.bin_nmi
        truth_counts = tr.groupby("bin").size()
        obs_counts = pos.assign(bin=(pos["range_nmi"] // a.bin_nmi) * a.bin_nmi).groupby("bin").size()
        print("\nagainst truth: range_bin  truth_reports  received  p_true")
        for b in truth_counts.index:
            o = int(obs_counts.get(b, 0))
            print(f"{b:8.0f}–{b + a.bin_nmi:<5.0f} {int(truth_counts[b]):8d} {o:9d} {o / truth_counts[b]:8.2f}")
    print("\nNote: the expected-vs-observed estimate is biased upward when vessels enter/leave a minute bin, "
          "and downward when the SOG-based interval is wrong (e.g., status 'at anchor' not set). Report both.")


if __name__ == "__main__":
    main()
