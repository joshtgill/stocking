from query.query_interface import QueryInterface
from query.query import Query
from datetime import datetime


class QueryService:

    def __init__(self, queryConfig, stockDataInterface):
        self.queryConfig = queryConfig
        self.stockDataInterface = stockDataInterface
        self.queryInterface = QueryInterface()
        self.queries = self.buildQueries()


    def buildQueries(self):
        queries = []
        for interval, intervalData in self.queryConfig.get('queries').items():
            for symbol in intervalData.get('symbols'):
                queries.append(Query(symbol, interval, intervalData.get('period')))

        return queries


    def initiateQueries(self):
        for query in self.queries:
            stock = self.queryInterface.performQuery(query)
            self.stockDataInterface.save(stock)
