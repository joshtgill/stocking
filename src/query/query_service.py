from common.stock_data_interface import StockDataInterface
from query.query import Query
from datetime import datetime, timedelta
from query.query_interface import QueryInterface


class QueryService:

    def __init__(self, configInterface, logService):
        self.configInterface = configInterface
        self.logService = logService
        self.stockDataInterfaces = self.initStockDataInterfaces()
        self.queries = self.buildQueries()


    def initStockDataInterfaces(self):
        stockDataInterfaces = {}  # {interval: interface}
        for queryConfig in self.configInterface.get('queries'):
            stockDataInterfaces.update({queryConfig.get('interval'):
                                        StockDataInterface(queryConfig.get('interval'))})

        return stockDataInterfaces


    def buildQueries(self):
        queries = {}  # {interval: list of queries}
        for queryConfig in self.configInterface.get('queries'):
            queries.update({queryConfig.get('interval'): []})
            for symbol in queryConfig.get('symbols'):
                start, end = self.determineQueryPeriod(symbol, queryConfig.get('interval'))
                queries.get(queryConfig.get('interval')).append(Query(symbol, queryConfig.get('interval'), start, end))

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
        stockHistory = self.stockDataInterfaces.get(interval).load(symbol, 1)
        if stockHistory:
            lastHistoryEntry = stockHistory[0][0]
            start = datetime.strptime(lastHistoryEntry, '%Y-%m-%d' if interval == '1d' else '%Y-%m-%d %H:%M:%S')

        return start.date(), end.date()


    def start(self):
        queryInterface = QueryInterface(self.logService)

        for interval in self.queries:
            self.logService.log('Query', 'Performing {} queries'.format(interval))
            for query in self.queries.get(interval):
                stock = queryInterface.performQuery(query)
                self.stockDataInterfaces.get(interval).save(stock)
