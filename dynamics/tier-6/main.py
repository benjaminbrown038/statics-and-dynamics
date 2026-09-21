"""Read the adjacent lesson, edit a case JSON, then run this file."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from sdlib.common import inputs, linspace, table, result, run_cli
from sdlib.motion import smooth_move, motion_times, trapezoid, rk4_step


def solve(case):
    """Compute single-strand cable tension and lifting work for a prescribed motion."""
    c=inputs(case,positive=("mass_kg","lift_m","duration_s","gravity_m_per_s2"))
    m,D,T,g=(c[k] for k in ("mass_kg","lift_m","duration_s","gravity_m_per_s2"))
    a_peak=10*math.sqrt(3)/3*D/T**2
    if a_peak>g: raise ValueError("prescribed deceleration requires negative cable tension; lengthen duration or use a bilateral actuator model")
    rows=[]
    for t in motion_times(T):
        x,v,a=smooth_move(t,T,0,D)
        tension=m*(g+a)
        rows.append(dict(time_s=t,height_m=x,velocity_m_per_s=v,acceleration_m_per_s2=a,
                         cable_tension_N=tension,power_W=tension*v,actuator_work_exact_J=m*g*x+m*v*v/2))
    work=trapezoid([r["time_s"] for r in rows],[r["power_W"] for r in rows])
    return result("Tier 6: particle dynamics and work-energy",{
        "static_weight_N":m*g,"peak_cable_tension_N":m*(g+a_peak),"minimum_cable_tension_N":m*(g-a_peak),
        "exact_total_lifting_work_J":m*g*D,"integrated_power_work_J":work,
        "work_integration_residual_J":work-m*g*D,"sampled_peak_power_W":max(r["power_W"] for r in rows),
    },[table("lift_loads",rows,"time_s",["cable_tension_N"],"Time (s)","Single-strand tension (N)"),
       table("lift_power",rows,"time_s",["power_W"],"Time (s)","Mechanical power (W)")],
    ["Up is positive; a massless vertical cable carries the moving mass without pulley mechanical advantage.",
     "The cable pulls only. Inputs demanding negative tension are rejected because the prescribed motion would lose tautness.",
     "Work includes gravity and kinetic energy. Total work here equals m g lift because initial and final speeds are zero; motor losses are omitted."])

if __name__ == "__main__":
    run_cli(solve, __file__)
