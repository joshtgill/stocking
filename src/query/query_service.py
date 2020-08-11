from query.query import Query
from datetime import datetime, timedelta
from query.query_interface import QueryInterface


class QueryService:

    def __init__(self, dataInterface, logService, stockDataInterface):
        self.dataInterface = dataInterface
        self.logService = logService
        self.stockDataInterface = stockDataInterface


    def go(self):
        interval = self.dataInterface.configGet('interval')

        self.logService.track('QUERY {}'.format(interval))

        queryInterface = QueryInterface(self.dataInterface, self.logService)

        for query in self.buildQueries(interval):
            stock = queryInterface.performQuery(query)
            self.stockDataInterface.save(stock)

        self.logService.untrack('QUERY {}'.format(interval))


    def buildQueries(self, interval):
        queries = []
        for symbol in self.dataInterface.configGet('symbols'):
            start, end = self.determineQueryPeriod(symbol, interval)
            queries.append(Query(symbol, interval, start, end))

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
        self.stockDataInterface.load(interval, symbol, numLastRows=1)
        if self.stockDataInterface.peek():
            lastHistoryRow = self.stockDataInterface.peek()[0]
            start = datetime.strptime(lastHistoryRow, self.dataInterface.settingsGet('{}/dateTimeFormat'.format(interval)) if interval == '1d'
                                                      else self.dataInterface.settingsGet('{}/dateTimeFormat'.format(interval)))

        return start.date(), end.date()
