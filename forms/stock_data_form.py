class StockDataForm:

    def __init__(self, symbol, start, end, interval):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.interval = interval
        self.data = [[], [], [], [], []]
