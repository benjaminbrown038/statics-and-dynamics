# Baseline reference results

Generated from the included case JSON files. Unit names are part of the quantity
labels. Tiny conservation residuals can arise from roundoff or numerical
quadrature; each lesson distinguishes those effects.

## Tier 0: forces, vectors, and moments

| Quantity | Value |
|---|---:|
| resultant_x_N | 300 |
| resultant_y_N | -800 |
| resultant_magnitude_N | 854.400375 |
| resultant_angle_deg | -69.4439548 |
| force1_moment_Nm | -120 |
| force2_moment_Nm | 0 |
| total_moment_about_origin_Nm | -100 |

## Tier 1: support reactions and internal loads

| Quantity | Value |
|---|---:|
| reaction_A_N | 700 |
| reaction_B_N | 500 |
| distributed_resultant_N | 200 |
| maximum_moment_magnitude_Nm | 264 |
| maximum_moment_position_m | 0.4 |
| force_residual_N | 0 |
| moment_residual_Nm | 0 |

## Tier 2: trusses and a rigid frame

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

## Tier 3: friction and the start of motion

| Quantity | Value |
|---|---:|
| state | sliding from rest |
| normal_force_N | 92.1838461 |
| tangential_force_before_friction_N | 33.5521761 |
| static_friction_limit_N | 27.6551538 |
| actual_friction_N | -23.0459615 |
| downslope_acceleration_m_per_s2 | 1.05062145 |
| final_displacement_m | 2.10124291 |
| final_velocity_m_per_s | 2.10124291 |

## Tier 4: centroids and mass moment of inertia

| Quantity | Value |
|---|---:|
| area_m2 | 0.0052 |
| mass_kg | 0.08424 |
| centroid_x_m | 0.0530769231 |
| centroid_y_m | 0.0330769231 |
| mass_inertia_about_centroid_z_kg_m2 | 0.000309876923 |
| mass_inertia_about_origin_z_kg_m2 | 0.00063936 |
| area_second_moment_x_m4 | 6.20410256e-06 |
| area_second_moment_y_m4 | 1.29241026e-05 |

## Tier 5: position, velocity, and acceleration

| Quantity | Value |
|---|---:|
| travel_m | 0.5 |
| duration_s | 1 |
| peak_speed_m_per_s | 0.9375 |
| peak_acceleration_m_per_s2 | 2.88675135 |
| final_position_m | 0.5 |
| final_velocity_m_per_s | 0 |

## Tier 6: particle dynamics and work-energy

| Quantity | Value |
|---|---:|
| static_weight_N | 98.1 |
| peak_cable_tension_N | 126.967513 |
| minimum_cable_tension_N | 69.2324865 |
| exact_total_lifting_work_J | 49.05 |
| integrated_power_work_J | 49.0500001 |
| work_integration_residual_J | 6.61929249e-08 |
| sampled_peak_power_W | 97.7281523 |

## Tier 7: rigid-body dynamics of an actuated arm

| Quantity | Value |
|---|---:|
| mass_inertia_about_pivot_kg_m2 | 0.105 |
| center_of_mass_radius_m | 0.18 |
| sampled_peak_actuator_force_magnitude_N | 140.752999 |
| sampled_peak_quasistatic_force_magnitude_N | 130.852935 |
| sampled_peak_pivot_load_magnitude_N | 132.181064 |
| sampled_max_dynamic_force_increment_N | 14.4090532 |

## Tier 8: impulse, momentum, and stopping loads

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

## Tier 9: vibration and numerical verification

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
| energy_balance_residual_J | -8.35351247e-08 |
| sampled_peak_mount_load_N | 40 |
