from datetime import datetime


class QueryForm:

    def __init__(self, config):
        self.deserialize(config)


    def deserialize(self, config):
        self.symbol = config.get('symbols')[0]
        self.start = datetime.strptime(config.get('start'), '%Y-%m-%d')
        self.end = datetime.strptime(config.get('end'), '%Y-%m-%d')
        self.interval = config.get('interval')
