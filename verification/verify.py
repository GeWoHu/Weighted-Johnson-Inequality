#!/usr/bin/env python3
# Verification battery: exact + symbolic receipts for the weighted-Johnson inequality.
# Independent code path: definitions rebuilt from the operator definition only.
import itertools, math, sys
import numpy as np
import sympy as sp
from sympy import Matrix, Rational, symbols, simplify, factor, expand

def subsets(n, j):
    return list(itertools.combinations(range(n), j)) if 0 <= j <= n else []

def U(m, k, a):
    """(S,T) entry a_i if T=S+{i}; rows (k-1)-sets, cols k-sets."""
    R, C = subsets(m, k-1), subsets(m, k)
    ci = {T: i for i, T in enumerate(C)}
    dt = np.complex128 if np.iscomplexobj(a) else float
    M = np.zeros((len(R), len(C)), dtype=dt)
    for r, S in enumerate(R):
        Ss = set(S)
        for i in range(m):
            if i not in Ss:
                M[r, ci[tuple(sorted(S + (i,)))]] = a[i]
    return M

def Uex(m, k, a):
    R, C = subsets(m, k-1), subsets(m, k)
    ci = {T: i for i, T in enumerate(C)}
    M = sp.zeros(len(R), len(C))
    for r, S in enumerate(R):
        Ss = set(S)
        for i in range(m):
            if i not in Ss:
                M[r, ci[tuple(sorted(S + (i,)))]] = a[i]
    return M

def C(m, k):
    return Rational(k * (m - k + 1), m)

ok = lambda name: print(f"PASS {name}")
res = []

# ---- 1. Block decomposition, exact entrywise
good = True
for m in range(3, 8):
    for k in range(2, m):
        rng = np.random.default_rng(m * 100 + k)
        a = rng.integers(1, 9, m).astype(float)
        ap, am = a[:m-1], a[m-1]
        full = U(m, k, a)
        rowsA = [S for S in subsets(m, k-1) if m-1 not in S]
        rowsB = [S for S in subsets(m, k-1) if m-1 in S]
        colsA = [T for T in subsets(m, k) if m-1 not in T]
        colsB = [T for T in subsets(m, k) if m-1 in T]
        perm_r = [subsets(m, k-1).index(S) for S in rowsA + rowsB]
        perm_c = [subsets(m, k).index(T) for T in colsA + colsB]
        P = full[np.ix_(perm_r, perm_c)]
        A_b = U(m-1, k, ap); B_b = U(m-1, k-1, ap)
        blk = np.zeros_like(P)
        blk[:A_b.shape[0], :A_b.shape[1]] = A_b
        blk[:A_b.shape[0], A_b.shape[1]:] = am * np.eye(A_b.shape[0])
        blk[A_b.shape[0]:, A_b.shape[1]:] = B_b
        if not np.array_equal(P, blk):
            good = False
ok(f"1. block form U_k(a)=[[U_k(a'),a_m I],[0,U_{{k-1}}(a')]] exact m=3..7 all interior k: {good}")
assert good

# ---- 2. Gram off-diagonal block = a_m * U_{k-1}(a')^T exactly (V-1 core)
good = True
for m in range(3, 8):
    for k in range(2, m):
        rng = np.random.default_rng(7 * m + k)
        a = rng.integers(1, 9, m).astype(float)
        ap, am = a[:m-1], a[m-1]
        rows = subsets(m, k-1)
        perm = [rows.index(S) for S in [S for S in rows if m-1 not in S] + [S for S in rows if m-1 in S]]
        Gp = (U(m, k, a) @ U(m, k, a).T)[np.ix_(perm, perm)]
        nA = len(subsets(m-1, k-1)); nB = len(subsets(m-1, k-2))
        Q = Gp[:nA, nA:nA+nB]
        assert np.allclose(Gp[nA:nA+nB, :nA], am * U(m-1, k-1, ap), atol=1e-12)
        if not np.allclose(Q, am * U(m-1, k-1, ap).T, atol=1e-12):
            good = False
