# Intro to Statics and Dynamics

Learn how forces balance, how motion creates loads, and how to carry those loads
into mechanics of materials, machine/aerospace design, and FEA.

**Ten complete runnable tiers** cover force vectors, beam reactions, trusses,
frames, friction, mass properties, kinematics, lifting, rotating mechanisms,
stopping loads, and vibration. All equations also appear in this main README.

## Start here

Python 3.9 or newer. Core calculations, reports, CSV exports, and tests use only
the standard library. From the extracted repository folder:

```bash
python3 fundamentals/tier-0/main.py
python3 run_all.py
python3 -m unittest discover -s tests -v
```

Open `results/tier-0/report.md`, then read its lesson and edit its baseline case.
You can also run `python3 main.py` from inside any tier folder.

## Learning progression

| Tier | Topic | Implemented example |
|---|---|---|
| [0](fundamentals/tier-0/README.md) | Forces and moments | Equivalent planar force-couple system |
| [1](statics/tier-1/README.md) | Equilibrium and internal loads | Beam with point and distributed loads |
| [2](statics/tier-2/README.md) | Trusses and frames | Triangular truss plus rigid L-frame comparison |
| [3](statics/tier-3/README.md) | Friction | Sticking/sliding block on an incline |
| [4](statics/tier-4/README.md) | Centroids and mass inertia | Composite L-shaped plate |
| [5](dynamics/tier-5/README.md) | Kinematics | Smooth rest-to-rest motion |
| [6](dynamics/tier-6/README.md) | Particle dynamics and work-energy | Cable lift force, power, and work |
| [7](dynamics/tier-7/README.md) | Rigid-body dynamics | Accelerating arm, actuator force, mounting loads |
| [8](dynamics/tier-8/README.md) | Impulse and momentum | Half-sine stopping-force pulse |
| [9](dynamics/tier-9/README.md) | Vibration and numerical integration | Damped spring-mass response versus exact solution |

