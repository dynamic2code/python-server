import socket
from unittest.mock import patch
import string_verifier
from client import Client

def test_get_search_string_valid_input():
    # Mock the input function to provide a valid search string
    with patch('builtins.input', return_value='valid search string'):
        client = Client()
        search_string = client.get_search_string()
        assert search_string == 'valid search string'

def test_send_message(capsys):
    from sys import stderr
    # Mock the socket to simulate a ConnectionRefusedError
    with patch('socket.socket') as mock_socket:
        mock_client_socket = mock_socket.return_value
        mock_client_socket.connect.side_effect = ConnectionRefusedError

        with patch('builtins.input', side_effect=['search string', 'exit']):
            client = Client()
            client.send_message()

        # Assertions
        assert mock_client_socket.connect.call_count == 1
        assert mock_client_socket.send.call_count == 0
        assert mock_client_socket.close.call_count == 1
        assert "Connection refused by the server." in capsys.readouterr().out
