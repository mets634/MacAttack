import socket
import sys


class Master(object):
    """
        Class contains all variables and function the master uses

        variables:
            token - the token to break
            username - the username in the token
    """

    def __init__(self, token):
        """
            initialize all variables
        :param token: the token to break
        """
        self._token = token
        self._block_counter = 0

        # initialize socket
        self.init_socket()

    def init_socket(self):
        """
            initialize server socket
        """
        self._server_socket = socket.socket()

        self._server_socket.bind(("0.0.0.0", 3626))
        self._server_socket.listen(10)

    def main_loop(self):
        """
            main loop of the server
                - connect to new client
                - receive command
                - send data to client
                - close socket

        :return: returns key if one is given by client
        """
        # connect client
        (client_socket, address) = self._server_socket.accept()

        # receive data from client
        data = client_socket.recv(1024)

        # print new connection
        print "connection: " + str(address) + "\n\tdata: " + data

        # handle client by message
        if data == "new":
            # if 'new', send username and token
            client_socket.sendall("token=" + self._token)
        elif data == "next":
            # if 'next', send new block number
            client_socket.sendall(hex(self._block_counter))
            self._block_counter += 1
        elif data[:3] == "key":
            # if key received, close sockets and return key
            self.close_client_socket(client_socket)
            self.close_server_socket()
            return data.split("=", 1)[1]

        self.close_client_socket(client_socket)
        return 0

    def close_server_socket(self):
        """
            close the server socket
        """
        self._server_socket.shutdown(2)
        self._server_socket.close()

    def close_client_socket(self, client_socket):
        """
            close a client socket
        """
        client_socket.shutdown(2)
        client_socket.close()
        print "\tsocket closed"


def main():
    token = sys.argv[1]

    # create master
    master = Master(token)

    while key is None:
        # run master main loop
        try:
            key = master.main_loop()
        except KeyboardInterrupt:
            master.close_server_socket()

    print "key = " + key


if __name__ == '__main__':
    main()
