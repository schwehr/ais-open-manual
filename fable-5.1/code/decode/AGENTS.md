# `code/decode/`

Small, dependency-light Python helpers for the decoding chapters of *The AIS
Handbook*, an open, citable handbook on the maritime Automatic Identification
System. The directory covers the "wire format" side of AIS: parsing the NMEA
4.10 TAG block metadata that receivers prepend to `!AIVDM` sentences
(Chapter 26), and cross-checking several independent AIS decoders against the
same NMEA corpus (Chapter 44).

The scripts are intended to be run directly from the repository root against
sample data (default input is `data/samples/synthetic_harbor.nmea`) and to be
quoted or referenced from the book text as worked examples.

## Files
| File | Summary |
|---|---|
| `tagblock.py` | NMEA 4.10 TAG block parser. Defines `nmea_checksum()` (XOR of bytes), a `TagBlock` dataclass (`unix_time`, `destination`, `group`, `line_count`, `relative_time`, `source`, `text`, `checksum_ok`, `raw`), `parse_line()` which splits a logged line into `(TagBlock | None, sentence)`, and `format_tag()` which builds a checksummed `\...*hh\` prefix. Run as a script it parses stdin line by line and prints the result. |
| `compare_decoders.py` | Decodes the same NMEA file with pyais (required), libais (if importable) and gpsdecode (if on `PATH`), normalises each result to `type/mmsi/lat/lon/sog/cog/heading`, prints per-decoder message counts by type, and reports field differences versus pyais (tolerance 1e-4, first five diffs shown). |

## Notes for agents
- `compare_decoders.py` imports `parse_line` from `tagblock.py` via a
  `sys.path.insert` on its own directory, so the two files must stay
  side by side; there is no package `__init__.py`.
- Run from the repo root: `python code/decode/compare_decoders.py
  data/samples/synthetic_harbor.nmea` (the path argument is optional and
  defaults to that file). `tagblock.py` can be exercised with
  `python code/decode/tagblock.py < some.nmea`.
- Only `pyais` is a hard dependency (imported lazily inside `with_pyais`).
  `libais` (`import ais`, `ais.stream`) and `gpsdecode` (gpsd) are optional and
  reported as `not available` when missing. Field-by-field comparison is only
  attempted when a decoder returns the same number of messages as pyais.
- Field name mapping differs per decoder: pyais uses `msg_type/speed/course`,
  libais uses `id/x/y/sog/cog/true_heading` (note `x`=lon, `y`=lat), gpsdecode
  JSON uses `type/speed/course`. Keep the `COMMON` list and these mappings in
  sync if adding fields.
- TAG block parsing details worth preserving: checksum is computed over the
  text between the backslashes excluding `*hh`; the `c:` field is treated as
  milliseconds when the value exceeds `1e11`, otherwise seconds; `g:` is parsed
  as a 3-tuple `(index, total, id)` and silently ignored otherwise; unknown
  keys and fields without `:` are skipped. `format_tag()` emits fields in the
  order `g, s, n, c` and truncates `unix_time` to integer seconds.
- The docstrings tie the files to specific chapters (26 and 44); keep those
  references accurate if chapters are renumbered.
- There are no tests in this directory; repository tests live under
  `code/tests/`.
