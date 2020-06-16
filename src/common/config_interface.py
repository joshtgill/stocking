import json


class ConfigInterface:

    def __init__(self, configPath, fileInterface):
        self.fileInterface = fileInterface
        self.config = json.loads(self.fileInterface.read(configPath))
        self.loadVariables(self.config)
        self.rootConfig = self.config


    def loadVariables(self, config):
        variables = {'ALL_SYMBOLS': 'exe/symbols/all_symbols.json'}

        if type(config) is not dict:
            return

        for key in config:
            if type(config.get(key)) is dict:
                self.loadVariables(config.get(key))
            elif type(config.get(key)) is list:
                for itemValue in config.get(key):
                    self.loadVariables(itemValue)
            else:
                if config.get(key) in variables.keys():
                    variableData = json.loads(self.fileInterface.read(variables.get(config.get(key))))
                    config.update({key: variableData})


    def get(self, path='', defaultData=None):
        # Empty path returns the config
        if not path:
            return self.config

        data = self.config.get(path)

        # If key does not exists, return default data
        if not data:
            return defaultData

        return data


    def setConfig(self, key):
        self.config = self.config.get(key)


    def resetConfig(self):
        self.config = self.rootConfig
