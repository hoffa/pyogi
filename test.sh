#!/usr/bin/env bash
set -eux

echo '# Examples' >examples.md

for f in testdata/input/*.mxl; do
	expected=testdata/output/$(basename "$f" .mxl).svg
	title=$(cat "testdata/input/$(basename "$f" .mxl).txt")
	if [ "${UPDATE:-}" = "1" ]; then
		./render.sh "$f" "${title}" >"${expected}"
	fi
	diff -u "${expected}" <(./render.sh "$f" "${title}") >/dev/null
	printf "## [\`${expected}\`](https://raw.githubusercontent.com/hoffa/notation/main/${expected})\n\n" >>examples.md
	printf "![](${expected})\n\n" >>examples.md
done
