#!/usr/bin/env python3
"""Hex-free grid density map with coverage normalization in DuckDB (Chapters 48, 50).

Reads the parquet written by moving_pandas_pipeline.py (or decodes the sample
directly), bins positions on a 0.02° grid, counts distinct vessels and reports,
and divides by an estimated detection probability from a range-based model so
the map shows *traffic*, not *reception*.

Usage: python code/analytics/duckdb_density.py data/samples/synthetic_harbor.nmea --rx 42.36 -70.95
"""
from __future__ import annotations

import argparse
import pathlib
import sys

import duckdb

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from moving_pandas_pipeline import decode_file  # noqa: E402

SQL = """
WITH pos AS (
  SELECT mmsi, t, lat, lon,
         2*3440.065*asin(sqrt(pow(sin(radians(lat-$rxlat)/2),2)
             + cos(radians(lat))*cos(radians($rxlat))*pow(sin(radians(lon-$rxlon)/2),2))) AS range_nmi
  FROM df WHERE type IN (1,2,3,18,19) AND lat IS NOT NULL AND mmsi NOT IN (0, 1193046)
),
cells AS (
  SELECT floor(lat/$cell)*$cell AS cell_lat, floor(lon/$cell)*$cell AS cell_lon,
         count(*) AS reports, count(DISTINCT mmsi) AS vessels, avg(range_nmi) AS range_nmi
  FROM pos GROUP BY 1,2
)
SELECT cell_lat, cell_lon, reports, vessels, round(range_nmi,1) AS range_nmi,
       -- detection-probability model: 1 inside 15 nmi, linear to 0 at 35 nmi (replace with measured curve)
       round(greatest(0.05, least(1.0, 1 - (range_nmi-15)/20)), 2) AS p_detect,
       round(reports / greatest(0.05, least(1.0, 1 - (range_nmi-15)/20)), 0) AS reports_corrected
FROM cells ORDER BY reports DESC LIMIT $limit
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("--rx", nargs=2, type=float, required=True)
    ap.add_argument("--cell", type=float, default=0.02)
    ap.add_argument("--limit", type=int, default=15)
    a = ap.parse_args()
    df = decode_file(a.path)  # noqa: F841  (DuckDB reads the local variable)
    con = duckdb.connect()
    res = con.execute(SQL, {"rxlat": a.rx[0], "rxlon": a.rx[1], "cell": a.cell, "limit": a.limit}).fetchdf()
    print(res.to_string(index=False))


if __name__ == "__main__":
    main()
