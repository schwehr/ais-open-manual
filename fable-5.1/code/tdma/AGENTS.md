# `code/tdma/`

Companion code for the link-layer / channel-access chapters of *The AIS
Handbook* (an open, citable handbook on the maritime Automatic Identification
System). The directory holds a single, deliberately small simulator of the AIS
TDMA slot map: Class A stations using SOTDMA-style slot reservation and Class B
"CS" stations using carrier-sense (CSTDMA) access, plus an optional jammer and
hidden-terminal model. It is a teaching model used to illustrate channel
loading, collisions, Class B deferral/starvation, and capacity degradation; it
is explicitly *not* a full implementation of ITU-R M.1371 Annex 2.

The module docstring references Chapters 21, 30, and 61 of the handbook as the
chapters this code supports.

## Files
| File | Summary |
|---|---|
| `sotdma_sim.py` | Standalone Python 3 script (stdlib only: `argparse`, `random`, `dataclasses`) simulating one AIS channel as a 2250-slot one-minute frame. Class A stations pick slots within ±10% of their reporting interval around a nominal slot, avoiding slots they heard in use; Class B stations scan 10 candidate slots and defer if none is free; a jammer can pre-occupy a fraction of slots. Prints a stats dict (transmissions, collisions, deferrals, occupancy, loss/defer rates) or, with `--sweep`, a table of Class A count vs. occupancy/loss/deferral to show saturation. |

## Notes for agents
- Run directly: `python3 code/tdma/sotdma_sim.py` (single scenario, prints a dict) or `python3 code/tdma/sotdma_sim.py --sweep` (sweeps `n_A` over 50–600 and prints a `n_A  occupancy  A_loss  B_defer` table). There are no external dependencies and no build step.
- CLI flags: `--n-a` (default 60), `--n-b` (default 40), `--ri-a` (Class A interval in slots, default 375 = 10 s), `--ri-b` (Class B interval in slots, default 1125 = 30 s), `--frames` (default 5), `--hidden` (probability a station cannot hear another, default 0.0), `--jam` (fraction of slots occupied by a jammer, default 0.0), `--sweep`.
- `run(...)` is the reusable entry point and takes a `seed` argument (default 1, uses its own `random.Random`), so results are deterministic for a given parameter set — useful if other chapters or tests want reproducible numbers. Note `main()` does not expose `seed` on the CLI.
- Model simplifications to keep in mind when editing or quoting results: only one channel is modeled (`SLOTS = 2250`; real AIS alternates two channels for 4500 slots/min); Class A stations are processed before all Class B stations within a frame; reservations do not persist across frames (`Station.reserved` is declared but unused); the selection interval is `max(1, int(0.1 * ri))`; if no free candidate exists a Class A station is forced to reuse a busy slot.
- Collision accounting: `a_collided` counts every non-jammer user in any slot with more than one occupant (including Class B stations and slots shared with the jammer), despite its name. Keep this in mind if you change the statistics or describe them in prose.
- The docstring says "no transmit code — just slot bookkeeping"; keep the script as a pure bookkeeping model rather than adding RF or bit-level behaviour (that belongs under `code/rf/`).
- Sibling directories at `code/` level are `analytics/`, `decode/`, `figures/`, `rf/`, `security/`, `tests/`, and `viz/`; this directory has no subdirectories and no tests of its own.
