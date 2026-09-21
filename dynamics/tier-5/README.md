# Tier 5 — Position, velocity, and acceleration

[Previous tier](../../statics/tier-4/README.md) · [Next tier](../../dynamics/tier-6/README.md)

## Learning goal

Describe a smooth motion first, before asking which forces create it.

## Model and assumptions

A point moves along a straight line by signed distance D in duration T. A quintic position profile starts and ends with zero velocity and acceleration. The motion is prescribed, so this tier does not solve an equation of motion.

## Inputs and free-body diagram

Baseline travel is 0.5 m in 1 s. Positive travel is along +x. Plot position, velocity, and acceleration separately because they have different units.

Edit [cases/baseline.json](cases/baseline.json). See [units and signs](../../docs/units-and-signs.md)
and the [free-body diagram guide](../../docs/free-body-diagrams.md).

## Equations

With normalized time s = t/T for 0 <= t <= T:

$$
q(s)=10s^3-15s^4+6s^5,
\qquad x(t)=x_0+Dq(s).
$$

Differentiate with respect to physical time:

$$
v(t)=\frac{D}{T}(30s^2-60s^3+30s^4),
$$

$$
a(t)=\frac{D}{T^2}(60s-180s^2+120s^3).
$$

The exact peak magnitudes are:

$$
v_{\max}=\frac{15|D|}{8T},
\qquad |a|_{\max}=\frac{10\sqrt{3}|D|}{3T^2}.
$$

Speed peaks at s = 1/2. Acceleration extrema occur at:

$$
s=\frac{3\pm\sqrt{3}}{6}.
$$

The code includes these times in its output sampling. The same dimensionless
profile will prescribe the arm's angular position in Tier 7. Zero endpoint
acceleration does not imply zero endpoint jerk.

## Symbols

| Symbol / name | Meaning | Unit |
|---|---|---|
| D, x, x0 | Signed travel, position, initial position | m |
| T, t, s | Duration, time, normalized time | s; s; 1 |
| q | Dimensionless motion profile | 1 |
| v, a | Velocity and acceleration | m/s; m/s² |

## Run

From the repository root:

```bash
python3 dynamics/tier-5/main.py
```

Optional PNG plots:

```bash
python3 dynamics/tier-5/main.py --plot
```

The optional plotting dependency is installed with
`python3 -m pip install -r requirements-plot.txt`. Calculations need no packages.
Each run writes a Markdown report, an input/result JSON snapshot, and CSV tables
to `results/tier-5/`. Use `--case path/to/case.json` and
`--output results/my-study` for a separate study. Reusing an output folder
replaces matching files; PNGs are refreshed only by a run with `--plot`.

## Expected behavior

Peak speed is 0.9375 m/s and peak acceleration magnitude is 2.88675 m/s². The motion ends at 0.5 m with zero velocity and acceleration.

## Experiments

Predict before running, change one input at a time, and record the physical
reason in the [study template](../../templates/study-note.md).

1. Halve duration and predict the twofold speed and fourfold acceleration increase.
2. Reverse travel_m to -0.5 and inspect the signs.
3. Check the endpoint values before adding this motion to a force model.

## Project connections

Prescribed motion establishes a machine cycle. Particle and rigid-body dynamics then determine its required force, torque, and power.
