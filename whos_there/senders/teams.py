from typing import List

from whos_there.senders.base import Sender


class TeamsSender(Sender):
    def __init__(self, webhook_url: str, user_mentions: List[str] = []) -> None:
        """Initialize the Teams sender.

        Args:
            webhook_url: The Teams webhook URL.
            user_mentions: The list of users to mention.
        """
        super().__init__()
        self.webhook_url = webhook_url
        self.user_mentions = " ".join(user_mentions)

    def send(self, text: str) -> None:
        data = {
            "username": "Knock Knock",
            "icon_emoji": ":clapper:",  # ":tada:"
            "text": f"{text} {self.user_mentions}",
        }
        return self._send_json(self.webhook_url, data)
