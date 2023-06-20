import argparse
import os
import tempfile
from pathlib import Path

from PyPDF2 import PdfWriter
from reportlab.graphics import renderPDF  # type: ignore
from svglib.svglib import svg2rlg  # type: ignore

from parse import parse
from render import render


def svg2pdf(svg: Path, pdf: Path) -> None:
    drawing = svg2rlg(svg)
    renderPDF.drawToFile(drawing, str(pdf))


def merge_pdf(output: Path, pdfs: list[Path]) -> None:
    merger = PdfWriter()
    for path in pdfs:
        merger.append(str(path))
    merger.write(str(output))
    merger.close()


def replace_suffix(path: Path, suffix: str) -> Path:
    return Path(os.path.splitext(path)[0] + suffix)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--title", type=str)
    parser.add_argument("--composer", type=str)
    parser.add_argument("--format", type=str, choices=["pdf", "svg"], default="pdf")
    args = parser.parse_args()

    output = args.output or replace_suffix(args.file, f".{args.format}")
    print(f"Creating {output}")

    score, title, composer = parse(args.file)

    title = args.title or title or args.file.stem
    composer = args.composer or composer or ""

    if args.format == "pdf":
        yratio = 1.414  # A4
        svgs = render(score, title, composer, yratio)
        with tempfile.TemporaryDirectory() as _tmpdir:
            tmpdir = Path(_tmpdir)
            pdf_paths = []

            for i, svg in enumerate(svgs):
                page_path = tmpdir / f"tmp_{i}.svg"
                pdf_page_path = tmpdir / f"tmp_{i}.pdf"
                pdf_paths.append(pdf_page_path)
                page_path.write_text(str(svg))
                svg2pdf(page_path, pdf_page_path)

            merge_pdf(output, pdf_paths)
    elif args.format == "svg":
        yratio = float("inf")  # Single SVG
        svgs = render(score, title, composer, yratio)
        if len(svgs) != 1:
            raise Exception("Must have a single page")
        output.write_text(str(svgs[0]))
    else:
        raise Exception("Invalid format")


if __name__ == "__main__":
    main()
