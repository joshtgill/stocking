from common.data_interface import DataInterface


class StockDataInterface(DataInterface):

    def __init__(self, interval):
        super().__init__('data/stocks_{}.db'.format(interval))


    def __del__(self):
        self.database.close()


    def save(self, stock):
        self.insert(stock.symbol, stock.history)


    def load(self, symbol, start='', end=''):
        return self.select(symbol, start, end)
