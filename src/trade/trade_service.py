import json
from trade.fake_trade_interface import FakeTradeInterface


class TradeService:

    def __init__(self, dataInterface, logService, fileInterface):
        self.dataInterface = dataInterface
        self.logService = logService
        self.fileInterface = fileInterface


    def go(self):
        self.logService.track('TRADE')

        self.logService.untrack('TRADE')

