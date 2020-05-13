import json
import os
from common.stock import Stock
from datetime import datetime


class StockDataInterface:

    def __init__(self, fileService):
        self.fileService = fileService
        self.dataLocation = 'data/stock_data/'
        self.dataFiles = self.fileService.listLocation(self.dataLocation)


    def save(self, stock):
        historyDataStr = ''
        for historyItem in stock.history:
            historyDataStr += '{}\n'.format(historyItem)

        dataFile = '{}_{}.txt'.format(stock.symbol, stock.interval)
        self.dataFiles.append(dataFile)
        self.fileService.write(self.dataLocation + dataFile, historyDataStr)


    def load(self, symbol, interval):
        dataFile = '{}_{}.txt'.format(symbol, interval)
        if dataFile in self.dataFiles:
            stock = Stock(symbol, interval)
            for historyItem in self.fileService.readLines(self.dataLocation + dataFile)[: -1]:
                stock.history.append(eval(historyItem))

            return stock

        return None
