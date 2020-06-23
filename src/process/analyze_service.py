from common.stock_data_interface import StockDataInterface


class AnalyzeService:

    def __init__(self, interval, symbols):
        self.stockDataInterface = StockDataInterface(interval)
        self.symbols = symbols


    def start(self):
        print('goz')
