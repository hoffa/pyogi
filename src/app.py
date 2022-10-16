import tempfile
import zipfile
from pathlib import Path

import streamlit as st

from common import parse_and_render

st.set_page_config(page_title="Pyogi Converter", page_icon=":notes:")
st.title("Pyogi Converter")


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
                b = parse_and_render(filename)
                st.image(b)
