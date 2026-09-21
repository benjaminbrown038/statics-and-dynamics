# Tier 7 — Rigid-body dynamics of an actuated arm

[Previous tier](../../dynamics/tier-6/README.md) · [Next tier](../../dynamics/tier-8/README.md)

## Learning goal

Calculate actuator force and support reactions while an arm accelerates and decelerates.

## Model and assumptions

A uniform rigid rod of mass mr and length L rotates about a fixed frictionless pivot O. A point payload mp is attached at the rod tip. A massless push/pull actuator runs from a stationary anchor A to point B at radius r on the rod. Gravity acts downward. The quintic angular motion is prescribed; actuator dynamics, rod flexibility, backlash, and joint friction are omitted.

## Inputs and free-body diagram

Baseline: mr = 2 kg, mp = 0.5 kg, L = 0.3 m, r = 0.06 m, A = (-0.1, 0.08) m, and angular motion from 10 to 80 degrees in 1.2 s. Global x points right and y up. The geometry matches the design repo’s actuator attachment setup, while the loads here come from mass, gravity, and acceleration.

Edit [cases/baseline.json](cases/baseline.json). See [units and signs](../../docs/units-and-signs.md)
and the [free-body diagram guide](../../docs/free-body-diagrams.md).

## Equations

The moving assembly's mass properties about the fixed pivot are:

$$
m=m_r+m_p,
\qquad S_m=\frac{m_rL}{2}+m_pL,
\qquad r_G=\frac{S_m}{m},
\qquad I_O=\frac{m_rL^2}{3}+m_pL^2.
$$

Use the Tier 5 quintic profile with angular travel:

$$
\theta(t)=\theta_0+(\theta_1-\theta_0)q(t/T),
\qquad \omega=\dot\theta,
\qquad \alpha=\ddot\theta.
$$

The actuator geometry and signed moment arm are:

$$
\mathbf{B}=r\begin{bmatrix}\cos\theta\\\sin\theta\end{bmatrix},
\qquad \ell=\|\mathbf{A}-\mathbf{B}\|,
\qquad \mathbf{u}=\frac{\mathbf{A}-\mathbf{B}}{\ell},
\qquad h=B_xu_y-B_yu_x.
$$

Positive actuator force F pulls B toward A. Moment balance about the fixed pivot
includes gravity and angular acceleration:

$$
Fh-gS_m\cos\theta=I_O\alpha,
\qquad F=\frac{I_O\alpha+gS_m\cos\theta}{h}.
$$

The quasi-static comparison sets angular acceleration to zero at the same angle:

$$
F_{\mathrm{qs}}=\frac{gS_m\cos\theta}{h}.
$$

Center-of-mass acceleration includes both tangential and centripetal terms:

$$
a_{Gx}=r_G(-\alpha\sin\theta-\omega^2\cos\theta),
\qquad a_{Gy}=r_G(\alpha\cos\theta-\omega^2\sin\theta).
$$

Force balance gives the pivot reaction acting on the moving arm:

$$
R_x=ma_{Gx}-Fu_x,
\qquad R_y=ma_{Gy}-Fu_y+mg.
$$

Loads applied to the stationary mounting points have opposite action/reaction
directions:

$$
\mathbf{F}_{\mathrm{pivot\ mount}}=-\mathbf{R},
\qquad \mathbf{F}_{\mathrm{anchor\ mount}}=-F\mathbf{u}.
$$

The code rejects any angular interval containing zero moment arm, including a
collinear position between time samples. Reported peak loads are sampled; refine
the interval count in `sdlib/motion.py` before relying on a narrowly peaked curve.

## Symbols

| Symbol / name | Meaning | Unit |
|---|---|---|
| mr, mp, m | Rod, payload, and total moving mass | kg |
| L, r, rG, A, B, ell, h | Rod/attachment geometry, center radius, actuator length/moment arm | m |
| Sm, IO | First mass moment and fixed-pivot mass inertia | kg m; kg m² |
| theta, omega, alpha | Angle, angular velocity, angular acceleration | rad; rad/s; rad/s² |
| F, R | Actuator force and pivot reaction on moving body | N |
| g, aG | Gravity and center-of-mass acceleration | m/s² |

## Run

From the repository root:

```bash
python3 dynamics/tier-7/main.py
```

Optional PNG plots:

```bash
python3 dynamics/tier-7/main.py --plot
```

The optional plotting dependency is installed with
`python3 -m pip install -r requirements-plot.txt`. Calculations need no packages.
Each run writes a Markdown report, an input/result JSON snapshot, and CSV tables
to `results/tier-7/`. Use `--case path/to/case.json` and
`--output results/my-study` for a separate study. Reusing an output folder
replaces matching files; PNGs are refreshed only by a run with `--plot`.

## Expected behavior

Pivot mass inertia is 0.105 kg m². The sampled peak actuator magnitude is about 140.753 N versus 130.853 N for the quasi-static comparison. The largest pointwise dynamic increment is about 14.4091 N.

## Experiments

Predict before running, change one input at a time, and record the physical
reason in the [study template](../../templates/study-note.md).

1. Increase duration to 12 s. The angular-acceleration force increment falls by a factor of 100 at corresponding motion positions.
2. Increase the payload and observe both gravity and inertial contributions.
3. Set equal start and end angles to check a stationary configuration away from singularity.
4. Move the anchor to (0.1, 0.08) m and explain the rejected collinear position within the motion range.

## Project connections

Export `interface_loads.csv` to analyze pivot and actuator-anchor supports in your design or FEA projects. The quasi-static comparison is not numerically identical to the old constant-40-N-m design case because the applied load model differs.
