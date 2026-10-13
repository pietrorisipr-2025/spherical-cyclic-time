# SCT v2.2-H - Final upload clarification patch

## Decision

`SCT_V2_2_H_FINAL_UPLOAD_CLARIFICATION_PATCH_DONE`

## Reason

A final external review of v2.2-G found the bundle publishable and non-regressive, but recommended four refinements before upload:

1. Make the inherited v2.1-H QA-only manifest note visible in Zenodo/GitHub description text.
2. State explicitly that v2.2 is a wording clarification plus invariance audit, not a new numerical or observational result.
3. Mark `B(sigma) = {L_i(sigma)}` as descriptive-only notation.
4. Replace or supplement the hardcoded `/mnt/data/...` audit script with a path-configurable template.

## Actions taken

- Created upload-facing Zenodo description patch.
- Created GitHub README notice patch.
- Created public version note.
- Created `B(sigma)` descriptive-only note.
- Added a relative/configurable audit script template for future reruns.
- Preserved all earlier numerical and publication artifacts unchanged.

## Boundary

No new numerical execution. No formula change. No derivation change. No transfer-kernel result change. No observational claim. No physical cosmology claim. No modification to the already-published v2.1-H archive.

## Status

PASS - ready as a clarification patch to accompany the v2.2-G upload bundle.
