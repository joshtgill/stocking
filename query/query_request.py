class QueryRequest:

    def __init__(self):
        self.symbol = ''
        self.start = ''
        self.end = ''
        self.interval = ''


    def deserialize(self, data):
        self.symbol = data.get('symbol')
        self.start = data.get('start')
        self.end = data.get('end')
        self.interval = data.get('interval')
