# Blender Tools
# Copyright 2024 Ralph Wiedemeier, Frame Factory GmbH
# License: MIT

from zipfile import ZipFile
from pathlib import Path

def create_zip_archive(
        output_zip_path: str|Path,
        base_dir: str|Path,
        file_names_to_zip: list[str|Path]
    ):
    """
    Create a ZIP file from a list of files.
    
    Parameters:
    output_zip_path (str|Path): Path where the ZIP file should be created
    base_dir (str|Path): Base directory of the files to add
    file_names_to_zip (list[str|Path]): List of file names to include in the ZIP
    """
    zip_path = Path(output_zip_path)
    zip_path.parent.mkdir(parents=True, exist_ok=True)

    base_path = Path(base_dir)
    
    with ZipFile(zip_path, 'w') as zip_file:
        for file_name in file_names_to_zip:
            file_path = base_path / file_name
            
            if not file_path.exists():
                print(f"Warning: File not found - {file_path}")
                continue
            
            zip_file.write(file_path, file_name)
        
