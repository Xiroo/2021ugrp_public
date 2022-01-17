from discord_webhook import DiscordWebhook

from .auth import webhook as WEBHOOK
from .auth import error as WEB_ERR


def post_message(text):
    webhook = DiscordWebhook(url=WEBHOOK, content=text)
    response = webhook.execute()


def post_err(text):
    webhook = DiscordWebhook(url=WEB_ERR, content=text)
    response = webhook.execute()
