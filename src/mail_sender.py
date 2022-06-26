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
                    <div style='background-color:#FCF3CF; 
                                font-family: "Lucida Console", "Courier New", monospace;'>
                        <p style='font-weight: bold; font-size: large; text-align: center;'>
                            SISTEMA DE VIDEO VIGILANCIA INTELIGENTE "LIVE EYE SMART"
                        </p>
                        <p>{ message }</p>
                        <p>
                            <table border='1' align='center'>
                                <tr>
                                    <th>Hoy</th>
                                    <th>Mañana</th>
                                    <th>Domingo</th>
                                </tr>
                                <tr>
                                    <td>Soleado</td>
                                    <td>Mayormente soleado</td>
                                    <td>Parcialmente nublado</td>
                                </tr>
                                <tr>
                                    <td>19°C</td>
                                    <td>17°C</td>
                                    <td>12°C</td>
                                </tr>
                                <tr>
                                    <td>E 13 km/h</td>
                                    <td>E 11 km/h</td>
                                    <td>S 16 km/h</td>
                                </tr>
                            </table>
                        </p>

                        <p>
                            <table border='1' align='center'>
                                <tr>
                                    <th>Hoy</th>
                                    <th>Mañana</th>
                                    <th>Domingo</th>
                                </tr>
                                <tr>
                                    <td>Soleado</td>
                                    <td>Mayormente soleado</td>
                                    <td>Parcialmente nublado</td>
                                </tr>
                                <tr>
                                    <td>19°C</td>
                                    <td>17°C</td>
                                    <td>12°C</td>
                                </tr>
                                <tr>
                                    <td>E 13 km/h</td>
                                    <td>E 11 km/h</td>
                                    <td>S 16 km/h</td>
                                </tr>
                            </table>
                        </p>
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
                mail.attach(msg_image)
        return mail
        
    def send_mail(self, message):
        try:
            self.server.sendmail(sender_mail, receiver_mail, message)
        except Exception as e:
            print(e)
        finally:
            self.server.quit()
    
