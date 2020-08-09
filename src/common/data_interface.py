import json
from datetime import datetime, timedelta
import re


class DataInterface:

    def __init__(self, fileInterface, configPath, settingsPath):
        self.fileInterface = fileInterface
        self.config = json.loads(self.fileInterface.read(configPath))
        self.loadConfigVariables(self.config)
        self.rootConfig = self.config
        self.activePathList = []
        self.settings = json.loads(self.fileInterface.read(settingsPath))
        self.trades = json.loads(self.fileInterface.read(self.settings.get('tradesPath'), '{}'))
        self.bank = json.loads(self.fileInterface.read(self.settings.get('bankPath'), '{}'))


    def incrementConfig(self, path):
        self.activePathList.extend(self.pathToList(path))
        self.config = self.configGet(path)


    def decrementConfig(self, numDecrements=1):
        for i in range(numDecrements):
            self.activePathList.pop()

        self.config = self.rootConfig
        self.config = self.configGet('/'.join(self.activePathList))


    def loadConfigVariables(self, config):
        if type(config) is dict:
            for key in config:
                value = config.get(key)
                if type(value) is dict:
                    self.loadConfigVariables(value)
                elif type(value) is list:
                    for itemValue in value:
                        self.loadConfigVariables(itemValue)
                else:
                    config.update({key: self.translateConfigVariable(value)})
        elif type(config) is list:
            for item in config:
                self.loadConfigVariables(item)


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


    def tradesGet(self, path='', defaultData=None):
        return self.get('TRADES', path, defaultData)


    def bankGet(self, path='', defaultData=None):
        return self.get('BANK', path, defaultData)


    def get(self, sourceName, path, defaultData):
        sourceDir = {'CONFIG': self.config, 'SETTINGS': self.settings, 'TRADES': self.trades, 'BANK': self.bank}
        source = sourceDir.get(sourceName)

        pathList = self.pathToList(path)

        configRunner = source
        try:
            for key in pathList:
                if '[' in key:
                    keyIndex = int(key[key.index('[') + 1 : key.index(']')])
                    key = key[0: key.index('[')]
                    if key:
                        configRunner = configRunner.get(key)[keyIndex]
                    else:
                        configRunner = configRunner[keyIndex]
                else:
                    configRunner = configRunner.get(key)
        except AttributeError:
            return defaultData

        return configRunner


    def pathToList(self, path):
        if path == '':
            return []

        return path.strip().strip('/').split('/')


    # Termporary until a set() method is created
    def tradesSave(self):
        self.fileInterface.wipe(self.settingsGet('tradesPath'))
        self.fileInterface.write(self.settingsGet('tradesPath'), json.dumps(self.trades))


    # Termporary until a set() method is created
    def bankSave(self):
        self.fileInterface.wipe(self.settingsGet('bankPath'))
        self.fileInterface.write(self.settingsGet('bankPath'), json.dumps(self.bank))
