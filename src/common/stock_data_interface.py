from common.data_interface import DataInterface


class StockDataInterface(DataInterface):

    def __init__(self, interval):
        super().__init__('data/stocks_{}.db'.format(interval))

        self.header = '(timestamp, open, high, low, close)'


    def __del__(self):
        self.database.close()


    def save(self, stock):
        self.insert(stock.symbol, self.header, stock.history)


    def load(self, symbol, start='', end=''):
        return self.select(symbol, start, end)
