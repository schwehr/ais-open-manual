# `code/figures/`

This directory holds the single script that regenerates the handbook's
reproducible SVG figures. "The AIS Handbook" is an open, citable handbook on
the maritime Automatic Identification System; its figures are computed from
the same formulas and simulators that live elsewhere under `code/` (the RF
link-budget helpers in `code/rf/` and the SOTDMA teaching simulator in
`code/tdma/`) so that diagrams stay numerically consistent with the text.

Running the script writes SVGs into the repository-level `figures/chNN/`
directories (one per chapter) and rewrites `figures/LICENSES.md`. The SVGs
themselves are outputs, not sources, and are not stored here.

## Files
| File | Summary |
|---|---|
| `make_figures.py` | Matplotlib (Agg backend) script that generates eleven SVG figures into `<repo>/figures/chNN/` and writes `figures/LICENSES.md`. Imports `fspl_db`, `two_ray_db`, `radio_horizon_km`, `dbm`, `KM_PER_NMI` from `code/rf/linkbudget.py` and `run` from `code/tdma/sotdma_sim.py`. |

### Figures produced by `make_figures.py`

| Function | Output | Depicts |
|---|---|---|
| `fig_system_overview` | `figures/ch01/system-overview.svg` | Box-and-arrow diagram: Ship A (Class A), Ship B (Class B), AtoN, base station/shore network, LEO satellite (SAT-AIS / VDE-SAT), aggregators/VTS/analysts; caption line "VHF 161.975 / 162.025 MHz, 9.6 kbit/s GMSK, self-organised TDMA (2 × 2,250 slots/min)". |
| `fig_slot_map` | `figures/ch21/slot-map.svg` | First 60 of 2,250 slots in a one-minute SOTDMA frame, with a handful shaded as used, an "own nominal slot" annotation and a "next: +RI (e.g. 375 slots = 10 s), chosen within ±10 % selection interval" annotation. |
| `fig_burst_structure` | `figures/ch28/burst-structure.svg` | 256-bit packet layout: ramp-up 8, training 24, flag 8, data 168 (Msg 1), CRC-16 16, flag 8, buffer 24 (ITU-R M.1371 Annex 2). |
| `fig_path_loss` | `figures/ch27/path-loss.svg` | Path loss (dB) at 162 MHz vs distance 2–120 km: free-space curve, three two-ray curves (h_tx/h_rx = 5/30, 20/50, 30/200 m) with dotted 4/3-Earth radio-horizon lines, and a red horizontal "12.5 W budget to −107 dBm (max loss)" line. |
| `fig_radio_horizon` | `figures/ch27/radio-horizon.svg` | Radio horizon (nmi) vs receiver antenna height 1–300 m (log x), for a 2 m antenna, a 20 m antenna, and sea level; title `d = 4.12(√h₁ + √h₂) km`. |
| `fig_spectrum_adjacency` | `figures/ch31/spectrum-adjacency.svg` | VHF maritime band 156.4–162.7 MHz: DSC ch 70, ch 75/76 (long-range AIS), ASM 1/2, AIS 1/2, and the seven NOAA Weather Radio channels. |
| `fig_saturation` | `figures/ch30/saturation.svg` | Runs `sotdma_sim.run(n, 40, frames=3)` for n = 50…700 Class A stations plus 40 Class B; plots slot occupancy, Class A collision rate, Class B CS deferral rate. |
| `fig_satellite_footprint` | `figures/ch39/footprint.svg` | Concentric footprint circles for 400/600/800 km satellite altitudes vs a 50 m shore-mast radio horizon (≈55 km). |
| `fig_coverage_curve` | `figures/ch48/coverage-curve.svg` | Step plots of hard-coded "true detection probability" vs "expected-vs-observed estimate (SOG-based RI)" over 0–30 nmi. |
| `fig_timeline` | `figures/ch12/timeline.svg` | Alternating-stem timeline 1912–2024 (Titanic, SOLAS, STDMA patent, M.1371-0, SOLAS V/19, Class B, SAT-AIS, VDES, GFW, GNSS spoofing, etc.); one entry is marked "(verify)". |
| `fig_home_receiver` | `figures/ch42/signal-chain.svg` | Eight-box signal chain: 162 MHz antenna → lightning arrestor → LMR-400 coax → FM notch/bandpass → LNA → RTL-SDR/dAISy → Raspberry Pi AIS-catcher → NMEA/UDP to OpenCPN/feeds. |

## Notes for agents
- Run from the repository root: `python code/figures/make_figures.py`. It
  requires `matplotlib`; it derives `ROOT` from its own path
  (`parents[2]`), so do not move the file without updating that.
- The script adds `code/rf` and `code/tdma` to `sys.path` and imports
  `linkbudget` and `sotdma_sim`. Changing function names or return keys there
  (`occupancy`, `a_loss_rate`, `b_defer_rate`) will break figure generation.
- Output goes to `<repo>/figures/chNN/<name>.svg` via the `save(fig, ch, name)`
  helper; chapter numbers are hard-coded per figure. If chapters are
  renumbered, update the `save()` calls.
- `plt.rcParams["svg.fonttype"] = "none"` keeps text as real text in the SVGs
  (searchable/editable), so titles and labels in the script are the source of
  truth for what the figures say.
- The `__main__` block also overwrites `figures/LICENSES.md` with a CC-BY-4.0
  notice; any manually added imported-figure entries there will be lost on
  re-run unless the script is updated.
- `fig_coverage_curve` and `fig_slot_map` use hard-coded illustrative values,
  not live computation; `fig_saturation` is stochastic via the simulator.
- Add new figures as a `fig_*` function and append it to the tuple in the
  `__main__` block.
