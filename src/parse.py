import argparse
import json
from typing import Iterator, Literal, TypedDict

import music21
from music21.stream import Score

Accidental = Literal["natural", "sharp"]


class Note(TypedDict):
    time: float
    note: int
    accidental: Accidental


def parse(filename: str) -> Iterator[Note]:
    score = music21.converter.parse(filename)
    if isinstance(score, Score):
        for part in score.parts:
            for note in part.flat.notes:
                time = float(note.offset)
                for pitch in note.pitches:
                    note = pitch.diatonicNoteNum - 1
                    accidental = (
                        pitch.accidental.name if pitch.accidental else "natural"
                    )
                    # Convert flats to sharps
                    # TODO: Check correct and handle doubles
                    if "flat" in accidental:
                        note -= 1
                        accidental = "sharp"
                    # TODO: Handle doubles; this might be wrong
                    if "sharp" in accidental:
                        accidental = "sharp"
                    yield Note(
                        time=time,
                        note=note,
                        accidental=accidental,
                    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()

    print(json.dumps(list(parse(args.file))))


if __name__ == "__main__":
    main()
