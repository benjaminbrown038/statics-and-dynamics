# Verification record

All ten baseline examples ran successfully with Python 3.12.14, including runs
from inside each tier directory with site-package loading disabled. Core
calculations therefore do not require installed third-party packages.

The 29 automated checks cover:

- Force/moment equilibrium and exact supported-beam limits.
- Truss joint equilibrium and frame reaction moments.
- Static versus kinetic friction and direction of motion.
- Composite mass inertia checked against rectangle subtraction.
- Motion derivatives, endpoint conditions, and duration scaling.
- Cable tension, work-energy, and impossible negative-tension cases.
- Arm mass properties, quasi-static limits, continuous geometric singularities,
  dynamic force scaling, and action/reaction signs at the stationary mounts.
- Impulse, stopping work, and peak/average load distinctions.
- Free-vibration analytical agreement, energy, and fourth-order trajectory convergence.
- Consistent lesson headings, equation formatting, main-README equation coverage,
  and relative document links.

Run from the repository root:

```bash
python3 -m unittest discover -s tests -v
python3 run_all.py
```

The source parses with Python 3.9 grammar, which is the intended minimum. A
separate Python 3.9 interpreter was not used during preparation. Optional plots
were generated with Matplotlib 3.10.8; diagrams and the included plot gallery
were visually inspected.

The checks verify these idealized teaching models. They do not validate a
particular machine, material dataset, or real contact/load history. Numerical
force peaks in Tier 7 and peak power in Tier 6 are sampled values; time-step
and sampling choices are explicitly documented in the lessons.
