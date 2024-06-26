# pyogi

[![Tests](https://github.com/hoffa/notation/actions/workflows/build.yml/badge.svg)](https://github.com/hoffa/notation/actions/workflows/build.yml)
[![CC BY-NC-ND 4.0](https://img.shields.io/badge/license-CC%20BY--NC--ND%204.0-blue)](https://creativecommons.org/licenses/by-nc-nd/4.0/)

A simpler music notation for casual piano learners.

## Why?

I'm bad at piano but I'm trying to learn by myself, and I find modern music notation overwhelming.

For example:

1. Why does the note corresponding to a line on the [staff](<https://en.wikipedia.org/wiki/Staff_(music)>) depend on (1) the [clef](https://en.wikipedia.org/wiki/Clef), (2) the [key signature](https://en.wikipedia.org/wiki/Key_signature), and (3) the [accidental](<https://en.wikipedia.org/wiki/Accidental_(music)>) next to a note? I need to look in 3 places just to know which key to press.
1. Why have both C♯ and D♭ when they correspond to the same key?
1. Why aren't staff lines for different [octaves](https://en.wikipedia.org/wiki/Octave) consistent? If a note is on a solid line, the same note one octave higher is on a blank line.

## Example

<details>
  <summary>Schubert's Allegretto in Pyogi notation</summary>

  ![](testdata/output/svg/schubert-allegretto.svg)
  
</details>

See the [`testdata/output/pdf`](testdata/output/pdf) directory for more examples.

## The notation in 1 minute

- Thick lines are [C notes](<https://en.wikipedia.org/wiki/C_(musical_note)>).
- The higher the note, the higher the pitch.
- White notes are naturals.
- Black notes are sharps.

There are no explicit flats, rests, note values, time signatures, key signatures, etc. Play what sounds good.

## Usage

Convert a [MusicXML](https://en.wikipedia.org/wiki/MusicXML) file to a PDF in Pyogi notation:

```bash
make init
.venv/bin/python src/main.py score.mxl
```

## Development

Set up dependencies:

```bash
make init
```

Run tests:

```bash
make test
```

If the rendering changes, tests can be quickly updated with:

```bash
UPDATE=1 make test
```
