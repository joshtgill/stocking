from common.stock import Stock
from datetime import timedelta
import yfinance
import pandas
import numpy


class QueryInterface:

    def __init__(self, logService):
        self.logService = logService


    def performQuery(self, query):
        stock = Stock(query.symbol, query.interval)

        dateTimeFormat = '%Y-%m-%d' if query.interval == '1d' else '%Y-%m-%d %H:%M:%S'

        # Track number of consecutive yFinance errors
        numYErrors = 0

        # yFinance only allows a period of up to 7 days for 1m intervals
        # so break up queries into 7 day contiguous periods
        localQueryStart = query.start
        localQueryEnd = query.end
        if query.interval == '1m' and (localQueryEnd - localQueryStart).days > 7:
            localQueryEnd = localQueryStart + timedelta(days=7)

        while (query.end - localQueryStart).days > 0:
            # Get history data
            try:
                yStockHistory = yfinance.Ticker(query.symbol).history(interval=query.interval,
                                                                      start=localQueryStart,
                                                                      end=localQueryEnd)
                numYErrors = 0
            except ValueError:  # Weird json-decode-error with yfinance, try again (up to 5 times)
                if numYErrors < 6:
                    self.logService.log('query', 'yFinance json-decode-error', 'info')
                    numYErrors += 1
                    continue
                else:
                    self.logService.log('query', 'Max yFinance json-decode-errors', 'error')
                    return

            dateTimes = yStockHistory.index.values

            # Store stock data
            for rowIndex in range(len(yStockHistory)):
                if not numpy.isnan(yStockHistory.iloc[rowIndex, 0]):
                    historyDate = pandas.to_datetime((dateTimes[rowIndex])).strftime(dateTimeFormat)
                    stock.history.append((historyDate, yStockHistory.iloc[rowIndex, 0], yStockHistory.iloc[rowIndex, 1],
                                        yStockHistory.iloc[rowIndex, 2], yStockHistory.iloc[rowIndex, 3]))

            # Increment start and end
            localQueryStart = localQueryEnd
            localQueryEnd = localQueryEnd + timedelta(days=7)

        return stock
