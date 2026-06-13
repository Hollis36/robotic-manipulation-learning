"""Generate polished visual assets for the Jupyter Book pages."""

from __future__ import annotations

from pathlib import Path
import sys

import matplotlib

matplotlib.use("Agg")

from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch, Polygon, Rectangle
import matplotlib.pyplot as plt
import numpy as np


BOOK_FIGURE_DIR = Path(__file__).resolve().parents[1] / "book" / "assets" / "figures"

PALETTE = {
    "paper": "#F5F7FA",
    "ink": "#1E2633",
    "muted": "#6A7280",
    "grid": "#D8DEE8",
    "blue": "#2B6CB0",
    "sky": "#63B3ED",
    "teal": "#2C7A7B",
    "green": "#2F855A",
    "amber": "#D69E2E",
    "red": "#C05621",
    "violet": "#6B46C1",
    "white": "#FFFFFF",
}


def _save(fig: plt.Figure, output_dir: Path, name: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{name}.png"
    fig.savefig(path, dpi=170, facecolor=fig.get_facecolor(), bbox_inches="tight", pad_inches=0.18)
    plt.close(fig)
    return path


def _canvas(title: str, subtitle: str) -> tuple[plt.Figure, plt.Axes]:
    fig, ax = plt.subplots(figsize=(12.8, 7.2))
    fig.patch.set_facecolor(PALETTE["paper"])
    ax.set_facecolor(PALETTE["paper"])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    for x in np.linspace(0.05, 0.95, 10):
        ax.plot([x, x], [0.08, 0.92], color=PALETTE["grid"], lw=0.6, alpha=0.35, zorder=0)
    for y in np.linspace(0.12, 0.86, 7):
        ax.plot([0.05, 0.95], [y, y], color=PALETTE["grid"], lw=0.6, alpha=0.35, zorder=0)

    ax.text(0.055, 0.925, "ROBOTIC MANIPULATION", color=PALETTE["muted"], fontsize=9, weight="bold")
    ax.text(0.055, 0.86, title, color=PALETTE["ink"], fontsize=24, weight="bold")
    ax.text(0.057, 0.815, subtitle, color=PALETTE["muted"], fontsize=11)
    ax.plot([0.055, 0.25], [0.795, 0.795], color=PALETTE["blue"], lw=3, solid_capstyle="round")
    ax.plot([0.255, 0.34], [0.795, 0.795], color=PALETTE["amber"], lw=3, solid_capstyle="round")
    return fig, ax


def _label(ax: plt.Axes, x: float, y: float, text: str, color: str = "ink", size: int = 9) -> None:
    ax.text(x, y, text, ha="center", va="center", color=PALETTE[color], fontsize=size, weight="bold")


def _node(ax: plt.Axes, x: float, y: float, w: float, h: float, text: str, color: str) -> None:
    ax.add_patch(
        FancyBboxPatch(
            (x - w / 2, y - h / 2),
            w,
            h,
            boxstyle="round,pad=0.012,rounding_size=0.018",
            fc=PALETTE["white"],
            ec=PALETTE[color],
            lw=2.0,
            alpha=0.98,
        )
    )
    _label(ax, x, y, text, color="ink", size=8)


def _arrow(ax: plt.Axes, start: tuple[float, float], end: tuple[float, float], color: str = "blue", lw: float = 2.0) -> None:
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=14,
            lw=lw,
            color=PALETTE[color],
            shrinkA=6,
            shrinkB=6,
            connectionstyle="arc3,rad=0.0",
        )
    )


def _curved_arrow(
    ax: plt.Axes,
    start: tuple[float, float],
    end: tuple[float, float],
    color: str = "blue",
    rad: float = 0.2,
) -> None:
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=14,
            lw=2.0,
            color=PALETTE[color],
            shrinkA=4,
            shrinkB=4,
            connectionstyle=f"arc3,rad={rad}",
        )
    )


