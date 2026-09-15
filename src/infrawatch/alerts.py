import logging
from pathlib import Path
import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

from .config import load_config

load_dotenv()
last_status = "HEALTHY"

def send_alert(message):
    log_dir = Path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger("infrawatch")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        config = load_config()
        log_file = config["alerts"]["log_file"]

        file_handler =logging.FileHandler(log_file)

        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
        
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.critical(message)

def send_email(message):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    sender_email = os.getenv("SMTP_EMAIL")
    smtp_password = os.getenv("SMTP_PASSWORD")

    recipient_email = sender_email

    email = EmailMessage()

    email["Subject"] = "InfraWatch CRITICAL Alert"
    email["From"] = sender_email
    email["To"] = recipient_email

    email.set_content(message)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, smtp_password)
        server.send_message(email)

def handle_alert(status, message):
    global last_status

    if status == "CRITICAL" and last_status != "CRITICAL":
        send_alert(message)
        send_email(message)

    elif status == "HEALTHY" and last_status == "CRITICAL":
        recovery_message = "InfraWatch: System has recovered and is HEALTHY."
        send_alert(recovery_message)
        send_email(recovery_message)

    last_status = status
