import asyncio
import json
from discord import Client

client = Client()
bot_credentials = {'id': None, 'name': '', 'token': '', 'api_key': '', 'webhook_url': ''}

flag_dict = {'-t': False, '-d': False}

# Responses
usage_msg = 'Usage: /nasa [yyyy-mm-dd] [-d] [-t]'


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '/nasa':
        # TODO - get APOD
        pass
    elif message.content.startswith('/nasa'):
        params = message.content.split(' ')[1:]
        # TODO - get APOD with params[0]
        pass
    else:
        await message.channel.send(usage_msg)


def get_apod():
    pass


def load_credentials():
    with open('../../resources/nasa_apod/credentials.json') as credentials:
        for [key, value] in zip(bot_credentials.keys(), json.load(credentials).values()):
            bot_credentials[key] = value


async def main():
    load_credentials()
    await client.start(bot_credentials['token'])


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        loop.run_until_complete(client.close())
        exit(0)
    finally:
        loop.close()
