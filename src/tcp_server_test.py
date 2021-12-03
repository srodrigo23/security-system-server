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
# my_server = socketserver.ThreadingTCPServer(('127.0.0.1', 8881), MyHandler)
# my_server.serve_forever()

def run_connection(self, ident, connection, addr):
        """
        Method to get frames every thread connection
        """
        print_log('i', f"New connection ready to receive frames {addr}")
        data = b""
        payload_size = struct.calcsize(">L") # print("payload_size: {}".format(payload_size))
        while True:
            cabecera = 0
            while len(data) < payload_size:
                cabecera+=1
                data_received = connection.recv(4096) # critico
                if data_received == b"":
                    print('Operacion terminada')
                    break
                else:
                    data+=data_received
                    print(f'Recibiendo cabecera {cabecera} {ident}')
            #receive image row data from client socket
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            try:
                msg_size = struct.unpack(">L", packed_msg_size)[0]
            except struct.error as e:
                print(str(e))
                break
            while len(data) < msg_size:
                data_received = connection.recv(4096)
                if data_received == b"":
                    print('Operacion termanada')
                    break
                else:
                    data += data_received
            frame_data = data[:msg_size]
            data = data[msg_size:]     
            frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)  # Frame received
            # print(str(frame))
            time.sleep(0.1)
        connection.close()
    
    def show_server_info(self):
        """
        Method to show server info
        """
        print_log('i', f'Num. conections : { len(self.cons) }')
        for conn in self.cons:
            print_log('i', f"Connection : {conn[1][0]} Address : {conn[1][1]}")