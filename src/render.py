from typing import List

import svgwrite  # type: ignore

from parse import Note
from svg import SVG, Point

svg = SVG(margin=50)


NUM_NOTES = 7

WHOLE_NOTE_WIDTH = 100
STAFF_SPACE_HEIGHT = 15
EDGE_NOTE_PADDING = 2 * STAFF_SPACE_HEIGHT
HALF_STAFF_SPACE = STAFF_SPACE_HEIGHT / 2
STAFF_HEIGHT = NUM_NOTES * HALF_STAFF_SPACE
NOTE_SIZE = 10

THICK_LINE_WIDTH = 4


def draw_note(note: Note, point: Point, color: str) -> None:
    accidental = note.accidental
    if accidental == "natural":
        svg.circle(point, NOTE_SIZE, color)
    elif accidental == "sharp":
        svg.polygon(
            [
                Point(point.x - NOTE_SIZE, point.y - NOTE_SIZE),
                Point(point.x - NOTE_SIZE, point.y + NOTE_SIZE),
                Point(point.x + NOTE_SIZE, point.y),
            ],
            color,
        )


def line_width_at_index(index: int) -> int:
    index %= NUM_NOTES
    if index == 0:
        return THICK_LINE_WIDTH
    return 0


def draw_notes(origin: Point, notes: List[Note]) -> None:
    for note in notes:
        position = Point(
            origin.x + (note.time * WHOLE_NOTE_WIDTH),
            origin.y - (note.note * HALF_STAFF_SPACE),
        )
        # https://ai.googleblog.com/2019/08/turbo-improved-rainbow-colormap-for.html
        color = {
            0: svgwrite.utils.rgb(210, 49, 5),
            1: svgwrite.utils.rgb(251, 127, 34),
            2: svgwrite.utils.rgb(237, 208, 57),
            3: svgwrite.utils.rgb(164, 253, 61),
            4: svgwrite.utils.rgb(48, 241, 153),
            5: svgwrite.utils.rgb(45, 187, 236),
            6: svgwrite.utils.rgb(71, 107, 227),
        }.get(note.note % NUM_NOTES, "black")
        draw_note(note, position, color)


def draw_staff(origin: Point, width: float, draw_top: bool) -> None:
    for i in range(8 if draw_top else 7):
        line_width = line_width_at_index(i)
        if line_width > 0:
            line_y = origin.y + STAFF_HEIGHT - (i * HALF_STAFF_SPACE)
            svg.line(
                Point(origin.x, line_y),
                Point(origin.x + width, line_y),
                line_width,
                color=svgwrite.utils.rgb(127, 127, 127),
                opacity="0.5",
            )


def draw_staves(origin: Point, count: int, width: float) -> None:
    for i in range(count):
        draw_top = i == 0
        draw_staff(Point(origin.x, origin.y + (i * STAFF_HEIGHT)), width, draw_top)


def normalize_notes(notes: List[Note]) -> None:
    # Shift everything as much as possible
    min_note = min(note.note for note in notes)
    sub = (min_note // NUM_NOTES) * NUM_NOTES
    for note in notes:
        note.note -= sub


def render(score: List[Note]) -> str:
    normalize_notes(score)
    max_note = max(note.note for note in score)
    num_staves = (max_note // NUM_NOTES) + 1
    width = max(note.time for note in score) * WHOLE_NOTE_WIDTH
    draw_staves(Point(0, 0), num_staves, width + (2 * EDGE_NOTE_PADDING))
    draw_notes(Point(EDGE_NOTE_PADDING, num_staves * STAFF_HEIGHT), score)
    return str(svg)
