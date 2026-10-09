# `figures/ch31/`

Figure assets for Chapter 31 of *The AIS Handbook*, an open, citable handbook
on the maritime Automatic Identification System. This directory currently holds
a single Matplotlib-generated SVG that places the AIS channels in context with
their spectral neighbours in the VHF maritime band.

Figures in `figures/chNN/` are referenced from the corresponding chapter
source; the SVG here is a rendered output (generated 2026-10-04 by
Matplotlib v3.11.2 per its embedded metadata), not hand-drawn artwork.

## Files
| File | Summary |
|---|---|
| `spectrum-adjacency.svg` | Bar-style spectrum chart titled "AIS and neighbours in the VHF maritime band (not to scale in amplitude)". X axis is labelled "MHz" with ticks 157–162. Colored vertical bars mark: DSC ch 70 (grey, ~156.5 MHz), ch 75 and ch 76 (LR AIS, light green, ~156.8 MHz), ASM 1 / AIS 1 / ASM 2 / AIS 2 (alternating pale yellow and red bars clustered just below/around 162 MHz), and a group of seven blue bars labelled "NOAA Weather Radio (7 ch, up to 1 kW)" above ~162.4 MHz. No Y axis is drawn. |

## Notes for agents
- The SVG is a Matplotlib export (514×202 pt). Do not hand-edit it; if the
  figure needs changes, locate and rerun the generating Python script (not in
  this directory) and overwrite the SVG.
- The title explicitly states amplitudes are "not to scale"; bar heights are
  uniform and carry no power information. Only the horizontal (frequency)
  positions and the labels are meaningful.
- Channel labels are rotated −60° and are only 7 px; keep label text short if
  adding more bars so they do not overlap.
- Colors used: `#cccccc` DSC ch 70, `#ccffcc` long-range AIS ch 75/76,
  `#ffffdd` ASM 1/2, `#cc3333` AIS 1/2, `#9999ff` NOAA Weather Radio.
- This directory has no README, data, or code; it only contains the figure and
  this `AGENTS.md`.
