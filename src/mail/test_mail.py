
from .mail_controller import send_mail_camera_event_connection
from .mail_controller import send_mail_camera_event_detection

from util.date import get_current_time_string, get_current_raw_time, get_date, get_time

camera_info = {
    'id': '5540408015',
    'time_connection': get_time(),
    'date_connection': get_date()
}
status = False
link = "http://www.google.com"

other_cams=[
    {
        'id': '5540408015',
        'time_connection': get_time(),
        'date_connection': get_date(),
        'link' : 'https://www.google.com'
    },
    {
        'id': '5540408015',
        'time_connection': get_time(),
        'date_connection': get_date(),
        'link': 'https://www.google.com'
    },
    {
        'id': '5540408015',
        'time_connection': get_time(),
        'date_connection': get_date(),
        'link': 'https://www.google.com',
    }
]

# send_mail_camera_event_connection(
#     camera_info=camera_info,
#     status=status, 
#     link=link, 
#     other_cams=other_cams)

"""
detection codes :
fire
movement
human_siluhete
smoke
"""
detection_code = 'smoke'
detection_info = {
    'id': '5540408015',
    'time_detection': get_time(),
    'date_detection': get_date(),
    'link': 'https://www.google.com'
}
files = [
    'mail/img/fire.png',
    'mail/img/human.png',
    'mail/img/movement.png',
    'mail/img/smoke.png',
]
num_pics_ad = 4
send_mail_camera_event_detection(
    detection_code=detection_code, 
    detection_info=detection_info, 
    attachments=files
)