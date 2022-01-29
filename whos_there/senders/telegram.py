import telegram

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
        self._bot: telegram.Bot = None

    @property
    def bot(self):
        if not self._bot:
            self._bot = telegram.Bot(token=self.token)
        return self._bot

    def send(self, text: str) -> None:
        return self.bot.send_message(chat_id=self.chat_id, text=text)
