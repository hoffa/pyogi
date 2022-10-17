import argparse
from pathlib import Path

from parse import parse
from render import render


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=Path)
    args = parser.parse_args()

    print(render(parse(args.file), args.file))


if __name__ == "__main__":
    main()
