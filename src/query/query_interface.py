from shared.stock import Stock
import datetime
import yfinance
import pandas
import pytz


class QueryInterface:

    def __init__(self, dataInterface):
        self.dataInterface = dataInterface


    def performQuery(self, query):
        queryStock = Stock(query.symbol, query.interval, query.start, query.end)

        dataStart = query.start
        dataEnd = query.end
        while True:
            # Due to yfinance request granularity, cannot request more than 7 days of data at 1m intervals.
            if query.interval == '1m' and (dataEnd - dataStart).days > 7:
                dataEnd = dataStart + datetime.timedelta(days=7)

            # Get history
            stockHistory = None
            try:
                stockHistory = yfinance.Ticker(query.symbol).history(start=dataStart, end=dataEnd, interval=query.interval)
            except requests.exceptions.ConnectionError:
                continue  # Try again

            # Check history
            if len(stockHistory) == 0:
                self.dataInterface.log('No history for {} from {} to {}'.format(query.symbol, query.start, query.end), 'WARNING')
                return None

            # Store history
            dateTimes = stockHistory.index.values
            for rowIndex in range(len(stockHistory)):
                dataTimestamp = pandas.to_datetime((dateTimes[rowIndex])).replace(tzinfo=pytz.utc).astimezone('US/Eastern').strftime('%Y-%m-%d %H:%M:%S')
                queryStock.history.append([dataTimestamp, stockHistory.iloc[rowIndex, 0], stockHistory.iloc[rowIndex, 1], stockHistory.iloc[rowIndex, 2], stockHistory.iloc[rowIndex, 3]])

            # Stop if at end of query
            if dataEnd == query.end:
                break

            # Only here for 1m interval, iterate for next query
            dataStart = dataEnd
            dataEnd = query.end

        return queryStock

'''
TODO
stockHistory = None
stockHistory = yfinance.download(tickers='TSLA', period='max', interval='1h')

# Store history
dateTimes = stockHistory.index.values
for rowIndex in range(len(stockHistory)):
    dataTimestamp = pandas.to_datetime((dateTimes[rowIndex])).replace(tzinfo=pytz.utc).astimezone('US/Eastern').strftime('%Y-%m-%d %H:%M:%S')
    print(dataTimestamp)
'''
