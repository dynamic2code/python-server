#standard libs
import socket

# modules

class Server:
    def __init__(self) -> None:

        self.data = ""
        self.HOST = "127.0.0.1"
        self.PORT = 1234
        self.response = ""


    def handle_connection(self,client_socket):
        # Receive the data from the client
        self.data = client_socket.recv(1024).decode("utf-8")
        print("Received data:", self.data)

        # Process the received string (you can add your logic here)
        # ...

        # Send a response back to the client
        response = "Response from server"
        client_socket.send(response.encode("utf-8"))

        # Close the connection
        client_socket.close()

    def start_server(self):
        # Create a TCP socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


        # Bind the socket to the host and port
        server_socket.bind((self.HOST, self.PORT))

        # Listen for incoming connections
        server_socket.listen(1)
        print("Server listening on {}:{}".format(self.HOST, self.PORT))

        while True:
            # Accept a client connection
            client_socket, client_address = server_socket.accept()
            print("Connection from:", client_address)

            # Handle the connection in a separate thread
            obj.handle_connection(client_socket)

if __name__ == "__main__":
    obj = Server()
    obj.start_server()
