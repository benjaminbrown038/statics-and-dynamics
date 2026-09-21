"""Read the adjacent lesson, edit a case JSON, then run this file."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from sdlib.common import inputs, linspace, table, result, run_cli
from sdlib.motion import smooth_move, motion_times, trapezoid, rk4_step


def solve(case):
    """Reduce two planar forces and a couple to an equivalent force-couple system."""
    c=inputs(case,finite=("F1x_N","F1y_N","x1_m","y1_m","F2x_N","F2y_N","x2_m","y2_m","couple_Nm"))
    rx=c["F1x_N"]+c["F2x_N"]
    ry=c["F1y_N"]+c["F2y_N"]
    m1=c["x1_m"]*c["F1y_N"]-c["y1_m"]*c["F1x_N"]
    m2=c["x2_m"]*c["F2y_N"]-c["y2_m"]*c["F2x_N"]
    moment=m1+m2+c["couple_Nm"]
    rows=[dict(reference_x_m=x,moment_about_reference_Nm=moment-x*ry) for x in linspace(-0.2,0.2)]
    return result("Tier 0: forces, vectors, and moments",{
        "resultant_x_N":rx,"resultant_y_N":ry,"resultant_magnitude_N":math.hypot(rx,ry),
        "resultant_angle_deg":math.degrees(math.atan2(ry,rx)) if rx or ry else "undefined (zero resultant)",
        "force1_moment_Nm":m1,"force2_moment_Nm":m2,"total_moment_about_origin_Nm":moment,
    },[table("moment_reference",rows,"reference_x_m",["moment_about_reference_Nm"],"Reference point x, y=0 (m)","Counterclockwise moment (N m)")],
    ["Axes: x right, y up; positive moment is counterclockwise.",
     "An equivalent resultant must retain the correct moment; moving a force generally requires a couple.",
     "A free couple is independent of reference point. Equal-and-opposite forces can have zero resultant and nonzero moment."])

if __name__ == "__main__":
    run_cli(solve, __file__)
