import mmap
from typing import List, Tuple


def linear_search_string(file_path: str, search_string: str) -> bool:
    """
    Performs a linear search for the given search string in the file.

    Args:
        file_path (str): The path to the file to be searched.
        search_string (str): The string to search for.

    Returns:
        bool: True if the search string is found in the file, False otherwise.

    Raises:
        FileNotFoundError: If the file path is not found.
        IOError: If an error occurs while reading the file.

    Example:
        >>> linear_search_string("file.txt", "apple")
        True
        
        >>> linear_search_string("file.txt", "banana")
        False
    """
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if search_string in line:
                    return True
            return False
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except IOError:
        print(f"Error reading file '{file_path}'.")


def naive_string_search(file_path: str, search_string: str) -> List[Tuple[int, str]]:
    """
    Perform a naive string search in a file.

    Args:
        file_path (str): The path to the file to be searched.
        search_string (str): The string to search for.

    Returns:
        List[Tuple[int, str]]: A list of tuples containing the line number and matching line text.

    Raises:
        FileNotFoundError: If the file specified by `file_path` does not exist.
        Exception: If an error occurs while performing the search.

    Example:
        >>> naive_string_search("file.txt", "apple")
        [(1, 'I have an apple.'), (4, 'The apple is red.')]

        >>> naive_string_search("file.txt", "banana")
        []
    """
    try:
        with open(file_path, 'r') as file:
            line_number = 1
            matches = []

            for line in file:
                if search_string in line:
                    matches.append((line_number, line.strip()))

                line_number += 1

            return matches

    except FileNotFoundError:
        raise FileNotFoundError("File not found: {}".format(file_path))

    except Exception as e:
        raise Exception("An error occurred: {}".format(str(e)))


def boyer_moore_search(file_path: str, search_string: str) -> bool:
    """
    Perform a Boyer-Moore string search in a file.

    Args:
        file_path (str): The path to the file to be searched.
        search_string (str): The string to search for.

    Returns:
        bool: True if the search string is found, False otherwise.

    Raises:
        FileNotFoundError: If the file specified by `file_path` does not exist.
        Exception: If an error occurs while performing the search.

    Example:
        >>> boyer_moore_search("file.txt", "apple")
        True

        >>> boyer_moore_search("file.txt", "banana")
        False
    """
    try:
        with open(file_path, 'r') as file:
            pattern_length = len(search_string)
            text = file.read()
            text_length = len(text)
            skip_table = {}

            # Preprocessing: Generate skip table
            for i in range(pattern_length - 1):
                skip_table[search_string[i]] = pattern_length - i - 1

            # Searching
            i = pattern_length - 1
            while i < text_length:
                j = pattern_length - 1
                while j >= 0 and text[i] == search_string[j]:
                    i -= 1
                    j -= 1

                if j == -1:
                    return True  # Match found

                i += skip_table.get(text[i], pattern_length)

            return False  # Match not found

    except FileNotFoundError:
        raise FileNotFoundError("File not found: {}".format(file_path))

    except Exception as e:
        raise Exception("An error occurred: {}".format(str(e)))


def mmap_search(file_path: str, search_string: str) -> bool:
    """
    Perform an mmap string search in a file.

    Args:
        file_path (str): The path to the file to be searched.
        search_string (str): The string to search for.

    Returns:
        bool: True if the search string is found, False otherwise.

    Raises:
        FileNotFoundError: If the file specified by `file_path` does not exist.
        Exception: If an error occurs while performing the search.

    Example:
        >>> mmap_search("file.txt", "apple")
        True

        >>> mmap_search("file.txt", "banana")
        False
    """
    try:
        with open(file_path, "r") as file:
            # Memory map the file
            with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                if mm.find(search_string.encode()) != -1:
                    return True  # Match found

            return False  # Match not found

    except FileNotFoundError:
        raise FileNotFoundError("File not found: {}".format(file_path))

    except Exception as e:
        raise Exception("An error occurred: {}".format(str(e)))