def _draw_arm(ax: plt.Axes, base: tuple[float, float], angles: list[float], lengths: list[float], color: str = "blue") -> np.ndarray:
    points = [np.array(base, dtype=float)]
    angle = 0.0
    current = np.array(base, dtype=float)
    for delta, length in zip(angles, lengths):
        angle += delta
        current = current + length * np.array([np.cos(angle), np.sin(angle)])
        points.append(current.copy())
    pts = np.vstack(points)
    ax.plot(pts[:, 0], pts[:, 1], "-o", color=PALETTE[color], lw=5, markersize=9, solid_capstyle="round")
    ax.add_patch(Circle(base, 0.035, fc=PALETTE["white"], ec=PALETTE["ink"], lw=1.5))
    return pts


def _draw_frame(ax: plt.Axes, origin: tuple[float, float], angle: float, label: str, scale: float = 0.08) -> None:
    ox, oy = origin
    x_axis = np.array([np.cos(angle), np.sin(angle)]) * scale
    y_axis = np.array([-np.sin(angle), np.cos(angle)]) * scale
    ax.arrow(ox, oy, x_axis[0], x_axis[1], color=PALETTE["blue"], width=0.004, head_width=0.018)
    ax.arrow(ox, oy, y_axis[0], y_axis[1], color=PALETTE["red"], width=0.004, head_width=0.018)
    ax.text(ox + 0.015, oy + 0.018, label, fontsize=8, color=PALETTE["ink"], weight="bold")


def figure_intro(output_dir: Path) -> Path:
    fig, ax = _canvas("Learning Atlas", "from task intent to controlled contact")
    center = (0.5, 0.47)
    ax.add_patch(Circle(center, 0.11, fc=PALETTE["white"], ec=PALETTE["ink"], lw=2.2))
    _label(ax, *center, "MANIPULATION", size=10)
    labels = [
        ("setup", 0.24, 0.61, "blue"),
        ("frames", 0.38, 0.68, "teal"),
        ("perception", 0.62, 0.68, "green"),
        ("grasp", 0.76, 0.61, "red"),
        ("planning", 0.72, 0.34, "violet"),
        ("control", 0.5, 0.25, "amber"),
        ("learning", 0.28, 0.34, "blue"),
    ]
    for text, x, y, color in labels:
        ax.add_patch(Circle((x, y), 0.062, fc=PALETTE["white"], ec=PALETTE[color], lw=2.2))
        _label(ax, x, y, text, size=8)
        _curved_arrow(ax, center, (x, y), color=color, rad=0.12)
    for (_, x0, y0, c0), (_, x1, y1, _) in zip(labels, labels[1:] + labels[:1]):
        _curved_arrow(ax, (x0, y0), (x1, y1), color=c0, rad=0.16)
    return _save(fig, output_dir, "intro")


def figure_stack(output_dir: Path) -> Path:
    fig, ax = _canvas("Manipulation Stack", "a closed loop, not a single trick")
    layers = [
        ("task goal", "amber"),
        ("sensors", "teal"),
        ("state", "green"),
        ("geometry", "blue"),
        ("grasp", "red"),
        ("planning", "violet"),
        ("control", "amber"),
    ]
    x = 0.5
    ys = np.linspace(0.72, 0.24, len(layers))
    for (text, color), y in zip(layers, ys):
        _node(ax, x, y, 0.23, 0.052, text, color)
    for y0, y1 in zip(ys[:-1], ys[1:]):
        _arrow(ax, (x, y0 - 0.03), (x, y1 + 0.03), color="blue")
    _curved_arrow(ax, (0.63, 0.25), (0.63, 0.71), color="red", rad=-0.45)
    ax.text(0.69, 0.49, "feedback", color=PALETTE["red"], fontsize=10, weight="bold", rotation=90)
    return _save(fig, output_dir, "00_manipulation_stack")


