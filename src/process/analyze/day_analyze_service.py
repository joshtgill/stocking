from common.stock_data_interface import StockDataInterface
import statistics


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

        passedStockDir = self.determinePassedStocks()

        recommendedStocks = self.selectRecommendedStocks(passedStockDir)

        self.logService.untrack('DAY ANALYZE')

        return recommendedStocks


    def determinePassedStocks(self):
        growthDir = {}
        for symbol in self.symbols:
            increasePercent, decreasePercent = self.calculateIncreaseAndDecreasePercent(symbol)
            if increasePercent < self.dataInterface.configGet('minimumIncreasePercent'):
                continue

            averageGrowthPercent = self.calculateAverageGrowthPercent(symbol)
            if averageGrowthPercent < self.dataInterface.configGet('minimumAverageGrowthPercent'):
                continue

            score = self.calculateScore(decreasePercent, averageGrowthPercent)
            growthDir.update({symbol: (increasePercent, decreasePercent, averageGrowthPercent, score)})

        growthDir = {k: v for k, v in sorted(growthDir.items(), key=lambda item: item[1][3], reverse=True)}

        return growthDir


    def selectRecommendedStocks(self, passedStockDir):
        return list(passedStockDir.keys())[: 3]


    def calculateIncreaseAndDecreasePercent(self, symbol):
        stockHistory = self.stockDataInterface.load('1d', symbol, self.start, self.end)

        if not stockHistory:
            return 0, 0

        numIncreases = 0
        numDecreases = 0
        lastStockPrice = stockHistory[0][4]
        i = 1
        while i < len(stockHistory):
            stockPrice = stockHistory[i][4]

            if stockPrice > lastStockPrice:
                numIncreases += 1
            elif stockPrice < lastStockPrice:
                numDecreases += 1

            lastStockPrice = stockPrice

            i += 1

        return round(numIncreases / (i - 1) * 100, 2), round(numDecreases / (i - 1) * 100, 2)


    def calculateAverageGrowthPercent(self, symbol):
        stockHistory = self.stockDataInterface.load('1d', symbol, self.start, self.end)

        if not stockHistory:
            return 0

        cumulativeGrowth = 0
        lastStockPrice = stockHistory[0][4]
        i = 1
        while i < len(stockHistory):
            stockPrice = stockHistory[i][4]

            cumulativeGrowth += ((stockPrice - lastStockPrice) / lastStockPrice) * 100

            lastStockPrice = stockPrice

            i += 1

        return round(cumulativeGrowth / (i - 1), 2)


    def calculateScore(self, decreasePercent, averageGrowthPercent):
        return averageGrowthPercent / decreasePercent * 100
