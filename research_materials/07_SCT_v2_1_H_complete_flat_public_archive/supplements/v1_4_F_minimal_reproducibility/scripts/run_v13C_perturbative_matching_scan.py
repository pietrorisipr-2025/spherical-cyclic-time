#!/usr/bin/env python3
"""Reproduce SCT v1.3-C perturbative matching toy scan."""
from pathlib import Path
import argparse
import numpy as np
import pandas as pd

k = np.logspace(-3, 1, 512)
logk = np.log(k)

def transfer(k, kind, kc, p):
    if kind == 'exp_uv_cutoff':
        return np.exp(-(k / kc) ** p)
    if kind == 'soft_power_cutoff':
        return 1.0 / (1.0 + (k / kc) ** p)
    if kind == 'sharp_logistic_cutoff':
        return 1.0 / (1.0 + np.exp(p * np.log(k / kc)))
    raise ValueError(kind)

def classify(row):
    FL, FS, FG = row['F_large_median'], row['F_small_median'], row['F_global_mean']
    frac_dom = row['frac_modes_F_gt_0p7']
    monotone = row['monotone_large_to_small']
    tsharp = row['transfer_kind'] == 'sharp_logistic_cutoff' and row['p'] >= 4
    if FL < 0.10 and FG < 0.10:
        return 'failed', 'memory_erased_all_scales'
    if frac_dom > 0.65:
        return 'critical', 'memory_dominant_suspicious'
    if FS >= 0.30:
        if FS >= 0.70:
            return 'critical', 'small_scale_memory_dominant'
        return 'weak', 'small_scale_memory_not_cleanly_erased'
    if FL < 0.20:
        return 'failed', 'no_large_scale_transmission'
    if 0.30 <= FL <= 0.70 and FS < 0.30 and monotone:
        if tsharp:
            return 'weak', 'coherent_shape_but_sharp_filter_stress_test'
        return 'coherent_toy', 'large_scale_partial_memory_small_scale_regeneration'
    if (0.20 <= FL < 0.30 or 0.70 < FL <= 0.90) and FS < 0.30 and monotone:
        return 'weak', 'borderline_large_scale_memory'
    return 'weak', 'not_clean_transition'

def run_scan():
    rows = []
    for kind in ['exp_uv_cutoff', 'soft_power_cutoff', 'sharp_logistic_cutoff']:
        for ns in [0.90, 0.965, 1.00, 1.10]:
            Pn = (k / 1.0) ** (ns - 1.0)
            for kc in [0.03, 0.10, 0.30, 1.00, 3.00]:
                for p in [1.0, 2.0, 4.0]:
                    T = transfer(k, kind, kc, p)
                    for Axi in [0.01, 0.03, 0.10, 0.30, 1.00, 3.00, 10.00]:
                        for nxi in [-1.0, 0.0, 1.0, 2.0]:
                            Pxi = Axi * (k / 1.0) ** nxi
                            mem = (T * T * Pn) / (T * T * Pn + Pxi + 1e-300)
                            large = k < 0.05
                            mid = (k >= 0.05) & (k < 0.5)
                            small = k >= 0.5
                            idx = np.where(mem < 0.3)[0]
                            row = {
                                'transfer_kind': kind,
                                'n_s_proxy': ns,
                                'k_c': kc,
                                'p': p,
                                'A_xi': Axi,
                                'n_xi': nxi,
                                'F_large_median': float(np.median(mem[large])),
                                'F_mid_median': float(np.median(mem[mid])),
                                'F_small_median': float(np.median(mem[small])),
                                'F_global_mean': float(np.trapz(mem, logk) / (logk[-1] - logk[0])),
                                'frac_modes_F_gt_0p7': float(np.mean(mem > 0.7)),
                                'frac_modes_F_0p3_to_0p7': float(np.mean((mem >= 0.3) & (mem <= 0.7))),
                                'frac_modes_F_lt_0p3': float(np.mean(mem < 0.3)),
                                'transition_k_F_lt_0p3': float(k[idx[0]]) if len(idx) > 0 else None,
                                'monotone_large_to_small': bool(np.median(mem[large]) >= np.median(mem[mid]) >= np.median(mem[small])),
                            }
                            row['classification'], row['reason'] = classify(row)
                            rows.append(row)
    return pd.DataFrame(rows)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--outdir', default='outputs/v13C')
    args = ap.parse_args()
    out = Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)
    df = run_scan()
    df.to_csv(out / 'SCT_v1_3_C_matching_scan_full.csv', index=False)
    df.groupby(['classification', 'reason']).size().reset_index(name='count').to_csv(out / 'SCT_v1_3_C_matching_classification_counts.csv', index=False)
    df.groupby(['transfer_kind', 'classification']).size().unstack(fill_value=0).reset_index().to_csv(out / 'SCT_v1_3_C_transfer_kind_summary.csv', index=False)
    print(f'v1.3-C rows={len(df)} coherent_toy={(df.classification == "coherent_toy").sum()} outdir={out}')

if __name__ == '__main__':
    main()
