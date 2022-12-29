from collections import defaultdict
from typing import Any, Iterator, List, Optional, Tuple

from parse import Note
from svg import SVG, Point

NUM_NOTES = 7
"""
Number of notes on the diatonic scale.
"""

SCALE = 0.5
"""
Rendering scale.
"""

STAFF_WIDTH = 15

NOTE_HSCALE = SCALE * 110
"""
Horizontal scale between notes.
"""

MAX_X = STAFF_WIDTH * NOTE_HSCALE

STAFF_SPACE_HEIGHT = SCALE * 19

HALF_STAFF_SPACE = STAFF_SPACE_HEIGHT / 2
STAFF_HEIGHT = NUM_NOTES * HALF_STAFF_SPACE

NOTE_SIZE = (5 / 4.75) * HALF_STAFF_SPACE
"""
Note scale.
"""

TOP_STAVE_PADDING = 3 * STAFF_HEIGHT
"""
Top padding on first page (which has the title) to the first staff.
"""

PART_GAP_HEIGHT = 2 * STAFF_HEIGHT
"""
Padding between staves within the grand staff.
"""

GAP_HEIGHT = 3 * STAFF_HEIGHT
"""
Padding between the wrapped grand staff.
"""

THIN_LINE_WIDTH = SCALE * 1.3
"""
Width of thin lines.
"""

THICK_LINE_WIDTH = 2.8 * THIN_LINE_WIDTH
"""
Width of thick lines.
"""


def draw_note(svg: SVG, note: Note, point: Point) -> None:
    RX = 0.9 * 1.1 * NOTE_SIZE
    RY = 0.63 * 0.95 * NOTE_SIZE
    ANGLE = -20
    accidental = note.accidental
    if accidental == "natural":
        svg.ellipse(point, RX, RY, ANGLE, "white", "black", THICK_LINE_WIDTH)
    elif accidental == "sharp":
        svg.ellipse(point, RX, RY, ANGLE, "black", "black", THICK_LINE_WIDTH)


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
            origin.x + (note.time * NOTE_HSCALE),
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


def get_num_staves(notes: List[Note]) -> int:
    if not notes:
        return 1
    max_note = max(note.note for note in notes)
    if max_note == 0:
        return 1
    r = max_note // NUM_NOTES
    q = max_note % NUM_NOTES
    if q == 0:
        return r
    return r + 1


def draw_notes_with_staves(
    svg: SVG, origin: Point, notes: List[Note], width: float
) -> float:
    num_staves = get_num_staves(notes)
    height = num_staves * STAFF_HEIGHT
    draw_staves(svg, origin, num_staves, width)
    draw_notes(svg, Point(origin.x, origin.y + height), notes)
    return height


def get_staves_height(score: List[List[Note]]) -> float:
    staves_count = [get_num_staves(notes) for notes in score]
    # gap + staff heights
    staves_height = ((len(staves_count) - 1) * PART_GAP_HEIGHT) + sum(
        staves_count
    ) * STAFF_HEIGHT
    return staves_height


def draw_score_row(
    svg: SVG,
    origin: Point,
    score: List[List[Note]],
    staff_width: float,
    staves_height: float,
) -> None:
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
    y: float = 0
    for notes in score:
        height = draw_notes_with_staves(
            svg, Point(origin.x, origin.y + y), notes, staff_width
        )
        y += height + PART_GAP_HEIGHT


def draw_score_rows(
    title: str,
    subtitle: str,
    score_rows: List[List[List[Note]]],
    staff_width: float,
    max_y: float,
) -> List[SVG]:
    svgs = []
    svg, origin = new_page((title, subtitle))
    point = Point(origin.x, origin.y)
    for row in score_rows:
        row = [list(normalize_notes(notes)) for notes in row]
        height = get_staves_height(row)
        if point.y + height > max_y:
            svgs.append(svg)
            svg, origin = new_page()
            point = Point(origin.x, origin.y)
            draw_score_row(svg, point, row, staff_width, height)
            point = Point(point.x, point.y + height + GAP_HEIGHT)
        else:
            draw_score_row(svg, point, row, staff_width, height)
            point = Point(point.x, point.y + height + GAP_HEIGHT)
    svgs.append(svg)
    return svgs


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


def getindex(v: List[Any], i: int, default: Any) -> Any:
    if 0 <= i < len(v):
        return v[i]
    return default


def zip_score_rows(score_rows: List[List[List[Note]]]) -> List[List[List[Note]]]:
    d = []
    # Find the length of the longest part
    max_len = max(len(part) for part in score_rows)
    # Zip the rows of all parts, filling in with empty lists if necessary
    for i in range(max_len):
        d.append([getindex(part, i, []) for part in score_rows])
    return d


# return page and origin
def new_page(title: Optional[Tuple[str, str]] = None) -> Tuple[SVG, Point]:
    svg = SVG(margin_w=int(2 * STAFF_HEIGHT), margin_h=int(3 * STAFF_HEIGHT))
    if not title:
        origin = Point(0, 0)
        return svg, origin
    svg.text(Point(MAX_X / 2, -20), title[0], 25, "bold")
    svg.text(Point(MAX_X / 2, 20), title[1], 20)
    origin = Point(0, TOP_STAVE_PADDING)
    return svg, origin


def render(
    score: List[List[Note]], title: str, subtitle: str, yratio: float
) -> List[SVG]:
    a = [list(split_note_rows(notes, STAFF_WIDTH)) for notes in score]
    b = zip_score_rows(a)

    max_y = MAX_X * yratio
    svgs = draw_score_rows(title, subtitle, b, MAX_X, max_y)

    return svgs
