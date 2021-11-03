# Who's there?

<div align="center">
    
[![Build](https://github.com/twsl/whos-there/actions/workflows/build.yml/badge.svg)](https://github.com/twsl/whos-there/actions/workflows/build.yml)
[![Python Version](https://img.shields.io/pypi/pyversions/whos-there.svg)](https://pypi.org/project/whos-there/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/twsl/whos-there/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/twsl/whos-there/blob/master/.pre-commit-config.yaml)
[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/twsl/whos-there/releases)
[![License](https://img.shields.io/github/license/twsl/whos-there)](https://github.com/twsl/whos-there/blob/master/LICENSE)

The spiritual successor to [knockknock](https://github.com/huggingface/knockknock) for [PyTorch Lightning](https://github.com/PyTorchLightning/pytorch-lightning), to get a notification when your training is complete or when it crashes during the process with a single callback.

</div>

## 🚀 Features

- Supports E-Mail, Discord, Slack, Teams, Telegram

## 🎯 Installation

```bash
pip install -U whos-there
```

or install with `Poetry`

```bash
poetry add whos-there
```

## 🤯 How to use it

```python
from whos_there.callback import NotificationCallback
from whos_there.senders.debug import DebugSender

trainer = pl.Trainer(
    callbacks=[
        NotificationCallback(senders=[
            # Add your senders here
            DebugSender(),
        ])
    ]
)
```

### E-Mail
Requires your e-mail provider specific SMTP settings.

```python
from whos_there.senders.email import EmailSender
# ...
EmailSender(
    host="smtp.example.de",
    port=587,
    sender_email="from@example.com",
    password="*********",
    recipient_emails=[
        "to1@example.com",
        "to2@example.com",
    ]
)
```

### Discord
Requires your Discord channel's [webhook URL](https://support.discordapp.com/hc/en-us/articles/228383668-Intro-to-Webhooks).

```python
from whos_there.senders.discord import DiscordSender
# ...
DiscordSender(
    webhook_url="https://discord.com/api/webhooks/XXXXXXXXXXXXXX/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
)
```

### Slack
Requires your Slack room [webhook URL](https://api.slack.com/incoming-webhooks#create_a_webhook) and optionally your [user id](https://api.slack.com/methods/users.identity) (if you want to tag yourself or someone else).

```python
from whos_there.senders.slack import SlackSender
# ...
SlackSender(
    webhook_url="https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX",
    channel="channel_name",
    user_mentions=[
        "XXXXXXXX"
    ]
)
```

### Teams
Requires your Team Channel [webhook URL](https://docs.microsoft.com/en-us/microsoftteams/platform/concepts/connectors/connectors-using).

```python
from whos_there.senders.teams import TeamsSender
# ...
TeamsSender(
    webhook_url="https://XXXXX.webhook.office.com/",
    user_mentions=[
        "twsl"
    ]
)
```

### Telegram
You can also use Telegram Messenger to get notifications. You'll first have to create your own notification bot by following the three steps provided by Telegram [here](https://core.telegram.org/bots#6-botfather) and save your API access `TOKEN`.
Telegram bots are shy and can't send the first message so you'll have to do the first step. By sending the first message, you'll be able to get the `chat_id` required (identification of your messaging room) by visiting `https://api.telegram.org/bot<YourBOTToken>/getUpdates` and get the `int` under the key `message['chat']['id']`.

```python
from whos_there.senders.telegram import TelegramSender
# ...
TelegramSender(
    chat_id=1234567890,
    token="XXXXXXX:XXXXXXXXXXXXXXXXXXXXXXXXXXX"
)
```

## 🛡 License

[![License](https://img.shields.io/github/license/twsl/whos-there)](https://github.com/twsl/whos-there/blob/master/LICENSE)

This project is licensed under the terms of the MIT license. See [LICENSE](https://github.com/twsl/whos-there/blob/master/LICENSE) for more details.

## 🏅 Credits

This project was generated with [![🚀 Your next Python package needs a bleeding-edge project structure.](https://img.shields.io/badge/python--package--template-%F0%9F%9A%80-brightgreen)](https://github.com/TezRomacH/python-package-template)

Big thanks to [knockknock](https://github.com/huggingface/knockknock) for the idea and code snippets.
