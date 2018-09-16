#!/usr/bin/env python3

import json
import math
import sys

import cairosvg
import svgwrite

NUM_NOTES = 7

STAFF_SPACE_HEIGHT = 10
HALF_STAFF_SPACE_HEIGHT = STAFF_SPACE_HEIGHT / 2
STAFF_HEIGHT = NUM_NOTES * HALF_STAFF_SPACE_HEIGHT
PART_HEIGHT = 5 * STAFF_HEIGHT

LINE_WIDTH = 1
THICK_LINE_WIDTH = 2 * LINE_WIDTH
NOTE_SIZE = 0.95 * STAFF_SPACE_HEIGHT

MARGIN_SIZE = 100
WHOLE_NOTE_WIDTH = 200


class SVG:
    def __init__(self, margin):
        self.svg = svgwrite.Drawing()
        self.margin = margin

    def add(self, element):
        self.svg.add(element).translate(self.margin, self.margin)
        return element

    def line(self, start, end, line_width):
        return self.add(
            self.svg.line(start, end, stroke="black", stroke_width=line_width)
        )

    def polygon(self, points):
        return self.add(self.svg.polygon(points, fill="black"))

    def ellipse(self, center, r):
        return self.add(self.svg.ellipse(center, r, fill="black"))

    def text(self, origin, s):
        return self.add(self.svg.text(s, insert=origin))

    def export_pdf(self, filename, width, height):
        cairosvg.svg2pdf(
            bytestring=self.svg.tostring(),
            write_to=filename,
            parent_width=width + (2 * self.margin),
            parent_height=height + (2 * self.margin),
        )


svg = SVG(MARGIN_SIZE)


def get_stem_height(length):
    if length == 1:
        return 0
    return (math.log2(1 / length) + 1) * STAFF_SPACE_HEIGHT


def draw_notehead_flat(x, y):
    width = 1.5 * NOTE_SIZE
    svg.polygon(
        [
            (x, y),
            (x + (0.55 * width), y),
            (x + width, y + NOTE_SIZE),
            (x + (0.45 * width), y + NOTE_SIZE),
        ]
    ).translate(-0.5 * THICK_LINE_WIDTH, -0.5 * NOTE_SIZE)


def draw_notehead_sharp(x, y):
    svg.polygon(
        [(x, y), (x + (1.5 * NOTE_SIZE), y + (0.5 * NOTE_SIZE)), (x, y + NOTE_SIZE)]
    ).translate(-0.5 * THICK_LINE_WIDTH, -0.5 * NOTE_SIZE)


def draw_notehead_natural(x, y):
    head = svg.ellipse((x, y), (0.6 * NOTE_SIZE, 0.42 * NOTE_SIZE))
    head.translate(0.462 * NOTE_SIZE)
    head.rotate(-35, center=(x, y))


def draw_note(x, y, accidental, length):
    stem_y = y
    if accidental == "flat":
        stem_y -= 0.5 * NOTE_SIZE
        draw_notehead_flat(x, y)
    elif accidental == "sharp":
        draw_notehead_sharp(x, y)
    elif accidental == "natural":
        stem_y += 0.15 * NOTE_SIZE
        draw_notehead_natural(x, y)
    svg.line((x, stem_y), (x, y + get_stem_height(length)), THICK_LINE_WIDTH)


def line_width_at_index(index):
    index %= NUM_NOTES
    if index == 0:
        return THICK_LINE_WIDTH
    elif index % 2 == 0:
        return LINE_WIDTH
    else:
        return 0


def draw_ledger_lines(x, y, index):
    indices = range(index + 1) if index >= 0 else range(index, 1)
    for i in indices:
        line_width = line_width_at_index(i)
        if line_width > 0:
            line_y = y - (i * HALF_STAFF_SPACE_HEIGHT)
            svg.line((x - NOTE_SIZE, line_y), (x + (2 * NOTE_SIZE), line_y), line_width)


def draw_notes(x, y, notes):
    y += 2 * STAFF_HEIGHT
    for i, note in enumerate(notes):
        note_x = x + (note["time"] * WHOLE_NOTE_WIDTH)
        note_y = y - (note["index"] * HALF_STAFF_SPACE_HEIGHT)
        draw_ledger_lines(note_x, y, note["index"])
        draw_note(note_x, note_y, note["accidental"], note["duration"])
        if i > 0:
            delta_shift = notes[i]["shift"] - notes[i - 1]["shift"]
            if delta_shift:
                svg.text((note_x, y), delta_shift)


def draw_staff(x, y, width):
    for i in range(8):
        line_width = line_width_at_index(i)
        if line_width > 0:
            line_y = y + STAFF_HEIGHT - (i * HALF_STAFF_SPACE_HEIGHT)
            svg.line((x, line_y), (x + width, line_y), line_width)


def draw_staves(x, y, width):
    for i in (1, 2):
        draw_staff(x, y + (i * STAFF_HEIGHT), width)
    svg.line((x, y + STAFF_HEIGHT), (x, y + (3 * STAFF_HEIGHT)), LINE_WIDTH)


def get_notes_width(notes):
    return max(note["time"] + note["duration"] for note in notes)


def render(score):
    y = 0
    for part in score:
        x = 0
        for notes in part:
            width = get_notes_width(notes) * WHOLE_NOTE_WIDTH
            draw_staves(x, y, width)
            draw_notes(x, y, notes)
            x += width
        y += PART_HEIGHT
    svg.export_pdf("out.pdf", x, y)


def main():
    render(json.load(sys.stdin))


if __name__ == "__main__":
    main()
