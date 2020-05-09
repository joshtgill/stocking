from query.query import Query
import datetime


class QueryService:

    def __init__(self, dataInterface, queryInterface):
        self.dataInterface = dataInterface
        self.queryInterface = queryInterface

        self.queries = self.buildQueries()


    def buildQueries(self):
        queries = []
        for interval, intervalData in self.dataInterface.queryConfig.get('queries').items():
            for symbol in intervalData.get('symbols'):
                optimizedQuery = self.optimizeQuery(Query(symbol, interval, intervalData.get('period')))
                if optimizedQuery:
                    queries.append(optimizedQuery)

        return queries


    def optimizeQuery(self, query):
        return query


    def performQueries(self):
        numQueries = len(self.queries)
        for i in range(numQueries):
            queryStock = self.queryInterface.performQuery(self.queries[i])
            if queryStock:
                self.dataInterface.saveStock(queryStock)
