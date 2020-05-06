import json
import os
from objects.stock_data import StockData
from datetime import datetime


class DataService:

    def __init__(self, configFilePath):
        self.loadConfig(configFilePath)

        open(self.config.get('logFilePath'), 'w').close()  # Clear log file contents


    def loadConfig(self, configFilePath):
        self.config = {}
        with open(configFilePath, 'r') as filee:
            self.config = json.loads(filee.read())

        # Load in any vars
        configVarMap = {'ALL_SYMBOLS': 'data/symbols/all_symbols.json'}
        for interval in self.config.get('queries'):
            configVar = self.config.get('queries').get(interval)
            if not isinstance(configVar, list) and configVar in configVarMap.keys():
                configVar = self.config.get('queries').get(interval)
                symbolsData = []
                with open(configVarMap.get(configVar), 'r') as filee:
                    symbolsData = json.loads(filee.read())
                self.config.get('queries').update({interval: symbolsData})


    def saveStockData(self, stockData):
        queryDataStr = ''
        for history in stockData.history:
            queryDataStr += str(history) + '\n'

        fileName = '{}_{}.txt'.format(stockData.symbol, stockData.interval)

        with open('data/stock_data/' + fileName, 'a+') as filee:
            filee.write(queryDataStr)


    def getStockDataEnd(self, symbol, interval):
        dataEnd = None

        for dataFileName in os.listdir('{}/'.format(self.config.get('stockDataLoc'))):
            splitDataFileName = dataFileName.split('_')
            fileSymbol = splitDataFileName[0]
            fileInterval = splitDataFileName[1][: splitDataFileName[1].index('.')]
            if fileSymbol == symbol and fileInterval == interval:
                lastLine = ''
                with open('data/stock_data/' + dataFileName, 'rb') as filee:
                    filee.seek(-100, 2)
                    lastLine = filee.readlines()[-1].decode()
                dataEnd = datetime.strptime(eval(lastLine)[0], '%Y-%m-%d %H:%M:%S')

                break

        return dataEnd


    def log(self, logMessage, logType='INFO'):
        with open(self.config.get('logFilePath'), 'a+') as filee:
            filee.write('[{}] ({}): {}\n'.format(datetime.now(), logType, logMessage))


    def write(self, fileLocation, fileName, data):
        with open(fileLocation + fileName, 'a+') as filee:
            filee.write(data)
