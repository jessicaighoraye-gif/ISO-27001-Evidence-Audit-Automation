import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "audit-engine"))

from collector import load_population_csv, generate_hash_manifest, verify_against_manifest, normalize_timestamp
import pytest

CSV_PATH = Path(__file__).resolve().parent.parent / "evidence-pack-source" / "audit-populations.csv"


def test_positive_valid_rows_loaded():
    """Positive case: a real, well-formed CSV loads valid records."""
    result = load_population_csv(CSV_PATH)
    assert len(result["valid_records"]) > 0


def test_negative_duplicate_excluded():
    """Negative case: the known ACC-004 duplicate must be excluded, not silently kept."""
    result = load_population_csv(CSV_PATH)
    excluded_ids = [item["record"]["record_id"] for item in result["excluded_records"]]
    assert "ACC-004" in excluded_ids


def test_malformed_timestamp_rejected():
    """Malformed input: a timestamp with no timezone must raise, not silently pass through."""
    with pytest.raises(ValueError):
        normalize_timestamp("2026-07-01T08:00:00")  # no timezone info


def test_clean_state_hash_manifest(tmp_path):
    """Clean-state: hash verification must not depend on leftover files from a previous run."""
    manifest_path = tmp_path / "manifest.json"
    generate_hash_manifest([CSV_PATH], manifest_path)
    matches, expected, actual = verify_against_manifest(CSV_PATH, manifest_path)
    assert matches is True
