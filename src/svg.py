from dataclasses import dataclass
from typing import List

import svgwrite  # type: ignore


@dataclass
class Point:
    x: float
    y: float


class SVG:
    def __init__(self) -> None:
        self.svg = svgwrite.Drawing()

    def line(
        self, start: Point, end: Point, width: float, color: str = "black"
    ) -> None:
        self.svg.add(
            self.svg.line(
                (start.x, start.y),
                (end.x, end.y),
                stroke_width=width,
                stroke=color,
            )
        )

    def circle(self, center: Point, radius: float, color: str = "black") -> None:
        self.svg.add(
            self.svg.circle(
                (center.x, center.y),
                radius,
                fill=color,
            )
        )

    def polygon(self, points: List[Point], color: str = "black") -> None:
        self.svg.add(
            self.svg.polygon(
                [(point.x, point.y) for point in points],
                fill=color,
                stroke=color,
            )
        )

    def __str__(self) -> str:
        return str(self.svg.tostring())
