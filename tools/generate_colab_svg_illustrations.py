"""Generate professional SVG-sourced concept illustrations for Colab notebooks."""

from __future__ import annotations

from dataclasses import dataclass
from html import escape
import math
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont


WIDTH = 1600
HEIGHT = 900
SCALE = 2

PALETTE = {
    "paper": "#f4f7fb",
    "panel": "#ffffff",
    "ink": "#182232",
    "muted": "#697586",
    "line": "#d7e0ea",
    "grid": "#e8eef5",
    "blue": "#2d6cdf",
    "teal": "#128b82",
    "green": "#3f8f55",
    "amber": "#d99722",
    "orange": "#d86f3a",
    "red": "#c94b38",
    "violet": "#5867d8",
    "steel": "#9aa8bb",
    "dark": "#263241",
}

FONT_REGULAR = [
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/Library/Fonts/Arial.ttf",
]
FONT_BOLD = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/Library/Fonts/Arial Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
]


def _hex_to_rgba(hex_color: str, alpha: float = 1.0) -> tuple[int, int, int, int]:
    hex_color = hex_color.lstrip("#")
    return (
        int(hex_color[0:2], 16),
        int(hex_color[2:4], 16),
        int(hex_color[4:6], 16),
        round(max(0.0, min(1.0, alpha)) * 255),
    )


def _font(size: int, weight: str = "regular") -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    paths = FONT_BOLD if weight == "bold" else FONT_REGULAR
    for path in paths:
        try:
            return ImageFont.truetype(path, size * SCALE)
        except OSError:
            continue
    return ImageFont.load_default()


def _arrow_head(x1: float, y1: float, x2: float, y2: float, size: float) -> list[tuple[float, float]]:
    angle = math.atan2(y2 - y1, x2 - x1)
    left = angle + math.pi * 0.82
    right = angle - math.pi * 0.82
    return [
        (x2, y2),
        (x2 + math.cos(left) * size, y2 + math.sin(left) * size),
        (x2 + math.cos(right) * size, y2 + math.sin(right) * size),
    ]


class SvgCanvas:
    """Small SVG writer intentionally limited to this illustration system."""

    def __init__(self) -> None:
        self.elements: list[str] = []

    def _style(self, fill: str | None, stroke: str | None, width: float, alpha: float) -> str:
        attrs = []
        attrs.append(f'fill="{fill if fill else "none"}"')
        attrs.append(f'stroke="{stroke if stroke else "none"}"')
        if width:
            attrs.append(f'stroke-width="{width:.2f}"')
            attrs.append('stroke-linecap="round"')
            attrs.append('stroke-linejoin="round"')
        if alpha < 1:
            attrs.append(f'opacity="{alpha:.3f}"')
        return " ".join(attrs)

    def line(self, x1: float, y1: float, x2: float, y2: float, color: str, width: float = 2, alpha: float = 1) -> None:
        self.elements.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'{self._style(None, color, width, alpha)} />'
        )

    def polyline(self, points: list[tuple[float, float]], color: str, width: float = 2, alpha: float = 1) -> None:
        point_text = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
        self.elements.append(f'<polyline points="{point_text}" {self._style(None, color, width, alpha)} />')

    def polygon(
        self,
        points: list[tuple[float, float]],
        fill: str,
        stroke: str | None = None,
        width: float = 0,
        alpha: float = 1,
    ) -> None:
        point_text = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
        self.elements.append(f'<polygon points="{point_text}" {self._style(fill, stroke, width, alpha)} />')

    def rect(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        fill: str,
        stroke: str | None = None,
        width: float = 0,
        radius: float = 0,
        alpha: float = 1,
    ) -> None:
        self.elements.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{radius:.1f}" '
            f'{self._style(fill, stroke, width, alpha)} />'
        )

    def circle(
        self,
        x: float,
        y: float,
        r: float,
        fill: str,
        stroke: str | None = None,
        width: float = 0,
        alpha: float = 1,
    ) -> None:
        self.elements.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" {self._style(fill, stroke, width, alpha)} />'
        )

    def text(
        self,
        x: float,
        y: float,
        text: str,
        size: int,
        fill: str,
        weight: str = "regular",
        anchor: str = "start",
        alpha: float = 1,
    ) -> None:
        svg_weight = "700" if weight == "bold" else "500"
        self.elements.append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-family="Arial, Helvetica, sans-serif" '
            f'font-size="{size}" font-weight="{svg_weight}" text-anchor="{anchor}" '
            f'fill="{fill}" opacity="{alpha:.3f}">{escape(text)}</text>'
        )

    def save(self, path: Path, metadata: str) -> None:
        content = "\n".join(self.elements)
        path.write_text(
            f'''<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}" data-rml-style="technical-svg-v1">
  <title>Robotic Manipulation Learning Concept Illustration</title>
  <desc>{escape(metadata)}</desc>
  <metadata>
    Canonical Colab concept asset. Generated by tools/generate_colab_svg_illustrations.py.
    Visual system: cool engineering paper, restrained robotics palette, shared line widths,
    large readable primitives, no photo textures, no random image-generation artifacts.
    Use the SVG as the source of truth; PNG exports are for notebook and static site display.
  </metadata>
  <defs>
    <filter id="soft-shadow" x="-10%" y="-10%" width="120%" height="120%">
      <feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#182232" flood-opacity="0.12"/>
    </filter>
  </defs>
  {content}
</svg>
''',
            encoding="utf-8",
        )


