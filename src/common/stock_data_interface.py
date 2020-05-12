import json
import os
from common.stock import Stock
from datetime import datetime


class StockDataInterface:

    def __init__(self, fileService):
        self.fileService = fileService
        self.dataLocation = 'data/stock_data/'
        self.dataFileNames = self.fileService.listDirectory(self.dataLocation)


    def save(self, stock):
        historyStr = ''
        for historyItem in stock.history:
            historyStr += '{}\n'.format(str(historyItem))

        fileName = '{}_{}.txt'.format(stock.symbol, stock.interval)
        if fileName not in self.dataFileNames:
            self.dataFileNames.append(fileName)

        self.fileService.write(self.dataLocation + fileName, historyStr)


    def load(self, symbol, interval, onlyLastItem=False):
        stockDataTitle = symbol + '_' + interval
        if stockDataTitle in self.stockDataTitles:
            stock = Stock(symbol, interval)
            filePath = self.dataLocation + stockDataTitle
            if onlyLastItem:
                stock.history.append(eval(self.fileService.readLastLine(filePath)))
            else:
                for historyItem in self.fileService.readlines(filePath)[: -1]:
                    stock.history.append(eval(historyItem))

            return stock

        return None
