class TradeService:

    def __init__(self, dataInterface, logService, fileInterface, stockDataInterface, processService):
        self.dataInterface = dataInterface
        self.logService = logService
        self.fileInterface = fileInterface
        self.stockDataInterface = stockDataInterface
        self.processService = processService


    def go(self):
        self.logService.start('TRADE')

        self.logService.stop('TRADE')
