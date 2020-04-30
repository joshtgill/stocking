from datetime import datetime


class QueryRequest:

    def __init__(self):
        self.symbols = None
        self.symbol = None
        self.end = None
        self.interval = None


    def deserialize(self, config):
        self.symbols = config.get('symbols')
        self.start = datetime.strptime(config.get('start'), '%Y-%m-%d')
        self.end = datetime.strptime(config.get('end'), '%Y-%m-%d')
        self.interval = config.get('interval')
