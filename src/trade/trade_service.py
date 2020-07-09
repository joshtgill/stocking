import json
from trade.fake_trade_interface import FakeTradeInterface


class TradeService:

    def __init__(self, configInterface, logService, fileInterface):
        self.configInterface = configInterface
        self.logService = logService
        self.fileInterface = fileInterface


    def __del__(self):
        self.logService.unregister('TRADE')


    def go(self):
        self.logService.register('TRADE')

        print('Josh is the name, trade is the game')
