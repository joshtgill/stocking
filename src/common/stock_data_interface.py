from common.database_interface import DatabaseInterface


class StockDataInterface:

    def __init__(self, databasePathDir):
        self.databaseDir = self.initDatabases(databasePathDir)


    def initDatabases(self, databasePathDir):
        databaseDir = {}
        for key, value in databasePathDir.items():
            databaseDir.update({key: DatabaseInterface(value)})

        return databaseDir


    def save(self, stock):
        self.databaseDir.get(stock.interval).insert(stock.symbol, stock.history)


    def load(self, interval, symbol, start='', end='', numLastRows=0):
        database = self.databaseDir.get(interval)

        if start and end and not numLastRows:
            return database.selectPeriod(symbol, start, end)
        elif not start and not end and numLastRows:
            return database.selectLastRows(symbol, numLastRows)
        elif not start and not end and not numLastRows:
            return database.selectAll(symbol)
        else:
            return []
