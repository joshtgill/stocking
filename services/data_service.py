import json
import os
from objects.stock_data import StockData
from datetime import datetime


class DataService:

    def __init__(self, configFileName):
        self.config = json.loads(self.read('data/', configFileName, '{}'))

        self.logStr = ''
        open(self.config.get('logFilePath'), 'w').close()  # Clear log


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
        self.logStr += '{}\n'.format(logMessage)
        self.write(self.config.get('logFilePath'), '', self.logStr)


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
