import socket

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def get_search_string(self):
        """
        Gets the user input.

        recieves the string to be searched from the user and checks if it is a valid input.

        :client_input: holds the user input.
        :type client_input: Type of arg1
        :search_string: holds the string after validation.
        :type search_string: Str
        :return: Description of the return value.
        :rtype: Type of the return value
        :raises SpecificException: Description of the raised exception(s), if any.
        """
        client_input = input("Enter the string you wish to search: ")
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

        while True:
            string = client.get_search_string()

            try:
                # Connect to the server
                client_socket.connect((self.host, self.port))

                # Send the message to the server
                client_socket.send(string.encode("utf-8"))

                # Receive the response from the server
                response = client_socket.recv(1024).decode("utf-8")
                print("Response from server:", response)

            finally:
                # Close the socket
                client_socket.close()

if __name__ == "__main__":
    # Create a Client instance with the server's host and port
    client = Client("127.0.0.1", 1234)

    # Send a message to the server
    
    client.send_message()