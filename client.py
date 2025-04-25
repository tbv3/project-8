import socket


def client_echo():

    HOST = input("Enter an IP address: ")
    PORT = int(input("Enter a port number: "))

    while True:
        message = input("Enter a message to send or type 'exit' to exit: ")
        if message.lower() == 'exit':
            break

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientTCPSocket:
                clientTCPSocket.connect((HOST, PORT))
                clientTCPSocket.sendall(message.encode())
                message_modified = clientTCPSocket.recv(1024).decode()
                print("Received from server: ", message_modified)

        except Exception as e:
            print("Error: ", e)


if __name__ == '__main__':
    client_echo()
