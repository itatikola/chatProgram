from socket import *
import argparse
import threading
import sys
from datetime import datetime, timedelta

clients = {}  # global map of username : connection socket
clientsLock = threading.Lock()  # threading lock for the clients dictionary

'''
Thread-safe helper method for displaying the current clients dictionary.
'''
def print_all_clients():
    with clientsLock:
        for user in clients:
            print(user, clients[user])
            sys.stdout.flush()

'''
Thread-safe helper method for broadcasting the same message to all clients.

If there is a sending user, do not broadcast to this user.
'''
def broadcast_to_all_clients(message, sendingUser=None):
    with clientsLock:
        for user in clients:
            if user != sendingUser:
                clients[user].send(message.encode())

'''
Thread-safe helper method for broadcasting the same message to a specific client.
'''
def broadcast_to_specific_client(message, receivingUser):
    with clientsLock:
        clients[receivingUser].send(message.encode())

'''
Handling an authenticated connection socket.
'''
def client_thread(connectionSocket, addr, username, password):
    newClientMessage = "Correct passcode"
    existingClientMessage = username + " joined the chatroom"

    # 5.1/5.2 mandatory print statement on server
    print(existingClientMessage)
    sys.stdout.flush()

    with clientsLock:
        # Notify new client (that they successfully were authenticated)
        connectionSocket.send(newClientMessage.encode())
        # Add existing client to clients dictionary
        clients[username] = connectionSocket
    
    # Notify existing clients that the new client joined
    broadcast_to_all_clients(existingClientMessage, username)
    
    # print_all_clients()
    
    # Handle incoming messages from clients, send out to all other clients
    while True:
        chat = connectionSocket.recv(1024).decode()

        try:
            # Handle user leaving chatroom
            if chat == ":Exit":
                # Notify server & clients
                leavingMessage = f"{username} left the chatroom"
                print(leavingMessage)
                sys.stdout.flush()
                broadcast_to_all_clients(leavingMessage, username)

                # Delete user from clients dictionary
                with clientsLock:
                    del clients[username]

                # Close connection socket
                connectionSocket.close()
                break

            # Sending messages
            if chat.startswith(":dm"): # Handling direct messages - :dm <receiving user> <message>
                # Parse and format input
                chat = chat[4:]
                receivingUser = chat[:chat.find(" ")]
                privateChat = chat[chat.find(" ") + 1:]

                # Create messages
                serverMessage = f"{username} to {receivingUser}: {privateChat}"
                receiverMessage = f"{username}: {privateChat}"

                # Send messages
                print(serverMessage)
                sys.stdout.flush()
                broadcast_to_specific_client(receiverMessage, receivingUser)
            else: # Handling regular messages
                chatMessage = f"{username}: {chat}"
                print(chatMessage)
                sys.stdout.flush()
                broadcast_to_all_clients(chatMessage, username)
        except Exception as e:
            print(f"Error: {e}")
            sys.stdout.flush()


'''
Starts server socket and authenticates connection sockets.
'''
def start_server(port, passcode):
    # create socket - using IPv4, specifying TCP
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('127.0.0.1', port))

    # 5.1/5.2 - mandatory print statement
    statement1 = "Server started on port " + str(port) + ". Accepting connections"
    print(statement1)
    sys.stdout.flush()

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

            # Authenticating user
            if password == passcode:
                # Start client thread only after successful login
                new_client_thread = threading.Thread(target=client_thread, args=(connectionSocket, addr, username, password))
                new_client_thread.daemon = True
                new_client_thread.start()

            else:
                newClientMessage = "Incorrect passcode"
                connectionSocket.send(newClientMessage.encode())
                connectionSocket.close()
        except Exception as e:
            print(f"Error handling client {addr}: {e}")
            sys.stdout.flush()
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