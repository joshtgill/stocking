from interfaces.query_interface import QueryInterface
from forms.query import Query
from interfaces.stock_data_interface import StockDataInterface
from services.file_service import FileService


class QueryService:

    def __init__(self, configInterface, fileService):
        self.configInterface = configInterface
        self.fileService = fileService
        self.queryInterface = QueryInterface(self.configInterface)

        self.queries = self.buildQueries()
        self.verifyQueries()


    def buildQueries(self):
        queries = []
        for queryData in self.configInterface.get('queries'):
            for i in range(len(queryData.get('symbols'))):
                query = Query(queryData, i)
                queries.append(query)

        return queries


    def verifyQueries(self):
        i = 0
        while i < len(self.queries):
            query = self.queries[i]
            stockDataInterface = StockDataInterface(self.configInterface, self.fileService, query.symbol)
            if stockDataInterface.data is not None and stockDataInterface.data.interval == query.interval:
                query.start = stockDataInterface.data.end
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

            filePath = '{}/{}_{}_to_{}_{}.txt'.format(self.configInterface.get('stockDataDirectory'),
                                                      stockData.symbol,
                                                      stockData.start.strftime(self.configInterface.get('dateFormat')),
                                                      stockData.end.strftime(self.configInterface.get('dateFormat')),
                                                      stockData.interval)
            self.fileService.write(filePath, queryDataStr)
