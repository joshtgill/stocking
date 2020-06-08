import datetime
import json


class AnalyzeService:

    def __init__(self, stockDataInterface, fileInterface):
        self.stockDataInterface = stockDataInterface
        self.fileInterface = fileInterface


    def start(self):
        hottestStocks = self.determineHottestStocks(10, 10, 5)
        print(hottestStocks)

        symbols = ['TSLA', 'AAPL', 'MSFT']


    def determineHottestStocks(self, numStocks, historyItemsBack, minimumDifference=0):
        hottestStocks = [('', 0)] * numStocks
        for stockDataFileName in self.stockDataInterface.dataFileNames:
            # Get stock data
            stockData = self.stockDataInterface.load(stockDataFileName, historyItemsBack)
            if not stockData:
                continue
            # Calculate relevant data
            difference = stockData.history[historyItemsBack - 1][4] - stockData.history[0][1]
            if difference < minimumDifference:
                continue
            growthPoints = (difference / stockData.history[0][1]) * 100
            # Insert into list
            minHottestIndex = hottestStocks.index(min(hottestStocks, key=lambda a: a[1]))
            if growthPoints > hottestStocks[minHottestIndex][1]:
                hottestStocks[minHottestIndex] = (stockData.symbol, round(growthPoints, 3))

        # Organize
        hottestStocks.sort(key=lambda a: a[1])
        hottestStocks.reverse()
        hottestStocks[:] = [a for a in hottestStocks if a != ('', 0)]

        return hottestStocks


    def createOrder(self, symbols):
        # Get the next trading day

        orderFilePath = 'orders/{}.json'.format(datetime.strftime(datetime.now(), '%Y%m%d'))
        self.logPath = 'log/{}.log'.format(datetime.strftime(datetime.now(), '%Y%m%d%H%M%S'))

        self.fileInterface.write('data/order.json', json.dumps(symbols))
