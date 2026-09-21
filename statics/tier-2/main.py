"""Read the adjacent lesson, edit a case JSON, then run this file."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from sdlib.common import inputs, linspace, table, result, run_cli
from sdlib.motion import smooth_move, motion_times, trapezoid, rk4_step


def truss(L,H,Fx,Fy):
    length=math.hypot(L/2,H)
    co,si=L/(2*length),H/length
    Ax=-Fx
    By=-Fy/2+H*Fx/L
    Ay=-Fy-By
    AC=(Fy/si+Fx/co)/2
    BC=(Fy/si-Fx/co)/2
    AB=-Ax-co*AC
    return Ax,Ay,By,AB,AC,BC,co,si


def solve(case):
    """Compare axial truss forces with the reactions of a rigid bent cantilever."""
    c=inputs(case,positive=("span_m","height_m"),finite=("load_x_N","load_y_N"))
    L,H,Fx,Fy=(c[k] for k in ("span_m","height_m","load_x_N","load_y_N"))
    Ax,Ay,By,AB,AC,BC,co,si=truss(L,H,Fx,Fy)
    residuals=[Ax+AB+co*AC,Ay+si*AC,-AB-co*BC,By+si*BC,Fx-co*AC+co*BC,Fy-si*AC-si*BC]
    members=[dict(member=name,axial_force_N=value,state="tension" if value>0 else "compression" if value<0 else "zero")
             for name,value in (("AB",AB),("AC",AC),("BC",BC))]
    sweep=[]
    for h in linspace(H/2,2*H):
        _,_,_,fAB,fAC,fBC,_,_=truss(L,h,Fx,Fy)
        sweep.append(dict(height_m=h,AB_N=fAB,AC_N=fAC,BC_N=fBC))
    return result("Tier 2: trusses and a rigid frame",{
        "truss_Ax_N":Ax,"truss_Ay_N":Ay,"truss_By_N":By,
        "truss_AB_N":AB,"truss_AC_N":AC,"truss_BC_N":BC,
        "maximum_joint_residual_N":max(map(abs,residuals)),
        "frame_root_Rx_N":-Fx,"frame_root_Ry_N":-Fy,"frame_root_reaction_moment_Nm":-(L*Fy-H*Fx),
        "frame_elbow_cut_moment_on_horizontal_member_Nm":-L*Fy,
    },[table("members",members,"member",[],"",""),
       table("truss_height",sweep,"height_m",["AB_N","AC_N","BC_N"],"Apex height (m)","Member force, tension positive (N)")],
    ["Truss joints: A=(0,0) pin; B=(L,0) roller; C=(L/2,H) loaded. Each member is a two-force member.",
     "Separate frame: A=(0,0) fixed, elbow B=(0,H), tip C=(L,H) loaded. Its rigid elbow transmits moment.",
     "Both are specific determinate examples, not general truss/frame solvers. A negative roller reaction requires hold-down rather than unilateral contact."])

if __name__ == "__main__":
    run_cli(solve, __file__)
