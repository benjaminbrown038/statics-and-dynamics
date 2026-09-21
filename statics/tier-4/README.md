# Tier 4 — Centroids and mass moments of inertia

[Previous tier](../../statics/tier-3/README.md) · [Next tier](../../dynamics/tier-5/README.md)

## Learning goal

Locate a composite plate’s center of mass and distinguish mass inertia from beam section properties.

## Model and assumptions

A uniform L-shaped plate has horizontal outer length L, vertical outer length H, equal leg width w, thickness t, and density rho. Its origin is the outer lower-left corner. Divide it into a w by H rectangle and a (L-w) by w rectangle so the shared corner is not double counted. The inertia axis z is perpendicular to the plate.

## Inputs and free-body diagram

Baseline: L = 160 mm, H = 120 mm, w = 20 mm, t = 6 mm, density = 2700 kg/m³. Inputs use meters. Mark the centroid of each rectangle before combining them.

Edit [cases/baseline.json](cases/baseline.json). See [units and signs](../../docs/units-and-signs.md)
and the [free-body diagram guide](../../docs/free-body-diagrams.md).

## Equations

Compute area, mass, and centroid from non-overlapping pieces:

$$
A_i=b_i h_i,
\qquad m_i=\rho t A_i,
\qquad m=\sum_i m_i,
$$

$$
x_G=\frac{\sum_i m_i x_i}{m},
\qquad y_G=\frac{\sum_i m_i y_i}{m}.
$$

Each rectangle's centroidal mass moment and the composite parallel-axis sum are:

$$
I_{z,i}=\frac{m_i(b_i^2+h_i^2)}{12},
\qquad I_{G,z}=\sum_i\left[I_{z,i}+m_i\big((x_i-x_G)^2+(y_i-y_G)^2\big)\right].
$$

$$
I_{O,z}=I_{G,z}+m(x_G^2+y_G^2),
\qquad I_{Q,z}=I_{G,z}+md^2.
$$

For comparison, centroidal area second moments are:

$$
I_{A,x}=\sum_i\left[\frac{b_i h_i^3}{12}+A_i(y_i-y_G)^2\right],
\qquad I_{A,y}=\sum_i\left[\frac{h_i b_i^3}{12}+A_i(x_i-x_G)^2\right].
$$

For this uniform-thickness, uniform-density plate:

$$
I_{G,z}=\rho t(I_{A,x}+I_{A,y}).
$$

Mass moments have units kg m² and enter angular dynamics. Area moments have
units m⁴ and enter beam bending. Matching symbols in textbooks do not make
these interchangeable quantities.

## Symbols

| Symbol / name | Meaning | Unit |
|---|---|---|
| L, H, w, t, bi, hi | Plate and rectangular-piece dimensions | m |
| rho, mi, m | Density, piece mass, total mass | kg/m³; kg; kg |
| xG, yG, d | Centroid coordinates and parallel-axis offset | m |
| IGz, IOz, IQz | Mass moment about specified z axis | kg m² |
| IAx, IAy | Centroidal area second moments | m⁴ |

## Run

From the repository root:

```bash
python3 statics/tier-4/main.py
```

Optional PNG plots:

```bash
python3 statics/tier-4/main.py --plot
```

The optional plotting dependency is installed with
`python3 -m pip install -r requirements-plot.txt`. Calculations need no packages.
Each run writes a Markdown report, an input/result JSON snapshot, and CSV tables
to `results/tier-4/`. Use `--case path/to/case.json` and
`--output results/my-study` for a separate study. Reusing an output folder
replaces matching files; PNGs are refreshed only by a run with `--plot`.

## Expected behavior

Mass is 0.08424 kg and centroid is (53.0769, 33.0769) mm. Centroidal z mass inertia is 0.000309877 kg m²; origin z inertia is 0.00063936 kg m².

## Experiments

Predict before running, change one input at a time, and record the physical
reason in the [study template](../../templates/study-note.md).

1. Double density; mass and mass moments double while the centroid and area moments stay unchanged.
2. Double thickness; the z mass moments double.
3. Move the rotation axis away from the centroid and explain the quadratic increase in inertia.

## Project connections

Use mass inertia to calculate acceleration torque. Use area moments in your mechanics-of-materials beam models.
