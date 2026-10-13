# SCT v1.4-F — Minimal Reproducibility Package / Conservative Closure

## Decision status

`SCT_v1_4_F_MINIMAL_REPRODUCIBILITY_PACKAGE_OR_CLOSE_V1_4_BRANCH_DONE; MINIMAL_REPRODUCIBILITY_PACKAGE_CREATED; V1_3_B_ALPHA_TEMPLATE_SCAN_REPRODUCIBLE; V1_3_C_PERTURBATIVE_MATCHING_SCAN_REPRODUCIBLE; V1_4_E_FAILURE_VOLUME_SUMMARIES_REPRODUCIBLE; V1_4_BRANCH_CONSERVATIVELY_CLOSED_PREPUBLICATION; NO_NEW_NUMERICAL_SCAN; NO_PARAMETER_TUNING; NO_MICROPHYSICAL_DERIVATION; NO_PHYSICAL_COSMOLOGY_CLAIM; NO_OBSERVATIONAL_CLAIM; NOT_PEER_REVIEWED; SINGLE_ZIP_OUTPUT_CREATED.`

## What this checkpoint does

v1.4-F converts the current pre-publication branch into a minimal reproducibility package. It preserves the methodologically important negative results:

- many physically suggestive `Gamma_S` templates fail;
- the fixed physical-clock template remains only a toy baseline;
- the perturbative matching coherent region is small and conditioned on non-derived toy parameters;
- `P_xi(k)`, `k_c`, and `p` are not physically derived;
- no observational signature is claimed.

## What this checkpoint does not do

It does not add a new route, tune parameters, introduce new data, infer physical cosmology, or rescue failed branches.

## Reproducibility scope

The package includes code to regenerate:

1. the v1.3-B 4320-row alpha/Gamma_S template scan;
2. the v1.3-C 5040-row perturbative matching scan;
3. the compact v1.4-E parameter-volume/failure summaries.

It also includes reference CSV outputs and expected summary values. Reproduction checks compare the main row counts and classifications against those expected values.

## Closure interpretation

The v1.4 branch is closed conservatively at the level of toy/informational reproducibility. Reopening requires at least one of:

- an independently specified microphysical `Gamma_S` model;
- an independently specified regeneration spectrum `P_xi(k)` with `k_c` and `p` not chosen from restart success;
- a covariant light-sheet/causal-patch construction that distinguishes bound, capacity, and equality;
- a public/reproducibility-driven release preparation, not a new physics claim.
