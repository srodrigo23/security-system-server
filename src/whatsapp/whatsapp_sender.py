import settings as s
from twilio.rest import Client

def send_textual_message(message_body:str)->None:

    account_sid = s.get_twilio_account_sid()
    auth_token = s.get_twilio_token()
    client = Client(account_sid, auth_token)

    from_whatsapp_number = f'whatsapp:+{s.get_phone_number_notificator()}'
    to_whatsapp_number = f'whatsapp:+{s.get_phone_number_client()}'

    message = client.messages.create(
        body=message_body,
        # media_url='https://raw.githubusercontent.com/dianephan/flask_upload_photos/main/UPLOADS/DRAW_THE_OWL_MEME.png',
        # media_url='https://ik.imagekit.io/srodrigo23/test/241188806_1013240782576434_1846265590439094677_n.jpg?ik-sdk-version=javascript-1.4.3&updatedAt=1676909762705',
        # media_url='https://drive.google.com/file/d/1kLSdvKFK2ePVUiYH2iXtsTG6FnNhBH0e/view?usp=sharing', drive don't works
        # media_url=media_url,
        from_=from_whatsapp_number,
        to=to_whatsapp_number
    )
    # print(message.sid)

def send_media_message(message_body:str, media_url:str) -> None:
    account_sid = s.get_twilio_account_sid()
    auth_token = s.get_twilio_token()
    client = Client(account_sid, auth_token)

    from_whatsapp_number = f'whatsapp:+{s.get_phone_number_notificator()}'
    to_whatsapp_number = f'whatsapp:+{s.get_phone_number_client()}'

    message = client.messages.create(
        body=message_body,
        media_url=media_url,
        from_=from_whatsapp_number,
        to=to_whatsapp_number
    )
    # print(message.sid)./