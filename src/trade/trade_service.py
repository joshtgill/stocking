import json
from trade.fake_trade_interface import FakeTradeInterface


class TradeService:

    def __init__(self, dataInterface, logService, fileInterface, stockDataInterface):
        self.dataInterface = dataInterface
        self.logService = logService
        self.fileInterface = fileInterface
        self.tradeInterface = FakeTradeInterface(dataInterface, logService, stockDataInterface)
        self.stocksToTrade = []


    def go(self):
        self.logService.track('TRADE')

        self.buyStocks()

        self.logService.untrack('TRADE')


    def buyStocks(self):
        for symbol in self.stocksToTrade:
            self.tradeInterface.buy(symbol, 5)

        self.dataInterface.trades.update({'JOSH': 'GILLETTE'})
        self.dataInterface.tradesSave()