# `figures/ch01/`

Figure assets for Chapter 1 of "The AIS Handbook", an open, citable handbook
on the maritime Automatic Identification System. Chapter 1 is the introductory
system-level overview, and this directory holds the rendered figure(s) that
the chapter text embeds.

The directory currently contains a single Matplotlib-generated SVG that gives
a block-diagram view of the AIS system: who transmits, who receives, and over
which links.

## Files
| File | Summary |
|---|---|
| `system-overview.svg` | Matplotlib (v3.11.2) rendered SVG, 460.8 × 261.5 pt, titled "AIS as a system: ship–ship, ship–shore, shore–ship, and space". Six rounded boxes ("Ship A / Class A", "Ship B / Class B", "AtoN (real/virtual)", "Base station / shore network", "LEO satellite (SAT-AIS / VDE-SAT)", "Aggregators, VTS, analysts") connected by black double-headed arrows (terrestrial VHF links among ships, AtoN and base station) and grey single-headed arrows (ship/AtoN uplinks to the satellite, satellite and base-station feeds to aggregators). An italic caption across the middle reads "VHF 161.975 / 162.025 MHz, 9.6 kbit/s GMSK, self-organised TDMA (2 × 2,250 slots/min)". |

## Notes for agents
- The SVG is generated output (Matplotlib, dated 2026-10-04 in its metadata),
  not hand-drawn. Prefer regenerating it from its source script rather than
  editing the SVG XML by hand; the generating script is not in this
  directory, so look for it elsewhere in the repository before changing the
  figure.
- All labels are plain `<text>` elements, so the figure's content (box names,
  caption, title) can be verified or grepped directly from the SVG.
- Box fill is `#eeeeff` with black outlines; terrestrial AIS links are black,
  satellite/downstream data flows are grey (`#808080`). Keep this convention
  if adding boxes or links.
- The technical parameters in the caption (161.975/162.025 MHz, 9.6 kbit/s
  GMSK, 2 × 2,250 slots/min SOTDMA) should stay consistent with the text of
  Chapter 1 and any RF/link-layer chapters.
- There are no subdirectories and no data files here.
