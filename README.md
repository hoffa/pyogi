![Header](media/header.svg)

# 🎵 notation

[![Build Status](https://travis-ci.org/hoffa/notation.svg?branch=master)](https://travis-ci.org/hoffa/notation)

Reading music is hard.

I got frustrated with the inconsistencies and (what I perceived as) unnecessary complexity in modern music notation. All I want to know is where to put my fingers. Note length, tempo, velocity, progression and other stuff are minor worries in comparison. Those things can be _felt_, without learning.

I wanted to create a simple and consistent music notation, along with parsers, converters and whatnot. Turns out writing beautiful renderers is tough, and it can get quite ugly with edge cases and the variety of sheets out there. I haven't yet had the motivation to finish the code, so instead for some peace of mind, I'm documenting the envisioned notation here.

This is written from the perspective of a clueless piano beginner who just wants to play.

## Staves

![Staff](media/staff.svg)

* Thick lines always represent [C notes](https://en.wikipedia.org/wiki/C_(musical_note)), no matter the [key](https://en.wikipedia.org/wiki/Key_(music)).
* [Measures](https://en.wikipedia.org/wiki/Bar_(music)) are separated by vertical lines.
* [Time signatures](https://en.wikipedia.org/wiki/Time_signature) and [key signatures](https://en.wikipedia.org/wiki/Key_signature) are not shown.
* Changes in [octave](https://en.wikipedia.org/wiki/Octave) are indicated using a signed number at the start of the measure.

## Notes

[Note value](https://en.wikipedia.org/wiki/Note_value) and [accidental](https://en.wikipedia.org/wiki/Accidental_(music)) are encoded in the shape of the note.

[Natural](https://en.wikipedia.org/wiki/Natural_(music)), [sharp](https://en.wikipedia.org/wiki/Sharp_(music)) and [flat](https://en.wikipedia.org/wiki/Flat_(music)) notes have the following shapes:

![Notes](media/notes.svg)

### Rests

[Rests](https://en.wikipedia.org/wiki/Rest_(music)) aren't explicitly displayed.

### Stem length

Assuming `d` is the note value (where 1 is a whole note) and `h` is the size of the gap between staff lines, the stem length is `(log₂(1 / d) + 1) * h`. If `d` is 1, the stem length is 0.

For example, a [whole note](https://en.wikipedia.org/wiki/Whole_note) will have no stem, a [quarter note](https://en.wikipedia.org/wiki/Quarter_note) will have a stem length of `log₂(1 / 0.25) + 1 = 3` staff line gaps, an [eighth note](https://en.wikipedia.org/wiki/Eighth_note) will have a length of `log₂(1 / 0.125) + 1 = 4` staff line gaps, etc.

The longer the note, the shorter the stem.
