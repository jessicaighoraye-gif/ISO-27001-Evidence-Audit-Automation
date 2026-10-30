from pathlib import Path
import yaml

RULES_PATH = Path(__file__).resolve().parent.parent / "evidence-pack-source" / "severity-rules.yaml"


def load_rules(rules_path=RULES_PATH):
    with open(rules_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def evaluate_condition(condition_name, facts):
    """
    Maps each rule's 'when' condition name to actual logic using the facts dict.
    Facts come from public_fixtures.json's 'facts' structure.
    """
    if condition_name == "required_control_design_missing":
        return facts["required_control_design_missing"]

    if condition_name == "failed_required_samples_gte_2_and_affected_units_gte_2":
        return facts["failed_required_samples"] >= 2 and facts["affected_units"] >= 2

    if condition_name == "prior_major_open_or_repeated":
        return facts["prior_major_open_or_repeated"]

    if condition_name == "failed_required_samples_gte_1":
        return facts["failed_required_samples"] >= 1

    if condition_name == "required_evidence_stale_missing_or_hash_failed":
        return facts["required_evidence_stale_missing_or_hash_failed"]

    if condition_name == "population_or_required_procedure_unavailable":
        return facts["population_or_required_procedure_unavailable"]

    if condition_name == "all_required_samples_pass_and_evidence_is_current_and_valid":
        return (
            facts["failed_required_samples"] == 0
            and not facts["required_evidence_stale_missing_or_hash_failed"]
            and not facts["required_control_design_missing"]
            and not facts["population_or_required_procedure_unavailable"]
        )

    raise ValueError(f"Unknown condition: {condition_name}")


def evaluate_verdict(facts, rules=None):
    """
    Applies severity-rules.yaml in first-match order.
    Returns the matching rule's id and verdict.
    """
    if rules is None:
        rules = load_rules()

    for rule in rules["rules"]:
        if evaluate_condition(rule["when"], facts):
            return {"rule_id": rule["id"], "verdict": rule["verdict"]}

    raise ValueError("No rule matched — this should never happen if CONFORMS is the correct catch-all.")
