import os
from typing import List, Union


def list_files(directory_path: Union[str, os.PathLike]) -> List[str]:
    """List file in a directory"""
    items = os.listdir(directory_path)
    return [
        os.path.join(directory_path, item)
        for item in items
        if os.path.isfile(os.path.join(directory_path, item))
    ]
