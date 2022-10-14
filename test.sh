#!/usr/bin/env bash
set -eux

echo '# Examples' >examples.md

for f in testdata/input/*.mxl; do
	expected=testdata/output/$(basename "$f" .mxl).svg
	expected_turbo=testdata/output/$(basename "$f" .mxl)-turbo.svg
	if [ "${UPDATE:-}" = "1" ]; then
		./render.sh "$f" >"${expected}"
		./render.sh --theme turbo "$f" >"${expected_turbo}"
	fi
	diff -u "${expected}" <(./render.sh "$f") >/dev/null
	diff -u "${expected_turbo}" <(./render.sh --theme turbo "$f") >/dev/null
	printf "## [\`${expected}\`](${expected})\n\n" >>examples.md
	printf "![](${expected})\n\n" >>examples.md
	printf "## [\`${expected_turbo}\`](${expected_turbo})\n\n" >>examples.md
	printf "![](${expected_turbo})\n\n" >>examples.md
done
