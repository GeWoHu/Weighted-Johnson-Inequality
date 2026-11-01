# Verification notes

Two kinds of checks are provided, deliberately separated:

**Symbolic (universal, general parameters).**
- The closure identity `X(t)² − [(A−B+t)² + 4Bt] =
  4k(k−1)(m−k)(m−k+1)((m−1)t−1)²/(m²(m−1)²)` is verified by sympy as a
  rational-function identity in **general symbols** `(m, k, t)` — not
  inferred from finite samples (`verify.py` section 3a/3b).
- Monotonicity of the 2×2 corner eigenvalue is confirmed from the closed
  form of its partial derivatives (section 4).

**Exact / illustrative (finite, regression evidence).**
- Block and Gram identities checked entrywise on concrete parameters
  (sections 1–2), including the exact singular value of the off-diagonal block.
- Sharpness `λmax(U_k(1)U_k(1)ᵀ) = k(m−k+1)` computed exactly for `m ≤ 8`,
  all `k` (section 5).
- Complement duality as an exact permutation identity (section 6).
- The inequality at 30 exact rational instances with certified real-root
  isolation of spectral maxima: zero violations, worst ratio 0.979016
  (section 7).
- Degenerate cases: `a′ = 0`, zero coordinates, equal weights (attainment),
  perturbed equal weights (strictness) (section 8).
- Complex phase reduction on a random complex instance (section 9).
- Block-norm lemma stress test, 200 random symmetric block matrices
  (section 10).

**Status of the mathematics.** Every step of the written proof is either an
exact identity, an elementary lemma with a written proof, or the symbolic
closure identity above. No step requires computer assistance. The manuscript
passed independent adversarial AI review rounds with zero mathematical
objections; an independent human referee has not yet reviewed it, and this
package is designed to support exactly that review.
