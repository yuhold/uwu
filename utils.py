import logging
import smtplib
from email.mime.text import MIMEText
import configparser

def load_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    return config

def send_email(config, message):
    if not config.getboolean('EMAIL', 'enabled'):
        logging.info("Email notification is disabled.")
        return
    
    sender = config.get('EMAIL', 'sender')
    password = config.get('EMAIL', 'password')
    receiver = config.get('EMAIL', 'receiver')
    smtp_server = config.get('EMAIL', 'smtp_server')
    smtp_port = config.getint('EMAIL', 'smtp_port')

    try:
        smtp_server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        smtp_server.login(sender, password)
        msg = MIMEText(message)
        msg['Subject'] = 'Runyun Website Down'
        msg['From'] = sender
        msg['To'] = receiver
        smtp_server.send_message(msg)
        smtp_server.quit()
        logging.info("Email notification sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
