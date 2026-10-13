# Reproducibility and evidence status

- 23 original files: Zenodo MD5 and SHA-256 verified locally.
- 11 direct original files preserved in this repository.
- 4 published nested research ZIP archives: CRC checked.
- The original nested ZIPs remain in the separate original Release asset; selected plain text/scripts/data were extracted under `research_materials/`.
- Scientific results and scripts were not rerun here; any published test logs are historical claims of those records.
- Verify environment and run original scripts in a controlled environment, and report discrepancies rather than changing old result hashes.

## Known limitations

Earlier public v1.0.0 and v1.2.0 not byte-compared. Three inherited QA/log manifest mismatches in nested v2.1-H archives; see QA summary.

- The base v2.1-H manifest and both embedded supplement manifests contain one inherited log/QA hash mismatch each; see `QA_CURRENT_RECORD.json` for exact paths. Originals were not silently repaired.
