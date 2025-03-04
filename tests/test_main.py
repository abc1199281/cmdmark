import pytest
import yaml
from cmdmark.main import load_yaml  # Adjust import path as needed


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
