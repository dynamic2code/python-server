import socket
from unittest.mock import patch
from server import Server

def test_handle_connection():
    # Create a mock socket object
    mock_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Mock the behavior of the server
    with patch('socket.socket') as mock_socket:
        mock_server_socket = mock_socket.return_value
        mock_server_socket.accept.return_value = (mock_client_socket, ('127.0.0.1', 12345))

        # Create a server instance
        server = Server()

        # Mock the behavior of the file_searcher module
        with patch('file_searcher.linear_search_string') as mock_search_string:
            # Configure the mock behavior
            mock_search_string.return_value = True

            # Call the handle_connection method
            server.handle_connection(mock_client_socket)

            # Assertions
            mock_search_string.assert_called_once()
            mock_client_socket.send.assert_called_with('STRING EXISTS \n'.encode('utf-8'))


