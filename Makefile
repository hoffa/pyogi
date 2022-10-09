init:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt
	.venv/bin/pip install mypy pyflakes isort

format:
	.venv/bin/isort .
	.venv/bin/black .

check:
	.venv/bin/mypy --strict --implicit-reexport *.py
	.venv/bin/pyflakes *.py
	.venv/bin/isort --check .
	.venv/bin/black --check .

clean:
	rm -r .venv