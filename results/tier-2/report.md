# Tier 2: trusses and a rigid frame

| Quantity | Value |
|---|---:|
| truss_Ax_N | -0 |
| truss_Ay_N | 500 |
| truss_By_N | 500 |
| truss_AB_N | 500 |
| truss_AC_N | -707.106781 |
| truss_BC_N | -707.106781 |
| maximum_joint_residual_N | 0 |
| frame_root_Rx_N | -0 |
| frame_root_Ry_N | 1000 |
| frame_root_reaction_moment_Nm | 2000 |
| frame_elbow_cut_moment_on_horizontal_member_Nm | 2000 |

## Interpretation

- Truss joints: A=(0,0) pin; B=(L,0) roller; C=(L/2,H) loaded. Each member is a two-force member.
- Separate frame: A=(0,0) fixed, elbow B=(0,H), tip C=(L,H) loaded. Its rigid elbow transmits moment.
- Both are specific determinate examples, not general truss/frame solvers. A negative roller reaction requires hold-down rather than unilateral contact.

Inputs and full numerical tables are preserved in `result.json`.
