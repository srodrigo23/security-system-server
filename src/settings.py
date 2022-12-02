"""
Methods to get config values
"""
from configparser import ConfigParser

parser = ConfigParser()
parser.read('../config.ini')

def get_host():
    return parser.get('server', 'host')

def get_port():
    return parser.get('server', 'port')

def get_media_folder_name():
    return parser.get('media', 'folder_name')

def get_stream_folder_name():
    return parser.get('stream', 'folder_name')

def get_captures_folder_name():
    return parser.get('captures', 'folder_name')

def get_database_file_name():
    return parser.get('database', 'db_file_name')

def get_index_stream_file_name():
    return parser.get('stream', 'index')

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

def get_stream_enabled():
    return parser.getboolean('stream', 'enabled')

def get_fire_detector_status():
    return parser.getboolean('detectors', 'fire')

def get_motion_detector_status():
    return parser.getboolean('detectors', 'motion')

def get_people_detector_status():
    return parser.getboolean('detectors', 'people')
