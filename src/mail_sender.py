from os.path import basename
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase

from _thread import start_new_thread

from settings import get_email_port
from settings import get_smtp_server
from settings import get_sender_mail
from settings import get_pass_sender
from settings import get_receiver_mail

import smtplib
import ssl

class MailSender:
    
    def __init__(self):
        """
        Method to initialize mail sender
        """
        self.__port__ = int(get_email_port())
        self.__sender_mail__ = get_sender_mail()
        self.__password__ = get_pass_sender()
        self.__receiver_mail__ = get_receiver_mail()
        self.__smtp_sever__ = get_smtp_server()
        self.__server__ = smtplib.SMTP(self.__smtp_sever__, self.__port__)
    
    def prepare_server(self):
        """
        Method to prepare smtp server to send mails
        """
        try:
            self.__server__.ehlo()  # Can be omitted
            self.__server__.starttls()
            self.__server__.ehlo()  # Can be omitted
            self.__server__.login(self.__sender_mail__, self.__password__)
        except Exception as e:
            print(e)
        # finally:
            # self.__server__.quit()
    
    def prepare_mail(self, message, attachments, hls_stream_link):
        """
        Method to prepare a mail in a thread
        message = "Se ha identificado la presencia de un(os) intruso(s)."
        """
        my_message = MIMEMultipart("related")
        my_message["Subject"] = "Urgente"
        my_message["From"] = self.__sender_mail__
        my_message["To"] = self.__receiver_mail__
        my_message["X-Priority"] = '1'
        
        html = f"""
            <html>
                <body>
                    <div style="background-color:#7BB1FF;">
                        <p>
                            Hi,<br>
                            How are you?<br>
                            <a href="http://www.realpython.com">Real Python</a> has many great tutorials.
                        </p>
                        <p>
                            El enlace para ver lo que esta pasando en vivo es <a href="{hls_stream_link}">este.</a>
                        <p/>
                    </div>
                </body>
            </html>"""
        
        message_html = MIMEText(html, "html")
        my_message.attach(message_html)
        if(len(attachments) > 0):
            with open(attachments[0], 'rb') as file:
                msg_image = MIMEImage(file.read(), name=basename(attachments[0]))
            # msg_image.add_header('Content-ID', '<{}>'.format(0))
            my_message.attach(msg_image)
            
            with open(attachments[1], 'rb') as file:
                msg_image = MIMEImage(file.read(), name=basename(attachments[1]))
            # msg_image.add_header('Content-ID', '<{}>'.format(1))
            my_message.attach(msg_image)
            
            with open(attachments[2], 'rb') as file:
                msg_image = MIMEImage(file.read(), name=basename(attachments[2]))
            # msg_image.add_header('Content-ID', '<{}>'.format(2))
            my_message.attach(msg_image)
        
        
        # if len(attachments)>0:
        #     for attachment in attachments: #attachging files in a email
                
                # file = open(attachment, 'rb')
                # part = MIMEImage(file.read(), name=basename(attachment))        
                # part['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(attachment))
                    # my_message.attach(msg_image)
                # with open(attachment, 'rb') as f:
                #     mime = MIMEBase('image', 'jpg', filename=basename(attachment))
                #     # add required header data:
                #     mime.add_header('Content-Disposition', 'attachment', filename=basename(attachment))
                #     mime.add_header('X-Attachment-Id', '0')
                #     mime.add_header('Content-ID', '<0>')
                #     # read attachment file content into the MIMEBase object
                #     mime.set_payload(f.read())
                #     # encode with base64
                #     # encoders.encode_base64(mime)
                #     # add MIMEBase object to MIMEMultipart object
                #     my_message.attach(mime)

        
        # start_new_thread(self.send_mail, (my_message.as_string(),))
        self.send_mail(my_message.as_string())  
        
    def send_mail(self, message):
        try:
            self.__server__.sendmail(self.__sender_mail__, self.__receiver_mail__, message)
        except Exception as e:
            print(e)
        finally:
            self.__server__.quit()

        
message = "Se ha identificado la presencia de un(os) intruso(s)."
# attach = ['./img/pic1.jpg', './img/pic2.jpg', './img/pic4.jpeg']
attach = []
hls_link = "http://google.com.bo"

mail_sender = MailSender()
mail_sender.prepare_server()
mail_sender.prepare_mail(message, attach, hls_link)