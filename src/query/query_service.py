from query.query import Query
import datetime


class QueryService:

    def __init__(self, dataInterface, queryInterface):
        self.dataInterface = dataInterface
        self.queryInterface = queryInterface

        self.queries = self.buildQueries()


    def buildQueries(self):
        queryEnd = datetime.datetime.now().replace(second=0, microsecond=0)
        queryStart = (queryEnd - datetime.timedelta(days=29)).replace(hour=0, minute=0)
        queries = []
        for interval in self.dataInterface.config.get('queries'):
            for symbol in self.dataInterface.config.get('queries').get(interval):
                optimizedQuery = self.optimizeQuery(Query(symbol, interval, queryStart, queryEnd))
                if optimizedQuery:
                    queries.append(optimizedQuery)

        return queries


    def optimizeQuery(self, query):
        stockDataEnd = self.dataInterface.getStockDataEnd(query.symbol, query.interval)
        if stockDataEnd:
            query.start = stockDataEnd.replace(second=0) + datetime.timedelta(minutes=1)  # Query start/end is inclusive
            if query.start >= query.end:  # Stored stock data is just as or more recent than query
                return None

        return query


    def performQueries(self):
        numQueries = len(self.queries)
        for i in range(numQueries):
            queryStock = self.queryInterface.performQuery(self.queries[i])
            if queryStock:
                self.dataInterface.saveStock(queryStock)
