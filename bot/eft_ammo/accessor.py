import json
import os

from bson import ObjectId
from pymongo import MongoClient

resources_root = '/Users/henrylarson/PycharmProjects/eft-api/resources/'
credentials_root = 'credentials.json'


class Accessor:
    credentials = {}
    client = None
    database = None

    def __init__(self):
        self.load_credentials()
        self.load_database()

    def load_credentials(self):
        self.credentials = json.load(open(os.path.join(resources_root, credentials_root)))

    def load_database(self):
        connection_string = str(self.credentials['connection']) \
            .replace('<username>', self.credentials['username']) \
            .replace('<password>', self.credentials['password'])

        self.client = MongoClient(connection_string)
        self.database = self.client['eft_ammo']

    def get_cartridge(self, cartridge=''):
        return self.database.get_collection('all_cartridges').find({'nom': {'$regex': '%s+|'.join(cartridge)}})


class Encoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        else:
            return json.JSONEncoder.default(self, o)


if __name__ == '__main__':
    accessor = Accessor()
    cartridges = accessor.get_cartridge()
    [print(cartridge) for cartridge in cartridges]
