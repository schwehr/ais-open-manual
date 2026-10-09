# `figures/ch48/`

Figure assets for chapter 48 of "The AIS Handbook", an open, citable handbook
on the maritime Automatic Identification System. This directory holds the
rendered SVG figures that the chapter text embeds; the chapter deals with
receiver coverage estimation (probability of detecting a vessel as a function
of range from the receiver).

The single figure here was generated with Matplotlib (v3.11.2, per the SVG
metadata, dated 2026-10-04) from a synthetic sample, and compares a known
"true" detection probability against an expected-vs-observed estimate.

## Files
| File | Summary |
|---|---|
| `coverage-curve.svg` | Matplotlib line chart titled "Coverage estimation on the synthetic sample: shape right, level biased by the RI model". X axis: "range from receiver (nmi)", ticks 0–35 in steps of 5. Y axis: "p(detect)", 0.0–1.0. Two step curves in 5 nmi bins: blue "true detection probability (generator)" (flat at 1.0 out to 15 nmi, then falling to roughly 0.17 by 30–35 nmi) and orange "expected-vs-observed estimate (SOG-based RI)" (starts near 0.6 at 0–5 nmi, peaks near 0.73 at 10–15 nmi, then falls to roughly 0.16 by 30–35 nmi, tracking the true curve's shape but biased low at short range). |

## Notes for agents
- The SVG is a generated artifact (Matplotlib output, ~490×257 pt, white
  background, DejaVu Sans). Do not hand-edit it; regenerate it from whatever
  script produced it if the figure needs to change. No generator script lives
  in this directory.
- The "RI" in the title/legend refers to the reporting interval model used to
  compute expected message counts (the legend says "SOG-based RI", i.e. the
  reporting interval is derived from speed over ground). The figure's stated
  point is that the estimate reproduces the *shape* of the coverage curve but
  its *level* is biased by the RI model.
- Curves are step plots with 5 nmi bins (0, 5, 10, ..., 35 nmi); the last bin
  is repeated so the step extends to the right edge.
- Chapter text referencing this figure should use the path
  `figures/ch48/coverage-curve.svg` relative to the repository root.
