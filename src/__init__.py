from tcp_server import TCPServer

import settings as s

def run_tcp_server(host, port):
    """
    Method to run a tcp server
    """
    tcp_server = TCPServer(host, port)
    tcp_server.run()

if __name__ == "__main__":
    """
    Main block code
    """
    run_tcp_server(s.get_host(), int(s.get_port()))