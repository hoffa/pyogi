#!/usr/bin/env bash
set -eux

mkdir -p .tmp

for f in testdata/input/*.mxl; do
	bname=$(basename "$f" .mxl)
	expected_svg=testdata/output/svg/${bname}.svg
	expected_pdf=testdata/output/pdf/${bname}.pdf
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
done
