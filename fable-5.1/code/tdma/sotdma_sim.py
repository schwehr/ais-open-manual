#!/usr/bin/env python3
"""A deliberately small SOTDMA / CSTDMA slot-map simulator (Chapters 21, 30, 61).

Model (one channel, one minute frame = 2250 slots; AIS alternates two channels so
real capacity is 4500 slots/min):
  * Class A stations use SOTDMA: each picks a nominal slot and a reporting
    interval (RI, in slots); candidate slots are chosen in a selection interval
    of ±10% RI around the nominal; stations avoid slots they *heard* used
    (perfect knowledge within a cell, i.e., no hidden terminals unless
    `hidden_fraction` > 0).
  * Class B "CS" stations carrier-sense: they look for a free slot among 10
    candidates in a selection window and transmit only if no one else is heard
    there; otherwise they defer (starvation accounting).
  * A "jammer" can occupy a fraction of slots to show capacity degradation
    (no transmit code — just slot bookkeeping).

Outputs loss statistics: Class A collisions, Class B deferrals, slot occupancy.
This is a teaching model, not ITU-R M.1371 Annex 2 in full.
"""
from __future__ import annotations

import argparse
import random
from dataclasses import dataclass, field

SLOTS = 2250


@dataclass
class Station:
    sid: int
    cls: str            # "A" or "B"
    ri: int             # reporting interval in slots (A: 2 s => 75 slots; 10 s => 375)
    nominal: int = 0
    reserved: dict = field(default_factory=dict)   # slot -> timeout


def run(n_a=60, n_b=40, ri_a=375, ri_b=1125, frames=5, hidden_fraction=0.0, jam_fraction=0.0, seed=1):
    rnd = random.Random(seed)
    stations = [Station(i, "A", ri_a, rnd.randrange(SLOTS)) for i in range(n_a)]
    stations += [Station(1000 + i, "B", ri_b, rnd.randrange(SLOTS)) for i in range(n_b)]
    # hidden terminal matrix: station i cannot hear station j with prob hidden_fraction
    hidden = {(s.sid, t.sid) for s in stations for t in stations if s is not t and rnd.random() < hidden_fraction}

    stats = dict(a_tx=0, a_collided=0, b_tx=0, b_deferred=0, slots_used=0, slots_jammed=0)
    for _ in range(frames):
        slot_map: dict[int, list[int]] = {}   # slot -> [sids]
        jammed = set(rnd.sample(range(SLOTS), int(SLOTS * jam_fraction)))
        for s in jammed:
            slot_map.setdefault(s, []).append(-1)
        stats["slots_jammed"] += len(jammed)

        def heard_busy(me: Station, slot: int) -> bool:
            for sid in slot_map.get(slot, []):
                if sid == -1 or (me.sid, sid) not in hidden:
                    return True
            return False

        # Class A: SOTDMA-like
        for st in stations:
            if st.cls != "A":
                continue
            t = st.nominal
            while t < SLOTS:
                si = max(1, int(0.1 * st.ri))
                cands = [(t + d) % SLOTS for d in range(-si, si + 1)]
                free = [c for c in cands if not heard_busy(st, c)]
                chosen = rnd.choice(free) if free else rnd.choice(cands)  # forced reuse if none free
                slot_map.setdefault(chosen, []).append(st.sid)
                stats["a_tx"] += 1
                t += st.ri
        # Class B: CSTDMA-like
        for st in stations:
            if st.cls != "B":
                continue
            t = st.nominal
            while t < SLOTS:
                cands = [(t + d) % SLOTS for d in range(0, 10)]
                free = [c for c in cands if not heard_busy(st, c)]
                if free:
                    slot_map.setdefault(free[0], []).append(st.sid)
                    stats["b_tx"] += 1
                else:
                    stats["b_deferred"] += 1
                t += st.ri
        for slot, users in slot_map.items():
            real = [u for u in users if u != -1]
            if real:
                stats["slots_used"] += 1
            if len(users) > 1:
                stats["a_collided"] += sum(1 for u in real)
    occ = stats["slots_used"] / (SLOTS * frames)
    return {**stats, "occupancy": round(occ, 3),
            "a_loss_rate": round(stats["a_collided"] / max(1, stats["a_tx"]), 3),
            "b_defer_rate": round(stats["b_deferred"] / max(1, stats["b_tx"] + stats["b_deferred"]), 3)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-a", type=int, default=60)
    ap.add_argument("--n-b", type=int, default=40)
    ap.add_argument("--ri-a", type=int, default=375, help="Class A interval in slots (375 = 10 s)")
    ap.add_argument("--ri-b", type=int, default=1125, help="Class B interval in slots (1125 = 30 s)")
    ap.add_argument("--frames", type=int, default=5)
    ap.add_argument("--hidden", type=float, default=0.0)
    ap.add_argument("--jam", type=float, default=0.0)
    ap.add_argument("--sweep", action="store_true", help="sweep Class A count to show saturation")
    a = ap.parse_args()
    if a.sweep:
        print("n_A  occupancy  A_loss  B_defer")
        for n in (50, 100, 200, 300, 400, 500, 600):
            r = run(n, a.n_b, a.ri_a, a.ri_b, a.frames, a.hidden, a.jam)
            print(f"{n:4d}  {r['occupancy']:.3f}     {r['a_loss_rate']:.3f}   {r['b_defer_rate']:.3f}")
    else:
        print(run(a.n_a, a.n_b, a.ri_a, a.ri_b, a.frames, a.hidden, a.jam))


if __name__ == "__main__":
    main()