def figure_robot_setup(output_dir: Path) -> Path:
    fig, ax = _canvas("Robot Setup", "model, sensors, scene, and command interface")
    _draw_arm(ax, (0.34, 0.25), [1.15, -0.75, 0.55], [0.18, 0.16, 0.12], "blue")
    ax.add_patch(Rectangle((0.22, 0.19), 0.24, 0.035, fc=PALETTE["ink"], ec="none", alpha=0.9))
    ax.add_patch(Circle((0.69, 0.32), 0.045, fc=PALETTE["amber"], ec=PALETTE["ink"], lw=1.3))
    ax.add_patch(Polygon([[0.72, 0.66], [0.61, 0.41], [0.78, 0.41]], fc=PALETTE["teal"], alpha=0.16, ec=PALETTE["teal"], lw=1.5))
    ax.add_patch(Rectangle((0.68, 0.66), 0.08, 0.045, fc=PALETTE["white"], ec=PALETTE["teal"], lw=2))
    _draw_frame(ax, (0.34, 0.25), 0.0, "base")
    _draw_frame(ax, (0.69, 0.32), 0.4, "object")
    _node(ax, 0.27, 0.68, 0.16, 0.05, "URDF", "blue")
    _node(ax, 0.45, 0.68, 0.16, 0.05, "limits", "red")
    _node(ax, 0.63, 0.68, 0.16, 0.05, "camera", "teal")
    _node(ax, 0.81, 0.68, 0.16, 0.05, "plant", "green")
    return _save(fig, output_dir, "01_robot_setup")


def figure_transforms(output_dir: Path) -> Path:
    fig, ax = _canvas("Transforms, Kinematics, IK", "frames become motion through the Jacobian")
    _draw_frame(ax, (0.23, 0.34), 0.0, "W", 0.09)
    _draw_frame(ax, (0.43, 0.48), 0.55, "G", 0.09)
    _draw_frame(ax, (0.59, 0.55), 0.95, "B", 0.09)
    _arrow(ax, (0.28, 0.36), (0.39, 0.45), "blue")
    _arrow(ax, (0.48, 0.5), (0.55, 0.54), "teal")
    pts = _draw_arm(ax, (0.26, 0.22), [0.55, -0.2, 0.42], [0.2, 0.16, 0.12], "blue")
    ax.scatter([0.78], [0.58], marker="*", s=180, color=PALETTE["amber"], edgecolor=PALETTE["ink"], zorder=5)
    _arrow(ax, tuple(pts[-1]), (0.77, 0.57), "red")
    for i, row in enumerate(["dx", "dy"]):
        ax.text(0.75, 0.31 - i * 0.055, row, fontsize=9, color=PALETTE["muted"], weight="bold")
        for j in range(3):
            ax.add_patch(Rectangle((0.8 + j * 0.042, 0.29 - i * 0.055), 0.032, 0.032, fc=PALETTE["white"], ec=PALETTE["blue"], lw=1.0))
    ax.text(0.82, 0.21, "J dq", fontsize=10, color=PALETTE["ink"], weight="bold")
    return _save(fig, output_dir, "02_transforms_kinematics_ik")


def figure_icp(output_dir: Path) -> Path:
    fig, ax = _canvas("Geometric Perception", "point clouds align into object pose")
    source = np.array([[0.18, 0.34], [0.25, 0.47], [0.34, 0.37], [0.39, 0.57], [0.46, 0.43]])
    target = source @ np.array([[0.92, -0.25], [0.25, 0.92]]) + np.array([0.32, 0.03])
    ax.scatter(source[:, 0], source[:, 1], s=120, color=PALETTE["sky"], edgecolor=PALETTE["ink"], lw=0.8)
    ax.scatter(target[:, 0], target[:, 1], s=120, color=PALETTE["red"], marker="s", edgecolor=PALETTE["ink"], lw=0.8)
    for a, b in zip(source, target):
        ax.plot([a[0], b[0]], [a[1], b[1]], color=PALETTE["muted"], lw=1.0, ls=":", alpha=0.8)
    _curved_arrow(ax, (0.45, 0.62), (0.68, 0.62), "teal", rad=0.2)
    _node(ax, 0.22, 0.68, 0.16, 0.05, "source", "blue")
    _node(ax, 0.78, 0.68, 0.16, 0.05, "target", "red")
    _node(ax, 0.5, 0.2, 0.22, 0.05, "rigid transform", "teal")
    return _save(fig, output_dir, "03_geometric_perception_icp")


