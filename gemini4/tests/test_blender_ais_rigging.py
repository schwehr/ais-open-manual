#!/usr/bin/env python3
"""Unit tests for 3D Blender (`bpy`) AIS scene engineering: local tangent plane
(ENU) float32-safe coordinate centering, Message 5/24 hull dimension scaling,
GNSS antenna-reference-point pivot offsets, bow/stern sweep kinematics, and
COG vs. True Heading crabbing angles (TASK-803).
"""

import math
import struct
import unittest


WGS84_A = 6378137.0
WGS84_F = 1.0 / 298.257223563
WGS84_E2 = 2.0 * WGS84_F - WGS84_F**2


def geodetic_to_enu(
    lon_deg: float,
    lat_deg: float,
    h_m: float,
    lon0_deg: float,
    lat0_deg: float,
    h0_m: float = 0.0,
) -> tuple[float, float, float]:
  """Transforms WGS84 (lon, lat, h) to local East-North-Up (ENU) meters

  centered at (lon0, lat0, h0) for float32-safe Blender scene coordinates.
  """
  lat0 = math.radians(lat0_deg)
  lon0 = math.radians(lon0_deg)
  lat = math.radians(lat_deg)
  lon = math.radians(lon_deg)

  sin_lat0 = math.sin(lat0)
  cos_lat0 = math.cos(lat0)
  n0 = WGS84_A / math.sqrt(1.0 - WGS84_E2 * sin_lat0 * sin_lat0)
  m0 = (WGS84_A * (1.0 - WGS84_E2)) / (
      (1.0 - WGS84_E2 * sin_lat0 * sin_lat0) ** 1.5
  )

  east = (lon - lon0) * (n0 + h0_m) * cos_lat0
  north = (lat - lat0) * (m0 + h0_m)
  up = h_m - h0_m
  return east, north, up


def to_float32(val: float) -> float:
  """Simulates Blender's internal single-precision IEEE 754 float32 storage."""
  return struct.unpack("<f", struct.pack("<f", val))[0]


def compute_hull_antenna_rigging(
    to_bow: int, to_stern: int, to_port: int, to_starboard: int
) -> dict[str, float]:
  """Computes LOA, Beam, and geometric hull center offset relative to the

  GNSS antenna reference point in the ship's body frame (+x=stbd, +y=bow).
  """
  loa = float(to_bow + to_stern)
  beam = float(to_port + to_starboard)
  # If object origin (0,0) is placed at the GNSS antenna, the geometric center
  # of the hull bounding box sits at (dx_center, dy_center):
  dx_center = (to_starboard - to_port) / 2.0
  dy_center = (to_bow - to_stern) / 2.0
  return {
      "loa": loa,
      "beam": beam,
      "dx_center_from_antenna": dx_center,
      "dy_center_from_antenna": dy_center,
  }


def hull_point_enu(
    ant_east: float,
    ant_north: float,
    true_heading_deg: float,
    x_body_stbd: float,
    y_body_bow: float,
) -> tuple[float, float]:
  """Computes world ENU position of any point (x_body_stbd, y_body_bow) relative

  to the GNSS antenna at True Heading `true_heading_deg` (clockwise from North).
  """
  psi = math.radians(true_heading_deg)
  sin_p = math.sin(psi)
  cos_p = math.cos(psi)
  east = ant_east + x_body_stbd * cos_p + y_body_bow * sin_p
  north = ant_north - x_body_stbd * sin_p + y_body_bow * cos_p
  return east, north


def compute_crabbing_leeway_deg(cog_deg: float, true_heading_deg: float) -> float:
  """Computes signed crabbing/leeway angle (COG - True Heading) in [-180, 180]."""
  diff = (cog_deg - true_heading_deg + 180.0) % 360.0 - 180.0
  return diff


class TestBlenderAisRigging(unittest.TestCase):

  def test_float32_jitter_mitigation_with_local_enu(self):
    # Raw UTM Northing ~ 4,700,000.0 m moved by 0.15 m loses precision in float32:
    utm_n0 = 4700000.0
    utm_n1 = 4700000.15
    f32_utm_delta = to_float32(utm_n1) - to_float32(utm_n0)
    self.assertEqual(f32_utm_delta, 0.0)  # Complete quantization stall in raw UTM!

    # In centered ENU near (lon0=-70.3, lat0=42.4), a 0.15 m move retains < 0.0001 m accuracy in float32:
    _, n0, _ = geodetic_to_enu(-70.3, 42.4, 0.0, -70.3, 42.4)
    _, n1, _ = geodetic_to_enu(-70.3, 42.4 + (0.15 / 111080.0), 0.0, -70.3, 42.4)
    f32_enu_delta = to_float32(n1) - to_float32(n0)
    self.assertAlmostEqual(f32_enu_delta, 0.15, places=3)

  def test_antenna_offset_bow_sweep_during_turn(self):
    # 400 m ULCS container ship with GNSS antenna near the stern (to_bow=350m, to_stern=50m, to_port=30m, to_stbd=30m)
    rig = compute_hull_antenna_rigging(350, 50, 30, 30)
    self.assertEqual(rig["loa"], 400.0)
    self.assertEqual(rig["beam"], 60.0)
    self.assertEqual(rig["dx_center_from_antenna"], 0.0)
    self.assertEqual(rig["dy_center_from_antenna"], 150.0)

    # Even if the GNSS antenna remains stationary at (0, 0), a 30-degree yaw turn
    # sweeps the bow laterally by 350 * sin(30 deg) = 175.0 meters East!
    bow_e0, bow_n0 = hull_point_enu(0.0, 0.0, true_heading_deg=0.0, x_body_stbd=0.0, y_body_bow=350.0)
    bow_e1, bow_n1 = hull_point_enu(0.0, 0.0, true_heading_deg=30.0, x_body_stbd=0.0, y_body_bow=350.0)
    self.assertAlmostEqual(bow_e0, 0.0)
    self.assertAlmostEqual(bow_n0, 350.0)
    self.assertAlmostEqual(bow_e1, 175.0)
    self.assertAlmostEqual(bow_n1, 350.0 * math.cos(math.radians(30.0)))

  def test_crabbing_angle_wraparound(self):
    # Heading 355 deg, COG 005 deg -> +10 deg starboard leeway/crabbing
    self.assertAlmostEqual(compute_crabbing_leeway_deg(5.0, 355.0), 10.0)
    # Heading 005 deg, COG 355 deg -> -10 deg port leeway/crabbing
    self.assertAlmostEqual(compute_crabbing_leeway_deg(355.0, 5.0), -10.0)


if __name__ == "__main__":
  unittest.main()
