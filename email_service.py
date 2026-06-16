import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

class EmailService:
    def __init__(self):
        self.smtp_host = "smtp.gmail.com"
        self.smtp_port = 465
        self.email_address = os.getenv("EMAIL_ADDRESS")
        self.email_password = os.getenv("EMAIL_PASSWORD")

    def send_email(self, recipient: str, subject: str, body: str):
        """
        Sends an email via Gmail SMTP SSL.
        """
        if not self.email_address or not self.email_password:
            raise Exception("Email credentials not configured in .env")

        msg = MIMEMultipart()
        msg['From'] = self.email_address
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port) as server:
                server.login(self.email_address, self.email_password)
                server.send_message(msg)
        except Exception as e:
            raise Exception(f"Gmail SMTP Error: {str(e)}")
