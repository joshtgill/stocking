import json
from datetime import datetime, timedelta
import re


class DataInterface:

    def __init__(self, fileInterface, configPath, settingsPath):
        self.fileInterface = fileInterface
        self.config = json.loads(self.fileInterface.read(configPath))
        self.settings = json.loads(self.fileInterface.read(settingsPath))
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

        if variable == 'NOW':
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
        return self.get(self.config, path, defaultData)


    def settingsGet(self, path='', defaultData=None):
        return self.get(self.settings, path, defaultData)


    def get(self, source, path, defaultData):
        pathList = self.pathToList(path)

        try:
            sourceRunner = source
            for key in pathList:
                if '[' in key:
                    keyIndex = int(key[key.index('[') + 1 : key.index(']')])
                    key = key[0: key.index('[')]
                    if key:
                        sourceRunner = sourceRunner.get(key)[keyIndex]
                    else:
                        sourceRunner = sourceRunner[keyIndex]
                else:
                    sourceRunner = sourceRunner.get(key)
        except AttributeError:
            return defaultData

        return sourceRunner if sourceRunner != None else defaultData


    def sett(self, source, path, value, filePath):
        pathList = self.pathToList(path)
        lastKey = pathList.pop()

        sourceRunner = source
        for key in pathList:
            if key not in sourceRunner:
                sourceRunner.update({key: {}})
            sourceRunner = sourceRunner.get(key)

        # If value is None then delete the existing key
        if value:
            sourceRunner.update({lastKey: value})
        else:
            value = sourceRunner.pop(lastKey)

        self.fileInterface.wipe(filePath)
        self.fileInterface.write(filePath, json.dumps(source))
        source = json.loads(self.fileInterface.read(filePath))

        return value


    def pathToList(self, path):
        if path == '':
            return []

        return path.strip().strip('/').split('/')
