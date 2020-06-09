from query.query_interface import QueryInterface
from query.query import Query
from datetime import datetime


class QueryService:

    def __init__(self, config, stockDataInterface):
        self.config = config
        self.stockDataInterface = stockDataInterface
        self.queryInterface = QueryInterface()
        self.queries = self.buildQueries()


    def buildQueries(self):
        queries = []
        interval = self.config.get('interval')
        for symbol in self.config.get('symbols'):
            queries.append(Query(symbol, interval))

        return queries


    def start(self):
        for query in self.queries:
            stock = self.queryInterface.performQuery(query)
            self.stockDataInterface.save(stock)
