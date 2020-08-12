import statistics


class MinuteAnalyzeService:

    def __init__(self, dataInterface, logService, stockDataInterface):
        self.dataInterface = dataInterface
        self.logService = logService
        self.stockDataInterface = stockDataInterface


    def go(self, symbols, start, end):
        self.logService.track('MINUTE ANALYZE')

        self.logService.untrack('MINUTE ANALYZE')
