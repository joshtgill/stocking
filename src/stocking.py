from common.file_interface import FileInterface
from common.config_interface import ConfigInterface
from common.stock_data_interface import StockDataInterface
from common.log_service import LogService
from query.query_service import QueryService
from process.analyze_service import AnalyzeService


class Stocking:

    def __init__(self):
        self.fileInterface = FileInterface()
        self.dayStockDataInterface = StockDataInterface(self.fileInterface, '1d')
        self.minuteStockDataInterface = StockDataInterface(self.fileInterface, '1m')


    def query(self, configFilePath):
        configInterface = ConfigInterface(self.fileInterface)
        queryConfig = configInterface.load(configFilePath, 'query')
        queryService = QueryService(queryConfig, self.minuteStockDataInterface)
        logService = LogService(self.fileInterface)

        logService.start()

        queryService.start()

        logService.stop()


    def analyze(self):
        analyzeService = AnalyzeService(self.dayStockDataInterface, self.fileInterface)

        analyzeService.start()
