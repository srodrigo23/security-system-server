from os.path import basename
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from _thread import start_new_thread
from settings import get_email_port, get_smtp_server, get_sender_mail, get_pass_sender, get_receiver_mail

import smtplib
import ssl

subject = "Live Eye Smart Report"
port = int(get_email_port())
smtp_server = get_smtp_server()
sender_mail = get_sender_mail()
password = get_pass_sender()
receiver_mail = get_receiver_mail()

def send_mail(message, attach, hls_link):
    mail_sender = MailSender()
    mail_sender.prepare_server()
    mail = mail_sender.prepare_mail(message, attach, hls_link)
    mail_sender.send_mail(mail.as_string())

class MailSender:

    def __init__(self): 
        self.server = smtplib.SMTP(smtp_server, port)
    
    def prepare_server(self):
        """ Method to prepare smtp server to send mails """
        try:
            self.server.ehlo()  # Can be omitted
            self.server.starttls()
            self.server.ehlo()  # Can be omitted
            self.server.login(sender_mail, password)
        except Exception as e:
            print(e)
    
    def prepare_mail(self, message, attachments, hls_stream_link):
        """ Method to prepare a mail in a thread """
        mail = MIMEMultipart("related")

        mail["Subject"] = subject
        mail["From"] = sender_mail
        mail["To"] = receiver_mail
        mail["X-Priority"] = '1'
        
        body = f"""
            <html>
                <body>
                    <div style='background-color:#7BB1FF;'>
                        <p>
                            Hi,<br>
                            How are you?<br>
                            <a href='http://www.realpython.com'>Real Python</a> has many great tutorials.
                        </p>
                        <p>{ message }</p>
                        <p>
                            Puedes ver <a href='{hls_stream_link}'>aqui</a> la transmision en vivo.
                        <p/>
                    </div>
                </body>
            </html>"""
        
        body_mail = MIMEText(body, "html")
        mail.attach(body_mail)

        if(len(attachments) > 0):
            for attach in attachments:
                with open(attach, 'rb') as file:
                    msg_image = MIMEImage(file.read(), name=basename(attach))
                # msg_image.add_header('Content-ID', '<{}>'.format(0))
                mail.attach(msg_image)
        return mail
        
    def send_mail(self, message):
        try:
            self.server.sendmail(sender_mail, receiver_mail, message)
        except Exception as e:
            print(e)
        finally:
            self.server.quit()

send_mail('este es un mensaje', [], 'www.google.com')
send_mail('este es otro mensaje', [], 'www.google.com')