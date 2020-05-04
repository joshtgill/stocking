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
        for i in range(len(self.queries)):
            query = self.queries[i]
            stockData = self.dataService.readStockData(query.symbol, query.interval)
            if stockData is not None:
                if stockData.end >= query.end:
                    del self.queries[i]
                    continue
                elif stockData.end >= query.start:
                    query.start = stockData.end
                    query.start = query.start.replace(minute=query.start.minute + 1, second=0)


    def initiateQueries(self):
        for query in self.queries:
            stockData = self.queryInterface.performQuery(query)

            self.dataService.writeStockData(stockData)
