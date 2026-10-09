#!/usr/bin/env python3
"""Generate the handbook's reproducible SVG figures into figures/chNN/ (Phase 2).

All figures are computed from the formulas/simulators in code/, so they stay
consistent with the text. Run: python code/figures/make_figures.py
"""
from __future__ import annotations

import math
import pathlib
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle, Circle, FancyBboxPatch  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[2]
FIG = ROOT / "figures"
sys.path.insert(0, str(ROOT / "code/rf"))
sys.path.insert(0, str(ROOT / "code/tdma"))
from linkbudget import fspl_db, two_ray_db, radio_horizon_km, dbm, KM_PER_NMI  # noqa: E402
from sotdma_sim import run as sim  # noqa: E402

plt.rcParams.update({"font.size": 9, "svg.fonttype": "none"})


def save(fig, ch, name):
    d = FIG / f"ch{ch:02d}"
    d.mkdir(parents=True, exist_ok=True)
    fig.savefig(d / f"{name}.svg", bbox_inches="tight")
    plt.close(fig)
    print("wrote", d / f"{name}.svg")


def fig_system_overview():
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis("off")
    boxes = {
        "Ship A\nClass A": (1, 1.2), "Ship B\nClass B": (3.2, 0.6), "AtoN\n(real/virtual)": (5.2, 1.0),
        "Base station /\nshore network": (7.6, 1.3), "LEO satellite\n(SAT-AIS / VDE-SAT)": (5.0, 4.0),
        "Aggregators,\nVTS, analysts": (9.0, 3.6),
    }
    for label, (x, y) in boxes.items():
        ax.add_patch(FancyBboxPatch((x - 0.9, y - 0.4), 1.8, 0.8, boxstyle="round,pad=0.05", fc="#eef", ec="k"))
        ax.text(x, y, label, ha="center", va="center", fontsize=8)
    def arrow(a, b, style="<->", color="k"):
        ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle=style, color=color, lw=1))
    arrow((1.9, 1.2), (2.3, 0.8)); arrow((1.6, 1.6), (4.2, 3.7), "->", "gray"); arrow((3.6, 1.0), (4.6, 3.6), "->", "gray")
    arrow((4.1, 0.9), (4.3, 1.0)); arrow((6.1, 1.1), (6.7, 1.3)); arrow((1.9, 1.4), (6.7, 1.5)); arrow((8.5, 1.5), (8.6, 3.2), "->")
    arrow((5.9, 4.0), (8.1, 3.8), "->", "gray")
    ax.text(5, 2.6, "VHF 161.975 / 162.025 MHz, 9.6 kbit/s GMSK, self-organised TDMA (2 × 2,250 slots/min)",
            ha="center", fontsize=8, style="italic")
    ax.set_title("AIS as a system: ship–ship, ship–shore, shore–ship, and space")
    save(fig, 1, "system-overview")


def fig_slot_map():
    fig, ax = plt.subplots(figsize=(8, 2.2))
    slots = 60
    for i in range(slots):
        used = i % 7 == 3 or i % 11 == 5
        ax.add_patch(Rectangle((i, 0), 1, 1, fc="#c33" if used else "#eee", ec="k", lw=0.4))
    ax.set_xlim(0, slots); ax.set_ylim(-0.6, 1.8); ax.set_yticks([])
    ax.set_xlabel("slot number within the 1-minute frame (first 60 of 2,250; each 26.67 ms = 256 bits)")
    ax.annotate("own nominal slot", xy=(3.5, 1), xytext=(3.5, 1.5), ha="center", arrowprops=dict(arrowstyle="->"))
    ax.annotate("next: +RI (e.g. 375 slots = 10 s), chosen within ±10 % selection interval", xy=(16.5, 1),
                xytext=(30, 1.5), ha="center", fontsize=8, arrowprops=dict(arrowstyle="->"))
    ax.set_title("SOTDMA slot map (one channel)")
    save(fig, 21, "slot-map")


def fig_burst_structure():
    fig, ax = plt.subplots(figsize=(8, 1.8))
    parts = [("ramp-up", 8), ("training 0101…", 24), ("flag 7E", 8), ("data (Msg 1: 168 bits)", 168), ("CRC-16", 16), ("flag 7E", 8), ("buffer", 24)]
    x = 0
    for name, n in parts:
        ax.add_patch(Rectangle((x, 0), n, 1, fc="#ddf" if "data" in name else "#eee", ec="k"))
        ax.text(x + n / 2, 0.5, f"{name}\n{n}", ha="center", va="center", fontsize=7)
        x += n
    ax.set_xlim(0, 256); ax.set_ylim(0, 1); ax.set_yticks([]); ax.set_xlabel("bits (256 per slot at 9,600 bit/s = 26.67 ms)")
    ax.set_title("AIS transmission packet layout (ITU-R M.1371 Annex 2); bit stuffing may consume part of the buffer")
    save(fig, 28, "burst-structure")


