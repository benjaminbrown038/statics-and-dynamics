"""Read the adjacent lesson, edit a case JSON, then run this file."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from sdlib.common import inputs, linspace, table, result, run_cli
from sdlib.motion import smooth_move, motion_times, trapezoid, rk4_step


def solve(case):
    """Find beam reactions, shear, and moment for point and uniform distributed loads."""
    c=inputs(case,positive=("length_m",),nonnegative=("point_load_N","point_position_m","uniform_load_N_per_m"))
    L,P,a,q=(c[k] for k in ("length_m","point_load_N","point_position_m","uniform_load_N_per_m"))
    if a>L: raise ValueError("point_position_m must lie within the span")
    RB=(P*a+q*L**2/2)/L
    RA=P+q*L-RB
    def moment(x): return RA*x-q*x*x/2-P*max(0,x-a)
    critical=[0,a,L]
    if q:
        if 0<RA/q<a: critical.append(RA/q)
        if a<(RA-P)/q<L: critical.append((RA-P)/q)
    rows=[]
    for x in sorted(set(linspace(0,L)+critical)):
        if x==a: rows.append(dict(x_m=x,shear_N=RA-q*x,moment_Nm=moment(x)))
        rows.append(dict(x_m=x,shear_N=RA-q*x-(P if x>=a else 0),moment_Nm=moment(x)))
    max_x=max(critical,key=lambda x:abs(moment(x)))
    return result("Tier 1: support reactions and internal loads",{
        "reaction_A_N":RA,"reaction_B_N":RB,"distributed_resultant_N":q*L,
        "maximum_moment_magnitude_Nm":abs(moment(max_x)),"maximum_moment_position_m":max_x,
        "force_residual_N":RA+RB-P-q*L,"moment_residual_Nm":RB*L-P*a-q*L**2/2,
    },[table("beam_shear",rows,"x_m",["shear_N"],"Position (m)","Shear (N)"),
       table("beam_moment",rows,"x_m",["moment_Nm"],"Position (m)","Sagging moment (N m)")],
    ["A pin at x=0 and roller at x=L support downward loads. Horizontal reaction is zero.",
     "The uniform load's resultant acts at midspan for whole-beam equilibrium; retain the distributed load for internal diagrams.",
     "Maximum moment is evaluated at endpoints, the point load, and valid zero-shear locations."])

if __name__ == "__main__":
    run_cli(solve, __file__)
