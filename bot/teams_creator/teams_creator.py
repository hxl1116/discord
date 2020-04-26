import json
import os
import random

# Resources
# resource_root = '/Users/henrylarson/PycharmProjects/discord/resources/'
resource_root = '/home/pi/Discord/resources/'
presets_root = 'bot/teams_creator/presets.json'


class TeamsCreator:
    teams_display_format = '%s%s: \033[0m\n\t%s'

    names = []
    presets = {}
    teams = {'Blue': [], 'Orange': []}
    last_teams = {'Blue': [], 'Orange': []}
    cheers = ['Wow, so cool!', 'Great moves, keep it up!', 'This doing me an impress!']

    def __init__(self):
        self.load_presets()

    def load_presets(self):
        with open(os.path.join(resource_root, presets_root)) as presets:
            self.presets = json.load(presets)
            presets.close()

    def get_preset(self, preset_id):
        return self.presets[preset_id]

    def get_presets(self):
        return self.presets

    def add_preset(self, names):
        self.presets[str(len(self.presets) + 1)] = names
        with open(os.path.join(resource_root, presets_root), 'w') as presets:
            presets.write(json.dumps(self.presets, separators=(',', ':')))
            presets.close()

    def set_names(self, names):
        self.names = names

    def randomize_teams(self):
        random.shuffle(self.names)
        self.teams['Blue'] = self.names[: len(self.names) // 2]
        self.teams['Orange'] = self.names[len(self.names) // 2:]

        if self.teams['Blue'] == self.last_teams['Blue'] and self.teams['Orange'] == self.last_teams['Orange']:
            self.randomize_teams()

    def make_teams(self, names):
        self.set_names(names)
        self.randomize_teams()
        return self.get_teams()

    def display_teams(self):
        for team in self.teams.keys():
            team_display = self.teams_display_format % \
                           (('\033[33m' if team == 'Orange' else '\033[34m'), team, ',\n\t'.join(self.teams[team]))
            self.teams[team] = ['\n'.join(self.teams[team])]
            print(team_display)

    def get_teams(self):
        return self.teams

    @staticmethod
    def get_cheer():
        return TeamsCreator.cheers[random.randint(0, len(TeamsCreator.cheers) - 1)]
