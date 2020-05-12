from query.query_interface import QueryInterface
from query.query import Query
from datetime import datetime


class QueryService:

    def __init__(self, queryConfig, stockDataInterface, logService):
        self.queryConfig = queryConfig
        self.stockDataInterface = stockDataInterface
        self.logService = logService

        self.queryInterface = QueryInterface()
        self.queries = self.buildQueries()


    def buildQueries(self):
        queries = []
        for interval, intervalData in self.queryConfig.get('queries').items():
            for symbol in intervalData.get('symbols'):
                optimizedQuery = self.optimizeQuery(Query(symbol, interval, intervalData.get('period')))
                if optimizedQuery:
                    queries.append(optimizedQuery)

        return queries


    def optimizeQuery(self, query):
        stockData = self.stockDataInterface.load(query.symbol, query.interval, True)
        if stockData:
            query.start = datetime.strptime(stockData.history[0][0], '%Y-%m-%d %H:%M:%S')
            query.end = datetime.now()
            query.period = None

        return query


    def performQueries(self):
        numQueries = len(self.queries)
        for query in self.queries:
            stock = self.queryInterface.performQuery(query)
            if stock:
                self.stockDataInterface.save(stock)
