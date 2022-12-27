import argparse
from pathlib import Path

from parse import parse
from render import render


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=Path)
    parser.add_argument("title")
    parser.add_argument("--yratio", type=float, default=1.414)  # A4
    parser.add_argument("--export", action="store_true")
    args = parser.parse_args()

    subtitle, title = args.title.split("{sub}", 1)

    svgs = render(parse(args.file), title, subtitle, args.yratio)

    if args.export:
        for i, svg in enumerate(svgs):
            p = str(args.file)
            page_path = Path(p[: p.rindex(".")] + f"_{i + 1}.svg")
            print(f"Writing {page_path}")
            page_path.write_text(str(svg))
    else:
        # One line per page
        print("\n".join(str(svg) for svg in svgs))


if __name__ == "__main__":
    main()
