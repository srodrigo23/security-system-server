"""
Author  : Sergio Rodrigo Cardenas Rivera
Email   : rodrigosergio93@gmail.com
Version : 1.0
GitHub  : @srodrigo23
"""

from twilio.rest import Client
import settings as s

def send_textual_message(message_body:str)->None:
    account_sid = s.get_twilio_account_sid()
    auth_token = s.get_twilio_token()
    client = Client(account_sid, auth_token)
    from_whatsapp_number = f'whatsapp:+{s.get_phone_number_notificator()}'
    to_whatsapp_number = f'whatsapp:+{s.get_phone_number_client()}'
    client.messages.create(
        body=message_body,
        from_=from_whatsapp_number,
        to=to_whatsapp_number
    )

def send_media_message(message_body:str, media_url:str) -> None:
    account_sid = s.get_twilio_account_sid()
    auth_token = s.get_twilio_token()
    client = Client(account_sid, auth_token)
    from_whatsapp_number = f'whatsapp:+{s.get_phone_number_notificator()}'
    to_whatsapp_number = f'whatsapp:+{s.get_phone_number_client()}'
    client.messages.create(
        body=message_body,
        media_url=media_url,
        from_=from_whatsapp_number,
        to=to_whatsapp_number
    )
