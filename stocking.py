from services.data_service import DataService
from services.query_service import QueryService
from interfaces.query_interface import QueryInterface


class Stocking:

    def __init__(self, configFileName):
        self.dataService = DataService(configFileName)
        self.queryInterface = QueryInterface(self.dataService)
        self.queryService = QueryService(self.dataService, self.queryInterface)

    def start(self):
        self.queryService.initiateQueries()
