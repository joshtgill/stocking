from common.stock import Stock
import yfinance
import pandas
import pytz
import datetime
import numpy


class QueryInterface:

    def performQuery(self, query):
        # Get history data
        stockHistory = yfinance.Ticker(query.symbol).history(interval=query.interval, period=query.period)
        dateTimes = stockHistory.index.values

        # Store history data
        stock = Stock(query.symbol, query.interval)
        for rowIndex in range(len(stockHistory)):
            if not numpy.isnan(stockHistory.iloc[rowIndex, 0]):
                dataTimestamp = pandas.to_datetime((dateTimes[rowIndex])).replace(tzinfo=pytz.utc).astimezone('US/Eastern')
                dataTimestampFixed = dataTimestamp + datetime.timedelta(days=1)  # Yfinance's timestamp is behind by one day
                stock.history.append([dataTimestampFixed.strftime('%Y-%m-%d %H:%M:%S'), stockHistory.iloc[rowIndex, 0],
                                      stockHistory.iloc[rowIndex, 1], stockHistory.iloc[rowIndex, 2], stockHistory.iloc[rowIndex, 3]])

        return stock
