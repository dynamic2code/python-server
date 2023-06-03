import socket
import ssl
import string_verifier


class Client:
    def __init__(self):
        self.host: str = "localhost"
        self.port: int = 2000
        self.SSL_AUTHENTICATION: bool = False
        self.PSK: str = "my_secret_psk"

    def get_search_string(self):
        """
        Prompts the user to enter a search string and validates it.

        client_input(str):
            the user input

        return(str):
            The validated search string.

        Example:
            >>> client = Client()
            >>> client.get_search_string()
            Enter the string you wish to search: 12;0;1;28;0;17;4;0;
            '12;0;1;28;0;17;4;0;'
        
        """
        while True:
            client_input = input("Enter the string you wish to search: ")

            if not string_verifier.validate_string(client_input):
                print("Invalid input. Please enter a valid string.")
            else:
                return client_input

    def send_message(self):
        """
        Sends a search string to the server and receives the response.

        This function communicates with the server by sending the search string
        and receiving the response.

        Args:
            client_socket: Tcp socket 
            string(str):returned form the method geting user input
            response: response form the server

        return:
            None: None

        raises:
            ConnectionRefusedError if the connection is refused
            ConnectionResetError if the connection is reset
        
        Example:
            >>> client = Client()
            >>> client.send_message()
            Enter the string you wish to search: 12;0;1;28;0;17;4;0;
            Response from server: STRING FOUND.
            Enter the string you wish to search: exit
        """
        # Create a TCP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            if self.SSL_AUTHENTICATION:
                # Wrap the socket with SSL using PSK
                context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
                context.psk_client_callback = lambda identity: (self.PSK.encode("utf-8"), identity)
                context.set_ciphers('PSK-AES128-CBC-SHA')

                # Provide the server hostname or IP address for check_hostname
                server_hostname = self.host
                client_socket = context.wrap_socket(client_socket, server_hostname=server_hostname)


            # Connection with the server
            client_socket.connect((self.host, self.port))
            print("Enter 'exit' to close the connection.")

            while True:
                string = self.get_search_string()

                # Sending  the message to the server
                client_socket.send(string.encode("utf-8"))

                # Receiveing the response from the server
                response = client_socket.recv(1024).decode("utf-8")
                print("Response from server:", response)

                # option to exit
                if string.lower() == "exit":
                    break

        except ConnectionRefusedError:
            print("Connection refused by the server.")

        except ConnectionResetError:
            print("Connection reset by the server.")

        finally:
            # Closing the connection with server
            client_socket.close()

if __name__ == "__main__":
    # Create a Client instance with the server's host and port
    client = Client()
    # Send a message to the server
    client.send_message()