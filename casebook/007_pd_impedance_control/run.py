import numpy as np

from rml.control import simulate_pd_mass


def main() -> None:
    trace = simulate_pd_mass(x0=0.0, v0=0.0, target=1.0, kp=25.0, kd=10.0, dt=0.01, steps=500)

    print("case=007_pd_impedance_control")
    print(f"final_position={trace.positions[-1]:.6f}")
    print(f"final_velocity={trace.velocities[-1]:.6f}")
    print(f"max_control={np.max(np.abs(trace.controls)):.3f}")


if __name__ == "__main__":
    main()

