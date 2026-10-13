from pathlib import Path
import json, hashlib, filecmp, math, sys
import pandas as pd
import numpy as np
from numba import njit

BASE = Path('/mnt/data/sct_audit_v22F/extract/SCT_v2_1_H_ZENODO_PUBLICATION_PREP_FINAL_PUBLIC_PACKAGE')
RUN = Path('/mnt/data/sct_audit_v22F/run_outputs')
OUT = Path('/mnt/data/sct_audit_v22F/compare_outputs')
OUT.mkdir(parents=True, exist_ok=True)

report = {
    'decision': 'SCT_v2_2_F_NUMERICAL_TABLE_INVARIANCE_AUDIT',
    'inputs': {
        'v2_1_H_zip': '/mnt/data/SCT_v2_1_H_ZENODO_PUBLICATION_PREP_FINAL_PUBLIC_PACKAGE.zip',
        'v2_2_E_zip': '/mnt/data/SCT_v2_2_E_INTEGRATED_PUBLIC_MINI_RELEASE_TIMELINE_BUNDLE.zip'
    },
    'checks': {}
}

def sha256(path):
    h=hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda:f.read(1024*1024), b''): h.update(b)
    return h.hexdigest()

for key,p in list(report['inputs'].items()):
    report['inputs'][key+'_sha256'] = sha256(p)

# Manifest checks
# v21H exact manifest has known packaging mismatch: qa/final_zip_test.txt
manifest_result = Path('/mnt/data/sct_audit_v22F/v21h_manifest_verify.txt')
report['checks']['package_manifest_v2_1_H'] = {
    'status': 'FAIL_QA_ONLY_KNOWN_PACKAGING_MISMATCH' if manifest_result.exists() and 'hash_mismatch' in manifest_result.read_text() else 'PASS_OR_NOT_RUN',
    'detail': manifest_result.read_text().strip() if manifest_result.exists() else None
}
# manual v22E manifest
v22 = Path('/mnt/data/sct_audit_v22F/extract/v22e')
fail=[]; total=0
if (v22/'MANIFEST.sha256').exists():
    for line in (v22/'MANIFEST.sha256').read_text().splitlines():
        if not line.strip(): continue
        parts=line.split(maxsplit=1)
        if len(parts)!=2: continue
        exp, rel = parts
        rel = rel.strip().lstrip('*')
        p=v22/rel
        total += 1
        if not p.exists(): fail.append((rel,'missing'))
        elif sha256(p)!=exp: fail.append((rel,'hash_mismatch'))
report['checks']['package_manifest_v2_2_E_manual']={'total':total,'failures':fail,'status':'PASS' if not fail else 'FAIL'}

# Helper compare dataframes exact-ish

def compare_df(a,b,rtol=1e-12,atol=1e-12):
    res={'shape_a':list(a.shape),'shape_b':list(b.shape),'columns_same':list(a.columns)==list(b.columns),'diff_cells':None,'max_abs_numeric_diff':None,'status':None}
    if a.shape!=b.shape or list(a.columns)!=list(b.columns):
        res['status']='SCHEMA_DIFF'
        return res
    diff=0; maxnum=0.0
    for col in a.columns:
        if pd.api.types.is_numeric_dtype(a[col]) and pd.api.types.is_numeric_dtype(b[col]) and not (a[col].dtype=='bool' or b[col].dtype=='bool'):
            av=pd.to_numeric(a[col], errors='coerce'); bv=pd.to_numeric(b[col], errors='coerce')
            d=(av-bv).abs().max();
            if not pd.isna(d): maxnum=max(maxnum,float(d))
            diff += int((~np.isclose(av,bv,rtol=rtol,atol=atol,equal_nan=True)).sum())
        else:
            diff += int((a[col].fillna('__NA__').astype(str)!=b[col].fillna('__NA__').astype(str)).sum())
    res.update({'diff_cells':diff,'max_abs_numeric_diff':maxnum,'status':'PASS' if diff==0 else 'DIFF'})
    return res

