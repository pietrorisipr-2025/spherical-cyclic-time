# Spherical Cyclic Time (SCT)

**Pietro Risi · exploratory, human-directed and AI-assisted research · not peer-reviewed.**

> **Current official scientific record: v2.2.1 (4 November 2026), [Zenodo 23964270](https://zenodo.org/records/23964270), DOI [10.5281/zenodo.23964270](https://doi.org/10.5281/zenodo.23964270).** This corrective release supersedes conflicting historical numerical tables and formula statements while preserving their original archives.

## Start with the current erratum

- [Technical erratum, English](https://zenodo.org/records/23964270/files/SCT_v2_2_M_erratum_EN.pdf?download=1)
- [Erratum tecnico, italiano](https://zenodo.org/records/23964270/files/SCT_v2_2_M_erratum_IT.pdf?download=1)
- [Full Zenodo record and corrected CSV data](https://zenodo.org/records/23964270)
- [Version 2.2.1 corrections, status and provenance](release-notes/v2.2.1/README.md)
- [Scientific status and open questions](SCIENTIFIC_STATUS.md)
- [Verify the official release files](REPRODUCIBILITY.md)

## Corrected numerical results

| Historical experiment | Historical OK toy | Corrected OK toy |
| --- | ---: | ---: |
| v1.2.0 phase scan (720 cases) | 217 | **227** |
| v1.3-A Hubble/apparent horizon (720 cases) | 216 | **218** |
| v1.3-A future-event horizon (720 cases) | 330 | **330 (unchanged)** |
| v1.3-B entropy templates (4,320 cases) | 681 | **536** |

The corrected v1.3-B scan changes 824 of 4,320 historical classifications. Three v1.0.0 mathematical errors are corrected (spherical angular parametrization non-uniqueness, a derivative sign, Gaussian integral normalization). Tables 1–3, Figure 3, threshold analyses and dependent v1.4-E summaries are replaced where affected.

**Important:** the earlier v2.2-F invariance audit reproduced older program outputs, but did *not* verify that those programs implemented the published differential equation. Do not quote old results as independently validated because the historical programs reproduced them. See the English/Italian erratum for details.

## Research scope

SCT is an exploratory toy/informational mathematical framework, not a validated physical cosmology. The centerless timeline-bundle semantic clarification introduced in v2.2.0 is retained. The independent v2.0/v2.1 toy transfer-kernel results are not directly changed by the v2.2.1 erratum; this does not certify them. There is no demonstrated cosmological restart mechanism, new observational prediction, or independent human peer review.

## Historical research, permanently preserved

The original 2026-07-08 v2.2.0 Zenodo record [21269182](https://zenodo.org/records/21269182) and archived manuscripts remain the record of what was previously published. Historical files in `originals_verified/` and `research_materials/` **must not be silently edited**. In particular, do not treat the upload guide as the scientific paper.

- [v1.6 historical English base paper](originals_verified/21269182/01_spherical_cyclic_time_v1_6_0_main_EN.pdf)
- [v2.1-E computational interpretation patch](originals_verified/21269182/06_SCT_v2_1_E_public_patch_after_transfer_route_decision.pdf)
- [v2.2-E semantic clarification](originals_verified/21269182/08_SCT_v2_2_E_INTEGRATED_PUBLIC_MINI_RELEASE_TIMELINE_BUNDLE.pdf)
- [v2.2-F historical invariance audit — limited scope](originals_verified/21269182/10_SCT_v2_2_F_NUMERICAL_FORMULA_INVARIANCE_AUDIT.pdf)
- [v2.2-H final clarification](originals_verified/21269182/12_SCT_v2_2_H_FINAL_UPLOAD_CLARIFICATION_PATCH.pdf)
- [Original archives and provenance](SOURCES.md) and [version history](VERSION_HISTORY.md)

The old archives, checksums and repository evidence retain their provenance; old superseded scientific conclusions do not regain authority because they are archived.

## Reproducibility, rights and transparency

The seven v2.2.1 Zenodo files remain authoritative at Zenodo. The repository includes a URL/checksum manifest at [`release-notes/v2.2.1/assets.json`](release-notes/v2.2.1/assets.json) and a [Python integrity/count checker](scripts/verify_sct_zenodo_v2_2_1.py), without duplicating binary release files inside Git history. The script checks official-file MD5, the ZIP's companion SHA-256, CSV row counts, and the published `ok toy` counts; it **does not** re-integrate the equations or validate the physical model.

See [reproducibility](REPRODUCIBILITY.md), [licensing policy](LICENSE_POLICY.md), [rights and AI disclosure](RIGHTS_AND_AI_USE.md) and [AI assistance and validation](AI_ASSISTANCE_AND_VALIDATION.md). License assertions apply only to materials for which sufficient rights exist and do not override historical source licenses.

**This archive does not imply human peer review, independent physical validation, or independent legal verification.**
