from forms.query_request import QueryRequest
from interfaces.stock_data_interface import StockDataInterface
from services.file_service import FileService


class QueryService:

    def __init__(self, configInterface, queryInterface):
        self.configInterface = configInterface
        self.queryInterface = queryInterface

        self.queryRequests = self.buildRequests()
        self.verifyRequests()


    def buildRequests(self):
        queryRequests = []
        for queryData in self.configInterface.get('queries'):
            for i in range(len(queryData.get('symbols'))):
                queryRequest = QueryRequest(queryData, i)
                queryRequests.append(queryRequest)

        return queryRequests


    def verifyRequests(self):
        deleteIndicies = []
        for i in range(len(self.queryRequests)):
            queryRequest = self.queryRequests[i]
            stockDataInterface = StockDataInterface(self.configInterface, queryRequest.symbol)
            if stockDataInterface.stockData is not None and stockDataInterface.stockData.interval == queryRequest.interval:
                queryRequest.start = stockDataInterface.stockData.end
                if queryRequest.start == queryRequest.end or queryRequest.start > queryRequest.end:
                    deleteIndicies.append(i)

        deleteIndicies.reverse()
        for i in deleteIndicies:
            del self.queryRequests[i]


    def makeQueries(self):
        for queryRequest in self.queryRequests:
            stockData = self.queryInterface.query(queryRequest)

            queryDataStr = ''
            for i in range(len(stockData.data[0])):
                queryRow = []
                for queryCol in stockData.data:
                    queryRow.append(queryCol[i])
                queryDataStr += str(queryRow) + '\n'

            fileService = FileService('{}/{}_{}_to_{}_{}.txt'.format(self.configInterface.get('stockDataDirectory'),
                                                                     stockData.symbol,
                                                                     stockData.start.strftime(self.configInterface.get('dateFormat')),
                                                                     stockData.end.strftime(self.configInterface.get('dateFormat')),
                                                                     stockData.interval))
            fileService.write(queryDataStr)
