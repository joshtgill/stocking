from common.base_service import BaseService


class DayAnalyzeService(BaseService):

    def __init__(self, dataInterface, logInterface, stockSymbolsInterface, stockHistoryInterface):
        super().__init__('DAY ANALYZE', dataInterface, logInterface, stockSymbolsInterface, stockHistoryInterface)


    def go(self, symbols, start, end):
        pass
