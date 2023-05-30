import os

def search_file(filename):
    """
    Takes in a file name and finds the path in the paticular OS

    The function is to improve flexibility and protability form one OS to another
    
    """
    for root, dirs, files in os.walk("/"):
        if filename in files:
            return os.path.join(root, filename)
    
    return None

