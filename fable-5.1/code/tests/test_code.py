"""Smoke tests for the handbook's runnable snippets (run: pytest -q code)."""
import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
SAMPLE = ROOT / "data/samples/synthetic_harbor.nmea"
TRUTH = ROOT / "data/samples/synthetic_harbor_truth.csv"
sys.path.insert(0, str(ROOT / "code/decode"))
sys.path.insert(0, str(ROOT / "code/analytics"))
sys.path.insert(0, str(ROOT / "code/rf"))
sys.path.insert(0, str(ROOT / "code/tdma"))


def run(*args):
    return subprocess.run([sys.executable, *map(str, args)], cwd=ROOT, capture_output=True, text=True)


def test_tagblock_roundtrip():
    from tagblock import format_tag, parse_line
    tag = format_tag(unix_time=1768478400, source="RX1", line_count=7)
    tb, s = parse_line(tag + "!AIVDM,1,1,,A,15MwpU@01prtlJ0H9J@<Can00000,0*25")
    assert tb.checksum_ok and tb.unix_time == 1768478400 and tb.source == "RX1" and tb.line_count == 7
    assert s.startswith("!AIVDM")


def test_tagblock_bad_checksum():
    from tagblock import parse_line
    tb, _ = parse_line("\\s:X,c:1*00\\!AIVDM,1,1,,A,1,0*00")
    assert tb is not None and not tb.checksum_ok


def test_sample_exists_and_decodes():
    assert SAMPLE.exists() and TRUTH.exists()
    from moving_pandas_pipeline import decode_file
    df = decode_file(SAMPLE)
    assert len(df) > 1900 and set(df["type"].unique()) >= {1, 4, 5, 18, 21, 24}
    assert df["t"].notna().all()


def test_pipeline_cleaning_and_trajectories():
    from moving_pandas_pipeline import clean, decode_file, trajectories
    pos, rep = clean(decode_file(SAMPLE))
    assert rep["vessels"] == 6            # MMSI 0 and 1193046 removed
    assert rep["dropped"] < 0.2 * rep["position_reports"]
    tc = trajectories(pos)
    assert len(tc) == 6


def test_linkbudget_numbers():
    from linkbudget import fspl_db, radio_horizon_km, two_ray_db
    assert abs(radio_horizon_km(30, 50) - 51.7) < 0.2
    assert abs(fspl_db(10) - 96.6) < 0.2
    assert two_ray_db(50, 30, 50) > fspl_db(50)   # two-ray loss exceeds free space at range


def test_gmsk_crc_roundtrip():
    r = run("code/rf/gmsk_demo.py", "--snr-db", "20")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "CRC ok=True" in r.stdout


def test_sotdma_saturation_monotonic():
    from sotdma_sim import run as sim
    low = sim(n_a=50, n_b=20, frames=2)
    high = sim(n_a=500, n_b=20, frames=2)
    assert low["occupancy"] < high["occupancy"]
    assert low["a_loss_rate"] <= high["a_loss_rate"]


def test_coverage_estimate_runs():
    r = run("code/analytics/coverage_estimate.py", SAMPLE, "--rx", "42.36", "-70.95", "--truth", TRUTH)
    assert r.returncode == 0, r.stderr
    assert "p_detect" in r.stdout and "against truth" in r.stdout


def test_duckdb_density_runs():
    r = run("code/analytics/duckdb_density.py", SAMPLE, "--rx", "42.36", "-70.95", "--limit", "3")
    assert r.returncode == 0, r.stderr
    assert "reports_corrected" in r.stdout


def test_kinematic_checks_flags_bad_mmsi():
    r = run("code/security/kinematic_checks.py", SAMPLE, "--rx", "42.36", "-70.95")
    assert r.returncode == 0, r.stderr
    assert "1193046" in r.stdout


def test_compare_decoders_runs():
    r = run("code/decode/compare_decoders.py", SAMPLE)
    assert r.returncode == 0, r.stderr
    assert "pyais" in r.stdout


def test_blender_scripts_parse_without_bpy():
    r = run("code/viz/blender_ais_animation.py", "--csv", TRUTH)
    assert r.returncode == 0 and "tracks" in r.stdout
    r = run("code/viz/blender_coverage_satpass.py")
    assert r.returncode == 0 and "footprint radius" in r.stdout


def test_blender_headless_if_available():
    if not shutil.which("blender"):
        import pytest
        pytest.skip("blender not installed")
    out = ROOT / ".cache" / "ais_anim.blend"
    out.parent.mkdir(exist_ok=True)
    r = subprocess.run(["blender", "--background", "--python", str(ROOT / "code/viz/blender_ais_animation.py"), "--",
                        "--csv", str(TRUTH), "--out", str(out)], capture_output=True, text=True, cwd=ROOT)
    assert r.returncode == 0 and out.exists()
