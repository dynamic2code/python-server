import os
from find_file import search_file

def test_search_file():
    #File exists in the current directory
    current_directory = os.getcwd()
    file_name = "test_file.txt"
    file_path = os.path.join(current_directory, file_name)
    open(file_path, 'w').close()  # Create an empty file

    assert search_file(file_name) == file_path

    # where File does not exist
    non_existing_file = "non_existing_file.txt"

    assert search_file(non_existing_file) is None

    # Clean up temporary files and directories
    os.remove(os.path.join(current_directory, "test_file.txt"))


