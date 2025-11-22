import os

def get_file_structure(root_path: str):
    """
    Recursively builds a dictionary representing the file structure.
    """
    structure = {"name": os.path.basename(root_path), "type": "directory", "children": []}
    
    try:
        for entry in os.scandir(root_path):
            if entry.is_dir():
                structure["children"].append(get_file_structure(entry.path))
            else:
                structure["children"].append({
                    "name": entry.name,
                    "type": "file",
                    "path": entry.path
                })
    except PermissionError:
        pass
        
    return structure
