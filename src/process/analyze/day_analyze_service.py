class DayAnalyzeService:

    def __init__(self, dataInterface, logService, stockDataInterface):
        self.dataInterface = dataInterface
        self.logService = logService
        self.stockDataInterface = stockDataInterface


    def go(self, symbols, start, end):
        self.logService.start('DAY ANALYZE')

        self.logService.stop('DAY ANALYZE')
