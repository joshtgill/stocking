class LearnService:

    def __init__(self, stockDataInterface):
        self.stockDataInterface = stockDataInterface


    def start(self):
        hottestStocks = self.determineHottestStocks(10, 10, 5)
        print(hottestStocks)


    def determineHottestStocks(self, numStocks, daysPast, minimumDifference=0):
        hottestStocks = [('', 0)] * numStocks
        for stockDataFileName in self.stockDataInterface.dataFileNames:
            # Get stock data
            symbol, interval = self.stockDataInterface.parseSymbolAndInterval(stockDataFileName)
            data = self.stockDataInterface.load(symbol, interval, daysPast)
            if not data:
                continue
            # Calculate relevant data
            difference = data.history[daysPast - 1][4] - data.history[0][1]
            if difference < minimumDifference:
                continue
            growthPoints = (difference / data.history[0][1]) * 100
            # Insert into list
            minHottestIndex = hottestStocks.index(min(hottestStocks, key=lambda a: a[1]))
            if growthPoints > hottestStocks[minHottestIndex][1]:
                hottestStocks[minHottestIndex] = (symbol, round(growthPoints, 3))

        # Organize
        hottestStocks.sort(key=lambda a: a[1])
        hottestStocks.reverse()
        hottestStocks[:] = [a for a in hottestStocks if a != ('', 0)]

        return hottestStocks
