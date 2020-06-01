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
        interval = self.queryConfig.get('interval')
        period = self.queryConfig.get('period')
        for symbol in self.queryConfig.get('symbols'):
            queries.append(Query(symbol, interval, period))

        return queries


    def initiateQueries(self):
        showStatus = self.queryConfig.get('showStatus')
        for i in range(len(self.queries)):
            stock = self.queryInterface.performQuery(self.queries[i])
            self.stockDataInterface.save(stock)
            if showStatus:
                print('{}/{}'.format(i + 1, len(self.queries)), end='\r')
