
from .mail_controller import send_mail_camera_event_connection
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

send_mail_camera_event_connection(
    camera_info=camera_info,
    status=status, 
    link=link, 
    other_cams=other_cams)