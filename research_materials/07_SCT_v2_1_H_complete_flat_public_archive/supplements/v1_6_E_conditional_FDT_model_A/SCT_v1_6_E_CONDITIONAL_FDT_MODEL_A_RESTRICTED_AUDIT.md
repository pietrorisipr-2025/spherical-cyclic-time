# SCT v1.6-E — Conditional FDT Model A Restricted Audit

## Question
Execute the v1.6-D preregistered conditional Model-A/FDT closure, without reopening the transfer exponent, without using a power-law regenerated spectrum, and without selecting parameters after observing restart success.

## Preregistered closure

[
T_R(k)=exp[-(k/k_c)^2]
]

[
P_xi(k)=A_F\,frac{1-exp[-2(k/k_c)^2]}{(k/k_c)^2}
]

with finite low-k limit \(P_xi to 2A_F\). The axes are exactly those locked in v1.6-D:

- \(n_s^{proxy}in{0.9,0.965,1.0,1.1}\)
- \(k_cin{0.03,0.1,0.3,1.0,3.0}\)
- \(A_Fin{0.01,0.03,0.1,0.3,1.0,3.0,10.0}\)
- \(p=2\) fixed
- no \(n_\xi\) axis

Total cells: 140.

## Result

Classification counts:

| classification | count |
|---|---:|
| weak | 52 |
| failed | 35 |
| critical | 28 |
| coherent_toy | 25 |


The coherent toy region is nonempty but still conditional:

[
N_{coherent}=25/140 approx 17.86%.
]

## Interpretation

The FDT closure improves the internal discipline of the regenerated component because \(P_xi(k)\) is no longer an arbitrary power law. It is fixed by the conditional bath/free-energy model once \(k_c\) and \(A_F\) are specified. However, SCT still does not derive the bath, the free-energy functional, the amplitude \(A_F\), or the numerical value of \(k_c\) from a cosmological action.

Therefore the result supports only a **conditional toy restart region**, not a physical restart claim.

## Main comparison to v1.5-D

v1.5-D used a Gaussian transfer with a power-law \(P_xi\) grid and had 31 coherent toy rows out of 560. v1.6-E uses a stricter FDT-shaped \(P_xi\) and has 25 coherent toy rows out of 140. These fractions are not a physical improvement metric because the parameter axes differ; the relevant improvement is structural: no free \(n_\xi\) power-law axis remains.

## Claim boundary

- No physical restart is derived.
- No microphysical bath is derived.
- No cosmological action, gauge-invariant perturbation variable, or causal transition model is derived.
- No observational prediction is claimed.
- The result is a preregistered, deterministic toy audit.
