from objects.query_form import QueryForm
import datetime


class QueryService:

    def __init__(self, dataService, queryInterface):
        self.dataService = dataService
        self.queryInterface = queryInterface

        self.queries = self.buildQueries()


    def buildQueries(self):
        queryEnd = datetime.datetime.now().replace(second=0, microsecond=0)
        queryStart = (queryEnd - datetime.timedelta(days=29)).replace(hour=0, minute=0)
        queries = []
        for interval in self.dataService.config.get('queries'):
            for symbol in self.dataService.config.get('queries').get(interval):
                query = self.optimizeQuery(QueryForm(symbol, interval, queryStart, queryEnd))
                if query:
                    queries.append(query)

        return queries


    def optimizeQuery(self, query):
        stockData = self.dataService.loadStockData(query.symbol, query.interval)
        if stockData:
            query.start = stockData.end.replace(second=0) + datetime.timedelta(minutes=1)  # Query start/end is inclusive
            if query.start >= query.end:  # Stored stock data is just as or more recent than query
                return None

        return query


    def performQueries(self):
        for query in self.queries:
            stockData = self.queryInterface.performQuery(query)

            self.dataService.saveStockData(stockData)
