# Continuation Requirements and Obtainability — SCT v2.1-H

This document separates what is needed for publication from what is needed for scientific continuation.

## A. Publication now

Status: **obtainable now**.

Required:

- Clean public package: obtained in v2.1-H.
- Public addenda v2.0-G and v2.1-E: obtained.
- Transfer tables/scripts/figure: obtained.
- Main baseline papers: obtained as v1.6 PDFs.
- Claim boundary: obtained.
- Zenodo metadata draft: obtained.

Still user-dependent:

- Actual Zenodo new-version draft and DOI registration.
- Optional ORCID/community fields.
- Final publication date.

## B. Continue with physical matching route

Status: **not obtainable from current SCT artifacts alone**.

Needed before execution:

1. Independent background/action.
2. Gauge-invariant perturbation variable.
3. The function `z(eta)` or equivalent structure entering the perturbation equation.
4. Matching surface and matching conditions.
5. A preregistered transfer extraction metric.

Can it be obtained?

- Partially yes, but only by selecting a concrete model from the literature or deriving one independently before any numerical execution.
- It cannot be obtained by choosing a new background after looking for gaussianity.

Recommendation:

- Do not execute this route until all five inputs are fixed in a preregistration package.

## C. Continue with open-system/diffusive route

Status: **blocked unless independent environment physics is specified**.

Needed:

1. Environment degrees of freedom.
2. State `rho_env`.
3. Coupling `S_int`.
4. Spectral density / noise kernel.
5. Timescale hierarchy justifying Markov/FDT/KMS, if used.
6. Entropy map and no-double-counting rule with `S_cap`.

Can it be obtained?

- Not from the current toy model alone.
- Potentially from a fully specified open-system cosmological model, but this would be a new project branch, not a continuation by packaging.

## D. Continue analytically on the plateau mechanism

Status: **obtainable now, but limited novelty**.

Possible task:

- Formalize a small lemma for closed deterministic proxy equations: high-k transparency plus low-k reference amplification naturally leads to a normalized plateau-like transfer shape.

Risk:

- Useful as a clarity patch, but not a physical kernel derivation.

## Recommended research decision

Publish v2.1 first. Then only continue if one of these inputs is obtained independently:

- a concrete physical matching model; or
- a concrete open-system environment model.

Do not continue by adding a third toy background solely to rescue gaussianity.
