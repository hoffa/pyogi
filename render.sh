#!/bin/sh
set -eux

if [ ! -d .venv ]; then
    make init
fi

.venv/bin/python src/main.py "$1"