class PngCanvas:
    def __init__(self) -> None:
        self.image = Image.new("RGBA", (WIDTH * SCALE, HEIGHT * SCALE), _hex_to_rgba(PALETTE["paper"]))
        self.draw = ImageDraw.Draw(self.image)

    def _p(self, value: float) -> int:
        return round(value * SCALE)

    def line(self, x1: float, y1: float, x2: float, y2: float, color: str, width: float = 2, alpha: float = 1) -> None:
        self.draw.line(
            [(self._p(x1), self._p(y1)), (self._p(x2), self._p(y2))],
            fill=_hex_to_rgba(color, alpha),
            width=max(1, self._p(width)),
        )

    def polyline(self, points: list[tuple[float, float]], color: str, width: float = 2, alpha: float = 1) -> None:
        scaled = [(self._p(x), self._p(y)) for x, y in points]
        self.draw.line(scaled, fill=_hex_to_rgba(color, alpha), width=max(1, self._p(width)), joint="curve")

    def polygon(
        self,
        points: list[tuple[float, float]],
        fill: str,
        stroke: str | None = None,
        width: float = 0,
        alpha: float = 1,
    ) -> None:
        scaled = [(self._p(x), self._p(y)) for x, y in points]
        self.draw.polygon(scaled, fill=_hex_to_rgba(fill, alpha))
        if stroke and width:
            self.draw.line(scaled + [scaled[0]], fill=_hex_to_rgba(stroke), width=max(1, self._p(width)), joint="curve")

    def rect(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        fill: str,
        stroke: str | None = None,
        width: float = 0,
        radius: float = 0,
        alpha: float = 1,
    ) -> None:
        xy = [self._p(x), self._p(y), self._p(x + w), self._p(y + h)]
        if radius:
            self.draw.rounded_rectangle(
                xy,
                radius=self._p(radius),
                fill=_hex_to_rgba(fill, alpha),
                outline=_hex_to_rgba(stroke) if stroke else None,
                width=max(1, self._p(width)) if stroke and width else 1,
            )
        else:
            self.draw.rectangle(
                xy,
                fill=_hex_to_rgba(fill, alpha),
                outline=_hex_to_rgba(stroke) if stroke else None,
                width=max(1, self._p(width)) if stroke and width else 1,
            )

    def circle(
        self,
        x: float,
        y: float,
        r: float,
        fill: str,
        stroke: str | None = None,
        width: float = 0,
        alpha: float = 1,
    ) -> None:
        xy = [self._p(x - r), self._p(y - r), self._p(x + r), self._p(y + r)]
        self.draw.ellipse(
            xy,
            fill=_hex_to_rgba(fill, alpha),
            outline=_hex_to_rgba(stroke) if stroke else None,
            width=max(1, self._p(width)) if stroke and width else 1,
        )

    def text(
        self,
        x: float,
        y: float,
        text: str,
        size: int,
        fill: str,
        weight: str = "regular",
        anchor: str = "start",
        alpha: float = 1,
    ) -> None:
        font = _font(size, weight)
        scaled_x = self._p(x)
        scaled_y = self._p(y)
        bbox = self.draw.textbbox((0, 0), text, font=font)
        width = bbox[2] - bbox[0]
        if anchor == "middle":
            scaled_x -= width // 2
        elif anchor == "end":
            scaled_x -= width
        self.draw.text((scaled_x, scaled_y - (bbox[3] - bbox[1])), text, font=font, fill=_hex_to_rgba(fill, alpha))

    def save(self, path: Path) -> None:
        resized = self.image.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)
        resized.convert("RGB").save(path, optimize=True)


