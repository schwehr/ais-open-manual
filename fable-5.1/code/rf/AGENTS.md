# `code/rf/`

Radio-frequency companion scripts for "The AIS Handbook", an open, citable
handbook on the maritime Automatic Identification System. The three Python
scripts here back the physical-layer and propagation chapters: a NumPy-only
GMSK burst synthesiser/demodulator (Chapters 28, 34), a 162 MHz radio-horizon
and link-budget calculator (Chapters 27, 29, 39), and a tool that compares
empirical reception rates from an NMEA log against free-space / two-ray
predictions (Chapter 29).

The scripts are standalone command-line tools (standard library + NumPy; the
propagation comparison additionally depends on pandas via the sibling
`code/analytics/` modules). They exist so that numbers and figures quoted in
the text can be reproduced by readers.

## Files
| File | Summary |
|---|---|
| `gmsk_demo.py` | Builds a 256-bit AIS burst (ramp-up, 24-bit training, 0x7E flags, 168 payload bits, CRC-16/CCITT, HDLC bit stuffing), NRZI-encodes it, GMSK-modulates it (BT=0.4, h=0.5), adds AWGN, then demodulates with a frequency discriminator and reports raw BER and whether the CRC checks. Can optionally dump complex64 baseband samples to a `.cf32` file; exits 0 on CRC success, 1 otherwise. |
| `linkbudget.py` | Helpers for AIS at 162 MHz: 4/3-Earth radio horizon (`4.12*(sqrt(h1)+sqrt(h2))` km), free-space path loss, flat-sea two-ray loss, watts→dBm, and a `link_budget()` function returning a dict including margin against a -107 dBm sensitivity. CLI prints a single-distance budget with `--d` or a range sweep (5–100 km) by default. |
| `propagation_compare.py` | Decodes an NMEA file, computes range of each Class A position report (types 1–3) to a receiver, bins by range, and prints the fraction of expected reports actually received alongside predicted received power and two-ray margin, flagging bins that look like ducting or shadowing. |

## Notes for agents
- **Legal/safety:** `gmsk_demo.py` writes baseband samples to a *file only*. Its
  docstring explicitly states it must never be connected to a transmitter;
  do not add any SDR transmit path.
- `propagation_compare.py` imports from `linkbudget.py` (same directory) and
  from `../analytics/` (`moving_pandas_pipeline.decode_file`,
  `coverage_estimate.haversine_nmi`, `coverage_estimate.nominal_interval_s`)
  by inserting both directories into `sys.path`. Changes to those analytics
  modules' function names or the decoded DataFrame columns (`type`, `lat`,
  `lon`, `t`, `sog`, `status`, `mmsi`) will break this script.
- The "auto" propagation model in `linkbudget.link_budget()` uses
  `max(FSPL, two-ray)`, on the reasoning that two-ray cannot be lower-loss than
  free space in the far field. `propagation_compare.py` applies the same rule
  inline.
- The -107 dBm sensitivity figure is described in `linkbudget.py` as the
  IEC 61993-2 20% PER requirement with a note to "verify exact clause in the
  chapter"; keep the code and chapter text consistent if either changes.
- Constants: `BIT_RATE = 9600`, `BT = 0.4`, `H = 0.5` in `gmsk_demo.py`;
  `F_MHZ = 162.0`, `KM_PER_NMI = 1.852` in `linkbudget.py`.
- Burst layout per ITU-R M.1371 Annex 2 is documented in the `gmsk_demo.py`
  docstring; the demodulator assumes a known start offset (8+24+8 bits) rather
  than searching for the start flag.
- Run examples (from repo root):
  - `python code/rf/gmsk_demo.py --snr-db 15 --sps 8 [--out burst.cf32]`
  - `python code/rf/linkbudget.py` (sweep) or `python code/rf/linkbudget.py --d 40 --model two_ray`
  - `python code/rf/propagation_compare.py data/samples/synthetic_harbor.nmea --rx 42.36 -70.95 --hrx 30 --htx 20`
- There are no tests in this directory; see `code/tests/` for the repository's
  test suite.
