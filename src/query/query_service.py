from query.query_interface import QueryInterface
from query.query import Query
from datetime import datetime
from datetime import timedelta


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
        # Default start and end datetime
        start = datetime(1970, 1, 1)
        end = datetime.now().replace(second=0, microsecond=0)

        # Load stock history containing only last history entry
        # If no history exists, return default period
        stockHistory = self.stockDataInterface.load(symbol, 1)
        if not stockHistory:
            return start, end

        # Determine start datetime
        lastHistoryEntry = stockHistory[0][0]
        start = datetime.strptime(lastHistoryEntry, '%Y-%m-%d').replace(second=0)
        if interval == '1d':
            start = start + timedelta(days=1)

        return start, end


    def start(self):
        for query in self.queries:
            stock = self.queryInterface.performQuery(query)
            self.stockDataInterface.save(stock)
