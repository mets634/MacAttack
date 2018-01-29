import socket
import time
import re
from subprocess import call


def main():
    # send 'new' message to server and receive token and username
    server_message = send_message("new")
    # extract token from server message
    token = re.match("token=(.+)", server_message).group(1)

    print "token = " + token

    while True:
        # send 'next' message and receive new block number
        block_number = send_message("next")
        print server_message

        # run the script with the provided username, token and block number
        print "block_number = " + block_number

        # run script and get key
        key = run_script(token, block_number)

        # if key is not empty then key found
        if key != 0:
            send_message("key=" + str(key))
            exit(0)


def send_message(message):
    """
        send message to server and get message from server
    :param message: message to send
    :return: message from server
    """
    # create socket
    client_socket = socket.socket()
    # connect to server
    client_socket.connect(('127.0.0.1', 3626))
    # send message
    client_socket.sendall(message)
    # receive message
    server_message = client_socket.recv(1024)
    # close socket
    client_socket.close()

    return server_message


def run_script(token, block_number):
    """
        run the c program to find the key for the hash
    :param token: token to break
    :param block_number: block number to process
    :return: key; if key not found then return 0
    """
    time.sleep(2)
    print "block number = " + str(int(block_number, 16))

    # TODO: Change path to differ for each OS
    # run program with given params
    return subprocess.check_output(['MacSmasher.exe', token, str(block_number)])


if __name__ == '__main__':
    main()
