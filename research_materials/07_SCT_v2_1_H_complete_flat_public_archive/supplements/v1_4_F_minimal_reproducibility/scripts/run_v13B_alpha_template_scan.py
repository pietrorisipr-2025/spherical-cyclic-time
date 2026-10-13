#!/usr/bin/env python3
"""Reproduce SCT v1.3-B alpha/Gamma_S template scan.

This is a toy diagnostic scan, not a physical cosmology simulation.
It regenerates the 4320-row alpha-template dynamic scan and compact counts.
"""
from pathlib import Path
import argparse, itertools, math
import numpy as np
import pandas as pd

TEMPLATES = [
    'legacy_H_scaled_constant',
    'fixed_physical_clock_Gamma_const',
    'capacity_growth_locked_dlnScap',
    'matter_fraction_window',
    'radiation_fraction_window',
    'matter_lambda_transition_window',
]
C_M = [1, 3, 9, 30, 100]
C_R = [0, 1, 10, 100]
AMPLITUDES = [0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10]
QCRITS = [0.8, 0.9, 0.95, 0.99]
DU = 0.001
U_MAX = 20.0

def classify(restart, u, s_cap, q_eff, qcrit):
    if restart:
        if s_cap < 0.5:
            return 'critico: capienza molto immatura'
        if s_cap < 0.9:
            return 'debole: capienza non matura'
        if u < 1.0:
            return 'critico: restart precoce'
        if u > 12.0:
            return 'debole: scala tardiva'
        return 'ok toy'
    if q_eff >= 0.9 * qcrit:
        return 'debole/quasi: nessun restart entro u_max'
    return 'fallisce: nessun restart entro u_max'

def run_scan():
    combos = list(itertools.product(TEMPLATES, C_M, C_R, AMPLITUDES, QCRITS))
    n = len(combos)
    template = np.array([c[0] for c in combos], dtype=object)
    c_m = np.array([c[1] for c in combos], dtype=float)
    c_r = np.array([c[2] for c in combos], dtype=float)
    amp = np.array([c[3] for c in combos], dtype=float)
    qcrit = np.array([c[4] for c in combos], dtype=float)

    delta_s = np.zeros(n)
    integrated_alpha = np.zeros(n)
    restart = np.zeros(n, dtype=bool)
    u_star = np.full(n, U_MAX)
    s_star = np.full(n, np.nan)
    q_star = np.full(n, np.nan)

    steps = int(U_MAX / DU)
    for i in range(steps):
        active = ~restart
        if not active.any():
            break
        idx = np.where(active)[0]
        u = i * DU
        exp3 = np.exp(-3.0 * u)
        exp4 = np.exp(-4.0 * u)
        e2 = 1.0 + c_m[idx] * exp3 + c_r[idx] * exp4
        s_cap = 1.0 / e2
        omega_m = c_m[idx] * exp3 / e2
        omega_r = c_r[idx] * exp4 / e2
        omega_l = 1.0 / e2

        alpha_eff = np.zeros(len(idx))
        t = template[idx]
        mask = t == 'legacy_H_scaled_constant'
        alpha_eff[mask] = amp[idx][mask]
        mask = t == 'fixed_physical_clock_Gamma_const'
        alpha_eff[mask] = amp[idx][mask] / np.sqrt(e2[mask])
        mask = t == 'capacity_growth_locked_dlnScap'
        alpha_eff[mask] = amp[idx][mask] * (3.0 * c_m[idx][mask] * exp3 + 4.0 * c_r[idx][mask] * exp4) / e2[mask]
        mask = t == 'matter_fraction_window'
        alpha_eff[mask] = amp[idx][mask] * omega_m[mask]
        mask = t == 'radiation_fraction_window'
        alpha_eff[mask] = amp[idx][mask] * omega_r[mask]
        mask = t == 'matter_lambda_transition_window'
        alpha_eff[mask] = amp[idx][mask] * 4.0 * omega_m[mask] * omega_l[mask]

        delta_s[idx] = s_cap + (delta_s[idx] - s_cap) * np.exp(-alpha_eff * DU)
        integrated_alpha[idx] += alpha_eff * DU

        u_next = (i + 1) * DU
        e2_next = 1.0 + c_m[idx] * np.exp(-3.0 * u_next) + c_r[idx] * np.exp(-4.0 * u_next)
        s_next = 1.0 / e2_next
        q_eff = delta_s[idx] / s_next
        hit = q_eff >= qcrit[idx]
        if hit.any():
            hidx = idx[hit]
            restart[hidx] = True
            u_star[hidx] = u_next
            s_star[hidx] = s_next[hit]
            q_star[hidx] = q_eff[hit]

    idx = np.where(~restart)[0]
    e2_final = 1.0 + c_m[idx] * np.exp(-3.0 * U_MAX) + c_r[idx] * np.exp(-4.0 * U_MAX)
    s_final = 1.0 / e2_final
    s_star[idx] = s_final
    q_star[idx] = delta_s[idx] / s_final

    classification = [classify(r, u, s, q, qc) for r, u, s, q, qc in zip(restart, u_star, s_star, q_star, qcrit)]
    df = pd.DataFrame({
        'alpha_template': template,
        'C_m': c_m.astype(int),
        'C_r': c_r.astype(int),
        'amplitude': amp,
        'qcrit': qcrit,
        'restart': restart,
        'u_star_or_umax': u_star,
        'log10_a_ratio': u_star / math.log(10),
        'S_cap': s_star,
        'DeltaS': delta_s,
        'q_eff': q_star,
        'integrated_alpha': integrated_alpha,
        'classification': classification,
    })
    return df

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--outdir', default='outputs/v13B')
    args = ap.parse_args()
    out = Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)
    df = run_scan()
    df.to_csv(out / 'SCT_v1_3_B_alpha_template_dynamic_scan.csv', index=False)
    counts = df.groupby(['alpha_template', 'classification']).size().reset_index(name='count')
    counts.to_csv(out / 'SCT_v1_3_B_alpha_template_counts.csv', index=False)
    summary = df.groupby('alpha_template').agg(
        total_cases=('classification', 'size'),
        restarts=('restart', 'sum'),
        median_u_restart=('u_star_or_umax', lambda s: s[df.loc[s.index, 'restart']].median()),
        ok_toy=('classification', lambda s: int((s == 'ok toy').sum())),
        failures=('classification', lambda s: int((s == 'fallisce: nessun restart entro u_max').sum())),
    ).reset_index()
    summary.to_csv(out / 'SCT_v1_3_B_alpha_template_summary.csv', index=False)
    print(f'v1.3-B rows={len(df)} ok_toy={(df.classification == "ok toy").sum()} outdir={out}')

if __name__ == '__main__':
    main()
