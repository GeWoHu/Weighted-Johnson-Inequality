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

## Provenance of the manuscript
This repository's `paper/weighted-johnson.tex` is the final submission
manuscript of the underlying project (frozen 2026-10-31, sha256
16142b3d79057ce5969f1563b8263d1886348cda72e781810e6011709d7b010e) with
exactly one documented intentional difference: the closing paragraph of
Appendix A was reworded to point at this repository's `verification/`
directory instead of private project archives (a reproducibility-instruction
change). **No mathematical statement, proof step, or citation was changed.**
The mathematical content is identical to the frozen manuscript; the compiled
PDF in this repository is built from the source alongside it.

## Verification status
- Written proof: self-contained, elementary (linear algebra, induction,
  AM–GM); no step requires computer assistance.
- Machine checks: general-symbolic closure identity + independent
  from-the-definition battery, zero violations.
- Independent adversarial AI review: zero mathematical objections.
- Independent human review: pending (this repository is prepared for it).
