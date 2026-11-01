# A Sharp Norm Bound for Weighted Up-Operators on the Boolean Lattice

A short mathematical note (with a fully reproducible verification package)
on the operator norm of weighted inclusion matrices between adjacent levels
of the Boolean lattice, plus an application to a squarefree arithmetic
compression of a von Mangoldt-type operator.

**Paper:** [PDF](paper/weighted-johnson.pdf) ·
[LaTeX source](paper/weighted-johnson.tex) ·
[proof outline](proofs/proof-outline.md) ·
[reproducibility](docs/reproducibility.md)

## Abstract

For `a = (a₁,…,a_m) ∈ ℂᵐ` and `1 ≤ k ≤ m`, let `U_k(a)` be the weighted
up-operator — the weighted `(k, k−1)` inclusion matrix — acting from
`H_k = ℓ²([m] choose k)` to `H_{k−1} = ℓ²([m] choose k−1)` (orthonormal
subset basis) by

```
(U_k(a) f)(S) = Σ_{i ∉ S} aᵢ f(S ∪ {i}),    |S| = k − 1.
```

The paper proves the sharp inequality

```
‖U_k(a)‖² ≤ k(m − k + 1)/m · Σᵢ |aᵢ|²,
```

with an exact equality classification, and applies it to an arithmetic
operator on squarefree integers.

## Main theorem

For all `m ≥ 2`, `1 ≤ k ≤ m`, and `a ∈ ℂᵐ`,

```
‖U_k(a)‖² ≤ (k(m − k + 1) / m) · Σᵢ |aᵢ|².
```

The indexing is exact: `U_k(a)` maps level `k` down to level `k − 1`, and
the sum defining `(U_k(a)f)(S)` runs over the `m − k + 1` coordinates
`i ∉ S`. By complement duality the same bound holds for the weighted
down-operators `U_k(a)*`.

## Sharpness

The constant `C(m,k) = k(m−k+1)/m` cannot be lowered: at `a = 1` the
operator is the classical Boolean up-operator with
`‖U_k(1)‖² = k(m−k+1)` exactly, while `Σᵢ |1|² = m`.

Equality classification (for `a ≠ 0`):

- `k = 1` or `k = m`: equality for every `a`;
- `1 < k < m`: equality **iff** all `|aᵢ|` are equal.

Generic weights destroy the association-scheme diagonalization, so the
weighted statement is out of reach of the classical Johnson-scheme spectral
method; the proof replaces it with a coordinate-deletion induction.

## Proof overview

A two-page induction with a scalar closure step:

1. **Phase reduction.** `U_k(a) = D_r U_k(|a|) D_c` (diagonal unitaries),
   so it suffices to treat nonnegative weights.
2. **Coordinate deletion.** Splitting on the last coordinate gives the
   exact block form `U_k(a) ≃ [[U_k(a′), aₘ I], [0, U_{k−1}(a′)]]`.
3. **Corner comparison.** The top eigenvalue of `U_k(a)U_k(a)*` reduces to
   a `2×2` corner matrix whose diagonal entries the induction hypothesis
   bounds.
4. **Scalar closure.** The remaining one-variable inequality closes
   because the squared defect factors as a perfect square,

   ```
   4k(k−1)(m−k)(m−k+1) / (m²(m−1)²) · ((m−1)t − 1)² ≥ 0,
   ```

   an identity in general `(m, k, t)` — equality iff `t = 1/(m−1)`, which
   drives the equality classification.

See `proofs/proof-outline.md` for the dependency map and
`proofs/operator-definitions.md` for conventions.

## Arithmetic application (Section 6 of the paper)

On `ℓ²({1..N}, φ)` define the von Mangoldt operator
`T_N y(r) = Σ_{k ≤ N/r} Λ(k) y(rk)` and let `P_sqf` be the orthogonal
projection onto squarefree indices. Squarefree-to-squarefree edges are
exactly `s = rp` with `p ∤ r`, so the compression is entrywise a sum of
weighted Boolean-lattice incidence blocks with prime weights
`a_p = log p / √(p−1)`. Level orthogonality (via the adjoint `S*S`
argument, using both domain and range decompositions) gives

```
‖P_sqf T_N P_sqf‖² = sup_k ‖V_k‖² ≤ k_max(N) · Σ_{p≤N} (log p)²/(p−1)
                   = (1/2 + o(1)) · (log N)³ / log log N,
```

