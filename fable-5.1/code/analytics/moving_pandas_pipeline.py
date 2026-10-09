#!/usr/bin/env python3
"""Raw NMEA → decoded table → cleaned → MovingPandas trajectories → stops (Chapters 45, 47).

Usage: python code/analytics/moving_pandas_pipeline.py data/samples/synthetic_harbor.nmea [out.parquet]
"""
from __future__ import annotations

import pathlib
import sys
import warnings

import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "decode"))
from tagblock import parse_line  # noqa: E402

warnings.filterwarnings("ignore")

INVALID_MMSI = {0, 1193046, 123456789, 111111111, 999999999}


def decode_file(path):
    """Decode a TAG-blocked NMEA log with pyais; receiver time comes from the TAG block 'c:' field."""
    from pyais.stream import FileReaderStream
    rows = []
    for m in FileReaderStream(str(path)):
        t = None
        if m.tag_block is not None:
            m.tag_block.init()
            ts = m.tag_block.receiver_timestamp
            if ts is not None:
                ts = float(ts)
                t = ts / 1000.0 if ts > 1e11 else ts
        try:
            d = m.decode().asdict()
        except Exception:
            continue
        rows.append({"t": t, "type": d.get("msg_type"), "mmsi": d.get("mmsi"), "lat": d.get("lat"), "lon": d.get("lon"),
                     "sog": d.get("speed"), "cog": d.get("course"), "heading": d.get("heading"),
                     "name": d.get("shipname"), "status": d.get("status")})
    df = pd.DataFrame(rows)
    df["t"] = pd.to_datetime(df["t"], unit="s", utc=True)
    return df


def clean(df):
    pos = df[df["type"].isin([1, 2, 3, 18, 19, 27])].copy()
    before = len(pos)
    pos = pos[~pos["mmsi"].isin(INVALID_MMSI)]
    pos = pos[(pos["lat"].abs() <= 90) & (pos["lon"].abs() <= 180) & (pos["lat"] != 91) & (pos["lon"] != 181)]
    pos = pos.drop_duplicates(subset=["mmsi", "t", "lat", "lon"])
    pos = pos.sort_values(["mmsi", "t"])
    # implied-speed outlier filter: drop fixes implying > 60 kn from previous fix
    import numpy as np
    keep = []
    for mmsi, g in pos.groupby("mmsi"):
        lat = np.radians(g["lat"].to_numpy()); lon = np.radians(g["lon"].to_numpy())
        t = (g["t"] - pd.Timestamp(0, tz="UTC")).dt.total_seconds().to_numpy()
        ok = np.ones(len(g), dtype=bool)
        for i in range(1, len(g)):
            dlat = lat[i] - lat[i - 1]; dlon = lon[i] - lon[i - 1]
            a = np.sin(dlat / 2) ** 2 + np.cos(lat[i]) * np.cos(lat[i - 1]) * np.sin(dlon / 2) ** 2
            d_nmi = 2 * 3440.065 * np.arcsin(np.sqrt(a))
            dt_h = max(t[i] - t[i - 1], 1) / 3600
            if d_nmi / dt_h > 60:
                ok[i] = False
        keep.append(g[ok])
    pos = pd.concat(keep) if keep else pos
    report = {"position_reports": before, "after_mmsi_filter_and_dedupe_and_speed": len(pos),
              "dropped": before - len(pos), "vessels": pos["mmsi"].nunique()}
    return pos, report


def trajectories(pos):
    import geopandas as gpd
    import movingpandas as mpd
    gdf = gpd.GeoDataFrame(pos, geometry=gpd.points_from_xy(pos["lon"], pos["lat"]), crs="EPSG:4326")
    tc = mpd.TrajectoryCollection(gdf, traj_id_col="mmsi", t="t", min_length=10)
    tc.add_speed(overwrite=True, units=("nm", "h"))
    return tc


def main(path, out=None):
    df = decode_file(path)
    pos, report = clean(df)
    print("cleaning report:", report)
    tc = trajectories(pos)
    print(f"{len(tc)} trajectories")
    for traj in tc.trajectories:
        print(f"  mmsi={traj.id} fixes={len(traj.df)} length_km={traj.get_length(units='km'):.1f} "
              f"start={traj.get_start_time():%H:%M:%S} end={traj.get_end_time():%H:%M:%S} "
              f"mean_sog_reported={traj.df['sog'].mean():.1f} kn mean_speed_derived={traj.df['speed'].mean():.1f} kn")
    try:
        import movingpandas as mpd
        stops = mpd.TrajectoryStopDetector(tc).get_stop_points(min_duration=pd.Timedelta(minutes=5), max_diameter=200)
        print(f"{len(stops)} stops (>=5 min within 200 m)")
    except Exception as e:  # pragma: no cover
        print("stop detection skipped:", e)
    if out:
        pos.to_parquet(out)
        print("wrote", out)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "data/samples/synthetic_harbor.nmea",
                  sys.argv[2] if len(sys.argv) > 2 else None))
