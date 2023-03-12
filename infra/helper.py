import os


def list_files(directory_path):
    items = os.listdir(directory_path)
    return [
        os.path.join(directory_path, item)
        for item in items
        if os.path.isfile(os.path.join(directory_path, item))
    ]
