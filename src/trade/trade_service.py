from common.base_service import BaseService


class TradeService(BaseService):

    def __init__(self, dataInterface, logInterface, fileInterface, stockHistoryInterface, processService):
        super().__init__('TRADE', dataInterface, logInterface)
        self.fileInterface = fileInterface
        self.stockHistoryInterface = stockHistoryInterface
        self.processService = processService


    def go(self):
        pass
