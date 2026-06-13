"""A tiny RL-style manipulation environment."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GridState:
    agent_pos: tuple[int, int]
    holding_object: bool


class GridGraspWorld:
    """Gridworld where an agent moves to an object and executes grasp."""

    _ACTIONS = {
        "up": (0, 1),
        "down": (0, -1),
        "left": (-1, 0),
        "right": (1, 0),
    }

    def __init__(
        self,
        width: int = 5,
        height: int = 5,
        object_pos: tuple[int, int] = (2, 2),
        start_pos: tuple[int, int] = (0, 0),
    ) -> None:
        if width <= 0 or height <= 0:
            raise ValueError("width and height must be positive")
        self.width = width
        self.height = height
        self.object_pos = object_pos
        self.start_pos = start_pos
        self._validate_position(object_pos)
        self._validate_position(start_pos)
        self._state = GridState(agent_pos=start_pos, holding_object=False)

    def _validate_position(self, pos: tuple[int, int]) -> None:
        x, y = pos
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise ValueError("position outside grid")

    def reset(self) -> GridState:
        self._state = GridState(agent_pos=self.start_pos, holding_object=False)
        return self._state

    def step(self, action: str) -> tuple[GridState, float, bool, dict]:
        if action == "grasp":
            if self._state.agent_pos == self.object_pos:
                self._state = GridState(agent_pos=self._state.agent_pos, holding_object=True)
                return self._state, 1.0, True, {"event": "grasp_success"}
            return self._state, -0.2, False, {"event": "grasp_failed"}

        if action not in self._ACTIONS:
            raise ValueError(f"unknown action: {action}")

        dx, dy = self._ACTIONS[action]
        x, y = self._state.agent_pos
        new_pos = (x + dx, y + dy)
        if not (0 <= new_pos[0] < self.width and 0 <= new_pos[1] < self.height):
            return self._state, -0.05, False, {"event": "blocked"}

        self._state = GridState(agent_pos=new_pos, holding_object=self._state.holding_object)
        return self._state, -0.01, False, {"event": "move"}

