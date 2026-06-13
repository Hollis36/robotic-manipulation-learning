# Drake And pydrake Setup Guide

This repository does not require Drake for the first concept pass. Drake should enter after the core stack is clear.

## Why Drake Matters Here

Drake is the course's main software toolchain. It supports multibody modeling, systems composition, optimization, simulation, and Python bindings. In this repository, Drake labs should be optional extensions of NumPy concept cases, not prerequisites for reading the notes.

## Recommended Setup Order

1. Run the current repository tests:

```bash
pytest -q
```

2. Read the official Drake tutorials page:

<https://drake.mit.edu/tutorials/>

3. Check pydrake availability:

```bash
python - <<'PY'
try:
    import pydrake
    print("pydrake available")
except Exception as exc:
    print(f"pydrake unavailable: {exc}")
PY
```

4. If installed, launch local tutorials:

```bash
python3 -m pydrake.tutorials
```

5. Keep Drake labs guarded:

```python
import pytest

pydrake = pytest.importorskip("pydrake")
```

## First Drake Lab Targets

| Lab | Goal | Depends On |
| --- | --- | --- |
| `ch02_robot_setup/drake_labs/model_loading` | Load a simple model and inspect names | Chapter 2 |
| `ch03_basic_pick_and_place/drake_labs/frame_inspection` | Print frames and transforms | Chapter 3 |
| `ch03_basic_pick_and_place/drake_labs/basic_ik` | Solve a simple IK target | Chapter 3 |
| `ch04_geometric_pose_estimation/drake_labs/point_cloud` | Generate or inspect a point cloud | Chapter 4 |
| `ch07_motion_planning/drake_labs/planning_intro` | Compare a planned path with a scripted path | Chapter 7 |

## Environment Notes

- Keep concept examples independent of Drake.
- Do not commit downloaded model caches or generated heavy files.
- Document exact commands when a Drake lab is added.
- Prefer small smoke tests that skip cleanly when pydrake is unavailable.

