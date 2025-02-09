from socket import *
import argparse

def start_server(port, passcode):
    if False:
        return
    
    # create socket - using IPv4, specifying TCP
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('127.0.0.1', port))

    # 5.1/5.2 - mandatory print statement
    statement1 = "Server started on port " + str(port) + ". Accepting connections"
    print(statement1)

    serverSocket.listen(1)  # 1 = maximum number of queued connections
    while True:
        # establishing connection between clientSocket that "knocked" and connectionSocket
        connectionSocket, addr = serverSocket.accept()

        # receive messages from clientSocket
        loginInfo = connectionSocket.recv(1024).decode().split(" ")
        username, password = loginInfo[0], loginInfo[1]

        if password == passcode:
            responseMessage = "Valid password"
            connectionSocket.send(responseMessage.encode())

            # 5.1/5.2 - mandatory print statement
            print(username, "joined the chatroom")
        else:
            responseMessage = "Invalid password"
            connectionSocket.send(responseMessage.encode())

        # close connectionSocket
        connectionSocket.close()



if __name__ == "__main__":
    # set up argument parser for 'python3 server.py -start -port <port> -passcode <passcode>'
    parser = argparse.ArgumentParser(description="Start a simple chat server.")
    parser.add_argument("-start", action="store_true", help="Start the server")
    parser.add_argument("-port", type=int, required=True, help="Port number to run the server on")
    parser.add_argument("-passcode", type=str, required=True, help="Passcode for authentication")
    
    args = parser.parse_args()
    if args.start:
        start_server(args.port, args.passcode)