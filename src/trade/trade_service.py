from trade.trade_report import TradeReport


class TradeService:

    def __init__(self, dataInterface, logService, fileInterface, stockDataInterface):
        self.dataInterface = dataInterface
        self.logService = logService
        self.fileInterface = fileInterface
        self.stockDataInterface = stockDataInterface


    def buyStocks(self, symbols, date):
        self.dataInterface.trades = {}

        for symbol in symbols:
            self.stockDataInterface.load('1d', symbol, date)
            if not self.stockDataInterface.peek():
                continue
            closePrice = self.stockDataInterface.peek()[4]
            self.dataInterface.trades.update({symbol: closePrice})

        self.dataInterface.tradesSave()


    def go(self):
        self.logService.track('TRADE')

        tradeReport = self.sellStocks()

        self.fileInterface.wipe(self.dataInterface.settingsGet('tradeReportPath'))
        self.fileInterface.write(self.dataInterface.settingsGet('tradeReportPath'), tradeReport.serialize())
        self.logService.log('Trade report created')

        self.logService.untrack('TRADE')


    def sellStocks(self):
        date = self.dataInterface.configGet('date')

        averageGrowth = 0
        redCount = 0
        for symbol, boughtPrice in self.dataInterface.tradesGet().items():
            self.stockDataInterface.load('1d', symbol, date)

            sellPrice = self.stockDataInterface.peek()[4]
            averageGrowth += ((sellPrice - boughtPrice) / boughtPrice) * 100
            if sellPrice <= boughtPrice:
                redCount += 1


        return TradeReport(averageGrowth / len(self.dataInterface.trades),
                           redCount / len(self.dataInterface.trades) * 100)
