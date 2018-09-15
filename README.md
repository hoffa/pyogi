# notation

Reading music sheets is hard. I got frustrated with the inconsistencies and (what I perceived as) unnecessary complexity in modern music notation. All I want to know is where to put my fingers. Note length, tempo, velocity and other stuff are minor worries in comparison. Those things can be _felt_, without learning.

I wanted to create a simple and consistent music notation, along with parsers, converters and whatnot. Turns out writing beautiful renderers is tough, and it can get quite ugly with edge cases and the variety of sheets out there. I haven't yet had the motivation to finish the code, so instead for some peace of mind, I'm documenting the envisioned notation here.

This is written from the perspective of a clueless piano beginner who just wants to play.

## Staves

![](stave.svg)

* Thick lines always represent [C notes](https://en.wikipedia.org/wiki/C_(musical_note)), no matter the key.
* [Measures](https://en.wikipedia.org/wiki/Bar_(music)) are separated by vertical lines.
* [Time signatures](https://en.wikipedia.org/wiki/Time_signature) and [key signatures](https://en.wikipedia.org/wiki/Key_signature) are not shown.

## Notes

### Natural

![](natural.svg)

### Sharp

![](sharp.svg)

### Flat

![](flat.svg)

### Stem

Assuming `d` is the [note value](https://en.wikipedia.org/wiki/Note_value) (where 1 is a whole note), the stem length is `(log2(1 / d) + 1) * c`. If `d` is 1, the stem length is 0.

The longer the note, the shorter the stem.