class Canvas:
    def __init__(self) -> None:
        self.svg = SvgCanvas()
        self.png = PngCanvas()

    def line(self, *args, **kwargs) -> None:
        self.svg.line(*args, **kwargs)
        self.png.line(*args, **kwargs)

    def polyline(self, *args, **kwargs) -> None:
        self.svg.polyline(*args, **kwargs)
        self.png.polyline(*args, **kwargs)

    def polygon(self, *args, **kwargs) -> None:
        self.svg.polygon(*args, **kwargs)
        self.png.polygon(*args, **kwargs)

    def rect(self, *args, **kwargs) -> None:
        self.svg.rect(*args, **kwargs)
        self.png.rect(*args, **kwargs)

    def circle(self, *args, **kwargs) -> None:
        self.svg.circle(*args, **kwargs)
        self.png.circle(*args, **kwargs)

    def text(self, *args, **kwargs) -> None:
        self.svg.text(*args, **kwargs)
        self.png.text(*args, **kwargs)

    def arrow(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        color: str,
        width: float = 3,
        head: float = 18,
        alpha: float = 1,
    ) -> None:
        self.line(x1, y1, x2, y2, color, width, alpha)
        self.polygon(_arrow_head(x1, y1, x2, y2, head), color, alpha=alpha)


@dataclass(frozen=True)
class SceneSpec:
    module: str
    title: str
    subtitle: str
    image_name: str
    draw: str


SCENES = [
    SceneSpec(
        "02",
        "Transforms, Kinematics, IK",
        "Frames compose into a reachable tool pose; differential IK shrinks the target error.",
        "02_transforms_kinematics_ik_concept.png",
        "transforms",
    ),
    SceneSpec(
        "03",
        "Geometric Perception and ICP",
        "Correspondences estimate the rigid transform that aligns source and target points.",
        "03_geometric_perception_icp_concept.png",
        "icp",
    ),
    SceneSpec(
        "04",
        "Grasp Scoring",
        "Antipodal contact balance separates robust candidates from weak grasps.",
        "04_grasp_scoring_concept.png",
        "grasp",
    ),
    SceneSpec(
        "05",
        "Motion Planning with RRT",
        "Random samples grow a collision-free tree until a short path reaches the goal.",
        "05_motion_planning_rrt_concept.png",
        "rrt",
    ),
    SceneSpec(
        "06",
        "PD and Impedance Control",
        "Virtual stiffness and damping turn pose error into a controlled response.",
        "06_control_pd_impedance_concept.png",
        "control",
    ),
    SceneSpec(
        "07",
        "Segmentation to Grasp",
        "A mask selects the target points before downstream grasp proposals are ranked.",
        "07_segmentation_to_grasp_concept.png",
        "segmentation",
    ),
    SceneSpec(
        "08",
        "RL Grasping Gridworld",
        "State, action, reward, and policy can be studied in a compact manipulation world.",
        "08_rl_gridworld_concept.png",
        "rl",
    ),
]


def draw_base(c: Canvas, spec: SceneSpec) -> None:
    c.rect(0, 0, WIDTH, HEIGHT, PALETTE["paper"])
    for x in range(80, WIDTH, 80):
        c.line(x, 0, x, HEIGHT, PALETTE["grid"], 1)
    for y in range(80, HEIGHT, 80):
        c.line(0, y, WIDTH, y, PALETTE["grid"], 1)
    for x in range(160, WIDTH, 320):
        c.line(x, 184, x, 820, PALETTE["line"], 1.2, 0.75)

    c.rect(52, 52, 1496, 796, PALETTE["panel"], PALETTE["line"], 2, radius=6)
    c.rect(52, 52, 1496, 106, PALETTE["panel"], PALETTE["line"], 1, radius=6)
    c.rect(86, 78, 80, 52, PALETTE["ink"], radius=4)
    c.text(126, 115, spec.module, 28, PALETTE["panel"], "bold", "middle")
    c.text(190, 104, spec.title, 40, PALETTE["ink"], "bold")
    c.text(190, 137, spec.subtitle, 22, PALETTE["muted"])
    c.text(1355, 103, "RML COLAB", 18, PALETTE["muted"], "bold", "end")
    c.text(1355, 131, "concept map", 16, PALETTE["steel"], "regular", "end")
    c.rect(1385, 82, 96, 46, PALETTE["blue"], radius=4)
    c.text(1433, 113, "RUN", 18, PALETTE["panel"], "bold", "middle")

    legend = [
        ("state", PALETTE["blue"]),
        ("target", PALETTE["amber"]),
        ("error", PALETTE["red"]),
        ("policy", PALETTE["teal"]),
    ]
    x = 86
    for label, color in legend:
        c.circle(x + 8, 812, 8, color)
        c.text(x + 24, 819, label, 15, PALETTE["muted"], "bold")
        x += 118


