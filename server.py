import socket


# capitalize message
def capitalize_message(message):
    return message.upper()


def server_echo():

    HOST = input("Enter an IP address: ")
    PORT = int(input("Enter a port number: "))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverTCPSocket:
        serverTCPSocket.bind((HOST, PORT))
        serverTCPSocket.listen()

        print("Server listening from port: ", PORT)
        # accept client connection
        while True:
            client_socket, client_address = serverTCPSocket.accept()
            print("Connected to client: ", client_address)

            with client_socket:
                while True:
                    message_received = client_socket.recv(1024)
                    if not message_received:
                        break

                    print(message_received)
                    # capitalize message and send it back to client
                    modified_message = capitalize_message(message_received.decode())
                    client_socket.sendall(modified_message.encode())


if __name__ == '__main__':
    server_echo()
