from whos_there.senders.base import Sender


class DiscordSender(Sender):
    def __init__(self, webhook_url: str) -> None:
        """Initialize the Discord sender.

        Args:
            webhook_url: The Discord webhook URL.
        """
        super().__init__()
        self.webhook_url = webhook_url

    def send(self, text: str) -> None:
        return self._send_json(self.webhook_url, {"content": text})