def frame_axes(c: Canvas, x: float, y: float, scale: float, label: str) -> None:
    c.arrow(x, y, x + 58 * scale, y, PALETTE["red"], 4, 12)
    c.arrow(x, y, x, y - 58 * scale, PALETTE["teal"], 4, 12)
    c.circle(x, y, 7 * scale, PALETTE["ink"])
    c.text(x - 8, y + 34, label, 16, PALETTE["muted"], "bold", "middle")


def draw_robot_arm(c: Canvas, points: list[tuple[float, float]], color: str, alpha: float = 1, width: float = 18) -> None:
    for p1, p2 in zip(points, points[1:]):
        c.line(p1[0], p1[1], p2[0], p2[1], color, width, alpha)
    for idx, (x, y) in enumerate(points):
        fill = PALETTE["panel"] if idx else PALETTE["dark"]
        c.circle(x, y, 22, fill, color, 6, alpha)


def draw_transforms(c: Canvas) -> None:
    c.rect(120, 214, 860, 544, "#f8fbff", PALETTE["line"], 2, radius=6)
    base = (250, 650)
    ghost_arms = [
        [(250, 650), (430, 560), (610, 520), (760, 450)],
        [(250, 650), (455, 600), (640, 500), (805, 405)],
        [(250, 650), (470, 610), (690, 535), (845, 480)],
    ]
    for arm in ghost_arms:
        draw_robot_arm(c, arm, PALETTE["steel"], 0.35, 12)
    main_arm = [(250, 650), (475, 585), (675, 515), (845, 480)]
    draw_robot_arm(c, main_arm, PALETTE["blue"], 1, 20)
    c.line(830, 468, 890, 430, PALETTE["ink"], 7)
    c.line(850, 493, 914, 486, PALETTE["ink"], 7)
    c.circle(975, 360, 22, PALETTE["amber"], PALETTE["ink"], 3)
    c.arrow(850, 470, 952, 374, PALETTE["red"], 5, 18)
    c.text(918, 420, "pose error", 17, PALETTE["red"], "bold", "middle")
    for x, y in [(790, 505), (825, 482), (865, 447), (910, 402), (952, 374)]:
        c.circle(x, y, 7, PALETTE["red"], alpha=0.65)
    frame_axes(c, 250, 650, 1.0, "world")
    frame_axes(c, 845, 480, 0.72, "tool")
    frame_axes(c, 975, 360, 0.72, "target")

    c.rect(1045, 246, 380, 470, "#fbfcfe", PALETTE["line"], 2, radius=6)
    c.text(1080, 300, "Differential IK loop", 24, PALETTE["ink"], "bold")
    steps = [
        ("1", "measure current pose", PALETTE["blue"]),
        ("2", "compute target error", PALETTE["red"]),
        ("3", "update joint rates", PALETTE["teal"]),
    ]
    y = 366
    for number, label, color in steps:
        c.circle(1102, y - 8, 26, color)
        c.text(1102, y + 1, number, 20, PALETTE["panel"], "bold", "middle")
        c.rect(1152, y - 42, 214, 58, "#ffffff", PALETTE["line"], 2, radius=4)
        c.text(1172, y - 4, label, 19, PALETTE["ink"], "bold")
        if number != "3":
            c.arrow(1102, y + 28, 1102, y + 86, PALETTE["steel"], 3, 12)
        y += 118
    c.polyline([(1185, 658), (1235, 632), (1290, 646), (1345, 604), (1385, 620)], PALETTE["teal"], 5)
    c.text(1288, 690, "error decreases", 17, PALETTE["muted"], "bold", "middle")


def deterministic_cloud(cx: float, cy: float, rx: float, ry: float, n: int, phase: float = 0) -> list[tuple[float, float]]:
    pts = []
    for i in range(n):
        t = i * 2.399963 + phase
        r = math.sqrt((i + 0.5) / n)
        wobble = 1 + 0.13 * math.sin(i * 1.7 + phase)
        pts.append((cx + math.cos(t) * rx * r * wobble, cy + math.sin(t) * ry * r * wobble))
    return pts


def rotate_translate(points: list[tuple[float, float]], cx: float, cy: float, angle: float, dx: float, dy: float) -> list[tuple[float, float]]:
    out = []
    ca = math.cos(angle)
    sa = math.sin(angle)
    for x, y in points:
        px = x - cx
        py = y - cy
        out.append((cx + px * ca - py * sa + dx, cy + px * sa + py * ca + dy))
    return out


