class LearnService:

    def __init__(self, stockDataInterface):
        self.stockDataInterface = stockDataInterface


    def start(self):
        hottestStocks = self.determineHottestStocks(10, 10, 5)
        print(hottestStocks)


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
