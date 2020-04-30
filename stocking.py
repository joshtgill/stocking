from services.config_service import ConfigService
from services.query_service import QueryService


class Stocking:

    def __init__(self, configFileName):
        self.config = ConfigService(configFileName)


    def start(self):
        QueryService(self.config).start()
