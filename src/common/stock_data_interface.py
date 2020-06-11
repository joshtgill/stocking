from common.data_interface import DataInterface
import json
import os
from common.stock import Stock
from datetime import datetime


class StockDataInterface(DataInterface):

    def __init__(self, fileInterface, interval):
        super().__init__('data/stocks_{}.db'.format(interval))

        self.header = '(timestamp, open, high, low, close)'


    def __del__(self):
        self.database.close()


    def save(self, stock):
        self.insert(stock.symbol, self.header, stock.history)


    def load(self, symbol, numLastEntries=0):
        return self.select(symbol, numLastEntries)
