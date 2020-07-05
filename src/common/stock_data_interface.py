from common.data_interface import DataInterface


class StockDataInterface(DataInterface):

    def __init__(self, dataPath):
        super().__init__(dataPath)


    def __del__(self):
        self.database.close()


    def save(self, stock):
        self.insert(stock.symbol, stock.history)


    def load(self, symbol, start='', end='', numLastRows=0):
        if start and end and not numLastRows:
            return self.selectPeriod(symbol, start, end)
        elif not start and not end and numLastRows:
            return self.selectLastRows(symbol, numLastRows)
        elif not start and not end and not numLastRows:
            return self.selectAll(symbol)
        else:
            return []
