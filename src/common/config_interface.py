import json
from datetime import datetime, timedelta
import re


class ConfigInterface:

    def __init__(self, fileInterface, configPath, settingsPath):
        self.fileInterface = fileInterface
        self.config = json.loads(self.fileInterface.read(configPath))
        self.settings = json.loads(self.fileInterface.read(settingsPath))
        self.loadConfigVariables(self.config)
        self.rootConfig = self.config


    def loadConfigVariables(self, config):
        if type(config) is not dict:
            return

        for key in config:
            value = config.get(key)
            if type(value) is dict:
                self.loadConfigVariables(value)
            elif type(value) is list:
                for itemValue in value:
                    self.loadConfigVariables(itemValue)
            else:
                config.update({key: self.translateConfigVariable(value)})


    def translateConfigVariable(self, variable):
        if variable == 'ALL_SYMBOLS':
            return json.loads(self.fileInterface.read('exe/symbols/all_symbols.json'))
        elif variable == 'GOOD_SYMBOLS':
            return json.loads(self.fileInterface.read('exe/symbols/good_symbols.json'))
        else:
            return variable


    def configGet(self, path='', defaultData=None):
        return self.get('CONFIG', path, defaultData)


    def settingsGet(self, path='', defaultData=None):
        return self.get('SETTINGS', path, defaultData)


    def get(self, sourceName, path, defaultData):
        source = self.config if sourceName == 'CONFIG' else self.settings

        if not path:
            return source

        pathList = path.strip().strip('/').split('/')

        configRunner = source
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
        self.config = self.configGet(path)


    def resetConfig(self):
        self.config = self.rootConfig
