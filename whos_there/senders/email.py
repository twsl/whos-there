import smtplib
from email.message import EmailMessage
from typing import List

from whos_there.senders.base import Sender


class EmailSender(Sender):
    def __init__(self, host: str, port: int, sender_email: str, password: str, recipient_emails: List[str]) -> None:
        super().__init__()
        self.sender_email = sender_email
        self.recipient_emails = recipient_emails
        self.server = smtplib.SMTP(host, port)
        self.server.starttls()
        self.server.login(sender_email, password)

    def send(self, text: str) -> None:
        msg = EmailMessage()
        msg.set_content(text)
        msg["Subject"] = "Knock Knock"
        msg["From"] = self.sender_email
        msg["To"] = self.recipient_emails
        self.server.sendmail(self.sender_email, self.recipient_emails, msg.as_string())
        self.server.quit()
