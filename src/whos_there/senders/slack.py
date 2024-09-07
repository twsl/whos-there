from __future__ import annotations  # remove when dropping 3.8 support

from typing import Any

from whos_there.senders.base import Sender


class SlackSender(Sender):
    def __init__(
        self,
        webhook_url: str,
        channel: str,
        user_mentions: list[str] | None = None,
        sender_username: str = "Kock Knock",
        icon_emoji: str = ":bell:",
    ) -> None:
        """Initialize the Slack sender.

        Args:
            webhook_url: The Slack webhook URL.
            channel: The Slack channel name.
            sender_username: User name used for notifications.
            user_mentions: The list of users to mention.
            icon_emoji: Emoji to use for the notifications.
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
