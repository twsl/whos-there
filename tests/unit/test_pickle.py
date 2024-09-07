from multiprocessing.reduction import ForkingPickler

from whos_there.callback import NotificationCallback
from whos_there.senders import DebugSender, DiscordSender, EmailSender, SlackSender, TeamsSender, TelegramSender


def test_notification_pickle() -> None:
    ForkingPickler.dumps(NotificationCallback())


def test_debug_pickle() -> None:
    ForkingPickler.dumps(DebugSender())


def test_discord_pickle() -> None:
    ForkingPickler.dumps(DiscordSender(webhook_url=""))


def test_email_pickle() -> None:
    ForkingPickler.dumps(EmailSender(host="", port=0, sender_email="", password="", recipient_emails=[]))  # nosec


def test_slack_pickle() -> None:
    ForkingPickler.dumps(SlackSender(webhook_url="", channel=""))


def test_telegram_pickle() -> None:
    ForkingPickler.dumps(TelegramSender(token="", chat_id=-1))  # nosec
