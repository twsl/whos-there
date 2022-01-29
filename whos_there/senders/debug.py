from whos_there.senders.base import Sender
from whos_there.utils.logging import get_logger

logger = get_logger(__name__)


class DebugSender(Sender):
    def __init__(self, print: bool = False) -> None:
        """Initialize the Debug sender.
        Uses the Python logger. Performs logging on rank zero only in a distributed mode.

        Args:
            print: If enabled, outputs using the print command in addition. Defaults to False.. Defaults to False.
        """
        super().__init__()
        self.print = print

    def send(self, text: str) -> None:
        logger.debug(text)
        if self.print:
            print(text)
