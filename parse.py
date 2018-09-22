#!/usr/bin/env python3

import argparse
import json

import music21


def pitch_accidental(pitch):
    if pitch.accidental:
        if "sharp" in pitch.accidental.name:
            return "sharp"
        elif "flat" in pitch.accidental.name:
            return "flat"
    return "natural"


def split_by_indices(xs, indices):
    indices = sorted(set(indices + [0, len(xs)]))
    for i in range(len(indices) - 1):
        yield xs[indices[i] : indices[i + 1]]


def notes_from_spanner(spanner):
    for element in spanner.getSpannedElements():
        for pitch in element.pitches:
            yield {
                "time": float(spanner.offset / 4),
                "index": pitch.diatonicNoteNum - 1,
                "duration": float(spanner.duration.quarterLength / 4),
                "accidental": pitch_accidental(pitch),
            }


def notes_from_chord(chord):
    for pitch in chord.pitches:
        yield {
            "time": float(chord.offset / 4),
            "index": pitch.diatonicNoteNum - 1,
            "duration": float(chord.duration.quarterLength / 4),
            "accidental": pitch_accidental(pitch),
        }


def process_part(part):
    notes = []
    measures = {0}
    for measure in part.makeMeasures():
        measures.add(len(notes))
        for note in measure:
            if "Spanner" in note.classes:
                notes.extend(notes_from_spanner(note))
            elif "Note" in note.classes or "Chord" in note.classes:
                notes.extend(notes_from_chord(note))
    measures.add(len(notes))
    return notes, sorted(measures)


def parse(filename):
    for part in music21.converter.parse(filename).parts:
        flat_notes, measure_pos = process_part(part)
        yield list(split_by_indices(flat_notes, measure_pos))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()
    print(json.dumps(list(parse(args.file))))


if __name__ == "__main__":
    main()
