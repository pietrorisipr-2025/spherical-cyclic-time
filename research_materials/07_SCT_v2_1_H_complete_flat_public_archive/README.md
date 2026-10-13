# SCT v2.1-H — Zenodo Publication Prep / Final Public Package

This package is a flat, publication-oriented release package for **Spherical Cyclic Time (SCT) v2.1.0**.
It is prepared for a Zenodo **new version** upload linked to the existing public v1.2.0 record.

## Purpose

The package consolidates the public-facing material after the v2.0 and v2.1 updates:

- v1.6 main bilingual papers as the current full working-paper baseline.
- v1.5-F and v1.6-F addenda.
- v2.0-G public synthesis of the two preregistered minimal closed-background transfer tests.
- v2.1-E public patch updating transfer-kernel language.
- Result tables, scripts, figures, TeX sources, claim boundary, and Zenodo metadata draft.

## Main scientific status

The conservative mainline transfer language is now:

```text
T_R(k) = model-dependent transfer operator
```

The gaussian/diffusive form is **not** treated as the default closed-background expectation.
It remains allowed only as a conditional open-system/diffusive toy limit. The plateau-like form is recorded only as a closed deterministic proxy toy branch, not as a universal physical kernel.

## Claim boundary

This release does not claim a physical cyclic cosmology, observational prediction, no-go theorem for cyclic/bounce cosmology, universal transfer kernel, entropy-map derivation, or derivation of bath/noise/FDT/Gamma/restart dynamics.

## Upload recommendation

Use this ZIP as the single public upload file, or upload the files in `upload_set/` individually. The package intentionally contains no recursive ZIP archives and no internal recovery bundles.
