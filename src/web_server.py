from flask import Flask, send_from_directory
import sys

__server__ = Flask(__name__)

@__server__.route('/')
def main():
    return ("Hello from flask")

@__server__.route('/stream/<path:numstream>/<path:filename>')
def assets(code_stream, filename):
	return send_from_directory(f'../stream/live_{code_stream}', filename)

def run_web_server(host, port):
    __server__.run(host=host, port=port, debug=True)
    
if __name__ == "__main__":
    host = sys.argv[1]
    port = sys.argv[2]
    run_web_server(host, port)
