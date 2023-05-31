import os
from typing import Optional


def search_file(filename: str) -> Optional[str]:
    """
    Searches for a file in the file system and returns its path.

    The function traverses the file system starting from the root directory ("/")
    and searches for the given filename in the files.

    :param filename: The name of the file to search for.
    :type filename: str
    :return: The path of the file if found, None otherwise.
    :rtype: Optional[str]
    """
    for root, dirs, files in os.walk("/"):
        if filename in files:
            return os.path.join(root, filename)

    return None

