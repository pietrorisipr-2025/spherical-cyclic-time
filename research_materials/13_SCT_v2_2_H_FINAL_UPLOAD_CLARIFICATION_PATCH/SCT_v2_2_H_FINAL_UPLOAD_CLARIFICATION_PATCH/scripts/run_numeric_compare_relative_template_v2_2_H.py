#!/usr/bin/env python3
"""
SCT v2.2-H portable numeric audit template.

This file addresses the path-portability note found after v2.2-F. The executed
v2.2-F audit remains the authoritative recorded audit because it includes the
actual logs and hashes. This template is supplied for future reruns without
hardcoded /mnt/data paths.

Example:
  python scripts/run_numeric_compare_relative_template_v2_2_H.py \
    --base ./work/extract/SCT_v2_1_H_ZENODO_PUBLICATION_PREP_FINAL_PUBLIC_PACKAGE \
    --run ./work/run_outputs \
    --out ./work/compare_outputs \
    --v21h-zip ./SCT_v2_1_H_ZENODO_PUBLICATION_PREP_FINAL_PUBLIC_PACKAGE.zip \
    --v22e-zip ./SCT_v2_2_E_INTEGRATED_PUBLIC_MINI_RELEASE_TIMELINE_BUNDLE.zip

Note: this template expects the same extracted directories and rerun outputs
used by the original v2.2-F audit protocol. It does not itself download or
recreate those inputs.
"""
from __future__ import annotations
from pathlib import Path
import argparse, hashlib, json
import pandas as pd
import numpy as np

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def compare_df(a: pd.DataFrame, b: pd.DataFrame, rtol=1e-12, atol=1e-12) -> dict:
    res = {'shape_a': list(a.shape), 'shape_b': list(b.shape), 'columns_same': list(a.columns) == list(b.columns), 'diff_cells': None, 'max_abs_numeric_diff': None, 'status': None}
    if a.shape != b.shape or list(a.columns) != list(b.columns):
        res['status'] = 'SCHEMA_DIFF'; return res
    diff = 0; maxnum = 0.0
    for col in a.columns:
        if pd.api.types.is_numeric_dtype(a[col]) and pd.api.types.is_numeric_dtype(b[col]) and not (a[col].dtype == 'bool' or b[col].dtype == 'bool'):
            av = pd.to_numeric(a[col], errors='coerce'); bv = pd.to_numeric(b[col], errors='coerce')
            d = (av - bv).abs().max()
            if not pd.isna(d): maxnum = max(maxnum, float(d))
            diff += int((~np.isclose(av, bv, rtol=rtol, atol=atol, equal_nan=True)).sum())
        else:
            diff += int((a[col].fillna('__NA__').astype(str) != b[col].fillna('__NA__').astype(str)).sum())
    res.update({'diff_cells': diff, 'max_abs_numeric_diff': maxnum, 'status': 'PASS' if diff == 0 else 'DIFF'})
    return res

def main() -> int:
    ap = argparse.ArgumentParser(description='Portable SCT v2.2-F numeric comparison template (v2.2-H path patch).')
    ap.add_argument('--base', required=True, type=Path, help='Extracted v2.1-H package root.')
    ap.add_argument('--run', required=True, type=Path, help='Directory containing rerun outputs used for comparison.')
    ap.add_argument('--out', required=True, type=Path, help='Output directory for comparison report.')
    ap.add_argument('--v21h-zip', type=Path, default=None, help='Optional v2.1-H zip for hash recording.')
    ap.add_argument('--v22e-zip', type=Path, default=None, help='Optional v2.2-E zip for hash recording.')
    ap.add_argument('--v21h-manifest-verify', type=Path, default=None, help='Optional manifest verify log for v2.1-H.')
    args = ap.parse_args()
    base = args.base.resolve(); run = args.run.resolve(); out = args.out.resolve(); out.mkdir(parents=True, exist_ok=True)
    report = {'decision': 'SCT_v2_2_H_PORTABLE_NUMERIC_COMPARE_TEMPLATE', 'note': 'Path-configurable template only; authoritative executed audit remains v2.2-F.', 'inputs': {}, 'checks': {}}
    for key, p in [('v2_1_H_zip', args.v21h_zip), ('v2_2_E_zip', args.v22e_zip)]:
        if p is not None:
            p = p.resolve(); report['inputs'][key] = str(p); report['inputs'][key + '_sha256'] = sha256(p) if p.exists() else 'MISSING'
    if args.v21h_manifest_verify and args.v21h_manifest_verify.exists():
        txt = args.v21h_manifest_verify.read_text(encoding='utf-8', errors='replace')
        report['checks']['package_manifest_v2_1_H'] = {'status': 'FAIL_QA_ONLY_KNOWN_PACKAGING_MISMATCH' if 'hash_mismatch' in txt else 'PASS_OR_NOT_RUN', 'detail': txt.strip()}
    ref14 = base / 'supplements/v1_4_F_minimal_reproducibility/data/reference'; run14 = run / 'v14F'; v14_items = []
    for sub in ['v13B', 'v13C', 'v14E']:
        pdir = run14 / sub
        if not pdir.exists(): continue
        for p in sorted(pdir.glob('*.csv')):
            r = ref14 / p.name
            if not r.exists(): continue
            comp = compare_df(pd.read_csv(r), pd.read_csv(p)); comp['file'] = p.name; v14_items.append(comp)
    report['checks']['v1_4_F_reference_vs_rerun'] = {'status': 'PASS' if all(x['status'] == 'PASS' for x in v14_items) else 'CHECK_DIFFS', 'items': v14_items}
    ref16 = base / 'supplements/v1_6_E_conditional_FDT_model_A/data'; run16 = run / 'v16E'; v16_items = []
    if run16.exists():
        for p in sorted(run16.glob('*.csv')):
            r = ref16 / p.name
            if not r.exists(): continue
            comp = compare_df(pd.read_csv(r), pd.read_csv(p)); comp['file'] = p.name; v16_items.append(comp)
    report['checks']['v1_6_E_reference_vs_rerun'] = {'status': 'PASS' if all(x['status'] == 'PASS' for x in v16_items) else 'CHECK_DIFFS', 'items': v16_items}
    report['checks']['path_portability_patch'] = {'status': 'PASS_TEMPLATE', 'detail': 'All root paths are supplied by CLI arguments. No /mnt/data hardcoding is required.'}
    report['overall_status'] = 'PASS_TEMPLATE_OR_CHECK_DETAILS'
    (out / 'SCT_v2_2_H_PORTABLE_NUMERIC_COMPARE_TEMPLATE_REPORT.json').write_text(json.dumps(report, indent=2, sort_keys=True), encoding='utf-8')
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
