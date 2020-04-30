from interfaces.config_interface import ConfigInterface
from interfaces.query_interface import QueryInterface
from services.query_service import QueryService
from interfaces.stock_data_interface import StockDataInterface


class Stocking:

    def __init__(self, configFileName):
        self.configInterface = ConfigInterface(configFileName)
        self.queryInterface = QueryInterface(self.configInterface)


    def start(self):
        # QueryService(self.configInterface, self.queryInterface).start()
        StockDataInterface(self.configInterface, 'TSLA')
