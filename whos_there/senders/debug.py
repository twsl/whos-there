import logging

from whos_there.senders.base import Sender

logger = logging.getLogger(__name__)


class DebugSender(Sender):
    def __init__(self, print=False) -> None:
        super().__init__()
        self.print = print

    def send(self, text: str) -> None:
        logger.debug(text)
        if self.print:
            print(text)
