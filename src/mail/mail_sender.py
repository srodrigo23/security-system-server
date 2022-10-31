from os.path import basename
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase

import settings as s
import smtplib
import ssl

subject   = "Live Eye Smart Report"
port      = int(s.get_email_port())
smtp_server   = s.get_smtp_server()
sender_mail   = s.get_sender_mail()
password      = s.get_pass_sender()
receiver_mail = s.get_receiver_mail()

def send_mail(mail_body : str):
    mail_sender = MailSender()
    mail_sender.prepare_server()
    mail = mail_sender.prepare_mail(mail_body=mail_body)
    mail_sender.send_mail(mail.as_string())
    
class MailSender:
    
    def __init__(self) -> None: 
        self.server = smtplib.SMTP(smtp_server, port)
    
    def prepare_server(self) -> None:
        """ Method to prepare smtp server to send mails """
        try:
            self.server.ehlo()  # Can be omitted
            self.server.starttls()
            self.server.ehlo()  # Can be omitted
            self.server.login(sender_mail, password)
        except Exception as e:
            print(e)
    
    def prepare_mail(self, mail_body:str) -> None :
        """
        Method to prepare a mail in a thread.
        """
        mail = MIMEMultipart("related")
        mail["Subject"] = subject
        mail["From"]    = sender_mail
        mail["To"]      = receiver_mail
        mail["X-Priority"] = '1'
         
        body_mail = MIMEText(mail_body, "html")
        mail.attach(body_mail)

        # if (attachments is not None) and (len(attachments) > 0) :
        #     for attach in attachments:
        #         with open(attach, 'rb') as file:
        #             msg_image = MIMEImage(file.read(), name=basename(attach))
        #         mail.attach(msg_image)
        return mail
        
    def send_mail(self, message) -> None:
        try:
            self.server.sendmail(sender_mail, receiver_mail, message)
        except Exception as e:
            print(e)
        finally:
            self.server.quit()