# Reproducibility Instructions

## Requirements

- Python 3.10+
- `numpy`
- `pandas`

No internet access is required. No external cosmological datasets are required.

## Run all checks

```bash
python scripts/run_all_reproducibility_checks.py
```

This regenerates the v1.3-B and v1.3-C toy scans, builds the compact v1.4-E summaries, and compares core counts with `expected/expected_summary.json`.

## Run components separately

```bash
python scripts/run_v13B_alpha_template_scan.py --outdir outputs/v13B
python scripts/run_v13C_perturbative_matching_scan.py --outdir outputs/v13C
python scripts/run_v14E_failure_taxonomy_audit.py       --v13b outputs/v13B/SCT_v1_3_B_alpha_template_dynamic_scan.csv       --v13c outputs/v13C/SCT_v1_3_C_matching_scan_full.csv       --outdir outputs/v14E
```

## Verify package integrity

```bash
python verify_manifest.py
```

## Important limitation

Reproducibility here means reproducibility of the toy diagnostic calculations and classifications. It does **not** validate a physical cosmology.
