"""NMEA 4.10 TAG block parser (Chapter 26).

A TAG block precedes a sentence:  \\s:STATION,c:1768478400,n:42*5A\\!AIVDM,...
Fields: c = UNIX time (s or ms), d = destination, g = grouping "n-total-id",
n = line count, r = relative time, s = source station, t = text.
Checksum = XOR of all bytes between the backslashes, excluding '*hh'.
"""
from __future__ import annotations

import dataclasses
import re
from typing import Optional

TAG_RE = re.compile(r"^\\([^\\]*)\\(.*)$")


def nmea_checksum(s: str) -> int:
    c = 0
    for ch in s:
        c ^= ord(ch)
    return c


@dataclasses.dataclass
class TagBlock:
    unix_time: Optional[float] = None
    destination: Optional[str] = None
    group: Optional[tuple[int, int, int]] = None  # (index, total, id)
    line_count: Optional[int] = None
    relative_time: Optional[int] = None
    source: Optional[str] = None
    text: Optional[str] = None
    checksum_ok: bool = False
    raw: str = ""


def parse_line(line: str) -> tuple[Optional[TagBlock], str]:
    """Split a logged line into (TagBlock or None, sentence)."""
    line = line.rstrip("\r\n")
    m = TAG_RE.match(line)
    if not m:
        return None, line
    block, sentence = m.group(1), m.group(2)
    body, _, cks = block.partition("*")
    tb = TagBlock(raw=block)
    tb.checksum_ok = bool(cks) and nmea_checksum(body) == int(cks, 16)
    for field in body.split(","):
        if ":" not in field:
            continue
        k, v = field.split(":", 1)
        if k == "c":
            t = float(v)
            tb.unix_time = t / 1000.0 if t > 1e11 else t  # ms vs s heuristic
        elif k == "d":
            tb.destination = v
        elif k == "g":
            parts = v.split("-")
            if len(parts) == 3:
                tb.group = tuple(int(p) for p in parts)  # type: ignore[assignment]
        elif k == "n":
            tb.line_count = int(v)
        elif k == "r":
            tb.relative_time = int(v)
        elif k == "s":
            tb.source = v
        elif k == "t":
            tb.text = v
    return tb, sentence


def format_tag(unix_time: Optional[float] = None, source: Optional[str] = None,
               group: Optional[tuple[int, int, int]] = None, line_count: Optional[int] = None) -> str:
    fields = []
    if group:
        fields.append("g:%d-%d-%d" % group)
    if source:
        fields.append(f"s:{source}")
    if line_count is not None:
        fields.append(f"n:{line_count}")
    if unix_time is not None:
        fields.append(f"c:{int(unix_time)}")
    body = ",".join(fields)
    return f"\\{body}*{nmea_checksum(body):02X}\\"


if __name__ == "__main__":
    import sys
    for ln in sys.stdin:
        tb, s = parse_line(ln)
        print(tb, s)
