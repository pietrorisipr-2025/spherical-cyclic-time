#!/usr/bin/env python3
"""Reproduce SCT v1.6-E conditional FDT Model A restricted audit.
No random numbers. Uses only the preregistered v1.6-D grid.
"""
from pathlib import Path
import argparse, json
import numpy as np
import pandas as pd

k = np.logspace(-3, 1, 512)
logk = np.log(k)

def fdt_pxi_shape(x):
    return (1.0-np.exp(-2.0*x*x))/(x*x)

def classify(row):
    FL, FS, FG = row['F_large_median'], row['F_small_median'], row['F_global_mean']
    frac_dom = row['frac_modes_F_gt_0p7']
    monotone = row['monotone_large_to_small']
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
        return 'coherent_toy', 'large_scale_partial_memory_small_scale_regeneration'
    if (0.20 <= FL < 0.30 or 0.70 < FL <= 0.90) and FS < 0.30 and monotone:
        return 'weak', 'borderline_large_scale_memory'
    return 'weak', 'not_clean_transition'

def run_scan():
    rows=[]
    for ns in [0.90,0.965,1.00,1.10]:
        Pn=(k/1.0)**(ns-1.0)
        for kc in [0.03,0.10,0.30,1.00,3.00]:
            x=k/kc
            T=np.exp(-x*x)
            shape=fdt_pxi_shape(x)
            for AF in [0.01,0.03,0.10,0.30,1.00,3.00,10.00]:
                Pxi=AF*shape
                mem=(T*T*Pn)/(T*T*Pn+Pxi+1e-300)
                large=k<0.05; mid=(k>=0.05)&(k<0.5); small=k>=0.5
                idx=np.where(mem<0.3)[0]
                row={'closure_kind':'model_A_critical_massless_FDT_toy','transfer_kind':'gaussian_diffusive_p2_FDT','n_s_proxy':ns,'k_c':kc,'p':2.0,'A_F':AF,'F_large_median':float(np.median(mem[large])),'F_mid_median':float(np.median(mem[mid])),'F_small_median':float(np.median(mem[small])),'F_global_mean':float(np.trapezoid(mem, logk)/(logk[-1]-logk[0])),'frac_modes_F_gt_0p7':float(np.mean(mem>0.7)),'frac_modes_F_0p3_to_0p7':float(np.mean((mem>=0.3)&(mem<=0.7))),'frac_modes_F_lt_0p3':float(np.mean(mem<0.3)),'transition_k_F_lt_0p3':float(k[idx[0]]) if len(idx)>0 else None,'monotone_large_to_small':bool(np.median(mem[large])>=np.median(mem[mid])>=np.median(mem[small])),'Pxi_low_k_limit':'2*A_F','Pxi_shape':'A_F*(1-exp(-2*(k/k_c)^2))/(k/k_c)^2'}
                row['classification'],row['reason']=classify(row)
                rows.append(row)
    return pd.DataFrame(rows)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--outdir', default='outputs/v16E')
    args=ap.parse_args()
    out=Path(args.outdir); out.mkdir(parents=True, exist_ok=True)
    df=run_scan()
    df.to_csv(out/'SCT_v1_6_E_conditional_FDT_ModelA_restricted_scan.csv', index=False)
    df['classification'].value_counts().rename_axis('classification').reset_index(name='count').to_csv(out/'SCT_v1_6_E_classification_counts.csv', index=False)
    df.groupby(['classification','reason']).size().reset_index(name='count').to_csv(out/'SCT_v1_6_E_classification_reason_counts.csv', index=False)
    summary={'rows':int(len(df)), 'classification_counts':{str(k):int(v) for k,v in df['classification'].value_counts().to_dict().items()}, 'coherent_fraction':float((df.classification=='coherent_toy').mean())}
    (out/'SCT_v1_6_E_summary.json').write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))
if __name__=='__main__':
    main()