def draw_icp(c: Canvas) -> None:
    c.rect(108, 228, 950, 512, "#f9fbfe", PALETTE["line"], 2, radius=6)
    c.rect(145, 640, 850, 38, "#e5ecf4", PALETTE["line"], 2, radius=4)
    c.rect(186, 410, 110, 120, "#dfe7f0", PALETTE["steel"], 3, radius=6)
    c.circle(238, 408, 36, PALETTE["dark"])
    c.circle(238, 408, 20, PALETTE["blue"])
    c.arrow(296, 430, 440, 460, PALETTE["blue"], 4, 16, 0.8)
    c.text(198, 568, "RGB-D camera", 17, PALETTE["muted"], "bold")

    target = deterministic_cloud(720, 470, 170, 96, 64, 0.2)
    source = rotate_translate(target, 720, 470, -0.42, -230, -34)
    for idx in range(0, len(target), 8):
        sx, sy = source[idx]
        tx, ty = target[idx]
        c.line(sx, sy, tx, ty, PALETTE["steel"], 1.4, 0.38)
    for x, y in target:
        c.circle(x, y, 5, PALETTE["amber"], alpha=0.9)
    for x, y in source:
        c.circle(x, y, 5, PALETTE["blue"], alpha=0.88)
    c.polyline([(512, 324), (600, 278), (710, 294), (812, 356)], PALETTE["violet"], 5)
    c.arrow(760, 350, 838, 420, PALETTE["violet"], 5, 18)
    c.text(650, 286, "rigid transform", 18, PALETTE["violet"], "bold", "middle")
    frame_axes(c, 494, 540, 0.64, "source")
    frame_axes(c, 775, 560, 0.64, "target")

    c.rect(1110, 250, 314, 438, "#ffffff", PALETTE["line"], 2, radius=6)
    c.text(1140, 303, "ICP estimate", 24, PALETTE["ink"], "bold")
    labels = [("nearest neighbors", PALETTE["blue"]), ("least-squares pose", PALETTE["violet"]), ("repeat until stable", PALETTE["teal"])]
    y = 372
    for label, color in labels:
        c.circle(1146, y - 8, 9, color)
        c.line(1170, y - 8, 1355, y - 8, color, 7, 0.28)
        c.text(1170, y + 20, label, 17, PALETTE["muted"], "bold")
        y += 100
    c.polyline([(1160, 622), (1202, 588), (1265, 600), (1328, 548), (1372, 556)], PALETTE["teal"], 5)


def draw_gripper(c: Canvas, x: float, y: float, angle: float, color: str, alpha: float = 1, scale: float = 1.0) -> None:
    length = 122 * scale
    jaw = 48 * scale
    ca = math.cos(angle)
    sa = math.sin(angle)

    def tx(px: float, py: float) -> tuple[float, float]:
        return (x + px * ca - py * sa, y + px * sa + py * ca)

    p1 = tx(-length / 2, -jaw / 2)
    p2 = tx(length / 2, -jaw / 2)
    p3 = tx(-length / 2, jaw / 2)
    p4 = tx(length / 2, jaw / 2)
    c.line(*p1, *p2, color, 8 * scale, alpha)
    c.line(*p3, *p4, color, 8 * scale, alpha)
    c.line(*tx(-length / 2, -jaw / 2), *tx(-length / 2, jaw / 2), color, 6 * scale, alpha)
    c.line(*tx(-length / 2 - 52 * scale, 0), *tx(-length / 2, 0), color, 7 * scale, alpha)


