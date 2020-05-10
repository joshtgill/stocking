from common.stock_data_interface import StockDataInterface
from query.query_service import QueryService
from query.query_interface import QueryInterface
from trade.trade_service import TradeService
from datetime import datetime


class Stocking:

    def __init__(self, mainConfigFileName):
        self.stockDataInterface = StockDataInterface(mainConfigFileName)
        self.queryInterface = QueryInterface(self.stockDataInterface)
        self.queryService = QueryService(self.stockDataInterface, self.queryInterface)
        self.tradeService = None


    def start(self):
        start = datetime.now()
        self.queryService.performQueries()
        end = datetime.now()
        self.stockDataInterface.log('Completed in {}'.format(end - start), 'STAT')
