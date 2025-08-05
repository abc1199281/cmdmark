# Usage

`cmdmark` scans a directory of YAML files that group useful commands. Each
category is a folder containing one or more YAML files with a `commands`
section.

By default, the configuration directory is `~/.command_bookmarks`. You can
change it with the `CMDMARK_CONFIG_DIR` environment variable or the
`--config-dir` option.

```bash
# list categories and run a command
cmdmark

# include command descriptions while listing
cmdmark --verbose
```
