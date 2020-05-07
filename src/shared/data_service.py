import json
import os
from shared.stock import Stock
from datetime import datetime


class DataService:

    def __init__(self, configFilePath):
        self.loadConfig(configFilePath)

        self.basicWrite(self.config.get('logFilePath'), ('-' * 30) + '\n')  # Divider


    def loadConfig(self, configFilePath):
        self.config = json.loads(self.basicRead(configFilePath, {}))

        # Load any config vars
        configVarMap = {'ALL_SYMBOLS': 'data/symbols/all_symbols.json', 'GOOD_SYMBOLS': 'data/symbols/good_symbols.json',
                        'QUIET_SYMBOLS': 'data/symbols/quiet_symbols.json'}
        for interval in self.config.get('queries'):
            configVar = self.config.get('queries').get(interval)
            if not isinstance(configVar, list) and configVar in configVarMap.keys():
                symbolsData = json.loads(self.basicRead(configVarMap.get(configVar), []))
                self.config.get('queries').update({interval: symbolsData})


    def saveStock(self, stock):
        stockDataStr = ''
        for history in stock.history:
            stockDataStr += str(history) + '\n'

        fileName = '{}_{}.txt'.format(stock.symbol, stock.interval)

        self.basicWrite('data/stock_data/' + fileName, stockDataStr)


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
        logStr = '[{}] ({}): {}\n'.format(datetime.now(), logType, logMessage)
        self.basicWrite(self.config.get('logFilePath'), logStr)


    def basicWrite(self, path, data):
        with open(path, 'a+') as filee:
            filee.write(data)


    def basicRead(self, path, defaultData = ''):
        with open(path, 'r') as filee:
            return filee.read()

        return defaultData
