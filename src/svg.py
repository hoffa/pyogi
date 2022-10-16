from dataclasses import dataclass
from typing import Any

import svgwrite  # type: ignore


@dataclass
class Point:
    x: float
    y: float


class SVG:
    def __init__(
        self, margin_w: float, margin_h: float, bg_color: str = "white"
    ) -> None:
        self.svg = svgwrite.Drawing(style=f"background-color: {bg_color};")
        self.width: float = 0
        self.height: float = 0
        self.margin_w = margin_w
        self.margin_h = margin_h

    def _update_size(self, point: Point) -> None:
        self.width = max(self.width, point.x)
        self.height = max(self.height, point.y)

    def _add(self, element: Any) -> Any:
        self.svg.add(element).translate(self.margin_w, self.margin_h)

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

    def ellipse(
        self,
        center: Point,
        rx: float,
        ry: float,
        angle: float,
        color: str = "black",
        stroke: str = "black",
        stroke_width: float = 1.0,
    ) -> None:
        shape = self.svg.ellipse(
            (center.x, center.y),
            (rx, ry),
            fill=color,
            stroke=stroke,
            stroke_width=str(stroke_width),
        )
        shape.rotate(angle, (center.x, center.y))
        self._add(shape)

    def __str__(self) -> str:
        # It's ugly but works
        width = int(self.width + (2 * self.margin_w))
        height = int(self.height + (2 * self.margin_h))
        return (
            str(self.svg.tostring())
            .replace('width="100%"', f'width="{width}"')
            .replace('height="100%"', f'height="{height}"')
        )
