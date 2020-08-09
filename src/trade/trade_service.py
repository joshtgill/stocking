class TradeService:

    def __init__(self, dataInterface, logService, fileInterface, stockDataInterface):
        self.dataInterface = dataInterface
        self.logService = logService
        self.fileInterface = fileInterface
        self.stocksToTrade = []


    def go(self):
        self.logService.track('TRADE')

        self.logService.untrack('TRADE')
