from socket import *
import argparse
import threading
import sys

'''
Handles receiving and displaying messages from the server.
'''
def receive_messages(clientSocket, username):
    # print("INDIRA: started receiving messages thread for", username)
    while True:
        message = clientSocket.recv(1024).decode()
        print(message)
        sys.stdout.flush()

'''
Initiates the client socket, mimicking the idea of the client "joining the chatroom."
'''
def join_chatroom(hostname, port, username, password):
    # create socket - using IPv4, specifying TCP
    clientSocket = socket(AF_INET, SOCK_STREAM)

    # establishing connection to server
    clientSocket.connect((hostname, port))
    
    # send login information to server
    loginInfo = username + " " + password
    clientSocket.send(loginInfo.encode())

    # receive data from server
    serverResponse = clientSocket.recv(1024).decode()
    if serverResponse == "Valid password":
        # 5.1/5.2 - mandatory output line
        print("Connected to", hostname, "on port", port)
        sys.stdout.flush()

        # start new thread for receiving messages
        receive_thread = threading.Thread(target=receive_messages, args=(clientSocket, username))
        receive_thread.daemon = True
        receive_thread.start()

        # reserve main thread for sending messages
        while True:
            sendingMessage = input("")
            clientSocket.send(sendingMessage.encode())

            if sendingMessage == ":Exit":
                break

        clientSocket.close()


if __name__ == "__main__":
    # set up argument parser for 'python3 client.py -join -host <hostname> -port <port> -username <username> -passcode <passcode>'
    parser = argparse.ArgumentParser(description="Start a simple chat client.")
    parser.add_argument("-join", action="store_true", help="New client is joining the server")
    parser.add_argument("-host", type=str, required=True, help="Destination server hostname")
    parser.add_argument("-port", type=int, required=True, help="Destination port number")
    parser.add_argument("-username", type=str, required=True, help="Client's username/display name - will be less than or equal to 8 characters")
    parser.add_argument("-password", type=str, required=True, help="Client's password - must be less than or equal to 5 characters, won't be greater than 20 characters")

    
    args = parser.parse_args()
    if args.join:
        join_chatroom(args.host, args.port, args.username, args.password)