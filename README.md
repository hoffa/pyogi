
# notation

[![Tests](https://github.com/hoffa/notation/actions/workflows/build.yml/badge.svg)](https://github.com/hoffa/notation/actions/workflows/build.yml)

A simpler music notation for piano learners.

Under development, so changes are expected.

## Comparison

Here's the beginning of Beethoven's Für Elise in modern musical notation:

![](media/modern.png)

And here using the proposed notation (see [here](https://raw.githubusercontent.com/hoffa/notation/main/testdata/output/fur-elise.svg) for the full composition):

![](media/example.svg)

## The notation in 1 minute

![](media/staff.svg)

- Thick lines are [C notes](https://en.wikipedia.org/wiki/C_(musical_note)).
- Circles are naturals (i.e. white keys).
- Triangles are sharps (i.e. black keys).

There are no explicit flats, rests, note values, time signatures, key signatures, etc.

The notation gets you started, you do the rest. Play what sounds good.

## Usage

```bash
./render.sh score.mxl > score.svg
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
