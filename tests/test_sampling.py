import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "audit-engine"))

from sampler import select_sample
import pytest

SAMPLE_RECORDS = [
    {"population": "access", "record_id": "ACC-001"},
    {"population": "access", "record_id": "ACC-002"},
    {"population": "access", "record_id": "ACC-003"},
]
MARKER = "UBI-A7-598D6B60F230"


def test_positive_reproducible_sample():
    """Positive case: same marker, same input -> identical sample both times."""
    s1 = select_sample(SAMPLE_RECORDS, "access", MARKER, sample_size=2)
    s2 = select_sample(SAMPLE_RECORDS, "access", MARKER, sample_size=2)
    assert s1 == s2


def test_negative_mixed_population_rejected():
    """Negative case: mixed populations must raise, not silently sample across them."""
    mixed = [
        {"population": "access", "record_id": "ACC-001"},
        {"population": "training", "record_id": "TRN-101"},
    ]
    with pytest.raises(ValueError):
        select_sample(mixed, "access", MARKER, sample_size=1)


def test_malformed_wrong_population_name_rejected():
    """Malformed input: population_name that doesn't match the records' actual
    population must raise, catching a caller mistake early."""
    with pytest.raises(ValueError):
        select_sample(SAMPLE_RECORDS, "training", MARKER, sample_size=1)


def test_clean_state_sample_size_larger_than_population():
    """Clean-state / edge case: asking for more than exists must not crash,
    and must just return everything available."""
    result = select_sample(SAMPLE_RECORDS, "access", MARKER, sample_size=999)
    assert len(result) == len(SAMPLE_RECORDS)
