#!/usr/bin/env python3
"""Generate a small, fully synthetic AIS sample set (NMEA with TAG blocks + CSV truth).

Why synthetic: it is redistributable without licence questions, and the ground
truth is known exactly, which the coverage/cleaning examples rely on.

Output:
  data/samples/synthetic_harbor.nmea   TAG-blocked !AIVDM sentences (Messages 1, 4, 5, 18, 21, 24)
  data/samples/synthetic_harbor_truth.csv   per-report truth (mmsi, t, lat, lon, sog, cog, heading)

Scenario (60 minutes, 2026-01-15 12:00Z, fictional harbour approach near 42.35N, -70.9W):
  - 4 Class A ships (Message 1 every 10 s underway, Message 5 every 6 min)
  - 3 Class B craft (Message 18 every 30 s; Message 24 A/B every 6 min)
  - 1 base station (Message 4 every 10 s)
  - 2 AtoN (Message 21 every 3 min)
  - one receiver at (42.36, -70.95), 30 m; reports beyond a soft 25 nmi range are
    dropped with increasing probability to mimic coverage falloff;
  - one Class A unit has a deliberately wrong MMSI (all zeros) for 5 minutes and one
    Class B unit uses the infamous default 1193046 — for the data-quality chapter.
"""
import csv
import math
import pathlib
import random
from datetime import datetime, timedelta, timezone

from pyais.encode import encode_dict

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "samples"
RX = (42.36, -70.95)
T0 = datetime(2026, 1, 15, 12, 0, 0, tzinfo=timezone.utc)
random.seed(1371)

SHIPS = [
    # mmsi, name, callsign, type, dims(a,b,c,d), start(lat,lon), cog, sog, dest
    dict(mmsi=366999701, name="NEPTUNE TRADER", cs="WDX1234", type=70, dims=(150, 50, 15, 15), pos=(42.20, -70.60), cog=315.0, sog=12.0, dest="BOSTON"),
    dict(mmsi=338999702, name="HARBOR PILOT 2", cs="WDX2345", type=50, dims=(12, 6, 3, 3), pos=(42.34, -70.92), cog=120.0, sog=18.0, dest="PILOT STN"),
    dict(mmsi=244999703, name="ROTTERDAM EXPRESS", cs="PDAB", type=71, dims=(250, 90, 20, 22), pos=(42.10, -70.30), cog=330.0, sog=14.5, dest="BOSTON MA"),
    dict(mmsi=316999704, name="ACADIA FERRY", cs="CFA1", type=60, dims=(60, 25, 8, 8), pos=(42.38, -70.80), cog=90.0, sog=20.0, dest="PROVINCETOWN"),
]
CLASS_B = [
    dict(mmsi=338123456, name="SEA BISCUIT", pos=(42.33, -70.90), cog=200.0, sog=6.0),
    dict(mmsi=1193046,   name="DEFAULT MMSI", pos=(42.37, -70.93), cog=45.0, sog=4.5),   # default MMSI case
    dict(mmsi=338654321, name="FISH HAWK", pos=(42.45, -70.70), cog=270.0, sog=7.5),
]
ATONS = [
    dict(mmsi=993672001, name="BOSTON APPROACH LB B", pos=(42.3755, -70.7836), aton_type=19, virtual=0),
    dict(mmsi=993672002, name="VIRTUAL WRECK MARK", pos=(42.3300, -70.8500), aton_type=28, virtual=1),
]
BASE = dict(mmsi=3669712, pos=(42.3600, -70.9500))


def haversine_nmi(a, b):
    R = 3440.065
    p1, p2 = math.radians(a[0]), math.radians(b[0])
    dp, dl = math.radians(b[0] - a[0]), math.radians(b[1] - a[1])
    h = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def advance(pos, cog, sog_kn, dt_s):
    d_nmi = sog_kn * dt_s / 3600.0
    dlat = d_nmi / 60.0 * math.cos(math.radians(cog))
    dlon = d_nmi / 60.0 * math.sin(math.radians(cog)) / math.cos(math.radians(pos[0]))
    return (pos[0] + dlat, pos[1] + dlon)


def received(pos):
    """Soft coverage: p=1 inside 15 nmi, linear to 0 at 35 nmi."""
    r = haversine_nmi(RX, pos)
    p = 1.0 if r < 15 else max(0.0, 1 - (r - 15) / 20)
    return random.random() < p


