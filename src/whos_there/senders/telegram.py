from typing import Any

from telegram import Bot
from telegram.constants import MessageLimit

from whos_there.senders.base import Sender


class TelegramSender(Sender):
    def __init__(self, token: str, chat_id: int) -> None:
        """Initialize the Telegram sender.

        Args:
            token: The Telegram token.
            chat_id: The Telegram chat id.
        """
        super().__init__()
        self.token = token
        self.chat_id = chat_id
        self._bot: Bot | None = None

    @property
    def bot(self) -> Bot:
        if not self._bot:
            self._bot = Bot(token=self.token)
        return self._bot

    def send(self, text: str) -> Any:
        length = MessageLimit.MAX_TEXT_LENGTH
        chunks = [text[i : length + i] for i in range(0, len(text), length)]
        for chunk in chunks:
            _ = self.bot.send_message(chat_id=self.chat_id, text=chunk)
