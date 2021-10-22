import socketserver

# https://www.oreilly.com/library/view/python-cookbook/0596001673/ch10s03.html

class MyHandler(socketserver.BaseRequestHandler):
    
    def handle(self):
        while True:
            data_received = self.request.recv(1024)
            
            self.request.send(data_received)
            # print(data_received)
            if not data_received: 
                break
            self.request.send(data_received)

# my_server = socketserver.TCPServer(('', 8881), MyHandler)
my_server = socketserver.ThreadingTCPServer(('127.0.0.1', 8881), MyHandler)
my_server.serve_forever()
