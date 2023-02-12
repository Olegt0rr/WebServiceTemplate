.PHONY: *

pre-commit:
	pre-commit install
	pre-commit autoupdate

isort:
	isort app/

black:
	black app/

flake8:
	flake8 app/

mypy:
	mypy -p app

pylint:
	pylint app/

lint: isort black mypy flake8 pylint


run:
	poetry run python -m app
