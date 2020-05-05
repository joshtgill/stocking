from forms.stock_data import StockData
import datetime
import yfinance
import pandas


class QueryInterface:

    def __init__(self, dataService):
        self.dataService = dataService


    def performQuery(self, query):
        stockData = StockData(query.symbol, query.interval, query.start, query.end)

        dataStart = query.start
        dataEnd = query.end
        while True:
            # Due to yfinance request granularity, cannot request more than 7 days of data at 1m intervals.
            if query.interval == '1m' and (dataEnd - dataStart).days > 6:
                dataEnd = dataStart + datetime.timedelta(days=6, hours=6.5)

            # Get history
            stockHistory = yfinance.Ticker(query.symbol).history(start=dataStart, end=dataEnd, interval=query.interval)
            dateTimes = stockHistory.index.values
            for rowIndex in range(len(stockHistory)):
                dataTimestamp = pandas.to_datetime((dateTimes[rowIndex])).strftime('%Y-%m-%d %H:%M:%S')
                stockData.history.append([dataTimestamp, stockHistory.iloc[rowIndex, 0], stockHistory.iloc[rowIndex, 1], stockHistory.iloc[rowIndex, 2], stockHistory.iloc[rowIndex, 3]])

            # Stop if at end
            if dataEnd == query.end:
                break

            # Only here for 1m interval, iterate for next query
            dataStart = dataEnd + datetime.timedelta(hours=17.5)
            dataEnd = query.end

        return stockData