def draw_grasp(c: Canvas) -> None:
    c.rect(106, 238, 942, 500, "#f9fbfe", PALETTE["line"], 2, radius=6)
    c.rect(160, 642, 820, 42, "#e1e9f2", PALETTE["line"], 2, radius=4)
    object_outline = [(400, 510), (450, 420), (550, 380), (680, 402), (755, 470), (725, 575), (600, 626), (475, 600)]
    c.polygon(object_outline, "#e8edf5", PALETTE["steel"], 3)
    for x, y in deterministic_cloud(580, 505, 190, 118, 92, 1.1):
        c.circle(x, y, 4.5, PALETTE["steel"], alpha=0.72)
    draw_gripper(c, 610, 502, -0.14, PALETTE["teal"], 1, 1.28)
    c.circle(520, 490, 15, PALETTE["teal"], PALETTE["ink"], 2)
    c.circle(704, 466, 15, PALETTE["teal"], PALETTE["ink"], 2)
    c.arrow(520, 490, 478, 486, PALETTE["teal"], 4, 13)
    c.arrow(704, 466, 750, 455, PALETTE["teal"], 4, 13)
    draw_gripper(c, 520, 390, 0.78, PALETTE["steel"], 0.52, 0.92)
    draw_gripper(c, 700, 610, -0.95, PALETTE["red"], 0.48, 0.92)
    c.text(600, 354, "balanced antipodal contacts", 20, PALETTE["teal"], "bold", "middle")

    c.rect(1110, 248, 318, 456, "#ffffff", PALETTE["line"], 2, radius=6)
    c.text(1142, 304, "Candidate scores", 24, PALETTE["ink"], "bold")
    bars = [("A", 210, PALETTE["teal"]), ("B", 124, PALETTE["amber"]), ("C", 70, PALETTE["red"])]
    y = 378
    for label, width, color in bars:
        c.text(1144, y + 18, label, 20, PALETTE["ink"], "bold")
        c.rect(1180, y, 218, 28, "#edf2f7", radius=4)
        c.rect(1180, y, width, 28, color, radius=4)
        c.text(1180 + width - 10, y + 21, f"{width / 218:.2f}", 16, PALETTE["panel"], "bold", "end")
        y += 86
    c.text(1142, 650, "high score = contact normals oppose each other", 16, PALETTE["muted"], "bold")


def draw_rrt(c: Canvas) -> None:
    c.rect(120, 220, 900, 520, "#f9fbfe", PALETTE["line"], 2, radius=6)
    c.circle(565, 482, 98, "#f2c8bf", PALETTE["red"], 3, 0.9)
    c.text(565, 488, "obstacle", 17, PALETTE["red"], "bold", "middle")
    start = (214, 640)
    goal = (908, 318)
    c.circle(*start, 22, PALETTE["green"], PALETTE["ink"], 3)
    c.circle(*goal, 22, PALETTE["amber"], PALETTE["ink"], 3)
    c.text(start[0], start[1] + 52, "start", 17, PALETTE["green"], "bold", "middle")
    c.text(goal[0], goal[1] - 34, "goal", 17, PALETTE["amber"], "bold", "middle")
    nodes = [start]
    parents = [0]
    samples = [(310, 595), (365, 518), (280, 450), (455, 560), (500, 638), (650, 675), (728, 605), (780, 515), (820, 430), (904, 380), (740, 330), (625, 315), (458, 322), (350, 370), (865, 570), (920, 500), (710, 240), (500, 260)]
    parent_indices = [0, 1, 0, 1, 4, 5, 6, 7, 8, 9, 8, 10, 12, 13, 7, 15, 11, 13]
    for sample, parent in zip(samples, parent_indices):
        px, py = nodes[parent]
        sx, sy = sample
        c.circle(sx, sy, 4.5, PALETTE["steel"], alpha=0.62)
        c.line(px, py, sx, sy, PALETTE["blue"], 3, 0.58)
        nodes.append(sample)
    final_path = [start, (310, 595), (455, 560), (500, 638), (650, 675), (728, 605), (780, 515), (820, 430), (904, 380), goal]
    c.polyline(final_path, PALETTE["teal"], 9)
    for x, y in final_path:
        c.circle(x, y, 8, PALETTE["teal"])

    c.rect(1095, 248, 335, 450, "#ffffff", PALETTE["line"], 2, radius=6)
    c.text(1128, 306, "Sampling planner", 24, PALETTE["ink"], "bold")
    metrics = [("samples", "18", PALETTE["blue"]), ("collision checks", "many", PALETTE["red"]), ("returned path", "1", PALETTE["teal"])]
    y = 382
    for label, value, color in metrics:
        c.rect(1130, y - 32, 250, 58, "#f5f8fc", PALETTE["line"], 1, radius=4)
        c.text(1150, y - 1, label, 17, PALETTE["muted"], "bold")
        c.text(1362, y - 1, value, 20, color, "bold", "end")
        y += 94
    c.polyline([(1140, 626), (1196, 604), (1240, 618), (1298, 580), (1374, 594)], PALETTE["teal"], 5)


def draw_spring(c: Canvas, x1: float, y: float, x2: float, turns: int, amp: float, color: str) -> None:
    points = [(x1, y)]
    length = x2 - x1
    for i in range(1, turns * 2):
        x = x1 + length * i / (turns * 2)
        points.append((x, y + (amp if i % 2 else -amp)))
    points.append((x2, y))
    c.polyline(points, color, 5)


