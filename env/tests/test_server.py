import pytest
import threading
from server import Server

# Define a global variable to check if the server was started
server_started = False

# Define a global variable to store the server object
server_obj = None

# Create a test function to start the server
def start_server():
    global server_started, server_obj
    server_obj = Server()
    server_obj.start_server()
    server_started = True

def test_start_server():
    # Create a thread to start the server
    thread = threading.Thread(target=start_server)
    thread.start()

    # Wait for the server to start
    thread.join(timeout=2)

    # Assert that the server was started successfully
    assert server_started



