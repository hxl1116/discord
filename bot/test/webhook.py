from aiohttp import ClientSession
from discord import Webhook, AsyncWebhookAdapter


async def get_webhook(webhook_url):
    async with ClientSession() as session:
        webhook = Webhook.from_url(webhook_url, adapter=AsyncWebhookAdapter(session))
        await webhook.send('Hello Test!', username='Test Message')


async def send_msg(webhook, message=''):
    await webhook.send(message, username='Test Message')
