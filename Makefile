.PHONY: *

pre-commit:
	pre-commit install
	pre-commit autoupdate

black:
	black app/

mypy:
	mypy -p app

ruff:
	ruff check app --fix

lint: black ruff mypy


run:
	poetry run python -m app
