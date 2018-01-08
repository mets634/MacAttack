import socket
import time
import re
from subprocess import call


def main():

    server_message = send_message("new")
    token = re.match(".+\|token=(.+)", server_message).group(1)
    username = re.match("username=([^|]+)", server_message).group(1)
    print "token = " + token
    print "username = " + username

    while True:
        server_message = send_message("next")
        print server_message
        run_script(token, username, server_message)
        continue
        print "block_number = " + block_number

        key = run_script(token, username, block_number)

        # if key is not empty then key found
        if key:
            client_socket.sendall("key=" + key)
            client_socket.close()
            exit(0)


def send_message(message):
    client_socket = socket.socket()
    client_socket.connect(('127.0.0.1', 3626))
    client_socket.sendall(message)
    server_message = client_socket.recv(1024)
    client_socket.close()
    return server_message

def run_script(token, username, block_number):
    time.sleep(2)
    # call(["./script", "token", "username", "block_number"])
    key = 0
    return key


if __name__ == '__main__':
    main()
