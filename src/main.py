import argparse
from pathlib import Path

from parse import parse
from render import render


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=Path)
    parser.add_argument("title")
    args = parser.parse_args()

    subtitle, title = args.title.split("{sub}", 1)

    print(render(parse(args.file), title, subtitle))


if __name__ == "__main__":
    main()
