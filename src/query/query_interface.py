import urllib
from query.stock import Stock
from datetime import timedelta
import yfinance
import pandas
import numpy


class QueryInterface:

    def __init__(self, dataInterface, logInterface):
        self.dataInterface = dataInterface
        self.logInterface = logInterface


    def performSymbolsQuery(self):
        capitalSymbols = []
        globalSymbols = []
        globalSelectSymbols = []

        with urllib.request.urlopen(self.dataInterface.settingsGet('nasdaqSymbolsUrlPath')) as page:
            for line in page.readlines():
                line = line.decode('utf-8').strip()
                if 'Common Stock' in line:
                    # Extract symbol and market category
                    symbol = line[ : line.find('|')]
                    if symbol in self.dataInterface.settingsGet('blacklistedSymbols'):
                        continue
                    marketCategory = line[line.find('Common Stock') + len('Common Stock') : ].split('|')[1]

                    # Add to corresponding list
                    if marketCategory == 'S':
                        capitalSymbols.append(symbol)
                    elif marketCategory == 'G':
                        globalSymbols.append(symbol)
                    elif marketCategory == 'Q':
                        globalSelectSymbols.append(symbol)

        return capitalSymbols, globalSymbols, globalSelectSymbols


    def performStockQuery(self, query):
        stock = Stock(query.symbol, query.interval)

        dateTimeFormat = (self.dataInterface.settingsGet('{}/dateTimeFormat'.format(query.interval)) if query.interval == 'day'
                          else self.dataInterface.settingsGet('{}/dateTimeFormat'.format(query.interval)))

        # Track number of consecutive yFinance errors
        numYErrors = 0

        # yFinance only allows a period of up to 7 days for minute intervals
        # so break up queries into 7 day contiguous periods
        localQueryStart = query.start
        localQueryEnd = query.end
        if query.interval == 'minute' and (localQueryEnd - localQueryStart).days > 7:
            localQueryEnd = localQueryStart + timedelta(days=7)

        while (query.end - localQueryStart).days > 0:
            # Get stock history
            try:
                yStockHistory = yfinance.Ticker(query.symbol).history(interval=query.interval,
                                                                      start=localQueryStart,
                                                                      end=localQueryEnd)
            except Exception:  # Any error with yfinance, try again (up to 5 times)
                numYErrors += 1
                if numYErrors == 6:
                    break
                else:
                    continue

            # Reset yFinance error counter following success
            numYErrors = 0

            # Store stock data
            dateTimes = yStockHistory.index.values
            for rowIndex in range(len(yStockHistory)):
                if not numpy.isnan(yStockHistory.iloc[rowIndex, 0]):
                    historyDate = pandas.to_datetime((dateTimes[rowIndex])).strftime(dateTimeFormat)
                    stock.history.append((historyDate, yStockHistory.iloc[rowIndex, 0], yStockHistory.iloc[rowIndex, 1],
                                        yStockHistory.iloc[rowIndex, 2], yStockHistory.iloc[rowIndex, 3]))

            # Increment start and end
            localQueryStart = localQueryEnd
            localQueryEnd = localQueryEnd + timedelta(days=7)

        # Report yFinance errors
        if numYErrors:
            self.logInterface.log('yFinance failed for {} start={} end={}'.format(query.symbol, localQueryStart, localQueryEnd),
                                'ERROR')

        return stock
