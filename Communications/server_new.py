import socket
import select


class Master(object):
    """
        Master class -
            holds the information of a master

            variables:
                token - token
                username - username
                block counter - block counter
                slave list - slave_list
                server socket - socket
    """

    def __init__(self, token, username):
        """
            initialize variables
        :param token: token to crack
        :param username: username inside token
        """
        self._block_counter = 0
        self._token = token
        self._username = username
        self._slave_list = []

        self.init_server()

    def init_server(self):
        """
            initialize server
        """
        # make socket
        self._socket = socket.socket()

        # bind to socket
        self._socket.bind(("0.0.0.0", 3626))

        # listen for connections
        self._socket.listen(5)

    def add_slave(self, slave):
        """
            Add slave to slave list.
        :param slave: the slave to add
        """
        self._slave_list.append(slave)

    def remove_slave(self, slave):
        """
            Remove slave from slave list
        :param slave: slave to remove
        """
        self._slave_list.remove(slave)

    def main_loop(self):
        rlist, wlist, xlist = select.select([self._socket] + self._slave_list, self._slave_list, [])

        for curr_socket in rlist:
            if curr_socket is self._socket:
                (slave_socket, address) = self._socket.accept()

                print "New connection with - " + str(address)

                slave_socket.sendall("token=" + self._token)
                slave_socket.sendall("username=" + self._username)

                self._slave_list.append(slave_socket)

            else:
                data = curr_socket.recv(1024)
                if data == "":
                    self._slave_list.remove(curr_socket)
                    print "Connection closed with - " + str(curr_socket.getsockname())

                elif data == "next":
                    curr_socket.sendall("process_block=" + hex(self._block_counter))
                    self._block_counter += 1

                elif data[:4] == "done":
                    self._socket.close()
                    return data.split("=", 1)[1]

        return 0
#
#
# class Slave(object):
#     """
#         Slave class -
#             holds the information of a slave
#
#             variables:
#                 connection
#                 address
#                 TODO: block list
#     """
#
#     def __init__(self, connection, address):
#         """
#             initialize variables
#         :param connection: socket for connection
#         :param address: address of slave
#         """
#         self._connection = connection
#         self._address = address


def main():
    # set token and username
    token = "1234"
    username = "enommer"

    # create master
    master = Master(token, username)
    key = 0

    while not key:
        key = master.main_loop()

    print "key=" + key


if __name__ == '__main__':
    main()






    """
        check for new connections 
    
        
        handle new slaves
        
        wait for data
            1) SLV disconnects
                ?1.1?) if SLV did not finish block send to someone else
            2) recv 'next'
                2.1) give new block number
            3) recv 'done'
                3.1) close all connections
                3.2) close all sockets
                
    """



