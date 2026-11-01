# Theorem statement (exact)

Let `m ≥ 2`, `1 ≤ k ≤ m`, and let `U_k(a) : H_k → H_{k−1}` be the weighted
up-operator of the Boolean lattice (see `proofs/operator-definitions.md`).

**Theorem.** For all `m ≥ 2`, `1 ≤ k ≤ m`, and `a ∈ ℝᵐ`,

```
‖U_k(a)‖² ≤ k(m − k + 1)/m · Σᵢ aᵢ² .
```

The constant `C(m, k) = k(m − k + 1)/m` is best possible. Moreover:

1. for `k = 1` and `k = m`, equality holds for every `a`;
2. for `1 < k < m` and `a ≠ 0`, equality holds iff `|a₁| = ⋯ = |aₘ|`.

**Complex weights.** The same statement holds for `a ∈ ℂᵐ` with `Σᵢ |aᵢ|²`
on the right, and the equality classification unchanged in magnitudes
(Corollary 1 of the paper, via the exact two-sided unitary phase reduction).

**Classical content.** At `a = 1` this is the classical Boolean-lattice
up-operator spectrum `‖U_k(1)‖² = k(m − k + 1)`; that ray is cited, not
claimed. The weighted inequality and its equality rigidity are the content
of this paper (novelty status: see `docs/limitations.md`).
