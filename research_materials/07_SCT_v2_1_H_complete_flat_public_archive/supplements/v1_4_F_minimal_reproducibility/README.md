# SCT v1.4-F — Minimal Reproducibility Package / Conservative Branch Closure

Project: **Spherical Cyclic Time / Tempo Sferico Ciclico**

This package is a minimal reproducibility and closure checkpoint for the pre-publication v1.4 branch.

It does **not** introduce a new numerical scan, new parameter tuning, a microphysical derivation, a physical cosmology claim, or an observational claim.

## Purpose

The package makes the v1.3-B, v1.3-C, and v1.4-E diagnostic results reproducible from small scripts and lightweight reference outputs:

- v1.3-B alpha/Gamma_S template scan: 4320 rows.
- v1.3-C perturbative matching scan: 5040 rows.
- v1.4-E compact failure/parameter-volume summaries.

## Quick check

From the package root:

```bash
python scripts/run_all_reproducibility_checks.py
python verify_manifest.py
```

Expected core results:

- v1.3-B total rows: 4320
- v1.3-B ok toy total: 681
- fixed physical-clock ok toy: 345 / 720
- matter/radiation window ok toy: 0
- v1.3-C total rows: 5040
- v1.3-C coherent_toy: 228 (~4.52%)
- v1.3-C weak: 2357
- v1.3-C critical: 1378
- v1.3-C failed: 1077

## Status

- Not peer reviewed.
- Toy/informational only.
- No physical cosmology claim.
- No observational claim.
- v1.4 branch is conservatively closed for now unless a real independent derivation/source is supplied.
