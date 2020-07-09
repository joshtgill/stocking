import json
from trade.fake_trade_interface import FakeTradeInterface


class TradeService:

    def __init__(self, configInterface, logService, fileInterface):
        self.configInterface = configInterface
        self.logService = logService
        self.logService.register('TRADE')
        self.fileInterface = fileInterface
        self.trades = json.loads(self.fileInterface.read(self.configInterface.settingsGet('tradesPath')))


    def __del__(self):
        self.logService.unregister('TRADE')


    def go(self):
        print(self.trades)
