from common.stock_data_interface import StockDataInterface
import statistics


class MacroAnalyzeService:

    def __init__(self, configInterface, logService, symbols, start, end):
        self.configInterface = configInterface
        self.logService = logService
        self.symbols = symbols
        self.start = start
        self.end = end
        self.stockDataInterface = StockDataInterface(self.configInterface.settingsGet('1d/stockDataPath'))


    def __del__(self):
        self.logService.unregister('MACRO ANALYZE')


    def go(self):
        self.logService.register('MACRO ANALYZE')

        averageGrowthDir = {}
        for symbol in self.symbols:
            averageGrowth = self.calculateAverageGrowth(symbol)
            averageGrowthDir.update({symbol: averageGrowth})

        averageGrowthDir = {k: v for k, v in sorted(averageGrowthDir.items(), key=lambda item: item[1], reverse=True)}
        # for key, value in averageGrowthDir.items():
        #    print(key, value)


    def calculateAverageGrowth(self, symbol):
        stockHistory = self.stockDataInterface.load(symbol, self.start, self.end)

        if not stockHistory:
            return 0

        cumulativeGrowth = 0
        lastStockPrice = stockHistory[0][4]
        i = 1
        while i < len(stockHistory):
            currentStockPrice = stockHistory[i][4]

            percentIncrease = ((currentStockPrice - lastStockPrice) / lastStockPrice) * 100

            cumulativeGrowth += percentIncrease

            lastStockPrice = currentStockPrice

            i += 1

        return cumulativeGrowth / (len(stockHistory) - 1)
