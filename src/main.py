import argparse

from parse import parse
from render import render


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()

    print(render(list(parse(args.file))))


if __name__ == "__main__":
    main()
