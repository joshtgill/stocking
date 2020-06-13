from common.file_interface import FileInterface
from common.config_interface import ConfigInterface
from common.stock_data_interface import StockDataInterface
from common.log_service import LogService
from query.query_service import QueryService
from process.analyze_service import AnalyzeService
import traceback

class Stocking:

    def __init__(self, configPath):
        self.fileInterface = FileInterface()
        self.config = ConfigInterface(self.fileInterface).load(configPath)
        self.logService = LogService(self.fileInterface)


    def startServices(self):
        self.logService.start()

        # Start services based on config
        try:
            if 'queries' in self.config:
                self.query()
        except Exception as e:
            tb = traceback.format_exc()
            print(tb)

        self.logService.stop()


    def query(self):
        for queryConfig in self.config.get('queries'):
            self.logService.log('Starting {} query'.format(queryConfig.get('interval')))

            stockDataInterface = StockDataInterface(queryConfig.get('interval'))
            queryService = QueryService(queryConfig, stockDataInterface)
            queryService.start()


    def analyze(self):
        pass
