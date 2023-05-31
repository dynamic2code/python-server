from typing import Optional

def extract_linux_path(file_path: str) -> Optional[str]:
    """
    Extracts the path to the text file from the configuration file.

    The function searches through the config file for the line starting with "linuxpath=".

    :param file_path: Path to the configuration file.
    :type file_path: str
    :return: The Linux path if found, None otherwise.
    :rtype: Optional[str]
    """
    with open(file_path, 'r') as config_file:
        for line in config_file:
            if line.startswith("linuxpath="):
                path = line.strip().split("=")[1]
                print("Linux path:", path)
                return path

    print("Path not found in the configuration file.")
    return None


