import argparse
from pathlib import Path

from common import parse_and_render


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=Path)
    args = parser.parse_args()

    print(parse_and_render(args.file))


if __name__ == "__main__":
    main()
