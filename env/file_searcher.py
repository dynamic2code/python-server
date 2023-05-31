def linear_search_string(file_path: str, search_string: str) -> bool:
    """
    Performs a linear search for the given search string in the file.

    :param file_path: The path to the file to be searched.
    :type file_path: str
    :param search_string: The string to search for.
    :type search_string: str
    :return: True if the search string is found in the file, False otherwise.
    :rtype: bool
    """
    with open(file_path, 'r') as file:
        for line in file:
            if search_string in line:
                return True

    return False

        