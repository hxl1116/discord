import json
import os
import sys

from accessor import Accessor
from discord import Client
from webhook import EFTWebhook

client = Client()
accessor = Accessor()
webhook = EFTWebhook(test_mode=True)

resources_root = '/Users/henrylarson/PycharmProjects/discord/resources/'
credentials_root = 'eft_ammo/bot_credentials.json'

credentials = {}

# TODO: Add flags to query by stat
flags = {}

eft_channel_id = 400833561885802496
test_channel_id = 688191103706333185


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.channel.id != eft_channel_id and message.channel.id != test_channel_id:
        return

    if message.content.startswith('/eft'):
        # Split arguments and discard '/eft'
        params = message.content.split(' ')[1:]
        if params[0] in flags:
            # TODO: Handle flag operations
            pass
        else:
            cartridges = accessor.get_cartridge(params)
            if len(cartridges) > 5:
                # Trim and set cartridge list
                webhook.set_items(cartridges[:5])
            else:
                # Set cartridge list
                webhook.set_items(cartridges)
            await webhook.fire()


def load_credentials():
    for key, value in json.load(open(os.path.join(resources_root, credentials_root))).items():
        credentials[key] = value


def main():
    load_credentials()
    client.run(credentials['token'])


if __name__ == '__main__':
    if 'test' in sys.argv:
        credentials_root = 'test_credentials.json'
    main()
