from rml.gridworld import GridGraspWorld


def test_gridworld_moves_and_rewards_successful_grasp():
    env = GridGraspWorld(width=4, height=4, object_pos=(1, 0), start_pos=(0, 0))

    state = env.reset()
    assert state.agent_pos == (0, 0)
    assert not state.holding_object

    state, reward, done, info = env.step("right")
    assert state.agent_pos == (1, 0)
    assert reward == -0.01
    assert not done
    assert info["event"] == "move"

    state, reward, done, info = env.step("grasp")
    assert state.holding_object
    assert reward == 1.0
    assert done
    assert info["event"] == "grasp_success"


def test_gridworld_blocks_motion_at_boundary():
    env = GridGraspWorld(width=3, height=3, object_pos=(2, 2), start_pos=(0, 0))
    env.reset()

    state, reward, done, info = env.step("left")

    assert state.agent_pos == (0, 0)
    assert reward == -0.05
    assert not done
    assert info["event"] == "blocked"

