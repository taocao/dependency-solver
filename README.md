# Dependency Solver

A Python tool for solving and visualizing project/tasks dependencies.

## Features

- Interactive UI for managing dependencies
- Visual representation of dependency graphs
- Topological sorting for finding optimal task order
- Circular dependency detection

## Project Structure
.
├── Makefile
├── README.md
├── dependency_solver
│   ├── __init__.py
│   ├── core.py
│   ├── ui.py
│   └── visualization.py
├── pyproject.toml
├── tests
│   ├── test_core.py
│   ├── test_ui.py
│   └── test_visualization.py
└── tox.ini

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/dependency-solver.git
cd dependency-solver

# Install poetry if you haven't already
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install
```

## Usage

```bash
# Run the application
poetry run streamlit run dependency_solver/ui.py

# Run tests
make test

# Run linting and type checking
make lint

# Format code
make format
```

## Development

This project uses:
- Poetry for dependency management
- Pytest for testing
- Black for code formatting
- Flake8 for linting
- MyPy for type checking
- Tox for testing across Python versions

## Testing

```bash
# Run tests with coverage
make test

# Run tests across Python versions
tox
```