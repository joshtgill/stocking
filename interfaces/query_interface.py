from forms.stock_data import StockData
import datetime
import yfinance
import pandas


class QueryInterface:

    def __init__(self, dataService):
        self.dataService = dataService


    def performQuery(self, query):
        stockData = StockData(query.symbol, query.interval, query.start, query.end)

        start = query.start
        end = query.end
        while True:
            # Due to yfinance request granularity, cannot request more than 7 days of data at 1m intervals.
            if query.interval == '1m' and (end - start).days > 6:
                end = start + datetime.timedelta(days=6, hours=6.5)

            # Get history
            stockHistory = yfinance.Ticker(query.symbol).history(start=start, end=end, interval=query.interval)
            dateTimes = stockHistory.index.values
            for rowIndex in range(len(stockHistory)):
                timeStamp = pandas.to_datetime(str(dateTimes[rowIndex]))
                formattedTimeStamp = timeStamp.strftime('{} {}'.format(self.dataService.configGet('dateFormat'), self.dataService.configGet('timeFormat')))
                stockData.history.append([formattedTimeStamp, stockHistory.iloc[rowIndex, 0], stockHistory.iloc[rowIndex, 1], stockHistory.iloc[rowIndex, 2], stockHistory.iloc[rowIndex, 3]])

            # Stop if at end
            if end == query.end:
                break

            # Only here for 1m interval, iterate for next query
            start = end + datetime.timedelta(hours=17.5)
            end = query.end

        return stockData
