"""Read the adjacent lesson, edit a case JSON, then run this file."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from sdlib.common import inputs, linspace, table, result, run_cli
from sdlib.motion import smooth_move, motion_times, trapezoid, rk4_step


def solve(case):
    """Compute dynamic actuator force and pivot loads for a rotating door-arm model."""
    c=inputs(case,positive=("rod_mass_kg","rod_length_m","attachment_radius_m","duration_s"),
             nonnegative=("payload_mass_kg","gravity_m_per_s2"),finite=("anchor_x_m","anchor_y_m","start_angle_deg","end_angle_deg"))
    m,mp,L,r,T,g=(c[k] for k in ("rod_mass_kg","payload_mass_kg","rod_length_m","attachment_radius_m","duration_s","gravity_m_per_s2"))
    if r>L: raise ValueError("attachment_radius_m must not exceed rod_length_m")
    ax,ay=c["anchor_x_m"],c["anchor_y_m"]
    if math.hypot(ax,ay)==0: raise ValueError("an anchor at the pivot has no moment arm")
    start,end=math.radians(c["start_angle_deg"]),math.radians(c["end_angle_deg"])
    if abs(end-start)>2*math.pi: raise ValueError("this example allows at most one revolution per move")
    # Check the continuous angular interval for collinearity, not just sampled times.
    base=math.atan2(ay,ax)
    lo,hi=min(start,end),max(start,end)
    crossing=base+math.ceil((lo-base)/math.pi)*math.pi
    if crossing<=hi+1e-12: raise ValueError("motion includes zero actuator moment arm (collinear anchor, attachment, pivot)")
    mass=m+mp
    first_moment=m*L/2+mp*L
    rG=first_moment/mass
    IO=m*L*L/3+mp*L*L
    rows=[]
    for t in motion_times(T):
        theta,omega,alpha=smooth_move(t,T,start,end)
        co,si=math.cos(theta),math.sin(theta)
        bx,by=r*co,r*si
        length=math.hypot(ax-bx,ay-by)
        if length<1e-12: raise ValueError("actuator endpoints coincide")
        ux,uy=(ax-bx)/length,(ay-by)/length
        h=bx*uy-by*ux
        if abs(h)<1e-10: raise ValueError("actuator moment arm is too small for this model")
        gravity_moment=g*first_moment*co
        force=(IO*alpha+gravity_moment)/h
        static_force=gravity_moment/h
        gx=rG*(-alpha*si-omega*omega*co)
        gy=rG*(alpha*co-omega*omega*si)
        Rx=mass*gx-force*ux
        Ry=mass*gy-force*uy+mass*g
        rows.append(dict(time_s=t,angle_deg=math.degrees(theta),omega_rad_per_s=omega,alpha_rad_per_s2=alpha,
                         actuator_length_m=length,moment_arm_m=h,actuator_force_N=force,quasistatic_force_N=static_force,
                         pivot_load_on_mount_x_N=-Rx,pivot_load_on_mount_y_N=-Ry,
                         fixed_anchor_load_on_mount_x_N=-force*ux,fixed_anchor_load_on_mount_y_N=-force*uy,
                         center_acceleration_x_m_per_s2=gx,center_acceleration_y_m_per_s2=gy))
    return result("Tier 7: rigid-body dynamics of an actuated arm",{
        "mass_inertia_about_pivot_kg_m2":IO,"center_of_mass_radius_m":rG,
        "sampled_peak_actuator_force_magnitude_N":max(abs(row["actuator_force_N"]) for row in rows),
        "sampled_peak_quasistatic_force_magnitude_N":max(abs(row["quasistatic_force_N"]) for row in rows),
        "sampled_peak_pivot_load_magnitude_N":max(math.hypot(row["pivot_load_on_mount_x_N"],row["pivot_load_on_mount_y_N"]) for row in rows),
        "sampled_max_dynamic_force_increment_N":max(abs(row["actuator_force_N"]-row["quasistatic_force_N"]) for row in rows),
    },[table("interface_loads",rows,"time_s",["actuator_force_N","quasistatic_force_N"],"Time (s)","Actuator force, tension positive (N)"),
       table("pivot_loads",rows,"time_s",["pivot_load_on_mount_x_N","pivot_load_on_mount_y_N"],"Time (s)","Force applied to pivot mount (N)")],
    ["The moving body is a uniform rigid rod plus a point payload at its tip. Gravity acts vertically downward.",
     "The massless actuator can push and pull; positive force pulls the arm attachment toward the fixed anchor.",
     "CSV includes equal-and-opposite loads on the stationary pivot and actuator anchor, with global x right and y up.",
     "Peak force and pivot load are sampled, not guaranteed continuous extrema. Joint friction, backlash, flexibility, and actuator mass are omitted."])

if __name__ == "__main__":
    run_cli(solve, __file__)
