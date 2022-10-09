
# notation

[![Tests](https://github.com/hoffa/notation/actions/workflows/build.yml/badge.svg)](https://github.com/hoffa/notation/actions/workflows/build.yml)

A simpler music notation for piano learners.

## Example

Here's the beginning of Beethoven's Für Elise:

![](https://raw.githubusercontent.com/hoffa/notation/main/media/example.svg)

All you need to know is:

- Thick lines are [C notes](https://en.wikipedia.org/wiki/C_(musical_note)).
- Circles are naturals (i.e. white keys).
- Triangles are sharps (i.e. black keys).

There are no flats, rests, note values, time signatures, key signatures, etc. Play what sounds good.

## Usage

```bash
./render.sh score.mxl > score.svg
```
