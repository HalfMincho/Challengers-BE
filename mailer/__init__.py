from typing import Union
from smtplib import SMTP, SMTP_SSL
from config import mailer as config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_one(rcpt_addr: str, rcpt_name: Union[str, None], mail_title: str, mail_body: str, sub_type="plain") -> bool:
    try:
        if config.encryption == 'ssl':
            smtp = SMTP_SSL(host=config.host, port=config.port, timeout=3)
        else:
            smtp = SMTP(host=config.host, port=config.port, timeout=3)

        if config.encryption == 'tls':
            smtp.starttls()

        smtp.login(user=config.username, password=config.password)

        message = MIMEMultipart()

        message['Subject'] = mail_title
        message['From'] = f'GISTORY.me admin<{config.username}>'
        message['To'] = f'{rcpt_name}<{rcpt_addr}>'

        message.attach(MIMEText(_text=mail_body, _charset='utf-8', _subtype=sub_type))

        smtp.sendmail(config.username, rcpt_addr, message.as_string())

        smtp.close()
    except:
        return False
    else:
        return True
