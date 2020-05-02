import json
import os

from aiohttp import ClientSession
from discord import AsyncWebhookAdapter, Embed, Webhook

resources_root = '/Users/henrylarson/PycharmProjects/discord/resources/'
credentials_root = 'eft_ammo/bot_credentials.json'


class EFTWebhook:
    key_conversions = {'ico': 'Icon', 'nom': 'Name', 'dmg': 'Damage', 'pen': 'Penetration', 'arm': 'Armor Damage',
                       'acc': 'Accuracy', 'rec': 'Recoil', 'frg': 'Fragmentation Chance', 'ric': 'Ricochet Chance',
                       'vel': 'Projectile Speed', 'spc': 'Special Stat', 'sld': 'Sold by'}

    cartridges = []

    def __init__(self, test_mode=False):
        self.test_mode = test_mode
        self.info = json.load(
            open(os.path.join(resources_root, credentials_root)))

    def set_items(self, items):
        self.cartridges = items

    def get_embed(self):
        if len(self.cartridges) == 1:
            # Result cartridge embed
            embed = Embed.from_dict({'title': self.cartridges[0]['nom']}).set_thumbnail(url=self.cartridges[0]['ico'])
            for key in [key for key in self.cartridges[0].keys()][2:]:
                embed.add_field(name=self.key_conversions[key], value=self.cartridges[0][key], inline=True)
            return embed
        elif len(self.cartridges) > 1:
            # Results list embed
            return Embed.from_dict({
                'title': 'Results',
                'description': '\n'.join([cartridge['nom'] for cartridge in self.cartridges])
            })
        else:
            # No results embed
            return Embed.from_dict({
                'title': 'Uh-oh!',
                'description': 'The query returned no results.'
            })

    async def fire(self):
        async with ClientSession() as session:
            webhook = Webhook.from_url(self.info['testUrl' if self.test_mode else 'url'],
                                       adapter=AsyncWebhookAdapter(session))
            await webhook.send(username=self.info['name'], embed=self.get_embed())
