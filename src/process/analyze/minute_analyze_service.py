import statistics


class MinuteAnalyzeService:

    def __init__(self, dataInterface, logService, stockDataInterface, symbols, start, end):
        self.dataInterface = dataInterface
        self.logService = logService
        self.stockDataInterface = stockDataInterface
        self.symbols = symbols
        self.start = start
        self.end = end


    def go(self):
        self.logService.track('MINUTE ANALYZE')

        for symbol in self.symbols:
            approved = self.vetStock(symbol)
            break

        self.logService.untrack('MINUTE ANALYZE')


    def vetStock(self, symbol):
        self.stockDataInterface.load('1m', symbol, start=self.start, end=self.end)

        minuteDataItem = self.stockDataInterface.peek()
        while minuteDataItem:
            print(minuteDataItem)

            minuteDataItem = self.stockDataInterface.next()

        return True