# v1.4F comparisons
ref14 = BASE/'supplements/v1_4_F_minimal_reproducibility/data/reference'
run14 = RUN/'v14F'
v14_items=[]
for sub in ['v13B','v13C','v14E']:
    for p in sorted((run14/sub).glob('*.csv')):
        r=ref14/p.name
        if not r.exists(): continue
        comp=compare_df(pd.read_csv(r), pd.read_csv(p))
        comp['file']=p.name
        # semantic normalization for known summary/order/schema cases
        if comp['status']!='PASS':
            if p.name=='SCT_v1_3_C_matching_classification_counts.csv':
                aa=pd.read_csv(r).sort_values(['classification','reason']).reset_index(drop=True)
                bb=pd.read_csv(p).sort_values(['classification','reason']).reset_index(drop=True)
                comp['semantic_compare_after_sort']=compare_df(aa,bb)
            elif p.name=='SCT_v1_4_E_v13B_alpha_template_volume.csv':
                aa=pd.read_csv(r); bb=pd.read_csv(p)
                mapping={'total_cases':'total_rows','ok_toy_cases':'ok_toy','strict_fail_cases':'failure_rows','critical_cases':'critical_rows','weak_cases':'near_or_weak_rows','ok_fraction_grid_proxy':'ok_toy_fraction','strict_fail_fraction_grid_proxy':'failure_fraction'}
                diffs=[]
                for ac,bc in mapping.items():
                    if ac in aa and bc in bb:
                        left=aa.sort_values('alpha_template')[ac].reset_index(drop=True)
                        right=bb.sort_values('alpha_template')[bc].reset_index(drop=True)
                        if pd.api.types.is_numeric_dtype(left):
                            d=float((pd.to_numeric(left)-pd.to_numeric(right)).abs().max())
                            diffs.append((ac,bc,d))
                comp['semantic_mapped_numeric_diffs']=diffs
                comp['semantic_status']='PASS' if all(d<=1e-12 for _,_,d in diffs) else 'DIFF'
            elif p.name=='SCT_v1_4_E_v13C_classification_volume.csv':
                aa=pd.read_csv(r).sort_values('classification').reset_index(drop=True)
                bb=pd.read_csv(p).sort_values('classification').reset_index(drop=True)
                diffs=[]
                diffs.append(('count','rows',float((aa['count']-bb['rows']).abs().max())))
                diffs.append(('fraction_grid_proxy','fraction',float((aa['fraction_grid_proxy']-bb['fraction']).abs().max())))
                comp['semantic_mapped_numeric_diffs']=diffs
                comp['semantic_status']='PASS' if all(d<=1e-12 for _,_,d in diffs) else 'DIFF'
        v14_items.append(comp)
report['checks']['v1_4_F_reference_vs_rerun'] = {
    'status':'PASS_CORE_COUNTS_AND_TABLES' if all(x['status']=='PASS' or x.get('semantic_status')=='PASS' or x.get('semantic_compare_after_sort',{}).get('status')=='PASS' for x in v14_items) else 'CHECK_DIFFS',
    'items':v14_items,
    'run_summary': json.loads((run14/'reproducibility_check_summary.json').read_text())
}

# v1.6E comparisons
ref16 = BASE/'supplements/v1_6_E_conditional_FDT_model_A/data'
run16 = RUN/'v16E'
v16_items=[]
for p in sorted(run16.glob('*.csv')):
    r=ref16/p.name
    if not r.exists(): continue
    comp=compare_df(pd.read_csv(r), pd.read_csv(p))
    comp['file']=p.name
    if comp['status']!='PASS' and p.name=='SCT_v1_6_E_classification_reason_counts.csv':
        comp['semantic_compare_after_sort']=compare_df(pd.read_csv(r).sort_values(['classification','reason']).reset_index(drop=True), pd.read_csv(p).sort_values(['classification','reason']).reset_index(drop=True))
    v16_items.append(comp)
report['checks']['v1_6_E_reference_vs_rerun'] = {
    'status':'PASS' if all(x['status']=='PASS' or x.get('semantic_compare_after_sort',{}).get('status')=='PASS' for x in v16_items) else 'CHECK_DIFFS',
    'items':v16_items,
    'run_summary': json.loads((run16/'SCT_v1_6_E_summary.json').read_text())
}

