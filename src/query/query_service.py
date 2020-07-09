from common.stock_data_interface import StockDataInterface
from query.query import Query
from datetime import datetime, timedelta
from query.query_interface import QueryInterface


class QueryService:

    def __init__(self, configInterface, logService):
        self.configInterface = configInterface
        self.logService = logService
        self.initStockDataInterfaces()


    def __del__(self):
        self.logService.unregister('QUERY')


    def initStockDataInterfaces(self):
        self.stockDataInterfaces = {}  # {interval: StockDataInterface}
        for interval in self.configInterface.configGet('queries'):
            self.stockDataInterfaces.update({interval:
                                             StockDataInterface(self.configInterface.settingsGet('{}/stockDataPath'.format(interval)))})


    def go(self):
        self.logService.register('QUERY')

        queryInterface = QueryInterface(self.configInterface, self.logService)

        queries = self.buildQueries()

        for interval in queries:
            self.logService.log('Performing {} queries'.format(interval))
            for query in queries.get(interval):
                stock = queryInterface.performQuery(query)
                self.stockDataInterfaces.get(interval).save(stock)


    def buildQueries(self):
        queries = {}  # {interval: list of Querys}
        for interval in self.configInterface.configGet('queries'):
            queries.update({interval: []})
            for symbol in self.configInterface.configGet('queries/{}'.format(interval)):
                start, end = self.determineQueryPeriod(symbol, interval)
                queries.get(interval).append(Query(symbol, interval, start, end))

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
        stockHistory = self.stockDataInterfaces.get(interval).load(symbol, numLastRows=1)
        if stockHistory:
            lastHistoryRow = stockHistory[0][0]
            start = datetime.strptime(lastHistoryRow, self.configInterface.settingsGet('{}/dateTimeFormat'.format(interval)) if interval == '1d'
                                                      else self.configInterface.settingsGet('{}/dateTimeFormat'.format(interval)))

        return start.date(), end.date()
