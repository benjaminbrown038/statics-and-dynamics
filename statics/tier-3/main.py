"""Read the adjacent lesson, edit a case JSON, then run this file."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from sdlib.common import inputs, linspace, table, result, run_cli
from sdlib.motion import smooth_move, motion_times, trapezoid, rk4_step


def solve(case):
    """Decide whether an initially stationary block sticks or begins sliding."""
    c=inputs(case,positive=("mass_kg","gravity_m_per_s2","duration_s"),
             nonnegative=("incline_deg","mu_static","mu_kinetic"),finite=("applied_downslope_N",))
    m,g,tend=c["mass_kg"],c["gravity_m_per_s2"],c["duration_s"]
    if c["incline_deg"]>=90: raise ValueError("incline_deg must be in [0,90)")
    if c["mu_kinetic"]>c["mu_static"]: raise ValueError("this model requires mu_kinetic <= mu_static")
    theta=math.radians(c["incline_deg"])
    normal=m*g*math.cos(theta)
    demand=m*g*math.sin(theta)+c["applied_downslope_N"]
    limit=c["mu_static"]*normal
    sticks=abs(demand)<=limit
    friction=-demand if sticks else -math.copysign(c["mu_kinetic"]*normal,demand)
    acceleration=(demand+friction)/m
    rows=[dict(time_s=t,displacement_m=acceleration*t*t/2,velocity_m_per_s=acceleration*t) for t in linspace(0,tend,201)]
    return result("Tier 3: friction and the start of motion",{
        "state":"sticking" if sticks else "sliding from rest","normal_force_N":normal,
        "tangential_force_before_friction_N":demand,"static_friction_limit_N":limit,
        "actual_friction_N":friction,"downslope_acceleration_m_per_s2":acceleration,
        "final_displacement_m":rows[-1]["displacement_m"],"final_velocity_m_per_s":rows[-1]["velocity_m_per_s"],
    },[table("block_motion",rows,"time_s",["displacement_m"],"Time (s)","Downslope displacement (m)")],
    ["Positive displacement and applied force are downhill. The block starts at rest on a sufficiently long plane.",
     "Static friction adjusts to the required value up to its limit; it is not always mu_static times normal force.",
     "The kinetic phase has constant loads and no velocity reversal. Tipping and rolling are outside this model."])

if __name__ == "__main__":
    run_cli(solve, __file__)
