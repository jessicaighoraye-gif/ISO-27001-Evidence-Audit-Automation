import csv
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

import jsonschema

SCHEMA_DIR = Path(__file__).resolve().parent.parent / "schemas"


def load_schema(schema_filename):
    """Load one .schema.json file from the schemas/ folder."""
    schema_path = SCHEMA_DIR / schema_filename
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)


def compute_file_hash(file_path):
    """Return the SHA-256 hash of a file, used to prove it wasn't altered."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def validate_record(record, schema):
    """Check one record against a schema. Returns (is_valid, list_of_error_messages)."""
    validator = jsonschema.Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(record), key=lambda e: e.path)
    error_messages = [e.message for e in errors]
    return len(error_messages) == 0, error_messages


def normalize_timestamp(timestamp_str):
    """
    Parse an ISO 8601 timestamp (with or without a timezone offset) and
    return it converted to UTC. Raises ValueError if there's no timezone info. """
    dt = datetime.fromisoformat(timestamp_str)
    if dt.tzinfo is None:
        raise ValueError(f"Timestamp '{timestamp_str}' has no timezone info — cannot normalize safely.")
    return dt.astimezone(timezone.utc)


def load_population_csv(csv_path):
    """
    Load a population CSV, validate every row against population.schema.json,
    and separate valid records from excluded ones (schema failures or duplicates)
    while keeping a reason for every exclusion.
    """
    schema = load_schema("population.schema.json")

    valid_records = []
    excluded_records = []
    seen_ids = set()

    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            is_valid, errors = validate_record(row, schema)

            if not is_valid:
                excluded_records.append({"record": row, "reason": "schema_validation_failed: " + "; ".join(errors)})
                continue

            dedup_key = (row["population"], row["record_id"])
            if dedup_key in seen_ids:
                excluded_records.append({"record": row, "reason": "duplicate_record_id"})
                continue

            seen_ids.add(dedup_key)
            valid_records.append(row)

    return {
        "valid_records": valid_records,
        "excluded_records": excluded_records,
        "source_file": str(csv_path),
        "source_hash": compute_file_hash(csv_path),
    }


def generate_hash_manifest(file_paths, manifest_path):
    """
    Compute SHA-256 for each file and save as the baseline 'expected hash'
    manifest. Run this once, at collection time, on trusted raw evidence.
    """
    manifest = {}
    for file_path in file_paths:
        manifest[str(file_path)] = compute_file_hash(file_path)

    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)

    return manifest


def verify_against_manifest(file_path, manifest_path):
    """
    Recompute a file's hash and compare it against the saved baseline.
    Returns (matches: bool, expected_hash: str or None, actual_hash: str).
    A missing manifest entry means the file was never baselined
    """
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    expected_hash = manifest.get(str(file_path))
    actual_hash = compute_file_hash(file_path)

    if expected_hash is None:
        return False, None, actual_hash

    return expected_hash == actual_hash, expected_hash, actual_hash


def run_collector(csv_path, manifest_path):
    """
    Full collection pipeline for one population CSV:
    verify file hash against baseline, then load/validate/dedupe rows.
    """
    hash_ok, expected_hash, actual_hash = verify_against_manifest(csv_path, manifest_path)

    result = load_population_csv(csv_path)
    result["hash_verified"] = hash_ok
    result["expected_hash"] = expected_hash
    result["actual_hash"] = actual_hash

    return result
