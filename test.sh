#!/usr/bin/env bash
set -eux

# Test Fur Elise with default paging
diff -u testdata/output/fur-elise-paged.svg.txt <(.venv/bin/python src/main.py testdata/input/fur-elise.mxl "$(cat testdata/input/fur-elise.txt)")

echo '# Examples' >examples.md

# Test all inputs with a single scroll (huge yratio)
for f in testdata/input/*.mxl; do
	expected=testdata/output/$(basename "$f" .mxl).svg
	title=$(cat "testdata/input/$(basename "$f" .mxl).txt")
	if [ "${UPDATE:-}" = "1" ]; then
		.venv/bin/python src/main.py "$f" "${title}" --yratio 99999 >"${expected}"
	fi
	diff -u "${expected}" <(.venv/bin/python src/main.py "$f" "${title}" --yratio 9999) >/dev/null
	printf "## [\`${expected}\`](https://raw.githubusercontent.com/hoffa/notation/main/${expected})\n\n" >>examples.md
	printf "![](${expected})\n\n" >>examples.md
done
