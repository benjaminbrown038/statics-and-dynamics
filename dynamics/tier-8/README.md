# Tier 8 — Impulse, momentum, and stopping loads

[Previous tier](../../dynamics/tier-7/README.md) · [Next tier](../../dynamics/tier-9/README.md)

## Learning goal

Distinguish peak stopping force, average force, impulse, and energy removal.

## Model and assumptions

A mass moves horizontally at speed v0 and stops over prescribed time T under a half-sine force pulse. Initial velocity is positive. Normal force balances gravity, and no other horizontal force acts. The pulse is an assumed load history; contact stiffness, restitution, and rebound are not simulated.

## Inputs and free-body diagram

Baseline: m = 20 kg, v0 = 2 m/s, T = 0.1 s. Draw the negative stopping force on the mass and the equal positive reaction on the stop as forces on separate bodies.

Edit [cases/baseline.json](cases/baseline.json). See [units and signs](../../docs/units-and-signs.md)
and the [free-body diagram guide](../../docs/free-body-diagrams.md).

## Equations

Impulse changes momentum:

$$
\int_0^T F(t)\,dt=m(v_f-v_0)=-mv_0.
$$

For the prescribed pulse:

$$
F(t)=-F_{\mathrm{pk}}\sin\left(\frac{\pi t}{T}\right),
\qquad F_{\mathrm{pk}}=\frac{\pi mv_0}{2T},
\qquad F_{\mathrm{avg,mag}}=\frac{mv_0}{T}.
$$

Integrating acceleration gives exact velocity and position:

$$
v(t)=\frac{v_0}{2}\left[1+\cos\left(\frac{\pi t}{T}\right)\right],
$$

$$
x(t)=\frac{v_0}{2}\left[t+\frac{T}{\pi}\sin\left(\frac{\pi t}{T}\right)\right],
\qquad x(T)=\frac{v_0T}{2}.
$$

Work equals the change in kinetic energy:

$$
\int_0^{x(T)}F\,dx=-\frac{1}{2}mv_0^2.
$$

The force applied to the stop is -F(t). Numerical trapezoidal integrations of
force over time and displacement provide independent checks on impulse and work.
Shorter stopping duration increases peak force without changing the initial
energy that must be removed.

## Symbols

| Symbol / name | Meaning | Unit |
|---|---|---|
| m, v0, vf | Mass, initial speed, final speed | kg; m/s; m/s |
| T, t | Stopping duration and elapsed time | s |
| F, Fpk, Favg | Signed force on mass, peak and average magnitudes | N |
| x, v | Displacement and velocity | m; m/s |
| Impulse, work | Force-time integral, force-displacement integral | N s; J |

## Run

From the repository root:

```bash
python3 dynamics/tier-8/main.py
```

Optional PNG plots:

```bash
python3 dynamics/tier-8/main.py --plot
```

The optional plotting dependency is installed with
`python3 -m pip install -r requirements-plot.txt`. Calculations need no packages.
Each run writes a Markdown report, an input/result JSON snapshot, and CSV tables
to `results/tier-8/`. Use `--case path/to/case.json` and
`--output results/my-study` for a separate study. Reusing an output folder
replaces matching files; PNGs are refreshed only by a run with `--plot`.

## Expected behavior

Peak force on the stop is 628.319 N, average force is 400 N, impulse on the mass is -40 N s, stop distance is 0.1 m, and removed kinetic energy is 40 J.

## Experiments

Predict before running, change one input at a time, and record the physical
reason in the [study template](../../templates/study-note.md).

1. Halve stopping time: peak force doubles, distance halves, and removed energy stays the same.
2. Double initial speed: impulse doubles and initial kinetic energy quadruples.
3. Explain why an impulse value alone cannot determine the peak force without a duration and shape.

## Project connections

The exported pulse is a candidate load history for a stop or bumper. A static stress calculation at peak force omits the support’s own dynamic response; use vibration or transient structural analysis when that response matters.
