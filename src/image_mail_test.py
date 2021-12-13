from os import listdir
from os.path import isfile, join
import cgi
import uuid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
import os
import html
import smtplib
from email.mime.base import MIMEBase
from email import encoders
import numpy as np

gmail_user = "rodrigosergio93@gmail.com"
gmail_pwd = "nemesis@666"
final_path_current = "/Users/sergiorodrigo/Documents/tesis/code/tcpserver/src/img"
receive_mail = "rodrigosergio93@gmail.com"

def attach_image(img_dict):
    with open(img_dict['path'], 'rb') as file:
        msg_image = MIMEImage(file.read(), name=os.path.basename(img_dict['path']))
    msg_image.add_header('Content-ID', '<{}>'.format(img_dict['cid']))
    return msg_image


def attach_file(filename):
    part = MIMEBase('application', 'octect-stream')
    part.set_payload(open(filename, 'rb').read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename=%s' % os.path.basename(filename))
    return part


def generate_email(gmail_user, to_list, img_dict):
    msg = MIMEMultipart('related')
    msg['Subject'] = Header(u'Subject', 'utf-8')
    msg['From'] = gmail_user
    msg['To'] = ','.join(to_list)
    msg_alternative = MIMEMultipart('alternative')
    msg_text = MIMEText(u'Image not working', 'plain', 'utf-8')
    msg_alternative.attach(msg_text)
    msg.attach(msg_alternative)
    msg_html = u'<h1>Below are the images</h1>'
    for img in img_dict:
        msg_html += u'<h3>'+img["title"][:-4]+'</h3><div dir="ltr">''<img src="cid:{cid}" alt="{alt}"><br></div>'.format(
            alt=html.escape(img['title'], quote=True), **img)
    msg_html = MIMEText(msg_html, 'html', 'utf-8')
    msg_alternative.attach(msg_html)
    for img in img_dict:
        msg.attach(attach_image(img))

    return msg


def send_email(msg, gmail_user, gmail_pwd, to_list):
    mailServer = smtplib.SMTP('smtp.gmail.com', 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pwd)
    mailServer.sendmail(gmail_user, to_list, msg.as_string())
    mailServer.quit()


img_dict = []
all_files = [f for f in listdir(final_path_current) if isfile(join(final_path_current, f))]

for file in all_files:
    img_dict_single = dict(title=file, path=final_path_current+"/"+file, cid=str(uuid.uuid4()))
    img_dict.append(img_dict_single)

email_msg = generate_email(gmail_user, [receive_mail], img_dict=img_dict)
send_email(email_msg, gmail_user, gmail_pwd, [receive_mail])