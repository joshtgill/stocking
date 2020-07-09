from common.stock_data_interface import StockDataInterface


class MicroAnalyzeService():

    def __init__(self, configInterface, logService, symbols, start, end):
        self.configInterface = configInterface
        self.logService = logService
        self.logService.register('MICRO ANALYZE')
        self.symbols = symbols
        self.start = start
        self.end = end
        self.stockDataInterface = StockDataInterface(self.configInterface.settingsGet('1m/stockDataPath'))


    def __del__(self):
        self.logService.unregister('MICRO ANALYZE')


    def go(self):
        for symbol in self.symbols:
            self.findGrowth(symbol, 30, 1, 3)


    def findGrowth(self, symbol, steps, minimumPercentIncrease, maximumPercentIncrease):
        stockHistory = self.stockDataInterface.load(symbol, self.start, self.end)

        startStockPrice = stockHistory[0][1]
        i = steps
        while i < len(stockHistory):
            stockPrice = stockHistory[i][1]

            percentIncrease = ((stockPrice - startStockPrice) / startStockPrice) * 100

            i += steps
