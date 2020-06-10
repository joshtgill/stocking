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
        # Default query start and end
        start = datetime(1970, 1, 1)
        end = datetime.now()
        if interval == '1m':
            daysBack = 29 if (datetime.now() > datetime(end.year, end.month, end.day, 9, 30)) else 30
            start = end - timedelta(days=daysBack)

        # If stock history already exists, determine query start
        stockHistory = self.stockDataInterface.load(symbol, 1)
        if stockHistory:
            lastHistoryEntry = stockHistory[0][0]
            if interval == '1d':
                start = datetime.strptime(lastHistoryEntry, '%Y-%m-%d') + timedelta(days=1)
            elif interval == '1m':
                start = datetime.strptime(lastHistoryEntry, '%Y-%m-%d %H:%M:%S')

        return start.date(), end.date()


    def start(self):
        for query in self.queries:
            stock = self.queryInterface.performQuery(query)
            self.stockDataInterface.save(stock)
