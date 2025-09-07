from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import ssl
from app.settings import Settings
from worker.celery import send_email_task


class MailClient:

    @staticmethod
    def send_welcome_email(to: str) -> None:
        return send_email_task.delay(f"welcome email", f"Welcome to pomodoro", to)
        
 