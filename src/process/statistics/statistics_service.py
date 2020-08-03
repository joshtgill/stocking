class StatisticsService:

    def __init__(self, logService, stockDataInterface, symbols, start, end):
        self.logService = logService
        self.stockDataInterface = stockDataInterface
        self.symbols = symbols
        self.start = start
        self.end = end


    def go(self):
        self.logService.track('STATISTICS')

        self.logService.untrack('STATISTICS')
