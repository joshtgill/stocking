import json
import os
from shared.stock import Stock
from datetime import datetime


class DataInterface:

    def __init__(self, mainConfigFilePath):
        self.config = json.loads(self.basicRead(mainConfigFilePath))
        self.queryConfig = self.loadQueryConfig(self.config.get('queryConfigPath'))
        self.tradeConfig = json.loads(self.basicRead(self.config.get('tradeConfigPath'), {}))

        self.logFilePath = 'log/{}.log'.format(datetime.strftime(datetime.now(), '%Y%m%d%H%M%S'))
        self.stockDataTitles = self.loadStockDataTitles()  # A stock title is of the format SYMBOL_INTERVAL


    def loadQueryConfig(self, configFilePath):
        config = json.loads(self.basicRead(configFilePath, {}))

        # Load any config vars
        configVarMap = {'ALL_SYMBOLS': 'data/symbols/all_symbols.json'}

        for interval, intervalData in config.get('queries').items():
            symbols = intervalData.get('symbols')
            if not isinstance(symbols, list):
                if symbols in configVarMap.keys():  # Symbols value is config var
                    symbolsData = json.loads(self.basicRead(configVarMap.get(intervalSymbols), []))
                else:  # Symbols value is a single symbol
                    symbolsData = [symbols]
                intervalData.update({'symbols': symbolsData})

        return config


    def loadStockDataTitles(self):
        titles = []
        for fileName in os.listdir('{}/'.format('data/stock_data')):
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
            lastLines = []
            with open('data/stock_data/{}.txt'.format(title), 'rb') as filee:
                filee.seek(-500, 2)
                lastLines = filee.readlines()

            del lastLines[0]  # First item is likely cut off
            lastGoodLine = []
            for line in lastLines:
                try:
                    lastGoodLine = eval(line.decode())
                    break
                except NameError:
                    self.log('NAN value for ' + symbol, 'WARNING')
                    continue
            return datetime.strptime(lastGoodLine[0], '%Y-%m-%d %H:%M:%S')

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
        self.basicWrite(self.logFilePath, logStr)


    def basicWrite(self, path, data):
        with open(path, 'a+') as filee:
            filee.write(data)


    def basicRead(self, path, defaultData = ''):
        with open(path, 'r') as filee:
            return filee.read()

        return defaultData
