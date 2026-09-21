# Carrying loads into your other projects

Statics and dynamics calculate a load. Stress analysis still needs a component
geometry, a section, a material model, and an appropriate restraint description.

| Output | Available quantity | Next use |
|---|---|---|
| Tier 1 `beam_moment.csv` | Internal moment and shear versus position | Mechanics beam stress and deflection models |
| Tier 2 `members.csv` | Signed truss axial force | Axial stress and compression/buckling checks |
| Tier 6 `lift_loads.csv` | One cable strand's tension versus time | Cable/anchor sizing after drawing the actual support load path |
| Tier 7 `interface_loads.csv` | Simultaneous x/y forces on pivot and fixed actuator anchor | Brackets, mounts, bolt groups, or FEA boundary loads |
| Tier 8 `stop_loads.csv` | Force pulse on a stop | Stop/bumper stress and transient response |
| Tier 9 `vibration.csv` | Signed dynamic mount force | Add any applicable static preload, then analyze the support |

## A concrete arm-mount handoff

1. Run `python3 dynamics/tier-7/main.py`.
2. Open `results/tier-7/interface_loads.csv`.
3. Select a time row and keep its simultaneous x and y components together.
4. For a pivot bracket, use the columns containing `pivot_load_on_mount`.
   For the separate actuator anchor, use `fixed_anchor_load_on_mount`.
5. Map global x/y directions into the receiving model and specify the actual
   point of application. Add the moment produced by any offset from the support.
6. Evaluate the receiving model over the time rows to find its governing stress
   or deflection; the largest force magnitude need not govern every failure mode.

Do not combine independently maximized force components from different times
and describe that combination as an actual time state. Such an envelope, if
chosen, is a separate bounding assumption. Do not apply both an already-shifted
force-couple system and the same eccentricity again.

For a planar force applied at offset (rx, ry), the moment about the receiving
reference is:

$$
M_z=r_xF_y-r_yF_x.
$$

For example, a horizontal idealized support of span ell with tip components Fx
and Fy has axial force Fx and root bending-moment magnitude |Fy| ell. The actual
bracket geometry must justify that idealization before using the beam equations.

## Where dynamic structural response enters

The arm model determines rigid-body interface loads. A quasi-static structural
check at each time assumes the support responds without significant dynamic
amplification. A flexible support can vibrate under the same force history;
Tier 9 introduces that response concept, and transient FEA can resolve more
complex structural behavior. No automatic connection to the other repos or
transient 3D structural solver is included here.

The design repo's door-arm case uses a prescribed constant 40 N m resisting
moment. This repo uses gravity and acceleration of an explicit mass distribution.
The attachment geometry is comparable, but forces will differ with those loads.
