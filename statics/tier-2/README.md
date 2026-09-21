# Tier 2 — Trusses, two-force members, and a rigid frame

[Previous tier](../../statics/tier-1/README.md) · [Next tier](../../statics/tier-3/README.md)

## Learning goal

Use joint equilibrium to find truss forces, then distinguish a frame member that transmits moment.

## Model and assumptions

Two separate structures use the same signed load components. The triangular truss has pin A = (0,0), roller B = (L,0), and loaded apex C = (L/2,H). Joints are ideal pins and members are straight, weightless two-force members. The separate L-frame is fixed at A = (0,0), has a rigid elbow B = (0,H), and is loaded at tip C = (L,H).

## Inputs and free-body diagram

Baseline: L = 2 m, H = 1 m, Fx = 0, Fy = -1000 N. Draw each joint separately for the truss. Draw the whole frame and then cut its horizontal arm at the elbow. A negative ideal roller reaction would require a hold-down support.

Edit [cases/baseline.json](cases/baseline.json). See [units and signs](../../docs/units-and-signs.md)
and the [free-body diagram guide](../../docs/free-body-diagrams.md).

## Equations

For the truss diagonal geometry:

$$
\ell_d=\sqrt{(L/2)^2+H^2},
\qquad c_\theta=\frac{L}{2\ell_d},
\qquad s_\theta=\frac{H}{\ell_d}.
$$

Whole-truss equilibrium gives:

$$
A_x=-F_x,
\qquad B_y=-\frac{F_y}{2}+\frac{HF_x}{L},
\qquad A_y=-F_y-B_y.
$$

Take member force positive in tension. Joint C and then joint A give:

$$
N_{AC}=\frac{1}{2}\left(\frac{F_y}{s_\theta}+\frac{F_x}{c_\theta}\right),
\qquad N_{BC}=\frac{1}{2}\left(\frac{F_y}{s_\theta}-\frac{F_x}{c_\theta}\right),
$$

$$
N_{AB}=-A_x-c_\theta N_{AC}.
$$

For the separate rigid frame, whole-body equilibrium gives:

$$
R_x=-F_x,
\qquad R_y=-F_y,
\qquad M_A=-(LF_y-HF_x).
$$

The cut moment acting on the isolated horizontal arm at B is:

$$
M_{B,\mathrm{cut}}=-LF_y.
$$

The frame's members carry shear and bending in addition to possible axial force.
The truss and frame are specific determinate examples, not general solvers.

## Symbols

| Symbol / name | Meaning | Unit |
|---|---|---|
| L, H, ell d | Span/horizontal reach, height, truss diagonal length | m |
| Fx, Fy | Signed applied force components | N |
| NAB, NAC, NBC | Member forces; positive tension, negative compression | N |
| Ax, Ay, By, Rx, Ry | Support-force components | N |
| MA, MB cut | Counterclockwise reaction/cut moment | N m |

## Run

From the repository root:

```bash
python3 statics/tier-2/main.py
```

Optional PNG plots:

```bash
python3 statics/tier-2/main.py --plot
```

The optional plotting dependency is installed with
`python3 -m pip install -r requirements-plot.txt`. Calculations need no packages.
Each run writes a Markdown report, an input/result JSON snapshot, and CSV tables
to `results/tier-2/`. Use `--case path/to/case.json` and
`--output results/my-study` for a separate study. Reusing an output folder
replaces matching files; PNGs are refreshed only by a run with `--plot`.

## Expected behavior

Truss reactions are 500 N upward at each support. AB carries +500 N tension; AC and BC each carry -707.107 N compression. The separate frame requires a +2000 N m root reaction moment.

## Experiments

Predict before running, change one input at a time, and record the physical
reason in the [study template](../../templates/study-note.md).

1. Reduce H at fixed span and vertical load; diagonal and bottom-chord force magnitudes increase.
2. Add a horizontal apex load and check the unequal support reactions and all three joint balances.
3. Explain why modeling a rigid frame elbow as a pin changes the structural problem.

## Project connections

Truss axial forces feed rod stress and buckling checks. Frame internal moments feed bending checks. Connections determine which idealization is appropriate.
