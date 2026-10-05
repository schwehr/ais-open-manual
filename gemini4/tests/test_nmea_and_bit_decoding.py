#!/usr/bin/env python3
"""Unit tests for AIS NMEA 0183 framing, 6-bit ASCII armor, two's complement
bit extraction, nonlinear Rate of Turn (ROT), HDLC CRC-16/bit-stuffing,
and IMO 7-digit hull number check-digit verification (TASK-801).
"""

import math
import unittest


def nmea_checksum(sentence_body: str) -> str:
  """Computes the 2-hex-digit XOR checksum between '!' or '$' and '*'."""
  xor_val = 0
  for ch in sentence_body:
    xor_val ^= ord(ch)
  return f"{xor_val:02X}"


def verify_nmea_sentence(sentence: str) -> bool:
  """Verifies an NMEA 0183 sentence with optional TAG block."""
  s = sentence.strip()
  if s.startswith("\\"):
    end_tag = s.find("\\", 1)
    if end_tag == -1:
      return False
    tag_block = s[1:end_tag]
    if "*" in tag_block:
      tag_body, tag_cs = tag_block.rsplit("*", 1)
      if nmea_checksum(tag_body) != tag_cs.upper():
        return False
    s = s[end_tag + 1 :]
  if not (s.startswith("!") or s.startswith("$")) or "*" not in s:
    return False
  body, cs = s[1:].rsplit("*", 1)
  return nmea_checksum(body) == cs.upper()


def armor_to_bits(payload: str, fill_bits: int = 0) -> str:
  """De-armors NMEA 6-bit ASCII payload string into MSB-first bit string."""
  bits = []
  for ch in payload:
    val = ord(ch) - 48
    if val > 40:
      val -= 8
    if not (0 <= val <= 63):
      raise ValueError(f"Invalid 6-bit ASCII armor character: {ch!r}")
    bits.append(f"{val:06b}")
  bit_str = "".join(bits)
  if fill_bits > 0:
    bit_str = bit_str[:-fill_bits]
  return bit_str


def bits_to_armor(bit_str: str) -> tuple[str, int]:
  """Packs MSB-first bit string into NMEA 6-bit ASCII armor and fill_bits."""
  rem = len(bit_str) % 6
  fill_bits = (6 - rem) % 6
  padded = bit_str + ("0" * fill_bits)
  chars = []
  for i in range(0, len(padded), 6):
    val = int(padded[i : i + 6], 2)
    ascii_val = val + 48 if val < 40 else val + 56
    chars.append(chr(ascii_val))
  return "".join(chars), fill_bits


def extract_uint(bit_str: str, start: int, width: int) -> int:
  """Extracts an unsigned integer from 0-based MSB-first bit slice."""
  return int(bit_str[start : start + width], 2)


def extract_int(bit_str: str, start: int, width: int) -> int:
  """Extracts a two's complement signed integer from 0-based MSB-first slice."""
  val = extract_uint(bit_str, start, width)
  if val >= (1 << (width - 1)):
    val -= 1 << width
  return val


def decode_rot_ais_to_deg_per_min(rot_ais: int) -> float | None:
  """Converts 8-bit signed AIS ROT_AIS to physical deg/min per ITU-R M.1371-5."""
  if rot_ais == -128:
    return None  # Not available
  if rot_ais == 127:
    return math.inf  # Turning right > 5 deg/30s without TI
  if rot_ais == -127:
    return -math.inf  # Turning left > 5 deg/30s without TI
  sign = 1.0 if rot_ais >= 0 else -1.0
  return sign * ((rot_ais / 4.733) ** 2)


def encode_deg_per_min_to_rot_ais(rot_deg_min: float | None) -> int:
  """Encodes physical deg/min into 8-bit signed AIS ROT_AIS."""
  if rot_deg_min is None:
    return -128
  sign = 1 if rot_deg_min >= 0 else -1
  val = round(4.733 * math.sqrt(abs(rot_deg_min)))
  val = min(val, 126)
  return sign * val


def validate_imo_number(imo: int | str) -> bool:
  """Validates a 7-digit IMO ship identification number check digit."""
  s = str(imo).strip().upper()
  if s.startswith("IMO"):
    s = s[3:].strip()
  if len(s) != 7 or not s.isdigit():
    return False
  digits = [int(d) for d in s]
  if digits[0] == 0:
    return False
  weighted_sum = sum(digits[i] * (7 - i) for i in range(6))
  return (weighted_sum % 10) == digits[6]


def crc16_ccitt_ais(payload_bits: str) -> str:
  """Computes 16-bit HDLC CRC-CCITT (0x1021, init 0xFFFF, inverted) on bit string."""
  crc = 0xFFFF
  for b_ch in payload_bits:
    bit = int(b_ch)
    xor_flag = ((crc >> 15) & 1) ^ bit
    crc = ((crc << 1) & 0xFFFF) ^ (0x1021 if xor_flag else 0)
  crc ^= 0xFFFF
  return f"{crc:016b}"


def hdlc_bit_stuff(bits: str) -> str:
  """Inserts a 0 bit after every five consecutive 1 bits."""
  out = []
  ones = 0
  for b in bits:
    out.append(b)
    if b == "1":
      ones += 1
      if ones == 5:
        out.append("0")
        ones = 0
    else:
      ones = 0
  return "".join(out)


