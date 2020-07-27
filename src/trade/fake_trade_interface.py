from common.stock_data_interface import StockDataInterface


class FakeTradeInterface:

    def __init__(self, dataInterface, logService):
        self.dataInterface = dataInterface
        self.logService = logService
        self.stockDataInterface = StockDataInterface(self.dataInterface.settingsGet('1d/stockDataPath'))


    def buy(self, symbol, numShares):
        lastClosePrice = self.stockDataInterface.load(symbol, numLastRows=1)[0][4]

        numOwnedShares = 0
        if symbol in self.dataInterface.bank:
            numOwnedShares = self.dataInterface.bank.get(symbol)
        self.dataInterface.bank.update({symbol: numShares + numOwnedShares})
        self.dataInterface.bankSave()

        self.logService.log('Bought {} shares of {} at ${} a share'.format(numShares, symbol, lastClosePrice))
