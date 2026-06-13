from rml.gridworld import GridGraspWorld


def main() -> None:
    env = GridGraspWorld(width=4, height=4, object_pos=(1, 0), start_pos=(0, 0))
    state = env.reset()
    print("case=009_rl_grasping_gridworld")
    print(f"reset={state}")

    for action in ["right", "grasp"]:
        state, reward, done, info = env.step(action)
        print(f"action={action} state={state} reward={reward:.2f} done={done} event={info['event']}")


if __name__ == "__main__":
    main()

