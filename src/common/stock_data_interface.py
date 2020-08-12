from common.database_interface import DatabaseInterface


class StockDataInterface:

    def __init__(self, databasePathDir):
        self.databaseDir = self.initDatabases(databasePathDir)
        self.data = []
        self.dataIndex = 0


    def initDatabases(self, databasePathDir):
        databaseDir = {}
        for key, value in databasePathDir.items():
            databaseDir.update({key: DatabaseInterface(value)})

        return databaseDir


    def save(self, stock):
        self.databaseDir.get(stock.interval).insert(stock.symbol, stock.history)


    def load(self, interval, symbol, start='', end='', numLastRows=0):
        self.data = []
        self.dataIndex = 0

        database = self.databaseDir.get(interval)

        if start and not end and not numLastRows:
            self.data = database.selectPeriod(symbol, start, start)
        elif start and end and not numLastRows:
            self.data = database.selectPeriod(symbol, start, end)
        elif not start and not end and numLastRows:
            self.data = database.selectLastRows(symbol, numLastRows)
        elif not start and not end and not numLastRows:
            self.data = database.selectAll(symbol)


    def size(self):
        return len(self.data)


    def peek(self):
        try:
            return self.data[self.dataIndex]
        except IndexError:
            return None


    def next(self):
        self.dataIndex += 1

        return self.peek()


    def reset(self):
        self.dataIndex = 0
