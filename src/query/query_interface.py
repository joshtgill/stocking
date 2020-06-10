from common.stock import Stock
import yfinance
import pandas
import pytz
import numpy


class QueryInterface:

    def performQuery(self, query):
        # Get time format
        dateTimeFormat = '%Y-%m-%d' if query.interval == '1d' else '%Y-%m-%d %H:%M:%S'

        # Get history data
        yStockHistory = yfinance.Ticker(query.symbol).history(interval=query.interval, start=query.start, end=query.end)
        dateTimes = yStockHistory.index.values

        # Store stock data
        stock = Stock(query.symbol, query.interval)
        for rowIndex in range(len(yStockHistory)):
            if not numpy.isnan(yStockHistory.iloc[rowIndex, 0]):
                historyDate = pandas.to_datetime((dateTimes[rowIndex])).strftime(dateTimeFormat)
                stock.history.append([historyDate, yStockHistory.iloc[rowIndex, 0], yStockHistory.iloc[rowIndex, 1],
                                      yStockHistory.iloc[rowIndex, 2], yStockHistory.iloc[rowIndex, 3]])

        return stock
