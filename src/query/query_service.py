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
        showStatus = self.queryConfig.get('showStatus')
        numQueries = len(self.queries)
        for i in range(numQueries):
            stock = self.queryInterface.performQuery(self.queries[i])
            self.stockDataInterface.save(stock)
            if showStatus:
                print('{}/{}'.format(i + 1, numQueries), end='\r')
