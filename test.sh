#!/usr/bin/env bash
set -eux

for f in testdata/input/*.mxl; do
    expected=testdata/output/$(basename "$f" .mxl).svg
    if [ "${UPDATE:-}" = "1" ]; then
        ./render.sh "$f" > "${expected}"
    fi
    diff -u "${expected}" <(./render.sh "$f") > /dev/null
done