def hdlc_bit_unstuff(stuffed_bits: str) -> str:
  """Removes stuffed 0 bit following five consecutive 1 bits."""
  out = []
  ones = 0
  i = 0
  while i < len(stuffed_bits):
    b = stuffed_bits[i]
    out.append(b)
    if b == "1":
      ones += 1
      if ones == 5:
        i += 1
        if i >= len(stuffed_bits) or stuffed_bits[i] != "0":
          raise ValueError("Invalid HDLC bit-stuffed stream (flag or abort)")
        ones = 0
    else:
      ones = 0
    i += 1
  return "".join(out)


class TestNmeaAndBitDecoding(unittest.TestCase):

  def test_canonical_msg1_aivdm(self):
    # Canonical ITU-R M.1371 Class A Position Report (Message 1)
    tag_body = "s:uscg-nais,c:1711430000"
    tag_cs = nmea_checksum(tag_body)
    sentence = (
        f"\\{tag_body}*{tag_cs}\\!AIVDM,1,1,,B,15M67FC000G?ufbE`FepT@3n00Sa,0*5C"
    )
    self.assertTrue(verify_nmea_sentence(sentence))
    payload = "15M67FC000G?ufbE`FepT@3n00Sa"
    bits = armor_to_bits(payload, fill_bits=0)
    self.assertEqual(len(bits), 168)

    # Round-trip 6-bit ASCII armor
    re_armored, fill = bits_to_armor(bits)
    self.assertEqual(re_armored, payload)
    self.assertEqual(fill, 0)

    # Extract standard Message 1 fields
    msg_id = extract_uint(bits, 0, 6)
    repeat = extract_uint(bits, 6, 2)
    mmsi = extract_uint(bits, 8, 30)
    nav_status = extract_uint(bits, 38, 4)
    rot_raw = extract_int(bits, 42, 8)
    sog_raw = extract_uint(bits, 50, 10)
    pos_acc = extract_uint(bits, 60, 1)
    lon_raw = extract_int(bits, 61, 28)
    lat_raw = extract_int(bits, 89, 27)
    cog_raw = extract_uint(bits, 116, 12)
    hdg_raw = extract_uint(bits, 128, 9)

    self.assertEqual(msg_id, 1)
    self.assertEqual(repeat, 0)
    self.assertEqual(mmsi, 366053209)
    self.assertEqual(nav_status, 3)
    self.assertEqual(rot_raw, 0)
    self.assertEqual(decode_rot_ais_to_deg_per_min(rot_raw), 0.0)
    self.assertIsNone(decode_rot_ais_to_deg_per_min(-128))
    self.assertAlmostEqual(sog_raw / 10.0, 0.0)
    self.assertEqual(pos_acc, 0)
    self.assertAlmostEqual(lon_raw / 600000.0, -122.341618, places=4)
    self.assertAlmostEqual(lat_raw / 600000.0, 37.802118, places=4)
    self.assertTrue(0.0 <= cog_raw / 10.0 <= 360.0)
    self.assertTrue(0 <= hdg_raw <= 511)

  def test_twos_complement_sentinels(self):
    # Longitude sentinel: 181.0 deg = 108,600,000 = 0x6791AC0 (28 bits)
    lon_na_bits = f"{108600000:028b}"
    self.assertAlmostEqual(extract_int(lon_na_bits, 0, 28) / 600000.0, 181.0)
    # Latitude sentinel: 91.0 deg = 54,600,000 = 0x3412140 (27 bits)
    lat_na_bits = f"{54600000:027b}"
    self.assertAlmostEqual(extract_int(lat_na_bits, 0, 27) / 600000.0, 91.0)
    # Negative coordinate (-122.5 deg = -73,500,000)
    neg_lon_raw = (1 << 28) - 73500000
    neg_lon_bits = f"{neg_lon_raw:028b}"
    self.assertAlmostEqual(extract_int(neg_lon_bits, 0, 28) / 600000.0, -122.5)

  def test_rot_nonlinear_formula(self):
    for deg_min in [0.0, 10.0, -25.0, 100.0, -400.0]:
      encoded = encode_deg_per_min_to_rot_ais(deg_min)
      decoded = decode_rot_ais_to_deg_per_min(encoded)
      self.assertIsNotNone(decoded)
      # Within quantization tolerance of 8-bit square-root compression
      self.assertAlmostEqual(decoded, deg_min, delta=max(1.0, abs(deg_min) * 0.05))

  def test_imo_check_digit(self):
    # IMO 9074729 (canonical IMO check-digit example: 9*7+0*6+7*5+4*4+7*3+2*2 = 139 -> 9)
    self.assertTrue(validate_imo_number("IMO9074729"))
    self.assertTrue(validate_imo_number(9811000))  # Ever Given (9*7+8*6+1*5+1*4 = 120 -> 0)
    self.assertFalse(validate_imo_number(9811001))
    self.assertFalse(validate_imo_number(12345))

  def test_hdlc_crc_and_bit_stuffing(self):
    bits = armor_to_bits("15M67FC000G?ufbE`FepT@3n00Sa", 0)
    fcs = crc16_ccitt_ais(bits)
    self.assertEqual(len(fcs), 16)
    stuffed = hdlc_bit_stuff(bits + fcs)
    self.assertNotIn("111111", stuffed)  # Never 6 consecutive ones!
    unstuffed = hdlc_bit_unstuff(stuffed)
    self.assertEqual(unstuffed, bits + fcs)


if __name__ == "__main__":
  unittest.main()
