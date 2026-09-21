"""Benchmarks, limiting cases, conservation, and convergence checks."""
import json
import math
from pathlib import Path
import runpy
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from sdlib.motion import smooth_move


def load(n):
    group="fundamentals" if n==0 else "statics" if n<=4 else "dynamics"
    path=ROOT/group/f"tier-{n}"
    return runpy.run_path(str(path/"main.py")),json.loads((path/"cases/baseline.json").read_text())


class PhysicsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tiers=[load(n) for n in range(10)]

    def data(self,n,**changes):
        module,case=self.tiers[n]
        return module["solve"](dict(case,**changes))

    def metrics(self,n,**changes):
        return self.data(n,**changes)["metrics"]

    def test_force_couple_benchmark(self):
        m=self.metrics(0)
        self.assertEqual(m["resultant_x_N"],300)
        self.assertEqual(m["resultant_y_N"],-800)
        self.assertEqual(m["total_moment_about_origin_Nm"],-100)

    def test_moment_translation_and_pure_couple(self):
        a=self.metrics(0)
        b=self.metrics(0,x1_m=1.12,x2_m=1)
        self.assertAlmostEqual(b["total_moment_about_origin_Nm"]-a["total_moment_about_origin_Nm"],-800)
        couple=self.data(0,F1x_N=0,F1y_N=0,F2x_N=0,F2y_N=0)
        self.assertTrue(all(row["moment_about_reference_Nm"]==20 for row in couple["tables"][0]["rows"]))
        self.assertIn("undefined",couple["metrics"]["resultant_angle_deg"])

    def test_beam_benchmark_and_uniform_load_limit(self):
        m=self.metrics(1)
        self.assertEqual((m["reaction_A_N"],m["reaction_B_N"],m["maximum_moment_magnitude_Nm"]),(700,500,264))
        uniform=self.metrics(1,length_m=2,point_load_N=0,uniform_load_N_per_m=100)
        self.assertEqual(uniform["reaction_A_N"],100)
        self.assertEqual(uniform["maximum_moment_magnitude_Nm"],50)
        self.assertEqual(uniform["maximum_moment_position_m"],1)

    def test_beam_equilibrium_and_end_moments(self):
        for a in (0,0.3,0.8,1):
            data=self.data(1,point_position_m=a)
            self.assertAlmostEqual(data["metrics"]["force_residual_N"],0)
            self.assertAlmostEqual(data["metrics"]["moment_residual_Nm"],0)
            rows=data["tables"][0]["rows"]
            self.assertAlmostEqual(rows[0]["moment_Nm"],0)
            self.assertAlmostEqual(rows[-1]["moment_Nm"],0)

    def test_truss_known_solution_and_joint_balance(self):
        m=self.metrics(2)
        self.assertEqual(m["truss_AB_N"],500)
        self.assertAlmostEqual(m["truss_AC_N"],-500*math.sqrt(2))
        for Fx,Fy in ((500,-800),(-250,-1000),(100,200),(0,0)):
            self.assertLess(self.metrics(2,load_x_N=Fx,load_y_N=Fy)["maximum_joint_residual_N"],1e-10)

    def test_frame_reaction_moment_includes_both_components(self):
        m=self.metrics(2,load_x_N=300,load_y_N=-1000)
        self.assertEqual(m["frame_root_Rx_N"],-300)
        self.assertEqual(m["frame_root_reaction_moment_Nm"],2300)
        self.assertEqual(m["frame_elbow_cut_moment_on_horizontal_member_Nm"],2000)

    def test_static_friction_adjusts_below_limit(self):
        m=self.metrics(3,mu_static=0.5)
        self.assertEqual(m["state"],"sticking")
        self.assertEqual(m["downslope_acceleration_m_per_s2"],0)
        self.assertLess(abs(m["actual_friction_N"]),m["static_friction_limit_N"])

    def test_sliding_friction_opposes_motion(self):
        downhill=self.metrics(3)
        uphill=self.metrics(3,applied_downslope_N=-100)
        self.assertGreater(downhill["downslope_acceleration_m_per_s2"],0)
        self.assertLess(downhill["actual_friction_N"],0)
        self.assertLess(uphill["downslope_acceleration_m_per_s2"],0)
        self.assertGreater(uphill["actual_friction_N"],0)
        level=self.metrics(3,incline_deg=0,applied_downslope_N=0)
        self.assertEqual(level["actual_friction_N"],0)

    def test_mass_inertia_against_rectangle_subtraction(self):
        # Independent origin integral: full vertical + full horizontal - overlap.
        L,H,w,t,rho=0.16,0.12,0.02,0.006,2700
        def origin_rect(b,h): return rho*t*b*h*(b*b+h*h)/3
        expected=origin_rect(w,H)+origin_rect(L,w)-origin_rect(w,w)
        m=self.metrics(4)
        self.assertAlmostEqual(m["mass_inertia_about_origin_z_kg_m2"],expected,places=13)
        self.assertAlmostEqual(m["mass_kg"],rho*t*(w*H+w*L-w*w))

    def test_density_changes_mass_not_geometry(self):
        a,b=self.metrics(4),self.metrics(4,density_kg_per_m3=5400)
        self.assertEqual(a["centroid_x_m"],b["centroid_x_m"])
        self.assertEqual(a["area_second_moment_x_m4"],b["area_second_moment_x_m4"])
        self.assertAlmostEqual(b["mass_inertia_about_centroid_z_kg_m2"]/a["mass_inertia_about_centroid_z_kg_m2"],2)
        symmetric=self.metrics(4,horizontal_length_m=0.12)
        self.assertAlmostEqual(symmetric["centroid_x_m"],symmetric["centroid_y_m"])

    def test_motion_endpoints_and_derivatives(self):
        self.assertEqual(smooth_move(0,1,0,0.5),(0,0,0))
        self.assertEqual(smooth_move(1,1,0,0.5),(0.5,0,0))
        t,h=0.37,1e-5
        left=smooth_move(t-h,1,0,0.5)
        right=smooth_move(t+h,1,0,0.5)
        middle=smooth_move(t,1,0,0.5)
        self.assertAlmostEqual((right[0]-left[0])/(2*h),middle[1],places=8)
        self.assertAlmostEqual((right[1]-left[1])/(2*h),middle[2],places=8)

    def test_motion_duration_scaling(self):
        a,b=self.metrics(5),self.metrics(5,duration_s=0.5)
        self.assertEqual(b["peak_speed_m_per_s"],2*a["peak_speed_m_per_s"])
        self.assertEqual(b["peak_acceleration_m_per_s2"],4*a["peak_acceleration_m_per_s2"])

    def test_lift_newton_and_work_energy(self):
        data=self.data(6)
        for row in data["tables"][0]["rows"]:
            self.assertAlmostEqual(row["cable_tension_N"]-98.1,10*row["acceleration_m_per_s2"],places=10)
        self.assertAlmostEqual(data["metrics"]["exact_total_lifting_work_J"],49.05)
        self.assertLess(abs(data["metrics"]["work_integration_residual_J"]),1e-5)
        slow=self.metrics(6,duration_s=10)
        self.assertAlmostEqual((data["metrics"]["peak_cable_tension_N"]-98.1)/(slow["peak_cable_tension_N"]-98.1),100)

    def test_cable_cannot_push(self):
        with self.assertRaisesRegex(ValueError,"negative cable tension"):
            self.data(6,duration_s=0.4)

    def test_arm_mass_properties_and_stationary_limit(self):
        data=self.data(7,start_angle_deg=30,end_angle_deg=30)
        self.assertAlmostEqual(data["metrics"]["mass_inertia_about_pivot_kg_m2"],0.105)
        for row in data["tables"][0]["rows"]:
            self.assertAlmostEqual(row["actuator_force_N"],row["quasistatic_force_N"])
            self.assertEqual(row["center_acceleration_x_m_per_s2"],0)

    def test_arm_mount_loads_balance_inertia_and_weight(self):
        data=self.data(7)
        for row in data["tables"][0]["rows"]:
            x=row["pivot_load_on_mount_x_N"]+row["fixed_anchor_load_on_mount_x_N"]
            y=row["pivot_load_on_mount_y_N"]+row["fixed_anchor_load_on_mount_y_N"]
            self.assertAlmostEqual(x,-2.5*row["center_acceleration_x_m_per_s2"],places=10)
            self.assertAlmostEqual(y,-2.5*(row["center_acceleration_y_m_per_s2"]+9.81),places=10)
            # Stationary-interface moment is opposite the moment driving the moving assembly.
            moment=-0.1*row["fixed_anchor_load_on_mount_y_N"]-0.08*row["fixed_anchor_load_on_mount_x_N"]
            expected=-(0.105*row["alpha_rad_per_s2"]+9.81*0.45*math.cos(math.radians(row["angle_deg"])))
            self.assertAlmostEqual(moment,expected,places=10)

    def test_arm_dynamic_increment_scales_with_inverse_time_squared(self):
        a,b=self.data(7),self.data(7,duration_s=12)
        for rowa,rowb in zip(a["tables"][0]["rows"],b["tables"][0]["rows"]):
            da=rowa["actuator_force_N"]-rowa["quasistatic_force_N"]
            db=rowb["actuator_force_N"]-rowb["quasistatic_force_N"]
            self.assertAlmostEqual(da,100*db,places=8)

    def test_arm_zero_gravity_has_only_inertial_actuator_force(self):
        data=self.data(7,gravity_m_per_s2=0)
        for row in data["tables"][0]["rows"]:
            self.assertEqual(row["quasistatic_force_N"],0)
            self.assertAlmostEqual(row["actuator_force_N"]*row["moment_arm_m"],0.105*row["alpha_rad_per_s2"])

    def test_arm_continuous_singularity_is_rejected(self):
        with self.assertRaisesRegex(ValueError,"collinear"):
            self.data(7,anchor_x_m=0.1,anchor_y_m=0.08)

    def test_stopping_impulse_work_and_peak(self):
        data=self.data(8)
        m=data["metrics"]
        self.assertAlmostEqual(m["peak_stop_load_N"],200*math.pi)
        self.assertEqual(m["exact_impulse_on_mass_Ns"],-40)
        self.assertEqual(m["stop_distance_m"],0.1)
        self.assertLess(abs(m["impulse_integration_residual_Ns"]),0.001)
        self.assertLess(abs(m["work_integration_residual_J"]),0.001)
        self.assertAlmostEqual(data["tables"][0]["rows"][-1]["velocity_m_per_s"],0)

    def test_stop_duration_changes_peak_not_energy(self):
        a,b=self.metrics(8),self.metrics(8,stop_duration_s=0.05)
        self.assertEqual(b["peak_stop_load_N"],2*a["peak_stop_load_N"])
        self.assertEqual(b["stop_distance_m"],a["stop_distance_m"]/2)
        self.assertEqual(a["initial_kinetic_energy_J"],b["initial_kinetic_energy_J"])

    def test_vibration_rk4_converges_at_fourth_order(self):
        a=self.metrics(9,time_step_s=0.004)["maximum_displacement_error_mm"]
        b=self.metrics(9,time_step_s=0.002)["maximum_displacement_error_mm"]
        self.assertTrue(15<a/b<17,a/b)

    def test_undamped_energy_and_zero_state(self):
        m=self.metrics(9,damping_ratio=0)
        self.assertLess(abs(m["initial_energy_J"]-m["final_energy_J"]),2e-8)
        zero=self.metrics(9,initial_displacement_m=0,initial_velocity_m_per_s=0)
        self.assertEqual(zero["maximum_displacement_error_mm"],0)
        self.assertEqual(zero["sampled_peak_mount_load_N"],0)

    def test_damping_energy_and_frequency_scaling(self):
        a,b=self.metrics(9),self.metrics(9,stiffness_N_per_m=16000)
        self.assertEqual(b["natural_frequency_Hz"],2*a["natural_frequency_Hz"])
        self.assertLess(a["final_energy_J"],a["initial_energy_J"])
        self.assertLess(abs(a["energy_balance_residual_J"]),1e-6)

    def test_invalid_inputs_and_json_finiteness(self):
        invalid=[(0,dict(F1x_N=float("inf"))),(1,dict(point_position_m=2)),(2,dict(height_m=0)),
                 (3,dict(mu_kinetic=0.6)),(3,dict(incline_deg=90)),(4,dict(leg_width_m=0.2)),
                 (5,dict(duration_s=True)),(7,dict(attachment_radius_m=0.4)),
                 (8,dict(stop_duration_s=0)),(9,dict(damping_ratio=1)),(9,dict(time_step_s=0.1))]
        for n,change in invalid:
            with self.subTest(tier=n):
                with self.assertRaises(ValueError): self.data(n,**change)
        for n in range(10): json.dumps(self.data(n),allow_nan=False)
        with self.assertRaises(ValueError): self.data(4,misspelled_key=1)


if __name__=="__main__": unittest.main()
