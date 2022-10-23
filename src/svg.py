from dataclasses import dataclass
from typing import Any, List

import svgwrite  # type: ignore
from svgwrite.container import Group  # type: ignore


@dataclass
class Point:
    x: float
    y: float


class SVG:
    # TODO: Add margin, either by translating each or translating a container <g>
    def __init__(self, margin_w: int, margin_h: int, bg_color: str = "white") -> None:
        self.svg = svgwrite.Drawing(style=f"background-color: {bg_color};")
        self.g = Group()
        self.g.translate(margin_w, margin_h)
        self.svg.add(self.g)
        self.width: float = 0
        self.height: float = 0
        self.margin_w = margin_w
        self.margin_h = margin_h

    def _update_size(self, point: Point) -> None:
        self.width = max(self.width, point.x)
        self.height = max(self.height, point.y)

    def _add(self, element: Any) -> Any:
        self.g.add(element)

    def line(
        self,
        start: Point,
        end: Point,
        width: float,
        color: str = "black",
    ) -> None:
        self._update_size(start)
        self._update_size(end)
        self._add(
            self.svg.line(
                (start.x, start.y),
                (end.x, end.y),
                stroke_width=width,
                stroke=color,
                stroke_linecap="square",
            )
        )

    def polygon(self, points: List[Point], color: str = "black") -> None:
        for point in points:
            self._update_size(point)
        self._add(
            self.svg.polygon(
                [(point.x, point.y) for point in points],
                fill=color,
                stroke=color,
            )
        )

    def ellipse(
        self, center: Point, rx: float, ry: float, angle: float, color: str = "black"
    ) -> None:
        self._update_size(center)
        shape = self.svg.ellipse(
            (center.x, center.y),
            (rx, ry),
            fill=color,
            stroke=color,
        )
        shape.rotate(angle, (center.x, center.y))
        self._add(shape)

    def text(self, origin: Point, s: str, size: int) -> None:
        self._add(
            self.svg.text(
                s,
                insert=(origin.x, origin.y),
                alignment_baseline="middle",
                font_family="serif",
                font_size=f"{size}px",
                text_anchor="middle",
            )
        )

    def __str__(self) -> str:
        # It's ugly but works
        width = self.width + (2 * self.margin_w)
        height = self.height + (2 * self.margin_h)
        return (
            str(self.svg.tostring())
            .replace('width="100%"', f'width="{int(width)}"')
            .replace('height="100%"', f'height="{int(height)}"')
        )
