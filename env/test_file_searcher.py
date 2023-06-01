import os
from file_searcher import linear_search_string

def test_linear_search_string():
    # Test case 1: Search string found in the file
    file_path = "test_file.txt"
    search_string = "world"
    with open(file_path, 'w') as file:
        file.write("Hello, world!")

    assert linear_search_string(file_path, search_string) is True

    # Test case 2: Search string not found in the file
    file_path = "test_file.txt"
    search_string = "foo"
    with open(file_path, 'w') as file:
        file.write("Hello, world!")

    assert linear_search_string(file_path, search_string) is False

    # Test case 3: Empty file
    file_path = "empty_file.txt"
    search_string = "hello"
    open(file_path, 'w').close()  # Create an empty file

    assert linear_search_string(file_path, search_string) is False

    # Test case 4: Non-existing file
    file_path = "non_existing_file.txt"
    search_string = "hello"

    assert linear_search_string(file_path, search_string) is False

    # Clean up temporary files
    os.remove("test_file.txt")
    os.remove("empty_file.txt")

