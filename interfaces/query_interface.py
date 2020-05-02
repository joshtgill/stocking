import yfinance as yf
import datetime
from forms.stock_data import StockData
import pandas


class QueryInterface:

    def __init__(self, configInterface):
        self.configInterface = configInterface


    def performQuery(self, query):
        stockData = StockData(query.symbol, query.start, query.end, query.interval)

        start = query.start
        end = query.end
        while True:
            # Due to yfinance request granularity, cannot request more than 7 days of data at 1m intervals.
            if (end - start).days > 7:
                end = start + datetime.timedelta(days=7)

            # Get history
            stockHistory = yf.Ticker(query.symbol).history(start=start, end=end, interval=query.interval)
            dateTimes = stockHistory.index.values
            for rowIndex in range(len(stockHistory)):
                timeStamp = pandas.to_datetime(str(dateTimes[rowIndex]))
                formattedTimeStamp = timeStamp.strftime('{} {}'.format(self.configInterface.get('dateFormat'), self.configInterface.get('timeFormat')))
                stockData.history.append([formattedTimeStamp, stockHistory.iloc[rowIndex, 0], stockHistory.iloc[rowIndex, 1], stockHistory.iloc[rowIndex, 2], stockHistory.iloc[rowIndex, 3]])

            # Stop if at end
            if end == query.end:
                break

            # Iterate for next query
            start = end
            end = query.end

        return stockData
