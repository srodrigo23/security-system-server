"""
Author  : Sergio Rodrigo Cardenas Rivera
Email   : rodrigosergio93@gmail.com
Version : 1.0
GitHub  : @srodrigo23
"""

from tcp_server import TCPServer
import sys

if __name__ == "__main__":
    tcp_server = TCPServer(server_mode=sys.argv[1] if len(sys.argv)>1 else None)
    tcp_server.prepare_server()
    tcp_server.run()
