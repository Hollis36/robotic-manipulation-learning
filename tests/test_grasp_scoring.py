import numpy as np

from rml.grasp_scoring import score_antipodal_grasps


def test_score_antipodal_grasps_prefers_candidate_with_balanced_contacts():
    points = np.array(
        [
            [-0.5, 0.02],
            [-0.48, -0.02],
            [0.5, 0.01],
            [0.52, -0.01],
            [0.0, 0.6],
        ]
    )
    candidates = [
        {"name": "off_center", "center": [0.0, 0.4], "angle": 0.0, "width": 1.0},
        {"name": "balanced", "center": [0.0, 0.0], "angle": 0.0, "width": 1.0},
        {"name": "too_narrow", "center": [0.0, 0.0], "angle": 0.0, "width": 0.4},
    ]

    ranked = score_antipodal_grasps(points, candidates)

    assert ranked[0].name == "balanced"
    assert ranked[0].score > ranked[-1].score
    assert ranked[0].left_contacts == 2
    assert ranked[0].right_contacts == 2

