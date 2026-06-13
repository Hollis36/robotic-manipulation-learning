from rml.control import simulate_pd_mass


def test_simulate_pd_mass_converges_to_target():
    trace = simulate_pd_mass(x0=0.0, v0=0.0, target=1.0, kp=25.0, kd=10.0, dt=0.01, steps=500)

    assert abs(trace.positions[-1] - 1.0) < 1e-3
    assert abs(trace.velocities[-1]) < 1e-3
    assert trace.times[-1] == 5.0

