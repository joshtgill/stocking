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
                query = Query(queryData, i)
                queries.append(query)

        return queries


    def verifyQueries(self):
        i = 0
        while i < len(self.queries):
            query = self.queries[i]
            stockData = self.dataService.loadStockData(query.symbol, query.interval)
            if stockData is not None and stockData.interval == query.interval:
                query.start = stockData.end
                if query.start >= query.end:
                    del self.queries[i]
                    i -= 1
            i += 1


    def initiateQueries(self):
        for query in self.queries:
            stockData = self.queryInterface.performQuery(query)

            queryDataStr = ''
            for history in stockData.history:
                queryDataStr += str(history) + '\n'
            queryDataStr = queryDataStr[:-1]

            filePath = '{}/{}_{}_to_{}_{}.txt'.format(self.dataService.configGet('stockDataDirectory'),
                                                      stockData.symbol,
                                                      stockData.start.strftime(self.dataService.configGet('dateFormat')),
                                                      stockData.end.strftime(self.dataService.configGet('dateFormat')),
                                                      stockData.interval)
            self.dataService.write(filePath, queryDataStr)
