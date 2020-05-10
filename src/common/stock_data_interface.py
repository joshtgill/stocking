import json
import os
from common.stock import Stock
from datetime import datetime


class StockDataInterface:

    def __init__(self):
        self.stockDataTitles = self.loadTitles()  # A stock title is of the format SYMBOL_INTERVAL


    def loadTitles(self):
        titles = []
        for fileName in os.listdir('{}/'.format('data/stock_data')):
            titles.append(fileName[: fileName.index('.txt')])

        return titles


    def save(self, stock):
        dataStr = ''
        for history in stock.history:
            dataStr += str(history) + '\n'

        fileTitle = '{}_{}'.format(stock.symbol, stock.interval)
        if fileTitle not in self.stockDataTitles:
            self.stockDataTitles.append(fileTitle)

        filePath = 'data/stock_data/{}.txt'.format(fileTitle)
        with open(filePath, 'a+') as stockDataFile:
            stockDataFile.write(dataStr)


    def load(self, symbol, interval):
        stockDataTitle = symbol + '_' + interval
        if stockDataTitle in self.stockDataTitles:
            stock = Stock(symbol, interval)
            with open('data/stock_data/{}.txt'.format(stockDataTitle), 'r') as filee:
                for historyItem in filee.readlines()[: -1]:
                    stock.history.append(eval(historyItem))

            return stock

        return None


    def loadDataEnd(self, symbol, interval):
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
