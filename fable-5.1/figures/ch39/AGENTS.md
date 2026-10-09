# `figures/ch39/`

Figure assets for chapter 39 of "The AIS Handbook", an open, citable handbook
on the maritime Automatic Identification System. This directory holds the
rendered SVG figure(s) that the chapter's text references; the chapter's
subject, judging from the single figure here, is satellite AIS (S-AIS)
reception and why a satellite's radio footprint covers vastly more ships, and
therefore more overlapping SOTDMA slot transmissions, than a shore station.

The SVG was produced by Matplotlib (v3.11.2, dated 2026-10-04 in its metadata),
so it is a generated artifact rather than a hand-drawn illustration.

## Files
| File | Summary |
|---|---|
| `footprint.svg` | Matplotlib-generated plot titled "Why satellites see thousands of ships (and their slot collisions) at once". A square, equal-aspect plot with both axes in km (−3000 to 3000) showing three dashed concentric circles for satellite radio-horizon footprint radii (400 km altitude: r ≈ 2,201 km; 600 km: r ≈ 2,663 km; 800 km: r ≈ 3,038 km) and a tiny solid red dot at the origin representing a shore receiver with a 50 m mast (≈ 55 km range). A legend in the upper right labels all four. |

## Notes for agents
- `footprint.svg` is a generated figure, not a source file. If the numbers
  need to change, regenerate it from the producing script (not located in this
  directory) rather than hand-editing path coordinates in the SVG.
- The figure has no explicit x/y axis titles other than a single "km" label
  below the x-axis; the axes are offsets from the receiver at the origin.
- The visual point of the figure is the scale contrast: the shore-receiver
  footprint is drawn as a barely visible dot against satellite footprints
  with radii of ~2,200–3,000 km. Keep that contrast if restyling.
- Text in the SVG uses Unicode minus signs (−) and "≈"; preserve the UTF-8
  encoding if the file is touched.
- Font sizes are small (7–10.8 px) because the figure is sized at roughly
  398 × 279 pt for inline placement in the book.
