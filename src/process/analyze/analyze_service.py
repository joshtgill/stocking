from common.stock_data_interface import StockDataInterface


class AnalyzeService:

    def __init__(self, interval, symbols, start, end):
        self.stockDataInterface = StockDataInterface(interval)
        self.symbols = symbols
        self.start = start
        self.end = end


    def go(self):
        for symbol in self.symbols:
            print(self.stockDataInterface.load(symbol, self.start, self.end))