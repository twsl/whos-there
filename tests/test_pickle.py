from multiprocessing.reduction import ForkingPickler

from whos_there.callback import NotificationCallback
from whos_there.senders import DebugSender, DiscordSender, EmailSender, SlackSender, TeamsSender, TelegramSender


def test_notification_pickle():
    ForkingPickler.dumps(NotificationCallback())


def test_debug_pickle():
    ForkingPickler.dumps(DebugSender())


def test_discord_pickle():
    ForkingPickler.dumps(DiscordSender(webhook_url=None))


def test_email_pickle():
    ForkingPickler.dumps(EmailSender(host=None, port=0, sender_email=None, password=None, recipient_emails=[]))


def test_slack_pickle():
    ForkingPickler.dumps(SlackSender(webhook_url=None, channel=None))


def test_telegram_pickle():
    ForkingPickler.dumps(TelegramSender(token=None, chat_id=None))
