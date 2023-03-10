from .whatsapp_sender import send_textual_message

def send_message_event_camera_connection(camera_info:dict, status:bool, link:None)->None:
    from .message_templates import new_camera_connected, camera_disconnected
    if status:
        send_textual_message(
            message_body=new_camera_connected(
                cam_id=camera_info['id'],
                time=camera_info['time_connection'],
                date=camera_info['date_connection'],
                link=link)
            )
    else:
        send_textual_message(
            message_body=camera_disconnected(
                cam_id=camera_info['id'],
                time=camera_info['time_connection'],
                date=camera_info['date_connection']
            )
        )
