from aiohttp import ClientSession
from discord import AsyncWebhookAdapter, Embed, Webhook
from teams_creator import TeamsCreator
import json
import os

# Resources
# resource_root = '/Users/henrylarson/PycharmProjects/discord/resources/'
resource_root = '/home/pi/Discord/resources/'
info_root = 'bot/teams_creator/info.json'


class TeamsWebhook:
    info = {}
    teams = {}

    def __init__(self, test_mode=False):
        self.test_mode = test_mode
        self.info = json.load(open(os.path.join(resource_root, info_root)))

    def set_teams(self, teams):
        self.teams = teams

    def get_team_embeds(self):
        team_embeds = []
        for item in self.teams.items():
            team_embeds.append(Embed.from_dict({
                'title': item[0],
                'description': ', '.join(item[1]),
                'color': 26367 if item[0] == 'Blue' else 16750899
            }).set_footer(text=TeamsCreator.get_cheer()))
        return team_embeds

    async def fire(self):
        async with ClientSession() as session:
            webhook = Webhook.from_url(self.info['test_url' if self.test_mode else 'url'],
                                       adapter=AsyncWebhookAdapter(session))
            await webhook.send(username=self.info['name'], embeds=self.get_team_embeds())
