"""Read the adjacent lesson, edit a case JSON, then run this file."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from sdlib.common import inputs, linspace, table, result, run_cli
from sdlib.motion import smooth_move, motion_times, trapezoid, rk4_step


def solve(case):
    """Prescribe a smooth straight-line rest-to-rest motion without assigning forces."""
    c=inputs(case,positive=("duration_s",),finite=("travel_m",))
    D,T=c["travel_m"],c["duration_s"]
    rows=[]
    for t in motion_times(T):
        x,v,a=smooth_move(t,T,0,D)
        rows.append(dict(time_s=t,position_m=x,velocity_m_per_s=v,acceleration_m_per_s2=a))
    return result("Tier 5: position, velocity, and acceleration",{
        "travel_m":D,"duration_s":T,"peak_speed_m_per_s":1.875*abs(D)/T,
        "peak_acceleration_m_per_s2":10*math.sqrt(3)/3*abs(D)/T**2,
        "final_position_m":rows[-1]["position_m"],"final_velocity_m_per_s":rows[-1]["velocity_m_per_s"],
    },[table("position",rows,"time_s",["position_m"],"Time (s)","Position (m)"),
       table("velocity",rows,"time_s",["velocity_m_per_s"],"Time (s)","Velocity (m/s)"),
       table("acceleration",rows,"time_s",["acceleration_m_per_s2"],"Time (s)","Acceleration (m/s²)")],
    ["This is kinematics: motion is prescribed, with no mass or force calculation yet.",
     "Velocity and acceleration are zero at both endpoints; jerk is not constrained to zero.",
     "Halving motion time doubles peak speed and quadruples peak acceleration."])

if __name__ == "__main__":
    run_cli(solve, __file__)
