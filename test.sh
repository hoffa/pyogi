#!/usr/bin/env bash
set -eux

for f in testdata/input/*.mxl; do
    expected=testdata/output/$(basename "$f" .mxl).svg
    diff -u "${expected}" <(./render.sh "$f") > /dev/null
done