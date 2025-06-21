# Repository Summary

This project contains **cmdmark**, a CLI tool that manages command bookmarks defined in YAML files. Users select categories, YAML files, and commands interactively and execute them directly from the terminal.

## Key Components

- `cmdmark/main.py` – Implements listing functions, YAML loading, user selection, and command execution.
- `pyproject.toml` – Project metadata and dependencies (`pyyaml` and `pytest`), exposing the `cmdmark` console script.
- `tests/` – Unit tests validating YAML loading and directory listing logic, along with sample YAML files.

## Development

The codebase targets Python 3.12. To run the test suite:

```bash
pytest -q
```

This command should report all tests passing.
