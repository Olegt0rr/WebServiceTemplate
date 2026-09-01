.PHONY: *

pre-commit:
	pre-commit install
	pre-commit autoupdate

format:
	ruff format .

mypy:
	mypy -p app

ruff:
	ruff check . --fix

lint: format ruff mypy


run:
	uv run python -m app
