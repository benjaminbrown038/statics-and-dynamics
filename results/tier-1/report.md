# Tier 1: support reactions and internal loads

| Quantity | Value |
|---|---:|
| reaction_A_N | 700 |
| reaction_B_N | 500 |
| distributed_resultant_N | 200 |
| maximum_moment_magnitude_Nm | 264 |
| maximum_moment_position_m | 0.4 |
| force_residual_N | 0 |
| moment_residual_Nm | 0 |

## Interpretation

- A pin at x=0 and roller at x=L support downward loads. Horizontal reaction is zero.
- The uniform load's resultant acts at midspan for whole-beam equilibrium; retain the distributed load for internal diagrams.
- Maximum moment is evaluated at endpoints, the point load, and valid zero-shear locations.

Inputs and full numerical tables are preserved in `result.json`.
