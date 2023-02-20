

def send_message_event_camera_connected()->None:

    from .message_templates import new_camera_connected
    from .whatsapp_sender import send_message

    send_message(message_body=new_camera_connected)
    
