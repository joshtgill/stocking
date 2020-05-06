import json
import os
from objects.stock_data import StockData
from datetime import datetime


class DataService:

    def __init__(self, configFileName):
        self.loadConfig(configFileName)

        open(self.config.get('logFilePath'), 'w').close()  # Clear log file contents


    def loadConfig(self, configFileName):
        self.config = json.loads(self.read('data/', configFileName, '{}'))

        # Load in any vars
        configVarMap = {'MASTER_LIST': 'data/symbols/master_list.json'}
        for interval in self.config.get('queries'):
            configVar = self.config.get('queries').get(interval)
            if not isinstance(configVar, list) and configVar in configVarMap.keys():
                configVar = self.config.get('queries').get(interval)
                self.config.get('queries').update({interval: json.loads(self.read(configVarMap.get(configVar), ''))})


    def saveStockData(self, stockData):
        queryDataStr = ''
        for history in stockData.history:
            queryDataStr += str(history) + '\n'

        fileName = '{}_{}.txt'.format(stockData.symbol, stockData.interval)

        self.write('data/stock_data/', fileName, queryDataStr)


    def getStockDataEnd(self, symbol, interval):
        dataEnd = None

        for dataFileName in os.listdir('{}/'.format(self.config.get('stockDataLoc'))):
            splitDataFileName = dataFileName.split('_')
            fileSymbol = splitDataFileName[0]
            fileInterval = splitDataFileName[1][: splitDataFileName[1].index('.')]
            if fileSymbol == symbol and fileInterval == interval:
                fileLines = self.read('data/stock_data/', dataFileName).split('\n')[: -1]
                for dataLine in fileLines:
                    pass  # Only want last line of data file
                lastData = eval(dataLine)  # Convert to list
                dataEnd = datetime.strptime(lastData[0], '%Y-%m-%d %H:%M:%S')

                break

        return dataEnd


    def addLogMessage(self, logMessage):
        self.write(self.config.get('logFilePath'), '', logMessage + '\n')


    def write(self, fileLocation, fileName, data):
        with open(fileLocation + fileName, 'a+') as filee:
            filee.write(data)


    def read(self, fileLocation, fileName, defaultData = ''):
        dataStr = ''

        filePath = fileLocation + fileName
        if os.path.exists(filePath):
            with open(filePath, 'r') as filee:
                dataStr = filee.read()

        return dataStr