def figure_grasp(output_dir: Path) -> Path:
    fig, ax = _canvas("Grasp Scoring", "contact balance turns point clouds into choices")
    rng = np.random.default_rng(8)
    left = rng.normal([-0.16, 0.42], [0.025, 0.06], size=(30, 2))
    right = rng.normal([0.16, 0.42], [0.025, 0.06], size=(30, 2))
    clutter = rng.normal([0.0, 0.62], [0.08, 0.03], size=(22, 2))
    points = np.vstack([left, right, clutter])
    ax.scatter(points[:, 0] + 0.5, points[:, 1], s=32, color=PALETTE["teal"], alpha=0.8)
    ax.plot([0.26, 0.74], [0.42, 0.42], color=PALETTE["amber"], lw=5, solid_capstyle="round")
    ax.plot([0.26, 0.26], [0.31, 0.53], color=PALETTE["amber"], lw=5, solid_capstyle="round")
    ax.plot([0.74, 0.74], [0.31, 0.53], color=PALETTE["amber"], lw=5, solid_capstyle="round")
    _arrow(ax, (0.35, 0.42), (0.44, 0.42), "red")
    _arrow(ax, (0.65, 0.42), (0.56, 0.42), "red")
    _node(ax, 0.5, 0.68, 0.18, 0.05, "antipodal", "red")
    return _save(fig, output_dir, "04_grasp_scoring")


def figure_planning(output_dir: Path) -> Path:
    fig, ax = _canvas("Motion Planning", "sample a tree, return a safe path")
    ax.add_patch(Circle((0.51, 0.43), 0.11, fc=PALETTE["red"], ec=PALETTE["red"], alpha=0.2, lw=2))
    rng = np.random.default_rng(4)
    nodes = [np.array([0.22, 0.24])]
    for _ in range(55):
        sample = rng.uniform([0.2, 0.22], [0.82, 0.68])
        nearest = min(nodes, key=lambda p: np.linalg.norm(sample - p))
        direction = sample - nearest
        if np.linalg.norm(direction) == 0:
            continue
        new = nearest + direction / np.linalg.norm(direction) * 0.055
        if np.linalg.norm(new - np.array([0.51, 0.43])) < 0.13:
            continue
        nodes.append(new)
        ax.plot([nearest[0], new[0]], [nearest[1], new[1]], color=PALETTE["sky"], lw=0.9, alpha=0.75)
    path = np.array([[0.22, 0.24], [0.31, 0.32], [0.39, 0.58], [0.58, 0.66], [0.79, 0.68]])
    ax.plot(path[:, 0], path[:, 1], "-o", color=PALETTE["blue"], lw=4, markersize=6)
    ax.scatter([0.22], [0.24], s=120, color=PALETTE["green"], edgecolor=PALETTE["ink"])
    ax.scatter([0.79], [0.68], marker="*", s=220, color=PALETTE["amber"], edgecolor=PALETTE["ink"])
    return _save(fig, output_dir, "05_motion_planning_rrt")


def figure_control(output_dir: Path) -> Path:
    fig, ax = _canvas("Control", "planned motion meets dynamics and damping")
    t = np.linspace(0, 1, 160)
    response = 1 - np.exp(-5.5 * t) * (np.cos(8 * t) + 0.24 * np.sin(8 * t))
    ax.plot(0.18 + 0.42 * t, 0.22 + 0.38 * response / max(response), color=PALETTE["blue"], lw=3.2)
    ax.plot([0.18, 0.6], [0.6, 0.6], color=PALETTE["ink"], lw=1.2, ls=":")
    ax.text(0.18, 0.63, "target", fontsize=9, color=PALETTE["muted"], weight="bold")
    ax.add_patch(Rectangle((0.72, 0.37), 0.11, 0.11, fc=PALETTE["white"], ec=PALETTE["ink"], lw=2))
    ax.plot([0.65, 0.72], [0.425, 0.425], color=PALETTE["amber"], lw=4)
    for i in range(4):
        ax.plot([0.65 + i * 0.017, 0.66 + i * 0.017], [0.39, 0.46], color=PALETTE["red"], lw=1.4)
    _arrow(ax, (0.86, 0.425), (0.93, 0.425), "teal")
    _node(ax, 0.33, 0.7, 0.14, 0.05, "PD trace", "blue")
    _node(ax, 0.79, 0.62, 0.16, 0.05, "impedance", "amber")
    return _save(fig, output_dir, "06_control_pd_impedance")


