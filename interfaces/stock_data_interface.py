import os
from forms.stock_data import StockData
from services.file_service import FileService
from datetime import datetime


class StockDataInterface:

    def __init__(self, configService, symbol):
        self.configService = configService
        self.symbol = symbol

        self.stockData = None

        self.load()


    def load(self):
        for dataFileName in os.listdir('{}/'.format(self.configService.get('stockDataDirectory'))):
            splitDataFileName = dataFileName.split('_')
            if splitDataFileName[0] == self.symbol:
                self.stockData = StockData(splitDataFileName[0],
                                                   datetime.strptime(splitDataFileName[1], '%Y-%m-%d'),
                                                   datetime.strptime(splitDataFileName[3], '%Y-%m-%d'),
                                                   splitDataFileName[4][: splitDataFileName[4].index('.')])

                with open('{}/{}'.format(self.configService.get('stockDataDirectory'), dataFileName)) as dataFile:
                    for dataLine in dataFile.readlines():
                        dataItem = eval(dataLine.strip())
                        for stockDataCol, dataValue in zip(self.stockData.data, dataItem):
                            stockDataCol.append(dataValue)
