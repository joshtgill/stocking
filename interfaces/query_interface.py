import yfinance as yf
import datetime
import pandas


class QueryInterface:

    def __init__(self, configInterface):
        self.configInterface = configInterface


    def query(self, queryForm):
        results = []
        start = queryForm.start
        end = queryForm.end
        while True:
            # Due to yfinance request granularity, cannot request more than 7 days of data at 1m intervals.
            if (end - start).days > 7:
                end = start + datetime.timedelta(days=7)

            # Get data
            data = yf.Ticker(queryForm.symbol).history(start=start, end=end, interval=queryForm.interval)
            dateTimes = data.index.values
            for rowIndex in range(len(data)):
                timeStamp = pandas.to_datetime(str(dateTimes[rowIndex]))
                results.append((timeStamp.strftime('{} {}'.format(self.configInterface.get('dateFormat'), self.configInterface.get('timeFormat'))), data.iloc[rowIndex, 0], data.iloc[rowIndex, 1], data.iloc[rowIndex, 2], data.iloc[rowIndex, 3]))

            # Stop if at end
            if end == queryForm.end:
                break

            # Iterate for next query
            start = end
            end = queryForm.end

        return results