def tag(t, sentence, station="SYNTH01"):
    body = f"s:{station},c:{int(t.timestamp())}"
    cks = 0
    for ch in body:
        cks ^= ord(ch)
    return f"\\{body}*{cks:02X}\\{sentence}"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    lines, truth = [], []
    for sec in range(0, 3600 + 1, 1):
        t = T0 + timedelta(seconds=sec)
        # Class A dynamic
        for i, s in enumerate(SHIPS):
            if sec % 10 == (i * 3) % 10:
                if sec > 0:
                    s["pos"] = advance(s["pos"], s["cog"], s["sog"], 10)
                    s["cog"] = (s["cog"] + random.uniform(-1.5, 1.5)) % 360
                mmsi = 0 if (s["mmsi"] == 366999701 and 600 <= sec < 900) else s["mmsi"]
                if received(s["pos"]):
                    msg = encode_dict(dict(msg_type=1, mmsi=mmsi, status=0, turn=0, speed=s["sog"],
                                           accuracy=1, lon=s["pos"][1], lat=s["pos"][0], course=s["cog"],
                                           heading=int(s["cog"]) % 360, second=t.second, maneuver=0, raim=0,
                                           radio=0), radio_channel="A", talker_id="AI", sentence_type="VDM")
                    for sent in msg:
                        lines.append(tag(t, sent))
                truth.append([mmsi, t.isoformat(), f"{s['pos'][0]:.5f}", f"{s['pos'][1]:.5f}", s["sog"], f"{s['cog']:.1f}", int(s["cog"]) % 360, "A"])
            if sec % 360 == (i * 90) % 360 and received(s["pos"]):
                a, b, c, d = s["dims"]
                msg = encode_dict(dict(msg_type=5, mmsi=s["mmsi"], ais_version=2, imo=9000000 + i, callsign=s["cs"],
                                       shipname=s["name"], ship_type=s["type"], to_bow=a, to_stern=b, to_port=c,
                                       to_starboard=d, epfd=1, month=1, day=16, hour=8, minute=0, draught=7.5 + i,
                                       destination=s["dest"], dte=0), radio_channel="B", talker_id="AI", sentence_type="VDM")
                for sent in msg:
                    lines.append(tag(t, sent))
        # Class B
        for i, s in enumerate(CLASS_B):
            if sec % 30 == (i * 10) % 30:
                if sec > 0:
                    s["pos"] = advance(s["pos"], s["cog"], s["sog"], 30)
                    s["cog"] = (s["cog"] + random.uniform(-4, 4)) % 360
                if received(s["pos"]):
                    msg = encode_dict(dict(msg_type=18, mmsi=s["mmsi"], speed=s["sog"], accuracy=0, lon=s["pos"][1],
                                           lat=s["pos"][0], course=s["cog"], heading=511, second=t.second, cs=1,
                                           display=0, dsc=1, band=1, msg22=0, assigned=0, raim=0, radio=0),
                                      radio_channel="A", talker_id="AI", sentence_type="VDM")
                    for sent in msg:
                        lines.append(tag(t, sent))
                truth.append([s["mmsi"], t.isoformat(), f"{s['pos'][0]:.5f}", f"{s['pos'][1]:.5f}", s["sog"], f"{s['cog']:.1f}", 511, "B"])
            if sec % 360 == (i * 120 + 60) % 360 and received(s["pos"]):
                for part, extra in ((0, dict(shipname=s["name"])),
                                    (1, dict(ship_type=37, vendorid="SYN", callsign="", to_bow=5, to_stern=5, to_port=2, to_starboard=2))):
                    msg = encode_dict(dict(msg_type=24, mmsi=s["mmsi"], partno=part, **extra), radio_channel="B", talker_id="AI", sentence_type="VDM")
                    for sent in msg:
                        lines.append(tag(t, sent))
        # Base station
        if sec % 10 == 0:
            msg = encode_dict(dict(msg_type=4, mmsi=BASE["mmsi"], year=t.year, month=t.month, day=t.day, hour=t.hour,
                                   minute=t.minute, second=t.second, accuracy=1, lon=BASE["pos"][1], lat=BASE["pos"][0],
                                   epfd=7, raim=0, radio=0), radio_channel="A", talker_id="AI", sentence_type="VDM")
            for sent in msg:
                lines.append(tag(t, sent))
        # AtoN
        for i, a in enumerate(ATONS):
            if sec % 180 == (i * 60) % 180:
                msg = encode_dict(dict(msg_type=21, mmsi=a["mmsi"], aid_type=a["aton_type"], name=a["name"], accuracy=1,
                                       lon=a["pos"][1], lat=a["pos"][0], to_bow=2, to_stern=2, to_port=2, to_starboard=2,
                                       epfd=1, second=t.second, off_position=0, reserved_1=0, raim=0, virtual_aid=a["virtual"],
                                       assigned=0), radio_channel="B", talker_id="AI", sentence_type="VDM")
                for sent in msg:
                    lines.append(tag(t, sent))

    (OUT / "synthetic_harbor.nmea").write_text("\n".join(lines) + "\n")
    with (OUT / "synthetic_harbor_truth.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["mmsi", "time", "lat", "lon", "sog", "cog", "heading", "class"])
        w.writerows(truth)
    print(f"wrote {len(lines)} sentences, {len(truth)} truth rows")


if __name__ == "__main__":
    main()
