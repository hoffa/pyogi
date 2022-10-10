#!/usr/bin/env bash
set -eux

echo '# Examples' >examples.md

for f in testdata/input/*.mxl; do
	expected=testdata/output/$(basename "$f" .mxl).svg
	if [ "${UPDATE:-}" = "1" ]; then
		./render.sh "$f" >"${expected}"
	fi
	diff -u "${expected}" <(./render.sh "$f") >/dev/null
	printf "## [\`${expected}\`](${expected})\n\n" >>examples.md
	printf "![](${expected})\n\n" >>examples.md
done
