"""Read the adjacent lesson, edit a case JSON, then run this file."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from sdlib.common import inputs, linspace, table, result, run_cli
from sdlib.motion import smooth_move, motion_times, trapezoid, rk4_step


def solve(case):
    """Stop a horizontally moving mass with a prescribed half-sine force pulse."""
    c=inputs(case,positive=("mass_kg","stop_duration_s"),nonnegative=("initial_speed_m_per_s",))
    m,v0,T=(c[k] for k in ("mass_kg","initial_speed_m_per_s","stop_duration_s"))
    peak=math.pi*m*v0/(2*T)
    rows=[]
    for t in linspace(0,T,201):
        angle=math.pi*t/T
        force=-peak*math.sin(angle)
        velocity=v0*(1+math.cos(angle))/2
        x=v0*(t+T/math.pi*math.sin(angle))/2
        rows.append(dict(time_s=t,force_on_mass_N=force,load_on_stop_N=-force,
                         velocity_m_per_s=velocity,displacement_m=x,kinetic_energy_J=m*velocity**2/2))
    impulse=trapezoid([r["time_s"] for r in rows],[r["force_on_mass_N"] for r in rows])
    work=trapezoid([r["displacement_m"] for r in rows],[r["force_on_mass_N"] for r in rows])
    return result("Tier 8: impulse, momentum, and stopping loads",{
        "peak_stop_load_N":peak,"average_stop_load_N":m*v0/T,"exact_impulse_on_mass_Ns":-m*v0,
        "integrated_impulse_Ns":impulse,"impulse_integration_residual_Ns":impulse+m*v0,
        "stop_distance_m":v0*T/2,"initial_kinetic_energy_J":m*v0**2/2,
        "integrated_work_on_mass_J":work,"work_integration_residual_J":work+m*v0**2/2,
    },[table("stop_loads",rows,"time_s",["load_on_stop_N"],"Time (s)","Force on stop (N)"),
       table("stop_velocity",rows,"time_s",["velocity_m_per_s"],"Time (s)","Velocity (m/s)")],
    ["The mass moves initially in +x. Stopping force is negative; the reaction load on the stop is positive.",
     "Pulse shape and duration are prescribed; the model does not derive them from contact stiffness or simulate rebound.",
     "Average and peak force differ. Initial kinetic energy is removed over the stopping distance."])

if __name__ == "__main__":
    run_cli(solve, __file__)
