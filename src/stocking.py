from shared.data_interface import DataInterface
from query.query_service import QueryService
from query.query_interface import QueryInterface
from trade.trade_service import TradeService
from datetime import datetime


class Stocking:

    def __init__(self, mainConfigFileName):
        self.dataInterface = DataInterface(mainConfigFileName)
        self.queryInterface = QueryInterface(self.dataInterface)
        self.queryService = QueryService(self.dataInterface, self.queryInterface)
        self.tradeService = None


    def start(self):
        start = datetime.now()
        self.queryService.performQueries()
        end = datetime.now()
        self.dataInterface.log('Completed in {}'.format(end - start), 'STAT')

        self.tradeService = TradeService(self.dataInterface)
        self.tradeService.simulateTrading()
