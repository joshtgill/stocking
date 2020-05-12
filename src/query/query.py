class Query:

    def __init__(self, symbol, interval, period):
        self.symbol = symbol
        self.interval = interval
        self.period = period
        self.start = None
        self.end = None
