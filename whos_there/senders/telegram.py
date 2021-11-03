import json

import telegram

from whos_there.senders.base import Sender


class TelegramSender(Sender):
    def __init__(self, token: str, chat_id: int) -> None:
        super().__init__()
        self.chat_id = chat_id
        self.bot = telegram.Bot(token=token)

    def send(self, text: str) -> None:
        return self.bot.send_message(chat_id=self.chat_id, text=text)