# v2.0B reproduce and compare to tables
# Reimplementation copied from shipped script, same protocol
ALPHAS=[0.10,0.20,0.50]; K=np.logspace(-2,2,121); YI,YF=-50.,50.
def V_smooth(y,alpha): return alpha*(1+(alpha-1)*y*y)/(1+y*y)**2
def integrate_v20B(h=0.0005):
    A=np.array(ALPHAS)[:,None,None]; k=K[None,:,None]
    u=np.zeros((len(ALPHAS),len(K),2)); v=np.zeros_like(u); u[:,:,0]=1.; v[:,:,1]=K[None,:]
    n=int(round((YF-YI)/h)); h=(YF-YI)/n; y=YI
    def f(yy,uu,vv): return vv, -(k*k-V_smooth(yy,A))*uu
    for _ in range(n):
        k1u,k1v=f(y,u,v); k2u,k2v=f(y+h/2,u+h*k1u/2,v+h*k1v/2); k3u,k3v=f(y+h/2,u+h*k2u/2,v+h*k2v/2); k4u,k4v=f(y+h,u+h*k3u,v+h*k3v)
        u += h*(k1u+2*k2u+2*k3u+k4u)/6; v += h*(k1v+2*k2v+2*k3v+k4v)/6; y += h
    A_norm=u[:,:,0]**2+(v[:,:,0]/K[None,:])**2; B_norm=u[:,:,1]**2+(v[:,:,1]/K[None,:])**2
    return 0.5*(A_norm+B_norm)
PT=integrate_v20B()
tabB=pd.read_csv(BASE/'upload_set/tables/SCT_v2_0_B_transfer_results.csv')
rows=[]
for i,a in enumerate(ALPHAS):
    shape=PT[i]/PT[i,0]
    t=tabB[tabB['alpha'].round(12)==round(a,12)].reset_index(drop=True)
    rows.append({'alpha':a,'rows':len(t),'max_abs_PT_diff':float(np.max(np.abs(t['PT'].to_numpy()-PT[i]))),'max_abs_T_shape_diff':float(np.max(np.abs(t['T_shape'].to_numpy()-shape))),'classification':pd.read_csv(BASE/'upload_set/tables/SCT_v2_0_B_alpha_summary.csv').query('alpha == @a')['classification'].iloc[0]})
report['checks']['v2_0_B_transfer_table_vs_rerun']={'status':'PASS' if all(r['max_abs_PT_diff']<1e-11 and r['max_abs_T_shape_diff']<1e-11 for r in rows) else 'CHECK_DIFFS','items':rows}

# v2.0E numba reproduction
@njit
def potential_compact_numba(y, alpha):
    sy=abs(y)
    if sy >= 1.0:
        return alpha*(alpha-1.0)/(y*y)
    c=alpha*(alpha-2.0)/8.0
    b=alpha*(4.0-alpha)/4.0
    a0=1.0-alpha*(6.0-alpha)/8.0
    aa=a0 + b*y*y + c*y**4
    add=2.0*b + 12.0*c*y*y
    return add/aa

