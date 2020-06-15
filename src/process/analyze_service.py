import datetime
import json


class AnalyzeService:

    def __init__(self, configInterface, stockDataInterface, fileInterface):
        self.configInterface = configInterface
        self.stockDataInterface = stockDataInterface
        self.fileInterface = fileInterface


    def start(self):
        print(self.configInterface.get('symbols'))


    def calculateGrowth(self, symbol):
        pass
