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

        passedStocks = self.inspect()
        for key, value in passedStocks.items():
            print(key, value)

        self.logService.untrack('DAY ANALYZE')


    def inspect(self):
        passedStocks = {}
        for symbol in self.symbols:
            increasePercent, decreasePercent = self.calculateIncreaseAndDecreasePercent(symbol)
            if increasePercent < self.dataInterface.configGet('minimumIncreasePercent'):
                continue

            averageGrowthPercent = self.calculateAverageGrowthPercent(symbol)
            if averageGrowthPercent < self.dataInterface.configGet('minimumAverageGrowthPercent'):
                continue

            # If here, accept the stock
            passedStocks.update({symbol: averageGrowthPercent})

        passedStocks = {k: v for k, v in sorted(passedStocks.items(), key=lambda item: item[1], reverse=True)}

        return passedStocks


    def calculateIncreaseAndDecreasePercent(self, symbol):
        self.stockDataInterface.load('1d', symbol, start=self.start, end=self.end)

        if not self.stockDataInterface.peek():
            return 0, 0

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
        self.stockDataInterface.load('1d', symbol, start=self.start, end=self.end)

        if not self.stockDataInterface.peek():
            return 0

        cumulativeGrowth = 0
        lastStockPrice = self.stockDataInterface.peek()[4]
        while self.stockDataInterface.next():
            stockPrice = self.stockDataInterface.peek()[4]

            cumulativeGrowth += ((stockPrice - lastStockPrice) / lastStockPrice) * 100

            lastStockPrice = stockPrice

        return round(cumulativeGrowth / (self.stockDataInterface.size() - 1), 2)


    def calculateScore(self, decreasePercent, averageGrowthPercent):
        return averageGrowthPercent / decreasePercent * 100
