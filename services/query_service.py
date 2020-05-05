from forms.query import Query
import datetime


class QueryService:

    def __init__(self, dataService, queryInterface):
        self.dataService = dataService
        self.queryInterface = queryInterface

        self.queries = self.buildQueries()
        self.verifyQueries()


    def buildQueries(self):
        queries = []
        for queryData in self.dataService.config.get('queries'):
            for i in range(len(queryData.get('symbols'))):
                query = Query(queryData, i)
                queries.append(query)

        return queries


    def verifyQueries(self):
        i = 0
        while i < len(self.queries):
            query = self.queries[i]
            stockData = self.dataService.loadStockData(query.symbol, query.interval)
            if stockData:
                query.start = (stockData.end + datetime.timedelta(minutes=1)).replace(second=0)
                if query.start >= query.end:  # Stored stock data is just as or more recent than query
                    del self.queries[i]
                    i -= 1
            i += 1


    def initiateQueries(self):
        for query in self.queries:
            stockData = self.queryInterface.performQuery(query)

            self.dataService.saveStockData(stockData)
