import yfinance as yf
import datetime
from forms.stock_data import StockData
import pandas


class QueryInterface:

    def __init__(self, configInterface):
        self.configInterface = configInterface


    def query(self, queryRequest):
        stockData = StockData(queryRequest.symbol, queryRequest.start, queryRequest.end, queryRequest.interval)

        start = queryRequest.start
        end = queryRequest.end
        while True:
            # Due to yfinance request granularity, cannot request more than 7 days of data at 1m intervals.
            if (end - start).days > 7:
                end = start + datetime.timedelta(days=7)

            # Get data
            data = yf.Ticker(queryRequest.symbol).history(start=start, end=end, interval=queryRequest.interval)
            dateTimes = data.index.values
            for rowIndex in range(len(data)):
                timeStamp = pandas.to_datetime(str(dateTimes[rowIndex]))
                formattedTimeStamp = timeStamp.strftime('{} {}'.format(self.configInterface.get('dateFormat'), self.configInterface.get('timeFormat')))
                stockData.data[0].append(formattedTimeStamp)
                for i in range(4):
                    stockData.data[i + 1].append(data.iloc[rowIndex, i])

            # Stop if at end
            if end == queryRequest.end:
                break

            # Iterate for next query
            start = end
            end = queryRequest.end

        return stockData
