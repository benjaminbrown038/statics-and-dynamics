"""Read the adjacent lesson, edit a case JSON, then run this file."""
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from sdlib.common import inputs, linspace, table, result, run_cli
from sdlib.motion import smooth_move, motion_times, trapezoid, rk4_step


def exact_state(t,x0,v0,wn,zeta):
    decay=zeta*wn
    wd=wn*math.sqrt(1-zeta*zeta)
    B=(v0+decay*x0)/wd
    co,si=math.cos(wd*t),math.sin(wd*t)
    envelope=math.exp(-decay*t)
    x=envelope*(x0*co+B*si)
    v=envelope*((-decay*x0+B*wd)*co+(-decay*B-x0*wd)*si)
    return x,v


def solve(case):
    """Integrate free damped vibration and compare every time step with an exact solution."""
    c=inputs(case,positive=("mass_kg","stiffness_N_per_m","duration_s","time_step_s"),
             nonnegative=("damping_ratio",),finite=("initial_displacement_m","initial_velocity_m_per_s"))
    m,k,T,dt,zeta,x0,v0=(c[key] for key in ("mass_kg","stiffness_N_per_m","duration_s","time_step_s","damping_ratio","initial_displacement_m","initial_velocity_m_per_s"))
    if zeta>=1: raise ValueError("this introductory exact comparison requires 0 <= damping_ratio < 1")
    wn=math.sqrt(k/m)
    damping=2*zeta*math.sqrt(k*m)
    if dt*wn>0.2: raise ValueError("reduce time_step_s so omega_n * time_step_s <= 0.2")
    steps=math.ceil(T/dt)
    if steps>200000: raise ValueError("requested more than 200000 steps; reduce duration or increase a suitably small time step")
    h=T/steps
    def derivative(t,state):
        x,v=state
        return [v,(-damping*v-k*x)/m]
    state=[x0,v0]
    rows=[]
    for i in range(steps+1):
        t=i*h
        x,v=state
        xe,ve=exact_state(t,x0,v0,wn,zeta)
        rows.append(dict(time_s=t,numerical_displacement_mm=x*1000,exact_displacement_mm=xe*1000,
                         velocity_m_per_s=v,mount_load_N=k*x+damping*v,energy_J=m*v*v/2+k*x*x/2,
                         damping_power_W=damping*v*v))
        if i<steps: state=rk4_step(derivative,t,state,h)
    dissipated=trapezoid([r["time_s"] for r in rows],[r["damping_power_W"] for r in rows])
    return result("Tier 9: vibration and numerical verification",{
        "natural_frequency_rad_per_s":wn,"natural_frequency_Hz":wn/(2*math.pi),
        "damped_frequency_rad_per_s":wn*math.sqrt(1-zeta*zeta),"damping_Ns_per_m":damping,
        "actual_time_step_s":h,"integration_steps":steps,
        "maximum_displacement_error_mm":max(abs(r["numerical_displacement_mm"]-r["exact_displacement_mm"]) for r in rows),
        "initial_energy_J":rows[0]["energy_J"],"final_energy_J":rows[-1]["energy_J"],
        "integrated_damping_loss_J":dissipated,"energy_balance_residual_J":rows[-1]["energy_J"]+dissipated-rows[0]["energy_J"],
        "sampled_peak_mount_load_N":max(abs(r["mount_load_N"]) for r in rows),
    },[table("vibration",rows,"time_s",["numerical_displacement_mm","exact_displacement_mm"],"Time (s)","Displacement from equilibrium (mm)"),
       table("vibration_energy",rows,"time_s",["energy_J"],"Time (s)","Mechanical energy (J)")],
    ["One translational degree of freedom, linear spring, viscous damping, fixed base, and no external forcing.",
     "Displacement is measured from static equilibrium; the CSV load is the dynamic increment on the mount, excluding any gravity preload.",
     "RK4 error and damping-loss quadrature error are separate numerical effects. Refine the time step to check both."])

if __name__ == "__main__":
    run_cli(solve, __file__)
