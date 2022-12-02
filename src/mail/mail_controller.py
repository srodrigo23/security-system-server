"""
Methods to send notification mail
"""
from threading import Thread
from .mail_sender import send_mail
from .mail_template import get_body_mail_camera_connected
from .mail_template import get_body_mail_event_happen

def send_mail_camera_event_connection(
    camera_info: dict,
    status: bool,
    link: str,
    other_cams: list) -> None:
    """
    Method to send connetion cam event
    """
    try:
        send_mail(
            mail_body=get_body_mail_camera_connected(
                camera_data=camera_info,
                status=status,
                link=link,
                other_cams=other_cams,
            )
        )
    except Exception as err:
        print(f'Error sending Connection/Disconnection Mail {err}')


def send_sending_mail_with_thread(self) -> None:
    """
    Start thread to send event mail.
    """
    thread = Thread(
        target=self.send_mail_notification_connection,
        args=(
            self.cam_id,
            self.running,
            f"{self.stream_link if self.stream_enabled else ''}"))
    thread.start()

def send_mail_camera_event_detection(
    detection_code: str,
    detection_info: dict,
    attachments: list) -> None:
    """
    Method to notify about a detection
    """
    try:
        send_mail(
            mail_body=get_body_mail_event_happen(
                detection_code=detection_code,
                detection_info=detection_info,
                num_pics_ad=len(attachments)
            ),
            attachments=attachments
        )
    except Exception as err:
        print(f'Error sending Event detected Mail {err}')
        