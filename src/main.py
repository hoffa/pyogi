import argparse
from pathlib import Path

from PyPDF2 import PdfWriter
from reportlab.graphics import renderPDF  # type: ignore
from svglib.svglib import svg2rlg  # type: ignore

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
        pdf_paths = []

        for i, svg in enumerate(svgs):
            p = str(args.file)
            page_path = Path(p[: p.rindex(".")] + f"_{i + 1}.svg")
            pdf_page_path = Path(p[: p.rindex(".")] + f"_{i + 1}.pdf")
            pdf_paths.append(pdf_page_path)
            print(f"Writing {page_path}")
            page_path.write_text(str(svg))

            print(f"Writing {pdf_page_path}")
            drawing = svg2rlg(str(page_path))
            renderPDF.drawToFile(drawing, str(pdf_page_path))

        merged_pdf_path = Path(p[: p.rindex(".")] + ".pdf")
        merger = PdfWriter()
        for path in pdf_paths:
            merger.append(path)
        print(f"Writing {merged_pdf_path}")
        merger.write(merged_pdf_path)
        merger.close()
    else:
        # One line per page
        print("\n".join(str(svg) for svg in svgs))


if __name__ == "__main__":
    main()
