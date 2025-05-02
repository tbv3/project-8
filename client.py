import socket


VALID_QUERIES = {
        "1": "What is the average moisture inside my kitchen fridge in the past three hours?",
        "2": "What is the average water consumption per cycle in my smart dishwasher?",
        "3": "Which device consumed more electricity among my three IoT devices (two refrigerators and a dishwasher)?"
}

def client_echo():
    HOST = input("Enter an IP address: ")
    PORT = int(input("Enter a port number: "))

    while True:
        print("\nPlease choose a query to send:")
        print("1. Average moisture in kitchen fridge in last 3 hours?")
        print("2. Average water usage per cycle of dishwasher?")
        print("3. Which of the three devices consumed more electricity?")
        print("Type 'exit' to end")

        choice = input("Enter 1, 2, or 3, or type 'exit' to end: ").strip()

        if choice.lower() == 'exit':
            break
        elif choice in VALID_QUERIES:
            message = VALID_QUERIES[choice]
        else:
            print("Sorry, this query cannot be processed. Please choose between the options listed above.")
            continue

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientTCPSocket:
                clientTCPSocket.connect((HOST, PORT))
                clientTCPSocket.sendall(message.encode())
                message_modified = clientTCPSocket.recv(1024).decode()
                print("\nReceived from server:", message_modified)
        except Exception as e:
            print("Error:", e)

if __name__ == '__main__':
    client_echo()


