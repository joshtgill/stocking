class DisplayService:

    def __init__(self, dataInterface, logService, stockDataInterface):
        self.dataInterface = dataInterface
        self.logService = logService
        self.stockDataInterface = stockDataInterface


    def go(self):
        self.logService.track('DISPLAY')

        interval = self.dataInterface.configGet('interval')
        symbols = self.dataInterface.configGet('symbols')
        for symbol in symbols:
            self.displayStockData(symbol, interval)
            print()

        self.logService.untrack('DISPLAY')


    def displayStockData(self, symbol, interval):
        self.stockDataInterface.load(interval, symbol)

        print(self.stockDataInterface.peek())
        while self.stockDataInterface.next():
            print(self.stockDataInterface.peek())
