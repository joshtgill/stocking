from interfaces.config_interface import ConfigInterface
from services.file_service import FileService
from services.query_service import QueryService


class Stocking:

    def __init__(self, configFileName):
        self.fileService = FileService()
        self.configInterface = ConfigInterface(self.fileService, configFileName)


    def start(self):
        QueryService(self.configInterface, self.fileService).initiateQueries()
