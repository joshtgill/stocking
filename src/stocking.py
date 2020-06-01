from common.file_service import FileService
from common.config_interface import ConfigInterface
from common.stock_data_interface import StockDataInterface
from common.log_service import LogService
from query.query_service import QueryService
from learn.learn_service import LearnService


class Stocking:

    def __init__(self):
        self.fileService = FileService()
        self.stockDataInterface = StockDataInterface(self.fileService)


    def query(self, mainConfigFileName):
        queryConfigInterface = ConfigInterface(mainConfigFileName, self.fileService)
        queryService = QueryService(queryConfigInterface.queryConfig, self.stockDataInterface)
        logService = LogService(self.fileService)

        logService.signalStart()

        queryService.initiateQueries()

        logService.signalEnd()


    def learn(self):
        learnService = LearnService(self.stockDataInterface)

        learnService.analyzeData()
