# Draft Replacement Text — Transfer Kernel Status

The transfer kernel should no longer be presented as a single gaussian default for the framework. The conservative mainline is now an unspecified transfer operator `T_R(k)` whose form depends on the route by which the restart/transition is modeled.

For an open-system or diffusive toy route, a gaussian kernel such as

```text
T_R(k)=exp[-(k/k_c)^2]
```

remains a conditional toy limit, requiring an independently specified dissipative or coarse-graining mechanism.

For the closed deterministic background route tested in v2.0, two preregistered toy background families did not produce gaussian damping. They produced bounded, plateau-like transfer shapes. This does not constitute a no-go theorem for cyclic or bouncing cosmologies, but it does demote the gaussian kernel for the closed-background route.

A minimal plateau-like explanatory toy branch may be written as

```text
T_pl(k)=p_inf + (1-p_inf)/(1+(k/k_x)^2),
```

where `p_inf` is the normalized high-k plateau. This is not a physical universal kernel; it records the mechanism found in the closed proxy tests: high-k transparency plus low-k amplification under the chosen normalization.
