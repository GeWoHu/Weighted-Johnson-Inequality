#!/usr/bin/env python3
"""Complex-weight regression: dtype-preserving phase reduction and bound.

Ported during the 2026-11-09 consolidation from the companion repository
GeWoHu/Boolean-Lattice (v1.1 complex_weights.py), with two upgrades:

1. the two-sided phase identity of the manuscript (eq. ``eq:phase``),
   U_k(a) = D_r U_k(|a|) D_c  with  (D_r e)_S = e^{-i sum_{j in S} theta_j},
   (D_c e)_T = e^{+i sum_{j in T} theta_j},  is now checked entrywise --
   the one-sided form U_k(sigma.a) = D_{k-1} U_k(a) D_k that the companion
   remark originally claimed is FALSE for general phases (it holds only for
   signs, sigma_i^2 = 1);
2. hard exit codes: any failed check exits 1 (R2 CI discipline).

Convention at zero coordinates: theta_i := 0 when a_i = 0 (the diagonal
unitaries are then arbitrary on that coordinate; the identity below does
not depend on the choice).

Run: python3 complex_weights.py   (numpy only; deterministic seed)
Expected final line: ALL PASS
"""
import sys
import itertools

import numpy as np

rng = np.random.default_rng(11)


def U(m, k, a):
    cols = list(itertools.combinations(range(m), k))
    rows = list(itertools.combinations(range(m), k - 1))
    ci = {T: j for j, T in enumerate(cols)}
    M = np.zeros((len(rows), len(cols)), dtype=np.result_type(a, 1.0))
    for i, r in enumerate(rows):
        for x in range(m):
            if x not in r:
                M[i, ci[tuple(sorted(r + (x,)))]] = a[x]
    return M


def phase_unitaries(m, k, theta):
    cols = list(itertools.combinations(range(m), k))
    rows = list(itertools.combinations(range(m), k - 1))
    D_c = np.diag([np.exp(1j * sum(theta[j] for j in T)) for T in cols])
    D_r = np.diag([np.exp(-1j * sum(theta[j] for j in S)) for S in rows])
    return D_r, D_c


allok = True


def check(name, ok):
    global allok
    print(f"  {name}: {'ok' if ok else 'FAIL'}")
    allok = allok and ok


print("Complex weights (dtype-preserving; deterministic seed 11)")
for m, k in ((5, 2), (5, 3), (6, 3), (6, 4), (7, 3)):
    c = k * (m - k + 1) / m

    # 1. two-sided phase identity U_k(a) = D_r U_k(|a|) D_c
    ident_ok = True
    for _ in range(20):
        a = rng.normal(size=m) + 1j * rng.normal(size=m)
        theta = np.angle(a)  # angle(0) = 0 matches the stated convention
        D_r, D_c = phase_unitaries(m, k, theta)
        lhs = U(m, k, a)
        rhs = D_r @ U(m, k, np.abs(a)) @ D_c
        ident_ok = ident_ok and np.max(np.abs(lhs - rhs)) < 1e-12
    check(f"phase identity (m,k)=({m},{k})", ident_ok)

    # 2. bound over Gaussian complex draws
    worst = 0.0
    for _ in range(300):
        z = rng.normal(size=m) + 1j * rng.normal(size=m)
        r = np.linalg.svd(U(m, k, z), compute_uv=False)[0] ** 2 / (
            c * np.vdot(z, z).real
        )
        worst = max(worst, r)
    check(f"bound worst-ratio <= 1 (m,k)=({m},{k}): {worst:.10f}", worst <= 1 + 1e-9)

    # 3. flat phase vectors attain equality exactly
    z = np.exp(1j * rng.uniform(0, 2 * np.pi, m))
    flat = np.linalg.svd(U(m, k, z), compute_uv=False)[0] ** 2 / (c * m)
    check(f"flat-phase equality (m,k)=({m},{k}): {flat:.10f}", abs(flat - 1) < 1e-9)

print("ALL PASS" if allok else "FAIL")
sys.exit(0 if allok else 1)
