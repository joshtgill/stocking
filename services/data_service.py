import json
import os
from forms.stock_data import StockData
from datetime import datetime


class DataService:

    def loadConfig(self, configFileName):
        self.config = json.loads(self.read(configFileName, '{}'))


    def configGet(self, path, Obj = None):
        # Make list from path string
        pathList = path.strip().strip('/').split('/')

        # Traverse config down path
        configRunner = self.config
        for pathItem in pathList:
            if '[' in pathItem:
                index = int(pathItem[pathItem.find('[') + 1 : pathItem.find(']')])
                pathItem = pathItem[0 : pathItem.index('[')]
                configRunner = configRunner.get(pathItem)[index]
            else:
                configRunner = configRunner.get(pathItem)

        # If None, then assume value is an empty list
        if configRunner == None:
            return []

        # Build found config
        if isinstance(configRunner, list):
            itemList = []
            for item in configRunner:
                if Obj is not None:
                    obj = Obj()
                    obj.deserialize(item)
                    itemList.append(obj)
                else:
                    itemList.append(item)

            return itemList
        else:
            if Obj is not None:
                obj = Obj()
                obj.deserialize(configRunner)

                return obj
            else:
                return configRunner


    def loadStockData(self, symbol, interval):
        stockData = None
        for dataFileName in os.listdir('{}/'.format(self.configGet('stockDataDirectory'))):
            splitDataFileName = dataFileName.split('_')
            fileSymbol = splitDataFileName[0]
            fileInterval = splitDataFileName[1][: splitDataFileName[1].index('.')]
            if fileSymbol == symbol and fileInterval == interval:
                stockData = StockData(fileSymbol, fileInterval)

                fileLines = self.read('{}/{}'.format(self.configGet('stockDataDirectory'), dataFileName)).split('\n')[: -1]
                for dataLine in fileLines:
                    dataLine = eval(dataLine.strip())
                    stockData.history.append(dataLine)

                stockData.start = datetime.strptime(stockData.history[0][0], '{} {}'.format(self.configGet('dateFormat'), self.configGet('timeFormat')))
                stockData.end = datetime.strptime(stockData.history[len(stockData.history) - 1][0], '{} {}'.format(self.configGet('dateFormat'), self.configGet('timeFormat')))

                break

        return stockData


    def write(self, filePath, data):
        with open(filePath, 'a+') as file:
            file.write(data)


    def read(self, filePath, defaultData = ''):
        dataStr = ''

        if not os.path.exists(filePath):
            return dataStr

        with open(filePath, 'r') as file:
            dataStr = file.read()

        return dataStr
