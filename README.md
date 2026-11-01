# A Sharp Norm Bound for Weighted Up-Operators on the Boolean Lattice

**Paper:** `paper/weighted-johnson.pdf` (LaTeX source `paper/weighted-johnson.tex`, ~9 pages)

## Abstract (short)

For weights `a = (a_1, …, a_m)` and `1 ≤ k ≤ m`, let

```
U_k(a) : H_k → H_{k-1}
```

be the weighted up-operator on the Boolean lattice — the weighted `(k, k−1)`
inclusion matrix — where `H_j = ℓ²([m] choose j)` has orthonormal basis
`{e_S : |S| = j}`, and

```
(U_k(a) f)(S) = Σ_{i ∉ S} a_i f(S ∪ {i}),   |S| = k − 1.
```

We prove the sharp inequality

```
‖U_k(a)‖² ≤ k(m − k + 1)/m · Σᵢ |aᵢ|²
```

with equality for all `a` at the endpoints `k = 1, m` and, for interior `k`
and `a ≠ 0`, if and only if `|a₁| = … = |aₘ|`. The classical equal-weight
identity `‖U_k(1)‖² = k(m − k + 1)` is the case `a = 1`.

## Exact theorem statement

**Theorem.** For all `m ≥ 2`, `1 ≤ k ≤ m`, and `a ∈ ℝᵐ`,

```
‖U_k(a)‖² ≤ k(m − k + 1)/m · Σᵢ aᵢ² .
```

The constant `C(m, k) = k(m − k + 1)/m` is best possible. Moreover:

1. for `k = 1` and `k = m`, equality holds for every `a`;
2. for `1 < k < m` and `a ≠ 0`, equality holds **iff** `|a₁| = ⋯ = |aₘ|`.

The same statement holds for complex weights `a ∈ ℂᵐ` with `Σᵢ |aᵢ|²`
(two-sided unitary phase reduction, Corollary 1 in the paper).

## Why the constant is the right one

At `a = 1` the operator is the classical Boolean up-operator, whose top
singular value squared is exactly `k(m − k + 1)` (Johnson-scheme spectrum).
Since `Σᵢ 1² = m`, the bound reads `k(m − k + 1) ≤ C(m,k) · m` with equality,
so no smaller constant works at any level: the rescaled classical constant
is optimal, and the theorem says generic weights can never beat it. For
generic `a` the association-scheme diagonalization is unavailable, so the
weighted statement is out of reach of the classical spectral toolkit.

## Proof strategy

A coordinate-deletion induction (strong induction on `m`, simultaneous in
`k`): deleting a coordinate gives the exact block form
`U_k(a) ≃ [[U_k(a′), aₘ I], [0, U_{k−1}(a′)]]`; a block-norm comparison
reduces the top eigenvalue to a `2 × 2` corner matrix; the induction
hypothesis bounds its two diagonal entries; and the scalar closure
inequality closes the argument because the squared defect factors as the
perfect square

```
4k(k−1)(m−k)(m−k+1) / (m²(m−1)²) · ((m−1)t − 1)² ≥ 0,
```

an identity in general `(m, k, t)`, with equality iff `t = 1/(m−1)`.
Equality cases are obtained by tracing equality through every step.
See `proofs/proof-outline.md` for the dependency map.

## Compile the paper

```
cd paper
tectonic weighted-johnson.tex     # or: pdflatex weighted-johnson.tex (twice)
```

No custom style files are required (standard `article` class).

## Reproduce the computational checks

```
cd verification
pip install -r requirements.txt   # numpy==2.4.3, sympy==1.14.0
python3 verify.py                 # ~2–5 min, ends with "ALL RECEIPTS COMPLETE"
```

The symbolic closure identity is verified as an identity in **general
symbols** `(m, k, t)` — not from finite samples. Exact and symbolic checks
are separated from illustrative regression tests inside `verify.py`
(sections 3a/3b symbolic; section 7 exact-rational regression). See
`verification/README.md`.

## Known limitations

- The method is specific to the Boolean lattice level structure.
- Only the top eigenvalue of `U_k(a) U_k(a)ᵀ` is controlled, not the full spectrum.
- Novelty: the equal-weight ray is classical and cited. The weighted sharp
  bound with its equality classification surfaced in no surveyed source, but
  a full MathSciNet-level literature check by a human remains open
  (classification: PLAUSIBLY NEW — SEARCH INCOMPLETE).
- Connections to Riemann-hypothesis-type operator programs are historical
  motivation only; this paper makes **no** RH claim. See `docs/limitations.md`.

## Verification and review status (accurate)

- Every identity used in the proof is written in closed form in the paper;
  no proof step requires computer assistance.
- Machine verification: general-symbolic proof of the closure identity and
  an independent from-the-definition battery (exact block/Gram/duality/phase
  identities, sharpness for `m ≤ 8`, 30 exact rational inequality instances,
  zero violations).
- The manuscript passed independent adversarial AI review rounds with zero
  mathematical objections. **Independent human review has not yet been
  performed**; this repository is offered to support exactly that review.

## AI assistance disclosure

The proof search, symbolic verification, literature screening, and
manuscript preparation were performed with substantial assistance from an
AI research agent (LLM-based, 2026). The human author takes full
responsibility for all claims. No AI system is presented as an author, and
no AI review is presented as peer review.

## License

Licensing is pending the author's choice (options under consideration:
CC BY 4.0 for the text, MIT for the verification code). Until then, all
rights are reserved.

## Repository layout

```
paper/         manuscript (tex, pdf) + references.bib
proofs/        proof outline, operator definitions, verification notes
verification/  verify.py + pinned requirements + instructions
docs/          theorem statement, reproducibility, limitations
```
