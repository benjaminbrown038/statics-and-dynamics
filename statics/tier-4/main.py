"""Read the adjacent lesson, edit a case JSON, then run this file."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from sdlib.common import inputs, linspace, table, result, run_cli
from sdlib.motion import smooth_move, motion_times, trapezoid, rk4_step


def solve(case):
    """Find centroid and mass moments of inertia of a uniform L-shaped plate."""
    c=inputs(case,positive=("horizontal_length_m","vertical_length_m","leg_width_m","thickness_m","density_kg_per_m3"))
    L,H,w,t,rho=(c[k] for k in ("horizontal_length_m","vertical_length_m","leg_width_m","thickness_m","density_kg_per_m3"))
    if w>=min(L,H): raise ValueError("leg_width_m must be smaller than both leg lengths")
    # Non-overlapping rectangles: vertical leg, then horizontal leg beyond it.
    pieces=[(w,H,w/2,H/2),(L-w,w,(L+w)/2,w/2)]
    areas=[b*h for b,h,_,_ in pieces]
    A=sum(areas)
    xG=sum(a*p[2] for a,p in zip(areas,pieces))/A
    yG=sum(a*p[3] for a,p in zip(areas,pieces))/A
    masses=[rho*t*a for a in areas]
    mass=sum(masses)
    Ix=sum(b*h**3/12+a*(y-yG)**2 for a,(b,h,x,y) in zip(areas,pieces))
    Iy=sum(h*b**3/12+a*(x-xG)**2 for a,(b,h,x,y) in zip(areas,pieces))
    IG=sum(m*((b*b+h*h)/12+(x-xG)**2+(y-yG)**2) for m,(b,h,x,y) in zip(masses,pieces))
    IO=IG+mass*(xG*xG+yG*yG)
    rows=[dict(axis_offset_m=d,mass_inertia_kg_m2=IG+mass*d*d) for d in linspace(0,max(L,H))]
    return result("Tier 4: centroids and mass moment of inertia",{
        "area_m2":A,"mass_kg":mass,"centroid_x_m":xG,"centroid_y_m":yG,
        "mass_inertia_about_centroid_z_kg_m2":IG,"mass_inertia_about_origin_z_kg_m2":IO,
        "area_second_moment_x_m4":Ix,"area_second_moment_y_m4":Iy,
    },[table("parallel_axis",rows,"axis_offset_m",["mass_inertia_kg_m2"],"Distance from centroidal z axis (m)","Mass moment of inertia (kg m²)")],
    ["The L plate occupies the union of [0,w]x[0,H] and [0,L]x[0,w]; the shared corner is counted once.",
     "The z axis is normal to the plate. Uniform density and thickness make the area and mass centroids coincide.",
     "Mass inertia has units kg m²; section area moments have units m⁴. They serve different equations."])

if __name__ == "__main__":
    run_cli(solve, __file__)
