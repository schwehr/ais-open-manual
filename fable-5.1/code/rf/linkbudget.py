#!/usr/bin/env python3
"""Radio horizon and link-budget helpers for AIS at 162 MHz (Chapters 27, 29, 39).

Formulas
  radio horizon (4/3 Earth):  d_km = 4.12 * (sqrt(h1_m) + sqrt(h2_m))
  free-space path loss:       FSPL_dB = 20 log10(d_km) + 20 log10(f_MHz) + 32.44
  two-ray (flat sea, far field): L_dB ≈ 40 log10(d_m) - 20 log10(h1_m) - 20 log10(h2_m)
  received power:             P_rx = P_tx + G_tx + G_rx - L_cable_tx - L_cable_rx - L_path
Typical numbers: Class A 12.5 W = 41 dBm; Class B 2 W = 33 dBm; receiver
sensitivity for 20% PER about -107 dBm (IEC 61993-2 requirement; verify exact
clause in the chapter).
"""
from __future__ import annotations

import argparse
import math

F_MHZ = 162.0
KM_PER_NMI = 1.852


def radio_horizon_km(h1_m: float, h2_m: float = 0.0) -> float:
    return 4.12 * (math.sqrt(max(h1_m, 0)) + math.sqrt(max(h2_m, 0)))


def fspl_db(d_km: float, f_mhz: float = F_MHZ) -> float:
    return 20 * math.log10(d_km) + 20 * math.log10(f_mhz) + 32.44


def two_ray_db(d_km: float, h1_m: float, h2_m: float) -> float:
    d_m = d_km * 1000.0
    return 40 * math.log10(d_m) - 20 * math.log10(h1_m) - 20 * math.log10(h2_m)


def dbm(watts: float) -> float:
    return 10 * math.log10(watts * 1000.0)


def link_budget(p_tx_w: float, g_tx_dbi: float, g_rx_dbi: float, d_km: float, h_tx_m: float, h_rx_m: float,
                cable_tx_db: float = 1.0, cable_rx_db: float = 1.5, model: str = "auto") -> dict:
    fs = fspl_db(d_km)
    tr = two_ray_db(d_km, h_tx_m, h_rx_m)
    if model == "fspl":
        loss = fs
    elif model == "two_ray":
        loss = tr
    else:  # auto: two-ray cannot be lower-loss than free space in the far field
        loss = max(fs, tr)
    p_rx = dbm(p_tx_w) + g_tx_dbi + g_rx_dbi - cable_tx_db - cable_rx_db - loss
    return {"d_km": d_km, "d_nmi": d_km / KM_PER_NMI, "fspl_db": round(fs, 1), "two_ray_db": round(tr, 1),
            "loss_used_db": round(loss, 1), "p_rx_dbm": round(p_rx, 1),
            "margin_vs_-107dBm": round(p_rx + 107, 1), "horizon_km": round(radio_horizon_km(h_tx_m, h_rx_m), 1)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ptx", type=float, default=12.5, help="W")
    ap.add_argument("--gtx", type=float, default=2.0, help="dBi")
    ap.add_argument("--grx", type=float, default=3.0, help="dBi")
    ap.add_argument("--htx", type=float, default=30.0, help="m")
    ap.add_argument("--hrx", type=float, default=50.0, help="m")
    ap.add_argument("--d", type=float, help="km (default: sweep)")
    ap.add_argument("--model", choices=["auto", "fspl", "two_ray"], default="auto")
    a = ap.parse_args()
    if a.d:
        print(link_budget(a.ptx, a.gtx, a.grx, a.d, a.htx, a.hrx, model=a.model))
        return
    print(f"radio horizon for h_tx={a.htx} m, h_rx={a.hrx} m: {radio_horizon_km(a.htx, a.hrx):.1f} km "
          f"({radio_horizon_km(a.htx, a.hrx)/KM_PER_NMI:.1f} nmi)")
    print(" d_km  d_nmi  FSPL  2-ray  used   Prx_dBm  margin")
    for d in (5, 10, 20, 30, 40, 50, 60, 80, 100):
        r = link_budget(a.ptx, a.gtx, a.grx, d, a.htx, a.hrx, model=a.model)
        print(f"{d:5.0f} {r['d_nmi']:6.1f} {r['fspl_db']:5.1f} {r['two_ray_db']:6.1f} {r['loss_used_db']:6.1f} "
              f"{r['p_rx_dbm']:8.1f} {r['margin_vs_-107dBm']:7.1f}")


if __name__ == "__main__":
    main()
