import os
import json
import shutil
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from extensions_dict import extension_paths


class DesktopEventHandler(FileSystemEventHandler):
    def __init__(self, desktop_path):
        self.desktop_path = desktop_path

    def on_modified(self, event):
        """This will be triggered when files on Desktop are modified/added/removed."""
        if event.is_directory:
            return  # Ignore directory events
        print(f"File changed: {event.src_path}")
        file_sorter(self.desktop_path)  # Run the file sorter whenever there's a change

    def on_created(self, event):
        """This will be triggered when a new file is created on Desktop."""
        if event.is_directory:
            return  # Ignore directory events
        print(f"New file created: {event.src_path}")
        file_sorter(self.desktop_path)  # Run the file sorter whenever a new file is created


def main(): 
    desktop_path = get_desktop()
    folder_creator(desktop_path)

    # Set up the watchdog observer to monitor the Desktop directory
    event_handler = DesktopEventHandler(desktop_path)
    observer = Observer()
    observer.schedule(event_handler, str(desktop_path), recursive=False)
    observer.start()

    print("Monitoring Desktop for changes... Press Ctrl+C to stop.")
    try:
        while True:
            pass  # Keep the script running to monitor changes
    except KeyboardInterrupt:
        observer.stop()
        print("Stopped monitoring.")
    observer.join()


# Locate Desktop or create config for custom path
def get_desktop():
    config_file = Path("config.json")
    
    if config_file.exists():
        with open(config_file, "r") as f:
            desktop_path = Path(json.load(f)["desktop_path"])
    else:
        try:
            desktop_path = Path(os.path.join(os.getenv('USERPROFILE'), 'Desktop'))
        except:
            desktop_path = Path(os.path.join(os.path.expanduser("~"), 'Desktop'))
        
    if not desktop_path.exists():
        custom_path = input("Enter the Desktop path (e.g., D:/Users/YourUser/Desktop): ")
        desktop_path = Path(custom_path)
        
        # Save custom path to config file
        with open(config_file, "w") as f:
            json.dump({"desktop_path": str(desktop_path)}, f)
            
    return Path(desktop_path)


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
            
            
# Sort files
def file_sorter(desktop_path):
    if desktop_path.exists():
        print(f"Sorting files in {desktop_path}: ")
        files = [file for file in desktop_path.iterdir() if file.is_file()]
        for file in files:
            extension = file.suffix.lower()
            if extension in extension_paths:
                destination_folder = desktop_path / extension_paths[extension]
            else:
                destination_folder = desktop_path / extension_paths['noname']
        
        # Possible replacement of folder_creator     
        # destination_folder.mkdir(parents=True, exist_ok=True)
        
            destination_path = destination_folder / file.name 
            shutil.move(str(file), str(destination_path))
            print(f"Moved: {file.name} -> {destination_folder}")
            
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
 