from common.base_service import BaseService


class TradeService(BaseService):

    def __init__(self, dataInterface, logService, fileInterface, stockHistoryInterface, processService):
        super().__init__('TRADE', dataInterface, logService)
        self.fileInterface = fileInterface
        self.stockHistoryInterface = stockHistoryInterface
        self.processService = processService


    def go(self):
        pass
