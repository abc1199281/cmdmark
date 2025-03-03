import os

CONFIG_PATH = os.path.expanduser("~/command_bookmarks")

def list_items(path):
    items = sorted(os.listdir(path))
    for idx, item in enumerate(items, 1):
        print(f"{idx}. {item}")
    return items

def select_item(items):
    while True:
        try:
            choice = int(input("Select a number: ")) - 1
            if 0 <= choice < len(items):
                return items[choice]
        except ValueError:
            pass
        print("Invalid choice. Try again.")

def execute_command(filepath):
    with open(filepath, "r") as f:
        command = f.read().strip()
    os.system(command)

def main():
    print("hello world")
    """
    if not os.path.exists(CONFIG_PATH):
        print(f"Config folder not found: {CONFIG_PATH}")
        return

    print("=== Shortcuts ===")
    folders = [f for f in list_items(CONFIG_PATH) if os.path.isdir(os.path.join(CONFIG_PATH, f))]
    if not folders:
        print("No folders found.")
        return

    selected_folder = select_item(folders)
    folder_path = os.path.join(CONFIG_PATH, selected_folder)

    print(f"\n=== {selected_folder} Commands ===")
    commands = [f for f in list_items(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    if not commands:
        print("No commands found.")
        return

    selected_command = select_item(commands)
    command_path = os.path.join(folder_path, selected_command)

    print(f"\nExecuting: {selected_command}\n")
    execute_command(command_path)
    """

if __name__ == "__main__":
    main()