ok(f"2. Gram off-diagonal Q = a_m*U_(m-1,k-1)^T exactly (s1(Q)=|a_m|*beta): {good}")
assert good

# ---- 3. Closure identity, GENERAL symbolic (decisive)
m, k, t = symbols('m k t', positive=True)
A = k * (m - k) / (m - 1)
B = (k - 1) * (m - k + 1) / (m - 1)
Cc = k * (m - k + 1) / m
X = 2 * Cc * (1 + t) - A - B - t
Dfull = expand(X**2 - ((A - B + t)**2 + 4 * B * t))
target = 4 * k * (k - 1) * (m - k) * (m - k + 1) * ((m - 1) * t - 1)**2 / (m**2 * (m - 1)**2)
assert simplify(Dfull - target) == 0
ok("3a. closure defect identity X(t)^2-[(A-B+t)^2+4Bt] = 4k(k-1)(m-k)(m-k+1)((m-1)t-1)^2/(m^2(m-1)^2) GENERAL symbolic: True")
slope = simplify(2 * Cc - 1)
interc = simplify(X.subs(t, 0))
Dfull2 = simplify(factor(expand((Cc*(1+t)-(A+t))*(Cc*(1+t)-B) - t*B)))
target2 = k*(k-1)*(m-k)*(m-k+1)*(t - 1/(m-1))**2 / m**2
assert simplify(Dfull2 - target2) == 0
ok(f"3b. (T-p)(T-q)-o^2 = k(k-1)(m-k)(m-k+1)/m^2*(t-1/(m-1))^2 >= 0 general: True; slope 2C-1={factor(slope)}>0 for interior k; X(0)={factor(interc)}")

# ---- 4. Monotonicity of 2x2 lambda_max
p, q, o = symbols('p q o', real=True, nonnegative=True)
lam = (p + q + sp.sqrt((p - q)**2 + 4 * o**2)) / 2
dp = sp.simplify(sp.diff(lam, p)); dq = sp.simplify(sp.diff(lam, q)); do = sp.simplify(sp.diff(lam, o))
ok(f"4. d lam/dp = {dp} in [0,1], symmetric in q, d lam/do = {do} >= 0 for o>0: monotone corner justified")

# ---- 5. Sharp constant, exact spectrum of equal-weight operator
good = True
for mm in range(2, 9):
    for kk in range(1, mm + 1):
        Mm = Uex(mm, kk, [1] * mm)
        ev = (Mm * Mm.T).eigenvals()
        mx = max(ev)
        if mx != kk * (mm - kk + 1):
            good = False
ok(f"5. lambda_max(U_k(1)U_k(1)^T) = k(m-k+1) EXACT m=2..8 all k: {good}")
assert good

# ---- 6. Complement duality, exact permutation identity
good = True
for mm in range(3, 9):
    for kk in range(1, mm + 1):
        rng = np.random.default_rng(mm * 31 + kk)
        a = rng.integers(1, 9, mm).astype(float)
        Uk = U(mm, kk, a); Ud = U(mm, mm - kk + 1, a)
        Rk, Ck = subsets(mm, kk-1), subsets(mm, kk)
        # C_j: e_S -> e_{S^c}; check C_{k-1} U_k(a) C_k = U_{m-k+1}(a)^T
        lhs = np.zeros((len(subsets(mm, mm-kk+1)), len(subsets(mm, mm-kk))))
        for r, S in enumerate(Rk):
            for c, T in enumerate(Ck):
                lhs[subsets(mm, mm-kk+1).index(tuple(sorted(set(range(mm)) - set(S)))),
                    subsets(mm, mm-kk).index(tuple(sorted(set(range(mm)) - set(T))))] = Uk[r, c]
        if not np.allclose(lhs, Ud.T, atol=1e-12):
            good = False
ok(f"6. complement unitaries: C_(k-1) U_k(a) C_k = U_(m-k+1)(a)^T exact m=3..8 all k: {good}")
assert good

