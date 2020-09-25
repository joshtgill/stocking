import json
import yfinance


class DisplayService:

    def __init__(self, dataInterface, logService, stockHistoryInterface):
        self.dataInterface = dataInterface
        self.logService = logService
        self.stockHistoryInterface = stockHistoryInterface


    def go(self):
        self.logService.start('DISPLAY')

        symbols = self.dataInterface.configGet('symbols')
        interval = self.dataInterface.configGet('interval')

        for symbol in symbols:
            self.displayStockHistory(symbol, interval)
            print()

        self.logService.stop('DISPLAY')


    def displayStockHistory(self, symbol, interval):
        self.stockHistoryInterface.load(interval, symbol)

        while self.stockHistoryInterface.next():
            print(self.stockHistoryInterface.peek())
