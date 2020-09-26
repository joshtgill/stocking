from common.base_service import BaseService
import json
import yfinance


class DisplayService(BaseService):

    def __init__(self, dataInterface, logService, stockHistoryInterface):
        super().__init__('DISPLAY', dataInterface, logService)
        self.stockHistoryInterface = stockHistoryInterface


    def go(self):
        pass


    def displayStockHistory(self, symbol, interval):
        self.stockHistoryInterface.load(interval, symbol)

        while self.stockHistoryInterface.next():
            print(self.stockHistoryInterface.peek())
