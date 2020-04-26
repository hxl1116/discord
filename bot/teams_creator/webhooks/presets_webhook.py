from aiohttp import ClientSession
from discord import AsyncWebhookAdapter, Embed, Webhook

import json
import os

# Resources
# resource_root = '/Users/henrylarson/PycharmProjects/discord/resources/'
resource_root = '/home/pi/Discord/resources/'
info_root = 'bot/teams_creator/info.json'
presets_root = 'bot/teams_creator/presets.json'


class PresetsWebhook:
    info = {}
    presets = {}

    def __init__(self, test_mode=False):
        self.test_mode = test_mode
        self.info = json.load(open(os.path.join(resource_root, info_root)))

    def set_presets(self, presets):
        self.presets = presets

    def get_presets_embed(self):
        presets_embed = Embed.from_dict({'title': 'Presets'})
        for preset_id, preset_names in self.presets.items():
            presets_embed.add_field(name='Preset %s' % preset_id, value=', '.join(preset_names), inline=False)
        return presets_embed

    async def fire(self):
        async with ClientSession() as session:
            webhook = Webhook.from_url(self.info['test_url' if self.test_mode else 'url'],
                                       adapter=AsyncWebhookAdapter(session))
            await webhook.send(username=self.info['name'], embed=self.get_presets_embed())
