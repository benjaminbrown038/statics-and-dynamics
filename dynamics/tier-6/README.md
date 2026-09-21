# Tier 6 — Particle dynamics, lifting loads, and work-energy

[Previous tier](../../dynamics/tier-5/README.md) · [Next tier](../../dynamics/tier-7/README.md)

## Learning goal

Turn a prescribed motion into force and power, and independently check total work.

## Model and assumptions

A mass is lifted vertically by a single massless, taut cable using the Tier 5 motion profile. Up is positive. Gravity is constant; guide friction, pulley ratios, cable elasticity, and motor losses are omitted. The cable can pull but cannot push, so cases requiring negative tension are rejected.

## Inputs and free-body diagram

Baseline: m = 10 kg, lift D = 0.5 m, T = 1 s, g = 9.81 m/s². Draw tension upward and weight downward on the moving mass.

Edit [cases/baseline.json](cases/baseline.json). See [units and signs](../../docs/units-and-signs.md)
and the [free-body diagram guide](../../docs/free-body-diagrams.md).

## Equations

Use the Tier 5 x(t), v(t), and a(t) with positive upward displacement. Newton's
second law gives cable tension F:

$$
F-mg=ma,
\qquad F(t)=m[g+a(t)].
$$

The tension-only model requires:

$$
F_{\min}=m(g-|a|_{\max})\geq0,
\qquad F_{\max}=m(g+|a|_{\max}).
$$

Power and work-energy provide a separate way to track the motion:

$$
\mathcal{P}(t)=F(t)v(t),
\qquad W_F(t)=\int_0^t Fv\,dt=mgx(t)+\frac{1}{2}mv(t)^2.
$$

Because both endpoint speeds are zero:

$$
W_F(T)=mgD.
$$

The program numerically integrates power and compares it with this exact work.
Peak power is sampled; tension extrema follow the exact acceleration extrema.
For cases reaching zero tension, the taut-cable condition is marginal.

## Symbols

| Symbol / name | Meaning | Unit |
|---|---|---|
| m, g | Lifted mass and gravity | kg; m/s² |
| F | Single-strand cable tension | N |
| x, v, a | Upward position, velocity, acceleration | m; m/s; m/s² |
| P calligraphic, WF | Mechanical power and work done by the cable | W; J |
| D, T | Lift and move duration | m; s |

## Run

From the repository root:

```bash
python3 dynamics/tier-6/main.py
```

Optional PNG plots:

```bash
python3 dynamics/tier-6/main.py --plot
```

The optional plotting dependency is installed with
`python3 -m pip install -r requirements-plot.txt`. Calculations need no packages.
Each run writes a Markdown report, an input/result JSON snapshot, and CSV tables
to `results/tier-6/`. Use `--case path/to/case.json` and
`--output results/my-study` for a separate study. Reusing an output folder
replaces matching files; PNGs are refreshed only by a run with `--plot`.

## Expected behavior

Static weight is 98.1 N, peak tension is 126.968 N, and minimum tension is 69.2325 N. Exact total lifting work is 49.05 J.

## Experiments

Predict before running, change one input at a time, and record the physical
reason in the [study template](../../templates/study-note.md).

1. Double mass: tension, power, and work double, while the prescribed motion stays the same.
2. Increase duration and observe tension approach static weight.
3. Try duration_s = 0.4 and explain the negative-tension rejection. A cable cannot enforce that deceleration profile.

## Project connections

Use cable tension as a load on the appropriate anchor. Pulley/drum support reactions need their own free-body diagram and may differ from one strand’s tension.