def draw_control(c: Canvas) -> None:
    c.rect(110, 236, 900, 500, "#f9fbfe", PALETTE["line"], 2, radius=6)
    c.line(220, 610, 880, 610, PALETTE["line"], 3)
    c.rect(720, 474, 104, 104, PALETTE["blue"], PALETTE["ink"], 4, radius=6)
    c.text(772, 535, "x", 32, PALETTE["panel"], "bold", "middle")
    c.circle(330, 526, 26, PALETTE["amber"], PALETTE["ink"], 3)
    c.text(330, 488, "target", 18, PALETTE["amber"], "bold", "middle")
    draw_spring(c, 356, 526, 720, 9, 26, PALETTE["teal"])
    c.rect(485, 568, 136, 42, "#e8eef5", PALETTE["steel"], 3, radius=4)
    c.line(505, 568, 505, 610, PALETTE["steel"], 6)
    c.line(600, 568, 600, 610, PALETTE["steel"], 6)
    c.arrow(824, 526, 900, 526, PALETTE["red"], 5, 18)
    c.text(872, 496, "control effort", 17, PALETTE["red"], "bold", "middle")
    c.text(536, 452, "virtual stiffness + damping", 21, PALETTE["teal"], "bold", "middle")

    c.rect(1078, 248, 360, 450, "#ffffff", PALETTE["line"], 2, radius=6)
    c.text(1112, 304, "Step response", 24, PALETTE["ink"], "bold")
    graph_x, graph_y = 1128, 628
    c.line(graph_x, graph_y, graph_x + 250, graph_y, PALETTE["line"], 3)
    c.line(graph_x, graph_y, graph_x, graph_y - 240, PALETTE["line"], 3)
    c.line(graph_x, graph_y - 150, graph_x + 252, graph_y - 150, PALETTE["amber"], 3, 0.55)
    response = []
    for i in range(80):
        t = i / 79 * 1.0
        y = 1 - math.exp(-4.2 * t) * (math.cos(10.5 * t) + 0.38 * math.sin(10.5 * t))
        response.append((graph_x + 250 * t, graph_y - 150 * y))
    c.polyline(response, PALETTE["blue"], 5)
    c.text(graph_x + 236, graph_y - 160, "target", 15, PALETTE["amber"], "bold", "end")
    c.text(graph_x + 128, graph_y + 42, "time", 16, PALETTE["muted"], "bold", "middle")
    c.text(graph_x - 20, graph_y - 218, "x", 16, PALETTE["muted"], "bold", "middle")


def draw_segmentation(c: Canvas) -> None:
    c.rect(102, 238, 430, 500, "#101722", PALETTE["line"], 2, radius=6)
    c.rect(132, 280, 370, 258, "#253348", radius=4)
    c.polygon([(190, 430), (232, 364), (310, 382), (344, 456), (280, 500)], PALETTE["teal"], alpha=0.75)
    c.circle(405, 416, 54, PALETTE["amber"], alpha=0.82)
    c.rect(146, 564, 342, 96, "#1d2736", PALETTE["steel"], 1, radius=4)
    for x, y in deterministic_cloud(267, 440, 92, 62, 46, 0.4):
        c.circle(x, y, 4.2, PALETTE["teal"], alpha=0.95)
    c.text(144, 704, "RGB-D view + mask", 19, PALETTE["panel"], "bold")
    c.arrow(535, 488, 655, 488, PALETTE["blue"], 5, 18)

    c.rect(660, 260, 300, 440, "#f9fbfe", PALETTE["line"], 2, radius=6)
    for x, y in deterministic_cloud(812, 482, 95, 132, 64, 1.6):
        c.circle(x, y, 5, PALETTE["teal"], alpha=0.82)
    for x, y in deterministic_cloud(876, 390, 52, 36, 14, 0.7):
        c.circle(x, y, 4, PALETTE["red"], alpha=0.38)
    frame_axes(c, 756, 620, 0.58, "object")
    c.text(810, 314, "target cloud", 20, PALETTE["teal"], "bold", "middle")
    c.arrow(963, 488, 1075, 488, PALETTE["blue"], 5, 18)

    c.rect(1082, 260, 350, 440, "#ffffff", PALETTE["line"], 2, radius=6)
    object_outline = [(1170, 500), (1210, 420), (1290, 414), (1340, 484), (1300, 565), (1210, 575)]
    c.polygon(object_outline, "#e8edf5", PALETTE["steel"], 3)
    draw_gripper(c, 1255, 492, -0.22, PALETTE["teal"], 1, 1.04)
    c.circle(1202, 480, 12, PALETTE["teal"], PALETTE["ink"], 2)
    c.circle(1300, 458, 12, PALETTE["teal"], PALETTE["ink"], 2)
    c.text(1256, 646, "ranked grasp proposal", 20, PALETTE["teal"], "bold", "middle")


