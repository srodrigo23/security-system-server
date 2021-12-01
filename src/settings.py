from configparser import ConfigParser

parser = ConfigParser()
parser.read('../config.ini')

def get_host():
    return parser.get('server', 'host')

def get_port():
    return parser.get('server', 'port')

def get_path_folder_streaming():
    return parser.get('streaming', 'path_folder')