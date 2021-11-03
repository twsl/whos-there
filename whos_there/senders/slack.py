import json
from typing import List

import requests

from whos_there.senders.base import Sender


class SlackSender(Sender):
    def __init__(self, webhook_url: str, channel: str, user_mentions: List[str] = []) -> None:
        super().__init__()
        self.webhook_url = webhook_url
        self.channel = channel
        self.user_mentions = " ".join(user_mentions)

    def send(self, text: str) -> None:
        data = {
            "username": "Knock Knock",
            "channel": self.channel,
            "icon_emoji": ":clapper:",  # ":tada:"
            "text": f"{text} {self.user_mentions}",
        }
        return self._send_json(self.webhook_url, data)
