import json
import os
from shared.stock import Stock
from datetime import datetime


class DataService:

    def __init__(self, configFilePath):
        self.loadConfig(configFilePath)
        self.stockDataTitles = self.loadStockDataTitles()  # A stock title is of the format SYMBOL_INTERVAL

        self.basicWrite(self.config.get('logFilePath'), ('-' * 30) + '\n')  # Write divider


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


    def loadStockDataTitles(self):
        titles = []
        for fileName in os.listdir('{}/'.format(self.config.get('stockDataLoc'))):
            titles.append(fileName[: fileName.index('.txt')])

        return titles


    def saveStock(self, stock):
        dataStr = ''
        for history in stock.history:
            dataStr += str(history) + '\n'

        fileName = '{}_{}.txt'.format(stock.symbol, stock.interval)

        self.basicWrite('data/stock_data/' + fileName, dataStr)


    def getStockDataEnd(self, symbol, interval):
        title = '{}_{}'.format(symbol, interval)
        if title in self.stockDataTitles:
            lastLine = ''
            with open('data/stock_data/{}.txt'.format(title), 'rb') as filee:
                filee.seek(-100, 2)
                lastLine = filee.readlines()[-1].decode()

            return datetime.strptime(eval(lastLine)[0], '%Y-%m-%d %H:%M:%S')

        return None


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
