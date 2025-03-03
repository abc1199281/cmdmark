import os
import yaml

CONFIG_DIR = os.path.expanduser("~/.command_bookmarks")

def list_items(path):
    """List folders and YAML files."""
    items = sorted(os.listdir(path))
    for idx, item in enumerate(items, 1):
        print(f"{idx}. {item}")
    return items

def list_commands(data):
    """List available commands from a parsed 2YAML file."""
    if "commands" not in data or not isinstance(data["commands"], dict):
        print("No valid commands found in the YAML file.")
        return []

    commands = []
    print(f"id. [alias]:cmd (short description)")
    for idx, (alias, cmd_data) in enumerate(data["commands"].items(), 1):
        if isinstance(cmd_data, dict) and "command" in cmd_data:
            description = cmd_data.get("description", "No description")
            cmd = cmd_data.get("command")
            print(f"{idx}. {alias}:{cmd} ({description})")
            commands.append(cmd)
        else:
            print(f"Invalid command format for {cmd}") #Handles invalid format
    return commands

def select_item(items):
    """Prompt user to select an item by number."""
    while True:
        try:
            choice = int(input("Select a number: ")) - 1
            if 0 <= choice < len(items):
                return items[choice]
        except ValueError:
            pass
        print("Invalid choice. Try again.")

def load_yaml(filepath):
    """Load commands from a YAML file."""
    with open(filepath, "r") as f:
        return yaml.safe_load(f)

def main():
    if not os.path.exists(CONFIG_DIR):
        print(f"Config folder not found: {CONFIG_DIR}")
        return

    print("=== Categories ===")
    categories = list_items(CONFIG_DIR)
    selected_category = select_item(categories)
    category_path = os.path.join(CONFIG_DIR, selected_category)

    print(f"\n=== {selected_category} Files ===")
    files = [f for f in list_items(category_path) if f.endswith(".yml")]
    if not files:
        print("No YAML files found.")
        return

    selected_file = select_item(files)
    file_path = os.path.join(category_path, selected_file)

    print(f"\n=== {selected_file} Commands ===")
    data = load_yaml(file_path)
    if "commands" not in data:
        print("Invalid YAML format.")
        return

    command_keys = list_commands(data)
    command = select_item(command_keys)

    print(f"\nExecuting: {command}\n")
    os.system(command)

if __name__ == "__main__":
    main()
