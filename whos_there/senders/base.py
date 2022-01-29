import abc
import json
from typing import Any

import requests


class Sender(abc.ABC):
    def __init__(self) -> None:
        super().__init__()

    @abc.abstractmethod
    def send(self, text: str) -> Any:
        """Actually send the text to the desired output method.

        Args:
            text: Message to send.

        Returns:
            Optional return value.
        """
        pass

    def _send_json(self, url: str, data: Any) -> requests.Response:
        """Send JSON data to URL.

        Args:
            url: URL to send the data payload to.
            data: Payload data.

        Returns:
            Response of the HTTP request.
        """
        headers = {"Content-Type": "application/json"}
        payload = json.dumps(data)
        return requests.post(url=url, data=payload, headers=headers)
