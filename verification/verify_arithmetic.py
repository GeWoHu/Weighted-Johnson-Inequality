#!/usr/bin/env python3
"""Arithmetic-application regression (independent from-the-definition build).

Reconstructs, from the matrix definition alone:
  - T~ on ordinary l2({1..N}): T~[r,s] = Lambda(s/r)*sqrt(phi(r)/phi(s)) for r|s, s!=r
    (unitarily equivalent to T_N on l2({1..N}, phi) via D = mult. sqrt(phi)).
  - Squarefree compression S = P_sqf T~ P_sqf built DIRECTLY from the matrix,
    compared to the Boolean-incidence side sum_k P_{k-1} U_k(a) P_k,
    a_p = log p / sqrt(p-1), cutoff prod(S) <= N.
  - Cross-term check: S*S must be block-diagonal across input levels (S_k^* S_j = 0).
  - Certified norm check: ||S||^2 <= k_max * sum_{p<=N} (log p)^2/(p-1).
  - Lower-bound identity: ||T~^* e_1||^2 == sum_{2<=k<=N} Lambda(k)^2/phi(k),
    and T~ e_1 = 0 (operator lowers indices; the witness is the adjoint column).
Usage: python3 verify_arithmetic.py [N ...]
"""
import math
import sys
import numpy as np

def smallest_prime_factor(n):
    lp = list(range(n + 1))
    for i in range(2, int(n ** 0.5) + 1):
        if lp[i] == i:
            for j in range(i * i, n + 1, i):
                if lp[j] == j:
                    lp[j] = i
    return lp

def phi_fn(n):
    r, m, d = n, n, 2
    while d * d <= m:
        if m % d == 0:
            r -= r // d
            while m % d == 0:
                m //= d
        d += 1
    if m > 1:
        r -= r // m
    return r

def sqfree(n):
    m, d = n, 2
    while d * d <= m:
        if m % (d * d) == 0:
            return False
        if m % d == 0:
            while m % d == 0:
                m //= d
        d += 1
    return True

def omega(n):
    c, d, m = 0, 2, n
    while d * d <= m:
        if m % d == 0:
            c += 1
            while m % d == 0:
                m //= d
        d += 1
    if m > 1:
        c += 1
    return c

def run(N):
    lp = smallest_prime_factor(N)
    def lam(k):
        if k == 1:
            return 0.0
        p, m = lp[k], k
        while m % p == 0:
            m //= p
        return math.log(p) if m == 1 else 0.0
    primes = [p for p in range(2, N + 1) if lp[p] == p]
    phiN = [phi_fn(r) for r in range(1, N + 1)]
    # Direct T~ matrix
    T = np.zeros((N, N))
    for r in range(1, N + 1):
        for s in range(2 * r, N + 1, r):
            l = lam(s // r)
            if l:
                T[r - 1, s - 1] = l * math.sqrt(phiN[r - 1] / phiN[s - 1])
    sf = [r for r in range(1, N + 1) if sqfree(r)]
    si = {r: i for i, r in enumerate(sf)}
    S_direct = np.array([[T[r - 1, s - 1] for s in sf] for r in sf])
    # Boolean side: k_max via primorial; S_bool[r, r*p] = a_p when both squarefree
    kmax, prod = 0, 1
    for p in primes:
        if prod * p > N:
            break
        prod *= p
        kmax += 1
    a = {p: math.log(p) / math.sqrt(p - 1) for p in primes}
    S_bool = np.zeros((len(sf), len(sf)))
    for r in sf:
        for p in primes:
            s = r * p
            if s > N:
                break
            if sqfree(s):
                S_bool[si[r], si[s]] += a[p]
    maxdiff = float(np.max(np.abs(S_direct - S_bool)))
    # Cross-term check: S*S block-diagonal across input levels
    lev_in = [omega(s) for s in sf]
    SS = S_direct.T @ S_direct
    cross = 0.0
    for i in range(len(sf)):
        for j in range(len(sf)):
            if lev_in[i] != lev_in[j]:
                cross = max(cross, abs(SS[i, j]))
    normS = float(np.linalg.svd(S_direct, compute_uv=False)[0])
    sumap2 = sum(a[p] ** 2 for p in primes)
    bound = kmax * sumap2
    lb_sq = sum(lam(k) ** 2 / phiN[k - 1] for k in range(2, N + 1))
    Te1 = float(np.linalg.norm(T[:, 0]))
    Tstar_e1_sq = float(np.sum(T[0, :] ** 2))
    ok_identity = maxdiff < 1e-12
    ok_cross = cross < 1e-12
    ok_bound = normS ** 2 <= bound + 1e-9
    ok_lb = abs(Tstar_e1_sq - lb_sq) < 1e-9 and Te1 < 1e-15
    print(f"N={N:5d} kmax={kmax} ||S||={normS:.6f} ||S||^2={normS**2:.4f} "
          f"kmax*sum_a2={bound:.4f} hold={ok_bound} "
          f"identity_diff={maxdiff:.2e} cross_max={cross:.2e} "
          f"||T e1||={Te1:.1e} ||T*e1||^2={Tstar_e1_sq:.4f} sumL2/phi={lb_sq:.4f} "
          f"lb_ok={ok_lb} identity_ok={ok_identity} cross_ok={ok_cross}")
    return ok_identity and ok_cross and ok_bound and ok_lb

if __name__ == "__main__":
    Ns = [int(x) for x in sys.argv[1:]] or [30, 60, 120, 240, 480]
    allok = all(run(N) for N in Ns)
    print("ALL PASS" if allok else "FAIL")
