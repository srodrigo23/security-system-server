
from .whatsapp_sender import send_textual_message, send_media_message

def send_message_event_camera_connection(camera_info:dict, status:bool, link:bool)->None:
    from .message_templates import new_camera_connected, camera_disconnected
    if status:
        textual_message = new_camera_connected(
            cam_id=camera_info['id'],
            time=camera_info['time_connection'],
            date=camera_info['date_connection'],
            link=link
        )
        send_textual_message(
            message_body=textual_message
        )
    else:
        send_textual_message(
            message_body=camera_disconnected(
                cam_id=camera_info['id'],
                time=camera_info['time_connection'],
                date=camera_info['date_connection']
            )
        )

def send_message_event_detection(type_detection:str, media_url:str, cam_id:str)->None:
    from .message_templates import fire_detection
    from .message_templates import motion_detection
    from .message_templates import human_detection

    if type_detection == "fire":
        send_media_message(
            message_body=fire_detection(cam_id=cam_id),
            media_url=media_url
        )
    elif type_detection == "motion":
        send_media_message(
            message_body=motion_detection(cam_id=cam_id),
            media_url=media_url
        )
    else:
        send_media_message(
            message_body=human_detection(cam_id=cam_id),
            media_url=media_url
        )
