def extract_linux_path(file_path):
    """
    The function finds the path to the text file

    The function searches through the config file to the part with linuxpath= 

    """
    with open(file_path, 'r') as config_file:
        for line in config_file:
            if line.startswith("linuxpath="):
                path = line.strip().split("=")[1]
                print("Linux path:", path)
                return path
    
    print("Path not found in the configuration file.")
    return None


