import socket
import select


def main():
    block_counter = 0
    token = "123456"
    username = "enommer"
    server_socket = socket.socket()
    server_socket.bind(("0.0.0.0", 3626))
    server_socket.listen(5)

    open_client_sockets = []

    while True:
        rlist, wlist, xlist = select.select([server_socket] + open_client_sockets, [], [])

        for current_socket in rlist:
                # new client
                if current_socket is server_socket:
                    (new_socket, address) = server_socket.accept()
                    open_client_sockets.append(new_socket)
                    print "Connection opened with client: " + str(address)
                    new_socket.sendall("token=" + token)
                    new_socket.sendall("username=" + username)

                else:
                    data = current_socket.recv(1024)

                    # client disconnects
                    if data == "":
                        open_client_sockets.remove(current_socket)
                        print "Connection closed with client: " + str(current_socket.getsockname())

                    # client sends data
                    else:
                        print "data received from client: " + str(current_socket.getsockname()) + " Data=" + data

                        if data == "next":
                            new_socket.sendall("process_block=" + hex(block_counter))
                            block_counter += 1
                        if data[:4] == "done":
                            print "KEY = " + data.split("=", 1)[1]
                            server_socket.close()
                            exit(0)
        print "pass"


if __name__ == '__main__':
    main()
