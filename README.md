# Who's there?

[![Build](https://github.com/twsl/whos-there/actions/workflows/build.yaml/badge.svg)](https://github.com/twsl/whos-there/actions/workflows/build.yaml)
[![Documentation](https://github.com/twsl/whos-there/actions/workflows/docs.yaml/badge.svg)](https://github.com/twsl/whos-there/actions/workflows/docs.yaml)
![GitHub Release](https://img.shields.io/github/v/release/twsl/whos-there?include_prereleases)
[![PyPI - Package Version](https://img.shields.io/pypi/v/whos-there?logo=pypi&style=flat&color=orange)](https://pypi.org/project/whos-there/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/whos-there?logo=pypi&style=flat&color=blue)](https://pypi.org/project/whos-there/)
[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/twsl/whos-there/pulls?utf8=%E2%9C%93&q=is:pr%20author:app/dependabot)
[![Conda - Platform](https://img.shields.io/conda/pn/conda-forge/whos-there?logo=anaconda&style=flat)](https://anaconda.org/conda-forge/whos-there)
[![Conda (channel only)](https://img.shields.io/conda/vn/conda-forge/whos-there?logo=anaconda&style=flat&color=orange)](https://anaconda.org/conda-forge/whos-there)
[![Docs with MkDocs](https://img.shields.io/badge/MkDocs-docs?style=flat&logo=materialformkdocs&logoColor=white&color=%23526CFE)](https://squidfunk.github.io/mkdocs-material/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![linting: ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](.pre-commit-config.yaml)
[![Checked with pyright](https://microsoft.github.io/pyright/img/pyright_badge.svg)](https://microsoft.github.io/pyright/)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/twsl/whos-there/releases)
[![Copier](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-grayscale-border.json)](https://github.com/copier-org/copier)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

The spiritual successor to [knockknock](https://github.com/huggingface/knockknock) for [PyTorch Lightning](https://github.com/PyTorchLightning/pytorch-lightning), to get a notification when your training is complete or when it crashes during the process with a single callback.


## Features

- Supports E-Mail, Discord, Slack, Teams, Telegram


## Installation

With `pip`:
```bash
python -m pip install whos-there
```

With [`poetry`](https://python-poetry.org/):
```bash
poetry add whos-there
```

With `conda`:

```bash
conda install conda-forge::whos-there
```
Check [here](https://github.com/conda-forge/whos-there-feedstock) for more information.


## How to use it

```python
import lightning.pytorch as pl
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
    webhook_url="https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX",   # gitleaks:allow
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


## Docs

```bash
poetry run mkdocs build -f ./docs/mkdocs.yml -d ./_build/
```


## Conda

The conda repository is maintained [here](https://github.com/conda-forge/whos-there-feedstock).


## Update template

```bash
copier update --trust
```

## Credits

This project was generated with [![🚀 A generic python project template.](https://img.shields.io/badge/python--project--template-%F0%9F%9A%80-brightgreen)](https://github.com/twsl/python-project-template)

Big thanks to [knockknock](https://github.com/huggingface/knockknock) for the idea and code snippets.
