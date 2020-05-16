import json
import logging
import os

from bson import ObjectId
from pymongo import MongoClient

test_resources_root = '/Users/henrylarson/PycharmProjects/discord/resources/'
prod_resources_root = '/home/pi/Discord/resources/'
credentials_root = 'eft_ammo/db_credentials.json'


class Accessor:
    credentials = {}
    client = None
    database = None

    cartridges = []

    # TODO: Add >/< operator functionality to 'exact' regex patterns
    query_regexes = {
        'nom': {'def': '(?=.*%s)'},
        'dmg': {'def': '^(%s){1}$'},
        'pen': {'def': '^(%s){1}$'},
        'arm': {'def': '^(%s){1}$'},
        'acc': {'def': '([+|-]%s){1}$', '+': '([+]%s){1}$', '-': '([-]%s){1}$'},
        'rec': {'def': '([+|-]%s){1}$', '+': '([+]%s){1}$', '-': '([-]%s){1}$'},
        'frg': {'def': '^(%s){1}$'},
        'ric': {'def': '^(%s){1}$'},
        'vel': {'def': '^(%s){1}$'},
        'spc': {'def': '(?=.*%s)'},
        'sld': {'def': '(?=.*%s)'}
    }

    identifiers = ['+', '-']

    def __init__(self, test_mode=False):
        self.test_mode = test_mode
        self.load_credentials()
        self.load_database()

    def load_credentials(self):
        self.credentials = json.load(open(os.path.join(test_resources_root if self.test_mode else prod_resources_root, credentials_root)))

    def load_database(self):
        connection_string = str(self.credentials['url']) \
            .replace('<username>', self.credentials['username']) \
            .replace('<password>', self.credentials['password'])

        self.client = MongoClient(connection_string)
        self.database = self.client['eft_ammo']

    def get_identifier(self, param):
        for identifier in self.identifiers:
            if str(param).__contains__(identifier):
                logging.info('Identifier: %s' % identifier)
                return identifier
        logging.info('Identifier: def')
        return 'def'

    def get_regex(self, query, params):
        logging.info('Query: %s\nParams: %s' % (query, params))
        regex_string = ''.join([
            self.query_regexes[query][self.get_identifier(param)] %
            param.translate({ord(identifier): None for identifier in self.identifiers}) for param in params
        ])
        logging.info('Regex String: %s' % regex_string)
        return regex_string

    def get_cartridges(self, command_string=None):
        logging.info('Command String: %s' % command_string)
        if isinstance(command_string, dict):
            if 'help' in command_string.keys():
                return None
            elif 'res' in command_string.keys():
                return self.get_result_cartridge(int(command_string['res'][0]) - 1)
            elif 'next' in command_string.keys():
                self.cartridges = self.cartridges[5:] + self.cartridges[:5]
                return self.cartridges
            elif 'prev' in command_string.keys():
                self.cartridges = self.cartridges[-5:] + self.cartridges[:-5]
                return self.cartridges
            else:
                query_string = {
                    query: {'$regex': self.get_regex(query=query, params=params)}
                    for query, params in command_string.items()
                }
                logging.info('Query String: %s' % query_string)
                self.cartridges = [cartridge for cartridge in self.database.get_collection('all_cartridges')
                    .find(query_string)]
                return self.cartridges
        elif isinstance(command_string, list):
            self.cartridges = [cartridge for cartridge in self.database['all_cartridges'].find({
                'nom': {'$regex': self.get_regex('nom', command_string)}
            })]
            return self.cartridges
        else:
            return []

    def get_result_cartridge(self, idx):
        logging.info('Result Index: %d' % idx)
        return [self.cartridges[idx]]

    def display_cartridge(self, params=None):
        if params is None:
            params = []
        [print(cartridge) for cartridge in self.get_cartridges(params)]


class Encoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        else:
            return json.JSONEncoder.default(self, o)
