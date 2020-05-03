class StockData:

    def __init__(self, symbol, interval, start = None, end = None):
        self.symbol = symbol
        self.interval = interval
        self.start = start
        self.end = end
        self.history = []  # [timestamp, open, high, low, close]
