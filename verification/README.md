# Verification scripts

Run:

```
pip install -r requirements.txt
python3 verify.py
```

Runtime ≈ 2–5 minutes (the exact-rational spectral computations dominate).
Expected final line: `ALL RECEIPTS COMPLETE`; every section prints `PASS`.

Sections:
1. Block decomposition identity (exact, entrywise)
2. Gram off-diagonal block = `a_m · U_{k−1}(a′)ᵀ` with exact `s₁`
3. **Closure identity in general symbols `(m, k, t)`** (symbolic, universal)
4. Monotonicity of the 2×2 corner eigenvalue (symbolic derivative forms)
5. Sharp constant: exact spectrum of `U_k(1)` for `m = 2..8`
6. Complement duality (exact permutation identity)
7. Full-theorem exact-rational regression (30 instances, certified isolation)
8. Boundary/degenerate cases (`a′ = 0`, zero coordinates, equal weights)
9. Complex phase reduction (exact unitary equivalence)
10. Block-norm lemma stress test (200 random instances)

Sections 3–4 are symbolic proofs of universal statements. Sections 1–2,
5–10 are exact or floating-point checks of stated identities and are
regression evidence only — the paper's proof does not depend on them.

No external services, private APIs, or unpublished local files are required.
