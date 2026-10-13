#!/usr/bin/env python3
"""Reproduce compact v1.4-E failure/volume summaries from v1.3-B and v1.3-C outputs.

This script does not run a new parameter scan. It summarizes already-generated toy grids.
"""
from pathlib import Path
import argparse
import pandas as pd

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--v13b', required=True, help='Path to SCT_v1_3_B_alpha_template_dynamic_scan.csv')
    ap.add_argument('--v13c', required=True, help='Path to SCT_v1_3_C_matching_scan_full.csv')
    ap.add_argument('--outdir', default='outputs/v14E')
    args = ap.parse_args()
    out = Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)
    b = pd.read_csv(args.v13b)
    c = pd.read_csv(args.v13c)

    # v1.3-B alpha-template volume summary
    rows = []
    for tmpl, g in b.groupby('alpha_template'):
        rows.append({
            'alpha_template': tmpl,
            'total_rows': len(g),
            'ok_toy': int((g.classification == 'ok toy').sum()),
            'ok_toy_fraction': float((g.classification == 'ok toy').mean()),
            'failure_rows': int((g.classification == 'fallisce: nessun restart entro u_max').sum()),
            'failure_fraction': float((g.classification == 'fallisce: nessun restart entro u_max').mean()),
            'critical_rows': int(g.classification.astype(str).str.startswith('critico').sum()),
            'near_or_weak_rows': int(g.classification.astype(str).str.startswith('debole').sum()),
        })
    pd.DataFrame(rows).sort_values('alpha_template').to_csv(out / 'SCT_v1_4_E_v13B_alpha_template_volume.csv', index=False)

    # v1.3-C classification volume
    pd.DataFrame([
        {'classification': cls, 'rows': int(n), 'fraction': float(n / len(c))}
        for cls, n in c.classification.value_counts().sort_index().items()
    ]).to_csv(out / 'SCT_v1_4_E_v13C_classification_volume.csv', index=False)

    # compact parameter-volume summary
    summary = pd.DataFrame([
        {
            'module': 'v1.3-B alpha/Gamma_S templates',
            'grid_rows': len(b),
            'favorable_definition': 'classification == ok toy',
            'favorable_rows': int((b.classification == 'ok toy').sum()),
            'favorable_fraction_grid_proxy': float((b.classification == 'ok toy').mean()),
            'strict_failure_rows': int((b.classification == 'fallisce: nessun restart entro u_max').sum()),
            'strict_failure_fraction_grid_proxy': float((b.classification == 'fallisce: nessun restart entro u_max').mean()),
            'critical_rows': int(b.classification.astype(str).str.startswith('critico').sum()),
            'critical_fraction_grid_proxy': float(b.classification.astype(str).str.startswith('critico').mean()),
            'main_caveat': 'favorable volume dominated by toy/control clock templates; no microphysical Gamma_S',
        },
        {
            'module': 'v1.3-C perturbative matching',
            'grid_rows': len(c),
            'favorable_definition': 'classification == coherent_toy',
            'favorable_rows': int((c.classification == 'coherent_toy').sum()),
            'favorable_fraction_grid_proxy': float((c.classification == 'coherent_toy').mean()),
            'strict_failure_rows': int((c.classification == 'failed').sum()),
            'strict_failure_fraction_grid_proxy': float((c.classification == 'failed').mean()),
            'critical_rows': int((c.classification == 'critical').sum()),
            'critical_fraction_grid_proxy': float((c.classification == 'critical').mean()),
            'main_caveat': 'coherent region is a small combinatorial grid fraction and uses non-derived k_c, p, P_xi',
        },
    ])
    summary.to_csv(out / 'SCT_v1_4_E_parameter_volume_summary.csv', index=False)

    print('v1.4-E compact summaries reproduced')
    print(summary.to_string(index=False))

if __name__ == '__main__':
    main()
