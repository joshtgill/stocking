import datetime
import json


class AnalyzeService:

    def __init__(self, config, stockDataInterface, fileInterface):
        self.config = config
        self.stockDataInterface = stockDataInterface
        self.fileInterface = fileInterface


    def start(self):
        pass