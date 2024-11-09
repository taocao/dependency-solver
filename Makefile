.PHONY: install test lint format clean

install:
	poetry install

test:
	poetry run pytest tests/ --cov=dependency_solver --cov-report=term-missing

lint:
	poetry run flake8 dependency_solver tests
	poetry run mypy dependency_solver tests
	poetry run black --check dependency_solver tests
	poetry run isort --check-only dependency_solver tests

format:
	poetry run black dependency_solver tests
	poetry run isort dependency_solver tests

clean:
	rm -rf .pytest_cache .coverage .mypy_cache .tox dist build
	find . -type d -name __pycache__ -exec rm -rf {} +