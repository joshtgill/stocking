import json
import yfinance


class DisplayService:

    def __init__(self, dataInterface, logService, stockDataInterface):
        self.dataInterface = dataInterface
        self.logService = logService
        self.stockDataInterface = stockDataInterface


    def go(self):
        self.logService.start('DISPLAY')

        symbols = self.dataInterface.configGet('symbols')
        interval = self.dataInterface.configGet('interval')

        for symbol in symbols:
            self.displayStockData(symbol, interval)
            print()

        self.logService.stop('DISPLAY')


    def displayStockData(self, symbol, interval):
        self.stockDataInterface.load(interval, symbol)

        while self.stockDataInterface.next():
            print(self.stockDataInterface.peek())
