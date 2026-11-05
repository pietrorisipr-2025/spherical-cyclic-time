# Reproducibility and integrity — current v2.2.1 vs historical material

## v2.2.1 (canonical public corrective deposit)

The **official** files live at [Zenodo 23964270](https://zenodo.org/records/23964270), not in historical `originals_verified/21269182/`. The manifest at [`release-notes/v2.2.1/assets.json`](release-notes/v2.2.1/assets.json) lists the seven public file names, URLs and their Zenodo MD5 strings; it records the expected CSV toy-case classifications.

With Python 3.9+ from repository root:

```bash
python scripts/verify_sct_zenodo_v2_2_1.py --download
```

The command downloads missing files to `original-zenodo-downloads/v2.2.1/` (ignored by Git) and checks:

1. Each downloaded asset matches the MD5 shown on its official Zenodo record.
2. The complete ZIP archive matches the **SHA-256** recorded in Zenodo's companion `.zip.sha256` file.
3. The three corrected datasets have 720, 1,440 and 4,320 data rows respectively; with `classification == "ok toy"`, counts are v1.2.0 = 227; v1.3-A = 218 (apparent horizon) + 330 (future event horizon); v1.3-B = 536.

No checksum result, ZIP test or counting script is proof that the underlying differential equations were solved correctly. Independent re-integration of the published equations, classification sensitivity, and scientific validation require separate methods.

## Historical v2.2.0 and earlier archives

Existing `SHA256SUMS.txt`, `FILE_INVENTORY.csv`, `QA_CURRENT_RECORD.json` and original Release assets refer to the prior public Zenodo 21269182 migration and its history, **not** a new 23964270 byte-by-byte comparison. Do not relabel them as verified against 23964270.

Historical repository preparation recorded 23 original files MD5/SHA-256-checked, four nested ZIPs CRC checked and three inherited v2.1-H QA/log manifest mismatches. Reproducing older code did not establish that its implementation matched the printed ODE. In particular, v2.2-F invariance testing does not override the 2.2.1 erratum.
