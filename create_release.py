import sys
import os
import re
import shutil
import zipfile
from pathlib import Path

def get_addon_version(init_file):
    with open(init_file, 'r') as f:
        init_contents = f.read()
        match = re.search(r'"version"\s*:\s*\((\d+),\s*(\d+),\s*(\d+)\)', init_contents)
        if match:
            version = '.'.join(match.groups())
            return version
    return None

def create_release(addon_name,addon_folder, release_folder):
    # Delete existing release folder and zip file
    version = get_addon_version(os.path.join(addon_folder, "__init__.py"))
    if not version:
        print("Failed to retrieve addon version.")
        return
    
    existing_release_path = os.path.join(release_folder, f"{addon_name}_release_{version}")
    existing_zip_file = os.path.join(release_folder, f"{addon_name}_release_{version}.zip")
    if os.path.exists(existing_release_path):
        shutil.rmtree(existing_release_path)
    if os.path.exists(existing_zip_file):
        os.remove(existing_zip_file)
    
    # Create a folder for the release
    release_path = os.path.join(release_folder, f"{addon_name}_release_{version}")
    os.makedirs(release_path, exist_ok=True)

    release_source= os.path.join(release_path, f"{addon_name}")
    os.makedirs(release_source, exist_ok=True)
    
    # Copy addon files to the release folder
    for root, dirs, files in os.walk(addon_folder):
        # Ignore __pycache__ folders
        if "__pycache__" in dirs:
            dirs.remove("__pycache__")
        
        relative_root = os.path.relpath(root, addon_folder)
        release_root = os.path.join(release_source, relative_root)
        os.makedirs(release_root, exist_ok=True)
        for file in files:
            if file.endswith(('.py', '.png')):
                file_path = os.path.join(root, file)
                release_file_path = os.path.join(release_root, file)
                shutil.copy(file_path, release_file_path)
    
    # Create a zip file for the release
    zip_file = zipfile.ZipFile(os.path.join(release_path, f"{addon_name}.zip"), 'w')
    for folder_name, _, files in os.walk(release_path):
        for file in files:
            file_path = os.path.join(folder_name, file)
            zip_file.write(file_path, os.path.relpath(file_path, release_folder), compress_type=zipfile.ZIP_DEFLATED)
    zip_file.close()

    shutil.rmtree(release_source)
    
    print(f"Release {version} created successfully!")
    print(f"Release ZIP file stored in {str(os.path.join(release_path, f"{addon_name}.zip"))}.")


def main():
    addon_name = "buildplanner"
    addon_folder = Path(str(Path(__file__).parents[1])+"/buildplanner/buildplanner")
    release_folder = Path(str(Path(__file__).parents[1])+"/buildplanner/release_folder")
    create_release(addon_name, addon_folder, release_folder)

if __name__ == '__main__':
    main()