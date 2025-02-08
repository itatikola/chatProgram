from socket import *
import argparse

def start_server(port, passcode):
    if False:
        return
    
    # create socket - using IPv4, specifying TCP
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', port))
    print("Server started on port", port, ". Accepting connections")  # mandatory print statement
    serverSocket.listen(1)  # 1 = maximum number of queued connections
    while True:
        # establishing connection between clientSocket that "knocked" and connectionSocket
        connectionSocket, addr = serverSocket.accept()

        print("Heard from client")

        # receive messages from clientSocket
        sentence = connectionSocket.recv(1024).decode()
        #print("<username> joined the chatroom")  # mandatory print statement
        capitalizedSentence = sentence.upper()
        connectionSocket.send(capitalizedSentence.encode())

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