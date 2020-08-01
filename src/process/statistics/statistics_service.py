class StatisticsService:

    def __init__(self, logService, stockDataInterface, symbols, start, end):
        self.logService = logService
        self.stockDataInterface = stockDataInterface
        self.symbols = symbols
        self.start = start
        self.end = end


    def go(self):
        self.logService.track('STATISTICS')

        for symbol in self.symbols:
            self.observeDayGrowthSpike(symbol)

        self.logService.untrack('STATISTICS')


    def observeDayGrowthSpike(self, symbol):
        self.stockDataInterface.load('1d', symbol, self.start, self.end)

        if not self.stockDataInterface.peek():
            return 0

        spikeFound = False
        lastStockPrice = self.stockDataInterface.peek()[4]
        while self.stockDataInterface.next():
            stockPrice = self.stockDataInterface.peek()[4]

            percentGrowth = ((stockPrice - lastStockPrice) / lastStockPrice) * 100
            if spikeFound:
                print(percentGrowth)
                spikeFound = False
            else:
                if percentGrowth > 40:
                    spikeFound = True

            lastStockPrice = stockPrice
