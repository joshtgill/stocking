from common.database_interface import DatabaseInterface


class StockHistoryInterface:

    def __init__(self, databasePathDir):
        self.databaseInterfaceDir = self.initDatabases(databasePathDir)
        self.history = []
        self.historyIndex = -1
        self.reset(True)


    def initDatabases(self, databasePathDir):
        databaseInterfaceDir = {}
        for key, value in databasePathDir.items():
            databaseInterfaceDir.update({key: DatabaseInterface(value)})

        return databaseInterfaceDir


    def save(self, stock):
        databaseInterface = self.databaseInterfaceDir.get(stock.interval)

        if not databaseInterface.tableExists(stock.symbol):
            databaseInterface.createTable(stock.symbol, '(timestamp, open, high, low, close, UNIQUE(timestamp))')

        databaseInterface.insert(stock.symbol, '(timestamp, open, high, low, close)', stock.history)


    def load(self, interval, symbol, start='', end='', numLastRows=0):
        self.reset(True)

        databaseInterface = self.databaseInterfaceDir.get(interval)

        if start and not end and not numLastRows:
            self.history = databaseInterface.selectPeriod(symbol, start, start)
        elif start and end and not numLastRows:
            self.history = databaseInterface.selectPeriod(symbol, start, end)
        elif not start and not end and numLastRows:
            self.history = databaseInterface.selectLastRows(symbol, numLastRows)
        elif not start and not end and not numLastRows:
            self.history = databaseInterface.selectAll(symbol)


    def size(self):
        return len(self.history)


    def all(self, count=1, index=-1):
        history = []
        while self.next(count):
            if index == -1:
                history.append(self.peek())
            else:
                history.append(self.peek()[index])

        return history


    def hasNext(self):
        return self.historyIndex < len(self.history) - 1


    def next(self, count=1):
        self.historyIndex += 1 if self.historyIndex == -1 else count

        try:
            return self.history[self.historyIndex]
        except IndexError:
            return None


    def end(self):
        self.historyIndex = len(self.history) - 1

        return self.peek()


    def reset(self, hard=False):
        self.historyIndex = -1

        if hard:
            self.history = []
