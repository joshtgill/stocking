from common.base_service import BaseService


class TradeService(BaseService):

    def __init__(self, dataInterface, logInterface, stockSymbolsInterface, stockHistoryInterface, fileInterface, processService):
        super().__init__('TRADE', dataInterface, logInterface, stockSymbolsInterface, stockHistoryInterface)
        self.fileInterface = fileInterface
        self.processService = processService


    def go(self):
        pass
