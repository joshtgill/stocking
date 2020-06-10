from datetime import timedelta
from common.stock import Stock
import yfinance
import pandas
import pytz
import numpy


class QueryInterface:

    def performQuery(self, query):
        # Stock to populate
        stock = Stock(query.symbol, query.interval)

        # Get time format
        dateTimeFormat = '%Y-%m-%d' if query.interval == '1d' else '%Y-%m-%d %H:%M:%S'

        # yFinance only allows a period of up to 7 days for 1m intervals
        # so break up queries into 7 day contiguous periods
        localQueryStart = query.start
        localQueryEnd = query.end
        if query.interval == '1m' and (localQueryEnd - localQueryStart).days > 7:
            localQueryEnd = localQueryStart + timedelta(days=7)

        while (query.end - localQueryStart).days > 0:
            print(localQueryStart, localQueryEnd)
            # Get history data
            yStockHistory = yfinance.Ticker(query.symbol).history(interval=query.interval,
                                                                  start=localQueryStart,
                                                                  end=localQueryEnd)
            dateTimes = yStockHistory.index.values

            # Store stock data
            for rowIndex in range(len(yStockHistory)):
                if not numpy.isnan(yStockHistory.iloc[rowIndex, 0]):
                    historyDate = pandas.to_datetime((dateTimes[rowIndex])).strftime(dateTimeFormat)
                    stock.history.append([historyDate, yStockHistory.iloc[rowIndex, 0], yStockHistory.iloc[rowIndex, 1],
                                        yStockHistory.iloc[rowIndex, 2], yStockHistory.iloc[rowIndex, 3]])

            # Increment start and end
            localQueryStart = localQueryEnd
            localQueryEnd = localQueryEnd + timedelta(days=7)

        return stock
