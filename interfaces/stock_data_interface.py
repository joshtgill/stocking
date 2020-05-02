import os
from forms.stock_data import StockData
from services.file_service import FileService
from datetime import datetime


class StockDataInterface:

    def __init__(self, configInterface, fileService, symbol):
        self.configInterface = configInterface
        self.fileService = fileService
        self.symbol = symbol

        self.data = self.load()


    def load(self):
        for dataFileName in os.listdir('{}/'.format(self.configInterface.get('stockDataDirectory'))):
            splitDataFileName = dataFileName.split('_')
            if splitDataFileName[0] == self.symbol:
                stockData = StockData(splitDataFileName[0],
                                      datetime.strptime(splitDataFileName[1], '%Y-%m-%d'),
                                      datetime.strptime(splitDataFileName[3], '%Y-%m-%d'),
                                      splitDataFileName[4][: splitDataFileName[4].index('.')])

                fileData = self.fileService.read('{}/{}'.format(self.configInterface.get('stockDataDirectory'), dataFileName))
                for dataLine in fileData.split('\n'):
                    dataLine = eval(dataLine.strip())
                    for stockDataCol, dataValue in zip(stockData.history, dataLine):
                        stockDataCol.append(dataValue)

                return stockData
