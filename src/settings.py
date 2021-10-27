from configparser import ConfigParser

parser = ConfigParser()
parser.read('../config.ini')

def get_host_web_server():
    return parser.get('web_server', 'host')

def get_port_web_server():
    return parser.get('web_server', 'port')

def get_host_tcp_server():
    return parser.get('tcp_server', 'host')

def get_port_tcp_server():
    return int(parser.get('tcp_server', 'port'))