init:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt
	.venv/bin/pip install black mypy pyflakes isort

format:
	.venv/bin/isort src
	.venv/bin/black src

check:
	.venv/bin/mypy --strict --implicit-reexport src
	./test.sh
	.venv/bin/pyflakes src
	.venv/bin/isort --check src
	.venv/bin/black --check src

clean:
	rm -r .venv