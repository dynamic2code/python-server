# import socket
# from unittest.mock import patch
# from server import Server

# def test_handle_connection():
#     # Create a mock socket object
#     mock_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#     # Mock the behavior of the server
#     with patch('socket.socket') as mock_socket:
#         mock_server_socket = mock_socket.return_value
#         mock_server_socket.accept.return_value = (mock_client_socket, ('127.0.0.1', 12345))

#         # Create a server instance
#         server = Server()

#         # Mock the behavior of the file_searcher module
#         with patch('file_searcher.linear_search_string') as mock_search_string:
#             # Configure the mock behavior
#             mock_search_string.return_value = True

#             # Call the handle_connection method
#             server.handle_connection(mock_client_socket)

#             # Assertions
#             mock_search_string.assert_called_once()
#             mock_client_socket.send.assert_called_with('STRING EXISTS \n'.encode('utf-8'))

import pytest
import threading
import socket

from server import Server


def test_server_handle_connection():
    # Create a server instance
    server = Server()

    # Set the server properties for testing
    server.HOST = "127.0.0.1"
    server.PORT = 12345
    server.REREAD_ON_QUERY = False
    server.SSL_AUTHENTICATION = False

    # Start the server in a separate thread
    server_thread = threading.Thread(target=server.start_server)
    server_thread.start()

    # Sleep for a short time to allow the server to start listening
    # This can be adjusted as needed based on the server startup time
    # You may need to increase this if you encounter connection issues
    # with slower test environments or network conditions
    import time
    time.sleep(1)

    # Connect to the server using a client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server.HOST, server.PORT))

    # Send test data to the server
    data = "Hello, server!"
    client_socket.sendall(data.encode("utf-8"))

    # Receive the server's response
    response = client_socket.recv(1024).decode("utf-8")

    # Close the client socket
    client_socket.close()

    # Stop the server thread
    server_thread.join()

    # Check the response
    assert "STRING NOT FOUND" in response


