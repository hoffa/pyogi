import argparse
from typing import Dict

import svgwrite  # type: ignore

from parse import parse
from render import Theme, render

THEMES: Dict[str, Theme] = {
    # https://personal.sron.nl/~pault/
    "default": {
        "bg_color": "white",
        "colors": [
            "#000000",
            "#CC3311",
            "#EE3377",
            "#EE7733",
            "#0077BB",
            "#009988",
            "#33BBEE",
        ],
    },
    # https://ai.googleblog.com/2019/08/turbo-improved-rainbow-colormap-for.html
    "turbo": {
        "bg_color": "black",
        "colors": [
            svgwrite.utils.rgb(210, 49, 5),
            svgwrite.utils.rgb(251, 127, 34),
            svgwrite.utils.rgb(237, 208, 57),
            svgwrite.utils.rgb(164, 253, 61),
            svgwrite.utils.rgb(48, 241, 153),
            svgwrite.utils.rgb(45, 187, 236),
            svgwrite.utils.rgb(71, 107, 227),
        ],
    },
    "monochrome": {
        "bg_color": "white",
        "colors": [
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
            "black",
        ],
    },
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--theme", choices=THEMES.keys(), default="default")
    args = parser.parse_args()

    print(render(list(parse(args.file)), THEMES[args.theme]))


if __name__ == "__main__":
    main()
