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

def get_twilio_account_sid():
    return parser.get('twilio', 'account_sid')

def get_twilio_token():
    return parser.get('twilio', 'auth_token')

def get_phone_number_notificator():
    return parser.get('twilio', 'phone_number_notificator')

def get_phone_number_client():
    return parser.get('twilio', 'phone_number_client')

def get_imagekit_private_key():
    return parser.get('imagekit', 'private_key')

def get_imagekit_public_key():
    return parser.get('imagekit', 'public_key')

def get_imagekit_url_endpoint():
    return parser.get('imagekit', 'url_endpoint')

def set_stream_enabled(enabled:str) -> None:
    parser.set('stream', 'enabled', enabled)
    with open(r"../config.ini", 'w') as configfile:
        parser.write(configfile)
    # return parser.getboolean('stream', 'enabled')

def set_fire_detector_status(enabled:str) -> None:
    parser.set('detectors', 'fire', enabled)
    with open(r"../config.ini", 'w') as configfile:
        parser.write(configfile)
    # return parser.getboolean('detectors', 'fire')

def set_motion_detector_status(enabled:str )-> None:
    parser.set('detectors', 'motion', enabled)
    with open(r"../config.ini", 'w') as configfile:
        parser.write(configfile)
    # return parser.getboolean('detectors', 'motion')

def set_people_detector_status(enabled:str) -> None:
    parser.set('detectors', 'people', enabled)
    with open(r"../config.ini", 'w') as configfile:
        parser.write(configfile)
    # return parser.getboolean('detectors', 'people')