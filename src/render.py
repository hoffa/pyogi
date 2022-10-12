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

THIN_LINE_WIDTH = 2
THICK_LINE_WIDTH = 2 * THIN_LINE_WIDTH


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
    if index in [2, 5]:
        return THIN_LINE_WIDTH
    return 0


def draw_notes(origin: Point, notes: List[Note]) -> None:
    for note in notes:
        position = Point(
            origin.x + (note.time * WHOLE_NOTE_WIDTH),
            origin.y - (note.note * HALF_STAFF_SPACE),
        )
        # https://ai.googleblog.com/2019/08/turbo-improved-rainbow-colormap-for.html
        color = {
            1: svgwrite.utils.rgb(123, 3, 3),
            2: svgwrite.utils.rgb(223, 70, 13),
            3: svgwrite.utils.rgb(251, 186, 56),
            4: svgwrite.utils.rgb(164, 253, 61),
            5: svgwrite.utils.rgb(34, 227, 181),
            6: svgwrite.utils.rgb(70, 134, 250),
            0: svgwrite.utils.rgb(49, 18, 59),
        }.get(note.note % NUM_NOTES, "black")
        draw_note(note, position, color)


def draw_staff(origin: Point, width: float) -> None:
    for i in range(8):
        line_width = line_width_at_index(i)
        if line_width > 0:
            line_y = origin.y + STAFF_HEIGHT - (i * HALF_STAFF_SPACE)
            svg.line(
                Point(origin.x, line_y),
                Point(origin.x + width, line_y),
                line_width,
            )


def draw_staves(origin: Point, count: int, width: float) -> None:
    for i in range(count):
        draw_staff(Point(origin.x, origin.y + (i * STAFF_HEIGHT)), width)


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
