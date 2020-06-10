import json
import os
from common.stock import Stock
from datetime import datetime


class StockDataInterface:

    def __init__(self, fileInterface, interval):
        self.fileInterface = fileInterface
        self.interval = interval
        self.dataLocation = 'data/stock_data/{}/'.format(interval)
        self.dataFileNames = self.fileInterface.listLocation(self.dataLocation)


    def save(self, stock):
        historyStr = ''
        for historyEntry in stock.history:
            historyStr += '{}\n'.format(historyEntry)

        dataFileName = '{}_{}.txt'.format(stock.symbol, self.interval)
        self.dataFileNames.append(dataFileName)
        self.fileInterface.write(self.dataLocation + dataFileName, historyStr)


    def load(self, symbol, numLastLines=0):
        # Make date file name
        dataFileName = '{}_{}.txt'.format(symbol, self.interval)

        # Build stock history
        stockHistory = []
        if numLastLines == 0:
            for historyEntry in self.fileInterface.readLines(self.dataLocation + dataFileName)[: -1]:
                stockHistory.append(eval(historyEntry))
        else:
            for historyEntry in self.fileInterface.readLastLines(self.dataLocation + dataFileName, numLastLines):
                stockHistory.append(eval(historyEntry))

        return stockHistory
