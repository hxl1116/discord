import json
import os

from aiohttp import ClientSession
from discord import AsyncWebhookAdapter, Embed, Webhook

resources_root = '/Users/henrylarson/PycharmProjects/discord/resources/'
credentials_root = 'eft_ammo/bot_credentials.json'

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
        if self.cartridges is None:
            embed = Embed.from_dict({
                'title': 'Commands',
                'description': 'These are the list of flags to modify your input to the EFT Ammo Bot.\n'
                               'Every command starts with **/eft** and each parameter is space-delimited.\n'
            })
            for key, value in flags.items():
                embed.add_field(name='**%s**' % key, value=value)
            return embed
        elif len(self.cartridges) == 0:
            # No results embed
            return Embed.from_dict({
                'title': 'Uh-oh!',
                'description': 'The query returned no results.'
            })
        elif len(self.cartridges) == 1:
            # Result cartridge embed
            embed = Embed.from_dict({'title': self.cartridges[0]['nom']}).set_thumbnail(url=self.cartridges[0]['ico'])
            for key, val in [key for key in self.cartridges[0].items()][2:]:
                if val:
                    embed.add_field(name=self.key_conversions[key], value=val, inline=True)
            return embed
        else:
            # Results list embed
            embed = Embed.from_dict({
                'title': 'Results',
                'description': '\nQuick stats: **/eft -res** *result id*'
            }).set_footer(text='page %d of %d' % (1, (len(self.cartridges) // 5) + 1))
            [embed.add_field(name='Result %d' % (self.cartridges.index(cartridge) + 1),
                             value=cartridge['nom'],
                             inline=False)
             for cartridge in self.cartridges]

            # TODO: Conditionally add fields based on result indexes
            embed.add_field(name='Next results', value='\n**/eft -next**')
            embed.add_field(name='Previous results', value='\n**/eft -prev**')
            return embed

    async def fire(self):
        async with ClientSession() as session:
            webhook = Webhook.from_url(self.info['testUrl' if self.test_mode else 'url'],
                                       adapter=AsyncWebhookAdapter(session))
            await webhook.send(username=self.info['name'], embed=self.get_embed())
