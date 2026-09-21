# Units, directions, and frames of reference

Inputs use SI. Key names and CSV column names identify units. The planar examples
use a fixed inertial frame: x right, y up, and z toward the viewer. Positive
rotation/moment is counterclockwise in the x-y plane. Tier 3 instead labels its
one-dimensional coordinate explicitly as positive downslope; Tier 6 is upward.

| Quantity | Unit | Meaning |
|---|---|---|
| Mass | kg | Inertial property; weight is mg in N |
| Force | N | kg m/s² |
| Moment/torque | N m | Signed moment about a specified point/axis |
| Work/energy | J | N m, but a scalar energy rather than a moment vector |
| Angular velocity | rad/s | Convert degrees before trigonometry/differentiation |
| Mass moment of inertia | kg m² | Resistance to angular acceleration |
| Area second moment | m⁴ | Section geometry used in beam bending |
| Impulse | N s | Change in linear momentum |
| Power | W | Energy transfer per second |
| Spring stiffness | N/m | Force per displacement |
| Viscous damping | N s/m | Force per velocity |

The distinction between mass and weight is:

$$
W=mg.
$$

For a fixed axis of rotation of a rigid body, use the mass inertia about that
same axis:

$$
\sum M_{O,z}=I_{O,z}\alpha.
$$

General 3D rotation requires angular-momentum balance rather than blindly using
one scalar inertia. The Tier 7 planar model has a fixed pivot and satisfies the
conditions for the scalar equation.

Reports distinguish forces acting on a moving body from equal-and-opposite
loads that body applies to its mount. Preserve those signs when exporting loads.
CSV output is machine-readable; edit JSON case files using a decimal point and
no trailing commas. All stored numeric inputs must be finite.
