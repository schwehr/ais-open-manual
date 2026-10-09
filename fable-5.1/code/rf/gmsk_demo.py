#!/usr/bin/env python3
"""GMSK burst synthesis and demodulation in NumPy (Chapter 28, 34).

LEGAL NOTE: this script writes complex baseband samples to a .npy/.cf32 FILE ONLY.
It must not be connected to a transmitter. Transmitting on AIS frequencies
without authorization is unlawful in essentially every jurisdiction.

Pipeline
  bits -> HDLC bit-stuffing (insert 0 after five 1s) -> NRZI -> GMSK (BT=0.4, h=0.5)
       -> AWGN -> frequency discriminator -> NRZI decode -> unstuff -> compare

AIS burst layout (ITU-R M.1371, Annex 2): 8 bits ramp-up, 24 training (0101...),
8 start flag 0x7E, 168 data (Message 1), 16 CRC-16/CCITT, 8 end flag, 24 buffer
= 256 bits in one 26.67 ms slot at 9600 bit/s.
"""
from __future__ import annotations

import argparse
import math

import numpy as np

BIT_RATE = 9600
BT = 0.4
H = 0.5


def crc16_ccitt(bits: np.ndarray) -> np.ndarray:
    """CRC-16/CCITT as used by HDLC (poly 0x1021, init 0xFFFF, final XOR 0xFFFF), bits MSB-first per byte."""
    data = np.packbits(bits)
    crc = 0xFFFF
    for b in data:
        crc ^= int(b) << 8
        for _ in range(8):
            crc = ((crc << 1) ^ 0x1021) & 0xFFFF if crc & 0x8000 else (crc << 1) & 0xFFFF
    crc ^= 0xFFFF
    return np.array([(crc >> (15 - i)) & 1 for i in range(16)], dtype=np.uint8)


def bit_stuff(bits):
    out, run = [], 0
    for b in bits:
        out.append(b)
        run = run + 1 if b else 0
        if run == 5:
            out.append(0)
            run = 0
    return np.array(out, dtype=np.uint8)


def bit_unstuff(bits):
    out, run = [], 0
    i = 0
    while i < len(bits):
        b = bits[i]
        out.append(b)
        run = run + 1 if b else 0
        if run == 5:
            i += 1  # skip stuffed zero
            run = 0
        i += 1
    return np.array(out, dtype=np.uint8)


def nrzi_encode(bits):
    level, out = 1, []
    for b in bits:
        if b == 0:
            level ^= 1
        out.append(level)
    return np.array(out, dtype=np.uint8)


def nrzi_decode(levels):
    prev = 1
    out = []
    for l in levels:
        out.append(1 if l == prev else 0)
        prev = l
    return np.array(out, dtype=np.uint8)


def gaussian_taps(sps, bt=BT, span=3):
    t = np.arange(-span * sps, span * sps + 1) / sps
    a = math.sqrt(math.log(2) / 2) / bt
    g = (math.sqrt(math.pi) / a) * np.exp(-(np.pi * t / a) ** 2)
    return g / g.sum()


def gmsk_modulate(levels, sps=8):
    nrz = 2.0 * levels.astype(float) - 1.0
    up = np.repeat(nrz, sps)
    freq = np.convolve(up, gaussian_taps(sps), mode="same")
    phase = np.cumsum(freq) * (np.pi * H / sps)
    return np.exp(1j * phase)


def gmsk_demod(iq, sps=8):
    d = np.angle(iq[1:] * np.conj(iq[:-1]))
    # simple matched-ish smoothing then symbol-centre sampling
    d = np.convolve(d, np.ones(sps) / sps, mode="same")
    samples = d[sps // 2::sps]
    return (samples > 0).astype(np.uint8)


def build_burst(payload_bits):
    training = np.tile([0, 1], 12)
    flag = np.array([0, 1, 1, 1, 1, 1, 1, 0], dtype=np.uint8)
    crc = crc16_ccitt(payload_bits)
    body = bit_stuff(np.concatenate([payload_bits, crc]))
    ramp = np.zeros(8, dtype=np.uint8)
    return np.concatenate([ramp, training, flag, body, flag]), len(body)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--snr-db", type=float, default=15.0)
    ap.add_argument("--sps", type=int, default=8)
    ap.add_argument("--out", default=None, help="write complex64 baseband to this .cf32 file (file only!)")
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    rng = np.random.default_rng(a.seed)
    payload = rng.integers(0, 2, 168, dtype=np.uint8)
    burst, body_len = build_burst(payload)
    levels = nrzi_encode(burst)
    iq = gmsk_modulate(levels, a.sps)
    noise = (rng.standard_normal(iq.shape) + 1j * rng.standard_normal(iq.shape)) / math.sqrt(2)
    iq_n = iq + noise * 10 ** (-a.snr_db / 20)
    if a.out:
        iq_n.astype(np.complex64).tofile(a.out)
    rx_levels = gmsk_demod(iq_n, a.sps)
    n = min(len(rx_levels), len(levels))
    rx_bits = nrzi_decode(rx_levels[:n])
    ber = np.mean(rx_bits[:n] != burst[:n])
    # locate start flag and check CRC
    start = 8 + 24 + 8
    body = bit_unstuff(rx_bits[start:start + body_len])
    ok = len(body) >= 184 and np.array_equal(crc16_ccitt(body[:168]), body[168:184])
    print(f"burst bits={len(burst)} (slot budget 256), SNR={a.snr_db} dB, raw BER={ber:.4f}, CRC ok={ok}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
