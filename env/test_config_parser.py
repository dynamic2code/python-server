from config_parser import extract_linux_path

def test_extract_linux_path():
    # if Path found in the configuration file
    file_path = "config_file.conf"
    expected_path = "/root/200k.txt"
    result = extract_linux_path(file_path)
    assert result == expected_path

    # if Empty configuration file
    file_path = "empty_config_file.conf"
    result = extract_linux_path(file_path)
    assert result is None

    # if Configuration file with invalid format
    file_path = "invalid_config_file.conf"
    result = extract_linux_path(file_path)
    assert result is None

    # if Non-existing configuration file
    file_path = "non_existing_config_file.conf"
    result = extract_linux_path(file_path)
    assert result is None

