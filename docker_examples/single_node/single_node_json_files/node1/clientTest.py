import socket
import json
import sys

def send_test(message, host, port):
    data = message
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        sock.connect((host, int(port)))
        sock.sendall(bytes(data + "\n", "utf-8"))
        # Receive data from the server and shut down
        received = str(sock.recv(1024), "utf-8")
        return received


def split(string):
    li = list(string.split(":"))
    return li


if __name__ == "__main__":
    args = sys.argv[1:]
    HOST = split(args[0])[0]
    PORT = int(split(args[0])[1])
    print(send_test(args[1], HOST, PORT))
