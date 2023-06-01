from typing import Optional

def extract_linux_path(file_path: str) -> Optional[str]:
    """
    Extracts the path to the text file from the configuration file.

    The function searches through the config file for the line starting with "linuxpath=".

    :param file_path: Path to the configuration file.
    :type file_path: str
    :return: The Linux path if found, None otherwise.
    :rtype: Optional[str]
    :raises: FileNotFoundError if the configuration file is not found.
    :raises: ValueError if the path is not found in the configuration file.
    """
    try:
        with open(file_path, 'r') as config_file:
            for line in config_file:
                if line.startswith("linuxpath="):
                    path = line.strip().split("=")[1]
                    print("Linux path:", path)
                    return path

        raise ValueError("Path not found in the configuration file.")

    except FileNotFoundError:
        print("Configuration file not found.")
        return None

    except Exception as e:
        print("An error occurred:", str(e))
        return None


