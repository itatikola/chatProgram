from socket import *
import argparse

def start_client(hostname, port, username, password):
    # create socket - using IPv4, specifying TCP
    clientSocket = socket(AF_INET, SOCK_STREAM)

    # establishing connection to server
    clientSocket.connect((hostname, port))
    print("Connected to", hostname, "on port", port)  # mandatory output line (Section 5.1)

    # get data to send to server
    sentence = input("Input lowercase sentence:")

    # send data to server
    clientSocket.send(sentence.encode())

    # receive data from server
    modifiedSentence = clientSocket.recv(1024)

    # close client
    print("From Server: ", modifiedSentence.decode())
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
        start_client(args.host, args.port, args.username, args.password)