from shared.stock import Stock
import datetime
import yfinance
import pandas
import pytz


class QueryInterface:

    def __init__(self, dataInterface):
        self.dataInterface = dataInterface


    def performQuery(self, query):
        stock = Stock(query.symbol, query.interval)

        # Get history
        stockHistory = yfinance.Ticker(query.symbol).history(interval=query.interval, period=query.period)

        # Store history
        dateTimes = stockHistory.index.values
        for rowIndex in range(len(stockHistory)):
            dataTimestamp = pandas.to_datetime((dateTimes[rowIndex])).replace(tzinfo=pytz.utc).astimezone('US/Eastern').strftime('%Y-%m-%d %H:%M:%S')
            stock.history.append([dataTimestamp, stockHistory.iloc[rowIndex, 0], stockHistory.iloc[rowIndex, 1],
                                                 stockHistory.iloc[rowIndex, 2], stockHistory.iloc[rowIndex, 3]])

        return stock
