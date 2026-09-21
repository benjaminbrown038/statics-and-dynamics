# Tier 4: centroids and mass moment of inertia

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

## Interpretation

- The L plate occupies the union of [0,w]x[0,H] and [0,L]x[0,w]; the shared corner is counted once.
- The z axis is normal to the plate. Uniform density and thickness make the area and mass centroids coincide.
- Mass inertia has units kg m²; section area moments have units m⁴. They serve different equations.

Inputs and full numerical tables are preserved in `result.json`.
