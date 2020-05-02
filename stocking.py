from services.data_service import DataService
from services.query_service import QueryService
from interfaces.query_interface import QueryInterface


class Stocking:

    def __init__(self, configFileName):
        self.dataService = DataService()
        self.queryInterface = QueryInterface(self.dataService)

        self.dataService.loadConfig(configFileName)


    def start(self):
        QueryService(self.dataService, self.queryInterface).initiateQueries()
