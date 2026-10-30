""""
18 tests across 12 controls: original 12 (AT-01 to AT-12, one per
control, matching audit-test-sheet.csv's template) plus 6 additional
operating-effectiveness tests (AT-13 to AT-18) resolving the 12-vs-18
gap between the template and the narrative files (brief.md,
Build_sequence_, Project_faq, etc.), each using a DISTINCT evidence-pack
fact from its sibling test on the same control.
"""

DEFAULT_FACTS = {
    "affected_units": 0,
    "failed_required_samples": 0,
    "population_or_required_procedure_unavailable": False,
    "prior_major_open_or_repeated": False,
    "required_control_design_missing": False,
    "required_evidence_stale_missing_or_hash_failed": False,
}


def facts_for(overrides):
    """Start from all-clear defaults, apply only what evidence-pack.md supports."""
    f = dict(DEFAULT_FACTS)
    f.update(overrides)
    return f


TEST_FACTS = {
    "AT-01": {
        "control_id": "A.5.15",
        "facts": facts_for({"failed_required_samples": 1, "affected_units": 1}),
        "failed_sample_ids": [],
        "affected_unit_ids": ["excluded-emergency-accounts"],
        "evidence_locators": ["evidence-pack.md::Identity export[bullet=3]"],
    },
    "AT-02": {
        "control_id": "A.5.16",
        "facts": facts_for({"failed_required_samples": 1, "affected_units": 1}),
        "failed_sample_ids": ["n.adamu", "vendor-backup"],
        "affected_unit_ids": ["n.adamu", "vendor-backup"],
        "evidence_locators": ["evidence-pack.md::Identity export[bullet=4]"],
    },
    "AT-03": {
        "control_id": "A.5.18",
        "facts": facts_for({"failed_required_samples": 2, "affected_units": 2}),
        "failed_sample_ids": ["IAM-4412", "IAM-5031"],
        "affected_unit_ids": ["IAM-4412", "IAM-5031"],
        "evidence_locators": [
            "evidence-pack.md::Access-review tickets[id=IAM-4412]",
            "evidence-pack.md::Access-review tickets[id=IAM-5031]",
        ],
    },
    "AT-04": {
        "control_id": "A.5.19",
        "facts": facts_for({"required_control_design_missing": True}),
        "failed_sample_ids": [],
        "affected_unit_ids": ["HelpSphere"],
        "evidence_locators": ["evidence-pack.md::Supplier evidence[bullet=3]"],
    },
    "AT-05": {
        "control_id": "A.5.24",
        "facts": facts_for({"required_evidence_stale_missing_or_hash_failed": True}),
        "failed_sample_ids": ["IR-EX-2025-02"],
        "affected_unit_ids": ["IR-EX-2025-02"],
        "evidence_locators": ["evidence-pack.md::Incident evidence[id=IR-EX-2025-02]"],
    },
    "AT-06": {
        "control_id": "A.5.30",
        "facts": facts_for({"prior_major_open_or_repeated": True}),
        "failed_sample_ids": ["NC-25-02"],
        "affected_unit_ids": ["restore-report-2024"],
        "evidence_locators": [
            "evidence-pack.md::ICT continuity and backup evidence[bullet=3]",
            "evidence-pack.md::ICT continuity and backup evidence[bullet=4]",
        ],
    },
    "AT-07": {
        "control_id": "A.6.3",
        "facts": facts_for({"failed_required_samples": 1, "affected_units": 1}),
        "failed_sample_ids": ["secure-dev-training-roster"],
        "affected_unit_ids": ["secure-dev-training-roster"],
        "evidence_locators": ["evidence-pack.md::Awareness evidence[bullet=3]"],
    },
    "AT-08": {
        "control_id": "A.8.5",
        "facts": facts_for({"prior_major_open_or_repeated": True}),
        "failed_sample_ids": ["NC-25-01"],
        "affected_unit_ids": ["excluded-emergency-accounts"],
        "evidence_locators": [
            "evidence-pack.md::Identity export[bullet=3]",
        ],
    },
    "AT-09": {
        "control_id": "A.8.8",
        "facts": facts_for({"failed_required_samples": 1, "affected_units": 1}),
        "failed_sample_ids": ["VULN-882"],
        "affected_unit_ids": ["VULN-882"],
        "evidence_locators": ["evidence-pack.md::Vulnerability evidence[id=VULN-882]"],
    },
    "AT-10": {
        "control_id": "A.8.13",
        "facts": facts_for({"prior_major_open_or_repeated": True}),
        "failed_sample_ids": ["NC-25-02"],
        "affected_unit_ids": ["restore-report-2024"],
        "evidence_locators": ["evidence-pack.md::ICT continuity and backup evidence[bullet=3]"],
    },
    "AT-11": {
        "control_id": "A.8.15",
        "facts": facts_for({"failed_required_samples": 1, "affected_units": 1}),
        "failed_sample_ids": ["billing-worker-host"],
        "affected_unit_ids": ["billing-worker-host"],
        "evidence_locators": ["evidence-pack.md::Logging evidence[bullet=3]"],
    },
    "AT-12": {
        "control_id": "A.8.32",
        "facts": facts_for({"failed_required_samples": 1, "affected_units": 1}),
        "failed_sample_ids": ["CHG-2281"],
        "affected_unit_ids": ["CHG-2281"],
        "evidence_locators": ["evidence-pack.md::Change sample[id=CHG-2281]"],
    },

    # --- Additional 6 tests (AT-13 to AT-18), resolving 12-vs-18 gap ---
    "AT-13": {
        "control_id": "A.5.24",
        "facts": facts_for({"failed_required_samples": 1, "affected_units": 1}),
        "failed_sample_ids": ["IR-2026-06-06-lessons-learned"],
        "affected_unit_ids": ["IR-2026-06-06"],
        "evidence_locators": ["evidence-pack.md::Incident evidence[bullet=3]"],
    },
    "AT-14": {
        "control_id": "A.6.3",
        "facts": facts_for({"failed_required_samples": 1, "affected_units": 1}),
        "failed_sample_ids": [],
        "affected_unit_ids": ["overdue-awareness-15-workers"],
        "evidence_locators": ["evidence-pack.md::Awareness evidence[bullet=2]"],
    },
    "AT-15": {
        "control_id": "A.8.8",
        "facts": facts_for({"failed_required_samples": 1, "affected_units": 1}),
        "failed_sample_ids": [],
        "affected_unit_ids": ["six-high-severity-vulns"],
        "evidence_locators": ["evidence-pack.md::Vulnerability evidence[bullet=5]"],
    },
    "AT-16": {
        "control_id": "A.8.32",
        "facts": facts_for({"failed_required_samples": 1, "affected_units": 1}),
        "failed_sample_ids": ["CHG-2344"],
        "affected_unit_ids": ["CHG-2344"],
        "evidence_locators": ["evidence-pack.md::Change sample[id=CHG-2344]"],
    },
    "AT-17": {
        "control_id": "A.8.15",
        "facts": facts_for({"failed_required_samples": 1, "affected_units": 1}),
        "failed_sample_ids": [],
        "affected_unit_ids": ["identity-audit-log-retention"],
        "evidence_locators": ["evidence-pack.md::Logging evidence[bullet=4]"],
    },
    "AT-18": {
        "control_id": "A.5.19",
        "facts": facts_for({"failed_required_samples": 1, "affected_units": 1}),
        "failed_sample_ids": [],
        "affected_unit_ids": ["HelpSphere"],
        "evidence_locators": [
            "evidence-pack.md::Supplier evidence[bullet=3]",
            "evidence-pack.md::Interview notes[speaker=Procurement Analyst]",
        ],
    },
}
