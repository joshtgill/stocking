from common.database_interface import DatabaseInterface


class StockSplitsInterface:

    def __init__(self, databaseFilePath):
        self.databaseInterface = DatabaseInterface(databaseFilePath)


    def save(self, symbol, splits):
        if not self.databaseInterface.tableExists(symbol):
            self.databaseInterface.createTable(symbol, '(timestamp, factor, UNIQUE(timestamp))')

        self.databaseInterface.insert(symbol, '(timestamp, factor)', splits)


    def load(self, symbol):
        return [split for split in self.databaseInterface.selectAll(symbol)]
