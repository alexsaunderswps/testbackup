# Folder Cleaner Script - cleans logs, reports, and screenshots from folders
import os
import shutil

def clean_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

def main():
    # Use the current directory as the root folder
    root_folder = os.path.dirname(os.path.abspath(__file__))
    folders_to_clean = ['logs', 'screenshots', 'reports']

    for folder in folders_to_clean:
        folder_path = os.path.join(root_folder, folder)
        if os.path.exists(folder_path):
            print(f"Cleaning {folder}...")
            clean_folder(folder_path)
        else:
            print(f"Folder {folder} not found.")

if __name__ == "__main__":
    main()