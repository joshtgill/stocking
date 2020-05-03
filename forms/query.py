from datetime import datetime


class Query:

    def __init__(self, dataService, queryData, symbolIndex = 0):
        self.dataService = dataService

        self.deserialize(queryData, symbolIndex)


    def deserialize(self, queryData, symbolIndex):
        self.symbol = queryData.get('symbols')[symbolIndex]
        self.start = datetime.strptime(queryData.get('start'), '{} {}'.format(self.dataService.configGet('dateFormat'), self.dataService.configGet('timeFormat')))
        self.end = datetime.strptime(queryData.get('end'), '{} {}'.format(self.dataService.configGet('dateFormat'), self.dataService.configGet('timeFormat')))
        self.interval = queryData.get('interval')
