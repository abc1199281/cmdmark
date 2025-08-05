# Modules

## `cmdmark.main`

- `list_items(path)` – list folders and YAML files while skipping Git metadata.
- `list_commands(data, verbose=False)` – display available commands from a YAML file.
- `select_item(items)` – prompt the user to select an entry by number.
- `load_yaml(filepath)` – load commands from a YAML file.
- `parse_args(argv=None)` – parse command line arguments.
- `run_command(command)` – execute a command via `subprocess.run`.
- `main()` – entry point used by the `cmdmark` console script.
