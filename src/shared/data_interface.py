import json
import os
from shared.stock import Stock
from datetime import datetime


class DataInterface:

    def __init__(self, queryConfigFilePath, tradeConfigFilePath):
        self.queryConfig = self.loadQueryConfig(queryConfigFilePath)
        self.tradeConfig = json.loads(self.basicRead(tradeConfigFilePath, {}))

        self.stockDataTitles = self.loadStockDataTitles()  # A stock title is of the format SYMBOL_INTERVAL
        self.basicWrite(self.queryConfig.get('logFilePath'), ('-' * 30) + '\n')  # Write divider


    def loadQueryConfig(self, configFilePath):
        config = json.loads(self.basicRead(configFilePath, {}))

        # Load any config vars
        configVarMap = {'ALL_SYMBOLS': 'data/symbols/all_symbols.json', 'GOOD_SYMBOLS': 'data/symbols/good_symbols.json',
                        'QUIET_SYMBOLS': 'data/symbols/quiet_symbols.json'}
        for interval in config.get('queries'):
            configVar = config.get('queries').get(interval)
            if not isinstance(configVar, list) and configVar in configVarMap.keys():
                symbolsData = json.loads(self.basicRead(configVarMap.get(configVar), []))
                config.get('queries').update({interval: symbolsData})

        return config


    def loadStockDataTitles(self):
        titles = []
        for fileName in os.listdir('{}/'.format(self.queryConfig.get('stockDataLoc'))):
            titles.append(fileName[: fileName.index('.txt')])

        return titles


    def saveStock(self, stock):
        dataStr = ''
        for history in stock.history:
            dataStr += str(history) + '\n'

        fileTitle = '{}_{}'.format(stock.symbol, stock.interval)
        if fileTitle not in self.stockDataTitles:
            self.stockDataTitles.append(fileTitle)
        self.basicWrite('data/stock_data/{}.txt'.format(fileTitle), dataStr)


    def loadStockData(self, symbol, interval):
        stockDataTitle = symbol + '_' + interval
        if stockDataTitle in self.stockDataTitles:
            stock = Stock(symbol, interval)
            with open('data/stock_data/{}.txt'.format(stockDataTitle), 'r') as filee:
                for historyItem in filee.readlines()[: -1]:
                    stock.history.append(eval(historyItem))

            return stock

        return None


    def getStockDataEnd(self, symbol, interval):
        title = '{}_{}'.format(symbol, interval)
        if title in self.stockDataTitles:
            lastLine = ''
            with open('data/stock_data/{}.txt'.format(title), 'rb') as filee:
                filee.seek(-100, 2)
                lastLine = filee.readlines()[-1].decode()

            return datetime.strptime(eval(lastLine)[0], '%Y-%m-%d %H:%M:%S')

        return None


    def loadTradeData(self):
        buys = {}
        for buy in self.tradeConfig.get('buys'):
            buys.update({datetime.strptime(buy.get('datetime'), '%Y-%m-%d %H:%M:%S'): (buy.get('symbol'), buy.get('shares'))})

        sells = {}
        for sell in self.tradeConfig.get('sells'):
            sells.update({datetime.strptime(sell.get('datetime'), '%Y-%m-%d %H:%M:%S'): (sell.get('symbol'), sell.get('shares'))})

        return buys, sells


    def log(self, logMessage, logType='INFO'):
        logStr = '[{}] ({}): {}\n'.format(datetime.now(), logType, logMessage)
        self.basicWrite(self.queryConfig.get('logFilePath'), logStr)


    def basicWrite(self, path, data):
        with open(path, 'a+') as filee:
            filee.write(data)


    def basicRead(self, path, defaultData = ''):
        with open(path, 'r') as filee:
            return filee.read()

        return defaultData
