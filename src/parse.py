import argparse
import json
from typing import Iterator, Literal, TypedDict

import music21
from music21.pitch import Pitch
from music21.stream import Score

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


def parse(filename: str) -> Iterator[Note]:
    score = music21.converter.parse(filename)
    if isinstance(score, Score):
        for part in score.parts:
            for note in part.flat.notes:
                for pitch in note.pitches:
                    yield Note(
                        time=float(note.offset),
                        note=pitch.diatonicNoteNum - 1,
                        accidental=get_pitch_accidental(pitch),
                    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()

    print(json.dumps(list(parse(args.file))))


if __name__ == "__main__":
    main()
