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
        self.logService.start('STOCKING')

        # Start services based on config
        try:
            if 'queries' in self.config:
                pass
                self.query()
        except Exception as e:
            self.logService.log('STOCKING', traceback.format_exc(), 'ERROR')

        self.logService.stop('STOCKING')


    def query(self):
        for queryConfig in self.config.get('queries'):
            self.logService.start('QUERY {}'.format(queryConfig.get('interval')))

            stockDataInterface = StockDataInterface(queryConfig.get('interval'))
            queryService = QueryService(queryConfig, stockDataInterface)
            queryService.start()

            self.logService.stop('QUERY {}'.format(queryConfig.get('interval')))


    def analyze(self):
        pass