unconditionally. **Scope:** this bounds the squarefree compression only —
not the full operator `T_N`. It does **not** imply `‖T_N‖ = O(log N)`, does
not address Nyman–Beurling distances or zero-free regions, and makes no
claim about the Riemann Hypothesis (which appears in neither title nor
abstract). A complementary proved lower bound,
`‖T_N‖ ≥ (1/√2 + o(1)) log N` via the adjoint test vector `T_N* e₁`, is
recorded in the paper. Regression code:
[`verification/verify_arithmetic.py`](verification/verify_arithmetic.py).

## Reproducing the checks

Requires Python 3.12+ with `numpy==2.4.3` and `sympy==1.14.0`
(see `verification/requirements.txt`); no other services or dependencies.

```
cd verification
pip install -r requirements.txt
python3 verify.py                # ~2–5 min; final line: ALL RECEIPTS COMPLETE
python3 verify_arithmetic.py     # final line: ALL PASS
```

`verify.py` checks the general-symbolic closure identity in parameters
`(m, k, t)` (a universal symbolic proof) and runs exact/floating-point
regression batteries built from the definition alone.
`verify_arithmetic.py` rebuilds the Section 6 object from the matrix
definition and checks the compression identity, cross-level block
diagonality of `S*S`, the certified inequality, and the adjoint
lower-bound identity. Finite tests are regression evidence, **not** proofs
of universal statements; the paper's proofs stand on their own. To rebuild
the PDF: `cd paper && tectonic weighted-johnson.tex` (or `pdflatex` ×2).
Failure behavior: any check violation prints `FAIL` with the offending
instance and the script exits non-zero.

## Research and review status

- **Proof status:** self-contained written proof; every identity stated in
  closed form; no step requires computer assistance.
- **Machine verification:** general-symbolic closure identity +
  independent from-the-definition batteries; zero violations.
- **Adversarial AI review:** multiple isolated AI referee rounds, including
  a fresh reviewer with no project context; findings repaired. These are
  self-checks, **not peer review**.
- **Independent human mathematical review: pending.**
- **Novelty verification: incomplete.** The equal-weight ray is classical
  and cited; the weighted sharp bound with equality classification surfaced
  in no surveyed source, but MathSciNet-level checks remain open
  (classification: PLAUSIBLY NEW — SEARCH INCOMPLETE). See
  [`docs/limitations.md`](docs/limitations.md).

## Citation and licensing

See [`CITATION.cff`](CITATION.cff). Recommended citation until a journal
version exists:

> Gerald, "A Sharp Norm Bound for Weighted Up-Operators on the Boolean
> Lattice," GitHub repository GeWoHu/weighted-johnson-inequality, 2026.
> https://github.com/GeWoHu/weighted-johnson-inequality

The author's full legal name and affiliation will be supplied before
submission (placeholder retained deliberately; nothing invented).

## License

This is an openly shared, AI-assisted mathematical research result. The
theorem and proof are publicly available for independent verification and
reuse. The mathematical statement itself is not claimed as exclusive
intellectual property.

- **Manuscript, mathematical exposition, and documentation** (paper text,
  `docs/`, `proofs/`, `README.md`): dedicated to the public domain under
  [CC0 1.0 Universal](LICENSE-CC0), to the extent possible under law.
  No attribution is required for reuse of the text.
- **Verification software** (`verification/`): released under the
  [MIT License](LICENSE-MIT). MIT's only condition for code reuse is
  preservation of the copyright and permission notice in copies or
  substantial portions of the software.

CC0 does not eliminate rights that cannot be waived under some legal
systems, does not guarantee public-domain status in every jurisdiction,
and does not affect third-party rights. Independent human mathematical
peer review has not occurred. No connection to a solution of the Riemann
Hypothesis is claimed.

## AI assistance

Proof search, symbolic verification, literature screening, and manuscript
preparation were performed with substantial assistance from an AI research
agent (LLM-based, 2026). The human author takes full responsibility for
all claims. No AI system is presented as an author and no AI review is
presented as peer review. Details: [`docs/ai-assistance.md`](docs/ai-assistance.md).

## Repository layout

```
paper/         manuscript (tex, pdf) + references.bib
proofs/        proof outline, operator definitions, verification notes
verification/  verify.py, verify_arithmetic.py, pinned requirements
docs/          reproducibility, limitations, theorem statement, AI disclosure
```
