# SCT v2.2-F - Numerical and Formula Invariance Audit

Decision: `SCT_V2_2_F_NUMERICAL_FORMULA_INVARIANCE_AUDIT_DONE`.

Overall status: `PASS_NUMERICAL_INVARIANCE_AUDIT_WITH_QA_MANIFEST_NOTE`.

This package checks whether the centerless timeline-bundle reformulation in SCT v2.2-E changes any numerical table, formula block, or computational result from the public v2.1-H line. The conclusion is that no numerical result is changed. v2.2-E is a public-framing/claim-boundary addendum, not a replacement of the v1.3/v1.4/v1.6/v2.0 numerical work.

## Inputs

- v2.1-H ZIP SHA256: `1cef1954a299717c8bf2330d3691053c5e78ffe7fd5833d1f7e60b49d6e1a452`
- v2.2-E ZIP SHA256: `6df6bce19dbd2ef930ac6e854501f0252e9951e2c8a6c2f45989e62bd3d44153`

## Checks

| Check | Status |
|---|---|
| `package_manifest_v2_1_H` | `FAIL_QA_ONLY_KNOWN_PACKAGING_MISMATCH` |
| `package_manifest_v2_2_E_manual` | `PASS` |
| `v1_4_F_reference_vs_rerun` | `PASS_CORE_COUNTS_AND_TABLES` |
| `v1_6_E_reference_vs_rerun` | `PASS` |
| `v2_0_B_transfer_table_vs_rerun` | `PASS` |
| `v2_0_E_transfer_table_vs_numba_rerun` | `PASS` |
| `v2_2_E_no_numeric_replacement_payload` | `PASS` |


## Numerical invariance summary

- v1.4-F reproducibility rerun: PASS.
- v1.3-B: 4320 rows, 681 `ok toy` cases.
- v1.3-C: 5040 rows, 228 `coherent_toy` cases.
- v1.6-E conditional FDT Model A: 140 rows; weak=52, failed=35, critical=28, coherent_toy=25.
- v2.0-B transfer family: all three alpha cases remain `NON_GAUSSIAN_TRANSFER`; maximum T-shape table-vs-rerun difference <= 9.72e-17.
- v2.0-E compact C2 transfer family: all three alpha cases remain `NON_GAUSSIAN_TRANSFER`; maximum T-shape table-vs-rerun difference <= 7.34e-14.
- v2.2-E contains no numerical replacement payload. The only CSV found is a metadata/source-index file.

## Formula invariance summary

The reformulation does not alter the operational formula blocks already audited in chat:

- cyclic phase and unwrapped time: `phi in S^1`, `tau in R`, `phi(tau)=tau mod 2pi` or normalized equivalent;
- absolute/relative entropy decomposition: `S_abs(n,u)=S_min(n)+Delta S_n(u)`, `S_rel=Delta S_n(u)`;
- monotone entropy floor: `S_min(n+1) >= S_min(n)`;
- accessible-capacity diagnostic based on `H^-2` in the flat-FLRW toy branch;
- entropy-clock ratio `alpha_eff(u)=Gamma_S(u)/H(u)`;
- transfer grammar `delta_{n+1}(k)=T_R(k) delta_n(k)+xi_n(k)` and the v2.1-E demotion of the Gaussian transfer to a conditional open-system/diffusive branch.

## Important QA note

The current v2.1-H ZIP hash is correct and the numerical checks pass, but its internal manifest check reports a QA-only mismatch on `qa/final_zip_test.txt`. This does not affect formulas, scripts, tables, PDF content, or numerical results. It is recorded instead of hidden.

## Claim boundary

This audit does not create a physical cosmology claim, observational claim, restart derivation, universal transfer-kernel derivation, or peer-reviewed validation. It only checks invariance of formulas/tables across the v2.2 timeline-bundle wording refactor.
