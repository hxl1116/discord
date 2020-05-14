import json
import logging
import os
import re
import sys

from accessor import Accessor
from discord import Client
from webhook import EFTWebhook

client = Client()
accessor = Accessor()
webhook = EFTWebhook(test_mode=True)

resources_root = '/Users/henrylarson/PycharmProjects/discord/resources/'
credentials_root = 'eft_ammo/bot_credentials.json'
log_file = 'eft_ammo/eft_bot.log'

credentials = {}
eft_channel_id = 400833561885802496
test_channel_id = 688191103706333185

# TODO: Add '-next' and '-prev' entries
flags = {
    '-nom': 'Get the cartridge(s) matching the given name identifier(s)',
    '-dmg': 'Get the cartridge(s) matching the given damage value',
    '-pen': 'Get the cartridge(s) matching the given penetration value',
    '-arm': 'Get the cartridge(s) matching the given armor damage value',
    '-acc': 'Get the cartridge(s) matching the given accuracy value',
    '-rec': 'Get the cartridge(s) matching the given recoil value',
    '-frg': 'Get the cartridge(s) matching the given fragmentation chance value',
    '-ric': 'Get the cartridge(s) matching the given ricochet chance value',
    '-vel': 'Get the cartridge(s) matching the given projectile speed value',
    '-spc': 'Get the cartridge(s) matching the given special attribute value',
    '-sld': 'Get the cartridge(s) matching the given "sold by" value',
    '-res': 'Get the cartridge with the given result identifier',
    '-help': 'Show this list of commands'
}


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    logging.info('Message: %s' % message)
    if message.author == client.user:
        return
    if message.channel.id != eft_channel_id and message.channel.id != test_channel_id:
        return

    if message.content.startswith('/eft'):
        # Split arguments and discard '/eft'
        if any(flag in message.content for flag in flags.keys()):  # If using a flag operator
            # Param groups by flag sans '/eft'
            command_string = {group[0][1:]: list(filter(None, group[1:]))
                      for group in [param.split(' ')
                                    for param in list(filter(None, re.split('((?=-[^0-9]){3})', message.content)[1:]))]}
        else:  # Not using a flag operator
            # Params sans '/eft'
            command_string = message.content.split(' ')[1:]
        result_set = accessor.get_cartridges(command_string=command_string)
        logging.info('Result set: %s' % result_set)
        if result_set is None:
            webhook.set_items(None)
        else:
            webhook.set_items(result_set[:5]) if len(result_set) > 5 else webhook.set_items(result_set)
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
        logging.basicConfig(filename=os.path.join(resources_root, log_file), level=logging.INFO)
    main()
