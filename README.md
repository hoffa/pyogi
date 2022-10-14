
# notation

[![Tests](https://github.com/hoffa/notation/actions/workflows/build.yml/badge.svg)](https://github.com/hoffa/notation/actions/workflows/build.yml)

A simpler music notation for piano learners.

## Comparison

Here's the beginning of Claude Debussy's [Arabesque No. 1](https://en.wikipedia.org/wiki/Two_Arabesques) in modern musical notation:

![](media/modern.png)

And here using the proposed notation (see [here](https://raw.githubusercontent.com/hoffa/notation/main/testdata/output/debussy-deux-arabesques.svg) for the full composition) in a few different themes:

![](testdata/output/debussy-deux-arabesques-short-mono.svg)

![](testdata/output/debussy-deux-arabesques-short.svg)

![](testdata/output/debussy-deux-arabesques-short-turbo.svg)

See [`examples.md`](examples.md) for more examples.

## The notation in 1 minute

- Lines are [C notes](https://en.wikipedia.org/wiki/C_(musical_note)).
- Each note has a different color.
- The higher the note, the higher the pitch.
- Circles are naturals (i.e. white keys).
- Triangles are sharps (i.e. black keys).

There are no explicit flats, rests, note values, time signatures, key signatures, etc. Play what sounds good.

## Usage

```bash
./render.sh score.mxl > score.svg
```

Where `score.mxl` is a compressed [MusicXML](https://en.wikipedia.org/wiki/MusicXML) file.

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
