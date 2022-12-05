from tcp_server import TCPServer
# from mail import test_mail

if __name__ == "__main__":
    tcp_server = TCPServer()
    tcp_server.prepare_server()
    tcp_server.run()
    