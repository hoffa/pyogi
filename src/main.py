import argparse

from parse import parse
from render import Theme, render

THEME: Theme = {
    "bg_color": "white",
    "staff_color": "black",
    "colors": [
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
        "black",
    ],
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()

    print(render(list(parse(args.file)), THEME))


if __name__ == "__main__":
    main()
