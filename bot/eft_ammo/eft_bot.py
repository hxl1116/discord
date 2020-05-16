import json
import logging
import os
import re
import sys

from accessor import Accessor
from discord import Client
from webhook import EFTWebhook

client = Client()

test_resources_root = '/Users/henrylarson/PycharmProjects/discord/resources/'
prod_resources_root = '/home/pi/Discord/resources/'
credentials_root = 'eft_ammo/bot_credentials.json'
log_file = 'eft_ammo/eft_bot.log'

credentials = {}
eft_channel_id = 400833561885802496
test_channel_id = 688191103706333185

# Flag query operators
flags = [
    '-nom',
    '-dmg',
    '-pen',
    '-arm',
    '-acc',
    '-rec',
    '-frg',
    '-ric',
    '-vel',
    '-spc',
    '-sld',
    '-res',
    '-next',
    '-prev',
    '-help'
]


@client.event
async def on_ready():
    """
    Print to the console when bot is initialized

    :return: None
    """
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    """
    Wait for message events, parse user input, gather data, and fire the webhook

    :param message: User message
    :return: None
    """
    logging.info('Message: %s' % message)
    # Prevent infinite message loop
    if message.author == client.user:
        return
    # Prevent production bot responding to test
    if 'test' not in sys.argv and message.channel.id == test_channel_id:
        return
    # Prevent messaging outside of 'test' and 'eft' channels
    if message.channel.id != eft_channel_id and message.channel.id != test_channel_id:
        return

    if message.content.startswith('/eft'):
        # Split arguments and discard '/eft'
        if any(flag in message.content for flag in flags):
            # Generate query/param map. Split flags by regex, filter out empty indexes, split associated params,
            # then map to query flag
            command_string = {group[0][1:]: list(filter(None, group[1:]))
                              for group in [param.split(' ')
                                            for param in
                                            list(filter(None, re.split('((?=-[^0-9]){3})', message.content)[1:]))]}
        else:
            # Params sans '/eft'
            command_string = message.content.split(' ')[1:]
        result_set = accessor.get_cartridges(command_string=command_string)
        logging.info('Result set: %s' % result_set)
        if result_set is None:
            webhook.set_items(None)
        else:
            # Set webhook items to limit of five if applicable
            webhook.set_items(result_set[:5]) if len(result_set) > 5 else webhook.set_items(result_set)
        await webhook.fire()


def load_credentials(resources_root):
    """
    Get the bot credentials

    :param resources_root:
    :return: None
    """
    for key, value in json.load(open(os.path.join(resources_root, credentials_root))).items():
        credentials[key] = value


def main():
    """
    Initialize and run the bot.

    :return: None
    """

    # Set the production/testing resource root and bot token
    resources_root, token = (test_resources_root, 'testToken') if 'test' in sys.argv \
        else (prod_resources_root, 'token')

    # Call to load bot credentials
    load_credentials(resources_root=resources_root)

    # Logging configuration
    logging.basicConfig(filename=os.path.join(resources_root, log_file))

    # Run the bot
    client.run(credentials[token])


if __name__ == '__main__':
    # Determine if in testing mode
    test_mode = True if 'test' in sys.argv else False

    # Construct the database accessor class
    accessor = Accessor(test_mode=test_mode)

    # Construct the webhook class
    webhook = EFTWebhook(test_mode=test_mode)

    main()
