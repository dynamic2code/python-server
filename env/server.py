#standard libs
import socket
import os
import threading
from datetime import datetime
import time
import logging


# modules
import file_searcher
import config_parser
import find_file
class Server:
    def __init__(self) -> None:

        self.data = ""
        self.HOST = "127.0.0.1"
        self.PORT = 1234
        self.response = ""
        self.REREAD_ON_QUERY = False
        self.SSLAUTHENTICATION = False
        # Configuration of the logging
        logging.basicConfig(filename='server.log', encoding='utf-8', level=logging.DEBUG)



    def handle_connection(self,client_socket):
        """
        """
        # Capture the start time
        start_time = time.time()
        # Receive the data of max payload of 1024 from the client
        client_string = client_socket.recv(1024)
        self.data = client_string.rstrip(b'\x00').decode("utf-8")

        # re-reads file if REREAD_ON_QUERY is set to true else just reads ones 
        while self.REREAD_ON_QUERY:
            #get file path of the txt file
            config_file = find_file.search_file("config_file.conf")
            file_path_from_config = config_parser.extract_linux_path(config_file)

            # file name of the txt file 
            file_name = os.path.basename(file_path_from_config)

            #full path of the txt file
            file_path = find_file.search_file(file_name)
                
            # Send a response back to the client
            if file_searcher.linear_search_string(file_path,self.data):
                response = "STRING EXISTS \n"
            else:
                response = "STRING NOT FOUND \n"
            
            client_socket.send(response.encode("utf-8"))

        else:
            #get file path of the txt file
            config_file = find_file.search_file("config_file.conf")
            file_path_from_config = config_parser.extract_linux_path(config_file)

            # file name of the txt file 
            file_name = os.path.basename(file_path_from_config)

            #full path of the txt file
            file_path = find_file.search_file(file_name)
                
            # Send a response back to the client
            if file_searcher.linear_search_string(file_path,self.data):
                response = "STRING EXISTS \n"
            else:
                response = "STRING NOT FOUND \n"
            
            client_socket.send(response.encode("utf-8"))

        # Close the client-server connection
        # client_socket.close()

        end_time = time.time()

        execution_time = end_time - start_time
        logging.debug("Execution time: {:.2f} seconds \n Received data:{}\n Received data at:{}".format(execution_time, self.data, datetime.now().time()))
        

    def start_server(self):
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

            # logging.debug("Connection from:", client_address)

if __name__ == "__main__":
    obj = Server()
    obj.start_server()
