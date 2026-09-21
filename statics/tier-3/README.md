# Tier 3 — Friction and the start of motion

[Previous tier](../../statics/tier-2/README.md) · [Next tier](../../statics/tier-4/README.md)

## Learning goal

Determine whether a block sticks, then calculate the motion when it begins sliding.

## Model and assumptions

A block starts from rest on a long rigid incline. An optional constant force acts parallel to the plane. Downslope is positive. The normal load is supplied by gravity; Coulomb coefficients are constant, with kinetic coefficient no greater than static coefficient. Rolling, tipping, and contact loss are excluded.

## Inputs and free-body diagram

Baseline: m = 10 kg, incline = 20 degrees, static coefficient 0.30, kinetic coefficient 0.25, no extra applied force, g = 9.81 m/s², duration = 2 s. Draw weight vertically, normal force perpendicular to the plane, and friction along the plane.

Edit [cases/baseline.json](cases/baseline.json). See [units and signs](../../docs/units-and-signs.md)
and the [free-body diagram guide](../../docs/free-body-diagrams.md).

## Equations

Normal force and tangential demand before friction are:

$$
N=mg\cos\theta,
\qquad D=mg\sin\theta+F_\parallel.
$$

Static friction adjusts within its bound:

$$
|D|\leq\mu_sN
\quad\Longrightarrow\quad f=-D,\qquad a=0.
$$

If the static bound is exceeded, the initially stationary block begins moving
in the direction of D. For this constant-load case:

$$
f=-\operatorname{sgn}(D)\mu_kN,
\qquad a=\frac{D+f}{m},
\qquad v(t)=at,
\qquad s(t)=\frac{1}{2}at^2.
$$

With zero additional force, the incipient-slip condition is:

$$
\tan\theta=\mu_s.
$$

Static friction is not automatically equal to its maximum. The kinetic formula
here assumes motion begins from rest under unchanged loads, so there is no
velocity reversal requiring a new friction state.

## Symbols

| Symbol / name | Meaning | Unit |
|---|---|---|
| m, g | Mass and gravitational acceleration | kg; m/s² |
| theta | Incline angle | rad internally |
| N, D, F parallel, f | Normal force, demand, applied force, signed friction | N |
| mu s, mu k | Static and kinetic friction coefficients | 1 |
| a, v, s, t | Acceleration, velocity, displacement, time | m/s²; m/s; m; s |

## Run

From the repository root:

```bash
python3 statics/tier-3/main.py
```

Optional PNG plots:

```bash
python3 statics/tier-3/main.py --plot
```

The optional plotting dependency is installed with
`python3 -m pip install -r requirements-plot.txt`. Calculations need no packages.
Each run writes a Markdown report, an input/result JSON snapshot, and CSV tables
to `results/tier-3/`. Use `--case path/to/case.json` and
`--output results/my-study` for a separate study. Reusing an output folder
replaces matching files; PNGs are refreshed only by a run with `--plot`.

## Expected behavior

The block slides: normal force is 92.1838 N, static limit 27.6552 N, and acceleration 1.05062 m/s² downslope. After 2 s it has moved 2.10124 m.

## Experiments

Predict before running, change one input at a time, and record the physical
reason in the [study template](../../templates/study-note.md).

1. Increase mu_static to 0.5 with other inputs unchanged; the block should stick.
2. With mu_static = 0.5, compare actual friction with its maximum allowable value.
3. Apply a sufficiently large negative tangential force and verify uphill motion with downhill friction.

## Project connections

Useful for fixtures, sliding guides, and load retention. The transition from sticking equilibrium to acceleration connects statics to dynamics.
