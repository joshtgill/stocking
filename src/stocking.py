from shared.data_service import DataService
from query.query_service import QueryService
from query.query_interface import QueryInterface
from datetime import datetime


class Stocking:

    def __init__(self, configFileName):
        self.dataService = DataService(configFileName)
        self.queryInterface = QueryInterface(self.dataService)
        self.queryService = QueryService(self.dataService, self.queryInterface)


    def start(self):
        start = datetime.now()
        self.queryService.performQueries()
        end = datetime.now()
        self.dataService.log('Completed in {}'.format(end - start), 'STAT')
