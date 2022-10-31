from .mail_sender import send_mail
from .mail_template import get_body_mail_camera_connected

def send_mail_camera_event_connection(camera_info: dict, status: bool, link: str) -> None:
    try:
        send_mail(
            mail_body=get_body_mail_camera_connected(
                camera_data=camera_info,
                status=status,
                link=link,
            )
        )
    except Exception as err:
        print(f'Error sending Mail {err}')