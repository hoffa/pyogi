
# notation

[![Tests](https://github.com/hoffa/notation/actions/workflows/build.yml/badge.svg)](https://github.com/hoffa/notation/actions/workflows/build.yml)

A simpler music notation for piano learners.

- No explicit rests.
- No explicit note durations.
- No flats (only natural and sharp).
- Thick line is always C, regardless of the key.

## Example

Here's the beginning of Beethoven's Für Elise:

![](https://raw.githubusercontent.com/hoffa/notation/main/media/example.svg)

All you need to know is:

- Thick lines are [C notes](https://en.wikipedia.org/wiki/C_(musical_note)).
- Circles are naturals (i.e. white keys).
- Triangles are sharps (i.e. black keys).

## Usage

```bash
./render.sh score.mxl > score.svg
```

## FAQ

### How do I know which key to play?

Play what sounds good.
