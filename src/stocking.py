from common.file_service import FileService
from common.config_interface import ConfigInterface
from common.stock_data_interface import StockDataInterface
from common.log_service import LogService
from query.query_service import QueryService
from trade.trade_service import TradeService
from datetime import datetime


class Stocking:

    def __init__(self, mainConfigFileName):
        self.fileService = FileService()
        self.configInterface = ConfigInterface(mainConfigFileName, self.fileService)
        self.stockDataInterface = StockDataInterface(self.fileService)
        self.logService = LogService(self.fileService)
        self.queryService = QueryService(self.configInterface.queryConfig, self.stockDataInterface, self.logService)
        self.tradeService = None


    def start(self):
        self.logService.signalStart()
        self.queryService.performQueries()
        self.logService.signalEnd()
