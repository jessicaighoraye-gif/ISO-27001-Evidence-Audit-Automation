# Northstar Health — ISO/IEC 27001:2022 Internal Audit Engine

Stage 7 GRC Advanced Assessment. Intern: UBI-2026-0030. Variant: V4.
Evidence marker: UBI-A7-598D6B60F230.


## Environment

- OS: Windows (VS Code terminal, PowerShell)
- Python: 3.10.7
- Key packages: jsonschema 4.26.0, pyyaml 6.0.3, pytest 9.1.1
- Virtual environment: `.venv` (created via `py -m venv .venv`)


## Reproduction order

From the project root, with `.venv` activated:

```powershell
py -m pip install jsonschema pyyaml pytest
py -m pytest tests\ -v

py .\audit-engine\generate_verdicts.py


Expected: 34/34 tests pass; sample-manifest.csv (30 rows), evidence-verdicts.json
(18 records), audit-test-sheet.csv (18 rows), nonconformity-register.csv (18 rows),
and evidence-index.csv (17 rows) are all regenerated identically on every run.



## Known limitations and identified ambiguities

- Sample sizes: the "Audit sampling sheet" referenced in the assignment
  Environment Gate requirements was not present in the shared base pack or the
  private overlay. Escalated to programme support on 10/08/26; no
  response received as of this submission. A placeholder value (99, larger
  than any real population) is used throughout. This
  affects `sample-manifest.csv`'s `sampled` outcome but not the 18 test
  verdicts.

- 12 vs. 18 test count: `audit-test-sheet.csv`'s supplied template
  contains 12 rows (one per control), while every narrative project file
  states eighteen audit tests are required. Resolved by adding a second,
  evidentially distinct operating-effectiveness test to six controls. see
  `control_facts.py` for the full reasoning per test.

- "Ingest the published evidence index": `brief.md` states the engine
  must ingest "the published populations and evidence index." No populated
  evidence index was issued, only a blank template and a fictional example.
  `evidence-index.csv` was therefore treated as a generated output of the
  audit process, not an input.

- Evidence-age rule: no fixed day-count threshold is specified anywhere
  in the assignment materials. Staleness is judged per item against facts
  explicitly stated in `evidence-pack.md`, rather than an invented number.

- Python 3.10 timestamp parsing: `normalize_timestamp()` does not handle
  the `Z` UTC suffix natively on Python 3.10 (support was added in 3.11).
  This was identified but intentionally not patched.


- Evidence sourcing: all 18 test findings trace to `evidence-pack.md`
  only. Population-level sampling data (`sample-manifest.csv`)
  is sourced separately from `audit-populations.csv`, which does carry its
  own `source_locator` values (e.g. `iam-export:2`).