def figure_segmentation(output_dir: Path) -> Path:
    fig, ax = _canvas("Segmentation To Grasp", "pixels become points, points become actions")
    for i in range(5):
        for j in range(5):
            color = PALETTE["teal"] if 1 <= i <= 3 and 1 <= j <= 3 else PALETTE["grid"]
            ax.add_patch(Rectangle((0.18 + i * 0.045, 0.45 + j * 0.045), 0.038, 0.038, fc=color, ec=PALETTE["white"], lw=1))
    _arrow(ax, (0.43, 0.54), (0.53, 0.54), "blue")
    pts = np.array([[0.58, 0.44], [0.62, 0.49], [0.67, 0.44], [0.64, 0.57], [0.71, 0.52]])
    ax.scatter(pts[:, 0], pts[:, 1], s=70, color=PALETTE["teal"], edgecolor=PALETTE["ink"], lw=0.7)
    ax.plot([0.55, 0.74], [0.39, 0.39], color=PALETTE["amber"], lw=4)
    ax.plot([0.55, 0.55], [0.34, 0.44], color=PALETTE["amber"], lw=4)
    ax.plot([0.74, 0.74], [0.34, 0.44], color=PALETTE["amber"], lw=4)
    _node(ax, 0.29, 0.7, 0.12, 0.05, "mask", "teal")
    _node(ax, 0.64, 0.7, 0.16, 0.05, "grasp input", "amber")
    return _save(fig, output_dir, "07_segmentation_to_grasp")


def figure_rl(output_dir: Path) -> Path:
    fig, ax = _canvas("RL Gridworld", "state, action, reward, policy")
    origin = np.array([0.22, 0.22])
    size = 0.09
    for i in range(4):
        for j in range(4):
            ax.add_patch(Rectangle(origin + [i * size, j * size], size, size, fc=PALETTE["white"], ec=PALETTE["grid"], lw=1.2))
    ax.add_patch(Circle(origin + [0.5 * size, 0.5 * size], 0.025, fc=PALETTE["blue"], ec=PALETTE["ink"], lw=1))
    ax.add_patch(Rectangle(origin + [1.22 * size, 0.22 * size], 0.055, 0.055, fc=PALETTE["amber"], ec=PALETTE["ink"], lw=1))
    ax.plot([origin[0] + 0.5 * size, origin[0] + 1.5 * size], [origin[1] + 0.5 * size, origin[1] + 0.5 * size], color=PALETTE["blue"], lw=4)
    loop = [("state", 0.63, 0.62, "blue"), ("action", 0.78, 0.54, "violet"), ("reward", 0.73, 0.36, "amber"), ("policy", 0.57, 0.4, "green")]
    for text, x, y, color in loop:
        ax.add_patch(Circle((x, y), 0.055, fc=PALETTE["white"], ec=PALETTE[color], lw=2))
        _label(ax, x, y, text, size=8)
    for (_, x0, y0, c0), (_, x1, y1, _) in zip(loop, loop[1:] + loop[:1]):
        _curved_arrow(ax, (x0, y0), (x1, y1), c0, rad=0.18)
    return _save(fig, output_dir, "08_rl_gridworld")


FIGURE_BUILDERS = [
    figure_intro,
    figure_stack,
    figure_robot_setup,
    figure_transforms,
    figure_icp,
    figure_grasp,
    figure_planning,
    figure_control,
    figure_segmentation,
    figure_rl,
]


def generate_book_figures(output_dir: Path | str = BOOK_FIGURE_DIR) -> list[Path]:
    """Generate all Jupyter Book page figures and return their paths."""
    output_dir = Path(output_dir)
    return [builder(output_dir) for builder in FIGURE_BUILDERS]


def main() -> None:
    output_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else BOOK_FIGURE_DIR
    for path in generate_book_figures(output_dir):
        print(path)


if __name__ == "__main__":
    main()
