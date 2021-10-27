from logger   import print_log

import socket

from threading import Thread
import socket as s
import time
import sys

class TCPServer():
    def __init__(self, host, port):
        self.__host__ = host
        self.__port__ = port
        self.__socket__ = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.setup_server()

    def setup_server(self):
        try:
            self.__socket__.bind((self.__host__, self.__port__))
            self.__socket__.listen(10)
        except s.error as e:
            print(str(e))
        else:
            self.__cons__ = []  # to manage conections
            
    def run(self):
        print("Listen connections >")
        while True:
            conn, addr = self.__socket__.accept()
            self.start_new_connection(conn)
            self.__cons.append__((conn, addr))
            self.show_server_info()

    def start_new_connection(self, conn):
        thread = Thread(target=self.run_connection, args=(conn, ))
        thread.setDaemon(True)
        thread.start()

    def run_connection(self, connection):
        connection.send(str.encode('Welcome to the Server'))
        while True:
            data = connection.recv(2048)
            entry = data.decode('utf-8')
            print(entry)
            reply = 'Server says ' + data.decode('utf-8')
            if not data:
                break
            connection.sendall(str.encode(reply))
        connection.close()
    
    def show_server_info(self):
        print(f'Num. conections : { len(self.cons) }')
        for con in self.cons:
            print(f"Connection : {con[1][0]} Address : {con[1][1]}")


def run_tcp_server(host, port):
    TCPServer(host, port).run()

if __name__ == "__main__":
    host = sys.argv[1]
    port = sys.argv[2]
    run_tcp_server(host, int(port))
    # run_tcp_server('127.0.0.1', 6000)