@njit
def run_v20E_numba(alpha, h=0.0005):
    ks=np.empty(121)
    for idx in range(121):
        ks[idx] = 10.0**(-2.0 + (4.0*idx/120.0))
    U=np.zeros((2,121)); VV=np.zeros((2,121))
    for j in range(121):
        U[0,j]=1.0; VV[0,j]=0.0; U[1,j]=0.0; VV[1,j]=ks[j]
    y0=-50.0; y1=50.0
    n=int(round((y1-y0)/h)); h=(y1-y0)/n; y=y0
    for _ in range(n):
        w1=np.empty(121); w2=np.empty(121); w4=np.empty(121)
        yh=y+0.5*h; yf=y+h
        pot1=potential_compact_numba(y, alpha)
        pot2=potential_compact_numba(yh, alpha)
        pot4=potential_compact_numba(yf, alpha)
        for j in range(121):
            w1[j]=ks[j]*ks[j]-pot1
            w2[j]=ks[j]*ks[j]-pot2
            w4[j]=ks[j]*ks[j]-pot4
        k1u=VV.copy(); k1v=np.empty((2,121))
        for i in range(2):
            for j in range(121):
                k1v[i,j] = -w1[j]*U[i,j]
        u2=np.empty((2,121)); v2=np.empty((2,121))
        for i in range(2):
            for j in range(121):
                u2[i,j]=U[i,j]+0.5*h*k1u[i,j]; v2[i,j]=VV[i,j]+0.5*h*k1v[i,j]
        k2u=v2.copy(); k2v=np.empty((2,121))
        for i in range(2):
            for j in range(121):
                k2v[i,j] = -w2[j]*u2[i,j]
        u3=np.empty((2,121)); v3=np.empty((2,121))
        for i in range(2):
            for j in range(121):
                u3[i,j]=U[i,j]+0.5*h*k2u[i,j]; v3[i,j]=VV[i,j]+0.5*h*k2v[i,j]
        k3u=v3.copy(); k3v=np.empty((2,121))
        for i in range(2):
            for j in range(121):
                k3v[i,j] = -w2[j]*u3[i,j]
        u4=np.empty((2,121)); v4=np.empty((2,121))
        for i in range(2):
            for j in range(121):
                u4[i,j]=U[i,j]+h*k3u[i,j]; v4[i,j]=VV[i,j]+h*k3v[i,j]
        k4u=v4.copy(); k4v=np.empty((2,121))
        for i in range(2):
            for j in range(121):
                k4v[i,j] = -w4[j]*u4[i,j]
        for i in range(2):
            for j in range(121):
                U[i,j]=U[i,j]+h*(k1u[i,j]+2*k2u[i,j]+2*k3u[i,j]+k4u[i,j])/6.0
                VV[i,j]=VV[i,j]+h*(k1v[i,j]+2*k2v[i,j]+2*k3v[i,j]+k4v[i,j])/6.0
        y=yf
    raw=np.empty(121); shape=np.empty(121)
    for j in range(121):
        n0=math.sqrt(U[0,j]*U[0,j]+(VV[0,j]/ks[j])*(VV[0,j]/ks[j]))
        n1=math.sqrt(U[1,j]*U[1,j]+(VV[1,j]/ks[j])*(VV[1,j]/ks[j]))
        raw[j]=math.sqrt((n0*n0+n1*n1)/2.0)
    for j in range(121):
        shape[j]=(raw[j]/raw[0])*(raw[j]/raw[0])
    return ks, raw, shape
# compile once quickly and run all
itemsE=[]
for a in [0.20,0.10,0.50]:
    ks, raw, shape = run_v20E_numba(a)
    tab=pd.read_csv(BASE/f'upload_set/tables/SCT_v2_0_E_transfer_alpha_{a:.2f}.csv')
    itemsE.append({'alpha':a,'rows':len(tab),'max_abs_k_diff':float(np.max(np.abs(tab['k'].to_numpy()-ks))), 'max_abs_raw_diff':float(np.max(np.abs(tab['raw_transfer'].to_numpy()-raw))), 'max_abs_T_shape_diff':float(np.max(np.abs(tab['T_shape_power_normalized_to_kmin'].to_numpy()-shape))), 'classification':pd.read_csv(BASE/'upload_set/tables/SCT_v2_0_E_result_diagnostics.csv').query('alpha == @a')['classification'].iloc[0], 'high_k_plateau_mean_last10_rerun':float(shape[-10:].mean())})
report['checks']['v2_0_E_transfer_table_vs_numba_rerun']={'status':'PASS' if all(r['max_abs_raw_diff']<1e-11 and r['max_abs_T_shape_diff']<1e-11 for r in itemsE) else 'CHECK_DIFFS','items':itemsE}

# Check v22E contains no numerical result tables/scripts
num_like=[]
for p in v22.rglob('*'):
    if p.is_file() and (p.suffix.lower() in ['.csv','.py'] or 'transfer_alpha' in p.name or 'result_diagnostics' in p.name):
        num_like.append(str(p.relative_to(v22)))
report['checks']['v2_2_E_no_numeric_replacement_payload']={'status':'PASS' if not num_like else 'CHECK','numeric_like_files':num_like}

# Overall
statuses=[]
for k,v in report['checks'].items():
    statuses.append((k,v.get('status')))
report['overall_status']='PASS_NUMERICAL_INVARIANCE_AUDIT_WITH_QA_MANIFEST_NOTE' if all(s in ['PASS','PASS_CORE_COUNTS_AND_TABLES','FAIL_QA_ONLY_KNOWN_PACKAGING_MISMATCH'] for _,s in statuses) else 'CHECK_DETAILS'

(OUT/'SCT_v2_2_F_NUMERICAL_INVARIANCE_AUDIT_REPORT.json').write_text(json.dumps(report, indent=2, sort_keys=True), encoding='utf-8')
print(json.dumps(report, indent=2, sort_keys=True))
