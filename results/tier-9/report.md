# Tier 9: vibration and numerical verification

| Quantity | Value |
|---|---:|
| natural_frequency_rad_per_s | 20 |
| natural_frequency_Hz | 3.18309886 |
| damped_frequency_rad_per_s | 19.9749844 |
| damping_Ns_per_m | 20 |
| actual_time_step_s | 0.002 |
| integration_steps | 1000 |
| maximum_displacement_error_mm | 1.57402763e-06 |
| initial_energy_J | 0.2 |
| final_energy_J | 0.00349489871 |
| integrated_damping_loss_J | 0.196505018 |
| energy_balance_residual_J | -8.35351248e-08 |
| sampled_peak_mount_load_N | 40 |

## Interpretation

- One translational degree of freedom, linear spring, viscous damping, fixed base, and no external forcing.
- Displacement is measured from static equilibrium; the CSV load is the dynamic increment on the mount, excluding any gravity preload.
- RK4 error and damping-loss quadrature error are separate numerical effects. Refine the time step to check both.

Inputs and full numerical tables are preserved in `result.json`.
