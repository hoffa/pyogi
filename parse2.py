#!/usr/bin/env python3

import json
import sys

import music21


def pitch_accidental(pitch):
    if pitch.accidental:
        if "sharp" in pitch.accidental.name:
            return "sharp"
        if "flat" in pitch.accidental.name:
            return "flat"
    return "natural"


def notes(part):
    for note in part.flat.notes:
        for pitch in note.pitches:
            yield {
                "time": note.offset,
                "note": pitch.diatonicNoteNum - 1,
                "duration": note.duration.quarterLength / 4,
                "accidental": pitch_accidental(pitch),
            }


def parse(filename):
    for part in music21.converter.parse(filename).parts:
        yield list(notes(part))


def main():
    print(json.dumps(list(parse(sys.argv[1]))))


if __name__ == "__main__":
    main()
