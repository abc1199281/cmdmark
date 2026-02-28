import subprocess
from unittest.mock import patch

import pytest
import yaml

from cmdmark.main import (
    list_commands,
    list_items,
    load_yaml,
    main,
    parse_args,
    print_items,
    run_command,
    select_item,
)

# --- load_yaml ---


def test_load_yaml_valid(tmp_path):
    test_file = tmp_path / "test.yml"
    test_data = {"commands": {"test": {"command": "echo hello", "description": "Test"}}}
    test_file.write_text(yaml.dump(test_data))

    loaded_data = load_yaml(str(test_file))
    assert loaded_data == test_data


def test_load_yaml_invalid(tmp_path):
    test_file = tmp_path / "invalid.yml"
    test_file.write_text(":\n  - :\n    - :")

    with pytest.raises(yaml.YAMLError):
        load_yaml(str(test_file))


def test_load_yaml_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_yaml("nonexistent_file.yml")


# --- list_items ---


def test_list_items_ignores_git(tmp_path):
    (tmp_path / ".git").mkdir()
    (tmp_path / ".gitignore").write_text("")
    (tmp_path / "visible.yml").write_text("")
    (tmp_path / "dir").mkdir()

    result = list_items(str(tmp_path))
    assert ".git" not in result
    assert ".gitignore" not in result
    assert result == ["dir", "visible.yml"]


def test_yaml_listing_skips_git(tmp_path):
    (tmp_path / ".git").mkdir()
    (tmp_path / "file.yml").write_text("commands: {}")
    (tmp_path / "not_yaml.txt").write_text("")

    files = [f for f in list_items(str(tmp_path)) if f.endswith(".yml")]
    assert files == ["file.yml"]


def test_list_items_filters_non_yml_files(tmp_path):
    (tmp_path / "valid.yml").write_text("commands: {}")
    (tmp_path / "also_valid.yaml").write_text("commands: {}")
    (tmp_path / "not_yaml.txt").write_text("")
    (tmp_path / "another.py").write_text("")
    (tmp_path / "README.md").write_text("")
    (tmp_path / "subdir").mkdir()

    result = list_items(str(tmp_path))
    assert result == ["also_valid.yaml", "subdir", "valid.yml"]


def test_list_items_empty_dir(tmp_path):
    result = list_items(str(tmp_path))
    assert result == []


# --- print_items ---


def test_print_items(capsys):
    print_items(["alpha", "beta", "gamma"])
    captured = capsys.readouterr()
    assert captured.out == "1. alpha\n2. beta\n3. gamma\n"


# --- list_commands ---


def test_list_commands_valid(capsys):
    data = {
        "commands": {
            "greet": {"command": "echo hi", "description": "Say hi"},
            "bye": {"command": "echo bye", "description": "Say bye"},
        }
    }
    result = list_commands(data)
    assert result == ["echo hi", "echo bye"]
    captured = capsys.readouterr()
    assert "echo hi" in captured.out
    assert "echo bye" in captured.out


def test_list_commands_verbose(capsys):
    data = {
        "commands": {
            "greet": {"command": "echo hi", "description": "Say hi"},
        }
    }
    result = list_commands(data, verbose=True)
    assert result == ["echo hi"]
    captured = capsys.readouterr()
    assert "echo hi - Say hi" in captured.out
    assert "id. command - description" in captured.out


def test_list_commands_no_commands_key(capsys):
    result = list_commands({"other": "stuff"})
    assert result == []
    captured = capsys.readouterr()
    assert "No valid commands found" in captured.out


def test_list_commands_invalid_format(capsys):
    data = {"commands": {"bad": "not a dict"}}
    result = list_commands(data)
    assert result == []
    captured = capsys.readouterr()
    assert "Invalid command format for bad" in captured.out


# --- select_item ---


def test_select_item_valid():
    items = ["a", "b", "c"]
    with patch("builtins.input", return_value="2"):
        result = select_item(items)
    assert result == "b"


def test_select_item_invalid_then_valid():
    items = ["a", "b"]
    with patch("builtins.input", side_effect=["0", "abc", "2"]):
        result = select_item(items)
    assert result == "b"


def test_select_item_keyboard_interrupt():
    items = ["a", "b"]
    with patch("builtins.input", side_effect=KeyboardInterrupt):
        result = select_item(items)
    assert result is None


def test_select_item_eof():
    items = ["a", "b"]
    with patch("builtins.input", side_effect=EOFError):
        result = select_item(items)
    assert result is None


# --- parse_args ---


def test_parse_args_defaults():
    args = parse_args([])
    assert args.verbose is False
    assert args.config_dir is not None


def test_parse_args_verbose():
    args = parse_args(["-v"])
    assert args.verbose is True


def test_parse_args_config_dir():
    args = parse_args(["-c", "/tmp/my_bookmarks"])
    assert args.config_dir == "/tmp/my_bookmarks"


def test_parse_args_env_var():
    with patch.dict("os.environ", {"CMDMARK_CONFIG_DIR": "/from/env"}):
        args = parse_args([])
    assert args.config_dir == "/from/env"


# --- run_command ---


def test_run_command_failure():
    with pytest.raises(subprocess.CalledProcessError):
        run_command("false")


def test_run_command_success(capsys):
    run_command("echo hello")
    captured = capsys.readouterr()
    assert "Command failed" not in captured.out


# --- main ---


def test_main_config_not_found(capsys):
    with patch("cmdmark.main.parse_args") as mock_args:
        mock_args.return_value = parse_args(["-c", "/nonexistent/path"])
        main()
    captured = capsys.readouterr()
    assert "Config folder not found" in captured.out


def test_main_empty_categories(tmp_path, capsys):
    with patch("cmdmark.main.parse_args") as mock_args:
        mock_args.return_value = parse_args(["-c", str(tmp_path)])
        main()
    captured = capsys.readouterr()
    assert "No categories found" in captured.out


def test_main_no_yaml_files(tmp_path, capsys):
    category = tmp_path / "mycat"
    category.mkdir()
    with (
        patch("cmdmark.main.parse_args") as mock_args,
        patch("builtins.input", return_value="1"),
    ):
        mock_args.return_value = parse_args(["-c", str(tmp_path)])
        main()
    captured = capsys.readouterr()
    assert "No YAML files found" in captured.out


def test_main_full_flow(tmp_path, capsys):
    category = tmp_path / "tools"
    category.mkdir()
    yml = category / "cmds.yml"
    yml.write_text(
        yaml.dump(
            {
                "commands": {
                    "greet": {"command": "echo hi", "description": "Say hi"},
                }
            }
        )
    )
    with (
        patch("cmdmark.main.parse_args") as mock_args,
        patch("builtins.input", side_effect=["1", "1", "1"]),
    ):
        mock_args.return_value = parse_args(["-c", str(tmp_path)])
        main()
    captured = capsys.readouterr()
    assert "Executing: echo hi" in captured.out


def test_main_ctrl_c_on_category(tmp_path, capsys):
    category = tmp_path / "mycat"
    category.mkdir()
    with (
        patch("cmdmark.main.parse_args") as mock_args,
        patch("builtins.input", side_effect=KeyboardInterrupt),
    ):
        mock_args.return_value = parse_args(["-c", str(tmp_path)])
        main()
    captured = capsys.readouterr()
    assert "Executing" not in captured.out
