#!/usr/bin/env bash
set -eux

for f in testdata/input/*.mxl; do
    expected=testdata/output/$(basename "$f" .mxl).svg
    diff -u "${expected}" <(.venv/bin/python src/parse.py "$f" | .venv/bin/python src/render.py) > /dev/null
done