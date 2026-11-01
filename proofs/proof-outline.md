# Proof outline and dependency map

Theorem (see `docs/theorem-statement.md`): for all `m ≥ 2`, `1 ≤ k ≤ m`,
`a ∈ ℝᵐ`: `‖U_k(a)‖² ≤ C(m,k) Σ aᵢ²`, sharp; interior equality (`a ≠ 0`)
iff all `|aᵢ|` equal.

Dependency order (acyclic; every item is proved in the paper):

```
L1  Phase reduction        U_k(a) = D_r U_k(|a|) D_c  ⇒  reduce to a ≥ 0
L2  Block deletion identity U_k(a) ≃ [[U_k(a′), a_m I],[0, U_{k−1}(a′)]]
    Gram form              U Uᵀ ≃ [[U_k U_kᵀ + a_m² I, a_m U_{k−1}ᵀ],
                                    [a_m U_{k−1},      U_{k−1} U_{k−1}ᵀ]]
    with s₁(a_m U_{k−1}ᵀ) = a_m ‖U_{k−1}(a′)‖ exactly
L3  Block-norm lemma       λmax([[P,Q],[Qᵀ,R]]) ≤ λmax([[λmax(P), s₁(Q)],
                                    [s₁(Q), λmax(R)]]);  2×2 corner
    monotone in p, q, |o|  (closed form + derivative signs)
L4  Strong induction on m  base m = 2; endpoints k = 1, m exact; interior
    simultaneous in k      step: IH at (m−1, k) and (m−1, k−1), monotone
                           corner substitution
L5  Closure lemma          λmax([[A+t, √(tB)],[√(tB), B]]) ≤ C(1+t), where
                           A = C(m−1,k), B = C(m−1,k−1), C = C(m,k);
           X(t)² − [(A−B+t)² + 4Bt]
         = 4k(k−1)(m−k)(m−k+1) ((m−1)t − 1)² / (m²(m−1)²) ≥ 0
    (identity in general (m,k,t)); squaring legitimate since X(t) > 0 for
    t ≥ 0 (affine, slope 2C−1 ≥ 1 > 0, intercept X(0) > 0); equality iff
    t = 1/(m−1) for interior k
L6  Equality classification chain forcing L5 ⇒ t = 1/(m−1); strict corner
    monotonicity ⇒ equality at children; boundary-child bookkeeping for
    k = 2, k = m−1; base m = 3, k = 2 by AM–GM determinant; converse via
    L1 + sharpness
SH  Sharpness              λmax(U_k(1) U_k(1)ᵀ) = k(m−k+1) (classical,
                           cited); attained at a = 1 at every level
```

The written proof in `paper/weighted-johnson.tex` is self-contained; the
machine checks in `verification/` are regression evidence only.
