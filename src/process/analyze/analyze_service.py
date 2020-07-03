from common.stock_data_interface import StockDataInterface
from datetime import datetime, timedelta
import re


class AnalyzeService:

    def __init__(self, interval, symbols, start, end):
        self.stockDataInterface = StockDataInterface(interval)
        self.symbols = symbols
        self.start = self.translateVariable(start)
        self.end = self.translateVariable(end)


    def translateVariable(self, variable):
        if variable == 'NOW':
            return datetime.now().strftime('%Y-%m-%d')
        elif 'NOW' in variable:
            entriesBack = int(re.sub(r'\s+', '', variable.replace('NOW', '').replace('-', '')))
            return (datetime.now().date() - timedelta(days=entriesBack)).strftime('%Y-%m-%d')
        else:
            return variable


    def go(self):
        for symbol in self.symbols:
            print(self.stockDataInterface.load(symbol, self.start, self.end))
