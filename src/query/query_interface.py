from common.stock import Stock
import yfinance
import pytz
import pandas


class QueryInterface:

    def performQuery(self, query):
        stock = Stock(query.symbol, query.interval)

        # Get history
        if query.period:
            stockHistory = yfinance.Ticker(query.symbol).history(interval=query.interval, period=query.period)
        else:
            stockHistory = yfinance.Ticker(query.symbol).history(interval=query.interval, start=query.start.strftime('%Y-%m-%d'),
                                                                                          end=query.end.strftime('%Y-%m-%d'))

        # Store history
        dateTimes = stockHistory.index.values
        for rowIndex in range(len(stockHistory)):
            dataTimestamp = pandas.to_datetime((dateTimes[rowIndex])).replace(tzinfo=pytz.utc).astimezone('US/Eastern').strftime('%Y-%m-%d %H:%M:%S')
            stock.history.append([dataTimestamp, stockHistory.iloc[rowIndex, 0], stockHistory.iloc[rowIndex, 1],
                                                 stockHistory.iloc[rowIndex, 2], stockHistory.iloc[rowIndex, 3]])

        return stock
