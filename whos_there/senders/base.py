import abc
import json
from typing import Any

import requests


class Sender(abc.ABC):
    def __init__(self) -> None:
        super().__init__()

    def send(self, text: str) -> None:
        pass

    def _send_json(self, url: str, data: Any) -> None:
        headers = {"Content-Type": "application/json"}
        payload = json.dumps(data)
        return requests.post(url=url, data=payload, headers=headers)
