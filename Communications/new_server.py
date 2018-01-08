import socket


class Master(object):
    """
        Class contains all variables and function the master uses

        variables:
            token - the token to break
            username - the username in the token
    """

    def __init__(self, token, username):
        self._token = token
        self._username = username
        self._block_counter = 0

        self.init_socket()

    def init_socket(self):
        self._server_socket = socket.socket()

        self._server_socket.bind(("0.0.0.0", 3626))
        self._server_socket.listen(10)

    def main_loop(self):
        (client_socket, address) = self._server_socket.accept()

        data = client_socket.recv(1024)
        print("new connection from " + str(address))
        print "data: " + data

        if data == "new":
            client_socket.sendall("username=" + self._username + "|token=" + self._token)
        elif data == "next":
            client_socket.sendall(hex(self._block_counter))
            self._block_counter += 1
        elif data[:3] == "key":
            client_socket.close()
            self._server_socket.close()
            return data.split("=", 1)[1]

        client_socket.shutdown(2)
        client_socket.close()
        print "socket closed"
        return 0


def main():
    token = "1234"
    username = "Enommer"

    # create master
    master = Master(token, username)

    # init key
    key = 0

    while key == 0:
        # run master main loop
        try:
            key = master.main_loop()
        except KeyboardInterrupt:
            master._server_socket.shutdown(2)
            master._server_socket.close()

    print "key = " + key


if __name__ == '__main__':
    main()
