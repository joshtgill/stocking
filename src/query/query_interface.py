from common.stock import Stock
import yfinance
import pytz
import pandas
import numpy


class QueryInterface:

    def performQuery(self, query):
        # Get history data
        stockHistory = yfinance.Ticker(query.symbol).history(interval=query.interval, period=query.period)
        dateTimes = stockHistory.index.values

        # Store history data
        stock = Stock(query.symbol, query.interval)
        for rowIndex in range(len(stockHistory)):
            dataTimestamp = pandas.to_datetime((dateTimes[rowIndex])).replace(tzinfo=pytz.utc).astimezone('US/Eastern').strftime('%Y-%m-%d %H:%M:%S')
            if not numpy.isnan(stockHistory.iloc[rowIndex, 0]):
                stock.history.append([dataTimestamp, stockHistory.iloc[rowIndex, 0], stockHistory.iloc[rowIndex, 1],
                                                    stockHistory.iloc[rowIndex, 2], stockHistory.iloc[rowIndex, 3]])

        return stock
