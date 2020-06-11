from common.file_interface import FileInterface
from common.config_interface import ConfigInterface
from common.stock_data_interface import StockDataInterface
from common.log_service import LogService
from query.query_service import QueryService
from process.analyze_service import AnalyzeService


class Stocking:

    def __init__(self, configPath):
        self.fileInterface = FileInterface()
        configInterface = ConfigInterface(self.fileInterface)
        self.config = configInterface.load(configPath)
        self.logService = LogService(self.fileInterface)


    def query(self):
        self.logService.start()
        for queryConfig in self.config.get('queries'):
            self.logService.log('Starting {} query'.format(queryConfig.get('interval')))

            stockDataInterface = StockDataInterface(self.fileInterface, queryConfig.get('interval'))
            queryService = QueryService(queryConfig, stockDataInterface)
            queryService.start()

        self.logService.stop()


    def analyze(self):
        pass
