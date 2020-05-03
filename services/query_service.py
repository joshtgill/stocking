from forms.query import Query


class QueryService:

    def __init__(self, dataService, queryInterface):
        self.dataService = dataService
        self.queryInterface = queryInterface

        self.queries = self.buildQueries()
        self.verifyQueries()


    def buildQueries(self):
        queries = []
        for queryData in self.dataService.configGet('queries'):
            for i in range(len(queryData.get('symbols'))):
                query = Query(self.dataService, queryData, i)
                queries.append(query)

        return queries


    def verifyQueries(self):
        i = 0
        while i < len(self.queries):
            query = self.queries[i]
            stockData = self.dataService.loadStockData(query.symbol, query.interval)
            if stockData is not None:
                if stockData.end >= query.end:
                    del self.queries[i]
                    continue
                if stockData.end >= query.start:
                    query.start = stockData.end
            i += 1


    def initiateQueries(self):
        for query in self.queries:
            stockData = self.queryInterface.performQuery(query)

            queryDataStr = ''
            for history in stockData.history:
                queryDataStr += str(history) + '\n'
            queryDataStr = queryDataStr[:-1] + '\n'

            filePath = '{}/{}_{}.txt'.format(self.dataService.configGet('stockDataDirectory'),
                                                      stockData.symbol,
                                                      stockData.interval)
            self.dataService.write(filePath, queryDataStr)
