#!/usr/bin/env bash
set -eux

echo '# Examples' >examples.md

mkdir -p .tmp

# it should test both svg and pdf
# svg should always be a continuous file, pdf always a page, with no configuration option
# so probably --svg and --pdf

# Test all inputs with a single scroll (huge yratio)
for f in testdata/input/*.mxl; do
	bname=$(basename "$f" .mxl)
	expected_svg=testdata/output/${bname}.svg
	expected_pdf=testdata/output/${bname}.pdf
	title=$(cat "testdata/input/${bname}.txt")

	if [ "${UPDATE:-}" = "1" ]; then
		.venv/bin/python src/main.py "$f" "${title}" --svg "${expected_svg}"
		.venv/bin/python src/main.py "$f" "${title}" --pdf "${expected_pdf}"
	fi

	tmp_svg=.tmp/${bname}.svg
	tmp_pdf=.tmp/${bname}.pdf

	.venv/bin/python src/main.py "$f" "${title}" --svg "${tmp_svg}"
	.venv/bin/python src/main.py "$f" "${title}" --pdf "${tmp_pdf}"

	cmp "${expected_svg}" "${tmp_svg}"
	cmp "${expected_pdf}" "${tmp_pdf}"

	printf "## [\`${expected_svg}\`](https://raw.githubusercontent.com/hoffa/notation/main/${expected_svg})\n\n" >>examples.md
	printf "![](${expected_svg})\n\n" >>examples.md
done
