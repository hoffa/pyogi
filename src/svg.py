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
        self.width = 0
        self.height = 0

    def _update_size(self, point: Point) -> None:
        self.width = max(self.width, point.x)
        self.height = max(self.height, point.y)

    def line(
        self, start: Point, end: Point, width: float, color: str = "black"
    ) -> None:
        self._update_size(start)
        self._update_size(end)
        self.svg.add(
            self.svg.line(
                (start.x, start.y),
                (end.x, end.y),
                stroke_width=width,
                stroke=color,
            )
        )

    def circle(self, center: Point, radius: float, color: str = "black") -> None:
        self._update_size(center)
        self.svg.add(
            self.svg.circle(
                (center.x, center.y),
                radius,
                fill=color,
            )
        )

    def polygon(self, points: List[Point], color: str = "black") -> None:
        for point in points:
            self._update_size(point)
        self.svg.add(
            self.svg.polygon(
                [(point.x, point.y) for point in points],
                fill=color,
                stroke=color,
            )
        )

    def __str__(self) -> str:
        # It's ugly but works
        width = int(self.width)
        height = int(self.height)
        return (
            str(self.svg.tostring())
            .replace('width="100%"', f'width="{width}"')
            .replace('height="100%"', f'height="{height}"')
        )
