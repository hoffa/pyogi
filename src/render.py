from typing import Iterator, List

from parse import Note
from svg import SVG, Point

NUM_NOTES = 7

WHOLE_NOTE_WIDTH = 100
STAFF_SPACE_HEIGHT = 17
EDGE_NOTE_PADDING = 2 * STAFF_SPACE_HEIGHT
HALF_STAFF_SPACE = STAFF_SPACE_HEIGHT / 2
STAFF_HEIGHT = NUM_NOTES * HALF_STAFF_SPACE
NOTE_SIZE = 10

NOTE_RX = 1.1 * NOTE_SIZE
NOTE_RY = 0.95 * 0.7 * NOTE_SIZE

THIN_LINE_WIDTH = 1
THICK_LINE_WIDTH = 2 * THIN_LINE_WIDTH


def draw_note(svg: SVG, note: Note, point: Point) -> None:
    accidental = note.accidental
    if accidental == "natural":
        svg.ellipse(point, 0.9 * NOTE_RX, NOTE_RY, -25)
    elif accidental == "sharp":
        svg.polygon(
            [
                Point(point.x - NOTE_RX, point.y - NOTE_RY),
                Point(point.x - NOTE_RX, point.y + NOTE_RY),
                Point(point.x + (1.2 * NOTE_RX), point.y),
            ],
        )


def line_width_at_index(index: int) -> int:
    index %= NUM_NOTES
    if index == 0:
        return THICK_LINE_WIDTH
    if index in [2, 5]:
        return THIN_LINE_WIDTH
    return 0


def draw_notes(svg: SVG, origin: Point, notes: List[Note]) -> None:
    for note in notes:
        position = Point(
            origin.x + (note.time * WHOLE_NOTE_WIDTH),
            origin.y - (note.note * HALF_STAFF_SPACE),
        )
        draw_note(svg, note, position)


def draw_staff(svg: SVG, origin: Point, width: float) -> None:
    for i in range(8):
        line_width = line_width_at_index(i)
        if line_width > 0:
            line_y = origin.y + STAFF_HEIGHT - (i * HALF_STAFF_SPACE)
            svg.line(
                Point(origin.x, line_y),
                Point(origin.x + width, line_y),
                line_width,
            )
    svg.line(origin, Point(origin.x, origin.y + STAFF_HEIGHT), THICK_LINE_WIDTH)
    svg.line(
        Point(origin.x + width, origin.y),
        Point(origin.x + width, origin.y + STAFF_HEIGHT),
        THICK_LINE_WIDTH,
    )


def draw_staves(svg: SVG, origin: Point, count: int, width: float) -> None:
    for i in range(count):
        draw_staff(svg, Point(origin.x, origin.y + (i * STAFF_HEIGHT)), width)


def normalize_notes(notes: List[Note]) -> Iterator[Note]:
    # Shift everything as much as possible
    min_note = min(note.note for note in notes)
    sub = (min_note // NUM_NOTES) * NUM_NOTES
    for note in notes:
        yield Note(
            note.time,
            note.note - sub,
            note.accidental,
        )


def get_width(notes: List[Note]) -> float:
    return max(note.time for note in notes) * WHOLE_NOTE_WIDTH


def draw_notes_with_staves(
    svg: SVG, origin: Point, notes: List[Note], width: float
) -> float:
    max_note = max(note.note for note in notes)
    num_staves = (max_note // NUM_NOTES) + 1
    height = num_staves * STAFF_HEIGHT
    draw_staves(svg, origin, num_staves, width + (2 * EDGE_NOTE_PADDING))
    draw_notes(svg, Point(origin.x + EDGE_NOTE_PADDING, origin.y + height), notes)
    return height


def render(score: List[List[Note]]) -> str:
    svg = SVG(margin_w=int(STAFF_HEIGHT), margin_h=int(STAFF_HEIGHT))
    width = max(get_width(notes) for notes in score)
    y: float = 0
    for notes in score:
        notes = list(normalize_notes(notes))
        height = draw_notes_with_staves(svg, Point(0, y), notes, width)
        y += height + STAFF_HEIGHT
    return str(svg)
