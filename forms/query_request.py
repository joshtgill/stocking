from datetime import datetime


class QueryRequest:

    def __init__(self, config, symbolIndex = 0):
        self.deserialize(config, symbolIndex)


    def deserialize(self, config, symbolIndex):
        self.symbol = config.get('symbols')[symbolIndex]
        self.start = datetime.strptime(config.get('start'), '%Y-%m-%d')
        self.end = datetime.strptime(config.get('end'), '%Y-%m-%d')
        self.interval = config.get('interval')
