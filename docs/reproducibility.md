# Reproducibility

## Compile the paper
```
cd paper
tectonic weighted-johnson.tex        # or: pdflatex weighted-johnson.tex ×2
```
Standard `article` class; packages used: amsmath, amsthm, amssymb, geometry,
natbib, hyperref — all in TeX Live / MiKTeX / tectonic bundles. No custom
style files.

## Run the checks
```
cd verification
pip install -r requirements.txt      # numpy==2.4.3, sympy==1.14.0
python3 verify.py                    # ends with "ALL RECEIPTS COMPLETE"
```
Tested with Python 3.12+ on Linux. The symbolic checks (sections 3–4) are
identities in general symbols; the remaining sections are exact or
floating-point regression evidence (see `verification/README.md`).

Arithmetic application (Section 6 of the paper):

```
cd verification
python3 verify_arithmetic.py        # ends with "ALL PASS"
```

Rebuilds the squarefree compression from the matrix definition alone and
checks the compression identity, the cross-level block-diagonality of
`S*S`, the certified inequality `||S||^2 <= k_max*sum (log p)^2/(p-1)`,
and the adjoint lower-bound identity. numpy only. Regression evidence;
the proofs do not depend on it.

## Provenance of the manuscript
This repository's `paper/weighted-johnson.tex` is the living development line
of the project. It descends from the manuscript frozen 2026-10-31 (git tag
`pre-public-20261101`, source sha256 `68a61ff2...`), but it is NOT identical
to it: the R2 revision of 2026-11-09 (external-review response) restricted the
block and closure lemmas to the interior range $1<k<m$, split the ambient
Boolean levels from the admissible subspaces in Section 6, corrected the
inclusion-matrix rank attribution (Gottlieb 1966; Wilson 1990 diagonal form),
downgraded the "exact singular value" phrasing to an optimal uniform bound,
added the zeon/Lefschetz/log-concavity literature neighborhood, and moved the
AI-assistance disclosure from the author line to the Acknowledgments. An
earlier version of this document claimed identity with the frozen manuscript
(hash `16142b3d...`) except for one reworded paragraph; that claim was
incorrect and this paragraph supersedes it. The current source hash is recorded
in `MANIFEST.sha256`; the compiled PDF is built from the source alongside it.

## Verification status
- Written proof: self-contained, elementary (linear algebra, induction,
  AM–GM); no step requires computer assistance.
- Machine checks: general-symbolic closure identity + independent
  from-the-definition battery, zero violations; complex-weight battery
  (`verification/complex_weights.py`, added with the 2026-11-09
  consolidation from the archived Boolean-Lattice companion) checks the
  two-sided phase identity, the bound over random complex draws, and
  exact flat-phase equality, all dtype-preserving.
- The R3 consolidation moved the squarefree arithmetic application from
  Section 6 to Appendix A.
- Independent adversarial AI review: zero mathematical objections.
- Independent human review: pending (this repository is prepared for it).
