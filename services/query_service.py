from structures.query_request import QueryRequest
from services.file_service import FileService
import datetime
import yfinance as yf
import pandas


class QueryService:

    def __init__(self, config):
        self.config = config

        self.queryRequest = self.config.get('query', QueryRequest)
        self.fileService = FileService('data/{}_{}_to_{}_{}.txt'.format(self.queryRequest.symbol,
                                                                        self.queryRequest.start.strftime(self.config.get('dateFormat')),
                                                                        self.queryRequest.end.strftime(self.config.get('dateFormat')),
                                                                        self.queryRequest.interval))


    def start(self):
        results = self.performQuery()

        resultsStr = ''
        for row in results:
            resultsStr += '{}\n'.format(row)

        self.fileService.write(resultsStr)


    def performQuery(self):
        results = []
        start = self.queryRequest.start
        end = self.queryRequest.end
        while True:
            # Due to yfinance request granularity, cannot request more than 7 days of data at 1m intervals.
            if (end - start).days > 7:
                end = start + datetime.timedelta(days=7)

            # Get data
            data = yf.Ticker(self.queryRequest.symbol).history(start=start, end=end, interval=self.queryRequest.interval)
            dateTimes = data.index.values
            for rowIndex in range(len(data)):
                timeStamp = pandas.to_datetime(str(dateTimes[rowIndex]))
                results.append((timeStamp.strftime('{} {}'.format(self.config.get('dateFormat'), self.config.get('timeFormat'))), data.iloc[rowIndex, 0], data.iloc[rowIndex, 3]))

            # Stop if at end
            if end == self.queryRequest.end:
                break

            # Iterate for next query
            start = end
            end = self.queryRequest.end


        return results
