from socket import *
import argparse
import threading

def client_thread(connectionSocket, addr, username, password):
    # print("INDIRA: starting client thread for user", username, "with address", addr)
    connectionSocket.close()


def start_server(port, passcode):
    # create socket - using IPv4, specifying TCP
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('127.0.0.1', port))

    # 5.1/5.2 - mandatory print statement
    statement1 = "Server started on port " + str(port) + ". Accepting connections"
    print(statement1)

    serverSocket.listen()  # defaults to maximum of 128 or 512 in the connection queue
    while True:
        # establishing connection between clientSocket that "knocked" and connectionSocket
        connectionSocket, addr = serverSocket.accept()

        try:
            loginInfo = connectionSocket.recv(1024).decode().split(" ")

            # Ensure loginInfo contains both username and password
            if len(loginInfo) < 2:
                connectionSocket.send("Invalid input".encode())
                connectionSocket.close()
                continue  # Wait for next client

            username, password = loginInfo[0], loginInfo[1]

            if password == passcode:
                responseMessage = "Valid password"
                connectionSocket.send(responseMessage.encode())

                print(f"{username} joined the chatroom")

                # Start client thread only after successful login
                new_client_thread = threading.Thread(target=client_thread, args=(connectionSocket, addr, username, password))
                new_client_thread.start()
            else:
                responseMessage = "Invalid password"
                connectionSocket.send(responseMessage.encode())
                connectionSocket.close()
        
        except Exception as e:
            print(f"Error handling client {addr}: {e}")
            connectionSocket.close()

        # close connectionSocket - MOVED TO client_thread

if __name__ == "__main__":
    # set up argument parser for 'python3 server.py -start -port <port> -passcode <passcode>'
    parser = argparse.ArgumentParser(description="Start a simple chat server.")
    parser.add_argument("-start", action="store_true", help="Start the server")
    parser.add_argument("-port", type=int, required=True, help="Port number to run the server on")
    parser.add_argument("-passcode", type=str, required=True, help="Passcode for authentication")
    
    args = parser.parse_args()
    if args.start:
        start_server(args.port, args.passcode)