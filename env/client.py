import socket
import ssl
import string_verifier


class Client:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 1234
        self.SSL_AUTHENTICATION = True
        self.PSK = "my_secret_psk"

    def get_search_string(self):
        """
        Prompts the user to enter a search string and validates it.

        :return: The validated search string.
        :rtype: str
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

        :return: None
        :rtype: None
        """
        while self.SSL_AUTHENTICATION:

            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            ssl_context.verify_mode = ssl.CERT_REQUIRED

            # Set PSK identity and key
            ssl_context.set_psk_identity("client_identity")
            ssl_context.set_psk_key(self.PSK.encode("utf-8"))

            # Create a TCP socket
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket = ssl_context.wrap_socket(client_socket, server_hostname=self.host)

            try:
                # Connect to the server
                client_socket.connect((self.host, self.port))
                print("Enter 'exit' to close the connection.")

                while True:
                    string = self.get_search_string()

                    # Send the message to the server
                    client_socket.send(string.encode("utf-8"))

                    # Receive the response from the server
                    response = client_socket.recv(1024).decode("utf-8")
                    print("Response from server:", response)

                    # Check if the user wants to exit
                    if string.lower() == "exit":
                        break

            except ConnectionRefusedError:
                print("Connection refused by the server.")

            except ConnectionResetError:
                print("Connection reset by the server.")

            finally:
                # Close the socket
                client_socket.close()

        else:
            # Create a TCP socket
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            try:
                # Connect to the server
                client_socket.connect((self.host, self.port))
                print("Enter 'exit' to close the connection.")

                while True:
                    string = self.get_search_string()

                    # Send the message to the server
                    client_socket.send(string.encode("utf-8"))

                    # Receive the response from the server
                    response = client_socket.recv(1024).decode("utf-8")
                    print("Response from server:", response)

                    # Check if the user wants to exit
                    if string.lower() == "exit":
                        break

            except ConnectionRefusedError:
                print("Connection refused by the server.")

            except ConnectionResetError:
                print("Connection reset by the server.")

            finally:
                # Close the socket
                client_socket.close()

if __name__ == "__main__":
    # Create a Client instance with the server's host and port
    client = Client()
    # Send a message to the server
    client.send_message()