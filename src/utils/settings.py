import os

import yaml


class Settings:
    SETTINGS_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'settings.yml')

    def __init__(self):
        with open(self.SETTINGS_PATH, 'r') as yaml_f:
            self.config = yaml.load(yaml_f)

    def get_database_settings(self):
        return self.config.get('database')['connection']

    def get_database_view(self, name):
        return self.config.get('database')['views'][name]

    def get_path(self, name):
        if type(name) is str:
            return self.config.get('paths')[name]
        elif type(name) is list:
            result = self.config.get('paths')
            for n in name:
                result = result[n]
            return result
        else:
            raise ValueError()
