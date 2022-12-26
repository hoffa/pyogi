import sys
from collections import defaultdict
from typing import Any, Iterator, List

from parse import Note
from svg import SVG, Point

NUM_NOTES = 7

SCALE = 0.5

WHOLE_NOTE_WIDTH = SCALE * 110
STAFF_SPACE_HEIGHT = SCALE * 19
EDGE_NOTE_PADDING = 2 * STAFF_SPACE_HEIGHT
HALF_STAFF_SPACE = STAFF_SPACE_HEIGHT / 2
STAFF_HEIGHT = NUM_NOTES * HALF_STAFF_SPACE
NOTE_SIZE = SCALE * 10

NOTE_RX = 1.1 * NOTE_SIZE
NOTE_RY = 0.95 * 0.7 * NOTE_SIZE

THIN_LINE_WIDTH = SCALE * 1.3
THICK_LINE_WIDTH = 2.8 * THIN_LINE_WIDTH


def draw_note(svg: SVG, note: Note, point: Point) -> None:
    accidental = note.accidental
    if accidental == "natural":
        svg.ellipse(
            point, 0.9 * NOTE_RX, 0.8 * NOTE_RY, -20, "white", "black", THICK_LINE_WIDTH
        )
    elif accidental == "sharp":
        svg.ellipse(point, 0.9 * NOTE_RX, 0.8 * NOTE_RY, -20)


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
    if not notes:
        return
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
    if not notes:
        return 1
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


TOP_STAVE_PADDING = 3 * STAFF_HEIGHT
PART_GAP_HEIGHT = 2 * STAFF_HEIGHT


def draw_score_row(
    svg: SVG, origin: Point, score: List[List[Note]], staff_width: float
) -> float:
    staves_count = [get_num_staves(notes) for notes in score]
    # gap + staff heights
    staves_height = ((len(staves_count) - 1) * PART_GAP_HEIGHT) + sum(
        staves_count
    ) * STAFF_HEIGHT
    y: float = 0
    for notes in score:
        height = draw_notes_with_staves(
            svg, Point(origin.x, origin.y + y), notes, staff_width
        )
        y += height + PART_GAP_HEIGHT
    svg.line(
        Point(origin.x, origin.y),
        Point(origin.x, origin.y + staves_height),
        THICK_LINE_WIDTH,
    )
    svg.line(
        Point(origin.x + staff_width, origin.y),
        Point(origin.x + staff_width, origin.y + staves_height),
        THICK_LINE_WIDTH,
    )
    return staves_height


def draw_score_rows(
    svg: SVG, origin: Point, score_rows: List[List[List[Note]]], staff_width: float
) -> None:
    point = Point(origin.x, origin.y)
    for row in score_rows:
        row = [list(normalize_notes(notes)) for notes in row]
        height = draw_score_row(svg, point, row, staff_width)
        point.y += height + (3 * STAFF_HEIGHT)


def split_note_rows(notes: List[Note], row_length: float) -> Iterator[List[Note]]:
    # TODO: should row_length be based on whole note and not absolute x?
    # Maybe that'll cut it off at more natural place!
    r = defaultdict(list)
    for note in notes:
        x = note.time % row_length
        row = note.time // row_length
        r[row].append(
            Note(
                time=x,
                note=note.note,
                accidental=note.accidental,
            )
        )
    for row in range(len(r)):
        yield r[row]


# split of each row in original score, gives more rows
# then zip up each by index

#
# [[1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2], ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l']]
#              to
# [ [ [1, 2, 3, 4], [5, 6, 7, 8], [9, 0, 1, 2]], [['a', 'b', 'c', 'd'], ['e', 'f', 'g', 'h'], ['i', 'j', 'k', 'l'] ] ]
#              to
# [[[1, 2, 3, 4], ['a', 'b', 'c', 'd']], [[5, 6, 7, 8], ['e', 'f', 'g', 'h']], [[9, 0, 1, 2], ['i', 'j', 'k', 'l']]]
#
# need to know how many parts fixed, n rows


def log(*v: Any) -> None:
    print(v, file=sys.stderr)


def getindex(v: List[Any], i: int, default: Any) -> Any:
    if 0 <= i < len(v):
        return v[i]
    return default


def zip_score_rows(score_rows: List[List[List[Note]]]) -> List[List[List[Note]]]:
    d = []
    # TODO: Support more than 2 parts
    v = score_rows[0]
    w = score_rows[1]
    for i in range(len(score_rows[0])):
        d.append([getindex(v, i, []), getindex(w, i, [])])
    return d


def render(score: List[List[Note]], title: str) -> str:
    svg = SVG(margin_w=int(2 * STAFF_HEIGHT), margin_h=int(3 * STAFF_HEIGHT))
    STAFF_WIDTH = 15

    svg.text(Point(STAFF_WIDTH * WHOLE_NOTE_WIDTH / 2, 0), title, 25)

    origin = Point(0, TOP_STAVE_PADDING)

    a = [
        list(
            split_note_rows(
                notes, STAFF_WIDTH - (2 * EDGE_NOTE_PADDING / WHOLE_NOTE_WIDTH)
            )
        )
        for notes in score
    ]
    b = zip_score_rows(a)

    draw_score_rows(svg, origin, b, STAFF_WIDTH * WHOLE_NOTE_WIDTH)

    return str(svg)
