#!/usr/bin/env python3

import json
import math
import sys

import cairosvg
import svgwrite

NUM_NOTES = 7

MARGIN_SIZE = 100
WHOLE_NOTE_WIDTH = 250
STAFF_SPACE_HEIGHT = 10

NOTE_SIZE = 0.8 * STAFF_SPACE_HEIGHT
HALF_STAFF_SPACE_HEIGHT = STAFF_SPACE_HEIGHT / 2
STAFF_HEIGHT = NUM_NOTES * HALF_STAFF_SPACE_HEIGHT
PART_HEIGHT = 5 * STAFF_HEIGHT
LINE_WIDTH = 1
THICK_LINE_WIDTH = 2 * LINE_WIDTH
STAFF_COLOR = "lightgray"


class SVG:
    def __init__(self, margin):
        self.svg = svgwrite.Drawing()
        self.margin = margin

    def add(self, element):
        self.svg.add(element).translate(self.margin, self.margin)
        return element

    def line(self, start, end, line_width, stroke="black"):
        return self.add(
            self.svg.line(start, end, stroke_width=line_width, stroke=stroke)
        )

    def circle(self, center, r):
        return self.add(self.svg.circle(center, r, fill="black"))

    def hollow_circle(self, center, r, stroke_width):
        return self.add(
            self.svg.circle(
                center, r, stroke_width=stroke_width, stroke="black", fill="white"
            )
        )

    def half_circle(self, x, y, r, angle_dir):
        p = svgwrite.path.Path(d=("M", x - r, y))
        p.push_arc((2 * r, 0), 0, 1, 0, angle_dir=angle_dir)
        return self.add(p)

    def text(self, origin, s):
        return self.add(self.svg.text(s, insert=origin))

    def export_pdf(self, filename, width, height):
        cairosvg.svg2pdf(
            bytestring=self.svg.tostring(),
            write_to=filename,
            parent_width=width + (2 * self.margin),
            parent_height=height + (2 * self.margin),
        )
        print(f"Rendered to {filename}")


svg = SVG(MARGIN_SIZE)


def draw_notehead_flat(x, y):
    svg.hollow_circle((x, y), (NOTE_SIZE - LINE_WIDTH) / 2, LINE_WIDTH)
    svg.half_circle(x, y, NOTE_SIZE / 2, "-")


def draw_notehead_sharp(x, y):
    svg.hollow_circle((x, y), (NOTE_SIZE - LINE_WIDTH) / 2, LINE_WIDTH)
    svg.half_circle(x, y, NOTE_SIZE / 2, "+")


def draw_notehead_natural(x, y):
    svg.circle((x, y), NOTE_SIZE / 2)


def draw_note(x, y, accidental, length):
    svg.line((x, y), (x + (length * WHOLE_NOTE_WIDTH), y), LINE_WIDTH)
    if accidental == "flat":
        draw_notehead_flat(x, y)
    elif accidental == "sharp":
        draw_notehead_sharp(x, y)
    elif accidental == "natural":
        draw_notehead_natural(x, y)


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
            svg.line(
                (x - NOTE_SIZE, line_y),
                (x + NOTE_SIZE, line_y),
                line_width,
                stroke=STAFF_COLOR,
            )


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
            svg.line((x, line_y), (x + width, line_y), line_width, stroke=STAFF_COLOR)


def draw_staves(x, y, width):
    for i in (1, 2):
        draw_staff(x, y + (i * STAFF_HEIGHT), width)
    svg.line(
        (x, y + STAFF_HEIGHT),
        (x, y + (3 * STAFF_HEIGHT)),
        LINE_WIDTH,
        stroke=STAFF_COLOR,
    )


def get_notes_width(notes):
    return max(note["time"] + note["duration"] for note in notes)


def main():
    y = 0
    for part in json.load(sys.stdin):
        x = 0
        for notes in part:
            width = get_notes_width(notes) * WHOLE_NOTE_WIDTH
            draw_staves(x, y, width)
            draw_notes(x, y, notes)
            x += width
        y += PART_HEIGHT
    svg.export_pdf("out.pdf", x, y)


if __name__ == "__main__":
    main()
