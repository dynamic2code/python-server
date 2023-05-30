def linear_search_string(file_path, search_string):
    with open(file_path, 'r') as file:
        for line in file:
            if search_string in line:
                return True
    
    return False
        