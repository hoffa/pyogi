import argparse
from pathlib import Path

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF

from parse import parse
from render import render


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=Path)
    parser.add_argument("title")
    parser.add_argument("--yratio", type=float, default=1.414)  # A4
    parser.add_argument("--export", action="store_true")
    parser.add_argument("--pdf", action="store_true")
    args = parser.parse_args()

    subtitle, title = args.title.split("{sub}", 1)

    svgs = render(parse(args.file), title, subtitle, args.yratio)

    if args.export:
        for i, svg in enumerate(svgs):
            p = str(args.file)
            page_path = Path(p[: p.rindex(".")] + f"_{i + 1}.svg")
            pdf_page_path = Path(p[: p.rindex(".")] + f"_{i + 1}.pdf")
            print(f"Writing {page_path}")
            page_path.write_text(str(svg))

            if args.pdf:
                print(f"Writing {pdf_page_path}")
                drawing = svg2rlg(str(page_path))
                renderPDF.drawToFile(drawing, str(pdf_page_path))
    else:
        # One line per page
        print("\n".join(str(svg) for svg in svgs))


if __name__ == "__main__":
    main()
