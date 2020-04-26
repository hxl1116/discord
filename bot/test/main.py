import asyncio
import json

from discord import Client

client = Client()
bot_credentials = {'name': '', 'id': None, 'token': '', 'webhook_url': ''}


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == '/test':
        await message.channel.send('Activity: ' + client.activity)
        # await hook_msg(bot_credentials['webhook_url'])


def load_credentials():
    with open('../../resources/test_credentials.json') as credentials:
        for [key, value] in zip(bot_credentials, json.load(credentials).values()):
            bot_credentials[key] = value


async def main():
    load_credentials()
    # schedule.every(3).seconds.do(hook_msg(bot_credentials['webhook_url']))
    await client.start(bot_credentials['token'], bot=True)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        client.close()
    finally:
        loop.close()
