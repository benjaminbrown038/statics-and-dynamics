# Tier 8: impulse, momentum, and stopping loads

| Quantity | Value |
|---|---:|
| peak_stop_load_N | 628.318531 |
| average_stop_load_N | 400 |
| exact_impulse_on_mass_Ns | -40 |
| integrated_impulse_Ns | -39.9991775 |
| impulse_integration_residual_Ns | 0.000822470416 |
| stop_distance_m | 0.1 |
| initial_kinetic_energy_J | 40 |
| integrated_work_on_mass_J | -39.9991775 |
| work_integration_residual_J | 0.000822470416 |

## Interpretation

- The mass moves initially in +x. Stopping force is negative; the reaction load on the stop is positive.
- Pulse shape and duration are prescribed; the model does not derive them from contact stiffness or simulate rebound.
- Average and peak force differ. Initial kinetic energy is removed over the stopping distance.

Inputs and full numerical tables are preserved in `result.json`.
