from datetime import datetime, timedelta


class Query:

    def __init__(self, queryData, symbolIndex = 0):
        self.deserialize(queryData, symbolIndex)


    def deserialize(self, queryData, symbolIndex):
        self.symbol = queryData.get('symbols')[symbolIndex]
        self.start = datetime.strptime(queryData.get('start'), '%Y-%m-%d') + timedelta(hours=9, minutes=30)
        self.end = datetime.strptime(queryData.get('end'), '%Y-%m-%d') + timedelta(hours=16, minutes=00)
        self.interval = queryData.get('interval')
