from shared.data_interface import DataInterface
from query.query_service import QueryService
from query.query_interface import QueryInterface
from datetime import datetime


class Stocking:

    def __init__(self, configFileName):
        self.dataInterface = DataInterface(configFileName)
        self.queryInterface = QueryInterface(self.dataInterface)
        self.queryService = QueryService(self.dataInterface, self.queryInterface)


    def start(self):
        start = datetime.now()
        self.queryService.performQueries()
        end = datetime.now()
        self.dataInterface.log('Completed in {}'.format(end - start), 'STAT')