def fig_path_loss():
    d = [x for x in range(2, 121, 2)]
    fig, ax = plt.subplots(figsize=(6.5, 4))
    for htx, hrx, c in ((5, 30, "C0"), (20, 50, "C1"), (30, 200, "C2")):
        ax.plot(d, [max(fspl_db(k), two_ray_db(k, htx, hrx)) for k in d], c, label=f"two-ray, h_tx={htx} m, h_rx={hrx} m")
        hz = radio_horizon_km(htx, hrx)
        ax.axvline(hz, color=c, ls=":", lw=0.8)
    ax.plot(d, [fspl_db(k) for k in d], "k--", label="free space")
    ax.axhline(dbm(12.5) + 5 - 2.5 + 107, color="r", lw=0.8, label="12.5 W budget to −107 dBm (max loss)")
    ax.set_xlabel("distance (km)"); ax.set_ylabel("path loss (dB) at 162 MHz"); ax.grid(alpha=.3); ax.legend(fontsize=7)
    ax.set_title("Path loss vs distance; dotted lines = 4/3-Earth radio horizon")
    save(fig, 27, "path-loss")


def fig_radio_horizon():
    fig, ax = plt.subplots(figsize=(6, 3.6))
    h = list(range(1, 301))
    for hs, lab in ((2, "to a 2 m antenna (small craft)"), (20, "to a 20 m antenna (ship)"), (0, "to sea level")):
        ax.plot(h, [radio_horizon_km(x, hs) / KM_PER_NMI for x in h], label=lab)
    ax.set_xscale("log"); ax.set_xlabel("receiver antenna height (m)"); ax.set_ylabel("radio horizon (nmi)")
    ax.grid(alpha=.3, which="both"); ax.legend(fontsize=7); ax.set_title("d = 4.12(√h₁ + √h₂) km")
    save(fig, 27, "radio-horizon")


def fig_spectrum_adjacency():
    fig, ax = plt.subplots(figsize=(8, 2.6))
    chans = [(156.525, "DSC ch 70", "#ccc"), (156.775, "ch 75 (LR AIS)", "#cfc"), (156.825, "ch 76 (LR AIS)", "#cfc"),
             (161.950, "ASM 1", "#ffd"), (161.975, "AIS 1", "#c33"), (162.000, "ASM 2", "#ffd"), (162.025, "AIS 2", "#c33")]
    for f, lab, c in chans:
        ax.add_patch(Rectangle((f - 0.0125, 0), 0.025, 1, fc=c, ec="k", lw=.5))
        ax.text(f, 1.05, lab, rotation=60, fontsize=7, ha="left")
    for f in (162.400, 162.425, 162.450, 162.475, 162.500, 162.525, 162.550):
        ax.add_patch(Rectangle((f - 0.0125, 0), 0.025, 1, fc="#99f", ec="k", lw=.5))
    ax.text(162.475, 1.05, "NOAA Weather Radio (7 ch, up to 1 kW)", fontsize=7, ha="center")
    ax.set_xlim(156.4, 162.7); ax.set_ylim(0, 1.6); ax.set_yticks([]); ax.set_xlabel("MHz")
    ax.set_title("AIS and neighbours in the VHF maritime band (not to scale in amplitude)")
    save(fig, 31, "spectrum-adjacency")


def fig_saturation():
    ns = [50, 100, 200, 300, 400, 500, 600, 700]
    rows = [sim(n, 40, frames=3) for n in ns]
    fig, ax = plt.subplots(figsize=(6, 3.6))
    ax.plot(ns, [r["occupancy"] for r in rows], "o-", label="slot occupancy")
    ax.plot(ns, [r["a_loss_rate"] for r in rows], "s-", label="Class A collision rate")
    ax.plot(ns, [r["b_defer_rate"] for r in rows], "^-", label="Class B CS deferral rate")
    ax.set_xlabel("Class A stations in the cell (10 s interval) + 40 Class B (30 s)"); ax.set_ylabel("fraction")
    ax.grid(alpha=.3); ax.legend(fontsize=7); ax.set_title("Teaching simulator: Class B starves first (code/tdma/sotdma_sim.py)")
    save(fig, 30, "saturation")


