"""
Author  : Sergio Rodrigo Cardenas Rivera
Email   : rodrigosergio93@gmail.com
Version : 1.0
GitHub  : @srodrigo23
"""

from os.path import basename
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import smtplib
import settings as s

SUBJECT       = "Live Eye Smart Report"
PORT          = int(s.get_email_port())
smtp_server   = s.get_smtp_server()
sender_mail   = s.get_sender_mail()
password      = s.get_pass_sender()
receiver_mail = s.get_receiver_mail()

def send_mail(mail_body : str, attachments=None) -> None:
    """
    sumary_line
    """
    mail_sender = MailSender()
    mail_sender.prepare_server()
    mail = mail_sender.prepare_mail(
        mail_body=mail_body,
        attachments=attachments
    )
    mail_sender.send_mail(mail.as_string())

class MailSender:
    """
    sumary_line
    """
    def __init__(self) -> None:
        self.server = smtplib.SMTP(smtp_server, PORT)
    
    def prepare_server(self) -> None:
        """
        Method to prepare smtp server to send mails
        """
        try:
            self.server.ehlo()  # Can be omitted
            self.server.starttls()
            self.server.ehlo()  # Can be omitted
            self.server.login(sender_mail, password)
        except Exception as error:
            print(error)
    
    def prepare_mail(self, mail_body: str, attachments=None) -> MIMEMultipart:
        """
        Method to prepare a mail in a thread.
        """
        mail = MIMEMultipart("related")
        mail["Subject"] = SUBJECT
        mail["From"]    = sender_mail
        mail["To"]      = receiver_mail
        mail["X-Priority"] = '1'
        body_mail = MIMEText(mail_body, "html")
        mail.attach(body_mail)

        if attachments is not None:
            for attach in attachments:
                with open(attach, 'rb') as file:
                    msg_image = MIMEImage(
                        file.read(),
                        name=basename(attach)
                    )
                mail.attach(msg_image)
        return mail
        
    def send_mail(self, message) -> None:
        """
        sumary_line
        """
        try:
            self.server.sendmail(
                sender_mail,
                receiver_mail,
                message
            )
        except Exception as error:
            print("Error sending mail...", error)
        finally:
            self.server.quit()
            