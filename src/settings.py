from configparser import ConfigParser

parser = ConfigParser()
parser.read('../config.ini')

def get_host():
    return parser.get('server', 'host')

def get_port():
    return parser.get('server', 'port')

def get_path_folder_streaming():
    return parser.get('streaming', 'path_folder')

def get_email_port():
    return parser.get('email', 'port')

def get_smtp_server():
    return parser.get('email', 'smtp_server')

def get_sender_mail():
    return parser.get('email', 'sender_mail')

def get_pass_sender():
    return parser.get('email', 'pass_sender')

def get_receiver_mail():
    return parser.get('email', 'receiver_mail')

def get_path_captures():
    return parser.get('captures', 'path_captures')