class TradeService:

    def __init__(self, dataInterface, logService, fileInterface, stockHistoryInterface, processService):
        self.dataInterface = dataInterface
        self.logService = logService
        self.fileInterface = fileInterface
        self.stockHistoryInterface = stockHistoryInterface
        self.processService = processService


    def go(self):
        self.logService.start('TRADE')

        self.logService.stop('TRADE')
