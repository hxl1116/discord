import json
import os

from accessor import Accessor
from discord import Client

client = Client()
accessor = Accessor()
credentials = {}

resources_root = '/Users/henrylarson/PycharmProjects/discord/resources/eft_ammo/'
credentials_root = 'bot_credentials.json'


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/eft'):
        # TODO: Create command conditionals
        pass


def load_credentials():
    for key, value in json.load(open(os.path.join(resources_root, credentials_root))).items():
        credentials[key] = value


def main():
    load_credentials()
    client.run(credentials['token'])


if __name__ == '__main__':
    main()
