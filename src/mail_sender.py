import smtplib
import ssl

from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

class MailSender:
    
    def __init__(self, port, sender_mail, password):
        self.__port__ = port
        self.__sender_mail__ = sender_mail
        self.__password__ = password
        
        self.__context__ = ssl.create_default_context() 
        self.__smtp_sever__ = "smtp.gmail.com"
        self.__server__ = smtplib.SMTP(self.__smtp_sever__, self.__port__)
    
    def send_email(self, receiver_email, message):
        try:
            self.__server__.ehlo()  # Can be omitted
            self.__server__.starttls()
            self.__server__.ehlo()  # Can be omitted
            self.__server__.login(self.__sender_mail__, self.__password__)
            my_message = self.prepare_message(receiver_email)
            self.__server__.sendmail(self.__sender_mail__, receiver_email, my_message)
        except Exception as e:
            print(e)
        finally:
            self.__server__.quit()
            
    def prepare_message(self, receiver_email):
        
        message = MIMEMultipart("alternative")
        message["Subject"] = "Urgente"
        message["From"] = self.__sender_mail__
        message["To"] = receiver_email
        message["X-Priority"] = '2'
        
        filename = 'chat.txt'
        with open(filename, 'r') as f:
            part = MIMEApplication(f.read(), Name=basename(filename))

        part['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(filename))
        message.attach(part)

        # Create the plain-text and HTML version of your message
        text = """\
        Hi,
        How are you?
        Real Python has many great tutorials:
        www.realpython.com"""
        
        html = """\
        <html>
        <body>
            <p>Hi,<br>
            How are you?<br>
            <a href="http://www.realpython.com">Real Python</a> 
            has many great tutorials.
            </p>
        </body>
        </html>
        """
        
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        
        message.attach(part1)
        message.attach(part2)
        return message.as_string()    
    
    
port = 587
sender_mail = "rodrigosergio93@gmail.com"
password = "nemesis@666"

receiver_email = "rodrigosergio93@gmail.com"
message = """
Subject : Hi there

This message is sent from Python sexo anal
"""

mail_sender = MailSender(port, sender_mail, password)
mail_sender.send_email(receiver_email, message)
