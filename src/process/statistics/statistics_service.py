class StatisticsService:

    def __init__(self, logService, stockDataInterface):
        self.logService = logService
        self.stockDataInterface = stockDataInterface


    def go(self):
        self.logService.track('STATISTICS')

        self.logService.untrack('STATISTICS')
