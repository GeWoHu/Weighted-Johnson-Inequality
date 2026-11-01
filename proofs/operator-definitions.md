# Operator definitions (canonical conventions)

`[m] = {1, …, m}`. For `0 ≤ j ≤ m`, `H_j = ℓ²([m] choose j)` is the Euclidean
space with orthonormal basis `{e_S : |S| = j}`.

**Weighted up-operator.** For weights `a ∈ ℂᵐ` and `1 ≤ k ≤ m`,

```
U_k(a) : H_k → H_{k−1},
(U_k(a) f)(S) = Σ_{i ∉ S} a_i f(S ∪ {i}),   |S| = k − 1.
```

Matrix form in the subset basis (the weighted `(k, k−1)` inclusion matrix):
the `(S, T)` entry equals `a_i` if `T = S ∪ {i}`, and `0` otherwise; rows are
`(k−1)`-sets, columns are `k`-sets.

`‖·‖` always denotes the operator norm `H_k → H_{k−1}` for the Euclidean
norms (equivalently, the largest singular value `s₁`).

**Constants.** `C(m, k) = k(m − k + 1)/m`.

**Gram operator.** `G_k(a) = U_k(a) U_k(a)ᵀ` on `H_{k−1}`, so
`‖U_k(a)‖² = λmax(G_k(a))`.

**Complement duality.** The unitaries `C_j : H_j → H_{m−j}`, `e_S ↦ e_{Sᶜ}`,
satisfy `C_{k−1} U_k(a) C_k = U_{m−k+1}(a)ᵀ` entrywise; hence
`‖U_k(a)‖ = ‖U_{m−k+1}(a)‖` and `C(m, k) = C(m, m−k+1)`.

**Phase reduction.** Writing `a_i = |a_i| e^{iθ_i}`, the diagonal unitaries
`D_r[S] = exp(−i Σ_{j∈S} θ_j)` on `H_{k−1}` and
`D_c[T] = exp(+i Σ_{j∈T} θ_j)` on `H_k` give the exact two-sided unitary
equivalence `U_k(a) = D_r U_k(|a|) D_c`; norms and equality cases depend only
on the magnitudes `|a|`.
