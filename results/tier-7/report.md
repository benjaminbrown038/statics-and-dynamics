# Tier 7: rigid-body dynamics of an actuated arm

| Quantity | Value |
|---|---:|
| mass_inertia_about_pivot_kg_m2 | 0.105 |
| center_of_mass_radius_m | 0.18 |
| sampled_peak_actuator_force_magnitude_N | 140.752999 |
| sampled_peak_quasistatic_force_magnitude_N | 130.852935 |
| sampled_peak_pivot_load_magnitude_N | 132.181064 |
| sampled_max_dynamic_force_increment_N | 14.4090532 |

## Interpretation

- The moving body is a uniform rigid rod plus a point payload at its tip. Gravity acts vertically downward.
- The massless actuator can push and pull; positive force pulls the arm attachment toward the fixed anchor.
- CSV includes equal-and-opposite loads on the stationary pivot and actuator anchor, with global x right and y up.
- Peak force and pivot load are sampled, not guaranteed continuous extrema. Joint friction, backlash, flexibility, and actuator mass are omitted.

Inputs and full numerical tables are preserved in `result.json`.
