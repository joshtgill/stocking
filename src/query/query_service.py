from query.query_interface import QueryInterface
from query.query import Query
import datetime


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
        return query


    def performQueries(self):
        numQueries = len(self.queries)
        for query in self.queries:
            stock = self.queryInterface.performQuery(query)
            if stock:
                self.stockDataInterface.save(stock)
