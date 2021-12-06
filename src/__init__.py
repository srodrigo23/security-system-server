from tcp_server import TCPServer
from util.logger import print_log
from database.firebase_manager import FirebaseManager
from util.date import get_current_time_string

import settings as s

def run_tcp_server(host, port):
    """
    Method to run a tcp server
    """
    tcp_server = TCPServer(host, port)
    print_log('i', "Welcome to the TCP-Server")
    tcp_server.run()

if __name__ == "__main__":
    """
    Main block code
    """
    run_tcp_server(s.get_host(), int(s.get_port()))