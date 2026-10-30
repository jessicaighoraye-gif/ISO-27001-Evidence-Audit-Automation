import hashlib


def generate_seed(evidence_marker, population_name, salt=""):
    """
    Deterministic seed from the evidence marker + population name + optional salt.
    Same inputs always produce the same seed.
    """
    seed_input = f"{evidence_marker}:{population_name}:{salt}".encode("utf-8")
    return hashlib.sha256(seed_input).hexdigest()


def select_sample(records, population_name, evidence_marker, sample_size, salt=""):
    """
    Deterministically select `sample_size` records from one population's
    valid records. Rejects mixed-population input.
    """
    populations_present = set(r["population"] for r in records)
    if len(populations_present) > 1:
        raise ValueError(f"select_sample received mixed populations: {populations_present}. Filter by population first.")

    if populations_present and population_name not in populations_present:
        raise ValueError(f"population_name '{population_name}' does not match records' actual population '{populations_present}'.")

    seed_hex = generate_seed(evidence_marker, population_name, salt)
    seed_int = int(seed_hex, 16)

    sorted_records = sorted(records, key=lambda r: r["record_id"])

    if sample_size > len(sorted_records):
        sample_size = len(sorted_records)

    indices = list(range(len(sorted_records)))
    rng_state = seed_int
    for i in range(len(indices) - 1, 0, -1):
        rng_state = (rng_state * 1103515245 + 12345) & 0x7FFFFFFF
        j = rng_state % (i + 1)
        indices[i], indices[j] = indices[j], indices[i]

    selected_indices = sorted(indices[:sample_size])
    return [sorted_records[i] for i in selected_indices]
