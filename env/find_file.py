import os
from typing import Optional


def search_file(filename: str) -> Optional[str]:
    """
    Searches for a file in the file system and returns its path.

    The function traverses the file system starting from the root directory ("/")
    and searches for the given filename in the files.

    Args:
        filename(str): The name of the file to search for.

    return:
        Optional[str]: The path of the file if found, None otherwise.
    """
    for root, dirs, files in os.walk("/"):
        if filename in files:
            return os.path.join(root, filename)

    return None

