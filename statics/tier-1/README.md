# Tier 1 — Equilibrium, support reactions, and internal loads

[Previous tier](../../fundamentals/tier-0/README.md) · [Next tier](../../statics/tier-2/README.md)

## Learning goal

Calculate reactions and internal shear/bending for a beam carrying point and distributed loads.

## Model and assumptions

A pin at A = (0, 0) and roller at B = (L, 0) support a beam. A point load P acts downward at x = a, and a uniform distributed load q acts downward over the entire span. Horizontal reaction is zero. Self-weight is included only if represented in q.

## Inputs and free-body diagram

Baseline: L = 1 m, P = 1000 N, a = 0.4 m, q = 200 N/m. Draw RA and RB upward, P downward, and the distributed arrows along the span. Positive internal moment is sagging.

Edit [cases/baseline.json](cases/baseline.json). See [units and signs](../../docs/units-and-signs.md)
and the [free-body diagram guide](../../docs/free-body-diagrams.md).

## Equations

Static equilibrium and the distributed-load resultant give:

$$
\sum\mathbf{F}=\mathbf{0},
\qquad \sum\mathbf{M}_O=\mathbf{0},
\qquad W=qL,
\qquad x_W=\frac{L}{2}.
$$

$$
R_B=\frac{Pa+qL^2/2}{L},
\qquad R_A=P+qL-R_B.
$$

After cutting the beam at x:

$$
V(x)=\begin{cases}
R_A-qx,&0<x<a,\\
R_A-qx-P,&a<x<L,
\end{cases}
$$

$$
M(x)=R_Ax-\frac{qx^2}{2}-P\max(0,x-a),
\qquad \frac{dV}{dx}=-q,
\qquad \frac{dM}{dx}=V.
$$

The point load produces a shear jump of -P. Moment stays continuous. Check the
endpoints, the load position, and valid zero-shear points to locate maximum
moment. Replacing q with its resultant works for whole-beam equilibrium but
does not preserve the internal shear/moment distribution.

## Symbols

| Symbol / name | Meaning | Unit |
|---|---|---|
| P, RA, RB, W | Point load, reactions, distributed-load resultant | N |
| q | Downward load per unit length | N/m |
| L, a, x | Span, point-load location, section position | m |
| V, M | Internal shear and bending moment | N; N m |

## Run

From the repository root:

```bash
python3 statics/tier-1/main.py
```

Optional PNG plots:

```bash
python3 statics/tier-1/main.py --plot
```

The optional plotting dependency is installed with
`python3 -m pip install -r requirements-plot.txt`. Calculations need no packages.
Each run writes a Markdown report, an input/result JSON snapshot, and CSV tables
to `results/tier-1/`. Use `--case path/to/case.json` and
`--output results/my-study` for a separate study. Reusing an output folder
replaces matching files; PNGs are refreshed only by a run with `--plot`.

## Expected behavior

RA = 700 N, RB = 500 N, and maximum moment is 264 N m at x = 0.4 m. Force and moment residuals are zero.

## Experiments

Predict before running, change one input at a time, and record the physical
reason in the [study template](../../templates/study-note.md).

1. Set q to zero to recover the point-load case from the mechanics-of-materials fundamentals.
2. Set P to zero: the reactions become qL/2 and maximum moment becomes qL²/8 at midspan.
3. Double all loads and predict every reaction and internal-force change.

## Project connections

Feed M(x) and V(x) into beam stress calculations. This tier determines internal loads; it does not calculate stress or deformation.