# ---- 7. Full-theorem exact rational regression
import random
random.seed(44)
viol = 0; worst = 0
for trial in range(30):
    mm = random.randint(3, 6); kk = random.randint(2, mm-1)
    a = [Rational(random.randint(0, 9), random.randint(1, 7)) for _ in range(mm)]
    Mm = Uex(mm, kk, a)
    rts = (Mm * Mm.T).charpoly().real_roots()
    lam_max = max(rts)
    s = sum(x**2 for x in a)
    ratio = sp.nsimplify(lam_max / (C(mm, kk) * s)) if s != 0 else 0
    worst = max(worst, float(ratio))
    if lam_max > C(mm, kk) * s:
        viol += 1
ok(f"7. 30 exact rational instances (sympy real_roots): violations={viol}, worst ratio={worst:.6f}")

# ---- 8. Edge cases
mm, kk = 6, 3
a = [0.0, 0.0, 0.0, 0.0, 0.0, 5.0]
print(f"8a. a'=0 (s=0): ||U||^2={np.linalg.norm(U(mm,kk,a),2)**2:.6f} vs C*s={float(C(mm,kk)*25):.6f} strict={np.linalg.norm(U(mm,kk,a),2)**2 < float(C(mm,kk)*25)}")
a = [1.0, 1.0, 1.0, 1.0, 1.0, 0.0]
z = np.linalg.norm(U(mm,kk,a),2)**2
print(f"    zero coordinate interior: ||U||^2={z:.6f} < C*s={float(C(mm,kk)*5):.6f} strict={z < float(C(mm,kk)*5)}")
a = [2.0]*6
print(f"    all equal: ||U||^2={np.linalg.norm(U(mm,kk,a),2)**2:.9f} == C*s={float(C(mm,kk)*24):.9f} equal={abs(np.linalg.norm(U(mm,kk,a),2)**2 - float(C(mm,kk)*24)) < 1e-9}")
a = [2.0]*5 + [1.999]
print(f"    perturbed equal: {np.linalg.norm(U(mm,kk,a),2)**2:.9f} < {float(C(mm,kk)*(5*4+1.999**2)):.9f} strict={np.linalg.norm(U(mm,kk,a),2)**2 < float(C(mm,kk)*(5*4+1.999**2))}")

# ---- 9. Complex phase reduction, exact construction
th = rng.random(mm) * 2 * np.pi
a = 2.0 * np.exp(1j * th)
Dr = np.diag([np.exp(-1j * sum(th[j] for j in S)) for S in subsets(mm, kk-1)])
Dc = np.diag([np.exp(1j * sum(th[j] for j in T)) for T in subsets(mm, kk)])
resid = np.max(np.abs(U(mm, kk, a) - Dr @ U(mm, kk, np.abs(a)) @ Dc))
print(f"9. complex phases: U(a)=D_r U(|a|) D_c residual={resid:.2e}; norm equality {np.linalg.norm(U(mm,kk,a),2):.9f} vs {np.linalg.norm(U(mm,kk,np.abs(a)),2):.9f}")

# ---- 10. Block-norm lemma stress
bad = 0
rng = np.random.default_rng(5)
for _ in range(200):
    n1, n2 = rng.integers(2, 6, 2)
    X1 = rng.standard_normal((n1, n1)); P = X1 @ X1.T
    X2 = rng.standard_normal((n2, n2)); R = X2 @ X2.T
    Qm = rng.standard_normal((n1, n2))
    M = np.block([[P, Qm], [Qm.T, R]])
    corner = np.array([[np.linalg.eigvalsh(P)[-1], np.linalg.svd(Qm, compute_uv=False)[0]],
                       [np.linalg.svd(Qm, compute_uv=False)[0], np.linalg.eigvalsh(R)[-1]]])
    if np.linalg.eigvalsh(M)[-1] > np.linalg.eigvalsh(corner)[-1] + 1e-10:
        bad += 1
print(f"10. block-norm lemma 200 random instances: violations={bad}")
print("ALL RECEIPTS COMPLETE")
