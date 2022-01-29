import smtplib
from email.message import EmailMessage
from typing import List

from whos_there.senders.base import Sender


class EmailSender(Sender):
    def __init__(self, host: str, port: int, sender_email: str, password: str, recipient_emails: List[str]) -> None:
        """Initialize the Email sender.

        Args:
            host: The SMTP host.
            port: The SMTP port.
            sender_email: The senders email adress.
            password: The email password.
            recipient_emails: The recipients emails.
        """
        super().__init__()
        self.host = host
        self.port = port
        self.sender_email = sender_email
        self.password = password
        self.recipient_emails = recipient_emails
        self._server: smtplib.SMTP = None

    @property
    def server(self) -> smtplib.SMTP:
        """SMTP server instance.

        Returns:
            The SMTP instance.
        """
        if not self._server:
            self._server = smtplib.SMTP(self.host, self.port)
            self._server.starttls()
            self._server.login(self.sender_email, self.password)
        return self._server

    def send(self, text: str) -> None:
        msg = EmailMessage()
        msg.set_content(text)
        msg["Subject"] = "Knock Knock"
        msg["From"] = self.sender_email
        msg["To"] = self.recipient_emails
        self.server.sendmail(self.sender_email, self.recipient_emails, msg.as_string())
        self.server.quit()
