#!/usr/bin/env python3

import argparse
import json

import music21

NUM_NOTES = 7


def pitch_accidental(pitch):
    if pitch.accidental:
        if "sharp" in pitch.accidental.name:
            return "sharp"
        elif "flat" in pitch.accidental.name:
            return "flat"
    return "natural"


def shift_notes_by_octaves(notes, a, b, num_octaves):
    for i in range(a, b):
        notes[i]["index"] += num_octaves * NUM_NOTES
        notes[i]["shift"] += num_octaves


def adjust_notes(notes, clefs):
    for i in range(len(clefs) - 1):
        a, b = clefs[i], clefs[i + 1]
        indices = [note["index"] for note in notes[a:b]]
        min_octave = min(indices) // NUM_NOTES
        octave_range = (max(indices) - min(indices)) // NUM_NOTES
        shift_notes_by_octaves(notes, a, b, -min_octave - (octave_range // 2))


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
                "shift": 0,
            }


def notes_from_chord(chord):
    for pitch in chord.pitches:
        yield {
            "time": float(chord.offset / 4),
            "index": pitch.diatonicNoteNum - 1,
            "duration": float(chord.duration.quarterLength / 4),
            "accidental": pitch_accidental(pitch),
            "shift": 0,
        }


def process_part(part):
    notes = []
    measures = {0}
    clefs = {0}
    for measure in part.makeMeasures():
        measures.add(len(notes))
        for note in measure:
            if "Spanner" in note.classes:
                notes.extend(notes_from_spanner(note))
            elif "Note" in note.classes or "Chord" in note.classes:
                notes.extend(notes_from_chord(note))
            elif "Clef" in note.classes:
                clefs.add(len(notes))
    measures.add(len(notes))
    clefs.add(len(notes))
    return notes, sorted(measures), sorted(clefs)


def parse(filename):
    for part in music21.converter.parse(filename).parts:
        flat_notes, measure_pos, clef_pos = process_part(part)
        adjust_notes(flat_notes, clef_pos)
        yield list(split_by_indices(flat_notes, measure_pos))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()
    print(json.dumps(list(parse(args.file))))


if __name__ == "__main__":
    main()
