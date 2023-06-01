import socket
import os
import threading
from datetime import datetime
import time
import logging
import ssl

import file_searcher
import config_parser
import find_file


class Server:
    def __init__(self) -> None:
        """
        Initializes the Server class.

        """
        self.data: str = ""
        self.HOST: str = "127.0.0.1"
        self.PORT: int = 1234
        self.response: str = ""
        self.REREAD_ON_QUERY: bool = False
        self.SSL_AUTHENTICATION: bool = True
        self.PSK: str = "my_secret_psk"
        self.execution_time: float = 0

        # Configuration of the logging
        logging.basicConfig(filename='server.log', encoding='utf-8', level=logging.DEBUG)

    def handle_connection(self, client_socket: socket.socket) -> None:
        """
        Handles the connection with a client.

        :param client_socket: The socket object for the client connection.
        :type client_socket: socket.socket
        :return: None
        :rtype: None
        """
        while True:
            # Capture the start time
            start_time = time.time()

            # Receive the data of max payload of 1024 from the client
            client_string = client_socket.recv(1024)
            self.data = client_string.rstrip(b'\x00').decode("utf-8")

            # Re-reads file if REREAD_ON_QUERY is set to True else just reads once
            while self.REREAD_ON_QUERY:
                # Get file path of the txt file
                config_file = find_file.search_file("config_file.conf")
                file_path_from_config = config_parser.extract_linux_path(config_file)

                # File name of the txt file
                file_name = os.path.basename(file_path_from_config)

                # Full path of the txt file
                file_path = find_file.search_file(file_name)

                # Send a response back to the client
                if file_searcher.linear_search_string(file_path, self.data):
                    response = "STRING EXISTS \n"
                else:
                    response = "STRING NOT FOUND \n"

                client_socket.send(response.encode("utf-8"))

            else:
                # Get file path of the txt file
                config_file = find_file.search_file("config_file.conf")
                file_path_from_config = config_parser.extract_linux_path(config_file)

                # File name of the txt file
                file_name = os.path.basename(file_path_from_config)

                # Full path of the txt file
                file_path = find_file.search_file(file_name)

                # Send a response back to the client
                if file_searcher.linear_search_string(file_path, self.data):
                    response = "STRING EXISTS \n"
                else:
                    response = "STRING NOT FOUND \n"

                client_socket.send(response.encode("utf-8"))

            end_time = time.time()
            self.execution_time = end_time - start_time

            logging.debug("Execution time: {:.2f} seconds \nReceived data: {}\nReceived data at: {}".format(
                self.execution_time, self.data, datetime.now().time()))

    def start_server(self) -> None:
        """
        Starts the server and listens for incoming connections.

        :return: None
        :rtype: None
        """
        # Create a TCP socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the host and port
        server_socket.bind((self.HOST, self.PORT))

        # Listen for incoming connections
        server_socket.listen(0)
        print("Server listening on {}:{}".format(self.HOST, self.PORT))

        while True:
            while self.SSL_AUTHENTICATION:
                # Accept a client connection
                client_socket, client_address = server_socket.accept()

                # Wrap the socket with SSL
                ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
                ssl_context.load_cert_chain(certfile="server.crt", keyfile="server.key")
                ssl_context.load_psk_identity(identity=self.PSK, psk=self.PSK)
                ssl_socket = ssl_context.wrap_socket(client_socket, server_side=True)

                # Handle each connection in a separate thread
                thread = threading.Thread(target=self.handle_connection, args=(ssl_socket,))
                thread.start()

                logging.debug("Connection from: {}\nExecution time: {:.2f} seconds \nReceived data: {} \nReceived data at: {}".format(
                    client_address, self.execution_time, self.data, datetime.now().time()))



            else:
                # Accept a client connection
                client_socket, client_address = server_socket.accept()

                # Handle each connection in a separate thread
                thread = threading.Thread(target=self.handle_connection, args=(client_socket,))
                thread.start()

                logging.debug("Connection from: {}\nExecution time: {:.2f} seconds \nReceived data: {} \nReceived data at: {}".format(
                    client_address, self.execution_time, self.data, datetime.now().time()))


if __name__ == "__main__":
    obj = Server()
    obj.start_server()
