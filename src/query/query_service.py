from query.query_interface import QueryInterface
from query.query import Query
from datetime import datetime, timedelta


class QueryService:

    def __init__(self, config, stockDataInterface):
        self.config = config
        self.stockDataInterface = stockDataInterface
        self.queryInterface = QueryInterface()
        self.queries = self.buildQueries()


    def buildQueries(self):
        queries = []
        for symbol in self.config.get('symbols'):
            start, end = self.determineQueryPeriod(symbol, self.config.get('interval'))
            queries.append(Query(symbol, self.config.get('interval'), start, end))

        return queries


    def determineQueryPeriod(self, symbol, interval):
        # Record current datetime
        now = datetime.now()

        # Default query start and end
        start = datetime(1970, 1, 1)
        end = now + timedelta(days=1)
        if interval == '1m':
            start = now - timedelta(days=29)

        # If stock history already exists, determine query start
        stockHistory = self.stockDataInterface.load(symbol, 1)
        if stockHistory:
            lastHistoryEntry = stockHistory[0][0]
            start = datetime.strptime(lastHistoryEntry, '%Y-%m-%d' if interval == '1d' else '%Y-%m-%d %H:%M:%S')

        return start.date(), end.date()


    def start(self):
        for query in self.queries:
            stock = self.queryInterface.performQuery(query)
            self.stockDataInterface.save(stock)
