from common.base_service import BaseService


class DayAnalyzeService(BaseService):

    def __init__(self, dataInterface, logInterface, stockHistoryInterface):
        super().__init__('DAY ANALYZE', dataInterface, logInterface)
        self.stockHistoryInterface = stockHistoryInterface


    def go(self, symbols, start, end):
        pass
