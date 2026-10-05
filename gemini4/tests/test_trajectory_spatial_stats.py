#!/usr/bin/env python3
"""Unit tests for AIS spatial statistics: continuous-time trajectory residence
time integration vs. naive ping counting, and Horvitz-Thompson inverse
probability-of-detection weighting (TASK-802).
"""

import unittest


def integrate_segment_grid_residence(
    x0: float,
    y0: float,
    t0: float,
    x1: float,
    y1: float,
    t1: float,
    cell_size: float = 1000.0,
    steps: int = 200,
) -> dict[tuple[int, int], float]:
  """Integrates continuous residence time (seconds) of a linear trajectory

  segment across uniform 2D equal-area grid cells of width `cell_size`.
  """
  dt = (t1 - t0) / steps
  residence: dict[tuple[int, int], float] = {}
  for k in range(steps):
    alpha = (k + 0.5) / steps
    x = x0 + alpha * (x1 - x0)
    y = y0 + alpha * (y1 - y0)
    cell = (int(x // cell_size), int(y // cell_size))
    residence[cell] = residence.get(cell, 0.0) + dt
  return residence


def accumulate_trajectory_residence(
    pings: list[tuple[float, float, float]], cell_size: float = 1000.0
) -> dict[tuple[int, int], float]:
  """Computes total vessel-seconds per grid cell from variable-rate pings."""
  total: dict[tuple[int, int], float] = {}
  for i in range(len(pings) - 1):
    x0, y0, t0 = pings[i]
    x1, y1, t1 = pings[i + 1]
    seg_res = integrate_segment_grid_residence(x0, y0, t0, x1, y1, t1, cell_size)
    for cell, sec in seg_res.items():
      total[cell] = total.get(cell, 0.0) + sec
  return total


def horvitz_thompson_vessel_hours(
    pings: list[tuple[float, float, float, float, float]]
) -> dict[tuple[int, int], float]:
  """Horvitz-Thompson inverse-detection-probability estimator.

  Each ping is (x, y, nominal_dt_sec, p_rf_coverage, p_vdl_no_collision).
  Returns estimated vessel-seconds in cell (0, 0).
  """
  est: dict[tuple[int, int], float] = {}
  for x, y, dt_nom, p_rf, p_vdl in pings:
    p_det = p_rf * p_vdl
    if p_det <= 0.0:
      raise ValueError("Detection probability must be strictly positive")
    cell = (int(x // 1000.0), int(y // 1000.0))
    est[cell] = est.get(cell, 0.0) + (dt_nom / p_det)
  return est


class TestTrajectorySpatialStats(unittest.TestCase):

  def test_reporting_rate_invariance_vs_naive_ping_bias(self):
    # Vessel A traverses a 1000 m cell at 10 m/s (100 s duration) reporting every 2 seconds (50 pings)
    pings_fast_rate = [(t * 10.0, 500.0, float(t)) for t in range(0, 101, 2)]
    # Vessel B traverses the exact same 1000 m cell at 10 m/s (100 s duration) reporting every 25 seconds (5 pings)
    pings_slow_rate = [(t * 10.0, 500.0, float(t)) for t in range(0, 101, 25)]

    # Naive ping count is biased by 10x (51 vs 5)
    self.assertEqual(len(pings_fast_rate), 51)
    self.assertEqual(len(pings_slow_rate), 5)

    # Continuous-time residence integration yields identical 100.0 vessel-seconds for both!
    res_a = accumulate_trajectory_residence(pings_fast_rate, cell_size=1000.0)
    res_b = accumulate_trajectory_residence(pings_slow_rate, cell_size=1000.0)
    self.assertAlmostEqual(res_a[(0, 0)], 100.0, places=3)
    self.assertAlmostEqual(res_b[(0, 0)], 100.0, places=3)

  def test_horvitz_thompson_packet_loss_correction(self):
    # Suppose a vessel spends 3,600 seconds in cell (0,0) transmitting every 10 s (360 bursts),
    # but p_rf = 0.8 and p_vdl = 0.5 (so combined detection probability p_det = 0.4 -> 144 received pings).
    received_pings = [
        (500.0, 500.0, 10.0, 0.8, 0.5) for _ in range(int(360 * 0.4))
    ]
    ht_est = horvitz_thompson_vessel_hours(received_pings)
    self.assertAlmostEqual(ht_est[(0, 0)], 3600.0, places=3)


if __name__ == "__main__":
  unittest.main()
