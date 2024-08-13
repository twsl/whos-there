from __future__ import annotations  # remove when dropping 3.8 support

from typing import Any

from whos_there.senders.base import Sender


class SlackSender(Sender):
    def __init__(
        self,
        webhook_url: str,
        channel: str,
        user_mentions: list[str] | None = None,
        sender_username: str = "Who's There notification",
        icon_emoji: str = ":bell:",
    ) -> None:
        """Initialize the Slack sender.

        Args:
            webhook_url (str): The Slack webhook URL.
            channel (str): The Slack channel name.
            sender_username (str): User name used for notifications (defaults to "Who's There notification").
            user_mentions (List[str]): The list of users to mention (defaults to None).
            icon_emoji (str): Emoji to use for the notifications (defaults to ":bell:")
                              See <https://www.webfx.com/tools/emoji-cheat-sheet/> for options.
        """
        super().__init__()
        self.webhook_url = webhook_url
        self.channel = channel
        self.sender_username = sender_username
        self.icon_emoji: str = icon_emoji
        self.user_mentions = " ".join(user_mentions) if user_mentions else ""

    def send(self, text: str) -> Any:
        data = {
            "username": self.sender_username,
            "channel": self.channel,
            "link_names": 1,
            "icon_emoji": self.icon_emoji,
            "text": f"{text} {self.user_mentions}",
        }
        return self._send_json(self.webhook_url, data)
