from tcp_server import TCPServer
from flask import Flask, send_from_directory

import settings as s

app = Flask("app")

@app.route('/')
def main():
    return("Web Server")

@app.route('/stream/<path:code_stream>/<path:filename>')
def streamming(code_stream, filename):
    """ """
    path = os.path.join(s.get_path_folder_streaming(), code_stream)
    return send_from_directory(path, filename)

def run_web_server(host, port):
    """ Method to run a web server """
    app.run(host=host, port=port``)

def run_tcp_server(host, port):
    """ Method to run a tcp server """
    tcp_server = TCPServer(host, port)
    tcp_server.prepare_server()
    tcp_server.start()

if __name__ == "__main__":
    run_tcp_server(s.get_host(), int(s.get_port()))
    run_web_server(s.get_host(), int(s.get_port_web()))