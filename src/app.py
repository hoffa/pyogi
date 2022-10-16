import tempfile
from typing import Any, Optional
from pathlib import Path
import zipfile

import streamlit as st
import svgwrite
from parse import parse

from render import render  # type: ignore

st.set_page_config(page_title="Pyogi Converter", page_icon=":notes:")
st.title("Pyogi Converter")


A = {
    "bg_color": "white",
    "staff_color": "black",
    "colors": [
        "#000000",
        "#CC3311",
        "#EE3377",
        "#EE7733",
        "#0077BB",
        "#009988",
        "#33BBEE",
    ],
}

f = st.file_uploader(
    "File", help="File must be in MusicXML format.", type=["mxl", "musicxml"]
)
if f:
    # TODO: Can't get music21 to accept zipped MusicXML bytes as input
    with tempfile.TemporaryDirectory() as dir:
        with zipfile.ZipFile(f) as zip:
            zip.extractall(dir)
            # Assumes only a single top-level XML file
            paths = list(Path(dir).glob("*.xml"))
            if len(paths) == 1:
                filename = paths[0]
                b = render(list(parse(filename)), A)
                st.image(b)
