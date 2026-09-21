# Tier 9 — Free vibration and numerical verification

[Previous tier](../../dynamics/tier-8/README.md) · [Load transfer guide](../../docs/load-transfer.md)

## Learning goal

Solve an equation of motion numerically, compare with an exact response, and check energy.

## Model and assumptions

A single mass is attached to a linear spring and viscous damper on a fixed base. Displacement is measured from static equilibrium. There is no external forcing. The supported damping range is 0 <= zeta < 1 so an underdamped or undamped exact solution is available. Gravity preload is not included in the dynamic mount-load column.

## Inputs and free-body diagram

Baseline: m = 10 kg, k = 4000 N/m, damping ratio = 0.05, initial displacement = 10 mm, initial velocity = 0, duration = 2 s, requested time step = 0.002 s. The code uses fourth-order Runge-Kutta and adjusts step size to land exactly on the final time.

Edit [cases/baseline.json](cases/baseline.json). See [units and signs](../../docs/units-and-signs.md)
and the [free-body diagram guide](../../docs/free-body-diagrams.md).

## Equations

The free-vibration equation and its frequency definitions are:

$$
m\ddot x+c\dot x+kx=0,
\qquad \omega_n=\sqrt{\frac{k}{m}},
\qquad c=2\zeta\sqrt{km},
$$

$$
f_n=\frac{\omega_n}{2\pi},
\qquad \omega_d=\omega_n\sqrt{1-\zeta^2}.
$$

For initial position x0 and velocity v0:

$$
x(t)=e^{-\zeta\omega_nt}\left[x_0\cos(\omega_dt)+\frac{v_0+\zeta\omega_nx_0}{\omega_d}\sin(\omega_dt)\right].
$$

For numerical integration, write a first-order state equation:

$$
\mathbf{y}=\begin{bmatrix}x\\v\end{bmatrix},
\qquad \dot{\mathbf{y}}=\mathbf{f}(t,\mathbf{y})=
\begin{bmatrix}v\\-(cv+kx)/m\end{bmatrix}.
$$

The implemented RK4 update with step h is:

$$
\mathbf{k}_1=\mathbf{f}(t_n,\mathbf{y}_n),
\qquad \mathbf{k}_2=\mathbf{f}(t_n+h/2,\mathbf{y}_n+h\mathbf{k}_1/2),
$$

$$
\mathbf{k}_3=\mathbf{f}(t_n+h/2,\mathbf{y}_n+h\mathbf{k}_2/2),
\qquad \mathbf{k}_4=\mathbf{f}(t_n+h,\mathbf{y}_n+h\mathbf{k}_3),
$$

$$
\mathbf{y}_{n+1}=\mathbf{y}_n+\frac{h}{6}(\mathbf{k}_1+2\mathbf{k}_2+2\mathbf{k}_3+\mathbf{k}_4).
$$

Energy and the signed dynamic load applied to the base are:

$$
E(t)=\frac{1}{2}m\dot x^2+\frac{1}{2}kx^2,
\qquad \frac{dE}{dt}=-c\dot x^2,
\qquad F_{\mathrm{mount}}=kx+c\dot x.
$$

$$
E(T)+\int_0^T c\dot x^2\,dt-E(0)=0.
$$

The code compares displacement with the exact curve at every time step. Its
time-step screen omega_n h <= 0.2 is a chosen teaching accuracy limit, not a
universal stability theorem. The energy-loss integral uses a separate trapezoidal
rule, so its error need not converge at the same rate as the RK4 trajectory.

## Symbols

| Symbol / name | Meaning | Unit |
|---|---|---|
| m, k, c | Mass, spring stiffness, viscous damping coefficient | kg; N/m; N s/m |
| zeta | Damping ratio | 1 |
| omega n, omega d, fn | Natural and damped angular frequencies; natural frequency | rad/s; rad/s; Hz |
| x, v, h | Displacement from equilibrium, velocity, time step | m; m/s; s |
| E, Fmount | Mechanical energy and dynamic force on fixed base | J; N |

## Run

From the repository root:

```bash
python3 dynamics/tier-9/main.py
```

Optional PNG plots:

```bash
python3 dynamics/tier-9/main.py --plot
```

The optional plotting dependency is installed with
`python3 -m pip install -r requirements-plot.txt`. Calculations need no packages.
Each run writes a Markdown report, an input/result JSON snapshot, and CSV tables
to `results/tier-9/`. Use `--case path/to/case.json` and
`--output results/my-study` for a separate study. Reusing an output folder
replaces matching files; PNGs are refreshed only by a run with `--plot`.

## Expected behavior

Natural frequency is 20 rad/s (3.18310 Hz), damping coefficient is 20 N s/m, and initial energy is 0.2 J. The baseline maximum displacement error is about 1.57e-6 mm. The initial dynamic mount load is 40 N.

## Experiments

Predict before running, change one input at a time, and record the physical
reason in the [study template](../../templates/study-note.md).

1. Set damping_ratio to zero; energy should remain nearly constant and motion should persist.
2. Halve time_step_s and observe roughly fourth-order convergence of trajectory error before roundoff dominates.
3. Quadruple stiffness at unchanged mass: natural frequency doubles.
4. Reduce initial displacement by half with zero initial velocity; displacement and load halve while energy falls by four.

## Project connections

This introduces transient support loading and verification habits for your FEA work. A one-degree-of-freedom spring model does not resolve structural mode shapes or local stresses.
