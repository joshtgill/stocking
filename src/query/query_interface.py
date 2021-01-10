import urllib
from query.stock import Stock
import datetime
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


    def performStockQuery(self, interval, symbol, start, end):
        stock = Stock(symbol, interval)
        stockTicker = yfinance.Ticker(stock.symbol)

        # Get past splits
        yStockSplits = stockTicker.splits
        stock.splits = [(datetime.datetime.utcfromtimestamp(yStockSplits.index.values[i].tolist() / 1e9).date(), yStockSplits[i])
                        for i in range(len(yStockSplits))]

        dateTimeFormat = (self.dataInterface.settingsGet('{}/dateTimeFormat'.format(interval)) if interval == 'day'
                          else self.dataInterface.settingsGet('{}/dateTimeFormat'.format(interval)))

        # Track number of consecutive yFinance errors
        numYErrors = 0

        # yFinance only allows a period of up to 7 days for minute intervals
        # so break up queries into 7 day contiguous periods
        localQueryStart = start
        localQueryEnd = end
        if interval == 'minute' and (localQueryEnd - localQueryStart).days > 7:
            localQueryEnd = localQueryStart + timedelta(days=7)

        while (end - localQueryStart).days > 0:
            # Get stock history
            try:
                yStockHistory = stockTicker.history(interval='1d' if interval == 'day' else '1m',
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
            self.logInterface.log('yFinance failed for {} start={} end={}'.format(symbol, localQueryStart, localQueryEnd),
                                  'ERROR')

        return stock
