from forms.query import Query
import datetime


class QueryService:

    def __init__(self, dataService, queryInterface):
        self.dataService = dataService
        self.queryInterface = queryInterface

        self.queries = self.buildQueries()
        self.verifyQueries()


    def buildQueries(self):
        queryEnd = datetime.datetime.now().replace(second=0, microsecond=0)
        queryStart = (queryEnd - datetime.timedelta(days=29)).replace(hour=0, minute=0)
        queries = []
        for interval in self.dataService.config.get('queries'):
            for symbol in self.dataService.config.get('queries').get(interval):
                query = Query(symbol, interval, queryStart, queryEnd)
                queries.append(query)

        return queries


    def verifyQueries(self):
        i = 0
        while i < len(self.queries):
            query = self.queries[i]
            stockData = self.dataService.loadStockData(query.symbol, query.interval)
            if stockData:
                query.start = stockData.end.replace(second=0) + datetime.timedelta(minutes=1)  # Query start/end is inclusive
                if query.start >= query.end:  # Stored stock data is just as or more recent than query
                    del self.queries[i]
                    i -= 1
            i += 1


    def initiateQueries(self):
        for query in self.queries:
            stockData = self.queryInterface.performQuery(query)

            self.dataService.saveStockData(stockData)
