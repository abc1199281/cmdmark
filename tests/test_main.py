import pytest
import yaml
import sys
from cmdmark.main import load_yaml, list_items, parse_args, ENV_CONFIG_DIR, DEFAULT_CONFIG_DIR


def test_load_yaml_valid(tmp_path):
    # Create a temporary YAML file
    test_file = tmp_path / "test.yml"
    test_data = {"commands": {"test": {"command": "echo hello", "description": "Test"}}}
    test_file.write_text(yaml.dump(test_data))

    # Load the YAML file using your function
    loaded_data = load_yaml(test_file)

    # Assert that the loaded data matches the expected data
    assert loaded_data == test_data


def test_load_yaml_invalid(tmp_path):
    test_file = tmp_path / "invalid.yml"
    test_file.write_text("not: valid: yaml")

    with pytest.raises(yaml.YAMLError):
        load_yaml(test_file)


def test_load_yaml_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_yaml("nonexistent_file.yml")


def test_list_items_ignores_git(tmp_path):
    (tmp_path / ".git").mkdir()
    (tmp_path / ".gitignore").write_text("")
    (tmp_path / "visible.yml").write_text("")
    (tmp_path / "dir").mkdir()

    result = list_items(tmp_path)
    assert ".git" not in result
    assert ".gitignore" not in result
    assert sorted(result) == ["dir", "visible.yml"]


def test_yaml_listing_skips_git(tmp_path):
    (tmp_path / ".git").mkdir()
    (tmp_path / "file.yml").write_text("commands: {}")
    (tmp_path / "not_yaml.txt").write_text("")

    files = [f for f in list_items(tmp_path) if f.endswith(".yml")]
    assert files == ["file.yml"]


def test_parse_args_uses_env(monkeypatch):
    custom = "/tmp/custom_cfg"
    monkeypatch.setenv(ENV_CONFIG_DIR, custom)
    monkeypatch.setattr(sys, "argv", ["cmdmark"])
    args = parse_args()
    assert args.config_dir == custom
