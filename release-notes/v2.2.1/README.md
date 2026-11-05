# Spherical Cyclic Time — v2.2.1 canonical erratum

**Zenodo:** https://zenodo.org/records/23964270 · **DOI:** https://doi.org/10.5281/zenodo.23964270 · **Publication date:** 2026-11-04 · **Author:** Pietro Risi.

This corrective release retains the centerless timeline-bundle clarification and supplies an integrated mathematical/numerical erratum for older SCT publications. It is an exploratory preprint, not peer-reviewed.

| Item | Previously published | Corrected result | Dataset |
| --- | ---: | ---: | --- |
| v1.2.0 phase scan OK toy | 217 | **227** | 720 rows |
| v1.3-A apparent/Hubble horizon OK toy | 216 | **218** | 720 of 1,440 rows |
| v1.3-A future event horizon OK toy | 330 | **330** | 720 of 1,440 rows |
| v1.3-B entropy template OK toy | 681 | **536** | 4,320 rows |

The v1.3-B error is a **specification–implementation mismatch**: the executable algorithm did not implement the equation printed in the paper. Re-integration of the printed equation changed 824 of 4,320 classifications. The v1.2.0 and v1.3-A counts are also corrected, and the v1.0.0 angular non-uniqueness, derivative sign and Gaussian normalization errors are documented. Changes propagate to Tables 1–3, Figure 3, threshold audit and dependent v1.4-E summaries. Exact details and equations are in the two official erratum papers.

## Canonical downloadable materials

- [Erratum PDF — English](https://zenodo.org/records/23964270/files/SCT_v2_2_M_erratum_EN.pdf?download=1)
- [Erratum PDF — Italian](https://zenodo.org/records/23964270/files/SCT_v2_2_M_erratum_IT.pdf?download=1)
- [Phase scan — corrected 720-row CSV](https://zenodo.org/records/23964270/files/SCT_corrected_v1_2_phase_scan_720.csv?download=1)
- [Horizon choice — corrected 1,440-row CSV](https://zenodo.org/records/23964270/files/SCT_corrected_v1_3_A_patch_choice_1440.csv?download=1)
- [Entropy scan — corrected 4,320-row CSV](https://zenodo.org/records/23964270/files/SCT_corrected_v1_3_B_entropy_scan_4320.csv?download=1)
- [Technical erratum, corrected data and reproduction ZIP](https://zenodo.org/records/23964270/files/SCT_v2_2_N_PUBLIC_ERRATUM_WITH_CORRECTED_DATA.zip?download=1)
- [Checksum companion for full ZIP](https://zenodo.org/records/23964270/files/SCT_v2_2_N_PUBLIC_ERRATUM_WITH_CORRECTED_DATA.zip.sha256?download=1)

All seven file names and Zenodo-listed MD5 hashes are recorded in [assets.json](assets.json); the Python script in the repository scripts directory verifies local downloads without altering canonical archives. This repository avoids committing large or binary canonical assets twice. GitHub release attachments may be added separately only after exact-byte verification.

## Historical interpretation and remaining work

The earlier v2.2-F audit only established reproducibility of historical numerical program outputs; it **did not validate adherence to the published differential equation**. The v2.2.1 erratum supersedes conflicting historical results. Its corrected data do not directly alter v2.0/v2.1 independently computed toy transfer-kernel results, and the centerless interpretation is unchanged.

Independent verification of v1.3-C and v1.6-E classifiers, documentation of the v2.0 transfer extraction protocol, bibliographic corrections and previously recorded packaging issues are outstanding. There is no claimed validated cosmology, verified physical restart, or new observational prediction. AI assistance is disclosed in [AI_ASSISTANCE_AND_VALIDATION.md](../../AI_ASSISTANCE_AND_VALIDATION.md).