def rabin_karp_search(file_path: str, search_string: str) -> bool:
    """
    Perform a Rabin-Karp string search in a file.

    Args:
        file_path (str): The path to the file to be searched.
        search_string (str): The string to search for.

    Returns:
        bool: True if the search string is found, False otherwise.

    Raises:
        FileNotFoundError: If the file specified by `file_path` does not exist.
        Exception: If an error occurs while performing the search.

    Example:
        >>> rabin_karp_search("file.txt", "apple")
        True

        >>> rabin_karp_search("file.txt", "banana")
        False
    """
    try:
        with open(file_path, 'r') as file:
            pattern_length = len(search_string)
            text = file.read()
            text_length = len(text)

            # Calculate the hash value of the search string
            search_hash = hash(search_string)

            # Calculate the initial hash value of the first pattern_length characters of the text
            text_hash = hash(text[:pattern_length])

            # Iterate through the text
            for i in range(text_length - pattern_length + 1):
                # Compare the hash values and the actual strings
                if text_hash == search_hash and text[i:i+pattern_length] == search_string:
                    return True  # Match found

                # Calculate the rolling hash value for the next window of pattern_length characters
                if i < text_length - pattern_length:
                    text_hash = hash(text[i+1:i+1+pattern_length])

            return False  # Match not found

    except FileNotFoundError:
        raise FileNotFoundError("File not found: {}".format(file_path))

    except Exception as e:
        raise Exception("An error occurred: {}".format(str(e)))


def kmp_search(file_path: str, search_string: str) -> bool:
    """
    Perform a Knuth-Morris-Pratt (KMP) string search in a file.

    Args:
        file_path (str): The path to the file to be searched.
        search_string (str): The string to search for.

    Returns:
        bool: True if the search string is found, False otherwise.

    Raises:
        FileNotFoundError: If the file specified by `file_path` does not exist.
        Exception: If an error occurs while performing the search.

    Example:
        >>> kmp_search("file.txt", "apple")
        True

        >>> kmp_search("file.txt", "banana")
        False
    """
    try:
        with open(file_path, 'r') as file:
            pattern_length = len(search_string)
            text = file.read()
            text_length = len(text)

            # Preprocess the search string to generate the prefix table
            prefix_table = [0] * pattern_length
            j = 0
            for i in range(1, pattern_length):
                if search_string[i] == search_string[j]:
                    j += 1
                    prefix_table[i] = j
                else:
                    if j != 0:
                        j = prefix_table[j-1]
                        i -= 1
                    else:
                        prefix_table[i] = 0

            # Searching
            i = 0
            j = 0
            while i < text_length:
                if search_string[j] == text[i]:
                    i += 1
                    j += 1

                    if j == pattern_length:
                        return True  # Match found
                else:
                    if j != 0:
                        j = prefix_table[j-1]
                    else:
                        i += 1

            return False  # Match not found

    except FileNotFoundError:
        raise FileNotFoundError("File not found: {}".format(file_path))

    except Exception as e:
        raise Exception("An error occurred: {}".format(str(e)))


def bitap_search(file_path: str, search_string: str) -> bool:
    """
    Perform a Bitap (Shift-Or) string search in a file.

    Args:
        file_path (str): The path to the file to be searched.
        search_string (str): The string to search for.

    Returns:
        bool: True if the search string is found, False otherwise.

    Raises:
        FileNotFoundError: If the file specified by `file_path` does not exist.
        Exception: If an error occurs while performing the search.

    Example:
        >>> bitap_search("file.txt", "apple")
        True

        >>> bitap_search("file.txt", "banana")
        False
    """
    try:
        with open(file_path, 'r') as file:
            pattern_length = len(search_string)
            text = file.read()

            # Preprocessing - Generate the mask table
            mask_table = {}
            for char in search_string:
                mask_table[char] = 0
            mask = 1
            for i in range(pattern_length - 1, -1, -1):
                mask_table[search_string[i]] |= mask
                mask <<= 1

            # Searching
            text_length = len(text)
            pattern_mask = 1 << (pattern_length - 1)
            state = 0

            for i in range(text_length):
                state = (state << 1 | 1) & mask_table.get(text[i], 0)

                if state & pattern_mask != 0:
                    return True  # Match found

            return False  # Match not found

    except FileNotFoundError:
        raise FileNotFoundError("File not found: {}".format(file_path))

    except Exception as e:
        raise Exception("An error occurred: {}".format(str(e)))


def binary_search_string(file_path: str, search_string: str) -> bool:
    """
    Perform a binary search for the given search string in the file.

    Args:
        file_path (str): The path to the file to be searched.
        search_string (str): The string to search for.

    Returns:
        bool: True if the search string is found in the file, False otherwise.

    Raises:
        FileNotFoundError: If the file path is not found.
        IOError: If an error occurs while reading the file.

    Example:
        >>> binary_search_string("file.txt", "apple")
        True

        >>> binary_search_string("file.txt", "banana")
        False
    """
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            start = 0
            end = len(lines) - 1

            while start <= end:
                mid = (start + end) // 2
                line = lines[mid]

                if search_string in line:
                    return True
                elif search_string < line:
                    end = mid - 1
                else:
                    start = mid + 1

            return False

    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found.")
    except IOError:
        raise IOError(f"Error reading file '{file_path}'.")
