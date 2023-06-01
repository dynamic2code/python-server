from string_verifier import validate_string

def test_validate_string():
    # Test case 1: Valid string
    input_string = "Hello, world!"
    result = validate_string(input_string)
    assert result == (True, "Input string is valid.")

    # Test case 2: Empty string
    input_string = ""
    result = validate_string(input_string)
    assert result == (True, "Input string is valid.")

    # Test case 3: Non-string input
    input_string = 12345
    result = validate_string(input_string)
    assert result == (False, "ValueError: Input is not a string.")

    # Test case 4: String with special characters
    input_string = "Hello, @world!"
    result = validate_string(input_string)
    assert result == (True, "Input string is valid.")

