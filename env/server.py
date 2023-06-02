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
        self.SSL_AUTHENTICATION: bool = False
        self.PSK: str = "my_secret_psk"
        self.execution_time: float = 0

        # Configuration of the logging
        logging.basicConfig(filename='server.log', encoding='utf-8', level=logging.DEBUG)

    def handle_connection(self, client_socket: socket.socket) -> None:
        """
        Handles the connection with a client.

        Args:
            client_socket(socket.socket): The socket object for the client connection.
        
        return:
            None

        raise:
            FileNotFoundErro: if an file path error occurs
            Exception: any other error occurse
            ConnectionError: if a server connection error occurs
            ssl.SSLError: if an error with ssl authentication occurs
            BrokenPipeErro: if the connection is interupted
        """
        try:
            while True:
                if self.SSL_AUTHENTICATION:
                    # Wrap the socket with SSL using PSK
                    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                    context.psk_server_callback = lambda identity: self.PSK.encode("utf-8")
                    context.set_ciphers('PSK-AES128-CBC-SHA')
                    client_socket = context.wrap_socket(client_socket, server_side=True)

                # Receive the data of max payload of 1024 from the client
                client_string = client_socket.recv(1024)
                self.data = client_string.rstrip(b'\x00').decode("utf-8")

                # Re-reads file if REREAD_ON_QUERY is set to True else just reads once
                while self.REREAD_ON_QUERY:
                    try:
                        # Capture the start time
                        start_time = time.time()
                        #to be used when file paths are not known
                        # # Get file path of the txt file
                        # config_file = find_file.search_file("config_file.conf")
                        # file_path_from_config = config_parser.extract_linux_path(config_file)

                        # # File name of the txt file
                        # file_name = os.path.basename(file_path_from_config)

                        # # Full path of the txt file
                        # file_path = find_file.search_file(file_name)

                        config_file = "/home/grrhrwh/Documents/GitHub/-Introductory-Task-for-Software-Engineers-at-Algorithmic-Sciences/env/config_file.conf"
                        file_path_from_config = config_parser.extract_linux_path(config_file)
                        file_path = file_path_from_config
                        # Send a response back to the client
                        if file_searcher.binary_search_string(file_path, self.data):
                            response = "STRING EXISTS \n"
                        else:
                            response = "STRING NOT FOUND \n"

                        client_socket.send(response.encode("utf-8"))

                        end_time = time.time()
                    except FileNotFoundError:
                        response = "Config file not found \n"
                        client_socket.send(response.encode("utf-8"))
                        break

                    except Exception as e:
                        response = "An error occurred during file search or parsing: {}\n".format(str(e))
                        client_socket.send(response.encode("utf-8"))
                        break

                else:
                    try:
                        # to use when the paths are not given
                        # # Get file path of the txt file
                        # config_file = find_file.search_file("config_file.conf")
                        # file_path_from_config = config_parser.extract_linux_path(config_file)

                        # # File name of the txt file
                        # file_name = os.path.basename(file_path_from_config)

                        # # Full path of the txt file
                        # file_path = find_file.search_file(file_name)

                        # Capture the start time
                        start_time = time.time()
                        config_file = "/home/grrhrwh/Documents/GitHub/-Introductory-Task-for-Software-Engineers-at-Algorithmic-Sciences/env/config_file.conf"
                        file_path_from_config = config_parser.extract_linux_path(config_file)
                        file_path = file_path_from_config
                        # Send a response back to the client
                        if file_searcher.naive_string_search(file_path, self.data):
                            response = "STRING EXISTS \n"
                        else:
                            response = "STRING NOT FOUND \n"

                        client_socket.send(response.encode("utf-8"))
                        end_time = time.time()
                    except FileNotFoundError:
                        response = "Config file not found \n"
                        client_socket.send(response.encode("utf-8"))

                    except Exception as e:
                        response = "An error occurred during file search or parsing: {}\n".format(str(e))
                        client_socket.send(response.encode("utf-8"))

                end_time = time.time()
                self.execution_time = end_time - start_time

                logging.debug("Execution time: {:.2f} seconds \nReceived data: {}\nReceived data at: {}".format(
                    self.execution_time, self.data, datetime.now().time()))

        except ConnectionError as ce:
            response = "Connection error occurred: {}\n".format(str(ce))
            client_socket.send(response.encode("utf-8"))

        except ssl.SSLError as ssl_error:
            response = "SSL error occurred during handshake: {}\n".format(str(ssl_error))
            client_socket.send(response.encode("utf-8"))

        except BrokenPipeError as e:
            response = "Broken pipe error:: {}\n".format(str(e))
            client_socket.send(response.encode("utf-8"))

    def start_server(self) -> None:
        """
        Starts the server and listens for incoming connections.

        return: 
            None

        rise:
            OSError: if an os error occurs
            Exception: any other error occurs 

        """
        try:
            # Create a TCP socket
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Bind the socket to the host and port
            server_socket.bind((self.HOST, self.PORT))

            # Listen for incoming connections
            server_socket.listen(0)
            print("Server listening on {}:{}".format(self.HOST, self.PORT))

            while True:
                # Accept a client connection
                client_socket, client_address = server_socket.accept()

                # Handle each connection in a separate thread
                thread = threading.Thread(target=self.handle_connection, args=(client_socket,))
                thread.start()

                logging.debug("Connection from: {}\nExecution time: {:.2f} seconds \nReceived data: {} \nReceived data at: {}".format(
                    client_address, self.execution_time, self.data, datetime.now().time()))

        except OSError as os_error:
            response = "OS error occurred during socket operations: {}\n".format(str(os_error))
            print(response)

        except Exception as e:
            response = "An error occurred during server startup or listening: {}\n".format(str(e))
            print(response)


if __name__ == "__main__":
    obj = Server()
    obj.start_server()

