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
            if self.config.get('queries').get(interval) in configVarMap.keys():
                configVar = self.config.get('queries').get(interval)
                self.config.get('queries').update({interval: json.loads(self.read(configVarMap.get(configVar), ''))})


    def saveStockData(self, stockData):
        queryDataStr = ''
        for history in stockData.history:
            queryDataStr += str(history) + '\n'

        fileName = '{}_{}.txt'.format(stockData.symbol, stockData.interval)

        self.write('data/stock_data/', fileName, queryDataStr)


    def loadStockData(self, symbol, interval):
        stockData = None

        for dataFileName in os.listdir('{}/'.format(self.config.get('stockDataLoc'))):
            splitDataFileName = dataFileName.split('_')
            fileSymbol = splitDataFileName[0]
            fileInterval = splitDataFileName[1][: splitDataFileName[1].index('.')]
            if fileSymbol == symbol and fileInterval == interval:
                stockData = StockData(fileSymbol, fileInterval)
                fileLines = self.read('data/stock_data/', dataFileName).split('\n')[: -1]
                for dataLine in fileLines:
                    try:
                        dataLine = eval(dataLine.strip())
                    except NameError:
                        continue
                    stockData.history.append(dataLine)
                if len(stockData.history) > 0:
                    stockData.start = datetime.strptime(stockData.history[0][0], '%Y-%m-%d %H:%M:%S')
                    stockData.end = datetime.strptime(stockData.history[len(stockData.history) - 1][0], '%Y-%m-%d %H:%M:%S')
                else:
                    print(symbol)
                    return None

                break

        return stockData


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
