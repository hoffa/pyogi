from typing import Iterator, List

from parse import Note
from svg import SVG, Point

NUM_NOTES = 7

SCALE = 0.5

WHOLE_NOTE_WIDTH = SCALE * 110
STAFF_SPACE_HEIGHT = SCALE * 17
EDGE_NOTE_PADDING = 2 * STAFF_SPACE_HEIGHT
HALF_STAFF_SPACE = STAFF_SPACE_HEIGHT / 2
STAFF_HEIGHT = NUM_NOTES * HALF_STAFF_SPACE
NOTE_SIZE = SCALE * 10

NOTE_RX = 1.1 * NOTE_SIZE
NOTE_RY = 0.95 * 0.7 * NOTE_SIZE

THIN_LINE_WIDTH = SCALE * 1.3
THICK_LINE_WIDTH = 2 * THIN_LINE_WIDTH


def draw_note(svg: SVG, note: Note, point: Point) -> None:
    accidental = note.accidental
    if accidental == "natural":
        svg.ellipse(point, 0.9 * NOTE_RX, NOTE_RY, -25)
    elif accidental == "sharp":
        x_left = point.x - (0.875 * NOTE_RX)
        svg.polygon(
            [
                Point(x_left, point.y - 1.1 * NOTE_RY),
                Point(x_left, point.y + 1.1 * NOTE_RY),
                Point(point.x + (1.2 * NOTE_RX), point.y),
            ],
        )


def line_width_at_index(index: int) -> float:
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


def get_num_staves(notes: List[Note]) -> int:
    max_note = max(note.note for note in notes)
    num_staves = (max_note // NUM_NOTES) + 1
    return num_staves


def draw_notes_with_staves(
    svg: SVG, origin: Point, notes: List[Note], width: float
) -> float:
    num_staves = get_num_staves(notes)
    height = num_staves * STAFF_HEIGHT
    draw_staves(svg, origin, num_staves, width)
    draw_notes(svg, Point(origin.x + EDGE_NOTE_PADDING, origin.y + height), notes)
    return height


TOP_STAVE_PADDING = STAFF_HEIGHT


def render(score: List[List[Note]], title: str) -> str:
    score = [list(normalize_notes(notes)) for notes in score]
    svg = SVG(margin_w=int(STAFF_HEIGHT), margin_h=int(3 * STAFF_HEIGHT))

    svg.text(Point(0, 0), title, 25)

    width = max(get_width(notes) for notes in score) + (2 * EDGE_NOTE_PADDING)
    staves_count = [get_num_staves(notes) for notes in score]
    # gap + staff heights
    staves_height = ((len(staves_count) - 1) * STAFF_HEIGHT) + sum(
        staves_count
    ) * STAFF_HEIGHT
    y = TOP_STAVE_PADDING
    for notes in score:
        height = draw_notes_with_staves(svg, Point(0, y), notes, width)
        y += height + STAFF_HEIGHT
    svg.line(
        Point(0, TOP_STAVE_PADDING),
        Point(0, TOP_STAVE_PADDING + staves_height),
        THICK_LINE_WIDTH,
    )
    svg.line(
        Point(width, TOP_STAVE_PADDING),
        Point(width, TOP_STAVE_PADDING + staves_height),
        THICK_LINE_WIDTH,
    )
    return str(svg)
