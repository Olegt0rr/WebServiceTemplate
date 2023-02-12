.PHONY: *

pre-commit:
	pre-commit install
	pre-commit autoupdate

isort:
	isort app/

black:
	black app/

mypy:
	mypy -p app

pylint:
	pylint app/

ruff:
	ruff check app

lint: isort black ruff mypy pylint


run:
	poetry run python -m app
