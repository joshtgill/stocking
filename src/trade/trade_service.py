from trade.trade_report import TradeReport


class TradeService:

    def __init__(self, dataInterface, logService, fileInterface, stockDataInterface, processService):
        self.dataInterface = dataInterface
        self.logService = logService
        self.fileInterface = fileInterface
        self.stockDataInterface = stockDataInterface
        self.processService = processService


    def buyStocks(self, date):
        self.dataInterface.porfolio = {}

        for symbol in self.processService.passedSymbols:
            self.stockDataInterface.load('1d', symbol, date)
            if not self.stockDataInterface.next():
                continue
            closePrice = self.stockDataInterface.peek()[4]
            self.dataInterface.porfolio.update({symbol: closePrice})

        self.dataInterface.porfolioSave()


    def go(self):
        self.logService.track('TRADE')

        date = self.dataInterface.configGet('date')
        if self.dataInterface.configGet('action') == 'buy':
            self.buyStocks(date)
        else:
            tradeReport = self.sellStocks()

            self.fileInterface.wipe(self.dataInterface.settingsGet('tradeReportPath'))
            self.fileInterface.write(self.dataInterface.settingsGet('tradeReportPath'), tradeReport.serialize())
            self.logService.log('Trade report created')

        self.logService.untrack('TRADE')


    def sellStocks(self):
        date = self.dataInterface.configGet('date')

        averageGrowth = 0
        redCount = 0
        for symbol, boughtPrice in self.dataInterface.porfolioGet().items():
            self.stockDataInterface.load('1d', symbol, date)
            if not self.stockDataInterface.next():
                continue
            sellPrice = self.stockDataInterface.peek()[4]
            averageGrowth += ((sellPrice - boughtPrice) / boughtPrice) * 100
            if sellPrice <= boughtPrice:
                redCount += 1


        return TradeReport(averageGrowth / len(self.dataInterface.porfolio),
                           redCount / len(self.dataInterface.porfolio) * 100)
