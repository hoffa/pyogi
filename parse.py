import argparse
import json
from typing import Iterator, List, Literal, TypedDict

import music21
from music21.pitch import Pitch
from music21.stream import Score, Part

Accidental = Literal["natural", "flat", "sharp"]


class Note(TypedDict):
    time: float
    note: int
    accidental: Accidental


def get_pitch_accidental(pitch: Pitch) -> Accidental:
    if pitch.accidental:
        if "sharp" in pitch.accidental.name:
            return "sharp"
        if "flat" in pitch.accidental.name:
            return "flat"
    return "natural"


def get_notes(part: Part) -> Iterator[Note]:
    for note in part.flat.notes:
        for pitch in note.pitches:
            yield Note(
                time=float(note.offset),
                note=pitch.diatonicNoteNum - 1,
                accidental=get_pitch_accidental(pitch),
            )


def parse(filename: str) -> Iterator[List[Note]]:
    score = music21.converter.parse(filename)
    if isinstance(score, Score):
        for part in score.parts:
            yield list(get_notes(part))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()

    print(json.dumps(list(parse(args.file))))


main()
