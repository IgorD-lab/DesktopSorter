import os
import json
from pathlib import Path
from extensions_dict import extension_paths


def main(): 
    desktop_path = get_desktop()
    folder_creator(desktop_path)


# Locate Desktop or create config for custom path
def get_desktop():
    config_file = Path("config.json")
    
    if config_file.exists():
        with open(config_file, "r") as f:
            desktop_path = Path(json.load(f)["desktop_path"])
    else:
        desktop_path = Path(os.path.join(os.getenv('USERPROFILE'), 'Desktop'))
        
    if not desktop_path.exists():
        custom_path = input("Enter the Desktop path (e.g., D:/Users/YourUser/Desktop): ")
        desktop_path = Path(custom_path)
        
        # Save custom path to config file
        with open(config_file, "w") as f:
            json.dump({"desktop_path": str(desktop_path)}, f)
    return desktop_path


# Create folder structure
#* This should be executed only the first time that program runs
def folder_creator(desktop_path):
    if not desktop_path.exists():
        print("Desktop path doesn't exist")
    else:
        for ext, folder in extension_paths.items():
            # Join desktop path with folder path
            folder_path = desktop_path / folder
            
            # Create the folder if it doesn't exist
            if not folder_path.exists():
                folder_path.mkdir(parents=True, exist_ok=True)
                print(f"Created folder path: {folder_path}")
            else:
                print(f"Folder already exists: {folder_path}")
            
            
# Sort files
def file_sorter(desktop_path):
    if desktop_path.exists():
        print(f"Sorting files in {desktop_path}: ")
        files = [file.name for file in desktop_path.iterdir() if file.is_file()]
        for file in files:
            extension = file.suffix
            print(f"File: {file.name}, Extension: {extension}")
        
    else:
        print("Cannot List: The specified Desktop path does not exist.")


# List Desktop files
def list_desktop(desktop_path):
    if desktop_path.exists():
        print(f"Listing files in {desktop_path}: ")
        files = [file.name for file in desktop_path.iterdir() if file.is_file()]
        print(files)
    else:
        print("Cannot List: The specified Desktop path does not exist.")


            


if __name__ == '__main__':
    main()
 