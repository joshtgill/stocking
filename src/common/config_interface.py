import json
from datetime import datetime, timedelta
import re


class ConfigInterface:

    def __init__(self, configPath, fileInterface):
        self.fileInterface = fileInterface
        self.config = json.loads(self.fileInterface.read(configPath))
        self.loadVariables(self.config)
        self.rootConfig = self.config


    def loadVariables(self, config):
        if type(config) is not dict:
            return

        for key in config:
            value = config.get(key)
            if type(value) is dict:
                self.loadVariables(value)
            elif type(value) is list:
                for itemValue in value:
                    self.loadVariables(itemValue)
            else:
                config.update({key: self.translateVariable(value)})


    def translateVariable(self, variable):
        if variable == 'ALL_SYMBOLS':
            return json.loads(self.fileInterface.read('exe/symbols/all_symbols.json'))
        elif variable == 'GOOD_SYMBOLS':
            return json.loads(self.fileInterface.read('exe/symbols/good_symbols.json'))
        else:
            return variable


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
