# Baseline plot gallery

Run `python3 run_all.py --plot` to reproduce the response plots.
See the [free-body diagrams](free-body-diagrams.md) for model geometry and forces.

## Beam bending moment

![Beam bending moment](images/beam_moment.png)

The point load creates a slope change; the distributed load produces curvature in the moment diagram.

## Dynamic and quasi-static actuator force

![Dynamic and quasi-static actuator force](images/interface_loads.png)

The difference depends on angular acceleration and moment arm. Slowing the same motion reduces the inertial force increment.

## Stopping-force pulse

![Stopping-force pulse](images/stop_loads.png)

The assumed half-sine pulse has a larger peak than its average force.

## Damped free vibration

![Damped free vibration](images/vibration.png)

The numerical and exact curves closely overlap. Read the reported numerical error to see their small difference.
