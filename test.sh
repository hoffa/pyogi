#!/usr/bin/env bash
set -eux

mkdir -p .tmp

for f in testdata/input/*.mxl; do
	bname=$(basename "$f" .mxl)
	expected_svg=testdata/output/svg/${bname}.svg
	expected_pdf=testdata/output/pdf/${bname}.pdf

	if [ "${UPDATE:-}" = "1" ]; then
		.venv/bin/python src/main.py "$f" --svg "${expected_svg}" --pdf "${expected_pdf}"
	fi

	tmp_svg=.tmp/${bname}.svg
	tmp_pdf=.tmp/${bname}.pdf

	.venv/bin/python src/main.py "$f" --svg "${tmp_svg}" --pdf "${tmp_pdf}"

	cmp "${expected_svg}" "${tmp_svg}"
	cmp "${expected_pdf}" "${tmp_pdf}"
done
