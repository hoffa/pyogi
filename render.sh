#!/bin/sh
set -eux

if [ ! -d .venv ]; then
    make init
fi

.venv/bin/python src/parse.py "$1" | .venv/bin/python src/render.py