import json
import os
from common.stock import Stock
from datetime import datetime


class StockDataInterface:

    def __init__(self, fileInterface):
        self.fileInterface = fileInterface
        self.dataLocation = 'data/stock_data/'
        self.dataFileNames = self.fileInterface.listLocation(self.dataLocation)


    def save(self, stock):
        stockHistoryStr = ''
        for stockHistoryItem in stock.history:
            stockHistoryStr += '{}\n'.format(stockHistoryItem)

        dataFileName = '{}_{}.txt'.format(stock.symbol, stock.interval)
        self.dataFileNames.append(dataFileName)
        self.fileInterface.write(self.dataLocation + dataFileName, stockHistoryStr)


    def load(self, dataFileName, numLastLines=0):
        # Extract symbol and interval from data file name
        splitDataFileName = dataFileName.split('_')
        symbol = splitDataFileName[0]
        interval = splitDataFileName[1][: splitDataFileName[1].index('.txt')]

        # Build stock data
        stock = Stock(symbol, interval)
        if numLastLines == 0:
            for historyItem in self.fileInterface.readLines(self.dataLocation + dataFileName)[: -1]:
                stock.history.append(eval(historyItem))
        else:
            for historyItem in self.fileInterface.readLastLines(self.dataLocation + dataFileName, numLastLines):
                stock.history.append(eval(historyItem))

        return stock if stock.history else None
