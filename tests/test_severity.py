import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "audit-engine"))

from severity_engine import evaluate_verdict, evaluate_condition
import pytest

FIXTURES_PATH = Path(__file__).resolve().parent.parent / "evidence-pack-source" / "public-fixtures.json"


def load_fixtures():
    with open(FIXTURES_PATH) as f:
        return json.load(f)["fixtures"]


@pytest.mark.parametrize("fixture", load_fixtures(), ids=lambda fx: fx["case_id"])
def test_positive_all_public_fixtures(fixture):
    """Positive case: every one of the 24 public fixtures must match exactly."""
    result = evaluate_verdict(fixture["facts"])
    assert result["rule_id"] == fixture["expected"]["rule_id"]
    assert result["verdict"] == fixture["expected"]["verdict"]


def test_negative_unknown_condition_raises():
    """Negative case: an unrecognized rule condition must raise, not silently pass."""
    with pytest.raises(ValueError):
        evaluate_condition("not_a_real_condition", {})


def test_malformed_missing_facts_key_raises():
    """Malformed input: facts missing a required key must raise, not crash unpredictably
    or silently produce a wrong verdict."""
    with pytest.raises(KeyError):
        evaluate_verdict({"required_control_design_missing": False})  # incomplete facts
