from common.base_service import BaseService
import json
import yfinance


class DisplayService(BaseService):

    def __init__(self, dataInterface, logInterface, stockSymbolsInterface, stockHistoryInterface):
        super().__init__('DISPLAY', dataInterface, logInterface, stockSymbolsInterface, stockHistoryInterface)


    def go(self):
        interval = self.dataInterface.configGet('interval')
        symbols = self.translateConfigVariable(self.dataInterface.configGet('symbols'))

        for symbol in symbols:
            self.displayStockHistory(interval, symbol)


    def displayStockHistory(self, interval, symbol):
        self.stockHistoryInterface.load(interval, symbol)

        while self.stockHistoryInterface.next():
            print(self.stockHistoryInterface.peek())
