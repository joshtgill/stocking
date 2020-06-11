from common.file_interface import FileInterface
from common.config_interface import ConfigInterface
from common.stock_data_interface import StockDataInterface
from common.log_service import LogService
from query.query_service import QueryService
from process.analyze_service import AnalyzeService


class Stocking:

    def __init__(self):
        self.fileInterface = FileInterface()


    def query(self, configFilePath):
        configInterface = ConfigInterface(self.fileInterface)
        queryConfig = configInterface.load(configFilePath, 'query')
        stockDataInterface = StockDataInterface(self.fileInterface, queryConfig.get('interval'))
        queryService = QueryService(queryConfig, stockDataInterface)
        logService = LogService(self.fileInterface)

        logService.start()

        queryService.start()

        logService.stop()


    def analyze(self):
        pass