def draw_policy_arrow(c: Canvas, x: float, y: float, direction: str, color: str) -> None:
    delta = {"up": (0, -28), "down": (0, 28), "left": (-28, 0), "right": (28, 0)}[direction]
    c.arrow(x, y, x + delta[0], y + delta[1], color, 4, 11)


def draw_rl(c: Canvas) -> None:
    c.rect(124, 226, 620, 520, "#f9fbfe", PALETTE["line"], 2, radius=6)
    grid_x, grid_y, cell = 190, 288, 100
    heat = [
        [0.12, 0.20, 0.30, 0.45],
        [0.18, 0.32, 0.48, 0.62],
        [0.25, 0.42, 0.70, 0.84],
        [0.36, 0.54, 0.76, 1.00],
    ]
    for row in range(4):
        for col in range(4):
            alpha = heat[row][col]
            color = PALETTE["teal"] if alpha > 0.7 else PALETTE["blue"]
            c.rect(grid_x + col * cell, grid_y + row * cell, cell, cell, color, PALETTE["line"], 2, alpha=0.14 + alpha * 0.28)
    for i in range(5):
        c.line(grid_x, grid_y + i * cell, grid_x + 4 * cell, grid_y + i * cell, PALETTE["ink"], 2, 0.55)
        c.line(grid_x + i * cell, grid_y, grid_x + i * cell, grid_y + 4 * cell, PALETTE["ink"], 2, 0.55)
    directions = [
        ["right", "right", "down", "down"],
        ["right", "down", "down", "down"],
        ["right", "right", "right", "down"],
        ["right", "right", "right", "up"],
    ]
    for row in range(4):
        for col in range(4):
            draw_policy_arrow(c, grid_x + col * cell + 50, grid_y + row * cell + 50, directions[row][col], PALETTE["ink"])
    c.circle(grid_x + 50, grid_y + 350, 24, PALETTE["blue"], PALETTE["ink"], 3)
    c.line(grid_x + 32, grid_y + 350, grid_x + 68, grid_y + 350, PALETTE["panel"], 7)
    c.line(grid_x + 50, grid_y + 332, grid_x + 50, grid_y + 368, PALETTE["panel"], 7)
    c.rect(grid_x + 315, grid_y + 315, 70, 70, PALETTE["amber"], PALETTE["ink"], 3, radius=6)
    c.text(grid_x + 350, grid_y + 358, "R", 30, PALETTE["panel"], "bold", "middle")
    c.text(grid_x + 200, grid_y + 468, "compact state-action space", 20, PALETTE["muted"], "bold", "middle")

    c.rect(830, 256, 580, 450, "#ffffff", PALETTE["line"], 2, radius=6)
    c.text(866, 312, "Learning loop", 24, PALETTE["ink"], "bold")
    nodes = [
        ("state", 910, 418, PALETTE["blue"]),
        ("action", 1115, 418, PALETTE["violet"]),
        ("reward", 1320, 418, PALETTE["amber"]),
        ("policy", 1115, 590, PALETTE["teal"]),
    ]
    for label, x, y, color in nodes:
        c.circle(x, y, 48, color)
        c.text(x, y + 8, label, 18, PALETTE["panel"], "bold", "middle")
    c.arrow(958, 418, 1067, 418, PALETTE["ink"], 4, 14)
    c.arrow(1163, 418, 1272, 418, PALETTE["ink"], 4, 14)
    c.arrow(1320, 466, 1162, 574, PALETTE["ink"], 4, 14)
    c.arrow(1068, 574, 910, 466, PALETTE["ink"], 4, 14)
    c.polyline([(890, 662), (970, 642), (1050, 650), (1130, 614), (1210, 625), (1358, 592)], PALETTE["teal"], 5)


DRAWERS = {
    "transforms": draw_transforms,
    "icp": draw_icp,
    "grasp": draw_grasp,
    "rrt": draw_rrt,
    "control": draw_control,
    "segmentation": draw_segmentation,
    "rl": draw_rl,
}


def generate(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    svg_dir = output_dir / "svg"
    svg_dir.mkdir(parents=True, exist_ok=True)
    for spec in SCENES:
        canvas = Canvas()
        draw_base(canvas, spec)
        DRAWERS[spec.draw](canvas)
        stem = Path(spec.image_name).stem
        metadata = f"{spec.module} {spec.title}. {spec.subtitle}"
        canvas.svg.save(svg_dir / f"{stem}.svg", metadata)
        canvas.png.save(output_dir / spec.image_name)
        print(output_dir / spec.image_name)


def main() -> None:
    output_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("book/assets/colab")
    generate(output_dir)


if __name__ == "__main__":
    main()
