class DayAnalyzeService:

    def __init__(self, dataInterface, logService, stockDataInterface, symbols, start, end):
        self.dataInterface = dataInterface
        self.logService = logService
        self.stockDataInterface = stockDataInterface
        self.symbols = symbols
        self.start = start
        self.end = end


    def go(self):
        self.logService.track('DAY ANALYZE')

        passedStocksDirectory = self.inspect()

        self.logService.untrack('DAY ANALYZE')

        return passedStocksDirectory.keys()


    def inspect(self):
        passedStocksDirectory = {}
        for symbol in self.symbols:
            # Check that stock history exists
            self.stockDataInterface.load('1d', symbol, start=self.start, end=self.end)
            if self.stockDataInterface.size() < 2:
                continue

            increasePercent, decreasePercent = self.calculateIncreaseAndDecreasePercent(symbol)
            if increasePercent < self.dataInterface.configGet('minimumIncreasePercent'):
                continue

            averageGrowthPercent = self.calculateAverageGrowthPercent(symbol)
            if averageGrowthPercent < self.dataInterface.configGet('minimumAverageGrowthPercent'):
                continue

            # If here, accept the stock
            passedStocksDirectory.update({symbol: averageGrowthPercent})

        passedStocksDirectory = {k: v for k, v in sorted(passedStocksDirectory.items(), key=lambda item: item[1], reverse=True)}

        return passedStocksDirectory


    def calculateIncreaseAndDecreasePercent(self, symbol):
        self.stockDataInterface.reset()

        numIncreases = 0
        numDecreases = 0
        lastStockPrice = self.stockDataInterface.peek()[4]
        i = 1
        while self.stockDataInterface.next():
            stockPrice = self.stockDataInterface.peek()[4]

            if stockPrice > lastStockPrice:
                numIncreases += 1
            elif stockPrice < lastStockPrice:
                numDecreases += 1

            lastStockPrice = stockPrice
            i += 1

        return (round(numIncreases / (self.stockDataInterface.size() - 1) * 100, 2),
                round(numDecreases / (self.stockDataInterface.size() - 1) * 100, 2))


    def calculateAverageGrowthPercent(self, symbol):
        self.stockDataInterface.reset()

        cumulativeGrowth = 0
        lastStockPrice = self.stockDataInterface.peek()[4]
        while self.stockDataInterface.next():
            stockPrice = self.stockDataInterface.peek()[4]

            cumulativeGrowth += ((stockPrice - lastStockPrice) / lastStockPrice) * 100

            lastStockPrice = stockPrice

        return round(cumulativeGrowth / (self.stockDataInterface.size() - 1), 2)


    def calculateScore(self, decreasePercent, averageGrowthPercent):
        return averageGrowthPercent / decreasePercent * 100
