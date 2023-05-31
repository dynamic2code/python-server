import socket

import string_verifier

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def get_search_string(self):
        client_input = input("Enter the string you wish to search: ")

        if string_verifier.validate_string(client_input)[0] == False:
            print(string_verifier.validate_string(client_input)[1])
        elif string_verifier.validate_string(client_input):
            print(string_verifier.validate_string(client_input)[1])
            search_string = client_input
            return search_string


    def send_message(self):
        """
        The function uses the returned search_string and sends it to the server.

        The pourpose of this function is communicating with the server. It sends the string and recieves response.

        :string: the string recieved from the user.
        :type sttring: Str
        :response: response from the server.
        :type response: Type of arg2
        :return: None.
        :rtype: None.
        :raises SpecificException: Description of the raised exception(s), if any.
        """
        # Create a TCP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connect to the server
        client_socket.connect((self.host, self.port))
        print("Enter exit to close connection")
        while True:
            string = client.get_search_string()

            try:
                # Send the message to the server
                client_socket.send(string.encode("utf-8"))

                # Receive the response from the server
                response = client_socket.recv(1024).decode("utf-8")
                print("Response from server:", response)

                client_socket.close()
                # # Check if the user wants to exit
                # if string.lower() == "exit":
                #     break

            except BrokenPipeError:
                print("Connection closed by the server.")

                # Reconnect to the server
                client_socket.close()
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((self.host, self.port))

        # Close the socket
        # client_socket.close()



if __name__ == "__main__":
    # Create a Client instance with the server's host and port
    client = Client("127.0.0.1", 1234)
    # Send a message to the server
    client.send_message()