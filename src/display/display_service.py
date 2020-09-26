from common.base_service import BaseService
import json
import yfinance


class DisplayService(BaseService):

    def __init__(self, dataInterface, logService, stockSymbolsInterface, stockHistoryInterface):
        super().__init__('DISPLAY', dataInterface, logService)
        self.stockSymbolsInterface = stockSymbolsInterface
        self.stockHistoryInterface = stockHistoryInterface


    def go(self):
        interval = self.dataInterface.configGet('interval')
        symbols = self.dataInterface.configGet('symbols')

        for symbol in self.stockSymbolsInterface.load(self.dataInterface.configGet('marketType')):
            if (symbols and symbol in symbols) or not symbols:
                self.displayStockHistory(interval, symbol)


    def displayStockHistory(self, interval, symbol):
        self.stockHistoryInterface.load(interval, symbol)

        while self.stockHistoryInterface.next():
            print(self.stockHistoryInterface.peek())
