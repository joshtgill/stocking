from common.file_interface import FileInterface
from common.config_interface import ConfigInterface
from common.stock_data_interface import StockDataInterface
from common.log_service import LogService
from query.query_service import QueryService
from learn.learn_service import LearnService


class Stocking:

    def __init__(self):
        self.fileInterface = FileInterface()
        self.stockDataInterface = StockDataInterface(self.fileInterface)


    def query(self, queryConfigFileName):
        configInterface = ConfigInterface(self.fileInterface)
        queryConfig = configInterface.loadQueryConfig(queryConfigFileName)
        queryService = QueryService(queryConfig, self.stockDataInterface)
        logService = LogService(self.fileInterface)

        logService.start()

        queryService.start()

        logService.stop()


    def learn(self):
        learnService = LearnService(self.stockDataInterface)

        learnService.start()
