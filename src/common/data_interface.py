import json
from datetime import datetime, timedelta
import re


class DataInterface:

    def __init__(self, fileInterface, configPath, settingsPath):
        self.fileInterface = fileInterface
        self.config = json.loads(self.fileInterface.read(configPath))
        self.settings = json.loads(self.fileInterface.read(settingsPath))
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
