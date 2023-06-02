from typing import Optional

def extract_linux_path(file_path: str) -> Optional[str]:
    """
    Extracts the path to the text file from the configuration file.

    The function searches through the config file for the line starting with "linuxpath=".
    
    Args:
        file_path(str):Path to the configuration file.

    return: 
        Optional[str]:The Linux path if found, None otherwise.

    raises:
        FileNotFoundError if the configuration file is not found.
        ValueError if the path is not found in the configuration file.

    Example:
        >>> extract_linux_path("config.txt")
        '/home/user/text_files'
        
        >>> extract_linux_path("config.txt")
        Traceback (most recent call last):
        ...
        ValueError: Path not found in the configuration file.
    """
    try:
        with open(file_path, 'r') as config_file:
            for line in config_file:
                if line.startswith("linuxpath="):
                    path = line.strip().split("=")[1]
                    return path

        raise ValueError("Path not found in the configuration file.")

    except FileNotFoundError:
        print("Configuration file not found.")
        return None

    except Exception as e:
        print("An error occurred:", str(e))
        return None


