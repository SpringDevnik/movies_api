import:
	find . -name "*.py" -not -path "./.venv/*" -exec poetry run autoflake --in-place --remove-all-unused-imports {} +

flake:
	poetry run flake8 .

black:
	poetry run black .

mypy:
	poetry run mypy --no-color-output .

test:
	poetry run pytest -n 4
