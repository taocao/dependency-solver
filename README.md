# Dependency Solver

A Python tool for solving and visualizing project/tasks dependencies.

## Add Dependencies
<img width="1501" alt="pds" src="https://github.com/user-attachments/assets/f76c8fb5-d982-4105-84c4-764201b07ce3">
## Solve Dependencies
<img width="1455" alt="Dependency_Graph" src="https://github.com/user-attachments/assets/e8e351ba-0552-48e4-a67f-e648d4bd54af">

## Features

- Interactive UI for managing dependencies
- Visual representation of dependency graphs
- Topological sorting for finding optimal task order
- Circular dependency detection

## Project Structure

```bash
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
```

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
