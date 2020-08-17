from trade.trade_report import TradeReport


class TradeService:

    def __init__(self, dataInterface, logService, fileInterface, stockDataInterface, processService):
        self.dataInterface = dataInterface
        self.logService = logService
        self.fileInterface = fileInterface
        self.stockDataInterface = stockDataInterface
        self.processService = processService


    def go(self):
        self.logService.track('TRADE')

        date = self.dataInterface.configGet('date')
        module = self.dataInterface.configGet('module')

        if module == 'update':
            self.updatePorfolio(date)
        elif module == 'sell':
            self.updatePorfolio(date, True)

        self.logService.untrack('TRADE')


    def updatePorfolio(self, date, sellAll=False):
        grossPercentGrowth = 0
        grossProfit = 0

        existingSymbols = list(self.dataInterface.porfolioGet('stocks', {}).keys())
        passedSymbols = self.processService.passedSymbols if not sellAll else []

        # If an existing symbol in porfolio is no longer passing,
        # remove it from porfolio
        sellStockCount = 0
        cumulativePercentGrowth = 0
        grossProfit = 0
        for symbol in existingSymbols:
            if symbol not in passedSymbols:
                buyPrice, sellPrice = self.sellStock(symbol, date)
                if not buyPrice and not sellPrice:
                    self.logService.log('Failed to sell {}'.format(symbol))
                    continue

                grossProfit += sellPrice - buyPrice
                cumulativePercentGrowth += ((sellPrice - buyPrice) / buyPrice) * 100
                sellStockCount += 1

        if sellStockCount:
            grossPercentGrowth = cumulativePercentGrowth / sellStockCount
            print('Gross percent growth:', grossPercentGrowth)
            print('Gross profit:',  grossProfit)

        # Get symbols from updated porfolio
        existingSymbols = list(self.dataInterface.porfolioGet('stocks', {}).keys())

        # If a passed symbol is not an existing symbol in porfolio,
        # add it to porfolio
        for symbol in passedSymbols:
            if symbol not in existingSymbols:
                buyPrice = self.buyStock(symbol, date)


    def sellStock(self, symbol, date):
        self.stockDataInterface.load('1d', symbol, date)
        if not self.stockDataInterface.size():
            return 0, 0

        sellPrice = self.stockDataInterface.next()[4]

        buyPrice = self.dataInterface.porfolioSet('stocks/{}'.format(symbol), None)

        self.logService.log('Sold {} at ${}'.format(symbol, sellPrice))

        return round(buyPrice, 2), round(sellPrice, 2)


    def buyStock(self, symbol, date):
        self.stockDataInterface.load('1d', symbol, date)
        buyPrice = self.stockDataInterface.next()[4]

        self.dataInterface.porfolioSet('stocks/{}'.format(symbol), buyPrice)

        self.logService.log('Bought {} at ${}'.format(symbol, buyPrice))

        return round(buyPrice, 2)
