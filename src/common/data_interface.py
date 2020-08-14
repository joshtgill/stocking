import json
from datetime import datetime, timedelta
import re


class DataInterface:

    def __init__(self, fileInterface, configPath, settingsPath):
        self.fileInterface = fileInterface
        self.config = json.loads(self.fileInterface.read(configPath))
        self.settings = json.loads(self.fileInterface.read(settingsPath))
        self.trades = json.loads(self.fileInterface.read(self.settings.get('tradesPath'), '{}'))
        self.loadConfigVariables(self.config)
        self.rootConfig = self.config
        self.activePathList = []


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
        if type(variable) is not str:
            return variable

        if variable == 'ALL_SYMBOLS':
            return json.loads(self.fileInterface.read('exe/symbols/all_symbols.json'))
        elif variable == 'GOOD_SYMBOLS':
            return json.loads(self.fileInterface.read('exe/symbols/good_symbols.json'))
        elif variable == 'NOW':
            return datetime.now().strftime(self.settingsGet('{}/dateTimeFormat'.format('1d'))) # TODO: Standarize datetimes across project
        elif 'NOW' in variable:
            marketDaysBack = int(re.sub(r'\s+', '', variable.replace('NOW', '').replace('-', '')).replace('d', ''))
            return self.determineDate(marketDaysBack).strftime(self.settingsGet('{}/dateTimeFormat'.format('1d')))

        return variable


    def determineDate(self, marketDaysBack):
        # 2020 stock market holiday closures
        marketClosedDates = [datetime(2020, 1, 1).date(), datetime(2020, 1, 20).date(), datetime(2020, 2, 17).date(),
                             datetime(2020, 4, 10).date(), datetime(2020, 5, 25).date(), datetime(2020, 7, 3).date(),
                             datetime(2020, 9, 7).date(), datetime(2020, 11, 26).date(), datetime(2020, 12, 25).date()]

        # Find the date associated with the number of market days back
        date = datetime.now().date()
        while True:
            if date.weekday() < 5 and date not in marketClosedDates:
                marketDaysBack -= 1

            if not marketDaysBack:
                break

            date = date - timedelta(days=1)

        return date


    def configGet(self, path='', defaultData=None):
        return self.get('CONFIG', path, defaultData)


    def settingsGet(self, path='', defaultData=None):
        return self.get('SETTINGS', path, defaultData)


    def tradesGet(self, path='', defaultData=None):
        return self.get('TRADES', path, defaultData)


    def get(self, sourceName, path, defaultData):
        sourceDir = {'CONFIG': self.config, 'SETTINGS': self.settings, 'TRADES': self.trades}
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
