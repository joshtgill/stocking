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
        if not path:
            return self.config

        pathList = path.strip().strip('/').split('/')

        configRunner = self.config
        try:
            for key in pathList:
                if '[' in key:
                    keyIndex = int(key[key.index('[') + 1 : key.index(']')])
                    key = key[0: key.index('[')]
                    configRunner = configRunner.get(key)[keyIndex]
                else:
                    configRunner = configRunner.get(key)
        except AttributeError:
            return defaultData

        return configRunner


    def setConfig(self, path):
        self.config = self.get(path)


    def resetConfig(self):
        self.config = self.rootConfig
