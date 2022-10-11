from typing import List

from parse import Note
from svg import SVG, Point

svg = SVG(margin=50)


NUM_NOTES = 7

WHOLE_NOTE_WIDTH = 50
STAFF_SPACE_HEIGHT = 10
EDGE_NOTE_PADDING = 2 * STAFF_SPACE_HEIGHT
HALF_STAFF_SPACE = STAFF_SPACE_HEIGHT / 2
STAFF_HEIGHT = NUM_NOTES * HALF_STAFF_SPACE


def draw_note(note: Note, point: Point, color: str) -> None:
    accidental = note.accidental
    if accidental == "natural":
        svg.circle(point, HALF_STAFF_SPACE, color)
    elif accidental == "sharp":
        svg.polygon(
            [
                Point(point.x - HALF_STAFF_SPACE, point.y - HALF_STAFF_SPACE),
                Point(point.x - HALF_STAFF_SPACE, point.y + HALF_STAFF_SPACE),
                Point(point.x + HALF_STAFF_SPACE, point.y),
            ],
            color,
        )


def line_width_at_index(index: int) -> int:
    index %= NUM_NOTES
    if index == 0:
        return 2
    if index in [2, 5]:
        return 1
    return 0


def draw_notes(origin: Point, notes: List[Note]) -> None:
    for note in notes:
        position = Point(
            origin.x + (note.time * WHOLE_NOTE_WIDTH),
            # TODO: Should normalize to lowest modulo 7 otherwise kind of arbitrary?
            origin.y - (note.note * HALF_STAFF_SPACE),
        )
        color = {
            0: "black",
            1: "red",
            2: "blue",
        }.get(note.part, "black")
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
    draw_notes(Point(EDGE_NOTE_PADDING, (num_staves + 0) * STAFF_HEIGHT), score)
    return str(svg)