Work through the numbered sequence. Statics determines equilibrium loads;
kinematics describes motion; dynamics relates motion to forces. Tier numbers are
local to this repo. [All equations](#equation-reference) are collected below.

## Optional plots

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements-plot.txt
python3 run_all.py --plot
```

On Windows use `.venv\Scripts\activate`. Plots are saved to PNG without opening
a window. See the [plot gallery](docs/plots.md), [reference results](docs/baseline-results.md),
and [verification record](docs/verification.md).

## Change a case

```bash
cp dynamics/tier-7/cases/baseline.json dynamics/tier-7/cases/my-arm.json
python3 dynamics/tier-7/main.py \
  --case dynamics/tier-7/cases/my-arm.json \
  --output results/my-arm
```

Edit the copied file before running. SI units are named in the JSON keys.
Invalid inputs produce a clear error. A run that completes is a model
calculation, not a declaration that a component meets design requirements.
Reusing an output folder replaces matching files; CSV-only runs do not refresh
existing PNGs.

## Repository map

| Location | Purpose |
|---|---|
| `fundamentals/tier-0/` | Vectors, moments, and free-body reasoning |
| `statics/tier-1/` through `tier-4/` | Equilibrium, trusses/frames, friction, mass properties |
| `dynamics/tier-5/` through `tier-9/` | Motion, forces, energy, impulse, vibration |
| Each tier's `main.py` | Readable physical calculations |
| Each tier's `cases/baseline.json` | Editable inputs |
| `sdlib/common.py` | Input validation, reports, CSV export, optional plots |
| `sdlib/motion.py` | Quintic motion, quadrature, RK4 step |
| `tests/` | Equilibrium, analytical limits, conservation, convergence checks |
| `docs/`, `templates/` | Learning guides, diagrams, study notes, references |
| `results/` | Generated outputs, ignored by Git |

## Connect the projects

| Project | Role in a component study |
|---|---|
| Statics and dynamics | Determine forces, moments, motion, and time histories |
| Mechanics of materials | Calculate stresses, strains, deflection, and failure indicators |
| Machine/aerospace design | Choose dimensions, materials, attachments, and mechanisms |
| FEA | Investigate detailed geometry, constraints, and structural response |

Tier 7 exports pivot and actuator-anchor loads in `interface_loads.csv`.
Tier 8 exports stopping loads; Tier 9 exports dynamic mount force. Read the
[load-transfer guide](docs/load-transfer.md) before applying them to a different
geometry. This is a documented manual handoff, not automatic repo coupling.

The examples are idealized teaching cases. Model assumptions are stated beside
their equations. The arm is a planar component mechanism, not a whole-aircraft
flight-dynamics model. Native CAD files and full structural FEA are not included.

## Put it on GitHub

The archive contains source files without Git history or a remote. Create an
empty GitHub repository named `intro-to-statics-and-dynamics`, then run from
this folder after replacing `YOUR_USERNAME`:

```bash
git init -b main
git add .
git commit -m "Add progressive statics and dynamics learning examples"
git remote add origin https://github.com/YOUR_USERNAME/intro-to-statics-and-dynamics.git
git push -u origin main
```

If already initialized, retain your existing history and remote. No open-source
license is selected; choose one before inviting reuse or external contributions.

## Future extensions

Not implemented here: general truss/frame solvers, 3D rigid-body rotation,
multibody constraint solvers, contact/restitution, forced vibration and resonance
sweeps, multi-degree-of-freedom vibration, flexible mechanisms, and controls.

## Equation reference

All ten lessons’ equations are collected here, with model assumptions and symbol
definitions. Display equations use the same `$$` format throughout the repo.

### Tier 0 — Forces, vectors, moments, and free-body diagrams

[Full lesson and runnable example](fundamentals/tier-0/README.md)

Two forces act at specified points on a rigid body. A separate free couple may also act. Coordinates are x right and y up; positive moments are counterclockwise. This runnable example is planar. The vector equations also express the 3D generalization.

#### Equations

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

#### Symbols

| Symbol / name | Meaning | Unit |
|---|---|---|
| F, R | Applied force and resultant | N |
| r, x, y | Position relative to the reference | m |
| M, C | Force moment and free couple | N m |
| theta | Direction measured counterclockwise from +x | rad internally; degrees in output |

### Tier 1 — Equilibrium, support reactions, and internal loads

[Full lesson and runnable example](statics/tier-1/README.md)

A pin at A = (0, 0) and roller at B = (L, 0) support a beam. A point load P acts downward at x = a, and a uniform distributed load q acts downward over the entire span. Horizontal reaction is zero. Self-weight is included only if represented in q.

#### Equations

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

#### Symbols

| Symbol / name | Meaning | Unit |
|---|---|---|
| P, RA, RB, W | Point load, reactions, distributed-load resultant | N |
| q | Downward load per unit length | N/m |
| L, a, x | Span, point-load location, section position | m |
| V, M | Internal shear and bending moment | N; N m |

### Tier 2 — Trusses, two-force members, and a rigid frame

[Full lesson and runnable example](statics/tier-2/README.md)

Two separate structures use the same signed load components. The triangular truss has pin A = (0,0), roller B = (L,0), and loaded apex C = (L/2,H). Joints are ideal pins and members are straight, weightless two-force members. The separate L-frame is fixed at A = (0,0), has a rigid elbow B = (0,H), and is loaded at tip C = (L,H).

#### Equations

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

#### Symbols

| Symbol / name | Meaning | Unit |
|---|---|---|
| L, H, ell d | Span/horizontal reach, height, truss diagonal length | m |
| Fx, Fy | Signed applied force components | N |
| NAB, NAC, NBC | Member forces; positive tension, negative compression | N |
| Ax, Ay, By, Rx, Ry | Support-force components | N |
| MA, MB cut | Counterclockwise reaction/cut moment | N m |

### Tier 3 — Friction and the start of motion

[Full lesson and runnable example](statics/tier-3/README.md)

A block starts from rest on a long rigid incline. An optional constant force acts parallel to the plane. Downslope is positive. The normal load is supplied by gravity; Coulomb coefficients are constant, with kinetic coefficient no greater than static coefficient. Rolling, tipping, and contact loss are excluded.

#### Equations

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

#### Symbols

| Symbol / name | Meaning | Unit |
|---|---|---|
| m, g | Mass and gravitational acceleration | kg; m/s² |
| theta | Incline angle | rad internally |
| N, D, F parallel, f | Normal force, demand, applied force, signed friction | N |
| mu s, mu k | Static and kinetic friction coefficients | 1 |
| a, v, s, t | Acceleration, velocity, displacement, time | m/s²; m/s; m; s |

### Tier 4 — Centroids and mass moments of inertia

[Full lesson and runnable example](statics/tier-4/README.md)

A uniform L-shaped plate has horizontal outer length L, vertical outer length H, equal leg width w, thickness t, and density rho. Its origin is the outer lower-left corner. Divide it into a w by H rectangle and a (L-w) by w rectangle so the shared corner is not double counted. The inertia axis z is perpendicular to the plate.

#### Equations

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

#### Symbols

| Symbol / name | Meaning | Unit |
|---|---|---|
| L, H, w, t, bi, hi | Plate and rectangular-piece dimensions | m |
| rho, mi, m | Density, piece mass, total mass | kg/m³; kg; kg |
| xG, yG, d | Centroid coordinates and parallel-axis offset | m |
| IGz, IOz, IQz | Mass moment about specified z axis | kg m² |
| IAx, IAy | Centroidal area second moments | m⁴ |

### Tier 5 — Position, velocity, and acceleration

[Full lesson and runnable example](dynamics/tier-5/README.md)

A point moves along a straight line by signed distance D in duration T. A quintic position profile starts and ends with zero velocity and acceleration. The motion is prescribed, so this tier does not solve an equation of motion.

#### Equations

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

#### Symbols

| Symbol / name | Meaning | Unit |
|---|---|---|
| D, x, x0 | Signed travel, position, initial position | m |
| T, t, s | Duration, time, normalized time | s; s; 1 |
| q | Dimensionless motion profile | 1 |
| v, a | Velocity and acceleration | m/s; m/s² |

### Tier 6 — Particle dynamics, lifting loads, and work-energy

[Full lesson and runnable example](dynamics/tier-6/README.md)

A mass is lifted vertically by a single massless, taut cable using the Tier 5 motion profile. Up is positive. Gravity is constant; guide friction, pulley ratios, cable elasticity, and motor losses are omitted. The cable can pull but cannot push, so cases requiring negative tension are rejected.

#### Equations

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

#### Symbols

| Symbol / name | Meaning | Unit |
|---|---|---|
| m, g | Lifted mass and gravity | kg; m/s² |
| F | Single-strand cable tension | N |
| x, v, a | Upward position, velocity, acceleration | m; m/s; m/s² |
| P calligraphic, WF | Mechanical power and work done by the cable | W; J |
| D, T | Lift and move duration | m; s |

### Tier 7 — Rigid-body dynamics of an actuated arm

[Full lesson and runnable example](dynamics/tier-7/README.md)

A uniform rigid rod of mass mr and length L rotates about a fixed frictionless pivot O. A point payload mp is attached at the rod tip. A massless push/pull actuator runs from a stationary anchor A to point B at radius r on the rod. Gravity acts downward. The quintic angular motion is prescribed; actuator dynamics, rod flexibility, backlash, and joint friction are omitted.

#### Equations

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

#### Symbols

| Symbol / name | Meaning | Unit |
|---|---|---|
| mr, mp, m | Rod, payload, and total moving mass | kg |
| L, r, rG, A, B, ell, h | Rod/attachment geometry, center radius, actuator length/moment arm | m |
| Sm, IO | First mass moment and fixed-pivot mass inertia | kg m; kg m² |
| theta, omega, alpha | Angle, angular velocity, angular acceleration | rad; rad/s; rad/s² |
| F, R | Actuator force and pivot reaction on moving body | N |
| g, aG | Gravity and center-of-mass acceleration | m/s² |

### Tier 8 — Impulse, momentum, and stopping loads

[Full lesson and runnable example](dynamics/tier-8/README.md)

A mass moves horizontally at speed v0 and stops over prescribed time T under a half-sine force pulse. Initial velocity is positive. Normal force balances gravity, and no other horizontal force acts. The pulse is an assumed load history; contact stiffness, restitution, and rebound are not simulated.

#### Equations

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

#### Symbols

| Symbol / name | Meaning | Unit |
|---|---|---|
| m, v0, vf | Mass, initial speed, final speed | kg; m/s; m/s |
| T, t | Stopping duration and elapsed time | s |
| F, Fpk, Favg | Signed force on mass, peak and average magnitudes | N |
| x, v | Displacement and velocity | m; m/s |
| Impulse, work | Force-time integral, force-displacement integral | N s; J |

### Tier 9 — Free vibration and numerical verification

[Full lesson and runnable example](dynamics/tier-9/README.md)

A single mass is attached to a linear spring and viscous damper on a fixed base. Displacement is measured from static equilibrium. There is no external forcing. The supported damping range is 0 <= zeta < 1 so an underdamped or undamped exact solution is available. Gravity preload is not included in the dynamic mount-load column.

#### Equations

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

#### Symbols

| Symbol / name | Meaning | Unit |
|---|---|---|
| m, k, c | Mass, spring stiffness, viscous damping coefficient | kg; N/m; N s/m |
| zeta | Damping ratio | 1 |
| omega n, omega d, fn | Natural and damped angular frequencies; natural frequency | rad/s; rad/s; Hz |
| x, v, h | Displacement from equilibrium, velocity, time step | m; m/s; s |
| E, Fmount | Mechanical energy and dynamic force on fixed base | J; N |
