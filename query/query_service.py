import json
from query.query_request import QueryRequest
import yfinance as yf
import pandas


class QueryService:

    def __init__(self, configFileName):
        # Buld QueryRequest from JSON
        configData = {}
        with open(configFileName, 'r') as configFile:
            configData = json.loads(configFile.read())
        self.queryRequest = QueryRequest()
        self.queryRequest.deserialize(configData)

        # Format output file's filename
        self.outFileName = 'data/{}_{}_to_{}_{}.txt'.format(self.queryRequest.symbol, self.queryRequest.start, self.queryRequest.end, self.queryRequest.interval)


    def start(self):
        results = self.performQuery()
        with open(self.outFileName, 'w+') as outFile:
            for row in results:
                outFile.write(str(row) + '\n')


    def performQuery(self):
        tsla = yf.Ticker(self.queryRequest.symbol)
        data = tsla.history(start=self.queryRequest.start, end=self.queryRequest.end, interval=self.queryRequest.interval)

        results = []
        dateTimes = data.index.values
        for rowIndex in range(len(data)):
            t = pandas.to_datetime(str(dateTimes[rowIndex]))
            results.append((t.strftime('%Y/%m/%d %H:%M:%S'), data.iloc[rowIndex, 0], data.iloc[rowIndex, 3]))

        return results
