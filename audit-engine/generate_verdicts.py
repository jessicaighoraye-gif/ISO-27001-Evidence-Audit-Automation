import json
from pathlib import Path

from severity_engine import evaluate_verdict
from control_facts import TEST_FACTS

OUTPUT_PATH = Path(__file__).resolve().parent.parent / "evidence-verdicts.json"


def generate_all_verdicts():
    verdicts = []
    for test_id, entry in TEST_FACTS.items():
        result = evaluate_verdict(entry["facts"])
        verdicts.append({
            "test_id": test_id,
            "control_id": entry["control_id"],
            "rule_id": result["rule_id"],
            "verdict": result["verdict"],
            "failed_sample_ids": entry["failed_sample_ids"],
            "affected_unit_ids": entry["affected_unit_ids"],
            "evidence_locators": entry["evidence_locators"],
            "facts": entry["facts"],
        })
    return verdicts


if __name__ == "__main__":
    verdicts = generate_all_verdicts()
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(verdicts, f, indent=2)

    for v in verdicts:
        print(f"{v['test_id']} ({v['control_id']}): {v['rule_id']} -> {v['verdict']}")

    print(f"\nWrote {len(verdicts)} verdicts to {OUTPUT_PATH}")
