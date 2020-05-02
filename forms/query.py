from datetime import datetime


class Query:

    def __init__(self, queryData, symbolIndex = 0):
        self.deserialize(queryData, symbolIndex)


    def deserialize(self, queryData, symbolIndex):
        self.symbol = queryData.get('symbols')[symbolIndex]
        self.start = datetime.strptime(queryData.get('start'), '%Y-%m-%d')
        self.end = datetime.strptime(queryData.get('end'), '%Y-%m-%d')
        self.interval = queryData.get('interval')
