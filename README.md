
# notation

[![Tests](https://github.com/hoffa/notation/actions/workflows/build.yml/badge.svg)](https://github.com/hoffa/notation/actions/workflows/build.yml)

A simpler music notation for piano learners.

Under development, so changes are expected.

## Comparison

Here's the beginning of Claude Debussy's [Arabesque No. 1](https://en.wikipedia.org/wiki/Two_Arabesques) in modern musical notation:

![](media/modern.png)

And here using the proposed notation (see [here](https://raw.githubusercontent.com/hoffa/notation/main/testdata/output/fur-elise.svg) for the full composition):

![](testdata/output/debussy-deux-arabesques-short.svg)

## The notation in 1 minute

- Lines are [C notes](https://en.wikipedia.org/wiki/C_(musical_note)).
- Each note has a different color.
- Circles are naturals (i.e. white keys).
- Triangles are sharps (i.e. black keys).

There are no explicit flats, rests, note values, time signatures, key signatures, etc. Play what sounds good.

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
