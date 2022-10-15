#!/usr/bin/env bash
set -eux

echo '# Examples' >examples.md

for f in testdata/input/*.mxl; do
	expected=testdata/output/$(basename "$f" .mxl).svg
	expected_turbo=testdata/output/$(basename "$f" .mxl)-turbo.svg
	expected_mono=testdata/output/$(basename "$f" .mxl)-mono.svg
	if [ "${UPDATE:-}" = "1" ]; then
		./render.sh "$f" >"${expected}"
		./render.sh --theme dark "$f" >"${expected_turbo}"
		./render.sh --theme mono "$f" >"${expected_mono}"
	fi
	diff -u "${expected}" <(./render.sh "$f") >/dev/null
	diff -u "${expected_turbo}" <(./render.sh --theme dark "$f") >/dev/null
	diff -u "${expected_mono}" <(./render.sh --theme mono "$f") >/dev/null
	printf "## [\`${expected}\`](https://raw.githubusercontent.com/hoffa/notation/main/${expected})\n\n" >>examples.md
	printf "![](${expected})\n\n" >>examples.md
	printf "## [\`${expected_turbo}\`](https://raw.githubusercontent.com/hoffa/notation/main/${expected_turbo})\n\n" >>examples.md
	printf "![](${expected_turbo})\n\n" >>examples.md
	printf "## [\`${expected_mono}\`](https://raw.githubusercontent.com/hoffa/notation/main/${expected_mono})\n\n" >>examples.md
	printf "![](${expected_mono})\n\n" >>examples.md
done