def fig_satellite_footprint():
    fig, ax = plt.subplots(figsize=(6, 4))
    R = 6371.0
    for alt in (400, 600, 800):
        lam = math.acos(R / (R + alt)); r = R * lam
        ax.add_patch(Circle((0, 0), r, fill=False, ls="--", label=f"{alt} km altitude: r ≈ {r:,.0f} km"))
    ax.add_patch(Circle((0, 0), radio_horizon_km(50, 20), color="r", label="shore receiver, 50 m mast: ≈ 55 km"))
    ax.set_aspect("equal"); ax.set_xlim(-3500, 3500); ax.set_ylim(-3500, 3500); ax.legend(fontsize=7, loc="upper right")
    ax.set_xlabel("km"); ax.set_title("Why satellites see thousands of ships (and their slot collisions) at once")
    save(fig, 39, "footprint")


def fig_coverage_curve():
    truth = [(0, 1.00), (5, 1.00), (10, 1.00), (15, .91), (20, .54), (25, .38), (30, .17)]
    est = [(0, .60), (5, .70), (10, .73), (15, .64), (20, .32), (25, .27), (30, .16)]
    fig, ax = plt.subplots(figsize=(6, 3.6))
    ax.step([t[0] for t in truth] + [35], [t[1] for t in truth] + [truth[-1][1]], where="post", label="true detection probability (generator)")
    ax.step([t[0] for t in est] + [35], [t[1] for t in est] + [est[-1][1]], where="post", label="expected-vs-observed estimate (SOG-based RI)")
    ax.set_xlabel("range from receiver (nmi)"); ax.set_ylabel("p(detect)"); ax.set_ylim(0, 1.05); ax.grid(alpha=.3); ax.legend(fontsize=7)
    ax.set_title("Coverage estimation on the synthetic sample: shape right, level biased by the RI model")
    save(fig, 48, "coverage-curve")


def fig_timeline():
    events = [(1912, "Titanic"), (1914, "SOLAS"), (1989, "Exxon Valdez / STDMA patent (SE)"), (1998, "ITU-R M.1371-0; MSC.74(69)"),
              (2000, "SOLAS V/19 adopted"), (2002, "in force; MTSA; 9/11 acceleration"), (2004, "carriage complete (Dec)"),
              (2006, "Class B (IEC 62287)"), (2008, "first SAT-AIS (NTS)"), (2010, "AISSat-1; libais; Msg 27"),
              (2012, "Whale Alert"), (2014, "Trend Micro ACSAC"), (2015, "VDES M.2092; A.1106(29)"), (2016, "GFW launch"),
              (2017, "Black Sea GNSS spoofing"), (2021, "China feed drop"), (2024, "IALA IGO (verify)")]
    fig, ax = plt.subplots(figsize=(9, 3))
    for i, (y, lab) in enumerate(events):
        ax.plot([y, y], [0, 1 if i % 2 else -1], color="gray", lw=.6)
        ax.text(y, 1.05 if i % 2 else -1.05, f"{y} {lab}", rotation=90, fontsize=6.5, ha="center", va="bottom" if i % 2 else "top")
    ax.axhline(0, color="k"); ax.set_ylim(-4, 4); ax.set_yticks([]); ax.set_xlim(1905, 2030)
    ax.set_title("AIS timeline (selected; see Appendix A)")
    save(fig, 12, "timeline")


def fig_home_receiver():
    fig, ax = plt.subplots(figsize=(8, 2.4)); ax.axis("off"); ax.set_xlim(0, 10); ax.set_ylim(0, 2)
    chain = ["162 MHz\nantenna", "lightning\narrestor", "LMR-400\ncoax", "FM notch /\nbandpass", "LNA\n(optional)", "RTL-SDR or\ndAISy", "Raspberry Pi\nAIS-catcher", "NMEA/UDP →\nOpenCPN, feeds"]
    for i, c in enumerate(chain):
        x = 0.3 + i * 1.22
        ax.add_patch(FancyBboxPatch((x, 0.6), 1.05, 0.8, boxstyle="round,pad=0.03", fc="#eef", ec="k"))
        ax.text(x + 0.525, 1.0, c, ha="center", va="center", fontsize=7)
        if i < len(chain) - 1:
            ax.annotate("", xy=(x + 1.22, 1.0), xytext=(x + 1.05, 1.0), arrowprops=dict(arrowstyle="->"))
    ax.set_title("Low-budget home receiver signal chain")
    save(fig, 42, "signal-chain")


if __name__ == "__main__":
    for f in (fig_system_overview, fig_slot_map, fig_burst_structure, fig_path_loss, fig_radio_horizon,
              fig_spectrum_adjacency, fig_saturation, fig_satellite_footprint, fig_coverage_curve, fig_timeline, fig_home_receiver):
        f()
    (FIG / "LICENSES.md").write_text("# Figure licences\n\nAll figures under figures/ generated by code/figures/make_figures.py "
                                     "are original works licensed CC-BY-4.0 (see LICENSE). Any imported figure must be listed here with its source and licence.\n")
