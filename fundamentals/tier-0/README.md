# Tier 0 — Forces, vectors, moments, and free-body diagrams

[Overview](../../README.md) · [Next tier](../../statics/tier-1/README.md)

## Learning goal

Replace a planar load system with an equivalent resultant and moment, and identify the body being analyzed.

## Model and assumptions

Two forces act at specified points on a rigid body. A separate free couple may also act. Coordinates are x right and y up; positive moments are counterclockwise. This runnable example is planar. The vector equations also express the 3D generalization.

## Inputs and free-body diagram

Baseline: F1 = (300, -1000) N at (0.12, 0) m; F2 = (0, 200) N at (0, 0.1) m; applied couple = +20 N m. Sketch the isolated body, both application points, the origin, and all three loads.

Edit [cases/baseline.json](cases/baseline.json). See [units and signs](../../docs/units-and-signs.md)
and the [free-body diagram guide](../../docs/free-body-diagrams.md).

## Equations

A force's magnitude and direction follow from its components:

$$
\mathbf{F}=F_x\mathbf{i}+F_y\mathbf{j},
\qquad |\mathbf{F}|=\sqrt{F_x^2+F_y^2},
\qquad \theta=\operatorname{atan2}(F_y,F_x).
$$

Add vectors and moments, not their magnitudes:

$$
\mathbf{R}=\sum_i\mathbf{F}_i,
\qquad \mathbf{M}_O=\sum_i\mathbf{r}_{Oi}\times\mathbf{F}_i+\sum_j\mathbf{C}_j.
$$

In the planar example:

$$
M_O=\sum_i(x_iF_{iy}-y_iF_{ix})+C.
$$

Moving the reference from O to Q requires the reference-shift term:

$$
\mathbf{M}_Q=\mathbf{M}_O-\mathbf{r}_{OQ}\times\mathbf{R}.
$$

The output sweep sets Q = (xQ, 0). A couple stays the same about every point;
the moment of a nonzero resultant generally changes. Zero resultant with nonzero
moment describes a pure couple, so the resultant-force angle is then undefined.

## Symbols

| Symbol / name | Meaning | Unit |
|---|---|---|
| F, R | Applied force and resultant | N |
| r, x, y | Position relative to the reference | m |
| M, C | Force moment and free couple | N m |
| theta | Direction measured counterclockwise from +x | rad internally; degrees in output |

## Run

From the repository root:

```bash
python3 fundamentals/tier-0/main.py
```

Optional PNG plots:

```bash
python3 fundamentals/tier-0/main.py --plot
```

The optional plotting dependency is installed with
`python3 -m pip install -r requirements-plot.txt`. Calculations need no packages.
Each run writes a Markdown report, an input/result JSON snapshot, and CSV tables
to `results/tier-0/`. Use `--case path/to/case.json` and
`--output results/my-study` for a separate study. Reusing an output folder
replaces matching files; PNGs are refreshed only by a run with `--plot`.

## Expected behavior

The resultant is (300, -800) N, its magnitude is 854.400 N, and the moment about the origin is -100 N m.

## Experiments

Predict before running, change one input at a time, and record the physical
reason in the [study template](../../templates/study-note.md).

1. Set both force components to zero and retain the couple. Its moment should be independent of reference point.
2. Create equal-and-opposite forces at different points. Explain why the net force can be zero while moment is nonzero.
3. Move a force along its own line of action and verify that its moment is unchanged.

## Project connections

Use the equivalent force and moment to describe loads on a bracket or bolt group. A free-body diagram must identify which body each force acts on.
