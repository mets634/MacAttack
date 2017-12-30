import socket
import time


def main():
    client_socket = socket.socket()

    client_socket.connect(('127.0.0.1', 3626))
    token = client_socket.recv(1024).split("=", 1)[1]
    username = client_socket.recv(1024).split("=", 1)[1]
    print "token = " + token
    print "username = " + username

    while True:
        client_socket.sendall("next")
        block_number = client_socket.recv(1024).split("=", 1)[1]
        print "block_number = " + block_number

        key = run_script(token, username, block_number)

        # if key is not empty then key found
        if key:
            client_socket.sendall("done|key=" + key)
            client_socket.close()
            exit(0)

def run_script(token, username, block_number):
    time.sleep(5)
    key = 0
    return key


if __name__ == '__main__':
    main()
