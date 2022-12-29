from dataclasses import dataclass
from pathlib import Path
from typing import Iterator, List, Literal

import music21
from music21.stream import Part, Score

# https://github.com/cuthbertLab/music21/blob/1025c6cc5703e27ad5eb924c0098e11e3dd04f3b/music21/pitch.py#L93-L107
Accidental = Literal[
    "natural",
    "sharp",
]


@dataclass
class Note:
    time: float
    note: int  # note % 7 == 0 is C
    accidental: Accidental


def get_notes(part: Part) -> Iterator[Note]:
    for note in part.flat.notes:
        time = float(note.offset)
        for pitch in note.pitches:
            pitch.simplifyEnharmonic(inPlace=True)
            note = pitch.diatonicNoteNum - 1
            accidental = pitch.accidental.name if pitch.accidental else "natural"
            if accidental not in ["natural", "sharp", "flat"]:
                raise Exception("Unsupported accidental: " + accidental)
            if accidental == "flat":
                note -= 1
                accidental = "sharp"
            yield Note(
                time=time,
                note=note,
                accidental=accidental,
            )


def _parse(filename: Path) -> Iterator[List[Note]]:
    score = music21.converter.parse(filename)
    if isinstance(score, Score):
        for part in score.parts:
            yield list(get_notes(part))


def parse(filename: Path) -> List[List[Note]]:
    return list(_parse(filename))
