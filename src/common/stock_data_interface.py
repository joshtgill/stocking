import json
import os
from common.stock import Stock
from datetime import datetime


class StockDataInterface:

    def __init__(self, fileInterface):
        self.fileInterface = fileInterface
        self.dataLocation = 'data/stock_data/'
        self.dataFiles = self.fileInterface.listLocation(self.dataLocation)


    def save(self, stock):
        historyDataStr = ''
        for historyItem in stock.history:
            historyDataStr += '{}\n'.format(historyItem)

        dataFile = '{}_{}.txt'.format(stock.symbol, stock.interval)
        self.dataFiles.append(dataFile)
        self.fileInterface.write(self.dataLocation + dataFile, historyDataStr)


    def load(self, symbol, interval, numLastLines=0):
        dataFile = '{}_{}.txt'.format(symbol, interval)
        stock = Stock(symbol, interval)
        if numLastLines == 0:
            for historyItem in self.fileInterface.readLines(self.dataLocation + dataFile)[: -1]:
                stock.history.append(eval(historyItem))
        else:
            for historyItem in self.fileInterface.readLastLines(self.dataLocation + dataFile, numLastLines):
                stock.history.append(eval(historyItem))

        return stock if stock.history else None


    def parseSymbolAndInterval(self, dataFile):
        splitDataFile = dataFile.split('_')
        symbol = splitDataFile[0]
        interval = splitDataFile[1][: splitDataFile[1].index('.txt')]

        return symbol, interval
