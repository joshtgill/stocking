from common.database_interface import DatabaseInterface


class StockDataInterface:

    def __init__(self, databasePathDir):
        self.databaseDir = self.initDatabases(databasePathDir)
        self.data = []
        self.reset(True)


    def initDatabases(self, databasePathDir):
        databaseDir = {}
        for key, value in databasePathDir.items():
            databaseDir.update({key: DatabaseInterface(value)})

        return databaseDir


    def save(self, stock):
        self.databaseDir.get(stock.interval).insert(stock.symbol, stock.history)


    def load(self, interval, symbol, start='', end='', numLastRows=0):
        self.reset(True)

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


    def all(self, count=1, index=-1):
        data = []
        while self.next(count):
            if index == -1:
                data.append(self.peek())
            else:
                data.append(self.peek()[index])

        return data


    def next(self, count=1):
        self.dataIndex += 1 if self.dataIndex == -1 else count

        return self.peek()


    def end(self):
        self.dataIndex = len(self.data) - 1

        return self.peek()


    def peek(self):
        try:
            return self.data[self.dataIndex]
        except IndexError:
            return None


    def reset(self, hard=False):
        self.dataIndex = -1

        if hard:
            self.data = []
