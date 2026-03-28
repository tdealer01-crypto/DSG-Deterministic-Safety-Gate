.PHONY: install test lint format

install:
	pip install -r requirements-dev.txt

test:
	pytest -q

lint:
	ruff check .

format:
	ruff format .
