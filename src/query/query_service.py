from common.base_service import BaseService
from datetime import datetime, timedelta
from query.query_interface import QueryInterface


class QueryService(BaseService):

    def __init__(self, dataInterface, logInterface, stockSymbolsInterface, stockHistoryInterface, stockSplitsInterface):
        super().__init__('QUERY', dataInterface, logInterface, stockSymbolsInterface, stockHistoryInterface)
        self.stockSplitsInterface = stockSplitsInterface


    def go(self, *args):
        queryInterface = QueryInterface(self.dataInterface, self.logInterface)

        if not self.stockSymbolsInterface.upToDate:
            self.logInterface.log('Querying capital, global, and global select NASDAQ symbols')
            capital_symbols, global_symbols, global_select_symbols = queryInterface.performSymbolsQuery()
            self.stockSymbolsInterface.saveAll(capital_symbols, global_symbols, global_select_symbols)

        interval = self.dataInterface.configGet('interval')
        symbols = self.translateConfigVariable(self.dataInterface.configGet('symbols'))

        symbolsText = (', '.join(symbols) if isinstance(self.dataInterface.configGet('symbols'), list)
                                          else self.dataInterface.configGet('symbols'))
        self.logInterface.log('Querying {} history for {} symbol(s)'.format(interval, symbolsText))
        for symbol in symbols:
            start, end = self.determineQueryPeriod(symbol, interval)
            stock = queryInterface.performStockQuery(interval, symbol, start, end)
            self.stockHistoryInterface.save(stock.interval, stock.symbol, stock.history)
            self.stockSplitsInterface.save(stock.symbol, stock.splits)


    def buildQueries(self, interval, symbols):
        queries = []
        for symbol in symbols:
            start, end = self.determineQueryPeriod(symbol, interval)
            queries.append(Query(symbol, interval, start, end))

        return queries


    def determineQueryPeriod(self, symbol, interval):
        # Record current datetime
        now = datetime.now()

        # Default query start and end
        start = datetime(1970, 1, 1)
        end = now + timedelta(days=1)
        if interval == 'minute':
            start = now - timedelta(days=29)

        # If stock history already exists, determine query start
        self.stockHistoryInterface.load(interval, symbol, numLastRows=1)
        if self.stockHistoryInterface.hasNext():
            lastHistoryRow = self.stockHistoryInterface.next()[0]
            start = datetime.strptime(lastHistoryRow, self.dataInterface.settingsGet('{}/dateTimeFormat'.format(interval)) if interval == 'day'
                                                      else self.dataInterface.settingsGet('{}/dateTimeFormat'.format(interval)))

        return start.date(), end.date()
