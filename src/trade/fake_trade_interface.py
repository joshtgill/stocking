class FakeTradeInterface:

    def __init__(self, dataInterface, logService, stockDataInterface):
        self.dataInterface = dataInterface
        self.logService = logService
        self.stockDataInterface = stockDataInterface


    def buy(self, symbol, numShares):
        lastClosePrice = self.stockDataInterface.load('1d', symbol, numLastRows=1)[0][4]

        numOwnedShares = 0
        if symbol in self.dataInterface.bank:
            numOwnedShares = self.dataInterface.bank.get(symbol)
        self.dataInterface.bank.update({symbol: numShares + numOwnedShares})
        self.dataInterface.bankSave()

        self.logService.log('Bought {} shares of {} at ${} a share'.format(numShares, symbol, lastClosePrice))
