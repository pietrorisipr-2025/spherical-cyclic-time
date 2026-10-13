#!/usr/bin/env python3
"""Run SCT v1.4-F minimal reproducibility checks.

Outputs are written under the selected work directory. The script compares key counts to
`expected/expected_summary.json` and exits nonzero on mismatch.
"""
from pathlib import Path
import argparse, json, subprocess, sys, hashlib
import pandas as pd

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def run(cmd, cwd):
    print('+ ' + ' '.join(map(str, cmd)))
    subprocess.check_call(cmd, cwd=cwd)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--workdir', default='outputs/reproduced')
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[1]
    work = root / args.workdir
    work.mkdir(parents=True, exist_ok=True)
    expected = json.loads((root / 'expected/expected_summary.json').read_text(encoding='utf-8'))

    run([sys.executable, 'scripts/run_v13B_alpha_template_scan.py', '--outdir', str(work / 'v13B')], root)
    run([sys.executable, 'scripts/run_v13C_perturbative_matching_scan.py', '--outdir', str(work / 'v13C')], root)
    run([
        sys.executable, 'scripts/run_v14E_failure_taxonomy_audit.py',
        '--v13b', str(work / 'v13B/SCT_v1_3_B_alpha_template_dynamic_scan.csv'),
        '--v13c', str(work / 'v13C/SCT_v1_3_C_matching_scan_full.csv'),
        '--outdir', str(work / 'v14E'),
    ], root)

    b = pd.read_csv(work / 'v13B/SCT_v1_3_B_alpha_template_dynamic_scan.csv')
    c = pd.read_csv(work / 'v13C/SCT_v1_3_C_matching_scan_full.csv')
    checks = {
        'v13B_rows': len(b),
        'v13B_ok_toy_total': int((b['classification'] == 'ok toy').sum()),
        'v13B_fixed_clock_ok_toy': int(((b['alpha_template'] == 'fixed_physical_clock_Gamma_const') & (b['classification'] == 'ok toy')).sum()),
        'v13B_matter_window_ok_toy': int(((b['alpha_template'] == 'matter_fraction_window') & (b['classification'] == 'ok toy')).sum()),
        'v13B_radiation_window_ok_toy': int(((b['alpha_template'] == 'radiation_fraction_window') & (b['classification'] == 'ok toy')).sum()),
        'v13C_rows': len(c),
        'v13C_coherent_toy': int((c['classification'] == 'coherent_toy').sum()),
        'v13C_weak': int((c['classification'] == 'weak').sum()),
        'v13C_critical': int((c['classification'] == 'critical').sum()),
        'v13C_failed': int((c['classification'] == 'failed').sum()),
    }
    failures = []
    for key, actual in checks.items():
        exp = expected[key]
        if actual != exp:
            failures.append((key, exp, actual))
    report = {'checks': checks, 'failures': failures}
    (work / 'reproducibility_check_summary.json').write_text(json.dumps(report, indent=2, sort_keys=True), encoding='utf-8')
    if failures:
        print('FAILURES:')
        for key, exp, act in failures:
            print(f'  {key}: expected={exp} actual={act}')
        sys.exit(1)
    print('ALL REPRODUCIBILITY CHECKS PASS')

if __name__ == '__main__':
    main()
