from teams_creator import TeamsCreator
from webhooks.teams_webhook import TeamsWebhook
from webhooks.presets_webhook import PresetsWebhook

from discord import Client
import json
import os
import sys

client = Client()

usage_msg = '_Usage_: **/teams** **|** ' \
            '**/names** [-s] <*name*> [*name* [*name*]] **|** ' \
            '**/preset** [*preset value*] **|** ' \
            '**/presets** **|** ' \
            '**/help** **|** '

# Commands/flags dictionaries
commands_dict = {
    'teams': 'Show the current teams',
    'names': 'Create teams with provided names, space delimited',
    'preset': 'Create teams from the provided preset',
    'presets': 'Show the available presets',
    'help': 'Show this command list'
}

flags_dict = {
    '-s': 'Save the list of names to a preset'
}

# Channel IDs
teams_channel = 701508243419037747
test_channel = 688191103706333185

# Resources
# resource_root = '/Users/henrylarson/PycharmProjects/discord/resources/'
resource_root = '/home/pi/Discord/resources/'
credentials_root = 'bot/teams_creator/credentials.json'


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('/'):
        # TODO: Extrapolate teams webhook setup to function
        if message.content == ('/teams' or '/t'):
            # Set teams to most recent teams
            teams_webhook.set_teams(creator.get_teams())
            # Fire teams webhook
            await teams_webhook.fire()
        elif message.content.startswith('/names') or message.content.startswith('/n'):
            # Make teams and fire webhook
            names = message.content.split(' ')[1:]
            if names[0] == '-s' and message.author == client.get_user(credentials['admin_id']):
                # Add the preset
                creator.add_preset(names[1:])
                # Create teams sans '-s' flag
                teams = creator.make_teams(names[1:])
            else:
                # Create teams
                teams = creator.make_teams(names)
            # Set teams
            teams_webhook.set_teams(teams)
            # Fire teams webhook
            await teams_webhook.fire()
        elif message.content == '/presets' or message.content == '/ps':
            # Get presets
            presets = creator.get_presets()
            # Set presets
            presets_webhook.set_presets(presets)
            # Fire presets webhook
            await presets_webhook.fire()
        elif message.content.startswith('/preset') or message.content.startswith('/p'):
            # Get preset id
            preset_id = message.content.split(' ')[1:][0]
            # Retrieve preset names
            names = creator.get_preset(preset_id)
            # Create teams
            teams = creator.make_teams(names)
            # Set teams
            teams_webhook.set_teams(teams)
            # Fire teams webhook
            await teams_webhook.fire()
        else:
            # Send usage message
            await message.channel.send(usage_msg)


def get_credentials():
    return json.load(open(os.path.join(resource_root, credentials_root)))


def main():
    client.run(credentials['token'])


if __name__ == '__main__':
    credentials = get_credentials()
    creator = TeamsCreator()
    teams_webhook = TeamsWebhook(test_mode='test' in sys.argv)
    presets_webhook = PresetsWebhook(test_mode='test' in sys.argv)
    main()
