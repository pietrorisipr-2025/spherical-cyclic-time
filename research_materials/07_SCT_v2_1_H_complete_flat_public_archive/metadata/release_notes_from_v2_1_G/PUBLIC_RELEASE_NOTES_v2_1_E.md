# Public Release Notes - SCT v2.1-E

This public patch implements the transfer-route decision reached after v2.0-A..F and v2.1-A..D.

Main change: the gaussian/diffusive transfer kernel is demoted from the default closed-background transfer language. The conservative mainline now treats `T_R(k)` as a model-dependent transfer operator.

Evidence: two preregistered closed deterministic proxy tests returned non-gaussian, bounded, high-k plateau-like transfer shapes. The mechanism is high-k transparency of the closed proxy equation combined with low-k amplification under the chosen normalization.

Boundary: this is a limited toy/computational update, not a physical cosmology result, not an observational prediction, and not a no-go theorem.
